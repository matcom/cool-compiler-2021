import itertools as itt
from collections import OrderedDict
from typing import FrozenSet, List, Set, Tuple

from semantics.errors import *


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
        self.index = -1

    def set_parent(self, parent):
        if self.parent is not None:
            raise SemanticError(
                f"Type '{self.name}' already has parent type '{self.parent.name}'. Type '{parent.name}' cannot be set as parent."
            )
        if parent.name in {"String", "Int", "Bool"}:
            raise SemanticError(
                f"Cannot set '{self.name}' parent, '{parent.name}' type cannot be inherited."
            )
        self.parent = parent

    def define_attribute(self, name: str, typex):
        try:
            self.get_attribute(name)
        except SemanticError:
            attribute = Attribute(name, typex)
            self.attributes.append(attribute)
            return attribute
        else:
            raise SemanticError(
                f'Attribute "{name}" is already defined in "{self.name}".'
            )

    def get_attribute(self, name: str, first=None):
        if not first:
            first = self.name
        elif first == self.name:
            raise AttributeError(f'Attribute "{name}" is not defined in {self.name}.')

        try:
            return next(attr for attr in self.attributes if attr.name == name)
        except StopIteration:
            if self.parent is None:
                raise AttributeError(
                    f'Attribute "{name}" is not defined in {self.name}.'
                )
            try:
                return self.parent.get_attribute(name, first=first)
            except SemanticError:
                raise AttributeError(
                    f'Attribute "{name}" is not defined in {self.name}.'
                )

    def get_method(self, name: str, local: bool = False, first=None):
        if not first:
            first = self.name
        elif first == self.name:
            raise AttributeError(
                f'Method "{name}" is not defined in class {self.name}.'
            )

        try:
            return next(method for method in self.methods if method.name == name)
        except StopIteration:
            if self.parent is None:
                raise AttributeError(
                    f'Method "{name}" is not defined in class {self.name}.'
                )
            try:
                return self.parent.get_method(name, first=first)
            except AttributeError:
                raise AttributeError(
                    f'Method "{name}" is not defined in class {self.name}.'
                )

    def define_method(
        self, name: str, param_names: list, param_types: list, return_type
    ):
        if name in (method.name for method in self.methods):
            raise SemanticError(f"Method '{name}' already defined in '{self.name}'")

        try:
            parent_method = self.get_method(name)
        except SemanticError:
            parent_method = None
        if parent_method:
            error_list = []
            return_type.swap_self_type(self)
            return_clone = return_type.clone()
            parent_method.return_type.swap_self_type(self)
            if not conforms(return_type, parent_method.return_type):
                error_list.append(
                    f"    -> Same return type: Redefined method has '{return_clone.name}' as return type instead of '{parent_method.return_type.name}'."
                )
            if len(param_types) != len(parent_method.param_types):
                error_list.append(
                    f"    -> Same amount of params: Redefined method has {len(param_types)} params instead of {len(parent_method.param_types)}."
                )
            else:
                count = 0
                err = []
                for param_type, parent_param_type in zip(
                    param_types, parent_method.param_types
                ):
                    param_clone = param_type.clone()
                    if not conforms(param_type, parent_param_type):
                        err.append(
                            f"        -Param number {count} has {param_clone.name} as type instead of {parent_param_type.name}"
                        )
                    count += 1
                if err:
                    s = f"    -> Same param types:\n" + "\n".join(
                        child for child in err
                    )
                    error_list.append(s)
            return_type.swap_self_type(self, back=True)
            parent_method.return_type.swap_self_type(self, back=True)
            if error_list:
                err = (
                    f"Redifined method '{name}' in class '{self.name}' does not have:\n"
                    + "\n".join(child for child in error_list)
                )
                raise SemanticError(err)

        method = Method(name, param_names, param_types, return_type)
        self.methods.append(method)

        return method

    def all_attributes(self, clean=True, first=None):
        if not first:
            first = self.name
        elif first == self.name:
            return OrderedDict.values() if clean else OrderedDict()

        plain = (
            OrderedDict()
            if self.parent is None
            else self.parent.all_attributes(clean=False, first=first)
        )
        for attr in self.attributes:
            plain[attr.name] = (attr, self)
        return plain.values() if clean else plain

    def all_methods(self, clean=True, first=None):
        if not first:
            first = self.name
        elif first == self.name:
            return OrderedDict.values() if clean else OrderedDict()

        plain = (
            OrderedDict()
            if self.parent is None
            else self.parent.all_methods(clean=False, first=first)
        )
        for method in self.methods:
            plain[method.name] = (method, self)
        return plain.values() if clean else plain

    def conforms_to(self, other, first=None):
        if not first:
            first = self.name
        elif self.name == first:
            return False
        return (
            other.bypass()
            or self == other
            or self.parent
            and self.parent.conforms_to(other, first)
        )

    def bypass(self):
        return False

    def least_common_ancestor(self, other):
        this = self
        if isinstance(this, ErrorType) or isinstance(other, ErrorType):
            return ErrorType()

        while this.index < other.index:
            other = other.parent
        while other.index < this.index:
            this = this.parent
        if not (this and other):
            return None
        while this.name != other.name:
            this = this.parent
            other = other.parent
            if this == None:
                return None
        return this

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


