from __future__ import annotations
from typing import Dict, List

from coolcmp.utils.registers import Register, SP, DW


class Node:
    pass


class ProgramNode(Node):
    def __init__(
        self,
        data: Dict[str, Node],
        types: Dict[str, Type],
        functions: Dict[str, FunctionNode],
    ):
        self.data = data
        self.types = types
        self.functions = functions


class FunctionNode(Node):
    def __init__(self, name: str, params: List[str], local_vars: List[str]):
        self.name = name
        self.params = params
        self.local_vars = local_vars
        self.instructions = []


class InstructionNode(Node):
    pass


class DataNode(Node):
    def __init__(self, label: str):
        self.label = label


class StringNode(DataNode):
    def __init__(self, label: str, value: str):
        self.label = label
        self.value = value


class SWNode(Node):
    def __init__(self, dest: Register, offset: int, src: Register):
        self.dest = dest
        self.offset = offset
        self.src = src


class LWNode(Node):
    def __init__(self, dest: Register, offset: int, src: Register):
        self.dest = dest
        self.offset = offset
        self.src = src


class LINode(Node):
    def __init__(self, reg: Register, value: int):
        self.reg = reg
        self.value = value


class JALNode(Node):
    def __init__(self, dest: str):
        self.dest = dest


class LANode(Node):
    def __init__(self, reg: Register, value: int):
        self.reg = reg
        self.value = value


class ADDNode(Node):
    def __init__(
        self,
        dest: Register,
        src1: Register,
        src2: Register,
    ):
        self.dest = dest
        self.src1 = src1
        self.src2 = src2


class ADDINode(Node):
    def __init__(self, dest: Register, src: Register, isrc: Register):
        self.dest = dest
        self.src = src
        self.isrc = isrc


class JRNode(Node):
    pass


class SysCallNode(Node):
    pass


class Type:
    def __init__(self, label, address, attrs, methods, index, default=[]):
        self.label = label
        self.address = address
        self.attrs = attrs
        self.default_attrs = dict(default)
        self.methods = methods
        self.index = index

    def length(self):
        return len(self.attrs)

    def __str__(self):
        return f"{self.label}-{self.address}-{self.attrs}-{self.default_attrs}-{self.methods}-{self.index}"


def push_register_instructions(reg_name: str) -> List[InstructionNode]:
    """
    addi $sp, $sp, -4
    sw <reg_name>, 0($sp)
    """
    addi = ADDINode(SP, SP, -DW)
    sw = SWNode(reg_name, 0, SP)

    return [addi, sw]


def pop_register_instructions(reg_name: str) -> List[InstructionNode]:
    """
    lw <reg_name>, $sp, 0
    addi $sp, $sp, 4
    """
    lw = LWNode(reg_name, 0, SP)
    addi = ADDINode(SP, SP, DW)

    return [lw, addi]
