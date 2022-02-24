from __future__ import annotations
from typing import List, Tuple, Union

from coolcmp.utils.registers import FP, Register, SP, DW, ARG, V0


PROTOTYPES = "__prototypes_labels__"


class Node:
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

    def local_address(self, name: str):
        index = self.local_vars.index(name)
        locals_amount = len(self.local_vars)
        offset = (locals_amount + 2 - index) * DW
        return -offset

    def param_address(self, name: str):
        index = self.params.index(name)
        params_amount = len(self.params)
        offset = (params_amount + 2 - index) * DW
        return offset

    def variable_address(self, name: str):
        try:
            return self.param_address(name)
        except ValueError:
            return self.local_address(name)


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

    def __init__(self, dest: Register, offset: int, src: Register):
        self.dest = dest
        self.offset = offset
        self.src = src


class LWNode(InstructionNode):
    """
    load word | lw $1, 100($2) | $1 = Memory[$2 + 100]
    Copy from memory to register.
    """

    def __init__(self, dest: Register, offset: int, src: Register):
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

    def __init__(self, dest: str):
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


class SLLNode(InstructionNode):
    """
    shift left logical by a constant number of bits
    sll $1, $2, 10 -> $1 = $2<<10
    """

    def __init__(self, dest: Register, src: Register, bits: int):
        self.dest = dest
        self.src = src
        self.bits = bits


class MoveNode(InstructionNode):
    """
    copy from register to register
    move $1,$2 -> $1=$2
    """

    def __init__(self, reg1: Register, reg2: Register):
        self.reg1 = reg1
        self.reg2 = reg2


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
    lw <reg_name>, 0($sp)
    addi $sp, $sp, 4
    """
    lw = LWNode(reg_name, 0, SP)
    addi = ADDINode(SP, SP, DW)

    return [lw, addi]


def create_object_instructions(r1: Register, r2: Register):
    return [
        SLLNode(r1, r1, 2),
        LANode(r2, PROTOTYPES),
        ADDNode(r2, r2, r1),
        LWNode(r2, 0, r2),
        LWNode(ARG[0], 4, r2),
        SLLNode(ARG[0], ARG[0], 2),
        JALNode("malloc"),
        MoveNode(ARG[2], ARG[0]),
        MoveNode(ARG[0], r2),
        MoveNode(ARG[1], V0),
        JALNode("copy"),
    ]
