from lib.db import session
from lib.models import Project, FraudFlag


def check_budget_overspend():
    projects = session.query(Project).all()
    flags_created = 0
    
    for project in projects:
        total_spent = project.total_spent()
        
        if total_spent <= project.budget:
            continue
        
        overspend_amount = total_spent - project.budget
        overspend_percentage = (overspend_amount / project.budget) * 100
        
        if overspend_percentage < 2:
            continue
        
        existing = session.query(FraudFlag).filter_by(
            project_id=project.id,
            flag_type="BUDGET_OVERSPEND"
        ).first()
        
        if not existing:
            if overspend_percentage >= 20:
                severity = "HIGH"
            elif overspend_percentage >= 10:
                severity = "MEDIUM"
            else:
                severity = "LOW"
            
            flag = FraudFlag(
                project_id=project.id,
                flag_type="BUDGET_OVERSPEND",
                severity=severity,
                message=f"Spent ${total_spent:,.2f} exceeds budget ${project.budget:,.2f} by ${overspend_amount:,.2f} ({overspend_percentage:.1f}%)"
            )
            session.add(flag)
            flags_created += 1
    
    session.commit()
    return flags_created


def check_anomalous_transactions():
    projects = session.query(Project).all()
    flags_created = 0
    
    for project in projects:
        transactions = project.transactions
        
        if len(transactions) < 2:
            continue
        
        total = sum(t.amount for t in transactions)
        average = total / len(transactions)
        
        for t in transactions:
            if t.amount > average * 3:
                existing = session.query(FraudFlag).filter_by(
                    project_id=project.id,
                    flag_type="ANOMALOUS_TRANSACTION"
                ).filter(FraudFlag.message.contains(f"transaction #{t.id}")).first()
                
                if not existing:
                    flag = FraudFlag(
                        project_id=project.id,
                        flag_type="ANOMALOUS_TRANSACTION",
                        severity="MEDIUM",
                        message=f"Transaction #{t.id} of ${t.amount:,.2f} is {t.amount/average:.1f}x above average (${average:,.2f})"
                    )
                    session.add(flag)
                    flags_created += 1
    
    session.commit()
    return flags_created


def check_data_integrity():
    projects = session.query(Project).all()
    flags_created = 0
    
    for project in projects:
        issues = []
        
        if project.budget < 0:
            issues.append("Negative budget detected")
        
        negative_transactions = [t for t in project.transactions if t.amount < 0]
        if negative_transactions:
            issues.append(f"{len(negative_transactions)} transaction(s) with negative amounts")
        
        if issues:
            existing = session.query(FraudFlag).filter_by(
                project_id=project.id,
                flag_type="DATA_INTEGRITY"
            ).first()
            
            if not existing:
                flag = FraudFlag(
                    project_id=project.id,
                    flag_type="DATA_INTEGRITY",
                    severity="HIGH",
                    message=f"Data integrity issues: {', '.join(issues)}"
                )
                session.add(flag)
                flags_created += 1
    
    session.commit()
    return flags_created


def run_all_fraud_checks():
    print("\nRunning fraud detection scans...")
    
    results = {
        'budget_overspend': check_budget_overspend(),
        'anomalous_transactions': check_anomalous_transactions(),
        'data_integrity': check_data_integrity()
    }
    
    total = sum(results.values())
    
    print(f"\nScan complete!")
    print(f"  - Budget overspend flags: {results['budget_overspend']}")
    print(f"  - Anomalous transaction flags: {results['anomalous_transactions']}")
    print(f"  - Data integrity flags: {results['data_integrity']}")
    print(f"  - Total new flags: {total}")
    
    return results