class TypeBag:
    def __init__(self, type_set, heads=[]) -> None:
        self.type_set: set = (
            type_set if isinstance(type_set, set) else from_dict_to_set(type_set)
        )
        self.heads: list = heads
        if len(self.type_set) == 1:
            self.heads = list(self.type_set)

        self.name = "undefined"
        self.condition_list = []
        self.conform_list = []
        self.generate_name()

    def set_conditions(self, condition_list, conform_list):
        self.condition_list = condition_list
        self.conform_list = conform_list
        self.update_type_set_from_conforms()

    def update_type_set_from_conforms(self):
        intersect_set = set()
        for conform_set in self.conform_list:
            intersect_set = intersect_set.union(conform_set)
        self.type_set = self.type_set.intersection(intersect_set)
        self.update_heads()

    def update_heads(self):
        new_heads = []
        visited = set()
        for head in self.heads:
            if head in self.type_set:
                new_heads.append(head)
                continue
            pos_new_head = []
            lower_index = 2 ** 32
            for typex in self.type_set:
                if typex in visited:
                    continue
                # if typex.conforms_to(head):
                visited.add(typex)
                if typex.index < lower_index:
                    pos_new_head = [typex]
                    lower_index = typex.index
                elif typex.index == lower_index:
                    pos_new_head.append(typex)
            new_heads += pos_new_head
        self.heads = new_heads
        self.generate_name()

    def swap_self_type(self, swap_type, back=False):
        if not back:
            remove_type = SelfType()
            add_type = swap_type
        else:
            remove_type = swap_type
            add_type = SelfType()

        try:
            self.type_set.remove(remove_type)
            self.type_set.add(add_type)
        except KeyError:
            return self

        # for i in range(len(self.heads)):
        #    typex = self.heads[i]
        #    if typex.name == remove_type.name:
        #        self.heads[i] = add_type
        #        break
        #
        # self.generate_name()
        self.update_heads()
        return self

    def add_self_type(self, add_type) -> bool:
        if SelfType() in self.type_set and not add_type in self.type_set:
            self.type_set.add(add_type)
            return True
        return False

    def remove_self_type(self, remove_type):
        try:
            self.type_set.remove(remove_type)
        except KeyError:
            pass
        self.type_set.add(SelfType())
        self.update_heads()

    def generate_name(self):
        if len(self.type_set) == 1:
            self.name = self.heads[0].name
            return self.name

        s = "{"
        s += ", ".join(
            typex.name for typex in sorted(self.type_set, key=lambda t: t.index)
        )
        s += "}"
        self.name = s
        return s

    def clone(self):
        clone = TypeBag(self.type_set.copy(), self.heads.copy())
        clone.condition_list = self.condition_list.copy()
        clone.conform_list = self.conform_list.copy()
        return clone

    def __str__(self):
        return self.name

    def __repr__(self):
        return str(self)


class SelfType(Type):
    def __init__(self):
        self.name = "SELF_TYPE"
        self.index = 2 ** 31

    def conforms_to(self, other):
        if isinstance(other, SelfType):
            return True
        return False
        raise InternalError("SELF_TYPE is yet to be assigned, cannot conform.")

    def bypass(self):
        return False
        raise InternalError("SELF_TYPE is yet to be assigned, cannot bypass.")

    def __hash__(self) -> int:
        return hash(self.name)

    def __eq__(self, o: object) -> bool:
        return isinstance(o, SelfType)

    def __str__(self):
        return self.name

    def __repr__(self):
        return str(self)


