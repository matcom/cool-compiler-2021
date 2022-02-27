import cmp.visitor as visitor
from .spim_scope import *
from .ast_CIL import *

WSIZE = 4 # word size in bytes

class MIPSCodegen:
    def __init__(self, scope):
        self.scope = scope
        self.code = ""
        self.tabs = ''
        self.main = True

    # =================== Utils ========================
    def add_line(self,line):
        self.code += self.tabs + line + '\n'

    def set_tabs(self,n):
        self.tabs = '\t' * n

    def gen_push(self,src):
        self.add_line(f'# push {src} to the stack')
        self.add_line(f'sw {src}, 0($sp)')
        self.add_line(f'addi $sp $sp -{WSIZE}')
       
        self.add_line('')

    def gen_pop(self,dst):
        self.add_line(f'# pop the top of the stack to {dst}')
        self.add_line(f'addi $sp $sp {WSIZE}')
        self.add_line(f'lw {dst}, 0($sp)')
        self.add_line('')

    @visitor.on('node')
    def visit(self, node, frame):
        pass

    @visitor.when(CILProgramNode)
    def visit(self, node: CILProgramNode, frame):
        for t in node.types:
            self.visit(t, frame)
    
        self.set_tabs(1)
        self.add_line(".data")
        self.set_tabs(0)
        self.add_line("ObjectErrorMessage : .asciiz \"Program was halted\"")

        self.set_tabs(1)
        self.add_line(".data")
        self.set_tabs(0)
        self.add_line("IO_Buffer : .space 1001")
        for d in node.data:
            self.visit(d, frame)

        for f in node.functions:
            self.visit(f, frame)
            self.add_line('')

        with open('./code_generator/mips_built_in.txt') as file:
            self.code += file.read()

    @visitor.when(CILTypeNode)
    def visit(self, node: CILTypeNode, frame):
        # place the type name as a string in static data
        self.set_tabs(1)
        self.add_line(".data")
        self.set_tabs(0)
        t = self.scope.types[node.id]
        methods_str = ' '.join(m.function_id for m in node.methods)
        assert len(node.methods) == len(t.methods_offset)
        self.add_line(f"_{node.id}: .asciiz \"{node.id}\"")
        self.add_line("\t.data")
        self.add_line("\t.align 4")
        self.add_line(f"{node.id}: .word {t.size} _{node.id} {methods_str}")
        self.add_line('')

    @visitor.when(CILDataNode)
    def visit(self, node: CILDataNode, frame):
        self.set_tabs(1)
        self.add_line(".data")
        self.set_tabs(0)
        self.add_line(f"{node.id}: .asciiz {node.text}")
        self.add_line('')
        
    @visitor.when(CILFuncNode)
    def visit(self, node: CILFuncNode, frame):
        frame = self.scope.functions[node.id]
        self.set_tabs(1)
        self.add_line('.text')
        self.set_tabs(0)
        self.add_line(f'{node.id}:')
        self.set_tabs(1)
        self.add_line('# save the return address and frame pointer')
        self.gen_push('$ra') # Save the return address
        self.gen_push('$fp') # Save the frame pointer
        
        
        self.add_line('# update the frame pointer and allocate the frame in the stack')  
        self.add_line(f'move $fp $sp') # Update the frame pointer to the top of the stack

        # Allocate frame size in memory
        self.add_line(f'subu $sp $sp {frame.size}')
        self.add_line('')

        for i in node.instructions:
            self.visit(i, frame)
        
        self.add_line(f'# restore the stack pointer, frame pointer y return address')
        self.add_line(f'addu $sp $sp {frame.size}')
        self.gen_pop('$fp')
        self.gen_pop('$ra')

        if self.main:
            self.add_line('li $v0, 10')
            self.add_line('syscall')
            self.main = False
        else:
            self.add_line('jr $ra')

    @visitor.when(CILAttributeNode)
    def visit(self, node: CILAttributeNode, frame):
        pass

    @visitor.when(CILMethodNode)
    def visit(self, node: CILMethodNode, frame):
        pass

    @visitor.when(CILParamNode)
    def visit(self, node: CILParamNode, frame):
        pass

    @visitor.when(CILLocalNode)
    def visit(self, node: CILParamNode, frame):
        pass

    # ==================== Instructions ========================
    @visitor.when(CILInstructionNode)
    def visit(self, node, frame):
        pass

    @visitor.when(CILAssignNode)
    def visit(self, node: CILAssignNode, frame: ProcCallFrame):
        # Adds the code for calculating the expresion and stores the address for the value in register
        self.add_line(f'# assign (add here the expr.to_string) to {node.id.lex}')
        register = self.visit(node.expr, frame)
        id_addr = frame.get_addr(node.id.lex)
        self.add_line(f'sw {register}, {id_addr}')
        self.add_line(f'')

    @visitor.when(CILSetAttributeNode)
    def visit(self, node: CILSetAttributeNode, frame): 
        self.add_line(f'# Setting value of the attribute {node.attr.lex} in the instance {node.id.lex} to {node.var.lex}')
        inst_addr = frame.get_addr(node.id.lex)
        t = self.scope.types[node.type] # Change this for dynamic type? Not needed because the attributes are always declared in the same order in inhereted classes
        register1 = '$v1'
        register2 = '$s2'
        attr_addr = t.get_attr_addr(node.attr.lex, register1) #
        value_addr = self.visit(node.var, frame)
        self.add_line(f'move {register2}, {value_addr}')
        self.add_line(f'lw {register1}, {inst_addr}') 
        self.add_line(f'sw {register2}, {attr_addr}') 
        self.add_line('')

    @visitor.when(CILArgNode)
    def visit(self, node: CILArgNode, frame):
        frame.push_arg(node.var) # keep track of the args to be pass to the funcion to get the instance to bind the dynamic type
        value_addr = frame.get_addr(node.var.lex)
        self.add_line(f'lw $v0, {value_addr}')
        self.gen_push('$v0')
     
    @visitor.when(CILIfGotoNode)
    def visit(self, node: CILIfGotoNode, frame):
        value_addr = frame.get_addr(node.var.lex)
        self.add_line(f'lw $t1, {value_addr}')
        self.add_line(f'lw $t0, 4($t1)')
        self.add_line(f'bne $t0, $zero, {node.label.id}')
        
    @visitor.when(CILGotoNode)
    def visit(self, node: CILGotoNode, frame):
        self.add_line(f'j {node.label.id}')

    @visitor.when(CILLabelNode)
    def visit(self, node: CILLabelNode, frame):
        self.add_line(f'{node.id}:')

    @visitor.when(CILReturnNode)
    def visit(self, node: CILReturnNode,frame):
        register0 = '$v0'
        self.add_line(f'# return the value of the function in the register {register0}')
        register1 = self.visit(node.var, frame)
        self.add_line(f'move {register0}, {register1}')
        self.add_line('')


    @visitor.when(CILExpressionNode)
    def visit(self, node: CILExpressionNode,frame):
        pass

    @visitor.when(CILBinaryOperationNode)
    def visit(self, node: CILBinaryOperationNode, frame):
        pass

    @visitor.when(CILGetAttribute)
    def visit(self, node: CILGetAttribute, frame):
        var_addr = frame.get_addr(node.var.lex)
        register0 = '$v0'
        register1 = '$v1'
        t = self.scope.types[node.type]
        attr_addr = t.get_attr_addr(node.attr.lex, register1)
       
        # the memory of at var_addr contains the address to the instance of T
        # move the instance address to the register
        self.add_line(f'lw {register1}, {var_addr}')
        self.add_line(f'lw {register0}, {attr_addr}')
        return register0

    @visitor.when(CILAllocateNode)
    def visit(self, node: CILAllocateNode, frame):
        register0 = '$v0'
        register1 = '$a0'
        t = self.scope.types[node.type.lex]

        self.add_line(f'li {register1}, {t.size}')
        self.add_line(f'li {register0}, 9')
        self.add_line(f'syscall')
        self.add_line(f'la {register1}, {node.type.lex}')
        self.add_line(f'sw {register1},  0({register0})') # Place the dynamic type of the instance in memory
        return register0

    @visitor.when(CILTypeOfNode) # Get the dynamic type of an instance
    def visit(self, node: CILTypeOfNode, frame):
        register0 = '$v0'
        register1 = '$v1'
        var_addr = frame.get_addr(node.var.lex)
        # register0 points to the heap
        self.add_line = ('lw {register1}, {var_addr}')
        self.add_line = ('lw {register0}, {register1}')
        return register0

    @visitor.when(CILCallNode) # I don't think this is necessary
    def visit(self, node: CILCallNode, frame):
        register0 = '$v0'
        self.add_line(f'jal {node.func}')
        for a in frame.arg_queue:
            self.gen_pop('$v1')
        frame.clear_args() # clear arguments for the new function
        return register0

    @visitor.when(CILVCallNode)
    def visit(self, node: CILVCallNode, frame):
        # the instance of type T is always the first argument to be passed to the function
        self.add_line(f'# calling the method {node.func} of type {node.type}')
        instance = frame.arg_queue[0]
        instance_addr = self.visit(instance, frame) # load into a register the address of the instance in the heap

        register0 = '$v0'
        # register0 has the dynamic type address of the instance 
        # since every instance stores its type in the first word of the allocated memory
        self.add_line(f'lw {register0}, 0({instance_addr})')

        # use the information of the static type to get the location of the method in memory
        t = self.scope.types[node.type]
        try:
            method_addr = t.get_method_addr(node.func, register0)
        except:
            print(node.func)
            print(t.id)
            print('shdglsdglsjdg0000000000000')
            print(t.methods_offset)
        
        self.add_line(f'lw $v1, {method_addr}')
        self.add_line(f'jal $v1') # calls the method and by convention methods return in $v0
        for a in frame.arg_queue:
            self.gen_pop('$v1')
        frame.clear_args() # clear arguments for the new function

        return '$v0'

    @visitor.when(CILLoadNode)
    def visit(self, node: CILLoadNode, frame):
        self.add_line(f'#load the string {node.var}')
        register = '$v0'
        self.add_line(f'li $a0, 8')
        self.add_line(f'li $v0, 9')
        self.add_line(f'syscall')
        self.add_line(f'la $v1, String')
        self.add_line(f'sw $v1, 0($v0)')
        self.add_line(f'la $v1, {node.var}')
        self.add_line(f'sw $v1, 4($v0)')
        return register


    @visitor.when(CILNumberNode)
    def visit(self, node: CILNumberNode, frame):
        register = '$v0'
        self.add_line(f'# Creating Int instance for atomic {node.lex}')
        self.add_line(f'li $a0, 8')
        self.add_line(f'li $v0, 9')
        self.add_line(f'syscall')

        self.add_line(f'la $t0, Int')
        self.add_line(f'li $t1, {node.lex}')
        self.add_line(f'sw $t0, 0($v0)')
        self.add_line(f'sw $t1, 4($v0)')
        self.add_line(f'')
        return register

    @visitor.when(CILVariableNode)
    def visit(self, node: CILVariableNode, frame):
        self.add_line(f'#load the variable {node.lex}')
        register = '$v0'
        var_addr = frame.get_addr(node.lex)
        self.add_line(f'lw {register}, {var_addr}')
        return register

    @visitor.when(CILPlusNode)
    def visit(self, node: CILPlusNode, frame):
        register0 = '$v0'
        self.add_line(f'# computes the sum of (node.left.to_string) and (node.right.to_string) and stores it at {register0}')
        self.visit(node.left, frame) # in $v0 is the address of the Int instance 
        self.add_line(f'lw $t0, 4($v0)')
        self.gen_push('$t0')
        self.visit(node.right, frame)
        self.gen_pop('$t0')
        self.add_line(f'lw $t1, 4($v0)')
        self.add_line(f'add $t0, $t0, $t1')
        self.add_line(f'li $a0, 8')
        self.add_line(f'li $v0, 9')
        self.add_line(f'syscall')
        self.add_line(f'la $t1, Int')
        self.add_line(f'sw $t1, 0($v0)')
        self.add_line(f'sw $t0, 4($v0)')
        return register0

    @visitor.when(CILMinusNode)
    def visit(self, node: CILMinusNode, frame):
        register0 = '$v0'
        self.add_line(f'# computes the sub of (node.left.to_string) and (node.right.to_string) and stores it at {register0}')
        self.visit(node.left, frame) # in $v0 is the address of the Int instance 
        self.add_line(f'lw $t0, 4($v0)')
        self.gen_push('$t0')
        self.visit(node.right, frame)
        self.add_line(f'lw $t1, 4($v0)')
        self.gen_pop('$t0')
        self.add_line(f'sub $t0, $t0, $t1')
        self.add_line(f'li $a0, 8')
        self.add_line(f'li $v0, 9')
        self.add_line(f'syscall')
        self.add_line(f'la $t1, Int')
        self.add_line(f'sw $t1, 0($v0)')
        self.add_line(f'sw $t0, 4($v0)')
        return register0

    
    @visitor.when(CILStarNode)
    def visit(self, node: CILStarNode, frame):
        register0 = '$v0'
        register1 = '$v1'
        self.add_line(f'# computes the multiplication of (node.left.to_string) and (node.right.to_string) and stores it at {register0}')
        self.visit(node.left, frame)
        self.add_line(f'move {register1}, {register0}')
        self.visit(node.right, frame)
        self.add_line(f'mult {register0}, {register0}')
        self.add_line(f'mflo {register0}')
        return register0

    @visitor.when(CILDivNode)
    def visit(self, node: CILDivNode, frame):
        register0 = '$v0'
        register1 = '$v1'
        self.add_line(f'# computes the quotient of (node.left.to_string) and (node.right.to_string) and stores it at {register0}')
        self.visit(node.left, frame)
        self.add_line(f'move {register1}, {register0}')
        self.visit(node.right, frame)
        self.add_line(f'div {register1}, {register0}')
        self.add_line(f'mflo {register0}')
        return register0

    @visitor.when(CILLessNode)
    def visit(self, node: CILLessNode, frame):
        self.visit(node.left, frame)
        self.add_line(f'move $t1, $v0') # get the address to the left Int instance 
        self.add_line(f'lw $t1, 4($t1)') # get the value of the instance

        self.visit(node.right, frame)
        self.add_line(f'move $t2, $v0') # get the address to the right Int instance 
        self.add_line(f'lw $t2, 4($t2)') # get the value of the instance

        
        self.add_line(f'slt $t3, $t1, $t2') # l < r ?

        self.add_line(f'la $t4, Bool')
        self.add_line(f'li $a0, 8')
        self.add_line(f'li $v0, 9')
        self.add_line('syscall')
        self.add_line(f'sw $t4, 0($v0)')
        self.add_line(f'sw $t3, 4($v0)')
        return '$v0'

    @visitor.when(CILElessNode)
    def visit(self, node: CILElessNode, frame):
        self.visit(node.left, frame)
        self.add_line(f'move $t1, $v0') # get the address to the left Int instance 
        self.add_line(f'lw $t1, 4($t1)') # get the value of the instance

        self.visit(node.right, frame)
        self.add_line(f'move $t2, $v0') # get the address to the right Int instance 
        self.add_line(f'lw $t2, 4($t2)') # get the value of the instance

        
        self.add_line(f'slt $t4, $t2, $t1')  # r < l?
        self.add_line(f'li $t3, 1')
        self.add_line(f'xor $t3, $t3, $t4')
        self.add_line(f'andi $t3, $t3, 0x01') # get the last bit

        self.add_line(f'la $t4, Bool')
        self.add_line(f'li $a0, 8')
        self.add_line(f'li $v0, 9')
        self.add_line('syscall')
        self.add_line(f'sw $t4, 0($v0)')
        self.add_line(f'sw $t3, 4($v0)')
        return '$v0'

    @visitor.when(CILEqualsNode)
    def visit(self, node: CILEqualsNode, frame):
        self.visit(node.left, frame)
        self.gen_push('$v0')
        self.visit(node.right, frame)
        self.gen_push('$v0')
        self.add_line('jal compare')
        self.gen_pop('$t0')
        self.gen_pop('$t0')
        return '$v0'
        


        








        

        


        
        
        



        
