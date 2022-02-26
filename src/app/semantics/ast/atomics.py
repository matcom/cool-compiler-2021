from .base import ExpressionNode
from app.semantics.tools import TypeBag


class AtomicNode(ExpressionNode):
    def __init__(self, node):
        super().__init__(node)
        self.value = node.value


class VariableNode(AtomicNode):
    def __init__(self, node):
        super().__init__(node)
        self.defined = False

    @staticmethod
    def infer(node, scope, deep_inferrer):
        var_node = VariableNode(node)
        if not node.defined:
            var_node.inferenced_type = TypeBag(set())
            return var_node

        var_node.defined = True
        var = scope.get_variable(node.value)
        var_node.inferenced_type = var.get_type()
        return var_node


class InstantiateNode(ExpressionNode):
    @staticmethod
    def infer(node, _, __):
        instantiate_node = InstantiateNode(node)
        instantiate_node.inferenced_type = node.inferenced_type
        return instantiate_node

    def __init__(self, node):
        super().__init__(node)
        self.value = node.type
        self.type = node.type


class BooleanNode(AtomicNode):
    def infer(node, _, deep_inferrer):
        bool_node = BooleanNode(node)
        bool_node.inferenced_type = deep_inferrer.context.get_type("Bool")
        return bool_node
    pass


class IntNode(AtomicNode):
    def infer(node, _, deep_inferrer):
        int_node = IntNode(node)
        int_node.inferenced_type = deep_inferrer.context.get_type("Int")
        return int_node


class StringNode(AtomicNode):
    def infer(node, _, deep_inferrer):
        str_node = StringNode(node)
        str_node.inferenced_type = deep_inferrer.context.get_type("String")
        return str_node
    pass
