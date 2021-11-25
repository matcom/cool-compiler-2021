from AST_CIL import *
import visitor

class Build_Mips:
    def __init__(self, ast, sem, class_functions_list):
        self.lines = []
        self.idCount = 0
        self.current_function = None
        self.attributes = {}
        self.class_functions_list = class_functions_list
        for c, a in sem.class_attrs.items():
            self.attributes[c] = len(a)
        self.attributes['Int'] = 1
        self.attributes['String'] = 1
        self.attributes['Bool'] = 1
        self.attributes['Object'] = 0
        self.conform = {}
        self.compute_parents(sem.class_parent)
        self.visit(ast)

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

    def add(self, line):
        self.lines.append(line)

    def stack_pos(self, name):
        temp = self.current_function.params + self.current_function.localvars
        index = 4*temp.index(name)
        return -index

    @visitor.on('node')
    def visit(self, node):
        pass

    @visitor.when(Program)
    def visit(self, program):

        self.add('.data')
        self.add('p_error' + ':' + ' .asciiz ' + '"Abort called from class String\\n"')#"')
        self.add('runtime_error: .asciiz "RuntimeError: Index out of range Error\\n"')
        for c, _ in self.attributes.items():
            self.add(c + '_class_name' + ': .asciiz "' + c + '"')
        
        for c, conform_list in self.conform.items():
            line = c + '_conforms_to: .word '+ conform_list[0] + '_class_name'
            n = len(conform_list)
            for i in range(1, n): line += ', ' + conform_list[i] + '_class_name'
            self.add(line)

        for _str, tag in program.data_section.items():
            self.add(tag + ':' + ' .asciiz ' + _str)

        self.add('.text')
        self.add('.globl main')

        # self.add('main:')
        # self.add('jal function_Main_main')
        # self.add('li $v0, 10')
        # self.add('syscall')

        for f in program.code_section:
            self.visit(f)
        
        self.add('''
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
                    la $a0, runtime_error
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

    @visitor.when(Function)
    def visit(self, function):
        #ya se pusieron los argumentos en la pila
        self.current_function = function
        self.add(function.fname + ':')        

        #ya se guardaron los argumentos en la pila
        #tenemos que guardar espacio para las variables locales        

        line = 'addi $sp, $sp, -' + str(4*len(function.localvars))  #espacio para las variables locales
        self.add(line)        

        self.add('addi $sp, $sp, -8')   # adjust stack for 2 item
        self.add('sw $ra, 4($sp)')      # save return address
        self.add('sw $fp, 0($sp)')      # save old frame pointer

        n = 4*(len(function.params) + len(function.localvars) + 1)
        self.add('addi $fp, $sp, {}'.format(n)) # fp apunta al primer argumento

        for intr in function.instructions:
            self.visit(intr)
        
        #restaurar los valores de los registros
        #poner el frame pointer donde estaba

        self.add('lw $ra, 4($sp)')#restauro direccion de retorno
        self.add('lw $t1, 0($sp)')
        self.add('addi $sp, $fp, 4')
        self.add('move $fp, $t1')
        
        self.add('jr $ra')    # and return
        self.current_function = None

    @visitor.when(Arg)
    def visit(self, arg):
        self.add('#Arg')
        self.add('addi $sp, $sp, -4')   # adjust stack for 1 item
        #localizar el valor de arg en las variables locales
        index = self.stack_pos(arg.vinfo)
        #pasarlo a un registro
        self.add('lw $t1, {}($fp)'.format(index))
        self.add('sw $t1, 0($sp)')     # save argument for next function

    @visitor.when(Call)
    def visit(self, call):
        #ya se pusieron los argumentos en la pila
        self.add('#Call')
        self.add('jal ' + call.func)
        index = self.stack_pos(call.dest)
        self.add('sw $v0, {}($fp)'.format(index))

    @visitor.when(Dynamic_Call)
    def visit(self, dynamic_Call):
        #ya se pusieron los argumentos en la pila
        self.add('#Dynamic_Call')

        index_left = self.stack_pos(dynamic_Call.left)
        index_function = self.class_functions_list[dynamic_Call.ttype].index(dynamic_Call.func)

        self.add('lw $t0, {}($fp)'.format(index_left)) 	        # Dir en el heap
        self.add('lw $a0, 4($t0)')                              # Dispatch pointer
        self.add('lw $a1, {}($a0)'.format(4*index_function))    # Load function

        self.add('jalr $a1')
        
        index = self.stack_pos(dynamic_Call.dest)
        self.add('sw $v0, {}($fp)'.format(index))

    @visitor.when(Load)
    def visit(self, load):
        index = self.stack_pos(load.dest)
        self.add('#Load')
        self.add('la $t1, {}'.format(load.msg))
        self.add('lw $t2, {}($fp)'.format(index))      #direccion en el heap 
        self.add('sw $t1, 8($t2)')

    @visitor.when(PrintStr)
    def visit(self, _print):
        self.add('#PrintStr')
        self.add('li $v0, 4')		                    # system call code for print_str
        index = self.stack_pos(_print.str_addr)         # pos en la pila
        self.add('lw $t0, {}($fp)'.format(index)) 	    # dir en el heap
        self.add('lw $a0, 8($t0)')                      # str to print
        self.add('syscall')			                    # print it

    @visitor.when(PrintInt)
    def visit(self, _print):
        self.add('#PrintInt')
        self.add('li $v0, 1')		                    # system call code for print_int
        index = self.stack_pos(_print.value)            # pos en la pila de la instancia        
        self.add('lw $t0, {}($fp)'.format(index)) 	    # dir en el heap
        self.add('lw $a0, 8($t0)')                      # int to print
        self.add('syscall')			                    # print it

    @visitor.when(Return)
    def visit(self, ret):
        if not ret.value is None:
            index = self.stack_pos(ret.value)
            self.add('#Return')
            self.add('lw $t1, {}($fp)'.format(index))
            self.add('move $v0, $t1')

    @visitor.when(ReadInt)
    def visit(self, r):
        #leer un int de la consola
        self.add('li $v0, 5')
        self.add('syscall')
        #el valor esta en $v0
        index = self.stack_pos(r.dest)
        self.add('move $t1, $v0')
        self.add('sw $t1, {}($fp)'.format(index))
    
    @visitor.when(TypeOf)
    def visit(self, typeOf):
        self.add('#typeOf')
        index1 = self.stack_pos(typeOf.var)             # pos en la pila
        self.add('lw $s0, {}($fp)'.format(index1)) 	    # dir en el heap
        self.add('lw $t1, 0($s0)')                      # dir del array
        self.add('lw $t2, 0($t1)')                      # primer elemento del array
        ## $t1 = typeOf
                        
        #el valor esta en $t1
        index = self.stack_pos(typeOf.dest)
        self.add('sw $t2, {}($fp)'.format(index))

    @visitor.when(Length)
    def visit(self, length):
        self.add('#str_Length')
        index1 = self.stack_pos(length.str_addr)         # pos en la pila
        self.add('lw $s0, {}($fp)'.format(index1)) 	    # dir en el heap
        self.add('lw $a0, 8($s0)')   

        self.add('jal str_len')
                        
        #el valor esta en $v0
        index = self.stack_pos(length.dest)
        self.add('sw $v0, {}($fp)'.format(index))

    @visitor.when(Concat)
    def visit(self, concat):
        self.add('#concat')# Recibe en $a0 str1 y en $a1 str2
        index_str1 = self.stack_pos(concat.head)
        index_str2 = self.stack_pos(concat.tail)
        index_dest = self.stack_pos(concat.dest)

        self.add('lw $s0, {}($fp)'.format(index_str1)) 	    # dir en el heap
        self.add('lw $a0, 8($s0)')

        self.add('lw $s0, {}($fp)'.format(index_str2)) 	    # dir en el heap
        self.add('lw $a1, 8($s0)')

        self.add('jal str_concat')

        #el str esta en $v0
        self.add('sw $v0, {}($fp)'.format(index_dest))

    @visitor.when(Substring)
    def visit(self, substring):
        self.add('#substring')
        index1 = self.stack_pos(substring.str_addr)         # pos en la pila
        self.add('lw $s0, {}($fp)'.format(index1)) 	        # dir en el heap
        self.add('lw $a0, 8($s0)')
        index2 = self.stack_pos(substring.pos)
        self.add('lw $s0, {}($fp)'.format(index2)) 	        # dir en el heap
        self.add('lw $a1, 8($s0)')
        index3 = self.stack_pos(substring.length)
        self.add('lw $s0, {}($fp)'.format(index3)) 	        # dir en el heap
        self.add('lw $a2, 8($s0)')

        self.add('jal str_substring')        

        #el str esta en $v0
        index = self.stack_pos(substring.dest)
        self.add('sw $v0, {}($fp)'.format(index))

    @visitor.when(EqualStrThanStr)
    def visit(self, equalStrThanStr):
        self.add('#string_comparer')
        index1 = self.stack_pos(equalStrThanStr.left)          # pos en la pila
        index2 = self.stack_pos(equalStrThanStr.right)         # pos en la pila
        index = self.stack_pos(equalStrThanStr.dest)           # pos en la pila
        self.add('lw $s0, {}($fp)'.format(index1)) 	        # dir en el heap
        self.add('lw $a2, 8($s0)')
        self.add('lw $s0, {}($fp)'.format(index2)) 	        # dir en el heap
        self.add('lw $a3, 8($s0)')

        self.add('jal str_comparer')        

        #el resultado esta en $v0        
        self.add('lw $s0, {}($fp)'.format(index))           # dir en el heap
        self.add('sw $v0, 8($s0)')                          # store bool result

    @visitor.when(ReadStr)
    def visit(self, r):
        #leer string de la consola
        self.add('#read_string')
        self.add('li $v0, 9')           #make space
        self.add('li $a0, 100')         #space=100
        self.add('syscall')
        
        self.add('move $a0, $v0')       #buffer
        self.add('li $v0, 8')           #input str syscall
        self.add('la $a1, 100')
        self.add('syscall')
        self.add('move $t5, $a0')       #$t5=buffer(str start)

        self.add('move $a3, $ra')
        self.add('jal str_len')       #$v0=len(message2)
        self.add('move $ra, $a3')

        self.add('subu $v0, $v0, 1')
        self.add('addu $v1, $v0, $t5')
        self.add('sb $0, 0($v1)')       #null terminated
        self.add('move $v0, $t5')       #$v0=buffer

        #el buffer esta en $v0
        index = self.stack_pos(r.dest)
        self.add('sw $v0, {}($fp)'.format(index))

    @visitor.when(GetAttrib)
    def visit(self, get):

        index = self.stack_pos(get.instance)
        self.add('#GetAttrib') 
        self.add('lw $s1, {}($fp)'.format(index))
        self.add('lw $s0, {}($s1)'.format(4*get.attribute + 8))             #?????????????????????????????
        index = self.stack_pos(get.dest)
        self.add('sw $s0, {}($fp)'.format(index))

    @visitor.when(SetAttrib)
    def visit(self, _set):

        index = self.stack_pos(_set.instance) 
        self.add('#SetAttrib') 
        self.add('lw $s1, {}($fp)'.format(index))	                    #s1 = this

        if isinstance(_set.value, int):
            self.add('li $s0, {}'.format(_set.value))

        else:
            index = self.stack_pos(_set.value)
            self.add('lw $s0, {}($fp)'.format(index)) 

        self.add('sw $s0, {}($s1)'.format(4*_set.attribute + 8))		    #this.data = data

    @visitor.when(Allocate)
    def visit(self, allocate):
        #malloc(4)
        #cuantos atributos tiene el objeto(1)
        #devolver direccion de inicio del objeto

        sizeof = self.attributes[allocate.ttype]*4 + 8      #   + tag_name + Dispatch pointer
        self.add('#---Allocate-----')
        self.add('addiu $a0, $zero, {}'.format(sizeof))  #call sbrk(sizeof(Object))
        self.add('li $v0, 9')                        			    #set syscall code for sbrk
        self.add('syscall')
        
        #en $v0 se encuentra la direccion de inicio del objeto
        self.add('addu $s1, $zero, $v0')	                        #s1=this

        #############################################################################################

        count = len(self.class_functions_list[allocate.ttype])
        sizeof_dispatch = count*4                                               #Dispatch size
        self.add('addiu $a0, $zero, {}'.format(sizeof_dispatch))                #call sbrk(sizeof(Object))
        self.add('li $v0, 9')                        			                #set syscall code for sbrk
        self.add('syscall')
        
        #en $v0 se encuentra la direccion de inicio del objeto
        self.add('addu $s0, $zero, $v0')
        for i in range(count):
            self.add('la $a0, {}'.format(self.class_functions_list[allocate.ttype][i]))
            self.add('sw $a0, {}($s0)'.format(4*i))
        self.add('sw $s0, 4($s1)')              #$s1[1]=Dispatch pointer

        #############################################################################################

        #class tag
        self.add('la $a0, {}'.format(allocate.ttype + '_conforms_to'))
        self.add('sw $a0, 0($s1)')              #$s1[0]=tag_name

        index = self.stack_pos(allocate.dest)    
        self.add('sw $s1, {}($fp)'.format(index))

    @visitor.when(Copy)
    def visit(self, copy):
        index_dest = self.stack_pos(copy.dest)
        index_source = self.stack_pos(copy.source)
        self.add('lw $t0, {}($fp)'.format(index_source))
        self.add('sw $t0, {}($fp)'.format(index_dest))

    @visitor.when(Assign)
    def visit(self, assign):
        
        index1 = self.stack_pos(assign.source)
        self.add('#Assign:' + assign.type)
        self.add('lw $t0, {}($fp)'.format(index1))              #copia cada argumento
        
        index2 = self.stack_pos(assign.dest)
        self.add('lw $t1, {}($fp)'.format(index2))

        n = self.attributes[assign.type]
        
        for i in range(n):
            self.add('lw $s0, {}($t0)'.format(4*(i+2)))         #---error
            self.add('sw $s0, {}($t1)'.format(4*(i+2)))         #---error
            
    @visitor.when(Plus)
    def visit(self, plus):
        index = self.stack_pos(plus.left)
        self.add('#Plus')
        self.add('lw $t0, {}($fp)'.format(index))                   #direccion en el heap del int
        self.add('lw $t1, 8($t0)')                                  #valor del int
        index = self.stack_pos(plus.right)
        self.add('lw $t0, {}($fp)'.format(index))
        self.add('lw $t2, 8($t0)')
        self.add('add $t1, $t1, $t2')                               #$t1 = a + b
        index = self.stack_pos(plus.dest)
        self.add('lw $t0, {}($fp)'.format(index))
        self.add('sw $t1, 8($t0)')

    @visitor.when(Minus)
    def visit(self, minus):
        index = self.stack_pos(minus.left)
        self.add('#Minus')
        self.add('lw $t0, {}($fp)'.format(index))                   #direccion en el heap del int
        self.add('lw $t1, 8($t0)')                                  #valor del int
        index = self.stack_pos(minus.right)
        self.add('lw $t0, {}($fp)'.format(index))
        self.add('lw $t2, 8($t0)')
        self.add('sub $t1, $t1, $t2')                               #$t1 = a - b
        index = self.stack_pos(minus.dest)
        self.add('lw $t0, {}($fp)'.format(index))
        self.add('sw $t1, 8($t0)')

    @visitor.when(Star)
    def visit(self, star):
        index = self.stack_pos(star.left)
        self.add('#Star')
        self.add('lw $t0, {}($fp)'.format(index))                   #direccion en el heap del int
        self.add('lw $t1, 8($t0)')                                  #valor del int
        index = self.stack_pos(star.right)
        self.add('lw $t0, {}($fp)'.format(index))
        self.add('lw $t2, 8($t0)')
        self.add('mul $t1, $t1, $t2')                               #$t1 = a * b
        index = self.stack_pos(star.dest)
        self.add('lw $t0, {}($fp)'.format(index))
        self.add('sw $t1, 8($t0)')

    @visitor.when(Div)
    def visit(self, div):
        index = self.stack_pos(div.left)
        self.add('#Div')
        self.add('lw $t0, {}($fp)'.format(index))                   #direccion en el heap del int
        self.add('lw $t1, 8($t0)')                                  #valor del int
        index = self.stack_pos(div.right)
        self.add('lw $t0, {}($fp)'.format(index))
        self.add('lw $t2, 8($t0)')

        self.add('div $t1, $t1, $t2')                               #$t1 = a / b

        index = self.stack_pos(div.dest)
        self.add('lw $t0, {}($fp)'.format(index))
        self.add('sw $t1, 8($t0)')

    @visitor.when(Label)
    def visit(self, label):
        self.add('#Label')
        self.add(label.name + ':')

    @visitor.when(Goto)
    def visit(self, goto):
        self.add('#Goto')
        self.add('j ' + goto.name)

    @visitor.when(GotoIf)
    def visit(self, goto_if):
        index = self.stack_pos(goto_if.condition)
        self.add('#GotoIf')
        self.add('lw $t0, {}($fp)'.format(index))           #direccion en el heap
        self.add('lw $t1, 8($t0)')                          #value
        self.add('bnez $t1, {}'.format(goto_if.label))      #Branch on Not Equal Zero

    @visitor.when(EqualThan)
    def visit(self, equal):
        index = self.stack_pos(equal.dest)
        index_left = self.stack_pos(equal.left)
        index_right = self.stack_pos(equal.right)

        self.add('#EqualThan')
        self.add('lw $t2, {}($fp)'.format(index_left))
        self.add('lw $t3, {}($fp)'.format(index_right))
        
        self.add('lw $a0, 8($t2)')
        self.add('lw $a1, 8($t3)')

        label = 'eq_false_' + str(self.idCount)
        self.idCount += 1

        self.add('li $t1, 0') #false
        self.add('bne $a0, $a1 {}'.format(label))
        self.add('li $t1, 1') #true
        self.add(label + ':')
        self.add('lw $t0, {}($fp)'.format(index))
        self.add('sw $t1, 8($t0)')

    @visitor.when(LowerThan)
    def visit(self, equal):
        index = self.stack_pos(equal.dest)
        index_left = self.stack_pos(equal.left)
        index_right = self.stack_pos(equal.right)

        self.add('#LowerThan')
        self.add('lw $t2, {}($fp)'.format(index_left))
        self.add('lw $t3, {}($fp)'.format(index_right))
        
        self.add('lw $a0, 8($t2)')
        self.add('lw $a1, 8($t3)')

        label = 'eq_false_' + str(self.idCount)
        self.idCount += 1

        self.add('li $t1, 0') #false
        self.add('bge $a0, $a1 {}'.format(label))
        self.add('li $t1, 1') #true
        self.add(label + ':')
        self.add('lw $t0, {}($fp)'.format(index))
        self.add('sw $t1, 8($t0)')

    @visitor.when(LowerEqualThan)
    def visit(self, equal):
        index = self.stack_pos(equal.dest)
        index_left = self.stack_pos(equal.left)
        index_right = self.stack_pos(equal.right)

        self.add('#LowerEqualThan')
        self.add('lw $t2, {}($fp)'.format(index_left))
        self.add('lw $t3, {}($fp)'.format(index_right))
        
        self.add('lw $a0, 8($t2)')          #load atributo1
        self.add('lw $a1, 8($t3)')          #load atributo2

        label = 'eq_false_' + str(self.idCount)
        self.idCount += 1

        self.add('li $t1, 0') #false
        self.add('bgt $a0, $a1 {}'.format(label))
        self.add('li $t1, 1') #true
        self.add(label + ':')
        self.add('lw $t0, {}($fp)'.format(index))
        self.add('sw $t1, 8($t0)')

    @visitor.when(Array)
    def visit(self, array):
        line = array.name + ': .word ' + array.data_list[0]                #str_array: .word one, two, three
        n = len(array.data_list)
        for i in range(1, n):
            line += ', ' + array.data_list[i]
        self.lines.insert(1, line)

    @visitor.when(GetParent)
    def visit(self, get_parent):
        self.add('#GetParent') 
        index = self.stack_pos(get_parent.instance)
        index_dest = self.stack_pos(get_parent.dest)
        self.add('lw $s1, {}($fp)'.format(index))
        self.add('lw $a0, 0($s1)')
        self.add('la $a1, {}'.format(get_parent.array_name))
        self.add('li $a2, {}'.format((get_parent.length - 1) * 4))
        
        self.add('jal case_conform')
        
        #el valor esta en $v0
        self.add('sw $v0, {}($fp)'.format(index_dest))

    @visitor.when(EndProgram)
    def visit(self, end):
        self.add('#EndProgram')
        self.add('li $v0, 4')		    # system call code for print_str
        self.add('la $a0, p_error') 	# buscar el tag
        self.add('syscall')			    # print it

        #self.add('li $v0, 4')		        # system call code for print_str
        #self.add('la $a0, ' + end.type) 	# buscar el tag
        #self.add('syscall')			        # print it

        self.add('li $v0, 10')
        self.add('syscall')

    @visitor.when(Exit)
    def visit(self, exit):
        self.add('#Exit')
        self.add('li $v0, 10')
        self.add('syscall')

