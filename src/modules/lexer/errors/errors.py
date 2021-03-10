from src.shared.errors import CoolError
from src.shared.constants import (
    LEXICOGRAPHIC_ERROR,
    EOF_IN_COMMENT,
    UNEXPECTED_CHARACTER,
    UNTERMINATED_STRING_CONSTANT,
    EOF_IN_STRING_CONSTANT,
    STRING_CONTAINS_NULL_CHAR,
)


class LexicographicError(CoolError):
    def __init__(self, line: int, column: int, err_message: str):
        CoolError.__init__(self, line, column, LEXICOGRAPHIC_ERROR, err_message)

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
