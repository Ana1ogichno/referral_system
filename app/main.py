from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi_pagination import add_pagination
from starlette.middleware.sessions import SessionMiddleware

from app.config.docs_metadata import tags_metadata, app_description
from app.config.exception import (
    BackendException,
    backend_exception_handler,
    handle_exceptions_middleware,
    validation_exception_handler,
)
from app.config.settings import settings
from app.router import api_router

origins = [
    "*"
]

app = FastAPI(
    debug=True,
    title=settings.project.PROJECT_NAME,
    version=settings.project.PROJECT_VERSION,
    openapi_url=f"{settings.project.API_V1_STR}/openapi.json",
    openapi_tags=tags_metadata,
    exception_handlers={BackendException: backend_exception_handler},
    description=app_description,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(SessionMiddleware, secret_key=settings.project.OAUTH_SECRET_KEY)

app.middleware("http")(handle_exceptions_middleware)
app.exception_handler(RequestValidationError)(validation_exception_handler)

app.include_router(api_router, prefix=settings.project.API_V1_STR)
add_pagination(app)
