from utils.code_generation.mips.AST_MIPS import *
import cmp.visitor as visitor
from utils.code_generation.mips.AST_MIPS import mips_ast as nodes
from utils.code_generation.mips.utils_mips import *


class PrintMIPS:

    @visitor.on('node')
    def visit(self, node):
        pass

    @visitor.when(nodes.ProgramNode)
    def visit(self, node):
        data_section_header = "\t.data"
        static_strings = '\n'.join([self.visit(string_const)
                                   for string_const in node.data])

        names_table = f'{"type_name_table"}:\n' + \
            "\n".join(
                [f"\t.word\t{tp.string_name_label}" for tp in node.types])
        proto_table = f'{"proto_table"}:\n' + \
            "\n".join([f"\t.word\t{tp.label}_proto" for tp in node.types])

        types = "\n\n".join([self.visit(tp) for tp in node.types])

        code = "\n".join([self.visit(func) for func in node.functions])
        return f'{data_section_header}\n{static_strings}\n\n{names_table}\n\n{proto_table}\n\n{types}\n\t.text\n\t.globl main\n{code}\n\n{mips_static_code()}'

    @visitor.when(nodes.FunctionNode)
    def visit(self, node):
        instr = [self.visit(instruction) for instruction in node.instructions]
        instr2 = [inst for inst in instr if type(inst) == str]
        instructions = "\n\t".join(instr2)
        return f'{node.label}:\n\t{instructions}'

    @visitor.when(nodes.AddNode)
    def visit(self, node):
        return f"add {self.visit(node.reg1)} {self.visit(node.reg2)} {self.visit(node.reg3)}"

    @visitor.when(nodes.SubNode)
    def visit(self, node):
        return f"sub {self.visit(node.reg1)} {self.visit(node.reg2)} {self.visit(node.reg3)}"

    @visitor.when(nodes.MultiplyNode)
    def visit(self, node):
        return f"mul {self.visit(node.reg1)} {self.visit(node.reg2)} {self.visit(node.reg3)}"

    @visitor.when(nodes.DivideNode)
    def visit(self, node):
        return f"div {self.visit(node.reg1)} {self.visit(node.reg2)}"

    @visitor.when(nodes.LabelNode)
    def visit(self, node):
        return f"{node.name}:"

    @visitor.when(nodes.ComplementNode)
    def visit(self, node):
        return f"not {self.visit(node.reg1)} {self.visit(node.reg2)}"

    @visitor.when(nodes.StringConst)
    def visit(self, node):
        return f'{node.label}: .asciiz "{node.string}"'

    @visitor.when(nodes.MoveNode)
    def visit(self, node):
        return f'move {self.visit(node.reg1)} {self.visit(node.reg2 )}'

    @visitor.when(nodes.LoadInmediateNode)
    def visit(self, node):
        return f'li {self.visit(node.reg)}, {self.visit(node.value)}'

    @visitor.when(nodes.LoadWordNode)
    def visit(self, node):
        return f'lw {self.visit(node.reg)}, {self.visit(node.addr)}'

    @visitor.when(nodes.SyscallNode)
    def visit(self, node):
        return 'syscall'

    @visitor.when(nodes.LoadAddressNode)
    def visit(self, node):
        return f'la {self.visit(node.reg)}, {self.visit(node.label)}'

    @visitor.when(nodes.StoreWordNode)
    def visit(self, node):
        return f'sw {self.visit(node.reg)}, {self.visit(node.addr)}'

    @visitor.when(nodes.JumpAndLinkNode)
    def visit(self, node):
        return f'jal {node.label}'

    @visitor.when(nodes.JumpRegisterAndLinkNode)
    def visit(self, node):
        return f'jal {self.visit(node.reg)}'

    @visitor.when(nodes.JumpRegisterNode)
    def visit(self, node):
        return f'jr {self.visit(node.reg)}'

    @visitor.when(nodes.AddInmediateNode)
    def visit(self, node):
        return f'addi {self.visit(node.dest)}, {self.visit(node.src)}, {self.visit(node.value)}'

    @visitor.when(nodes.AddInmediateUnsignedNode)
    def visit(self, node):
        return f"addiu {self.visit(node.dest)} {self.visit(node.src)} {self.visit(node.value)}"

    @visitor.when(nodes.AddUnsignedNode)
    def visit(self, node):
        return f"addu {self.visit(node.dest)} {self.visit(node.sum1)} {self.visit(node.sum2)}"

    @visitor.when(nodes.ShiftLeftLogicalNode)
    def visit(self, node):
        return f"sll {self.visit(node.dest)} {self.visit(node.src)} {node.bits}"

    @visitor.when(nodes.BranchOnNotEqualNode)
    def visit(self, node):
        return f"bne {self.visit(node.reg1)} {self.visit(node.reg2)} {node.label}"

    @visitor.when(nodes.JumpNode)
    def visit(self, node):
        return f"j {node.label}"

    @visitor.when(nodes.MoveFromLowNode)
    def visit(self, node):
        return f"mflo {self.visit(node.reg)}"

    @visitor.when(Register)
    def visit(self, node):
        return f'${node.name}'

    @visitor.when(LabelRelativeLocation)
    def visit(self, node):
        return f'{node.label} + {node.offset}'

    @visitor.when(RegisterRelativeLocation)
    def visit(self, node):
        return f'{node.offset}({self.visit(node.register)})'

    @visitor.when(MIPSType)
    def visit(self, node):
        methods = "\n".join(
            [f"\t.word\t {node.methods[k]}" for k in node.methods])
        dispatch_table = f"{node.label}_dispatch:\n{methods}"
        proto_begin = f"{node.label}_proto:\n\t.word\t{node.index}\n\t.word\t{node.size}\n\t.word\t{node.label}_dispatch"
        proto_attr = "\n".join(
            [f'\t.word\t{node._default_attributes.get(attr, "0")}' for attr in node.attributes])
        proto_finish = f"\t.word\t{-1}"
        proto = f"{proto_begin}\n{proto_attr}\n{proto_finish}" if proto_attr != "" else f"{proto_begin}\n{proto_finish}"

        return f'{dispatch_table}\n\n{proto}'

    @visitor.when(int)
    def visit(self, node):
        return str(node)

    @visitor.when(str)
    def visit(self, node):
        return node


