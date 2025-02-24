from datetime import datetime
from uuid import UUID

from pydantic import ConfigDict

from app.common.decorators.partial_schema import partial_schema
from app.common.schemas import CoreSchema


class CodeBase(CoreSchema):
    model_config = ConfigDict(from_attributes=True)

    value: str
    lifetime: datetime


class CodeCreate(CodeBase):
    user_sid: UUID


@partial_schema
class CodeUpdate(CodeBase):
    pass


class CodeInDBBase(CodeBase):
    sid: UUID
    created_at: datetime
    updated_at: datetime
