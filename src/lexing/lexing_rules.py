# Lexer rules
#########################################################################################

literals = [
    '+', '-', '*', '/', '~', '=', '<', ':', '{',
    '}', '@', ',', '.', '(', ')', ';', '$'
]
# keywords
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


def t_LESSEQ(t):
    r'\<='
    set_pos(t)
    return t


def t_ASSIGN(t):
    r'\<-'
    set_pos(t)
    return t


def t_RET(t):
    r'\=>'
    set_pos(t)
    return t


def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    set_pos(t)
    lower_case = t.value.lower()
    if lower_case in ('true', 'false') and t.value[0].isupper():
        t.type = 'ID'
        return t
    t.type = reserved.get(t.value.lower(), 'ID')
    return t


def t_STRING(t):
    r'\"([^\\\n]|(\\.))*?\"'
    set_pos(t)
    t.value = str(t.value)
    return t


def t_INT(t):
    r'\d+'
    set_pos(t)
    t.value = int(t.value)
    return t

# One-line comments rule


def t_COMMENT(t):
    r'(--.*(\n | $))'
    t.lexer.lineno += 1
    t.col = t.lexer.col
    t.lexer.col = 1
    return t

# Multiline comments rules


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

# Rule so we can track line numbers


def t_ANY_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
    t.lexer.col = 1


def t_WHITESPACE(t):
    r'\s'
    t.lexer.col += len(t.value)


# Error handling rule


def t_ANY_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)
#########################################################################################


def set_pos(token):
    token.col = token.lexer.col
    token.lexer.col += len(token.value)
    # token.row = token.lexer.lineno

# TODO: Add line and column for each token