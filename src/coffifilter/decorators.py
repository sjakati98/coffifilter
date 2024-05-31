import functools
from .client import Client


def coffi_filter(filter_string: str):
    """
    Decorator that checks for the presence of a given string in Redis before calling the decorated function.

    Args:
        filter_string (str): The string to check for in Redis.
        host (str, optional): The hostname or IP address of the Redis server. Defaults to 'localhost'.
        port (int, optional): The port number of the Redis server. Defaults to 6379.
        db (int, optional): The database number to use. Defaults to 0.
        password (str, optional): The password for the Redis server. Defaults to None.

    Returns:
        callable: The decorated function.
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                Client()._check_tool_enabled(filter_string)
            except ValueError as e:
                return str(e)
            return func(*args, **kwargs)

        return wrapper

    return decorator
