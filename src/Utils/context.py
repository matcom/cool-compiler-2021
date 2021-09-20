from Utils.errors import AttributeException, MethodException, SemanticException, TypeException


class Attribute:
    def __init__(self, name, type, expr=None):
        self.name = name
        self.type = type
        self.expr = expr

class Method:
    def __init__(self, name, param_names, params_types, return_type):
        self.name = name
        self.param_names = param_names
        self.param_types = params_types
        self.return_type = return_type

    def __eq__(self, other):
        return other.name == self.name and \
            other.return_type == self.return_type and \
            other.param_types == self.param_types

class Type:
    def __init__(self, name:str, parent=None):
        self.name = name
        self.parent = parent
        
        self.methods = []
        self.attributes = []
  
    def set_parent(self, parent):
        if parent.name in ['Bool', 'Int', 'String']:
            raise SemanticException(f'Class {self.name} cannot inherit class {parent.name}.')
        self.parent = parent

    def get_attribute(self, name):
        try:
            return next(attr for attr in self.attributes if attr.name == name)
        except StopIteration:
            if self.parent is None:
                raise AttributeException(f'Attribute {name} is not defined in {self.name}.')
            else: return self.parent.get_attribute(name)

    def define_attribute(self, name:str, type, expr=None):
        try:
            self.get_attribute(name)
        except AttributeException:
            attribute = Attribute(name, type, expr)
            self.attributes.append(attribute)
            return attribute
        else:
            try:
                self.parent.get_attribute(name)
            except AttributeException:
                raise AttributeException(f'Attribute {name} is already defined in {self.name}.')
            else: raise AttributeException(f'Attribute {name} is an attribute of an inherited class')

    def get_method(self, name:str):
        try:
            return next(method for method in self.methods if method.name == name)
        except StopIteration:
            if self.parent is None:
                raise MethodException(f'Method "{name}" is not defined in {self.name}.')
            else: return self.parent.get_method(name)

    def define_method(self, name:str, param_names:list, param_types:list, return_type):
        if name in (method.name for method in self.methods):
            raise MethodException(f'Method {name} is multiply defined.')
        
        method = Method(name, param_names, param_types, return_type)
        self.methods.append(method)
        return method

    def conforms_to(self, other):
        return other.bypass() or self == other or self.parent is not None and self.parent.conforms_to(other)

    def bypass(self):
        return False

    def join_type(self, other):
        if self.conforms_to(other): return other
        return self.join_type(other.parent)

class ErrorType(Type):
    def __init__(self):
        super().__init__('<error>')

    def conforms_to(self, other):
        return True

    def bypass(self):
        return True

    def __eq__(self, other):
        return isinstance(other, Type)

class Context:
    def __init__(self):
        self.types = {}
        self.basic = ['Object', 'IO', 'Int', 'String', 'Bool']
        self.create_basic()
 
    def create_type(self, name:str, parent=None):
        try:
            self.types[name]
            if name in self.basic:
                raise TypeException(f'Redefinition of basic class {name}.')
            else:
                raise TypeException(f'Class {name} was previously defined.')
        except KeyError:
            type = self.types[name] = Type(name, parent)
            return type

    def get_type(self, name:str):
        return self.types[name]

    def create_basic(self):
        Object = self.create_type('Object')
        Io = self.create_type('IO', Object)
        Int = self.create_type('Int', Object)
        String = self.create_type('String', Object)
        Bool = self.create_type('Bool', Object)
        
        Object.define_method('abort', [], [], Object)
        Object.define_method('type_name', [], [], String)
        Object.define_method('copy', [], [], Object)

        Io.define_method('out_string', ['x'], [String], Io)
        Io.define_method('out_int', ['x'], [Int], Io)
        Io.define_method('in_string', [], [], String)
        Io.define_method('in_int', [], [], Int)

        String.define_attribute('length', Int)
        String.define_attribute('str', String)
        String.define_method('length', [], [], Int)
        String.define_method('concat', ['s'], [String], String)
        String.define_method('substr', ['i', 'l'], [Int, Int], String)

        Int.define_attribute('int', Int)
        Bool.define_attribute('bool', Bool)