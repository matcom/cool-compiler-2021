from .node__ import Node
from ..tools import VisitBase
from ..scope import Scope
from ..create_type import CoolClass as AST_CoolClass

class CoolClass(Node):
    def __init__(self, typee, parent_typee, feature_list) -> None:
        self.type = typee
        self.parent_type = parent_typee
        self.feature_list = feature_list 

class VisitCoolClass(VisitBase):
    def visit(self, node: AST_CoolClass, scope : Scope):
        cls_scope : Scope = scope.create_child()
        self.gclss.current_type = node.type
        error_handler = self.get_se_handler(node)

        if node.parent_type.conforms_to(node.type):
            error_handler().add_semantic_error(f"class {self.gclss.current_type.name} has circular inheritance")        
        
        cls_scope.define_variable('self', self.gclss.current_type)
        for name, atype in node.type.ite_attributes:
            if not cls_scope.is_local(name):
                cls_scope.define_variable(name, atype)

        feature_list = self.visit_all(node.feature_list, cls_scope)
        return node.type, node.parent_type, feature_list