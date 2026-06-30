import os
import uuid
from typing import Annotated

from dotenv import load_dotenv
from fastapi import Depends
from sqlalchemy import Column, DateTime, Integer, String, create_engine, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker

load_dotenv()

engine = create_engine(
    os.getenv("DB_URL"),
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10,
)


Base = declarative_base()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()


DbSession = Annotated[Session, Depends(get_db)]


class BaseModel(Base):
    """
    Base model for all SQLAlchemy models.
    """

    __abstract__ = True

    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True, nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(
        DateTime, nullable=False, server_default=func.now(), onupdate=func.now()
    )
    created_by = Column(String, nullable=True)
    updated_by = Column(String, nullable=True)


def check_connection(engine) -> bool:
    """
    Check if the database connection is alive.
    """
    try:
        with engine.connect() as connection:
            connection.execute("SELECT 1")
        return True
    except Exception:
        print("Database connection failed.")
        return False
