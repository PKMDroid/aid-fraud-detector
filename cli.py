#!/usr/bin/env python3

from lib.helpers import (
    create_project,
    create_transaction,
    list_projects,
    view_project_details,
    list_fraud_flags,
    view_flagged_projects,
    generate_summary_report,
    clear_all_fraud_flags
)
from lib.fraud_checker import run_all_fraud_checks
from lib.db import engine
from lib.models import Base


def initialize_database():
    Base.metadata.create_all(engine)


def display_menu():
    print("\n   AID FRAUD DETECTION SYSTEM " )
    
    print("\nProject Management:")
    print("  1. Add New Project")
    print("  2. View All Projects")
    print("  3. View Project Details")
    
    print("\nTransaction Management:")
    print("  4. Add Transaction to Project")
    
    print("\nFraud Detection:")
    print("  5. Run Fraud Detection Scan")
    print("  6. View All Fraud Flags")
    print("  7. View Flagged Projects Only")
    print("  8. Clear All Fraud Flags")
    
    print("\nAnalytics:")
    print("  9. Generate Summary Report")
    
    print("\n  0. Exit")


def get_valid_float(prompt):
    while True:
        try:
            value = float(input(prompt))
            return value
        except ValueError:
            print("Please enter a valid number.")


def get_valid_int(prompt):
    while True:
        try:
            value = int(input(prompt))
            return value
        except ValueError:
            print("Please enter a valid number.")


def handle_add_project():
    print("\nAdd New Project")
    name = input("Project name: ").strip()
    
    if not name:
        print("Project name cannot be empty!")
        return
    
    budget = get_valid_float("Budget amount ($): ")
    
    if budget <= 0:
        print("Budget must be greater than 0!")
        return
    
    project = create_project(name, budget)
    print(f"\nProject '{project.name}' created successfully (ID: {project.id})")


def handle_add_transaction():
    print("\nAdd Transaction")
    
    projects = list_projects()
    
    if not projects:
        print("\nNo projects available. Create a project first.")
        return
    
    project_id = get_valid_int("\nEnter Project ID: ")
    amount = get_valid_float("Transaction amount ($): ")
    description = input("Description: ").strip()
    
    if not description:
        description = "No description provided"
    
    transaction = create_transaction(project_id, amount, description)
    
    if transaction:
        print(f"\nTransaction of ${amount:,.2f} added successfully")


def handle_view_project_details():
    print("\nView Project Details")
    
    list_projects()
    
    project_id = get_valid_int("\nEnter Project ID: ")
    view_project_details(project_id)


def main():
    initialize_database()
    
    print("\nWelcome to the Aid Fraud Detection System")
    
    while True:
        display_menu()
        choice = input("\nEnter your choice: ").strip()
        
        if choice == "1":
            handle_add_project()
        
        elif choice == "2":
            print("\nAll Projects")
            list_projects()
        
        elif choice == "3":
            handle_view_project_details()
        
        elif choice == "4":
            handle_add_transaction()
        
        elif choice == "5":
            run_all_fraud_checks()
        
        elif choice == "6":
            print("\nAll Fraud Flags")
            list_fraud_flags()
        
        elif choice == "7":
            print("\nFlagged Projects")
            view_flagged_projects()

        elif choice == "8":
            print("\nClearing all fraud flags...")
            count = clear_all_fraud_flags()
            print(f"Cleared {count} fraud flag(s)")    
        
        elif choice == "9":
            generate_summary_report()
        
        elif choice == "0":
            print("\nExiting system. Goodbye!")
            break
        
        else:
            print("\nInvalid choice. Please try again.")
        
        input("\nPress Enter to continue...")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nExiting. Goodbye!")
    except Exception as e:
        print(f"\nError: {e}")