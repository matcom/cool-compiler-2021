from ast import Compare

class Program:
    def __init__(self) -> None:
        self.data = {}
        self.func = {}
    
    def __str__(self) -> str:
        result = ".data\n"

        for key in self.data.keys():
            result += str(self.data[key]) + '\n'
        
        result += '\n.text\n.globl main\n'
        result += str(self.func['main']) + '\n'

        for key in self.func.keys():
            if key == 'main': continue
            result += str(self.func[key]) + '\n'

        return result

class Data:
    def __init__(self, name, value) -> None:
        self.name = name
        self.value = value
    
    def __str__(self) -> str:
        if type(self.value) == type(str()) :
            replace_ = self.value.replace('\n', '\\n')
            return f"{self.name}: .asciiz \"{replace_}\""

        if type(self.value) == type([]):
            result = f'{self.name}: .word '
            for item in self.value:
                result += str(item) + ', '
            return result

        return f'{self.name}: .word \"{str(self.value)}\"'

class Func:
    def __init__(self, name) -> None:
        self.name = name
        self.cmd  = []

    def __str__(self) -> str:
        result = f'{self.name}:\n'
        for cmd in self.cmd:
            try: 
                if cmd.is_comment:
                    result = result[0:-1] + ' ' * 10 + str(cmd) + '\n' 
            except AttributeError:
                result += str(cmd) + '\n'
        return result

class Compare_String:
    def __init__(self) -> None:
        pass

    def __str__(self) -> str:
        return  """
 # compare str1 0($sp), str2 4($sp) salida en $s0
lw $a0 , 4($t0)     
lw $a1 , 4($t1)     

LOOP:
	lb $t0, ($a0)
	lb $t1, ($a1)
	add $a0, $a0, 1
	add $a1, $a1, 1
	beqz $t0, LOOP_END
	beqz $t1, LOOP_END
	beq $t0, $t1, LOOP
    li $s0 , 0
    j End
#	jr $ra 

EQUAL:
	li $s0, 1
	j END

LOOP_END:
	beq $t0, $t1, EQUAL
	li $s0 , 0

#	jr $ra
END:
#	jr $ra"""
        

class Comment:
    def __init__(self, msg) -> None:
        self.msg = msg
        self.is_comment = True

    def __str__(self) -> str:
        return f'#{self.msg}'

class Header_Comment:
    def __init__(self, msg) -> None:
        self.msg = msg

    def __str__(self) -> str:
        return f'#{self.msg}'


class Label:
    def __init__(self,label) -> None:
        self.label = label

    def __str__(self) -> str:
        return f'{self.label} : '    

class Load:
    def __init__(self, cmd ,registry, memory_dir) -> None:
        self.registry = registry
        self.memory_dir = memory_dir
        self.cmd = cmd

    def __str__(self) -> str:
        return f'{self.cmd} {self.registry}, {self.memory_dir}'

class Store:
    def __init__(self, cmd ,registry, memory_dir) -> None:
        self.registry = registry
        self.memory_dir = memory_dir
        self.cmd = cmd

    def __str__(self) -> str:
        return f'{self.cmd} {self.registry}, {self.memory_dir}'

class CmpNotJump:
    def __init__(self, cmd ,r_dest, r_src_1, r_src_2) -> None:
        self.r_assign =  r_dest
        self.r_op_1 = r_src_1
        self.r_op_2 = r_src_2
        self.cmd = cmd

    def __str__(self) -> str:
        return f'{self.cmd} {self.r_assign}, {self.r_op_1}, {self.r_op_2}'

class JumpInconditional:
    def __init__(self,cmd,dest) -> None:
        self.cmd=cmd
        self.dest = dest 

    
    def __str__(self) -> str:
        return f'{self.cmd} {self.dest}'

class JumpConditional:
    def __init__(self,cmd,reg1,reg2,label) -> None:
        self.cmd=cmd
        self.reg1=reg1
        self.reg2 = reg2
        self.label = label

    def __str__(self) -> str:
        return f'{self.cmd} {self.reg1} {self.reg2} {self.label}'    

    
class SysCall :
    def __init__(self) -> None:
        pass

    def __str__(self) -> str:
        return f'{"syscall"}'

class Operation:
     def __init__(self,cmd,dest,op1,op2) -> None:
        self.cmd=cmd
        self.dest = dest 
        self.op_1 = op1
        self.op_2 = op2

     def __str__(self) -> str:
        return f'{self.cmd} {self.dest}, {self.op_1}, {self.op_2}'


class Move :
    def __init__(self,cmd ,Rds) -> None:
        self.cmd = cmd
        self.Rds = Rds

    def __str__(self) -> str:
        return f'{self.cmd} {self.Rds}'
    

