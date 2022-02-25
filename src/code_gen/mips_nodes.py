from re import L
from soupsieve import select

from src.cmp.cil import InstructionNode


class MIPS_Node:
    pass


class ProgramNode(MIPS_Node):
    def __init__(self, data, code):
        self.data = data
        self.text = code

class MIPSDataNode(MIPS_Node):
        pass
    
class MIPSInstructionNode(MIPS_Node):
        pass
    
class DataTransferNode(MIPSInstructionNode):
    pass

class ProcedureNode(MIPSInstructionNode):
    def __init__(self, label):
        self.label = label
        self.instructions = []



class DataTransferWithOffset(DataTransferNode):
    def __init__(self,source,offset,dest):
        self.source = source
        self.offset = offset
        self.destination = dest
        
class LoadWordNode(DataTransferWithOffset):
    def __str__(self):
        return f'lw {self.source}, {str(self.offset)}({self.destination})'
        
class StoreWordNode(DataTransferWithOffset):
    def __str__(self):
        return f'sw {self.source}, {str(self.offset)}({self.destination})'
    
class LoadNode(DataTransferNode):
    def __init__(self,dest,value):
        self.destination = dest
        self.value

class LoadInmediate(LoadNode):
    def __str__(self):
        return f'li {self.destination}, {self.value}'

class LoadAddress(LoadNode):
    def __str__(self):
        return f'la {self.destination}, {self.value}'

class MoveNode(DataTransferNode):
    def __init__(self, destination, source):
        self.destination = destination
        self.source = source

    def __str__(self):
        return f"move {self.destination} {self.source}"


class DataTypeNode(MIPSDataNode):
    def __init__(self, name, datatype,vt_values):
        self.name = name
        self.datatype = datatype
        self.vt_values = vt_values

    def __str__(self):
        values = ""
        for value in self.vt_values:
            values += f", {value}"
        return f"{self.name} : {self.datatype}{values}"
    
class ArithAnfLogicNode(MIPSInstructionNode):
    def __init__(self, destination,left,right):
        self.destination = destination
        self.left = left
        self.right = right
        
class AddNode(ArithAnfLogicNode):
    def __str__(self):
        return f"add {self.destination}, {self.left}, {self.right}"        

class AddiNode(ArithAnfLogicNode):
    def __str__(self):
        return f"addi {self.destination}, {self.left}, {self.right}"

class SubNode(ArithAnfLogicNode):
    def __str__(self):
        return f"sub {self.destination}, {self.left}, {self.right}"
    
class ConditionalBranch(InstructionNode):
    def __init__(self,c1,c2,jump):
        self.c1 = c1
        self.c2 = c2
        self.jump = jump
        
class BranchOnEqualNode(ConditionalBranch):
    def __str__(self):
        return f"beq {self.c1}, {self.c2}, {self.jump}"
        
class BranchOnNotEqualNode(ConditionalBranch):
    def __str__(self):
        return f"bne {self.c1}, {self.c2}, {self.jump}"

class BranchOnGreaterThanNode(ConditionalBranch):
    def __str__(self):
        return f"bgt {self.c1}, {self.c2}, {self.jump}"

class BranchOnGreaterOrEqNode(ConditionalBranch):
    def __str__(self):
        return f"bge {self.c1}, {self.c2}, {self.jump}"

class BranchOnLessThanNode(ConditionalBranch):
    def __str__(self):
        return f"blt {self.c1}, {self.c2}, {self.jump}"
    
class BranchOnLessOrEqNode(ConditionalBranch):
    def __str__(self):
        return f"ble {self.c1}, {self.c2}, {self.jump}"

class ComparisonNode(InstructionNode):
    def __init__(self,m1,m2,dest):
        self.m1 = m1
        self.m2 = m2
        self.destination = dest
        
class SetOnLessThan(ComparisonNode):
    def __str__(self):
        return f"slt {self.dest}, {self.m1}, {self.m2}"
        
class SetOnLessThanInmediate(ComparisonNode):
    def __str__(self):
        return f"slt {self.dest}, {self.m1}, {self.m2}"
        
class UnconditionalJumpNode(InstructionNode):
    def __init__(self,jump):
        self.jump = jump
        
class Jump(UnconditionalJumpNode):
    def __str__(self):
        return f"j {self.jump}"        

class JumpRegister(UnconditionalJumpNode):
    def __str__(self):
        return f"jr {self.jump}"   

class JumpAndLink(UnconditionalJumpNode):
    def __str__(self):
        return f"jal {self.jump}"   

class Label(InstructionNode):
    def __init__(self,label):
        self.label = label
    
    def __str__(self):
        return f"{self.label}:"
    
class SyscallNode(InstructionNode):
    def __str__(self):
        return f"syscall"
    

class CommentNode(MIPS_Node):
    def __init__(self,text):
        self.text = text
    
    def __str__(self):
        return f"#{self.text}"