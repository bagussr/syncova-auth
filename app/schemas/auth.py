from pydantic import BaseModel, EmailStr, Field, model_validator

from app.models.users import AuthProvider


class SignUpRequestSchema(BaseModel):
    """Payload for social sign-up and email sign-up."""

    email: EmailStr
    full_name: str | None = Field(min_length=2, max_length=150)
    password: str | None = Field(min_length=8, max_length=255)
    provider: AuthProvider
    provider_subject: str | None = Field(None, min_length=2, max_length=255)

    @model_validator(mode="before")
    def validate_provider_subject(cls, values):
        provider = values.get("provider")
        provider_subject = values.get("provider_subject")

        if provider != AuthProvider.EMAIL and not provider_subject:
            raise ValueError("provider_subject is required for social sign-up")

        if provider == AuthProvider.EMAIL:
            values["provider_subject"] = values.get("email")
        return values


class SignInRequestSchema(BaseModel):
    """Payload for social sign-in and email sign-in"""

    email: EmailStr
    password: str | None = Field(min_length=8, max_length=255)
    provider: AuthProvider
    provider_subject: str | None = Field(None, min_length=2, max_length=255)

    @model_validator(mode="before")
    def validate_provider_subject(cls, values):
        provider = values.get("provider")
        provider_subject = values.get("provider_subject")

        if provider != AuthProvider.EMAIL and not provider_subject:
            raise ValueError("provider_subject is required for social sign-in")
        return values


class UserProfileSchema(BaseModel):
    """User profile returned from auth endpoints."""

    id: int
    uuid: str
    email: EmailStr
    full_name: str | None
    provider: AuthProvider

    model_config = {
        "from_attributes": True,
    }


class SignInResponseSchema(BaseModel):
    """Response schema for sign-in."""

    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int


class RefreshTokenSchema(BaseModel):
    """Payload for refreshing the access token."""

    refresh_token: str


class ClaimTokenSchema(BaseModel):
    """Schema for claims in the JWT token."""

    uuid: str
    email: EmailStr
    is_active: bool
