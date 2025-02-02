from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base

DATABASE_URL = "sqlite:///./data/social_media.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """Create database tables if they do not exist."""
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    init_db()
    print("✅ Banco de dados inicializado com sucesso!")

# Dependency to get the database session
def get_db():
    """
    Provides a new session for database operations.
    Ensures proper session management.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
