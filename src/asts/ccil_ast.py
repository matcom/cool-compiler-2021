from typing import Dict, List, Tuple
from __future__ import annotations


class Node:
    def __init__(self, node) -> None:
        self.line: int = node.line
        self.col: int = node.col

    def get_position(self) -> Tuple[int, int]:
        return (self.line, self.col)


class OperationNode(Node):
    """
    Base Class for all operation Nodes
    """

    def __init__(self, node) -> None:
        super().__init__(node)


class StorageNode(OperationNode):
    def __init__(self, node, idx: str, operation: ReturnOpNode) -> None:
        """
        Node used to store the value of operations done.
        Parameters:
        node <- Node to maintain knowledge of colummn and position in the original code.
        idx <- Id of this node.
        opeartion <- The operation this node is storing.
        """
        super().__init__(node)
        self.id = idx
        self.operation = operation


class ReturnOpNode(OperationNode):
    def __init__(self, node) -> None:
        super().__init__(node)


class BinaryOpNode(ReturnOpNode):
    def __init__(self, node, left: AtomOpNode, right: AtomOpNode) -> None:
        """
        Node that represents all binary operation
        Parameters:
        left <- Left atomic node.
        right <- Right atomic node.
        """
        super().__init__(node)
        self.left = left
        self.right = right


class AtomOpNode(ReturnOpNode):
    def __init__(self, node) -> None:
        """
        AtomNode represents all single value nodes, like ids and constants
        """
        super().__init__(node)


class IdNode(AtomOpNode):
    def __init__(self, node, idx: str) -> None:
        super().__init__(node)
        self.id = idx


class ConstantNode(AtomOpNode):
    def __init__(self, node) -> None:
        super().__init__(node)


class FlowControlNode(OperationNode):
    """
    Base class for all flow control operations like If, Label, goto, etc...
    """

    def __init__(self, node) -> None:
        super().__init__(node)


class IfNode(FlowControlNode):
    def __init__(self, node, eval_value: StorageNode, target: LabelNode) -> None:
        super().__init__(node)
        self.eval_value = eval_value
        self.target = target


class IfFalseNode(IfNode):
    def __init__(self, node, eval_value: StorageNode, target: LabelNode) -> None:
        super().__init__(node, eval_value, target)


class GoToNode(FlowControlNode):
    def __init__(self, node, target: LabelNode) -> None:
        super().__init__(node)
        self.target = target


class LabelNode(FlowControlNode):
    def __init__(self, node, idx: str) -> None:
        super().__init__(node)
        self.id = idx


def create_assignation(node, idx: str, target: str):
    return StorageNode(node, idx, IdNode(node, target))
