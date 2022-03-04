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
    def __init__(self, comment=""):
        self.comment = comment


class SyscallNode(InstructionNode):
    def __init__(self, comment=""):
        super().__init__(comment)


class BinaryOpNode(InstructionNode):
    def __init__(self, left, right, comment=""):
        super().__init__(comment)
        self.left = left
        self.right = right


class LoadAddressNode(BinaryOpNode):
    def __init__(self, register, address, comment=""):
        super().__init__(register, address, comment)


class LoadWordNode(BinaryOpNode):
    def __init__(self, register, ram_dir, comment=""):
        super().__init__(register, ram_dir, comment)


class LoadByteNode(BinaryOpNode):
    def __init__(self, register, ram_dir, comment=""):
        super().__init__(register, ram_dir, comment)


class StoreWordNode(BinaryOpNode):
    def __init__(self, register, ram_dir, comment=""):
        super().__init__(register, ram_dir, comment)


class LoadInmediateNode(BinaryOpNode):
    def __init__(self, register, value, comment=""):
        super().__init__(register, value, comment)


class MultNode(BinaryOpNode):
    def __init__(self, left, right, comment=""):
        super().__init__(left, right, comment)


class DivNode(BinaryOpNode):
    def __init__(self, left, right, comment=""):
        super().__init__(left, right, comment)


class MoveNode(BinaryOpNode):
    def __init__(self, left, right, comment=""):
        super().__init__(left, right, comment)


class StoreWordNode(BinaryOpNode):
    def __init__(self, register, address, comment=""):
        super().__init__(register, address, comment)


class StoreByteNode(BinaryOpNode):
    def __init__(self, register, address, comment=""):
        super().__init__(register, address, comment)


class TernaryOpNode(InstructionNode):
    def __init__(self, left, middle, right, comment=""):
        super().__init__(comment)
        self.left = left
        self.middle = middle
        self.right = right


class AddNode(TernaryOpNode):
    def __init__(self, register_dest, register_left, register_right, comment=""):
        super().__init__(register_dest, register_left, register_right, comment)


class SubNode(TernaryOpNode):
    def __init__(self, register_dest, register_left, register_right, comment=""):
        super().__init__(register_dest, register_left, register_right, comment)


class AddiNode(TernaryOpNode):
    def __init__(self, register_dest, register_left, value, comment=""):
        super().__init__(register_dest, register_left, value, comment)


class BgtzNode(BinaryOpNode):
    def __init__(self, register, target, comment=""):
        super().__init__(register, target, comment)


class BltzNode(BinaryOpNode):
    def __init__(self, register, target, comment=""):
        super().__init__(register, target, comment)


class BeqzNode(BinaryOpNode):
    def __init__(self, register, target, comment=""):
        super().__init__(register, target, comment)


class JumpNode(InstructionNode):
    def __init__(self, address, comment=""):
        super().__init__(comment)
        self.address = address


class JumpRegisterNode(InstructionNode):
    def __init__(self, register, comment=""):
        super().__init__(comment)
        self.register = register


class JumpAndLinkNode(InstructionNode):
    def __init__(self, address, comment=""):
        super().__init__(comment)
        self.address = address


class JumpRegisterLinkNode(InstructionNode):
    def __init__(self, register, comment=""):
        super().__init__(comment)
        self.register = register


class MoveFromHi(InstructionNode):
    def __init__(self, register, comment=""):
        super().__init__(comment)
        self.register = register


class MoveFromLo(InstructionNode):
    def __init__(self, register, comment=""):
        super().__init__(comment)
        self.register = register


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
