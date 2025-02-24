import asyncio
import logging
import sys

sys.path = ["", ".."] + sys.path[1:]

from app.config.db.session import DBSessionManager  # noqa: E402
from app.config.db.postgres.init import init_db  # noqa E402
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def init_psql() -> None:
    session_manager = DBSessionManager.register()
    db = session_manager.get_psql()
    await init_db(db)
    await db.close()


async def main() -> None:
    logger.info("Creating initial data")
    await init_psql()
    logger.info("Initial data created")


if __name__ == "__main__":
    asyncio.run(main())
