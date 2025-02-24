from fastapi import HTTPException
from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.common.logger import LoggerManager
from app.config.error_codes import ErrorCodes

logger = LoggerManager.get_base_logger()


class BackendException(HTTPException):
    cause: str = ""

    def __init__(self, error: ErrorCodes, *, cause: str = ""):
        self.error_code = error.value[0]
        self.status_code = error.value[1]
        self.description = error.value[2]
        self.cause = cause


def backend_exception_handler(request: Request, exc: BackendException):
    message = {"code": exc.error_code, "detail": exc.description, "cause": exc.cause}
    return JSONResponse(message, status_code=exc.status_code)


async def handle_exceptions_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as error:
        logger.warning(f"{error}")
        undefined_error = BackendException(ErrorCodes.UNDEFINED)

        return JSONResponse(
            content={
                "code": undefined_error.error_code,
                "detail": undefined_error.description,
            },
            status_code=undefined_error.status_code,
        )


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    unprocessable_entity_error = BackendException(
        ErrorCodes.HTTP_422_UNPROCESSABLE_ENTITY
    )
    exc_str = f"{exc}".replace("   ", " ")
    logger.error(f"{request}: {exc_str}")
    content = {
        "status_code": unprocessable_entity_error.status_code,
        "message": unprocessable_entity_error.description,
        "data": exc.__dict__.get("_errors", []),
    }
    return JSONResponse(
        content=content, status_code=unprocessable_entity_error.status_code
    )
