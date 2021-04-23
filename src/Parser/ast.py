#Root
class Node:
    pass

#Node
class ProgramNode(Node):
    def __init__(self, class_list):
        self.class_list = class_list

class DeclarationNode(Node):
    pass
class ExpressionNode(Node):
    pass

#DeclarationNode
class ClassNode(DeclarationNode):
    def __init__(self, ttype, feature_list, parent=None):
        self.type = ttype
        self.parent = parent
        self.feature_list = feature_list

class MethodNode(DeclarationNode):
    def __init__(self, identifier, parameter_list, ttype, expression):
        self.type = ttype
        self.id = identifier
        self.expression = expression
        self.parameter_list = parameter_list

class AttributeNode(DeclarationNode):
    def __init__(self, identifier, ttype, expression=None):
        self.type = ttype
        self.id = identifier
        self.expression = expression

#ExpressionNode
class AssignmentNode(ExpressionNode):
    def __init__(self, identifier, expression):
        self.id = identifier
        self.expression = expression

class Dispatch(ExpressionNode):
    def __init__(self, identifier, expression_list, expression=None, ttype=None):
        self.type = ttype
        self.id = identifier
        self.expression = expression
        self.expression_list = expression_list

class ConditionalNode(ExpressionNode):
    def __init__(self, predicate, then_branch, else_branch):
        self.predicate = predicate
        self.then_branch = then_branch
        self.else_branch = else_branch

class LoopsNode(ExpressionNode):
    def __init__(self, predicate, expression):
        self.predicate = predicate
        self.expression = expression

class BlockNode(ExpressionNode):
    def __init__(self, expression_list):
        self.expression_list = expression_list

class LetNode(ExpressionNode):
    def __init__(self, assignment_list, expression):
        self.expression = expression
        self.assignment_list = assignment_list

class CaseNode(ExpressionNode):
    def __init__(self, expresion, test_list):
        self.expresion = expresion
        self.test_list = test_list

class NewNode(ExpressionNode):
    def __init__(self, ttype):
        self.type = ttype

class VoidNode(ExpressionNode):
    def __init__(self, expression):
        self.expression = expression

class AtomicNode(ExpressionNode):
    def __init__(self, lexer):
        self.lexer = lexer

class UnaryNode(ExpressionNode):
    def __init__(self, node):
        self.node = node

class BinaryNode(ExpressionNode):
    def __init__(self, left, right):
        self.left = left
        self.right = right

#AtomicNode
class IdentifierNode(AtomicNode):
    pass
class TypeNode(AtomicNode):
    pass
class ConstantNode(AtomicNode):
    pass

#UnaryNode
class ComplementNode(UnaryNode):
    pass
class NegationNode(UnaryNode):
    pass

#BinaryNode
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

#ConstantNode
class IntegerNode(ConstantNode):
    pass
class StringNode(ConstantNode):
    pass
class BoolNode(ConstantNode):
    pass