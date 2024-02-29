class InvalidURLException(Exception):
    """
    Raised when the given URL is invalid.
    """

    def __init__(self, url: bytes | str, status_code: int):
        msg = f"Incorrect URL returned with [{status_code}]: {url}."
        super().__init__(msg)


class InvalidArgumentException(Exception):
    """
    Raised when the given argument is invalid.
    """

    def __init__(self, msg: str):
        super().__init__(msg)


class InvalidDatabaseException(Exception):
    """
    Raised when there is an invalid database operation.
    """

    def __init__(self, msg: str):
        super().__init__(msg)
