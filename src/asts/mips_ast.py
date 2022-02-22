from __future__ import annotations
from typing import Dict, List, Tuple


class Node:
    def __init__(self, node) -> None:
        if node is not None:
            self.line: int = node.line
            self.col: int = node.col

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


class Move(BinaryOpNode):
    """
    This node represents `move` instruction in MIPS
    """

    def __init__(self, node, left, right) -> None:
        super().__init__(node, left, right)


class LoadWord(BinaryOpNode):
    """
    This node represents `lw` instruction in MIPS
    """

    def __init__(self, node, left, right) -> None:
        super().__init__(node, left, right)


class StoreWord(BinaryOpNode):
    """
    This node represents `sw` instruction in MIPS
    """

    def __init__(self, node, left, right) -> None:
        super().__init__(node, left, right)


class Jump(Node):
    """
    This node represents `j` instruction in MIPS
    """

    def __init__(self, node, address) -> None:
        super().__init__(node)
        self.address = address


class JumpRegister(Node):
    """
    This node represents `jr` instruction in MIPS
    """

    def __init__(self, node, register) -> None:
        super().__init__(node)
        self.register = register


class JumpAndLink(Node):
    """
    This node represents `jal` instruction in MIPS
    """

    def __init__(self, node, address) -> None:
        super().__init__(node)
        self.address = address


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


