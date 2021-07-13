from cmp.semantic import Attribute, Method
from cmp.semantic import Type as DeprecatedType
from cmp.semantic import SemanticError as DeprecatedSemanticError
from cool.ast.ast import VoidNode,ConstantNumNode,StringNode,BoolNode,SpecialNode,InstantiateNode
from cool.semantic.atomic import ClassInstance
from cool.error.errors import RunError, SemanticError, TypeCoolError, InferError, \
    VOID_TYPE_CONFORMS, METHOD_NOT_DEFINED, METHOD_ALREADY_DEFINED, \
    SUBSTR_OUT_RANGE, ATTRIBUTE_NOT_DEFINED, ATTRIBUTE_ALREADY_DEFINED, \
    ATTRIBUTE_CANT_INFER, METHOD_CANT_INFER, TYPE_CANT_INFER, TYPE_CANT_BE_INHERITED, \
    NO_COMMON_TYPE, READ_IS_NOT_INT, ATTRIBUTE_ALREADY_DEFINED_IN_PARENT
import cool.visitors.utils as ut

class Type(DeprecatedType):
    
    def add_special_method(self,func,method_name,method_args):
        f = self.get_method(method_name,method_args)
        old_type = f.node.body.type
        f.node.body = SpecialNode(func,f.node.row,f.node.column)
        f.node.body.type = old_type
    
    def set_parent(self,parent):
        try:
            DeprecatedType.set_parent(self,parent)
            if not parent.can_have_children:
                self.parent = None
                raise SemanticError(TYPE_CANT_BE_INHERITED, self.name, parent.name)
        except DeprecatedSemanticError as er:
            raise SemanticError(er.text)
        
    def __hash__(self):
        return hash(self.name)

    def __eq__(self,other):
        return isinstance(other, type(self)) and other.name==self.name
    
    def get_method(self,name:str,args:int,current_type = None, only_local = False):
        self = self if not isinstance(self,SelfType) or not current_type else current_type
        try:
            return next(method for method in self.methods if method.name == name and len(method.param_names)==args)
        except StopIteration:
            if self.parent is None or self.parent == self:
                raise SemanticError(METHOD_NOT_DEFINED,name, "", self.name, args)
            try:
                if not only_local:
                    return self.parent.get_method(name,args)
                raise SemanticError()
            except SemanticError:
                raise SemanticError(METHOD_NOT_DEFINED, name, "" if not only_local else " locally", self.name, args)
    
    def define_method(self, name:str, param_names:list, param_types:list, return_type):
        if (name,len(param_names)) in ((method.name,len(method.param_names)) for method in self.methods):
            raise SemanticError(METHOD_ALREADY_DEFINED, name)
        method = Method(name, param_names, param_types, return_type)
        self.methods.append(method)
        return method

    def get_parents(self):
        if self.parent:
            parents = self.parent.get_parents()
            return [self.parent] + parents
        else:
            return []
        
    def get_attribute(self, name:str):
        return self._get_attribute(name, set())
        
    def _get_attribute(self, name:str, visited_types:set):
        if self in visited_types:
            raise SemanticError(ATTRIBUTE_NOT_DEFINED, name, self.name)
        try:
            return next(attr for attr in self.attributes if attr.name == name)
        except StopIteration:
            if self.parent is None or self.parent == self:
                raise SemanticError(ATTRIBUTE_NOT_DEFINED, name, self.name)
            try:
                visited_types.add(self)
                return self.parent._get_attribute(name, visited_types)
            except SemanticError:
                raise SemanticError(ATTRIBUTE_NOT_DEFINED, name, self.name)
    
    def define_attribute(self, name:str, typex):
        try:
            attribute = self.get_attribute(name)
        except SemanticError:
            attribute = Attribute(name, typex)
            self.attributes.append(attribute)
            return attribute
        else:
            if attribute in self.attributes:
                raise SemanticError(ATTRIBUTE_ALREADY_DEFINED, name)
            else:
                raise SemanticError(ATTRIBUTE_ALREADY_DEFINED_IN_PARENT, name)
    
    def conforms_to(self,other,current_type):
        self_type = self if not isinstance(self,SelfType) else current_type
        other_type = other if not isinstance(other,SelfType) else current_type
        if isinstance(other,AutoType):
            new_types = []
            for x in self_type.get_parents() + [self_type]:
                if x in other_type.possibles:
                    new_types.append(x)
            other.update_possibles(new_types)
            return bool(new_types)
        return self_type.__conforms_to(other_type)
    
    def __conforms_to(self, other):
        return other.bypass() or self == other or self.parent is not None and self.parent.__conforms_to(other)

    def join(self,other,current_type):
        self = self if not isinstance(self,SelfType) else current_type
        other = other if not isinstance(other,SelfType) else current_type

        self = self if not isinstance(self,AutoType) else self.get_lower(current_type)
        other = other if not isinstance(other,AutoType) else other.get_lower(current_type)
        
        self_parents = self.get_parents()
        other_parents = other.get_parents()
        other_types = [other] + other_parents
        self_types = [self] + self_parents
        for common in self_types:
            if common in other_types:
                return common
        raise TypeCoolError(NO_COMMON_TYPE, self.name, other.name)
        
    @property
    def can_have_children(self):
        return True

    @property
    def default(self):
        return InstantiateNode("Void")

