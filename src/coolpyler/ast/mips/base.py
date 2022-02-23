class MipsAstNode:
    pass


class ProgramNode(MipsAstNode):
    def __init__(self, node, text_section, data_section):
        super().__init__(node)
        self.text_section = text_section
        self.data_section = data_section


class TextNode(MipsAstNode):
    def __init__(self, node, instructions):
        super().__init__(node)
        if instructions is None:
            self.instructions = []
        self.instructions = instructions


class DataNode(MipsAstNode):
    def __init__(self, node, data):
        super().__init__(node)
        if data is None:
            self.data = []
        self.data = data


class RegisterNode(MipsAstNode):
    def __init__(self, node, number):
        super().__init__(node)
        self.number = number


class LabelNode(MipsAstNode):
    def __init__(self, node, idx):
        super().__init__(node)
        self.idx = idx


class InstructionNode(MipsAstNode):
    def __init__(self, node):
        super().__init__(node)


class LabelDeclarationNode(InstructionNode):
    def __init__(self, node, idx):
        super().__init__(node)
        self.idx = idx


class MemoryIndexNode(MipsAstNode):
    def __init__(self, node, address, index):
        super().__init__(node)
        self.address = address
        self.index = index


class BinaryOpNode(InstructionNode):
    def __init__(self, node, left, right):
        super().__init__(node)
        self.left = left
        self.right = right


class TernaryOpNode(InstructionNode):
    def __init__(self, node, left, middle, right):
        super().__init__(node)
        self.left = left
        self.middle = middle
        self.right = right


class MoveNode(BinaryOpNode):
    def __init__(self, node, left, right):
        super().__init__(node, left, right)


class LoadWordNode(BinaryOpNode):
    def __init__(self, node, left, right):
        super().__init__(node, left, right)


class StoreWordNode(BinaryOpNode):
    def __init__(self, node, left, right):
        super().__init__(node, left, right)


class JumpNode(MipsAstNode):
    def __init__(self, node, address):
        super().__init__(node)
        self.address = address


class JumpRegisterNode(MipsAstNode):
    def __init__(self, node, register):
        super().__init__(node)
        self.register = register


class JumpAndLinkNode(MipsAstNode):
    def __init__(self, node, address):
        super().__init__(node)
        self.address = address


class AssemblerDirectiveNode(MipsAstNode):
    def __init__(self, node, list):
        super().__init__(node)
        if list is None:
            list = []
        self.list = list


class WordDirectiveNode(AssemblerDirectiveNode):
    def __init__(self, node, list):
        super().__init__(node, list)
