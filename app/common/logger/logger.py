import logging
import sys

from app.common.consts.enums import LoggerFormatEnum, LoggerLevelEnum, LoggerNameEnum


class LoggerManager:
    # Base logger
    __base_log_name: str = LoggerNameEnum.BASE.value
    __base_log_level: str = LoggerLevelEnum.INFO.value
    __base_log_format: str = LoggerFormatEnum.BASE.value

    # Crud logger
    __crud_log_name: str = LoggerNameEnum.CRUD.value
    __crud_log_level: str = LoggerLevelEnum.INFO.value
    __crud_log_format: str = LoggerFormatEnum.BASE.value

    # Security logger
    __security_log_name: str = LoggerNameEnum.SECURITY.value
    __security_log_level: str = LoggerLevelEnum.INFO.value
    __security_log_format: str = LoggerFormatEnum.BASE.value

    # User logger
    __user_log_name: str = LoggerNameEnum.USER.value
    __user_log_level: str = LoggerLevelEnum.INFO.value
    __user_log_format: str = LoggerFormatEnum.BASE.value

    @staticmethod
    def __configure_logger(logger: logging.Logger, level: str, format_str: str) -> None:
        logger.setLevel(level)
        logger.propagate = False

        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(level)
        console_handler.setFormatter(logging.Formatter(format_str))
        logger.addHandler(console_handler)

    @classmethod
    def __get_logger(cls, name: str, level: str, format_str: str) -> logging.Logger:
        logger = logging.getLogger(name)
        if not logger.hasHandlers():
            cls.__configure_logger(
                logger=logger,
                level=level,
                format_str=format_str,
            )
        return logger

    @classmethod
    def get_base_logger(cls) -> logging.Logger:
        return cls.__get_logger(
            name=cls.__base_log_name,
            level=cls.__base_log_level,
            format_str=cls.__base_log_format,
        )

    @classmethod
    def get_crud_logger(cls) -> logging.Logger:
        return cls.__get_logger(
            name=cls.__crud_log_name,
            level=cls.__crud_log_level,
            format_str=cls.__crud_log_format,
        )

    @classmethod
    def get_security_logger(cls) -> logging.Logger:
        return cls.__get_logger(
            name=cls.__security_log_name,
            level=cls.__security_log_level,
            format_str=cls.__security_log_format,
        )

    @classmethod
    def get_user_logger(cls) -> logging.Logger:
        return cls.__get_logger(
            name=cls.__user_log_name,
            level=cls.__user_log_level,
            format_str=cls.__user_log_format,
        )
