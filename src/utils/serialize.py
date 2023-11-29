import dill
from lexer.lexer import Lexer
from parsers.parser_lr1 import LR1Parser

class DillLexer:
    def __init__(self):
        self.regEx = None
        self.eof = None
        self.lexer = None

    def Create(self, regEx, eof):
        self.regEx = regEx
        self.eof = eof
        self.lexer = Lexer(self.regEx, self.eof)
    
    def Save(self):
        with open('./serializedLexer', 'wb') as _lexer: 
            dill.dump(self.lexer, _lexer)
    
    def Load(self):
        with open('./serializedLexer', 'rb') as _lexer:
            self.lexer = dill.load(_lexer)
        return self.lexer

class DillParser:
    def __init__(self):
        self.Grammar = None
        self.Parser = None

    def Create(self, grammar):
        self.Grammar = grammar
        self.Parser = LR1Parser(self.Grammar)

    def Save(self):
        with open('./serializedParser', 'wb') as _parser: 
            dill.dump(self.Parser, _parser)
    
    def Load(self):
        with open('./serializedParser', 'rb') as _parser:
            self.Parser = dill.load(_parser)
        return self.Parser