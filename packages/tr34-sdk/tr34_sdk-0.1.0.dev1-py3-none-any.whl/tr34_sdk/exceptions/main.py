
class NoApiKey(Exception):
    def __init__(self, arg_name: str) -> None:
        self.msg = f"You need to set api key to access data with {arg_name} parameter"

    def __str__(self) -> str:
        return self.msg


class NoAdminAccessDisabled(Exception):
    def __init__(self, arg_name: str) -> None:
        self.msg = f"You need to set admin=True to access data with {arg_name} parameter"

    def __str__(self) -> str:
        return self.msg


class ResponseError(Exception):
    def __init__(self, code: int) -> None:
        if code == 403:
            self.msg = "Permission denied! Maybe your api key is wrong?"
        else:
            self.msg = f"Unhandled error with code {code}"

    def __str__(self) -> str:
        return self.msg


