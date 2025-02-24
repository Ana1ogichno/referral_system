from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends
from starlette import status
from starlette.responses import JSONResponse

from app.common.deps.current_user import get_current_user
from app.common.schemas import Msg
from ..consts import RoutersPath
from ..schemas import CodeInDBBase
from ..services import CodeService
from ...user.schemas import UserInDBBase

router = APIRouter()


@router.get(path=RoutersPath.my, response_model=CodeInDBBase)
async def get_my_code(
    current_user: Annotated[UserInDBBase, Depends(get_current_user)],
    code_service: CodeService.register_deps(),
) -> CodeInDBBase:
    """
    Get code of current user.
    """

    return await code_service.get_code_by_user_sid(user_sid=current_user.sid)


@router.post(path=RoutersPath.create, response_model=CodeInDBBase)
async def create_my_code(
    lifetime: datetime,
    current_user: Annotated[UserInDBBase, Depends(get_current_user)],
    code_service: CodeService.register_deps(),
) -> CodeInDBBase:
    """
    Create code of current user.
    """

    return await code_service.create_user_code(user_sid=current_user.sid, lifetime=lifetime)


@router.delete(path=RoutersPath.create, response_model=Msg)
async def delete_my_code(
    current_user: Annotated[UserInDBBase, Depends(get_current_user)],
    code_service: CodeService.register_deps(),
) -> JSONResponse:
    """
    Remove code of current user.
    """

    await code_service.delete_user_code(user_sid=current_user.sid)

    return JSONResponse(
        content=Msg(msg="Удалено").model_dump(), status_code=status.HTTP_200_OK
    )


@router.get(path=RoutersPath.by_email, response_model=CodeInDBBase)
async def get_code_by_email(
    current_user: Annotated[UserInDBBase, Depends(get_current_user)],
    email: str,
    code_service: CodeService.register_deps(),
) -> CodeInDBBase:
    """
    Get code by user's email.
    """

    return await code_service.get_code_by_user_email(email=email)
