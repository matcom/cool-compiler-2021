from coolpyler.lexer.base import BaseLexer, find_column
from coolpyler.lexer.errors import LexicographicError


class StringsLexer(BaseLexer):
    tokens = {QUOTE, NEWLINE, NULL_CHAR, INNER_STRING}

    QUOTE = r"\""
    INNER_STRING = r"[^\x00\n\\\"]+"
    ESCAPED_CHAR = r"(?s:\\.?)"
    NULL_CHAR = r"\x00"
    NEWLINE = r"\n"

    def INNER_STRING(self, token):
        self.current_string_value.value += token.value

    def QUOTE(self, token):
        self.leave_context()
        self.current_string_value.value += token.value
        temp = self.current_string_value
        self.current_string_value = None
        return temp

    def ESCAPED_CHAR(self, t):
        special_map = {"b": "\b", "t": "\t", "n": "\n", "f": "\f"}
        if t.value[-1] == "\n":
            self.lineno += 1
        self.current_string_value.value += special_map.get(
            t.value[-1], t.value[-1])

    def NULL_CHAR(self, token):
        self.lexer_errors.append(
            LexicographicError.StringContainsNullChar(
                self.lineno, find_column(self.text, token.index)
            )
        )
        self.index += 1

    def NEWLINE(self, token):
        self.lexer_errors.append(
            LexicographicError.UnterminatedStringConstant(
                self.lineno, find_column(self.text, token.index)
            )
        )
        self.lineno += 1
        self.leave_context()
        temp = self.current_string_value
        self.current_string_value = None
        return temp

    def handle_EOF(self):
        self.lexer_errors.append(
            LexicographicError.EOFInStringConstant(
                self.lineno, find_column(self.text, self.index)
            )
        )

    # Ignore errors (catch them in token's methods)
    def error(self, token):
        self.index += 1
