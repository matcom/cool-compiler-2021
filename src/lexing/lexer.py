from .errors import LexicographicError
from ply import lex


class Lexer:
    def __init__(self) -> None:
        self.errors = []
        self.literals = [
            "+",
            "-",
            "*",
            "/",
            "~",
            "=",
            "<",
            ":",
            "{",
            "}",
            "@",
            ",",
            ".",
            "(",
            ")",
            ";",
        ]
        # keywords
        self.reserved = {
            "true": "TRUE",
            "false": "FALSE",
            "if": "IF",
            "then": "THEN",
            "else": "ELSE",
            "fi": "FI",
            "class": "CLASS",
            "inherits": "INHERITS",
            "while": "WHILE",
            "loop": "LOOP",
            "pool": "POOL",
            "let": "LET",
            "in": "IN",
            "case": "CASE",
            "of": "OF",
            "esac": "ESAC",
            "new": "NEW",
            "isvoid": "ISVOID",
            "not": "NOT",
        }

        self.tokens = [
            "LESSEQ",
            "ASSIGN",
            "RET",
            "ID",
            "TYPE",
            "STRING",
            "INT",
            "ONELINECOMMENT",
        ]
        self.tokens = self.tokens + list(self.reserved.values())
        self.states = (("comment", "exclusive"),("string", "exclusive"))
        self._end_comment = True
        self._end_string = True
        self._build()

    def _build(self):
        self._lexer = lex.lex(module=self)
        self._lexer.col = 0

    def tokenize(self, data):
        self._lexer.input(data)
        while True:
            tok = self._lexer.token()
            if not self._end_comment:
                line, col = self._get_current_pos(data)
                self.errors.append(LexicographicError(line, col, "INVALID COMMENT"))
                break
            if not tok:
                break
            yield tok

    def _get_current_pos(self, data: str):
        data = data[: self._lexer.lexpos]
        line = data.count("\n") + 1
        col = len(data) - data.rfind("\n")
        return line, col

    def _set_pos(self, token):
        token.col = token.lexer.col
        token.line = token.lexer.lineno
        token.lexer.col += len(token.value)

    def t_LESSEQ(self, t):
        r"\<="
        self._set_pos(t)
        return t

    def t_ASSIGN(self, t):
        r"\<-"
        self._set_pos(t)
        return t

    def t_RET(self, t):
        r"\=>"
        self._set_pos(t)
        return t

    def t_TYPE(self, t):
        r"[A-Z][a-zA-Z_0-9]*"
        self._set_pos(t)
        lower_case = t.value.lower()
        if lower_case in ("true", "false"):
            t.type = "TYPE"
            return t
        t.type = self.reserved.get(lower_case, "TYPE")
        return t

    def t_ID(self, t):
        r"[a-z][a-zA-Z_0-9]*"
        self._set_pos(t)
        t.type = self.reserved.get(t.value.lower(), "ID")
        return t

    def t_STRING(self, t):
        r"\"([^\\\n]|(\\.))*?\""
        self._set_pos(t)
        t.value = str(t.value)
        return t

    def t_INT(self, t):
        r"\d+"
        self._set_pos(t)
        t.value = int(t.value)
        return t

    # One-line comments rule
    def t_ONELINECOMMENT(self, t):
        r"(--.*(\n | $))"
        t.lexer.lineno += 1
        t.col = t.lexer.col
        t.lexer.col = 1

    # String rules
    def t_string():
        pass

    # Multiline comments rules
    def t_comment(self, t):
        r"\(\*"
        t.lexer.comm_start = t.lexer.lexpos - 2
        t.lexer.level = 1
        t.lexer.begin("comment")

    def t_comment_lcomment(self, t):
        r"\(\*"
        t.lexer.level += 1

    def t_comment_rcomment(self, t):
        r"\*\)"
        t.lexer.level -= 1
        if t.lexer.level == 0:
            t.value = t.lexer.lexdata[t.lexer.comm_start : t.lexer.lexpos]
            t.type = "ONELINECOMMENT"
            t.lexer.lineno += t.value.count("\n")
            t.lexer.col = len(t.value) - t.value.rfind("\n")
            self._end_comment = True
            t.lexer.begin("INITIAL")

    def t_comment_pass(self, t):
        r".|\n"
        self._end_comment = False
        pass

    # Rule so we can track line numbers
    def t_newline(self, t):
        r"\n+"
        t.lexer.lineno += len(t.value)
        t.lexer.col = 1

    def t_WHITESPACE(self, t):
        r"\s"
        if t.value == "\t":
            t.lexer.col += 4
        else:
            t.lexer.col += len(t.value)

    def t_plus(self, t):
        r"\+"
        t.type = "+"
        self._set_pos(t)
        return t

    def t_minus(self, t):
        r"-"
        t.type = "-"
        self._set_pos(t)
        return t

    def t_star(self, t):
        r"\*"
        t.type = "*"
        self._set_pos(t)
        return t

    def t_slash(self, t):
        r"/"
        t.type = "/"
        self._set_pos(t)
        return t

    def t_neg(self, t):
        r"~"
        t.type = "~"
        self._set_pos(t)
        return t

    def t_equal(self, t):
        r"="
        t.type = "="
        self._set_pos(t)
        return t

    def t_less(self, t):
        r"<"
        t.type = "<"
        self._set_pos(t)
        return t

    def t_colon(self, t):
        r":"
        t.type = ":"
        self._set_pos(t)
        return t

    def t_ocur(self, t):
        r"\{"
        t.type = "{"
        self._set_pos(t)
        return t

    def t_ccur(self, t):
        r"\}"
        t.type = "}"
        self._set_pos(t)
        return t

    def t_at(self, t):
        r"@"
        t.type = "@"
        self._set_pos(t)
        return t

    def t_comma(self, t):
        r","
        t.type = ","
        self._set_pos(t)
        return t

    def t_dot(self, t):
        r"\."
        t.type = "."
        self._set_pos(t)
        return t

    def t_opar(self, t):
        r"\("
        t.type = "("
        self._set_pos(t)
        return t

    def t_cpar(self, t):
        r"\)"
        t.type = ")"
        self._set_pos(t)
        return t

    def t_semicolon(self, t):
        r";"
        t.type = ";"
        self._set_pos(t)
        return t

    # Error handling rule
    def t_ANY_error(self, t):
        self._set_pos(t)
        line = t.lineno
        col = t.col
        # it's an unterminated string
        if t.value[0] == '"':
            col = len(t.value)
        self.errors.append(LexicographicError(line, col, t.value[0]))
        t.lexer.skip(1)
        return None
