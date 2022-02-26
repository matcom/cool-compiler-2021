from inspect import stack
from .base import ExpressionNode
from typing import List
from app.semantics.tools import TypeBag
from app.semantics.tools.errors import AttributeError
from app.semantics.tools import (
    conforms,
    equal,
    join,
    join_list,
    SelfType,
    smart_add,
)


class BlocksNode(ExpressionNode):
    def __init__(self, expr_list, node):
        super().__init__(node)
        self.expr_list = expr_list

    @staticmethod
    def infer(node, scope, deep_inferrer):
        new_expr_list = []
        for expr in node.expr_list:
            new_expr_list.append(deep_inferrer.visit(expr, scope))

        block_node = BlocksNode(new_expr_list, node)
        block_node.inferenced_type = block_node.expr_list[-1].inferenced_type
        return block_node


class ConditionalNode(ExpressionNode):
    def __init__(self, condition, then_node, else_node, node):
        super().__init__(node)
        self.condition = condition
        self.then_body = then_node
        self.else_body = else_node

    @staticmethod
    def infer(node, scope, deep_inferrer):
        condition_node = deep_inferrer.visit(node.condition, scope)
        then_node = deep_inferrer.visit(node.then_body, scope)
        else_node = deep_inferrer.visit(node.else_body, scope)

        condition_type = condition_node.inferenced_type
        if not equal(condition_type, node.condition.inferenced_type):
            condition_clone = condition_type.clone()
            bool_type = deep_inferrer.context.get_type("Bool")
            if not conforms(condition_type, bool_type):
                deep_inferrer.add_error(
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


class CaseNode(ExpressionNode):
    def __init__(self, case_expr, options, node):
        super().__init__(node)
        self.case_expr = case_expr
        self.options: List[CaseOptionNode] = options

    @staticmethod
    def infer(node, scope, deep_inferrer):
        expr_node = deep_inferrer.visit(node.case_expr, scope)
        type_list = []
        new_options = []
        for option in node.options:
            child = scope.next_child()
            new_options.append(deep_inferrer.visit(option, child))
            type_list.append(new_options[-1].inferenced_type)

        join_type = join_list(type_list)
        case_node = CaseNode(expr_node, new_options, node)
        case_node.inferenced_type = join_type
        return case_node


class CaseOptionNode(ExpressionNode):
    def __init__(self, ret_expr, branch_type, node):
        super().__init__(node)
        self.id = node.id
        self.expr = ret_expr
        self.decl_type = node.type
        self.branch_type = branch_type
        self.type = node.type

    @staticmethod
    def infer(node, scope, deep_inferrer):
        expr_node = deep_inferrer.visit(node.expr, scope)
        opt_node = CaseOptionNode(expr_node, node.branch_type, node)
        opt_node.inferenced_type = expr_node.inferenced_type

        return opt_node


class LoopNode(ExpressionNode):
    def __init__(self, condition, body, node):
        super().__init__(node)
        self.condition = condition
        self.body = body

    @staticmethod
    def infer(node, scope, deep_inferrer):
        condition_node = deep_inferrer.visit(node.condition, scope)
        condition_type = condition_node.inferenced_type

        if not equal(condition_type, node.condition.inferenced_type):
            bool_type = deep_inferrer.context.get_type("Bool")
            condition_clone = condition_type.clone()
            if not conforms(condition_type, bool_type):
                deep_inferrer.add_error(
                    node,
                    f"TypeError: Loop condition type({condition_clone.name})"
                    " does not conforms to Bool type.",
                )

        body_node = deep_inferrer.visit(node.body, scope)
        loop_node = LoopNode(condition_node, body_node, node)
        loop_node.inferenced_type = node.inferenced_type
        return loop_node


class LetNode(ExpressionNode):
    def __init__(self, var_decl_list, in_expr, node):
        super().__init__(node)
        self.var_decl_list = var_decl_list
        self.in_expr = in_expr

    @staticmethod
    def infer(node, scope, deep_inferrer):
        child = scope.next_child()

        new_decl_list = []
        for var in node.var_decl_list:
            new_decl_list.append(deep_inferrer.visit(var, child))

        in_expr_node = deep_inferrer.visit(node.in_expr, child)

        let_node = LetNode(new_decl_list, in_expr_node, node)
        let_node.inferenced_type = in_expr_node.inferenced_type
        return let_node


class VarDeclarationNode(ExpressionNode):
    def __init__(self, node):
        super().__init__(node)
        self.id = node.id
        self.expr = None
        self.index = None
        self.type = node.type

    @staticmethod
    def infer(node, scope, deep_inferrer):
        var_decl_node = VarDeclarationNode(node)
        var_decl_node.index = node.index
        if node.expr is None:
            var_decl_node.inferenced_type = node.inferenced_type
            return var_decl_node

        expr_node = deep_inferrer.visit(node.expr, scope)
        var_decl_node.expr = expr_node

        node_type = scope.get_local_by_index(node.index).get_type()

        expr_type = expr_node.inferenced_type
        if equal(expr_type, node.expr.inferenced_type):
            expr_clone = expr_type.clone()
            if not conforms(expr_type, node_type):
                deep_inferrer.add_error(
                    node,
                    f"Semantic Error: Variable '{node.id}' expression type"
                    f" ({expr_clone.name}) does not conforms to declared"
                    f" type({node_type.name}).",
                )

        var_decl_node.inferenced_type = expr_node.inferenced_type
        return var_decl_node


class AssignNode(ExpressionNode):
    def __init__(self, expr, node):
        super().__init__(node)
        self.id = node.id
        self.expr = expr
        self.defined = False

    @staticmethod
    def infer(node, scope, deep_inferrer):
        expr_node = deep_inferrer.visit(node.expr, scope)
        assign_node = AssignNode(expr_node, node)

        if not node.defined or node.id == "self":
            assign_node.inferenced_type = TypeBag(set())
            return assign_node

        assign_node.defined = True

        decl_type = scope.get_variable(node.id).get_type()
        expr_type = expr_node.inferenced_type
        if not equal(expr_type, node.expr.inferenced_type):
            expr_clone = expr_type.clone()
            if not conforms(expr_type, decl_type):
                deep_inferrer.add_error(
                    node,
                    f"TypeError: Cannot assign new value to variable '{node.id}'."
                    f" Expression type({expr_clone.name}) does not conforms to"
                    f" declared type ({decl_type.name}).",
                )

        assign_node.inferenced_type = expr_node.inferenced_type
        assign_node.exec_inferred_type = expr_node.exec_inferred_type
        return assign_node


class MethodCallNode(ExpressionNode):
    def __init__(self, caller_type, expr, args, node):
        super().__init__(node)
        self.caller_type = caller_type
        self.expr = expr
        self.args = args
        self.id = node.id
        self.type = node.static_type
        self.static_type = node.static_type

    @staticmethod
    def infer(node, scope, deep_inferrer):
        caller_type: TypeBag = node.caller_type
        expr_node = None
        if node.type is not None and node.expr is not None:
            expr_node = deep_inferrer.visit(node.expr, scope)
            expr_type = expr_node.inferenced_type
            if not equal(expr_type, node.expr.inferenced_type):
                expr_clone = expr_type.clone()
                if not conforms(expr_type, caller_type):
                    deep_inferrer.add_error(
                        node,
                        f"SemanticError: Cannot effect dispatch because expression"
                        f" type({expr_clone.name}) does not conforms to "
                        f" caller type({caller_type.name}).",
                    )
        elif node.expr is not None:
            expr_node = deep_inferrer.visit(node.expr, scope)
            caller_type = expr_node.inferenced_type

        if len(caller_type.type_set) > 1:
            methods_by_name = deep_inferrer.context.get_method_by_name(
                node.id, len(node.args))
            types = [typex for typex, _ in methods_by_name]
            conforms(caller_type, TypeBag(set(types), types))
            if len(caller_type.heads) > 1:
                error = (
                    f"SemanticError: Method '{node.id}' found in"
                    f" {len(caller_type.heads)} unrelated types:\n"
                )
                error += "   -Found in: "
                error += ", ".join(typex.name for typex in caller_type.heads)
                deep_inferrer.add_error(node, error)
            elif len(caller_type.heads) == 0:
                deep_inferrer.add_error(
                    node,
                    f" SemanticError: There is no method called {node.id} which takes"
                    f" {len(node.args)} paramters.",
                )

        if len(caller_type.heads) != 1:
            new_args = []
            infered_type = TypeBag(set())
        else:
            caller = caller_type.heads[0]
            caller = deep_inferrer.current_type if isinstance(
                caller, SelfType) else caller
            try:
                method = caller.get_method(node.id)
            except AttributeError as err:
                new_args = []
                infered_type = TypeBag(set())
            else:
                if len(node.args) != len(method.param_types):
                    deep_inferrer.add_error(
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
                    new_args.append(deep_inferrer.visit(node.args[i], scope))
                    if i < len(method.param_types):
                        arg_type: TypeBag = new_args[-1].inferenced_type
                        added_type = arg_type.add_self_type(
                            deep_inferrer.current_type)
                        arg_name = arg_type.generate_name()
                        param_type = method.param_types[i]
                        if not conforms(arg_type, param_type):
                            deep_inferrer.add_error(
                                new_args[-1],
                                f"TypeError: Argument expression type({arg_name}) does"
                                f" not conforms parameter declared type({param_type.name})",
                            )
                        if added_type:
                            arg_type.remove_self_type(
                                deep_inferrer.current_type)
                infered_type = TypeBag(type_set, heads)

        real_caller_type_name = caller_type.name
        call_node = MethodCallNode(caller_type, expr_node, new_args, node)
        call_node.inferenced_type = infered_type
        if(real_caller_type_name == 'SELF_TYPE'):
            real_caller_type_name = deep_inferrer.current_type.name
        try:
            context_method = deep_inferrer.context.get_type(real_caller_type_name).get_method(
                node.id)
            real_return_type = context_method.return_type

            if(real_return_type.name == 'SELF_TYPE'):
                if(caller_type.name == 'SELF_TYPE'):
                    real_return_type = deep_inferrer.current_type
                else:
                    real_return_type = caller_type
            real_return_type = real_return_type if isinstance(
                real_return_type, TypeBag) else TypeBag({real_return_type})
            call_node = MethodCallNode(caller_type, expr_node, new_args, node)
            call_node.exec_inferred_type = real_return_type
            call_node.inferenced_type = infered_type

        except AttributeError as err:
            deep_inferrer.add_error(node, err.text)

        return call_node

    def __str__(self):
        return f"""caller_type: {self.caller_type},
        expr : {self.expr},
        args : {self.args},
        id: {self.id} ,
        static_type:  {self.static_type}"""
