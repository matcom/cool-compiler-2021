from .node__ import Expresion
from ..tools import defVisitClass
from ..factory_return_ast import Sum as AST_Sum
from ..factory_return_ast import Rest as AST_Rest
from ..factory_return_ast import Div as AST_Div
from ..factory_return_ast import Mult as AST_Mult
from ..factory_return_ast import Less as AST_Less
from ..factory_return_ast import LessOrEquals as AST_LessOrEquals
from ..factory_return_ast import Equals as AST_Equals

class Binary(Expresion):
    def __init__(self, left, right) -> None:
        self.left = left
        self.right = right

class Sum(Binary):
    pass

class Rest(Binary):
    pass

class Mult(Binary):
    pass

class Div(Binary):
    pass

class Less(Binary):
    pass

class LessOrEquals(Binary):
    pass

class Equals(Binary):
    pass

VisitBinary = defVisitClass(
    lambda self, node, error: self.gclss.visit(node.left),
    lambda self, node, error: self.gclss.visit(node.right),
)