from ast.inferencer_ast import (
    ArithmeticNode,
    AssignNode,
    AttrDeclarationNode,
    BlocksNode,
    BooleanNode,
    CaseNode,
    CaseOptionNode,
    ClassDeclarationNode,
    ComparerNode,
    ComplementNode,
    ConditionalNode,
    InstantiateNode,
    IntNode,
    IsVoidNode,
    LetNode,
    LoopNode,
    MethodCallNode,
    MethodDeclarationNode,
    Node,
    NotNode,
    ProgramNode,
    StringNode,
    VarDeclarationNode,
    VariableNode,
)
from utils import visitor
from semantics.tools import (
    Context,
    ErrorType,
    Scope,
    TypeBag,
    conforms,
    equal,
    join,
    join_list,
    smart_add,
)


class HardInferencer:
    def __init__(self, context: Context) -> None:
        self.context = context
        self.errors = []
        self.pos = set()
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

        scope.reset()
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
        attr_node.inferenced_type = node.inferenced_type

        if not node.expr:
            return attr_node

        expr_node = self.visit(node.expr, scope)
        expr_type = expr_node.inferenced_type

        attr_node.expr = expr_node
        if equal(expr_type, node.expr.inferenced_type):
            return attr_node

        expr_clone = expr_type.clone()
        node_type = attr_node.inferenced_type
        if not conforms(expr_type, attr_node.inferenced_type):
            self.add_error(
                node,
                (
                    f"TypeError: In class '{self.current_type.name}' attribue"
                    f"'{node.id}' expression type({expr_clone.name}) does not conforms"
                    f"to declared type ({node_type.name})."
                ),
            )
            expr_node.inferenced_type = ErrorType()

        return attr_node

    @visitor.when(MethodDeclarationNode)
    def visit(self, node, scopex: Scope):
        scope = scopex.next_child()

        body_node = self.visit(node.body, scope)
        body_type = body_node.inferenced_type
        method_node = MethodDeclarationNode(node.type, body_node, node)
        method_node.inferenced_type = node.inferenced_type

        if equal(body_type, node.body.inferenced_type):
            return method_node

        node_type = method_node.inferenced_type
        body_clone = body_type.clone()
        if not conforms(body_type, node_type):
            self.add_error(
                node,
                f"TypeError: In Class '{self.current_type.name}' method "
                f"'{method_node.id}' return expression type({body_clone.name})"
                f" does not conforms to declared return type ({node_type.name})",
            )
            body_node.inferenced_type = ErrorType()

        return method_node

    @visitor.when(BlocksNode)
    def visit(self, node, scope):
        new_expr_list = []
        for expr in node.expr_list:
            new_expr_list.append(self.visit(expr, scope))

        block_node = BlocksNode(new_expr_list, node)
        block_node.inferenced_type = block_node.expr_list[-1].inferenced_type
        return block_node

    @visitor.when(ConditionalNode)
    def visit(self, node, scope):
        condition_node = self.visit(node.condition, scope)
        then_node = self.visit(node.then_body, scope)
        else_node = self.visit(node.else_body, scope)

        condition_type = condition_node.inferenced_type
        if not equal(condition_type, node.condition.inferenced_type):
            condition_clone = condition_type.clone()
            bool_type = self.context.get_type("Bool")
            if not conforms(condition_type, bool_type):
                self.add_error(
                    node,
                    f"TypeError: If's condition type({condition_clone.name})"
                    " does not conforms to Bool type.",
                )
                condition_node.inferenced_type = ErrorType()

        if_node = ConditionalNode(condition_node, then_node, else_node)

        if not equal(
            then_node.inferenced_type, node.then_body.inferenced_type
        ) or not equal(else_node.inferenced_type, node.else_body.inferenced_type):
            then_type = then_node.inferenced_type
            else_type = else_node.inferenced_type
            joined_type = join(then_type, else_type)
        else:
            joined_type = node.inferenced_type

        if_node.inferenced_type = joined_type
        return if_node

    @visitor.when(CaseNode)
    def visit(self, node, scope: Scope):
        expr_node = self.visit(node.case_expr, scope)

        type_list = []
        new_options = []
        for option in node.options:
            child = scope.next_child()
            new_options.append(self.visit(option, child))
            type_list.append(new_options[-1].inferenced_type)

        join_type = join_list(type_list)
        case_node = CaseNode(expr_node, new_options, node)
        case_node.inferenced_type = join_type
        return case_node

    @visitor.when(CaseOptionNode)
    def visit(self, node, scope: Scope):
        expr_node = self.visit(node.expr, scope)
        opt_node = CaseOptionNode(expr_node, node)
        return opt_node

    @visitor.when(LoopNode)
    def visit(self, node, scope):
        condition_node = self.visit(node.condition, scope)
        condition_type = condition_node.inferenced_type

        if not equal(condition_type, node.condition.inferenced_type):
            bool_type = self.context.get_type("Bool")
            condition_clone = condition_type.clone()
            if not conforms(condition_type, bool_type):
                self.add_error(
                    node,
                    f"TypeError: Loop condition type({condition_clone.name})"
                    " does not conforms to Bool type.",
                )
                condition_node.inferenced_type = ErrorType()

        body_node = self.visit(node.body, scope)
        loop_node = LoopNode(condition_node, body_node, node)
        loop_node.inferenced_type = node.inferenced_type
        return loop_node

    @visitor.when(LetNode)
    def visit(self, node, scope: Scope):
        child = scope.next_child()

        new_decl_list = []
        for var in node.var_decl_list:
            new_decl_list.append(self.visit(var, child))

        in_expr_node = self.visit(node.in_expr, child)

        let_node = LetNode(new_decl_list, in_expr_node, node)
        let_node.inferenced_type = in_expr_node.inferenced_type
        return let_node

    @visitor.when(VarDeclarationNode)
    def visit(self, node, scope: Scope):
        var_decl_node = VarDeclarationNode(node)
        if node.expr is None:
            var_decl_node.inferenced_type = node.inferenced_type
            return var_decl_node

        expr_node = self.visit(node.expr, scope)
        var_decl_node.expr = expr_node

        if not node.defined:
            var_decl_node.inferenced_type = ErrorType()
            return var_decl_node

        var_decl_node.defined = True
        node_type = scope.find_variable(node.id).get_type()

        expr_type = expr_node.inferenced_type
        if equal(expr_type, node.expr.inferenced_type):
            expr_clone = expr_type.clone()
            if not conforms(expr_type, node_type):
                self.add_error(
                    node,
                    f"Semantic Error: Variable '{node.id}' expressiontype"
                    f"({expr_clone.name}) does not conforms to declared"
                    f"type({node_type.name}).",
                )
                expr_node.inferenced_type = ErrorType()

        var_decl_node.inferenced_type = node_type
        return var_decl_node

    @visitor.when(AssignNode)
    def visit(self, node, scope: Scope):
        expr_node = self.visit(node.expr, scope)
        assign_node = AssignNode(expr_node, node)

        if not node.defined or node.id == "self":
            assign_node.inferenced_type = ErrorType()
            return assign_node

        assign_node.defined = True

        decl_type = scope.find_variable(node.id).get_type()
        expr_type = expr_node.inferenced_type
        if not equal(expr_type, node.expr.inferenced_type):
            expr_clone = expr_type.clone()
            if not conforms(expr_type, decl_type):
                self.add_error(
                    node,
                    f"TypeError: Cannot assign new value to variable '{node.id}'."
                    f" Expression type({expr_clone.name}) does not conforms to"
                    f" declared type ({decl_type.name}).",
                )
                expr_node.inferenced_type = ErrorType()

        assign_node.inferenced_type = decl_type
        return assign_node

    @visitor.when(MethodCallNode)
    def visit(self, node, scope):
        caller_type = node.caller_type
        expr_node = None
        if node.type is not None and node.expr is not None:
            expr_node = self.visit(node.expr, scope)
            expr_type = expr_node.inferenced_type
            if not equal(expr_type, node.expression.inferenced_type):
                expr_clone = expr_type.clone()
                if not conforms(expr_type, caller_type):
                    self.add_error(
                        node,
                        f"SemanticError: Cannot effect dispatch because expression"
                        f"type({expr_clone.name}) does not conforms to "
                        f"caller type({caller_type.name}).",
                    )
                    caller_type = ErrorType()
        elif node.expr is not None:
            expr_node = self.visit(node.expr, scope)
            caller_type = expr_node.inferenced_type

        if len(caller_type.type_set) > 1:
            methods_by_name = self.context.get_method_by_name(node.id, len(node.args))
            types = [typex for typex, _ in methods_by_name]
            conforms(caller_type, TypeBag(set(types), types))
            if len(caller_type.heads) > 1:
                error = (
                    f"SemanticError: Method '{node.id}' found in"
                    f" {len(caller_type.heads)} unrelated types:\n"
                )
                error += "   -Found in: "
                error += ", ".join(typex.name for typex in caller_type.heads)
                self.add_error(node, error)
                caller_type = ErrorType()
            elif len(caller_type.heads) == 0:
                self.add_error(
                    node,
                    f" SemanticError: There is no method called {node.id} which takes"
                    f" {len(node.args)} paramters.",
                )
                caller_type = ErrorType()

        if len(caller_type.heads) == 1:
            caller = caller_type.heads[0]
            method = caller.get_method(node.id)

            if len(node.args) != len(method.param_types):
                self.add_error(
                    node,
                    f"SemanticError: Method '{node.id}' from class "
                    f"'{caller_type.name}' takes {len(node.args)} arguments but"
                    f" {method.param_types} were given.'",
                )
                node.inferenced_type = ErrorType()

            decl_return_type = method.return_type.clone()
            decl_return_type.swap_self_type(caller)
            type_set = set()
            heads = []
            type_set = smart_add(type_set, heads, decl_return_type)

            new_args = []
            for i in range(len(node.args)):
                new_args.append(self.visit(node.args[i], scope))

                arg_type = new_args[-1].inferenced_type
                arg_clone = arg_type.clone()
                param_type = method.param_types[i]
                if not conforms(arg_type, param_type):
                    self.add_error(
                        new_args[-1],
                        f"TypeError: Argument expression type({arg_clone.name}) does"
                        f" not conforms parameter declared type({param_type.name})",
                    )
            infered_type = TypeBag(type_set, heads)
        else:
            new_args = []
            infered_type = ErrorType()

        call_node = MethodCallNode(caller_type, expr_node, new_args, node)
        call_node.inferenced_type = infered_type
        return call_node

    @visitor.when(ArithmeticNode)
    def visit(self, node, scope):
        left_node = self.visit(node.left, scope)
        left_type = left_node.inferenced_type

        right_node = self.visit(node.right, scope)
        right_type = right_node.inferenced_type

        int_type = self.context.get_type("Int")
        if not equal(left_type, node.left.inferenced_type):
            if not conforms(left_type, int_type):
                left_clone = left_type.clone()
                self.add_error(
                    node.left,
                    f"TypeError: Arithmetic Error: Left member type({left_clone.name})"
                    "does not conforms to Int type.",
                )
                left_node.inferenced_type = ErrorType()
        if not equal(right_type, node.right.inferenced_type):
            right_clone = right_type.clone()
            if not conforms(right_type, int_type):
                self.add_error(
                    node.right,
                    f"Type Error: Arithmetic Error: Right member "
                    f"type({right_clone.name})does not conforms to Int type.",
                )
                right_node.inferenced_type = ErrorType()

        arith_node = ArithmeticNode(left_node, right_node, node)
        arith_node.inferenced_type = int_type
        return arith_node

    @visitor.when(ComparerNode)
    def visit(self, node, scope):
        left_node = self.visit(node.left, scope)
        left_type = left_node.inferenced_type

        right_node = self.visit(node.right, scope)
        right_type = right_node.inferenced_type

        if not equal(left_type, node.left.inferenced_type):
            if not conforms(left_type, right_type):
                left_clone = left_type.clone()
                self.add_error(
                    node.left,
                    f"TypeError: Comparer Error: Left expression"
                    f" type({left_clone.name}) "
                    f" does not conforms to right expression type ({right_type.name}).",
                )
                left_node.inferenced_type = ErrorType()

        if not equal(right_type, node.right.inferenced_type):
            right_clone = right_type.clone()
            if not conforms(right_type, left_type):
                self.add_error(
                    node.right,
                    f"TypeError: Comparer Error: Right expression"
                    f" type({right_clone.name})"
                    f" does not conforms to left expression type ({left_type.name}).",
                )
                right_node.inferenced_type = ErrorType()

        comparer = ComparerNode(left_node, right_node)
        comparer.inferenced_type = node.inferenced_type  # Bool Type :)
        return comparer

    @visitor.when(VariableNode)
    def visit(self, node, scope: Scope):
        var_node = VariableNode(node)
        if not node.defined:
            var_node.inferenced_type = ErrorType()
            return var_node

        var_node.defined = True
        var = scope.find_variable(node.value)
        var_node.inferenced_type = var.get_type()
        return var_node

    @visitor.when(NotNode)
    def visit(self, node, scope):
        expr_node = self.visit(node.expr, scope)
        expr_type = expr_node.inferenced_type
        bool_type = self.context.get_type("Bool")
        if not equal(expr_type, node.expr.inferenced_type):
            expr_clone = expr_type.clone()
            if not conforms(expr_type, bool_type):
                self.add_error(
                    node,
                    f"TypeError: Not's expresion type({expr_clone.name} does not"
                    " conforms to Bool type",
                )
                expr_node.inferenced_type = ErrorType()

        not_node = NotNode(expr_node, node)
        not_node.inferenced_type = bool_type
        return not_node

    @visitor.when(ComplementNode)
    def visit(self, node, scope):
        expr_node = self.visit(node.expr, scope)
        expr_type = expr_node.inferenced_type
        int_type = self.context.get_type("Int")
        if not equal(expr_type, node.expr.inferenced_type):
            expr_clone = expr_type.clone()
            if not conforms(expr_type, int_type):
                self.add_error(
                    node,
                    f"TypeError: ~ expresion type({expr_clone.name} does not"
                    " conforms to Bool type",
                )
                expr_node.inferenced_type = ErrorType()

        complement_node = ComplementNode(expr_node, node)
        complement_node.inferenced_type = int_type
        return complement_node

    @visitor.when(IsVoidNode)
    def visit(self, node, scope):
        node_expr = self.visit(node.expr, scope)
        is_void_node = IsVoidNode(node_expr, node)
        is_void_node.inferenced_type = self.context.get_type("Bool")
        return is_void_node

    @visitor.when(InstantiateNode)
    def visit(self, node, scope):
        instantiate_node = InstantiateNode(node)
        instantiate_node.inferenced_type = node.inferenced_type
        return instantiate_node

    @visitor.when(IntNode)
    def visit(self, node, scope):
        int_node = IntNode(node)
        int_node.inferenced_type = self.context.get_type("Int")
        return int_node

    @visitor.when(StringNode)
    def visit(self, node, scope):
        str_node = StringNode(node)
        str_node.inferenced_type = self.context.get_type("String")
        return str_node

    @visitor.when(BooleanNode)
    def visit(self, node, scope):
        bool_node = BooleanNode(node)
        bool_node.inferenced_type = self.context.get_type("Bool")
        return bool_node

    def add_error(self, node: Node, text: str):
        line, col = node.get_position() if node else (0, 0)
        if (line, col) in self.pos:
            return
        self.pos.add((line, col))
        self.errors.append(((line, col), f"({line}, {col}) - " + text))