class FuncType(Type):
    def __init__(self, name: str, params: Tuple[Type, ...], ret_type: Type) -> None:
        self.name = name
        self.params = params
        self.ret_type = ret_type

    def conforms_to(self, other):
        if not isinstance(other, FuncType):
            raise InternalError(
                (
                    "A FunctionType can only conform to other Function"
                    f"Type, not to {other.__class__.__name__}"
                )
            )


class ErrorType(TypeBag):
    def __init__(self):
        self.name = "<error-type>"
        self.index = 2 ** 32
        self.type_set = frozenset()
        self.heads = frozenset()

    def conforms_to(self, other):
        return True

    def bypass(self):
        return True

    def swap_self_type(self, swap_type, back=False):
        return self

    def set_conditions(self, *params):
        return

    def generate_name(self):
        return "<error-type>"

    def clone(self):
        return self


class Context:
    def __init__(self) -> None:
        self.types = {}
        self.num_autotypes = 0
        self.type_graph = None

    def create_type(self, name: str) -> Type:
        if name in self.types:
            raise SemanticError(f"Type with the same name ({name}) already exists.")
        typex = self.types[name] = Type(name)
        return typex

    def get_type(self, name: str, selftype=True, autotype=True, unpacked=False) -> Type:
        if not selftype and name == "SELF_TYPE":
            raise TypeError(f"Cannot use SELF_TYPE.")  # return TypeBag({SelfType()})
        if autotype and name == "AUTO_TYPE":
            self.num_autotypes += 1
            return TypeBag(self.types, [self.types["Object"]])
        try:
            if unpacked:
                return self.types[name]
            return TypeBag({self.types[name]})
        except KeyError:
            raise TypeError(f'Type "{name}" is not defined.')

    def get_method_by_name(self, name: str, args: int) -> list:
        def dfs(root: str, results: list):
            try:
                for typex in self.type_graph[root]:
                    for method in self.types[typex].methods:
                        if name == method.name and args == len(method.param_names):
                            results.append((self.types[typex], method))
                            break
                    else:
                        dfs(typex, results)
            except KeyError:
                pass

        results = []
        dfs("Object", results)
        return results

    def __str__(self):
        return (
            "{\n\t"
            + "\n\t".join(y for x in self.types.values() for y in str(x).split("\n"))
            + "\n}"
        )

    def __repr__(self):
        return str(self)


class VariableInfo:
    def __init__(self, name, vtype) -> None:
        self.name: str = name
        self.type: TypeBag = vtype

    def get_type(self) -> TypeBag or ErrorType:
        if len(self.type.type_set) == 0:
            self.type = ErrorType()
        return self.type

    def __str__(self):
        return self.name + ":" + self.type


class Scope:
    def __init__(self, parent=None):
        self.locals = []
        self.parent = parent
        self.children = []
        self.index = 0 if parent is None else len(parent)
        self.current_child = -1

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

    def find_variable(self, vname, index=None):
        locals = self.locals if index is None else itt.islice(self.locals, index)
        try:
            return next(x for x in locals if x.name == vname)
        except StopIteration:
            try:
                return (
                    self.parent.find_variable(vname, self.index)
                    if self.parent is not None
                    else None
                )
            except AttributeError:
                return None

    def get_local_by_index(self, index):
        return self.locals[index]

    def is_defined(self, vname):
        return self.find_variable(vname) is not None

    def is_local(self, vname):
        return any(True for x in self.locals if x.name == vname)

    def next_child(self):
        self.current_child += 1
        return self.children[self.current_child]

    def reset(self):
        self.current_child = -1
        for child in self.children:
            child.reset()

    def get_all_names(self, s: str = "", level: int = 0):
        if self.locals:
            s += "\n ".join(
                [
                    x.name + ":" + str([typex.name for typex in x.type.type_set])
                    for x in self.locals
                ]
            )
            s += "\n\n"
        for child in self.children:
            s = child.get_all_names(s, level + 1)
        return s


