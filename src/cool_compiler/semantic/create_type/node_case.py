from .node__ import Statement
from ..tools import VisitBase
from ..factory_return_ast import Case as AST_Case

class Case(Statement):
    def __init__(self, expr, case_list) -> None:
        self.case_list = case_list
        self.expr = expr
    
class VisitCase(VisitBase):
    def visit(self, node : AST_Case) : 
        error_handler = self.gclss.get_se_handler(node)

        case_list = []
        for name, atype, expr in node.case_list:
            rtype = self.get_type(atype, error_handler) 
            case_list.append((name, rtype, self.gclss.visit(expr)))
 
        return self.gclss.visit(node.expr), case_list
    
