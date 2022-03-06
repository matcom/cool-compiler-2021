class Node:
    def __init__(self, line_no: int, col_no: int):
        self.line_no = line_no
        self.col_no = col_no
        self.computed_type = None


class ProgramNode(Node):
    def __init__(self, line_no, col_no, declarations):
        super().__init__(line_no, col_no)
        self.declarations = declarations


class DeclarationNode(Node):
    pass


class ExpressionNode(Node):
    pass


class ClassDeclarationNode(DeclarationNode):
    def __init__(self, line_no, col_no, idx, features, parent=None):
        super().__init__(line_no, col_no)
        self.id = idx
        self.parent = parent
        self.features = features


class FuncDeclarationNode(DeclarationNode):
    def __init__(self, line_no, col_no, idx, params, return_type, body):
        super().__init__(line_no, col_no)
        self.id = idx
        self.params = params
        self.type = return_type
        self.body = body


class AttrDeclarationNode(DeclarationNode):
    def __init__(self, line_no, col_no, idx, typex, val=None):
        super().__init__(line_no, col_no)
        self.id = idx
        self.type = typex
        self.val = val


class ConditionalNode(ExpressionNode):
    def __init__(self, line_no, col_no, if_expr, then_expr, else_expr):
        super().__init__(line_no, col_no)
        self.if_expr = if_expr
        self.then_expr = then_expr
        self.else_expr = else_expr


class LoopNode(ExpressionNode):
    def __init__(self, line_no, col_no, condition, body):
        super().__init__(line_no, col_no)
        self.condition = condition
        self.body = body


class BlockNode(ExpressionNode):
    def __init__(self, line_no, col_no, expr_list):
        super().__init__(line_no, col_no)
        self.expr_list = expr_list


class LetNode(ExpressionNode):
    def __init__(self, line_no, col_no, var_list, body):
        super().__init__(line_no, col_no)
        self.var_list = var_list
        self.body = body


class CaseNode(ExpressionNode):
    def __init__(self, line_no, col_no, expr, branch_list):
        super().__init__(line_no, col_no)
        self.expr = expr
        self.branch_list = branch_list


class BranchNode(Node):
    def __init__(self, line_no, col_no, _id, _type, action):
        super().__init__(line_no, col_no)
        self.id = _id
        self.type = _type
        self.action = action


class AssignNode(ExpressionNode):
    def __init__(self, line_no, col_no, idx, expr):
        super().__init__(line_no, col_no)
        self.id = idx
        self.expr = expr


class CallNode(ExpressionNode):
    def __init__(self, line_no, col_no, obj, idx, args, ancestor_type=None):
        super().__init__(line_no, col_no)
        self.obj = obj
        self.id = idx
        self.args = args
        self.ancestor_type = ancestor_type


class NotNode(ExpressionNode):
    def __init__(self, line_no, col_no, expr):
        super().__init__(line_no, col_no)
        self.expr = expr


class IsVoidNode(ExpressionNode):
    def __init__(self, line_no, col_no, expr):
        super().__init__(line_no, col_no)
        self.expr = expr


class IntCompNode(ExpressionNode):
    def __init__(self, line_no, col_no, expr):
        super().__init__(line_no, col_no)
        self.expr = expr


class AtomicNode(ExpressionNode):
    def __init__(self, line_no, col_no, lex):
        super().__init__(line_no, col_no)
        self.lex = lex


class BinaryNode(ExpressionNode):
    def __init__(self, line_no, col_no, left, right):
        super().__init__(line_no, col_no)
        self.left = left
        self.right = right


class BooleanBinaryNode(BinaryNode):
    pass


class ArithBinaryNode(BinaryNode):
    pass


class ConstantNumNode(AtomicNode):
    pass


class StringNode(AtomicNode):
    pass


class VariableNode(AtomicNode):
    pass


class BoolNode(AtomicNode):
    pass


class InstantiateNode(AtomicNode):
    pass


class PlusNode(ArithBinaryNode):
    pass


class MinusNode(ArithBinaryNode):
    pass


class StarNode(ArithBinaryNode):
    pass


class DivNode(ArithBinaryNode):
    pass


class LessNode(BooleanBinaryNode):
    pass


class LessEqualNode(BooleanBinaryNode):
    pass


class EqualNode(BooleanBinaryNode):
    pass
