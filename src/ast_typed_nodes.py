from cmp.semantic import Context


class Node:
    pass


class ProgramNode(Node):
    def __init__(self, declarations, context=None):
        self.declarations = declarations
        self.context = context


class ExpressionNode(Node):
    def __init__(self, etype):
        self.static_type = etype


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
    def __init__(self, idx, expr, etype = None ):
        self.id = idx
        self.expr = expr
        self.static_type = etype


class LetNode(ExpressionNode):
    def __init__(self, identifiers, body, etype = None ):
        self.identifiers = identifiers
        self.body = body
        self.static_type = etype


class VarDeclarationNode:
    def __init__(self, idx, typex, expr=None, etype = None ):
        self.id = idx
        self.type = typex
        self.expr = expr
        self.static_type = etype


class IfNode(ExpressionNode):
    def __init__(self, if_exp, then_exp, else_exp, etype = None ):
        self.if_expr = if_exp
        self.then_expr = then_exp
        self.else_expr = else_exp
        self.static_type = etype


class WhileNode(ExpressionNode):
    def __init__(self, condition, body, etype = None ):
        self.condition = condition
        self.body = body
        self.static_type = etype


class CaseNode(ExpressionNode):
    def __init__(self, exp, case_items, etype = None ):
        self.expr = exp
        self.case_items = case_items
        self.static_type = etype


class CaseItemNode(ExpressionNode):
    def __init__(self, idx, typex, exp, etype = None ):
        self.id = idx
        self.type = typex
        self.expr = exp
        self.static_type = etype


class CallNode(ExpressionNode):
    def __init__(self, idx, args, obj=None, at_type=None, obj_type = None, etype = None):
        self.obj = obj
        self.id = idx
        self.args = args
        self.at_type = at_type
        self.obj_type = obj_type 
        self.static_type = etype

class BlockNode(ExpressionNode):
    def __init__(self, expression_list, etype = None ):
        self.expression_list = expression_list
        self.static_type = etype


class AtomicNode(ExpressionNode):
    def __init__(self, lex, etype = None ):
        self.lex = lex
        self.static_type = etype


class UnaryNode(ExpressionNode):
    def __init__(self, expr, etype = None ):
        self.expr = expr
        self.static_type = etype


class BinaryNode(ExpressionNode):
    def __init__(self, left, right, etype = None ):
        self.left = left
        self.right = right
        self.static_type = etype


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


class DefaultValueNode(ExpressionNode):
    def __init__(self, typex):
        self.type = typex