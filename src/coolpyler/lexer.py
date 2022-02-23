from sly import Lexer

from coolpyler.errors import UnexpectedCharError


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
            f"Token(type={self.type!r}, value={self.value!r},"
            + " lineno={self.lineno}, columnno={self.columnno}, index={self.index})"
        )


class CoolLexerBase(object):
    def compute_column(self, index):
        return index - self.text[:index].rfind("\n")

    def EOF(self):
        pass


class CoolLexer(CoolLexerBase, Lexer):
    tokens = {
        "INLINE_COMMENT",
        "OCOMMENT",
        "SEMICOLON",
        "OCURLY",
        "CCURLY",
        "OPAR",
        "CPAR",
        "COMMA",
        "COLON",
        "TILDE",
        "DOT",
        "AT",
        "LEFT_ARROW",
        "RIGHT_ARROW",
        "LEQ",
        "LE",
        "EQ",
        "PLUS",
        "MINUS",
        "STAR",
        "SLASH",
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
        "STRING",
        "INT",
    }

    INLINE_COMMENT = r"--[^\n]*"
    OCOMMENT = r"\(\*"
    SEMICOLON = r";"
    OCURLY = r"{"
    CCURLY = r"}"
    OPAR = r"\("
    CPAR = r"\)"
    COMMA = r","
    COLON = r":"
    TILDE = r"~"
    DOT = r"\."
    AT = r"@"
    LEFT_ARROW = r"<-"
    RIGHT_ARROW = r"=>"
    LEQ = r"<="
    LE = r"<"
    EQ = r"="
    PLUS = r"\+"
    MINUS = r"-"
    STAR = r"\*"
    SLASH = r"/"

    TYPE_ID = r"[A-Z][a-zA-Z0-9_]*"
    OBJECT_ID = r"[a-z][a-zA-Z0-9_]*"

    keywords = {
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
    }

    special_values = {"TRUE", "FALSE"}

    STRING = r"\""
    INT = r"[0-9]+"

    ignore_whitespace = r"[ \t\r\f\v]"
    ignore_newline = r"\n"

    def __init__(self, errors=None):
        if errors is None:
            errors = []
        self.errors = errors
        self.string = None
        self.multiline_comment_balance = 0

    def tokenize(self, text, lineno=1, index=0):
        tokens = [
            CoolToken.from_sly_token(t, self.compute_column(t.index))
            for t in super().tokenize(text, lineno=lineno, index=index)
        ]

        last_token = self.EOF()
        if last_token is not None:
            tokens.append(
                CoolToken.from_sly_token(
                    last_token, self.compute_column(last_token.index)
                )
            )

        yield from tokens

    def INLINE_COMMENT(self, t):
        pass

    def OCOMMENT(self, t):
        self.multiline_comment_balance = 1
        self.push_state(CoolMultilineCommentLexer)

    def TYPE_ID(self, t):
        uppercased = t.value.upper()
        if uppercased in CoolLexer.keywords:
            t.type = uppercased
        return t

    def OBJECT_ID(self, t):
        uppercased = t.value.upper()
        if uppercased in CoolLexer.keywords or uppercased in CoolLexer.special_values:
            t.type = uppercased
        return t

    def STRING(self, t):
        self.string = t
        self.push_state(CoolStringLexer)

    def INT(self, t):
        t.value = int(t.value)
        return t

    def ignore_newline(self, t):
        self.lineno += 1

    def error(self, t):
        t.value = t.value[0]
        self.index += 1
        self.errors.append(
            UnexpectedCharError(
                t.lineno, self.compute_column(t.index), repr(t.value[0])[1:-1],
            )
        )
        return t


class CoolMultilineCommentLexer(CoolLexerBase, Lexer):
    tokens = {"OCOMMENT", "CCOMMENT"}

    OCOMMENT = r"\(\*"
    CCOMMENT = r"\*\)"

    ignore_newline = r"\n"

    def OCOMMENT(self, t):
        self.multiline_comment_balance += 1

    def CCOMMENT(self, t):
        self.multiline_comment_balance -= 1
        if self.multiline_comment_balance == 0:
            self.pop_state()

    def EOF(self):
        self.errors.append(
            UnexpectedCharError(self.lineno, self.compute_column(self.index), "EOF")
        )

    def ignore_newline(self, t):
        self.lineno += 1

    def error(self, t):
        self.index += 1


class CoolStringLexer(CoolLexerBase, Lexer):
    tokens = {"STRING", "ESCAPED_CHAR", "BODY", "EOL"}

    STRING = r"\""
    ESCAPED_CHAR = r"(?s:\\.?)"
    BODY = r"[^\x00\n\\\"]+"
    EOL = r"\n"

    def STRING(self, t):
        self.pop_state()
        t = self.string
        self.string = None
        return t

    def ESCAPED_CHAR(self, t):
        special_map = {"b": "\b", "t": "\t", "n": "\n", "f": "\f"}
        if t.value[-1] == "\n":
            self.lineno += 1
        self.string.value += special_map.get(t.value[-1], t.value[-1])

    def BODY(self, t):
        self.string.value += t.value

    def EOL(self, t):
        self.errors.append(
            UnexpectedCharError(
                t.lineno, self.compute_column(t.index), repr(t.value[0])[1:-1],
            )
        )
        self.lineno += 1
        self.pop_state()
        t = self.string
        self.string = None
        return t

    def EOF(self):
        self.errors.append(
            UnexpectedCharError(self.lineno, self.compute_column(self.index), "EOF")
        )
        t = self.string
        self.string = None
        return t

    def error(self, t):
        self.index += 1
        self.errors.append(
            UnexpectedCharError(
                t.lineno, self.compute_column(t.index), repr(t.value[0])[1:-1],
            )
        )