def mips_static_code():
    return \
        local_vars() +\
        verify_obj() +\
        verify_obj_not_obj() +\
        verify_obj_is_obj() +\
        verify_obj_finish() +\
        concat() +\
        concat_size_alligned() +\
        concat_allign_size() +\
        concat_copy_first_cycle() +\
        concat_copy_second_cycle() +\
        concat_finish() +\
        copy() +\
        copy_cycle() +\
        copy_finish() +\
        eqs() +\
        eqs_eq() +\
        eqs_finish() +\
        eq_string() +\
        eq_string_cycle() +\
        eq_string_not_eq() +\
        eq_string_eq() +\
        eq_string_finish() +\
        extend_block() +\
        extend_block_extend() +\
        extend_block_finish() +\
        extend_heap() +\
        free_block() +\
        free_block_cycle_used_list() +\
        free_block_cycle_free_list() +\
        free_block_founded_prev() +\
        free_block_finish() +\
        get_gc() +\
        get_gc_cycle() +\
        get_gc_dfs() +\
        get_gc_outer_cycle() +\
        get_gc_extend() +\
        get_gc_free() +\
        get_gc_free_cycle() +\
        get_gc_free_cycle_free() +\
        get_gc_finish() +\
        get_gc_rec_extend() +\
        get_gc_rec_extend_attr_cycle() +\
        get_gc_rec_extend_string_obj() +\
        get_gc_rec_extend_finish() +\
        less_eq() +\
        less_eq_true() +\
        less_eq_finish() +\
        less() +\
        less_true() +\
        less_finish() +\
        lenx() +\
        len_cycle() +\
        len_finish() +\
        malloc() +\
        malloc_finish() +\
        malloc_cycle() +\
        malloc_search_finish() +\
        malloc_alloc_new_block() +\
        malloc_big_block() +\
        malloc_verify_valid_block() +\
        malloc_valid_block() +\
        malloc_first_valid_block() +\
        mem_manager_init() + \
        get_string() +\
        get_string_larger_block_cycle() +\
        get_string_reading() +\
        get_string_look_nl() +\
        get_string_zero_founded() +\
        get_string_nl_founded() +\
        get_string_nl_founded_alligned() +\
        get_string_no_nl() +\
        get_string_dup() +\
        get_string_extend_heap() +\
        get_string_last_block_cycle() +\
        get_string_last_block_founded() +\
        get_string_copy_prev() +\
        get_string_copy_cycle() +\
        get_string_copy_finish() +\
        get_string_finish() +\
        get_string_new_block() +\
        get_string_new_block_search_last() +\
        get_string_new_block_create() +\
        get_string_new_block_extended() +\
        divide_block() +\
        divide_block_same_size() +\
        divide_block_error_small() +\
        divide_block_finish() +\
        sub_string() +\
        sub_string_allign_size() +\
        sub_string_new_block() +\
        sub_string_copy_cycle() +\
        sub_string_finish() +\
        use_block() +\
        use_block_cycle() +\
        use_block_founded() +\
        use_block_finish()


# Mips labels

def local_vars():
    return '''
    
    alloc_size       = 2048
    free_list = 0
    header_size = 12
    header_size_slot = 0
    header_next_slot = 4
    header_reachable_slot = 8
    init_alloc_size = 28
    int_type = 0
    meta_data_obj_size = 4
    neg_header_size = -12
    new_line = 10
    obj_mark = -1
    obj_extended = -2
    reachable = 1
    state_size = 4
    stack_base = -4
    string_size_treshold = 1024
    string_type = 0
    total_alloc_size =  2060
    num_type = 0
    used_list = header_size\n\n'''


