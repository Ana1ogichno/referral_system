from typing import Annotated

from fastapi import Depends
from redis import Redis
from sqlalchemy.ext.asyncio import async_sessionmaker

from app.config.db.postgres.engine import db_engine
from app.config.settings import settings


class DBSessionManager:
    def __init__(self):
        self.postgres_session = async_sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=db_engine
        )
        self.redis_session = Redis(host=settings.redis.REDIS_HOST, port=settings.redis.REDIS_PORT)

    def get_psql(self):
        return self.postgres_session()

    def get_redis(self):
        return self.redis_session

    @staticmethod
    def register():
        return DBSessionManager()

    @staticmethod
    def register_deps():
        return Annotated[DBSessionManager, Depends(get_db_session_manager)]


async def get_db_session_manager():
    return DBSessionManager()
