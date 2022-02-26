from .base import DeclarationNode
from app.semantics.tools import (
    conforms,
    equal,
)


class ClassDeclarationNode(DeclarationNode):
    def __init__(self, features, node):
        super().__init__(node)
        self.features = features
        self.id = node.id
        self.parent = node.parent

    @staticmethod
    def infer(node, scope, hard_inferrer):
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
    def infer(node, scope, deep_inferrer):
        attr_node = AttrDeclarationNode(node)
        attr_node.inferenced_type = node.inferenced_type

        if not node.expr:
            return attr_node

        expr_node = deep_inferrer.visit(node.expr, scope)
        expr_type = expr_node.inferenced_type

        attr_node.expr = expr_node
        if equal(expr_type, node.expr.inferenced_type):
            return attr_node

        expr_name = expr_type.generate_name()
        node_type = attr_node.inferenced_type
        if not conforms(expr_type, attr_node.inferenced_type):
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
    def infer(node, scope, deep_inferrer):
        scope = scope.next_child()
        current_method = deep_inferrer.current_type.get_method(node.id)
        # print(f'En el hardinferer: {node.params}')
        new_params = []
        for idx, typex, param in zip(
            current_method.param_names, current_method.param_types, node.params
        ):
            new_params.append(param)

        body_node = deep_inferrer.visit(node.body, scope)
        body_type = body_node.inferenced_type
        method_node = MethodDeclarationNode(
            new_params, node.type, body_node, node)
        method_node.inferenced_type = node.inferenced_type

        if equal(body_type, node.body.inferenced_type):
            method_node.exec_inferred_type = body_type
            return method_node

        node_type = method_node.inferenced_type
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
