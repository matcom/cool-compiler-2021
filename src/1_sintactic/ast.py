class Node():
    def __init__(self):
        pass


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
        self.exp = exp


class AttrDeclarationNode(Node):
    def __init__(self, name, type, expr=None):
        super().__init__()
        self.name = name
        self.type = type
        self.exp = exp


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
    def __init__(self, id, args, object=None, type=None):
        super().__init__()
        self.id = id
        self.args = args
        self.object = object
        self.type = type


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
        self.case_list = case_list:


class CaseOptionNode(ExpressionNode):
    def __init__(self, id, expr, type):
        super().__init__()
        self.id = id
        self.expr = expr
        self.type = type


class VarNode(ExpressionNode):
    def __init__(self, id):
        super().__init__()
        self.id = id


class NewNode(ExpressionNode):
    def __init__(self, type):
        super().__init__()
        self.type = type


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


class LessThanNode(BinaryNode):
    pass


class LessEqNode(BinaryNode):
    pass


class EqNode(BinaryNode):
    pass


# ---------------- Unary Nodes ------------------

class UnaryNode(ExpressionNode):
    def __init__(self, value):
        super().__init__()
        self.value = value


class NotNode(UnaryNode):
    pass


class LogicNotNode(UnaryNode):
    pass


class AtomicNode(UnaryNode):
    pass


class IsVoidNode(UnaryNode):
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
