import itertools as itt
from collections import OrderedDict
from enum import Enum


class BasicTypes(Enum):
    BOOL = "Bool"
    INT = "Int"
    STRING = "String"
    SELF = "SELF_TYPE"
    OBJECT = "Object"
    IO = "IO"
    AUTO = "AUTO_TYPE"
    ERROR = "<error>"


class SemanticError(Exception):
    @property
    def text(self):
        return self.args[0]


class Attribute:
    def __init__(self, name, typex):
        self.name = name
        self.type = typex

    def __str__(self):
        return f"[attrib] {self.name} : {self.type.name};"

    def __repr__(self):
        return str(self)


class Method:
    def __init__(self, name, param_names, params_types, return_type):
        self.name = name
        self.param_names = param_names
        self.param_types = params_types
        self.return_type = return_type

    def __str__(self):
        params = ", ".join(
            f"{n}:{t.name}" for n, t in zip(self.param_names, self.param_types)
        )
        return f"[method] {self.name}({params}): {self.return_type.name};"

    def __eq__(self, other):
        return (
            other.name == self.name
            and other.return_type == self.return_type
            and other.param_types == self.param_types
        )


class Type:
    def __init__(self, name: str):
        self.name = name
        self.attributes = []
        self.methods = []
        self.parent = None
        self.tag = None
        self.max_tag = None

    def set_parent(self, parent):
        if self.parent is not None and self.parent.name != ObjType().name:
            raise SemanticError(f"Parent type is already set for {self.name}.")
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
                raise SemanticError(
                    f'Attribute "{name}" is not defined in {self.name}.'
                )
            try:
                return self.parent.get_attribute(name)
            except SemanticError:
                raise SemanticError(
                    f'Attribute "{name}" is not defined in {self.name}.'
                )

    def define_attribute(self, name: str, typex):
        try:
            self.get_attribute(name)
        except SemanticError:
            attribute = Attribute(name, typex)
            self.attributes.append(attribute)
            return attribute
        else:
            raise SemanticError(
                f'Attribute "{name}" is already defined in {self.name}.'
            )

    def get_method(self, name: str):
        try:
            return next(method for method in self.methods if method.name == name), self
        except StopIteration:
            if self.parent is None:
                raise SemanticError(f'Method "{name}" is not defined in {self.name}.')
            try:
                return self.parent.get_method(name)
            except SemanticError:
                raise SemanticError(f'Method "{name}" is not defined in {self.name}.')

    def get_type_that_define_method(self, name: str):
        for method in self.methods:
            if method.name == name:
                return self
        return self.parent.get_type_that_define_method(name)

    def define_method(
        self, name: str, param_names: list, param_types: list, return_type
    ):
        if name in (method.name for method in self.methods):
            raise SemanticError(f'Method "{name}" already defined in {self.name}')

        method = Method(name, param_names, param_types, return_type)
        self.methods.append(method)
        return method

    def get_all_attributes(self):
        all_attributes = self.parent and self.parent.get_all_attributes() or []
        all_attributes += [(self.name, attr) for attr in self.attributes]
        return all_attributes

    def get_all_methods(self):
        all_methods = self.parent and self.parent.get_all_methods() or []
        all_methods += [(self.name, method) for method in self.methods]
        return all_methods

    def all_attributes(self, clean=True):
        plain = (
            OrderedDict() if self.parent is None else self.parent.all_attributes(False)
        )
        for attr in self.attributes:
            plain[attr.name] = (attr, self)
        return plain.values() if clean else plain

    def all_methods(self, clean=True):
        plain = OrderedDict() if self.parent is None else self.parent.all_methods(False)
        for method in self.methods:
            plain[method.name] = (method, self)
        return plain.values() if clean else plain

    def conforms_to(self, other):
        return (
            other.bypass()
            or self == other
            or self.parent is not None
            and self.parent.conforms_to(other)
        )

    def bypass(self):
        return False

    def __str__(self):
        output = f"type {self.name}"
        parent = "" if self.parent is None else f" : {self.parent.name}"
        output += parent
        output += " {"
        output += "\n\t" if self.attributes or self.methods else ""
        output += "\n\t".join(str(x) for x in self.attributes)
        output += "\n\t" if self.attributes else ""
        output += "\n\t".join(str(x) for x in self.methods)
        output += "\n" if self.methods else ""
        output += "}\n"
        return output

    def __repr__(self):
        return str(self)


class ErrorType(Type):
    def __init__(self):
        Type.__init__(self, BasicTypes.ERROR.value)
        self.parent = ObjType()

    def conforms_to(self, other):
        return True

    def bypass(self):
        return True

    def __eq__(self, other):
        return isinstance(other, Type)


class ObjType(Type):
    def __init__(self):
        Type.__init__(self, BasicTypes.OBJECT.value)
        self.parent = None

    def __eq__(self, other):
        return isinstance(other, ObjType)

    def bypass(self):
        return True


class IntType(Type):
    def __init__(self):
        Type.__init__(self, BasicTypes.INT.value)
        self.parent = ObjType()

    def __eq__(self, other):
        return other.name == self.name or isinstance(other, IntType)


