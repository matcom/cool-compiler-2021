import coolpyler.ast.cool.base as base


class CoolProgramNode(base.CoolProgramNode):
    def __init__(self, lineno, columnno, classes, types):
        super().__init__(lineno, columnno)

        self.classes = classes
        self.types = types


class CoolClassNode(base.CoolClassNode):
    def __init__(self, lineno, columnno, type, features, parent=None):
        super().__init__(lineno, columnno)

        self.type = type
        self.parent = parent
        self.features = features
