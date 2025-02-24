from typing import Annotated
from uuid import UUID

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.base import ExecutableOption

from app.common.decorators.logger import logging_function_info
from app.common.deps import get_db
from app.common.logger import LoggerManager
from app.common.utils.sqlalchemy_options import UserCustomOptions
from app.config.error_codes import ErrorCodes
from app.config.exception import BackendException
from app.modules.referal_code.repositories import CodeRepository
from app.modules.user.models import UserModel
from app.modules.user.repositories import UserRepository
from app.modules.user.repositories.invitation import InvitationRepository
from app.modules.user.schemas import UserCreate
from app.modules.user.schemas.invitation import InvitationCreate

logger = LoggerManager.get_user_logger()


class UserService:
    def __init__(self, db: AsyncSession):
        self._user_repository = UserRepository(db=db)
        self._code_repository = CodeRepository(db=db)
        self._invitation_repository = InvitationRepository(db=db)
        self.db = db

    @logging_function_info(logger=logger, description="Get user by email in db")
    async def get_user_by_email(
        self, email: str, custom_options: tuple[ExecutableOption, ...] = None
    ) -> UserModel | None:
        return await self._user_repository.get_by_email(
            email=email, custom_options=custom_options
        )

    @logging_function_info(logger=logger, description="Get user by sid in db")
    async def get_user_by_sid(
        self, sid: UUID
    ) -> UserModel | None:
        return await self._user_repository.get_one(sid=sid)

    @logging_function_info(logger=logger, description="Create user in db")
    async def create_user(self, user_in: UserCreate):
        logger.debug("Get user by email")
        user = await self._user_repository.get_by_email(email=user_in.email)

        if user:
            logger.warning("User already exist")
            raise BackendException(ErrorCodes.EMAIL_ALREADY_EXISTS)

        logger.debug("Creating user")
        user = await self._user_repository.create(obj_in=user_in, with_commit=False)
        logger.debug("User created")

        return user

    @logging_function_info(logger=logger, description="Create user in db")
    async def create_user_by_code(self, code: str, user_in: UserCreate):

        logger.debug("Validate code")
        code_db = await self._code_repository.get_by_value(value=code)
        if not code_db:
            raise BackendException(ErrorCodes.CODE_NOT_FOUND, cause="Такой код не найден")

        logger.debug("Get user by email")

        if await self._user_repository.get_by_email(email=user_in.email):
            logger.warning("User already exist")
            raise BackendException(ErrorCodes.EMAIL_ALREADY_EXISTS)

        logger.debug("Creating user")
        user = await self._user_repository.create(obj_in=user_in)
        logger.debug("User created")

        await self.db.refresh(code_db)
        logger.debug("Creating invitation record")
        invitation_in = InvitationCreate(
            referrer=code_db.user_sid,
            referral=user.sid
        )

        await self._invitation_repository.create(obj_in=invitation_in)
        logger.debug("Invitation record created")
        await self.db.refresh(user)

        return user

    @logging_function_info(logger=logger, description="Authenticate user")
    async def authenticate_user(
        self,
        email: str,
        password: str,
    ):
        return await self._user_repository.authenticate(
            email=email, password=password
        )

    @logging_function_info(logger=logger, description="Get user's referrals")
    async def get_user_referrals(self, user_sid: UUID):
        logger.debug("Get user's referrals")
        user = await self._user_repository.get_referrals_by_user_sid(
            user_sid=user_sid,
            custom_options=UserCustomOptions.with_referrals()
        )
        return user

    @staticmethod
    def register(db: AsyncSession):
        return UserService(db=db)

    @staticmethod
    def register_deps():
        return Annotated[UserService, Depends(get_user_service)]


async def get_user_service(db: Annotated[AsyncSession, Depends(get_db)]):
    return UserService(db=db)
