from Semantic import visitor

t_REGISTERS = ['$t0', '$t1', '$t2', '$t3', '$t4', '$t5', '$t6', '$t7', '$t8']
a_REGISTERS = ['$a0', '$a1', '$a2', '$a3']
v_REGISTERS = ['$v0', '$v1']
zero_REGISTER = '$zero'
fp_REGISTER = '$fp'
sp_REGISTER = '$sp'
ra_REGISTER = '$ra'
lo_REGISTER = '$lo'
gp_REGISTER = '$gp'

LDATA = 8


class Node:
    pass

class Asciiz(Node):
    def __init__(self, name, string):
        self.name = name
        self.string = string

class Word(Node):
    def __init__(self, name, value):
        self.name = name
        self.value = value

class Type(Node):
    def __init__(self, name, attributes, methods):
        self.name = name
        self.attributes = attributes
        self.methods = methods

class Function(Node):
    def __init__(self, name, instructions):
        self.name = name
        self.instructions =  instructions

class Instruction(Node):
    def __init__(self, first = None, second = None, third = None):
        self.first = first
        self.second = second
        self.third = third

class AddImmediate(Instruction):
    pass

class JumpRegister(Instruction):
    pass
            
class LoadImmediate(Instruction):
    pass

class LoadWord(Instruction):
    pass

class StoreWord(Instruction):
    pass

class Subtract(Instruction):
    pass

class Xor(Instruction):
    pass

class MIPSVisitor:
    
    def __init__(self, dotdata, dottext):
        self.dotdata = dotdata
        self.dottext = dottext
        self.function_context = False
    
    def get_format(self):
        output = ".data"
        for data in self.dotdata:
            output = f'{output}{self.visit(data)}'
        
        output = f'{output}\n\n.text'
        for instruction in self.dottext:
            output = f'{output}{self.visit(instruction)}'
        return output
    
    @visitor.on('node')
    def visit(self, node):
        pass
    
    @visitor.when(Asciiz)
    def visit(self, node):
        return f'\n{node.name}: .asciiz "{node.string}"'
    
    @visitor.when(Word)
    def visit(self, node):
        return f'\n{node.name}:\t.word {node.value}'
    
    @visitor.when(Type)
    def visit(self, node):
        output = f'\n\ntype_{node.name}:'
        
        for _ in node.attributes:
            output += f'\n\t.word 0'
            
        for meth in node.methods:
            output += f'\n\t.word {meth[1]}'
            
        return output

    @visitor.when(Function)
    def visit(self, node):
        output = f'\n\n{node.name}:'
        self.function_context = True
        
        for instr in node.instructions:
            output += self.visit(instr)
        
        self.function_context = False
        return output

    @visitor.when(AddImmediate)
    def visit(self, node):
        tab = '\t' if self.function_context else ''
        return f'\n{tab}addi\t{node.first}, {node.second}, {node.third}'
    
    @visitor.when(JumpRegister)
    def visit(self, node):
        tab = '\t' if self.function_context else ''
        return f'\n{tab}jr  \t{node.first}'
    
    @visitor.when(LoadImmediate)
    def visit(self, node):
        tab = '\t' if self.function_context else ''
        return f'\n{tab}li  \t{node.first}, {node.second}'
    
    @visitor.when(LoadWord)
    def visit(self, node):
        tab = '\t' if self.function_context else ''
        return f'\n{tab}lw  \t{node.first}, {node.second}'
    
    @visitor.when(StoreWord)
    def visit(self, node):
        tab = '\t' if self.function_context else ''
        return f'\n{tab}sw  \t{node.first}, {node.second}'
    
    @visitor.when(Subtract)
    def visit(self, node):
        tab = '\t' if self.function_context else ''
        return f'\n{tab}sub \t{node.first}, {node.second}'
    
    @visitor.when(Xor)
    def visit(self, node):
        tab = '\t' if self.function_context else ''
        return f'\n{tab}xor \t{node.first}, {node.second}, {node.third}'