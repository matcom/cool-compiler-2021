from cool_cmp.shared.ast import BaseAST
from cool_cmp.shared import ICoolService
from typing import List

class ISemantic(ICoolService):
    """
    Semantic interface to implement
    """

    def __call__(self, ast:BaseAST) -> BaseAST:
        raise NotImplementedError()


class IType:
    """
    Type interface to implement
    """
    
    @property
    def name(self)->str:
        raise NotImplementedError()
    
    @property
    def father(self)->'IType':
        raise NotImplementedError()

    @property
    def is_inheritable(self)->bool:
        raise NotImplementedError()
    
    def add_attribute(self, name:str, attr_type:'IType')->'IAttributeInfo':
        raise NotImplementedError()
    
    def is_attribute_defined(self, name:str)->bool:
        raise NotImplementedError()
        
    def add_method(self, name:str, params:List['IVariableInfo'], return_type:'IType')->'IMethodInfo':
        raise NotImplementedError()

    def is_method_defined(self, name:str, params_count:int)->bool:
        raise NotImplementedError()
    
    def get_method(self, name:str, params_count:int)->'IMethodInfo':
        raise NotImplementedError()
    
    def get_attribute(self, name:str)->'IAttributeInfo':
        raise NotImplementedError()
    
    @property
    def methods(self)->List['IMethodInfo']:
        raise NotImplementedError()
        
    @property
    def attributes(self)->List['IAttributeInfo']:
        raise NotImplementedError()
    
    
class IVariableInfo:
    """
    Variable info interface to implement
    """
    
    @property
    def name(self)->str:
        raise NotImplementedError()
    
    @property
    def type(self)->IType:
        raise NotImplementedError()

class IMethodInfo:
    """
    Method info interface to implement
    """
    
    @property
    def name(self)->str:
        raise NotImplementedError()
    
    @property
    def parameters(self)->List[IVariableInfo]:
        raise NotImplementedError()
    
    @property
    def return_type(self)->IType:
        raise NotImplementedError()

class IAttributeInfo(IVariableInfo):
    """
    Attribute info interface to implement
    """
    pass

class IContext:
    """
    Context interface to implement
    """
    
    def add_type(self, name:str)->IType:
        raise NotImplementedError()
    
    def get_type(self, name:str)->IType:
        raise NotImplementedError()
    

class IScope:
    """
    Scope interface to implement
    """
    
    @property
    def father(self)->'IScope':
        raise NotImplementedError()
    
    def find_variable(self, name: str)->IVariableInfo:
        raise NotImplementedError()
    
    @property
    def local_variables(self)->List[IVariableInfo]:
        raise NotImplementedError()
    
    def is_local_variable_defined(self, name: str)->bool:
        raise NotImplementedError()
    
    def add_variable(self, name: str, variable_type: IType)->IVariableInfo:
        raise NotImplementedError()
        
    def create_child(self)->'IScope':
        raise NotImplementedError()