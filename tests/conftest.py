"""
Pytest Fixtures
Shared test configuration used across all test files.
Uses an in-memory SQLite database so tests are fast and isolated.
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.database import Base, get_db
from app.main import app

# ── Test Database ────────────────────────────────────────────────────────────
TEST_DATABASE_URL = "mysql+pymysql://root:1234@localhost:3306/Students.db"

test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


def override_get_db():
    """Dependency override: use test database instead of production DB."""
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="function")
def db_session():
    """
    Provides a fresh database session per test.
    Creates tables before the test, drops them after.
    """
    Base.metadata.create_all(bind=test_engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=test_engine)


@pytest.fixture(scope="function")
def client(db_session):
    """
    Provides a FastAPI TestClient backed by the test database.
    The get_db dependency is overridden for the duration of the test.
    """
    app.dependency_overrides[get_db] = override_get_db
    Base.metadata.create_all(bind=test_engine)

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=test_engine)


# ── Reusable Test Data ───────────────────────────────────────────────────────


@pytest.fixture
def sample_student_data():
    """Valid student payload for create tests."""
    return {
        "first_name": "Alice",
        "last_name": "Sharma",
        "email": "alice.sharma@university.edu",
        "age": 21,
        "grade": 8.5,
        "department": "Computer Science",
    }


@pytest.fixture
def second_student_data():
    """A second valid student payload."""
    return {
        "first_name": "Bob",
        "last_name": "Patel",
        "email": "bob.patel@university.edu",
        "age": 22,
        "grade": 7.2,
        "department": "Mathematics",
    }


@pytest.fixture
def created_student(client, sample_student_data):
    """Creates a student via the API and returns the response JSON."""
    response = client.post("/api/v1/students/", json=sample_student_data)
    assert response.status_code == 201
    return response.json()
