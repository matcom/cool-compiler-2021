import itertools as itt
from collections import OrderedDict

class SemanticException(Exception):
    @property
    def text(self):
        return self.args[0]

class NameException(Exception):
    @property
    def text(self):
        return self.args[0]

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
        self.methods = {}
        self.parent = None
        self.is_autotype = False

    def set_parent(self, parent):
        if self.parent is not None:
            raise SemanticException(f'Parent type is already set for {self.name}.')
        self.parent = parent

    def get_attribute(self, name:str):
        try:
            return next(attr for attr in self.attributes if attr.name == name)
        except StopIteration:
            if self.parent is None:
                raise SemanticException(f'Attribute "{name}" is not defined in {self.name}.')
            try:
                return self.parent.get_attribute(name)
            except SemanticException:
                raise SemanticException(f'Attribute "{name}" is not defined in {self.name}.')

    def define_attribute(self, name:str, typex):
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
            raise SemanticException(f'Attribute "{name}" is already defined in {self.name}.')

    def change_attr(self,name:str, new_typex):
        try:
            attr = self.get_attribute(name)
            attr.type = new_typex
        except SemanticException:
            print('REVISAR TYPE.CHANGE_TYPE')

    def change_method(self,name:str,new_typex):
        try:
            method = self.get_method(name)
            method.return_type = new_typex
        except:
            print('REVISAR TYPE.CHANGE_METHOD')

    def change_param(self,name:str,new_param_list):
        try:
            method = self.get_method(name)
            param_name = []
            param_type = []
            for var in new_param_list.locals:
                param_name.append(var.name)
                param_type.append(var.type)
            method.param_names = param_name
            method.param_types = param_type
        except:
            print('REVISAR TYPE.CHANGE_PARAM')

    def substitute_type(self, typeA , typeB):
        for attr in self.attributes:
            if attr.type == typeA:
                attr.type = typeB
        for meth in self.methods.values():
            if meth.return_type == typeA:
                meth.return_type = typeB
                for p_type in meth.param_types:
                    if p_type == typeA:
                        p_type = typeB

    def has_parent(self,typeA):
        return (self == typeA) or (self.parent and self.parent.has_parent(typeA))

    def get_method(self, name:str):
        try:
            return self.methods[name]
        except KeyError:
            if self.parent is None:
                raise SemanticException(f'Method "{name}" is not defined in {self.name}.')
            try:
                return self.parent.get_method(name)
            except SemanticException:
                raise SemanticException(f'Method "{name}" is not defined in {self.name}.')
            
    def get_all_parents(self):
        if self.parent is None: return []
        return [self.parent]+self.parent.get_all_parents()

    def all_attributes(self, clean=True):
        plain = OrderedDict() if self.parent is None else self.parent.all_attributes(False)
        for attr in self.attributes:
            plain[attr.name] = (attr, self)
        return plain.values() if clean else plain

    

    # def define_method(self, name:str, param_names:list, param_types:list, return_type):
    #     if name in self.methods:
    #         raise SemanticException(f'Method "{name}" already defined in {self.name}')
            # raise SemanticError(f'Method "{name}" already defined in {self.name} with a different signature.')

        method = self.methods[name] = Method(name, param_names, param_types, return_type)
        return method
    
    # my method, change it in future
    def define_method(self, name:str, param_names:list, param_types:list, return_type):
        if name in self.methods:
            raise SemanticException(f'Method "{name}" already defined in {self.name}')
        try:
            method = self.get_method(name)
        except SemanticException:
            pass
        else:
            if method.return_type != return_type or method.param_types != param_types:
                raise SemanticException(f'Method "{name}" already defined in {self.name} with a different signature.')
            ##############METHOD NO HEREDA AUTO)TYPE

        method = self.methods[name] = Method(name, param_names, param_types, return_type)
        return method

    def conforms_to(self, other):
        a = other.bypass() or self.name == other.name
        b = self.parent is not None and self.parent.conforms_to(other)
        return a or b

    def bypass(self):
        return False

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

class ObjectType(Type):
    def __init__(self):
        Type.__init__(self, 'Object')

    def __eq__(self,other):
        return other.name == self.name or isinstance(other, ObjectType)

class ErrorType(Type):
    def __init__(self):
        Type.__init__(self, 'Error')

    def conforms_to(self, other):
        return True

    def bypass(self):
        return True

    def __eq__(self, other):
        return isinstance(other, Type)

class VoidType(Type):
    def __init__(self):
        Type.__init__(self, 'Void')

    def conforms_to(self, other):
        raise Exception('Invalid type: void type.')

    def bypass(self):
        return True

    def __eq__(self, other):
        return isinstance(other, VoidType)

class IntType(Type):

    def __init__(self):
        Type.__init__(self, 'Int')
        self.parent = ObjectType()

    def __eq__(self, other):
        return other.name == self.name or isinstance(other, IntType)

class BoolType(Type):
    def __init__(self):
        Type.__init__(self , 'Bool')
        self.parent = ObjectType()

    def __eq__(self,other):
        return other.name == self.name or isinstance(other, BoolType)

