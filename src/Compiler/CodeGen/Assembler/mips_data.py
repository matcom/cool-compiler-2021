from CodeGen.Assembler.mips_instructions import *

# Registers
t_REGISTERS = ['$t0', '$t1', '$t2', '$t3', '$t4', '$t5', '$t6', '$t7', '$t8', '$t9']  #temporary (not preserved across call) 
s_REGISTERS = ['$s0', '$s1', '$s2', '$s3', '$s4', '$s5', '$s6', '$s7'] #saved temporary (preserved across call)
a_REGISTERS = ['$a0', '$a1', '$a2', '$a3'] # arguments
v_REGISTERS = ['$v0', '$v1'] #expression evaluation and results of a function
zero_REGISTER = '$zero' #constant 0
fp_REGISTER = '$fp' #frame pointer
sp_REGISTER = '$sp' #stack pointer
ra_REGISTER = '$ra' #return address (used by function call)
gp_REGISTER = '$gp' #pointer to global area

INTERNAL = "_INTERNAL"
INTERNAL_METHOD = "_INTERNAL_METHOD_"
INTERNAL_TYPE = "_INTERNAL_TYPE"

class Node:
    pass

class Label(Node):
    def __init__(self, label):
        self.label = label
    def __mips__(self):
        return '{}:'.format(self.label)

class Asciiz(Node):
    def __init__(self, name, string):
        self.name = name
        self.string = string
    def __mips__(self) -> str:
        return '\n{}: .asciiz "{}"'.format(self.name, self.string)

class Word(Node):
    def __init__(self, name, value):
        self.name = name
        self.value = value
    def __mips__(self) -> str:
         return '\n{}: .word {}'.format(self.name, self.string)


class Type(Node):
    def __init__(self, name, parent, attributes, methods):
        self.data = name
        self.parent = parent
        self.methods = methods
        self.attributes = attributes
    
    def __mips__(self):
        output = f'\n\ntype_{self.data.value}_methods:'
        
        for meth in self.methods:
            output += f'\n\t.word {meth[1]}'
        
        assigment = 'ref_assigment'
        equal = 'ref_equal'
        
        if self.data.value in ['Int', 'Bool']:
            assigment = 'val_assigment'
            equal = 'val_equal'
        elif self.data.value == 'String':
            assigment = 'str_assigment'
            equal = 'str_equal'        
        
        output += f'\n\ntype_{self.data.value}:'
        output += f'\n\t.word {4 * (len(self.attributes)+1)}'
        output += f'\n\t.word type_{self.data.value}_methods'
        output += f'\n\t.word {self.data.name}'
        output += f'\n\t.word {assigment}'
        output += f'\n\t.word {equal}'
        
        if self.parent is None:
            output += f'\n\t.word 0'
        else:
            output += f'\n\t.word type_{self.parent}'
        
        return output

class Function(Node):
    def __init__(self, name, instructions):
        self.name = name
        self.instructions =  instructions
    
    def __mips__(self):
        output = f'\n\n{self.name}:'
        
        for instr in self.instructions:
            output += f'\n\t{instr}'
        
        return output

