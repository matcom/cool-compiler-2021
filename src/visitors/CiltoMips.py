from utils.mip_utils import registers as r, operations as o, datatype as dt
import visitors.visitor as visitor
from cil_ast.cil_ast import *

class CiltoMipsVisitor:
    def __init__(self, context):
        self.dottypes = []
        self.dotdata =[]
        self.dotcode =[]
        self.context = context
        self.code = []
        self.data = []
        self.label_id = 0
        self.current_function: FunctionNode = None
        self.conform = {}
    def stack_offset(self, name):
        try:
            all_ = []
            for i in self.current_function.params:
                if isinstance(i, ParamNode):
                    all_.append(i.name)
                else:
                    all_.append(i)
            for i in self.current_function.localvars:
                if isinstance(i, LocalNode):
                    all_.append(i.name)
                else:
                    all_.append(i)
            return -4*all_.index(name)
        except:
            a = 0
            return 0
    def write_data(self, instruction):
        self.data.append(instruction)

    def write_code(self, instruction):
        self.code.append(instruction)

    def compute_parents(self, inherit):
        self.conform['Object'] = ['Object']
        class_list = []
        for c, _ in inherit.items():
            self.conform[c] = [c]
            class_list.append(c)
        for c in class_list:
            current = c
            while not current == 'Object':
                self.conform[c].append(inherit[current])
                current = inherit[current]

    @visitor.on('node')
    def visit(self, node):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node):
        self.dottypes = node.dottypes
        self.dotdata = node.dotdata
        self.dotcode = node.dotcode
        self.attrs = node.cattrs
        self.functions = node.dfunc
        self.parents = node.dparents
        self.compute_parents(self.parents)

        self.write_data('.data')  # initialize the .data segment
        self.write_data(f'p_error: {dt.asciiz} "Aborting from String"')
        self.write_data(f'zero_error: {dt.asciiz} "Division by zero"')
        self.write_data(f'range_error: {dt.asciiz} "Index out of range"')

        for c in self.attrs:
            self.write_data(c + '_class_name' + ': .asciiz "' + c + '"')

        for c, conform_list in self.conform.items():
            line = c + '_conforms_to: .word '+ conform_list[0] + '_class_name'
            n = len(conform_list)
            for i in range(1, n): line += ', ' + conform_list[i] + '_class_name'
            self.write_data(line)

        for usr_data in self.dotdata:
            data_addr = usr_data.name
            data_value = usr_data.value
            self.write_data('{}: {} {}'.format(usr_data.name, dt.asciiz, usr_data.value))

        self.write_code('.text')
        self.write_code('.globl main')
        self.write_code('''
            str_len:
                    li $v0,0
                    move $v1, $a0
                __lenLoop:
                    lbu $t1, 0($v1)
                    beq $t1,$0,__lenExit
                    addu $v0,$v0,1
                    addu $v1,$v1,1
                    b __lenLoop
                __lenExit:
                    jr $ra

            str_copy:
                lw $a0, -4($fp)
                lw $a1, -8($fp)
                lw $a2, -12($fp)
                
                move $v0, $a0
                
                str__while_copy:
                beqz $a2, str__end_copy
                
                xor $t0, $t0, $t0
                lb $t0, 0($a1)
                sb $t0, 0($a0)
                
                subu $a2, $a2,1
                addu $a0, $a0,1
                addu $a1, $a1,1
                j str__while_copy
                
                str__end_copy:
                jr $ra
                
                str_index_error:
                    li $v0, 4
                    la $a0, range_error
                    syscall
                    li $v0, 10
                    syscall
                    jr $ra

            str_substring:
                # load arguments
                move $t5, $a0
                move $t3, $a1
                li $t4, 0
                move $t2, $a2

                # check for index out of range
                move $a3, $ra
                jal str_len
                move $ra, $a3

                addu $t6, $t3, $t2
                bgt $t6, $v0, str_index_error

                # create substring
                move $a0, $t2           #length
                addu $a0, $a0, 1
                li $v0, 9       #make space
                syscall
                # tenemos en $v0 la direccion del nuevo string

                addu $t5, $t5, $t3

                subu $sp, $sp, 4
                sw $ra, 0($sp)
                subu $sp, $sp, 4
                sw $fp, 0($sp)
                move $fp,$sp
                subu $sp, $sp, 4
                sw $v0, 0($sp)
                subu $sp, $sp, 4
                sw $t5, 0($sp)
                subu $sp, $sp, 4
                sw $t2, 0($sp)

                jal str_copy
                move $sp,$fp

                lw $fp, 0($sp)
                addi $sp,$sp, 4

                lw $ra, 0($sp)
                addi $sp,$sp, 4

                addu $t9, $v0, $t2          #null terminated
                sb $0, 0($t9)
                jr $ra


                #$a0 el prefijo, y en $a1, el str.
            
            str1_prefix_of_str2:
                lb $t0, 0($a0)
                lb $t1, 0($a1)
                beqz $t0, prefixTrue
                bne	 $t0, $t1, prefixFalse
                addu $a0,$a0,1
                addu $a1,$a1,1
                b str1_prefix_of_str2
                prefixFalse:
                    li $v0, 0
                    jr $ra
                prefixTrue:
                    li $v0, 1
                    jr $ra

            str_comparer:
                move $a0, $a2
                move $a1, $ra
                jal str_len       #$v0=len(message1)
                move $ra, $a1

                move $s1, $v0

                move $a0, $a3

                move $a1, $ra
                jal str_len       #$v0=len(message2)
                move $ra, $a1

                beq $v0, $s1, string_length_comparer_end
                li $v0, 0
                j string_comparer_end

                string_length_comparer_end:
                move $a0, $a2
                move $a1, $a3
                move $s1, $ra
                jal str1_prefix_of_str2
                move $ra, $s1
                string_comparer_end:
                jr $ra

            case_conform:
                move $s0, $a0
                move $s1, $a1
                START_CASE_LOOP:

                    lw $a1, 0($s0)

                    addi $s0, $s0, 4

                    move $t0, $s1	# Address of 1st element in array.
                    li $v0, 4		# System call code 4 (print_string).
                    li $t1, 0		# Initialize array offset.

                loop_INTERNAL:

                    # Use the address mode label(register).

                    lw $a0, 0($t0)	# Load value at address str_array + $t1 (offset).	

                    beq $a0, $a1, END_CASE_LOOP

                    addi $t0, $t0, 4	# Next element, i.e., increment offset by 4.
                    addi $t1, $t1, 4	# Next element, i.e., increment offset by 4.

                    # Done or loop once more?

                    ble $t1, $a2, loop_INTERNAL
                    b START_CASE_LOOP
                END_CASE_LOOP:
                move $v0, $a0
                jr $ra

            str_concat:
                move $a3, $ra
                jal str_len
                move $ra, $a3

                # guardamos en $t4, la longitud de str1
                move $t4, $v0
                # el str1
                move $t5, $a0
                move $a0, $a1
                move $t8, $a1

                move $a3, $ra
                jal str_len
                move $ra, $a3

                # reservamos espacio para el nuevo string
                # guardamos en $t7 la longitud de str2
                move $t7, $v0
                addu $v0, $t4, $v0
                addu $v0, $v0, 1
                move $a0, $v0
                li $v0, 9
                syscall

                # en $t5 esta str1, y en $t8, str2-------------------------

                # save str1 part------------------------------------------
                # push $ra
                subu $sp, $sp, 4
                sw $ra, 0($sp)
                # push $fp
                subu $sp, $sp, 4
                sw $fp, 0($sp)

                move $fp, $sp

                # push dest to copy pointer
                subu $sp, $sp, 4
                sw $v0, 0($sp)

                # push copy from
                subu $sp, $sp, 4
                sw $t5, 0($sp)

                # push how much to copy
                subu $sp, $sp, 4
                sw $t4, 0($sp)

                jal str_copy

                move $sp, $fp

                lw $fp, 0($sp)
                addu $sp, $sp, 4

                lw $ra, 0($sp)
                addu $sp, $sp, 4

                # save str2 part-------------
                # push $ra
                subu $sp, $sp, 4
                sw $ra, 0($sp)

                # push $fp
                subu $sp, $sp, 4
                sw $fp, 0($sp)

                move $fp, $sp

                # push where to copy
                move $t9, $v0
                addu $t0, $v0, $t4
                subu $sp, $sp, 4
                sw $t0, 0($sp)

                # push copy from
                subu $sp, $sp, 4
                sw $t8, 0($sp)

                subu $sp, $sp, 4
                sw $t7, 0($sp)

                jal str_copy

                move $sp, $fp

                lw $fp, 0($sp)
                addu $sp, $sp, 4

                lw $ra, 0($sp)
                addu $sp, $sp, 4

                addu $v0, $t7, $v0
                sb $0, 0($v0)

                move $v0, $t9
                jr $ra
            ''')

        for c in self.dotcode:
            self.visit(c)


    @visitor.when(TypeNode)
    def visit(self, node):
        pass

    @visitor.when(DataNode)
    def visit(self, node):
        pass

    @visitor.when(FunctionNode)
    def visit(self, node):
        # methods = [
        #     'Object_abort',
        #     'Object_type_name',
        #     'Object_copy',
        #     'String_concat',
        #     'String_substr',
        #     'String_length',
        #     'IO_in_int',
        #     'IO_out_int',
        #     'IO_in_string',
        #     'IO_out_string',
        # ]
        # if node.fname in methods: 
        #     return
        
        self.current_function = node
        self.write_code(node.name + ':')        

        #ya se guardaron los argumentos en la pila
        #tenemos que guardar espacio para las variables locales        
        self.write_code('{} {}, {}, -{}'.format(o.addi, r.sp, r.sp, str(4*len(node.localvars))))        

        self.write_code('{} {}, {}, -8'.format(o.addi, r.sp, r.sp))
        self.write_code('{} {}, 4({}) # save $ra'.format(o.sw, r.ra, r.sp))
        self.write_code('{} {}, 0({}) # save $fp'.format(o.sw, r.fp, r.sp))

        n = 4*(len(node.params) + len(node.localvars) + 1)
        self.write_code('{} {}, {}, {}'.format(o.addi, r.fp, r.sp, n)) 

        for instruction in node.instructions:
            self.visit(instruction)
        

        self.write_code('{} {}, 4({}) # restore $ra'.format(o.lw, r.ra, r.sp))
        self.write_code('{} {}, 0({})'.format(o.lw, r.t1, r.sp))
        self.write_code('{} {}, {}, 4'.format(o.addi, r.sp, r.fp))
        self.write_code('{} {}, {} # restore $fp'.format(o.move, r.fp, r.t1))
        
        self.write_code('{} {}'.format(o.jr, r.ra))    # and return
        self.current_function = None
    
    @visitor.when(ParamNode)
    def visit(self, node):
        pass

    @visitor.when(LocalNode)
    def visit(self, node):
        pass

    @visitor.when(AssignNode)
    def visit(self, node):
        src = self.stack_pos(node.source)
        dest = self.stack_pos(node.dest)

        self.write_code('# Assign ')
        self.write_code('{} {}, {}({})'.format(o.lw, r.t0, src, r.fp))
        self.write_code('{} {}, {}({})'.format(o.lw, r.t1, dest, r.fp))

        n = self.attributes[node.type]
        for i in range(n):
            self.write_code('{} {}, {}({})'.format(o.lw, r.s0, 4*(i+2), r.t0))
            self.write_code('{} {}, {}({})'.format(o.sw, r.s0, 4*(i+2), r.t1))

    @visitor.when(PlusNode)
    def visit(self, node):
        left_pos = self.stack_offset(node.left)
        right_pos = self.stack_offset(node.right)
        dest_pos = self.stack_offset(node.dest)
        self.write_code('# Plus')
        self.write_code('{} {}, {}({}) # heap address of the left Int'.format(o.lw, r.t0, left_pos, r.fp))
        self.write_code('{} {}, 8({}) # left Int value'.format(o.lw, r.t1, r.t0))
        self.write_code('{} {}, {}({}) # heap address of the right Int'.format(o.lw, r.t0, right_pos, r.fp))
        self.write_code('{} {}, 8({}) # right Int value'.format(o.lw, r.t2, right_pos, r.t0))
        self.write_code('{} {}, {}, {} # saving to $t1 the result'.format(o.add, r.t1, r.t1, r.t2))
        self.write_code('{} {}, {}({}) # heap address of dest'.format(o.lw, r.t0, dest_pos, r.fp))
        self.write_code('{} {}, 8({}) # store result'.format(o.sw, r.t1, r.t0))
        
    @visitor.when(MinusNode)
    def visit(self, node):
        left_pos = self.stack_offset(node.left)
        right_pos = self.stack_offset(node.right)
        dest_pos = self.stack_offset(node.dest)
        self.write_code('# Plus')
        self.write_code('{} {}, {}({}) # heap address of the left Int'.format(o.lw, r.t0, left_pos, r.fp))
        self.write_code('{} {}, 8({}) # left Int value'.format(o.lw, r.t1, r.t0))
        self.write_code('{} {}, {}({}) # heap address of the right Int'.format(o.lw, r.t0, right_pos, r.fp))
        self.write_code('{} {}, 8({}) # right Int value'.format(o.lw, r.t2, right_pos, r.t0))
        self.write_code('{} {}, {}, {} # saving to $t1 the result'.format(o.sub, r.t1, r.t1, r.t2))
        self.write_code('{} {}, {}({}) # heap address of dest'.format(o.lw, r.t0, dest_pos, r.fp))
        self.write_code('{} {}, 8({}) # store result'.format(o.sw, r.t1, r.t0))

    @visitor.when(StarNode)
    def visit(self, node):
        left_pos = self.stack_offset(node.left)
        right_pos = self.stack_offset(node.right)
        dest_pos = self.stack_offset(node.dest)
        self.write_code('# Plus')
        self.write_code('{} {}, {}({}) # heap address of the left Int'.format(o.lw, r.t0, left_pos, r.fp))
        self.write_code('{} {}, 8({}) # left Int value'.format(o.lw, r.t1, r.t0))
        self.write_code('{} {}, {}({}) # heap address of the right Int'.format(o.lw, r.t0, right_pos, r.fp))
        self.write_code('{} {}, 8({}) # right Int value'.format(o.lw, r.t2, right_pos, r.t0))
        self.write_code('{} {}, {} # multiply'.format(o.mul, r.t1, r.t2))
        self.write_code('{} {} # get the result in lo'.format(o.mflo, r.t1, r.t2))
        self.write_code('{} {}, {}({}) # heap address of dest'.format(o.lw, r.t0, dest_pos, r.fp))
        self.write_code('{} {}, 8({}) # store result'.format(o.sw, r.t1, r.t0))

    @visitor.when(DivNode)
    def visit(self, node):
        left_pos = self.stack_offset(node.left)
        right_pos = self.stack_offset(node.right)
        dest_pos = self.stack_offset(node.dest)
        self.write_code('# Plus')
        self.write_code('{} {}, {}({}) # heap address of the left Int'.format(o.lw, r.t0, left_pos, r.fp))
        self.write_code('{} {}, 8({}) # left Int value'.format(o.lw, r.t1, r.t0))
        self.write_code('{} {}, {}({}) # heap address of the right Int'.format(o.lw, r.t0, right_pos, r.fp))
        self.write_code('{} {}, 8({}) # right Int value'.format(o.lw, r.t2, right_pos, r.t0))
        # zero exception
        # self.write_code("la $t0, zero_error")
        # self.write_code("sw $t0, ($sp)")
        # self.write_code("subu $sp, $sp, 4")
        self.write_code("beqz $t2, .raise")
        # self.write_code("addu $sp, $sp, 4")
        #
        self.write_code('{} {}, {} # divide'.format(o.div, r.t1, r.t2))
        self.write_code('{} {} # get the result in lo'.format(o.mflo, r.t1, r.t2))
        self.write_code('{} {}, {}({}) # heap address of dest'.format(o.lw, r.t0, dest_pos, r.fp))
        self.write_code('{} {}, 8({}) # store result'.format(o.sw, r.t1, r.t0))

    @visitor.when(EqualNode)
    def visit(self, node):
        pos_dest = self.stack_offset(node.dest)
        pos_left = self.stack_offset(node.left)
        pos_right = self.stack_offset(node.right)
        
        self.write_code('# equal ')
        self.write_code('{} {}, {}({})'.format(o.lw, r.t2, pos_left, r.fp))
        self.write_code('{} {}, {}({})'.format(o.lw, r.t3, pos_right, r.fp))
        
        self.write_code('{} {}, 8({})'.format(o.lw, r.a0, r.t2))
        self.write_code('{} {}, 8({})'.format(o.lw, r.a1, r.t3))

        self.write_code('{} {}, 0 # initialize with 0 '.format(o.li, r.t1))
        label = 'not_equal_label_{}'.format(self.label_id)
        self.label_id+=1
        self.write_code('{} {}, {} {} # branch if not equal to label'.format(o.bne, r.a0, r.a1, label))
        self.write_code('{} {}, 1 # change value to 1 if equal'. format(o.li, r.t1))
        self.write_code('{}:'.format(label))
        self.write_code('{} {}, {}({})'.format(o.lw, r.t0, pos_dest, r.fp))
        self.write_code('{} {}, 8({})'.format(o.sw, r.t1, r.t0))

    @visitor.when(LeqNode)
    def visit(self, node):
        pos_dest = self.stack_offset(node.dest)
        pos_left = self.stack_offset(node.left)
        pos_right = self.stack_offset(node.right)
        
        self.write_code('# less than or equal ')
        self.write_code('{} {}, {}({})'.format(o.lw, r.t2, pos_left, r.fp))
        self.write_code('{} {}, {}({})'.format(o.lw, r.t3, pos_right, r.fp))
        
        self.write_code('{} {}, 8({})'.format(o.lw, r.a0, r.t2))
        self.write_code('{} {}, 8({})'.format(o.lw, r.a1, r.t3))

        self.write_code('{} {}, 0 # initialize with 0 '.format(o.li, r.t1))
        label = 'not_less_than_ or_equal_label_{}'.format(self.label_id)
        self.label_id+=1
        self.write_code('{} {}, {} {} # branch if not less than or equal to label'.format(o.bgt, r.a0, r.a1, label))
        self.write_code('{} {}, 1 # change value to 1 if equal'. format(o.li, r.t1))
        self.write_code('{}:'.format(label))
        self.write_code('{} {}, {}({})'.format(o.lw, r.t0, pos_dest, r.fp))
        self.write_code('{} {}, 8({})'.format(o.sw, r.t1, r.t0)) 

    @visitor.when(LessNode)
    def visit(self, node):
        pos_dest = self.stack_offset(node.dest)
        pos_left = self.stack_offset(node.left)
        pos_right = self.stack_offset(node.right)
        
        self.write_code('# less than ')
        self.write_code('{} {}, {}({})'.format(o.lw, r.t2, pos_left, r.fp))
        self.write_code('{} {}, {}({})'.format(o.lw, r.t3, pos_right, r.fp))
        
        self.write_code('{} {}, 8({})'.format(o.lw, r.a0, r.t2))
        self.write_code('{} {}, 8({})'.format(o.lw, r.a1, r.t3))

        self.write_code('{} {}, 0 # initialize with 0 '.format(o.li, r.t1))
        label = 'not_less_than_label_{}'.format(self.label_id)
        self.label_id+=1
        self.write_code('{} {}, {} {} # branch if not less than to label'.format(o.bge, r.a0, r.a1, label))
        self.write_code('{} {}, 1 # change value to 1 if equal'. format(o.li, r.t1))
        self.write_code('{}:'.format(label))
        self.write_code('{} {}, {}({})'.format(o.lw, r.t0, pos_dest, r.fp))
        self.write_code('{} {}, 8({})'.format(o.sw, r.t1, r.t0))

    @visitor.when(GotoNode)
    def visit(self, node):
        self.write_code('# goto ')
        self.write_code('{} {} # jump unconditionally'.format(o.j, node.label))

    @visitor.when(GotoIfNode)
    def visit(self, node):
        pos = self.stack_offset(node.condition)
        self.write_code('# goto if')
        self.write_code( '{} {} {}({}) # heap address'.format(o.lw, r.t0, pos, r.fp))
        self.write_code('{} {} 8({}) # value of condition'.format(o.lw, r.t1, r.t0))
        self.write_code('{} {} {} # branch on not equal to 0'.format(o.bnez, r.t1, node.label))
        
    @visitor.when(GetAttribNode)
    def visit(self, node):
        inst = self.stack_offset(node.inst)
        dest = self.stack_offset(node.dest)
        self.write_code('# GetAttrib') 
        self.write_code('{} {}, {}({})'.format(o.lw, r.s1, inst, r.fp))
        self.write_code('{} {}, {}({})'.format(o.lw, r.s0, 4*node.attr + 8, r.s1))
        self.write_code('{} {}, {}({})'.format(o.sw, r.s0, dest, r.fp))

    @visitor.when(SetAttribNode)
    def visit(self, node):
        inst = self.stack_offset(node.inst) 

        self.write_code('# SetAttrib') 
        self.write_code('{} {}, {}({})'.format(o.lw, r.s1, inst, r.fp))

        if isinstance(node.source, int):
            self.write_code('{} {}, {}'.format(o.li, r.s0, node.source))

        else:
            src = self.stack_offset(node.source)
            self.write_code('{} {}, {}({})'.format(o.lw, r.s0, src, r.fp)) 

        self.write_code('{} {}, {}({})'.format(o.sw, r.s0, 4*node.attr + 8, r.s1))

    @visitor.when(AllocateNode)
    def visit(self, node):
        self.write_code('# Allocate ')
        sizeof = self.attrs[node.type]*4 + 8
        self.write_code('{} {}, {}, {}'.format(o.addiu, r.a0, r.zero, sizeof))
        self.write_code('{} {}, 9'.format(o.li, r.v0))
        self.write_code('{}'.format(o.syscall))
        
        self.write_code('{} {}, {}, {}'.format(o.addu, r.s1, r.zero, r.v0))
        
        count = len(self.functions[node.type])
        sizeof_dispatch = count*4
        self.write_code('{} {}, {}, {}'.format(o.addiu, r.a0, r.zero, sizeof_dispatch))
        self.write_code('{} {}, 9'. format(o.li, r.v0))
        self.write_code('{}'.format(o.syscall))
        
        self.write_code('{} {}, {}, {}'.format(o.addu, r.s0, r.zero, r.v0))
        for i in range(count):
            self.write_code('{} {}, {}'.format(o.la, r.a0, self.functions[node.type][i]))
            self.write_code('{} {}, {}({})'.format(o.sw, r.a0, 4*i, r.s0))
        self.write_code('{} {}, 4({})'.format(o.sw, r.s0, r.s1))

        #class tag
        self.write_code('{} {}, {}'.format(o.la, r.a0, node.type + '_conforms_to'))
        self.write_code('{} {}, 0({})'.format(o.sw, r.a0, r.s1))

        index = self.stack_offset(node.dest)    
        self.write_code('{} {}, {}({})'.format(o.sw, r.s1, index, r.fp))

    @visitor.when(TypeOfNode)
    def visit(self, node):
        self.write_code('# TypeOf')
        index1 = self.stack_offset(node.obj)
        self.write_code('{} {}, {}({})'.format(o.lw, r.s0, index1, r.fp))
        self.write_code('{} {}, 0({})'.format(o.lw, r.t1, r.s0))
        self.write_code('{} {}, 0({})'.format(o.lw, r.t2, r.t1))
        ## $t1 = typeOf
                        
        #el valor esta en $t1
        index = self.stack_offset(node.dest)
        self.write_code('{} {}, {}({})'.format(o.sw, r.t2, index, r.fp))

    @visitor.when(LabelNode)
    def visit(self, node):
        self.write_code("# a label")
        self.write_code("{}:".format(node.name))

    @visitor.when(IsTypeNode)
    def visit(self, node):
        pass

    @visitor.when(ParentTypeNode)
    def visit(self, node):
        pass

    @visitor.when(StaticCallNode)
    def visit(self, node):  
        self.write_code('# Static Call')
        self.write_code('{} {}'.format(o.jal, node.function))
        pos = self.stack_offset(node.dest)
        self.write_code('{} {}, {}({})'.format(o.sw, r.v0, pos, r.fp))

    @visitor.when(DynamicCallNode)
    def visit(self, node):
        self.add('# Dynamic_Call')

        _type = self.stack_offset(node.type)
        method = self.functions[node.type].index(node.method)
        dest = self.stack_offset(node.dest)

        self.write_code('{} {}, {}({})'.format(o.lw, r.t0, _type, r.fp))
        self.write_code('{} {}, 4({})'.format(o.lw, r.a0, r.t0))
        self.write_code('{} {}, {}({})'.format(o.lw, r.a1, 4*method, r.a0))   

        self.write_code('{} {}'.format(o.jalr, r.a1))
        
        self.write_code('{} {}, {}({})'.format(o.sw, r.v0, dest, r.fp))
    
    @visitor.when(ArgNode)
    def visit(self, node):
        self.write_code('# Arg')
        self.write_code('{} {}, {}, -4'.format(o.addi, r.sp, r.sp)) 
        
        pos = self.stack_offset(node.name)

        self.write_code('{} {}, {}({})'.format(o.lw, r.t1, pos, r.fp))
        self.write_code('{} {}, 0({})'.format(o.sw, r.t1, r.sp))

    @visitor.when(ReturnNode)
    def visit(self, node):
        stack_ptr = self.stack_offset(node.value)
        self.write_code('# ReturnNode')
        self.write_code(f'{o.lw} {r.t0}, {stack_ptr}({r.fp})')  # t0 <- stack pointer to the value
        self.write_code(f'{o.move} {r.v0}, {r.t0}') # return the node value

    @visitor.when(LoadNode)
    def visit(self, node):
        index = self.stack_offset(node.dest)
        self.write_code('# Load')
        self.write_code('{} {}, {}'.format(o.la, r.t1, node.msg.name))
        self.write_code('{} {}, {}({})'.format(o.lw, r.t2, index, r.fp))      #direccion en el heap 
        self.write_code('{} {}, 8({})'.format(o.sw, r.t1, r.t2))

    @visitor.when(LengthNode)
    def visit(self, node):
        self.write_code('# LengthNode')
        dest_addr = self.stack_offset(node.dest)
        string_addr = self.stack_offset(node.string)
        self.write_code(f'{o.lw} {r.s0}, {string_addr}({r.fp})')  # loads to s0(to keep it through calls) the string address
        self.write_code(f'{o.lw} {r.a0}, 8({r.s0})')
        self.write_code(f'{o.jal} str_len') # jumps to str_len multi-use function, length is stores at v0
        self.write_code(f'{o.sw} {r.v0}, {dest_addr}({r.fp})')


    @visitor.when(ConcatNode)
    def visit(self, node):
        self.write_code('# Concat')
        str1 = self.stack_offset(node.prefix)
        str2 = self.stack_offset(node.sufix)
        dest = self.stack_offset(node.dest)

        self.write_code('{} {}, {}({})'.format(o.lw, r.s0, str1, r.fp))
        self.write_code('{} {}, 8({})'. format(o.lw, r.a0, r.s0))

        self.write_code('{} {}, {}({})'.format(o.lw, r.s0, str2, r.fp))
        self.write_code('{} {}, 8({})'.format(o.lw, r.a1, r.s0))

        self.write_code('{} str_concat'.format(o.jal))

        #el str esta en $v0
        self.write_code('{} {}, {}({})'.format(o.sw, r.v0, dest, r.fp))

    @visitor.when(PrefixNode)
    def visit(self, node):
        pass

    @visitor.when(SubstringNode)
    def visit(self, node):
        self.write_code('# Substring')
        string = self.stack_offset(node.string)
        i = self.stack_offset(node.i)
        n = self.stack_offset(node.n)
        dest = self.stack_offset(node.dest)
        self.write_code('{} {}, {}({})'.format(o.lw, r.s0, string, r.fp))
        self.write_code('{} {}, 8({})'.format(o.lw, r.a0, r.s0))
        self.write_code('{} {}, {}({})'.format(o.lw, r.s0, i, r.fp))
        self.write_code('{} {}, 8({})'.format(o.lw, r.a1, r.s0))
        self.write_code('{} {}, {}({})'.format(o.lw, r.s0, n, r.fp))
        self.write_code('{} {}, 8({})'.format(o.lw, r.a2, r.s0))

        self.write_code('{} str_substring'.format(o.jal))        

        #el str esta en $v0
        self.write_code('{} {}, {}({})'.format(o.sw, r.v0, dest, r.fp))

    @visitor.when(ToStrNode)
    def visit(self, node):
        pass

    @visitor.when(AbortNode)
    def visit(self, node):
        pass

    @visitor.when(CopyNode)
    def visit(self, node):
        pos_dest = self.stack_offset(node.dest)
        pos_source = self.stack_offset(node.source)
        self.add('{} {}, {}({})'.format(o.lw, r.t0, pos_source, r.sp))
        self.add('{} {}, {}({})'.format(o.sw, r.t0, pos_dest, r.sp))

    @visitor.when(PrintStrNode)
    def visit(self, node):
        self.write_code('## out_string builtin')
        self.write_code(f'{o.li} {r.v0}, 4')  # syscall print str code, a0 = address of null-terminates string
        dest_pos = self.stack_offset(node.output)
        self.write_code(f'{o.lw} {r.t0}, {dest_pos}({r.fp})')
        self.write_code(f'{o.lw} {r.a0}, 8({r.t0})')
        self.write_code(f'{o.syscall}') # syscall with the parameters set

    @visitor.when(ReadStrNode)
    def visit(self, node):
        self.write_code('## in_string builtin')
        self.write_code(f'{o.li} {r.v0}, 9')  # syscall code for allocate mem
        self.write_code(f'{o.li} {r.a0}, 1024') # buffer size in bytes to allocate
        self.write_code(f'{o.syscall}') # stores in v0 address of allocated memory

        # time to set up the actual syscall for read string
        self.write_code(f'{o.move} {r.a0}, {r.v0}') # a0 <- v0, a0 = address of input buffer
        self.write_code(f'{o.li} {r.v0}, 8') # syscall(8) = read string
        self.write_code(f'{o.la} {r.a1}, 1024') # a1 = amount to read, input should be at most n-1 bytes, since last byte is used to null-terminate the stream
        self.write_code(f'{o.syscall}') # stores in a0 the data read, if any, an null terminates it

        # gotta add a null character to the input
        self.write_code(f'{o.move} {r.t0}, {r.a0}') # t0 <- a0, later used for the address of the last non-null character of the stream to null-terminate it
        self.write_code(f'{o.move} {r.a3}, {r.ra}') # store the return address of the current method before calling the length subroutine
        self.write_code(f'{o.jal} str_len') # stores in v0 the length+1 of the string, in v1 the v0-th character of the string
        self.write_code(f'{o.move} {r.ra}, {r.a3}')  #restore the ra address previously saved
        self.write_code(f'{o.subu} {r.v0}, {r.v0}, 1')  # actual length = v0-1
        self.write_code(f'{o.addu} {r.v1}, {r.v0}, {r.t0}') # v1 = v0 + t0 = address of the last character of the input
        self.write_code(f'{o.sb} $0, 0({r.v1})')  # null terminate that mf

        dest_pos = self.stack_offset(node.input)
        self.write_code(f'{o.move} {r.v0}, {r.t0}') # returns in v0 the address of the received string
        self.write_code(f'{o.sw} {r.v0}, {dest_pos}({r.fp})') # store the result in the param variable

    @visitor.when(PrintIntNode)
    def visit(self, node):
        self.write_code('## out_int builtin')
        self.write_code(f'{o.li} {r.v0}, 1')  # syscall print str code, a0 = address of null-terminates string
        dest_pos = self.stack_offset(node.output)
        self.write_code(f'{o.lw} {r.t0}, {dest_pos}({r.fp})')
        self.write_code(f'{o.lw} {r.a0}, 8({r.t0})')
        self.write_code(f'{o.syscall}') # syscall with the parameters set

    @visitor.when(ReadIntNode)
    def visit(self, node):
        self.write_code('## out_int builtin')
        self.write_code(f'{o.li} {r.v0}, 5')  # syscall read int code, result stored in v0
        self.write_code(f'{o.syscall}')

        dest_pos = self.stack_offset(node.input)
        self.write_code(f'{o.move} {r.t0}, {r.v0}')
        self.write_code(f'{o.sw} {r.t0}, {dest_pos}({r.fp})') # stores the result to the corresponding stack value

