from sqlalchemy.orm import Session
from db import SessionLocal
from models import Organization, Employee, OrganizationColumnConfig
from datetime import date
import json

def seed_organizations(db: Session):
    """Seed organizations table with sample data"""
    organizations = [
        Organization(
            name="Tech Corp",
            description="Leading technology company specializing in software development"
        ),
        Organization(
            name="Marketing Inc",
            description="Full-service digital marketing agency"
        ),
        Organization(
            name="Finance Ltd",
            description="Financial services and consulting firm"
        ),
    ]
    
    for org in organizations:
        existing = db.query(Organization).filter(Organization.name == org.name).first()
        if not existing:
            db.add(org)
    
    db.commit()

def seed_employees(db: Session):
    """Seed employees table with sample data"""
    # Get organization IDs
    tech_corp = db.query(Organization).filter(Organization.name == "Tech Corp").first()
    marketing_inc = db.query(Organization).filter(Organization.name == "Marketing Inc").first()
    finance_ltd = db.query(Organization).filter(Organization.name == "Finance Ltd").first()
    
    if not all([tech_corp, marketing_inc, finance_ltd]):
        print("Organizations not found. Please seed organizations first.")
        return
    
    employees = [
        # Tech Corp employees
        Employee(
            name="John Doe",
            email="john.doe@techcorp.com",
            phone="+1-555-0101",
            department="Engineering",
            position="Software Engineer",
            location="New York",
            hire_date=date(2022, 1, 15),
            salary=75000.0,
            organization_id=tech_corp.id
        ),
        Employee(
            name="Jane Smith",
            email="jane.smith@techcorp.com",
            phone="+1-555-0102",
            department="Engineering",
            position="Senior Software Engineer",
            location="San Francisco",
            hire_date=date(2021, 3, 10),
            salary=95000.0,
            organization_id=tech_corp.id
        ),
        Employee(
            name="Bob Johnson",
            email="bob.johnson@techcorp.com",
            phone="+1-555-0103",
            department="Product",
            position="Product Manager",
            location="Seattle",
            hire_date=date(2022, 6, 20),
            salary=85000.0,
            organization_id=tech_corp.id
        ),
        Employee(
            name="Frank Garcia",
            email="frank.garcia@techcorp.com",
            phone="+1-555-0104",
            department="Engineering",
            position="DevOps Engineer",
            location="Austin",
            hire_date=date(2023, 2, 28),
            salary=80000.0,
            organization_id=tech_corp.id
        ),
        Employee(
            name="Sarah Wilson",
            email="sarah.wilson@techcorp.com",
            phone="+1-555-0105",
            department="Engineering",
            position="Frontend Developer",
            location="Denver",
            hire_date=date(2023, 5, 15),
            salary=70000.0,
            organization_id=tech_corp.id
        ),
        
        # Marketing Inc employees
        Employee(
            name="Alice Brown",
            email="alice.brown@marketing.com",
            phone="+1-555-0201",
            department="Marketing",
            position="Marketing Manager",
            location="Chicago",
            hire_date=date(2021, 9, 1),
            salary=70000.0,
            organization_id=marketing_inc.id
        ),
        Employee(
            name="Charlie Wilson",
            email="charlie.wilson@marketing.com",
            phone="+1-555-0202",
            department="Marketing",
            position="Content Creator",
            location="Los Angeles",
            hire_date=date(2022, 11, 15),
            salary=55000.0,
            organization_id=marketing_inc.id
        ),
        Employee(
            name="Grace Martinez",
            email="grace.martinez@marketing.com",
            phone="+1-555-0203",
            department="Marketing",
            position="Social Media Manager",
            location="Miami",
            hire_date=date(2023, 1, 10),
            salary=58000.0,
            organization_id=marketing_inc.id
        ),
        Employee(
            name="David Lee",
            email="david.lee@marketing.com",
            phone="+1-555-0204",
            department="Creative",
            position="Graphic Designer",
            location="Portland",
            hire_date=date(2022, 8, 5),
            salary=62000.0,
            organization_id=marketing_inc.id
        ),
        
        # Finance Ltd employees
        Employee(
            name="Diana Davis",
            email="diana.davis@finance.com",
            phone="+1-555-0301",
            department="Finance",
            position="Financial Analyst",
            location="Boston",
            hire_date=date(2021, 12, 1),
            salary=65000.0,
            organization_id=finance_ltd.id
        ),
        Employee(
            name="Eve Miller",
            email="eve.miller@finance.com",
            phone="+1-555-0302",
            department="Finance",
            position="Senior Accountant",
            location="Denver",
            hire_date=date(2020, 8, 15),
            salary=72000.0,
            organization_id=finance_ltd.id
        ),
        Employee(
            name="Henry Lee",
            email="henry.lee@finance.com",
            phone="+1-555-0303",
            department="Finance",
            position="Controller",
            location="Phoenix",
            hire_date=date(2019, 5, 20),
            salary=90000.0,
            organization_id=finance_ltd.id
        ),
        Employee(
            name="Isabella Rodriguez",
            email="isabella.rodriguez@finance.com",
            phone="+1-555-0304",
            department="Accounting",
            position="Tax Specialist",
            location="Houston",
            hire_date=date(2022, 3, 12),
            salary=68000.0,
            organization_id=finance_ltd.id
        ),
    ]
    
    for employee in employees:
        existing = db.query(Employee).filter(Employee.email == employee.email).first()
        if not existing:
            db.add(employee)
    
    db.commit()

