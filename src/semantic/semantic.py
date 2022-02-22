from utils.ast import BoolNode, IntNode, IsVoidNode, StringNode, VoidNode
from utils.errors import SemanticError
from collections import OrderedDict
import itertools as itt


class Attribute:
    def __init__(self, name, typex, index, tok=None):
        self.name = name
        self.type = typex
        self.index = index
        self.expr = None

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
        params = ', '.join(f'{n}:{t.name}' for n, t in zip(
            self.param_names, self.param_types))
        return f'[method] {self.name}({params}): {self.return_type.name};'

    def __eq__(self, other):
        return other.name == self.name and \
            other.return_type == self.return_type and \
            other.param_types == self.param_types


class MethodError(Method):
    def __init__(self, name, param_names, param_types, return_types):
        super().__init__(name, param_names, param_types, return_types)

    def __str__(self):
        return f'[method] {self.name} ERROR'


class Type:
    def __init__(self, name: str, pos, parent=True):
        if name == 'ObjectType':
            return ObjectType(pos)
        self.name = name
        self.attributes = {}
        self.methods = {}
        if parent:
            self.parent = ObjectType(pos)
        else:
            self.parent = None
        self.pos = pos

    def set_parent(self, parent):
        if type(self.parent) != ObjectType and self.parent is not None:
            error_msg = f'Parent type is already set for {self.name}.'
            raise SemanticError(error_msg, *self.pos)
        self.parent = parent

    def get_attribute(self, name: str, pos) -> Attribute:
        try:
            return self.attributes[name]
        except KeyError:
            if self.parent is None:
                error_msg = f'Attribute {name} is not defined in {self.name}.'
                raise SemanticError(error_msg, *pos)
            try:
                return self.parent.get_attribute(name, pos)
            except:
                error_msg = f'Attribute {name} is not defined in {self.name}.'
                raise SemanticError(error_msg, *pos)

    def define_attribute(self, name: str, typex, pos):
        try:
            self.attributes[name]
        except KeyError:
            try:
                self.get_attribute(name, pos)
            except:
                self.attributes[name] = attribute = Attribute(
                    name, typex, len(self.attributes))
                return attribute
            else:
                error_msg = f'Attribute {name} is an attribute of an inherit class.'
                raise SemanticError(error_msg, *pos)
        else:
            error_msg = f'Attribute {name} is multiply defined in class.'
            raise SemanticError(error_msg, *pos)

    def get_method(self, name: str, pos) -> Method:
        try:
            return self.methods[name]
        except KeyError:
            error_msg = f'Method {name} is not defined in {self.name}.'
            if self.parent is None:
                raise SemanticError(error_msg, *pos)
            try:
                return self.parent.get_method(name, pos)
            except:
                raise SemanticError(error_msg, *pos)

    def define_method(self, name: str, param_names: list, param_types: list, return_type, pos=(0, 0)):
        if name in self.methods:
            error_msg = f'Method {name} is multiply defined'
            raise SemanticError(error_msg, *pos)

        method = self.methods[name] = Method(
            name, param_names, param_types, return_type)
        return method

    def change_type(self, method, nparm, newtype):
        idx = method.param_names.index(nparm)
        method.param_types[idx] = newtype

    def all_attributes(self, clean=True):
        plain = OrderedDict() if self.parent is None else self.parent.all_attributes(False)
        for attr in self.attributes.values():
            plain[attr.name] = (attr, self)
        return plain.values() if clean else plain

    def all_methods(self, clean=True):
        plain = OrderedDict() if self.parent is None else self.parent.all_methods(False)
        for method in self.methods.values():
            plain[method.name] = (method, self)
        return plain.values() if clean else plain

    def conforms_to(self, other):
        return other.bypass() or self == other or self.parent is not None and self.parent.conforms_to(other)

    def bypass(self):
        return False

    def __str__(self):
        output = f'type {self.name}'
        parent = '' if self.parent is None else f' : {self.parent.name}'
        output += parent
        output += ' {'
        output += '\n\t' if self.attributes or self.methods else ''
        output += '\n\t'.join(str(x) for x in self.attributes.values())
        output += '\n\t' if self.attributes else ''
        output += '\n\t'.join(str(x) for x in self.methods.values())
        output += '\n' if self.methods else ''
        output += '}\n'
        return output

    def __repr__(self):
        return str(self)


