from typing import Annotated
from uuid import UUID

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.base import ExecutableOption

from app.common.decorators.logger import logging_function_info
from app.common.deps import get_db
from app.common.logger import LoggerManager
from app.config.error_codes import ErrorCodes
from app.config.exception import BackendException
from app.modules.user.models import UserModel
from app.modules.user.repositories import UserRepository
from app.modules.user.schemas import UserCreate

logger = LoggerManager.get_user_logger()


class UserService:
    def __init__(self, db: AsyncSession):
        self._user_repository = UserRepository(db=db)
        self.db = db

    @logging_function_info(logger=logger, description="Get user by email in db")
    async def get_user_by_login(
        self, login: str, custom_options: tuple[ExecutableOption, ...] = None
    ) -> UserModel | None:
        return await self._user_repository.get_by_login(
            login=login, custom_options=custom_options
        )

    @logging_function_info(logger=logger, description="Get user by sid in db")
    async def get_user_by_sid(
        self, sid: UUID
    ) -> UserModel | None:
        return await self._user_repository.get_one(sid=sid)

    @logging_function_info(logger=logger, description="Create user in db")
    async def create_user(self, user_in: UserCreate):
        logger.debug("Get user by email")
        user = await self._user_repository.get_by_login(login=user_in.login)

        if user:
            logger.warning("User already exist")
            raise BackendException(ErrorCodes.LOGIN_ALREADY_EXISTS)

        logger.debug("Creating user")
        user = await self._user_repository.create(obj_in=user_in, with_commit=False)
        logger.debug("User created")

        return user

    @logging_function_info(logger=logger, description="Authenticate user")
    async def authenticate_user(
        self,
        login: str,
        password: str,
    ):
        return await self._user_repository.authenticate(
            login=login, password=password
        )

    @staticmethod
    def register(db: AsyncSession):
        return UserService(db=db)

    @staticmethod
    def register_deps():
        return Annotated[UserService, Depends(get_user_service)]


async def get_user_service(db: Annotated[AsyncSession, Depends(get_db)]):
    return UserService(db=db)
