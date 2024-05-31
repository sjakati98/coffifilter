# pylint: disable=invalid-name
import redis  # type: ignore
from .helpers import singleton


@singleton
class Client:
    """
    Client class for the CoffiFilter Service.

    Args:

        redis_host (str): Redis host. This is the host where the Redis server is running.
        redis_port (int): Redis port. This is the port where the Redis server is running.
        redis_db (int): Redis database. This is the database number to connect to.
        redis_password (str): Redis password. This is the password to connect to the Redis server.

    """

    def __init__(
        self,
        redis_host="localhost",
        redis_port=6379,
        redis_db=0,
        redis_password=None,
    ):
        self.redis_host = redis_host
        self.redis_port = redis_port
        self.redis_db = redis_db
        self.redis_password = redis_password

    def _check_tool_enabled(self, filter_string) -> None:
        """
        Check if the tool is enabled in the Redis database.

        Args:
            filter_string (str): The name of the tool to check.

        Raises:
            ValueError: If the tool is not enabled.
        """
        # Get the value associated with the filter string from the Redis database
        value = self.get_value_from_redis(
            filter_string,
            self.redis_host,
            self.redis_port,
            self.redis_db,
            self.redis_password,
        )

        # Convert the value to a boolean
        enabled = self.str_to_bool(value)

        # Check if the tool is enabled
        if not enabled:
            raise ValueError(f"Tool '{filter_string}' is not enabled")

    @staticmethod
    def get_value_from_redis(key, host="localhost", port=6379, db=0, password=None):
        """
        Retrieves the value associated with the given key from a Redis database.

        Args:
            key (str): The key to look up in the Redis database.
            host (str, optional): The hostname or IP address of the Redis server. Defaults to 'localhost'.
            port (int, optional): The port number of the Redis server. Defaults to 6379.
            db (int, optional): The database number to use. Defaults to 0.
            password (str, optional): The password for the Redis server. Defaults to None.

        Returns:
            str or None: The value associated with the given key, or None if the key is not found.
        """
        # Create a Redis connection
        r = redis.Redis(host=host, port=port, db=db, password=password)

        # Check if the key exists
        if r.exists(key):
            # Get the value associated with the key
            value = r.get(key)

            # Decode the value from bytes to string
            value = value.decode("utf-8")

            return value

        return None

    @staticmethod
    def str_to_bool(string):
        """
        Converts a string to a boolean value.

        Args:
            string (str): The input string to be converted.

        Returns:
            bool: The boolean value represented by the input string.

        Raises:
            ValueError: If the input string is not one of the expected values.
        """
        # Define a mapping of valid string values to their corresponding boolean values
        true_values = {"true", "True", "TRUE", "t"}
        false_values = {"false", "False", "FALSE", "f"}

        # Convert the input string to lowercase for case-insensitive comparison
        string = string.lower()

        # Check if the input string is a valid true value
        if string in true_values:
            return True

        # Check if the input string is a valid false value
        if string in false_values:
            return False

        raise ValueError(f"Invalid input: '{string}' is not a valid boolean string")
