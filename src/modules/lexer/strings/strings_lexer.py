from src.shared.lexer import BaseLexer, find_column
from src.modules.lexer.errors import LexicographicError


class StringsLexer(BaseLexer):
    tokens = {QUOTE, NEWLINE, NULL_CHAR, ESCAPED_INNER_STRING}

    @_(r"[^\"\\\n\x00]+(?:\\[\s\S][^\"\\\n\x00]*)*")
    def ESCAPED_INNER_STRING(self, token):
        self.lineno += len(token.value.split("\n")) - 1
        self.current_string_value = token

    @_(r"\"")
    def QUOTE(self, token):
        self.leave_context()
        return self.current_string_value

    @_(r"\x00")
    def NULL_CHAR(self, token):
        self.lexer_errors.append(
            LexicographicError.StringContainsNullChar(
                self.lineno, find_column(self.text, token.index)
            )
        )

    @_(r"\n")
    def NEWLINE(self, token):
        print("Found newline", (self.lineno, find_column(self.text, token.index)))
        self.lexer_errors.append(
            LexicographicError.UnterminatedStringConstant(
                self.lineno, find_column(self.text, token.index)
            )
        )
        self.lineno += 1
        self.leave_context()
        return self.current_string_value

    def handle_EOF(self):
        self.lexer_errors.append(
            LexicographicError.EOFInStringConstant(
                self.lineno, find_column(self.text, self.index)
            )
        )

    # Ignore errors (catch them in token's methods)
    def error(self, token):
        self.index += 1
