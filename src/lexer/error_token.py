from ply.lex import LexToken

class ErrorToken(LexToken):
    def __init__(self, msg, line, column):
        super().__init__()
        self.type = 'LexicographicError'
        self.value = msg
        self.line = line
        self.column = column

    def __str__(self):
        return f'({self.line}, {self.column}) - {self.type}: {self.value}'

    def __repr__(self):
        return str(self)