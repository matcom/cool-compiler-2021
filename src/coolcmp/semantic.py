from __future__ import annotations
import itertools as itt
from collections import OrderedDict

from coolcmp.ast import Node, ParamNode


class SemanticError(Exception):
    @property
    def text(self) -> str:
        return self.args[0]


class Attribute:
    def __init__(self, name: str, typex: Type):
        self.name = name
        self.type = typex

    def __str__(self) -> str:
        return f'[attrib] {self.name} : {self.type.name};'

    def __repr__(self) -> str:
        return str(self)


class Method:
    def __init__(self, name: str, param_names: list[str], params_types: list[Type], return_type: Type):
        self.name = name
        self.param_names = param_names
        self.param_types = params_types
        self.return_type = return_type

    def __str__(self) -> str:
        params = ', '.join(f'{n}: {t.name}' for n, t in zip(self.param_names, self.param_types))
        return f'[method] {self.name}({params}): {self.return_type.name};'

    def __eq__(self, other) -> bool:
        return other.name == self.name and \
            other.return_type == self.return_type and \
            other.param_types == self.param_types


class Type:
    def __init__(self, name: str):
        self.name = name
        self.attributes: list[Attribute] = []
        self.methods: list[Method] = []
        self.parent: Type | None = None

    def set_parent(self, parent: Type) -> None:
        if self.parent is not None:
            raise SemanticError(f'Parent type is already set for {self.name}.')
        self.parent = parent

    def get_attribute(self, name: str, from_class: str = None) -> Attribute:
        try:
            return next(attr for attr in self.attributes if attr.name == name)
        except StopIteration:
            if self.parent is None:
                raise SemanticError(f'Attribute "{name}" is not defined in {self.name}.')
            try:
                if from_class is not None and (self.parent.name == from_class or self.name == from_class):
                    raise SemanticError(f'Cyclic inheritance in class "{from_class}"')
                return self.parent.get_attribute(name, from_class)
            except SemanticError:
                raise SemanticError(f'Attribute "{name}" is not defined in {self.name}.')

    def define_attribute(self, name: str, typex: Type, from_class: str = None) -> Attribute:
        try:
            self.get_attribute(name, from_class)
        except SemanticError:
            attribute = Attribute(name, typex)
            self.attributes.append(attribute)
            return attribute
        else:
            raise SemanticError(f'Attribute "{name}" is already defined in {self.name}.')

    def get_method(self, name: str, get_owner: bool = False) -> Method | tuple[Method, Type]:
        try:
            meth = next(method for method in self.methods if method.name == name)
            return meth if not get_owner else (meth, self)
        except StopIteration:
            if self.parent is None:
                raise SemanticError(f'Method "{name}" is not defined in {self.name}.')
            try:
                return self.parent.get_method(name, get_owner)
            except SemanticError:
                raise SemanticError(f'Method "{name}" is not defined in {self.name}.')

    def define_method(self, name: str, param_names: list[str], param_types: list[Type], return_type: Type) -> Method:
        if name in (method.name for method in self.methods):
            raise SemanticError(f'Method "{name}" already defined in {self.name}')

        method = Method(name, param_names, param_types, return_type)
        self.methods.append(method)
        return method

    def all_attributes(self, clean: bool = True) -> dict[str, tuple[Attribute, Type]] | tuple[Attribute, Type]:
        plain = OrderedDict() if self.parent is None else self.parent.all_attributes(False)
        for attr in self.attributes:
            plain[attr.name] = (attr, self)
        return plain.values() if clean else plain

    def all_methods(self, clean: bool = True) -> dict[str, tuple[Method, Type]] | tuple[Method, Type]:
        plain = OrderedDict() if self.parent is None else self.parent.all_methods(False)
        for method in self.methods:
            plain[method.name] = (method, self)
        return plain.values() if clean else plain

    def get_ancestors(self, from_: str = None, ignore_from: bool = True) -> list[Type]:
        if not ignore_from and self.name == from_:
            raise SemanticError(f'Cyclic inheritance in class {from_}')
        if self.parent is None:
            return [self]
        else:
            return [self] + self.parent.get_ancestors(from_, False)

    def conforms_to(self, other: Type) -> bool:
        return other.bypass() or self == other or self.parent is not None and self.parent.conforms_to(other)

    def join(self, type_: Type) -> Type:
        ancestors = self.get_ancestors()
        current = type_
        while current is not None:
            if current in ancestors:
                break
            current = current.parent
        return current

    def bypass(self) -> bool:
        return False

    def __str__(self) -> str:
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

    def __repr__(self) -> str:
        return str(self)

    def __eq__(self, other: Type) -> bool:
        return self.name == other.name


