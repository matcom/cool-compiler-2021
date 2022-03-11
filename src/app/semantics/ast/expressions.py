from inspect import stack
from .base import ExpressionNode
from typing import List
from app.semantics.constants import *
import app.semantics.ast as inf_ast
from app.semantics.tools import TypeBag
from app.semantics.tools.errors import AttributeError, SemanticError
from app.semantics.constants import BOOL_TYPE, OBJECT_TYPE
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
    def soft_infer(node, scope, soft_inferrer):
        new_expr_list = []
        for expr in node.expr_list:
            new_expr_list.append(soft_inferrer.visit(expr, scope))

        block_node = inf_ast.BlocksNode(new_expr_list, node)
        block_node.inferred_type = block_node.expr_list[-1].inferred_type
        return block_node

    @staticmethod
    def deep_infer(node, scope, deep_inferrer):
        new_expr_list = []
        for expr in node.expr_list:
            new_expr_list.append(deep_inferrer.visit(expr, scope))

        block_node = BlocksNode(new_expr_list, node)
        block_node.inferred_type = block_node.expr_list[-1].inferred_type
        return block_node


class ConditionalNode(ExpressionNode):
    def __init__(self, condition, then_node, else_node, node):
        super().__init__(node)
        self.condition = condition
        self.then_body = then_node
        self.else_body = else_node

    @staticmethod
    def soft_infer(node, scope, soft_inferrer):
        condition_node = soft_inferrer.visit(node.cond, scope)

        condition_type = condition_node.inferred_type
        bool_type = soft_inferrer.context.get_type(BOOL_TYPE)

        condition_clone = condition_type.clone()
        if not conforms(condition_type, bool_type):
            soft_inferrer.add_error(
                node,
                f"TypeError: If's condition type({condition_clone.name})"
                " does not conforms to Bool type.",
            )

        then_node = soft_inferrer.visit(node.then_expr, scope)
        else_node = soft_inferrer.visit(node.else_expr, scope)

        if_node = inf_ast.ConditionalNode(
            condition_node, then_node, else_node, node)

        then_type = then_node.inferred_type
        else_type = else_node.inferred_type
        joined_type = join(then_type, else_type)

        if_node.inferred_type = joined_type
        return if_node

    @staticmethod
    def deep_infer(node, scope, deep_inferrer):
        condition_node = deep_inferrer.visit(node.condition, scope)
        then_node = deep_inferrer.visit(node.then_body, scope)
        else_node = deep_inferrer.visit(node.else_body, scope)

        condition_type = condition_node.inferred_type
        if not equal(condition_type, node.condition.inferred_type):
            condition_clone = condition_type.clone()
            bool_type = deep_inferrer.context.get_type(BOOL_TYPE)
            if not conforms(condition_type, bool_type):
                deep_inferrer.add_error(
                    node,
                    f"TypeError: If's condition type({condition_clone.name})"
                    " does not conforms to Bool type.",
                )

        if_node = ConditionalNode(condition_node, then_node, else_node, node)

        if not equal(
            then_node.inferred_type, node.then_body.inferred_type
        ) or not equal(else_node.inferred_type, node.else_body.inferred_type):
            then_type = then_node.inferred_type
            else_type = else_node.inferred_type
            joined_type = join(then_type, else_type)
        else:
            joined_type = node.inferred_type

        if_node.inferred_type = joined_type
        return if_node


