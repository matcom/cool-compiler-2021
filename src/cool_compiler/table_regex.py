from enum import  Enum

class TokenType(Enum):
    pass

class Token:
    def __init__(self, lex, ttype : TokenType, pos : tuple) :
        self.lex = lex
        self.type = ttype
        self.pos = pos

class RegexTable:

    def __call__(self):
        return self.symbol_table() + self.keyword_table() + self.identifier_table() 

    def symbol_table(self):
        pass
    
    def identifier_table(self):
        pass
    
    def keyword_table(self):
        pass