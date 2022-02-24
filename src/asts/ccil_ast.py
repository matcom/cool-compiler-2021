from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, List, Tuple

from semantics.tools.type import Type


@dataclass(frozen=True)
class CCILProgram:
    """Top level class that represents a CCIL program"""

    types_section: List[Class]
    code_section: List[FunctionNode]
    data_section: List[str]  # no idea what will be this the node,

    def __str__(self) -> str:
        types = "\n".join(str(type) for type in self.types_section)
        data = "\n".join(str(data) for data in self.data_section)
        code = "\n".join(str(func) for func in self.code_section)
        return f"TYPES:\n{types}\nDATA:\n{data}\nCODE:\n{code} "


@dataclass(frozen=True)
class Class:
    """
    This item represent the .type section in ccil
    """

    id: str
    attributes: List[Attribute]
    methods: List[Method]
    init_operations: FunctionNode

    def __str__(self) -> str:
        attributes = "\n".join(str(a) for a in self.attributes)
        methods = "\n".join(str(m) for m in self.methods)
        return f"\ttype {self.id} {{ {attributes} \n {methods} \n\t}}"


@dataclass(frozen=True)
class BaseVar:
    """
    This item represents the <id, type> pair common in attributes, parameters and local vars
    """

    id: str
    type: str

    def __str__(self) -> str:
        return f"{self.id} : {self.type}"


class Attribute(BaseVar):
    def __str__(self) -> str:
        return "\t\tattr " + super().__str__()


class Parameter(BaseVar):
    def __str__(self) -> str:
        return "\t\tparam " + super().__str__()


class Local(BaseVar):
    def __str__(self) -> str:
        return "\t\tlocal " + super().__str__()


@dataclass(frozen=True)
class Data:
    """
    This class hold constant values
    """

    id: str
    value: str

    def __str__(self) -> str:
        return f"\t{self.id} : '{self.value}'"


@dataclass(frozen=True)
class Method:
    """
    This item represent the method of every class
    """

    id: str
    function: FunctionNode

    def __str__(self) -> str:
        return f"\t\tmethod {self.id} : {self.function.id}"


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

    def __str__(self) -> str:
        params = "\n".join(str(p) for p in self.params)
        locals = "\n".join(str(l) for l in self.locals)
        ops = "\n".join(str(o) for o in self.operations)

        return f"\tfunc {self.id}:\n {params}\n {locals} \n {ops} \n \t\treturn {self.ret.id}"


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

    def __str__(self) -> str:
        return f"\t\t{self.id} = {str(self.operation)}"


class SetAttrOpNode(OperationNode):
    def __init__(
        self, instance_id: str, attr_id: str, new_value: AtomOpNode, instance_type: str
    ) -> None:
        self.instance_type = instance_type
        self.new_value = new_value
        self.attr = attr_id
        self.instance = instance_id


class Abort(OperationNode):
    def __str__(self) -> str:
        return "abort"


class PrintOpNode(OperationNode):
    def __init__(self, idx: str) -> None:
        super().__init__()
        self.id = idx

    def __str__(self) -> str:
        return f"print {self.id}"


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

    def __str__(self) -> str:
        return f"concat {self.source} {self.target}"


class SubstringOpNode(ReturnOpNode):
    def __init__(self, start: AtomOpNode, length: AtomOpNode) -> None:
        super().__init__()
        self.start = start
        self.length = length

    def __str__(self) -> str:
        return f"substr {self.start.value} {self.length.value}"


class AtomOpNode(ReturnOpNode):
    def __init__(self, value: str) -> None:
        """
        AtomNode represents all single value nodes, like ids and constants
        """
        super().__init__()
        self.value = str(value)

    def __str__(self) -> str:
        return self.value


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

    def __str__(self) -> str:
        return f"if {self.eval_value.value} goto {self.target.id}"


class IfFalseNode(IfNode):
    def __init__(self, eval_value: AtomOpNode, target: LabelNode) -> None:
        super().__init__(eval_value, target)

    def __str__(self) -> str:
        return f"ifFalse {self.eval_value.value} goto {self.target.id}"


class GoToNode(FlowControlNode):
    def __init__(self, target: LabelNode) -> None:
        super().__init__()
        self.target = target

    def __str__(self) -> str:
        return f"goto {self.target.id}"


class LabelNode(FlowControlNode):
    def __init__(self, idx: str) -> None:
        super().__init__()
        self.id = idx

    def __str__(self) -> str:
        return f"label {self.id}"


def extract_id(storage_node: StorageNode) -> IdNode:
    return IdNode(storage_node.id)
