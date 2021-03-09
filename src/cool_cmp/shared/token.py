class Token:

    # def __init__(self, lex:str, typex:str, line:int, column:int):
    #     self.lex = lex
    #     self.typex = typex
    #     self.line = line
    #     self.column = column

    def set_lex(self, lex:str):
        raise NotImplementedError()

    def set_type(self, typex:str):
        raise NotImplementedError()

    def set_position(self, line, column):
        raise NotImplementedError

    def __str__(self):
        return f"{self.lex}:{self.typex} Line:{self.line} Column:{self.column}"

    def __repr__(self):
        return str(self)