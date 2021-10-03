from .node__ import Expresion
from ..tools import defVisitClass
from ..factory_return_ast import CastingDispatch as AST_CastingDispatch
from ..factory_return_ast import StaticDispatch as AST_StaticDispatch
from ..factory_return_ast import Dispatch as AST_Dispatch

   
class CastingDispatch(Expresion):
    def __init__(self, expr, atype, idf, params) -> None:
        self.expr = expr
        self.type = atype
        self.id = idf
        self.params = params

VisitCastingDispatch = defVisitClass(
    lambda self, node, error: self.gclss.visit(node.expr),
    lambda self, node, error: self.get_type(node.type, error),
    lambda self, node, error: node.id,
    lambda self, node, error: self.visit_all(node.params),
)
##############################################################################

class Dispatch(Expresion):
    def __init__(self, expr, idf, params) -> None:
        self.expr = expr
        self.id = idf
        self.params = params

VisitDispatch = defVisitClass(
    lambda self, node, error: self.gclss.visit(node.expr),
    lambda self, node, error: node.id,
    lambda self, node, error: self.visit_all(node.params),
)

###############################################################################
class StaticDispatch(Expresion):
    def __init__(self, idf, params) -> None:
        self.id = idf
        self.params = params

VisitStaticDispatch = defVisitClass(
    lambda self, node, error: node.id,
    lambda self, node, error: self.visit_all(node.params),
)







