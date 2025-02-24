from fastapi import APIRouter

from app.modules.security.routers import auth_router
from app.modules.user.routers import users_router
from app.modules.referal_code.routers import codes_router


api_router = APIRouter()

api_router.include_router(auth_router, tags=["Auth"], prefix="/auth")
api_router.include_router(users_router, tags=["User"], prefix="/user")
api_router.include_router(codes_router, tags=["Code"], prefix="/code")
