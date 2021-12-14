class ast_nodes:

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

    class MethDeclarationNode(DeclarationNode):
        def __init__(self, idx, params, return_type, body):
            self.id = idx
            self.params = params
            self.type = return_type
            self.body = body

    class AttrDeclarationNode(DeclarationNode):
        def __init__(self, idx, typex, expr = None):
            self.id = idx
            self.type = typex
            self.expr = expr

    class AssignNode(ExpressionNode):
        def __init__(self, idx, expr):
            self.id = idx
            self.expr = expr

    class CallNode(ExpressionNode):
        def __init__(self, idx, args, obj = None, typex = None):
            self.obj = obj
            self.type = typex
            self.id = idx
            self.args = args
    
    class IfThenElseNode(ExpressionNode):
        def __init__(self, if_expr, then_expr, else_expr):
            self.if_expr = if_expr
            self.then_expr = then_expr
            self.else_expr = else_expr
    
    class WhileNode(ExpressionNode):
        def __init__(self, conditional_expr, loop_expr):
            self.conditional_expr = conditional_expr
            self.loop_expr = loop_expr

    class BlockNode(ExpressionNode):
        def __init__(self, expr_list):
            self.expr_list = expr_list
    
    class LetNode(ExpressionNode):
        def __init__(self, identifiers, in_expr):
            self.identifiers = identifiers
            self.in_expr = in_expr

    class CaseNode(ExpressionNode):
        def __init__(self, predicate, branches):
            self.predicate = predicate
            self.branches = branches
    
    class NotNode(ExpressionNode):
        def __init__(self, expr):
            self.expr = expr

    class AtomicNode(ExpressionNode):
        def __init__(self, lex):
            self.lex = lex

    class BinaryNode(ExpressionNode):
        def __init__(self, left, right):
            self.left = left
            self.right = right


    class ConstantNumNode(AtomicNode):
        pass
    class ConstantBoolNode(AtomicNode):
        pass
    class ConstantStringNode(AtomicNode):
        pass
    class VariableNode(AtomicNode):
        pass
    class InstantiateNode(AtomicNode):
        pass
    class IsVoidNode(AtomicNode):
        pass
    class ComplementNode(AtomicNode):
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