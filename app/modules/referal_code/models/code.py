from uuid import UUID, uuid4

from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING

from app.common.models import CoreModel
from app.common.utils import CustomDateTime
from app.config.db.postgres.schemas import Schemas
from app.config.db.postgres.table_args import table_args


if TYPE_CHECKING:
    from app.modules.user.models import UserModel


class CodeModel(CoreModel):
    __table_args__ = table_args(schema=Schemas.CODES)

    sid: Mapped[UUID] = mapped_column(
        primary_key=True,
        default=lambda: uuid4().hex,
        use_existing_column=True,
        unique=True,
    )
    user_sid: Mapped[UUID] = mapped_column(
        ForeignKey("users.user.sid", ondelete="CASCADE"), primary_key=True
    )
    value: Mapped[str] = mapped_column(index=True, unique=True, comment="value of referral code")
    lifetime: Mapped[DateTime] = mapped_column(
        DateTime(timezone=False),
        default=CustomDateTime.get_datetime,
        comment="Lifetime of referral code"
    )

    # relations
    user: Mapped["UserModel"] = relationship(
        back_populates="code"
    )
