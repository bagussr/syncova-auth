from fastapi import APIRouter, HTTPException

from app.controller.auth import AuthController
from app.models import DbSession
from app.schemas import BaseResponseCreateSchema
from app.schemas.auth import (
    SignUpRequestSchema,
    UserProfileSchema,
)
from app.utils.settings import Settings

controller = AuthController()

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/sign-in")
def sign_in(payload: SignUpRequestSchema, db: DbSession, setting: Settings):
    response = BaseResponseCreateSchema[UserProfileSchema]()
    try:
        result = controller.sign_in(db, payload, setting)
        response.success(result, "User signed in")
    except HTTPException as e:
        response.error(e.detail, e.status_code)
    return response


@router.post("/sign-up", status_code=201)
def sign_up(payload: SignUpRequestSchema, db: DbSession):
    response = BaseResponseCreateSchema[UserProfileSchema]()
    try:
        result = controller.sign_up(db, payload)
        response.success(result, "User registered")
    except HTTPException as e:
        response.error(e.detail, e.status_code)
    return response
