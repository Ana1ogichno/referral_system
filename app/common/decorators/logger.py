import logging


def logging_function_info(logger: logging.Logger, description: str | None = None):
    def decorator(func):
        def wrapper(*args, **kwargs):
            if description:
                logger.info(f"Start: {func.__name__}, description: {description}")
            else:
                logger.info(f"Start: {func.__name__}")

            result = func(*args, **kwargs)

            return result

        return wrapper

    return decorator
