import ply.lex as lex

from utils.utils import find_column

global errors
global input_text

tokens = ['INTEGER',  # Non-empty strings of digits 0-9
          'ID',  # Letters, digits, and the underscore character
          'TYPE_ID',  # Begin with a capital letter
          'OBJECT_ID',  # Begin with a lower case letter
          'self', 'SELF_TYPE',  # Other identifiers

          'BOOL', 'STRING',
          'COMMENT',
          'PLUS', 'MINUS', 'MULT', 'DIV',
          'EQ', 'LT', 'LTEQ', 'ASSIGN', 'ACTION', 'INT_COMP',
          'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE', 'DOT', 'COMMA', 'COLON', 'SEMICOLON', 'AT',

          ]

keywords = {
    # class <type> [ inherits <type> ] {
    # <feature_list>
    # };
    'class': 'CLASS',
    'inherits': 'INHERITS',

    # new <type>
    'new': 'NEW',

    # isvoid expr evaluates to true if expr is void and evaluates to false if expr is not void.
    'isvoid': 'ISVOID',

    # reads from the standard input
    'in': 'IN',

    # case <expr0> of
    # <id1> : <type1> => <expr1>;
    # . . .
    # <idn> : <typen> => <exprn>;
    # esac
    'case': 'CASE',
    'of': 'OF',
    'esac': 'ESAC',

    # if <expr> then <expr> else <expr> fi
    'if': 'IF',
    'then': 'THEN',
    'else': 'ELSE',
    'fi': 'FI',

    # while <expr> loop <expr> pool
    'while': 'WHILE',
    'loop': 'LOOP',
    'pool': 'POOL',

    # let <id1> : <type1> [ <- <expr1> ], ..., <idn> : <typen> [ <- <exprn> ] in <expr>
    'let': 'LET',

    'not': 'NOT'
}

tokens = tokens + list(keywords.values())

t_PLUS = r'\+'
t_MINUS = r'-'
t_MULT = r'\*'
t_DIV = r'/'

t_EQ = r'\='
t_LT = r'\<'
t_LTEQ = r'\<\='
t_ASSIGN = r'\<\-'
t_ACTION = r'\=\>'
t_INT_COMP = r'\~'

t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_DOT = r'\.'
t_COMMA = r'\,'
t_COLON = r'\:'
t_SEMICOLON = r'\;'

t_AT = r'\@'

states = (("STRING", "exclusive"), ("COMMENT", 'exclusive'),)


# Integers are non-empty strings of digits 0-9.
def t_INTEGER(t):
    r'[0-9]+'
    t.value = int(t.value)
    return t


# Booleans are true=True or false=False
def t_BOOL(t):
    r'[t][rR][uU][eE]|[f][aA][lL][sS][eE]'
    t.value = True if t.value.lower() == 'true' else False
    return t


# Type identifiers begin with a capital letter
# Object identifiers begin with a lower case letter
def t_TYPES(t):
    r'[a-zA-Z][a-zA-Z0-9_]*'
    t.type = keywords.get(t.value.lower(), 'IDENTIFIER')
    if t.type == 'IDENTIFIER':
        if t.value[0].islower():
            t.type = 'OBJECT_ID'
        else:
            t.type = 'TYPE_ID'
    return t


# Strings are enclosed in double quotes "..."
t_STRING_ignore = ''


# A string start with " caracter
def t_start_string(t):
    r'\"'
    t.lexer.push_state("STRING")  # Changes the lexing state and saves old on stack
    t.lexer.string_backslash = False
    t.lexer.string_buffer = ""  # start string with no chart


# A non-escaped newline character may not appear in a string. Example:
# "This \
# is OK"

# "This is not
# OK"
def t_STRING_newline(t):
    r'\n'
    if not t.lexer.string_backslash:  # FATAL ERROR
        errors.append('(%s)- LexicographicError: STRING ERROR NON-ESCAPED NEWLINE CHARACTER' % t.lexer.lineno)
        t.lexer.pop_state()
    else:
        t.lexer.string_backslash = False
    t.lexer.lineno += 1


