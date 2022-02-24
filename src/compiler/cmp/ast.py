from .utils import emptyToken


class Node:
    def __init__(self, token):
        self.token = token


class ProgramNode(Node):
    def __init__(self, declarations):
        super().__init__(emptyToken)
        self.declarations = declarations


class DeclarationNode(Node):
    pass


class ExpressionNode(Node):
    pass


class ClassDeclarationNode(DeclarationNode):
    def __init__(self, idx, features, token, parent=None):
        self.id = idx
        self.token = token
        self.parent = parent
        self.features = features


class FuncDeclarationNode(DeclarationNode):
    def __init__(self, token, params, return_type, body):
        self.id = token.lex
        # param = (name, type)
        self.params = params
        self.type = return_type
        self.body = body
        self.token = token


class AttrDeclarationNode(DeclarationNode):
    def __init__(self, idx, typex, expr=None, token=emptyToken):
        self.id = idx
        self.type = typex
        self.expr = expr
        self.token = token


class AssignNode(ExpressionNode):
    def __init__(self, idx, expr, token):
        self.id = idx
        self.expr = expr
        self.token = token


class CallNode(ExpressionNode):
    def __init__(self, obj, token, args, cast_type=emptyToken):
        self.obj = obj
        self.id = token.lex
        self.args = args
        self.type = cast_type.lex
        self.token = token
        self.typeToken = cast_type


class CaseNode(ExpressionNode):
    def __init__(self, expr, branch_list, token):
        self.expr = expr
        # [(id, type, expr), ...]
        self.branch_list = branch_list
        self.token = token


class BlockNode(ExpressionNode):
    def __init__(self, expr_list, token):
        self.expr_list = expr_list
        self.token = token


class LoopNode(ExpressionNode):
    def __init__(self, cond, body, token):
        self.condition = cond
        self.body = body
        self.token = token


class ConditionalNode(ExpressionNode):
    def __init__(self, cond, then_body, else_body, token):
        self.condition = cond
        self.then_body = then_body
        self.else_body = else_body
        self.token = token


class LetNode(ExpressionNode):
    def __init__(self, id_list, body, token):
        # [(id, type, expr), ...]
        self.id_list = id_list
        self.body = body
        self.token = token


class AtomicNode(ExpressionNode):
    def __init__(self, token):
        self.lex = token.lex
        self.token = token


class UnaryNode(ExpressionNode):
    def __init__(self, expr, symbol):
        self.expr = expr
        self.token = symbol


class BinaryNode(ExpressionNode):
    def __init__(self, left, right, symbol):
        self.left = left
        self.right = right
        self.token = symbol


class ArithmeticNode(BinaryNode):
    pass


class ComparisonNode(BinaryNode):
    pass


class ConstantNumNode(AtomicNode):
    pass


class ConstantStringNode(AtomicNode):
    pass


class ConstantBoolNode(AtomicNode):
    pass


class VariableNode(AtomicNode):
    pass


class InstantiateNode(AtomicNode):
    pass


class PlusNode(ArithmeticNode):
    pass


class MinusNode(ArithmeticNode):
    pass


class StarNode(ArithmeticNode):
    pass


class DivNode(ArithmeticNode):
    pass


class LeqNode(ComparisonNode):
    pass


class LessNode(ComparisonNode):
    pass


class EqualNode(BinaryNode):
    pass


class VoidNode(UnaryNode):
    pass


class NotNode(UnaryNode):
    pass


class NegNode(UnaryNode):
    pass
