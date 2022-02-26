from inspect import currentframe
from typing import Type
import app.semantics.inference.inferencer_ast as inf_ast
from app.parser.ast import *

import app.utils.visitor as visitor
from app.semantics.tools.errors import SemanticError, AttributeError
from app.semantics.tools import (
    Context,
    Scope,
    SelfType,
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
        self.current_type: Type = None

    @visitor.on("node")
    def visit(self, node, scope):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node: ProgramNode) -> inf_ast.ProgramNode:
        scope = Scope()
        new_classes = []
        for declaration in node.classes:
            new_classes.append(self.visit(
                declaration, scope.create_child()))

        program = inf_ast.ProgramNode(new_classes, scope, node)
        return program

    @visitor.when(ClassNode)
    def visit(self, node: ClassNode, scope: Scope) -> ClassNode:
        self.current_type = self.context.get_type(node.id, unpacked=True)
        scope.define_variable("self", self.context.get_type("SELF_TYPE"))

        for attr in self.current_type.attributes:
            if attr.name != "self":
                # Is not define, error is given later when visiting
                # the attribute
                scope.define_variable(attr.name, attr.type)

        new_features = []
        for feature in node.features:
            new_features.append(self.visit(feature, scope))

        class_node = inf_ast.ClassDeclarationNode(new_features, node)
        return class_node

    # TODO
    @visitor.when(AttrDeclNode)
    def visit(self, node: AttrDeclNode, scope: Scope):
        if node.id == "self":
            self.add_error(
                node, "SemanticError: An attribute cannot be named 'self'")

        node_type = self.current_type.get_attribute(node.id).type

        attr_node = inf_ast.AttrDeclarationNode(node)
        if not node.body:
            attr_node.inferenced_type = node_type
            return attr_node

        expr_node = self.visit(node.body, scope)
        expr_type: TypeBag = expr_node.inferenced_type
        added_type = expr_type.add_self_type(self.current_type)

        expr_name = expr_type.generate_name()
        if not conforms(expr_type, node_type):
            self.add_error(
                node,
                (
                    f"TypeError: In class '{self.current_type.name}' attribue"
                    f" '{node.id}' expression type({expr_name}) does not conforms"
                    f" to declared type ({node_type.name})."
                ),
            )
        if added_type:
            expr_type.remove_self_type(self.current_type)

        attr_node.expr = expr_node
        attr_node.inferenced_type = expr_type
        return attr_node

    # TODO: hacer este visitor
    @visitor.when(MethodDeclNode)
    def visit(self, node: MethodDeclNode, scopex: Scope):

        scope = scopex.create_child()
        current_method = self.current_type.get_method(node.id)

        new_params = []
        param_names = list(zip(node.param_names[0], node.param_names[1]))

        for idx, typex, param in zip(
            current_method.param_names, current_method.param_types, param_names
        ):

            scope.define_variable(idx, typex)
            new_params.append(param)

        ret_type_decl: TypeBag = current_method.return_type

        body_node = self.visit(node.body, scope)
        ret_type_expr = body_node.inferenced_type
        added_self = ret_type_expr.add_self_type(self.current_type)

        ret_expr_name = ret_type_expr.generate_name()
        if not conforms(ret_type_expr, ret_type_decl):
            self.add_error(
                node.body,
                f"TypeError: In Class '{self.current_type.name}' method"
                f" '{current_method.name}' return expression type({ret_expr_name})"
                f" does not conforms to declared return type ({ret_type_decl.name})",
            )

        if added_self:
            ret_type_expr.remove_self_type(self.current_type)

        method_node = inf_ast.MethodDeclarationNode(
            new_params, node.type, body_node, node
        )
        method_node.exec_inferred_type = ret_type_expr
        method_node.inferenced_type = ret_type_decl
        # Actualiza el context
        # real_caller_type = self.current_type.name
        # el_metodo_del_conte = self.context.get_type(real_caller_type).get_method(
        # node.id)
        # el_metodo_del_conte.return_type = method_node.inferenced_type

        # print(
        #     f"Inferido en soft_inferrer {node.id}({self.current_type.name}) tiene tipo {method_node.inferenced_type.name}")
        return method_node

    @visitor.when(BlockNode)
    def visit(self, node: BlockNode, scope):
        new_expr_list = []
        for expr in node.expr_list:
            new_expr_list.append(self.visit(expr, scope))

        block_node = inf_ast.BlocksNode(new_expr_list, node)
        block_node.inferenced_type = block_node.expr_list[-1].inferenced_type
        return block_node

    # TODO: revisar
    @visitor.when(IfThenElseNode)
    def visit(self, node: IfThenElseNode, scope):
        condition_node = self.visit(node.cond, scope)

        condition_type = condition_node.inferenced_type
        bool_type = self.context.get_type("Bool")

        condition_clone = condition_type.clone()
        if not conforms(condition_type, bool_type):
            self.add_error(
                node,
                f"TypeError: If's condition type({condition_clone.name})"
                " does not conforms to Bool type.",
            )

        then_node = self.visit(node.then_expr, scope)
        else_node = self.visit(node.else_expr, scope)

        if_node = inf_ast.ConditionalNode(
            condition_node, then_node, else_node, node)

        then_type = then_node.inferenced_type
        else_type = else_node.inferenced_type
        joined_type = join(then_type, else_type)

        if_node.inferenced_type = joined_type
        return if_node

    @visitor.when(CaseNode)
    def visit(self, node: CaseNode, scope: Scope):
        expr_node = self.visit(node.expr, scope)

        types_visited = set()
        type_list = []
        new_options = []
        for option in node.case_branches:
            child = scope.create_child()
            new_options.append(self.visit(option, child))
            type_list.append(new_options[-1].inferenced_type)
            var_type = child.get_variable(option.id).get_type()
            var_type = var_type.heads[0] if not var_type.error_type else var_type
            if var_type in types_visited:
                self.add_error(
                    option,
                    "SemanticError: Case Expression have 2 or more branches"
                    f"with same case type({var_type.name})",
                )
            types_visited.add(var_type)

        joined_type = join_list(type_list)

        case_node = inf_ast.CaseNode(expr_node, new_options, node)
        case_node.inferenced_type = joined_type
        return case_node

    @visitor.when(CaseBranchNode)
    def visit(self, node: CaseBranchNode, scope: Scope):
        try:
            node_type = self.context.get_type(
                node.type, selftype=False, autotype=False)
        except SemanticError as err:
            self.add_error(
                node, err.text +
                f" While defining Case Option variable {node.id}."
            )
            node_type = TypeBag(set())

        scope.define_variable(node.id, node_type)
        expr_node = self.visit(node.expr, scope)

        case_opt_node = inf_ast.CaseOptionNode(expr_node, node_type, node)
        case_opt_node.inferenced_type = expr_node.inferenced_type
        return case_opt_node

    @visitor.when(WhileNode)
    def visit(self, node: WhileNode, scope):
        condition_node = self.visit(node.cond, scope)
        condition_type = condition_node.inferenced_type

        bool_type = self.context.get_type("Bool")
        condition_clone = condition_type.clone()
        if not conforms(condition_type, bool_type):
            self.add_error(
                node,
                f"TypeError: Loop condition type({condition_clone.name})"
                " does not conforms to Bool type.",
            )

        body_node = self.visit(node.body, scope)
        loop_node = inf_ast.LoopNode(condition_node, body_node, node)
        loop_node.inferenced_type = self.context.get_type("Object")
        return loop_node

    @visitor.when(LetInNode)
    def visit(self, node: LetInNode, scope: Scope):
        child = scope.create_child()

        new_decl_list = []
        for var in node.decl_list:
            new_decl_list.append(self.visit(var, child))

        in_expr_node = self.visit(node.expr, child)

        let_node = inf_ast.LetNode(new_decl_list, in_expr_node, node)
        let_node.inferenced_type = in_expr_node.inferenced_type
        return let_node

    @visitor.when(LetDeclNode)
    def visit(self, node: LetDeclNode, scope: Scope):
        var_decl_node = inf_ast.VarDeclarationNode(node)

        try:
            node_type = self.context.get_type(node.type)
        except SemanticError as err:
            node_type = TypeBag(set(), [])
            self.add_error(node, err.text)

        if node.id == "self":
            self.add_error(
                node,
                "SemanticError: Cannot bound self in a let expression.",
            )
            var_decl_node.id = "<error-name(self)>"

        scope.define_variable(var_decl_node.id, node_type)
        var_decl_node.index = len(scope.locals) - 1

        var_decl_node.inferenced_type = node_type

        if node.expr:
            expr_node = self.visit(node.expr, scope)
            expr_type: TypeBag = expr_node.inferenced_type
            added_type = expr_type.add_self_type(self.current_type)
            expr_clone = expr_type.clone()
            if not conforms(expr_type, node_type):
                self.add_error(
                    node,
                    f"TypeError: Variable '{node.id}' expression type"
                    f" ({expr_clone.name}) does not conforms to declared"
                    f" type({node_type.name}).",
                )
            if added_type:
                expr_type.remove_self_type(self.current_type)
            var_decl_node.expr = expr_node
            var_decl_node.inferenced_type = expr_node.inferenced_type

        return var_decl_node

    @visitor.when(AssignNode)
    def visit(self, node: AssignNode, scope: Scope):
        expr_node = self.visit(node.expr, scope)
        assign_node = inf_ast.AssignNode(expr_node, node)

        var = scope.find_variable(node.id)
        if var is None:
            self.add_error(
                node,
                f"SemanticError: Cannot assign new value to"
                f"{node.id} beacuse it is not defined in the current scope",
            )
        else:
            decl_type = var.get_type()
            assign_node.defined = True
            if var.name == "self":
                self.add_error(
                    node,
                    "SemanticError: Cannot assign new value. "
                    "Variable 'self' is Read-Only.",
                )

            expr_type: TypeBag = expr_node.inferenced_type
            added_type = expr_type.add_self_type(self.current_type)
            expr_name = expr_type.name
            if not conforms(expr_type, decl_type):
                self.add_error(
                    node,
                    f"TypeError: Cannot assign new value to variable '{node.id}'."
                    f" Expression type({expr_name}) does not conforms to"
                    f" declared type ({decl_type.name}).",
                )
            if added_type:
                expr_type.remove_self_type(self.current_type)

        assign_node.inferenced_type = expr_node.inferenced_type
        return assign_node

    # TODO: separar en static y el otro
    @visitor.when(StaticDispatchNode)
    def visit(self, node: StaticDispatchNode, scope):
        caller_type: TypeBag
        if node.expr == 'self':
            #expr_node = None
            caller_type = TypeBag({self.current_type})
        elif node.static_type is None:
            expr_node = self.visit(node.expr, scope)
            caller_type = expr_node.inferenced_type
        else:
            try:
                caller_type = self.context.get_type(
                    node.static_type, selftype=False, autotype=False
                )
            except SemanticError as err:
                caller_type = TypeBag(set())
                self.add_error(node, err + " While setting dispatch caller.")

            expr_node = self.visit(node.expr, scope)
            expr_type = expr_node.inferenced_type
            added_type = expr_type.add_self_type(self.current_type)
            expr_name = expr_type.generate_name()
            if not conforms(expr_type, caller_type):
                self.add_error(
                    node,
                    f"TypeError: Cannot effect dispatch because expression"
                    f" type({expr_name}) does not conforms to"
                    f" caller type({caller_type.name}).",
                )
            if added_type:
                expr_type.remove_self_type(self.current_type)

        methods = None
        if len(caller_type.type_set) > 1:
            methods_by_name = self.context.get_method_by_name(
                node.id, len(node.args))
            types = [typex for typex, _ in methods_by_name]
            caller_type_name = caller_type.generate_name()
            conforms(caller_type, TypeBag(set(types), types))
            if len(caller_type.type_set):
                methods = [
                    (typex, typex.get_method(node.id)) for typex in caller_type.heads
                ]
            else:
                self.add_error(
                    node,
                    f"AtributeError: There is no method '{node.id}'"
                    f" that recieves {len(node.args)} arguments in"
                    f" types {caller_type_name}.",
                )
        elif len(caller_type.type_set) == 1:
            caller = caller_type.heads[0]
            caller = self.current_type if isinstance(
                caller, SelfType) else caller
            try:
                methods = [(caller, caller.get_method(node.id))]
            except AttributeError as err:
                self.add_error(
                    node,
                    err.text,
                )

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
            method_call_node.inferenced_type = TypeBag(set())  # ErrorType
        return method_call_node

    # TODO: separar en static y el otro
    @visitor.when(DispatchNode)
    def visit(self, node: DispatchNode, scope):
        caller_type: TypeBag
        if node.expr == 'self':
            caller_type = TypeBag({self.current_type})
        else:
            expr_node = self.visit(node.expr, scope)
            caller_type = expr_node.inferenced_type

        methods = None
        if len(caller_type.type_set) > 1:
            methods_by_name = self.context.get_method_by_name(
                node.id, len(node.args))
            types = [typex for typex, _ in methods_by_name]
            caller_type_name = caller_type.generate_name()
            conforms(caller_type, TypeBag(set(types), types))
            if len(caller_type.type_set):
                methods = [
                    (typex, typex.get_method(node.id)) for typex in caller_type.heads
                ]
            else:
                self.add_error(
                    node,
                    f"AtributeError: There is no method '{node.id}'"
                    f" that recieves {len(node.args)} arguments in"
                    f" types {caller_type_name}.",
                )
        elif len(caller_type.type_set) == 1:
            caller = caller_type.heads[0]
            caller = self.current_type if isinstance(
                caller, SelfType) else caller
            try:
                methods = [(caller, caller.get_method(node.id))]
            except AttributeError as err:
                self.add_error(
                    node,
                    err.text,
                )

        new_args = []
        for i in range(len(node.args)):
            new_args.append(self.visit(node.args[i], scope))
        node.static_type = None
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
            method_call_node.inferenced_type = TypeBag(set())  # ErrorType
        return method_call_node

    @visitor.when(ArithmeticNode)
    def visit(self, node: ArithmeticNode, scope):
        left_node, right_node = self.__arithmetic_operation(node, scope)
        if isinstance(node, PlusNode):
            arith_node = inf_ast.PlusNode(left_node, right_node, node)
        elif isinstance(node, MinusNode):
            arith_node = inf_ast.MinusNode(left_node, right_node, node)
        elif isinstance(node, MultNode):
            arith_node = inf_ast.StarNode(left_node, right_node, node)
        elif isinstance(node, DivNode):
            arith_node = inf_ast.DivNode(left_node, right_node, node)
        else:
            raise Exception("Unknown arithmetic node detected")

        arith_node.inferenced_type = self.context.get_type("Int")
        return arith_node

    @visitor.when(LeNode)
    def visit(self, node: LeNode, scope: Scope):
        left_node, right_node = self.__arithmetic_operation(node, scope)
        less_node = inf_ast.LessNode(left_node, right_node, node)
        less_node.inferenced_type = self.context.get_type("Bool")
        return less_node

    @visitor.when(LeqNode)
    def visit(self, node, scope: Scope):
        left_node, right_node = self.__arithmetic_operation(node, scope)
        lesseq_node = inf_ast.LessOrEqualNode(left_node, right_node, node)
        lesseq_node.inferenced_type = self.context.get_type("Bool")
        return lesseq_node

    @visitor.when(EqNode)
    def visit(self, node: EqNode, scope: Scope):
        left_node = self.visit(node.left_expr, scope)
        right_node = self.visit(node.right_expr, scope)

        equal_node = inf_ast.EqualsNode(left_node, right_node, node)
        equal_node.inferenced_type = self.context.get_type("Bool")
        return equal_node

    @visitor.when(VarNode)
    def visit(self, node: VarNode, scope: Scope):
        var_node = inf_ast.VariableNode(node)

        var = scope.find_variable(node.value)
        if var:
            var_node.defined = True
            var_type = var.get_type()
        else:
            self.add_error(
                node, f"NameError: Variable '{node.value}' is not defined.")
            var_type = TypeBag(set())

        var_node.inferenced_type = var_type
        return var_node

    @visitor.when(NotNode)
    def visit(self, node: NotNode, scope):
        expr_node = self.visit(node.expr, scope)

        expr_type = expr_node.inferenced_type
        expr_clone = expr_type.clone()
        bool_type = self.context.get_type("Bool")
        if not conforms(expr_type, bool_type):
            self.add_error(
                node,
                f"TypeError: Not's expresion type ({expr_clone.name} does not"
                " conforms to Bool type",
            )

        not_node = inf_ast.NotNode(expr_node, node)
        not_node.inferenced_type = bool_type
        return not_node

    @visitor.when(TildeNode)
    def visit(self, node: TildeNode, scope):
        expr_node = self.visit(node.expr, scope)

        expr_type = expr_node.inferenced_type
        expr_clone = expr_type.clone()
        int_type = self.context.get_type("Int")
        if not conforms(expr_type, int_type):
            self.add_error(
                node,
                f"TypeError: ~ expresion type({expr_clone.name}) does not"
                " conforms to Int type",
            )

        complement_node = inf_ast.ComplementNode(expr_node, node)
        complement_node.inferenced_type = int_type
        return complement_node

    @visitor.when(IsVoidNode)
    def visit(self, node: IsVoidNode, scope):
        node_expr = self.visit(node.expr, scope)
        is_void_node = inf_ast.IsVoidNode(node_expr, node)
        is_void_node.inferenced_type = self.context.get_type("Bool")
        return is_void_node

    @visitor.when(NewNode)
    def visit(self, node: NewNode, scope):
        instantiate_node = inf_ast.InstantiateNode(node)
        try:
            node_type = self.context.get_type(node.type, autotype=False)
        except SemanticError as err:
            self.add_error(
                node,
                err.text + f" Could not instantiate type '{node.type}'.",
            )
            node_type = TypeBag(set())

        instantiate_node.inferenced_type = node_type
        return instantiate_node

    @visitor.when(IntNode)
    def visit(self, node: IntNode, scope):
        int_node = inf_ast.IntNode(node)
        int_node.inferenced_type = self.context.get_type("Int")
        return int_node

    @visitor.when(StringNode)
    def visit(self, node: StringNode, scope):
        str_node = inf_ast.StringNode(node)
        str_node.inferenced_type = self.context.get_type("String")

        return str_node

    @visitor.when(BoolNode)
    def visit(self, node: BoolNode, scope):
        bool_node = inf_ast.BooleanNode(node)
        bool_node.inferenced_type = self.context.get_type("Bool")
        return bool_node

    @visitor.when(ParenthNode)
    def visit(self, node: ParenthNode, scope):
        return self.visit(node.expr, scope)

    def __arithmetic_operation(self, node: ArithmeticNode, scope):
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
