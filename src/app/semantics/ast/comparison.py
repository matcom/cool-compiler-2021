from .base import BinaryNode

from app.semantics.constants import *


class ComparerNode(BinaryNode):
    pass


class LessNode(ComparerNode):
    @staticmethod
    def shallow_infer(node, scope, shallow_inferrer):
        left_node, right_node = shallow_inferrer._arithmetic_operation(
            node, scope)
        less_node = LessNode(left_node, right_node, node)
        less_node.inferenced_type = shallow_inferrer.context.get_type(
            BOOL_TYPE)
        return less_node

    @staticmethod
    def deep_infer(node, scope, deep_inferrer):
        left_node, right_node = deep_inferrer._arithmetic_operation(
            node, scope)
        less_node = LessNode(left_node, right_node, node)
        less_node.inferenced_type = deep_inferrer.context.get_type(BOOL_TYPE)
        return less_node


class LessOrEqualNode(ComparerNode):

    @staticmethod
    def shallow_infer(node, scope, shallow_inferrer):
        left_node, right_node = shallow_inferrer._arithmetic_operation(
            node, scope)
        lesseq_node = LessOrEqualNode(left_node, right_node, node)
        lesseq_node.inferenced_type = shallow_inferrer.context.get_type(
            BOOL_TYPE)
        return lesseq_node

    @staticmethod
    def deep_infer(node, scope, deep_inferrer):
        left_node, right_node = deep_inferrer._arithmetic_operation(
            node, scope)
        lesseq_node = LessOrEqualNode(left_node, right_node, node)
        lesseq_node.inferenced_type = deep_inferrer.context.get_type(BOOL_TYPE)
        return lesseq_node


class EqualsNode(ComparerNode):
    def shallow_infer(node, scope, shallow_inferrer):
        left_node = shallow_inferrer.visit(node.left_expr, scope)
        right_node = shallow_inferrer.visit(node.right_expr, scope)

        equal_node = EqualsNode(left_node, right_node, node)
        equal_node.inferenced_type = shallow_inferrer.context.get_type(
            BOOL_TYPE)
        return equal_node

    @staticmethod
    def deep_infer(node, scope, deep_inferrer):
        left_node = deep_inferrer.visit(node.left, scope)
        right_node = deep_inferrer.visit(node.right, scope)

        deep_inferrer._check_member_types(left_node, right_node)

        eq_node = EqualsNode(left_node, right_node, node)
        eq_node.inferenced_type = node.inferenced_type  # Bool Type :)
        return eq_node
