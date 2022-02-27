from __future__ import annotations
from typing import Dict, List, Tuple, Union

from asts.parser_ast import BinaryNode


class Node:
    def __init__(self, node) -> None:
        # if node is not None:
        #     self.line: int = node.line
        #     self.col: int = node.col
        pass

    def get_position(self) -> Tuple[int, int]:
        return (self.line, self.col)


class MIPSProgram(Node):
    """
    This node represents the entire MIPS program ( .text and .data sections )
    """

    def __init__(self, node, text_section: List[InstructionNode], data_section) -> None:
        super().__init__(node)
        self.text_section = text_section
        self.data_section = data_section


class TextNode(Node):
    """
    This node represents the `.text` section in MIPS
    """

    def __init__(self, node, instructions: List[InstructionNode]) -> None:
        super().__init__(node)
        if instructions is None:
            self.instructions = []
        self.instructions = instructions


class DataNode(Node):
    """
    This node represents the `.data` section in MIPS
    """

    def __init__(
        self, node, data: List[Tuple[LabelDeclaration, AssemblerDirective]]
    ) -> None:
        super().__init__(node)
        if data is None:
            self.data = []
        self.data = data


class Constant(Node):
    """
    This class represents a literal integer in MIPS
    """

    def __init__(self, node, value: Union[str, int]) -> None:
        super().__init__(node)
        self.value = value


class RegisterNode(Node):
    """
    This class represents a 4-bytes MIPS' register
    """

    def __init__(self, node, number) -> None:
        super().__init__(node)
        self.number = number


class Label(Node):
    """
    This class represents a label declaration in MIPS
    """

    def __init__(self, node, idx) -> None:
        super().__init__(node)
        self.idx = idx


class InstructionNode(Node):
    def __init__(self, node) -> None:
        super().__init__(node)


class LabelDeclaration(InstructionNode):
    """
    This class represents a label declaration in MIPS
    """

    def __init__(self, node, idx) -> None:
        super().__init__(node)
        self.idx = idx


class MemoryIndexNode(Node):
    """
    This node represents a memory-indexation of the form `<address>(<index>)`
    """

    def __init__(self, node, address, index) -> None:
        super().__init__(node)
        self.address = address
        self.index = index


class BinaryOpNode(InstructionNode):
    def __init__(self, node, left, right) -> None:
        super().__init__(node)
        self.left = left
        self.right = right


class TernaryOpNode(InstructionNode):
    def __init__(self, node, left, middle, right) -> None:
        super().__init__(node)
        self.left = left
        self.middle = middle
        self.right = right


class MoveFromLo(InstructionNode):
    """
    This node represents `mflo` instruction in MIPS
    """

    def __init__(self, node, register) -> None:
        super().__init__(node)
        self.register = register


class Div(BinaryOpNode):
    """
    This node represents `div` instruction in MIPS
    """

    def __init__(self, node, left, right) -> None:
        super().__init__(node, left, right)


class Xori(TernaryOpNode):
    """
    This node represents `xori` instruction in MIPS
    """

    def __init__(self, node, left, middle, right) -> None:
        super().__init__(node, left, middle, right)


class Not(BinaryOpNode):
    """
    This node represents `not` instruction in MIPS
    """

    def __init__(self, node, left, right) -> None:
        super().__init__(node, left, right)


class Equal(TernaryOpNode):
    """
    This node represents `seq` instruction in MIPS
    """

    def __init__(self, node, left, middle, right) -> None:
        super().__init__(node, left, middle, right)


class LessOrEqual(TernaryOpNode):
    """
    This node represents `sle` instruction in MIPS
    """

    def __init__(self, node, left, middle, right) -> None:
        super().__init__(node, left, middle, right)


class Less(TernaryOpNode):
    """
    This node represents `slt` instruction in MIPS
    """

    def __init__(self, node, left, middle, right) -> None:
        super().__init__(node, left, middle, right)


