from typing import List
from cool_cmp.shared.token import Token
from cool_cmp.shared.pipeline import IPipeable

class ILexer(IPipeable):
    """
    Lexer interface to implement
    """
    
    def __call__(self, program_string:str) -> List[Token]:
        raise NotImplementedError()
