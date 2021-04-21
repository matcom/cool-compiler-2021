from utils.ast import *
from semantic.tools import *


class VarCollector:

    def __init__(self, context, errors=[]):
        self.context = context
        self.errors = errors

    @visitor.on('node')
    def visit(self, node, scope):
        pass

    @visit.when('ProgramNode')
    def visit(self, node:ProgramNode, scope:Scope):
        scope = Scope()
        for declaration in node.declarations:
            self.visit(declaration, scope.create_child())
        return scope
