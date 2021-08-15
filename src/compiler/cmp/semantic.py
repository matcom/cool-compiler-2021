import itertools as itt
from collections import OrderedDict


class SemanticError(Exception):
    @property
    def text(self):
        return self.args[0]

class Attribute:
    def __init__(self, name, typex, idx=None):
        self.name = name
        self.type = typex
        self.idx = idx

    def __str__(self):
        return f'[attrib] {self.name} : {self.type.name};'

    def __repr__(self):
        return str(self)

class Method:
    def __init__(self, name, param_names, param_types, return_type, param_idx, ridx=None):
        self.name = name
        self.param_names = param_names
        self.param_types = param_types
        self.param_idx = param_idx
        self.return_type = return_type
        self.ridx = ridx

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

    def set_parent(self, parent):
        if self.parent is not None:
            raise SemanticError(f'Parent type is already set for {self.name}.')
        self.parent = parent

    def get_attribute(self, name:str):
        try:
            return next(attr for attr in self.attributes if attr.name == name)
        except StopIteration:
            if self.parent is None:
                raise SemanticError(f'Attribute "{name}" is not defined in {self.name}.')
            try:
                return self.parent.get_attribute(name)
            except SemanticError:
                raise SemanticError(f'Attribute "{name}" is not defined in {self.name}.')

    def define_attribute(self, name:str, typex, idx=None):
        try:
            self.get_attribute(name)
        except SemanticError:
            attribute = Attribute(name, typex, idx)
            self.attributes.append(attribute)
            return attribute
        else:
            raise SemanticError(f'Attribute "{name}" is already defined in {self.name}.')

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

    def define_method(self, name:str, param_names:list, param_types:list, return_type, param_idx:list, ridx=None):
        if name in (method.name for method in self.methods):
            raise SemanticError(f'Method "{name}" already defined in {self.name}')

        method = Method(name, param_names, param_types, return_type, param_idx, ridx)
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

    def update_attr(self, attr_name, attr_type):
        for i, item in enumerate(self.attributes):
            if item.name == attr_name:
                self.attributes[i] = Attribute(attr_name, attr_type)
                break
    
    def update_method_rtype(self, method_name, rtype):
        for i, item in enumerate(self.methods):
            if item.name == method_name:
                self.methods[i].return_type = rtype
                break

    def update_method_param(self, method_name, param_type, param_idx):
        for i, item in enumerate(self.methods):
            if item.name == method_name:
                self.methods[i].param_types[param_idx] = param_type
                break

    def conforms_to(self, other):
        return other.bypass() or self.name == other.name or self.parent is not None and self.parent.conforms_to(other)

    def bypass(self):
        return False
    
    def can_be_inherited(self):
        return True

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

    def __eq__(self, other):
        return self.conforms_to(other) and other.conforms_to(self)

class ErrorType(Type):
    def __init__(self):
        Type.__init__(self, '<error>')

    def conforms_to(self, other):
        return True

    def bypass(self):
        return True

    def __eq__(self, other):
        return isinstance(other, Type)


class ObjectType(Type):
    def __init__(self):
        Type.__init__(self, 'Object')

    def __eq__(self, other):
        return other.name == self.name or isinstance(other, ObjectType)    

class IOType(Type):
    def __init__(self):
        Type.__init__(self, 'IO')

    def __eq__(self, other):
        return other.name == self.name or isinstance(other, IOType)

class StringType(Type):
    def __init__(self):
        Type.__init__(self, 'String')

    def __eq__(self, other):
        return other.name == self.name or isinstance(other, StringType)

    def can_be_inherited(self):
        return False

class BoolType(Type):
    def __init__(self):
        Type.__init__(self, 'Bool')

    def __eq__(self, other):
        return other.name == self.name or isinstance(other, BoolType)

    def can_be_inherited(self):
        return False

class IntType(Type):
    def __init__(self):
        Type.__init__(self, 'Int')

    def __eq__(self, other):
        return other.name == self.name or isinstance(other, IntType)
    
    def can_be_inherited(self):
        return False

class SelfType(Type):
    def __init__(self, fixed=None):
        Type.__init__(self, 'SELF_TYPE')
        self.fixed_type = fixed
    
    def can_be_inherited(self):
        return False

class AutoType(Type):
    def __init__(self):
        Type.__init__(self, 'AUTO_TYPE')

    def can_be_inherited(self):
        return False

    def conforms_to(self, other):
        return True

    def bypass(self):
        return True
    

