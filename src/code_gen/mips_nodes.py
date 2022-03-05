#from re import L
#from soupsieve import select

#from src.cmp.cil import InstructionNode


from matplotlib.pyplot import cla


class MIPS_Node:
    pass


class ProgramNode(MIPS_Node):
    def __init__(self, data, code):
        self.data = data
        self.text = code

class DataNode(MIPS_Node):
        pass
    
class InstructionNode(MIPS_Node):
        pass
    
class DataTransferNode(InstructionNode):
    pass

class ProcedureNode(InstructionNode):
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
    
class LoadByteNode(DataTransferWithOffset):
    def __str__(self):
        return f'lb {self.source}, {str(self.offset)}({self.destination})'
        
class StoreWordNode(DataTransferWithOffset):
    def __str__(self):
        return f'sw {self.source}, {str(self.offset)}({self.destination})'
    
class StoreByteNode(DataTransferWithOffset):
    def __str__(self):
        return f'sb {self.source}, {str(self.offset)}({self.destination})'
    
class LoadNode(DataTransferNode):
    def __init__(self,dest,value):
        self.destination = dest
        self.value = value

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


class DataTypeNode(DataNode):
    def __init__(self,datatype,name,vt_values):
        self.datatype = datatype
        self.name = name
        self.vt_values = vt_values

    def __str__(self):
        values = ""
        for value in self.vt_values:
            values += f", {value}"
        return f"{self.name} : {self.datatype}{values}"
    
class ArithAnfLogicNode(InstructionNode):
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

class HiLoOperationNode(InstructionNode):
    def __init__(self,left,right):
        self.left = left
        self.right = right
    
class MultNode(HiLoOperationNode):
     def __str__(self):
        return f'mult {self.left}, {self.right}'

class DivideNode(HiLoOperationNode):
     def __str__(self):
        return f'div {self.left}, {self.right}'

class MoveFromHi(InstructionNode):
    def __init__(self,register):
        self.register = register
        
    def __str__(self):
        return f'mfhi {self.register}'
    
class MoveFromLo(InstructionNode):
    def __init__(self,register):
        self.register = register
        
    def __str__(self):
        return f'mflo {self.register}'
        
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