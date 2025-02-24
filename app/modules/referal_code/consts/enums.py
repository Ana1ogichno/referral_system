from enum import Enum


class RoutersPath(str, Enum):
    my = "/my"
    create = "/create"
    delete = "/delete"
    by_email = "/{email}"
