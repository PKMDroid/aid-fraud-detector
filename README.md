# Aid Fraud Detection System

A command-line application that helps NGOs and aid organizations detect fraudulent spending patterns in humanitarian projects.

## Problem Statement

Billions of dollars in humanitarian aid are lost annually to fraud, corruption, and mismanagement. This system provides automated fraud detection to promote transparency and accountability in aid distribution.

## Features

- **Project Tracking**: Monitor aid projects with budgets and spending
- **Transaction Logging**: Record all financial transactions with descriptions
- **Automated Fraud Detection**: 
  - Budget overspend detection
  - Anomalous transaction identification
  - Data integrity checks
- **Risk Reporting**: View flagged projects and fraud alerts
- **Analytics Dashboard**: Generate summary statistics across all projects

## Technology Stack

- **Python 3.8+**
- **SQLAlchemy ORM**: Database management with 3 related tables
- **SQLite**: Lightweight database
- **Pipenv**: Virtual environment management

## Database Schema
```
Projects (1) ──< (many) Transactions
Projects (1) ──< (many) Fraud_Flags
```

### Tables:
1. **Projects**: Aid projects with budgets
2. **Transactions**: Financial transactions per project
3. **Fraud_Flags**: Automatically detected fraud indicators

## Installation
```bash
# Clone or download the project
cd aid-fraud-detector

# Install dependencies
pipenv install

# Activate virtual environment
pipenv shell

# Seed database with demo data
python seed.py

# Run the application
python cli.py
```

## Usage

### Main Menu Options:

1. **Add New Project** - Create aid project with budget
2. **View All Projects** - List all projects with spending summary
3. **View Project Details** - See transactions and fraud flags for specific project
4. **Add Transaction** - Log spending against a project
5. **Run Fraud Detection** - Analyze all projects for suspicious patterns
6. **View Fraud Flags** - See all detected fraud cases
7. **View Flagged Projects** - Filter projects with issues
8. **Generate Summary** - Statistical overview of all projects

### Example Workflow:
```bash
# 1. Seed demo data
python seed.py

# 2. Run application
python cli.py

# 3. In the menu:
#    - Select option 2 to view projects
#    - Select option 5 to run fraud detection
#    - Select option 6 to see detected fraud
```

## Fraud Detection Algorithms

### 1. Budget Overspend Detection (HIGH severity)
- Flags projects where total spending exceeds allocated budget
- Calculates overspend amount

### 2. Anomalous Transaction Detection (MEDIUM severity)
- Identifies transactions 3x above project average
- Potential indicator of embezzlement or invoice fraud

### 3. Data Integrity Check (HIGH severity)
- Detects negative values
- Flags missing or invalid data

## Project Structure
```
humanitarian-aid-detector/
├── lib/
│   ├── __init__.py
│   ├── db.py                 # Database configuration
│   ├── models.py             # SQLAlchemy models
│   ├── helpers.py            # CRUD operations
│   └── fraud_checker.py      # Fraud detection algorithms
├── cli.py                    # Main CLI application
├── seed.py                   # Demo data generator
├── Pipfile                   # Dependencies
└── README.md
```

## Requirements Met

 CLI application solving real-world problem  
 SQLAlchemy ORM with 3+ related tables  
 Pipenv virtual environment  
 Proper package structure  
 Use of lists, dicts, and tuples  

## Future Enhancements

- Beneficiary tracking (prevent ghost recipients)
- Organization trust scoring
- Time-based anomaly detection
- Export reports to CSV/PDF
- Web dashboard interface

## Author

Created as a Phase 3 CLI+ORM project demonstrating:
- Database design and relationships
- Object-oriented programming
- Data analysis and pattern detection
- Real-world problem solving

## License

Educational project - MIT License