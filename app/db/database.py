"""
Database Configuration
Uses SQLAlchemy with SQLite for simplicity.
Swap DATABASE_URL in .env to use PostgreSQL in production.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.core.config import settings

# Create engine — check_same_thread=False is only needed for SQLite
connect_args = (
    {"check_same_thread": False} if settings.DATABASE_URL.startswith("sqlite") else {}
)

engine = create_engine(
    settings.DATABASE_URL,
    connect_args=connect_args,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    """Base class for all SQLAlchemy models."""

    pass


def create_tables() -> None:
    """Create all database tables. Called once on app startup."""
    # Import models here so they are registered on Base.metadata
    from app.models import student  # noqa: F401

    Base.metadata.create_all(bind=engine)


def get_db():
    """
    Dependency that provides a database session per request.
    Ensures the session is closed after the request completes.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