class ObjectType(Type):
    def __init__(self):
        Type.__init__(self, 'Object')
        self.parent = None
        
    def complete(self):
        self.add_special_method(self.abort,'abort',0)
        self.add_special_method(self.copy,'copy',0)
        self.add_special_method(self.type_name,'type_name',0)
        
    def set_parent(self,parent):
        pass
    
    @staticmethod
    def abort(scope,context,operator,errors,**kwargs):
        raise RunError('Cool Program Aborted')

    @staticmethod
    def type_name(scope,context,operator,errors,**kwargs):
        this_type = scope.get_variable_value('self').type
        string = context.get_type('String')
        return ClassInstance(string,context,operator,errors,value=this_type.name)

    @staticmethod
    def copy(scope,context,operator,errors,**kwargs):
        value = scope.get_variable_value('self')
        return value.shallow_copy()

class SelfType(Type):
    
    def __init__(self):
        Type.__init__(self, 'SELF_TYPE')
    
    @property
    def can_have_children(self):
        return False

class IntType(Type):
    def __init__(self):
        Type.__init__(self, 'Int')

    @property
    def can_have_children(self):
        return False
    
    @property
    def default(self):
        return ConstantNumNode('0')

class BoolType(Type):
    def __init__(self):
        Type.__init__(self, 'Bool')

    @property
    def can_have_children(self):
        return False

    @property
    def default(self):
        return BoolNode('false')

class StringType(Type):
    def __init__(self):
        Type.__init__(self, 'String')
    
    def complete(self):
        self.add_special_method(self.length,'length',0)
        self.add_special_method(self.concat,'concat',1)
        self.add_special_method(self.substr,'substr',2)
        
    @staticmethod
    def length(scope,context,operator,errors,**kwargs):
        value = scope.get_variable_value('self').value
        int_type = context.get_type('Int')
        return ClassInstance(int_type,context,operator,errors,value=len(value))
        
    @staticmethod
    def concat(scope,context,operator,errors,**kwargs):
        value = scope.get_variable_value('self').value
        concat = scope.get_variable_value('s').value
        typex = context.get_type('String')
        return ClassInstance(typex,context,operator,errors,value=value + concat)

    @staticmethod
    def substr(scope,context,operator,errors,**kwargs):
        value = scope.get_variable_value('self').value
        i = scope.get_variable_value('i').value
        l = scope.get_variable_value('l').value
        typex = context.get_type('String')
        value_sliced = value[i:i+l]
        if len(value) < l-i or l < 0:
            raise RunError(SUBSTR_OUT_RANGE,value,i,l)
        return ClassInstance(typex,context,operator,errors,value=value_sliced)
    
    @property
    def can_have_children(self):
        return False
    
    @property
    def default(self):
        return StringNode('""')

class VoidType(Type):
    
    def __init__(self):
        Type.__init__(self, 'Void')
    
    def conforms_to(self, other, current_type):
        return True

    def bypass(self):
        return True

class ErrorType(Type):
    def __init__(self):
        Type.__init__(self, 'Error')

    def conforms_to(self, other, current_type):
        return True

    def bypass(self):
        return True

    def __eq__(self, other):
        return isinstance(other, Type)
    
    def __hash__(self):
        return super().__hash__()

