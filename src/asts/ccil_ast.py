from typing import Dict, List, Tuple
from __future__ import annotations
from code_gen.tools import Attribute, Method

from semantics.tools.type import Type


class Node:
    def __init__(self, node) -> None:
        self.line: int = node.line
        self.col: int = node.col

    def get_position(self) -> Tuple[int, int]:
        return (self.line, self.col)


class ClassNode(Node):
    def __init__(
        self,
        node,
        attributes: List[Attribute],
        methods: List[Method],
        init_operations: List[OperationNode],
    ) -> None:
        super().__init__(node)
        self.attributes = attributes
        self.methods = methods
        self.init_operations = init_operations


class MethodNode(Node):
    def __init__(self, node, idx: str, operations: List[OperationNode]) -> None:
        super().__init__(node)
        self.id = idx
        self.operations = operations


class OperationNode(Node):
    """
    Base Class for all operation Nodes
    """

    def __init__(self, node) -> None:
        super().__init__(node)


class LocalNode(OperationNode):
    def __init__(self, node, idx: str, typex: str) -> None:
        """
        Node represent initalization instruction"
        Parameter:
            idx <- node name
            type <- node type
        """
        super().__init__(node)
        assert isinstance(typex, str), "Typex is not string"

        self.id: str = idx
        self.type: str = typex.name


class ParamNode(LocalNode):
    def __init__(self, node, idx: str, typex: str) -> None:
        """
        Node represent function parameter initalization instruction"
        Parameter:
            idx <- node name
            type <- node type
        """
        super().__init__(node, idx, typex)


class ArgNode(OperationNode):
    def __init__(self, node, idx: str) -> None:
        super().__init__(node)
        self.id = idx


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
        self.decl_type = node.decl_type


class ReturnOpNode(OperationNode):
    def __init__(self, node) -> None:
        super().__init__(node)


class CallOpNode(ReturnOpNode):
    def __init__(self, node, idx: str) -> None:
        super().__init__(node)
        self.id = idx


class VCallOpNode(ReturnOpNode):
    def __init__(self, node, idx: str, type_idx: str) -> None:
        super().__init__(node, idx)
        self.type = type_idx


class VoidNode(ReturnOpNode):
    """Operation that indicate that the Storage Node is not initialized"""

    pass


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


class SumOpNode(BinaryOpNode):
    pass


class MinusOpNode(BinaryOpNode):
    pass


class MultOpNode(BinaryOpNode):
    pass


class DivOpNode(BinaryOpNode):
    pass


class EqualOpNode(BinaryOpNode):
    pass


class LessOrEqualOpNode(BinaryOpNode):
    pass


class LessOpNode(BinaryOpNode):
    pass


class UnaryOpNode(ReturnOpNode):
    def __init__(self, node, atom: AtomOpNode) -> None:
        super().__init__(node)
        self.atom = atom


class GetTypeOpNode(UnaryOpNode):
    """Extracts the type of a node"""

    pass


class IsVoidOpNode(UnaryOpNode):
    """Operation that returns true if the Storage Node is uninitialized"""

    pass


class NotOpNode(UnaryOpNode):
    pass


class NegOpNode(UnaryOpNode):
    pass


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
    def __init__(self, node, eval_value: AtomOpNode, target: LabelNode) -> None:
        super().__init__(node)
        self.eval_value = eval_value
        self.target = target


class IfFalseNode(IfNode):
    def __init__(self, node, eval_value: AtomOpNode, target: LabelNode) -> None:
        super().__init__(node, eval_value, target)


class GoToNode(FlowControlNode):
    def __init__(self, node, target: LabelNode) -> None:
        super().__init__(node)
        self.target = target


class LabelNode(FlowControlNode):
    def __init__(self, node, idx: str) -> None:
        super().__init__(node)
        self.id = idx


def create_call(node, storage_idx: str, method_idx: str):
    return StorageNode(node, storage_idx, CallOpNode(node, method_idx))


def create_vcall(node, storage_idx: str, method_idx: str, type_idx: str):
    return StorageNode(node, storage_idx, VCallOpNode(node, method_idx, type_idx))


def create_assignation(node, idx: str, target: str):
    return StorageNode(node, idx, IdNode(node, target))


def create_uninitialized_storage(node, idx: str):
    return StorageNode(node, idx, VoidNode(node))


def create_type_of(node, idx: str, target: AtomOpNode):
    return StorageNode(node, idx, GetTypeOpNode(node, target))


def create_equality(node, idx, left: AtomOpNode, right: AtomOpNode):
    return StorageNode(node, idx, EqualOpNode(node, left, right))


def extract_id(node, storage_node: StorageNode) -> IdNode:
    return IdNode(node, storage_node.id)
