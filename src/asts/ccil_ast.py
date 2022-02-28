from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, List, Tuple

from semantics.tools.type import Type


@dataclass(frozen=True)
class CCILProgram:
    """Top level class that represents a CCIL program"""

    entry_func: FunctionNode
    types_section: List[Class]
    code_section: List[FunctionNode]
    data_section: List[Data]

    def __str__(self, all=False) -> str:
        types_section = self.types_section
        code_section = self.code_section
        if not all:
            types_section = self.types_section[3:]
            code_section = self.code_section[10:]

        ident = "\t"
        types = "\n".join(ident + str(type) for type in types_section)
        data = "\n".join(ident + str(data) for data in self.data_section)
        code = "\n".join(str(func) for func in code_section)
        return f"TYPES:\n{types}\nDATA:\n{data}\nCODE:\n{code} "


@dataclass(frozen=False)
class Class:
    """
    This item represent the .type section in ccil
    """

    id: str
    attributes: List[Attribute]
    methods: List[Method]
    init_operations: FunctionNode

    def __str__(self, all=False) -> str:
        ident = "\t\t"
        attributes = "\n".join(ident + str(a) for a in self.attributes)
        methods = "\n".join(ident + str(m) for m in self.methods)
        init_function = "\n" + str(self.init_operations) + "\n" if all else ""
        return f"type {self.id} {{\n {attributes} \n {methods} \n  {init_function}\t}}"


@dataclass(frozen=True)
class BaseVar:
    """
    This item represents the <id, type> pair common in attributes, parameters and local vars
    """

    id: str
    type: str

    def __str__(self) -> str:
        return f"{self.id} : {self.type}"


@dataclass(frozen=True)
class Attribute(BaseVar):
    cool_id: str

    def __str__(self) -> str:
        return "attr " + super().__str__()


class Parameter(BaseVar):
    def __str__(self) -> str:
        return "param " + super().__str__()


class Local(BaseVar):
    def __str__(self) -> str:
        return "local " + super().__str__()


@dataclass(frozen=True)
class Data:
    """
    This class hold constant values
    """

    id: str
    value: str

    def __str__(self) -> str:
        return f"{self.id} : '{self.value}'"


@dataclass(frozen=True)
class Method:
    """
    This item represent the method of every class
    """

    id: str
    function: FunctionNode

    def __str__(self) -> str:
        return f"method {self.id} : {self.function.id}"


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
        indent = "\t\t"
        params = "\n".join(indent + str(p) for p in self.params)
        locals = "\n".join(indent + str(l) for l in self.locals)
        ops = "\n".join(indent + str(o) for o in self.operations)

        return f"\tfunc {self.id}:\n {params}\n {locals} \n {ops} \n {indent}return {self.ret}"


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
        return f"{self.id} = {str(self.operation)}"


class SetAttrOpNode(OperationNode):
    def __init__(
        self, instance_id: str, attr_id: str, new_value: AtomOpNode, instance_type: str
    ) -> None:
        self.instance_type = instance_type
        self.new_value = new_value
        self.attr = attr_id
        self.instance = instance_id

    def __str__(self) -> str:
        return f"set_attr {self.instance}({self.instance_type}) {self.attr} {self.new_value}"


class Abort(OperationNode):
    def __str__(self) -> str:
        return "abort"


class PrintStrNode(OperationNode):
    def __init__(self, idx: str) -> None:
        super().__init__()
        self.id = idx

    def __str__(self) -> str:
        return f"print_str {self.id}"


class PrintIntNode(PrintStrNode):
    def __str__(self) -> str:
        return f"print_int {self.id}"


class ReturnOpNode(OperationNode):
    def __init__(
        self,
    ) -> None:
        super().__init__()


class ReadStrNode(ReturnOpNode):
    """
    This nodes reads a string from the standard input
    """

    def __str__(self) -> str:
        return "read_str"


class ReadIntNode(ReturnOpNode):
    """
    This nodes reads an int from the standard input
    """

    def __str__(self) -> str:
        return "read_int"


class GetAttrOpNode(ReturnOpNode):
    def __init__(self, instance_type_id: str, instance_id: str, attr_id: str) -> None:
        super().__init__()
        self.instance_type = instance_type_id
        self.instance = instance_id
        self.attr = attr_id

    def __str__(self) -> str:
        return f"get_attr {self.instance}({self.instance_type}) {self.attr}"


class CallOpNode(ReturnOpNode):
    def __init__(self, idx: str, type_idx: str, args: List[IdNode]) -> None:
        super().__init__()
        self.id = idx
        self.type = type_idx
        self.args = args

    def __str__(self) -> str:
        args = ", ".join(f"{a.value}" for a in self.args)
        return f"call {self.id} : {self.type} (args: {args})"


class VCallOpNode(CallOpNode):
    def __init__(self, idx: str, type_idx: str, args: List[IdNode]) -> None:
        super().__init__(idx, type_idx, args)

    def __str__(self) -> str:
        return "v" + super().__str__()


class VoidNode(ReturnOpNode):
    """Operation that indicate that the Storage Node is not initialized"""

    def __str__(self) -> str:
        return "<Uninitalized>"


class NewOpNode(ReturnOpNode):
    def __init__(self, type_idx: str) -> None:
        super().__init__()
        self.type: str = type_idx

    def __str__(self) -> str:
        return f"new {self.type}"


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

    def __str__(self) -> str:
        return f"{self.left.value} op {self.right.value}"


class ArithmeticOpNode(BinaryOpNode):
    pass


class SumOpNode(ArithmeticOpNode):
    pass


class MinusOpNode(ArithmeticOpNode):
    pass


class MultOpNode(ArithmeticOpNode):
    pass


class DivOpNode(ArithmeticOpNode):
    pass


class ComparisonOpNode(BinaryOpNode):
    pass


class EqualIntNode(ComparisonOpNode):
    pass


class EqualStrNode(ComparisonOpNode):
    pass


class LessOrEqualOpNode(ComparisonOpNode):
    pass


class LessOpNode(ComparisonOpNode):
    pass


class UnaryOpNode(ReturnOpNode):
    def __init__(self, atom: AtomOpNode) -> None:
        super().__init__()
        self.atom = atom


class GetTypeOpNode(UnaryOpNode):
    """Extracts the type of a node"""

    def __str__(self) -> str:
        return f"typeof {self.atom.value}"


class NotOpNode(UnaryOpNode):
    def __str__(self) -> str:
        return f"not {self.atom.value}"


class NegOpNode(UnaryOpNode):
    def __str__(self) -> str:
        return f"neg {self.atom.value}"


class ChainOpNode(ReturnOpNode):
    def __init__(self, target: str) -> None:
        super().__init__()
        self.target = target


class LoadOpNode(ChainOpNode):
    def __str__(self) -> str:
        return f"load {self.target}"


class LengthOpNode(ChainOpNode):
    def __str__(self) -> str:
        return f"length {self.target}"


class StrOpNode(ChainOpNode):
    def __str__(self) -> str:
        return f"str {self.target}"


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

    def __init__(self) -> None:
        super().__init__()


class CurrentTypeNameNode(ReturnOpNode):
    def __init__(self, target: str) -> None:
        super().__init__()
        self.target = target


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
