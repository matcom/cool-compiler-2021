from utils import visitor
from ast.types_ast import (
    CaseNode,
    CaseOptionNode,
    ConditionalNode,
    IntNode,
    LetNode,
    LoopNode,
    ProgramNode,
    ClassDeclarationNode,
    AttrDeclarationNode,
    MethodDeclarationNode,
    BlocksNode,
    StringNode,
    VarDeclarationNode,
    VariableNode,
)


class CilGenerator:
    def __init__(self) -> None:
        pass

    @visitor.on("node")
    def visit(self, node):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node: ProgramNode):
        pass

    @visitor.when(ClassDeclarationNode)
    def visit(self, node: ClassDeclarationNode):
        pass

    @visitor.when(AttrDeclarationNode)
    def visit(self, node: AttrDeclarationNode):
        pass

    @visitor.when(MethodDeclarationNode)
    def visit(self, node: MethodDeclarationNode):
        pass

    @visitor.when(BlocksNode)
    def visit(self, node: BlocksNode):
        pass

    @visitor.when(ConditionalNode)
    def visit(self, node: ConditionalNode):
        pass

    @visitor.when(CaseNode)
    def visit(self, node: CaseNode):
        pass

    @visitor.when(CaseOptionNode)
    def visit(self, node: CaseOptionNode):
        pass

    @visitor.when(LoopNode)
    def visit(self, node: LoopNode):
        pass

    @visitor.when(LetNode)
    def visit(self, node: LetNode):
        pass

    @visitor.when(VarDeclarationNode)
    def visit(self, node: VarDeclarationNode):
        pass

    @visitor.when(VariableNode)
    def visit(self, node: VariableNode):
        pass

    @visitor.when(StringNode)
    def visit(self, node: StringNode):
        pass

    @visitor.when(IntNode)
    def visit(self, node: IntNode):
        pass
