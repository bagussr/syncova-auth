import datetime

from fastapi import HTTPException, status
from jose import jwt
from sqlalchemy import select

from app.models import DbSession
from app.models.users import Users
from app.schemas.auth import (
    SignInRequestSchema,
    SignInResponseSchema,
    SignUpRequestSchema,
)
from app.utils.password import hash_password
from app.utils.settings import BaseSettings


class AuthController:
    """
    Controller for handling authentication-related operations.
    """

    def sign_in(
        self, db: DbSession, payload: SignInRequestSchema, setting: BaseSettings
    ) -> SignInResponseSchema:
        """Authenticate a user based on the provided credentials."""

        user = db.execute(
            select(Users).where(
                Users.email == payload.email,
                Users.auth_provider == payload.provider,
                Users.provider_subject == payload.provider_subject,
            )
        ).scalar_one_or_none()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

        if payload.provider == "email" and not user.password_hash:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Password is required for email sign-in",
            )

        if payload.provider == "email" and not self.verify_password(
            payload.password, user.password_hash
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid password",
            )

        token = jwt.encode(
            {
                "user_id": user.id,
                "exp": datetime.datetime.now(datetime.timezone.utc)
                + datetime.timedelta(hours=24),
            },
            setting.JWT_SECRET,
            algorithm="HS256",
        )
        refresh_token = jwt.encode(
            {
                "user_id": user.id,
                "exp": datetime.datetime.now(datetime.timezone.utc)
                + datetime.timedelta(days=7),
            },
            setting.JWT_SECRET,
            algorithm="HS256",
        )

        return SignInResponseSchema(
            access_token=token,
            refresh_token=refresh_token,
            expires_in=24 * 60 * 60,
        )

    def sign_up(self, db: DbSession, payload: SignUpRequestSchema) -> Users:
        """Create a new user for a supported provider."""

        existing_user = db.execute(
            select(Users).where(Users.email == payload.email)
        ).scalar_one_or_none()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User with this email already exists",
            )

        existing_provider_subject = db.execute(
            select(Users).where(
                Users.auth_provider == payload.provider,
                Users.provider_subject == payload.provider_subject,
            )
        ).scalar_one_or_none()
        if existing_provider_subject:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Provider account is already registered",
            )

        user = Users(
            email=payload.email,
            full_name=payload.full_name,
            password_hash=hash_password(payload.password) if payload.password else None,
            auth_provider=payload.provider,
            provider_subject=payload.provider_subject,
            created_by="system",
            updated_by="system",
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        return user