def verify_obj():
    return '''verify_obj:
                addiu $sp $sp -20
                sw $t0 0($sp)
                sw $t1 4($sp)
                sw $t2 8($sp)
                sw $t3 12($sp)
                sw $a0 16($sp)

                move $t0 $a0

                li $v0 9
                move $a0 $zero
                syscall

                addiu $t1 $v0 -4    

                
                blt $t0 $gp verify_obj_not_obj
                bgt $t0 $t1 verify_obj_not_obj
                lw $t2 0($t0)
                blt $t2 $zero verify_obj_not_obj
                la $t3 num_type
                lw $t3 0($t3)
                bge $t2 $t3 verify_obj_not_obj

                addiu $t0 $t0 4
                blt $t0 $gp verify_obj_not_obj
                bgt $t0 $t1 verify_obj_not_obj
                lw $t2 0($t0)   

                addiu $t0 $t0 8
                

                li $t3 meta_data_obj_size
                sub $t2 $t2 $t3 
                sll $t2 $t2 2
                addu $t0 $t0 $t2
                
                
                blt $t0 $gp verify_obj_not_obj
                bgt $t0 $t1 verify_obj_not_obj
                lw $t2 0($t0)
                beq $t2 obj_mark verify_obj_is_obj
                beq $t2 obj_extended verify_obj_is_obj\n\n'''


def verify_obj_not_obj():
    return '''verify_obj_not_obj:
                li $v0 0
                j verify_obj_finish\n\n'''


def verify_obj_is_obj():
    return '''verify_obj_is_obj:
                li $v0 1\n\n'''


def verify_obj_finish():
    return '''verify_obj_finish:
                lw $t0 0($sp)
                lw $t1 4($sp)
                lw $t2 8($sp)
                lw $t3 12($sp)
                lw $a0 16($sp)
                addiu $sp $sp 20

                jr $ra\n\n'''


def concat():
    return '''concat:
                addiu $sp $sp -24
                sw $t0 0($sp)
                sw $t1 4($sp)
                sw $t2 8($sp)
                sw $a0 12($sp)
                sw $a1 16($sp)
                sw $ra 20($sp)

                move $t0 $a0
                move $t1 $a1


                addiu $a0 $a2 1
                li $t2 4
                div $a0 $t2
                mfhi $a0
                bne $a0 $zero concat_allign_size
                addiu $a0 $a2 1\n\n'''


def concat_size_alligned():
    return '''concat_size_alligned:
                jal malloc
                move $t2 $v0
                j concat_copy_first_cycle\n\n'''


def concat_allign_size():
    return '''concat_allign_size:
                sub $t2 $t2 $a0
                add $a0 $a2 $t2
                addiu $a0 $a0 1
                j concat_size_alligned\n\n'''


def concat_copy_first_cycle():
    return '''concat_copy_first_cycle:
                lb $a0 0($t0)
                beq $a0 $zero concat_copy_second_cycle
                sb $a0 0($t2)
                addiu $t0 $t0 1
                addiu $t2 $t2 1
                j concat_copy_first_cycle\n\n'''


def concat_copy_second_cycle():
    return '''concat_copy_second_cycle:
                lb $a0 0($t1)
                beq $a0 $zero concat_finish
                sb $a0 0($t2)
                addiu $t1 $t1 1
                addiu $t2 $t2 1
                j concat_copy_second_cycle\n\n'''


def concat_finish():
    return '''concat_finish:
                sb $zero 0($t2)
                lw $t0 0($sp)
                lw $t1 4($sp)
                lw $t2 8($sp)
                lw $a0 12($sp)
                lw $a1 16($sp)
                lw $ra 20($sp)
                addiu $sp $sp 24

                jr $ra\n\n'''


def copy():
    return '''copy:
                addiu $sp $sp -16
                sw $a0 0($sp)
                sw $a1 4($sp)
                sw $a2 8($sp)
                sw $t0 12($sp)\n\n'''


def copy_cycle():
    return '''copy_cycle:
                beq $a2 $zero copy_finish
                lw $t0 0($a0)
                sw $t0 0($a1)
                addiu $a0 $a0 4
                addiu $a1 $a1 4
                addi $a2 $a2 -4
                j copy_cycle\n\n'''


def copy_finish():
    return '''copy_finish:
                lw $a0 0($sp)
                lw $a1 4($sp)
                lw $a2 8($sp)
                lw $t0 12($sp)
                addiu $sp $sp 16

                jr $ra\n\n'''


def eqs():
    return '''eqs:
                beq $a0 $a1 eqs_eq
                li $v0 0
                j eqs_finish\n\n'''


