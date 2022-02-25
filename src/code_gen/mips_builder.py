from atexit import register
from email.quoprimime import body_length
import enum
from operator import le

from soupsieve import select
import cmp.visitor as visitor
import cmp.cil as cil
import random

import mips_nodes as mips



#type_info offsets
TYPENAME_OFFSET = 0
FUNCTION_OFFSET = 4
RA_OFFSET = 4

FP_ARGS_DISTANCE = 3 # how far finishes $fp from arguments in method call
FP_LOCALS_DISTANCE = 0 # how far finishes $fp from localvars in method call

#temporary registers
t0 = "$t0"
t1 = "$t1"
t2 = "$t2"
t3 = "$t3"
t4 = "$t4"
t5 = "$t5"
t6 = "$t6" # convenios
t7 = "$t7" # convenios
t8 = "$t8" 
t9 = "$t9" 

#Arguments Registers
a0 = "$a0"
a1 = "$a1"
a2 = "$a2"
a3 = "$a3"

#frame pointer
fp = "$fp"
#stack pointer
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

class MemoryManager:
    def __init__(self):
        self.all_reg = [t0,t1,t2,t3,t4,t5,t6,t7,t8,t9]
        self.used_reg = []
        self.stored = []
        
    def get_unused_reg(self):
        unused = list(set(self.all_reg) - set(self.used_reg)) + list(set(self.used_reg) - set(self.all_reg))
        reg = random.choice(unused)     
        self.used_reg.append(reg)
        return reg
    
    def clean(self):
        self.used_reg = self.stored
        self.stored = []
        
    def save(self):
        self.stored = self.used_reg.copy()
        

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
        self.main_procedure = mips.ProcedureNode("main")
        self.current_procedure = self.main_procedure
        self.text = [self.main_procedure]
        self.data = []
        self.params = []
        self.locals = []
        self.types = {}
        self.memo = MemoryManager()
    
    
    def get_dir_in_memo(self,x):
        if x in self.locals:
            index = self.locals.index(x)
            return -4*index
        elif x in self.params:
            index = self.params.index(x)
            return (4*index)+4
    
    def register_instruction(self, instruction_type, *args):
        instruction = instruction_type(*args)
        self.current_procedure.instructions.append(instruction)    
        
    def register_data(self,data_type,*args):
        data = data_type(*args)
        self.data.append(data)
      
        
    def register_push(self, reg):
        self.register_instruction(mips.StoreWordNode, reg, 0, sp)
        self.register_instruction(mips.AddiNode, sp, sp, -4)

    def register_pop(self, reg):
        self.register_instruction(mips.LoadWordNode, reg, 4, sp)
        self.register_instruction(mips.AddiNode, sp, sp, 4)    
    
    
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
        
        self.types[node.name] = node
        #for func in node.methods:
        values = [-1]*(len(node.methods)+1) 
        self.register_data(mips.DataTypeNode,'.word',node.name,values)
        self.register_data(mips.DataTypeNode, f'{node.name}_cname','.asciiz', [f'"{node.name}"'])
        
        
        #Filling type type info
        self.register_instruction(mips.CommentNode(f"Filling {node.name} VT"))
        self.register_instruction(mips.LoadAddress,t0,node.name)
        self.register_instruction(mips.LoadAddress,t1,f'{node.name}_cname')
        
        self.register_instruction(mips.StoreWordNode,t1,TYPENAME_OFFSET,t0) 
        
        #Filling type VT
        for i,func in enumerate(node.methods):
            offset = FUNCTION_OFFSET*i
            self.register_instruction(mips.LoadAddress,t1,func.name)
            self.register_instruction(mips.StoreWordNode,t1,offset,t0)
            
    @visitor.when(cil.DataNode)
    def visit(self, node):
        self.register_data(mips.DataTypeNode,'.ascii',node.vname,[node.value])

    @visitor.when(cil.LocalNode)
    def visit(self,node):
        self.memo.save()
        reg = self.memo.get_unused_reg()
        self.register_instruction(mips.LoadAddress,reg,node.name)
        self.register_instruction(mips.StoreWordNode,reg,0,sp)
        
        self.register_instruction(mips.AddiNode,sp,sp,-4)
        self.locals.append(node.name)
        self.memo.clean()
        
    @visitor.when(cil.ParamNode)
    def visit(self,node):
        self.memo.save()
        reg = self.memo.get_unused_reg()
        
        self.params.append(node.name)
        
        self.register_instruction(mips.LoadInmediate,reg,node.name)
        self.register_instruction(mips.StoreWordNode,reg,len(self.params)*4,fp)
        
        self.memo.clean()
        
    @visitor.when(cil.ArgNode)                                          
    def visit(self,node):
        self.memo.save()
        reg = self.memo.get_unused_reg()
        
        dir = self.get_dir_in_memo(node.name)
        self.register_instruction(mips.LoadWordNode,reg,dir,fp)
        
        self.register_instruction(mips.StoreWordNode,reg,0,sp)
        
        self.register_instruction(mips.AddiNode,sp,sp,4)
        
        self.memo.clean()
        
        
                            
        
        
    @visitor.when(cil.FunctionNode)
    def visit(self,node):
        self.current_procedure = mips.ProcedureNode(node.name)

        self.register_instruction(mips.CommentNode,"Pushing $ra")
        self.register_push(ra)

        self.register_instruction(mips.CommentNode,"Saving $fp")
        self.register_instruction(mips.MoveNode, fp, sp)
        
        self.register_comment("Reserving space for locals")
        self.register_instruction(mips.AddiNode, sp, sp, -4*len(node.localvars))                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 

        self.register_instruction(mips.CommentNode("Executing instructions"))
        for inst in node.instructions:
            self.visit(inst)
            

        self.register_instruction(mips.CommentNode("Restoring saved $ra"))
        self.register_instruction(mips.LoadWordNode, ra, RA_OFFSET, fp)#stored $ra
       

        self.register_comment("Restoring saved $fp")
        self.register_instruction(mips.LoadWordNode, fp, OLD_FP_OFFSET, fp)#stored (old)$fp

        AR = 4*(len(node.localvars) + len(node.arguments) + 2)
        self.register_instruction(mips.CommentNode("Cleaning stack after call"))
        self.register_instruction(mips.AddiNode, sp, sp, AR)
        
        self.register_instruction(mips.CommentNode("Return jump"))
        self.register_instruction(mips.JumpRegister, ra)
        

        self.text.append(self.current_procedure)    
        
  
    @visitor.when(cil.LoadNode)
    def visit(self,node):
        self.memo.save()
        reg = self.memo.used_reg()
        
        if isinstance(node.msg,int):
            self.register_instruction(mips.LoadInmediate,reg,node.msg)
        else:
            self.register_instruction(mips.LoadAddress,reg,node.msg)
        
        
        dir = self.get_dir_in_memo(node.dest)
        self.register_instruction(mips.StoreWordNode,reg,dir,fp)
        self.memo.clean()
    
        
        
    @visitor.when(cil.ReturnNode)
    def visit(self):
        pass
            
    @visitor.when(cil.GotoNode)
    def visit(self,node):
        self.register_instruction(mips.UnconditionalJumpNode,node.label)
        
    @visitor.when(cil.GotoIfNode)
    def visit(self,node):
        pass
    
    @visitor.when(cil.AllocateNode)
    def visit(self,node):
        _size = (len(self.types[node.type].attributes)+1)*4
        self.register_instruction(mips.LoadInmediate,v0,9)
        self.register_instruction(mips.LoadInmediate,a0,_size)
        self.register_instruction(mips.SyscallNode)
        
        dir = self.get_dir_in_memo(node.dest)
        
        self.register_instruction(mips.StoreWordNode,v0,dir,fp)        
        
        self.memo.clean()
        
    
    
    
    @visitor.when(cil.AssignNode)
    def visit(self,node):
        self.save()
        
        reg = self.memo.get_unused_reg()
        
        source_dir = self.get_dir_in_memo(node.source)
        dest_dir = self.get_dir_in_memo(node.dest)
        
        self.register_instruction(mips.LoadWordNode,reg,source_dir,fp)
        
        self.register_instruction(mips.StoreWordNode,reg,dest_dir,fp)

        self.memo.clean()        
        
        
        
    
    @visitor.when(cil.PlusNode)
    def visit(self,node):
        self.save()
        
        reg1 = self.memo.get_unused_reg()
        reg2 = self.memo.get_unused_reg()
        reg3 = self.memo.get_unused_reg()
        
        self.register_instruction(mips.LoadInmediate,reg1,node.left)
        self.register_instruction(mips.LoadInmediate,reg2,node.right)
        
        self.register_instruction(mips.AddNode,reg3,reg1,reg2)
        
        dir = self.get_dir_in_memo(node.dest)
        self.register_instruction(mips.StoreWordNode,reg3,dir,fp)
        
        self.memo.clean()
    
    @visitor.when(cil.MinusNode)
    def visit(self,node):
        self.save()
        
        reg1 = self.memo.get_unused_reg()
        reg2 = self.memo.get_unused_reg()
        reg3 = self.memo.get_unused_reg()
        
        self.register_instruction(mips.LoadInmediate,reg1,node.left)
        self.register_instruction(mips.LoadInmediate,reg2,node.right)
        
        self.register_instruction(mips.SubNode,reg3,reg1,reg2)
        
        dir = self.get_dir_in_memo(node.dest)
        self.register_instruction(mips.StoreWordNode,reg3,dir,fp)
        
        self.memo.clean()
        
    @visitor.when(cil.TypeOfNode)
    def visit(self,node):
        self.memo.save()
        
        reg1 = self.get_dir_in_memo()
        reg2 = self.get_dir_in_memo()
        
        
        
    