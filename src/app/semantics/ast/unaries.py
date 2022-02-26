from .base import UnaryNode

from app.semantics.tools import (
    conforms,
    equal,
)


class IsVoidNode(UnaryNode):
    def infer(node, scope, deep_inferrer):
        node_expr = deep_inferrer.visit(node.expr, scope)
        is_void_node = IsVoidNode(node_expr, node)
        is_void_node.inferenced_type = deep_inferrer.context.get_type("Bool")
        return is_void_node


class NotNode(UnaryNode):
    @staticmethod
    def infer(node, scope, deep_inferrer):
        expr_node = deep_inferrer.visit(node.expr, scope)
        expr_type = expr_node.inferenced_type
        bool_type = deep_inferrer.context.get_type("Bool")
        if not equal(expr_type, node.expr.inferenced_type):
            expr_clone = expr_type.clone()
            if not conforms(expr_type, bool_type):
                deep_inferrer.add_error(
                    node,
                    f"TypeError: Not's expresion type({expr_clone.name} does not"
                    " conforms to Bool type",
                )

        not_node = NotNode(expr_node, node)
        not_node.inferenced_type = bool_type
        return not_node


class ComplementNode(UnaryNode):

    @staticmethod
    def infer(node, scope, deep_inferrer):
        expr_node = deep_inferrer.visit(node.expr, scope)
        expr_type = expr_node.inferenced_type
        int_type = deep_inferrer.context.get_type("Int")
        if not equal(expr_type, node.expr.inferenced_type):
            expr_clone = expr_type.clone()
            if not conforms(expr_type, int_type):
                deep_inferrer.add_error(
                    node,
                    f"TypeError: ~ expresion type({expr_clone.name} does not"
                    " conforms to Int type",
                )

        complement_node = ComplementNode(expr_node, node)
        complement_node.inferenced_type = int_type
        return complement_node
