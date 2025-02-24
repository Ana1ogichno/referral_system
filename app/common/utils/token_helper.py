import uuid
from datetime import timedelta
from uuid import UUID

from jose import jwt

from app.common.schemas import TokenData
from app.common.utils import CustomDateTime
from app.config.db.session import DBSessionManager
from app.config.error_codes import ErrorCodes
from app.config.exception import BackendException
from app.config.settings import settings


class TokenHelper:
    def __init__(self):
        self.db_session_manager = DBSessionManager.register()
        self.redis_conn = self.db_session_manager.get_redis()

    def create_token(
            self,
            data: dict,
            expires_delta: timedelta | None,
            jti: UUID,
            refresh: bool = False,
    ) -> str:
        to_encode = data.copy()

        if isinstance(expires_delta, timedelta):
            expire = CustomDateTime.get_datetime_w_timezone() + expires_delta
        else:
            expire = CustomDateTime.get_datetime_w_timezone() + timedelta(minutes=15)

        to_encode.update({"exp": expire, "jti": str(jti)})

        if refresh:
            to_encode.update({"token": "refresh"})
        else:
            to_encode.update({"token": "access"})

        encoded_jwt = jwt.encode(
            to_encode, settings.project.TOKEN_SECRET_KEY, algorithm=settings.project.ALGORITHM
        )

        return encoded_jwt

    def token_payload(self, token: str, refresh: bool) -> TokenData:
        payload = jwt.decode(
            token, settings.project.TOKEN_SECRET_KEY, algorithms=[settings.project.ALGORITHM]
        )

        if refresh:
            if payload.get("token") != "refresh":
                raise BackendException(error=ErrorCodes.BAD_REFRESH_TOKEN)
        else:
            if payload.get("token") != "access":
                raise BackendException(error=ErrorCodes.BAD_ACCESS_TOKEN)

        sid: str = payload.get("sub")
        permissions: list[str] = payload.get("permissions")

        if not sid:
            raise BackendException(error=ErrorCodes.INCORRECT_CREDENTIALS)

        token_jti: str = payload.get("jti")
        token_key_died = self.redis_conn.get(f"{sid}:{token_jti}")

        if token_key_died != b"False":
            if refresh:
                raise BackendException(error=ErrorCodes.BAD_REFRESH_TOKEN)
            raise BackendException(error=ErrorCodes.BAD_ACCESS_TOKEN)

        return TokenData(sid=sid, jti=token_jti, permissions=permissions)

    def create_token_pair(self, payload: dict) -> tuple[str, str]:
        access_jti, refresh_jti = uuid.uuid4(), uuid.uuid4()

        access_token = self.create_token(
            data=payload,
            expires_delta=timedelta(seconds=settings.project.ACCESS_TOKEN_EXPIRE_SECONDS),
            jti=access_jti,
            refresh=False,
        )
        refresh_token = self.create_token(
            data=payload,
            expires_delta=timedelta(seconds=settings.project.REFRESH_TOKEN_EXPIRE_SECONDS),
            jti=refresh_jti,
            refresh=True,
        )

        self.redis_conn.setex(
            name=f"{payload.get('sub')}:{access_jti}",
            time=settings.project.ACCESS_TOKEN_EXPIRE_SECONDS,
            value="False",
        )
        self.redis_conn.setex(
            name=f"{payload.get('sub')}:{refresh_jti}",
            time=settings.project.REFRESH_TOKEN_EXPIRE_SECONDS,
            value="False",
        )

        return access_token, refresh_token

    async def create_access_key(
            self,
            table_number: int,
            device_id: str,
    ) -> str:
        data = {"table_number": table_number, "device_id": device_id}

        encoded_jwt = jwt.encode(
            data, settings.project.TOKEN_SECRET_KEY, algorithm=settings.project.ALGORITHM
        )

        return encoded_jwt


token_helper = TokenHelper()
