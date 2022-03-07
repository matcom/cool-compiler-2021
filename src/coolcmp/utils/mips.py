from __future__ import annotations
from typing import List, Union

from coolcmp.utils.registers import Register, sp, dw
from coolcmp.utils import cil

TYPES_LABELS = "__types_definition__"

Memory = Union[str, int]


class Node:
    pass


class Type:
    def __init__(self,
                 label: str,
                 attrs: list[str],
                 methods: dict[cil.MethodAt, str],
                 total_methods: int,
                 index: int):
        self.label = label
        self.attrs = attrs
        self.methods = methods
        self.total_methods = total_methods
        self.index = index

    def get_attr_index(self, name: str) -> int:
        return self.attrs.index(name) + 1

    @property
    def name_offset(self) -> int:
        return (self.total_methods + 1) * 4

    def length(self) -> int:
        return len(self.attrs)

    def __str__(self):
        return f"{self.label}-{self.attrs}-{self.methods}-{self.index}"


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
        offset = (locals_amount + 2 - index) * dw
        return -offset

    def param_address(self, name: str):
        index = self.params.index(name)
        offset = index * dw
        return offset

    def variable_address(self, name: str):
        try:
            return self.param_address(name)
        except ValueError:
            return self.local_address(name)


class InstructionNode(Node):
    def __init__(self):
        self._comment: str = ''

    def with_comm(self, comment: str) -> InstructionNode:
        self._comment = comment
        return self

    @property
    def comment(self):
        return f"\t\t\t# {self._comment}" if self._comment else ""

    @comment.setter
    def comment(self, comment: str):
        self._comment = comment


class CommentNode(InstructionNode):
    def __init__(self, text: str):
        super().__init__()
        self.text = text

    def __str__(self):
        return f"# {self.text}"


class DataNode(Node):
    def __init__(self, label: str):
        self.label = label

    def __str__(self):
        return f"{self.label}:"


class StringNode(DataNode):
    def __init__(self, label: str, value: str):
        super().__init__(label)
        self.value = value

    def __str__(self):
        return f"{self.label}: .asciiz {self.value}"


class LabelNode(InstructionNode):
    def __init__(self, label: str):
        super().__init__()
        self.label = label

    def __str__(self):
        return f"{self.label}:"


class SWNode(InstructionNode):
    """
    store word | sw $1, 100($2) | Memory[$2 + 100] = $1
    Copy from register to memory.
    """
    def __init__(self, dest: Register, offset: int, src: Memory):
        super().__init__()
        self.dest = dest
        self.offset = offset
        self.src = src

    def __str__(self):
        return f"sw     {self.dest}, {self.offset}({self.src})"


class LWNode(InstructionNode):
    """
    load word | lw $1, 100($2) | $1 = Memory[$2 + 100]
    Copy from memory to register.
    """
    def __init__(self, dest: Register, src: tuple[int, Memory] | str):
        super().__init__()
        self.dest = dest
        self.src = src

    def __str__(self):
        if isinstance(self.src, tuple):
            return f"lw     {self.dest}, {self.src[0]}({self.src[1]})"
        else:
            return f"lw     {self.dest}, {self.src}"


class LINode(InstructionNode):
    """
    load immediate | li $1, 100 | $1 = 100
    Loads immediate value into register.
    """
    def __init__(self, reg: Register, value: int):
        super().__init__()
        self.reg = reg
        self.value = value

    def __str__(self):
        return f"li     {self.reg}, {self.value}"


class JALNode(InstructionNode):
    """
    jump and link | jal 1000 | $ra = PC + 4; go to address 1000
    Use when making procedure call.
    This saves the return address in $ra.
    """
    def __init__(self, dest: str):
        super().__init__()
        self.dest = dest

    def __str__(self):
        return f"jal    {self.dest}"


class JALRNode(InstructionNode):
    """
    jump and link to register value
    """
    def __init__(self, reg: Register):
        super().__init__()
        self.reg = reg
    
    def __str__(self):
        return f"jalr    {self.reg}"


class LANode(InstructionNode):
    """
    load address | la $1, label | $1 = Address of label
    Loads computed address of label (not its contents) into register.
    """
    def __init__(self, reg: Register, label: str):
        super().__init__()
        self.reg = reg
        self.label = label

    def __str__(self):
        return f"la     {self.reg}, {self.label}"


class ADDNode(InstructionNode):
    """
    add | add $1, $2, $3 | $1 = $2 + $3
    """
    def __init__(self, dest: Register, src1: Register | int, src2: Register | int):
        super().__init__()
        self.dest = dest
        self.src1 = src1
        self.src2 = src2

    def __str__(self):
        return f"add    {self.dest}, {self.src1}, {self.src2}"


