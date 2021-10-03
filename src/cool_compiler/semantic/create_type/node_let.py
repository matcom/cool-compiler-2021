from .node__ import Statement
from ..tools import VisitBase
from ..factory_return_ast import LetIn as AST_LetIn

class LetIn(Statement):
    def __init__(self, assing_list, expr) -> None:
        self.assing_list = assing_list
        self.expr = expr
    
class VisitLetIn(VisitBase):
    def visit(self, node : AST_LetIn) : 
        error_handler = self.gclss.get_se_handler(node)

        assing_list = []
        for name, atype, expr in node.assing_list:
            rtype = self.get_type(atype, error_handler) 
            assing_list.append((name, rtype, self.gclss.visit(expr)))
 
        return assing_list, self.gclss.visit(node.expr)



        