"""
Lexer errors
"""

from cool_cmp.shared.errors import CoolError
from cool_cmp.shared.token import ICoolToken

class LexerCoolError(CoolError):
    """
    Error class for lexical errors
    """
    
    def __init__(self, error_message:str, error_token:ICoolToken):
        super().__init__(error_message)
        self.token = error_token