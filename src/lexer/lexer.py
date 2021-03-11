from ..utils import reservedKeywords, literals, ignored, tokens 

import ply.lex as lex

class CoolLexer:
    def __init__(self):
        self.reserved = reservedKeywords
        self.tokens = tokens
        self.errors = []
        self.lexer = lex.lex()

    def t_COMMENT(self, t):
        r'--[^\n]+\n|\(\*[^(\*\))]+\*\)'        
        pass

    def t_INTEGER(self,t):
        r'[0-9]+'
        t.value = int(t.value)
        return t

    def t_STRING(self, t):
        r'"[^\0\n"]*(\\\n[^\0\n"]*)*"'
        t.value = t.value[1:-1]
        return t

    def t_BOOL(self, t):
        r'true|false'
        t.value = True if t.value == 'true' else False
        return t

    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    def t_INTEGER(self, t):
        r'[0-9]+'
        t.value = int(t.value)
        return t


    def t_STRING(self, t):
        r'"[^\0\n"]*(\\\n[^\0\n"]*)*"'
        t.value = t.value[1:-1]
        return t

    def t_BOOL(self, t):
        r'true|false'
        t.value = True if t.value == 'true' else False
        return t

    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    def t_NOT(self, t):
        r'[nN][oO][tT]'
        return t

    def t_TYPE(self,t):
        r'[A-Z][A-Za-z0-9_]*'
        return t

    def t_ID(self, t):
        r'[a-z][A-Za-z0-9_]*'
        t.type = reservedKeywords.get(t.value.lower(), 'ID')
        return t

    def t_error(self, t):
        print("Illegal character '{}'".format(t.value[0]))
        t.lexer.skip(1)


    t_ignore = ''.join(ignored)