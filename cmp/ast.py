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
    def __init__(self, idx, typex, expr=None):
        self.id = idx
        self.type = typex
        self.expr = expr

class AssignNode(ExpressionNode):
    def __init__(self, idx, expr):
        self.id = idx
        self.expr = expr

class CallNode(ExpressionNode):
    def __init__(self, obj, idx, args, cast_type=None):
        self.obj = obj
        self.id = idx
        self.args = args
        self.type = cast_type

class CaseNode(ExpressionNode):
    def __init__(self, expr, branch_list):
        self.expr = expr
        self.branch_list = branch_list

class BlockNode(ExpressionNode):
    def __init__(self, expr_list):
        self.expr_list = expr_list

class LoopNode(ExpressionNode):
    def __init__(self, cond, body):
        self.condition = cond
        self.body = body

class ConditionalNode(ExpressionNode):
    def __init__(self, cond, then_body, else_body):
        self.condition = cond
        self.then_body = then_body
        self.else_body = else_body

class LetNode(ExpressionNode):
    def __init__(self, id_list, body):
        self.id_list = id_list
        self.body = body

class AtomicNode(ExpressionNode):
    def __init__(self, lex):
        self.lex = lex

class BinaryNode(ExpressionNode):
    def __init__(self, left, right):
        self.left = left
        self.right = right

class UnaryNode(ExpressionNode):
    def __init__(self, expr):
        self.expr = expr

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

class PlusNode(BinaryNode):
    pass

class MinusNode(BinaryNode):
    pass

class StarNode(BinaryNode):
    pass

class DivNode(BinaryNode):
    pass

class LeqNode(BinaryNode):
    pass

class LessNode(BinaryNode):
    pass

class EqualNode(BinaryNode):
    pass

class VoidNode(UnaryNode):
    pass

class NotNode(UnaryNode):
    pass

class NegNode(UnaryNode):
    pass