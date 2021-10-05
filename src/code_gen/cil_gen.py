from utils import visitor
from ast.types_ast import (
        ProgramNode,
        ClassDeclarationNode,
        AttrDeclarationNode,
        MethodDeclarationNode
    )

class CilGenerator:
    def __init__(self) -> None:
        pass

    @visitor.on("node")
    def visit(self, node):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node:ProgramNode):
        pass

    @visitor.when(ClassDeclarationNode)
    def visit(self, node:ClassDeclarationNode):
        pass
    
    @visitor.when(AttrDeclarationNode)
    def visit(self, node:AttrDeclarationNode):
        pass

    @visitor.when(MethodDeclarationNode)
    def visit(self, node:MethodDeclarationNode):
        pass
