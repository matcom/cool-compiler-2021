
from .base import ExprNode


class UnaryExprNode(ExprNode):
    def __init__(self, lineno, columnno, expr):
        super().__init__(lineno, columnno)
        self.expr = expr


class IsVoidNode(UnaryExprNode):
    @staticmethod
    def parse(p):
        expr = p.expr
        return IsVoidNode(p.lineno, 0, expr)


class NotNode(UnaryExprNode):
    @staticmethod
    def parse(p):
        expr = p.expr
        return NotNode(p.lineno, 0, expr)


class TildeNode(UnaryExprNode):
    @staticmethod
    def parse(p):
        expr = p.expr
        return TildeNode(p.lineno, 0, expr)