class ADDINode(InstructionNode):
    """
    add immediate | addi $1, $2, 100 | $1 = $2 + 100
    "Immediate" means a constant number.
    """
    def __init__(self, dest: Register, src: Register | int, isrc: Register | int):
        super().__init__()
        self.dest = dest
        self.src = src
        self.isrc = isrc

    def __str__(self):
        return f"addi   {self.dest}, {self.src}, {self.isrc}"


class ADDUNode(InstructionNode):
    """
    add unsigned | addu $1, $2, $3 | $1 = $2 + $3
    Values are treated as unsigned integers, not two's complement integers.
    """
    def __init__(self, rdest: Register, r1: Register, r2: Register | int):
        super().__init__()
        self.rdest = rdest
        self.r1 = r1
        self.r2 = r2

    def __str__(self):
        return f"addu   {self.rdest}, {self.r1}, {self.r2}"


class SUBNode(InstructionNode):
    """
    subtract | sub $1, $2, $3 | $1 = $2 - $3
    """
    def __init__(self, rdest: Register, r1: Register, r2: Register | int):
        super().__init__()
        self.rdest = rdest
        self.r1 = r1
        self.r2 = r2

    def __str__(self):
        return f"sub    {self.rdest}, {self.r1}, {self.r2}"


class SUBUNode(InstructionNode):
    """
    subtract unsigned | subu $1, $2, $3 | $1 = $2 - $3
    Values are treated as unsigned integers, not two's complement integers.
    """
    def __init__(self, rdest: Register, r1: Register, r2: Register | int):
        super().__init__()
        self.rdest = rdest
        self.r1 = r1
        self.r2 = r2

    def __str__(self):
        return f"subu   {self.rdest}, {self.r1}, {self.r2}"


class JRNode(InstructionNode):
    """
    jump register | jr $1 | go to address stored in $1
    For switch, procedure return.
    """
    def __init__(self, dest: Register):
        super().__init__()
        self.dest = dest

    def __str__(self):
        return f"jr     {str(self.dest)}"


class BEQNode(InstructionNode):
    """
    branch on equal | beq $1, $2, 100 | if($1 == $2) go to PC + 4 + 100
    Test if registers are equal.
    """
    def __init__(self, reg1: Register, reg2: Register, label: str):
        super().__init__()
        self.reg1 = reg1
        self.reg2 = reg2
        self.label = label

    def __str__(self):
        return f"beq    {self.reg1}, {self.reg2}, {self.label}"


class JNode(InstructionNode):
    """
    jump | j 1000 | go to address 1000
    Jump to target address
    """
    def __init__(self, label: str):
        super().__init__()
        self.label = label

    def __str__(self):
        return f"j      {self.label}"


class SLLNode(InstructionNode):
    """
    shift left logical by a constant number of bits
    sll $1, $2, 10 -> $1 = $2<<10
    """
    def __init__(self, dest: Register, src: Register, bits: int):
        super().__init__()
        self.dest = dest
        self.src = src
        self.bits = bits

    def __str__(self):
        return f"sll    {self.dest}, {self.src}, {self.bits}"


class MoveNode(InstructionNode):
    """
    copy from register to register
    move $1,$2 -> $1=$2
    """

    def __init__(self, reg1: Register, reg2: Register):
        super().__init__()
        self.reg1 = reg1
        self.reg2 = reg2

    def __str__(self):
        return f"move   {self.reg1}, {self.reg2}"


class SysCallNode(InstructionNode):
    def __init__(self):
        super().__init__()

    def __str__(self):
        return "syscall"


class PrintIntNode(SysCallNode):
    """
    print_int | $a0 = integer to be printed | code in v0 = 1
    Print integer number (32 bit).
    """
    def __init__(self):
        super().__init__()


class PrintStringNode(SysCallNode):
    """
    print_string | $a0 = address of string in memory | code in v0 = 4
    Print null-terminated character string.
    """
    def __init__(self):
        super().__init__()


def push_register_instructions(reg_name: str) -> List[InstructionNode]:
    """
    addi $sp, $sp, -4
    sw <reg_name>, 0($sp)
    """
    addi = ADDINode(sp, sp, -dw)
    sw = SWNode(reg_name, 0, sp)

    return [addi, sw]


def pop_register_instructions(reg_name: str) -> List[InstructionNode]:
    """
    lw <reg_name>, 0($sp)
    addi $sp, $sp, 4
    """
    lw = LWNode(reg_name, (0, sp))
    addi = ADDINode(sp, sp, dw)

    return [lw, addi]


# def create_object_instructions(r1: Register, r2: Register):
#     return [
#         SLLNode(r1, r1, 2),
#         LANode(r2, TYPES_LABELS),
#         ADDNode(r2, r2, r1),
#         LWNode(r2, (0, r2)),
#         LWNode(ARG[0], (4, r2)),
#         SLLNode(ARG[0], ARG[0], 2),
#         JALNode("malloc"),
#         MoveNode(ARG[2], ARG[0]),
#         MoveNode(ARG[0], r2),
#         MoveNode(ARG[1], V0),
#         JALNode("copy"),
#     ]
