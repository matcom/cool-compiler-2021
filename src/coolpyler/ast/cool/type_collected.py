import sys
import coolpyler.utils.meta as meta
import coolpyler.ast.cool.base as base


class CoolProgramNode:
    def __init__(self, lineno, columnno, classes, types):
        # super().__init__(lineno, columnno)
        self.lineno = lineno
        self.columno = columnno
        self.classes = classes
        self.types = types


class CoolClassNode:
    def __init__(self, lineno, columnno, type, features, parent=None):
        # super().__init__(lineno, columnno)
        self.lineno = lineno
        self.columno = columnno
        self.type = type
        self.parent = parent
        self.features = features


meta.map_hierarchy(
    base.CoolAstNode, [CoolProgramNode, CoolClassNode], sys.modules[__name__]
)
