from operator import le
from typing import Any, List, Optional, Tuple


class Node:
    comment: str = ""

    def set_comment(self, comment: str) -> "Node":
        self.comment = comment
        return self


class ProgramNode(Node):
    def __init__(
        self,
        dottypes: List["TypeNode"],
        dotdata: List["DataNode"],
        dotcode: List["FunctionNode"],
    ):
        self.dottypes: List[TypeNode] = dottypes
        self.dotdata: List[DataNode] = dotdata
        self.dotcode: List[FunctionNode] = dotcode


class TypeNode(Node):
    def __init__(self, name: str, parent: Optional[str] = None):
        self.name: str = name
        self.parent: str = parent or "null"
        self.attributes: List[str] = []
        self.methods: List[Tuple[str, str]] = []


class DataNode(Node):
    def __init__(self, name: str, value: Any):
        self.name: str = name
        self.value: Any = value


class FunctionNode(Node):
    def __init__(
        self,
        name: str,
        params: List["ParamNode"],
        local_vars: List["LoadNode"],
        instructions: List["InstructionNode"],
    ):
        self.name: str = name
        self.params: List[ParamNode] = params
        self.local_vars: List[LocalNode] = local_vars
        self.instructions: List[InstructionNode] = instructions


class ParamNode(Node):
    def __init__(self, name: str):
        self.name: str = name


class LocalNode(Node):
    def __init__(self, name: str, type: str = "Object"):
        self.name: str = name
        self.type: str = type


class InstructionNode(Node):
    pass


class AssignNode(InstructionNode):
    def __init__(self, dest: str, source: str):
        self.dest: str = dest
        self.source: str = source


class AssignIntNode(InstructionNode):
    def __init__(self, dest: str, source: str):
        self.dest: str = dest
        self.source: str = source


class ArithmeticNode(InstructionNode):
    def __init__(self, dest: str, left: str, right: str):
        self.dest: str = dest
        self.left: str = left
        self.right: str = right


class PlusNode(ArithmeticNode):
    pass


class MinusNode(ArithmeticNode):
    pass


class StarNode(ArithmeticNode):
    pass


class DivNode(ArithmeticNode):
    pass


class LessEqualNode(ArithmeticNode):
    pass


class LessThanNode(ArithmeticNode):
    pass


class EqualNode(ArithmeticNode):
    equality_type: str = "Object"
    pass


class XorNode(ArithmeticNode):
    pass


class GetAttributeNode(InstructionNode):
    def __init__(self, dest: str, instance: str, attr: str, attr_index: int) -> None:
        self.dest: str = dest
        self.instance: str = instance
        self.attr: str = attr
        self.attr_index: int = attr_index


class SetAttributeNode(InstructionNode):
    def __init__(self, instance: str, attr: str, source: str, attr_index: int) -> None:
        self.instance: str = instance
        self.attr: str = attr
        self.source: str = source
        self.attr_index: int = attr_index

class GetIndexNode(InstructionNode):
    def __init__(self, dest: str, instance: str, index: str) -> None:
        self.dest: str = dest
        self.instance: str = instance
        self.index: str = index


class SetIndexNode(InstructionNode):
    def __init__(self, instance: str, index: int, source: str) -> None:
        self.instance: str = instance
        self.index: int = index
        self.source: str = source


class GetValueInIndexNode(InstructionNode):
    def __init__(self, dest: str, instance: str, index: str) -> None:
        self.dest: str = dest
        self.instance: str = instance
        self.index: str = index


class SetValueInIndexNode(InstructionNode):
    def __init__(self, instance: str, index: int, source: str) -> None:
        self.instance: str = instance
        self.index: int = index
        self.source: str = source



class AllocateNode(InstructionNode):
    def __init__(self, itype: str, dest: str):
        self.type: str = itype
        self.dest: str = dest


class AllocateIntNode(InstructionNode):
    def __init__(self, dest: str, value: str):
        self.dest: str = dest
        self.value: str = value


class AllocateBoolNode(InstructionNode):
    def __init__(self, dest: str, value: str):
        self.dest: str = dest
        self.value: str = value


class AllocateNullPtrNode(InstructionNode):
    def __init__(self, dest: str):
        self.dest: str = dest


class ArrayNode(InstructionNode):
    def __init__(self, dest: str, size: int) -> None:
        self.dest: str = dest
        self.size: int = size


