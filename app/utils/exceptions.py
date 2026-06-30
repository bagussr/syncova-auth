from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from psycopg2.errors import NotNullViolation
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm.exc import MappedAnnotationError, NoResultFound


def handle_integrity_error(request: Request, exc: IntegrityError):
    print(f"Integriger error: {exc}")
    return JSONResponse(
        status_code=400,
        content={
            "message": "Integrity Error",
            "status_code": 400,
            "data": str(exc.orig) if exc.orig else str(exc),
        },
    )


def handle_sqlalchemy_error(request: Request, exc: SQLAlchemyError):
    print(f"SQLAlchemy error: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "message": "Database Error",
            "status_code": 500,
            "data": str(exc),
        },
    )


def handle_no_result_found(request: Request, exc: NoResultFound):
    print(f"No result found error: {exc}")
    return JSONResponse(
        status_code=404,
        content={
            "message": "No Result Found",
            "status_code": 404,
            "data": str(exc),
        },
    )


def handle_mapped_annotation_error(request: Request, exc: MappedAnnotationError):
    print(f"Mapped Annotation error: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "message": "Mapped Annotation Error",
            "status_code": 500,
            "data": str(exc),
        },
    )


def handle_validation_error(request: Request, exc: ValidationError):
    print(f"Validation error: {exc}")
    return JSONResponse(
        status_code=422,
        content={
            "message": "Validation Error",
            "status_code": 422,
            "data": exc.errors(),
        },
    )


def handle_generic_error(request: Request, exc: Exception):
    print(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "message": "Internal Server Error",
            "status_code": 500,
            "data": str(exc),
        },
    )


def handle_unauthorized_error(request: Request, exc: Exception):
    print(f"Unauthorized error: {exc}")
    return JSONResponse(
        status_code=401,
        content={
            "message": "Unauthorized",
            "status_code": 401,
            "data": str(exc),
        },
    )


def handle_not_null_violation(request: Request, exc: NotNullViolation):
    print(f"Not Null Violation error: {exc}")
    return JSONResponse(
        status_code=400,
        content={
            "message": "Not Null Violation",
            "status_code": 400,
            "data": str(exc),
        },
    )


def handle_request_validation_error(request: Request, exc: RequestValidationError):
    print(f"Request Validation error: {exc}")
    errors = exc.errors()
    error_messages = []
    for error in errors:
        message = error["msg"]
        error_messages.append(f"{message}")
    return JSONResponse(
        status_code=422,
        content={
            "message": "Request Validation Error",
            "status_code": 422,
            "data": error_messages,
        },
    )


class CustomExceptiom:
    app: FastAPI

    def __init__(self, app: FastAPI):
        self.app = app

    def init(self):
        self.app.add_exception_handler(IntegrityError, handle_integrity_error)
        self.app.add_exception_handler(SQLAlchemyError, handle_sqlalchemy_error)
        self.app.add_exception_handler(NoResultFound, handle_no_result_found)
        self.app.add_exception_handler(
            MappedAnnotationError, handle_mapped_annotation_error
        )
        self.app.add_exception_handler(ValidationError, handle_validation_error)
        self.app.add_exception_handler(Exception, handle_generic_error)
        self.app.add_exception_handler(NotNullViolation, handle_not_null_violation)
        self.app.add_exception_handler(
            RequestValidationError, handle_request_validation_error
        )
        self.app.add_exception_handler(401, handle_unauthorized_error)
