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
        def __init__(self, idx, features, token, parent=None):
            self.id = idx.lex
            self.line = idx.line
            self.column = idx.column
            self.classt_line = token.line
            self.classt_column = token.column + 4
            self.parent = parent.lex if parent else parent
            self.parent_column = parent.column if parent else None
            self.features = features

    class MethDeclarationNode(DeclarationNode):
        def __init__(self, idx, params, return_type, body, ocurToken):
            self.id = idx.lex
            self.line = idx.line
            self.column = idx.column
            self.body_line = ocurToken.next_token.line
            self.body_column = ocurToken.next_token.column
            self.params = [[item.lex if isinstance(
                item, Token) else item for item in _list] for _list in params]
            self.type = return_type.lex
            self.body = body

    class AttrDeclarationNode(DeclarationNode):
        def __init__(self, idx, typex, arrowToken=None, expr=None):
            self.id = idx.lex
            self.line = arrowToken.next_token.line if expr else typex.line
            self.column = arrowToken.next_token.column if expr else typex.column
            self.type = typex.lex
            self.expr = expr

    class AssignNode(ExpressionNode):
        def __init__(self, token, expr, token_pos):
            self.id = token.lex
            self.line = token_pos.line
            self.column = token_pos.column
            self.expr = expr

    class CallNode(ExpressionNode):
        def __init__(self, token, args, obj=None, typex=None):
            self.obj = obj.lex if isinstance(obj, Token) else obj
            self.type = typex.lex if typex else typex
            self.id = token.lex
            self.line = obj.line if obj else token.line
            self.column = obj.column if obj else token.column
            self.args = args

    class IfThenElseNode(ExpressionNode):
        def __init__(self, if_expr, then_expr, else_expr, token):
            self.if_expr = if_expr
            self.then_expr = then_expr
            self.else_expr = else_expr
            self.line = token.next_token.line
            self.column = token.next_token.column

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
            self.identifiers = [tuple([item.lex if isinstance(
                item, Token) else item for item in _list]) for _list in identifiers]
            self.in_expr = in_expr
            self.line = token.line
            self.column = token.column

    class CaseNode(ExpressionNode):
        def __init__(self, predicate, branches, token):
            self.predicate = predicate
            self.branches = []
            self.branchesPos = []
            for branch in branches:
                self.branches.append(
                    tuple([item.lex if isinstance(item, Token) else item for item in branch]))
                _, typex, _ = branch
                self.branchesPos.append((typex.line, typex.column))
            self.line = token.line
            self.column = token.column

    class NotNode(ExpressionNode):
        def __init__(self, expr, token):
            self.expr = expr
            self.line = token.next_token.line
            self.column = token.next_token.column

    class AtomicNode(ExpressionNode):
        def __init__(self, expr):
            self.lex = expr.lex if isinstance(expr, Token) else expr
            self.line = expr.line
            self.column = expr.column

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
        def __init__(self, expr):
            expr.lex = expr.lex[1:-1]
            super().__init__(expr)

    class VariableNode(AtomicNode):
        pass

    class InstantiateNode(AtomicNode):
        def __init__(self, typex, token):
            self.lex = typex.lex
            self.line = token.next_token.line
            self.column = token.next_token.column

    class IsVoidNode(AtomicNode):
        pass

    class ComplementNode(AtomicNode):
        def __init__(self, expr, token):
            self.lex = expr.lex if isinstance(expr, Token) else expr
            self.line = token.next_token.line
            self.column = token.next_token.column

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
