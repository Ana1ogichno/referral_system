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
    USER_NOT_FOUND = (102, 404, "Пользователь не найден")
    EMAIL_ALREADY_EXISTS = (102, 400, "Пользователь с данным email уже существует")
    # codes
    CODE_ALREADY_EXISTS = (200, 400, "У вас уже есть реферальный код")
    CODE_NOT_FOUND = (201, 404, "Код не найден")