def eqs_eq():
    return '''eqs_eq:
                li $v0 1\n\n'''


def eqs_finish():
    return '''eqs_finish:
                jr $ra\n\n'''


def eq_string():
    return '''eq_string:
                addiu $sp $sp -16
                sw $t0 0($sp)
                sw $t1 4($sp)
                sw $t2 8($sp)
                sw $t3 12($sp)

                move $t0 $a0
                move $t1 $a1\n\n'''


def eq_string_cycle():
    return '''eq_string_cycle:
                lb $t2 0($t0)
                lb $t3 0($t1)
                bne $t2 $t3 eq_string_not_eq
                beq $t2 $zero eq_string_eq

                addiu $t0 $t0 1
                addiu $t1 $t1 1
                j eq_string_cycle\n\n'''


def eq_string_not_eq():
    return '''eq_string_not_eq:
                move $v0 $zero
                j eq_string_finish\n\n'''


def eq_string_eq():
    return '''eq_string_eq:
                li $v0 1\n\n'''


def eq_string_finish():
    return '''eq_string_finish:
                lw $t0 0($sp)
                lw $t1 4($sp)
                lw $t2 8($sp)
                lw $t3 12($sp)
                addiu $sp $sp 16

                jr $ra\n\n'''


def extend_block():
    return '''extend_block:
                addiu $sp $sp -16
                sw $t0 0($sp)
                sw $t1 4($sp)
                sw $t2 8($sp)
                sw $t3 12($sp)

                
                addiu $t0 $gp free_list     

                beq $t0 $a0 extend_block_finish  
                move $t0 $a0

                lw $t1 header_next_slot($t0)
                lw $t2 header_size_slot($t0)
                move $t3 $t2
                addiu $t2 $t2 header_size
                addu $t2 $t2 $t0
                beq $t2 $t1 extend_block_extend
                j extend_block_finish\n\n'''


def extend_block_extend():
    return '''extend_block_extend:
                lw $t2 header_size_slot($t1)
                addi $t2 $t2 header_size
                add $t2 $t2 $t3
                sw $t2 header_size_slot($t0)
                lw $t1 header_next_slot($t1)
                sw $t1 header_next_slot($t0)\n\n'''


def extend_block_finish():
    return '''extend_block_finish:
                lw $t0 0($sp)
                lw $t1 4($sp)
                lw $t2 8($sp)
                lw $t3 12($sp)
                addiu $sp $sp 16

                jr $ra\n\n'''


def extend_heap():
    return '''extend_heap:
                addiu $sp $sp -12
                sw $a0 0($sp)
                sw $a1 4($sp)
                sw $t0 8($sp)

                
                li $v0 9
                addiu $a0 $a1 header_size
                syscall
                
                
                move $t0 $a1 
                sw $t0 header_size_slot($v0)
                sw $zero header_next_slot($v0)
                sw $zero header_reachable_slot($v0)

               
                lw $t0, 0($sp)
                sw $v0 header_next_slot($t0)

                move $a0 $t0
                lw $a1 4($sp)
                lw $t0 8($sp)
                addiu $sp $sp 12

                jr $ra\n\n'''


def free_block():
    return '''free_block:
                addiu $sp $sp -28
                sw $t0 0($sp)
                sw $t1 4($sp)
                sw $t2 8($sp)
                sw $a0 12($sp)
                sw $ra 16($sp)
                sw $t3 20($sp)
                sw $t4 24($sp)

                move $t0 $a0

                addiu $t1 $gp free_list

                addiu $t3 $gp used_list\n\n'''


def free_block_cycle_used_list():
    return '''free_block_cycle_used_list:
                lw $t4 header_next_slot($t3)
                beq $t4 $t0 free_block_cycle_free_list
                move $t3 $t4
                j free_block_cycle_used_list\n\n'''


def free_block_cycle_free_list():
    return '''free_block_cycle_free_list:
                lw $t2 header_next_slot($t1)
                beq $t2 $zero free_block_founded_prev
                bge $t2 $t0 free_block_founded_prev
                move $t1 $t2
                j free_block_cycle_free_list\n\n'''


def free_block_founded_prev():
    return '''free_block_founded_prev:  
                lw $t4 header_next_slot($t0)
                sw $t4 header_next_slot($t3)
                
                
                sw $t2 header_next_slot($t0)
                sw $t0 header_next_slot($t1)\n\n'''


def free_block_finish():
    return '''free_block_finish:
    
                move $a0 $t0
                jal extend_block
                move $a0 $t1
                jal extend_block

                lw $t0 0($sp)
                lw $t1 4($sp)
                lw $t2 8($sp)
                lw $a0 12($sp)
                lw $ra 16($sp)
                lw $t3 20($sp)
                lw $t4 24($sp)
                addiu $sp $sp 28

                jr $ra\n\n'''


