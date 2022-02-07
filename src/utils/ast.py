class Node():
    def __init__(self):
        self.line = 0
        self.column = 0

    def add_line_column(self, line, column):
        self.line = line
        self.column = column


class ProgramNode(Node):
    def __init__(self, classes):
        super().__init__()
        self.classes = classes


class ClassDeclarationNode(Node):
    def __init__(self, name, features, parent=None):
        super().__init__()
        self.name = name
        self.features = features
        self.parent = parent


class FuncDeclarationNode(Node):
    def __init__(self, name, params, return_type, expr=None):
        super().__init__()
        self.name = name
        self.params = params
        self.return_type = return_type
        self.expr = expr


class AttrDeclarationNode(Node):
    def __init__(self, name, typex, expr=None):
        super().__init__()
        self.name = name
        self.type = typex
        self.expr = expr


class ExpressionNode(Node):
    def __init__(self):
        super().__init__()
        self.computed_type = None


class AssignNode(ExpressionNode):
    def __init__(self, name, expr):
        super().__init__()
        self.name = name
        self.expr = expr


class FuncCallNode(ExpressionNode):
    def __init__(self, idx, args, obj=None, typex=None):
        super().__init__()
        self.id = idx
        self.args = args
        self.object = obj
        self.type = typex


class IfNode(ExpressionNode):
    def __init__(self, condition, then_expr, else_expr):
        super().__init__()
        self.condition = condition
        self.then_expr = then_expr
        self.else_expr = else_expr


class WhileNode(ExpressionNode):
    def __init__(self, condition, body):
        super().__init__()
        self.condition = condition
        self.body = body


class BlockNode(ExpressionNode):
    def __init__(self, exprs):
        super().__init__()
        self.exprs = exprs


class LetNode(ExpressionNode):
    def __init__(self, let_attrs, expr):
        super().__init__()
        self.let_attrs = let_attrs
        self.expr = expr


class CaseNode(ExpressionNode):
    def __init__(self, expr, case_list):
        super().__init__()
        self.expr = expr
        self.case_list = case_list


class CaseOptionNode(ExpressionNode):
    def __init__(self, idx, typex, expr):
        super().__init__()
        self.id = idx
        self.expr = expr
        self.type = typex


class VarNode(ExpressionNode):
    def __init__(self, idx):
        super().__init__()
        self.id = idx


class NewNode(ExpressionNode):
    def __init__(self, typex):
        super().__init__()
        self.type = typex


# ---------------- Binary Nodes ------------------

class BinaryNode(ExpressionNode):
    def __init__(self, lvalue, rvalue):
        super().__init__()
        self.lvalue = lvalue
        self.rvalue = rvalue


class PlusNode(BinaryNode):
    pass


class MinusNode(BinaryNode):
    pass


class StarNode(BinaryNode):
    pass


class DivNode(BinaryNode):
    pass


class LessNode(BinaryNode):
    pass


class LessEqNode(BinaryNode):
    pass


class EqualNode(BinaryNode):
    pass


# ---------------- Unary Nodes ------------------

class UnaryNode(ExpressionNode):
    def __init__(self, value):
        super().__init__()
        self.value = value


class NegationNode(UnaryNode):
    pass


class LogicNegationNode(UnaryNode):
    pass


class AtomicNode(UnaryNode):
    pass


class IsVoidNode(UnaryNode):
    pass

class SelfNode(UnaryNode):
    pass


# ---------------- Constant Nodes ------------------

class ConstantNode(ExpressionNode):
    def __init__(self, value):
        super().__init__()
        self.value = value


class IntNode(ConstantNode):
    pass


class BoolNode(ConstantNode):
    pass


class StringNode(ConstantNode):
    pass
