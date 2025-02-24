from datetime import datetime
from typing import Annotated
from uuid import UUID, uuid4

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.decorators.logger import logging_function_info
from app.common.deps import get_db
from app.common.logger import LoggerManager
from app.config.error_codes import ErrorCodes
from app.config.exception import BackendException
from app.modules.referal_code.models import CodeModel
from app.modules.referal_code.repositories import CodeRepository
from app.modules.referal_code.schemas import CodeCreate
from app.modules.user.repositories import UserRepository

logger = LoggerManager.get_user_logger()


class CodeService:
    def __init__(self, db: AsyncSession):
        self._code_repository = CodeRepository(db=db)
        self._user_repository = UserRepository(db=db)
        self.db = db

    @logging_function_info(logger=logger, description="Get code by user sid")
    async def get_code_by_user_sid(
        self, user_sid: UUID
    ) -> CodeModel | None:
        code = await self._code_repository.get_by_user_sid(user_sid=user_sid)
        if code:
            return code
        else:
            raise BackendException(ErrorCodes.CODE_NOT_FOUND, cause="Код для текущего юзера не найден")

    @logging_function_info(logger=logger, description="Create user's code")
    async def create_user_code(
        self, user_sid: UUID, lifetime: datetime,
    ) -> CodeModel | None:
        logger.debug(f"Check existing code for user: {user_sid}")
        if await self._code_repository.get_by_user_sid(
            user_sid=user_sid
        ):
            raise BackendException(ErrorCodes.CODE_ALREADY_EXISTS, cause="Код для текущего юзера уже существует")

        logger.debug(f"Creating code for user: {user_sid}")
        code_in = CodeCreate(
            user_sid=user_sid,
            value=str(uuid4()),
            lifetime=lifetime,
        )
        return await self._code_repository.create(obj_in=code_in)

    @logging_function_info(logger=logger, description="Delete user's code")
    async def delete_user_code(
        self, user_sid: UUID,
    ) -> CodeModel | None:
        logger.debug(f"Check existing code for user: {user_sid}")
        code = await self._code_repository.get_by_user_sid(
                user_sid=user_sid
        )
        if not code:
            raise BackendException(ErrorCodes.CODE_NOT_FOUND, cause="Код для текущего юзера не найден")

        logger.debug(f"Removing code for user: {user_sid}")
        return await self._code_repository.delete(sid=code.sid)

    @logging_function_info(logger=logger, description="Get code user's email")
    async def get_code_by_user_email(
        self, email: str
    ) -> CodeModel | None:
        logger.debug(f"Check existing user email: {email}")
        user = await self._user_repository.get_by_email(
            email=email
        )

        if not user:
            raise BackendException(ErrorCodes.USER_NOT_FOUND, cause="User не найден")

        logger.debug(f"Getting code for user with email: {email}")
        code = await self._code_repository.get_by_user_sid(user_sid=user.sid)
        if not code:
            raise BackendException(ErrorCodes.CODE_NOT_FOUND, cause="Код для текущего юзера не найден")
        return code

    @staticmethod
    def register(db: AsyncSession):
        return CodeService(db=db)

    @staticmethod
    def register_deps():
        return Annotated[CodeService, Depends(get_code_service)]


async def get_code_service(db: Annotated[AsyncSession, Depends(get_db)]):
    return CodeService(db=db)
