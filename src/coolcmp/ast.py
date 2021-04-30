"""
Cool AST.
"""


class Node:
    def __init__(self):
        self.line = 0
        self.col = 0

    def set_pos(self, line, col):
        self.line = line
        self.col = col


class ProgramNode(Node):
    def __init__(self, declarations):
        super().__init__()

        self.declarations = declarations


class DeclarationNode(Node):
    pass


class ExpressionNode(Node):
    pass


class ClassDeclarationNode(DeclarationNode):
    def __init__(self, idx, features, parent=None):
        super().__init__()

        self.id = idx
        self.parent = parent
        self.features = features


class FuncDeclarationNode(DeclarationNode):
    def __init__(self, idx, params, return_type, body):
        super().__init__()

        self.id = idx
        self.params = params
        self.return_type = return_type
        self.body = body


class AttrDeclarationNode(DeclarationNode):
    def __init__(self, idx, typex, expr=None):
        super().__init__()

        self.id = idx
        self.type = typex
        self.expr = expr


class LetDeclarationNode(DeclarationNode):
    def __init__(self, idx, typex, expr=None):
        super().__init__()

        self.id = idx
        self.type = typex
        self.expr = expr


class ParamNode(DeclarationNode):
    def __init__(self, idx, typex):
        super().__init__()

        self.id = idx
        self.type = typex


class ParenthesisExpr(ExpressionNode):
    def __init__(self, expr):
        super().__init__()

        self.expr = expr


class BlockNode(ExpressionNode):
    def __init__(self, expressions):
        super().__init__()

        self.expressions = expressions


class LetNode(ExpressionNode):
    def __init__(self, declarations, expr):
        super().__init__()

        self.declarations = declarations
        self.expr = expr


class CaseNode(ExpressionNode):
    def __init__(self, expr, cases):
        super().__init__()

        self.expr = expr
        self.cases = cases


class AssignNode(ExpressionNode):
    def __init__(self, idx, expr):
        super().__init__()

        self.id = idx
        self.expr = expr


class ConditionalNode(ExpressionNode):
    def __init__(self, ifx, then, elsex):
        super().__init__()

        self.if_expr = ifx
        self.then_expr = then
        self.else_expr = elsex


class WhileNode(ExpressionNode):
    def __init__(self, condition, body):
        super().__init__()

        self.condition = condition
        self.body = body


class CallNode(ExpressionNode):
    def __init__(self, idx, args, obj=None, typex=None):
        super().__init__()

        self.obj = obj
        self.id = idx
        self.args = args
        self.type = typex


class AtomicNode(ExpressionNode):
    def __init__(self, lex):
        super().__init__()

        self.lex = lex


class BinaryNode(ExpressionNode):
    def __init__(self, left, operation, right):
        super().__init__()

        self.left = left
        self.operation = operation
        self.right = right


class UnaryNode(ExpressionNode):
    def __init__(self, expr):
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
