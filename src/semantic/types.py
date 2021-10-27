from utils.errors import SemanticError


class Attribute:
    def __init__(self, name, typex, index):
        self.name = name
        self.type = typex
        self.index = index
        self.expr = None

    def __str__(self):
        return f'[attr] {self.name} : {self.type.name}'

    def __repr__(self):
        return str(self)


class Method:
    def __init__(self, name, param_names, param_types, return_type):
        self.name = name
        self.param_names = param_names
        self.param_types = param_types
        self.return_type = return_type


class Type:
    def __init__(self, name, position, parent=True):
        if name == 'ObjectType':
            return ObjectType(position)
        self.name = name
        self.attributes = {}
        self.methods = {}
        self.position = position
        if parent:
            self.parent = ObjectType(position)
        else:
            self.parent = None

    def set_parent(self, parent):
        if type(self.parent) != ObjectType and self.parent is not None:
            line, column = self.position
            raise SemanticError(
                f'Parent already defined for {self.name}', line, column)
        self.parent = parent

    def get_attribute(self, name, position):
        try:
            return self.attributes[name]
        except KeyError:
            if self.parent is None:
                line, column = self.position
                raise SemanticError(
                    f'Attribute {name} is not defined in {self.name}', line, column)
            try:
                return self.parent.get_attribute(name, position)
            except:
                line, column = self.position
                raise SemanticError(
                    f'Attribute {name} is not defined in {self.name}', line, column)

    def define_attribute(self, name, typex, position):
        try:
            self.attributes[name]
        except KeyError:
            try:
                self.get_attribute(name, position)
            except SemanticError:
                attribute = Attribute(name, typex, len(self.attributes))
                self.attributes[name] = attribute
                return attribute
            else:
                line, column = self.position
                raise SemanticError(
                    f'Attribute {name} is an attribute of an inherited class', line, column)
        else:
            line, column = self.position
            raise SemanticError(
                f'Attribute {name} is already defined', line, column)

    def get_method(self, name, position):
        try:
            return self.methods[name]
        except KeyError:
            if self.parent is None:
                line, column = self.position
                raise SemanticError(
                    f'Method {name} is not defined in {self.name}', line, column)
            try:
                return self.parent.get_method(name, position)
            except:
                line, column = self.position
                raise SemanticError(
                    f'Method {name} is not defined in {self.name}', line, column)

    def define_method(self, name, param_names, param_types, return_type, position=(0, 0)):
        if name in self.methods:
            line, column = self.position
            raise SemanticError(
                f'Method {name} is already defined', line, column)
        
        method = self.methods[name] = Method(name, param_names, param_types, return_type)
        return method


class ObjectType(Type):
    def __init__(self, position=(0, 0)):
        self.name = 'Object'
        self.attributes = {}
        self.methods = {}
        self.parent = None
        self.position = position
