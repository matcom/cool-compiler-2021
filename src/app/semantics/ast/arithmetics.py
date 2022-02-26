from .base import BinaryNode
from app.semantics.tools.errors import InternalError


class ArithmeticNode(BinaryNode):
    @staticmethod
    def infer(node, scope, deep_inferrer):
        left_node, right_node = deep_inferrer._arithmetic_operation(
            node, scope)
        if isinstance(node, PlusNode):
            arith_node = PlusNode(left_node, right_node, node)
        elif isinstance(node, MinusNode):
            arith_node = MinusNode(left_node, right_node, node)
        elif isinstance(node, StarNode):
            arith_node = StarNode(left_node, right_node, node)
        elif isinstance(node, DivNode):
            arith_node = DivNode(left_node, right_node, node)
        else:
            raise InternalError("This should never happen")

        arith_node.inferenced_type = deep_inferrer.context.get_type("Int")
        return arith_node


class PlusNode(ArithmeticNode):
    pass


class MinusNode(ArithmeticNode):
    pass


class StarNode(ArithmeticNode):
    pass


class DivNode(ArithmeticNode):
    pass
