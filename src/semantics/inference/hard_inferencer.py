from semantics.tools.errors import InternalError, AttributeError
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
    DivNode,
    EqualsNode,
    InstantiateNode,
    IntNode,
    IsVoidNode,
    LessNode,
    LessOrEqualNode,
    LetNode,
    LoopNode,
    MethodCallNode,
    MethodDeclarationNode,
    MinusNode,
    Node,
    NotNode,
    PlusNode,
    ProgramNode,
    StarNode,
    StringNode,
    VarDeclarationNode,
    VariableNode,
)
from utils import visitor
from semantics.tools import (
    Context,
    Scope,
    SelfType,
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

        expr_name = expr_type.generate_name()
        node_type = attr_node.inferenced_type
        if not conforms(expr_type, attr_node.inferenced_type):
            self.add_error(
                node,
                (
                    f"TypeError: In class '{self.current_type.name}' attribue"
                    f"'{node.id}' expression type({expr_name}) does not conforms"
                    f"to declared type ({node_type.name})."
                ),
            )

        return attr_node

    @visitor.when(MethodDeclarationNode)
    def visit(self, node, scopex: Scope):
        scope: Scope = scopex.next_child()
        current_method = self.current_type.get_method(node.id)

        for idx, typex in zip(current_method.param_names, current_method.param_types):
            scope.define_variable(idx, typex)

        new_params = []
        for param in node.params:
            new_params.append(self.visit(param, scope))
            # scope.define_variable(param.name, )

        body_node = self.visit(node.body, scope)
        body_type = body_node.inferenced_type
        method_node = MethodDeclarationNode(new_params, node.type, body_node, node)
        method_node.inferenced_type = node.inferenced_type

        if equal(body_type, node.body.inferenced_type):
            return method_node

        node_type = method_node.inferenced_type
        body_name = body_type.generate_name()
        if not conforms(body_type, node_type):
            self.add_error(
                body_node,
                f"TypeError: In Class '{self.current_type.name}' method "
                f"'{method_node.id}' return expression type({body_name})"
                f" does not conforms to declared return type ({node_type.name})",
            )

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

        if_node = ConditionalNode(condition_node, then_node, else_node, node)

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
        opt_node.inferenced_type = expr_node.inferenced_type
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
        var_decl_node.index = node.index
        if node.expr is None:
            var_decl_node.inferenced_type = node.inferenced_type
            return var_decl_node

        expr_node = self.visit(node.expr, scope)
        var_decl_node.expr = expr_node

        node_type = scope.get_local_by_index(node.index).get_type()

        expr_type = expr_node.inferenced_type
        if equal(expr_type, node.expr.inferenced_type):
            expr_clone = expr_type.clone()
            if not conforms(expr_type, node_type):
                self.add_error(
                    node,
                    f"Semantic Error: Variable '{node.id}' expression type"
                    f" ({expr_clone.name}) does not conforms to declared"
                    f" type({node_type.name}).",
                )

        var_decl_node.inferenced_type = expr_node.inferenced_type
        return var_decl_node

    @visitor.when(AssignNode)
    def visit(self, node, scope: Scope):
        expr_node = self.visit(node.expr, scope)
        assign_node = AssignNode(expr_node, node)

        if not node.defined or node.id == "self":
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

        assign_node.inferenced_type = expr_node.inferenced_type
        return assign_node

    @visitor.when(MethodCallNode)
    def visit(self, node, scope):
        caller_type = node.caller_type
        expr_node = None
        if node.type is not None and node.expr is not None:
            expr_node = self.visit(node.expr, scope)
            expr_type = expr_node.inferenced_type
            if not equal(expr_type, node.expr.inferenced_type):
                expr_clone = expr_type.clone()
                if not conforms(expr_type, caller_type):
                    self.add_error(
                        node,
                        f"SemanticError: Cannot effect dispatch because expression"
                        f" type({expr_clone.name}) does not conforms to "
                        f" caller type({caller_type.name}).",
                    )
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
            elif len(caller_type.heads) == 0:
                self.add_error(
                    node,
                    f" SemanticError: There is no method called {node.id} which takes"
                    f" {len(node.args)} paramters.",
                )

        if len(caller_type.heads) != 1:
            new_args = []
            infered_type = TypeBag(set())
        else:
            caller = caller_type.heads[0]
            caller = self.current_type if isinstance(caller, SelfType) else caller
            try:
                method = caller.get_method(node.id)
            except AttributeError as err:
                # self.add_error(node, err.text) Error notified in soft inferencer
                new_args = []
                infered_type = TypeBag(set())
            else:
                if len(node.args) != len(method.param_types):
                    self.add_error(
                        node,
                        f"SemanticError: Method '{node.id}' from class "
                        f"'{caller_type.name}' takes {len(method.param_types)}"
                        f" positional arguments but {len(node.args)} were given.'",
                    )

                decl_return_type = method.return_type.clone()
                decl_return_type.swap_self_type(caller)
                type_set = set()
                heads = []
                type_set = smart_add(type_set, heads, decl_return_type)

                new_args = []
                for i in range(len(node.args)):
                    new_args.append(self.visit(node.args[i], scope))
                    if i < len(method.param_types):
                        arg_type: TypeBag = new_args[-1].inferenced_type
                        added_type = arg_type.add_self_type(self.current_type)
                        arg_name = arg_type.generate_name()
                        param_type = method.param_types[i]
                        if not conforms(arg_type, param_type):
                            self.add_error(
                                new_args[-1],
                                f"TypeError: Argument expression type({arg_name}) does"
                                f" not conforms parameter declared type({param_type.name})",
                            )
                        if added_type:
                            arg_type.remove_self_type(self.current_type)
                infered_type = TypeBag(type_set, heads)

        call_node = MethodCallNode(caller_type, expr_node, new_args, node)
        call_node.inferenced_type = infered_type
        return call_node

    @visitor.when(ArithmeticNode)
    def visit(self, node, scope):
        left_node, right_node = self.__arithmetic_operation(node, scope)
        if isinstance(node, PlusNode):
            arith_node = PlusNode(left_node, right_node, node)
        elif isinstance(node, MinusNode):
            arith_node = MinusNode(left_node, right_node, node)
        elif isinstance(node, StarNode):
            arith_node = StarNode(left_node, right_node, node)
        elif isinstance(node, DivNode):
            arith_node = DivNode(left_node, right_node, node)
        arith_node.inferenced_type = self.context.get_type("Int")
        return arith_node

    @visitor.when(LessNode)
    def visit(self, node, scope: Scope):
        left_node, right_node = self.__arithmetic_operation(node, scope)
        less_node = LessNode(left_node, right_node, node)
        less_node.inferenced_type = self.context.get_type("Bool")
        return less_node

    @visitor.when(LessOrEqualNode)
    def visit(self, node, scope: Scope):
        left_node, right_node = self.__arithmetic_operation(node, scope)
        lesseq_node = LessOrEqualNode(left_node, right_node, node)
        lesseq_node.inferenced_type = self.context.get_type("Bool")
        return lesseq_node

    @visitor.when(EqualsNode)
    def visit(self, node, scope):
        left_node = self.visit(node.left, scope)
        right_node = self.visit(node.right, scope)

        self.__check_member_types(left_node, right_node)

        eq_node = EqualsNode(left_node, right_node, node)
        eq_node.inferenced_type = node.inferenced_type  # Bool Type :)
        return eq_node

    @visitor.when(VariableNode)
    def visit(self, node, scope: Scope):
        var_node = VariableNode(node)
        if not node.defined:
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
                    " conforms to Int type",
                )

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

    def __check_member_types(self, left_node, right_node):
        if self.__unrelated_types(left_node) or self.__unrelated_types(right_node):
            return

        bag1: TypeBag = left_node.inferenced_type
        bag2: TypeBag = right_node.inferenced_type

        u_obj = self.context.get_type("Object", unpacked=True)
        u_int = self.context.get_type("Int", unpacked=True)
        u_bool = self.context.get_type("Bool", unpacked=True)
        u_string = self.context.get_type("String", unpacked=True)

        contains_obj = u_obj in bag1.type_set and u_obj in bag2.type_set
        contains_int = u_int in bag1.type_set and u_int in bag2.type_set
        contains_bool = u_bool in bag1.type_set and u_bool in bag2.type_set
        contains_string = u_string in bag1.type_set and u_string in bag2.type_set

        if contains_obj or (
            (contains_int and not (contains_bool or contains_string))
            and (contains_bool and not (contains_int or contains_string))
            and (contains_string and not (contains_int or contains_bool))
        ):
            if contains_obj:
                self.__conform_to_type(left_node, TypeBag({u_obj}))
                self.__conform_to_type(right_node, TypeBag({u_obj}))
            elif contains_int:
                self.__conform_to_type(left_node, TypeBag({u_int}))
                self.__conform_to_type(right_node, TypeBag({u_int}))
            elif contains_bool:
                self.__conform_to_type(left_node, TypeBag({u_bool}))
                self.__conform_to_type(right_node, TypeBag({u_bool}))
            elif contains_string:
                self.__conform_to_type(left_node, TypeBag({u_string}))
                self.__conform_to_type(right_node, TypeBag({u_string}))
            else:
                raise InternalError(
                    "Compiler is not working correctly(HardInferencer.__check_member_types)"
                )
        else:
            basic_set = {u_int, u_bool, u_string}
            if len(bag1.type_set.intersection(basic_set)) == 1:
                self.__conform_to_type(right_node, bag1)
            elif len(bag2.type_set.intersection(basic_set)) == 1:
                self.__conform_to_type(left_node, bag2)

    def __conform_to_type(self, node: Node, bag: TypeBag):
        node_type = node.inferenced_type
        node_name = node_type.generate_name()
        if not conforms(node_type, bag):
            self.add_error(
                node,
                f"TypeError: Equal Node: Expression type({node_name})"
                f"does not conforms to expression({bag.name})",
            )

    def __arithmetic_operation(self, node, scope):
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

        if not equal(right_type, node.right.inferenced_type):
            right_clone = right_type.clone()
            if not conforms(right_type, int_type):
                self.add_error(
                    node.right,
                    f"TypeError: Arithmetic Error: Right member "
                    f"type({right_clone.name})does not conforms to Int type.",
                )

        return left_node, right_node

    def __unrelated_types(self, node):
        typex: TypeBag = node.inferenced_type
        if typex.error_type:
            return True
        if len(typex.heads) > 1:
            self.add_error(
                node,
                "AutotypeError: AUTO_TYPE is ambigous {"
                + ", ".join(typez.name for typez in typex.heads),
                +"}",
            )
            node.inferenced_type = TypeBag(set())
            return True
        return False