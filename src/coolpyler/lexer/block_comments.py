from coolpyler.lexer.base import BaseLexer, find_column
from coolpyler.lexer.errors import LexicographicError


class BlockCommentLexer(BaseLexer):
    tokens = {O_BLOCK_COMMENT, C_BLOCK_COMMENT}

    O_BLOCK_COMMENT = r"\(\*"
    C_BLOCK_COMMENT = r"\*\)"

    ignore_newline = r"\n"

    def ignore_newline(self, token):
        self.lineno += 1

    def O_BLOCK_COMMENT(self, token):
        self.comment_nesting_level += 1

    def C_BLOCK_COMMENT(self, token):
        self.comment_nesting_level -= 1
        if self.comment_nesting_level == 0:
            self.leave_context()

    def handle_EOF(self):
        self.lexer_errors.append(
            LexicographicError.EOFInComment(
                self.lineno, find_column(self.text, self.index)
            )
        )

    # Ignore errors
    def error(self, token):
        self.index += 1
