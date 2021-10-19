def find_column(text, pos):
    line_start = text.rfind('\n', 0, pos) + 1
    return (pos - line_start) + 1


class Token:
    def __init__(self, lex, token_type, row, column):
        self.lex = lex
        self.type = token_type
        self.line = line
        self.column = column

    def __str__(self):
        return f'{self.type}: {self.lex} ({self.line}, {self.column})'

    def __repr__(self):
        return str(self)