class Multiply(TernaryOpNode):
    """
    This node represents `mul` instruction in MIPS
    """

    def __init__(self, node, left, middle, right) -> None:
        super().__init__(node, left, middle, right)


class Subu(TernaryOpNode):
    """
    This node represents `subu` instruction in MIPS
    """

    def __init__(self, node, left, middle, right) -> None:
        super().__init__(node, left, middle, right)


class Sub(TernaryOpNode):
    """
    This node represents `sub` instruction in MIPS
    """

    def __init__(self, node, left, middle, right) -> None:
        super().__init__(node, left, middle, right)


class Addi(TernaryOpNode):
    """
    This node represents `addi` instruction in MIPS
    """

    def __init__(self, node, left, middle, right) -> None:
        super().__init__(node, left, middle, right)


class Addu(TernaryOpNode):
    """
    This node represents `addu` instruction in MIPS
    """

    def __init__(self, node, left, middle, right) -> None:
        super().__init__(node, left, middle, right)


class Add(TernaryOpNode):
    """
    This node represents `addu` instruction in MIPS
    """

    def __init__(self, node, left, middle, right) -> None:
        super().__init__(node, left, middle, right)


class Move(BinaryOpNode):
    """
    This node represents `move` instruction in MIPS
    """

    def __init__(self, node, left, right) -> None:
        super().__init__(node, left, right)


class LoadImmediate(BinaryOpNode):
    """
    This node represents `li` instruction in MIPS
    """

    def __init__(self, node, left, right) -> None:
        super().__init__(node, left, right)


class LoadByte(BinaryOpNode):
    """
    This node represents `lb` instruction in MIPS
    """

    def __init__(self, node, left, right) -> None:
        super().__init__(node, left, right)


class LoadWord(BinaryOpNode):
    """
    This node represents `lw` instruction in MIPS
    """

    def __init__(self, node, left, right) -> None:
        super().__init__(node, left, right)


class LoadAddress(BinaryOpNode):
    """
    This node represents `la` instruction in MIPS
    """

    def __init__(self, node, left, right) -> None:
        super().__init__(node, left, right)


class StoreWord(BinaryOpNode):
    """
    This node represents `sw` instruction in MIPS
    """

    def __init__(self, node, left, right) -> None:
        super().__init__(node, left, right)


class Jump(InstructionNode):
    """
    This node represents `j` instruction in MIPS
    """

    def __init__(self, node, address) -> None:
        super().__init__(node)
        self.address = address


class JumpRegister(InstructionNode):
    """
    This node represents `jr` instruction in MIPS
    """

    def __init__(self, node, register) -> None:
        super().__init__(node)
        self.register = register


class JumpAndLink(InstructionNode):
    """
    This node represents `jal` instruction in MIPS
    """

    def __init__(self, node, address) -> None:
        super().__init__(node)
        self.address = address


class BranchOnEqual(TernaryOpNode):
    """
    This node represents `beq` instruction in MIPS
    """

    def __init__(self, node, left, middle, right) -> None:
        super().__init__(node, left, middle, right)


class BranchOnNotEqual(TernaryOpNode):
    """
    This node represents `bne` instruction in MIPS
    """

    def __init__(self, node, left, middle, right) -> None:
        super().__init__(node, left, middle, right)


class AssemblerDirective(Node):
    def __init__(self, node, list) -> None:
        super().__init__(node)
        if list is None:
            list = []
        self.list = list


class WordDirective(AssemblerDirective):
    """
    This node represents `.word` assembler directive
    """

    def __init__(self, node, list) -> None:
        super().__init__(node, list)


class AsciizDirective(AssemblerDirective):
    """
    This node represents `.asciiz` assembler directive
    """

    def __init__(self, node, list) -> None:
        super().__init__(node, list)


class Syscall(InstructionNode):
    """
    This node represents `syscall` instruction in MIPS
    """

    def __init__(self, node) -> None:
        super().__init__(node)
