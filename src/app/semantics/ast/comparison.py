from .base import BinaryNode


class ComparerNode(BinaryNode):
    pass


class LessNode(ComparerNode):
    @staticmethod
    def infer(node, scope, deep_inferrer):
        left_node, right_node = deep_inferrer._arithmetic_operation(
            node, scope)
        less_node = LessNode(left_node, right_node, node)
        less_node.inferenced_type = deep_inferrer.context.get_type("Bool")
        return less_node


class LessOrEqualNode(ComparerNode):
    @staticmethod
    def infer(node, scope, deep_inferrer):
        left_node, right_node = deep_inferrer._arithmetic_operation(
            node, scope)
        lesseq_node = LessOrEqualNode(left_node, right_node, node)
        lesseq_node.inferenced_type = deep_inferrer.context.get_type("Bool")
        return lesseq_node


class EqualsNode(ComparerNode):
    @staticmethod
    def infer(node, scope, deep_inferrer):
        left_node = deep_inferrer.visit(node.left, scope)
        right_node = deep_inferrer.visit(node.right, scope)

        deep_inferrer._check_member_types(left_node, right_node)

        eq_node = EqualsNode(left_node, right_node, node)
        eq_node.inferenced_type = node.inferenced_type  # Bool Type :)
        return eq_node
