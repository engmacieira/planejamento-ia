from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

engine = create_engine(settings.DB_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    """
    Dependency function that yields a database session.
    Ensures safe closing of the session after the request is processed.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
