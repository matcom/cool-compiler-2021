from inspect import currentframe
from typing import Type
import app.semantics.ast as inf_ast
from app.parser.ast import *

import app.shared.visitor as visitor
from app.semantics.tools.errors import SemanticError, AttributeError
from app.semantics.tools import (
    Context,
    Scope,
    conforms,

)


class SoftInferrer:
    def __init__(self, context: Context) -> None:
        self.context = context
        self.errors = []
        self.current_type: Type = None

    @visitor.on("node")
    def visit(self, node, scope):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node: ProgramNode) -> inf_ast.ProgramNode:
        return inf_ast.ProgramNode.soft_infer(node, Scope(), self)

    @visitor.when(ClassNode)
    def visit(self, node: ClassNode, scope: Scope) -> ClassNode:
        return inf_ast.ClassDeclarationNode.soft_infer(node, scope, self)

    @visitor.when(AttrDeclNode)
    def visit(self, node: AttrDeclNode, scope: Scope):
        return inf_ast.AttrDeclarationNode.soft_infer(node, scope, self)

    @visitor.when(MethodDeclNode)
    def visit(self, node: MethodDeclNode, scope: Scope):
        return inf_ast.MethodDeclarationNode.soft_infer(node, scope, self)

    @visitor.when(BlockNode)
    def visit(self, node: BlockNode, scope):
        return inf_ast.BlocksNode.soft_infer(node, scope, self)

    @visitor.when(IfThenElseNode)
    def visit(self, node: IfThenElseNode, scope):
        return inf_ast.ConditionalNode.soft_infer(node, scope, self)

    @visitor.when(CaseNode)
    def visit(self, node: CaseNode, scope: Scope):
        return inf_ast.CaseNode.soft_infer(node, scope, self)

    @visitor.when(CaseBranchNode)
    def visit(self, node: CaseBranchNode, scope: Scope):
        return inf_ast.CaseOptionNode.soft_infer(node, scope, self)

    @visitor.when(WhileNode)
    def visit(self, node: WhileNode, scope):
        return inf_ast.LoopNode.soft_infer(node, scope, self)

    @visitor.when(LetInNode)
    def visit(self, node: LetInNode, scope: Scope):
        return inf_ast.LetNode.soft_infer(node, scope, self)

    @visitor.when(LetDeclNode)
    def visit(self, node: LetDeclNode, scope: Scope):
        return inf_ast.VarDeclarationNode.soft_infer(node, scope, self)

    @visitor.when(AssignNode)
    def visit(self, node: AssignNode, scope: Scope):
        return inf_ast.AssignNode.soft_infer(node, scope, self)

    @visitor.when(StaticDispatchNode)
    def visit(self, node: StaticDispatchNode, scope):
        return inf_ast.MethodCallNode.soft_infer_static(node, scope, self)

    @visitor.when(DispatchNode)
    def visit(self, node: DispatchNode, scope):
        return inf_ast.MethodCallNode.soft_infer_dynamic(node, scope, self)

    @visitor.when(ArithmeticNode)
    def visit(self, node: ArithmeticNode, scope):
        return inf_ast.ArithmeticNode.soft_infer(node, scope, self)

    @visitor.when(LeNode)
    def visit(self, node: LeNode, scope: Scope):
        return inf_ast.LessNode.soft_infer(node, scope, self)

    @visitor.when(LeqNode)
    def visit(self, node, scope: Scope):
        return inf_ast.LessOrEqualNode.soft_infer(node, scope, self)

    @visitor.when(EqNode)
    def visit(self, node: EqNode, scope: Scope):
        return inf_ast.EqualsNode.soft_infer(node, scope, self)

    @visitor.when(VarNode)
    def visit(self, node: VarNode, scope: Scope):
        return inf_ast.VariableNode.soft_infer(node, scope, self)

    @visitor.when(NotNode)
    def visit(self, node: NotNode, scope):
        return inf_ast.NotNode.soft_infer(node, scope, self)

    @visitor.when(TildeNode)
    def visit(self, node: TildeNode, scope):
        return inf_ast.ComplementNode.soft_infer(node, scope, self)

    @visitor.when(IsVoidNode)
    def visit(self, node: IsVoidNode, scope):
        return inf_ast.IsVoidNode.soft_infer(node, scope, self)

    @visitor.when(NewNode)
    def visit(self, node: NewNode, scope):
        return inf_ast.InstantiateNode.soft_infer(node, scope, self)

    @visitor.when(IntNode)
    def visit(self, node: IntNode, scope):
        return inf_ast.IntNode.soft_infer(node, scope, self)

    @visitor.when(StringNode)
    def visit(self, node: StringNode, scope):
        return inf_ast.StringNode.soft_infer(node, scope, self)

    @visitor.when(BoolNode)
    def visit(self, node: BoolNode, scope):
        return inf_ast.BooleanNode.soft_infer(node, scope, self)

    @visitor.when(ParenthNode)
    def visit(self, node: ParenthNode, scope):
        return self.visit(node.expr, scope)

    def _arithmetic_operation(self, node: ArithmeticNode, scope):
        left_node = self.visit(node.left_expr, scope)
        left_type = left_node.inferenced_type
        left_clone = left_type.clone()

        right_node = self.visit(node.right_expr, scope)
        right_type = right_node.inferenced_type
        right_clone = right_type.clone()

        int_type = self.context.get_type("Int")
        if not conforms(left_type, int_type):
            self.add_error(
                node.left_expr,
                f"TypeError: ArithmeticError: Left member type({left_clone.name})"
                " does not conforms to Int type.",
            )
        if not conforms(right_type, int_type):
            self.add_error(
                node.right_expr,
                f"TypeError: ArithmeticError: Right member type({right_clone.name})"
                " does not conforms to Int type.",
            )
        return left_node, right_node

    def add_error(self, node: AstNode, text: str):
        line, col = node.lineno, node.columnno if node else (0, 0)
        self.errors.append(f"({line}, {col}) - " + text)
