from typing import Annotated

from fastapi import Depends

from app.config.error_codes import ErrorCodes
from app.config.exception import BackendException
from .token import validate_access_token
from ..schemas import TokenData
from ...modules.user.schemas import UserInDBBase
from ...modules.user.services import UserService


async def get_current_user(
    user_service: UserService.register_deps(),
    payload: Annotated[TokenData, Depends(validate_access_token)],
) -> UserInDBBase:
    user = await user_service.get_user_by_sid(sid=payload.sid)

    if user is None:
        raise BackendException(error=ErrorCodes.INCORRECT_CREDENTIALS)

    return user
