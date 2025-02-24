from enum import Enum


class RoutersPath(str, Enum):
    register = "/register"
    register_by_code = "/{code}/register"
    login = "/login"
    refresh = "/refresh_token"
    logout = "/logout"

