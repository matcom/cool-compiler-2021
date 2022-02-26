# MESSAGES
GENERIC_ERR_TYPE = "Unhandled Error"
GENERIC_ERR_MESSAGE = ""
FILE_INPUT_ERROR = "File input error"


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
        self, line: int = 0, column: int = 0
    ):
        super().__init__(line, column, GENERIC_ERR_TYPE, GENERIC_ERR_MESSAGE)


class InvalidInputFileError(BaseError):
    """
    Reported when input file is invalid.
    """

    def __init__(self, path: str) -> None:
        super.__init__(0, 0, FILE_INPUT_ERROR,
                       f"File `{path}` is not a valid file.")
