from datetime import datetime
from uuid import UUID

from pydantic import ConfigDict, EmailStr

from app.common.decorators.partial_schema import partial_schema
from app.common.schemas import CoreSchema


class UserBase(CoreSchema):
    model_config = ConfigDict(from_attributes=True)

    email: EmailStr


class UserCreate(UserBase):
    password: str


@partial_schema
class UserUpdate(UserBase):
    pass


class UserInDBBase(UserBase):
    sid: UUID
    hashed_password: str

    created_at: datetime
    updated_at: datetime


class UserReferrals(CoreSchema):
    model_config = ConfigDict(from_attributes=True)
    sid: UUID
    referrals: list[UserInDBBase]
