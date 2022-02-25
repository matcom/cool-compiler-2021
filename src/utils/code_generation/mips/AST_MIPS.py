
class mips_ast:
    class Node:
        pass

    class ProgramNode(Node):
        def __init__(self, data, types, functions):
            self._data = data
            self._types = types
            self._functions = functions

        @property
        def data(self):
            return self._data

        @property
        def types(self):
            return self._types

        @property
        def functions(self):
            return self._functions

    class DataNode(Node):
        def __init__(self, label):
            self._label = label

        @property
        def label(self):
            return self._label

    class FunctionNode(Node):
        def __init__(self, label, params, localvars):
            self._label = label
            self._instructions = []
            self._params = params
            self._localvars = localvars

        @property
        def label(self):
            return self._label

        @property
        def instructions(self):
            return self._instructions

        def add_instructions(self, instructions):
            self._instructions.extend(instructions)

        def get_param_stack_location(self, name):
            index = self._params.index(name)
            offset = ((len(self._params) - 1) - index) * 4
            return RegisterRelativeLocation(Register('fp'), offset)

        def get_local_stack_location(self, name):
            index = self._localvars.index(name)
            offset = (index + 2) * -4
            return RegisterRelativeLocation(Register('fp'), offset)

        def get_var_location(self, name):
            try:
                return self.get_param_stack_location(name)
            except ValueError:
                return self.get_local_stack_location(name)

    class InstructionNode(Node):
        pass

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

    class LabelNode(InstructionNode):
        def __init__(self, name):
            self.name = name

    class ComplementNode(InstructionNode):
        def __init__(self, reg1, reg2):
            self.reg1 = reg1
            self.reg2 = reg2

    class StringConst(DataNode):
        def __init__(self, label, string):
            super().__init__(label)
            self._string = string

        @property
        def string(self):
            return self._string

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

    class JumpRegisterNode(InstructionNode):
        def __init__(self, reg):
            self.reg = reg

    class AddInmediateNode(InstructionNode):
        def __init__(self, dest, src, value):
            self.dest = dest
            self.src = src
            self.value = value

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

    class MoveFromLowNode(InstructionNode):
        def __init__(self, reg):
            self.reg = reg


class Register():
    def __init__(self, name):
        self.name = name


ARG_REGISTERS = [Register(name) for name in ['a0', 'a1', 'a2', 'a3']]


SP_REG = Register('sp')
RA_REG = Register('ra')
V0_REG = Register('v0')
V1_REG = Register('v1')
ZERO_REG = Register('zero')
LOW_REG = Register('low')


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
