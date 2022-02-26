from ply.lex import LexError
from cool.utils.Errors.CoolError import CoolError

class LexerErrors(CoolError):
    def __init__(self, column: int, line: int, text: str):
        super().__init__(column, line, text)
        
    UNKNOWN_TOKEN = 'Unknown token'
    NULL_STRING = 'Null character in string'
    UNTERMINATED_STRING = 'Unterminated string'
    EOF_STRING = 'EOF in string'
    EOF_COMMENT = 'EOF in comment'

    @property
    def errorType(self):
        return "LexicographicError"
