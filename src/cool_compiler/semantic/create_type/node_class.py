from .node__ import Node
from ..__dependency import Type, Object, SemanticError, ErrorType
from ..tools import VisitBase, find_type
from ..factory_return_ast import CoolClass as AST_CoolClass
   
class CoolClass(Node):
    def __init__(self, typee, parent_typee, feature_list) -> None:
        self.type : Type = typee
        self.parent_type : Type = parent_typee
        self.feature_list = feature_list

class VisitCoolClass(VisitBase):
    def visit(self, node : AST_CoolClass) : 
        self.gclss.current_type = self.gclss.global_types[node.name]
        error_handler = self.gclss.get_se_handler(node)
        
        parent_type = self.get_parent_type(node, error_handler)
        try: self.gclss.current_type.set_parent(parent_type)
        except SemanticError: pass

        feature_list = self.visit_all(node.feature_list)
        
        return self.gclss.current_type, parent_type, feature_list

    
    def get_parent_type(self, node : AST_CoolClass, error_handler):
        if node.parent is None: return Object()
            
        find_result = find_type(node.parent, self.gclss.global_types)
        parent_type = find_result.get_value( if_fail_do= error_handler().add_semantic_error )
            
        if parent_type.is_shield or parent_type.name == self.gclss.current_type.name: 
            error_handler().add_semantic_error( f"class {self.gclss.current_type.name} can't be inherited from {parent_type.name}" )
            return ErrorType()

        return parent_type 
        
        
        