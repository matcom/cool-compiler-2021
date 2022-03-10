import ply.lex as lex

from utils.utils import find_column

global errors
global input_text

tokens = [
    "INTEGER",
    "ID",
    "TYPE_ID",
    "OBJECT_ID",
    "self",
    "SELF_TYPE",
    "BOOL",
    "STRING",
    "COMMENT",
    "PLUS",
    "MINUS",
    "MULT",
    "DIV",
    "EQ",
    "LT",
    "LTEQ",
    "ASSIGN",
    "ACTION",
    "INT_COMP",
    "LPAREN",
    "RPAREN",
    "LBRACE",
    "RBRACE",
    "DOT",
    "COMMA",
    "COLON",
    "SEMICOLON",
    "AT",
]

keywords = {
    # class <type> [ inherits <type> ] {
    # <feature_list>
    # };
    "class": "CLASS",
    "inherits": "INHERITS",
    # new <type>
    "new": "NEW",
    # isvoid expr evaluates to true if expr is void and evaluates to false if expr is not void.
    "isvoid": "ISVOID",
    # reads from the standard input
    "in": "IN",
    # case <expr0> of
    # <id1> : <type1> => <expr1>;
    # . . .
    # <idn> : <typen> => <exprn>;
    # esac
    "case": "CASE",
    "of": "OF",
    "esac": "ESAC",
    # if <expr> then <expr> else <expr> fi
    "if": "IF",
    "then": "THEN",
    "else": "ELSE",
    "fi": "FI",
    # while <expr> loop <expr> pool
    "while": "WHILE",
    "loop": "LOOP",
    "pool": "POOL",
    # let <id1> : <type1> [ <- <expr1> ], ..., <idn> : <typen> [ <- <exprn> ] in <expr>
    "let": "LET",
    "not": "NOT",
}

tokens = tokens + list(keywords.values())

t_PLUS = r"\+"
t_MINUS = r"-"
t_MULT = r"\*"
t_DIV = r"/"

t_EQ = r"\="
t_LT = r"\<"
t_LTEQ = r"\<\="
t_ASSIGN = r"\<\-"
t_ACTION = r"\=\>"
t_INT_COMP = r"\~"

t_LPAREN = r"\("
t_RPAREN = r"\)"
t_LBRACE = r"\{"
t_RBRACE = r"\}"
t_DOT = r"\."
t_COMMA = r"\,"
t_COLON = r"\:"
t_SEMICOLON = r"\;"

t_AT = r"\@"

states = (
    ("STRING", "exclusive"),
    ("COMMENT", "exclusive"),
)


# Integers are non-empty strings of digits 0-9.
def t_INTEGER(t):
    r"[0-9]+"
    t.value = int(t.value)
    return t


# Booleans are true=True or false=False
def t_BOOL(t):
    r"[t][rR][uU][eE]|[f][aA][lL][sS][eE]"
    t.value = True if t.value.lower() == "true" else False
    return t


# Type identifiers begin with a capital letter
# Object identifiers begin with a lower case letter
def t_TYPES(t):
    r"[a-zA-Z][a-zA-Z0-9_]*"
    t.type = keywords.get(t.value.lower(), "IDENTIFIER")
    if t.type == "IDENTIFIER":
        if t.value[0].islower():
            t.type = "OBJECT_ID"
        else:
            t.type = "TYPE_ID"
    return t


# Strings double quotes "..."
t_STRING_ignore = ""


# A string start with "
def t_start_string(t):
    r"\""
    t.lexer.push_state("STRING")
    t.lexer.string_backslash = False
    t.lexer.string_buffer = ""


def t_STRING_newline(t):
    r"\n"
    if not t.lexer.string_backslash:
        errors.append(
            "(%s, %s) - LexicographicError: STRING ERROR NON-ESCAPED NEWLINE CHARACTER"
            % (t.lexer.lineno, find_column(t.lexer.lexdata, t.lexpos))
        )
        t.lexer.pop_state()
    else:
        t.lexer.string_backslash = False
    t.lexer.lineno += 1