class CaseNode(ExpressionNode):
    def __init__(self, case_expr, options, node):
        super().__init__(node)
        self.case_expr = case_expr
        self.options: List[CaseOptionNode] = options

    @staticmethod
    def soft_infer(node, scope, deep_inferrer):
        expr_node = deep_inferrer.visit(node.expr, scope)

        types_visited = set()
        type_list = []
        new_options = []
        for option in node.case_branches:
            child = scope.create_child()
            new_options.append(deep_inferrer.visit(option, child))
            type_list.append(new_options[-1].inferred_type)
            var_type = child.get_variable(option.id).get_type()
            var_type = var_type.heads[0] if not var_type.error_type else var_type
            if var_type in types_visited:
                deep_inferrer.add_error(
                    option,
                    "SemanticError: Case Expression have 2 or more branches"
                    f"with same case type({var_type.name})",
                )
            types_visited.add(var_type)

        joined_type = join_list(type_list)

        case_node = inf_ast.CaseNode(expr_node, new_options, node)
        case_node.inferred_type = joined_type
        return case_node

    @staticmethod
    def deep_infer(node, scope, deep_inferrer):
        expr_node = deep_inferrer.visit(node.case_expr, scope)
        type_list = []
        new_options = []
        for option in node.options:
            child = scope.next_child()
            new_options.append(deep_inferrer.visit(option, child))
            type_list.append(new_options[-1].inferred_type)

        join_type = join_list(type_list)
        case_node = CaseNode(expr_node, new_options, node)
        case_node.inferred_type = join_type
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
    def soft_infer(node, scope, deep_inferrer):
        try:
            node_type = deep_inferrer.context.get_type(
                node.type, selftype=False, autotype=False)
        except SemanticError as err:
            deep_inferrer.add_error(
                node, err.text +
                f" While defining Case Option variable {node.id}."
            )
            node_type = TypeBag(set())

        scope.define_variable(node.id, node_type)
        expr_node = deep_inferrer.visit(node.expr, scope)

        case_opt_node = inf_ast.CaseOptionNode(expr_node, node_type, node)
        case_opt_node.inferred_type = expr_node.inferred_type
        return case_opt_node

    @staticmethod
    def deep_infer(node, scope, deep_inferrer):
        expr_node = deep_inferrer.visit(node.expr, scope)
        opt_node = CaseOptionNode(expr_node, node.branch_type, node)
        opt_node.inferred_type = expr_node.inferred_type

        return opt_node


class LoopNode(ExpressionNode):
    def __init__(self, condition, body, node):
        super().__init__(node)
        self.condition = condition
        self.body = body

    def soft_infer(node, scope, soft_inferrer):
        condition_node = soft_inferrer.visit(node.cond, scope)
        condition_type = condition_node.inferred_type

        bool_type = soft_inferrer.context.get_type(BOOL_TYPE)
        condition_clone = condition_type.clone()
        if not conforms(condition_type, bool_type):
            soft_inferrer.add_error(
                node,
                f"TypeError: Loop condition type({condition_clone.name})"
                " does not conforms to Bool type.",
            )

        body_node = soft_inferrer.visit(node.body, scope)
        loop_node = inf_ast.LoopNode(condition_node, body_node, node)
        loop_node.inferred_type = soft_inferrer.context.get_type(
            OBJECT_TYPE)
        return loop_node

    @staticmethod
    def deep_infer(node, scope, deep_inferrer):
        condition_node = deep_inferrer.visit(node.condition, scope)
        condition_type = condition_node.inferred_type

        if not equal(condition_type, node.condition.inferred_type):
            bool_type = deep_inferrer.context.get_type(BOOL_TYPE)
            condition_clone = condition_type.clone()
            if not conforms(condition_type, bool_type):
                deep_inferrer.add_error(
                    node,
                    f"TypeError: Loop condition type({condition_clone.name})"
                    " does not conforms to Bool type.",
                )

        body_node = deep_inferrer.visit(node.body, scope)
        loop_node = LoopNode(condition_node, body_node, node)
        loop_node.inferred_type = node.inferred_type
        return loop_node


class LetNode(ExpressionNode):
    def __init__(self, var_decl_list, in_expr, node):
        super().__init__(node)
        self.var_decl_list = var_decl_list
        self.in_expr = in_expr

    @staticmethod
    def soft_infer(node, scope, soft_inferrer):
        child = scope.create_child()

        new_decl_list = []
        for var in node.decl_list:
            new_decl_list.append(soft_inferrer.visit(var, child))

        in_expr_node = soft_inferrer.visit(node.expr, child)

        let_node = inf_ast.LetNode(new_decl_list, in_expr_node, node)
        let_node.inferred_type = in_expr_node.inferred_type
        return let_node

    @staticmethod
    def deep_infer(node, scope, deep_inferrer):
        child = scope.next_child()

        new_decl_list = []
        for var in node.var_decl_list:
            new_decl_list.append(deep_inferrer.visit(var, child))

        in_expr_node = deep_inferrer.visit(node.in_expr, child)

        let_node = LetNode(new_decl_list, in_expr_node, node)
        let_node.inferred_type = in_expr_node.inferred_type
        return let_node


