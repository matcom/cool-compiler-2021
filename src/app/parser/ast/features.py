from .base import FeatureNode


class AttrDeclNode(FeatureNode):
    def __init__(self, lineno, columnno, id, type, body=None):
        super().__init__(lineno, columnno)
        self.id = id
        self.type = type
        self.body = body

    @staticmethod
    def parse(p):
        id, type, expr = p.OBJECT_ID, p.TYPE_ID, p.expr
        return AttrDeclNode(p.lineno, 0, id, type, expr)


class MethodDeclNode(FeatureNode):
    def __init__(self, lineno, columnno, id, param_names, type, body):
        super().__init__(lineno, columnno)

        self.id = id
        self.param_names = param_names
        self.type = type
        self.body = body

    @staticmethod
    def parse(p):
        return MethodDeclNode(p.lineno, 0, p.OBJECT_ID, p.formal_list if p.formal_list is not None else ([], []),  p.TYPE_ID, p.expr)
