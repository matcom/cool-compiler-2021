from cmp.semantic import Context as DeprecatedContext
from cool.semantic.type import Type, SelfType, AutoType
from cool.error.errors import SemanticError, TYPE_NOT_DEFINED, TYPE_ALREADY_DEFINED

class Context(DeprecatedContext):
    
    def __init__(self, special_types:dict):
        super().__init__()
        self.special_types = special_types
        for name in self.special_types:
            self.types[name] = self.special_types[name]()
    
    def get_type(self, name:str,self_type=None):
        if name == 'SELF_TYPE':
            if self_type:
                name = self_type.name
            else:
                return SelfType()
                # raise TypeError('Wrong argument combination: name is "SELF_TYPE" and no self_type given')
        elif name == 'AUTO_TYPE':
            return AutoType(self)
        try:
            return self.types[name]
        except KeyError:
            raise SemanticError(TYPE_NOT_DEFINED.format(name))
    
    def create_type(self, name:str):
        if name in self.types:
            raise SemanticError(TYPE_ALREADY_DEFINED.format(name))
        typex = self.types[name] = Type(name)
        return typex