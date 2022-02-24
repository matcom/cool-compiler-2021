from atexit import register
from email.quoprimime import body_length
import cmp.visitor as visitor
import cmp.cil as cil

import mips_nodes as mips

t0 = "$t0"
t1 = "$t1"
t2 = "$t2"
t3 = "$t3"
t6 = "$t6" # convenios
t7 = "$t7" # convenios
a0 = "$a0"
a1 = "$a1"
fp = "$fp"
sp = "$sp"
ra = "$ra"
lo = "lo"
hi = "hi"
v0 = "$v0"
s0 = "$s0"
s1 = "$s1"
s2 = "$s2"
s3 = "$s3"
zero = "$zero"

#type_info offsets
TYPENAME_OFFSET = 0
PARENT_OFFSET = 4
SIZE_OFFSET = 8


SYSCALL_PRINT_INT = 1
SYSCALL_PRINT_STR = 4
SYSCALL_READ_INT = 5
SYSCALL_READ_STR = 8
SYSCALL_SBRK = 9
SYSCALL_EXIT = 10


class MIPSBuilder:
    def __init__(self,errors,cil_ast):
        self.mips_code = ""
        self.cil_ast = cil_ast
        self.cil_types = cil_ast.types
        self.cil_code = cil_ast.code
        self.cil_data = cil_ast.data
        self.main_procedure = mips.ProcedureNode("main")
        self.current_procedure = self.main_procedure
        self.text = [self.main_procedure]
        self.data = []
    
    def register_instruction(self, instruction_type, *args):
        instruction = instruction_type(*args)
        self.current_procedure.instructions.append(instruction)    
        
    def register_data(self,data_type,*args):
        data = data_type(*args)
        self.data.append(data)    
    
    @visitor.on("node")
    def visit(self, node=None):
        pass
    
    @visitor.when(cil.ProgramNode)
    def visit(self, node):
        for type in node.types:
            self.visit(type)
            
                
        for str_data in node.data:
            self.visit(str_data)
        
        for instruction in node.code:
            self.visit(instruction)
        
        
        return mips.ProgramNode(self.data,self.text)
        

    @visitor.when(cil.TypeNode)
    def visit(self, node):
        
        #for func in node.methods:
        values = [-1]*(len(node.methods)+1) 
        self.register_data(mips.DataTypeNode,'.word',node.name,values)
        self.register_data(mips.DataTypeNode, f'{node.name}_cname','.asciiz', [f'"{node.name}"'])
        
        
        #Filling type VT
        self.register_instruction(mips.CommentNode(f"Filling {node.name} VT"))
        self.register_instruction(mips.LoadAddress(t0,node.name))
        
        
        
        
        