import itertools as itt
from collections import OrderedDict


class SemanticError(Exception):
    @property
    def text(self):
        return self.args[0]


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

    def set_parent(self, parent):
        self.parent = parent

    def get_attribute(self, name:str):
        try:
            return next(attr for attr in self.attributes if attr.name == name)
        except StopIteration:
            if self.parent is None:
                raise SemanticError(f'Attribute "{name}" is not defined in {self.name}.')
            try:
                return self.parent.get_attribute(name)
            except SemanticError:
                raise SemanticError(f'Attribute "{name}" is not defined in {self.name}.')

    def get_attribute_parent(self, name:str):
        try:
            next(attr for attr in self.attributes if attr.name == name)
            return self
        except StopIteration:
            if self.parent is None:
                raise SemanticError(f'Attribute "{name}" is not defined in {self.name}.')
            try:
                return self.parent.get_attribute_parent(name)
            except SemanticError:
                raise SemanticError(f'Attribute "{name}" is not defined in {self.name}.')

    def define_attribute(self, name:str, typex):
        try:
            self.get_attribute(name)
        except SemanticError:
            attribute = Attribute(name, typex)
            self.attributes.append(attribute)
            return attribute
        else:
            raise SemanticError(f'Attribute "{name}" is already defined in {self.name}.')

    def get_method(self, name:str):
        try:
            return next(method for method in self.methods if method.name == name)
        except StopIteration:
            if self.parent is None:
                raise SemanticError(f'Method "{name}" is not defined in {self.name}.')
            try:
                return self.parent.get_method(name)
            except SemanticError:
                raise SemanticError(f'Method "{name}" is not defined in {self.name}.')

    def get_method_parent(self, name:str):
        try:
            next(method for method in self.methods if method.name == name)
            return self
        except StopIteration:
            if self.parent is None:
                raise SemanticError(f'Method "{name}" is not defined in {self.name}.')
            try:
                return self.parent.get_method_parent(name)
            except SemanticError:
                raise SemanticError(f'Method "{name}" is not defined in {self.name}.')

    def define_method(self, name:str, param_names:list, param_types:list, return_type):
        if name in (method.name for method in self.methods):
            raise SemanticError(f'Method "{name}" already defined in {self.name}')

        method = Method(name, param_names, param_types, return_type)
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

    def conforms_to(self, other):
        return other.bypass() or self == other or self.parent is not None and self.parent.conforms_to(other)

    def bypass(self):
        return False

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


class ErrorType(Type):
    def __init__(self):
        Type.__init__(self, '<error>')

    def conforms_to(self, other):
        return True

    def bypass(self):
        return True

    def __eq__(self, other):
        return isinstance(other, ErrorType)


class ObjectType(Type):
    def __init__(self):
        Type.__init__(self, 'Object')
   
    def __eq__(self, other):
        return other.name == self.name or isinstance(other, ObjectType)    


class IntType(Type):
    def __init__(self):
        Type.__init__(self, 'Int')
        Type.set_parent(self, ObjectType())

    def __eq__(self, other):
        return other.name == self.name or isinstance(other, IntType)


class StringType(Type):
    def __init__(self):
        Type.__init__(self, 'String')
        Type.set_parent(self, ObjectType())

    def __eq__(self, other):
        return other.name == self.name or isinstance(other, StringType)


class BoolType(Type):
    def __init__(self):
        Type.__init__(self, 'Bool')
        Type.set_parent(self, ObjectType())
    
    def __eq__(self, other):
        return other.name == self.name or isinstance(other, BoolType)


class AutoType(Type):
    def __init__(self):
        Type.__init__(self, 'AUTO_TYPE')
        self.infered_type = None
    
    def __eq__(self, other):
        return isinstance(other, AutoType)


class SelfType(Type):
    def __init__(self):
       Type.__init__(self, 'SELF_TYPE')

    def __eq__(self, other):
        return isinstance(other, SelfType)


class IOType(Type):
    def __init__(self):
        Type.__init__(self, 'IO')
        Type.set_parent(self, ObjectType())
        
    def __eq__(self, other):
        return isinstance(other, IOType)
    

class Context:
    def __init__(self):
        self.types = {}

    def create_type(self, name:str):
        if name in self.types:
            raise SemanticError(f'Type with the same name ({name}) already in context.')
        typex = self.types[name] = Type(name)
        return typex

    def get_type(self, name:str):
        try:
            return self.types[name] if self.types[name] != AutoType() else AutoType()
        except KeyError:
            raise SemanticError(f'Type "{name}" is not defined.')

    def __str__(self):
        return '{\n\t' + '\n\t'.join(y for x in self.types.values() for y in str(x).split('\n')) + '\n}'

    def __repr__(self):
        return str(self)


class VariableInfo:
    def __init__(self, name, vtype):
        self.name = name
        self.type = vtype


class Scope:
    def __init__(self, parent=None):
        self.locals = []
        self.parent = parent
        self.children = []
        self.index = 0 if parent is None else len(parent)
        self.class_name = None
        self.method_name = None

    def __len__(self):
        return len(self.locals)

    def create_child(self, class_name=None, method_name=None):
        child = Scope(self)
        self.children.append(child)
        child.class_name = class_name
        child.method_name = method_name
        return child

    def define_variable(self, vname, vtype):
        info = VariableInfo(vname, vtype)
        self.locals.append(info)
        return info

    def remove_variable(self, vname):
        self.locals = [v for v in self.locals if v.name == vname]

    def find_variable(self, vname, index=None):
        locals = self.locals if index is None else itt.islice(self.locals, index)
        try:
            return next(x for x in locals if x.name == vname)
        except StopIteration:
            return self.parent.find_variable(vname, self.index) if self.parent is not None else None

    def find_variable_or_attribute(self, vname, current_type):
        var = self.find_variable(vname)
        if var is None:
            try: 
                return current_type.get_attribute(vname)
            except SemanticError:
                return None
        else:
            return var 

    def is_defined(self, vname, current_type):
        return self.find_variable_or_attribute(vname, current_type) is not None

    def is_local(self, vname):
        return any(True for x in self.locals if x.name == vname)

    def child_find_variable(self, vname):
        var =  next(x for x in self.locals if x.name == vname)
        if var is not  None:
            return self
        else:
            for child in self.children:
                child.child_find_variable(vname)  