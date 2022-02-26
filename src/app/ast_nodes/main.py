# from typing import List


# class CoolAstNode:
#     def __init__(self, lineno, columnno):
#         self.lineno = lineno
#         self.columnno = columnno


# class CoolClassNode(CoolAstNode):
#     def __init__(self, lineno, columnno, id, features, parent=None):
#         super().__init__(lineno, columnno)

#         self.id = id
#         self.parent = parent
#         self.features: List[CoolFeatureNode] = features

#     @staticmethod
#     def parse(p):
#         name, parent, features = p.TYPE_ID0, p.TYPE_ID1, p.feature
#         return CoolClassNode(p.lineno, 0, name, features, parent=parent)


# class CoolProgramNode(CoolAstNode):
#     def __init__(self, lineno, columnno, classes: List[CoolClassNode]):
#         super().__init__(lineno, columnno)
#         self.classes: List[CoolClassNode] = classes

#     @staticmethod
#     def parse(p):
#         classes = [p.cool_class0] + p.cool_class1
#         return CoolProgramNode(p.lineno, 0, classes)


# class CoolFeatureNode(CoolAstNode):
#     pass


# class CoolExprNode(CoolAstNode):
#     pass


# class CoolLetDeclNode(CoolAstNode):
#     def __init__(self, lineno, columnno, id, type, expr=None):
#         super().__init__(lineno, columnno)
#         self.id = id
#         self.type = type
#         self.expr = expr

#     @staticmethod
#     def parse(p):
#         return CoolLetDeclNode(p.lineno, 0, p.OBJECT_ID,  p.TYPE_ID, expr=p.expr)


# class CoolCaseBranchNode(CoolAstNode):
#     def __init__(self, lineno, columnno, id, type, expr):
#         super().__init__(lineno, columnno)

#         self.id = id
#         self.type = type
#         self.expr = expr

#     @staticmethod
#     def parse(p):
#         id, type, expr = p.OBJECT_ID, p.TYPE_ID, p.expr
#         return CoolCaseBranchNode(p.lineno, 0, id, type, expr)
