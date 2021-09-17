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

class TypeException(Exception): pass
class NameException(Exception): pass
class ParamException(Exception): pass
class SemanticException(Exception): pass
class SyntacticException(Exception): pass
class AttributeException(Exception): pass
class MethodException(Exception): pass
class LexicographicException(Exception): pass