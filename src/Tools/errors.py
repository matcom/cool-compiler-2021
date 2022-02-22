class CoolError(Exception):
    def __init__(self, text, line, column) -> None:
        Exception.__init__(self, text)
        self.line = line
        self.column = column
    
    @property
    def error_type(self):
        return 'CoolError'
    
    @property
    def text(self):
        return self.args[0]
    
    def __str__(self):
        return f'({self.line}, {self.column}) - {self.error_type}: {self.text}'
    
    def __repr__(self):
        return str(self)

class CompilerError(CoolError):
    
    @property
    def error_type(self):
        return 'CompilerError'

class LexicographicError(CoolError):
    
    @property
    def error_type(self):
        return 'LexicographicError'

class SyntaticError(CoolError):

    @property
    def error_type(self):
        return 'SyntacticError'
    

class SemanticError(CoolError):

    @property
    def error_type(self):
        return 'SemanticError'


class NamesError(SemanticError):

    @property
    def error_type(self):
        return 'NameError'
    

class TypesError(SemanticError):
    @property
    def error_type(self):
        return 'TypeError'
    

class AttributesError(SemanticError):
    @property
    def error_type(self):
        return 'AttributeError'
    