from utils.COOL_Lexer import Token


class ast_nodes:

    class Node:
        line = 0
        column = 0


    class ProgramNode(Node):
        def __init__(self, declarations):
            self.declarations = declarations

    class DeclarationNode(Node):
        pass
    class ExpressionNode(Node):
        pass


    class ClassDeclarationNode(DeclarationNode):
        def __init__(self, token, features, parent=None):
            self.id = token.lex
            self.line = token.line
            self.column = token.column
            self.parent = parent
            self.features = features

    class MethDeclarationNode(DeclarationNode):
        def __init__(self, token, params, return_type, body):
            self.id = token.lex
            self.line = token.line
            self.column = token.column
            self.params = params
            self.type = return_type
            self.body = body

    class AttrDeclarationNode(DeclarationNode):
        def __init__(self, token, typex, expr = None):
            self.id = token.lex
            self.line = token.line
            self.column = token.column
            self.type = typex
            self.expr = expr

    class AssignNode(ExpressionNode):
        def __init__(self, token, expr, token_pos):
            self.id = token.lex
            self.line = token_pos.line
            self.column = token_pos.column
            self.expr = expr

    class CallNode(ExpressionNode):
        def __init__(self, token, args, obj = None, typex = None):
            self.obj = obj.lex
            self.type = typex
            self.id = token.lex
            self.line = token.line
            self.column = token.column
            self.args = args
    
    class IfThenElseNode(ExpressionNode):
        def __init__(self, if_expr, then_expr, else_expr,token):
            self.if_expr = if_expr
            self.then_expr = then_expr
            self.else_expr = else_expr
            self.line = token.line
            self.column = token.column
    
    class WhileNode(ExpressionNode):
        def __init__(self, conditional_expr, loop_expr, token):
            self.conditional_expr = conditional_expr
            self.loop_expr = loop_expr
            self.line = token.line
            self.column = token.column

    class BlockNode(ExpressionNode):
        def __init__(self, expr_list, token):
            self.expr_list = expr_list
            self.line = token.line
            self.column = token.column
    
    class LetNode(ExpressionNode):
        def __init__(self, identifiers, in_expr, token):
            self.identifiers = [tuple([item.lex if isinstance(item, Token) else item for item in _list]) for _list in identifiers]
            self.in_expr = in_expr
            self.line = token.line
            self.column = token.column

    class CaseNode(ExpressionNode):
        def __init__(self, predicate, branches, token):
            self.predicate = predicate
            self.branches = [tuple([item.lex if isinstance(item, Token) else item for item in _list]) for _list in branches]
            self.line = token.line
            self.column = token.column
    
    class NotNode(ExpressionNode):
        def __init__(self, expr, token):
            self.expr = expr
            self.line = token.line
            self.column = token.column

    class AtomicNode(ExpressionNode):
        def __init__(self, token):
            self.lex = token.lex
            self.line = token.line
            self.column = token.column

    class BinaryNode(ExpressionNode):
        def __init__(self, left, right, token):
            self.left = left
            self.right = right
            self.line = token.line
            self.column = token.column 


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