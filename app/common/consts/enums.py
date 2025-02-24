from enum import Enum


class StringEnum(str, Enum):
    def __str__(self):
        return self.value

    def __repr__(self):
        return self.value


class LoggerFormatEnum(StringEnum):
    BASE = "%(asctime)s - [%(levelname)s] - %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"


class LoggerLevelEnum(StringEnum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class LoggerNameEnum(StringEnum):
    SECURITY = "SECURITY"
    CRUD = "CRUD"
    BASE = "BASE"
    USER = "USER"
    CODE = "CODE"
