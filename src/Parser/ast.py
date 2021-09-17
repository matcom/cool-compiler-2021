class Node:
    pass

class ProgramNode(Node):
    def __init__(self, class_list):
        self.class_list = class_list

class DeclarationNode(Node):
    pass

class ExpressionNode(Node):
    pass

class ClassNode(DeclarationNode):
    def __init__(self, type, feature_list, parent=None):
        self.type = type
        self.parent = parent
        self.feature_list = feature_list

class MethodNode(DeclarationNode):
    def __init__(self, id, params, type, expr):
        self.id = id
        self.expr = expr
        self.type = type
        self.params = params

class AttributeNode(DeclarationNode):
    def __init__(self, id, type, expr=None):
        self.id = id
        self.type = type
        self.expr = expr

class AssignmentNode(ExpressionNode):
    def __init__(self, id, expr, key):
        self.id = id
        self.key = key
        self.exp = expr

class DispatchNode(ExpressionNode):
    def __init__(self, id, args, expr=None, type=None):
        self.id = id
        self.type = type
        self.expr = expr
        self.args = args

class ConditionalNode(ExpressionNode):
    def __init__(self, pred, then, neth, key):
        self.key = key
        self.pred = pred
        self.then = then
        self.neth = neth

class LoopsNode(ExpressionNode):
    def __init__(self, pred, expr, key):
        self.key = key
        self.pred = pred
        self.expr = expr

class BlockNode(ExpressionNode):
    def __init__(self, exprs, key):
        self.key = key
        self.exprs = exprs

class LetNode(ExpressionNode):
    def __init__(self, assigs, expr, key):
        self.key = key
        self.expr = expr
        self.assigs = assigs

class CaseNode(ExpressionNode):
    def __init__(self, expr, tests, key):
        self.key = key
        self.expr = expr
        self.tests = tests

class NewNode(ExpressionNode):
    def __init__(self, ttype, keyword):
        self.type = ttype
        self.keyword = keyword

class IsvoidNode(ExpressionNode):
    def __init__(self, expression, keyword):
        self.expression = expression
        self.keyword = keyword

class AtomicNode(ExpressionNode):
    def __init__(self, lexer):
        self.lexer = lexer

class UnaryNode(ExpressionNode):
    def __init__(self, node):
        self.node = node

class BinaryNode(ExpressionNode):
    def __init__(self, left, right, keyword):
        self.left = left
        self.right = right
        self.keyword = keyword

class IdentifierNode(AtomicNode):
    pass

class TypeNode(AtomicNode):
    pass

class ConstantNode(AtomicNode):
    pass

class ComplementNode(UnaryNode):
    pass

class NegationNode(UnaryNode):
    pass

class PlusNode(BinaryNode):
    pass

class MinusNode(BinaryNode):
    pass

class StarNode(BinaryNode):
    pass

class DivideNode(BinaryNode):
    pass

class LessNode(BinaryNode):
    pass

class LequalNode(BinaryNode):
    pass

class EqualNode(BinaryNode):
    pass

class IntegerNode(ConstantNode):
    pass

class StringNode(ConstantNode):
    pass

class BoolNode(ConstantNode):
    pass