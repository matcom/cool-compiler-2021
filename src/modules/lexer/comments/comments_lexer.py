from src.grammars.common import CLOSE_BLOCK_COMMENT, NEWLINE, OPEN_BLOCK_COMMENT
from src.modules.lexer.errors import LexicographicError
from src.shared.lexer import BaseLexer, find_column


class BlockCommentLexer(BaseLexer):
    tokens = {O_BLOCK_COMMENT, C_BLOCK_COMMENT}

    ignore_newlines = r"\n+"

    def ignore_newlines(self, token):
        self.lineno += 1

    @_(r"\(\*")
    def O_BLOCK_COMMENT(self, token):
        self.comment_nesting_level += 1

    @_(r"\*\)")
    def C_BLOCK_COMMENT(self, token):
        self.comment_nesting_level -= 1
        # print("Leaving Comment ", (self.lineno, find_column(self.text, token.index)))
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