def conforms(bag1: TypeBag, bag2: TypeBag) -> bool:
    if isinstance(bag1, ErrorType) or isinstance(bag2, ErrorType):
        return True

    ordered_set = order_set_by_index(bag2.type_set)

    condition_list = []
    conform_list = []
    for condition in ordered_set:
        conform = conform_to_condition(bag1.type_set, condition)
        for i in range(len(condition_list)):
            conform_i = conform_list[i]
            if len(conform_i) == len(conform) and len(
                conform.intersection(conform_i)
            ) == len(conform):
                condition_list[i].add(condition)
                break
        else:
            condition_list.append({condition})
            conform_list.append(conform)

    bag1.set_conditions(condition_list, conform_list)
    return len(bag1.type_set) >= 1


def try_conform(bag1: TypeBag, bag2: TypeBag) -> TypeBag:
    clone1 = bag1.clone()
    if not conforms(bag1, bag2):
        return clone1
    return bag2


def join(bag1: TypeBag, bag2: TypeBag) -> TypeBag:
    if isinstance(bag1, ErrorType):
        return bag2
    if isinstance(bag2, ErrorType):
        return bag1

    ancestor_set = set()
    head_list = []
    ordered_set1: Set[Type] = order_set_by_index(bag1.type_set)
    ordered_set2: Set[Type] = order_set_by_index(bag2.type_set)
    ordered_set1, ordered_set2 = (
        (ordered_set1, ordered_set2)
        if len(ordered_set1) < len(ordered_set2)
        else (ordered_set2, ordered_set1)
    )
    for type1 in ordered_set1:
        same_branch = False
        previous_ancestor = None
        previous_type = None
        for type2 in ordered_set2:
            if same_branch and type2.conforms_to(previous_type):
                previous_type = type2
                continue
            common_ancestor = type1.least_common_ancestor(type2)
            previous_type = type2
            if not previous_ancestor:
                smart_add(ancestor_set, head_list, common_ancestor)
                previous_ancestor = common_ancestor
            else:
                if previous_ancestor == common_ancestor:
                    same_branch = True
                else:
                    same_branch = False
                    smart_add(ancestor_set, head_list, common_ancestor)
                    previous_ancestor = common_ancestor

    join_result = TypeBag(ancestor_set, head_list)
    return join_result


def join_list(type_list):
    join_result = type_list[0]
    for i in range(1, len(type_list)):
        type_i = type_list[i]
        join_result = join(join_result, type_i)
    return join_result


def equal(bag1: TypeBag, bag2: TypeBag):
    if isinstance(bag1, ErrorType) or isinstance(bag2, ErrorType):
        return True
    set1 = bag1.type_set
    set2 = bag2.type_set
    return len(set1) == len(set2) and len(set1.intersection(set2)) == len(set2)


def smart_add(type_set: set, head_list: list, typex: Type):
    if isinstance(typex, TypeBag):
        return auto_add(type_set, head_list, typex)

    type_set.add(typex)
    there_is = False
    for i in range(len(head_list)):
        head = head_list[i]
        ancestor = typex.least_common_ancestor(head)
        if ancestor in type_set:
            there_is = True
            if ancestor == typex:
                head_list[i] = typex
                break
    if not there_is:
        head_list.append(typex)
    return type_set


def auto_add(type_set: set, head_list: list, bag: TypeBag):
    type_set = type_set.union(bag.type_set)
    aux = set(bag.heads)
    for i in range(len(head_list)):
        head_i = head_list[i]
        for head_j in bag.heads:
            ancestor = head_i.least_common_ancestor(head_j)
            if ancestor in type_set:
                head_list[i] = ancestor
                aux.remove(head_j)
                break
    head_list += [typex for typex in aux]
    return type_set


def conform_to_condition(type_set, parent) -> set:
    set_result = set()
    for typex in type_set:
        if typex.conforms_to(parent):
            set_result.add(typex)
    return set_result


def order_set_by_index(type_set):
    return sorted(list(type_set), key=lambda x: x.index)


def set_intersection(parent, type_set) -> set:
    set_result = set()
    for typex in type_set:
        if typex.conforms_to(parent):
            set_result.add(typex)
    return set_result


def from_dict_to_set(types: dict):
    type_set = set()
    for typex in types:
        type_set.add(types[typex])
    return type_set
