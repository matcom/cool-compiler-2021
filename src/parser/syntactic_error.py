class SyntaxError():
    def __init__(self, msg, line, column):
        super().__init__()
        self.type = 'SyntacticError'
        self.value = msg
        self.line = line
        self.column = column

    def __str__(self):
        return f'({self.line}, {self.column}) - {self.type}: {self.value}'

    def __repr__(self):
        return str(self)