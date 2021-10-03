from .node__ import Statement
from ..tools import defVisitClass
from ..factory_return_ast import Assing as AST_Assing
from ..factory_return_ast import IfThenElse as AST_IfThenElse
from ..factory_return_ast import While as AST_While
from ..factory_return_ast import Block as AST_Block

class Assing(Statement):
    def __init__(self, name, expr) -> None:
        self.id = name
        self.expr = expr

VisitAssing = defVisitClass(
    lambda self, node, error: node.id,
    lambda self, node, error: self.gclss.visit(node.expr),
)

##############################################################################
class IfThenElse(Statement):
    def __init__(self, condition, then_expr, else_expr) -> None:
        self.condition = condition
        self.then_expr = then_expr
        self.else_expr = else_expr

VisitIfThenElse = defVisitClass(
    lambda self, node, error: self.gclss.visit(node.condition),
    lambda self, node, error: self.gclss.visit(node.then_expr),
    lambda self, node, error: self.gclss.visit(node.else_expr),
)

###############################################################################
class While(Statement):
    def __init__(self, condition, loop_expr) -> None:
        self.condition = condition
        self.loop_expr = loop_expr

VisitWhile = defVisitClass(
    lambda self, node, error: self.gclss.visit(node.condition),
    lambda self, node, error: self.gclss.visit(node.loop_expr),
)

###############################################################################
class Block(Statement):
    def __init__(self, expr_list) -> None:
        self.expr_list = expr_list

VisitBlock = defVisitClass(
    lambda self, node, error: self.visit_all(node.expr_list),
)