"""
Database session factory.

Provides the SessionLocal class for creating database sessions.
"""

from sqlalchemy.orm import sessionmaker
from app.db.base import engine

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_session():
    """Get a database session (context manager compatible)."""
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