class ErrorType(Type):
    def __init__(self):
        Type.__init__(self, '<error>')

    def conforms_to(self, other) -> bool:
        return True

    def bypass(self) -> bool:
        return True

    def __eq__(self, other: Type) -> bool:
        return isinstance(other, Type)


class VoidType(Type):
    def __init__(self):
        Type.__init__(self, '<void>')

    def conforms_to(self, other) -> bool:
        raise Exception('Invalid type: void type.')

    def bypass(self) -> bool:
        return True

    def __eq__(self, other: Type) -> bool:
        return isinstance(other, VoidType)


class IntType(Type):
    def __init__(self):
        Type.__init__(self, 'int')

    def __eq__(self, other) -> bool:
        return other.name == self.name or isinstance(other, IntType)


class Context:
    def __init__(self):
        self.types: dict[str, Type] = {}

    def create_type(self, name: str) -> Type:
        if name in self.types:
            raise SemanticError(f'Type with the same name ({name}) already in context.')
        typex = self.types[name] = Type(name)
        return typex

    def get_type(self, name: str) -> Type:
        try:
            return self.types[name]
        except KeyError:
            raise SemanticError(f'Type "{name}" is not defined.')

    def set_type(self, name: str, type_: Type) -> None:
        self.types[name] = type_

    def __str__(self) -> str:
        return '{\n\t' + '\n\t'.join(y for x in self.types.values() for y in str(x).split('\n')) + '\n}'

    def __repr__(self) -> str:
        return str(self)


class VariableInfo:
    def __init__(self, name: str, vtype: Type, is_attr: bool = False, is_param: bool = False):
        self.name = name
        self.type = vtype
        self.is_attr = is_attr
        self.is_param = is_param

    def __str__(self) -> str:
        return f'{self.name}: {self.type}'


class Scope:
    def __init__(self, parent: Scope = None):
        self.locals: list[VariableInfo] = []
        self.parent = parent
        self.children: list[Scope] = []
        self.index = 0 if parent is None else len(parent)

    def __len__(self) -> int:
        return len(self.locals)

    def create_child(self) -> Scope:
        child = Scope(self)
        self.children.append(child)
        return child

    def define_variable(self, vname: str, vtype: Type, is_attr: bool = False, is_param: bool = False) -> VariableInfo:
        info = VariableInfo(vname, vtype, is_attr, is_param)
        self.locals.append(info)
        return info

    def find_variable(self, vname: str, index: int = None) -> VariableInfo | None:
        locals_ = self.locals if index is None else itt.islice(self.locals, index)
        try:
            return next(x for x in locals_ if x.name == vname)
        except StopIteration:
            return self.parent.find_variable(vname, self.index) if self.parent is not None else None

    def is_defined(self, vname: str) -> bool:
        return self.find_variable(vname) is not None

    def is_local(self, vname: str) -> bool:
        return any(True for x in self.locals if x.name == vname)

    def __str__(self) -> str:
        s = 'Scope\n'
        for v in self.locals:
            s += f'{v.name}: {v.type.name}\n'
        if self.children:
            for child in self.children:
                s += str(child)
        return s
