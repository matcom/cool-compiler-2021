class Node:
    pass


class ProgramNode(Node):
    def __init__(self, declarations):
        self.declarations = declarations


class DeclarationNode(Node):
    pass


class ExpressionNode(Node):
    pass


class ClassDeclarationNode(DeclarationNode):
    def __init__(self, idx, features, parent=None):
        self.id = idx
        self.parent = parent
        self.features = features


class FuncDeclarationNode(DeclarationNode):
    def __init__(self, idx, params, return_type, body):
        self.id = idx
        self.params = params
        self.type = return_type
        self.body = body


class AttrDeclarationNode(DeclarationNode):
    def __init__(self, idx, typex, val=None):
        self.id = idx
        self.type = typex
        self.val = val


class ConditionalNode(ExpressionNode):
    def __init__(self, if_expr, then_expr, else_expr):
        self.if_expr = if_expr
        self.then_expr = then_expr
        self.else_expr = else_expr


class LoopNode(ExpressionNode):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body


class BlockNode(ExpressionNode):
    def __init__(self, expr_list):
        self.expr_list = expr_list


class LetNode(ExpressionNode):
    def __init__(self, var_list, body):
        self.var_list = var_list
        self.body = body


class CaseNode(ExpressionNode):
    def __init__(self, expr, branch_list):
        self.expr = expr
        self.branch_list = branch_list


class AssignNode(ExpressionNode):
    def __init__(self, idx, expr):
        self.id = idx
        self.expr = expr


class CallNode(ExpressionNode):
    def __init__(self, obj, idx, args, ancestor_type=None):
        self.obj = obj
        self.id = idx
        self.args = args
        self.ancestor_type = ancestor_type


class NotNode(ExpressionNode):
    def __init__(self, expr):
        self.expr = expr


class IsVoidNode(ExpressionNode):
    def __init__(self, expr):
        self.expr = expr


class IntCompNode(ExpressionNode):
    def __init__(self, expr):
        self.expr = expr


class AtomicNode(ExpressionNode):
    def __init__(self, lex):
        self.lex = lex


class BinaryNode(ExpressionNode):
    def __init__(self, left, right):
        self.left = left
        self.right = right


class BooleanBinaryNode(BinaryNode):
    pass


class ArithBinaryNode(BinaryNode):
    pass


class ConstantNumNode(AtomicNode):
    pass


class StringNode(AtomicNode):
    pass


class VariableNode(AtomicNode):
    pass


class BoolNode(AtomicNode):
    pass


class InstantiateNode(AtomicNode):
    pass


class PlusNode(ArithBinaryNode):
    pass


class MinusNode(ArithBinaryNode):
    pass


class StarNode(ArithBinaryNode):
    pass


class DivNode(ArithBinaryNode):
    pass


class LessNode(BooleanBinaryNode):
    pass


class LessEqualNode(BooleanBinaryNode):
    pass


class EqualNode(BooleanBinaryNode):
    pass
