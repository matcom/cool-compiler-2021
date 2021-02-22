class Token:
    def __init__(self, line, column, type, lex):
        self.line = line
        self.column = column
        self.type = type
        self.lex = lex

    def __str__(self):
        return f'({self.line}, {self.column}) - {self.type} : {self.lex}'

    def __repr__(self):
        return str(self)