class StringType(Type):
    def __init__(self):
        Type.__init__(self,'String')
        self.parent = ObjectType()

    def __eq__(self,other):
        return other.name == self.name or isinstance(other, StringType)

class IOType(Type):
    def __init__(self):
        Type.__init__(self,'IO')
        self.parent = ObjectType()

    def __eq__(self,other):
        return other.name == self.name or isinstance(other, StringType)

class SelfType(Type):
    def __init__(self):
        Type.__init__(self,'self')

class Context:
    def __init__(self):
        self.types = {}
        self.special_types = []
        object_type = ObjectType()

        IO_type = IOType()

        int_type = IntType()
        bool_type = BoolType()
        error_type = ErrorType()
        self_type = SelfType()
        string_type = StringType()

        self.types['Object'] = object_type
        self.types['Int'] = int_type
        self.types['String'] = string_type
        self.types['Bool'] = bool_type
        self.types['Error'] = error_type
        self.types['IO'] = IO_type
        
        object_type.define_method('abort',[],[],object_type)
        object_type.define_method('type_name',[],[],string_type)
        object_type.define_method('copy',[],[],self_type)
        IO_type.define_method('out_string',['x'],[string_type],self_type)
        IO_type.define_method('out_int',['x'],[int_type],self_type)
        IO_type.define_method('in_string',[],[],string_type)
        IO_type.define_method('in_int',[],[],int_type)
        string_type.define_method('length',[],[],int_type)
        string_type.define_method('concat',['s'],[string_type],string_type)
        string_type.define_method('substr', ['i','l'] ,[int_type,int_type],string_type)
        
        int_type.parent = object_type
        string_type.parent = object_type
        bool_type.parent = object_type
        error_type.parent = object_type
        IO_type.parent = object_type

    

    def create_type(self, name:str):
        if name in self.types:
            raise SemanticException(f'Redefinition of basic class {name}.')
        typex = self.types[name] = Type(name)
        return typex

    def change_type(self,name:str,typex:str):
        self.types[name] = self.types[typex]

    def get_type(self, name:str):
        try:
            return self.types[name]
        except KeyError:
            raise SemanticException(f'Type "{name}" is not defined.')

    def __str__(self):
        return '{\n\t' + '\n\t'.join(y for x in self.types.values() for y in str(x).split('\n')) + '\n}'

    def __repr__(self):
        return str(self)

class VariableInfo:
    def __init__(self, name, vtype):
        self.name = name
        self.type = vtype

class Scope:
    def __init__(self, parent=None):
        self.locals = []
        self.parent = parent
        self.cil_locals = {}
        self.children = []
        self.index = 0 if parent is None else len(parent)

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
        
    def define_cil_local(self,cool_var_name,cil_var_name):
        cil_local = self.cil_locals[cool_var_name] = cil_var_name
        return cil_local

    def find_variable(self, vname, index=None):
        locals = self.locals if index is None else itt.islice(self.locals, index)
        try:
            return next(x for x in locals if x.name == vname)
        except :
            if self.parent is not None:
                a = self.parent.find_variable(vname, self.index)
            else :
                a = None
            return a

    def find_cil_variable(self,vname,index = None):
        locals = self.cil_locals if index is None else itt.islice(self.cil_locals, index)
        try:
            return next(self.cil_locals[x] for x in locals.keys() if x == vname)
        except:
            if self.parent is not None:
                a = self.parent.find_cil_variable(vname)
            else:
                a = None
            return a

    def is_defined(self, vname):
        a = self.find_variable(vname) is not None
        return a

    def is_cil_defined(self,cool_name):
        a = self.find_cil_variable(cool_name) is not None
        return a

    def is_local(self, vname):
        return any(True for x in self.locals if x.name == vname)
    
    def change_type(self,vname:str,vtype):
        var = self.find_variable(vname)
        var.type = vtype
    
    def substitute_type(self,typeA,typeB):

        for var in self.locals:
            if var.type == typeA:
                var.type = typeB

        if self.parent:
            self.parent.substitute_type(typeA,typeB)



def get_common_parent(type_A, type_B = None, context = None):
    if type_A.name == 'Error' or type_B.name == 'Error':
        return ErrorType()

    if type_B:
        parent_listA = [type_A]
        parent_listB = [type_B]
        common_parent = type_B
        while type_A.parent is not None:
            parent_listA.append(type_A.parent)
            type_A = context.get_type(type_A.parent.name)
        parent_listA = reversed(parent_listA)

        while type_B.parent is not None:
            parent_listB.append(type_B.parent)
            type_B = context.get_type(type_B.parent.name)
        parent_listB = reversed(parent_listB)

        for itemA, itemB in zip(parent_listA,parent_listB):
            if(itemA == itemB):
                common_parent = itemA
            else:
                break
    else:
        common_parent = type_A

    return common_parent 

def multiple_get_common_parent(args, context):
        least_type = args.pop(0)
    
        for t in args:
            if isinstance(least_type, ErrorType) or isinstance(t, ErrorType):
                least_type = ErrorType()
                return least_type
            least_type = get_common_parent(least_type,t,context)

        return least_type

def is_local(vars,new_var):
    return any(new_var == var.name for var in vars)