class ErrorType(Type):
    def __init__(self, pos=(0, 0)):
        Type.__init__(self, '<error>', pos)

    def conforms_to(self, other):
        return True

    def bypass(self):
        return True

    def __eq__(self, other):
        return isinstance(other, ErrorType)

    def __ne__(self, other):
        return not isinstance(other, ErrorType)


class VoidType(Type):
    def __init__(self, pos=(0, 0)):
        Type.__init__(self, 'Void', pos)

    def conforms_to(self, other):
        return True

    def bypass(self):
        return True

    def __eq__(self, other):
        return isinstance(other, VoidType)


class BoolType(Type):
    def __init__(self, pos=(0, 0)):
        self.name = 'Bool'
        self.attributes = {}
        self.methods = {}
        self.parent = None
        self.pos = pos
        self.init_methods()

    def init_methods(self):
        self.define_method('abort', [], [], self)
        self.define_method('type_name', [], [], StringType())
        self.define_method('copy', [], [], SelfType())

    def conforms_to(self, other):
        return other.name == 'Object' or other.name == self.name

    def __eq__(self, other):
        return other.name == self.name or isinstance(other, BoolType)

    def __ne__(self, other):
        return other.name != self.name and not isinstance(other, BoolType)


class SelfType(Type):
    def __init__(self, pos=(0, 0)):
        self.name = 'Self'
        self.attributes = {}
        self.methods = {}
        self.parent = None
        self.pos = pos

    def __eq__(self, other):
        return other.name == self.name or isinstance(other, SelfType)

    def __ne__(self, other):
        return other.name != self.name and not isinstance(other, SelfType)


class IntType(Type):
    def __init__(self, pos=(0, 0)):
        self.name = 'Int'
        self.attributes = {}
        self.methods = {}
        self.parent = None
        self.pos = pos
        self.init_methods()

    def init_methods(self):
        self.define_method('abort', [], [], self)
        self.define_method('type_name', [], [], Type('String', (0, 0), False))
        self.define_method('copy', [], [], SelfType())

    def conforms_to(self, other):
        return other.name == 'Object' or other.name == self.name

    def __eq__(self, other):
        return other.name == self.name or isinstance(other, IntType)

    def __ne__(self, other):
        return other.name != self.name and not isinstance(other, IntType)


class StringType(Type):
    def __init__(self, pos=(0, 0)):
        self.name = 'String'
        self.attributes = {}
        self.methods = {}
        self.parent = None
        self.pos = pos
        self.init_methods()

    def init_methods(self):
        self.define_method('abort', [], [], self)
        self.define_method('type_name', [], [], self)
        self.define_method('copy', [], [], SelfType())
        self.define_method('length', [], [], IntType())
        self.define_method('concat', ['s'], [self], self)
        self.define_method('substr', ['i', 'l'], [IntType(), IntType()], self)

    def conforms_to(self, other):
        return other.name == 'Object' or other.name == self.name

    def __eq__(self, other):
        return other.name == self.name or isinstance(other, StringType)

    def __ne__(self, other):
        return other.name != self.name and not isinstance(other, StringType)


class ObjectType(Type):
    def __init__(self, pos=(0, 0)):
        self.name = 'Object'
        self.attributes = {}
        self.methods = {}
        self.parent = None
        self.pos = pos
        self.init_methods()

    def init_methods(self):
        self.define_method('abort', [], [], self)
        self.define_method('type_name', [], [], StringType())
        self.define_method('copy', [], [], SelfType())

    def __eq__(self, other):
        return other.name == self.name or isinstance(other, ObjectType)

    def __ne__(self, other):
        return other.name != self.name and not isinstance(other, ObjectType)


class IOType(Type):
    def __init__(self, pos=(0, 0)):
        self.name = 'IO'
        self.attributes = {}
        self.methods = {}
        self.parent = ObjectType(pos)
        self.pos = pos
        self.init_methods()

    def init_methods(self):
        self.define_method('out_string', ['x'], [StringType()], SelfType())
        self.define_method('out_int', ['x'], [IntType()], SelfType())
        self.define_method('in_string', [], [], StringType())
        self.define_method('in_int', [], [], IntType())

    def __eq__(self, other):
        return other.name == self.name or isinstance(other, IOType)

    def __ne__(self, other):
        return other.name != self.name and not isinstance(other, IOType)


class AutoType(Type):
    def __init__(self):
        Type.__init__(self, 'AUTO_TYPE')

    def __eq__(self, other):
        return other.name == self.name or isinstance(other, AutoType)

    def __ne__(self, other):
        return other.name != self.name and not isinstance(other, AutoType)