############################# Move ###################################################

class MFHI(Move):
      def __init__(self,Rds) -> None:
          super().__init__('mfhi', Rds)

class MFLO(Move):
    def __init__(self,Rds) -> None:
        super().__init__('mflo', Rds)          

############################  Loads   ##################################################
class LW(Load):
    def __init__(self, registry, memory_dir) -> None:
        super().__init__('lw', registry, memory_dir)

class LI(Load):
    def __init__(self, registry, memory_dir) -> None:
        super().__init__('li', registry, memory_dir)

class LA(Load):
    def __init__(self, registry, memory_dir) -> None:
        super().__init__('la', registry, memory_dir)



############################  Store   ##################################################
class SW(Store):
     def __init__(self, registry, memory_dir) -> None:
            super().__init__('sw', registry, memory_dir)



############################  Cmp   ##################################################

class SEQ(CmpNotJump):  #comparacion igualdad
    def __init__(self ,r_dest, r_src_1, r_src_2) -> None:
            super().__init__( 'seq' ,r_dest, r_src_1, r_src_2)

class SGE(CmpNotJump): #>=
    def __init__(self ,r_dest, r_src_1, r_src_2) -> None:
            super().__init__( 'sge' ,r_dest, r_src_1, r_src_2)

class SGT (CmpNotJump): #>
    def __init__(self, r_dest, r_src_1, r_src_2) -> None:
        super().__init__('sgt', r_dest, r_src_1, r_src_2)            

class SLT (CmpNotJump): #<
    def __init__(self ,r_dest, r_src_1, r_src_2) -> None:
        super().__init__( 'slt' ,r_dest, r_src_1, r_src_2)


class SLE(CmpNotJump):  # <=
    def __init__(self ,r_dest, r_src_1, r_src_2) -> None:
            super().__init__( 'sle' ,r_dest, r_src_1, r_src_2)





###########################  Jump #####################################################
class JAL(JumpInconditional):
    def __init__(self,dest) -> None:
            super().__init__('jal',dest)

class JR(JumpInconditional):
    def __init__(self,dest) -> None:
            super().__init__('jr',dest)

class Jump(JumpInconditional):
    def __init__(self,dest) -> None:
            super().__init__('j',dest)
################################# JUMPConditional #######################################

class BEQ (JumpConditional):
     def __init__(self ,register1, register2, label) -> None:
            super().__init__( 'beq' ,register1, register2,label)






################################# Operator ##############################################

class AddI(Operation):
    def __init__(self,dest,op1,op2) -> None:
            super().__init__('addi',dest,op1,op2)

class Add(Operation):
    def __init__(self,dest,op1,op2) -> None:
            super().__init__('add',dest,op1,op2)

class MUL (Operation):
    def __init__(self,dest,op1,op2) -> None:
            super().__init__('mul',dest,op1,op2)

class SUB (Operation):
     def __init__(self,dest,op1,op2) -> None:
            super().__init__('sub',dest,op1,op2)

class DIV (Operation):
    def __init__(self, dest, op1, op2) -> None:
        super().__init__('div', dest, op1, op2)   


class XOR(Operation):
    def __init__(self, dest, op1, op2) -> None:
        super().__init__('xor', dest, op1, op2)


################################# Native Func IO ################################################
class Out_String:
    def __str__(self) -> str:
       return  """
IO_out_string:
lw $t0 0($sp)   #Guarda en $t0 la direccion del string
li $v0, 4
lw $a0, 4($t0) #Pintando la propiedad value del string
syscall
addi $sp, $sp, 8
jr $ra"""

class Out_Int:
    def __str__(self) -> str:
       return """
IO_out_int:
li $v0, 1
lw $a0, 0($sp)
syscall
addi $sp, $sp, 8
jr $ra"""

class In_String:
    def __str__(self) -> str:
       return """
IO_in_string:
li $v0,8
li $a1 , 10000
syscall
move $s0 , $a0
addi $sp, $sp, 4
jr $ra
"""

class In_Int:
    def __str__(self) -> str:
       return """
IO_in_int:
li $v0, 5
syscall
move $s0 , $v0
addi $sp, $sp, 4
jr $ra
"""

class Contain:
    def __str__(self) -> str:
           return """
Contain:

loop:
    lw $s0 , ($s2)
    beq	$s0, $a1, Equal	# if $s0 ==a$t1 then target
    beq $s0 , $zero, END
    add $s2,$s2,4
    j loop
    
Equal:
li $s0 , 1
adii $sp , $sp ,4
jr $ra

END:
li $s0 , 0
addi $sp , $sp , 4
jr $ra
"""

