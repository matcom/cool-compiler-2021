from __future__ import annotations

import itertools as itt
from typing import Dict, List, Optional, OrderedDict, Set

import coolpyler.errors as errors


class BaseSemanticError(Exception):
    def __init__(self, msg: str) -> None:
        super().__init__(msg)
        self.msg = msg

    def with_pos(self, lineno: int, columnno: int) -> errors.CoolpylerError:
        raise NotImplementedError()


class NameError(BaseSemanticError):
    def with_pos(self, lineno: int, columnno: int) -> errors.CoolpylerError:
        return errors.NameError(lineno, columnno, self.msg)


class TypeError(BaseSemanticError):
    def with_pos(self, lineno: int, columnno: int) -> errors.CoolpylerError:
        return errors.TypeError(lineno, columnno, self.msg)


class AttributeError(BaseSemanticError):
    def with_pos(self, lineno: int, columnno: int) -> errors.CoolpylerError:
        return errors.AttributeError(lineno, columnno, self.msg)


class SemanticError(BaseSemanticError):
    def with_pos(self, lineno: int, columnno: int) -> errors.CoolpylerError:
        return errors.SemanticError(lineno, columnno, self.msg)


class Attribute:
    def __init__(self, name: str, type: Type):
        self.name = name
        self.type = type

    def __str__(self):
        return f"[attrib] {self.name} : {self.type.name};"

    def __repr__(self):
        return str(self)


class Method:
    def __init__(
        self,
        name: str,
        param_names: List[str],
        params_types: List[Type],
        return_type: Type,
    ):
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
        self.attributes: List[Attribute] = []
        self.methods: List[Method] = []
        self.parent: Optional[Type] = None

        self.reachable: Dict[str, Type] = {self.name: self}
        self.sealed = False

    def set_parent(self, parent: Type) -> None:
        if self.parent is not None:
            raise TypeError(f"Parent type is already set for `{self.name}`.")
        if parent.sealed:
            raise SemanticError(f"Cannot inherit from `{parent.name}`.")
        if parent.name in self.reachable:
            raise SemanticError(f"Cycle in hierarchy involving `{self.name}`.")
        self.parent = parent
        self.parent.update_reachable(self.reachable)

    def update_reachable(self, reachable: Dict[str, Type]):
        self.reachable.update(reachable)  # TODO
        if self.parent is not None:
            self.parent.update_reachable(self.reachable)

    def get_attribute(self, name: str) -> Attribute:
        try:
            return next(attr for attr in self.attributes if attr.name == name)
        except StopIteration:
            if self.parent is None:
                raise AttributeError(
                    f"Attribute `{name}` is not defined in `{self.name}`."
                )
            try:
                return self.parent.get_attribute(name)
            except BaseSemanticError:
                raise AttributeError(
                    f"Attribute `{name}` is not defined in `{self.name}`."
                )

    def define_attribute(self, name: str, type: Type) -> Attribute:
        if name == "self":
            raise SemanticError("`self` cannot be the name of an attribute.")
        try:
            self.get_attribute(name)
        except BaseSemanticError:
            attribute = Attribute(name, type)
            self.attributes.append(attribute)
            return attribute
        else:
            raise SemanticError(
                f"Attribute `{name}` is already defined in `{self.name}`."
            )

    def get_method(self, name: str) -> Method:
        try:
            return next(method for method in self.methods if method.name == name)
        except StopIteration:
            if self.parent is None:
                raise AttributeError(
                    f"Method `{name}` is not defined in `{self.name}`."
                )
            try:
                return self.parent.get_method(name)
            except BaseSemanticError:
                raise AttributeError(
                    f"Method `{name}` is not defined in `{self.name}`."
                )

    def define_method(
        self, name: str, param_names: list, param_types: list, return_type: Type
    ) -> Method:
        if name in (method.name for method in self.methods):
            raise SemanticError(f"Method `{name}` already defined in `{self.name}`")

        if "self" in param_names:
            raise SemanticError("`self` cannot be the name of a formal parameter.")

        method = Method(name, param_names, param_types, return_type)
        self.methods.append(method)
        return method

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

    def conforms_to(self, other: Type) -> bool:
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
        Type.__init__(self, "ERROR")

    def conforms_to(self, other: Type):
        return True

    def bypass(self):
        return True

    def __eq__(self, other):
        return isinstance(other, Type)


class ObjectType(Type):
    def __init__(self):
        Type.__init__(self, "Object")

    def __eq__(self, other: Type):
        return other.name == self.name or isinstance(other, ObjectType)


class IntType(Type):
    def __init__(self):
        Type.__init__(self, "Int")
        self.sealed = True

    def __eq__(self, other: Type):
        return other.name == self.name or isinstance(other, IntType)


class BoolType(Type):
    def __init__(self):
        Type.__init__(self, "Bool")
        self.sealed = True

    def __eq__(self, other: Type):
        return other.name == self.name or isinstance(other, BoolType)


class StringType(Type):
    def __init__(self):
        Type.__init__(self, "String")
        self.sealed = True

    def __eq__(self, other: Type):
        return other.name == self.name or isinstance(other, StringType)


class IOType(Type):
    def __init__(self):
        Type.__init__(self, "IO")

    def __eq__(self, other: Type):
        return other.name == self.name or isinstance(other, IOType)


class SelfType(Type):
    def __init__(self, type: Type):
        Type.__init__(self, f"SELF_TYPE_{type.name}")
        self.type = type

    def __eq__(self, other: Type):
        return other.name == self.name or isinstance(other, SelfType)

    def conforms_to(self, other: Type):
        return (
            isinstance(other, SelfType) and self.type == other.type
        ) or self.type.conforms_to(other)


class VariableInfo:
    def __init__(self, name: str, vtype: Type):
        self.name = name
        self.type = vtype


class Scope:
    def __init__(self, parent: Optional[Scope] = None):
        self.locals = []
        self.parent = parent
        self.children = []
        self.index = 0 if parent is None else len(parent)

    def __len__(self):
        return len(self.locals)

    def create_child(self) -> Scope:
        child = Scope(self)
        self.children.append(child)
        return child

    def define_variable(
        self, vname: str, vtype: Type, first_self=False, force=False
    ) -> VariableInfo:
        if (vname == "self" and not first_self) or (self.is_local(vname) and not force):
            raise SemanticError("Variable already exists in the current scope")

        info = VariableInfo(vname, vtype)
        self.locals.append(info)
        return info

    def find_variable(self, vname: str, index: Optional[int] = None) -> VariableInfo:
        locals = self.locals if index is None else itt.islice(self.locals, index)
        try:
            return next(x for x in locals if x.name == vname)
        except StopIteration:
            if self.parent is None:
                raise NameError(f"Variable `{vname}` is not defined in current scope.")
            try:
                return self.parent.find_variable(vname, self.index)
            except BaseSemanticError:
                raise NameError(f"Variable `{vname}` is not defined in current scope.")

    def is_defined(self, vname: str) -> bool:
        return self.find_variable(vname) is not None

    def is_local(self, vname: str) -> bool:
        return any(True for x in self.locals if x.name == vname)
