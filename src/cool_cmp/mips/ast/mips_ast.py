import enum

class Node:
    def __init__(self,row=None,column=None,comment=None):
        self.row = row
        self.column = column
        self.comment = comment

class ProgramNode(Node):
    def __init__(self, comment=None):
        super().__init__(row=-1, column=-1, comment=comment)
        self.instructions = []
        self.data = []

class DataNode(Node):
    def __init__(self, name, type, values, row=None, column=None, comment=None):
        """
        values: Value List. Must be a LIST
        """
        super().__init__(row=row, column=column, comment=comment)
        self.name = name
        self.type = type
        self.values = values

class ASCIIZNode(DataNode):
    def __init__(self, name, string, row=None, column=None, comment=None):
        super().__init__(name, MipsTypes.asciiz, [string], row=row, column=column, comment=comment)

class ArithmeticNode(Node):
    pass
        
class BinaryArithmeticNode(ArithmeticNode):
    def __init__(self, result, first_arg, second_arg, row=None, column=None, comment=None):
        super().__init__(row=row, column=column, comment=comment)
        self.result = result
        self.first_arg = first_arg
        self.second_arg = second_arg

class AddNode(BinaryArithmeticNode):
    pass

class SubstractNode(BinaryArithmeticNode):
    pass

class AddImmediateNode(BinaryArithmeticNode):
    pass

class AddUnsignedNode(BinaryArithmeticNode):
    pass

class SubstractUnsignedNode(BinaryArithmeticNode):
    pass

class AddImmediateUnsignedNode(BinaryArithmeticNode):
    pass

class MultiplyNoOverflowNode(BinaryArithmeticNode):
    pass

class AndNode(BinaryArithmeticNode):
    pass

class OrNode(BinaryArithmeticNode):
    pass

class NorNode(BinaryArithmeticNode):
    pass

class AndImmediateNode(BinaryArithmeticNode):
    pass

class OrImmediateNode(BinaryArithmeticNode):
    pass

class ShiftLeftNode(BinaryArithmeticNode):
    pass

class ShiftRightNode(BinaryArithmeticNode):
    pass

class SetLessThanNode(BinaryArithmeticNode):
    pass

class SetLessOrEqualThanNode(BinaryArithmeticNode):
    pass

class SetLessThanImmediateNode(BinaryArithmeticNode):
    pass

class SetGreaterOrEqualThanNode(BinaryArithmeticNode):
    pass

class SetGreaterThanNode(BinaryArithmeticNode):
    pass

class SetEqualToNode(BinaryArithmeticNode):
    pass

class SetNotEqualToNode(BinaryArithmeticNode):
    pass

class OperationOverflowNode(ArithmeticNode):
    def __init__(self, first_arg, second_arg, row=None, column=None, comment=None):
        super().__init__(row=row, column=column, comment=comment)
        self.first_arg = first_arg
        self.second_arg = second_arg

class MultiplyOverflowNode(OperationOverflowNode):
    pass

class DivideOverflowNode(OperationOverflowNode):
    pass

class InstructionNode(Node):
    pass

class LoadWordNode(InstructionNode):
    def __init__(self, dest, offset, base_source_dir, row=None, column=None, comment=None):
        super().__init__(row=row, column=column, comment=comment)
        self.dest = dest
        self.offset = offset
        self.base_source_dir = base_source_dir

class LoadByteNode(InstructionNode):
    def __init__(self, dest, offset, base_source_dir, row=None, column=None, comment=None):
        super().__init__(row=row, column=column, comment=comment)
        self.dest = dest
        self.offset = offset
        self.base_source_dir = base_source_dir

class StoreWordNode(InstructionNode):
    def __init__(self, source, offset, base_dest_dir, row=None, column=None, comment=None):
        super().__init__(row=row, column=column, comment=comment)        
        self.source = source
        self.offset = offset
        self.base_dest_dir = base_dest_dir

class StoreByteNode(InstructionNode):
    def __init__(self, source, offset, base_dest_dir, row=None, column=None, comment=None):
        super().__init__(row=row, column=column, comment=comment)        
        self.source = source
        self.offset = offset
        self.base_dest_dir = base_dest_dir

class LoadAddressNode(InstructionNode):
    def __init__(self, dest, label, row=None, column=None, comment=None):
        super().__init__(row=row, column=column, comment=comment)
        self.dest = dest
        self.label = label

class LoadImmediateNode(InstructionNode):
    def __init__(self, dest, value, row=None, column=None, comment=None):
        super().__init__(row=row, column=column, comment=comment)
        self.dest = dest
        self.value = value

class MoveFromHiNode(InstructionNode):
    def __init__(self, dest, row=None, column=None, comment=None):
        super().__init__(row=row, column=column, comment=comment)
        self.dest = dest

class MoveFromLoNode(InstructionNode):
    def __init__(self, dest, row=None, column=None, comment=None):
        super().__init__(row=row, column=column, comment=comment)
        self.dest = dest

class MoveNode(InstructionNode):
    def __init__(self, dest, source, row=None, column=None, comment=None):
        super().__init__(row=row, column=column, comment=comment)
        self.dest = dest
        self.source = source
        
class BranchNode(InstructionNode):
    def __init__(self, first_arg, second_arg, address, row=None, column=None, comment=None):
        super().__init__(row=row, column=column, comment=comment)
        self.first_arg = first_arg
        self.second_arg = second_arg
        self.address = address
        
class BranchEqualNode(BranchNode):
    pass

class BranchNotEqualNode(BranchNode):
    pass

class BranchGreaterNode(BranchNode):
    pass

class BranchGreaterEqualNode(BranchNode):
    pass

class BranchLessEqualNode(BranchNode):
    pass

class BranchLessNode(BranchNode):
    pass
        
class JumpNode(InstructionNode):
    def __init__(self, address, row=None, column=None, comment=None):
        super().__init__(row=row, column=column, comment=comment)
        self.address = address

class JumpRegisterNode(InstructionNode):
    def __init__(self, register, row=None, column=None, comment=None):
        super().__init__(row=row, column=column, comment=comment)
        self.register = register

class JumpAndLinkNode(InstructionNode):
    def __init__(self, address, row=None, column=None, comment=None):
        super().__init__(row=row, column=column, comment=comment)
        self.address = address

class LabelNode(InstructionNode):
    def __init__(self, label, row=None, column=None, comment=None):
        super().__init__(row=row, column=column, comment=comment)
        self.label = label

class SyscallNode(InstructionNode):
    def __init__(self, row=None, column=None, comment=None):
        super().__init__(row=row, column=column, comment=comment)

class MipsTypes():
    ascii = '.ascii'
    asciiz = '.asciiz'
    byte = '.byte'
    halfword = '.halfword'
    word = '.word'
    space = '.space'

# class PrintIntNode(InstructionNode):
#     pass

# class PrintStringNode(InstructionNode):
#     pass

# class ReadIntNode(InstructionNode):
#     pass

# class ReadStringNode(InstructionNode):
#     pass

# class ExitNode(InstructionNode):
#     pass
