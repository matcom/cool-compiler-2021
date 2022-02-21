from semantic.semantic import ErrorType
from utils.errors import SemanticError
from utils import visitor
from utils.ast import *


class TypeChecker:
    def __init__(self, context, errors):
        self.context = context
        self.currentType = None
        self.currentMethod = None
        self.errors = errors
        self.currentIndex = None

    @visitor.on('node')
    def visit(self, node, scope):
        pass

    @visitor.when(ProgramNode)
    def visit(self, programNode, scope):
        for i in range(0, len(programNode.declarations)):
            self.visit(programNode.declarations[i], scope.children[i])

    def _get_type(self, ntype, pos):
        try:
            return self.context.get_type(ntype, pos)
        except SemanticError as e:
            self.errors.append(e)
            return ErrorType()

    def _get_method(self, typex, name, pos):
        try:
            return typex.get_method(name, pos)
        except SemanticError:
            if type(typex) != ErrorType and type(typex) != AutoType:
                

