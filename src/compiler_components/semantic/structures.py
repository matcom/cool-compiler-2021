from collections import OrderedDict
import itertools as itt

############# Semantic Errors #######################
class SemanticError(Exception):
    @property
    def text(self):
        return str(self.args[0])
class TypeError(SemanticError):
    pass
class NameError(SemanticError):
    pass 
class AttributeError(SemanticError):
    pass
class ParamError(Exception):
    pass    
############## End Semantic Errors #############################

############ Class members ###############################
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
################# End Class Members #########################################


############# Type #######################################
class Type:
    def __init__(self, name:str,line=-1, column=-1):
        self.name = name
        self.attributes = []
        self.methods = []
        self.parent = None
        self.sons = []
        self.line = line
        self.column = column

    def set_parent(self, parent, pos=0):
        if self.parent is not None:
            raise SemanticError(f'Parent type is already set for {self.name}', pos)
        self.parent = parent
        parent.sons.append(self)

    def get_attribute(self, name:str,pos=0):
        try:
            return next(attr for attr in self.attributes if attr.name == name)
        except StopIteration:
            if self.parent is None:
                raise SemanticError(f'Attribute "{name}" is not defined in {self.name}',pos)
            try:
                return self.parent.get_attribute(name)
            except SemanticError:
                raise SemanticError(f'Attribute "{name}" is not defined in {self.name}',pos)

    def define_attribute(self, name:str, typex, pos):
        try:
            self.get_attribute(name)
        except SemanticError:
            a = Attribute(name, typex)
            self.attributes.append(a)
            return a
        else:
            raise SemanticError(f'Attribute "{name}" is already defined in {self.name}',pos)

    def get_method(self, name:str,line=0, col=0, own={'value':True}):
        try:
            return next(method for method in self.methods if method.name == name)
        except StopIteration:
            if self.parent is None:
                raise AttributeError(f'{line},{col} - NameError: Undeclared identifier {name}')
            try:
                own['value'] = False
                return self.parent.get_method(name, own)
            except SemanticError:
                raise AttributeError(f'{line},{col} - NameError: Undeclared identifier {name}')

    def define_method(self, name:str, param_names:list, param_types:list,  return_type, pos):
        try:
            own ={'value':True}
            method = self.get_method(name, pos, own = own)
            if method.return_type != return_type or method.param_types != param_types:
                raise SemanticError(f'Method "{name}" already defined in {self.name} with a different signature.', pos)
            else:
                if own['value']:
                    raise SemanticError(f'Method "{name}" already defined in {self.name} ', pos)
                raise AttributeError()

        except AttributeError as e:
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

    def __str__(self):
        output = f'Type {self.name}'
        return output

    def __repr__(self):
        return str(self)

class ErrorType(Type):
    def __init__(self):
        Type.__init__(self, '<error>')

    def conforms_to(self, other):
        return True

    def bypass(self):
        return True

    def __eq__(self, other):
        return isinstance(other, Type)

class VoidType(Type):
    def __init__(self):
        Type.__init__(self, '<void>')

    def conforms_to(self, other):
        raise Exception('Invalid type: void type.')

    def bypass(self):
        return True

    def __eq__(self, other):
        return isinstance(other, VoidType)

class SELF_TYPE(Type):
    def __init__(self):
        Type.__init__(self, "SELF_TYPE")

    def __eq__(self, other):
        return isinstance(other, SELF_TYPE)

########### End Type ##########################


########## Context ###################################
class Context:
    def __init__(self):
        self.types = {}
        self.built_in()

    def built_in(self):
        Bool = Type("Bool")
        self.types["Bool"] = Bool

        Int = Type("Int")
        self.types["Int"] = Int

        Object = Type("Object")
        self.types["Object"] =Object

        String = Type("String")
        self.types["String"] = String

        IO = Type("IO")
        self.types['IO']= IO

        Object.define_method("abort",[],[],Object,0)
        Object.define_method("type_name",[],[],String,0)
        Object.define_method("copy",[],[],SELF_TYPE(),0)

        String.define_method("length",[],[],Int,0)    
        String.define_method("concat",['s'],[String],String,0) 
        String.define_method("substr",['i','l'],[Int,Int],SELF_TYPE(),0)
        
        IO.define_method("out_string",["x"],[String],SELF_TYPE(),0)
        IO.define_method("out_int",['x'],[Int],SELF_TYPE(),0)
        IO.define_method("in_int",[],[],Int,0)
        IO.define_method("in_string",[], [], String, 0)

    def check_type(self,x:Type,y:Type,pos):
        if not x.conforms_to(y) :
            raise(TypeError(f"Expr type {x.name} is no subclass of {y.name} ",pos))

    def create_type(self, name:str,line=0, column=0):
        if name in self.types:
            raise SemanticError(f'Type with the same name ({name}) already in context.')
        t = self.types[name] = Type(name, line, column)
        return t
        
    def get_type(self, name:str,pos=0):
        try:
            return self.types[name]
        except KeyError:
            raise TypeError(f'Type "{name}" is not defined.' , pos)

    def closest_common_antecesor(self, type1:Type, type2:Type):
        antecesors = []
        while not type1 is None or not type2 is None :
            if not type2 is None :
                if type2 in antecesors:
                    return type2
                antecesors.append(type2)

            if not type1 is None:
                if type1 in antecesors:
                    return type1
                antecesors.append(type1)
            
            if not type1 is None:
                type1 = type1.parent
            if not type2 is None:
                type2 = type2.parent

        return self.get_type("Object")

    def circular_dependency(self):
        visited = set()
        on_cycle = {}
        count = 0
        for tp in self.types:
            temp = self.types[tp]
            ancestors = set()
            while True:
                if temp.name in visited:
                    break
                ancestors.add(temp.name)
                visited.add(temp.name)
                if temp.parent is None:
                    break
                if temp.parent.name in ancestors:
                    on_cycle[count] = []
                    on_cycle[count].append((temp.name,temp.line, temp.column))
                    temp2 = temp.parent
                    while temp != temp2:
                        on_cycle[count].append((temp2.name,temp2.line, temp2.column))
                        temp2 = temp2.parent
                    on_cycle[count].sort(key= lambda x:x[1],reverse=True)
                    count = count + 1
                    break
                temp = temp.parent
        return on_cycle.values()
############ End Context ########################

class VariableInfo:
    def __init__(self, name, typex):
        self.name = name
        self.type = typex

################## Scope ##############################
class Scope:
    def __init__(self, parent=None):
        self.locals = []
        self.parent = parent
        self.children = []
        self.id = 0
        self.index = 0 if parent is None else len(parent)

    def __len__(self):
        return len(self.locals)

    def create_child(self):
        child = Scope(self)
        child.id = self.id*10 +len(self.children)
        self.children.append(child)
        return child

    def is_defined(self, vname):
        return self.find_variable(vname) is not None

    def is_local(self, vname):
        return any(True for x in self.locals if x.name == vname)

    def define_variable(self, vname, vtype,pos=0):
        if  self.is_local(vname):
            raise SemanticError(f"Variable {vname} already define in scope " , pos)
        v = VariableInfo(vname, vtype)
        self.locals.append(v)
        return v

    def find_variable(self, vname, index=None):
        locals = self.locals if index is None else itt.islice(self.locals, index)
        
        for l in locals:
            if l.name == vname:
                return l
        
        if not self.parent is None:
            return self.parent.find_variable(vname, self.index)  
        else:
            return None