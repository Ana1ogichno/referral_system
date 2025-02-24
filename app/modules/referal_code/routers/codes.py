from typing import Annotated

from fastapi import APIRouter, Depends

from app.common.deps.current_user import get_current_user
from ..schemas import CodeInDBBase
from ..services import CodeService
from ...user.schemas import UserInDBBase

router = APIRouter()


@router.get(path="/my", response_model=CodeInDBBase)
async def get_user_me(
    current_user: Annotated[UserInDBBase, Depends(get_current_user)],
    code_service: CodeService.register_deps(),
) -> CodeInDBBase:
    """
    Get code of current user.
    """

    return await code_service.get_code_by_user_sid(user_sid=current_user.sid)