def get_gc():
    return '''get_gc:
                addiu $sp $sp -24
                sw $t0 0($sp)
                sw $t1 4($sp)
                sw $t2 8($sp)
                sw $t3 12($sp)
                sw $a0 16($sp)
                sw $ra 20($sp)

                li $t3 reachable    
                addiu $t0 $sp 20    
                lw $t1 stack_base($gp)  

                li $t2 1\n\n'''


def get_gc_cycle():
    return '''get_gc_cycle:

                addiu $t0 $t0 4
                beq $t0 $t1 get_gc_dfs      
                
                lw $a0 0($t0)
                jal verify_obj
                
                bne $v0 $t2 get_gc_cycle

                addiu $a0 $a0 neg_header_size
                sw $t3 header_reachable_slot($a0)
                
                j get_gc_cycle\n\n'''


def get_gc_dfs():
    return '''get_gc_dfs:
                addiu $t1 $gp used_list\n\n'''


def get_gc_outer_cycle():
    return '''get_gc_outer_cycle:
                lw $t1 header_next_slot($t1)
                beq $t1 $zero get_gc_free
                lw $t2 header_reachable_slot($t1)
                beq $t2 reachable get_gc_extend
                j get_gc_outer_cycle\n\n'''


def get_gc_extend():
    return '''get_gc_extend:
                addiu $a0 $t1 header_size    
                jal get_gc_rec_extend
                j get_gc_outer_cycle\n\n'''


def get_gc_free():
    return '''get_gc_free:
                addiu $t0 $gp used_list
                lw $t0 header_next_slot($t0)\n\n'''


def get_gc_free_cycle():
    return '''get_gc_free_cycle:
                beq $t0 $zero get_gc_finish
                lw $t1 header_reachable_slot($t0)
                bne $t1 reachable get_gc_free_cycle_free
                sw $zero header_reachable_slot($t0)
                move $a0 $t0
                jal verify_obj
                beq $v0 $zero get_gc_free_cycle
                li $t1 obj_mark
                addiu $t2 $t0 header_size
                lw $t3 4($t2)
                sll $t3 $t3 2
                addu $t2 $t2 $t3
                sw $t1 -4($t2)
                lw $t0 header_next_slot($t0)
                j get_gc_free_cycle\n\n'''


def get_gc_free_cycle_free():
    return '''get_gc_free_cycle_free:
                move $a0 $t0
                lw $t0 header_next_slot($t0)
                jal free_block
                j get_gc_free_cycle\n\n'''


def get_gc_finish():
    return '''get_gc_finish:
                lw $t0 0($sp)
                lw $t1 4($sp)
                lw $t2 8($sp)
                lw $t3 12($sp)
                lw $a0 16($sp)
                lw $ra 20($sp)
                addiu $sp $sp 24

                jr $ra\n\n'''


def get_gc_rec_extend():
    return '''get_gc_rec_extend:
                addiu $sp $sp -16
                sw $a0 0($sp)
                sw $t0 4($sp)
                sw $t1 8($sp)
                sw $ra 12($sp)
                
                jal verify_obj 
                beq $v0 $zero get_gc_rec_extend_finish

                lw $t0 4($a0)
                sll $t0 $t0 2
                addiu $t0 $t0 -4
                addu $t0 $a0 $t0
                lw $t1 0($t0)   
                beq $t1 obj_extended get_gc_rec_extend_finish
                
                
                li $t1 reachable
                addiu $a0 $a0 neg_header_size
                sw $t1 header_reachable_slot($a0)
                addiu $a0 $a0 header_size 

                
                li $t1 obj_extended
                sw $t1 0($t0)

                lw $t0 0($a0)   
                
                
                la $t1 int_type
                lw $t1 0($t1)
                beq $t0 $t1 get_gc_rec_extend_finish

                la $t1 string_type
                lw $t1 0($t1)
                beq $t0 $t1 get_gc_rec_extend_string_obj

                lw $t0 4($a0)
                li $t1 meta_data_obj_size
                sub $t0 $t0 $t1
                
                addiu $t1 $a0 12\n\n'''


def get_gc_rec_extend_attr_cycle():
    return '''get_gc_rec_extend_attr_cycle:
                beq $t0 $zero get_gc_rec_extend_finish
                lw $a0 0($t1)
                jal get_gc_rec_extend
                addiu $t1 $t1 4
                sub $t0 $t0 1
                j get_gc_rec_extend_attr_cycle\n\n'''


def get_gc_rec_extend_string_obj():
    return '''get_gc_rec_extend_string_obj:
                lw $t0 8($a0)
                addiu $t0 $t0 neg_header_size
                li $t1 reachable
                sw $t1 header_reachable_slot($t0)\n\n'''