class Context:
    def __init__(self):
        self.types = {}

    def create_type(self, name:str):
        if name in self.types:
            raise SemanticError(f'Type with the same name ({name}) already in context.')
        typex = self.types[name] = Type(name)
        return typex

    def get_type(self, name:str):
        try:
            return self.types[name]
        except KeyError:
            raise SemanticError(f'Type "{name}" is not defined.')

    def __str__(self):
        return '{\n\t' + '\n\t'.join(y for x in self.types.values() for y in str(x).split('\n')) + '\n}'

    def __repr__(self):
        return str(self)

class VariableInfo:
    def __init__(self, name, vtype, idx):
        self.name = name
        self.type = vtype
        self.idx = idx

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

    def define_variable(self, vname, vtype, idx=None):
        info = VariableInfo(vname, vtype, idx)
        self.locals.append(info)
        return info

    def find_variable(self, vname, index=None):
        locals = self.locals if index is None else itt.islice(self.locals, index)
        try:
            return next(x for x in locals if x.name == vname)
        except StopIteration:
            return self.parent.find_variable(vname, self.index) if self.parent is not None else None

    def is_defined(self, vname):
        return self.find_variable(vname) is not None

    def is_local(self, vname):
        return any(True for x in self.locals if x.name == vname)

    def update_variable(self, vname, vtype, index=None):
        locals = self.locals if index is None else itt.islice(self.locals, index)
        for i, item in enumerate(locals):
            if item.name == vname:
                self.locals[i] = VariableInfo(vname, vtype, item.idx)
                return True
        return self.parent.update_variable(vname, vtype, self.index) if self.parent is not None else False


class InferencerManager:
    def __init__(self):
        # given a type represented by int idx, types[idx] = (A, B), where A and B are sets
        # if x in A then idx.conforms_to(x)
        # if x in B then x.conforms_to(idx)
        self.conforms_to = []
        self.conformed_by = []
        self.infered_type = []
        self.count = 0

    def assign_id(self, obj_type):
        idx = self.count
        self.conforms_to.append([obj_type])
        self.conformed_by.append([])
        self.infered_type.append(None)
        self.count += 1

        return idx

    def upd_conforms_to(self, idx, other):
        for item in other:
            self.auto_to_type(idx, item)

    def upd_conformed_by(self, idx, other):
        for item in other:
            self.type_to_auto(idx, item)

    def auto_to_type(self, idx, typex):
        if isinstance(typex, SelfType):
            typex = typex.fixed_type
        try:
            assert not isinstance(typex, ErrorType)
            assert not any(item.name == typex.name for item in self.conforms_to[idx])
            
            self.conforms_to[idx].append(typex)
        except AssertionError:
            pass

    def type_to_auto(self, idx, typex):
        if isinstance(typex, SelfType):
            typex = typex.fixed_type
        try:
            assert not isinstance(typex, ErrorType)
            assert not any(item.name == typex.name for item in self.conformed_by[idx])
            
            self.conformed_by[idx].append(typex)
        except AssertionError:
            pass

    def infer(self, idx):
        try:
            assert self.infered_type[idx] is None
            assert len(self.conforms_to[idx]) > 1 or len(self.conformed_by[idx]) > 0

            try:
                start = self.get_min(self.conforms_to[idx])
                self.infered_type[idx] = start

                if len(self.conformed_by[idx]) > 0:
                    final = LCA(self.conformed_by[idx])
                    assert final.conforms_to(start)
                    self.infered_type[idx] = final

            except AssertionError:
                self.infered_type[idx] = ErrorType()
            return True
        except AssertionError:
            return False

    def infer_all(self):
        change = False
        for i in range(self.count):
            change |= self.infer(i)
        
        return change

    def infer_object(self, obj_type):
        for i in range(self.count):
            if self.infered_type[i] is None:
                self.infered_type[i] = obj_type

    def get_min(self, types):
        path = []

        def find(typex):
            for i, item in enumerate(path):
                if item.name == typex.name:
                    return i
            return len(path)


        for item in types:
            current = []
            while item is not None:
                idx = find(item)
                if idx == len(path):
                    current.append(item)
                    item = item.parent
                    continue
                
                assert idx == len(path) - 1 or len(current) == 0
                break
            current.reverse()
            path.extend(current)

        return path[-1]



def LCA(types):
    if len(types) == 0:
        return None

    # check ErrorType:
    if any(isinstance(item, ErrorType) for item in types):
        return ErrorType()

    # check AUTO_TYPE
    if any(isinstance(item, AutoType) for item in types):
        return AutoType()

    # check SELF_TYPE:
    if all(isinstance(item, SelfType) for item in types):
        return types[0]

    for i, item in enumerate(types):
        if isinstance(item, SelfType):
            types[i] = item.fixed_type

    current = types[0]
    while current:
        for item in types:
            if not item.conforms_to(current):
                break
        else:
            return current
        current = current.parent

    # This part of the code is supposed to be unreachable
    return None