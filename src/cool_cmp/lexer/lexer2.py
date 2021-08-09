"""
Lexer usando ply
"""
from typing import List, Tuple

from cool_cmp.lexer.interface import ILexer
from cool_cmp.shared.token import ICoolToken
from cool_cmp.shared.errors import ErrorTracker
from cool_cmp.lexer.errors import LexerCoolError
# from cool2.cool.lexer.cool_lexer import cool_lexer
# from cool2.cool.lexer.comment_lexer import comment_lexer
# from cool2.cool.pipeline import lexer_pipeline

# from cool2.lib.lexer.lexer import DetailToken, DetailLexer

class CoolToken2(ICoolToken):
    
    def set_lex(self, lex:str):
        self.lex = (lex, self.row, self.column)

    def get_lex(self)->str:
        return self.lex[0]

    def set_type(self, typex:str):
        self.token_type = typex

    def get_type(self)->str:
        return self.token_type

    def set_position(self, line:int, column:int):
        self.lex = (self.lex[0], line, column)
        self.row = line
        self.column = column

    def get_position(self)->Tuple[int,int]:
        return (self.row,self.column)

    def __str__(self):
        return f"{self.get_lex()}:{self.get_type()} Line:{self.get_position()[0]} Column:{self.get_position()[1]}"

    def __repr__(self):
        return str(self)

class CoolLexer2(ILexer):
    
    @property
    def name(self)->str:
        return "lexer_name"
    
    def __init__(self):
        self.error_tracker = ErrorTracker() # Error tracker implementation
    
    def __call__(self, program_string:str) -> List[ICoolToken]:
        result = lexer_pipeline(program_string)
        tokens = result["text_tokens"]
        for err in result["errors"]:
            self.add_error(err)
        
        # Adding context
        for key, value in result.items():
            self.add_extra_info(key, value)
        
        return [self.__DetailToken2CoolToken2(tok) for tok in tokens]
    
    def add_error(self, error:LexerCoolError):
        self.error_tracker.add_error(error)
    
    def get_errors(self)->List[LexerCoolError]:
        errors = self.error_tracker.get_errors()
        return errors
    
    def __DetailToken2CoolToken2(self, detail_token)->CoolToken2:
        return CoolToken2(detail_token.lex, detail_token.token_type)
