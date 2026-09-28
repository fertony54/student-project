"""
Unit Tests — Schemas & Service Layer
Tests validation logic and business rules in isolation.
"""

import pytest
from pydantic import ValidationError

from app.schemas.student import StudentCreate, StudentUpdate


class TestStudentCreateSchema:
    """Tests for StudentCreate Pydantic schema validation."""

    def test_valid_student_schema(self, sample_student_data):
        """Valid data should pass without errors."""
        student = StudentCreate(**sample_student_data)
        assert student.first_name == "Alice"
        assert student.last_name == "Sharma"
        assert student.email == "alice.sharma@university.edu"

    def test_name_is_title_cased(self, sample_student_data):
        """Names should be auto-title-cased."""
        sample_student_data["first_name"] = "alice"
        student = StudentCreate(**sample_student_data)
        assert student.first_name == "Alice"

    def test_invalid_email_raises(self, sample_student_data):
        """Invalid email format should raise ValidationError."""
        sample_student_data["email"] = "not-an-email"
        with pytest.raises(ValidationError) as exc_info:
            StudentCreate(**sample_student_data)
        assert "email" in str(exc_info.value).lower()

    def test_age_below_minimum_raises(self, sample_student_data):
        """Age below 16 should raise ValidationError."""
        sample_student_data["age"] = 10
        with pytest.raises(ValidationError):
            StudentCreate(**sample_student_data)

    def test_age_above_maximum_raises(self, sample_student_data):
        """Age above 100 should raise ValidationError."""
        sample_student_data["age"] = 150
        with pytest.raises(ValidationError):
            StudentCreate(**sample_student_data)

    def test_grade_out_of_range_raises(self, sample_student_data):
        """Grade above 10.0 should raise ValidationError."""
        sample_student_data["grade"] = 11.5
        with pytest.raises(ValidationError):
            StudentCreate(**sample_student_data)

    def test_negative_grade_raises(self, sample_student_data):
        """Negative grade should raise ValidationError."""
        sample_student_data["grade"] = -1.0
        with pytest.raises(ValidationError):
            StudentCreate(**sample_student_data)

    def test_empty_first_name_raises(self, sample_student_data):
        """Empty first name should raise ValidationError."""
        sample_student_data["first_name"] = ""
        with pytest.raises(ValidationError):
            StudentCreate(**sample_student_data)

    def test_name_with_numbers_raises(self, sample_student_data):
        """Names with digits should raise ValidationError."""
        sample_student_data["first_name"] = "Alice123"
        with pytest.raises(ValidationError):
            StudentCreate(**sample_student_data)

    def test_hyphenated_name_is_valid(self, sample_student_data):
        """Hyphenated names (e.g. Mary-Jane) should be allowed."""
        sample_student_data["first_name"] = "Mary-Jane"
        student = StudentCreate(**sample_student_data)
        assert "Mary" in student.first_name

    def test_boundary_grade_zero(self, sample_student_data):
        """Grade of 0.0 should be valid."""
        sample_student_data["grade"] = 0.0
        student = StudentCreate(**sample_student_data)
        assert student.grade == 0.0

    def test_boundary_grade_ten(self, sample_student_data):
        """Grade of 10.0 should be valid."""
        sample_student_data["grade"] = 10.0
        student = StudentCreate(**sample_student_data)
        assert student.grade == 10.0

    def test_boundary_age_sixteen(self, sample_student_data):
        """Age of 16 should be valid (lower bound)."""
        sample_student_data["age"] = 16
        student = StudentCreate(**sample_student_data)
        assert student.age == 16

    def test_missing_required_field_raises(self, sample_student_data):
        """Missing a required field should raise ValidationError."""
        del sample_student_data["email"]
        with pytest.raises(ValidationError):
            StudentCreate(**sample_student_data)


class TestStudentUpdateSchema:
    """Tests for StudentUpdate — all fields optional."""

    def test_empty_update_is_valid(self):
        """An update with no fields should be allowed."""
        update = StudentUpdate()
        assert update.model_dump(exclude_unset=True) == {}

    def test_partial_update_with_grade_only(self):
        """Update with only grade field should work."""
        update = StudentUpdate(grade=9.0)
        fields = update.model_dump(exclude_unset=True)
        assert fields == {"grade": 9.0}

    def test_invalid_email_in_update_raises(self):
        """Invalid email in update should still raise ValidationError."""
        with pytest.raises(ValidationError):
            StudentUpdate(email="bad-email")

    def test_valid_partial_update(self):
        """Multiple valid fields in update should pass."""
        update = StudentUpdate(first_name="Bob", grade=7.5)
        assert update.first_name == "Bob"
        assert update.grade == 7.5