def get_gc_rec_extend_finish():
    return '''get_gc_rec_extend_finish:
                lw $a0 0($sp)
                lw $t0 4($sp)
                lw $t1 8($sp)
                lw $ra 12($sp)
                addiu $sp $sp 16

                jr $ra\n\n'''


def less_eq():
    return '''less_eq:
                ble $a0 $a1 less_eq_true
                li $v0 0
                j less_eq_finish\n\n'''


def less_eq_true():
    return '''less_eq_true:
                li $v0 1\n\n'''


def less_eq_finish():
    return '''less_eq_finish:
                jr $ra\n\n'''


def less():
    return '''less:
                blt $a0 $a1 less_true
                li $v0 0
                j less_finish\n\n'''


def less_true():
    return '''less_true:
                li $v0 1\n\n'''


def less_finish():
    return '''less_finish:
                jr $ra\n\n'''


def lenx():
    return '''len:
                addiu $sp $sp -8
                sw $t0 0($sp)
                sw $t1 4($sp)

                move $t0 $a0
                move $v0 $zero\n\n'''


def len_cycle():
    return '''len_cycle:
                lb $t1 0($t0)
                beq $t1 $zero len_finish
                addi $v0 $v0 1
                addiu $t0 $t0 1
                j len_cycle\n\n'''


def len_finish():
    return '''len_finish:
                lw $t0 0($sp)
                lw $t1 4($sp)
                addiu $sp $sp 8

                jr $ra\n\n'''


def malloc():
    return '''malloc:
                move $v0 $zero
                addiu $sp $sp -28
                sw $t1 0($sp)
                sw $t0 4($sp)
                sw $a0 8($sp)
                sw $a1 12($sp)
                sw $ra 16($sp)
                sw $t2 20($sp)
                sw $t3 24($sp)
                
                addiu $t0 $gp free_list
                j malloc_cycle\n\n'''


def malloc_finish():
    return '''malloc_finish:
                move $a0 $v0
                lw $a1 8($sp)                  
                jal divide_block

                lw $t1 header_next_slot($v0)
                sw $t1 header_next_slot($t3)

                addiu $t1 $gp used_list
                lw $a0 header_next_slot($t1)

                sw $a0 header_next_slot($v0)
                sw $v0 header_next_slot($t1)
                
                addiu $v0 $v0 header_size

                lw $t3 24($sp)
                lw $t2 20($sp)
                lw $ra 16($sp)
                lw $a1 12($sp)
                lw $a0 8($sp)
                lw $t0 4($sp)
                lw $t1 0($sp)
                addiu $sp $sp 28

                jr $ra\n\n'''


def malloc_cycle():
    return '''malloc_cycle:
                move $t2 $t0                        
                lw $t0 header_next_slot($t0)        
                beq $t0 $zero malloc_search_finish     
                j malloc_verify_valid_block\n\n'''


def malloc_search_finish():
    return '''malloc_search_finish:
                beq $v0 $zero malloc_alloc_new_block 
                j malloc_finish\n\n'''


def malloc_alloc_new_block():
    return '''malloc_alloc_new_block:
                li $t1 alloc_size               
                move $t3 $t2
                move $a1 $a0                    
                move $a0 $t2                    
                bge $a1 $t1 malloc_big_block    
                li $a1 alloc_size        
                jal extend_heap
                
                j malloc_finish\n\n'''


def malloc_big_block():
    return '''malloc_big_block:
                jal extend_heap
                j malloc_finish\n\n'''


def malloc_verify_valid_block():
    return '''malloc_verify_valid_block:
                lw $t1 header_size_slot($t0)             
                bge $t1 $a0 malloc_valid_block    
                j malloc_cycle\n\n'''


def malloc_valid_block():
    return '''malloc_valid_block:
                beq $v0 $zero malloc_first_valid_block    
                bge $t1 $v1 malloc_cycle                    
                move $v0 $t0                        
                move $v1 $t1  
                move $t3 $t2
                j malloc_cycle\n\n'''


def malloc_first_valid_block():
    return '''malloc_first_valid_block:
                move $v0 $t0                        
                move $v1 $t1                        
                move $t3 $t2 
                j malloc_cycle\n\n'''


def mem_manager_init():
    return '''mem_manager_init:
                addiu $sp $sp -16
                sw $v0 0($sp)
                sw $a0 4($sp)
                sw $a1 8($sp)
                sw $ra 12($sp)
                li $v0 9
                li $a0 init_alloc_size
                syscall
                move $gp $v0
                addiu $gp $gp state_size

                sw $zero header_size_slot($gp)
                sw $zero header_reachable_slot($gp)

                move $a0 $gp
                li $a1 alloc_size
                jal extend_heap

                addiu $a0 $a0 header_size
                sw $zero header_size_slot($a0)
                sw $zero header_next_slot($a0)
                sw $zero header_reachable_slot($a0)



                lw $v0 0($sp)
                lw $a0 4($sp)
                lw $a1 8($sp)
                lw $ra 12($sp)
                addiu $sp $sp 16

                sw $sp stack_base($gp)

                jr $ra\n\n'''


