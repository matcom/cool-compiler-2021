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
