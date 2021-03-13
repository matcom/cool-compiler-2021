from src.shared.lexer import BaseLexer, find_column
from src.grammars.common import (
    NEWLINE,
    WS_INLINE,
    INLINE_COMMENT,
    OPEN_BLOCK_COMMENT,
    VAR_NAME,
    TYPE_NAME,
    INT,
)
from src.modules.lexer.comments import BlockCommentLexer
from src.modules.lexer.errors import LexicographicError


class CoolLexer(BaseLexer):
    tokens = {
        # GROUPING
        OPEN_PARENTHESIS,
        CLOSED_PARENTHESIS,
        OPEN_CURLY,
        CLOSED_CURLY,
        OPEN_BLOCK_COMMENT,
        # PUNCT
        SEMICOLON,
        COLON,
        COMMA,
        DOT,
        AT,
        TILDE,  # --> ~
        # ARITH OPERATORS
        LE,
        LEQ,
        EQ,
        PLUS,
        MINUS,
        TIMES,
        DIV,
        # ASSIGNMENT & ARROW
        ASSIGN,
        ARROW,
        # BOOLEAN OP & CONSTS
        NOT,
        TRUE,
        FALSE,
        INT,
        QUOTE,
        # IDENTIFIERS
        TYPE_ID,
        OBJECT_ID,
        # KEYWORDS
        CLASS,
        ELSE,
        FI,
        IF,
        IN,
        INHERITS,
        ISVOID,
        LET,
        LOOP,
        POOL,
        THEN,
        WHILE,
        CASE,
        ESAC,
        NEW,
        OF,
    }

    def error(self, token):
        self.lexer_errors.append(
            LexicographicError.UnexpectedCharacter(
                token.lineno, find_column(self.text, token.index), token.value[0]
            )
        )
        self.index += 1

    ignore_ws = r"[ \t\v\f\r]"
    ignore_inline_comment = r"--.*"

    @_(r"\n+")
    def ignore_newline(self, token):
        self.lineno += len(token.value)

    @_(r"\(\*")
    def OPEN_BLOCK_COMMENT(self, token):
        self.comment_nesting_level += 1
        # print("I'm in comment ", (self.lineno, find_column(self.text, token.index)))
        self.push_state(BlockCommentLexer)

    @_(r"\d+")
    def INT(self, token):
        token.value = int(token.value)
        return token

    OPEN_PARENTHESIS = r"\("
    CLOSED_PARENTHESIS = r"\)"
    OPEN_CURLY = r"{"
    CLOSED_CURLY = r"}"

    SEMICOLON = r";"
    COLON = r":"
    COMMA = r","
    DOT = r"\."
    TILDE = r"~"
    AT = r"@"

    ASSIGN = r"<-"
    ARROW = r"=>"

    LE = r"<"
    LEQ = r"<="
    EQ = r"="
    PLUS = r"\+"
    MINUS = r"-"
    TIMES = r"\*"
    DIV = r"/"

    CLASS = r"(?i)class"
    ELSE = r"(?i)else"
    FI = r"(?i)fi"
    IF = r"(?i)if"
    IN = r"(?i)in"
    INHERITS = r"(?i)inherits"
    ISVOID = r"(?i)isvoid"
    LET = r"(?i)let"
    LOOP = r"(?i)loop"
    POOL = r"(?i)pool"
    THEN = r"(?i)then"
    WHILE = r"(?i)while"
    CASE = r"(?i)case"
    ESAC = r"(?i)esac"
    NEW = r"(?i)new"
    OF = r"(?i)of"

    TYPE_ID = r"[A-Z][a-zA-Z0-9_]*"
    OBJECT_ID = r"[a-z][a-zA-Z0-9_]*"

    def handle_EOF(self):
        pass

    def tokenize(self, text: str):
        yield from super().tokenize(text)
        self.handle_EOF()
