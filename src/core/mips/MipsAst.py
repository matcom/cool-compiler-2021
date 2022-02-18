DOUBLE_WORD = 4
REGISTERS_NAMES = ['t0', 't1', 't2', 't3', 't4', 't5', 't6', 't7', 't8']
ARG_REGISTERS_NAMES = ['a0', 'a1', 'a2', 'a3']

TYPES_LABEL = "types_table"
PROTOTYPE_LABEL = "prototype_table"


class Register:
    def __init__(self, name):
        self.name = name


REGISTERS = [Register(i) for i in REGISTERS_NAMES]
ARG_REGISTERS = [Register(i) for i in ARG_REGISTERS_NAMES]
FP_REG = Register('fp')
SP_REG = Register('sp')
RA_REG = Register('ra')
V0_REG = Register('v0')
V1_REG = Register('v1')
ZERO_REG = Register('zero')
LOW_REG = Register('lo')
GP_REG = Register('gp')


class Node:
    def __init__(self, line=0, column=0):
        self.line = line
        self.column = column


class ProgramNode(Node):
    def __init__(self, data, types, functions, line, column):
        super().__init__(line, column)
        self.data = data
        self.types = types
        self.functions = functions


class FunctionNode(Node):
    def __init__(self, label, params, localvars, line, column):
        super().__init__(line, column)
        self.label = label
        self.instructions = []
        self.params = params
        self.localvars = localvars

    def add_instruction(self, instruction):
        self.instructions.append(instruction)

    def get_param_stack_location(self, name):
        # TODO Tener en cuenta que los primeros argumentos se guardan en los registros para argumentos
        index = self.params.index(name)
        offset = ((len(self.params) - 1) - index) * DOUBLE_WORD
        return RegisterRelativeLocation(FP_REG, offset)

    def get_local_stack_location(self, name):
        index = self.localvars.index(name)
        offset = (len(self.localvars) + 2 - index) * DOUBLE_WORD
        return RegisterRelativeLocation(FP_REG, -offset)

    def get_var_location(self, name):
        try:
            return self.get_param_stack_location(name)
        except ValueError:
            return self.get_local_stack_location(name)


class InstructionNode(Node):
    pass


class AbsoluteNode(InstructionNode):
    # rdest <- abs(rsrc)
    def __init__(self, rdest, rsrc, line, column):
        '''
        Put the absolute value of register rsrc in register rdest
        '''
        super().__init__(line, column)
        self.rdest = rdest
        self.rsrc = rsrc


class AdditionNode(InstructionNode):
    # rd <- rs + rt
    def __init__(self, rdest, rsrc1, rsrc2, line, column):
        '''
        Put the sum of registers rsrc1 and rsrc2 into register rdest.
        '''
        super().__init__(line, column)
        self.rdest = rdest
        self.rsrc1 = rsrc1
        self.rsrc2 = rsrc2


class AdditionInmediateNode(InstructionNode):
    def __init__(self, rdest, rsrc, imm, line, column):
        '''
        Put the sum of register rsrc and the sign-extended immediate into register rdest
        '''
        super().__init__(line, column)
        self.rdest = rdest
        self.rsrc = rsrc
        self.imm = imm


class DivideNode(InstructionNode):
    def __init__(self, rsrc1, rsrc2, line, column):
        '''
        Put the quotient of register rsrc1 and src2 into register Hi/Lo.
        '''
        super().__init__(line, column)
        self.rsrc1 = rsrc1
        self.rsrc2 = rsrc2

class MoveLowNode(InstructionNode):

    def __init__(self, dest, line, column):
        '''
        Put the content of register low into register rsrc.
        '''
        super().__init__(line, column)
        self.dest = dest

class MoveHighNode(InstructionNode):

    def __init__(self, dest, line, column):
        '''
        Put the content of register Hi into register rsrc.
        '''
        super().__init__(line, column)
        self.dest = dest



class MultiplyNode(InstructionNode):
    def __init__(self, rdest, rsrc1, rsrc2, line, column):
        '''
        Put the product of register rsrc1 and src2 into register rdest.
        '''
        super().__init__(line, column)
        self.rdest = rdest
        self.rsrc1 = rsrc1
        self.rsrc2 = rsrc2


class NegateNode(InstructionNode):
    def __init__(self, rdest, rsrc1, line, column):
        '''
        Put the negation of register rsrc1 into register rdest.
        '''
        super().__init__(line, column)
        self.rdest = rdest
        self.rsrc1 = rsrc1


class SubstractionNode(InstructionNode):
    def __init__(self, rdest, rsrc1, rsrc2, line, column):
        '''
        Put the difference of register rsrc1 and rsrc2 into register rdest.
        '''
        super().__init__(line, column)
        self.rdest = rdest
        self.rsrc1 = rsrc1
        self.rsrc2 = rsrc2


class LessNode(InstructionNode):
    def __init__(self, rdest, rsrc1, rsrc2, line, column):
        '''
        Set register rdest to 1 if register rsrc1 is less than rsrc2, and 0 otherwise
        '''
        super().__init__(line, column)
        self.rdest = rdest
        self.rsrc1 = rsrc1
        self.rsrc2 = rsrc2


class LessInmediateNode(InstructionNode):
    def __init__(self, rdest, rsrc1, imm, line, column):
        '''
        Set register rdest to 1 if register rsrc1 is less than imm, and 0 otherwise
        '''
        super().__init__(line, column)
        self.rdest = rdest
        self.rsrc1 = rsrc1
        self.imm = imm


