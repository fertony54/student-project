"""
Student Service Layer
Contains all business logic and database operations.
Keeps route handlers thin — they only validate and delegate.
"""

from typing import Optional

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.student import Student
from app.schemas.student import StudentCreate, StudentUpdate


class StudentService:
    """Encapsulates all CRUD operations for students."""

    # ──────────────────────────────────────────
    # Create
    # ──────────────────────────────────────────

    @staticmethod
    def create_student(db: Session, student_data: StudentCreate) -> Student:
        """
        Create a new student record.
        Raises 409 if the email already exists.
        """
        db_student = Student(
            first_name=student_data.first_name,
            last_name=student_data.last_name,
            email=student_data.email,
            age=student_data.age,
            grade=student_data.grade,
            department=student_data.department,
        )
        try:
            db.add(db_student)
            db.commit()
            db.refresh(db_student)
            return db_student
        except IntegrityError:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"A student with email '{student_data.email}' already exists.",
            )

    # ──────────────────────────────────────────
    # Read
    # ──────────────────────────────────────────

    @staticmethod
    def get_student_by_id(db: Session, student_id: int) -> Student:
        """Fetch a single student. Raises 404 if not found."""
        student = db.query(Student).filter(Student.id == student_id).first()
        if not student:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Student with id {student_id} not found.",
            )
        return student

    @staticmethod
    def get_student_by_email(db: Session, email: str) -> Optional[Student]:
        """Fetch a student by email. Returns None if not found."""
        return db.query(Student).filter(Student.email == email).first()

    @staticmethod
    def get_all_students(
        db: Session,
        page: int = 1,
        page_size: int = 10,
        department: Optional[str] = None,
        search: Optional[str] = None,
    ) -> tuple[int, list[Student]]:
        """
        Fetch paginated students with optional filtering.

        Args:
            db: Database session.
            page: 1-based page number.
            page_size: Number of records per page.
            department: Filter by department name (case-insensitive).
            search: Search by first name, last name, or email.

        Returns:
            Tuple of (total_count, list_of_students).
        """
        query = db.query(Student)

        if department:
            query = query.filter(Student.department.ilike(f"%{department}%"))

        if search:
            search_term = f"%{search}%"
            query = query.filter(
                Student.first_name.ilike(search_term)
                | Student.last_name.ilike(search_term)
                | Student.email.ilike(search_term)
            )

        total = query.count()
        offset = (page - 1) * page_size
        students = query.order_by(Student.id).offset(offset).limit(page_size).all()
        return total, students

    # ──────────────────────────────────────────
    # Update
    # ──────────────────────────────────────────

    @staticmethod
    def update_student(
        db: Session, student_id: int, update_data: StudentUpdate
    ) -> Student:
        """
        Partially update a student. Only provided fields are changed.
        Raises 404 if not found, 409 on duplicate email.
        """
        student = StudentService.get_student_by_id(db, student_id)

        update_fields = update_data.model_dump(exclude_unset=True)
        for field, value in update_fields.items():
            setattr(student, field, value)

        try:
            db.commit()
            db.refresh(student)
            return student
        except IntegrityError:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Email '{update_data.email}' is already in use.",
            )

    # ──────────────────────────────────────────
    # Delete
    # ──────────────────────────────────────────

    @staticmethod
    def delete_student(db: Session, student_id: int) -> dict:
        """
        Delete a student record.
        Raises 404 if not found.
        """
        student = StudentService.get_student_by_id(db, student_id)
        db.delete(student)
        db.commit()
        return {"message": f"Student {student_id} deleted successfully."}

    # ──────────────────────────────────────────
    # Stats
    # ──────────────────────────────────────────

    @staticmethod
    def get_statistics(db: Session) -> dict:
        """Return aggregate statistics for the student body."""
        from sqlalchemy import func

        total = db.query(func.count(Student.id)).scalar() or 0
        avg_grade = db.query(func.avg(Student.grade)).scalar()
        avg_age = db.query(func.avg(Student.age)).scalar()
        max_grade = db.query(func.max(Student.grade)).scalar()
        min_grade = db.query(func.min(Student.grade)).scalar()

        dept_counts = (
            db.query(Student.department, func.count(Student.id).label("count"))
            .group_by(Student.department)
            .all()
        )

        return {
            "total_students": total,
            "average_grade": round(avg_grade, 2) if avg_grade else None,
            "average_age": round(avg_age, 1) if avg_age else None,
            "highest_grade": max_grade,
            "lowest_grade": min_grade,
            "students_per_department": {dept: count for dept, count in dept_counts},
        }