class StrType(Type):
    def __init__(self):
        Type.__init__(self, BasicTypes.STRING.value)
        self.parent = ObjType()

    def __eq__(self, other):
        return other.name == self.name or isinstance(other, StrType)


class BoolType(Type):
    def __init__(self):
        Type.__init__(self, BasicTypes.BOOL.value)
        self.parent = ObjType()

    def __eq__(self, other):
        return other.name == self.name or isinstance(other, BoolType)


class SelfType(Type):
    def __init__(self):
        Type.__init__(self, BasicTypes.SELF.value)
        self.parent = ObjType()

    def __eq__(self, other):
        return other.name == self.name or isinstance(other, SelfType)


class AutoType(Type):
    def __init__(self):
        Type.__init__(self, BasicTypes.AUTO.value)
        self.parent = ObjType()

    def bypass(self):
        return True

    def conforms_to(self, other):
        return True

    def __eq__(self, other):
        return other.name == self.name or isinstance(other, AutoType)


class Context:
    def __init__(self):
        self.types = {}
        self.graph = {}
        self.classes = {}
        self.graph['Object'] = ['IO', 'String', 'Bool', 'Int']
        self.graph['IO'] = []
        self.graph['String'] = []
        self.graph['Int'] = []
        self.graph['Bool'] = []

    def create_type(self, node):
        if node.id in self.types:
            raise SemanticError(
                f'Type with the same name ({node.id}) already in context.')
        typex = self.types[node.id] = Type(node.id)
        self.classes[node.id] = node
        if not self.graph.__contains__(node.id):
            self.graph[node.id] = []
        if self.graph.__contains__(node.parent):
            self.graph[node.parent].append(node.id)
        else:
            self.graph[node.parent] = [node.id]
        return typex

    def get_type(self, name: str):
        try:
            return self.types[name]
        except KeyError:
            raise SemanticError(f'Type "{name}" is not defined.')

    def set_type_tags(self, node='Object', tag=0):
        self.types[node].tag = tag
        for i, t in enumerate(self.graph[node]):
            self.set_type_tags(t, tag + i + 1)

    def set_type_max_tags(self, node='Object'):
        if not self.graph[node]:
            self.types[node].max_tag = self.types[node].tag
        else:
            for t in self.graph[node]:
                self.set_type_max_tags(t)
            maximum = 0
            for t in self.graph[node]:
                maximum = max(maximum, self.types[t].max_tag)
            self.types[node].max_tag = maximum

    def __str__(self):
        return (
            "{\n\t"
            + "\n\t".join(y for x in self.types.values() for y in str(x).split("\n"))
            + "\n}"
        )

    def __repr__(self):
        return str(self)

    def find_first_common_ancestor(self, expr_type1, expr_type2):
        while True:
            if expr_type1.conforms_to(expr_type2):
                if isinstance(expr_type2, AutoType):
                    return expr_type1
                return expr_type2
            elif expr_type2.conforms_to(expr_type1):
                if isinstance(expr_type1, AutoType):
                    return expr_type2
                return expr_type1
            else:
                return self.find_first_common_ancestor(expr_type1.parent, expr_type2)


class VariableInfo:
    def __init__(self, name, vtype):
        self.name = name
        self.type = vtype


class Scope:
    def __init__(self, id=-1, parent=None):
        self.locals = []
        self.parent = parent
        self.children = []
        self.index = 0 if parent is None else len(parent)
        self.id = id
        self.cil_locals = {}

    def __len__(self):
        return len(self.locals)

    def create_child(self, id=-1):
        child = Scope(id, self)
        self.children.append(child)
        return child

    def define_variable(self, vname, vtype):
        info = VariableInfo(vname, vtype)
        self.locals.append(info)
        return info

    def define_cil_local(self, vname, cilname, vtype=None):
        self.define_variable(vname, vtype)
        self.cil_locals[vname] = cilname

    def get_cil_local(self, vname):
        if self.cil_locals.__contains__(vname):
            return self.cil_locals[vname]
        else:
            return None

    def find_cil_local(self, vname, index=None):
        locals = self.cil_locals.items() if index is None else itt.islice(self.cil_locals.items(), index)
        try:
            return next(cil_name for name, cil_name in locals if name == vname)
        except StopIteration:
            return self.parent.find_cil_local(vname, self.index) if (self.parent is not None) else None

    def find_variable(self, vname, index=None):
        locals = self.locals if index is None else itt.islice(self.locals, index)
        try:
            return next(x for x in locals if x.name == vname)
        except StopIteration:
            return (
                self.parent.find_variable(vname, self.index)
                if self.parent is None
                else None
            )

    def is_defined(self, vname):
        return self.find_variable(vname) is not None

    def is_local(self, vname):
        return any(True for x in self.locals if x.name == vname)

    def my_find_var(self, vname):
        s = self
        while s is not None:
            for local in s.locals:
                if local.name == vname:
                    return local, s.id
            s = s.parent
        return None, None

    def __str__(self, tabs=0):
        ans = "\t" * tabs + f"\\__ID:{self.id}, VARS:"
        for var_info in self.locals:
            ans += f" ({var_info.name},{var_info.type.name})"

        children = "\n".join(child.__str__(tabs + 1) for child in self.children)

        if len(self.children) == 0:
            return f"{ans}"
        return f"{ans}\n{children}"
