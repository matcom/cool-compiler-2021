FP = "$fp"
SP = "$sp"
RA = "$ra"
A0 = "$a0"
A1 = "$a1"
A2 = "$a2"
A3 = "$a3"
A4 = "$a4"
A5 = "$a5"
A6 = "$a6"
V0 = "$v0"
V1 = "$v1"
V2 = "$v2"
V3 = "$v3"
V4 = "$v4"
V5 = "$v5"
V6 = "$v6"
V7 = "$v7"

class MIPSFormatter:
    def __init__(self):
        self.code = ""

    def reset(self):
        self.code = ""

    def new_line(self):
        self.code += '\n'

    def move(self, reg1, reg2):
        self.code += f"\tmove {reg1}, {reg2}\n"
    
    def load_int(self, reg, val):
        self.code += f"\tli {reg}, {val}\n"

    def syscall(self):
        self.code += f"\tsyscall\n"

    def push(self, val):
        self.code += f"\tsw {val}, 0($sp)\n"
        self.code += f"\taddu $sp, $sp, -4\n"

    def pop(self, reg):
        self.code += f"\tlw {reg}, 0($sp)\n"
        self.code += f"\taddu $sp, $sp, 4\n"

    def label(self, label):
        self.code += f"{label}:\n"

    def load_byte(self, reg, val):
        self.code += f"\tlb {reg}, {val}\n"

    def jump(self, label):
        self.code += f"\tj {label}\n"

    def jump_return(self):
        self.code += f"\tjr $ra\n"

    def jal(self, proc):
        self.code += f"\tjal proc\n"

    def load_word(self, reg, addr):
        self.code += f"\tlw {reg}, {addr}\n" 

    def save_word(self, reg, addr):
        self.code += f"\tsw {reg}, {addr}\n"
    
    def addu(self, dst, op1, op2):
        self.code += f"\taddu {dst}, {op1}, {op2}\n"

    def bgtz(self, reg, label):
        self.code += f"\tbgtz {reg}, {label}\t"

    def addr(self, offset, reg):
        return f'{offset}({reg})' 
