class Node:
    pass

class ProgramNode(Node):
    def __init__(self, data, text):
        self.data = data
        self.text = text

    def __str__(self):
        data_code = ''
        for data in self.data:
            data_code += f'{data}\n'
        
        text_code = ''
        for text in self.text:
            text_code += f'{text}\n'
        
        return f'\t\t.data\n{data_code}\t\t.text\n{text_code}'

class DataNode(Node):
    def __init__(self, id, datas):
        self.id = id 
        self.datas = datas

    def __str__(self):
        data_code = ''
        for data in self.datas:
            data_code += f'{data}\n'

        return f'{self.id}:\n{data_code}'

class DataValuesNode(Node):
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        if self.type == 'ascii':
            return f'\t\t.{self.type}\t"{self.value}"'
        return f'\t\t.{self.type}\t{self.value}'

class SubroutineNode(Node):
    def __init__(self, id, instrs):
        self.id = id
        self.instrs = instrs

    def __str__(self):
        instrs_code = ''
        for instr in self.instrs:
            instrs_code += f'{instr}\n'

        return f'{self.id}:\n{instrs_code}'

class InstructionNode(Node):
    pass

class R_TypeNode(InstructionNode):
    def __init__(self, r0, r1=None, r2=None):
        self.r0 = r0
        self.r1 = r1
        self.r2 = r2

class AddNode(R_TypeNode):
    def __str__(self):
        return f'\t\tadd\t\t${self.r0}, ${self.r1}, ${self.r2}'

class AdduNode(R_TypeNode):
    def __str__(self):
        return f'\t\taddu\t\t${self.r0}, ${self.r1}, ${self.r2}'

class SubNode(R_TypeNode):
    def __str__(self):
        return f'\t\tsub\t\t${self.r0}, ${self.r1}, ${self.r2}'

class MultNode(R_TypeNode):
    def __str__(self):
        return f'\t\tmult\t\t${self.r0}, ${self.r1}'

class DivNode(R_TypeNode):
    def __str__(self):
        return f'\t\tdiv\t\t${self.r0}, ${self.r1}'

class MfhiNode(R_TypeNode):
    def __str__(self):
        return f'\t\tmfhi\t\t${self.r0}'

class MfloNode(R_TypeNode):
    def __str__(self):
        return f'\t\tmflo\t\t${self.r0}'

class AndNode(R_TypeNode):
    def __str__(self):
        return f'\t\tand\t\t${self.r0}, ${self.r1}, ${self.r2}'

class OrNode(R_TypeNode):
    def __str__(self):
        return f'\t\tor\t\t${self.r0}, ${self.r1}, ${self.r2}'

class XorNode(R_TypeNode):
    def __str__(self):
        return f'\t\txor\t\t${self.r0}, ${self.r1}, ${self.r2}'

class NorNode(R_TypeNode):
    def __str__(self):
        return f'\t\tnor\t\t${self.r0}, ${self.r1}, ${self.r2}'

class SltNode(R_TypeNode):
    def __str__(self):
        return f'\t\tslt\t\t${self.r0}, ${self.r1}, ${self.r2}'

class SltNode(R_TypeNode):
    def __str__(self):
        return f'\t\tslt\t\t${self.r0}, ${self.r1}, ${self.r2}'

class JrNode(R_TypeNode):
    def __str__(self):
        return f'\t\tjr\t\t${self.r0}'

class I_TypeNode(InstructionNode):
    def __init__(self, r0, const, r1=None):
        self.r0 = r0
        self.r1 = r1
        self.const = const

class AddiNode(I_TypeNode):
    def __str__(self):
        return f'\t\taddi\t\t${self.r0}, ${self.r1}, {self.const}'

class MoveNode(I_TypeNode):
    def __str__(self):
        return f'\t\taddi\t\t${self.r0}, ${self.r1}, 0'

class AddiuNode(I_TypeNode):
    def __str__(self):
        return f'\t\taddiu\t\t${self.r0}, ${self.r1}, {self.const}'

class LaNode(I_TypeNode):
    def __str__(self):
        return f'\t\tla\t\t${self.r0}, {self.const}'

class LwNode(I_TypeNode):
    def __str__(self):
        return f'\t\tlw\t\t${self.r0}, {self.const}(${self.r1})'

class SwNode(I_TypeNode):
    def __str__(self):
        return f'\t\tsw\t\t${self.r0}, {self.const}(${self.r1})'

class LiNode(I_TypeNode):
    def __str__(self):
        return f'\t\tli\t\t${self.r0}, {self.const}'

class AndiNode(I_TypeNode):
    def __str__(self):
        return f'\t\tandi\t\t${self.r0}, ${self.r1}, {self.const}'

class OriNode(I_TypeNode):
    def __str__(self):
        return f'\t\tori\t\t${self.r0}, ${self.r1}, {self.const}'

class SltiNode(I_TypeNode):
    def __str__(self):
        return f'\t\tslti\t\t${self.r0}, ${self.r1}, {self.const}'

class SllNode(I_TypeNode):
    def __str__(self):
        return f'\t\tsll\t\t${self.r0}, ${self.r1}, {self.const}'

class SrlNode(I_TypeNode):
    def __str__(self):
        return f'\t\tsrl\t\t${self.r0}, ${self.r1}, {self.const}'

class SraNode(I_TypeNode):
    def __str__(self):
        return f'\t\tsra\t\t${self.r0}, ${self.r1}, {self.const}'

class BeqNode(I_TypeNode):
    def __str__(self):
        return f'\t\tbeq\t\t${self.r0}, ${self.r1}, {self.const}'

class BneNode(I_TypeNode):
    def __str__(self):
        return f'\t\tbne\t\t${self.r0}, ${self.r1}, {self.const}'

class BgtNode(I_TypeNode):
    def __str__(self):
        return f'\t\tbgt\t\t${self.r0}, ${self.r1}, {self.const}'

class BltNode(I_TypeNode):
    def __str__(self):
        return f'\t\tblt\t\t${self.r0}, ${self.r1}, {self.const}'

class BgeNode(I_TypeNode):
    def __str__(self):
        return f'\t\tbge\t\t${self.r0}, ${self.r1}, {self.const}'

class BleNode(I_TypeNode):
    def __str__(self):
        return f'\t\tble\t\t${self.r0}, ${self.r1}, {self.const}'

class BeqNode(I_TypeNode):
    def __str__(self):
        return f'\t\tbeq\t\t${self.r0}, ${self.r1}, {self.const}'

class BeqzNode(I_TypeNode):
    def __str__(self):
        return f'\t\tbeqz\t\t${self.r0}, ${self.r1}, {self.const}'

class BgtuNode(I_TypeNode):
    def __str__(self):
        return f'\t\tbgtu\t\t${self.r0}, ${self.r1}, {self.const}'

class BgtzNode(I_TypeNode):
    def __str__(self):
        return f'\t\tbgtz\t\t${self.r0}, ${self.r1}, {self.const}'

class J_TypeNode(InstructionNode):
    def __init__(self, const):
        self.const = const

class JNode(J_TypeNode):
    def __str__(self):
        return f'\t\tj\t\t{self.const}'

class JalNode(J_TypeNode):
    def __str__(self):
        return f'\t\tjal\t\t{self.const}'

class SyscallNode(InstructionNode):
    def __str__(self):
        return f'\t\tsyscall'