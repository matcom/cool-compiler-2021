from utils.ast import *
from utils import visitor
from semantic.tools import *
from semantic.types import *

class TypeChecker:
    def __init__(self, context:Context, errors=[]):
        self.context:Context = context
        self.errors:list = errors
        self.current_index = None
        self.current_type:Type = None
        self.current_method:Method = None

    @visitor.on('node')
    def visit(self, node, scope):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node:ProgramNode, scope:Scope):
        for declaration,new_scope in zip(node.declarations, scope.children):
            self.visit(declaration, new_scope)

    @visitor.when(ClassDeclarationNode)
    def visit(self, node:ClassDeclarationNode, scope:Scope):
        self.current_type = self.context.get_type(node.id, node.pos)
        fd = [ feature for feature in node.features 
                    if isinstance(feature, FuncDeclarationNode) ]

        for feature in node.features:
            if isinstance(feature, FuncDeclarationNode):
                self.visit(feature, scope)

        for feature,child_scope in zip(fd, scope.functions.values()):
            self.visit(feature, child_scope)

