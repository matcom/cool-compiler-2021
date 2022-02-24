from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, List, Tuple

from code_gen.tools import Attribute, Method
from semantics.tools.type import Type


@dataclass(frozen=True)
class CCILProgram:
    """Top level class that represents a CCIL program"""

    types_section: List[Class]
    code_section: List[FunctionNode]
    data_section: List[str]  # no idea what will be this the node,


@dataclass(frozen=True)
class Class:
    """
    This item represent the .type section in ccil
    """

    id: str
    attributes: List[Attribute]
    methods: List[Method]
    init_operations: FunctionNode


@dataclass(frozen=True)
class BaseVar:
    """
    This item represents the <id, type> pair common in attributes, parameters and local vars
    """

    id: str
    type: str


class Attribute(BaseVar):
    pass


class Parameter(BaseVar):
    pass


class Local(BaseVar):
    pass


@dataclass(frozen=True)
class Data:
    """
    This class hold constant values
    """

    id: str
    value: str


@dataclass(frozen=True)
class Method:
    """
    This item represent the method of every class
    """

    id: str
    function: FunctionNode


class Node:
    pass


class FunctionNode(Node):
    """
    This class represents funtions in the .code section. Most of a Cool program is split along this nodes.
    """

    def __init__(
        self,
        idx: str,
        params: List[Parameter],
        locals: List[Local],
        operations: List[OperationNode],
        ret: str,
    ) -> None:
        super().__init__()
        # Function identifier, different than Method identifier
        self.id = idx
        # Variable that holds the return value
        self.ret = ret
        # Function operations
        self.params = params
        self.locals = locals
        self.operations = operations


class OperationNode(Node):
    """
    Base Class for all operation Nodes
    """

    def __init__(self) -> None:
        super().__init__()


class StorageNode(OperationNode):
    def __init__(self, idx: str, operation: ReturnOpNode) -> None:
        """
        Node used to store the value of operations done.
        Parameters:
        node <- Node to maintain knowledge of colummn and position in the original code.
        idx <- Id of this node.
        opeartion <- The operation this node is storing.
        """
        super().__init__()
        self.id = idx
        self.operation = operation


class SetAttrOpNode(OperationNode):
    def __init__(self, type_id: str, attr_id: str, source_id: AtomOpNode) -> None:
        self.type = type_id
        self.attr = attr_id
        self.source_id = source_id


class Abort(OperationNode):
    pass


class PrintOpNode(OperationNode):
    def __init__(self, idx: str) -> None:
        super().__init__()
        self.idx = idx


class ReturnOpNode(OperationNode):
    def __init__(
        self,
    ) -> None:
        super().__init__()


class ReadStrNode(ReturnOpNode):
    """
    This nodes reads a string from the standard input
    """

    pass


class ReadIntNode(ReturnOpNode):
    """
    This nodes reads an int from the standard input
    """


class GetAttrOpNode(ReturnOpNode):
    def __init__(self, instance_type_id: str, instance_id: str, attr_id: str) -> None:
        super().__init__()
        self.instance_type = instance_type_id
        self.instance = instance_id
        self.attr = attr_id


class CallOpNode(ReturnOpNode):
    def __init__(self, idx: str, type_idx: str, args: List[str]) -> None:
        super().__init__()
        self.id = idx
        self.type = type_idx
        self.args = args


class VCallOpNode(ReturnOpNode):
    def __init__(self, idx: str, type_idx: str, args: List[str]) -> None:
        super().__init__()
        self.id = idx
        self.type = type_idx
        self.args = args


class VoidNode(ReturnOpNode):
    """Operation that indicate that the Storage Node is not initialized"""

    pass


class NewOpNode(ReturnOpNode):
    def __init__(self, type_idx: str) -> None:
        super().__init__()
        self.type_idx: str = type_idx


class BinaryOpNode(ReturnOpNode):
    def __init__(self, left: AtomOpNode, right: AtomOpNode) -> None:
        """
        Node that represents all binary operation
        Parameters:
        left <- Left atomic node.
        right <- Right atomic node.
        """
        super().__init__()
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
    def __init__(self, atom: AtomOpNode) -> None:
        super().__init__()
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


class ChainOpNode(ReturnOpNode):
    def __init__(self, target: str) -> None:
        super().__init__()
        self.target = target


class LoadOpNode(ChainOpNode):
    pass


class LengthOpNode(ChainOpNode):
    pass


class StrOpNode(ChainOpNode):
    pass


class ConcatOpNode(ChainOpNode):
    def __init__(self, source: str, target: str) -> None:
        super().__init__(target)
        self.source = source


class SubstringOpNode(ReturnOpNode):
    def __init__(self, start: AtomOpNode, length: AtomOpNode) -> None:
        super().__init__()
        self.start = start
        self.length = length


class AtomOpNode(ReturnOpNode):
    def __init__(self, value: str) -> None:
        """
        AtomNode represents all single value nodes, like ids and constants
        """
        super().__init__()
        self.value = value


class IdNode(AtomOpNode):
    def __init__(self, value: str) -> None:
        super().__init__(value)


class ConstantNode(AtomOpNode):
    def __init__(self, value: str) -> None:
        super().__init__(value)


class IntNode(ConstantNode):
    def __init__(self, value: str) -> None:
        super().__init__(value)


class FlowControlNode(OperationNode):
    """
    Base class for all flow control operations like If, Label, goto, etc...
    """

    def __init__(self, node) -> None:
        super().__init__(node)


class CurrentTypeNameNode(ReturnOpNode):
    def __init__(self) -> None:
        super().__init__()


class IfNode(FlowControlNode):
    def __init__(self, eval_value: AtomOpNode, target: LabelNode) -> None:
        super().__init__()
        self.eval_value = eval_value
        self.target = target


class IfFalseNode(IfNode):
    def __init__(self, eval_value: AtomOpNode, target: LabelNode) -> None:
        super().__init__(eval_value, target)


class GoToNode(FlowControlNode):
    def __init__(self, target: LabelNode) -> None:
        super().__init__()
        self.target = target


class LabelNode(FlowControlNode):
    def __init__(self, idx: str) -> None:
        super().__init__()
        self.id = idx


def extract_id(storage_node: StorageNode) -> IdNode:
    return IdNode(storage_node.id)
