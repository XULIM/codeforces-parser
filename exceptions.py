class InvalidURLException(Exception):
    def __init__(self, url: bytes | str, status_code: int):
        msg = f"Incorrect URL returned with [{status_code}]: {url}."
        super().__init__(msg)


class InvalidArgumentException(Exception):
    def __init__(self, msg: str):
        super().__init__(msg)
