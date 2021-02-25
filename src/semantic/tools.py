from utils.errors import *
from semantic.types import Type

class Context:
    def __init__(self):
        self.types = {}

    def get_depth(self, class_name):
        typex = self.types[class_name]
        if typex.parent is None:
            return 0
        return 1 + self.get_depth(typex.parent.name)

    def build_inheritance_graph(self):
        graph = {}
        for type_name, typex in self.types.items():
            if typex.parent is not None:
                graph[type_name] = typex.parent.name 
            else:
                if type_name == 'SELF_TYPE':
                    continue
                graph[type_name] = None
        return graph

    def create_type(self, name:str, pos) -> Type:
        if name in self.types:
            error_text = SemanticError.TYPE_ALREADY_DEFINED
            raise SemanticError(*pos, error_text)
        typex = self.types[name] = Type(name, pos)
        return typex

    def get_type(self, name:str, pos) -> Type:
        try:
            return self.types[name]
        except KeyError:
            error_text = TypesError.TYPE_NOT_DEFINED % name
            raise TypesError(*pos, error_text)

    def __str__(self):
        return '{\n    ' + '\n    '.join(y for x in self.types.values() for y in str(x).split('\n')) + '\n}'

    def __repr__(self):
        return str(self)

class VariableInfo:
    def __init__(self, name, vtype, index=None):
        self.name = name
        self.type = vtype
        self.index = index

    def __str__(self):
        return f'{self.name} : {self.type.name}'

    def __repr__(self):
        return str(self)