class Context:
    def __init__(self):
        self.types = {}

    def get_depth(self, class_name):
        typex = self.types[class_name]
        if typex.parent is None:
            return 0
        return 1 + self.get_depth(typex.parent.name)

    def build_inheritance_graph(self):
        graph = {}
        for type_name, typex in self.types.items():
            if typex.parent is not None:
                graph[type_name] = typex.parent.name
            else:
                if type_name == 'SELF_TYPE':
                    continue
                graph[type_name] = None
        return graph

    def create_type(self, name: str, pos) -> Type:
        if name in self.types:
            error_text = 'Classes may not be redefined.'
            raise SemanticError(error_text, *pos)
        typex = self.types[name] = Type(name, pos)
        return typex

    def get_type(self, name: str, pos) -> Type:
        try:
            return self.types[name]
        except KeyError:
            error_text = f'Type {name} is not defined.'
            raise SemanticError(error_text, *pos)

    def __str__(self):
        return '{\n\t' + '\n\t'.join(y for x in self.types.values() for y in str(x).split('\n')) + '\n}'

    def __repr__(self):
        return str(self)


class VariableInfo:
    def __init__(self, name, vtype, index=None):
        self.name = name
        self.type = vtype
        self.index = index  # saves the index in the scope of the variable

    def __str__(self):
        return f'{self.name} : {self.type.name}'

    def __repr__(self):
        return str(self)


class Scope:
    def __init__(self, parent=None):
        self.locals = []
        self.attributes = []
        self.parent = parent
        self.children = []
        self.expr_dict = {}
        self.functions = {}
        self.index = 0 if parent is None else len(parent)

    def __len__(self):
        return len(self.locals)

    def __str__(self):
        res = ''
        for scope in self.children:
            try:
                classx = scope.locals[0]
                name = classx.type.name
            except:
                name = '1'
            # '\n\t' +  ('\n' + '\t').join(str(local) for local in scope.locals) + '\n'
            res += name + scope.tab_level(1, '', 1)
        return res

    def tab_level(self, tabs, name, num) -> str:
        res = ('\t' * tabs) + ('\n' + ('\t' * tabs)).join(str(local)
                                                          for local in self.locals)
        if self.functions:
            children = '\n'.join(v.tab_level(
                tabs + 1, '[method] ' + k, num) for k, v in self.functions.items())
        else:
            children = '\n'.join(child.tab_level(
                tabs + 1, num, num + 1) for child in self.children)
        return "\t" * (tabs-1) + f'{name}' + "\t" * tabs + f'\n{res}\n{children}'

    def __repr__(self):
        return str(self)

    def create_child(self):
        child = Scope(self)
        self.children.append(child)
        return child

    def define_variable(self, vname, vtype) -> VariableInfo:
        info = VariableInfo(vname, vtype)
        if info not in self.locals:
            self.locals.append(info)
        return info

    def find_variable(self, vname, index=None) -> VariableInfo:
        locals = self.attributes + self.locals
        locals = locals if index is None else itt.islice(locals, index)
        try:
            return next(x for x in locals if x.name == vname)
        except StopIteration:
            return self.parent.find_variable(vname, index) if self.parent is not None else None

    def find_local(self, vname, index=None) -> VariableInfo:
        locals = self.locals if index is None else itt.islice(
            self.locals, index)
        try:
            return next(x for x in locals if x.name == vname)
        except StopIteration:
            return self.parent.find_local(vname, self.index) if self.parent is not None else None

    def find_attribute(self, vname, index=None):
        locals = self.attributes if index is None else itt.islice(
            self.attributes, index)
        try:
            return next(x for x in locals if x.name == vname)
        except StopIteration:
            return self.parent.find_attribute(vname, index) if self.parent is not None else None

    def get_class_scope(self):
        if self.parent == None or self.parent.parent == None:
            return self
        return self.parent.get_class_scope()

    def is_defined(self, vname) -> VariableInfo:
        return self.find_variable(vname) is not None

    def is_local(self, vname):
        return any(True for x in self.locals if x.name == vname)

    def define_attribute(self, attr):
        self.attributes.append(attr)

def define_default_value(self, typex, node):
    if typex == IntType():
        node.expr = IntNode(0)
    elif typex == StringType():
        node.expr = StringNode("")
    elif typex == BoolType():
        node.expr = BoolNode('false')
    else:
        node.expr = VoidNode(node.id)