def seed_column_configs(db: Session):
    """Seed organization column configurations"""
    # Get organization IDs
    tech_corp = db.query(Organization).filter(Organization.name == "Tech Corp").first()
    marketing_inc = db.query(Organization).filter(Organization.name == "Marketing Inc").first()
    finance_ltd = db.query(Organization).filter(Organization.name == "Finance Ltd").first()
    
    if not all([tech_corp, marketing_inc, finance_ltd]):
        print("Organizations not found. Please seed organizations first.")
        return
    
    # Tech Corp configuration - standard columns
    tech_corp_columns = [
        ("name", 1, 1),
        ("email", 2, 1),
        ("department", 3, 1),
        ("position", 4, 1),
        ("location", 5, 1),
    ]
    
    # Marketing Inc configuration - minimal columns
    marketing_inc_columns = [
        ("name", 1, 1),
        ("department", 2, 1),
        ("location", 3, 1),
        ("position", 4, 1),
    ]
    
    # Finance Ltd configuration - detailed columns
    finance_ltd_columns = [
        ("name", 1, 1),
        ("email", 2, 1),
        ("phone", 3, 1),
        ("department", 4, 1),
        ("position", 5, 1),
        ("location", 6, 1),
        ("hire_date", 7, 1),
    ]
    
    configurations = [
        (tech_corp.id, tech_corp_columns),
        (marketing_inc.id, marketing_inc_columns),
        (finance_ltd.id, finance_ltd_columns),
    ]
    
    for org_id, columns in configurations:
        for column_name, display_order, is_visible in columns:
            existing = db.query(OrganizationColumnConfig).filter(
                OrganizationColumnConfig.organization_id == org_id,
                OrganizationColumnConfig.column_name == column_name
            ).first()
            
            if not existing:
                config = OrganizationColumnConfig(
                    organization_id=org_id,
                    column_name=column_name,
                    display_order=display_order,
                    is_visible=is_visible
                )
                db.add(config)
    
    db.commit()

def seed_all_data():
    """Seed all data in the correct order"""
    db = SessionLocal()
    try:
        print("Seeding organizations...")
        seed_organizations(db)
        
        print("Seeding employees...")
        seed_employees(db)
        
        print("Seeding column configurations...")
        seed_column_configs(db)
        
        print("All data seeded successfully!")
        
    except Exception as e:
        print(f"Error seeding data: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_all_data()