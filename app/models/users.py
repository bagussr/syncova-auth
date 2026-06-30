from enum import Enum

from sqlalchemy import Boolean, Column, String, UniqueConstraint
from sqlalchemy import Enum as SqlEnum

from app.models import BaseModel


class AuthProvider(str, Enum):
    """Supported social sign-up providers."""

    GOOGLE = "google"
    APPLE = "apple"
    MICROSOFT = "microsoft"
    EMAIL = "email"


class Users(BaseModel):
    """
    Users model for representing user data in the database.
    """

    __tablename__ = "users"

    __table_args__ = (
        UniqueConstraint(
            "auth_provider",
            "provider_subject",
            name="uq_users_auth_provider_subject",
        ),
    )

    email = Column(String(100), unique=True, nullable=False)
    full_name = Column(String(150), nullable=True)
    password_hash = Column(String(255), nullable=True)
    auth_provider = Column(
        SqlEnum(AuthProvider, name="auth_provider_enum"),
        nullable=False,
    )
    provider_subject = Column(String(255), nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)
