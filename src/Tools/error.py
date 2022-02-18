class ErrorClass:
    def __init__(self, line, column, info):
        self.info = info
        self.line = line
        self.column = column

    @property
    def error_type(self):
        return type(self).__name__[:-1]

    def __repr__(self):
        return str(self)
    
    def __str__(self):
        return f'({self.line}, {self.column}) - {self.error_type}: {self.info}'

class TypeErrors(ErrorClass): 
    pass
class NameErrors(ErrorClass): 
    pass
class ParamErrors(ErrorClass): 
    pass
class SemanticErrors(ErrorClass): 
    pass
class SyntacticErrors(ErrorClass): 
    pass
class AttributeErrors(ErrorClass): 
    pass
class LexicographicErrors(ErrorClass): 
    pass