class VarDeclarationNode(ExpressionNode):
    def __init__(self, node):
        super().__init__(node)
        self.id = node.id
        self.expr = None
        self.index = None
        self.type = node.type

    def soft_infer(node, scope, soft_inferrer):
        var_decl_node = inf_ast.VarDeclarationNode(node)

        try:
            node_type = soft_inferrer.context.get_type(node.type)
        except SemanticError as err:
            node_type = TypeBag(set(), [])
            soft_inferrer.add_error(node, err.text)

        if node.id == "self":
            soft_inferrer.add_error(
                node,
                "SemanticError: Cannot bound self in a let expression.",
            )
            var_decl_node.id = "<error-name(self)>"

        scope.define_variable(var_decl_node.id, node_type)
        var_decl_node.index = len(scope.locals) - 1

        var_decl_node.inferred_type = node_type

        if node.expr:
            expr_node = soft_inferrer.visit(node.expr, scope)
            expr_type: TypeBag = expr_node.inferred_type
            added_type = expr_type.add_self_type(soft_inferrer.current_type)
            expr_clone = expr_type.clone()
            if not conforms(expr_type, node_type):
                soft_inferrer.add_error(
                    node,
                    f"TypeError: Variable '{node.id}' expression type"
                    f" ({expr_clone.name}) does not conforms to declared"
                    f" type({node_type.name}).",
                )
            if added_type:
                expr_type.remove_self_type(soft_inferrer.current_type)
            var_decl_node.expr = expr_node
            var_decl_node.inferred_type = expr_node.inferred_type

        return var_decl_node

    @staticmethod
    def deep_infer(node, scope, deep_inferrer):
        var_decl_node = VarDeclarationNode(node)
        var_decl_node.index = node.index
        if node.expr is None:
            var_decl_node.inferred_type = node.inferred_type
            return var_decl_node

        expr_node = deep_inferrer.visit(node.expr, scope)
        var_decl_node.expr = expr_node

        node_type = scope.get_local_by_index(node.index).get_type()

        expr_type = expr_node.inferred_type
        if equal(expr_type, node.expr.inferred_type):
            expr_clone = expr_type.clone()
            if not conforms(expr_type, node_type):
                deep_inferrer.add_error(
                    node,
                    f"Semantic Error: Variable '{node.id}' expression type"
                    f" ({expr_clone.name}) does not conforms to declared"
                    f" type({node_type.name}).",
                )

        var_decl_node.inferred_type = expr_node.inferred_type
        return var_decl_node


