from typing import Generic, Optional, Sequence, Type, TypeVar

from fastapi import Response
from pydantic import BaseModel

T = TypeVar("T", bound=Sequence[BaseModel | str], contravariant=True)


class PaginatedRequestSchema(BaseModel):
    """
    Schema for paginated requests.
    """

    page: int = 1
    per_page: int = 10
    search: str | None = None
    sort_by: str | None = None
    sort_order: str = "asc"


class PaginatedListSchema(BaseModel, Generic[T]):
    """
    Schema for paginated list responses.
    """

    total: int = 0
    items: list[T] = []
    page: int = 1
    per_page: int = 10


class BaseResponseCreateSchema(BaseModel, Generic[T]):
    """
    Base schema for all response data during creation.
    """

    message: str | None = None
    status_code: int = 201
    data: Optional[T] = None

    model_config = {
        "from_attributes": True,
    }

    def success(
        self, data=None, message: str = "Created", schema_extra: Type[BaseModel] = None
    ):
        """
        Set the response as successful.
        """
        self.status_code = 201
        self.data = schema_extra.model_validate(data) if schema_extra else data
        self.message = message
        return self

    def error(self, message: str = "Error", status_code: int = 400):
        """
        Set the response as an error.
        """
        self.status_code = status_code
        self.data = None
        self.message = message
        return self

    def render(self, *args, **kwds) -> Response:
        """
        Render the response as a FastAPI Response object.
        """
        return Response(
            content=self.model_dump_json(exclude_none=True),
            status_code=self.status_code,
            media_type="application/json",
        )

    def __call__(self, *args, **kwds):
        """
        Allow the schema to be called like a function.
        """
        return self.render(*args, **kwds)


class BaseResponseSchema(BaseModel, Generic[T]):
    """
    Base schema for all response data.
    """

    message: str | None = None
    status_code: int = 200
    data: Optional[T] = None

    model_config = {
        "from_attributes": True,
    }

    def success(self, data=None, message: str = "Success"):
        """
        Set the response as successful.
        """
        self.status_code = 200
        self.data = data
        self.message = message
        return self

    def error(self, message: str = "Error", status_code: int = 400):
        """
        Set the response as an error.
        """
        self.status_code = status_code
        self.data = None
        self.message = message
        return self

    def render(self, *args, **kwds) -> Response:
        """
        Render the response as a FastAPI Response object.
        """
        exclude_none = kwds.get("exclude_none", True)
        return Response(
            content=self.model_dump_json(exclude_none=exclude_none),
            status_code=self.status_code,
            media_type="application/json",
        )

    def __call__(self, *args, **kwds) -> Response:
        """
        Allow the schema to be called like a function.
        """
        return self.render(*args, **kwds)


class BaseListResponseSchema(BaseModel, Generic[T]):
    """
    Base schema for all list response data.
    """

    message: str | None = None
    status_code: int = 200
    total: int = 0
    page: int = 1
    per_page: int = 10
    data: list[T] = []

    def __init__(self, page, per_page):
        super().__init__()
        self.page = page
        self.per_page = per_page

    model_config = {
        "from_attributes": True,
    }

    def success(
        self,
        data: list[T] = None,
        total=None,
        message: str = "Success",
    ):
        """
        Set the response as successful.
        """
        self.status_code = 200
        self.data = data
        self.total = total if total is not None else len(data)
        self.message = message
        return self

    def error(self, message: str = "Error", status_code: int = 400):
        """
        Set the response as an error.
        """
        self.status_code = status_code
        self.data = []
        self.message = message
        return self

    def render(self, *args, **kwds) -> Response:
        """
        Render the response as a FastAPI Response object.
        """
        exclude_none = kwds.get("exclude_none", True)
        return Response(
            content=self.model_dump_json(exclude_none=exclude_none),
            status_code=self.status_code,
            media_type="application/json",
        )

    def __call__(self, *args, **kwds):
        """
        Allow the schema to be called like a function.
        """
        return self.render(*args, **kwds)
