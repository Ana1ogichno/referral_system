from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.common.models import CoreModel
from app.config.db.postgres.schemas import Schemas
from app.config.db.postgres.table_args import table_args


class InvitationModel(CoreModel):
    __table_args__ = table_args(schema=Schemas.USERS)

    referrer: Mapped[UUID] = mapped_column(
        ForeignKey("users.user.sid"), primary_key=True
    )
    referral: Mapped[UUID] = mapped_column(
        ForeignKey("users.user.sid"), primary_key=True
    )
