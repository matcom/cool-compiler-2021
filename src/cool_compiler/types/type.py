from collections import OrderedDict
from .tools import  *


class Type:
    def __init__(self, name:str):
        self.name = name
        self.attributes = []
        self.methods = []
        self.parent = None
         
    @property
    def is_shield(self):
        return False
    
    @property
    def is_self_type(self):
        return False

    @property
    def is_auto_type(self):
        return False
    
    @property
    def is_error_type(self):
        return False

    def bypass(self):
        return False

    
    def real_type(self, possible):
        return self
    
    def conforms_to(self, other):
        return other.bypass() or self == other or self.parent is not None and self.parent.conforms_to(other)

    def __eq__(self,other):
        return other.name == self.name
#################################################################################################################
    @property
    def ite_attributes(self):
        for attr in self.attributes:
            yield attr.name, attr.type
        if not self.parent is None:
            for attr in self.parent.ite_attributes:
                yield attr
    
    def set_parent(self, parent):
        if self.parent is not None:
            raise SemanticError(f'Parent type is already set for {self.name}.')
        self.parent = parent

    def get_attribute(self, name:str) -> Attribute:
        try:
            return next(attr for attr in self.attributes if attr.name == name)

        except StopIteration:
            if self.parent is None:
                raise SemanticError(f'Attribute "{name}" is not defined in {self.name}.')
            try:
                return self.parent.get_attribute(name)
            except SemanticError:
                raise SemanticError(f'Attribute "{name}" is not defined in {self.name}.')

    def define_attribute(self, name:str, typex):
        if name == "self":
            raise SemanticError("Can't define attribute with name self")
        try:
            self.get_attribute(name)
        except SemanticError:
            attribute = Attribute(name, typex)
            self.attributes.append(attribute)
            return attribute
        else:
            raise SemanticError(f'Attribute "{name}" is already defined in {self.name}.')

    def get_method(self, name:str) -> Method:
        try:
            return next(method for method in self.methods if method.name == name)

        except StopIteration:
            if self.parent is None:
                raise SemanticError(f'Method "{name}" is not defined in {self.name}.')
            try:
                return self.parent.get_method(name)
            except SemanticError:
                raise SemanticError(f'Method "{name}" is not defined in {self.name}.')

    def define_method(self, name:str, params:list, return_type):
        if name in (method.name for method in self.methods):
            raise SemanticError(f'Method "{name}" already defined in {self.name}')

        names = ['self']
        for _name, _t in params:
            if _name in names:
                raise SemanticError(f"Formal parameter a is multiply defined")
            names.append(_name)
        
        method = Method(name, params, return_type)
        self.methods.append(method)
        return method

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

    

    def __str__(self):
        output = f'type {self.name}'
        parent = '' if self.parent is None else f' : {self.parent.name}'
        output += parent
        output += ' {'
        output += '\n\t' if self.attributes or self.methods else ''
        output += '\n\t'.join(str(x) for x in self.attributes)
        output += '\n\t' if self.attributes else ''
        output += '\n\t'.join(str(x) for x in self.methods)
        output += '\n' if self.methods else ''
        output += '}\n'
        return output

    def __repr__(self):
        return str(self)

    

   