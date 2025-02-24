from typing import Annotated

from fastapi import Depends
from jose import JWTError

from app.common.utils import token_helper
from app.config.error_codes import ErrorCodes
from app.config.exception import BackendException
from . import oauth2_scheme
from ..schemas import TokenData


def validate_access_token(
        token: Annotated[str, Depends(oauth2_scheme)],
) -> TokenData:
    incorrect_credentials = BackendException(error=ErrorCodes.INCORRECT_CREDENTIALS)

    if not token:
        raise incorrect_credentials

    try:
        payload = token_helper.token_payload(token=token, refresh=False)
    except JWTError:
        raise incorrect_credentials
    except BackendException:
        raise incorrect_credentials

    return payload


def validate_refresh_token(token: str) -> TokenData:
    if not token:
        raise BackendException(error=ErrorCodes.INCORRECT_CREDENTIALS)

    try:
        payload = token_helper.token_payload(token=token, refresh=True)
    except JWTError:
        raise BackendException(error=ErrorCodes.incorrect_credentials)  # noqa B904

    return payload
