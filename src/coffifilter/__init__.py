"""CoffiFilter."""

from .client import Client
from .decorators import coffi_filter


def init(
    redis_host="localhost",
    redis_port=6379,
    redis_db=0,
    redis_password=None,
):
    """
    Initialize the CoffiFilter client.

    Args:

        redis_host (str): Redis host. This is the host where the Redis server is running.
        redis_port (int): Redis port. This is the port where the Redis server is running.
        redis_db (int): Redis database. This is the database number to connect to.
        redis_password (str): Redis password. This is the password to connect to the Redis server.

    Returns:

        Client: The client object for the CoffiFilter service.

    """

    return Client(
        redis_host=redis_host,
        redis_port=redis_port,
        redis_db=redis_db,
        redis_password=redis_password,
    )
