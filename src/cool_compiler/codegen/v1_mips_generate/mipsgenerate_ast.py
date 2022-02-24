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

class SGE(CmpNotJump):
    def __init__(self ,r_dest, r_src_1, r_src_2) -> None:
            super().__init__( 'sge' ,r_dest, r_src_1, r_src_2)

class SLT (CmpNotJump):
    def __init__(self ,r_dest, r_src_1, r_src_2) -> None:
        super().__init__( 'slt' ,r_dest, r_src_1, r_src_2)


class SLE(CmpNotJump):
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
            super().__init__('mult',dest,op1,op2)

class SUB (Operation):
     def __init__(self,dest,op1,op2) -> None:
            super().__init__('sub',dest,op1,op2)


################################# Native Func IO ################################################
class Out_String:
    def __str__(self) -> str:
       return  """
IO_out_string:
li $v0, 4
lw $a0, 0($sp)
syscall
lw $a0, 4($sp)
addi $sp, $sp, 8
jr $ra"""

class Out_Int:
    def __str__(self) -> str:
       return """
IO_out_int:
li $v0, 1
lw $a0, 0($sp)
syscall
lw $a0, 4($sp)
addi $sp, $sp, 8
jr $ra"""

class In_String:
    def __str__(self) -> str:
       return """
"""

class In_Int:
    def __str__(self) -> str:
       return """
"""
################################# Native Func Str ################################################
class Length:
    def __str__(self) -> str:
       return """
"""

class Concat:
    def __str__(self) -> str:
       return """
"""

class SubStr:
    def __str__(self) -> str:
       return """
"""
################################# Native Func Obj ################################################
class Copy:
    def __str__(self) -> str:
       return """
"""

class Abort:
    def __str__(self) -> str:
       return """
"""

class Type_Name:
    def __str__(self) -> str:
       return """
"""


