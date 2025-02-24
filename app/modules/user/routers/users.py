from typing import Annotated

from fastapi import APIRouter, Depends

from app.common.deps import oauth2_scheme
from app.common.deps.current_user import get_current_user
from ..schemas import UserInDBBase

router = APIRouter()


@router.get(path="/me", response_model=UserInDBBase)
async def get_user_me(
    current_user: Annotated[UserInDBBase, Depends(get_current_user)],
    token: Annotated[str, Depends(oauth2_scheme)],
) -> UserInDBBase:
    """
    Get current user info.
    """

    return current_user
