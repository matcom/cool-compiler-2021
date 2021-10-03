from .node__ import Feature
from ..__dependency import Type, Object, SemanticError, ErrorType
from ..tools import VisitBase, find_type
from ..factory_return_ast import AtrDef as AST_AtrDef
   
class AtrDef(Feature):
    def __init__(self, name, atype, expr) -> None:
        self.name = name
        self.type = atype
        self.expr = expr

class VisitAttrDef(VisitBase):
    def visit(self, node : AST_AtrDef) : 
        error_handler = self.gclss.get_se_handler(node)
        
        atype = self.get_type(node.type, error_handler)
        self.gclss.current_type.define_attribute(node.name, atype)

        expr = self.gclss.visit(node.expr)
        return node.name, atype, expr




         