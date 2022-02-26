from .base import (ExprNode, LetDeclNode)
from typing import List


class AssignNode(ExprNode):
    def __init__(self, lineno, columnno, id, expr):
        super().__init__(lineno, columnno)
        self.id = id
        self.expr = expr

    @staticmethod
    def parse(p):
        return AssignNode(p.lineno, 0, p.OBJECT_ID, p.expr)


class StaticDispatchNode(ExprNode):
    def __init__(self, lineno, columnno, expr, static_type, id, args):
        super().__init__(lineno, columnno)

        self.expr = expr
        self.static_type = static_type
        self.id = id
        self.args = args

    @staticmethod
    def parse(p):
        return StaticDispatchNode(p.lineno, 0, p.expr, p.TYPE_ID, p.OBJECT_ID, p.arg_list if p.arg_list is not None else [])


class DispatchNode(ExprNode):
    def __init__(self, lineno, columnno, id, args, expr=None):
        super().__init__(lineno, columnno)
        self.expr = expr
        self.id = id
        self.args = args

    @staticmethod
    def parse(p, expr):
        return DispatchNode(p.lineno, 0,  p.OBJECT_ID, p.arg_list if p.arg_list is not None else [], expr)


class IfThenElseNode(ExprNode):
    def __init__(self, lineno, columnno, cond, then_expr, else_expr):
        super().__init__(lineno, columnno)
        self.cond = cond
        self.then_expr = then_expr
        self.else_expr = else_expr

    @staticmethod
    def parse(p):
        return IfThenElseNode(p.lineno, 0, p.expr0, p.expr1, p.expr2)


class WhileNode(ExprNode):
    def __init__(self, lineno, columnno, cond, body):
        super().__init__(lineno, columnno)
        self.cond = cond
        self.body = body

    @staticmethod
    def parse(p):
        return WhileNode(p.lineno, 0, p.expr0, p.expr1)


class BlockNode(ExprNode):
    def __init__(self, lineno, columnno, expr_list):
        super().__init__(lineno, columnno)
        self.expr_list = expr_list

    @staticmethod
    def parse(p):
        return BlockNode(p.lineno, 0, [p.expr0, *p.expr1])


class LetInNode(ExprNode):
    def __init__(self, lineno, columnno, decl_list, expr):
        super().__init__(lineno, columnno)
        self.decl_list: List[LetDeclNode] = decl_list
        self.expr = expr

    @staticmethod
    def parse(p):
        return LetInNode(p.lineno, 0, [p.let_decl0, *p.let_decl1], p.expr)


class CaseNode(ExprNode):
    def __init__(self, lineno, columnno, expr, case_branches):
        super().__init__(lineno, columnno)
        self.expr = expr
        self.case_branches = case_branches

    @staticmethod
    def parse(p):
        return CaseNode(p.lineno, 0, p.expr, [p.case0, * p.case1])


class NewNode(ExprNode):
    def __init__(self, lineno, columnno, type):
        super().__init__(lineno, columnno)
        self.type = type

    @staticmethod
    def parse(p):
        type = p.TYPE_ID
        return NewNode(p.lineno, 0, type)


class ParenthNode(ExprNode):
    def __init__(self, lineno, columnno, expr):
        super().__init__(lineno, columnno)
        self.expr = expr

    @staticmethod
    def parse(p):
        expr = p.expr
        return ParenthNode(p.lineno, 0, expr)


class BinaryExprNode(ExprNode):
    def __init__(self, lineno, columnno, left_expr, right_expr):
        super().__init__(lineno, columnno)

        self.left_expr = left_expr
        self.right_expr = right_expr
