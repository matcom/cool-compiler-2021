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


# FUNC CALLS NODES MISSING


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
        
