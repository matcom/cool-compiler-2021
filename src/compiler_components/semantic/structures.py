class SemanticError(Exception):
    @property
    def text(self):
        return f'({self.args[1]}, 11) - {self.__class__.__name__}: {self.args[0]}.'
class TypeError(SemanticError):
    pass
class NameError(SemanticError):
    pass 
class AttributeError(SemanticError):
    pass

class Attribute:
    def __init__(self, name, typex):
        self.name = name
        self.type = typex

class Method:
    def __init__(self, name, param_names, params_types, return_type):
        self.name = name
        self.param_names = param_names
        self.param_types = params_types
        self.return_type = return_type

    def __eq__(self, other):
        return other.name == self.name and other.return_type == self.return_type and other.param_types == self.param_types

class Type:
    def __init__(self, name:str,line=-1):
        self.name = name
        self.attributes = []
        self.methods = []
        self.parent = None
        self.sons = []
        self.line = line

    def set_parent(self, parent, pos=0):
        if self.parent is not None:
            raise SemanticError(f'Parent type is already set for {self.name}', pos)
        self.parent = parent
        parent.sons.append(self)

    def get_attribute(self, name:str,pos=0):
        try:
            return next(attr for attr in self.attributes if attr.name == name)
        except StopIteration:
            if self.parent is None:
                raise SemanticError(f'Attribute "{name}" is not defined in {self.name}',pos)
            try:
                return self.parent.get_attribute(name)
            except SemanticError:
                raise SemanticError(f'Attribute "{name}" is not defined in {self.name}',pos)

    def define_attribute(self, name:str, typex, pos):
        try:
            self.get_attribute(name)
        except SemanticError:
            a = Attribute(name, typex)
            self.attributes.append(a)
            return a
        else:
            raise SemanticError(f'Attribute "{name}" is already defined in {self.name}',pos)

    def get_method(self, name:str,pos=0):
        try:
            return next(method for method in self.methods if method.name == name)
        except StopIteration:
            if self.parent is None:
                raise AttributeError(f'Method "{name}" is not defined in {self.name}',pos)
            try:
                return self.parent.get_method(name)
            except SemanticError:
                raise AttributeError(f'Method "{name}" is not defined in {self.name}',pos)

    def define_method(self, name:str, param_names:list, param_types:list,  return_type, pos):
        try:
            method = self.get_method(name, pos)
            if method.return_type != return_type or method.param_types != param_types:
                raise SemanticError(f'Method "{name}" already defined in {self.name} with a different signature.', pos)
            else:
                raise SemanticError(f'Method "{name}" already defined in {self.name} ', pos)
            
            except SemanticError:
            method = Method(name, param_names, param_types, return_type)
            self.methods.append(method)

    def all_attributes(self, clean=True):
        plain = OrderedDict() if self.parent is None else self.parent.all_attributes(False)
        for attr in self.attributes:
            plain[attr.name] = (attr, self)
        return plain.values() if clean else plain

    def all_methods(self, clean=True):
        plain = OrderedDict() if self.parent is None else self.parent.all_methods(False)
        for method in self.methods:
            plain[method.name] = (method, self)
        return plain.values() if clean else plain

    def conforms_to(self, other):
        return other.bypass() or self == other or self.parent is not None and self.parent.conforms_to(other)