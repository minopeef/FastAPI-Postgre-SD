# Database configuration and session management
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import QueuePool
from orm import modelos
import os
from typing import Generator


# Database connection configuration
DATABASE_URI = os.getenv("db_uri", "sqlite:///bd_ejemplo.db")

# Create engine with connection pooling for better performance
if DATABASE_URI.startswith("sqlite"):
    engine = create_engine(
        DATABASE_URI,
        connect_args={"check_same_thread": False},
        echo=False
    )
else:
    # PostgreSQL configuration with connection pooling
    engine = create_engine(
        DATABASE_URI,
        poolclass=QueuePool,
        pool_size=5,
        max_overflow=10,
        pool_pre_ping=True,  # Verify connections before using
        echo=False
    )

# Create all tables
modelos.BaseClass.metadata.create_all(engine)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def generador_sesion() -> Generator[Session, None, None]:
    """
    Dependency injection for database sessions.
    Ensures proper session lifecycle management.
    """
    sesion = SessionLocal()
    try:
        yield sesion
    except Exception:
        sesion.rollback()
        raise
    finally:
        sesion.close()


