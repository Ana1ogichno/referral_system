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
    login: Mapped[str] = mapped_column(index=True, unique=True, comment="email/referral_code")
    hashed_password: Mapped[str] = mapped_column(comment="password")

    code: Mapped["CodeModel"] = relationship(
        back_populates="user"
    )
