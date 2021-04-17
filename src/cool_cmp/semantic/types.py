from cool_cmp.semantic.interface import IContext, IVariableInfo, IAttributeInfo, IMethodInfo, IType, IScope
from cool_cmp.semantic.implementations import CoolType
from typing import List

class ObjectType(CoolType):
    """
    Cool Object Type
    """
    
    def __init__(self):
        super().__init__("Object", None)
    
class IntType(CoolType):
    """
    Cool Int Type
    """
    
    def __init__(self, father:ObjectType = ObjectType()):
        super().__init__("Int", father, False)
        
class BoolType(CoolType):
    """
    Cool Bool Type
    """
    
    def __init__(self, father:ObjectType = ObjectType()):
        super().__init__("Bool", father, False)
        
class StringType(CoolType):
    """
    Cool String Type
    """
    
    def __init__(self, father:ObjectType = ObjectType()):
        super().__init__("String", father, False)
        
class IOType(CoolType):
    """
    Cool IO Type
    """
    
    def __init__(self, father:ObjectType = ObjectType()):
        super().__init__("IO", father)
        
        