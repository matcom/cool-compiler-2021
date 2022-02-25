from copy import copy, deepcopy
from semantics.tools.errors import SemanticError
from typing import Tuple

from semantics.tools.type import Method, SelfType, Type
from semantics.tools import Context, Scope, TypeBag, join, join_list, unify
from utils import visitor
from asts.inferencer_ast import (
    ParamNode,
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


class BackInferencer:
    def __init__(self, context: Context) -> None:
        self.context = context
        self.errors = []
        self.current_type: Type
        self.changed = False

    @visitor.on("node")
    def visit(self, node, scope):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node: ProgramNode) -> Tuple[ProgramNode, bool]:
        scope = Scope()
        self.changed = False
        new_declaration = []
        for declaration in node.declarations:
            new_declaration.append(self.visit(declaration, scope.create_child()))

        program = ProgramNode(new_declaration, scope, node)
        return program, self.changed

    @visitor.when(ClassDeclarationNode)
    def visit(self, node: ClassDeclarationNode, scope: Scope) -> ClassDeclarationNode:
        self.current_type = self.context.get_type(node.id, unpacked=True)
        scope.define_variable("self", TypeBag({SelfType()}))

        new_features = []
        for feature in node.features:
            new_features.append(self.visit(feature, scope))

        class_node = ClassDeclarationNode(new_features, node)
        return class_node

    @visitor.when(AttrDeclarationNode)
    def visit(self, node, scope: Scope):
        attr_node = AttrDeclarationNode(node)

        if not node.expr:
            attr_node.inferenced_type = node.inferenced_type
            scope.define_variable(node.id, node.inferenced_type)
            return attr_node

        expr_node = self.visit(node.expr, scope)
        expr_type = expr_node.inferenced_type

        decl_type = node.inferenced_type
        decl_type, changed = unify(decl_type, expr_type)
        scope.define_variable(node.id, decl_type)
        self.changed |= changed

        attr_node.expr = expr_node
        attr_node.inferenced_type = decl_type
        return attr_node

    @visitor.when(MethodDeclarationNode)
    def visit(self, node: MethodDeclarationNode, scope) -> MethodDeclarationNode:
        scope = scope.create_child()
        current_method: Method = self.current_type.get_method(node.id)

        new_params = []
        for idx, typex, param in zip(
            current_method.param_names, current_method.param_types, node.params
        ):
            scope.define_variable(idx, typex)
            new_params.append(ParamNode(param, idx, typex))

        param_types = [
            unify(typex, new_param.type)
            for new_param, typex in zip(new_params, current_method.param_types)
        ]
        current_method.param_types = [i[0] for i in param_types]
        self.changed |= any([i[1] for i in param_types])

        new_body_node = self.visit(node.body, scope)
        body_type = new_body_node.inferenced_type.swap_self_type(self.current_type)
        new_node = MethodDeclarationNode(new_params, node.type, new_body_node, node)
        decl_type = node.inferenced_type
        body_type = new_body_node.inferenced_type
        new_node.inferenced_type, changed = unify(decl_type, body_type)
        self.changed |= changed
        return new_node

    @visitor.when(BlocksNode)
    def visit(self, node: BlocksNode, scope) -> BlocksNode:
        new_expr_list = []
        for expr in node.expr_list:
            new_expr_list.append(self.visit(expr, scope))

        new_node = BlocksNode(new_expr_list, node)
        decl_type = node.inferenced_type
        expr_type = new_expr_list[-1].inferenced_type
        new_node.inferenced_type, changed = unify(decl_type, expr_type)
        self.changed |= changed
        return new_node

    @visitor.when(ConditionalNode)
    def visit(self, node: ConditionalNode, scope) -> ConditionalNode:
        new_condition_node = self.visit(node.condition, scope)
        new_then_node = self.visit(node.then_body, scope)
        new_else_node = self.visit(node.else_body, scope)

        join_type = join(new_then_node.inferenced_type, new_else_node.inferenced_type)
        decl_type = node.inferenced_type
        expr_type = join_type
        new_node = ConditionalNode(
            new_condition_node, new_then_node, new_else_node, node
        )
        new_node.inferenced_type, changed = unify(decl_type, expr_type)
        self.changed |= changed
        return new_node

    @visitor.when(CaseNode)
    def visit(self, node: CaseNode, scope: Scope) -> CaseNode:
        new_case_node = self.visit(node.case_expr, scope)
        new_options_nodes = []
        for option in node.options:
            child_scope = scope.create_child()
            new_options_nodes.append(self.visit(option, child_scope))

        join_type = join_list([option.inferenced_type for option in new_options_nodes])

        new_node = CaseNode(new_case_node, new_options_nodes, node)
        decl_type = node.inferenced_type
        expr_type = join_type
        new_node.inferenced_type, changed = unify(decl_type, expr_type)
        self.changed |= changed
        return new_node

    @visitor.when(CaseOptionNode)
    def visit(self, node: CaseOptionNode, scope: Scope) -> CaseOptionNode:
        try:
            node_type = self.context.get_type(node.type, selftype=False, autotype=False)
        except SemanticError as err:
            node_type = TypeBag(set())

        scope.define_variable(node.id, node_type)

        new_node_expr = self.visit(node.expr, scope)
        new_node = CaseOptionNode(new_node_expr, node_type, node)
        decl_type = node.inferenced_type
        expr_type = new_node_expr.inferenced_type
        new_node.inferenced_type, changed = unify(decl_type, expr_type)

        self.changed |= changed
        return new_node

    @visitor.when(LoopNode)
    def visit(self, node: LoopNode, scope) -> LoopNode:
        new_condition_node = self.visit(node.condition, scope)
        new_body_node = self.visit(node.body, scope)

        new_node = LoopNode(new_condition_node, new_body_node, node)
        new_node.inferenced_type = node.inferenced_type
        return new_node

    @visitor.when(LetNode)
    def visit(self, node: LetNode, scope) -> LetNode:
        child_scope = scope.create_child()

        new_var_decl_nodes = []
        for var_decl in node.var_decl_list:
            new_var_decl_nodes.append(self.visit(var_decl, child_scope))

        new_in_node = self.visit(node.in_expr, child_scope)

        new_node = LetNode(new_var_decl_nodes, new_in_node, node)
        decl_type = node.inferenced_type
        expr_type = new_in_node.inferenced_type
        new_node.inferenced_type, changed = unify(decl_type, expr_type)
        self.changed |= changed
        return new_node

    @visitor.when(VarDeclarationNode)
    def visit(self, node: VarDeclarationNode, scope: Scope) -> VarDeclarationNode:

        scope.define_variable(
            node.id, node.inferenced_type.swap_self_type(self.current_type)
        )
        new_node = VarDeclarationNode(node)

        if node.expr:
            new_expr_node = self.visit(node.expr, scope)
            new_node.expr = new_expr_node
            decl_type = node.inferenced_type
            expr_type = new_expr_node.inferenced_type
            new_node.inferenced_type, changed = unify(decl_type, expr_type)
            self.changed |= changed
        else:
            new_node.inferenced_type = node.inferenced_type

        return new_node

    @visitor.when(AssignNode)
    def visit(self, node: AssignNode, scope) -> AssignNode:
        new_expr_node = self.visit(node.expr, scope)
        if node.defined:
            decl_type = scope.find_variable(node.id).get_type()
        else:
            decl_type = new_expr_node.inferenced_type
        expr_type = new_expr_node.inferenced_type
        new_node = AssignNode(new_expr_node, node)
        new_node.defined = node.defined
        new_node.inferenced_type, changed = unify(decl_type, expr_type)
        self.changed |= changed
        return new_node

    @visitor.when(MethodCallNode)
    def visit(self, node: MethodCallNode, scope) -> MethodCallNode:
        caller_type: Type = node.caller_type.heads[0]
        method: Method = caller_type.get_method(node.id)

        new_args = []
        for arg_expr, param_type in zip(node.args, method.param_types):
            arg_node = self.visit(arg_expr, scope)
            arg_node.inferenced_type, changed = unify(
                param_type, arg_node.inferenced_type
            )
            self.changed |= changed
            new_args.append(arg_node)

        new_expr = self.visit(node.expr, scope) if node.expr else None
        new_node = MethodCallNode(node.caller_type, new_expr, new_args, node)

        method_return_type = method.return_type.clone().swap_self_type(caller_type)
        new_node.inferenced_type, changed = unify(
            node.inferenced_type, method_return_type
        )
        self.changed |= changed
        return new_node

    @visitor.when(BinaryNode)
    def visit(self, node: BinaryNode, scope) -> BinaryNode:
        new_node = copy(node)
        new_left_node = self.visit(node.left, scope)
        new_right_node = self.visit(node.right, scope)

        new_node.left = new_left_node
        new_node.right = new_right_node

        return new_node

    @visitor.when(UnaryNode)
    def visit(self, node: UnaryNode, scope) -> UnaryNode:
        new_node = copy(node)
        new_expr_node = self.visit(node.expr, scope)

        new_node.expr = new_expr_node
        return new_node

    @visitor.when(VariableNode)
    def visit(self, node: VariableNode, scope: Scope) -> VariableNode:
        new_node = copy(node)
        if node.defined:
            decl_type = node.inferenced_type.swap_self_type(self.current_type)
            expr_type = scope.find_variable(node.value)
            if expr_type is not None:
                expr_type = expr_type.get_type().swap_self_type(self.current_type)
            else:
                expr_type = decl_type
            new_node.inferenced_type, changed = unify(decl_type, expr_type)
            self.changed |= changed
            return new_node
        return new_node

    @visitor.when(InstantiateNode)
    def visit(self, node, scope) -> InstantiateNode:
        return copy(node)

    @visitor.when(IntNode)
    def visit(self, node, scope) -> IntNode:
        return copy(node)

    @visitor.when(StringNode)
    def visit(self, node, scope) -> StringNode:
        return copy(node)

    @visitor.when(BooleanNode)
    def visit(self, node, scope) -> BooleanNode:
        return copy(node)
