class Error:
    def __init__(self, line, column, text):
        self.line = line
        self.text = text
        self.column = column
    
    def __str__(self):
        return f'({self.line}, {self.column}) - {type(self).__name__[:-1]}: {self.text}'
    
    def __repr__(self):
        return str(self)

class TypeErrors(Error):pass
class NameErrors(Error): pass
class ParamErrors(Error): pass
class SemanticErrors(Error): pass
class SyntacticErrors(Error): pass
class AttributeErrors(Error): pass
class LexicographicErrors(Error): pass

class TypeException(Exception): pass
class NameException(Exception): pass
class ParamException(Exception): pass
class SemanticException(Exception): pass
class SyntacticException(Exception): pass
class AttributeException(Exception): pass
class MethodException(Exception): pass
class LexicographicException(Exception): pass