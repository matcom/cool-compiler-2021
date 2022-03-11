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
        return f'([attrib] {self.name} : {self.type.name})'

    def __repr__(self):
        return str(self)


class Method:
    def __init__(self, name, param_names, params_types, return_type):
        self.name = name
        self.param_names = param_names
        self.param_types = params_types
        self.return_type = return_type

    def __str__(self):
        params = ', '.join(f'{n}:{t.name}' for n, t in zip(self.param_names, self.param_types))
        return f'([method] {self.name}({params}): {self.return_type.name})'

    def __repr__(self):
        return str(self)

    # def __eq__(self, other):
    #     return other.name == self.name and \
    #            other.return_type == self.return_type and \
    #            other.param_types == self.param_types


class Type:
    def __init__(self, name: str):
        self.name = name
        self.attributes: OrderedDict = OrderedDict()
        self.methods: OrderedDict = OrderedDict()
        self.parent = None

    def set_parent(self, parent):
        if self.parent is not None:
            raise SemanticError(f'Parent type is already set for {self.name}.')
        self.parent = parent

    def get_attribute(self, name: str):
        try:
            return self.attributes[name]
        except KeyError:
            if self.parent is None:
                raise SemanticError(f'Attribute "{name}" is not defined in {self.name}.')
            try:
                return self.parent.get_attribute(name)
            except SemanticError:
                raise SemanticError(f'Attribute "{name}" is not defined in {self.name}.')

    def define_attribute(self, name: str, typex):
        try:
            self.get_attribute(name)
        except SemanticError:
            attribute = Attribute(name, typex)
            self.attributes[name] = attribute
            return attribute
        else:
            raise SemanticError(f'Attribute "{name}" is already defined in {self.name}.')

    def get_method(self, name: str):
        try:
            return self.methods[name]
        except KeyError:
            if self.parent is None:
                raise SemanticError(f'Method "{name}" is not defined in {self.name}.')
            try:
                return self.parent.get_method(name)
            except SemanticError:
                raise SemanticError(f'Method "{name}" is not defined in {self.name}.')

    def define_method(self, name: str, param_names: list, param_types: list, return_type):
        if name in self.methods:
            raise SemanticError(f'Method "{name}" already defined in {self.name}')

        method = Method(name, param_names, param_types, return_type)
        self.methods[name] = method
        return method

    def all_attributes(self, clean=True):
        plain = OrderedDict() if self.parent is None else self.parent.all_attributes(False)
        for attr in self.attributes.values():
            plain[attr.name] = (attr, self)
        return plain.values() if clean else plain

    def all_methods(self, clean=True):
        plain = OrderedDict() if self.parent is None else self.parent.all_methods(False)
        for method in self.methods.values():
            plain[method.name] = (method, self)
        return plain.values() if clean else plain

    def conforms_to(self, other):
        return other.bypass() or self == other or self.parent is not None and self.parent.conforms_to(other)

    def bypass(self):
        return False

    def join(self, other):
        if isinstance(self, ErrorType):
            return other
        if isinstance(other, ErrorType):
            return self

        self_ancestors = set(self.get_ancestors())

        current_type = other
        while current_type is not None:
            if current_type in self_ancestors:
                break
            current_type = current_type.parent
        return current_type

    # @staticmethod
    def multi_join(types):
        static_type = types[0]
        for t in types[1:]:
            static_type = static_type.join(t)
        return static_type


    def __str__(self):
        output = f'type {self.name}'
        # parent = '' if self.parent is None else f' : {self.parent.name}'
        # output += parent
        # output += ' {'
        # output += '\n\t' if self.attributes or self.methods else ''
        # output += '\n\t'.join(str(x) for x in self.attributes.values())
        # output += '\n\t' if self.attributes else ''
        # output += '\n\t'.join(str(x) for x in self.methods.values())
        # output += '\n' if self.methods else ''
        # output += '}\n'
        return output

    def __repr__(self):
        return str(self)

    def common_ancestor(self, other):
        current_anc = self.get_ancestors()
        other_anc = other

        while other_anc is not None:
            if other_anc in current_anc:
                return other_anc
            other_anc = other_anc.parent
        
        return current_anc[-1]
        
    def get_ancestors(self):
        if self.parent is None:
            return [self]
        return [self] + self.parent.get_ancestors()



class ErrorType(Type):
    def __init__(self):
        Type.__init__(self, '<error>')

    def conforms_to(self, other):
        return True

    def bypass(self):
        return True

    def __eq__(self, other):
        return isinstance(other, Type)


class VoidType(Type):
    def __init__(self):
        Type.__init__(self, '<void>')

    def conforms_to(self, other):
        raise Exception('Invalid type: void type.')

    def bypass(self):
        return True

    def __eq__(self, other):
        return isinstance(other, VoidType)


class IntType(Type):
    def __init__(self):
        Type.__init__(self, 'int')

    def __eq__(self, other):
        return other.name == self.name or isinstance(other, IntType)


class BoolType(Type):
    def __init__(self):
        Type.__init__(self, 'bool')

    def __eq__(self, other):
        return other.name == self.name or isinstance(other, BoolType)


class StringType(Type):
    def __init__(self, lenght):
        self.lenght = lenght
        Type.__init__(self, 'string')

    def __eq__(self, other):
        return other.name == self.name or isinstance(other, StringType)


class Context:
    def __init__(self):
        self.types = {}

    def create_type(self, name: str):
        if name in self.types:
            raise SemanticError(f'Type ({name}) already in context.')
        typex = self.types[name] = Type(name)
        return typex

    def get_type(self, name: str):
        try:
            return self.types[name]
        except KeyError:
            raise SemanticError(f'Type "{name}" is not defined.')

    def __str__(self):
        return '{\n\t' + '\n\t'.join(y for x in self.types for y in str(x).split('\n')) + '\n}'

    def __repr__(self):
        return str(self)


class VariableInfo:
    def __init__(self, name, vtype):
        self.name = name
        self.type = vtype

    def __str__(self):
        return self.name + ': ' + self.type.name
    
    def __repr__(self):
        return str(self)


class Scope:
    def __init__(self, parent=None):
        self.local_variable = []
        self.parent = parent
        self.children = []
        self.index = 0 if parent is None else len(parent)

    def __len__(self):
        return len(self.local_variable)

    def create_child(self):
        child = Scope(self)
        self.children.append(child)
        return child

    def define_variable(self, vname, vtype):
        info = VariableInfo(vname, vtype)
        self.local_variable.append(info)
        return info

    def find_variable(self, vname, index=None):
        local_variables = self.local_variable if index is None else itt.islice(self.local_variable, index)
        try:
            return next(x for x in local_variables if x.name == vname)
        except StopIteration:
            return self.parent.find_variable(vname, self.index) if self.parent is not None else None

    def is_variable_defined(self, vname):
        return self.find_variable(vname) is not None

    def is_local_variable(self, vname):
        return any(True for x in self.local_variable if x.name == vname)

    def __str__(self):
        s = ""
        scope = self
        while scope != None:
            for v in scope.local_variable:
                s += v.name + '\n'
            scope = scope.parent if scope.parent is not None else None
        return s
