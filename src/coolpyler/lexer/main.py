from coolpyler.lexer.errors import LexicographicError
from coolpyler.lexer.base import BaseLexer, find_column
from coolpyler.lexer.block_comments import BlockCommentLexer
from coolpyler.lexer.strings import StringsLexer


class CoolToken(object):
    """
    Representation of a single cool token.
    """

    @staticmethod
    def from_sly_token(token, columnno):
        return CoolToken(token.type, token.value, token.lineno, columnno, token.index)

    def __init__(self, type, value, lineno, columnno, index):
        self.type = type
        self.value = value
        self.lineno = lineno
        self.columnno = columnno
        self.index = index

    def __repr__(self):
        return (
            f"Token(type={self.type!r}, value={self.value!r}, lineno={self.lineno}, columnno={self.columnno}, index={self.index})"
        )


class CoolLexer(BaseLexer):
    tokens = {
        "OPEN_PARENTHESIS",
        "CLOSED_PARENTHESIS",
        "OPEN_CURLY",
        "CLOSED_CURLY",
        "OPEN_BLOCK_COMMENT",
        "SEMICOLON",
        "COLON",
        "COMMA",
        "DOT",
        "AT",
        "TILDE",
        "LE",
        "LEQ",
        "EQ",
        "PLUS",
        "MINUS",
        "TIMES",
        "DIV",
        "ASSIGN",
        "ARROW",
        "INT",
        "QUOTE",
        "TYPE_ID",
        "OBJECT_ID",
        "NOT",
        "CLASS",
        "INHERITS",
        "ISVOID",
        "IF",
        "THEN",
        "ELSE",
        "FI",
        "WHILE",
        "LOOP",
        "POOL",
        "LET",
        "IN",
        "CASE",
        "ESAC",
        "OF",
        "NEW",
        "TRUE",
        "FALSE",
    }

    reserved_words = {
        "NOT",
        "CLASS",
        "INHERITS",
        "ISVOID",
        "IF",
        "THEN",
        "ELSE",
        "FI",
        "WHILE",
        "LOOP",
        "POOL",
        "LET",
        "IN",
        "CASE",
        "ESAC",
        "OF",
        "NEW",
        "TRUE",
        "FALSE",
    }

    ignore_inline_comment = r"--.*"

    OPEN_BLOCK_COMMENT = r"\(\*"
    CLOSED_PARENTHESIS = r"\)"
    OPEN_PARENTHESIS = r"\("
    OPEN_CURLY = r"{"
    CLOSED_CURLY = r"}"

    SEMICOLON = r";"
    COLON = r":"
    COMMA = r","
    DOT = r"\."
    AT = r"@"
    TILDE = r"~"

    ASSIGN = r"<-"
    ARROW = r"=>"

    INT = r"[0-9]+"
    LEQ = r"<="
    LE = r"<"
    EQ = r"="
    PLUS = r"\+"
    MINUS = r"-"
    TIMES = r"\*"
    DIV = r"/"

    QUOTE = r"\""
    TYPE_ID = r"[A-Z][a-zA-Z0-9_]*"
    OBJECT_ID = r"[a-z][a-zA-Z0-9_]*"

    # IGNORE
    ignore_ws = r"[ \t\v\f\r]"
    ignore_newline = r"\n"

    def ignore_newline(self, token):
        self.lineno += len(token.value)

    def OPEN_BLOCK_COMMENT(self, token):
        self.comment_nesting_level += 1
        self.push_state(BlockCommentLexer)

    def INT(self, token):
        token.value = int(token.value)
        return token

    def QUOTE(self, token):
        self.current_string_value = token
        self.push_state(StringsLexer)

    def handle_EOF(self):
        pass

    def TYPE_ID(self, t):
        uppercased = t.value.upper()
        if uppercased in self.reserved_words:
            t.type = uppercased
        return t

    def OBJECT_ID(self, t):
        uppercased = t.value.upper()
        if uppercased in self.reserved_words:
            t.type = uppercased
        return t

    def error(self, token):
        token.value = token.value[0]
        self.index += 1
        self.lexer_errors.append(
            LexicographicError.UnexpectedCharacter(
                token.lineno, find_column(
                    self.text, token.index), repr(token.value[0])[1:-1]
            )
        )
        return token

    def tokenize(self, text: str, lineno=1, index=0):
        tokens = [
            CoolToken.from_sly_token(t, find_column(text, t.index))
            for t in super().tokenize(text, lineno=lineno, index=index)
        ]

        last_token = self.handle_EOF()
        if last_token is not None:
            tokens.append(
                CoolToken.from_sly_token(
                    last_token, find_column(text, last_token.index)
                )
            )

        yield from tokens