class AssignNode(ExpressionNode):
    def __init__(self, expr, node):
        super().__init__(node)
        self.id = node.id
        self.expr = expr
        self.defined = False

    def soft_infer(node, scope, soft_inferrer):

        expr_node = soft_inferrer.visit(node.expr, scope)
        assign_node = inf_ast.AssignNode(expr_node, node)

        var = scope.find_variable(node.id)
        if var is None:
            soft_inferrer.add_error(
                node,
                f"SemanticError: Cannot assign new value to"
                f"{node.id} because it is not defined in the current scope",
            )
        else:
            decl_type = var.get_type()
            assign_node.defined = True
            if var.name == "self":
                soft_inferrer.add_error(
                    node,
                    "SemanticError: Cannot assign new value. "
                    "Variable 'self' is Read-Only.",
                )

            expr_type: TypeBag = expr_node.inferred_type
            added_type = expr_type.add_self_type(soft_inferrer.current_type)
            expr_name = expr_type.name
            if not conforms(expr_type, decl_type):
                soft_inferrer.add_error(
                    node,
                    f"TypeError: Cannot assign new value to variable '{node.id}'."
                    f" Expression type({expr_name}) does not conforms to"
                    f" declared type ({decl_type.name}).",
                )
            if added_type:
                expr_type.remove_self_type(soft_inferrer.current_type)

        assign_node.inferred_type = expr_node.inferred_type
        return assign_node

    @staticmethod
    def deep_infer(node, scope, deep_inferrer):
        expr_node = deep_inferrer.visit(node.expr, scope)
        assign_node = AssignNode(expr_node, node)

        if not node.defined or node.id == "self":
            assign_node.inferred_type = TypeBag(set())
            return assign_node

        assign_node.defined = True

        decl_type = scope.get_variable(node.id).get_type()
        expr_type = expr_node.inferred_type
        if not equal(expr_type, node.expr.inferred_type):
            expr_clone = expr_type.clone()
            if not conforms(expr_type, decl_type):
                deep_inferrer.add_error(
                    node,
                    f"TypeError: Cannot assign new value to variable '{node.id}'."
                    f" Expression type({expr_clone.name}) does not conforms to"
                    f" declared type ({decl_type.name}).",
                )

        assign_node.inferred_type = expr_node.inferred_type
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

    def soft_infer_static(node, scope, soft_inferrer):
        caller_type: TypeBag
        if node.expr == 'self':
            #expr_node = None
            caller_type = TypeBag({soft_inferrer.current_type})
        elif node.static_type is None:
            expr_node = soft_inferrer.visit(node.expr, scope)
            caller_type = expr_node.inferred_type
        else:
            try:
                caller_type = soft_inferrer.context.get_type(
                    node.static_type, selftype=False, autotype=False
                )
            except SemanticError as err:
                caller_type = TypeBag(set())
                soft_inferrer.add_error(
                    node, err + " While setting dispatch caller.")

            expr_node = soft_inferrer.visit(node.expr, scope)
            expr_type = expr_node.inferred_type
            added_type = expr_type.add_self_type(soft_inferrer.current_type)
            expr_name = expr_type.generate_name()
            if not conforms(expr_type, caller_type):
                soft_inferrer.add_error(
                    node,
                    f"TypeError: Cannot effect dispatch because expression"
                    f" type({expr_name}) does not conforms to"
                    f" caller type({caller_type.name}).",
                )
            if added_type:
                expr_type.remove_self_type(soft_inferrer.current_type)

        methods = None
        if len(caller_type.type_set) > 1:
            methods_by_name = soft_inferrer.context.get_method_by_name(
                node.id, len(node.args))
            types = [typex for typex, _ in methods_by_name]
            caller_type_name = caller_type.generate_name()
            conforms(caller_type, TypeBag(set(types), types))
            if len(caller_type.type_set):
                methods = [
                    (typex, typex.get_method(node.id)) for typex in caller_type.heads
                ]
            else:
                soft_inferrer.add_error(
                    node,
                    f"AtributeError: There is no method '{node.id}'"
                    f" that recieves {len(node.args)} arguments in"
                    f" types {caller_type_name}.",
                )
        elif len(caller_type.type_set) == 1:
            caller = caller_type.heads[0]
            caller = soft_inferrer.current_type if isinstance(
                caller, SelfType) else caller
            try:
                methods = [(caller, caller.get_method(node.id))]
            except AttributeError as err:
                soft_inferrer.add_error(
                    node,
                    err.text,
                )

        new_args = []
        for i in range(len(node.args)):
            new_args.append(soft_inferrer.visit(node.args[i], scope))

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
            method_call_node.inferred_type = TypeBag(type_set, heads)
        else:
            method_call_node.inferred_type = TypeBag(set())
        return method_call_node

    def soft_infer_dynamic(node, scope, soft_inferrer):

        caller_type: TypeBag
        if node.expr == 'self':
            caller_type = TypeBag({soft_inferrer.current_type})
        else:
            expr_node = soft_inferrer.visit(node.expr, scope)
            caller_type = expr_node.inferred_type

        methods = None
        if len(caller_type.type_set) > 1:
            methods_by_name = soft_inferrer.context.get_method_by_name(
                node.id, len(node.args))
            types = [typex for typex, _ in methods_by_name]
            caller_type_name = caller_type.generate_name()
            conforms(caller_type, TypeBag(set(types), types))
            if len(caller_type.type_set):
                methods = [
                    (typex, typex.get_method(node.id)) for typex in caller_type.heads
                ]
            else:
                soft_inferrer.add_error(
                    node,
                    f"AtributeError: There is no method '{node.id}'"
                    f" that recieves {len(node.args)} arguments in"
                    f" types {caller_type_name}.",
                )
        elif len(caller_type.type_set) == 1:
            caller = caller_type.heads[0]
            caller = soft_inferrer.current_type if isinstance(
                caller, SelfType) else caller
            try:
                methods = [(caller, caller.get_method(node.id))]
            except AttributeError as err:
                soft_inferrer.add_error(
                    node,
                    err.text,
                )

        new_args = []
        for i in range(len(node.args)):
            new_args.append(soft_inferrer.visit(node.args[i], scope))
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
            method_call_node.inferred_type = TypeBag(type_set, heads)
        else:
            method_call_node.inferred_type = TypeBag(set())  # ErrorType
        return method_call_node

    @staticmethod
    def deep_infer(node, scope, deep_inferrer):
        caller_type: TypeBag = node.caller_type
        expr_node = None
        if node.type is not None and node.expr is not None:
            expr_node = deep_inferrer.visit(node.expr, scope)
            expr_type = expr_node.inferred_type
            if not equal(expr_type, node.expr.inferred_type):
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
            caller_type = expr_node.inferred_type

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
                        arg_type: TypeBag = new_args[-1].inferred_type
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
        call_node.inferred_type = infered_type
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
            call_node.inferred_type = infered_type

        except AttributeError as err:
            deep_inferrer.add_error(node, err.text)

        return call_node

    def __str__(self):
        return f"""caller_type: {self.caller_type},
        expr : {self.expr},
        args : {self.args},
        id: {self.id} ,
        static_type:  {self.static_type}"""
