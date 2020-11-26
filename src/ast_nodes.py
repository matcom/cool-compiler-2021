class Node:
    pass


class ProgramNode(Node):
    def __init__(self, declarations):
        self.declarations = declarations


class ExpressionNode(Node):
    pass


class ClassDeclarationNode:
    def __init__(self, idx, features, parent=None):
        self.id = idx
        self.parent = parent
        self.features = features


class FuncDeclarationNode:
    def __init__(self, idx, params, return_type, body):
        self.id = idx
        self.params = params
        self.type = return_type
        self.body = body


class AttrDeclarationNode:
    def __init__(self, idx, typex, init_exp=None):
        self.id = idx
        self.type = typex
        self.init_exp = init_exp


class AssignNode(ExpressionNode):
    def __init__(self, idx, expr):
        self.id = idx
        self.expr = expr


class LetNode(ExpressionNode):
    def __init__(self, identifiers, body):
        self.identifiers = identifiers
        self.body = body


class VarDeclarationNode:
    def __init__(self, idx, typex, expr=None):
        self.id = idx
        self.type = typex
        self.expr = expr


class IfNode(ExpressionNode):
    def __init__(self, if_exp, then_exp, else_exp):
        self.if_expr = if_exp
        self.then_expr = then_exp
        self.else_expr = else_exp


class WhileNode(ExpressionNode):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body


class CaseNode(ExpressionNode):
    def __init__(self, exp, case_items):
        self.expr = exp
        self.case_items = case_items


class CaseItemNode(ExpressionNode):
    def __init__(self, idx, typex, exp):
        self.id = idx
        self.type = typex
        self.expr = exp


class CallNode(ExpressionNode):
    def __init__(self, idx, args, obj=None, at_type=None):
        self.obj = obj
        self.id = idx
        self.args = args
        self.at_type = at_type


class BlockNode(ExpressionNode):
    def __init__(self, expression_list):
        self.expression_list = expression_list


class AtomicNode(ExpressionNode):
    def __init__(self, lex):
        self.lex = lex


class UnaryNode(ExpressionNode):
    def __init__(self, expr):
        self.expr = expr


class BinaryNode(ExpressionNode):
    def __init__(self, left, right):
        self.left = left
        self.right = right


class ArithmeticOperation(BinaryNode):
    pass


class ComparisonOperation(BinaryNode):
    pass


class ConstantNumNode(AtomicNode):
    pass


class VariableNode(AtomicNode):
    pass


class StringNode(AtomicNode):
    pass


class BooleanNode(AtomicNode):
    pass


class InstantiateNode(AtomicNode):
    pass


class NotNode(UnaryNode):
    pass


class IsvoidNode(UnaryNode):
    pass


class NegNode(UnaryNode):
    pass


class PlusNode(ArithmeticOperation):
    pass


class MinusNode(ArithmeticOperation):
    pass


class StarNode(ArithmeticOperation):
    pass


class DivNode(ArithmeticOperation):
    pass


class LessNode(ComparisonOperation):
    pass


class LessEqualNode(ComparisonOperation):
    pass


class EqualNode(ComparisonOperation):
    pass
