import ply.lex as lex


literals = [
    '+', '-', '*', '/', '~', '=', '<', ':', '{',
    '}', '@', ',', '.', '(', ')', ';', '$'
]

reserved = {
    'true': 'TRUE',
    'false': 'FALSE',
    'if': 'IF',
    'then': 'THEN',
    'else': 'ELSE',
    'fi': 'FI',
    'class': 'CLASS',
    'inherits': 'INHERITS',
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
    'not': 'NOT'
}

tokens = [
    'LESSEQ',
    'ASSIGN',
    'RET',
    'ID',
    'STRING',
    'INT',
    'COMMENT',
]
tokens = tokens + list(reserved.values())

states = (
    ('aux', 'exclusive'),
)

t_LESSEQ = r'\<='
t_ASSIGN = r'\<-'
t_RET = r'\=>'


def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    lower_case = t.value.lower()
    if lower_case in ('true', 'false') and t.value[0].isupper():
        t.type = 'ID'
        return t
    t.type = reserved.get(t.value.lower(), 'ID')
    return t


def t_STRING(t):
    r'\"([^\\\n]|(\\.))*?\"'
    t.value = str(t.value)
    return t


def t_INT(t):
    r'\d+'
    t.value = int(t.value)
    return t

# One-line comments
def t_COMMENT(t):
    r'(--.*(\n | $))'
    return t

# Multiline comments
def t_aux(t):
    r'\(\*'
    t.lexer.comm_start = t.lexer.lexpos - 2
    t.lexer.level = 1
    t.lexer.begin('aux')


def t_aux_lcomment(t):
    r'\(\*'
    t.lexer.level += 1


def t_aux_rcomment(t):
    r'\*\)'
    t.lexer.level -= 1
    if t.lexer.level == 0:
        t.value = t.lexer.lexdata[t.lexer.comm_start:t.lexer.lexpos+1]
        t.type = "COMMENT"
        t.lexer.lineno += t.value.count('\n')
        t.lexer.begin('INITIAL')
        return t


def t_aux_pass(t):
    r'[^.]'
    pass

# Define a rule so we can track line numbers
def t_ANY_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


# A string containing ignored characters (spaces and tabs)
t_ANY_ignore = ' \t'

# Error handling rule
def t_ANY_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


def tokenize(data: str) -> list:
    lexer = lex.lex()
    lexer.input(data)
    tokens = []
    for token in lexer:
        tokens.append(token)
    return tokens
