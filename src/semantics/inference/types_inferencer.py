from semantics.tools.type import ErrorType
from utils import visitor

from semantics.tools import TypeBag
import ast.types_ast as types_ast
from ast.inferencer_ast import (
    ProgramNode,
    ClassDeclarationNode,
    MethodDeclarationNode,
    AttrDeclarationNode,
    BlocksNode,
    ConditionalNode,
    CaseNode,
    CaseOptionNode,
    LoopNode,
    LetNode,
    VarDeclarationNode,
    AssignNode,
    MethodCallNode,
    BinaryNode,
    BooleanNode,
    ClassDeclarationNode,
    InstantiateNode,
    IntNode,
    ProgramNode,
    AttrDeclarationNode,
    Node,
    StringNode,
    UnaryNode,
    VariableNode,
)


class TypesInferencer:
    def __init__(self) -> None:
        pass

    @visitor.on("node")
    def visit(self, node):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node: ProgramNode) -> types_ast.ProgramNode:
        class_decl = []
        for decl in node.declarations:
            class_decl.append(self.visit(decl))

        return types_ast.ProgramNode(class_decl, node)

    @visitor.when(ClassDeclarationNode)
    def visit(self, node: ClassDeclarationNode) -> types_ast.ClassDeclarationNode:
        features = []
        for feature in node.features:
            features.append(self.visit(feature))

        return types_ast.ClassDeclarationNode(features, node)

    @visitor.when(AttrDeclarationNode)
    def visit(self, node: AttrDeclarationNode) -> types_ast.AttrDeclarationNode:
        new_node = types_ast.AttrDeclarationNode(node)
        if node.expr:
            new_node.expr = self.visit(node.expr)
        new_node.type = self._reduce_to_type(node.inferenced_type)
        return new_node

    @visitor.when(MethodDeclarationNode)
    def visit(self, node: MethodDeclarationNode) -> types_ast.MethodDeclarationNode:
        body = self.visit(node.body)
        params = [self.visit(param) for param in node.params]
        ret_type = self._reduce_to_type(node.inferenced_type)
        return types_ast.MethodDeclarationNode(params, ret_type, node)

    @visitor.when(BlocksNode)
    def visit(self, node: BlocksNode) -> types_ast.BlocksNode:
        expr_list = [self.visit(expr) for expr in node.expr_list]

        new_node = types_ast.BlocksNode(expr_list, node)
        new_node.type = expr_list[-1].type
        return new_node

    @visitor.when(ConditionalNode)
    def visit(self, node: ConditionalNode) -> types_ast.ConditionalNode:
        condition = self.visit(node.condition)
        then_body = self.visit(node.then_body)
        else_body = self.visit(node.else_body)

        new_node = types_ast.ConditionalNode(condition, then_body, else_body, node)
        new_node.type = self._reduce_to_type(node.inferenced_type)
        return new_node

    @visitor.when(CaseNode)
    def visit(self, node: CaseNode) -> types_ast.CaseNode:
        expr = self.visit(node.case_expr)
        case_options = [self.visit(option) for option in node.options]
        new_node = types_ast.CaseNode(expr, case_options, node)
        new_node.type = self._reduce_to_type(node.inferenced_type)
        return new_node

    @visitor.when(CaseOptionNode)
    def visit(self, node: CaseOptionNode) -> types_ast.CaseOptionNode:
        return types_ast.CaseOptionNode(self.visit(node.expr),node)

    @visitor.when()
        

    def _reduce_to_type(self, bag: TypeBag, node: Node):
        if bag.heads > 1:
            self.add_error(node, "ErrorType: Ambiguous type declaration")
            return ErrorType()
        return bag.heads[0]

    def add_error(self, node, text: str):
        line, col = node.get_position() if node else (0, 0)
        self.errors.append(((line, col), f"({line}, {col}) - " + text))