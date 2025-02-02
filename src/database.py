"""
Database module for managing the SQLAlchemy engine and session.

This module initializes the database connection, creates tables if they do not exist,
and provides a session dependency for database operations.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base

# Database connection URL (using SQLite for this project)
DATABASE_URL = "sqlite:///./data/social_media.db"

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Create a session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """
    Initializes the database by creating tables if they do not already exist.
    """
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    init_db()
    print("✅ Database initialized successfully!")

# Dependency to provide a session instance for database operations
def get_db():
    """
    Provides a new database session for request handling.
    Ensures proper session management by closing the session after use.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
