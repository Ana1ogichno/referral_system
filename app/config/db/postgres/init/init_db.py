import logging

from sqlalchemy.ext.asyncio import AsyncSession

from app.config.settings import settings
from app.modules.user.schemas import UserCreate
from app.modules.user.services.user_service import UserService


async def init_db(db: AsyncSession) -> None:
    user_service = UserService(db)

    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables un-commenting the next line
    # Base.metadata.create_all(bind=engine)

    ########################
    # Init First SuperUser
    logging.info("Start Create Superuser")

    superuser = await user_service.get_user_by_email(
        email=settings.project.FIRST_SUPERUSER_LOGIN
    )

    if not superuser:
        user_in = UserCreate(
            email=settings.project.FIRST_SUPERUSER_LOGIN,
            password=settings.project.FIRST_SUPERUSER_PASSWORD,
        )

        await user_service.create_user(user_in=user_in)  # noqa: F841

    await db.commit()

    logging.info("End Create Superuser")