# A string ends with " caracter
def t_STRING_end(t):
    r'\"'
    if t.lexer.string_backslash:
        t.lexer.string_buffer += '\"'
        t.lexer.string_backslash = False
    else:
        t.lexer.pop_state()
        t.value = t.lexer.string_buffer
        t.type = "STRING"
        return t


def t_STRING_null(t):
    r'\0'
    errors.append('(%s)- LexicographicError: STRING NULL ERROR' % t.lexer.lineno)
    t.lexer.skip(1)


# Within a string, a sequence ‘\c’ denotes the character ‘c’, with the exception of the following:
# \b backspace
# \t tab
# \f formfeed
# \\ backslash caracter
# A string may not contain the null
def t_STRING_something(t):
    r'[^\n]'
    if not t.lexer.string_backslash:  # if the previosur chat is not '\'
        if t.value == '\\':
            t.lexer.string_backslash = True  # backslash caracter
        else:
            t.lexer.string_buffer += t.value  # no backslash caracter situation
    else:
        t.lexer.string_backslash = False
        if t.value == 'b':  # \b backspace
            t.lexer.string_buffer += '\b'
        elif t.value == 't':  # \t tab
            t.lexer.string_buffer += '\t'
        elif t.value == 'f':  # \f formfeed
            t.lexer.string_buffer += '\f'
        elif t.value == '\\':  # \\ backslash caracter
            t.lexer.string_buffer += '\\'
            t.lexer.string_backslash = True
        else:
            t.lexer.string_buffer += t.value


# String Error handling
def t_STRING_error(t):
    col = find_column(input_text, t)
    errors.append('(%s, %s)- LexicographicError: ERROR %s ' % (col, t.lexer.lineno, t.value[0]))
    t.lexer.skip(1)


# A string may not contain EOF
# STRING EOF handling
def t_STRING_eof(t):
    if t.lexer.current_state():
        errors.append('(%s)- LexicographicError: EOF ERROR IN STRING STATE' % t.lexer.lineno)


# Exist two forms of comments in Cool:
# Type1: Any characters between two dashes “--” and the next newline (or EOF, if there is no next newline)
# Type2: Enclosing text in (∗ . . . ∗)
t_COMMENT_ignore = ''


# COMMENT TYPE 1:  “--” and the next newline (or EOF, if there is no next newline)
def t_COMMENT(t):
    r'\-\-[^\n]*'
    t.value = t.value[2:]
    # return t


# COMMENT TYPE 2:  enclosing text in (∗ . . . ∗)
def t_start_comment(t):
    r'\(\*'
    t.lexer.push_state("COMMENT")  # Changes the lexing state and saves old on stack
    t.lexer.comment_count = 0
    t.lexer.string_buffer = ""


# A comment start with " (* "
def t_COMMENT_start(t):
    r'\(\*'
    t.lexer.comment_count += 1


# A comment can has as many lines as it wants.. until the end comment " *) "
def t_COMMENT_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


# A comment finish with " *) "
def t_COMMENT_end(t):
    r'\*\)'
    if t.lexer.comment_count == 0:
        t.lexer.pop_state()
        t.value = t.lexer.string_buffer
        t.type = "COMMENT"
        # return t
    else:
        t.lexer.comment_count -= 1


# any caracter in a COMMENT
def t_COMMENT_something(t):
    r'[^\n]'
    t.lexer.string_buffer += t.value


# Comment Error handling
def t_COMMENT_error(t):
    col = find_column(input_text, t)
    errors.append('(%s, %s)- LexicographicError: COMMENT ERROR ' % (col, t.lexer.lineno))
    t.lexer.skip(1)


# comment may not contain EOF
# Comment EOF handling
def t_COMMENT_eof(t):
    if t.lexer.current_state():
        col = find_column(input_text, t)
        errors.append('(%s, %s)- LexicographicError: EOF in comment' % (col, t.lexer.lineno))


# Ignore blanks, tabs, carriage return, form feed
t_ignore = ' \t\r\f'


# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


# Error handling rule
def t_error(t):
    col = find_column(input_text, t)
    errors.append('(%s, %s)- LexicographicError: ILLEGAL CHARACTER "%s"' % (col, t.lexer.lineno, t.value[0]))
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
