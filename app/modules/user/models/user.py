from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.common.models import CoreModel
from app.config.db.postgres.schemas import Schemas
from app.config.db.postgres.table_args import table_args

if TYPE_CHECKING:
    from app.modules.referal_code.models import CodeModel


class UserModel(CoreModel):
    __table_args__ = table_args(schema=Schemas.USERS)

    sid: Mapped[UUID] = mapped_column(
        primary_key=True,
        default=lambda: uuid4().hex,
        use_existing_column=True,
        unique=True,
    )
    email: Mapped[str] = mapped_column(index=True, unique=True, comment="email of user")
    hashed_password: Mapped[str] = mapped_column(comment="password")

    code: Mapped["CodeModel"] = relationship(
        back_populates="user"
    )

    referrer: Mapped["UserModel"] = relationship(
        secondary="users.invitation",
        primaryjoin="UserModel.sid==users.invitation.c.referral",
        secondaryjoin="UserModel.sid==users.invitation.c.referrer",
        back_populates="referrals"
    )

    referrals: Mapped[list["UserModel"]] = relationship(
        secondary="users.invitation",
        primaryjoin="UserModel.sid==users.invitation.c.referrer",
        secondaryjoin="UserModel.sid==users.invitation.c.referral",
        back_populates="referrer"
    )