class IOType(Type):
    def __init__(self):
        Type.__init__(self, 'IO')
    
    def complete(self):
        self.add_special_method(self.out_string,'out_string',1)
        self.add_special_method(self.out_int,'out_int',1)
        self.add_special_method(self.in_string,'in_string',0)
        self.add_special_method(self.in_int,'in_int',0)
        
    @staticmethod
    def out_string(scope,context,operator,errors,**kwargs):
        out = scope.get_variable_value('x').value
        print(out, end="")
        typex = context.get_type('IO')
        return scope.get_variable_value('self')
    
    @staticmethod
    def out_int(scope,context,operator,errors,**kwargs):
        out = scope.get_variable_value('x').value
        print(out, end="")
        typex = context.get_type('IO')
        return scope.get_variable_value('self')
    
    @staticmethod
    def in_string(scope,context,operator,errors,**kwargs):
        value = input()
        typex = context.get_type('String')
        return ClassInstance(typex,context,operator,errors,value=value)
    
    @staticmethod
    def in_int(scope,context,operator,errors,**kwargs):
        value = input()
        import re
        m = re.search(" *([1234567890]+)[^1234567890\n]*\n?", value)
        typex = context.get_type('Int')
        try:
            if m:
                return ClassInstance(typex,context,operator,errors,value=int(m.group(1)))
            else:
                raise ValueError()
        except ValueError:
            raise RunError(READ_IS_NOT_INT, value)

class AutoType(Type):
    def __init__(self,context):
        Type.__init__(self, 'AUTO_TYPE')
        self.parent = None
        self.context = context
        self.possibles = [ x for x in context.types.values() if not isinstance(x, ErrorType) ]
        self.equals = [self,]
    
    def update_possibles(self, new_possibles):
        for x in self.equals:
            x.possibles = new_possibles
    
    def get_attribute(self,name):
        self.update_possibles([x for x in self.possibles if any(attr for attr,typex in x.all_attributes() if attr.name==name)])
        if not self.possibles:
            raise InferError(ATTRIBUTE_CANT_INFER, name)
        return self.possibles[-1].get_attribute(name)
        
    def get_method(self,name,args,current_type = None):
        self.update_possibles([x for x in self.possibles if any(meth for meth,typex in x.all_methods() if (meth.name==name and len(meth.param_names) == args))])
        if not self.possibles:
            raise InferError(METHOD_CANT_INFER, name, args)
        return self.possibles[-1].get_method(name,args)
   
    def conforms_to(self,other,current_type):
        self_type = self if not isinstance(self,SelfType) else current_type
        other_type = other if not isinstance(other,SelfType) else current_type
        if isinstance(other,AutoType):
            new_possibles = []
            for p_type in self.possibles:
                if p_type in other_type.possibles:
                    new_possibles.append(p_type)
            
            self.add_to_equals(other)
            
            self.update_possibles(new_possibles)
            
            return bool(new_possibles)
        else:
            self.update_possibles([x for x in self.possibles if other_type.conforms_to(x,current_type)])
            return bool(self.possibles)
    
    def is_valid(self,current_type):
        """
        Return True if the graph of the possible types is unilaterally connected 
        """
        if not self.possibles: return False
        graph = ut.reverse_graph(ut.build_graph_list(self.possibles))
        _, topo_sort = ut.any_cycles(graph, True)
        current = topo_sort[0]
        d, f = ut.dfs(graph, current)
        if len(d) == len(graph):
            return True
        return False
        
    def add_to_equals(self,other):
        if not id(other) in [id(x) for x in self.equals]:
            for x in self.possibles:
                if not x in other.possibles:
                    self.possibles.remove(x)
            for eq in other.equals:
                self.equals.append(eq)
                eq.equals = self.equals
                eq.possibles = self.possibles
    
    def remove_possible(self, typex):
        self.possibles.remove(typex)
        self.update_possibles(self.possibles)
    
    def get_higher(self, current_type):
        valid = self.is_valid(current_type)
        if not valid: raise InferError(TYPE_CANT_INFER)
        graph = ut.reverse_graph(ut.build_graph_list(self.possibles))
        _, topo_sort = ut.any_cycles(graph, True)
        
        current = topo_sort[0]
        while len(graph[current]) == 1:
            current = graph[current][0]
            
        return current
    
    def get_lower(self,current_type):
        ## Lower implementation using graphs
        valid = self.is_valid(current_type)
        if not valid: raise InferError(TYPE_CANT_INFER)
        graph = ut.reverse_graph(ut.build_graph_list(self.possibles))
        _, topo_sort = ut.any_cycles(graph, True)
        
        current = topo_sort[0]
        return current
        ## Lower implementation using join operator
        # possibles = [x for x in self.possibles if not isinstance(x, ErrorType)]
        # lesser = possibles[0]
        # for x in possibles:
        #     lesser = x.join(lesser,current_type)
        # return lesser