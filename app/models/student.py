"""
Student Database Model
Defines the students table schema.
"""

from datetime import datetime, timezone

from sqlalchemy import CheckConstraint, Column, DateTime, Float, Integer, String

from app.db.database import Base


class Student(Base):
    """SQLAlchemy ORM model for the students table."""

    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False, index=True)
    age = Column(Integer, nullable=False)
    grade = Column(Float, nullable=False)
    department = Column(String(100), nullable=False)
    created_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    updated_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    __table_args__ = (
        CheckConstraint("age >= 16 AND age <= 100", name="check_age_range"),
        CheckConstraint("grade >= 0.0 AND grade <= 10.0", name="check_grade_range"),
    )

    def __repr__(self) -> str:
        return (
            f"<Student(id={self.id}, "
            f"name={self.first_name} {self.last_name}, "
            f"email={self.email})>"
        )
