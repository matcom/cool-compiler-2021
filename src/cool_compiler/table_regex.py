from enum import  Enum

class TokenType(Enum):
    pass


class RegexTable:

    def __call__(self):
        return self.symbol_table() + self.keyword_table() + self.identifier_table() 

    def symbol_table(self):
        pass
    
    def identifier_table(self):
        pass
    
    def keyword_table(self):
        pass