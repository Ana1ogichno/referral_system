from datetime import datetime

import pytz
from pydantic import BaseModel, model_validator, ConfigDict

from app.config.settings import settings


class CoreSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    @model_validator(mode="after")
    def format_datetime(self) -> "CoreSchema":
        fields = {
            k: v.replace(microsecond=0).astimezone(pytz.timezone(settings.postgres.TZ))
            for k, v in self.__dict__.items()
            if isinstance(v, datetime) and not v.tzinfo
        }
        for key, value in fields.items():
            setattr(self, key, value)
        return self
