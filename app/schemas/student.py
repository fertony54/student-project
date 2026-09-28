"""
Pydantic Schemas
Used for request validation and response serialization.
Keeps API contracts separate from database models.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field, field_validator

# ──────────────────────────────────────────────
# Base Schema (shared fields)
# ──────────────────────────────────────────────


class StudentBase(BaseModel):
    """Fields shared by create and update schemas."""

    first_name: str = Field(
        ...,
        min_length=1,
        max_length=50,
        description="Student's first name",
        examples=["Alice"],
    )
    last_name: str = Field(
        ...,
        min_length=1,
        max_length=50,
        description="Student's last name",
        examples=["Sharma"],
    )
    email: EmailStr = Field(
        ...,
        description="Unique email address",
        examples=["alice.sharma@university.edu"],
    )
    age: int = Field(
        ...,
        ge=16,
        le=100,
        description="Student age (16–100)",
        examples=[21],
    )
    grade: float = Field(
        ...,
        ge=0.0,
        le=10.0,
        description="GPA on a 0–10 scale",
        examples=[8.5],
    )
    department: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="Department or major",
        examples=["Computer Science"],
    )

    @field_validator("first_name", "last_name")
    @classmethod
    def name_must_be_alpha(cls, value: str) -> str:
        """Names should contain only letters, spaces, and hyphens."""
        stripped = value.strip()
        if not all(c.isalpha() or c in (" ", "-", "'") for c in stripped):
            raise ValueError(
                "Name must contain only letters, spaces, hyphens, or apostrophes"
            )
        return stripped.title()

    @field_validator("department")
    @classmethod
    def department_strip(cls, value: str) -> str:
        return value.strip()


# ──────────────────────────────────────────────
# Create Schema
# ──────────────────────────────────────────────


class StudentCreate(StudentBase):
    """Schema for creating a new student (POST body)."""

    pass


# ──────────────────────────────────────────────
# Update Schema (all fields optional)
# ──────────────────────────────────────────────


class StudentUpdate(BaseModel):
    """Schema for partial updates (PATCH body). All fields optional."""

    first_name: Optional[str] = Field(None, min_length=1, max_length=50)
    last_name: Optional[str] = Field(None, min_length=1, max_length=50)
    email: Optional[EmailStr] = None
    age: Optional[int] = Field(None, ge=16, le=100)
    grade: Optional[float] = Field(None, ge=0.0, le=10.0)
    department: Optional[str] = Field(None, min_length=2, max_length=100)

    @field_validator("first_name", "last_name")
    @classmethod
    def name_must_be_alpha(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return value
        stripped = value.strip()
        if not all(c.isalpha() or c in (" ", "-", "'") for c in stripped):
            raise ValueError(
                "Name must contain only letters, spaces, hyphens, or apostrophes"
            )
        return stripped.title()


# ──────────────────────────────────────────────
# Response Schema
# ──────────────────────────────────────────────


class StudentResponse(StudentBase):
    """Schema returned in API responses — includes DB-generated fields."""

    id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


# ──────────────────────────────────────────────
# List Response Schema
# ──────────────────────────────────────────────


class StudentListResponse(BaseModel):
    """Paginated list response wrapper."""

    total: int
    page: int
    page_size: int
    students: list[StudentResponse]
