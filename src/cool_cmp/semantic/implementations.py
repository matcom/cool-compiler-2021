from cool_cmp.semantic.interface import IContext, IVariableInfo, IAttributeInfo, IMethodInfo, IType, IScope
from cool_cmp.semantic.errors import SemanticError, VARIABLE_ALREADY_DEFINED, ATTRIBUTE_ALREADY_DEFINED, \
    METHOD_ALREADY_DEFINED, METHOD_REDEFINITION_INVALID, METHOD_NOT_DEFINED, ATTRIBUTE_NOT_DEFINED, \
    TYPE_NOT_DEFINED, TYPE_ALREADY_DEFINED, VARIABLE_NOT_DEFINED, TYPE_NOT_INHERITABLE
from typing import List

class VariableInfo(IVariableInfo):
    """
    Base VariableInfo
    """
    
    def __init__(self, name:str, variable_type:IType):
        self._name = name
        self._type = variable_type
    
    @property
    def name(self)->str:
        return self._name
    
    @property
    def type(self)->IType:
        return self._type

class AttributeInfo(IAttributeInfo):
    """
    Base AttributeInfo
    """
    
    def __init__(self, name:str, variable_type:IType):
        self._name = name
        self._type = variable_type
    
    @property
    def name(self)->str:
        return self._name
    
    @property
    def type(self)->IType:
        return self._type

class MethodInfo(IMethodInfo):
    """
    Base MethodInfo
    """
    
    def __init__(self, name:str, parameters:List[IVariableInfo], return_type:IType):
        self._name = name
        self._parameters = parameters
        self._return_type = return_type
    
    @property
    def name(self)->str:
        return self._name
    
    @property
    def parameters(self)->List[IVariableInfo]:
        return self._parameters
    
    @property
    def return_type(self)->IType:
        return self._return_type

class CoolType(IType):
    """
    Base Type
    """
    
    ATTRIBUTE_INFO_TYPE = AttributeInfo
    METHOD_INFO_TYPE = MethodInfo
    
    def __init__(self, name:str, father:IType, inheritable:bool=True):
        self._name = name
        self._father = father
        self._inheritable = inheritable
        self._attributes = []
        self._methods = []
        
    
    @property
    def name(self)->str:
        return self._name
    
    @property
    def father(self)->IType:
        return self._father

    @property
    def is_inheritable(self)->bool:
        return self._inheritable
    
    def add_attribute(self, name:str, attr_type:IType)->IAttributeInfo:
        if self.is_attribute_defined(name):
            raise SemanticError(ATTRIBUTE_ALREADY_DEFINED(name, self.name))
        attribute = self.ATTRIBUTE_INFO_TYPE(name, attr_type)
        self._attributes.append(attribute)
        return attribute
    
    def is_attribute_defined(self, name:str)->bool:
        try:
            attr = self.get_attribute(name)
            return bool(attr)
        except SemanticError:
            return False
        
    def add_method(self, name:str, params:List[IVariableInfo], return_type:IType)->IMethodInfo:
        try:
            # Checking if a local method already exist with the given signature
            local_method = next(x for x in self._methods if x.name == name and len(x.parameters) == len(params))
            raise SemanticError(METHOD_ALREADY_DEFINED(name, len(params), self.name))
        except StopIteration:
            # Checking if the method already exist in parents types and can be redefined
            if self.father:
                try:
                    parent_method = self.father.get_method(name, len(params))
                    if not all([parent_method.return_type == return_type, *[x.type == y.type for x,y in zip(params, parent_method.parameters)]]):
                        # The params types or the return type of the new and the old method doesn't match
                        raise SemanticError(METHOD_REDEFINITION_INVALID(name, parent_method.parameters + [parent_method.return_type]))
                except SemanticError:
                    # No method exist
                    pass
                
            # The method can be defined in this type
            method = self.METHOD_INFO_TYPE(name, params, return_type)
            self._methods.append(method)
            return method
            
    def is_method_defined(self, name:str, params_count:int)->bool:
        try:
            method = self.get_method(name, params_count)
            return bool(method)
        except SemanticError:
            return False 
    
    def get_method(self, name:str, params_count:int)->IMethodInfo:
        try:
            method = next(x for x in self.methods if x.name == name and len(x.parameters) == len(params))
            return method
        except StopIteration:
            raise SemanticError(METHOD_NOT_DEFINED(name, params_count, self.name))
            
    def get_attribute(self, name:str)->IAttributeInfo:
        try:
            attr = next(x for x in self.attributes if x.name == name)
        except StopIteration:
            raise SemanticError(ATTRIBUTE_NOT_DEFINED(name, self.name))
    
    @property
    def methods(self)->List[IMethodInfo]:
        father_methods = []
        if self.father:
            father_methods = self.father.methods
        return self._methods + father_methods
        
    @property
    def attributes(self)->List[IAttributeInfo]:
        father_attrs = []
        if self.father:
            father_attrs = self.father.attributes
        return self._attributes + father_attrs

class Context(IContext):
    """
    Base Context
    """
    
    TYPE_TYPE = CoolType
        
    def __init__(self, basic_types:List[IType]=[]):
        self._types = basic_types
        
    def add_type(self, name:str, father:IType)->IType:
        if not father.is_inheritable:
            raise SemanticError(TYPE_NOT_INHERITABLE(father.name))
        try:
            typex = self.get_type(name)
        except SemanticError:
            typex = self.TYPE_TYPE(name, father)
            self._types.append(typex)
            return typex
        raise SemanticError(TYPE_ALREADY_DEFINED(name))
    
    def get_type(self, name:str)->IType:
        try:
            typex = next(x for x in self._types if x.name == name)
            return typex
        except StopIteration:
            raise SemanticError(TYPE_NOT_DEFINED(name))

class Scope(IScope):
    """
    Base Scope
    """
    
    # Implementation type for IVariableInfo used by this scope
    VARIABLE_INFO_TYPE = VariableInfo
    
    def __init__(self, father=None, children:List[IScope]=[], locals:List[IVariableInfo]=[]):
        self._locals = locals
        self._father = father
        self.children = children
        self.index = 0 if father is None else len(father)

    def __len__(self):
        return len(self._locals)
    
    @property
    def father(self)->IScope:
        return self._father
    
    def find_variable(self, name: str, index=None)->IVariableInfo:
        index = index if not index is None else len(self.local_variables)
        for var in self.local_variables[:index]:
            if var.name == name:
                return var
        if self.father:
            return self.father.find_variable(name, self.index)
        raise SemanticError(VARIABLE_NOT_DEFINED(name))
    
    @property
    def local_variables(self)->List[IVariableInfo]:
        return self._locals
    
    def is_local_variable_defined(self, name: str)->bool:
        return len([v for v in self.local_variables if v.name == name]) == 1
    
    def add_variable(self, name: str, variable_type: IType)->IVariableInfo:
        if self.is_local_variable_defined(name):
            raise SemanticError(VARIABLE_ALREADY_DEFINED(name))
        variable = self.VARIABLE_INFO_TYPE(name, variable_type)
        self._locals.append(variable)
        return variable
        
    def create_child(self)->IScope:
        child = type(self)(self) # In case of been inherited the Scope class the child created will have the same type of its father
        self.children.append(child)
        return child