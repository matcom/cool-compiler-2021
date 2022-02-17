"""
Cool AST.
"""
from __future__ import annotations


class Node:
    def __init__(self):
        self.line = 0
        self.col = 0

    def set_pos(self, line, col) -> None:
        self.line = line
        self.col = col

    @property
    def pos(self) -> tuple[int, int]:
        return self.line, self.col


class ProgramNode(Node):
    def __init__(self, declarations: list[DeclarationNode]):
        super().__init__()

        self.declarations = declarations


class DeclarationNode(Node):
    id: str


class ExpressionNode(Node):
    pass


class ClassDeclarationNode(DeclarationNode):
    def __init__(self,
                 idx: str,
                 features: list[FuncDeclarationNode | AttrDeclarationNode],
                 parent: str = None):
        super().__init__()

        self.id = idx
        self.parent = parent
        self.features = features

        self.parent_pos = (-1, -1)


class ParamNode(DeclarationNode):
    def __init__(self, idx: str, typex: str):
        super().__init__()

        self.id = idx
        self.type = typex

        self.type_pos = (-1, -1)


class FuncDeclarationNode(DeclarationNode):
    def __init__(self, idx: str, params: list[ParamNode], return_type: str, body):
        super().__init__()

        self.id = idx
        self.params = params
        self.return_type = return_type
        self.body = body

        self.type_pos = (-1, -1)


class AttrDeclarationNode(DeclarationNode):
    def __init__(self, idx: str, typex: str, expr: ExpressionNode = None):
        super().__init__()

        self.id = idx
        self.type = typex
        self.expr = expr

        self.type_pos = (-1, -1)
        self.expr_pos = (-1, -1)


class LetDeclarationNode(DeclarationNode):
    def __init__(self, idx: str, typex: str, expr: ExpressionNode = None):
        super().__init__()

        self.id = idx
        self.type = typex
        self.expr = expr

        self.type_pos = (-1, -1)
        self.expr_pos = (-1, -1)


class ParenthesisExpr(ExpressionNode):
    def __init__(self, expr: ExpressionNode):
        super().__init__()

        self.expr = expr


class BlockNode(ExpressionNode):
    def __init__(self, expressions: list[ExpressionNode]):
        super().__init__()

        self.expressions = expressions


class LetNode(ExpressionNode):
    def __init__(self, declarations: list[LetDeclarationNode], expr: ExpressionNode):
        super().__init__()

        self.declarations = declarations
        self.expr = expr


class CaseBranchNode(DeclarationNode):
    def __init__(self, id_: str, type_: str, expr: ExpressionNode):
        super().__init__()

        self.id = id_
        self.type = type_
        self.expr = expr

        self.type_pos = (-1, -1)


class CaseNode(ExpressionNode):
    def __init__(self, expr: ExpressionNode, cases: list[CaseBranchNode]):
        super().__init__()

        self.expr = expr
        self.cases = cases


class AssignNode(ExpressionNode):
    def __init__(self, idx: str, expr: ExpressionNode):
        super().__init__()

        self.id = idx
        self.expr = expr


class ConditionalNode(ExpressionNode):
    def __init__(self, ifx: ExpressionNode, then: ExpressionNode, elsex: ExpressionNode):
        super().__init__()

        self.if_expr = ifx
        self.then_expr = then
        self.else_expr = elsex


class WhileNode(ExpressionNode):
    def __init__(self, condition: ExpressionNode, body: ExpressionNode):
        super().__init__()

        self.condition = condition
        self.body = body


class CallNode(ExpressionNode):
    def __init__(self, idx: str, args, obj: ExpressionNode = None, typex: str = None):
        super().__init__()

        self.obj = obj
        self.id = idx
        self.args = args
        self.type = typex

        self.parent_pos = (-1, -1)


class AtomicNode(ExpressionNode):
    def __init__(self, lex: str):
        super().__init__()

        self.lex = lex


class BinaryNode(ExpressionNode):
    def __init__(self, left: ExpressionNode, operation: str, right: ExpressionNode):
        super().__init__()

        self.left = left
        self.operation = operation
        self.right = right


class UnaryNode(ExpressionNode):
    def __init__(self, expr: ExpressionNode):
        super().__init__()

        self.expr = expr


class VariableNode(AtomicNode):
    pass


class InstantiateNode(AtomicNode):
    pass


class IntegerNode(AtomicNode):
    pass


class StringNode(AtomicNode):
    pass


class BooleanNode(AtomicNode):
    pass


class PlusNode(BinaryNode):
    pass


class MinusNode(BinaryNode):
    pass


class StarNode(BinaryNode):
    pass


class DivNode(BinaryNode):
    pass


class LessThanNode(BinaryNode):
    pass


class LessEqualNode(BinaryNode):
    pass


class EqualNode(BinaryNode):
    pass


class IsVoidNode(UnaryNode):
    pass


class NegationNode(UnaryNode):
    pass


class ComplementNode(UnaryNode):
    pass
