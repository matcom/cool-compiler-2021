class BaseError:
    """COOL error"""

    def __init__(self, line: int, column: int, err_type: str, err_message: str):
        self.line = line
        self.column = column
        self.err_type = err_type
        self.err_message = err_message

    def __str__(self) -> str:
        return f"({self.line}, {self.column}) - {self.err_type}: {self.err_message}"

    __repr__ = __str__


class GenericAppError(BaseError):
    """A generic app error used for unknown errors"""

    def __init__(
        self, line: int = 0, column: int = 0, err_message: str = "UnknownError"
    ):
        CoolError.__init__(self, line, column, err_message)
