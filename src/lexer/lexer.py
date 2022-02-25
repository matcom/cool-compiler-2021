import ply.lex as lex

states = (
    ('commentLine', 'exclusive'),
    ('commentText', 'exclusive'),
    ('string', 'exclusive'),
)

reserved = {
    'class': 'CLASS',
    'inherits': 'INHERITS',
    'if': 'IF',
    'then': 'THEN',
    'else': 'ELSE',
    'fi': 'FI',
    'while': 'WHILE',
    'loop': 'LOOP',
    'pool': 'POOL',
    'let': 'LET',
    'in': 'IN',
    'case': 'CASE',
    'of': 'OF',
    'esac': 'ESAC',
    'new': 'NEW',
    'isvoid': 'ISVOID',
    'not' : 'NOT'
}

t_ignore = ' \t'

tokens = [
    #Identifiers
    'TYPE', 'ID',
    #Primitive data types
    'INTEGER', 'STRING', 'BOOL',
    # Special keywords
    'ACTION',
    # Operators
    'ASSIGN', 'LESS', 'LESSEQUAL', 'EQUAL', 'PLUS', 'MINUS', 'MULT', 'DIV', 'INT_COMPLEMENT',
    #Literals
    'OPAR', 'CPAR', 'OBRACE', 'CBRACE', 'COLON', 'COMMA', 'DOT', 'SEMICOLON', 'AT',  
] + list(reserved.values())

# Special keywords

t_ACTION = r'=>'

# Operators

t_ASSIGN = r'<-'
t_LESS = r'<'
t_LESSEQUAL = r'<='
t_EQUAL = r'='
t_PLUS = r'\+'
t_MINUS = r'-'
t_MULT = r'\*'
t_DIV = r'/'
t_INT_COMPLEMENT = r'~'

# Literals

t_OPAR = r'\('
t_CPAR = r'\)'
t_OBRACE = r'{'
t_CBRACE = r'}'
t_COLON = r':'
t_COMMA = r','
t_DOT = r'\.'
t_SEMICOLON = r';'
t_AT = r'@'


def t_INTEGER(t):
    r'\d+'
    t.value = int(t.value)
    return t


def t_TYPE(t):
    r'[A-Z][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value.lower(), 'TYPE')
    return t


def t_BOOL(t):
    r'f[Aa][Ll][Ss][Ee]|t[Rr][Uu][Ee]'
    t.value = (t.value.lower() == 'true')
    return t


def t_ID(t):
    r'[a-z][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value.lower(), 'ID')
    return t

t_commentLine_ignore = ' \t'

def t_LINECOMMENT(t):
    r'--'
    t.lexer.begin('commentLine')


def t_TEXTCOMMENT(t):
    r'\(\*'
    t.lexer.comment_start = t.lexer.lexpos
    t.lexer.level = 1
    t.lexer.begin('commentText')


def t_STRING(t):
    r'"'
    t.lexer.string_start = t.lexer.lexpos
    t.lexer.begin('string')


def t_commentLine_error(t):
    t.lexer.skip(1)


def t_commentLine_newline(t):
    r'\n+'
    t.lexer.begin('INITIAL')
    t.lexer.lineno += len(t.value)


t_commentText_ignore = ' \t'


def t_commentText_error(t):
    t.lexer.skip(1)


def t_commentText_OPENTEXT(t):
    r'\(\*'
    t.lexer.level += 1


def t_commentText_CLOSETEXT(t):
    r'\*\)'
    t.lexer.level -= 1
    if t.lexer.level == 0:
        t.lexer.begin('INITIAL')


def t_commentText_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_commentText_eof(t):
    append_error_lexing(t.lexer.lineno, find_column1(t), "EOF in comment")


t_string_ignore = ''


def t_string_CLOSESTRING(t):
    r'"'
    t.value = t.lexer.lexdata[t.lexer.string_start:t.lexer.lexpos - 1]
    t.type = 'STRING'
    t.lexer.begin('INITIAL')
    return t


def t_string_newline(t):
    r'\\\n'
    t.lexer.lineno += 1


def t_string_body(t):
    r'([^\n\"\\]|\\.)+'
    if t.value.rfind('\0') != -1:
        append_error_lexing(t.lineno, find_column1(t) + t.value.rfind('\0'),
                        "String contains null character")


def t_string_error(t):
    if t.value[0] == '\n':
        append_error_lexing(t.lineno, find_column1(t), "Unterminated string constant")
        t.lexer.lineno += 1
        t.lexer.skip(1)
        t.lexer.begin('INITIAL')


def t_string_eof(t):
    append_error_lexing(t.lineno, find_column1(t), "Unterminated string constant")


def t_error(t):
    append_error_lexing(t.lineno, find_column1(t), f'ERROR \"{t.value[0]}\"')
    t.lexer.skip(1)


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def find_column(lexdata, lexpos):
    line_start = lexdata.rfind('\n', 0, lexpos)
    return (lexpos - line_start)

def find_column1(t, i = None):
    lexpos = t.lexpos if (i is None) else t.lexpos(i)
    line_start = t.lexer.lexdata.rfind('\n', 0, lexpos)
    return (lexpos - line_start)

errors_lexing = []

def append_error_lexing(line, column, message):
    errors_lexing.append(f'({line}, {column}) - LexicographicError: {message}')

lexer = lex.lex()
