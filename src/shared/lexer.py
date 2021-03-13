from enum import Enum

from sly import Lexer

from src.modules.lexer.errors import LexicographicError
from src.shared.constants import UNHANDLED_LEXICOGRAPHIC_ERROR


def find_column(text: str, token_index: int) -> int:
    last_cr = text.rfind("\n", 0, token_index)
    if last_cr < 0:
        last_cr = 0
    column = token_index - last_cr
    return column


class BaseLexer(Lexer):
    tokens = {}

    @property
    def errors(self):
        return list(map(str, self.lexer_errors))

    def __init__(self, lexer_errors=[]):
        self.lexer_errors = lexer_errors
        self.comment_nesting_level = 0

    def error(self, token):
        self.lexer_errors.append(
            LexicographicError(0, 0, UNHANDLED_LEXICOGRAPHIC_ERROR)
        )

    def leave_context(self):
        self.pop_state()

    def handle_EOF(self):
        raise NotImplementedError()