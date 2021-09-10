import itertools as itt
from cmp.errors import SemanticError

class Attribute:
    def __init__(self, name, typex, expression=None):
        self.name = name
        self.type = typex
        self.expression = expression

    def __str__(self):
        _type = str(self.type) if self.type.name == 'AUTO_TYPE' else self.type.name
        return f'[attrib] {self.name} : {_type};'

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
        return_type = str(self.return_type) if self.return_type.name == 'AUTO_TYPE' else self.return_type.name
        return f'[method] {self.name}({params}): {return_type};'

    def __eq__(self, other):
        return other.name == self.name and \
            other.return_type == self.return_type and \
            other.param_types == self.param_types

class Type:
    def __init__(self, name:str, errors = []):
        self.name = name
        self.attributes = []
        self.methods = []
        self.parent = None
        self.errors = errors

    def set_parent(self, parent):
        self.parent = parent
    
    def get_attribute(self, name:str):
        try:
            return next(attr for attr in self.attributes if attr.name == name)
        except StopIteration:
            if self.parent is None:
                raise SemanticError(f'Attribute {name} is not defined in {self.name}.')
            try:
                return self.parent.get_attribute(name)
            except SemanticError:
                raise SemanticError(f'Attribute {name} is not defined in {self.name}.')

    def define_attribute(self, name:str, typex, expression = None):
        try:
            self.get_attribute(name)
        except SemanticError as err:
            attribute = Attribute(name, typex, expression)
            self.attributes.append(attribute)
            return attribute
        else:
            try:
                self.parent.get_attribute(name)
            except SemanticError:
                raise SemanticError(f'Attribute {name} is already defined in {self.name}.')
            else:
                raise SemanticError(f'Attribute {name} is an attribute of an inherited class')

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

    def define_method(self, name:str, param_names:list, param_types:list, return_type):
        if name in (method.name for method in self.methods):
            raise SemanticError(f'Method {name} is multiply defined.')
        
        method = Method(name, param_names, param_types, return_type)

        self.methods.append(method)
        return method

    #def all_attributes(self, clean=True):
    #    plain = OrderedDict() if self.parent is None else self.parent.all_attributes(False)
    #    for attr in self.attributes:
    #        plain[attr.name] = (attr, self)
    #    return plain.values() if clean else plain

    #def all_methods(self, clean=True):
    #    plain = OrderedDict() if self.parent is None else self.parent.all_methods(False)
    #    for method in self.methods:
    #        plain[method.name] = (method, self)
    #    return plain.values() if clean else plain

    def conforms_to(self, other):
        return other.bypass() or self == other or self.parent is not None and self.parent.conforms_to(other)

    def bypass(self):
        return False

    def join_type(self, other):
        if self.conforms_to(other): return other
        return self.join_type(other.parent)

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

class Context:
    def __init__(self):
        self.types = {}
        self.built_it()

    def create_type(self, name:str):  
        if name in self.types:
            if name in ['IO', 'String', 'Int', 'Bool', 'Object']:
                raise SemanticError(f'Redefinition of basic class {name}.')
            else:
                raise SemanticError(f'Class {name} was previously defined.')
        
        typex = self.types[name] = Type(name)
        return typex

    def get_type(self, name:str):
        try:
            return self.types[name]
        except KeyError:
            raise SemanticError(f'Type "{name}" is no defained.')
    
    #region Delte that later
    def __str__(self):
        return '{\n\t' + '\n\t'.join(y for x in self.types.values() for y in str(x).split('\n')) + '\n}'

    def __repr__(self):
        return str(self)
    #endregion
    
    def built_it(self):
        Object = self.create_type('Object')
        Io = self.create_type('IO')
        Int = self.create_type('Int')
        String = self.create_type('String')
        Bool = self.create_type('Bool')

        Io.set_parent(Object)
        Int.set_parent(Object)
        String.set_parent(Object)
        Bool.set_parent(Object)
        
        Object.define_method('abort', [], [], Object)
        Object.define_method('type_name', [], [], String)
        Object.define_method('copy', [], [], Object)

        Io.define_method('out_string', ['x'], [String], Io)
        Io.define_method('out_int', ['x'], [Int], Io)
        Io.define_method('in_string', [], [], String)
        Io.define_method('in_int', [], [], Int)

        String.define_method('length', [], [], Int)
        String.define_method('concat', ['s'], [String], String)
        String.define_method('substr', ['i', 'l'], [Int, Int], String)

class VariableInfo:
    def __init__(self, name, vtype):
        self.name = name
        self.type = vtype
    
    def __str__(self):
        return self.name + ' : ' + self.type.name + '\n'

class Scope:
    def __init__(self, parent=None):
        self.locals = []
        self.parent = parent
        self.children = []
        self.index = 0 if parent is None else len(parent)

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

    def find_variable(self, vname, scope_class, current_type, index=None):
        locals = self.locals if index is None else itt.islice(self.locals, index)
        try:
            return next(x for x in locals if x.name == vname)
        except StopIteration:
            variable = self.parent.find_variable(vname, scope_class, current_type, self.index) if not self.parent is None else None

            if variable is None and not current_type.parent is None and not current_type.parent.name is 'Object':
                variable = scope_class[current_type.parent.name].find_variable(vname, scope_class, current_type.parent)

            return variable

    def is_defined(self, vname, scope_class, current_type):
        return self.find_variable(vname, scope_class, current_type) is not None

    def is_local(self, vname):
        return any(True for x in self.locals if x.name == vname)

    def __str__(self):
        output = ''
        for x in self.locals:
            if not x.name == 'self':
                output += str(x)
        if self.children:
            for x in self.children:
                output += str(x)
        return output

class ErrorType(Type):
    def __init__(self):
        Type.__init__(self, '<error>')

    def conforms_to(self, other):
        return True

    def bypass(self):
        return True

    def __eq__(self, other):
        return isinstance(other, Type)
        