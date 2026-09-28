"""
Student API Endpoints
All routes are mounted at /api/v1/students
"""

from typing import Optional

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.student import (
    StudentCreate,
    StudentListResponse,
    StudentResponse,
    StudentUpdate,
)
from app.services.student_service import StudentService

router = APIRouter(prefix="/students")


# ──────────────────────────────────────────────
# POST /students
# ──────────────────────────────────────────────


@router.post(
    "/",
    response_model=StudentResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new student",
    description="Register a new student. Email must be unique.",
)
def create_student(
    student_data: StudentCreate,
    db: Session = Depends(get_db),
):
    return StudentService.create_student(db, student_data)


# ──────────────────────────────────────────────
# GET /students
# ──────────────────────────────────────────────


@router.get(
    "/",
    response_model=StudentListResponse,
    status_code=status.HTTP_200_OK,
    summary="List all students",
    description="Retrieve a paginated list of students with optional filtering.",
)
def list_students(
    page: int = Query(default=1, ge=1, description="Page number (1-based)"),
    page_size: int = Query(default=10, ge=1, le=100, description="Records per page"),
    department: Optional[str] = Query(None, description="Filter by department"),
    search: Optional[str] = Query(None, description="Search by name or email"),
    db: Session = Depends(get_db),
):
    total, students = StudentService.get_all_students(
        db=db,
        page=page,
        page_size=page_size,
        department=department,
        search=search,
    )
    return StudentListResponse(
        total=total,
        page=page,
        page_size=page_size,
        students=students,
    )


# ──────────────────────────────────────────────
# GET /students/stats
# ──────────────────────────────────────────────


@router.get(
    "/stats",
    status_code=status.HTTP_200_OK,
    summary="Get student statistics",
    description="Aggregate statistics: totals, averages, department breakdown.",
)
def get_statistics(db: Session = Depends(get_db)):
    return StudentService.get_statistics(db)


# ──────────────────────────────────────────────
# GET /students/{student_id}
# ──────────────────────────────────────────────


@router.get(
    "/{student_id}",
    response_model=StudentResponse,
    status_code=status.HTTP_200_OK,
    summary="Get a student by ID",
)
def get_student(
    student_id: int,
    db: Session = Depends(get_db),
):
    return StudentService.get_student_by_id(db, student_id)


# ──────────────────────────────────────────────
# PATCH /students/{student_id}
# ──────────────────────────────────────────────


@router.patch(
    "/{student_id}",
    response_model=StudentResponse,
    status_code=status.HTTP_200_OK,
    summary="Update a student",
    description="Partially update a student. Only provided fields are changed.",
)
def update_student(
    student_id: int,
    update_data: StudentUpdate,
    db: Session = Depends(get_db),
):
    return StudentService.update_student(db, student_id, update_data)


# ──────────────────────────────────────────────
# DELETE /students/{student_id}
# ──────────────────────────────────────────────


@router.delete(
    "/{student_id}",
    status_code=status.HTTP_200_OK,
    summary="Delete a student",
)
def delete_student(
    student_id: int,
    db: Session = Depends(get_db),
):
    return StudentService.delete_student(db, student_id)