def get_string():
    return '''get_string:
                addiu $sp $sp -36
                sw $t0 0($sp)
                sw $t1 4($sp)
                sw $t2 8($sp)
                sw $t3 12($sp)
                sw $t4 16($sp)
                sw $t5 20($sp)
                sw $a0 24($sp)
                sw $a1 28($sp)
                sw $ra 32($sp)
                
                addiu $t0 $gp free_list
                move $t1 $zero
                move $t2 $t0\n\n'''


def get_string_larger_block_cycle():
    return '''get_string_larger_block_cycle:
                lw $t0 header_next_slot($t0)
                beq $t0 $zero get_string_reading
                lw $t3 header_size_slot($t0)
                bge $t1 $t3 get_string_larger_block_cycle
                move $t1 $t3
                move $t2 $t0
                j get_string_larger_block_cycle\n\n'''


def get_string_reading():
    return '''get_string_reading:
                beq $t1 $zero get_string_new_block
                move $a1 $t1
                li $v0 8
                addiu $a0 $t2 header_size
                syscall
                move $t0 $a0
                move $t1 $zero\n\n'''


def get_string_look_nl():
    return '''get_string_look_nl:
                lb $t2 0($t0)
                beq $t2 new_line get_string_nl_founded
                beq $t2 $zero get_string_zero_founded
                addi $t1 $t1 1
                addi $t0 $t0 1
                j get_string_look_nl\n\n'''


def get_string_zero_founded():
    return '''get_string_zero_founded:
                blt $t1 $t3 get_string_nl_founded
                j get_string_no_nl\n\n'''


def get_string_nl_founded():
    return '''get_string_nl_founded:
                sb $zero 0($t0)
                addi $t1 $t1 1
                li $t2 4
                div $t1 $t2
                mfhi $t3
                beq $t3 $zero get_string_nl_founded_alligned
                sub $t2 $t2 $t3
                add $t1 $t1 $t2\n\n'''


def get_string_nl_founded_alligned():
    return '''get_string_nl_founded_alligned:
                move $a1 $t1
                addiu $a0 $a0 neg_header_size
                jal divide_block
                jal use_block

                addiu $v0 $a0 header_size
                j get_string_finish\n\n'''


def get_string_no_nl():
    return '''get_string_no_nl:
                addi $t1 $t1 1
                blt $t1 string_size_treshold get_string_dup
                addi $t1 $t1 alloc_size
                j get_string_extend_heap\n\n'''


def get_string_dup():
    return '''get_string_dup:
	            sll $t1 $t1 1\n\n'''


def get_string_extend_heap():
    return '''get_string_extend_heap:
                move $a1 $t1
                move $t0 $a0
                addiu $a0 $gp free_list\n\n'''


def get_string_last_block_cycle():
    return '''get_string_last_block_cycle:
                lw $t1 header_next_slot($a0)
                beq $t1 $zero get_string_last_block_founded
                lw $a0 header_next_slot($a0)
                j get_string_last_block_cycle\n\n'''


def get_string_last_block_founded():
    return '''get_string_last_block_founded:
                jal extend_heap
                jal extend_block
                lw $t1 header_next_slot($a0)
                bne $t1 $zero get_string_copy_prev
                move $t1 $a0\n\n'''


def get_string_copy_prev():
    return '''get_string_copy_prev:
                lw $t3 header_size_slot($t1)
                move $t2 $zero
                move $t5 $t1
                addiu $t1 $t1 header_size\n\n'''


def get_string_copy_cycle():
    return '''get_string_copy_cycle:
                lb $t4 0($t0)
                beq $t4 $zero get_string_copy_finish
                sb $t4 0($t1)
                addi $t2 $t2 1
                addi $t0 $t0 1
                addi $t1 $t1 1
                j get_string_copy_cycle\n\n'''


def get_string_copy_finish():
    return '''get_string_copy_finish:
                sub $t3 $t3 $t2
                move $a0 $t1
                move $a1 $t3
                li $v0 8
                syscall
                move $t0 $a0
                move $t1 $t2
                addiu $a0 $t5 header_size
                j get_string_look_nl\n\n'''


def get_string_finish():
    return '''get_string_finish:
                lw $t0 0($sp)
                lw $t1 4($sp)
                lw $t2 8($sp)
                lw $t3 12($sp)
                lw $t4 16($sp)
                lw $t5 20($sp)
                lw $a0 24($sp)
                lw $a1 28($sp)
                lw $ra 32($sp)
                addiu $sp $sp 36

                jr $ra\n\n'''


def get_string_new_block():
    return '''get_string_new_block:
    addiu $t0 $gp free_list\n\n'''


