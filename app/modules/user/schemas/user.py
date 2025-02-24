from datetime import datetime
from uuid import UUID

from pydantic import ConfigDict

from app.common.decorators.partial_schema import partial_schema
from app.common.schemas import CoreSchema


class UserBase(CoreSchema):
    model_config = ConfigDict(from_attributes=True)

    login: str


class UserCreate(UserBase):
    password: str


@partial_schema
class UserUpdate(UserBase):
    login: str


class UserInDBBase(UserBase):
    sid: UUID
    hashed_password: str

    created_at: datetime
    updated_at: datetime
