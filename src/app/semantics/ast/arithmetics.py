from .base import BinaryNode
from app.semantics.tools.errors import InternalError
import app.parser.ast as parser_node
from app.semantics.constants import *


class ArithmeticNode(BinaryNode):
    def soft_infer(node, scope, soft_inferrer):
        left_node, right_node = soft_inferrer._arithmetic_operation(
            node, scope)
        if isinstance(node, parser_node.PlusNode):
            arith_node = PlusNode(left_node, right_node, node)
        elif isinstance(node, parser_node.MinusNode):
            arith_node = MinusNode(left_node, right_node, node)
        elif isinstance(node, parser_node.MultNode):
            arith_node = StarNode(left_node, right_node, node)
        elif isinstance(node, parser_node.DivNode):
            arith_node = DivNode(left_node, right_node, node)
        else:
            raise Exception("Unknown arithmetic node detected")

        arith_node.inferenced_type = soft_inferrer.context.get_type(
            INT_TYPE)
        return arith_node

    @staticmethod
    def deep_infer(node, scope, deep_inferrer):
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

        arith_node.inferred_type = deep_inferrer.context.get_type("Int")
        return arith_node


class PlusNode(ArithmeticNode):
    pass


class MinusNode(ArithmeticNode):
    pass


class StarNode(ArithmeticNode):
    pass


class DivNode(ArithmeticNode):
    pass
