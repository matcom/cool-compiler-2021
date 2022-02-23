class MipsAstNode:
    pass


class ProgramNode(MipsAstNode):
    def __init__(self, text_section, data_section):
        # super().__init__(node)
        self.text_section = text_section
        self.data_section = data_section


class TypeNode(MipsAstNode):
    def __init__(self, name, attributes, methods):
        self.name = name
        self.attributes = attributes
        self.methods = methods
        self.label = LabelNode(name)


class TextNode(MipsAstNode):
    def __init__(self, instructions):
        # super().__init__(node)

        self.instructions = instructions


class DataSectionNode(MipsAstNode):
    def __init__(self, data):
        # super().__init__(node)
        self.data = data


class DataNode(MipsAstNode):
    def __init__(self, label, storage_type, data):
        # super().__init__(node)
        self.label = label
        self.storage_type = storage_type
        self.data = data


class RegisterNode(MipsAstNode):
    def __init__(self, number):
        # super().__init__(node)
        self.number = number


class LabelNode(MipsAstNode):
    def __init__(self, idx):
        # super().__init__(node)
        self.idx = idx


class InstructionNode(MipsAstNode):
    def __init__(self):
        # super().__init__(node)
        pass


class SyscallNode(InstructionNode):
    def __init__(self):
        # super().__init__(node)
        pass


class BinaryOpNode(InstructionNode):
    def __init__(self, left, right):
        # super().__init__(node)
        self.left = left
        self.right = right


class LoadAddressNode(BinaryOpNode):
    def __init__(self, register, label):
        super().__init__(register, label)


class LoadWordNode(BinaryOpNode):
    def __init__(self, register, ram_dir):
        super().__init__(register, ram_dir)


class StoreWordNode(BinaryOpNode):
    def __init__(self, register, ram_dir):
        super().__init__(register, ram_dir)


class LoadInmediateNode(BinaryOpNode):
    def __init__(self, register, value):
        super().__init__(register, value)


class MultNode(BinaryOpNode):
    def __init__(self, left, right):
        super().__init__(left, right)


class DivNode(BinaryOpNode):
    def __init__(self, left, right):
        super().__init__(left, right)


class MoveNode(BinaryOpNode):
    def __init__(self, left, right):
        super().__init__(left, right)


class StoreWordNode(BinaryOpNode):
    def __init__(self, register, address):
        super().__init__(register, address)


class TernaryOpNode(InstructionNode):
    def __init__(self, left, middle, right):
        # super().__init__(node)
        self.left = left
        self.middle = middle
        self.right = right


class AddNode(TernaryOpNode):
    def __init__(self, register_dest, register_left, register_right):
        super().__init__(register_dest, register_left, register_right)


class SubNode(TernaryOpNode):
    def __init__(self, register_dest, register_left, register_right):
        super().__init__(register_dest, register_left, register_right)


class AddiNode(TernaryOpNode):
    def __init__(self, register_dest, register_left, value):
        super().__init__(register_dest, register_left, value)


class JumpNode(MipsAstNode):
    def __init__(self, address):
        # super().__init__(node)
        self.address = address


class JumpRegisterNode(MipsAstNode):
    def __init__(self, register):
        # super().__init__(node)
        self.register = register


class JumpAndLinkNode(MipsAstNode):
    def __init__(self, address):
        # super().__init__(node)
        self.address = address


class JumpRegisterLinkNode(MipsAstNode):
    def __init__(self, register):
        # super().__init__(node)
        self.register = register


class AssemblerDirectiveNode(MipsAstNode):
    def __init__(self, list=[]):
        # super().__init__(node)
        self.list = list


class WordDirectiveNode(AssemblerDirectiveNode):
    def __init__(self, list):
        super().__init__(list)


class MemoryAddressLabelNode(MipsAstNode):
    def __init__(self, address, index):
        # super().__init__(node)
        self.address = address
        self.index = index


class MemoryAddressRegisterNode(MipsAstNode):
    def __init__(self, register, index):
        # super().__init__(node)
        self.register = register
        self.index = index


class LabelInstructionNode(InstructionNode):
    def __init__(self, label):
        # super().__init__(node)
        self.label = label

