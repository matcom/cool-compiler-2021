import coolpyler.utils.meta as meta
import coolpyler.ast.cool.base as base

meta.from_module(base)


class CoolProgramNode(*meta.get_bases("CoolProgramNode")):
    def __init__(self, lineno, columnno, classes, types):
        super().__init__(lineno, columnno)
        self.classes = classes
        self.types = types


class CoolClassNode(*meta.get_bases("CoolClassNode")):
    def __init__(self, lineno, columnno, type, features, parent=None):
        super().__init__(lineno, columnno)
        self.type = type
        self.parent = parent
        self.features = features
