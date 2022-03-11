from .base import BinaryNode

from app.semantics.constants import *


class ComparerNode(BinaryNode):
    pass


class LessNode(ComparerNode):
    @staticmethod
    def soft_infer(node, scope, soft_inferrer):
        left_node, right_node = soft_inferrer._arithmetic_operation(
            node, scope)
        less_node = LessNode(left_node, right_node, node)
        less_node.inferred_type = soft_inferrer.context.get_type(
            BOOL_TYPE)
        return less_node

    @staticmethod
    def deep_infer(node, scope, deep_inferrer):
        left_node, right_node = deep_inferrer._arithmetic_operation(
            node, scope)
        less_node = LessNode(left_node, right_node, node)
        less_node.inferred_type = deep_inferrer.context.get_type(BOOL_TYPE)
        return less_node


class LessOrEqualNode(ComparerNode):

    @staticmethod
    def soft_infer(node, scope, soft_inferrer):
        left_node, right_node = soft_inferrer._arithmetic_operation(
            node, scope)
        lesseq_node = LessOrEqualNode(left_node, right_node, node)
        lesseq_node.inferred_type = soft_inferrer.context.get_type(
            BOOL_TYPE)
        return lesseq_node

    @staticmethod
    def deep_infer(node, scope, deep_inferrer):
        left_node, right_node = deep_inferrer._arithmetic_operation(
            node, scope)
        lesseq_node = LessOrEqualNode(left_node, right_node, node)
        lesseq_node.inferred_type = deep_inferrer.context.get_type(BOOL_TYPE)
        return lesseq_node


class EqualsNode(ComparerNode):
    def soft_infer(node, scope, soft_inferrer):
        left_node = soft_inferrer.visit(node.left_expr, scope)
        right_node = soft_inferrer.visit(node.right_expr, scope)

        equal_node = EqualsNode(left_node, right_node, node)
        equal_node.inferred_type = soft_inferrer.context.get_type(
            BOOL_TYPE)
        return equal_node

    @staticmethod
    def deep_infer(node, scope, deep_inferrer):
        left_node = deep_inferrer.visit(node.left, scope)
        right_node = deep_inferrer.visit(node.right, scope)

        deep_inferrer._check_member_types(left_node, right_node)

        eq_node = EqualsNode(left_node, right_node, node)
        eq_node.inferred_type = node.inferred_type  # Bool Type :)
        return eq_node
