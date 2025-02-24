from datetime import datetime
from uuid import UUID

from pydantic import ConfigDict

from app.common.decorators.partial_schema import partial_schema
from app.common.schemas import CoreSchema


class InvitationBase(CoreSchema):
    model_config = ConfigDict(from_attributes=True)

    referrer: UUID
    referral: UUID


class InvitationCreate(InvitationBase):
    pass


@partial_schema
class InvitationUpdate(InvitationBase):
    pass


class InvitationInDBBase(InvitationBase):
    created_at: datetime
    updated_at: datetime
