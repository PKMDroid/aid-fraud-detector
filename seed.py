#!/usr/bin/env python3

from lib.db import session, engine
from lib.models import Base, Project, Transaction


def clear_database():
    print("Clearing old data...")
    session.query(Transaction).delete()
    session.query(Project).delete()
    session.commit()


def create_demo_data():
    print("Adding demo projects and transactions...")
    
    projects_data = [
        ("Water Wells in Rural Kenya", 50000),
        ("School Supplies for Uganda", 20000),
        ("Medical Clinic in Ghana", 100000),
        ("Food Distribution Somalia", 75000),
        ("Education Program Ethiopia", 30000),
    ]
    
    projects = []
    for name, budget in projects_data:
        project = Project(name=name, budget=budget, status="active")
        session.add(project)
        projects.append(project)
    
    session.commit()
    print(f"Added {len(projects)} projects")
    
    transactions = [
        Transaction(project_id=1, amount=15000, date="2024-01-15", description="Well drilling equipment"),
        Transaction(project_id=1, amount=20000, date="2024-02-10", description="Labor and installation costs"),
        Transaction(project_id=1, amount=18000, date="2024-03-05", description="Materials and supplies"),
        
        Transaction(project_id=2, amount=5000, date="2024-01-20", description="Textbooks purchase"),
        Transaction(project_id=2, amount=4500, date="2024-02-15", description="School supplies"),
        Transaction(project_id=2, amount=3000, date="2024-03-10", description="Uniforms"),
        
        Transaction(project_id=3, amount=10000, date="2024-01-10", description="Medical equipment"),
        Transaction(project_id=3, amount=8000, date="2024-01-25", description="Pharmaceuticals"),
        Transaction(project_id=3, amount=12000, date="2024-02-05", description="Construction materials"),
        Transaction(project_id=3, amount=45000, date="2024-02-20", description="Consulting fees"),
        Transaction(project_id=3, amount=9000, date="2024-03-01", description="Medical supplies"),
        
        Transaction(project_id=4, amount=5000, date="2024-01-05", description="Rice procurement"),
        Transaction(project_id=4, amount=6000, date="2024-01-20", description="Beans and grains"),
        Transaction(project_id=4, amount=4500, date="2024-02-10", description="Cooking oil"),
        Transaction(project_id=4, amount=5500, date="2024-02-25", description="Distribution costs"),
        Transaction(project_id=4, amount=7000, date="2024-03-15", description="Emergency rations"),
        
        Transaction(project_id=5, amount=8000, date="2024-01-12", description="Teacher training"),
        Transaction(project_id=5, amount=25000, date="2024-01-30", description="Infrastructure"),
        Transaction(project_id=5, amount=6000, date="2024-02-18", description="Learning materials"),
    ]
    
    session.add_all(transactions)
    session.commit()
    print(f"Added {len(transactions)} transactions")
    
    print("\nDemo data includes some projects with fraudulent patterns.")
    print("Run the CLI and use option 5 to detect them.")


def main():
    print("\nSetting up demo database...")
    
    Base.metadata.create_all(engine)
    clear_database()
    create_demo_data()
    
    print("\nDone! Run 'python cli.py' to start the application.\n")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\nError: {e}")
        session.rollback()