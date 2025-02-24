from enum import Enum


class ErrorCodes(Enum):
    """
    Ошибка в формате: имя = (код, HTTP код, описание)
    """

    # common
    UNDEFINED = (0, 500, "Неизвестная ошибка")
    BAD_REFRESH_TOKEN = (1, 401, "Невалидный refresh token")
    BAD_ACCESS_TOKEN = (2, 401, "Невалидный access token")
    NOT_UNIQUE = (3, 400, "Не уникальные поле(я) при создании")
    # users
    NOT_ALLOWED = (100, 405, "Доступ запрещен")
    INCORRECT_CREDENTIALS = (101, 401, "Неверные логин/пароль")
    USER_DEACTIVATED = (102, 403, "Учётная запись заблокирована")
    LOGIN_ALREADY_EXISTS = (102, 400, "Пользователь с данным login уже существует")
