from .base import ExpressionNode
from app.semantics.tools import TypeBag
from app.semantics.tools.errors import SemanticError
from app.semantics.constants import *


class AtomicNode(ExpressionNode):
    def __init__(self, node):
        super().__init__(node)
        self.value = node.value


class VariableNode(AtomicNode):
    def __init__(self, node):
        super().__init__(node)
        self.defined = False

    @staticmethod
    def shallow_infer(node, scope, shallow_inferrer):
        var_node = VariableNode(node)

        var = scope.find_variable(node.value)
        if var:
            var_node.defined = True
            var_type = var.get_type()
        else:
            shallow_inferrer.add_error(
                node, f"NameError: Variable '{node.value}' is not defined.")
            var_type = TypeBag(set())

        var_node.inferred_type = var_type
        return var_node

    @staticmethod
    def deep_infer(node, scope, deep_inferrer):
        var_node = VariableNode(node)
        if not node.defined:
            var_node.inferred_type = TypeBag(set())
            return var_node

        var_node.defined = True
        var = scope.get_variable(node.value)
        var_node.inferred_type = var.get_type()
        return var_node


class InstantiateNode(ExpressionNode):
    def shallow_infer(node, _, shallow_inferrer):
        instantiate_node = InstantiateNode(node)
        try:
            node_type = shallow_inferrer.context.get_type(
                node.type, autotype=False)
        except SemanticError as err:
            shallow_inferrer.add_error(
                node,
                err.text + f" Could not instantiate type '{node.type}'.",
            )
            node_type = TypeBag(set())

        instantiate_node.inferred_type = node_type
        return instantiate_node

    @staticmethod
    def deep_infer(node, _, __):
        instantiate_node = InstantiateNode(node)
        instantiate_node.inferred_type = node.inferred_type
        return instantiate_node

    def __init__(self, node):
        super().__init__(node)
        self.value = node.type
        self.type = node.type


class BooleanNode(AtomicNode):
    def shallow_infer(node, _, shallow_inferrer):
        bool_node = BooleanNode(node)
        bool_node.inferred_type = shallow_inferrer.context.get_type(
            BOOL_TYPE)
        return bool_node

    def deep_infer(node, _, deep_inferrer):
        bool_node = BooleanNode(node)
        bool_node.inferred_type = deep_inferrer.context.get_type(BOOL_TYPE)
        return bool_node


class IntNode(AtomicNode):
    def shallow_infer(node, _, shallow_inferrer):
        int_node = IntNode(node)
        int_node.inferred_type = shallow_inferrer.context.get_type(INT_TYPE)
        return int_node

    def deep_infer(node, _, deep_inferrer):
        int_node = IntNode(node)
        int_node.inferred_type = deep_inferrer.context.get_type(INT_TYPE)
        return int_node


class StringNode(AtomicNode):
    def shallow_infer(node, _, shallow_inferrer):
        string_node = StringNode(node)
        string_node.inferred_type = shallow_inferrer.context.get_type(
            STRING_TYPE)
        return string_node

    def deep_infer(node, _, deep_inferrer):
        str_node = StringNode(node)
        str_node.inferred_type = deep_inferrer.context.get_type(STRING_TYPE)
        return str_node
    pass
