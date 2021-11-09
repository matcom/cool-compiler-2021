from AST_CIL import *
import visitor

class Build_Mips:
    def __init__(self, ast, sem):
        self.lines = []
        self.idCount = 0
        self.current_function = None
        self.attributes = {}
        for c, a in sem.class_attrs.items():
            self.attributes[c] = len(a)
        self.attributes['Int'] = 1
        self.attributes['String'] = 1
        self.attributes['Bool'] = 1
        self.attributes['Object'] = 0
        self.visit(ast)


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
        #self.add('buffer: .space 1025')

        #self.add('String' + ':' + ' .asciiz ' + '"String"')

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

    @visitor.when(Load)
    def visit(self, load):
        index = self.stack_pos(load.dest)
        self.add('#Load')
        self.add('la $t1, {}'.format(load.msg))
        self.add('lw $t2, {}($fp)'.format(index))      #direccion en el heap 
        self.add('sw $t1, 0($t2)')

    @visitor.when(PrintStr)
    def visit(self, _print):
        self.add('#PrintStr')
        self.add('li $v0, 4')		                    # system call code for print_str
        index = self.stack_pos(_print.str_addr)         # pos en la pila
        self.add('lw $t0, {}($fp)'.format(index)) 	    # dir en el heap
        self.add('lw $a0, 0($t0)')                      # str to print
        self.add('syscall')			                    # print it

    @visitor.when(PrintInt)
    def visit(self, _print):
        self.add('#PrintInt')
        self.add('li $v0, 1')		                    # system call code for print_int
        index = self.stack_pos(_print.value)            # pos en la pila de la instancia        
        self.add('lw $t0, {}($fp)'.format(index)) 	    # dir en el heap
        self.add('lw $a0, 0($t0)')                      # int to print
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
    
    @visitor.when(Length)
    def visit(self, length):
        self.add('#str_Length')
        index1 = self.stack_pos(length.str_addr)         # pos en la pila
        self.add('lw $s0, {}($fp)'.format(index1)) 	    # dir en el heap
        self.add('lw $t0, 0($s0)')        
        self.add('li $t1,0')        
        self.add('loop:')
        self.add('lb   $a0,0($t0)')
        self.add('beqz $a0,done')
        self.add('addi $t0,$t0,1')
        self.add('addi $t1,$t1,1')
        self.add('j     loop')
        self.add('done:')
        ## $t1 = count
                        
        #el valor esta en $t1
        index = self.stack_pos(length.dest)
        self.add('sw $t1, {}($fp)'.format(index))

    @visitor.when(Substring)
    def visit(self, substring):
        self.add('#substring')
        index1 = self.stack_pos(substring.str_addr)         # pos en la pila
        self.add('lw $s0, {}($fp)'.format(index1)) 	        # dir en el heap
        self.add('lw $a0, 0($s0)')
        index2 = self.stack_pos(substring.pos)
        self.add('lw $s0, {}($fp)'.format(index2)) 	        # dir en el heap
        self.add('lw $a1, 0($s0)')
        index3 = self.stack_pos(substring.length)
        self.add('lw $s0, {}($fp)'.format(index3)) 	        # dir en el heap
        self.add('lw $a2, 0($s0)')

        self.add('j __get_substring')

        self.add('str__copy:')
        self.add('    lw $a0, -4($fp)')
        self.add('    lw $a1, -8($fp)')
        self.add('    lw $a2, -12($fp)')
            
        self.add('    move $v0, $a0')
            
        self.add('    __while_copy:')
        self.add('    beqz $a2, __end_copy')
            
        self.add('    xor $t0, $t0, $t0')
        self.add('    lb $t0, 0($a1)')
        self.add('    sb $t0, 0($a0)') 
            
        self.add('    subu $a2, $a2,1')
        self.add('    addu $a0, $a0,1')
        self.add('    addu $a1, $a1,1')
        self.add('    j __while_copy')
            
        self.add('    __end_copy:')
        self.add('    jr $ra')

        self.add('__str_len:')
        self.add('        li $v0,0')
        self.add('        move $v1, $a0')
        self.add('    __lenLoop:')
        self.add('        lbu $t1, 0($v1)')
        self.add('        beq $t1,$0,__lenExit')
        self.add('        addu $v0,$v0,1')
        self.add('        addu $v1,$v1,1')
        self.add('        b __lenLoop')
        self.add('    __lenExit:')
        self.add('        jr $ra')        

        self.add('__abort_substrig_error:')
        self.add('    li $v0, 4')
        self.add('    la $a0, runtime_error')
        self.add('    syscall')
        self.add('    li $v0, 10')
        self.add('    syscall')
        self.add('    jr $ra')

        self.add('__get_substring:')
        # load arguments
        self.add('move $t5, $a0')
        self.add('move $t3, $a1')
        self.add('li $t4, 0')
        self.add('move $t2, $a2')

        # check for index out of range
        self.add('move $a3, $ra')
        self.add('jal __str_len')
        self.add('move $ra, $a3')

        self.add('addu $t6, $t3, $t2')
        self.add('bgt $t6, $v0, __abort_substrig_error')

        # create substring
        self.add('move $a0, $t2')           #length
        self.add('addu $a0, $a0, 1')
        self.add('li $v0, 9')       #make space
        self.add('syscall')
        # tenemos en $v0 la direccion del nuevo string

        self.add('addu $t5, $t5, $t3')

        self.add('subu $sp, $sp, 4')
        self.add('sw $ra, 0($sp)')
        self.add('subu $sp, $sp, 4')
        self.add('sw $fp, 0($sp)')
        self.add('move $fp,$sp')
        self.add('subu $sp, $sp, 4')
        self.add('sw $v0, 0($sp)')
        self.add('subu $sp, $sp, 4')
        self.add('sw $t5, 0($sp)')
        self.add('subu $sp, $sp, 4')
        self.add('sw $t2, 0($sp)')

        self.add('jal str__copy')
        self.add('move $sp,$fp')

        self.add('lw $fp, 0($sp)')
        self.add('addi $sp,$sp, 4')

        self.add('lw $ra, 0($sp)')
        self.add('addi $sp,$sp, 4')

        self.add('addu $t9, $v0, $t2')          #null terminated
        self.add('sb $0, 0($t9)')

        #el str esta en $v0
        index = self.stack_pos(substring.dest)
        self.add('sw $v0, {}($fp)'.format(index))

    @visitor.when(EqualStrThanStr)
    def visit(self, equalStrThanStr):
        self.add('#string_comparer')
        self.add('j str_comparer')

        #Recibe en $a0 el prefijo, y en $a1, el str.
        #:param output:
        #:return: Devuelve en $v0 1 si es prefijo, 0 en otro caso.
        self.add('__get_if_its_prefix:')
        self.add('    lb $t0, 0($a0)')
        self.add('    lb $t1, 0($a1)')
        self.add('    beqz $t0, prefixTrue')
        self.add('    bne	 $t0, $t1, prefixFalse')
        self.add('    addu $a0,$a0,1')
        self.add('    addu $a1,$a1,1')
        self.add('    b __get_if_its_prefix')
        self.add('    prefixFalse:')
        self.add('        li $v0, 0')
        self.add('        jr $ra')
        self.add('    prefixTrue:')
        self.add('        li $v0, 1')
        self.add('        jr $ra') 

        self.add('str_comparer:')
        index1 = self.stack_pos(equalStrThanStr.left)         # pos en la pila
        self.add('lw $s0, {}($fp)'.format(index1)) 	        # dir en el heap
        self.add('lw $a0, 0($s0)')

        self.add('move $a3, $ra')
        self.add('jal __str_len')       #$v0=len(message1)
        self.add('move $ra, $a3')

        self.add('move $s1, $v0')

        index2 = self.stack_pos(equalStrThanStr.right)         # pos en la pila
        self.add('lw $s0, {}($fp)'.format(index2)) 	        # dir en el heap
        self.add('lw $a0, 0($s0)')

        self.add('move $a3, $ra')
        self.add('jal __str_len')       #$v0=len(message2)
        self.add('move $ra, $a3')

        self.add('beq $v0, $s1, string_length_comparer_end')
        self.add('li $v0, 0')
        self.add('j string_comparer_end')

        self.add('string_length_comparer_end:')
        self.add('lw $s0, {}($fp)'.format(index1)) 	        # dir en el heap
        self.add('lw $a0, 0($s0)')

        self.add('lw $s0, {}($fp)'.format(index2)) 	        # dir en el heap
        self.add('lw $a1, 0($s0)')
        self.add('jal __get_if_its_prefix')
        self.add('string_comparer_end:')

        #el resultado esta en $v0
        index = self.stack_pos(equalStrThanStr.dest)        # pos en la pila
        self.add('lw $s0, {}($fp)'.format(index))           # dir en el heap
        self.add('sw $v0, 0($s0)')                          # store bool result

    @visitor.when(ReadStr)
    def visit(self, r):
        #leer string de la consola
        self.add('li $v0, 9')           #make space
        self.add('li $a0, 100')         #space=100
        self.add('syscall')
        
        self.add('move $a0, $v0')       #buffer
        self.add('li $v0, 8')           #input str syscall
        self.add('la $a1, 100')
        self.add('syscall')
        self.add('move $t5, $a0')       #$t5=buffer(str start)

        self.add('move $a3, $ra')
        self.add('jal __str_len')       #$v0=len(message2)
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
        self.add('lw $s0, {}($s1)'.format(4*get.attribute))             #?????????????????????????????
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

        self.add('sw $s0, {}($s1)'.format(4*_set.attribute))		    #this.data = data

    @visitor.when(Allocate)
    def visit(self, allocate):
        #malloc(4)
        #cuantos atributos tiene el objeto(1)
        #devolver direccion de inicio del objeto

        sizeof = self.attributes[allocate.ttype]*4# + 1
        self.add('#Allocate')
        self.add('addiu $a0, $zero, {}'.format(sizeof))  #call sbrk(sizeof(Object))
        self.add('li $v0, 9')                        			    #set syscall code for sbrk
        self.add('syscall')
        
        #en $v0 se encuentra la direccion de inicio del objeto
        self.add('addu $s1, $zero, $v0')	                        #s1=this
        index = self.stack_pos(allocate.dest)    
        self.add('sw $s1, {}($fp)'.format(index))

    @visitor.when(Assign)
    def visit(self, assign):
        index1 = self.stack_pos(assign.source)
        self.add('#Assign:' + assign.type)
        self.add('lw $t0, {}($fp)'.format(index1))              #copia cada argumento
        index2 = self.stack_pos(assign.dest)
        self.add('lw $t1, {}($fp)'.format(index2))
        n = self.attributes[assign.type]
        for i in range(n):
            self.add('lw $s0, {}($t0)'.format(4*i))         #---error
            self.add('sw $s0, {}($t1)'.format(4*i))         #---error
            
    @visitor.when(Plus)
    def visit(self, plus):
        index = self.stack_pos(plus.left)
        self.add('#Plus')
        self.add('lw $t0, {}($fp)'.format(index))                   #direccion en el heap del int
        self.add('lw $t1, 0($t0)')                                  #valor del int
        index = self.stack_pos(plus.right)
        self.add('lw $t0, {}($fp)'.format(index))
        self.add('lw $t2, 0($t0)')
        self.add('add $t1, $t1, $t2')                               #$t1 = a + b
        index = self.stack_pos(plus.dest)
        self.add('lw $t0, {}($fp)'.format(index))
        self.add('sw $t1, 0($t0)')

    @visitor.when(Minus)
    def visit(self, minus):
        index = self.stack_pos(minus.left)
        self.add('#Minus')
        self.add('lw $t0, {}($fp)'.format(index))                   #direccion en el heap del int
        self.add('lw $t1, 0($t0)')                                  #valor del int
        index = self.stack_pos(minus.right)
        self.add('lw $t0, {}($fp)'.format(index))
        self.add('lw $t2, 0($t0)')
        self.add('sub $t1, $t1, $t2')                               #$t1 = a - b
        index = self.stack_pos(minus.dest)
        self.add('lw $t0, {}($fp)'.format(index))
        self.add('sw $t1, 0($t0)')

    @visitor.when(Star)
    def visit(self, star):
        index = self.stack_pos(star.left)
        self.add('#Star')
        self.add('lw $t0, {}($fp)'.format(index))                   #direccion en el heap del int
        self.add('lw $t1, 0($t0)')                                  #valor del int
        index = self.stack_pos(star.right)
        self.add('lw $t0, {}($fp)'.format(index))
        self.add('lw $t2, 0($t0)')
        self.add('mul $t1, $t1, $t2')                               #$t1 = a * b
        index = self.stack_pos(star.dest)
        self.add('lw $t0, {}($fp)'.format(index))
        self.add('sw $t1, 0($t0)')

    @visitor.when(Div)
    def visit(self, div):
        index = self.stack_pos(div.left)
        self.add('#Div')
        self.add('lw $t0, {}($fp)'.format(index))                   #direccion en el heap del int
        self.add('lw $t1, 0($t0)')                                  #valor del int
        index = self.stack_pos(div.right)
        self.add('lw $t0, {}($fp)'.format(index))
        self.add('lw $t2, 0($t0)')

        self.add('div $t1, $t1, $t2')                               #$t1 = a / b

        index = self.stack_pos(div.dest)
        self.add('lw $t0, {}($fp)'.format(index))
        self.add('sw $t1, 0($t0)')

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
        self.add('lw $t1, 0($t0)') 
        self.add('bnez $t1, {}'.format(goto_if.label))      #Branch on Not Equal Zero

    @visitor.when(EqualThan)
    def visit(self, equal):
        index = self.stack_pos(equal.dest)
        index_left = self.stack_pos(equal.left)
        index_right = self.stack_pos(equal.right)

        self.add('#EqualThan')
        self.add('lw $t2, {}($fp)'.format(index_left))
        self.add('lw $t3, {}($fp)'.format(index_right))
        
        self.add('lw $a0, 0($t2)')
        self.add('lw $a1, 0($t3)')

        label = 'eq_false_' + str(self.idCount)
        self.idCount += 1

        self.add('li $t1, 0') #false
        self.add('bne $a0, $a1 {}'.format(label))
        self.add('li $t1, 1') #true
        self.add(label + ':')
        self.add('lw $t0, {}($fp)'.format(index))
        self.add('sw $t1, 0($t0)')

    @visitor.when(LowerThan)
    def visit(self, equal):
        index = self.stack_pos(equal.dest)
        index_left = self.stack_pos(equal.left)
        index_right = self.stack_pos(equal.right)

        self.add('#LowerThan')
        self.add('lw $t2, {}($fp)'.format(index_left))
        self.add('lw $t3, {}($fp)'.format(index_right))
        
        self.add('lw $a0, 0($t2)')
        self.add('lw $a1, 0($t3)')

        label = 'eq_false_' + str(self.idCount)
        self.idCount += 1

        self.add('li $t1, 0') #false
        self.add('bge $a0, $a1 {}'.format(label))
        self.add('li $t1, 1') #true
        self.add(label + ':')
        self.add('lw $t0, {}($fp)'.format(index))
        self.add('sw $t1, 0($t0)')

    @visitor.when(LowerEqualThan)
    def visit(self, equal):
        index = self.stack_pos(equal.dest)
        index_left = self.stack_pos(equal.left)
        index_right = self.stack_pos(equal.right)

        self.add('#LowerEqualThan')
        self.add('lw $t2, {}($fp)'.format(index_left))
        self.add('lw $t3, {}($fp)'.format(index_right))
        
        self.add('lw $a0, 0($t2)')
        self.add('lw $a1, 0($t3)')

        label = 'eq_false_' + str(self.idCount)
        self.idCount += 1

        self.add('li $t1, 0') #false
        self.add('bgt $a0, $a1 {}'.format(label))
        self.add('li $t1, 1') #true
        self.add(label + ':')
        self.add('lw $t0, {}($fp)'.format(index))
        self.add('sw $t1, 0($t0)')

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