class TypeOfNode(InstructionNode):
    def __init__(
        self,
        dest: str,
        obj: str,
    ):
        self.source: str = obj
        self.dest: str = dest


class AncestorNode(InstructionNode):
    def __init__(self, dest: str, source: str):
        self.source: str = source
        self.dest: str = dest


class TypeAddressNode(InstructionNode):
    def __init__(self, dest: str, name: str):
        self.name: str = name
        self.dest: str = dest


class EqualAddressNode(InstructionNode):
    def __init__(self, dest: str, left: str, right: str):
        self.left: str = left
        self.right: str = right
        self.dest: str = dest


class EqualIntNode(InstructionNode):
    def __init__(self, dest: str, left: str, right: str):
        self.left: str = left
        self.right: str = right
        self.dest: str = dest


class EqualStrNode(InstructionNode):
    def __init__(self, dest: str, left: str, right: str):
        self.left: str = left
        self.right: str = right
        self.dest: str = dest

class LabelNode(InstructionNode):
    def __init__(self, label: str):
        self.label: str = label


class GotoNode(InstructionNode):
    def __init__(self, address: str):
        self.address: str = address


class GotoIfNode(InstructionNode):
    def __init__(self, condition: str, address: str):
        self.condition: str = condition
        self.address: str = address


class StaticCallNode(InstructionNode):
    def __init__(self, function: str, dest: str, total_args: int):
        self.function: str = function
        self.dest: str = dest
        self.total_args: str = total_args 


class DynamicCallNode(InstructionNode):
    def __init__(self, xtype: str, method: str, dest: str, total_args: int):
        self.type = xtype
        self.method = method
        self.dest = dest
        self.total_args = total_args


class ArgNode(InstructionNode):
    def __init__(self, name: str, arg_index: int, total_args: int):
        self.name: str = name
        self.arg_index: int = arg_index
        self.total_args: int = total_args


class ReturnNode(InstructionNode):
    def __init__(self, value: str = None):
        self.value: str = value


class LoadNode(InstructionNode):
    def __init__(self, dest, msg):
        self.dest = dest
        self.msg = msg


class LengthNode(InstructionNode):
    def __init__(self, dest: str, str_address: str) -> None:
        self.dest: str = dest
        self.str_address: str = str_address


class ConcatNode(InstructionNode):
    def __init__(self, dest: str, str1: str, str2: str):
        self.dest: str = dest
        self.str1: str = str1
        self.str2: str = str2


class PrefixNode(InstructionNode):
    pass


class SubstringNode(InstructionNode):
    def __init__(self, dest: str, str_address: str, start: int, length: int):
        self.dest: str = dest
        self.str_address: str = str_address
        self.start: int = start
        self.length: int = length

class AllocateStrNode(InstructionNode):
    def __init__(self, dest: str, value: str):
        self.dest: str = dest
        self.value: str = value

    @property
    def string(self):
        s = self.value.replace('\\n', '\n')
        s = s.replace('\\t', '\t')
        s = s.replace('\\b', '\b')
        s = s.replace('\\f', '\f')
        return s[1:-1]

    @property
    def length(self):
        x = self.value.count('\\n')
        x += self.value.count('\\t')
        x += self.value.count('\\b')
        x += self.value.count('\\f')
        return len(self.value)  - x -  2

class ReadStringNode(InstructionNode):
    def __init__(self, dest):
        self.dest = dest


class ReadIntNode(InstructionNode):
    def __init__(self, dest):
        self.dest = dest


class PrintStringNode(InstructionNode):
    def __init__(self, str_addr):
        self.str_addr = str_addr


class PrintIntNode(InstructionNode):
    def __init__(self, value):
        self.source = value


class CopyNode(InstructionNode):
    def __init__(self, dest: str, source: str) -> None:
        self.dest: str = dest
        self.source: str = source


class CommentNode(InstructionNode):
    def __init__(self, comment):
        self.comment = comment


class EmptyInstruction(InstructionNode):
    def __init__(self):
        pass


class TypeNameNode(InstructionNode):
    def __init__(self, dest, source):
        self.dest = dest
        self.source = source


class HaltNode(InstructionNode):
    def __init__(self):
        pass


class AssertTypeNode(InstructionNode):
    def __init__(self, address: str):
        self.address: str = address