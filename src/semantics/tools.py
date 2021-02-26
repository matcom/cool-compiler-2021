import itertools as itt
from collections import OrderedDict
from typing import FrozenSet

from semantics.utils import conform_to_condition, order_set_by_index

class InternalError(Exception):
    @property
    def text(self):
        return "Internal Error: " + self.args[0]

class SemanticError(Exception):
    @property
    def text(self):
        return "Semantic Error: " + self.args[0]

class TypeError(SemanticError):
    @property
    def text(self):
        return "Type Error: " + self.args[0]

class AttributeError(SemanticError):
    @property
    def text(self):
        return "Attribute Error: " + self.args[0]

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
        self.index = -1

    def set_parent(self, parent):
        if self.parent is not None:
            raise SemanticError(f'Type \'{self.name}\' already has parent type \'{self.parent.name}\'. Type \'{parent.name}\' cannot be set as parent.')
        if parent.name in {"String", "Int", "Bool"}:
            raise SemanticError(f'Cannot set \'{self.name}\' parent, \'{parent.name}\' type cannot be inherited.')
        self.parent = parent

    def define_attribute(self, name:str, typex):
        try:
            self.get_attribute(name)
        except SemanticError:
            attribute = Attribute(name, typex)
            self.attributes.append(attribute)
            return attribute
        else:
            raise SemanticError(f'Attribute "{name}" is already defined in {self.name}.')

    def get_attribute(self, name:str):
        try:
            return next(attr for attr in self.attributes if attr.name == name)
        except StopIteration:
            if self.parent is None:
                raise AttributeError(f'Attribute "{name}" is not defined in {self.name}.')
            try:
                return self.parent.get_attribute(name)
            except SemanticError:
                raise AttributeError(f'Attribute "{name}" is not defined in {self.name}.')
    
    def get_method(self, name:str, local:bool = False):
        try:
            return next(method for method in self.methods if method.name == name)
        except StopIteration:
            if self.parent is None:
                raise SemanticError(f'Method "{name}" is not defined in class {self.name}.')
            try:
                return self.parent.get_method(name)
            except SemanticError:
                raise SemanticError(f'Method "{name}" is not defined in class {self.name}.')

    def define_method(self, name:str, param_names:list, param_types:list, return_type):
        if name in (method.name for method in self.methods):
            raise SemanticError(f'Method \'{name}\' already defined in \'{self.name}\'')

        try:
            parent_method = self.get_method(name)
        except SemanticError:
            parent_method = None
        if parent_method:
            error_list = []
            if conforms(return_type, parent_method.return_type):
                error_list.append(f"    -> Same return type: Redefined method has \'{return_type.name}\' as return type instead of \'{parent_method.return_type.name}\'.")
            if len(param_types) != len(parent_method.param_types):
                error_list.append(f"    -> Same amount of params: Redefined method has {len(param_types)} params instead of {len(parent_method.param_types)}.")
            else:
                count = 0
                err = []
                for param_type, parent_param_type in zip(param_types, parent_method.param_types):
                    if param_type != parent_param_type:
                        err.append(f"        -Param number {count} has {param_type.name} as type instead of {parent_param_type.name}")
                    count += 1
                if err:
                    s = f"    -> Same param types:\n" + "\n".join(child for child in err)
                    error_list.append(s)
            if error_list:
                err = f"Redifined method \"{name}\" in class {self.name} does not have:\n" + "\n".join(child for child in error_list)
                raise SemanticError(err)

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

    def least_common_ancestor(self, other):
        this = self
        if isinstance(this, ErrorType) or isinstance(other, ErrorType):
            return ErrorType()
            #raise SemanticError("Error Type detected while perfoming Join. Aborting.") 

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

class TypeBag:
    def __init__(self, type_set, heads = []) -> None:
        self.type_set:set = type_set if isinstance(type_set, set) else from_dict_to_set(type_set)
        self.heads:list = heads
        if len(self.type_set) == 1:
            self.heads = list(self.type_set)
        
        self.name = self.generate_name()
        self.condition_list = []
        self.conform_list = []
    
    def set_conditions(self, condition_list, conform_list):
        self.condition_list = condition_list
        self.conform_list = conform_list
        self.update_type_set_from_conforms()
        self.name = self.generate_name()

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
            new_heads = []
            lower_index = 2**32
            for typex in self.type_set:
                if typex in visited:
                    continue
                if typex.conforms_to(head):
                    visited.add(typex)
                    if typex.index < lower_index:
                        new_heads = [typex]
                        lower_index = typex.index
                    elif typex.index == lower_index:
                        new_heads.append(typex)
            new_heads += new_heads
        self.heads = new_heads

    def swap_self_type(self, update_type):
        try:
            self.type_set.remove(SelfType())
            self.type_set.add(update_type)
        except KeyError:
            pass
        return self
    
    def swap_types(self, update_type, remove_type):
        try:
            self.type_set.remove(remove_type)
            self.type_set.add(update_type)
        except KeyError:
            pass
        return self
    
    def generate_name(self):
        if len(self.type_set) == 1:
            return self.heads[0].name

        s = "{"
        s += ', '.join(typex.name for typex in sorted(self.type_set, key = lambda t: t.index))
        s += "}"
        return s

    def clone(self):
        clone = TypeBag(self.type_set, self.heads)
        clone.condition_list = self.condition_list
        clone.conform_list = self.conform_list
        return clone

