from .base import DeclarationNode
import app.semantics.ast as inf_ast
from app.semantics.constants import *
from app.semantics.tools import (
    TypeBag,
    conforms,
    equal,
)


class ClassDeclarationNode(DeclarationNode):
    def __init__(self, features, node):
        super().__init__(node)
        self.features = features
        self.id = node.id
        self.parent = node.parent

    def soft_infer(node, scope, soft_inferrer):
        soft_inferrer.current_type = soft_inferrer.context.get_type(
            node.id, unpacked=True)
        scope.define_variable(
            "self", soft_inferrer.context.get_type(SELF_TYPE))

        for attr in soft_inferrer.current_type.attributes:
            if attr.name != "self":
                scope.define_variable(attr.name, attr.type)

        new_features = []
        for feature in node.features:
            new_features.append(soft_inferrer.visit(feature, scope))

        class_node = inf_ast.ClassDeclarationNode(new_features, node)
        return class_node

    @staticmethod
    def deep_infer(node, scope, hard_inferrer):
        hard_inferrer.current_type = hard_inferrer.context.get_type(
            node.id, unpacked=True)

        new_features = []
        for feature in node.features:
            new_features.append(hard_inferrer.visit(feature, scope))

        class_node = ClassDeclarationNode(new_features, node)
        return class_node


class ParamNode(DeclarationNode):
    def __init__(self, node, idx: str, typex) -> None:
        super().__init__(node)
        self.id = idx
        self.type = typex


class AttrDeclarationNode(DeclarationNode):
    def __init__(self, node):
        super().__init__(node)
        self.id = node.id
        self.expr = None
        self.type = node.type

    @staticmethod
    def soft_infer(node, scope, soft_inferrer):
        if node.id == "self":
            soft_inferrer.add_error(
                node, "SemanticError: An attribute cannot be named 'self'")
        node_type = soft_inferrer.current_type.get_attribute(node.id).type

        attr_node = inf_ast.AttrDeclarationNode(node)
        if not node.body:
            attr_node.inferred_type = node_type
            return attr_node

        expr_node = soft_inferrer.visit(node.body, scope)
        expr_type: TypeBag = expr_node.inferenced_type
        added_type = expr_type.add_self_type(soft_inferrer.current_type)

        expr_name = expr_type.generate_name()
        if not conforms(expr_type, node_type):
            soft_inferrer.add_error(
                node,
                (
                    f"TypeError: In class '{soft_inferrer.current_type.name}'"
                    f" '{node.id}' expression type({expr_name}) does not conforms"
                    f" to declared type ({node_type.name})."
                ),
            )
        if added_type:
            expr_type.remove_self_type(soft_inferrer.current_type)

        attr_node.expr = expr_node
        attr_node.inferred_type = expr_type
        return attr_node

    @staticmethod
    def deep_infer(node, scope, deep_inferrer):
        attr_node = AttrDeclarationNode(node)
        attr_node.inferred_type = node.inferred_type

        if not node.expr:
            return attr_node

        expr_node = deep_inferrer.visit(node.expr, scope)
        expr_type = expr_node.inferred_type

        attr_node.expr = expr_node
        if equal(expr_type, node.expr.inferred_type):
            return attr_node

        expr_name = expr_type.generate_name()
        node_type = attr_node.inferred_type
        if not conforms(expr_type, attr_node.inferred_type):
            deep_inferrer.add_error(
                node,
                (
                    f"TypeError: In class '{deep_inferrer.current_type.name}' attribue"
                    f"'{node.id}' expression type({expr_name}) does not conforms"
                    f"to declared type ({node_type.name})."
                ),
            )

        return attr_node


class MethodDeclarationNode(DeclarationNode):
    def __init__(self, params, return_type, body, node):
        super().__init__(node)
        self.id = node.id
        self.params = params
        self.type = return_type
        self.body = body

    @staticmethod
    def soft_infer(node, scope, soft_inferrer):

        scope = scope.create_child()
        current_method = soft_inferrer.current_type.get_method(node.id)

        new_params = []
        param_names = list(zip(node.param_names[0], node.param_names[1]))

        for idx, type, param in zip(
            current_method.param_names, current_method.param_types, param_names
        ):

            scope.define_variable(idx, type)
            new_params.append(param)

        ret_type_decl: TypeBag = current_method.return_type

        body_node = soft_inferrer.visit(node.body, scope)
        ret_type_expr = body_node.inferenced_type
        added_self = ret_type_expr.add_self_type(soft_inferrer.current_type)

        ret_expr_name = ret_type_expr.generate_name()
        if not conforms(ret_type_expr, ret_type_decl):
            soft_inferrer.add_error(
                node.body,
                f"TypeError: In Class '{soft_inferrer.current_type.name}' method"
                f" '{current_method.name}' return expression type({ret_expr_name})"
                f" does not conforms to declared return type ({ret_type_decl.name})",
            )

        if added_self:
            ret_type_expr.remove_self_type(soft_inferrer.current_type)

        method_node = inf_ast.MethodDeclarationNode(
            new_params, node.type, body_node, node
        )
        method_node.exec_inferred_type = ret_type_expr
        method_node.inferred_type = ret_type_decl
        return method_node

    @staticmethod
    def deep_infer(node, scope, deep_inferrer):
        scope = scope.next_child()
        current_method = deep_inferrer.current_type.get_method(node.id)
        new_params = []
        for _, __, param in zip(
            current_method.param_names, current_method.param_types, node.params
        ):
            new_params.append(param)

        body_node = deep_inferrer.visit(node.body, scope)
        body_type = body_node.inferred_type
        method_node = MethodDeclarationNode(
            new_params, node.type, body_node, node)
        method_node.inferred_type = node.inferred_type

        if equal(body_type, node.body.inferred_type):
            method_node.exec_inferred_type = body_type
            return method_node

        node_type = method_node.inferred_type
        body_name = body_type.generate_name()
        if not conforms(body_type, node_type):
            deep_inferrer.add_error(
                body_node,
                f"TypeError: In Class '{deep_inferrer.current_type.name}' method "
                f"'{method_node.id}' return expression type({body_name})"
                f" does not conforms to declared return type ({node_type.name})",
            )

        return method_node


class ParamNode(DeclarationNode):
    def __init__(self, node, idx: str, typex) -> None:
        super().__init__(node)
        self.id = idx
        self.type = typex
