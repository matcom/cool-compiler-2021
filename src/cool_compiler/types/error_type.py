from .type import  Type

class ErrorType(Type):
    def __init__(self):
        Type.__init__(self, '<error>')

    def conforms_to(self, other):
        return True

    def bypass(self):
        return True
    
    @property
    def is_error_type(self):
        return True

    def __eq__(self, other):
        return isinstance(other, Type)