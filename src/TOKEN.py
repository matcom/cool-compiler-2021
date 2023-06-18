class LexToken:
    def __init__(self, name, symbol, Ln, Col):
        self.name = name
        self.symbol = symbol
        self.Ln = Ln
        self.Col = Col

    def to_string(self):
        return "LexToken({},'{}',{},{})".format(self.name, self.symbol, self.Ln, self.Col)