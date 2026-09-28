"""
Seed Script — Populate the database with sample student records.
Run with: python scripts/seed_data.py
"""

import os
import sys

# Add project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.database import SessionLocal, create_tables
from app.models.student import Student

SAMPLE_STUDENTS = [
    {
        "first_name": "Alice",
        "last_name": "Sharma",
        "email": "alice.sharma@university.edu",
        "age": 21,
        "grade": 9.1,
        "department": "Computer Science",
    },
    {
        "first_name": "Bob",
        "last_name": "Patel",
        "email": "bob.patel@university.edu",
        "age": 22,
        "grade": 7.8,
        "department": "Mathematics",
    },
    {
        "first_name": "Chitra",
        "last_name": "Nair",
        "email": "chitra.nair@university.edu",
        "age": 20,
        "grade": 8.5,
        "department": "Computer Science",
    },
    {
        "first_name": "David",
        "last_name": "Kumar",
        "email": "david.kumar@university.edu",
        "age": 23,
        "grade": 6.9,
        "department": "Physics",
    },
    {
        "first_name": "Esha",
        "last_name": "Mehta",
        "email": "esha.mehta@university.edu",
        "age": 21,
        "grade": 9.8,
        "department": "Data Science",
    },
    {
        "first_name": "Farhan",
        "last_name": "Khan",
        "email": "farhan.khan@university.edu",
        "age": 24,
        "grade": 7.3,
        "department": "Electrical Engineering",
    },
]


def seed():
    print("🌱 Seeding database...")
    create_tables()
    db = SessionLocal()

    try:
        existing = db.query(Student).count()
        if existing > 0:
            print(f"⚠️  Database already has {existing} students. Skipping seed.")
            return

        students = [Student(**data) for data in SAMPLE_STUDENTS]
        db.add_all(students)
        db.commit()
        print(f"✅ Seeded {len(students)} students successfully!")

    except Exception as e:
        db.rollback()
        print(f"❌ Seeding failed: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed()
