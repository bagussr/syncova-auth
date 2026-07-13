from typing import Annotated

from fastapi import HTTPException
from fastapi.params import Depends
from fastapi.security import HTTPBearer
from jose import jwt
from jose.exceptions import JWTClaimsError, JWTError
from pydantic import BaseModel

from app import settings
from app.schemas.auth import ClaimTokenSchema


class TokenSchema(BaseModel):
    """
    Schema for token validation.
    """

    scheme: str
    credentials: str


security = HTTPBearer()


def get_current_user(
    token: Annotated[TokenSchema, Depends(security)],
) -> ClaimTokenSchema:
    """
    Valiate the token and return the user UUID.
    """
    try:
        payload = jwt.decode(
            token.credentials,
            settings.JWT_SECRET,
            algorithms=["HS256"],
        )

        return ClaimTokenSchema.model_validate(payload)
    except JWTClaimsError:
        raise HTTPException(status_code=401, detail="Invalid token claims")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    except Exception as e:
        raise e


def refresh_token(token: Annotated[TokenSchema, Depends(security)]) -> str:
    """
    Valiate the refresh token and return the user UUID.
    """
    if token.credentials is None:
        raise Exception("Refresh token is required")
    return token.credentials


AUTH = Annotated[ClaimTokenSchema, Depends(get_current_user)]
REFRESH_AUTH = Annotated[str, Depends(refresh_token)]
