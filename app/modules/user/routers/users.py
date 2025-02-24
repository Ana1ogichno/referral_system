from typing import Annotated

from fastapi import APIRouter, Depends

from app.common.deps import oauth2_scheme
from app.common.deps.current_user import get_current_user
from ..consts import RoutersPath
from ..schemas import UserInDBBase, UserReferrals
from ..services import UserService

router = APIRouter()


@router.get(path=RoutersPath.me, response_model=UserInDBBase)
async def get_user_me(
    current_user: Annotated[UserInDBBase, Depends(get_current_user)],
    token: Annotated[str, Depends(oauth2_scheme)],
) -> UserInDBBase:
    """
    Get current user info.
    """

    return current_user


@router.get(path=RoutersPath.referrals, response_model=UserReferrals)
async def get_my_referrals(
    current_user: Annotated[UserInDBBase, Depends(get_current_user)],
    user_service: UserService.register_deps(),
) -> UserReferrals:
    """
    Get current user info.
    """

    return await user_service.get_user_referrals(user_sid=current_user.sid)
