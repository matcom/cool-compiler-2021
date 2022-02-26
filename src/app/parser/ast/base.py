from typing import List


class AstNode:
    '''Base clase for AST parser'''

    def __init__(self, lineno, columnno):
        self.lineno = lineno
        self.columnno = columnno


class ClassNode(AstNode):
    def __init__(self, lineno, columnno, id, features, parent=None):
        super().__init__(lineno, columnno)

        self.id = id
        self.parent = parent
        self.features: List[FeatureNode] = features

    @staticmethod
    def parse(p):
        name, parent, features = p.TYPE_ID0, p.TYPE_ID1, p.feature
        return ClassNode(p.lineno, 0, name, features, parent=parent)


class ProgramNode(AstNode):
    def __init__(self, lineno, columnno, classes: List[ClassNode]):
        super().__init__(lineno, columnno)
        self.classes: List[ClassNode] = classes

    @staticmethod
    def parse(p):
        classes = [p._class0] + p._class1
        return ProgramNode(p.lineno, 0, classes)


class FeatureNode(AstNode):
    pass


class ExprNode(AstNode):
    pass


class LetDeclNode(AstNode):
    def __init__(self, lineno, columnno, id, type, expr=None):
        super().__init__(lineno, columnno)
        self.id = id
        self.type = type
        self.expr = expr

    @staticmethod
    def parse(p):
        return LetDeclNode(p.lineno, 0, p.OBJECT_ID,  p.TYPE_ID, expr=p.expr)


class CaseBranchNode(AstNode):
    def __init__(self, lineno, columnno, id, type, expr):
        super().__init__(lineno, columnno)
        self.id = id
        self.type = type
        self.expr = expr

    @staticmethod
    def parse(p):
        id, type, expr = p.OBJECT_ID, p.TYPE_ID, p.expr
        return CaseBranchNode(p.lineno, 0, id, type, expr)
