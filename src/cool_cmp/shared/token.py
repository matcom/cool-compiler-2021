class Token:

    def __init__(self, lex:str, line:int, column:int):
        self.lex = lex
        self.line = line
        self.column = column

    def __str__(self):
        return f"{self.lex} Line:{self.line} Column:{self.column}"

    def __repr__(self):
        return str(self)