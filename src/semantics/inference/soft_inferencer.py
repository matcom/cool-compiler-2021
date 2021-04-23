import ast.inferencer_ast as inf_ast
from ast.parser_ast import (
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
from semantics.errors import SemanticError
from semantics.tools import (
    Context,
    ErrorType,
    Scope,
    TypeBag,
    conforms,
    join,
    join_list,
    smart_add,
)


class SoftInferencer:
    def __init__(self, context: Context) -> None:
        self.context = context
        self.errors = []
        self.current_type = None

    @visitor.on("node")
    def visit(self, node, scope):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node: ProgramNode) -> inf_ast.ProgramNode:
        scope = Scope()
        new_declaration = []
        for declaration in node.declarations:
            new_declaration.append(self.visit(declaration, scope.create_child()))

        program = inf_ast.ProgramNode(new_declaration, scope, node)
        return program

    @visitor.when(ClassDeclarationNode)
    def visit(self, node: ClassDeclarationNode, scope: Scope) -> ClassDeclarationNode:
        self.current_type = self.context.get_type(node.id, unpacked=True)
        scope.define_variable("self", TypeBag({self.current_type}))

        for attr in self.current_type.attributes:
            scope.define_variable(attr.name, attr.type)

        new_features = []
        for feature in node.features:
            new_features.append(self.visit(feature, scope))

        class_node = inf_ast.ClassDeclarationNode(new_features, node)
        return class_node

    @visitor.when(AttrDeclarationNode)
    def visit(self, node, scope):
        node_type = self.current_type.get_attribute(node.id).type.swap_self_type(
            self.current_type
        )

        attr_node = inf_ast.AttrDeclarationNode(node)
        if not node.expr:
            attr_node.inferenced_type = node_type
            return attr_node

        expr_node = self.visit(node.expr, scope)

        node_expr = expr_node.inferenced_type

        expr_clone = node_expr.clone()
        if not conforms(node_expr, node_type):
            self.add_error(
                node,
                (
                    f"TypeError: In class '{self.current_type.name}' attribue"
                    f"'{node.id}' expression type({expr_clone.name}) does not conforms"
                    f"to declared type ({node_type.name})."
                ),
            )
            expr_node.inferenced_type = ErrorType()
        attr_node.expr = expr_node
        attr_node.inferenced_type = node_type
        return attr_node

    @visitor.when(MethodDeclarationNode)
    def visit(self, node, scopex: Scope):
        scope = scopex.create_child()
        current_method = self.current_type.get_method(node.id)

        for idx, typex in zip(current_method.param_names, current_method.param_types):
            scope.define_variable(idx, typex)

        ret_type_decl = current_method.return_type.swap_self_type(self.current_type)
        body_node = self.visit(node.body, scope)

        ret_type_expr = body_node.inferenced_type
        ret_expr_clone = ret_type_expr.clone()
        if not conforms(ret_type_expr, ret_type_decl):
            self.add_error(
                node,
                f"TypeError: In Class '{self.current_type.name}' method"
                f" '{current_method.name}' return expression type({ret_expr_clone.name})"
                f" does not conforms to declared return type ({ret_type_decl.name})",
            )
            body_node.inferenced_type = ErrorType()

        ret_type_decl.swap_self_type(self.current_type, back=True)

        method_node = inf_ast.MethodDeclarationNode(node.type, body_node, node)
        method_node.inferenced_type = ret_type_decl
        return method_node

    @visitor.when(BlocksNode)
    def visit(self, node, scope):
        new_expr_list = []
        for expr in node.expr_list:
            new_expr_list.append(self.visit(expr, scope))

        block_node = inf_ast.BlocksNode(new_expr_list, node)
        block_node.inferenced_type = block_node.expr_list[-1].inferenced_type
        return block_node

    @visitor.when(ConditionalNode)
    def visit(self, node, scope):
        condition_node = self.visit(node.condition, scope)

        condition_type = condition_node.inferenced_type
        bool_type = self.context.get_type("Bool")

        condition_clone = condition_type.clone()
        if not conforms(condition_type, bool_type):
            self.add_error(
                node,
                f"TypeError: If's condition type({condition_clone.name})"
                " does not conforms to Bool type.",
            )
            condition_node.inferenced_type = ErrorType()

        then_node = self.visit(node.then_body, scope)
        else_node = self.visit(node.else_body, scope)

        if_node = inf_ast.ConditionalNode(condition_node, then_node, else_node, node)

        then_type = then_node.inferenced_type
        else_type = else_node.inferenced_type
        joined_type = join(then_type, else_type)

        if_node.inferenced_type = joined_type
        return if_node

    @visitor.when(CaseNode)
    def visit(self, node, scope: Scope):
        expr_node = self.visit(node.case_expr, scope)

        types_visited = set()
        type_list = []
        new_options = []
        for option in node.options:
            child = scope.create_child()
            new_options.append(self.visit(option, child))
            type_list.append(new_options[-1].inferenced_type)
            var_type = child.find_variable(option.id).type
            if var_type in types_visited:
                self.add_error(
                    node,
                    "SemanticError: Case Expression can't have branches"
                    f"with same case type({var_type.name})",
                )

        joined_type = join_list(type_list)

        case_node = inf_ast.CaseNode(expr_node, new_options, node)
        case_node.inferenced_type = joined_type
        return case_node

    @visitor.when(CaseOptionNode)
    def visit(self, node, scope: Scope):
        try:
            node_type = self.context.get_type(node.type, selftype=False, autotype=False)
        except SemanticError as err:
            self.add_error(node, err)
            node_type = ErrorType()

        scope.define_variable(node.id, node_type)
        expr_node = self.visit(node.expr, scope)

        case_opt_node = inf_ast.CaseOptionNode(expr_node, node)
        case_opt_node.inferenced_type = expr_node.inferenced_type
        return case_opt_node

    @visitor.when(LoopNode)
    def visit(self, node, scope):
        condition_node = self.visit(node.condition, scope)
        condition_type = condition_node.inferenced_type

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
        loop_node = inf_ast.LoopNode(condition_node, body_node, node)
        loop_node.inferenced_type = self.context.get_type("Object")
        return loop_node

    @visitor.when(LetNode)
    def visit(self, node, scope: Scope):
        child = scope.create_child()

        new_decl_list = []
        for var in node.var_decl_list:
            new_decl_list.append(self.visit(var, child))

        in_expr_node = self.visit(node.in_expr, child)

        let_node = inf_ast.LetNode(new_decl_list, in_expr_node, node)
        let_node.inferenced_type = in_expr_node.inferenced_type
        return let_node

    @visitor.when(VarDeclarationNode)
    def visit(self, node, scope: Scope):
        var_decl_node = inf_ast.VarDeclarationNode(node)

        try:
            node_type = self.context.get_type(node.type).swap_self_type(
                self.current_type
            )
        except SemanticError as err:
            node_type = ErrorType()
            self.add_error(node, err)

        if not scope.is_local(node.id):
            scope.define_variable(node.id, node_type)
            var_decl_node.defined = True
        else:
            self.add_error(
                node,
                f"SemanticError: Variable '{node.id}' already defined"
                " in current scope.",
            )
            node_type = ErrorType()

        var_decl_node.inferenced_type = node_type

        if node.expr:
            expr_node = self.visit(node.expr, scope)
            expr_type = expr_node.inferenced_type
            expr_clone = expr_type.clone()
            if not conforms(expr_type, node_type):
                self.add_error(
                    node,
                    f"TypeError: Variable '{node.id}' expressiontype"
                    f"({expr_clone.name}) does not conforms to declared"
                    f"type({node_type.name}).",
                )
                expr_node.inferenced_type = ErrorType()
            var_decl_node.expr = expr_node

        return var_decl_node

    @visitor.when(AssignNode)
    def visit(self, node, scope: Scope):
        expr_node = self.visit(node.expr, scope)
        assign_node = inf_ast.AssignNode(expr_node, node)

        var = scope.find_variable(node.id)
        if not var:
            self.add_error(
                node,
                f"ScopeError: Cannot assign new value to"
                f"{node.id} beacuse it is not defined in the current scope",
            )
            decl_type = ErrorType()
        else:
            decl_type = var.type.swap_self_type(self.current_type)
            assign_node.defined = True

        if var is not None:
            if var.name == "self":
                self.add_error(
                    node,
                    "SemanticError: Cannot assign new value. "
                    "Variable 'self' is Read-Only.",
                )
                decl_type = ErrorType()

            expr_type = expr_node.inferenced_type
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
        if node.expr is None:
            expr_node = None
            caller_type = TypeBag({self.current_type})
        elif node.type is None:
            expr_node = self.visit(node.expr, scope)
            caller_type = expr_node.inferenced_type
        else:
            expr_node = self.visit(node.expr, scope)
            expr_type = expr_node.inferenced_type
            caller_type = self.context.get_type(
                node.type, selftype=False, autotype=False
            )
            expr_clone = expr_type.clone()
            if not conforms(expr_type, caller_type):
                self.add_error(
                    node,
                    f"TypeError: Cannot effect dispatch because expression"
                    f"type({expr_clone.name}) does not conforms to "
                    f"caller type({caller_type.name}).",
                )
                caller_type = ErrorType()

        methods = None
        if len(caller_type.type_set) > 1:
            methods_by_name = self.context.get_method_by_name(node.id, len(node.args))
            types = [typex for typex, _ in methods_by_name]
            conforms(caller_type, TypeBag(set(types), types))
            if len(caller_type.type_set):
                methods = [
                    (typex, typex.get_method(node.id)) for typex in caller_type.heads
                ]
            else:
                self.add_error(
                    node,
                    f"SemanticError: There is no method '{node.id}'"
                    f"that recieves {len(node.params)} arguments in"
                    f"types {caller_type.name}.",
                )
                caller_type = ErrorType()
        elif len(caller_type.type_set) == 1:
            caller = caller_type.heads[0]
            try:
                methods = [(caller, caller.get_method(node.id))]
            except SemanticError:
                self.add_error(
                    node,
                    f"SemanticError: There is no method '{node.id}'"
                    f"that recieves {len(node.params)} arguments in"
                    f"Type '{caller.name}'.",
                )
                caller_type = ErrorType()

        new_args = []
        for i in range(len(node.args)):
            new_args.append(self.visit(node.args[i], scope))

        method_call_node = inf_ast.MethodCallNode(
            caller_type, expr_node, new_args, node
        )

        if methods:
            type_set = set()
            heads = []
            for typex, method in methods:
                ret_type = method.return_type.clone()
                ret_type.swap_self_type(typex)
                type_set = smart_add(type_set, heads, ret_type)
            method_call_node.inferenced_type = TypeBag(type_set, heads)
        else:
            # Errors already notified previuosly
            method_call_node.inferenced_type = ErrorType()

        return method_call_node

    @visitor.when(ArithmeticNode)
    def visit(self, node, scope):
        left_node = self.visit(node.left, scope)
        left_type = left_node.inferenced_type
        left_clone = left_type.clone()

        right_node = self.visit(node.right, scope)
        right_type = right_node.inferenced_type
        right_clone = right_type.clone()

        int_type = self.context.get_type("Int")
        if not conforms(left_type, int_type):
            self.add_error(
                node.left,
                f"TypeError: ArithmeticError: Left member type({left_clone.name})"
                " does not conforms to Int type.",
            )
            left_node.inferenced_type = ErrorType()
        if not conforms(right_type, int_type):
            self.add_error(
                node.right,
                f"TypeError: ArithmeticError: Right member type({right_clone.name})"
                " does not conforms to Int type.",
            )
            right_node.inferenced_type = ErrorType()

        arith_node = inf_ast.ArithmeticNode(left_node, right_node, node)
        arith_node.inferenced_type = int_type
        return arith_node

    @visitor.when(ComparerNode)
    def visit(self, node, scope):
        left_node = self.visit(node.left, scope)
        left_type = left_node.inferenced_type
        left_clone = left_type.clone()

        right_node = self.visit(node.right, scope)
        right_type = right_node.inferenced_type
        right_clone = right_type.clone()

        if not conforms(left_type, right_type):
            self.add_error(
                node,
                f"TypeError: Left expression type({left_clone.name})"
                f"does not conforms to right expression type({right_type.name})",
            )
            left_node.inferenced_type = ErrorType()
        elif not conforms(right_type, left_type):
            self.add_error(
                node,
                f"TypeError: Right expression type({right_clone.name})"
                f"does not conforms to left expression type({left_type.name})",
            )
            right_node.inferenced_type = ErrorType()

        comparer_node = inf_ast.ComparerNode(left_node, right_node, node)
        comparer_node.inferenced_type = self.context.get_type("Bool")
        return comparer_node

    @visitor.when(VariableNode)
    def visit(self, node, scope: Scope):
        var_node = inf_ast.VariableNode(node)

        var = scope.find_variable(node.value)
        if var:
            var_node.defined = True
            var_type = var.get_type()
        else:
            var_type = ErrorType()
            self.add_error(
                node, f"SemanticError: Variable '{node.value}' is not defined."
            )
        var_node.inferenced_type = var_type
        return var_node

    @visitor.when(NotNode)
    def visit(self, node, scope):
        expr_node = self.visit(node.expr, scope)

        expr_type = expr_node.inferenced_type
        expr_clone = expr_type.clone()
        bool_type = self.context.get_type("Bool")
        if not conforms(expr_type, bool_type):
            self.add_error(
                node,
                f"TypeError: Not's expresion type({expr_clone.name} does not"
                " conforms to Bool type",
            )
            expr_node.inferenced_type = ErrorType()

        not_node = inf_ast.NotNode(expr_node, node)
        not_node.inferenced_type = bool_type
        return not_node

    @visitor.when(ComplementNode)
    def visit(self, node, scope):
        expr_node = self.visit(node.expr, scope)

        expr_type = expr_node.inferenced_type
        expr_clone = expr_type.clone()
        int_type = self.context.get_type("Int")
        if not conforms(expr_type, int_type):
            self.add_error(
                node,
                f"TypeError: ~ expresion type({expr_clone.name} does not"
                " conforms to Int type",
            )
            expr_node.inferenced_type = ErrorType()

        complement_node = inf_ast.ComplementNode(expr_node, node)
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
        instantiate_node = inf_ast.InstantiateNode(node)
        try:
            node_type = self.context.get_type(
                node.value, selftype=False, autotype=False
            )
        except SemanticError as err:
            self.add_error(
                node,
                err.text + f" Could not instantiate type '{node.value}'.",
            )
            node_type = ErrorType()
        instantiate_node.inferenced_type = node_type
        return instantiate_node

    @visitor.when(IntNode)
    def visit(self, node, scope):
        int_node = inf_ast.IntNode(node)
        int_node.inferenced_type = self.context.get_type("Int")
        return int_node

    @visitor.when(StringNode)
    def visit(self, node, scope):
        str_node = inf_ast.StringNode(node)
        str_node.inferenced_type = self.context.get_type("String")
        return str_node

    @visitor.when(BooleanNode)
    def visit(self, node, scope):
        bool_node = inf_ast.BooleanNode(node)
        bool_node.inferenced_type = self.context.get_type("Bool")
        return bool_node

    def add_error(self, node: Node, text: str):
        line, col = node.get_position() if node else (0, 0)
        self.errors.append(((line, col), f"({line}, {col}) - " + text))
