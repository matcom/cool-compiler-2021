class CoolError(Exception):
    def __init__(self, text: str, line: int, column: int):
        #print(text)
        #print(type(text))
        super().__init__(text)
        self.line = line
        self.column = column

    @property
    def error_type(self) -> str:
        return 'CoolError'
    
    @property
    def text(self) -> str:
        return self.args[0] 

    def __str__(self):
        return f'({self.line}, {self.column}) - {self.error_type}: {self.text}'
    
    def __repr__(self):
        return str(self)

class LexicographicError(CoolError):

    UNKNOWN_TOKEN = 'ERROR "%s"'
    UNDETERMINATED_STRING = 'Undeterminated string constant'
    EOF_COMMENT = 'EOF in comment'
    EOF_STRING = 'EOF in string constant'
    NULL_STRING = 'String contains null character'

    @property
    def error_type(self) -> str:
        return 'LexicographicError'