# Input espacio a reservar en $a0
# Output direccion de memoria reservada en $a0
    def mem_alloc(self):
        self.write_code(f"# Declartation of the mem_alloc")

        self.write_code(f"mem_alloc:")
        self.write_code(f"{o.add} {r.gp} {r.gp} {r.a0}")
        self.write_code(f"{o.blt} {r.gp} {r.s7} mem_alloc_end")# si se pasa del límite de memoria dar error
        self.write_code(f"{o.j} mem_error")
        self.write_code(f"mem_alloc_end:")
        self.write_code(f"{o.sub} {r.a0} {r.gp} {r.a0}")    
        self.write_code(f"{o.jr} {r.ra}")
        self.write_code(f"")

# en a0 tengo el la instancia
    def get_parent_prot(self):
        self.write_code(f"# get parent prototype") #
        self.write_code(f"get_parent_prot:")
        self.write_code(f"{o.lw} {r.t0} ({r.a0})")
        self.write_code(f"{o.sll} {r.t0} {r.t0} 2")# mult por 4 pa tener el offset
        self.write_code(f"{o.lw} {r.t0} ({r.s4})")
        self.write_code(f"{o.move} {r.a0} {r.t0}")
        self.write_code(f"{o.jr} {r.ra}")
        self.write_code(f"")

