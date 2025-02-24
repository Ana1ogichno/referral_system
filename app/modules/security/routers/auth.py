from typing import Annotated

from fastapi import APIRouter, Depends, Query
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from starlette import status
from starlette.responses import JSONResponse

from app.common.deps import oauth2_scheme
from app.common.deps.current_user import get_current_user
from app.common.deps.token import validate_refresh_token
from app.common.logger import LoggerManager
from app.common.schemas import LoginToken, RefreshToken, Msg
from app.common.utils import token_helper
from app.config.db.session import DBSessionManager
from app.config.error_codes import ErrorCodes
from app.config.exception import BackendException
from app.config.settings import settings
from ...user.schemas import UserInDBBase, UserCreate
from ...user.services import UserService

router = APIRouter()

logger = LoggerManager.get_security_logger()


@router.post(path="/register", response_model=UserInDBBase)
async def register(
    user_in: UserCreate,
    user_service: UserService.register_deps(),
) -> UserInDBBase:
    """
    User registering
    """

    user = await user_service.create_user(
        user_in=user_in
    )

    logger.debug("User has been created")
    return user


@router.post(path="/login", response_model=LoginToken)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    user_service: UserService.register_deps(),
) -> LoginToken:
    """
    Login method (Create JWT access and refresh tokens)
    """

    logger.debug("Authenticate user")
    user = await user_service.authenticate_user(
        login=form_data.username,
        password=form_data.password,
    )
    if not user:
        logger.warning("Incorrect credentials")
        raise BackendException(ErrorCodes.INCORRECT_CREDENTIALS)
    payload = {
        "sub": str(user.sid),
        "permissions": ["777"],
    }
    logger.debug("Creating access_token and refresh_token")
    access_token, refresh_token = token_helper.create_token_pair(payload)
    logger.debug("access_token and refresh_token created")

    return LoginToken(access_token=access_token, refresh_token=refresh_token)


@router.post(path="/refresh_token", response_model=LoginToken)
async def update_access_token(
    refresh_token: Annotated[RefreshToken, Depends()],
    db_session_manager: DBSessionManager.register_deps(),
) -> LoginToken:
    """
    Method for update JWT access token
    """
    logger.debug("Validate refresh token")
    payload = validate_refresh_token(refresh_token.refresh_token)

    redis_conn = db_session_manager.get_redis()

    logger.debug("Reset expire seconds")
    redis_conn.setex(
        name=f"{payload.sid}:{payload.jti}",
        time=settings.project.REFRESH_TOKEN_EXPIRE_SECONDS,
        value="True",
    )

    logger.debug("Get payload for tokens")
    payload = {"sub": payload.sid, "permissions": payload.permissions}

    logger.debug("Updating access_token and refresh_token")
    access_token, refresh_token = token_helper.create_token_pair(payload)
    logger.debug("access_token and refresh_token updated")

    return LoginToken(access_token=access_token, refresh_token=refresh_token)


@router.post(path="/logout", response_model=Msg)
async def logout(
    token: Annotated[str, Depends(oauth2_scheme)],
    current_user: Annotated[UserInDBBase, Depends(get_current_user)],
    db_session_manager: DBSessionManager.register_deps(),
    everywhere: bool = Query(False, description="Выйти со всех устройств"),
) -> JSONResponse:
    """
    Method for logout.
    """

    redis_conn = db_session_manager.get_redis()

    if everywhere:
        logger.debug("Logout from all devices")
        keys = redis_conn.keys(f"{str(current_user.sid)}:*")
        logger.debug("Reset expire seconds")
        for key in keys:
            redis_conn.setex(
                name=key,
                time=settings.project.ACCESS_TOKEN_EXPIRE_SECONDS,
                value="True",
            )
    else:
        logger.debug("Logout current user")
        payload = jwt.decode(
            token,
            settings.project.TOKEN_SECRET_KEY,
            algorithms=[settings.project.ALGORITHM],
        )
        logger.debug("Reset expire seconds")
        redis_conn.setex(
            name=f"{str(current_user.sid)}:{payload.get('jti')}",
            time=settings.project.ACCESS_TOKEN_EXPIRE_SECONDS,
            value="True",
        )

    logger.debug("Logout success")
    response = JSONResponse(
        content=Msg(msg="Успешный выход из аккаунта").model_dump(),
        status_code=status.HTTP_200_OK,
    )

    return response
