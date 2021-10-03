from re import S
from sly import Lexer, lex

class CoolString(Lexer):
    tokens = { TEXT, BACKNEWL,
        FORMFEED, TAB, BACKESPACE, NEWLINE
    }

    
    ignore_newline = r'\n'
    ignore_close = r'"'
    ignore_null = r'\0'
    
    FORMFEED  = r'\\f'
    TAB       = r'\\t'
    BACKESPACE= r'\\b'
    NEWLINE   = r'\\n'
    CHARTER   =r'\\.'
    BACKNEWL  = r'\\ *\n'
    TEXT      = r'.'

    def __init__(self, lexer ):
        self.lexer = lexer
        self.pos = 0
        self.count_new_line = 0
        self.len = 0
    
    def ignore_close(self, token):
        self.index = self.len
        self.pos = token.index + 1

    def ignore_newline(self, token):
        index = self.lexer.index + token.index
        lineno = self.lexer.lineno + self.count_new_line
        self.lexer.cool_error(lineno, index)
        self.lexer.cool_error.add_lexical("Unterminated string constant")
        self.index = self.len
        self.pos = token.index 
    
    def ignore_null(self, token):
        index = self.lexer.index + token.index
        lineno = self.lexer.lineno + self.count_new_line
        self.lexer.cool_error(lineno, index)
        self.lexer.cool_error.add_lexical("String contains null character")

    
    def FORMFEED(self, token):
        token.value = '\f'
        return token
    
    def TAB(self, token):
        token.value = '\t'
        return token
    
    def BACKESPACE(self, token):
        token.value = '\b'
        return token

    def NEWLINE(self, token):
        token.value = '\n'
        return token

    def CHARTER(self, token):
        token.value =  token.value[1:]
        return token

    def BACKNEWL(self, token):
        self.count_new_line += 1
        token.value ="\n"
        return token
    

    
    def string_analizer(self):
        text = self.lexer.text[self.lexer.index:]
        self.len = len(text)
        _list = []
        for t in self.tokenize(text):
            _list.append(t.value)

        result = ''.join(_list)
        return result, self.pos, self.count_new_line

    