################################# Native Func Str ################################################
class Length:
    def __str__(self) -> str:
       return """ 
       
    String_length:
    lw $t4 , ($sp)   #self
    li $t0 , 0       #contador
    lw $s2 , 4($t4)  # propiedad value

        loop:
        lb $s0 , ($s2)
        beq $s0 , $zero, END
        add $t0 , $t0 ,1
        add $s2,$s2,4
        j loop
    

    END:
        move $s0 , $t0
        addi $sp, $sp, 4
        jr $ra
       return """        


class Concat:
    def __str__(self) -> str:
       return """ 
    Concat:
    lw $t2 , 4($sp)   #self
    lw $t1 , 0($sp)   # str1
    lw $s2 ,4($t2)    # propiedad value
    lw $s1 ,4($t1)    # propiedad value

    li $v0 , 9
    li $a0 , 100      # reservar memoria pal proximo string
    syscall
    move $s3 , $v0

    loop_str1:
        lb $t0 , ($s1)
        beq  $t0 , $zero, loop_str2
        add $s1 , $s1 ,1
        sb $t0,($s3)
        add $s3 , $s3 , 1
        j loop_str1

    loop_str2:
        lb $t0 , ($s2)
        beq  $t0 , $zero, ENDConcat
        add $s2 , $s2 ,1
        sb $t0,($s3)
        add $s3 , $s3 , 1
        j loop_str1

    ENDConcat:
        move $s0, $v0
        addi $sp, $sp, 8
        jr $ra
"""

class SubStr:
    def __str__(self) -> str:
       return """   

    lw $s1 , (sp)   # guarda el indice
    lw $t4 , 4(sp) # guarda el j 
    lw $s5 , 8(sp) # self.
    lw $s3 , 4($s5)   # tomar la propiedad value del string
    add $a0 , $s1 , $t4   #tamano a reservar

    li $v0 , 9
    syscall
    move $s4 , $v0           # $s4 direciion de destino


Substring:
    li $t0 ,0 
    find_index:
        beq			$t0, $s1, find_length	# if $t0 == $s1 then estas en el indice
        add			$s3, $s3, 1		#s2 = s2 + 1
        add			$t0, $t0, 1	    # $t0 = $t0 + 1
        j find_index

    find_length:
        lb			$t1, ($s3)			# 
        sb		    $t1, ($s4)
        beq			$t0, $s2, END_Substring	# if $t0 == $t1 then target
        add			$s4, $s4, 1		# $S4 = s41 1t2
        			# 
        add			$s3, $s3, 1		#s2 = s2 + 1
        add			$t0, $t0, 1	    # $t0 = $t0 + 1
        j find_length
        
    END_Substring:
        move s0 , $a0
        addi $sp, $sp, 12
        jr $ra  
"""
################################# Native Func Obj ################################################
class Copy:
    def __str__(self) -> str:
       return """
Object_copy:
lw $t0, 0($sp)   #Guarda en $t0 self
lw $t1, 0($t0)   #Guarda definicion del tipo
lw $t3, 4($t1)   #En la segunda posicion la definicion de tipo contiene el
move $a0, $t3    #tamaño que ocupa en la pila 
li $v0, 9        
syscall          #En $v0 la nueva instancia
move $s0, $v0
copy_loop:
    beq $t3, $zero, end_copy
    lw  $t1, 0($t0)
    sw  $t1, 0($v0)
    addi $t3, $t3, -4
    add $t0, $t0, 4
    add $v0, $v0, 4
    jr copy_loop
end_copy:
addi $sp, $sp, 4
jr $ra
"""

class Abort:
    def __str__(self) -> str:
       return """
Object_abort:
li		$v0, 4		# system call #4 - print string
la		$a0, _______error______
syscall	
li		$v0, 10
syscall				# execute
"""

class Type_Name:
    def __str__(self) -> str:
       return """
IO_out_string:
lw $t0 0($sp)   #Guarda en $t0 la direccion del self
lw $t1 0($t0)   #La primera posicion de self es la propiedad type_name 
lw $t2 0($t1)   #La propiedad type_name apunta a la definicion del tipo
la $t3 0($t2)   #La definicion de tipo tiene en la primera poscion su nombre 
#Allocate a una class String puntero en sp + 12
#atributo type_name en puntero + 0
#atributo value en puntero + 4
li $a0, 8
li $v0, 9
syscall         # En $v0 la instancia del nuevo string
la $t4, String
sw $t4, 0($v0)   # Asigna el tipo String al string
sw $t3, 4($v0)  # Asigan el nombre de la clase a la propiededa value del string

addi $sp, $sp, 4
move $s0, $v0
jr $ra
"""


