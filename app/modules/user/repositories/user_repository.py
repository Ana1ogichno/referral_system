from sqlalchemy import select, Result
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.base import ExecutableOption

from app.common.decorators.logger import logging_function_info
from app.common.logger import LoggerManager
from app.common.services import CrudRepository
from app.common.utils import password_helper
from app.config.error_codes import ErrorCodes
from app.config.exception import BackendException
from app.modules.user.models import UserModel
from app.modules.user.schemas import UserCreate, UserUpdate

logger = LoggerManager.get_user_logger()


class UserRepository(CrudRepository[UserModel, UserCreate, UserUpdate]):
    """Класс для всех взаимодействий с таблицей User"""

    def __init__(self, db: AsyncSession):
        super().__init__(UserModel, db)

    @logging_function_info(logger=logger)
    async def get_by_login(
        self, login: str, custom_options: tuple[ExecutableOption, ...] = None
    ) -> UserModel | None:
        query = select(self.model).where(self.model.login == login)

        if isinstance(custom_options, tuple):
            query = query.options(*custom_options)

        result: Result = await self.db.execute(query)
        return result.scalars().first()

    @logging_function_info(logger=logger)
    async def create(self, obj_in: UserCreate, with_commit: bool = True) -> UserModel:
        try:
            obj = obj_in.model_dump()
            obj["hashed_password"] = password_helper.get_password_hash(obj_in.password)
            obj.pop("password")
            db_obj = self.model(**obj)

            self.db.add(db_obj)

            if with_commit:
                await self.db.commit()
                await self.db.refresh(db_obj)
            else:
                await self.db.flush()

            return db_obj
        except IntegrityError as e:
            raise BackendException(error=ErrorCodes.NOT_UNIQUE) from e

    @logging_function_info(logger=logger)
    async def authenticate(
        self,
        login: str,
        password: str,
        custom_options: tuple[ExecutableOption, ...] = None,
    ) -> UserModel | None:
        user = await self.get_by_login(login=login, custom_options=custom_options)

        if not user:
            return None
        if not password_helper.verify_password(password, user.hashed_password):
            return None

        return user
