# ***********************Registers***********************
class Register:
    def __init__(self, name):
        self.name = name


FP = Register("fp")
SP = Register("sp")
RA = Register("ra")
V0 = Register("v0")
RA = Register("ra")
A0 = Register("a0")
A1 = Register("a1")
A2 = Register("a2")
A3 = Register("a3")
ZERO = Register("zero")
T0 = Register("t0")
T1 = Register("t1")
T2 = Register("t2")

# ***********************Registers***********************

# ***********************Utils***********************

MAIN_FUNCTION_NAME = "function_main_at_Main"
VIRTUAL_TABLE = "virtual_table"
TYPE_LIST = "type_list"


def push_to_stack(register: Register):
    update_sp = AddInmediateNode(SP, SP, -4)
    offset = RegisterRelativeLocation(SP, 0)
    store_word = StoreWordNode(register, offset)
    return [update_sp, store_word]


def pop_from_stack(register: Register):
    load_word = LoadWordNode(register, RegisterRelativeLocation(SP, 0))
    update_sp = AddInmediateNode(SP, SP, 4)
    return [load_word, update_sp]


def exit_program():
    instructions = []
    instructions.append(LoadInmediateNode(V0, 10))
    instructions.append(SyscallNode())
    return instructions


# ***********************Utils***********************


# ***********************AST***********************


class Node:
    pass


class ProgramNode(Node):
    def __init__(self, types, data, text):
        self.types = types
        self.data = data
        self.text = text


class DataNode(Node):
    def __init__(self, label, data):
        self.label = label
        self.data = data


class FunctionNode(Node):
    def __init__(self, label, params, localvars):
        self.label = label
        self.params = params
        self.localvars = localvars
        self.instructions = []


class TypeNode(Node):
    def __init__(self, label):
        self.label = label
        self.methods = []
        self.attributes = []
        self.label_name = None
        self.pos = -1


class InstructionNode(Node):
    pass


class LabelNode(InstructionNode):
    def __init__(self, label):
        self.label = label


class MoveNode(InstructionNode):
    def __init__(self, reg1, reg2):
        self.reg1 = reg1
        self.reg2 = reg2


class LoadInmediateNode(InstructionNode):
    def __init__(self, reg, value):
        self.reg = reg
        self.value = value


class LoadWordNode(InstructionNode):
    def __init__(self, reg, addr):
        self.reg = reg
        self.addr = addr


class SyscallNode(InstructionNode):
    pass


class LoadAddressNode(InstructionNode):
    def __init__(self, reg, label):
        self.reg = reg
        self.label = label


class StoreWordNode(InstructionNode):
    def __init__(self, reg, addr):
        self.reg = reg
        self.addr = addr


class JumpAndLinkNode(InstructionNode):
    def __init__(self, label):
        self.label = label


class JumpRegisterAndLinkNode(InstructionNode):
    def __init__(self, reg):
        self.reg = reg


class JumpRegister(InstructionNode):
    def __init__(self, reg):
        self.reg = reg


class AddInmediateNode(InstructionNode):
    def __init__(self, dest, src, value):
        self.dest = dest
        self.src = src
        self.constant_number = value


class AddInmediateUnsignedNode(InstructionNode):
    def __init__(self, dest, src, value):
        self.dest = dest
        self.src = src
        self.value = value


class AddUnsignedNode(InstructionNode):
    def __init__(self, dest, sum1, sum2):
        self.dest = dest
        self.sum1 = sum1
        self.sum2 = sum2


class ShiftLeftLogicalNode(InstructionNode):
    def __init__(self, dest, src, bits):
        self.dest = dest
        self.src = src
        self.bits = bits


class BranchOnNotEqualNode(InstructionNode):
    def __init__(self, reg1, reg2, label):
        self.reg1 = reg1
        self.reg2 = reg2
        self.label = label


class JumpNode(InstructionNode):
    def __init__(self, label):
        self.label = label


class AddNode(InstructionNode):
    def __init__(self, reg1, reg2, reg3):
        self.reg1 = reg1
        self.reg2 = reg2
        self.reg3 = reg3


class SubNode(InstructionNode):
    def __init__(self, reg1, reg2, reg3):
        self.reg1 = reg1
        self.reg2 = reg2
        self.reg3 = reg3


class MultiplyNode(InstructionNode):
    def __init__(self, reg1, reg2, reg3):
        self.reg1 = reg1
        self.reg2 = reg2
        self.reg3 = reg3


class DivideNode(InstructionNode):
    def __init__(self, reg1, reg2):
        self.reg1 = reg1
        self.reg2 = reg2


class ComplementNode(InstructionNode):
    def __init__(self, reg1, reg2):
        self.reg1 = reg1
        self.reg2 = reg2


class MoveFromLowNode(InstructionNode):
    def __init__(self, reg):
        self.reg = reg


class RegisterRelativeLocation:
    def __init__(self, register, offset):
        self.register = register
        self.offset = offset


class LabelRelativeLocation:
    def __init__(self, label, offset):
        self.label = label
        self.offset = offset
