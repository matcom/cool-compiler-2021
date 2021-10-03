from .node__ import Feature
from ..__dependency import Type, Object, SemanticError, ErrorType
from ..tools import VisitBase, find_type
from ..factory_return_ast import FuncDef as AST_FuncDef
   
class FuncDef(Feature):
    def __init__(self, name, param_list, return_type, expr) -> None:
        self.name = name
        self.params = param_list
        self.return_type = return_type
        self.expr = expr

class VisitFuncDef(VisitBase):
    def visit(self, node : AST_FuncDef) : 
        error_handler = self.gclss.get_se_handler(node)
        
        return_type = self.get_type(node.return_type, error_handler)

        params = []
        for name, ptype in node.params:
            param_type = self.get_type(ptype, error_handler)
            params.append((name, param_type))

        self.gclss.current_type.define_method(node.name, params, return_type)
        expr = self.gclss.visit(node.expr)
        return node.name, params, return_type, expr        