from fastapi import APIRouter, HTTPException

from app.controller.auth import AuthController
from app.middleware.authentication import AUTH, REFRESH_AUTH
from app.models import DbSession
from app.schemas import BaseResponseCreateSchema
from app.schemas.auth import (
    RefreshTokenSchema,
    SignInRequestSchema,
    SignInResponseSchema,
    SignUpRequestSchema,
    UserProfileSchema,
)
from app.utils.settings import Settings

controller = AuthController()

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post(
    "/refresh",
    description="Refresh the access token using the refresh token (Bearer the refresh token)",
)
def refresh_token(
    data: RefreshTokenSchema, auth: REFRESH_AUTH
) -> BaseResponseCreateSchema[SignInResponseSchema]:
    """
    Refresh Token Endpoint
    """
    response = BaseResponseCreateSchema[SignInResponseSchema]()
    try:
        result = controller.refresh_token(auth, data.refresh_token)
        response.success(result, "Token refreshed successfully", SignInResponseSchema)
    except HTTPException as e:
        response.error(e.detail, e.status_code)
    except Exception as e:
        response.error(str(e), 500)
    return response()


@router.post("/sign-in")
def sign_in(payload: SignInRequestSchema, db: DbSession, setting: Settings):
    response = BaseResponseCreateSchema[SignInResponseSchema]()
    try:
        result = controller.sign_in(db, payload, setting)
        response.success(result, "User signed in")
    except HTTPException as e:
        response.error(e.detail, e.status_code)
    return response()


@router.post("/sign-up", status_code=201)
def sign_up(payload: SignUpRequestSchema, db: DbSession):
    response = BaseResponseCreateSchema[UserProfileSchema]()
    try:
        result = controller.sign_up(db, payload)
        response.success(result, "User registered")
    except HTTPException as e:
        response.error(e.detail, e.status_code)
    return response()


@router.get("/profile", status_code=200)
def get_profile(auth: AUTH, db: DbSession):
    response = BaseResponseCreateSchema[UserProfileSchema]()
    try:
        user = controller.get_user_by_uuid(db, auth.uuid)
        response.success(user, "User profile retrieved")
    except HTTPException as e:
        response.error(e.detail, e.status_code)
    return response()


@router.get("/verify_token", status_code=200)
def verify_token(auth: AUTH) -> BaseResponseCreateSchema:
    response = BaseResponseCreateSchema()
    try:
        print(auth)
        response.success(True, "Token is valid")
    except HTTPException as e:
        response.error(e.detail, e.status_code)
    return response()
