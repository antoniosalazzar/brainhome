from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# Create engine (connection pool)
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True, # To check if connections are alive
    echo=settings.DEBUG # Log SQL queries in debug mode
)

# SessionLocal: a factory for new Session objects
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base class for declarative ORM models
Base = declarative_base()

# Dependency for FastAPI (endpoint level)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()