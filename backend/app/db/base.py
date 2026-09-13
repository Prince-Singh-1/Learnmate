"""
SQLAlchemy Base and engine configuration.

Provides the declarative Base class used by all models
and the database engine configuration.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base

# Database URL — will be loaded from config when DB is integrated
# For now, using SQLite in-memory as a fallback
DATABASE_URL = "sqlite:///./learnmate_dev.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},  # SQLite only
    echo=False,
)

Base = declarative_base()
