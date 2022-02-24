from distutils.log import debug
from compiler.cmp.pycompiler import EOF
import ply.lex as lex

from ..cmp.grammar import *
from ..cmp.utils import Token


class CoolLexer(object):
    def __init__(self):
        self.count = 0
        self.build()

    states = (
        ("string", "exclusive"),
        ("comment", "exclusive"),
    )

    reserved = {
        "class": "CLASS",
        "inherits": "INHERITS",
        "let": "LET",
        "in": "IN",
        "case": "CASE",
        "of": "OF",
        "esac": "ESAC",
        "while": "WHILE",
        "loop": "LOOP",
        "pool": "POOL",
        "if": "IF",
        "then": "THEN",
        "else": "ELSE",
        "fi": "FI",
        "isvoid": "ISVOID",
        "not": "NOT",
        "new": "NEW",
        "true": "TRUE",
        "false": "FALSE",
    }

    tokens = [
        "SEMICOLON",
        "COLON",
        "COMMA",
        "DOT",
        "OPAR",
        "CPAR",
        "OCUR",
        "CCUR",
        "LARROW",
        "RARROW",
        "AT",
        "EQUAL",
        "PLUS",
        "MINUS",
        "STAR",
        "DIV",
        "LESS",
        "LEQ",
        "NEG",
        "TYPEIDENTIFIER",
        "OBJECTIDENTIFIER",
        "NUMBER",
        "STRING",
        "ERROR",
    ] + list(reserved.values())

    token_type = {
        "CLASS": classx,
        "INHERITS": inherits,
        "LET": let,
        "IN": inx,
        "CASE": case,
        "OF": of,
        "ESAC": esac,
        "WHILE": whilex,
        "LOOP": loop,
        "POOL": pool,
        "IF": ifx,
        "THEN": then,
        "ELSE": elsex,
        "FI": fi,
        "ISVOID": isvoid,
        "NOT": notx,
        "NEW": new,
        "TRUE": boolx,
        "FALSE": boolx,
        "SEMICOLON": semi,
        "COLON": colon,
        "COMMA": comma,
        "DOT": dot,
        "OPAR": opar,
        "CPAR": cpar,
        "OCUR": ocur,
        "CCUR": ccur,
        "LARROW": larrow,
        "RARROW": rarrow,
        "AT": at,
        "EQUAL": equal,
        "PLUS": plus,
        "MINUS": minus,
        "STAR": star,
        "DIV": div,
        "LESS": less,
        "LEQ": leq,
        "NEG": neg,
        "TYPEIDENTIFIER": typeid,
        "OBJECTIDENTIFIER": objectid,
        "NUMBER": num,
        "STRING": stringx,
    }

    def t_begin_STARTSTRING(self, t):
        r'"'
        self.string = ""
        self.lexer.begin("string")

    def t_string_ENDSTRING(self, t):
        r'"'
        self.lexer.begin("INITIAL")
        t.value = self.string
        t.type = "STRING"
        self.add_column(t)
        return t

    def t_string_NULL(self, t):
        r"\0"
        self.lexer.begin("INITIAL")
        self.add_column(t)
        t.type = "ERROR"
        t.value = f"({t.lineno}, {t.col}) - LexicographicError: String contains null character"
        return t

    def t_string_newline1(self, t):
        r"\\n"
        self.string += "\n"

    def t_string_escaped_newline(self, t):
        r"\\\n"
        self.string += "\n"
        t.lexer.lineno += 1
        self.count = t.lexpos + len(t.value)

    def t_string_invalid_newline2(self, t):
        r"\n"
        self.lexer.begin("INITIAL")
        self.add_column(t)
        self.count = t.lexpos + len(t.value)
        t.type = "ERROR"
        t.value = (
            f"({t.lineno}, {t.col}) - LexicographicError: Unterminated string constant"
        )
        t.lexer.lineno += 1
        return t

    def t_string_special_character(self, t):
        r"\\[btf]"
        self.string += t.value

    def t_string_escaped_character(self, t):
        r"\\."
        self.string += t.value[1]

    def t_string_character(self, t):
        r"."
        self.string += t.value

    def t_string_eof(self, t):
        self.add_column(t)
        t.type = "ERROR"
        t.value = f"({t.lineno},{t.col}) - LexicographicError: EOF in string constant"
        t.lexer.begin("INITIAL")
        return t

    def t_begin_STARTCOMMENT(self, t):
        r"\(\*"
        self.comment_level = 1
        self.lexer.begin("comment")

    def t_comment_STARTCOMMENT(self, t):
        r"\(\*"
        self.comment_level += 1

    def t_comment_ENDCOMMENT(self, t):
        r"\*\)"
        self.comment_level -= 1
        if self.comment_level == 0:
            self.lexer.begin("INITIAL")

    def t_comment_character(self, t):
        r"."

    def t_comment_eof(self, t):
        self.add_column(t)
        t.type = "ERROR"
        t.value = f"({t.lexer.lineno}, {t.col}) - LexicographicError: EOF in comment"
        self.lexer.begin("INITIAL")
        return t

    def t_NUMBER(self, t):
        r"\d+"
        t.value = int(t.value)
        self.add_column(t)
        return t

    # Rule to track line numbers
    def t_ANY_newline(self, t):
        r"\n+"
        t.lexer.lineno += len(t.value)
        self.count = t.lexpos + len(t.value)

    t_ignore = " \t\f\r\v"

    def t_COMMENTLINE(self, t):
        r"--.*"

    def t_TYPEIDENTIFIER(self, t):
        r"[A-Z][0-9A-Za-z_]*"
        val = t.value.lower()
        if val not in ["true", "false"]:
            t.type = self.reserved.get(val, "TYPEIDENTIFIER")
        self.add_column(t)
        return t

    def t_OBJECTIDENTIFIER(self, t):
        r"[a-z][0-9A-Za-z_]*"
        val = t.value.lower()
        t.type = self.reserved.get(val, "OBJECTIDENTIFIER")
        self.add_column(t)
        return t

    def t_SEMICOLON(self, t):
        r";"
        self.add_column(t)
        return t

    def t_COLON(self, t):
        r":"
        self.add_column(t)
        return t

    def t_COMMA(self, t):
        r","
        self.add_column(t)
        return t

    def t_DOT(self, t):
        r"\."
        self.add_column(t)
        return t

    def t_OPAR(self, t):
        r"\("
        self.add_column(t)
        return t

    def t_CPAR(self, t):
        r"\)"
        self.add_column(t)
        return t

    def t_OCUR(self, t):
        r"{"
        self.add_column(t)
        return t

    def t_CCUR(self, t):
        r"}"
        self.add_column(t)
        return t

    def t_LARROW(self, t):
        r"<-"
        self.add_column(t)
        return t

    def t_RARROW(self, t):
        r"=>"
        self.add_column(t)
        return t

    def t_AT(self, t):
        r"@"
        self.add_column(t)
        return t

    def t_EQUAL(self, t):
        r"="
        self.add_column(t)
        return t

    def t_PLUS(self, t):
        r"\+"
        self.add_column(t)
        return t

    def t_MINUS(self, t):
        r"-"
        self.add_column(t)
        return t

    def t_STAR(self, t):
        r"\*"
        self.add_column(t)
        return t

    def t_DIV(self, t):
        r"/"
        self.add_column(t)
        return t

    def t_LEQ(self, t):
        r"<="
        self.add_column(t)
        return t

    def t_LESS(self, t):
        r"<"
        self.add_column(t)
        return t

    def t_NEG(self, t):
        r"~"
        self.add_column(t)
        return t

    def t_eof(self, t):
        t.lexer.eof = (t.lexer.lineno, self.add_column(t))
        return None

    def t_error(self, t):
        self.add_column(t)
        t.type = "ERROR"
        error_msg = t.value[0]
        t.value = f'({t.lineno}, {t.col}) - LexicographicError: ERROR "{error_msg}"'
        t.lexer.skip(1)
        return t

    # Build the lexer
    def build(self, **kwargs):
        # self.lexer = lex.lex(module=self, **kwargs)
        self.lexer = lex.lex(
            module=self, errorlog=lex.NullLogger(), debug=False, **kwargs
        )
        self.lexer.eof = (1, 1)
        self.comment_level = 0
        self.string = ""

    def add_column(self, t):
        t.col = t.lexpos - self.count + 1

    def tokenize(self, data):
        self.lexer.input(data)
        token_list = []
        errors = []
        while True:
            tok = self.lexer.token()
            if not tok:
                break

            if tok.type == "ERROR":
                errors.append(tok.value)
            else:
                token_list.append(
                    Token(tok.value, self.token_type[tok.type], (tok.lineno, tok.col))
                )
        if not token_list:
            errors.append("(0, 0) - SyntacticError: Unexpected token EOF")
        token_list.append(Token("$", G.EOF, self.lexer.eof))
        return token_list, errors


def pprint_tokens(tokens, get=False):
    indent = 0
    pending = []
    result = ""
    for token in tokens:
        pending.append(token)
        if token.token_type in {ocur, ccur, semi}:
            if token.token_type == ccur:
                indent -= 1
            if get:
                result += (
                    "    " * indent
                    + " ".join(str(t.token_type) for t in pending)
                    + "\n"
                )
            else:
                print("    " * indent + " ".join(str(t.token_type) for t in pending))
            pending.clear()
            if token.token_type == ocur:
                indent += 1
    if get:
        result += " ".join([str(t.token_type) for t in pending]) + "\n"
        return result
    else:
        print(" ".join([str(t.token_type) for t in pending]))
