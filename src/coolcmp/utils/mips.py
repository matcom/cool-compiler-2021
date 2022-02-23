from __future__ import annotations
from typing import List, Union

from coolcmp.utils.registers import Register


class Node:
    pass


class ProgramNode(Node):
    def __init__(
        self,
        data: List[Node],
        types: List[Type],
        functions: List[FunctionNode],
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
        super().__init__(label)

        self.value = value


class SWNode(InstructionNode):
    """
    store word | sw $1, 100($2) | Memory[$2 + 100] = $1
    Copy from register to memory.
    """
    def __init__(self, dest: int, offset: int, src: Register):
        self.dest = dest
        self.offset = offset
        self.src = src


class LWNode(InstructionNode):
    """
    load word | lw $1, 100($2) | $1 = Memory[$2 + 100]
    Copy from memory to register.
    """
    def __init__(self, dest: Register, offset: int, src: int):
        self.dest = dest
        self.offset = offset
        self.src = src


class LINode(InstructionNode):
    """
    load immediate | li $1, 100 | $1 = 100
    Loads immediate value into register.
    """
    def __init__(self, reg: Register, value: int):
        self.reg = reg
        self.value = value


class JALNode(InstructionNode):
    """
    jump and link | jal 1000 | $ra = PC + 4; go to address 1000
    Use when making procedure call.
    This saves the return address in $ra.
    """
    def __init__(self, dest: int):
        self.dest = dest


class LANode(InstructionNode):
    """
    load address | la $1, label | $1 = Address of label
    Loads computed address of label (not its contents) into register.
    """
    def __init__(self, reg: Register, label: str):
        self.reg = reg
        self.label = label


class ADDNode(InstructionNode):
    """
    add | add $1, $2, $3 | $1 = $2 + $3
    """
    def __init__(self, dest: Register, src1: Register | int, src2: Register | int):
        self.dest = dest
        self.src1 = src1
        self.src2 = src2


class ADDINode(InstructionNode):
    """
    add immediate | addi $1, $2, 100 | $1 = $2 + 100
    "Immediate" means a constant number.
    """
    def __init__(self, dest: Register, src: Register | int, isrc: Register | int):
        self.dest = dest
        self.src = src
        self.isrc = isrc


class JRNode(InstructionNode):
    """
    jump register | jr $1 | go to address stored in $1
    For switch, procedure return.
    """
    def __init__(self, dest: Register):
        self.dest = dest


class SysCallNode(InstructionNode):
    pass


class PrintIntNode(SysCallNode):
    """
    print_int | $a0 = integer to be printed | code in v0 = 1
    Print integer number (32 bit).
    """
    pass


class PrintStringNode(SysCallNode):
    """
    print_string | $a0 = address of string in memory | code in v0 = 4
    Print null-terminated character string.
    """
    pass


class Type:
    def __init__(self, label, address, attrs, methods, index, default=None):
        self.label = label
        self.address = address
        self.attrs = attrs
        self.default_attrs = dict(default) if default is not None else {}
        self.methods = methods
        self.index = index

    def length(self):
        return len(self.attrs)

    def __str__(self):
        return f"{self.label}-{self.address}-{self.attrs}-{self.default_attrs}-{self.methods}-{self.index}"
