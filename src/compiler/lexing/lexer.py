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
        self.states = (("comment", "exclusive"), ("string", "exclusive"))

        self._string_value = ""
        self._string_start = -1
        self._string_col = -1
        self._string_line = -1
        self._string_slash = False
        self._end_string = True

        self._end_comment = True
        self._build()

    def _build(self):
        self._lexer = lex.lex(module=self)
        self._lexer.col = 1

    def tokenize(self, data):
        self._lexer.input(data)
        while True:
            tok = self._lexer.token()
            if not self._end_comment and self._lexer.lexpos - 1 <= len(data):
                line, col = self._get_current_pos(data)
                self.errors.append(LexicographicError(line, col, "INVALID COMMENT"))
                break
            if not self._end_string and self._lexer.lexpos - 1 <= len(data):
                line = self._lexer.lineno
                col = self._lexer.col + 1
                self.errors.append(LexicographicError(line, col, "UNTERMINATED STRING"))
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
    def t_string(self, t):
        r'"'
        self._string_value = ''
        t.lexer.col += 1
        self._string_value += t.value
        self._string_line = t.lexer.lineno
        self._string_col = t.lexer.col - 1
        self._end_string = False
        t.lexer.begin("string")

    def t_string_end(self, t):
        r'(?<!\\)"'
        col = len(t.value)
        t.lexer.col += col
        self._end_string = True
        t.lexer.begin("INITIAL")
        t.type = "STRING"
        t.value = self._string_value + t.value
        t.col = self._string_col
        t.line = self._string_line
        for index, char in enumerate(t.value):
            if char == "\0":
                null_col = t.col + index
                null_line = t.line
                self.errors.append(
                    LexicographicError(null_line, null_col, "NULL CHARACTER")
                )
        t.value = t.value[1:-1]
        return t

    def t_string_space(self, t):
        r"\s"
        self._string_value += t.value
        t.lexer.col += len(t.value)
        if t.value == "\n":
            if not self._string_slash:
                line = t.lexer.lineno
                col = t.lexer.col - 1
                t.lexer.col = 1
                self.errors.append(LexicographicError(line, col, "\\n"))
                t.lexer.begin("INITIAL")
            t.lexer.lineno += 1
            t.lexer.col = 0

    def t_string_pass(self, t):
        r"."
        if t.value == "\\":
            self._string_slash = True
        else:
            self._string_slash = False
        self._string_value += t.value
        t.lexer.col += len(t.value)

    # Multiline comments rules
    def t_comment(self, t):
        r"\(\*"
        t.lexer.col += len(t.value)
        t.lexer.comm_start = t.lexer.lexpos - 2
        t.lexer.level = 1
        self._end_comment = False
        t.lexer.begin("comment")

    def t_comment_lcomment(self, t):
        r"\(\*"
        t.lexer.level += 1
        t.lexer.col += len(t.value)

    def t_comment_rcomment(self, t):
        r"\*\)"
        t.lexer.col += len(t.value)
        t.lexer.level -= 1
        if t.lexer.level == 0:
            t.value = t.lexer.lexdata[t.lexer.comm_start : t.lexer.lexpos]
            t.type = "ONELINECOMMENT"
            self._end_comment = True
            t.lexer.begin("INITIAL")

    def t_comment_pass(self, t):
        r".|\n"
        self._end_comment = False
        if t.value == "\n":
            t.lexer.lineno += 1
            t.lexer.col = 1
        else:
            t.lexer.col += len(t.value)

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
        self.errors.append(LexicographicError(line, col, t.value[0]))
        t.lexer.skip(1)
