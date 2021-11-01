import itertools as itt
from .error import SemanticException
from .attribute import Attribute
from .methods import Method

class Type:
    def __init__(self, name: str):
        self.name = name
        self.sealed = False  # indicates if this type is restricted for inheritance
        self.attributes = []
        self.methods = {}
        self.parent = None
        self.tag = None 
        self.max_tag = None # biggest tag reachable in dfs from this type

    def set_parent(self, parent):
        if self.parent is not None:
            raise SemanticException(f'Parent type is already set for {self.name}.')
        self.parent = parent

    def has_attr(self, name: str):
        try: 
            attr_name = self.get_attribute(name)
        except:
            return False
        else:
            return True

    def get_attribute(self, name: str):
        try:
            return next(attr for attr in self.attributes if attr.name == name)
        except StopIteration:
            if self.parent is None:
                raise SemanticException(
                    f'Attribute "{name}" is not defined in {self.name}.')
            try:
                return self.parent.get_attribute(name)
            except SemanticException:
                raise SemanticException(
                    f'Attribute "{name}" is not defined in {self.name}.')

    def define_attribute(self, name: str, typex):
        if name == 'self':
            raise SemanticException(
                "'self' cannot be the name of an attribute")
        try:
            self.get_attribute(name)
        except SemanticException:
            attribute = Attribute(name, typex)
            self.attributes.append(attribute)
            return attribute
        else:
            raise SemanticException(
                f'Attribute "{name}" is already defined in {self.name}.')

    def get_method(self, name: str):
        try:
            return self.methods[name]
        except KeyError:
            if self.parent is None:
                raise SemanticException(
                    f'Method "{name}" is not defined in {self.name}.')
            try:
                return self.parent.get_method(name)
            except SemanticException:
                raise SemanticException(
                    f'Method "{name}" is not defined in {self.name}.')


    def define_method(self, name: str, param_names: list, param_types: list, return_type):
        try:
            method = self.get_method(name)
        except SemanticException:
            method = self.methods[name] = Method(
                name, param_names, param_types, return_type)
            return method
        else:
            try:
                self.methods[name]
            except KeyError:
                if method.return_type != return_type or method.param_types != param_types:
                    raise SemanticException(
                        f'Method "{name}" is already defined in {self.name} with a different signature')
                else:
                    self.methods[name] = Method(name, param_names, param_types, return_type)
            else:
                raise SemanticException(
                    f'Method "{name}" is already defined in {self.name}')

        return method

    def get_all_attributes(self):
        all_attributes = self.parent and self.parent.get_all_attributes() or []
        all_attributes += [(self.name, attr) for attr in self.attributes]
        return all_attributes
    
    def get_all_methods(self):
        all_methods = self.parent and self.parent.get_all_methods() or []
        all_methods += [(self.name, method) for method in self.methods]
        return all_methods

    def conforms_to(self, other):
        return other.bypass() or self == other or self.parent is not None and self.parent.conforms_to(other)

    def bypass(self):
        return False

    def ancestors_path(self):
        l = []
        l.append(self)
        current_parent = self.parent
        while (current_parent is not None):
            l.append(current_parent)
            current_parent = current_parent.parent
        return l

    def join(self, other):
        if self.name == other.name: 
            return self

        other_path = other.ancestors_path()
        for p in self.ancestors_path():
            for o in other_path:
                if o.name == p.name:
                    return p
        return other

    def multiple_join(self, args):
        least_type = self
    
        for t in args:
            if isinstance(least_type, Error_Type) or isinstance(t, Error_Type):
                least_type = Error_Type()
                return least_type
            least_type = least_type.join(t)

        return least_type

    def __str__(self):
        output = f'type {self.name}'
        parent = '' if self.parent is None else f' : {self.parent.name}'
        output += parent
        output += ' {'
        output += '\n\t' if self.attributes or self.methods else ''
        output += '\n\t'.join(str(x) for x in self.attributes)
        output += '\n\t' if self.attributes else ''
        output += '\n\t'.join(str(x) for x in self.methods.values())
        output += '\n' if self.methods else ''
        output += '}\n'
        return output

    def __repr__(self):
        return str(self)


class Error_Type(Type):
    def __init__(self):
        Type.__init__(self, '<error>')

    def conforms_to(self, other):
        return True

    def bypass(self):
        return True

    def __eq__(self, other):
        return isinstance(other, Type)


class Object_Type(Type):
    def __init__(self):
        Type.__init__(self, 'Object')

    def bypass(self):
        return True

    def __eq__(self, other):
        return other.name == self.name or isinstance(other, Object_Type)


class IO_Type(Type):
    def __init__(self):
        Type.__init__(self, 'IO')

    def __eq__(self, other):
        return other.name == self.name or isinstance(other, IO_Type)


class String_Type(Type):
    def __init__(self):
        Type.__init__(self, 'String')
        self.sealed = True

    def __eq__(self, other):
        return other.name == self.name or isinstance(other, String_Type)


class Int_Type(Type):
    def __init__(self):
        Type.__init__(self, 'Int')
        self.sealed = True

    def __eq__(self, other):
        return other.name == self.name or isinstance(other, Int_Type)


class Bool_Type(Type):
    def __init__(self):
        Type.__init__(self, 'Bool')
        self.sealed = True

    def __eq__(self, other):
        return other.name == self.name or isinstance(other, Bool_Type)
