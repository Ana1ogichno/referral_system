from sqlalchemy.orm import selectinload

from app.modules.user.models import UserModel


class UserCustomOptions:
    @staticmethod
    def with_referrals():
        return (
            selectinload(UserModel.referrals),
        )