class EqualNode(InstructionNode):
    def __init__(self, rdest, rsrc1, rsrc2, line, column):
        '''
        Set register rdest to 1 if register rsrc1 equals rsrc2, and 0 otherwise
        '''
        super().__init__(line, column)
        self.rdest = rdest
        self.rsrc1 = rsrc1
        self.rsrc2 = rsrc2


class LessEqualNode(InstructionNode):
    def __init__(self, rdest, rsrc1, rsrc2, line, column):
        '''
        Set register rdest to 1 if register rsrc1 is less than or equal to rsrc2, and 0 otherwise
        '''
        super().__init__(line, column)
        self.rdest = rdest
        self.rsrc1 = rsrc1
        self.rsrc2 = rsrc2


class JumpNode(InstructionNode):
    def __init__(self, label, line, column):
        '''
        Unconditionally jump to the instruction at the label.
        '''
        super().__init__(line, column)
        self.label = label

class JumpRegisterNode(InstructionNode):
    def __init__(self, reg, line, column):
        '''
        Unconditionally jump to the instruction at the label.
        '''
        super().__init__(line, column)
        self.reg = reg


class JalNode(InstructionNode):
    def __init__(self, label, line, column):
        '''
        Unconditionally jump to the instruction at target. Save the address of the next
        instruction in register ra (rd said the manual).
        '''
        super().__init__(line, column)
        self.label = label


class MoveNode(InstructionNode):
    def __init__(self, reg1, reg2, line, column):
        super().__init__(line, column)
        self.reg1 = reg1
        self.reg2 = reg2


class StoreWordNode(InstructionNode):
    def __init__(self, reg, addr, line, column):
        super().__init__(line, column)
        self.reg = reg
        self.addr = addr


class LoadInmediateNode(InstructionNode):
    def __init__(self, reg, value, line, column):
        super().__init__(line, column)
        self.reg = reg
        self.value = value


class LoadWordNode(InstructionNode):
    def __init__(self, reg, addr, line, column):
        super().__init__(line, column)
        self.reg = reg
        self.addr = addr


class LoadAddressNode(InstructionNode):
    def __init__(self, reg, label, line, column):
        '''
        Load computed address , not the contents of the location, into register rdest
        '''
        super().__init__(line, column)
        self.reg = reg
        self.label = label


class BranchOnNotEqualNode(InstructionNode):
    def __init__(self, reg1, reg2, label, line, column):
        super().__init__(line, column)
        self.reg1 = reg1
        self.reg2 = reg2
        self.label = label


class LabelNode(InstructionNode):
    def __init__(self, name, line, column):
        super().__init__(line, column)
        self.name = name


class NotNode(InstructionNode):
    def __init__(self, dest, src, line, column):
        super().__init__(line, column)
        self.dest = dest
        self.src = src


class ShiftLeftNode(InstructionNode):  # Shift Left Logical
    def __init__(self, dest, src, bits, line, column):
        super().__init__(line, column)
        self.dest = dest
        self.src = src
        self.bits = bits


class SyscallNode(InstructionNode):
    pass


class DataNode(Node):
    def __init__(self, label, line, column):
        super().__init__(line, column)
        self.label = label


class StringConst(DataNode):
    def __init__(self, label, string, line, column):
        super().__init__(label, line, column)
        self.string = string


class MIPSType:
    def __init__(self, label, name_addr, attributes,
                 methods, index, default=[]):
        self.label = label
        self.name = name_addr
        self.attributes = attributes
        self.default_attributes = dict(default)
        self.methods = methods
        self.index = index

    @property
    def size(self):
        return len(self.attributes) + DOUBLE_WORD

    @property
    def string_name_label(self):
        return self.name


class MemoryLocation:
    pass


class RegisterRelativeLocation(MemoryLocation):
    def __init__(self, register, offset):
        self._register = register
        self._offset = offset

    @property
    def register(self):
        return self._register

    @property
    def offset(self):
        return self._offset


class LabelRelativeLocation(MemoryLocation):
    def __init__(self, label, offset):
        self._label = label
        self._offset = offset

    @property
    def label(self):
        return self._label

    @property
    def offset(self):
        return self._offset


def push_register(reg, line, column):
    move_stack = AdditionInmediateNode(SP_REG, SP_REG, -DOUBLE_WORD, line, column)
    save_location = RegisterRelativeLocation(SP_REG, 0)
    save_register = StoreWordNode(reg, save_location, line, column)
    return [move_stack, save_register]


def pop_register(reg, line, column):
    load_value = LoadWordNode(reg, RegisterRelativeLocation(SP_REG, 0), line, column)
    move_stack = AdditionInmediateNode(SP_REG, SP_REG, DOUBLE_WORD, line, column)
    return [load_value, move_stack]


def create_object(reg1, reg2, line, column):
    instructions = []

    instructions.append(ShiftLeftNode(reg1, reg1, 2, line, column))
    instructions.append(LoadAddressNode(reg2, PROTOTYPE_LABEL, line, column))
    instructions.append(AdditionNode(reg2, reg2, reg1, line, column))
    instructions.append(LoadWordNode(reg2, RegisterRelativeLocation(reg2, 0), line, column))
    instructions.append(LoadWordNode(ARG_REGISTERS[0], RegisterRelativeLocation(reg2, 4), line, column))
    instructions.append(ShiftLeftNode(ARG_REGISTERS[0], ARG_REGISTERS[0], 2, line, column))
    instructions.append(JalNode("malloc", line, column))
    instructions.append(MoveNode(ARG_REGISTERS[2], ARG_REGISTERS[0], line, column))
    instructions.append(MoveNode(ARG_REGISTERS[0], reg2, line, column))
    instructions.append(MoveNode(ARG_REGISTERS[1], V0_REG, line, column))
    instructions.append(JalNode("copy", line, column))

    return instructions
