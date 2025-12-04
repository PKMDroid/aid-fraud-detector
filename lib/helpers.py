from lib.db import session
from lib.models import Project, Transaction, FraudFlag
from datetime import datetime


def create_project(name, budget, status="active"):
    project = Project(name=name, budget=budget, status=status)
    session.add(project)
    session.commit()
    return project


def list_projects():
    projects = session.query(Project).all()
    
    if not projects:
        print("\nNo projects found.")
        return []
    
    print(f"\n{' ID ':<6} {'Name':<35} {'Budget':<15} {'Spent':<15} {'Remaining':<15} {'Status'}")
    print("-" * 95)
    
    for p in projects:
        spent = p.total_spent()
        remaining = p.remaining_budget()
        print(f"{p.id:<6} {p.name:<35} ${p.budget:<14,.2f} ${spent:<14,.2f} ${remaining:<14,.2f} {p.status}")
    
    return projects


def get_project_by_id(project_id):
    return session.query(Project).get(project_id)


def view_project_details(project_id):
    project = get_project_by_id(project_id)
    
    if not project:
        print(f"\nProject with ID {project_id} not found.")
        return None
    
    print(f"\nProject: {project.name}")
    print("-" * 50)
    print(f"Budget:        ${project.budget:,.2f}")
    print(f"Total Spent:   ${project.total_spent():,.2f}")
    print(f"Remaining:     ${project.remaining_budget():,.2f}")
    print(f"Status:        {project.status}")
    print(f"Fraud Flags:   {len(project.fraud_flags)}")
    
    if project.transactions:
        print(f"\nTransactions ({len(project.transactions)}):")
        print(f"{'ID':<5} {'Date':<12} {'Amount':<15} {'Description'}")
        print("-" * 70)
        for t in project.transactions:
            print(f"{t.id:<5} {t.date:<12} ${t.amount:<14,.2f} {t.description}")
    else:
        print("\nNo transactions yet.")
    
    if project.fraud_flags:
        print(f"\nFraud Flags ({len(project.fraud_flags)}):")
        for f in project.fraud_flags:
            print(f"  [{f.severity}] {f.message}")
    else:
        print("\nNo fraud flags.")
    
    return project


def create_transaction(project_id, amount, description):
    project = get_project_by_id(project_id)
    if not project:
        print(f"\nProject with ID {project_id} not found.")
        return None
    
    is_valid, msg = validate_amount(amount)
    if not is_valid:
        print(f"\nInvalid amount: {msg}")
        return None
    
    transaction = Transaction(
        project_id=project_id,
        amount=amount,
        description=description,
        date=datetime.now().strftime("%Y-%m-%d")
    )
    session.add(transaction)
    session.commit()
    return transaction


def validate_amount(amount):
    if amount < 0:
        return (False, "Amount cannot be negative")
    if amount > 10000000:
        return (False, "Amount exceeds maximum limit of $10M")
    return (True, "Valid")


def create_fraud_flag(project_id, flag_type, severity, message):
    flag = FraudFlag(
        project_id=project_id,
        flag_type=flag_type,
        severity=severity,
        message=message
    )
    session.add(flag)
    session.commit()
    return flag


def list_fraud_flags():
    flags = session.query(FraudFlag).all()
    
    if not flags:
        print("\nNo fraud flags found.")
        return []
    
    print(f"\n{'ID':<5} {'Project':<35} {'Type':<25} {'Severity':<10} {'Status'}")
    print("-" * 90)
    
    for f in flags:
        print(f"{f.id:<5} {f.project.name:<35} {f.flag_type:<25} {f.severity:<10} {f.status}")
        print(f"      {f.message}")
    
    return flags


def view_flagged_projects():
    flagged = session.query(Project).join(FraudFlag).distinct().all()
    
    if not flagged:
        print("\nNo flagged projects found.")
        return []
    
    print(f"\n{'ID':<6} {'Name':<35} {'Flags':<10} {'Severity'}")
    print("-" * 65)
    
    for p in flagged:
        severities = [f.severity for f in p.fraud_flags]
        highest = "HIGH" if "HIGH" in severities else "MEDIUM" if "MEDIUM" in severities else "LOW"
        
        print(f"{p.id:<6} {p.name:<35} {len(p.fraud_flags):<10} {highest}")
    
    return flagged

def clear_all_fraud_flags():
    "Delete all fraud flags from database"
    count = session.query(FraudFlag).count()
    session.query(FraudFlag).delete()
    session.commit()
    return count


def generate_summary_report():
    projects = session.query(Project).all()
    flags = session.query(FraudFlag).all()
    
    total_budget = sum(p.budget for p in projects)
    total_spent = sum(p.total_spent() for p in projects)
    flagged_count = len(session.query(Project).join(FraudFlag).distinct().all())
    
    summary = {
        'total_projects': len(projects),
        'active_projects': len([p for p in projects if p.status == 'active']),
        'total_budget': total_budget,
        'total_spent': total_spent,
        'total_flags': len(flags),
        'flagged_projects': flagged_count,
        'high_severity_flags': len([f for f in flags if f.severity == 'HIGH'])
    }
    
    print("\nSummary Report")
    print("-" * 50)
    
    for key, value in summary.items():
        label = key.replace('_', ' ').title()
        if 'budget' in key.lower() or 'spent' in key.lower():
            print(f"{label:<30} ${value:>15,.2f}")
        else:
            print(f"{label:<30} {value:>15}")
    
    if summary['total_projects'] > 0:
        fraud_rate = (summary['flagged_projects'] / summary['total_projects']) * 100
        print(f"{'Fraud Rate':<30} {fraud_rate:>14.1f}%")
    
    return summary