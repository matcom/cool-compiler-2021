from sly import Lexer

from app.shared.errors import GenericAppError


def find_column(text: str, token_index: int) -> int:
    last_cr = text.rfind("\n", 0, token_index)
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
        self.current_string_value = None

    # ignore token, this must be an unhandled error
    def error(self):
        self.lexer_errors.append(
            GenericAppError()
        )

    def leave_context(self):
        self.pop_state()

    def handle_EOF(self):
        raise NotImplementedError()
