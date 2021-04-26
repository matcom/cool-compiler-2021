from copy import deepcopy

from semantics.tools.type import Method, Type

from ast.inferencer_ast import (
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
from semantics.tools import Context, Scope, TypeBag, join, join_list, try_conform
from utils import visitor
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
)


class BackInferencer:
    def __init__(self, context: Context) -> None:
        self.context = context
        self.errors = []
        self.current_type = None

    @visitor.on("node")
    def visit(self, node, scope):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node: ProgramNode) -> ProgramNode:
        scope: Scope = node.scope
        new_declaration = []
        for declaration in node.declarations:
            new_declaration.append(self.visit(declaration, scope.next_child()))

        program = ProgramNode(new_declaration, scope, node)
        return program

    @visitor.when(ClassDeclarationNode)
    def visit(self, node: ClassDeclarationNode, scope: Scope) -> ClassDeclarationNode:
        self.current_type = self.context.get_type(node.id, unpacked=True)

        new_features = []
        for feature in node.features:
            new_features.append(self.visit(feature, scope))

        class_node = ClassDeclarationNode(new_features, node)
        return class_node

    @visitor.when(AttrDeclarationNode)
    def visit(self, node, scope):
        attr_node = AttrDeclarationNode(node)

        if not node.expr:
            return attr_node

        expr_node = self.visit(node.expr, scope)
        expr_type = expr_node.inferenced_type

        decl_type = node.inferenced_type
        decl_type = try_conform(decl_type, expr_type)

        attr_node.expr = expr_node
        attr_node.inferenced_type = decl_type
        return attr_node

    @visitor.when(MethodDeclarationNode)
    def visit(self, node: MethodDeclarationNode, scope) -> MethodDeclarationNode:
        scope = scope.create_child()
        current_method = self.current_type.get_method(node.id)

        for idx, typex in zip(current_method.param_names, current_method.param_types):
            scope.define_variable(idx, typex)

        new_body_node = self.visit(node.body, scope)
        body_type = new_body_node.inferenced_type
        new_node = MethodDeclarationNode(node.type, new_body_node, node)
        decl_type = node.inferenced_type
        body_type = new_body_node.inferenced_type
        new_node.inferenced_type = try_conform(decl_type, body_type)
        return new_node

    @visitor.when(BlocksNode)
    def visit(self, node: BlocksNode, scope) -> BlocksNode:
        new_expr_list = []
        for expr in node.expr_list:
            new_expr_list.append(self.visit(expr, scope))

        new_node = BlocksNode(new_expr_list, node)
        decl_type = node.inferenced_type
        expr_type = new_expr_list[-1].inferenced_type
        new_node.inferenced_type = try_conform(decl_type, expr_type)
        return new_node

    @visitor.when(ConditionalNode)
    def visit(self, node: ConditionalNode, scope) -> ConditionalNode:
        new_condition_node = self.visit(node.condition, scope)
        new_then_node = self.visit(node.then_body, scope)
        new_else_node = self.visit(node.else_body, scope)

        join_type = join(
            new_condition_node.inferenced_type, new_else_node.inferenced_type
        )
        decl_type = node.inferenced_type
        expr_type = join_type
        new_node = ConditionalNode(new_then_node, new_then_node, new_else_node, node)
        new_node.inferenced_type = try_conform(decl_type, expr_type)
        return new_node

    @visitor.when(CaseNode)
    def visit(self, node: CaseNode, scope) -> CaseNode:
        new_case_node = self.visit(node.case_expr, scope)
        new_options_nodes = []
        for option in node.options:
            child_scope = scope.create_child()
            new_options_nodes.append(self.visit(option, child_scope))

        join_type = join_list([option.inferenced_type for option in new_options_nodes])

        new_node = CaseNode(new_case_node, new_options_nodes, node)
        decl_type = node.inferenced_type
        expr_type = join_type
        new_node.inferenced_type = try_conform(decl_type, expr_type)
        return new_node

    @visitor.when(CaseOptionNode)
    def visit(self, node: CaseOptionNode, scope) -> CaseOptionNode:
        new_node_expr = self.visit(node.expr, scope)
        new_node = CaseOptionNode(new_node_expr, node)
        decl_type = node.inferenced_type
        expr_type = new_node_expr.inferenced_type
        new_node.inferenced_type = try_conform(decl_type, expr_type)
        return new_node

    @visitor.when(LoopNode)
    def visit(self, node: LoopNode, scope) -> LoopNode:
        new_condition_node = self.visit(node.condition, scope)
        new_body_node = self.visit(node.body, scope)

        new_node = LoopNode(new_condition_node, new_body_node, node)
        decl_type = node.inferenced_type
        expr_type = self.context.get_type("Object")
        new_node.inferenced_type = try_conform(decl_type, expr_type)
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
        new_node.inferenced_type = try_conform(decl_type, expr_type)
        return new_node

    @visitor.when(VarDeclarationNode)
    def visit(self, node: VarDeclarationNode, scope: Scope) -> VarDeclarationNode:
        scope.define_variable(node.id, node.inferenced_type)
        new_expr_node = self.visit(node.expr, scope)
        decl_type = node.inferenced_type
        expr_type = new_expr_node.inferenced_type
        new_node = VarDeclarationNode(node)
        new_node.inferenced_type = try_conform(decl_type, expr_type)
        return new_node

    @visitor.when(AssignNode)
    def visit(self, node: AssignNode, scope) -> AssignNode:
        new_expr_node = self.visit(node.expr, scope)
        if node.defined:
            decl_type = scope.find_variable(node.id).get_type()
        decl_type = node.inferenced_type
        expr_type = new_expr_node.inferenced_type
        new_node = AssignNode(new_expr_node, node)
        new_node.inferenced_type = try_conform(decl_type, expr_type)
        return new_node

    @visitor.when(MethodCallNode)
    def visit(self, node: MethodCallNode, scope) -> MethodCallNode:
        caller_type: Type = node.caller_type.heads[0]
        method: Method = caller_type.get_method(node.id)

        new_args = []
        for arg_expr, param_type in zip(node.args, method.param_types):
            arg_node = self.visit(arg_expr, scope)
            arg_node.inferenced_type = try_conform(arg_node.inferenced_type, param_type)
            new_args.append(arg_node)

        new_expr = self.visit(node.expr,scope) if node.expr else None
        new_node = MethodCallNode(node.caller_type, new_expr, new_args, node)
        new_node.inferenced_type = try_conform(node.inferenced_type, method.return_type)
        return new_node

    @visitor.when(BinaryNode)
    def visit(self, node: BinaryNode, scope) -> BinaryNode:
        new_node = deepcopy(node)
        new_left_node = self.visit(node.left, scope)
        new_right_node = self.visit(node.right, scope)

        new_node.left = new_left_node
        new_node.right = new_right_node

        return new_node

    @visitor.when(UnaryNode)
    def visit(self, node: UnaryNode, scope) -> UnaryNode:
        new_node = deepcopy(node)
        new_expr_node = self.visit(node.expr, scope)

        new_node.expr = new_expr_node
        return new_node

    @visitor.when(VariableNode)
    def visit(self, node: VariableNode, scope: Scope) -> VariableNode:
        new_node = deepcopy(node)
        if node.defined:
            decl_type = node.inferenced_type
            expr_type = scope.find_variable(node.value).get_type()
            new_node.inferenced_type = try_conform(decl_type, expr_type)
            return new_node
        return new_node

    @visitor.when(InstantiateNode)
    def visit(self, node: InstantiateNode, scope) -> InstantiateNode:
        return deepcopy(node)

    @visitor.when(IntNode)
    def visit(self, node, scope) -> IntNode:
        return deepcopy(node)

    @visitor.when(StringNode)
    def visit(self, node, scope) -> StringNode:
        return deepcopy(node)

    @visitor.when(BooleanNode)
    def visit(self, node, scope) -> BooleanNode:
        return deepcopy(node)

    # Este metodo deber ser innecesario pues todos los errores son recogidos previamente
    def add_error(self, node: Node, text: str):
        line, col = node.get_position() if node is not None else (0, 0)
        self.errors.append(((line, col), f"({line}, {col}) - " + text))
