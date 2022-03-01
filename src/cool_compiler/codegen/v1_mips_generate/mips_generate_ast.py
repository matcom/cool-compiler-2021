from .general_macros import sys_macro_load

class Program:
    def __init__(self) -> None:
        self.data = {}
        self.func = {}
        self.sys = sys_macro_load()

    
    def __str__(self) -> str:
        result = ".data\n"

        for key in self.data.keys():
            result += str(self.data[key]) + '\n'
        
        result += '\n.text\n.globl main\n'
        result += str(self.func['main']) + '\n'

        for key in self.func.keys():
            if key == 'main': continue
            result += str(self.func[key]) + '\n'

        result += '##########################################################################'
        return result + str(self.sys)

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
    def __init__(self, name, comment = "") -> None:
        self.name = name
        self.cmd  = []
        self.comment = comment

    def __str__(self) -> str:
        result = f'{self.name}:     #{self.comment}\n'
        for cmd in self.cmd:
            try: 
                if cmd.is_comment:
                    result = result[0:-1] + ' ' * 10 + str(cmd) + '\n' 
            except AttributeError:
                result += str(cmd) + '\n'
        return result

class LiteralMips:
    def __init__(self, text) -> None:
        self.text = text

    def __str__(self) -> str:
        return self.text

class Header_Comment:
    def __init__(self, msg) -> None:
        self.msg = msg

    def __str__(self) -> str:
        return f'#{self.msg}'

class Label:
    def __init__(self,label) -> None:
        self.label = label

    def __str__(self) -> str:
        return f'{self.label}:'

class SysCall :
    def __init__(self) -> None:
        pass

    def __str__(self) -> str:
        return f'{"syscall"}'

#################################################################################
class UnaryOp:
    def __init__(self, cmd, op, comment = '') -> None:
        self.op = op
        self.cmd = cmd
        self.comment = comment

    def __str__(self) -> str:
        return f'{self.cmd} {self.op}                               #{self.comment}'

class Jal(UnaryOp):
    def __init__(self,dest, comment = '') -> None:
            super().__init__('jal',dest, comment)

class Jr(UnaryOp):
    def __init__(self,dest, comment = '') -> None:
            super().__init__('jr',dest, comment)

class Jump(UnaryOp):
    def __init__(self,dest, comment = '') -> None:
            super().__init__('j',dest, comment)

#################################################################################  
class BinaryOp:
    def __init__(self, cmd ,registry, memory_dir, comment = '') -> None:
        self.registry = registry
        self.memory_dir = memory_dir
        self.cmd = cmd
        self.comment = comment


    def __str__(self) -> str:
        return f'{self.cmd} {self.registry}, {self.memory_dir}      #{self.comment}'

class LW(BinaryOp):
    def __init__(self, registry, memory_dir, comment = '') -> None:
        super().__init__('lw', registry, memory_dir, comment)

class LI(BinaryOp):
    def __init__(self, registry, memory_dir, comment = '') -> None:
        super().__init__('li', registry, memory_dir, comment)

class LA(BinaryOp):
    def __init__(self, registry, memory_dir, comment = '') -> None:
        super().__init__('la', registry, memory_dir, comment)

class Move(BinaryOp):
    def __init__(self, registry, memory_dir, comment = '') -> None:
        super().__init__('move', registry, memory_dir, comment)

class SW(BinaryOp):
     def __init__(self, registry, memory_dir, comment = '') -> None:
            super().__init__('sw', registry, memory_dir, comment)

###################################################################################
class TernaryOp:
    def __init__(self, cmd, dest, op1, op2, comment = '') -> None:
        self.op1 = op1
        self.op2 = op2
        self.dest = dest
        self.cmd = cmd
        self.comment = comment

    def __str__(self) -> str:
        return f'{self.cmd} {self.dest}, {self.op1}, {self.op2}     #{self.comment}'

class Seq(TernaryOp):
    def __init__(self ,r_dest, r_src_1, r_src_2, comment = '') -> None:
            super().__init__( 'seq' ,r_dest, r_src_1, r_src_2, comment)

class Beq(TernaryOp):
    def __init__(self ,r_dest, r_src_1, r_src_2, comment = '') -> None:
            super().__init__( 'beq' ,r_dest, r_src_1, r_src_2, comment)

class AddI(TernaryOp):
    def __init__(self,dest,op1,op2, comment = '') -> None:
            super().__init__('addi',dest,op1,op2, comment)
