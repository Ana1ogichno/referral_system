from typing import Generic, TypeVar, Type, Any, Sequence

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel as PydanticBaseModel
from sqlalchemy import select, Result, delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.base import ExecutableOption

from app.common.decorators.logger import logging_function_info
from app.common.logger import LoggerManager
from app.common.models import CoreModel
from app.config.error_codes import ErrorCodes
from app.config.exception import BackendException

ModelType = TypeVar("ModelType", bound=CoreModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=PydanticBaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=PydanticBaseModel)

logger = LoggerManager.get_crud_logger()


class CrudRepository(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType], db: AsyncSession):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).

        **Parameters**

        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model
        self.db = db

    @logging_function_info(logger=logger)
    async def get_one(
        self, sid: Any, custom_options: tuple[ExecutableOption, ...] = None
    ) -> ModelType | None:
        query = select(self.model).where(self.model.sid == sid)  # noqa

        if custom_options is not None:
            query = query.options(*custom_options)

        result: Result = await self.db.execute(query)
        return result.scalars().first()

    @logging_function_info(logger=logger)
    async def get_all(
        self, custom_options: tuple[ExecutableOption, ...] = None
    ) -> Sequence[ModelType]:
        query = select(self.model)

        if isinstance(custom_options, tuple):
            query = query.options(*custom_options)

        result: Result = await self.db.execute(query)
        return result.scalars().all()

    @logging_function_info(logger=logger)
    async def create(
        self, *, obj_in: CreateSchemaType, with_commit: bool = True
    ) -> ModelType:
        try:
            db_obj = self.model(**obj_in.model_dump())

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
    async def update(
        self,
        *,
        db_obj: ModelType,
        obj_in: UpdateSchemaType | dict[str, Any],
    ) -> ModelType:
        try:
            obj_data = jsonable_encoder(db_obj)

            if isinstance(obj_in, dict):
                update_data = obj_in
            else:
                update_data = obj_in.model_dump(exclude_unset=True)

            for field in obj_data:
                if field in update_data:
                    setattr(db_obj, field, update_data[field])

            self.db.add(db_obj)

            await self.db.commit()
            await self.db.refresh(db_obj)

            return db_obj
        except IntegrityError as e:
            raise BackendException(error=ErrorCodes.NOT_UNIQUE) from e

    @logging_function_info(logger=logger)
    async def delete(self, *, sid: Any, with_commit: bool = True) -> ModelType | None:
        query = select(self.model).where(self.model.sid == sid)  # noqa
        result: Result = await self.db.execute(query)
        obj = result.scalars().first()

        await self.db.delete(obj)

        if with_commit:
            await self.db.commit()
        else:
            await self.db.flush()

        return obj
