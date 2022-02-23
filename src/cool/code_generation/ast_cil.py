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
    def __init__(self, name: str):
        self.name: str = name


class InstructionNode(Node):
    pass


class AssignNode(InstructionNode):
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
    pass


class XorNode(ArithmeticNode):
    pass


class GetAttribNode(InstructionNode):
    def __init__(self, dest: str, instance: str, attr: str) -> None:
        self.dest: str = dest
        self.instance: str = instance
        self.attr: str = attr


class SetAttribNode(InstructionNode):
    def __init__(self, instance: str, attr: str, source: str) -> None:
        self.instance: str = instance
        self.attr: str = attr
        self.source: str = source


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


class AllocateNode(InstructionNode):
    def __init__(self, itype: str, dest: str):
        self.type: str = itype
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
        self.obj: str = obj
        self.dest: str = dest


class AncestorNode(InstructionNode):
    def __init__(self, dest: str, obj: str):
        self.obj: str = obj
        self.dest: str = dest


class TypeDirectionNode(InstructionNode):
    def __init__(self, dest: str, name: str):
        self.name: str = name
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
    def __init__(self, function, dest):
        self.function = function
        self.dest = dest


class DynamicCallNode(InstructionNode):
    def __init__(self, xtype: str, method: str, dest: str):
        self.type = xtype
        self.method = method
        self.dest = dest


class ArgNode(InstructionNode):
    def __init__(self, name: str):
        self.name: str = name


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

class ToStrNode(InstructionNode):
    def __init__(self, dest, ivalue):
        self.dest = dest
        self.ivalue = ivalue


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
        self.value = value


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
