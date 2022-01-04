from typing import Dict, List
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
from code_gen.tools import make_id
import ast.ccil_ast as ccil


class CCILGenerator:
    def __init__(self) -> None:
        self.constant_data: List[str]
        # This is not needed in this layer of abstraction
        self.count: Dict[str, int] = {"while": 0, "if": 0, "case": 0, "function": 0}

    @visitor.on("node")
    def visit(self, _):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node: ProgramNode) -> ccil.ProgramNode:
        class_decl: List[ccil.ClassDeclarationNode] = []
        for declaration in node.declarations:
            class_decl.append(self.visit(declaration))

        return ccil.ProgramNode(class_decl, self.constant_data, node)

    @visitor.when(ClassDeclarationNode)
    def visit(self, node: ClassDeclarationNode) -> ccil.ClassDeclarationNode:
        class_features: List[ccil.DeclarationNode] = []
        for feature in node.features:
            class_features.append(self.visit(feature))

        return ccil.ClassDeclarationNode(class_features, node)

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

        for param in node.params:
            pass

        body: ccil.ExpressionNode = self.visit(node.body)
        return MethodDeclarationNode()

    @visitor.when(BlocksNode)
    def visit(self, node: BlocksNode) -> ccil.BlocksNode:
        expr_list: List[ccil.ExpressionNode] = [
            self.visit(expr) for expr in node.expr_list
        ]
        return ccil.BlocksNode(expr_list, node)

    @visitor.when(ConditionalNode)
    def visit(self, node: ConditionalNode) -> ccil.ConditionalNode:
        condition: ccil.ExpressionNode = self.visit(node.condition)
        then_body: ccil.ExpressionNode = self.visit(node.then_body)
        else_body: ccil.ExpressionNode = self.visit(node.else_body)

        value = self.generate_var_name()
        return ccil.ConditionalNode(condition, then_body, else_body, value, [value])

    @visitor.when(CaseNode)
    def visit(self, node: CaseNode) -> ccil.CaseNode:
        locals = []
        expressions = []

    @visitor.when(CaseOptionNode)
    def visit(self, node: CaseOptionNode) -> ccil.CaseOptionNode:
        pass

    @visitor.when(LoopNode)
    def visit(self, node: LoopNode) -> ccil.LoopNode:
        pass

    @visitor.when(LetNode)
    def visit(self, node: LetNode) -> ccil.LetNode:
        new_decl_list: List[VarDeclarationNode] = []
        for let_decl_node in node.var_decl_list:
            new_decl_list.append(self.visit(let_decl_node))
        node_expr: ccil.ExpressionNode = self.visit(node.in_expr)

    @visitor.when(VarDeclarationNode)
    def visit(self, node: VarDeclarationNode) -> ccil.VarDeclarationNode:
        value = self.generate_var_name()
        if node.expr is not None:
            ccil_node_expr: ccil.ExpressionNode = self.visit(node.expr)
            return ccil.VarDeclarationNode(ccil_node_expr, node, value, [value])
        return ccil.VarDeclarationNode(None, node, value, [value])

    @visitor.when(VariableNode)
    def visit(self, node: VariableNode) -> ccil.VariableNode:
        return ccil.VariableNode(node, value=node.id)

    @visitor.when(StringNode)
    def visit(self, node: StringNode) -> ccil.StringNode:
        pass

    @visitor.when(IntNode)
    def visit(self, node: IntNode) -> ccil.IntNode:
        return ccil.IntNode(node, value="")
