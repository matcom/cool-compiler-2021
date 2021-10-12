from typing import List
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
import ast.ccil_ast as ccil


class CCILGenerator:
    def __init__(self) -> None:
        self.count = 0

    @visitor.on("node")
    def visit(self, node):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node: ProgramNode) -> ccil.ProgramNode:
        class_decl: List[ccil.ClassDeclarationNode] = []
        for declaration in node.declarations:
            class_decl.append(self.visit(declaration))

        # The other things need should be deleted?
        return ccil.ProgramNode(class_decl)

    @visitor.when(ClassDeclarationNode)
    def visit(self, node: ClassDeclarationNode) -> ccil.ClassDeclarationNode:
        class_features: List[ccil.DeclarationNode] = []
        for feature in node.features:
            class_features.append(self.visit(feature))

        # Parent apparently is not needed?
        return ccil.ClassDeclarationNode(node.id, parent="?", features=class_features)

    @visitor.when(AttrDeclarationNode)
    def visit(self, node: AttrDeclarationNode) -> ccil.AttrDeclarationNode:
        ccil_node: ccil.AttrDeclarationNode = ccil.AttrDeclarationNode(
            node.id, node.type, None
        )
        if node.expr is not None:
            ccil_node.expression = self.visit(node.expr)
        return ccil_node

    @visitor.when(MethodDeclarationNode)
    def visit(self, node: MethodDeclarationNode) -> ccil.MethodDeclarationNode:
        # What to do about parameter ?? Unanswered question from the past...

        body: ccil.ExpressionNode = self.visit(node.body)
        # Fill return with something :(
        return MethodDeclarationNode()

    @visitor.when(BlocksNode)
    def visit(self, node: BlocksNode) -> ccil.BlocksNode:
        expr_list: List[ccil.ExpressionNode] = [
            self.visit(expr) for expr in node.expr_list
        ]
        return ccil.BlocksNode(expr_list)

    @visitor.when(ConditionalNode)
    def visit(self, node: ConditionalNode) -> ccil.ConditionalNode:
        condition: ccil.ExpressionNode = self.visit(node.condition)
        then_body: ccil.ExpressionNode = self.visit(node.then_body)
        else_body: ccil.ExpressionNode = self.visit(node.else_body)

        return ccil.ConditionalNode(condition, then_body, else_body)

    @visitor.when(CaseNode)
    def visit(self, node: CaseNode) -> ccil.CaseNode:
        pass

    @visitor.when(CaseOptionNode)
    def visit(self, node: CaseOptionNode) -> ccil.CaseOptionNode:
        pass

    @visitor.when(LoopNode)
    def visit(self, node: LoopNode) -> ccil.LoopNode:
        pass

    @visitor.when(LetNode)
    def visit(self, node: LetNode) -> ccil.LetNode:
        pass

    @visitor.when(VarDeclarationNode)
    def visit(self, node: VarDeclarationNode) -> ccil.VarDeclarationNode:
        pass

    @visitor.when(VariableNode)
    def visit(self, node: VariableNode) -> ccil.VariableNode:
        pass

    @visitor.when(StringNode)
    def visit(self, node: StringNode) -> ccil.StringNode:
        pass

    @visitor.when(IntNode)
    def visit(self, node: IntNode) -> ccil.IntNode:
        pass

    def generate_var_name(self) -> str:
        """Generate a new local name"""
        self.count += 1
        return f"v{self.count}"
