import ply.lex as lex

tokens = (
    'NUMBER',
    'PLUS',
)

t_PLUS = r'\+'


def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


t_ignore = ' \t'


lexer = lex.lex()
text = '''
    5 +88+ 47+ 567
'''
lexer.input(text)
for tok in lexer:
    print(tok)
