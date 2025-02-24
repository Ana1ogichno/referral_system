from typing import Annotated
from uuid import UUID

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.base import ExecutableOption

from app.common.decorators.logger import logging_function_info
from app.common.deps import get_db
from app.common.logger import LoggerManager
from app.modules.referal_code.models import CodeModel
from app.modules.referal_code.repositories import CodeRepository

logger = LoggerManager.get_user_logger()


class CodeService:
    def __init__(self, db: AsyncSession):
        self._code_repository = CodeRepository(db=db)
        self.db = db

    @logging_function_info(logger=logger, description="Get code by user sid")
    async def get_code_by_user_sid(
        self, user_sid: UUID, custom_options: tuple[ExecutableOption, ...] = None
    ) -> CodeModel | None:
        return await self._code_repository.get_by_user_sid(
            user_sid=user_sid, custom_options=custom_options
        )

    @staticmethod
    def register(db: AsyncSession):
        return CodeService(db=db)

    @staticmethod
    def register_deps():
        return Annotated[CodeService, Depends(get_code_service)]


async def get_code_service(db: Annotated[AsyncSession, Depends(get_db)]):
    return CodeService(db=db)
