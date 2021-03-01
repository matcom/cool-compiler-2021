# Clases necesarias para representar el AST del programa COOL
class Node:
    pass

# Raiz del AST
class ProgramNode(Node):
    def __init__(self, declarations):
        self.declarations = declarations
        self.line = declarations[0].line
        self.column = declarations[0].column


class DeclarationNode(Node):
    pass


class ClassDeclarationNode(DeclarationNode):
    def __init__(self, classx, idx, features, parent=None):
        self.id = idx
        self.parent = parent
        self.features = features
        self.line = classx.line
        self.column = classx.column


class AttrDeclarationNode(DeclarationNode):
    def __init__(self, idx, typex, expression=None):
        self.id = idx
        self.type = typex
        self.expression = expression
        self.line = idx.line
        self.column = idx.column


class FuncDeclarationNode(DeclarationNode):
    def __init__(self, idx, params, return_type, body):
        self.id = idx
        self.params = params
        self.type = return_type
        self.body = body
        self.line = idx.line
        self.column = idx.column


class ExpressionNode(Node):
    pass


class IfThenElseNode(ExpressionNode):
    def __init__(self, ifx, condition, if_body, else_body):
        self.condition = condition
        self.if_body = if_body
        self.else_body = else_body
        self.line = ifx.line
        self.column = ifx.column


class WhileLoopNode(ExpressionNode):
    def __init__(self, whilex, condition, body):
        self.condition = condition
        self.body = body
        self.line = whilex.line
        self.column = whilex.column


class BlockNode(ExpressionNode):
    def __init__(self, brace, expressions):
        self.expressions = expressions
        self.line = brace.line
        self.column = brace.column


class LetInNode(ExpressionNode):
    def __init__(self, let, let_body, in_body):
        self.let_body = let_body
        self.in_body = in_body
        self.line = let.line
        self.column = let.column


class CaseOfNode(ExpressionNode):
    def __init__(self, case, expression, branches):
        self.expression = expression
        self.branches = branches
        self.line = case.line
        self.column = case.column


class AssignNode(ExpressionNode):
    def __init__(self, idx, expression):
        self.id = idx
        self.expression = expression
        self.line = idx.line
        self.column = idx.column


class UnaryNode(ExpressionNode):
    def __init__(self, expression):
        self.expression = expression
        self.line = expression.line
        self.column = expression.column


class NotNode(UnaryNode):
    def __init__(self, notx, expression):
        super().__init__(expression)
        self.line = notx.line
        self.column = notx.column


class BinaryNode(ExpressionNode):
    def __init__(self, left, operator, right):
        self.left = left
        self.right = right
        self.line = operator.line
        self.column = operator.column


class LessEqualNode(BinaryNode):
    pass


class LessNode(BinaryNode):
    pass


class EqualNode(BinaryNode):
    pass


class ArithmeticNode(BinaryNode):
    pass


class PlusNode(ArithmeticNode):
    pass


class MinusNode(ArithmeticNode):
    pass


class StarNode(ArithmeticNode):
    pass


class DivNode(ArithmeticNode):
    pass


class IsVoidNode(UnaryNode):
    def __init__(self, isvoid, expression):
        super().__init__(expression)
        self.line = isvoid.line
        self.column = isvoid.column


class ComplementNode(UnaryNode):
    def __init__(self, complement, expression):
        super().__init__(expression)
        self.line = complement.line
        self.column = complement.column


class FunctionCallNode(ExpressionNode):
    def __init__(self, obj, idx, args, typex=None):
        self.obj = obj
        self.id = idx
        self.args = args
        self.type = typex
        self.line = obj.line
        self.column = obj.column


class MemberCallNode(ExpressionNode):
    def __init__(self, idx, args):
        self.id = idx
        self.args = args
        self.line = idx.line
        self.column = idx.column


class NewNode(ExpressionNode):
    def __init__(self, new, typex):
        self.type = typex
        self.line = new.line
        self.column = new.column


class AtomicNode(ExpressionNode):
    def __init__(self, token):
        self.token = token
        self.line = token.line
        self.column = token.column


class IntegerNode(AtomicNode):
    pass


class IdNode(AtomicNode):
    pass


class StringNode(AtomicNode):
    pass


class BoolNode(AtomicNode):
    pass
