#region Root
class Node:
    pass
#endregion 

#region Node
class ProgramNode(Node):
    def __init__(self, class_list):
        self.class_list = class_list

class DeclarationNode(Node):
    pass

class ExpressionNode(Node):
    pass
#endregion

#region DeclarationNode
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
#endregion

#region ExpressionNode
class AssignmentNode(ExpressionNode):
    def __init__(self, identifier, expression, keyword):
        self.id = identifier
        self.expression = expression
        self.keyword = keyword

class DispatchNode(ExpressionNode):
    def __init__(self, identifier, argument_list, expression=None, ttype=None):
        self.type = ttype
        self.id = identifier
        self.expression = expression
        self.argument_list = argument_list

class ConditionalNode(ExpressionNode):
    def __init__(self, predicate, then_branch, else_branch, keyword):
        self.predicate = predicate
        self.then_branch = then_branch
        self.else_branch = else_branch
        self.keyword = keyword

class LoopsNode(ExpressionNode):
    def __init__(self, predicate, expression, keyword):
        self.predicate = predicate
        self.expression = expression
        self.keyword = keyword

class BlockNode(ExpressionNode):
    def __init__(self, expression_list, keyword):
        self.expression_list = expression_list
        self.keyword = keyword

class LetNode(ExpressionNode):
    def __init__(self, assignment_list, expression, keyword):
        self.expression = expression
        self.assignment_list = assignment_list
        self.keyword = keyword

class CaseNode(ExpressionNode):
    def __init__(self, expression, test_list, keyword):
        self.expression = expression
        self.test_list = test_list
        self.keyword = keyword

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
#endregion

#region AtomicNode
class IdentifierNode(AtomicNode):
    pass

class TypeNode(AtomicNode):
    pass

class ConstantNode(AtomicNode):
    pass
#endregion

#region UnaryNode
class ComplementNode(UnaryNode):
    pass

class NegationNode(UnaryNode):
    pass
#endregion

#region BinaryNode
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
#endregion

#region ConstantNode
class IntegerNode(ConstantNode):
    pass

class StringNode(ConstantNode):
    pass

class BoolNode(ConstantNode):
    pass
#endregion