# A string ends with "
def t_STRING_end(t):
    r"\""
    if t.lexer.string_backslash:
        t.lexer.string_buffer += '"'
        t.lexer.string_backslash = False
    else:
        t.lexer.pop_state()
        t.value = t.lexer.string_buffer
        t.type = "STRING"
        return t


def t_STRING_null(t):
    r"\0"
    errors.append("(%s, %s) - LexicographicError: STRING NULL ERROR" %
                  (t.lexer.lineno, find_column(t.lexer.lexdata, t.lexpos)))
    t.lexer.skip(1)


def t_STRING_something(t):
    r"[^\n]"
    if not t.lexer.string_backslash:  # if the previous chat is not '\'
        if t.value == "\\":
            t.lexer.string_backslash = True  # backslash
        else:
            t.lexer.string_buffer += t.value  # no backslash
    else:
        t.lexer.string_backslash = False
        if t.value == "b":  # \b backspace
            t.lexer.string_buffer += "\b"
        elif t.value == "t":  # \t tab
            t.lexer.string_buffer += "\t"
        elif t.value == 'n':
            t.lexer.string_buffer += '\n'
        elif t.value == "f":  # \f
            t.lexer.string_buffer += "\f"
        elif t.value == "\\":  # \\ backslash
            t.lexer.string_buffer += "\\"
            t.lexer.string_backslash = True
        else:
            t.lexer.string_buffer += t.value


# String Error handling
def t_STRING_error(t):
    col = find_column(t.lexer.lexdata, t.lexpos)
    errors.append(
        "(%s, %s) - LexicographicError: ERROR %s " % (t.lexer.lineno, col, t.value[0])
    )
    t.lexer.skip(1)


# STRING EOF handling
def t_STRING_eof(t):
    if t.lexer.current_state():
        errors.append(
            "(%s, %s) - LexicographicError: EOF ERROR IN STRING STATE" %
            (t.lexer.lineno, find_column(t.lexer.lexdata, t.lexpos))
        )


t_COMMENT_ignore = ""


# COMMENT:  “--” and the next newline (or EOF, if there is no next newline)
def t_COMMENT(t):
    r"\-\-[^\n]*"
    t.value = t.value[2:]


# COMMENT:  enclosing text in (∗ . . . ∗)
def t_start_comment(t):
    r"\(\*"
    t.lexer.push_state("COMMENT")
    t.lexer.comment_count = 0
    t.lexer.string_buffer = ""


# COMMENT: newline
def t_COMMENT_newline(t):
    r"\n+"
    t.lexer.lineno += len(t.value)


# COMMENT: end " *) "
def t_COMMENT_end(t):
    r"\*\)"
    t.lexer.pop_state()
    t.value = t.lexer.string_buffer
    t.type = "COMMENT"


def t_COMMENT_something(t):
    r"[^\n]"
    t.lexer.string_buffer += t.value


# COMMENT: Error handling
def t_COMMENT_error(t):
    col = find_column(t.lexer.lexdata, t.lexpos)
    errors.append(
        "(%s, %s) - LexicographicError: COMMENT ERROR " % (t.lexer.lineno, col)
    )
    t.lexer.skip(1)


# COMMENT: EOF handling
def t_COMMENT_eof(t):
    if t.lexer.current_state():
        col = find_column(t.lexer.lexdata, t.lexpos)
        errors.append(
            "(%s, %s) - LexicographicError: EOF in comment" % (t.lexer.lineno, col)
        )


# Ignore blanks, tabs, carriage return, form feed
t_ignore = " \t\r\f"


# Line numbers
def t_newline(t):
    r"\n+"
    t.lexer.lineno += len(t.value)


# Error handling rule
def t_error(t):
    col = find_column(t.lexer.lexdata, t.lexpos)
    errors.append(
        '(%s, %s) - LexicographicError: ILLEGAL CHARACTER "%s"'
        % (t.lexer.lineno, col, t.value[0])
    )
    t.lexer.skip(1)


def tokenize(text: str) -> (lex.Lexer, list):
    global errors
    global input_text

    errors = []
    input_text = text
    lexer = get_a_lexer()
    lexer.input(text)
    return lexer, errors


def get_a_lexer() -> lex.Lexer:
    lexer = lex.lex()
    return lexer
