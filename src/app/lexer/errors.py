
from app.shared.errors import BaseError


# Error Type
LEXICOGRAPHIC_ERROR = "LexicographicError"

# Error Message
EOF_IN_COMMENT = "EOF in comment"
UNEXPECTED_CHARACTER = 'ERROR "{}"'
UNTERMINATED_STRING_CONSTANT = "Unterminated string constant"
EOF_IN_STRING_CONSTANT = "EOF in string constant"
STRING_CONTAINS_NULL_CHAR = "String contains null character"


class LexicographicError(BaseError):
    def __init__(self, line: int, column: int, err_message: str):
        BaseError.__init__(self, line, column,
                           LEXICOGRAPHIC_ERROR, err_message)

    @staticmethod
    def EOFInComment(line: int, column: int):
        return LexicographicError(line, column, EOF_IN_COMMENT)

    @staticmethod
    def UnexpectedCharacter(line: int, column: int, character: str):
        return LexicographicError(line, column, UNEXPECTED_CHARACTER.format(character))

    @staticmethod
    def UnterminatedStringConstant(line: int, column: int):
        return LexicographicError(line, column, UNTERMINATED_STRING_CONSTANT)

    @staticmethod
    def EOFInStringConstant(line: int, column: int):
        return LexicographicError(line, column, EOF_IN_STRING_CONSTANT)

    @staticmethod
    def StringContainsNullChar(line: int, column: int):
        return LexicographicError(line, column, STRING_CONTAINS_NULL_CHAR)
