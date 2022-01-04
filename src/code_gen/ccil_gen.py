from typing import Dict, List
from code_gen.constants import ATTR_NAME
from utils import visitor
from asts.types_ast import (
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
from code_gen.tools import Feature, make_id
import asts.ccil_ast as ccil


class CCILGenerator:
    def __init__(self) -> None:
        self.warnings: List[str] = []
        self.constant_data: List[str] = []
        self.count: Dict[str, int] = {"while": 0, "if": 0, "case": 0, "function": 0}

        self.class_name: str
        self.attr_count: int
        self.func_count: int
        self.feature_name: str
        self.local_var_count: int

    @visitor.on("node")
    def visit(self, _):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node: ProgramNode) -> ccil.ProgramNode:
        class_decl: List[ccil.ClassDeclarationNode] = []
        for declaration in node.declarations:
            self.set_class_params(declaration.id)
            class_decl.append(self.visit(declaration))

        return ccil.ProgramNode(class_decl, self.constant_data, node)

    @visitor.when(ClassDeclarationNode)
    def visit(self, node: ClassDeclarationNode) -> ccil.ClassDeclarationNode:
        class_attr: List[ccil.AttrDeclarationNode] = []
        class_func: List[ccil.MethodDeclarationNode] = []
        class_feat: List[Feature] = []

        # Sort by putting attributes first, delete if this is the case already
        node.features.sort(key=lambda x: isinstance(x, AttrDeclarationNode))
        for feature in node.features:
            self.set_feature_params(feature.id)
            if isinstance(feature, AttrDeclarationNode):
                class_attr.append(self.visit(feature))
                class_feat.append(Feature(feature.id, "ccil_name", True))
            else:
                class_func.append(self.visit(feature))
                class_feat.append(Feature(feature.id, "ccil_name", False))

        return ccil.ClassDeclarationNode(class_attr, class_func, class_feat, node)

    @visitor.when(AttrDeclarationNode)
    def visit(self, node: AttrDeclarationNode) -> ccil.AttrDeclarationNode:
        ccil_node_name = make_id(
            ATTR_NAME,
        )
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
        return ccil.ConditionalNode(condition, then_body, else_body, [value])

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

    def set_class_params(self, name: str):
        self.class_name = name
        self.attr_count = 0
        self.func_count = 0

    def set_feature_params(self, name: str):
        self.feature_name = name
        self.local_var_count = 0