class SelfType(Type):
    def __init__(self):
        self.name = "SELF_TYPE"
        self.index = 2**31
    def conforms_to(self, other):
        #if isinstance(other, SelfType):
        #    return True
        raise InternalError("SELF_TYPE is yet to be assigned, cannot conform.")
    def bypass(self):
        raise InternalError("SELF_TYPE is yet to be assigned, cannot bypass.")


    def __str__(self):
        return self.name

    def __repr__(self):
        return str(self)

class ErrorType(Type):
    def __init__(self):
        self.name = "<error>"
        self.index = 2**32
        self.type_set = frozenset()
    def conforms_to(self, other):
        return True
    def bypass(self):
        return True

    def swap_self_type(self, update_type):
        return self

    def set_conditions(self, *params):
        return

class Context:
    def __init__(self) -> None:
        self.types = {}
        self.num_autotypes = 0
        self.type_graph = None
    
    def create_type(self, name:str) -> Type:
        if name in self.types:
            raise SemanticError(f'Type with the same name ({name}) already exists.')
        if name[0] != name[0].upper():
            raise SemanticError(f'Type name ({name}) must start with upper case')
        typex = self.types[name] = Type(name)
        return typex
    
    def get_type(self, name:str, selftype=True, autotype=True, unpacked=False) -> Type:
        if selftype and name == "SELF_TYPE":
            return TypeBag({SelfType()}) #SelfType()
        if autotype and name == "AUTO_TYPE":
            self.num_autotypes += 1
            return TypeBag(self.types, [self.types['Object']]) #AutoType(f"T{self.num_autotypes}", [self.types["Object"]], self.types)
        try:
            if unpacked:
                return self.types[name]
            return TypeBag({self.types[name]})
        except KeyError:
            raise TypeError(f'Type "{name}" is not defined.')

    def get_method_by_name(self, name:str, args:int) -> list:
        def dfs(root:str, results:list):
            try:
                for typex in self.type_tree[root]:
                    for method in self.types[typex].methods:
                        if name == method.name and args == len(method.param_names):
                            results.append((method, self.types[typex]))
                            break
                    else:
                        dfs(typex, results)
            except KeyError:
                pass
        results = []
        dfs("Object", results)
        return results

    def __str__(self):
        return '{\n\t' + '\n\t'.join(y for x in self.types.values() for y in str(x).split('\n')) + '\n}'

    def __repr__(self):
        return str(self)

class VariableInfo:
    def __init__(self, name, vtype):
        self.name = name
        self.type = vtype
    
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
                return self.parent.find_variable(vname, self.index) if self.parent else None
            except AttributeError:
                return None

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


def conforms(bag1:TypeBag, bag2:TypeBag):
    ordered_set = order_set_by_index(bag2.type_set)

    condition_list = []
    conform_list = []
    for condition in ordered_set:
        conform = conform_to_condition(bag1.type_set, condition)
        for i in range(len(condition_list)):
            conform_i = conform_list[i]
            if len(conform_i) == len(conform) and len(conform.intersection(conform_i)) == len(conform):
                condition_list[i].add(condition)
                break
        else:
            condition_list.append({condition})
            conform_list.append(conform)
    
    bag1.set_conditions(condition_list, conform_list)
    return len(bag1.type_set) >= 1

def join(bag1:TypeBag, bag2:TypeBag) -> TypeBag:
    ancestor_set = set()
    head_list = []
    ordered_set1 = order_set_by_index(bag1.type_set)
    ordered_set2 = order_set_by_index(bag2.type_set)
    ordered_set1, ordered_set2 = (ordered_set1, ordered_set2) if len(ordered_set1) < len(ordered_set2) else (ordered_set2, ordered_set1)
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

def smart_add(type_set:set, head_list:list, typex:Type):
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
    return head_list, type_set

def auto_add(type_set:set, head_list:list, bag:TypeBag):
    type_set = type_set.union(bag.type_set)
    aux = set(bag.heads)
    for i in range(len(head_list)):
        head_i = head_list[i]
        for head in bag.heads:
            ancestor = head_i.least_common_ancestor(head)
            if ancestor in type_set:
                head_i[i] = ancestor
                aux.pop(head)
                break
    head_list += [typex for typex in aux]
    return head_list, type_set

