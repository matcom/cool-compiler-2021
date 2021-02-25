import itertools as itt
from collections import OrderedDict

class InternalError(Exception):
    @property
    def text(self):
        return "Internal Error: " + self.args[0]

class SemanticError(Exception):
    @property
    def text(self):
        return "Semantic Error: " + self.args[0]

class TypeError(SemanticError):
    @property
    def text(self):
        return "Type Error: " + self.args[0]

class AttributeError(SemanticError):
    @property
    def text(self):
        return "Attribute Error: " + self.args[0]

class Attribute:
    def __init__(self, name, typex):
        self.name = name
        self.type = typex

    def __str__(self):
        return f'[attrib] {self.name} : {self.type.name};'

    def __repr__(self):
        return str(self)

class Method:
    def __init__(self, name, param_names, params_types, return_type):
        self.name = name
        self.param_names = param_names
        self.param_types = params_types
        self.return_type = return_type

    def __str__(self):
        params = ', '.join(f'{n}:{t.name}' for n,t in zip(self.param_names, self.param_types))
        return f'[method] {self.name}({params}): {self.return_type.name};'

    def __eq__(self, other):
        return other.name == self.name and \
            other.return_type == self.return_type and \
            other.param_types == self.param_types

class Type:
    def __init__(self, name:str):
        self.name = name
        self.attributes = []
        self.methods = []
        self.parent = None
        self.index = -1

    def set_parent(self, parent):
        if self.parent is not None:
            raise SemanticError(f'Type \'{self.name}\' already has parent type \'{self.parent.name}\'. Type \'{parent.name}\' cannot be set as parent.')
        if parent.name in {"String", "Int", "Bool"}:
            raise SemanticError(f'Cannot set \'{self.name}\' parent, \'{parent.name}\' type cannot be inherited.')
        self.parent = parent

    def get_attribute(self, name:str):
        try:
            return next(attr for attr in self.attributes if attr.name == name)
        except StopIteration:
            if self.parent is None:
                raise AttributeError(f'Attribute "{name}" is not defined in {self.name}.')
            try:
                return self.parent.get_attribute(name)
            except SemanticError:
                raise AttributeError(f'Attribute "{name}" is not defined in {self.name}.')

class SelfType(Type):
    def __init__(self):
        self.name = "SELF_TYPE"
    def conforms_to(self, other):
        #if isinstance(other, SelfType):
        #    return True
        raise InternalError("SELF_TYPE yet to be assigned, cannot conform.")
    def bypass(self):
        raise InternalError("SELF_TYPE yet to be assigned, cannot bypass.")

class AutoType(Type):
    pass

class ErrorType(Type):
    pass

class Context:
    def __init__(self) -> None:
        self.types = {}
        self.num_autotypes = 0
        self.type_graph = None
    
    def create_type(self, name:str) -> Type:
        if name in self.types:
            raise SemanticError(f'Type with the same name ({name}) already exists.')
        if name[0] != name[0].upper:
            raise SemanticError(f'Type name ({name}) must start with upper case')
        typex = self.types[name] = Type(name)
        return typex
    
    def get_type(self, name:str, selftype=True, autotype=True) -> Type:
        if selftype and name == "SELF_TYPE":
            return SelfType()
        if autotype and name == "AUTO_TYPE":
            self.num_autotypes += 1
            return AutoType(f"T{self.num_autotypes}", [self.types["Object"]], self.types)
        try:
            return self.types[name]
        except KeyError:
            raise TypeError(f'Type "{name}" is not defined.')
    
    def __str__(self):
        return '{\n\t' + '\n\t'.join(y for x in self.types.values() for y in str(x).split('\n')) + '\n}'

    def __repr__(self):
        return str(self)

class VariableInfo:
    def __init__(self, name, vtype):
        self.name = name
        self.type = vtype
    
    def __str__(self):
        return self.name + ":" + self.type


class Scope:
    def __init__(self, parent=None):
        self.locals = []
        self.parent = parent
        self.children = []
        self.index = 0 if parent is None else len(parent)
        self.current_child = -1

    def __len__(self):
        return len(self.locals)

    def create_child(self):
        child = Scope(self)
        self.children.append(child)
        return child

    def define_variable(self, vname, vtype):
        info = VariableInfo(vname, vtype)
        self.locals.append(info)
        return info

    def find_variable(self, vname, index=None):
        locals = self.locals if index is None else itt.islice(self.locals, index)
        try:
            return next(x for x in locals if x.name == vname)
        except StopIteration:
            try:
                return self.parent.find_variable(vname, self.index)# if self.parent else None
            except AttributeError:
                return None

    def is_defined(self, vname):
        return self.find_variable(vname) is not None

    def is_local(self, vname):
        return any(True for x in self.locals if x.name == vname)
    
    def next_child(self):
        self.current_child += 1
        return self.children[self.current_child]
    
    def reset(self):
        self.current_child = -1
        for child in self.children:
            child.reset()