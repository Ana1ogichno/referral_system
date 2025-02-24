from datetime import datetime

import pytz

from app.config.settings import settings


class CustomDateTime:
    @staticmethod
    def get_datetime() -> datetime:
        return datetime.now().replace(microsecond=0)

    @staticmethod
    def get_datetime_w_timezone() -> datetime:
        return (
            datetime.now()
            .replace(microsecond=0)
            .astimezone(pytz.timezone(settings.postgres.TZ))
        )