# funciones para errores en runtime
    def zero_error(self): # error al dividir por 0
        self.write_code(f"# Declartation of the zero-div runtime error")

        self.write_code(f"zero_error:")
        self.write_code(f"{o.la} {r.a0} _zero")
        self.write_code(f"")

        self.write_code(f"{o.li} {r.v0} 4")
        self.write_code(f"{o.syscall}")
        self.write_code(f"{o.li} {r.v0} 10")
        self.write_code(f"{o.syscall}")
        self.write_code(f"")

    def substr_error(self):
        self.write_code(f"# Declartation of the substr-index.out.of.range runtime error")

        self.write_code(f"substr_error:")
        self.write_code(f"{o.la} {r.a0} _substr")
        self.write_code(f"")
        
        self.write_code(f"{o.li} {r.v0} 4")
        self.write_code(f"{o.syscall}")
        self.write_code(f"{o.li} {r.v0} 10")
        self.write_code(f"{o.syscall}")
        self.write_code(f"")
    
    def mem_error(self):
        self.write_code(f"# Declartation of the memory-overflow runtime error")
        self.write_code(f"mem_error:")
        self.write_code(f"{o.la} {r.a0} _mem")
        self.write_code(f"")
        
        self.write_code(f"{o.li} {r.v0} 4")
        self.write_code(f"{o.syscall}")
        self.write_code(f"{o.li} {r.v0} 10")
        self.write_code(f"{o.syscall}")
        self.write_code(f"")


    def utils_functs(self):
        self.mem_alloc()
        self.get_parent_prot()
        self.object_copy()
        self.str_eq()
        self.str_concat()
        self.str_substr()
        self.length()
        self.zero_error()
        self.mem_error()
        self.substr_error()