

DOUBLE_WORD = 4
REGISTERS_NAMES  = ['t0', 't1', 't2', 't3', 't4', 't5', 't6', 't7', 't8']
ARG_REGISTERS_NAMES = ['a0', 'a1', 'a2', 'a3']


class Register:
    def __init__(self, name):
        self.name = name


REGISTERS = [Register(i) for i in REGISTERS_NAMES]
ARG_REGISTERS = [Register(i) for i in ARG_REGISTERS_NAMES]
FP_REG     = Register('fp')
SP_REG     = Register('sp')
RA_REG     = Register('ra')
V0_REG     = Register('v0')
V1_REG     = Register('v1')
ZERO_REG   = Register('zero')
LOW_REG    = Register('low')


class Node:
    pass

class ProgramNode(Node):
    def __init__(self, data, types, functions):
        self.data = data
        self.types = types
        self.functions = functions


class FunctionNode(Node):
    def __init__(self, label, instructions, params, localvars):
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
        offset = (index + 2) * -DOUBLE_WORD
        return RegisterRelativeLocation(FP_REG, offset)

    def get_var_location(self, name):
        try:
            return self.get_param_stack_location(name)
        except ValueError:
            return self.get_local_stack_location(name)


class InstructionNode(Node):
    pass


class PrintIntNode(InstructionNode):
    # $a0 = integer
    pass

class PrintStringNode(InstructionNode):
    # $a0 = string
    pass

class ReadIntNode(InstructionNode):
    # integer(int $v0)
    pass

class ReadStringNode(InstructionNode):
    # integer(int $v0)
    pass

class ExitNode(InstructionNode):
    pass



class AbsoluteNode(InstructionNode):
    # rdest <- abs(rsrc)
    def __init__(self, rdest, rsrc):
        '''
        Put the absolute value of register rsrc in register rdest
        '''
        self.rdest = rdest
        self.rsrc = rsrc

class AdditionNode(InstructionNode):
    # rd <- rs + rt
    def __init__(self, rdest, rsrc1, rsrc2):
        '''
        Put the sum of registers rsrc1 and rsrc2 into register rdest.
        '''
        self.rdest = rdest
        self.rsrc1 = rsrc1
        self.rsrc2 = rsrc2

class AdditionInmediateNode(InstructionNode):
    def __init__(self, rdest, rsrc, imm):
        '''
        Put the sum of register rsrc and the sign-extended immediate into register rdest
        '''
        self.rdest = rdest
        self.rsrc = rsrc
        self.imm = imm

class DivideNode(InstructionNode):
    def __init__(self, rsrc1, rsrc2):
        '''
        Put the quotient of register rsrc1 and src2 into register Hi/Lo.
        '''
        self.rsrc1 = rsrc1
        self.rsrc2 = rsrc2

class MultiplyNode(InstructionNode):
    def __init__(self, rdest, rsrc1, rsrc2):
        '''
        Put the product of register rsrc1 and src2 into register rdest.
        '''
        self.rdest = rdest
        self.rsrc1 = rsrc1
        self.rsrc2 = rsrc2

class NegateNode(InstructionNode):
    def __init__(self, rdest, rsrc1):
        '''
        Put the negation of register rsrc1 into register rdest.
        '''
        self.rdest = rdest
        self.rsrc1 = rsrc1

class SubstractionNode(InstructionNode):
    def __init__(self, rdest, rsrc1, rsrc2):
        '''
        Put the difference of register rsrc1 and src2 into register rdest.
        '''
        self.rdest = rdest
        self.rsrc1 = rsrc1
        self.rsrc2 = rsrc2

class LessNode(InstructionNode):
    def __init__(self, rdest, rsrc1, rsrc2):
        '''
        Set register rdest to 1 if register rsrc1 is less than rsrc2, and 0 otherwise
        '''
        self.rdest = rdest
        self.rsrc1 = rsrc1
        self.rsrc2 = rsrc2

class LessInmediateNode(InstructionNode):
    def __init__(self, rdest, rsrc1, imm):
        '''
        Set register rdest to 1 if register rsrc1 is less than imm, and 0 otherwise
        '''
        self.rdest = rdest
        self.rsrc1 = rsrc1
        self.imm = imm

class EqualNode(InstructionNode):
    def __init__(self, rdest, rsrc1, rsrc2):
        '''
        Set register rdest to 1 if register rsrc1 equals rsrc2, and 0 otherwise
        '''
        self.rdest = rdest
        self.rsrc1 = rsrc1
        self.rsrc2 = rsrc2

class LessEqualNode(InstructionNode):
    def __init__(self, rdest, rsrc1, rsrc2):
        '''
        Set register rdest to 1 if register rsrc1 is less than or equal to rsrc2, and 0 otherwise
        '''
        self.rdest = rdest
        self.rsrc1 = rsrc1
        self.rsrc2 = rsrc2

class JumpNode(InstructionNode):
    def __init__(self, label):
        '''
        Unconditionally jump to the instruction at the label.
        '''
        self.label = label

class JalNode(InstructionNode):
    def __init__(self, label):
        '''
        Unconditionally jump to the instruction at target. Save the address of the next
        instruction in register ra (rd said the manual).
        '''
        self.label = label

class MoveNode(InstructionNode):
    def __init__(self, reg1, reg2):
        self.reg1 = reg1
        self.reg2 = reg2

class StoreWordNode(InstructionNode):
    def __init__(self, reg, addr):
        self.reg  = reg
        self.addr = addr

class LoadInmediateNode(InstructionNode):
    def __init__(self, reg, value):
        self.reg = reg
        self.value = value

class LoadWordNode(InstructionNode):
    def __init__(self, reg, addr):
        self.reg = reg
        self.addr = addr

class DataNode(Node):
    def __init__(self, label):
        self.label = label

class StringConst(DataNode):
    def __init__(self, label, string):
        super().__init__(label)
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

