DW = 4
from coolcmp.utils import mips
from typing import List


class Register:
    def __init__(self, name: str):
        self.name = name

    def __str__(self):
        return f"reg_{self.name}"


T = [Register(f"t{i}") for i in range(9)]
ARG = [Register(f"a{i}") for i in range(4)]
ZERO = Register("zero")
LOW = Register("low")
V0 = Register("v0")
V1 = Register("v1")
A0 = Register("a0")
FP = Register("fp")
SP = Register("sp")
RA = Register("ra")


class RegisterLocation:
    def __init__(self, name, offset):
        self.name = name
        self.offset = offset


def push_register_instructions(reg_name: str) -> List[mips.InstructionNode]:
    """
    addi $sp, $sp, -4
    sw <reg_name>, 0($sp)
    """
    addi = mips.ADDINode(SP, SP, -DW)
    sw = mips.SWNode(reg_name, 0, SP)

    return [addi, sw]


def pop_register_instructions(reg_name: str) -> List[mips.InstructionNode]:
    """
    lw <reg_name>, $sp, 0
    addi $sp, $sp, 4
    """
    lw = mips.LWNode(reg_name, 0, SP)
    addi = mips.ADDINode(SP, SP, DW)

    return [lw, addi]