def get_string_new_block_search_last():
    return '''get_string_new_block_search_last:
                lw $t1 header_next_slot($t0)
                beq $t1 $zero get_string_new_block_create
                move $t0 $t1
                j get_string_new_block_search_last\n\n'''


def get_string_new_block_create():
    return '''get_string_new_block_create:
                move $a0 $t0
                li $a1 alloc_size
                jal extend_heap
                jal extend_block
                lw $t2 header_next_slot($a0)
                beq $t2 $zero get_string_new_block_extended
                lw $t1 header_size_slot($t2)
                j get_string_reading\n\n'''


def get_string_new_block_extended():
    return '''get_string_new_block_extended:
                move $t2 $a0
                lw $t1 header_size_slot($a0)
                j get_string_reading\n\n'''


def divide_block():
    return '''divide_block:
                addiu $sp $sp -16
                sw $t0 0($sp)
                sw $t1 4($sp)
                sw $a0 8($sp)
                sw $a1 12($sp)

                
                lw $t0 header_size_slot($a0)
                bgt $a1 $t0 divide_block_error_small
                
    
                sub $t0 $t0 $a1
                li $t1 header_size
                ble $t0 $t1 divide_block_same_size

               
                addu $t0 $a0 $a1
                addiu $t0 $t0 header_size     

                
                lw $t1 header_next_slot($a0)    
                sw $t1 header_next_slot($t0)
                sw $t0 header_next_slot($a0)

                lw $t1 header_size_slot($a0)    
                sub $t1 $t1 $a1

                addi $t1 $t1 neg_header_size
                sw $t1 header_size_slot($t0)
                sw $a1 header_size_slot($a0)
                move $v0 $a0
                j divide_block_finish\n\n'''


def divide_block_same_size():
    return '''divide_block_same_size:
                move $v0 $a0
                j divide_block_finish\n\n'''


def divide_block_error_small():
    return '''divide_block_error_small:
                j divide_block_finish\n\n'''


def divide_block_finish():
    return '''divide_block_finish:
                lw $t0 0($sp)
                lw $t1 4($sp)
                lw $a0 8($sp)
                lw $a1 12($sp)
                addiu $sp $sp 16

                jr $ra\n\n'''


def sub_string():
    return '''sub_string:
                addiu $sp $sp -24
                sw $t0 0($sp)
                sw $t1 4($sp)
                sw $t2 8($sp)
                sw $t3 12($sp)
                sw $a0 16($sp)
                sw $ra 20($sp)

                move $t0 $a0
                li $t1 4
                addiu $t3 $a2 1
                div $t3 $t1
            
                mfhi $t2
                bne $t2 $zero sub_string_allign_size
                move $t1 $t3
                j sub_string_new_block\n\n'''


def sub_string_allign_size():
    return '''sub_string_allign_size:
                sub $t1 $t1 $t2
                add $t1 $t1 $t3\n\n'''


def sub_string_new_block():
    return '''sub_string_new_block:
                move $a0 $t1
                jal malloc
                move $t3 $v0
                move $t1 $zero
                addu $t0 $t0 $a1\n\n'''


def sub_string_copy_cycle():
    return '''sub_string_copy_cycle:
                beq $t1 $a2 sub_string_finish
                lb $t2 0($t0)
                sb $t2 0($t3)
                addiu $t0 $t0 1
                addiu $t3 $t3 1
                addiu $t1 $t1 1
                j sub_string_copy_cycle\n\n'''


def sub_string_finish():
    return '''sub_string_finish:
                sb $zero 0($t3)
                lw $t0 0($sp)
                lw $t1 4($sp)
                lw $t2 8($sp)
                lw $t3 12($sp)
                lw $a0 16($sp)
                lw $ra 20($sp)
                addiu $sp $sp 24

                jr $ra\n\n'''


def use_block():
    return '''use_block:
    addiu $sp $sp -12
    sw $t0 0($sp)
    sw $t1 4($sp)
    sw $t2 8($sp)

    addiu $t0 $gp free_list\n\n'''


def use_block_cycle():
    return '''use_block_cycle:
                move $t1 $t0
                lw $t0 header_next_slot($t0)
                beq $t0 $zero use_block_finish
                beq $t0 $a0 use_block_founded
                j use_block_cycle\n\n'''


def use_block_founded():
    return '''use_block_founded:
                lw $t2 header_next_slot($t0)
                sw $t2 header_next_slot($t1)

                addiu $t1 $gp used_list
                lw $t2 header_next_slot($t1)
                sw $t0 header_next_slot($t1)
                sw $t2 header_next_slot($t0)\n\n'''


def use_block_finish():
    return '''use_block_finish:
                lw $t0 0($sp)
                lw $t1 4($sp)
                lw $t2 8($sp)
                addiu $sp $sp 12

                jr $ra\n\n'''
