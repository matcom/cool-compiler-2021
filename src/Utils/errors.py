class Error:
    def __init__(self, line, column, text):
        self.line = line
        self.text = text
        self.column = column
    
    def __str__(self):
        return f'({self.line}, {self.column}) - {type(self).__name__}: {self.text}'
    
    def __repr__(self):
        return str(self)

class TypesError(Error): pass
class NamesError(Error): pass
class ParamError(Error): pass
class SemanticError(Error): pass
class SyntacticError(Error): pass
class AttributesError(Error): pass
class LexicographicError(Error): pass