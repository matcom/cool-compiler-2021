from typing import List
from cool_cmp.shared.token import ICoolToken
from cool_cmp.shared import ICoolService

class ILexer(ICoolService):
    """
    Lexer interface to implement
    """
    
    def __call__(self, program_string:str) -> List[ICoolToken]:
        raise NotImplementedError()
