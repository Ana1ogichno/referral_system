from uuid import UUID

from sqlalchemy import select, Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.base import ExecutableOption

from app.common.decorators.logger import logging_function_info
from app.common.logger import LoggerManager
from app.common.services import CrudRepository
from app.modules.referal_code.models import CodeModel
from app.modules.referal_code.schemas import CodeCreate, CodeUpdate

logger = LoggerManager.get_code_logger()


class CodeRepository(CrudRepository[CodeModel, CodeCreate, CodeUpdate]):
    """Класс для всех взаимодействий с таблицей Code"""

    def __init__(self, db: AsyncSession):
        super().__init__(CodeModel, db)

    @logging_function_info(logger=logger)
    async def get_by_user_sid(
        self, user_sid: UUID, custom_options: tuple[ExecutableOption, ...] = None
    ) -> CodeModel | None:
        query = select(self.model).where(self.model.user_sid == user_sid)

        if isinstance(custom_options, tuple):
            query = query.options(*custom_options)

        result: Result = await self.db.execute(query)
        return result.scalars().first()

    @logging_function_info(logger=logger)
    async def get_by_value(
            self, value: str, custom_options: tuple[ExecutableOption, ...] = None
    ) -> CodeModel | None:
        query = select(self.model).where(self.model.value == value)

        if isinstance(custom_options, tuple):
            query = query.options(*custom_options)

        result: Result = await self.db.execute(query)
        return result.scalars().first()

