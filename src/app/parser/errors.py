
from app.shared.errors import BaseError


# Error Type
SYNTACTIC_ERROR = "SyntacticError"

# Error Message
UNEXPECTED_EOF = "Unexpected EOF"
UNEXPECTED_TOKEN = 'Unexpected token near or at "{}"'


class ParsingError(BaseError):
    def __init__(self, line: int, column: int, err_message: str):
        BaseError.__init__(self, line, column,
                           SYNTACTIC_ERROR, err_message)

    @staticmethod
    def UnexpectedEof(line: int, column: int):
        return ParsingError(line, column, UNEXPECTED_EOF)

    @staticmethod
    def UnexpectedToken(line: int, column: int, character: str):
        return ParsingError(line, column, UNEXPECTED_TOKEN.format(character))
