class Node:
    pass


class IType(Node):
    def __init__(self, op = None, first = None, second = None, third = None):
        self.op = op      
        self.first = first           
        self.second = second            
        self.third = third            

    def __mips__(self):
        if self.first is None:
            return '{}'.format(self.op)

        elif self.second is None: # instruction with 1 factor
            return '{}  {}'.format(self.op, self.first,)

        elif self.third is None: # instruction with 2 factors
            return '{}  {}, {}'.format(self.op, self.first, self.second)

        else: # instruction with 3 factors
            return '{}  {}, {}, {}'.format(self.op, self.first, self.second, self.third)


############################### INMEDIATE TYPE INSTRUCTIONS ##############################

####### ARITHMETIC AND LOGIC #######

class Addi(IType): 
    """
    Addition inmediate with overflow
    """
    def __init__(self, rt, rs, inmediate):          
        super(Addi, self).__init__('addi', rt, rs, inmediate)
         

class Addiu(IType):
    """
    Addition inmediate without overflow
    """
    def __init__(self, rt, rs, inmediate):        
        super(Addiu, self).__init__('addiu', rt, rs, inmediate)


class Andi(IType):
    """
    AND inmediate: Put the logical AND of register rs and the zero-extended immediate into register rt 
    """ 
    def __init__(self, rt, rs, inmediate):
        super(Andi, self).__init__('andi', rt, rs, inmediate)


class Ori(IType):
    """
    OR inmediate: Put the logical OR of register rs and the zero-extended immediate into register rt 
    """ 
    def __init__(self, rt, rs, inmediate):
        super(Ori, self).__init__('ori', rt, rs, inmediate)


class Xori(IType):
    """
    XOR inmediate: Put the logical XOR of register rs and the zero-extended immediate into register rt 
    """ 
    def __init__(self, rt, rs, inmediate):
        super(Xori, self).__init__('xori', rt, rs, inmediate)


####### COMPARISON #######

class Slti(IType):
    """
     Set less than immediate signed: Set register rt to 1 if register rs is less than the sign-extended immediate, and to 0 otherwise. Signed.
    """ 
    def __init__(self, rt, rs, inmediate):
        super(Slti, self).__init__('slti', rt, rs, inmediate)


class Sltiu(IType):
    """
    Set less than immediate unsigned: Set register rt to 1 if register rs is less than the sign-extended immediate, and to 0 otherwise. Unigned.
    """
    def __init__(self, rt, rs, inmediate):
        super(Sltiu, self).__init__('sltiu', rt, rs, inmediate)


class Lui(IType):
    """
    Load upper immediate: Load the lower halfword of the immediate imm into the upper halfword of register rt.
    """
    def __init__(self, rt, inmediate):
        super(Lui, self).__init__('lui', rt, inmediate)


class Li(IType):
    """
    Load immediate: Move the immediate imm into register rdest.
    """
    def __init__(self, rdest, inm):
        super(Li, self).__init__('li', rdest, inm)


class Slti(IType): 
    """
    Set less than immediate signed: Set register rd to 1 if register rs is less than the immediate, and to 0 otherwise. Signed.
    """
    def __init__(self, rt, rs, inmediate):
        super(Slti, self).__init__('slti', rt, rs, inmediate)


class Sltiu(IType): 
    """
    Set less than immediate unsigned: Set register rd to 1 if register rs is less than the immediate, and to 0 otherwise. Unigned.
    """
    def __init__(self, rt, rs, inmediate):
        super(Sltiu, self).__init__('sltiu', rt, rs, inmediate)



####### BRANCH INSTRUCTIONS #######

class B(IType):
    """
    Unconditionally branch to the instruction at the label.
    """ 
    def __init__(self, label):
        super(B, self).__init__('b', label)


class Beq(IType): 
    """
    Branch on equal: Conditionally branch the number of instructions specified by the offset if register rs equals rt.
    """
    def __init__(self, rs, rt, label):
        super(Beq, self).__init__('beq', rs, rt, label)


class Bgez(IType):
    """
    Branch on greater than equal zero: Conditionally branch the number of instructions specified by the offset if register rs is greater than or equal to 0.
    """
    def __init__(self, rs, label):
        super(Bgez, self).__init__('bgez', rs, label)


class Bgezal(IType):
    """
    Branch on greater than equal zero and link: Conditionally branch the number of instructions specified by the offset if register rs is greater than or equal to 0, then save the address of the next instruction in register 31.
    """ 
    def __init__(self, rs, label):
        super(Bgezal, self).__init__('bgezal', rs, label)


class Bgtz(IType):
    """
    Branch on greater than zero: Conditionally branch the number of instructions specified by the offset if register rs is greater than 0.
    """ 
    def __init__(self, rs, label):
        super(Bgtz, self).__init__('bgtz', rs, label)


class Blez(IType): 
    """
    Branch on less than equal zero: Conditionally branch the number of instructions specified by the offset if register rs is less than or equal to 0.
    """
    def __init__(self, rs, label):
        super(Blez, self).__init__('blez', rs, label)


class Bltz(IType): 
    """
    Branch on less than zero: Conditionally branch the number of instructions specified by the offset if register rs is less than 0.
    """
    def __init__(self, rs, label):
        super(Bltz, self).__init__('bltz', rs, label) 


class Bltzal(IType): 
    """
    Branch on less than zero and link: Conditionally branch the number of instructions specified by the offset if register rs is less than 0. Save the address of the next instruction in register 31.
    """
    def __init__(self, rs, label):
        super(Bltzal, self).__init__('bltzal', rs, label) 


class Bne(IType): 
    """
    Branch on not equal: Conditionally branch the number of instructions specified by the offset if register rs is not equal to rt. 
    """
    def __init__(self, rs, label):
        super(Bne, self).__init__('bne', rs, label) 


class Beqz(IType): 
    def __init__(self, rs, label):
        """
        Branch on equal zero: Conditionally branch to the instruction at the label if rs equals 0.
        """
        super(Beqz, self).__init__('beqz', rs, label) 


class Bnez(IType): 
    """
    Branch on not equal zero: Conditionally branch to the instruction at the label if register rs is not equal to 0.
    """
    def __init__(self, rs, label):
        super(Bnez, self).__init__('bnez', rs, label) 


class Bge(IType):
    """
    Branch on greater than equal signed: Conditionally branch to the instruction at the label if register rs1 is greater than or equal to rs2. Signed.
    """ 
    def __init__(self, rs1, rs2, label):
        super(Bge, self).__init__('bge', rs1, rs2, label) 


class Bgeu(IType):
    """
    Branch on greater than equal unsigned: Conditionally branch to the instruction at the label if register rs1 is greater than or equal to rs2. Unsigned.
    """  
    def __init__(self, rs1, rs2, label):
        super(Bgeu, self).__init__('bgeu', rs1, rs2, label) 


class Bgt(IType): 
    """
    Branch on greater than signed: Conditionally branch to the instruction at the label if register rs1 is greater than rs2. Signed.
    """
    def __init__(self, rs1, rs2, label):
        super(Bgt, self).__init__('bgt', rs1, rs2, label) 


class Bgtu(IType):
    """
    Branch on greater than unsigned: Conditionally branch to the instruction at the label if register rs1 is greater than rs2. Unsigned.
    """
    def __init__(self, rs1, rs2, label):
        super(Bgtu, self).__init__('bgtu', rs1, rs2, label) 


class Ble(IType): 
    """
    Branch on less than equal signed: Conditionally branch to the instruction at the label if register rs1 is less than or equal to rs2. Signed.
    """
    def __init__(self, rs1, rs2, label):
        super(Ble, self).__init__('ble', rs1, rs2, label) 


class Bleu(IType):
    """
    Branch on less than equal unsigned: Conditionally branch to the instruction at the label if register rs1 is less than or equal to rs2. Unsigned.
    """
    def __init__(self, rs1, rs2, label):
        super(Bleu, self).__init__('bleu', rs1, rs2, label) 


class Blt(IType): 
    """
    Branch on less than signed: Conditionally branch to the instruction at the label if register rs1 is less than rs2. Signed. 
    """
    def __init__(self, rs1, rs2, label):
        super(Blt, self).__init__('blt', rs1, rs2, label) 


class Bltu(IType):
    """
    Branch on less than unsigned: Conditionally branch to the instruction at the label if register rs1 is less than rs2. Unsigned. 
    """
    def __init__(self, rs1, rs2, label):
        super(Bltu, self).__init__('bltu', rs1, rs2, label) 



####### LOAD INSTRUCTIONS #######

class La(IType): 
    """
    Load address: Load computed address (not the contents of the location) into register rdest.
    """
    def __init__(self, rdest, address):
        super(La, self).__init__('la', rdest, address) 

 
class Lb(IType): 
    """
    Load byte signed: Load the byte at address into register rt. Signed.
    """
    def __init__(self, rt, address):
        super(Lb, self).__init__('lb', rt, address) 


class Lbu(IType):
    """
    Load byte unsigned: Load the byte at address into register rt. Unsigned.
    """
    def __init__(self, rt, address):
        super(Lbu, self).__init__('lbu', rt, address) 


class Lh(IType): 
    """
    Load halfword signed: Load the 16-bit quantity (halfword) at address into register rt. Signed.
    """
    def __init__(self, rt, address):
        super(Lh, self).__init__('lh', rt, address) 


class Lhu(IType):
    """
    Load halfword unsigned: Load the 16-bit quantity (halfword) at address into register rt. Unsigned.
    """
    def __init__(self, rt, address):
        super(Lhu, self).__init__('lhu', rt, address) 


class Lw(IType):
    """
    Load word: Load the 32-bit quantity (word) at address into register rt.
    """ 
    def __init__(self, rt, address):
        super(Lw, self).__init__('lw', rt, address) 


class Lwl(IType):
    """
    Load word: Load the left bytes from the word at the possibly unaligned address into register rt.
    """
    def __init__(self, rt, address):
        super(Lwl, self).__init__('lwl', rt, address)


class Lwr(IType):
    """
    Load word: Load the right bytes from the word at the possibly unaligned address into register rt.
    """
    def __init__(self, rt, address):
        super(Lwr, self).__init__('lwr', rt, address)


class Ld(IType): 
    """
    Load doubleword: Load the 64-bit quantity at address into registers rdest and rdest + 1.
    """
    def __init__(self, rdest, address):
        super(Ld, self).__init__('ld', rdest, address)

 
class Ulh(IType):
    """
    Unaligned load halfword signed: Load the 16-bit quantity (halfword) at the possibly unaligned address into register rdest. Signed.
    """ 
    def __init__(self, rdest, address):
        super(Ulh, self).__init__('ulh', rdest, address)  


class Ulhu(IType):
    """
    Unaligned load halfword unsigned: Load the 16-bit quantity (halfword) at the possibly unaligned address into register rdest. Unsigned.
    """ 
    def __init__(self, rdest, address):
        super(Ulhu, self).__init__('ulhu', rdest, address)        


class Ulw(IType):
    """
    Load the 32-bit quantity (word) at the possibly unaligned address into register rdest.
    """ 
    def __init__(self, rdest, address):
        super(Ulw, self).__init__('ulw', rdest, address)  



####### STORE INSTRUCTIONS #######

class Sb(IType):
    """
    Store byte: Store the low byte from register rt at address.
    """ 
    def __init__(self, rt, address):
        super(Sb, self).__init__('sb', rt, address) 


class Sh(IType):
    """
    Store halfword: Store the low halfword from register rt at address.
    """ 
    def __init__(self, rt, address):
        super(Sh, self).__init__('sh', rt, address) 


class Sw(IType):
    """
    Store word: Store the word from register rt at address.
    """ 
    def __init__(self, rt, address):
        super(Sw, self).__init__('sw', rt, address) 


class Swl(IType):
    """
    Store word: Store the left bytes from register rt at the possibly unaligned address.
    """
    def __init__(self, rt, address):
        super(Swl, self).__init__('swl', rt, address) 


class Swr(IType):
    """
    Store word: Store the right bytes from register rt at the possibly unaligned address.
    """
    def __init__(self, rt, address):
        super(Swr, self).__init__('swr', rt, address) 


class Sd(IType):
    """
    Store doubleword: Store the 64-bit quantity in registers rs and rs + 1 at address.
    """ 
    def __init__(self, rs, address):
        super(Sd, self).__init__('sd', rs, address) 


class Ush(IType): 
    """
    Unaligned store halfword: Store the low halfword from register rs at the possibly unaligned address.
    """
    def __init__(self, rs, address):
        super(Ush, self).__init__('ush', rs, address) 


class Usw(IType):
    """
    Unaligned store word: Store the word from register rs at the possibly unaligned address.
    """ 
    def __init__(self, rs, address):
        super(Usw, self).__init__('usw', rs, address) 



############################### JUMP TYPE INSTRUCTIONS ##############################


class J(IType):
    """
    Jump: Unconditionally jump to the instruction at target.
    """ 
    def __init__(self, target):
        super(J, self).__init__('j', target) 


class Jal(IType):
    """
    Jump: Same as before and save the address of the next instruction in register rd (defaults to 31). 
    """ 
    def __init__(self, target):
        super(Jal, self).__init__('jal', target) 


class Jr(IType):
    """
    Jump register: Unconditionally jump to the instruction whose address is in register rs. 
    """ 
    def __init__(self, rs):
        super(Jr, self).__init__('jr', rs)


class Jalr(IType):
    """
    Jump and link register: Unconditionally jump to the instruction whose address is in register rs. Save the address of the next instruction in register rd.
    """ 
    def __init__(self, rs, rd):
        super(Jalr, self).__init__('jalr', rs, rd)



############################### REGISTER TYPE INSTRUCTIONS ##############################

####### ARITHMETIC AND LOGIC #######

class Abs(IType): 
    """
    Absolute value: Put the absolute value of register rs in register rd.
    """
    def __init__(self, rd, rs):
        super(Abs, self).__init__('abs', rd, rs)


 
class Mult(IType):
    """
    Multiply signed: Multiply registers rs and rt. Leave the low-order word of the product in register lo and the high-order word in register hi. Signed.
    """
    def __init__(self, rs, rt):
        super(Mult, self).__init__('mult', rs, rt)


class Multu(IType):
    """
    Multiply unsigned: Multiply registers rs and rt. Leave the low-order word of the product in register lo and the high-order word in register hi. Unsigned.
    """
    def __init__(self, rs, rt):
        super(Multu, self).__init__('multu', rs, rt)


#Multiply: Put the product of register rs and rt into register rd 
class Mul(IType): 
    """
    Multiply: Put the product of register rs and rt into register rd. Signed multiply without overflow.
    """
    def __init__(self, rd, rs, rt):
        super(Mul, self).__init__('mul', rd, rs, rt)


class Mulo(IType):
    """
    Multiply: Put the product of register rs and rt into register rd. Signed multiply with overflow.
    """
    def __init__(self, rd, rs, rt):
        super(Mulo, self).__init__('mulo', rd, rs, rt)


class Mulou(IType):
    """
    Multiply: Put the product of register rs and rt into register rd. Unsigned multiply with overflow.
    """
    def __init__(self, rd, rs, rt):
        super(Mulou, self).__init__('mulou', rd, rs, rt)


class Neg(IType): # with overflow
    """
    Negate: Put the negative of register rs into register rd. With overflow.
    """
    def __init__(self, rd, rs):
        super(Neg, self).__init__('neg', rd, rs)


class Negu(IType):
    """
    Negate: Put the negative of register rs into register rd. Without overflow.
    """
    def __init__(self, rd, rs):
        super(Negu, self).__init__('negu', rd, rs)


class Add(IType):
    """
    Addition: Put the sum of registers rs and rt into register rd. With overflow.
    """
    def __init__(self, rd, rs, rt):
        super(Add, self).__init__('add', rd, rs, rt)


class Addu(IType):
    """
    Addition: Put the sum of registers rs and rt into register rd. Without overflow.
    """
    def __init__(self, rd, rs, rt):
        super(Addu, self).__init__('addu', rd, rs, rt)


class Sub(IType):
    """
    Substraction: Put the difference of registers rs and rt into register rd. With overflow.
    """
    def __init__(self, rd, rs, rt):
        super(Sub, self).__init__('sub', rd, rs, rt)


class Subu(IType):
    """
    Substraction: Put the difference of registers rs and rt into register rd. Without overflow.
    """
    def __init__(self, rd, rs, rt):
        super(Subu, self).__init__('subu', rd, rs, rt)


class Not(IType): 
    """
     Put the bitwise logical negation of register rs into register rd.
    """
    def __init__(self, rd, rs):
        super(Not, self).__init__('not', rd, rs)


class And(IType):
    """
    Put the logical AND of registers rs and rt into register rd
    """
    def __init__(self, rd, rs, rt):
        super(And, self).__init__('and', rd, rs, rt)


class Or(IType):
    """
    Put the logical OR of registers rs and rt into register rd
    """
    def __init__(self, rd, rs, rt):
        super(Or, self).__init__('or', rd, rs, rt)

 
class Nor(IType):
    """
    Put the logical NOR of registers rs and rt into register rd
    """
    def __init__(self, rd, rs, rt):
        super(Nor, self).__init__('nor', rd, rs, rt)


class Xor(IType):
    """
    Put the logical XOR of registers rs and rt into register rd 
    """
    def __init__(self, rd, rs, rt):
        super(Xor, self).__init__('xor', rd, rs, rt)


class Div(IType):
    """
    Divide (2 parameters):  Divide register rs by register rt. Leave the quotient in register lo and the remainder in register hi. With overflow.
    Divide (3 parameters):  Put the quotient of register nd and rd into register rs. With overflow.
    """
    def __init__(self, rs, nd, rd = None):
        super(Div, self).__init__('div', rs, nd, rd)


class Divu(IType):
    """
    Divide (2 parameters):  Divide register rs by register rt. Leave the quotient in register lo and the remainder in register hi. Without overflow.
    Divide (3 parameters):  Put the quotient of register nd and rd into register rs. Without overflow.
    """
    def __init__(self, rs, nd, rd = None):
        super(Divu, self).__init__('divu', rs, nd, rd)


class Rem(IType): 
    """
    Remainder: Put the remainder of register rsrc1 divided by register rsrc2 into register rdest. Signed.
    """
    def __init__(self, rdest, rsrc1, rsrc2):
        super(Rem, self).__init__('rem', rdest, rsrc1, rsrc2)


class Remu(IType):
    """
    Remainder: Put the remainder of register rsrc1 divided by register rsrc2 into register rdest. Unsigned.
    """
    def __init__(self, rdest, rsrc1, rsrc2):
        super(Remu, self).__init__('remu', rdest, rsrc1, rsrc2)


class Sll(IType): 
    """
    Shift left logical: Shift register rt left by the distance indicated by immediate shamt and put the result in register rd.
    """
    def __init__(self, rd, rt, shamt):
        super(Sll, self).__init__('sll', rd, rt, shamt)


class Sllv(IType):
    """
    Shift left logical: Shift register rt left by the distance indicated by the register rs and put the result in register rd.
    """ 
    def __init__(self, rd, rt, rs):
        super(Sllv, self).__init__('sllv', rd, rt, rs)


class Sra(IType):
    """
    Shift right aritmethic: Shift register rt right by the distance indicated by immediate shamt and put the result in register rd.
    """ 
    def __init__(self, rd, rt, shamt):
        super(Sra, self).__init__('sra', rd, rt, shamt)


class Srav(IType):
    """
    Shift right aritmethic: Shift register rt right by the distance indicated by the register rs and put the result in register rd.
    """ 
    def __init__(self, rd, rt, rs):
        super(Srav, self).__init__('srav', rd, rt, rs)


class Srl(IType):
    """
    Shift right logical: Shift register rt right by the distance indicated by immediate shamt and put the result in register rd.
    """ 
    def __init__(self, rd, rt, shamt):
        super(Srl, self).__init__('srl', rd, rt, shamt)


class Srlv(IType):
    """
    Shift right logical: Shift register rt right by the distance indicated by the register rs and put the result in register rd.
    """ 
    def __init__(self, rd, rt, rs):
        super(Srlv, self).__init__('srlv', rd, rt, rs)


class Rol(IType):
    """
    Rotate: Rotate register rsrc1 left by the distance indicated by rsrc2 and put the result in register rdest. 
    """
    def __init__(self, rdest, rsrc1, rsrc2):
        super(Rol, self).__init__('rol', rdest, rsrc1, rsrc2)


class Ror(IType):
    """
    Rotate: Rotate register rsrc1 right by the distance indicated by rsrc2 and put the result in register rdest. 
    """
    def __init__(self, rdest, rsrc1, rsrc2):
        super(Ror, self).__init__('ror', rdest, rsrc1, rsrc2)


####### COMPARISON #######

class Slt(IType):
    """
    Set less than: Set register rd to 1 if register rs is less than  rt , and to 0 otherwise. Signed.
    """ 
    def __init__(self, rd, rs, rt):
        super(Slt, self).__init__('slt', rd, rs, rt)


class Sltu(IType):
    """
    Set less than: Set register rd to 1 if register rs is less than  rt , and to 0 otherwise. Unsigned.
    """ 
    def __init__(self, rd, rs, rt):
        super(Sltu, self).__init__('sltu', rd, rs, rt)


class Seq(IType):
    """
    Set equal: Set register rdest to 1 if register rsrc1 equals rsrc2, and to 0 otherwise.
    """ 
    def __init__(self, rdest, rsrc1, rsrc2 ):
        super(Seq, self).__init__('seq', rdest, rsrc1, rsrc2)


class Sne(IType):
    """
    Set not equal: Set register rdest to 1 if register rsrc1 is not equal to rsrc2, and to 0 otherwise.
    """ 
    def __init__(self, rdest, rsrc1, rsrc2 ):
        super(Sne, self).__init__('sne', rdest, rsrc1, rsrc2)


class Sge(IType):
    """
    Set greater than equal: Set register rdest to 1 if register rsrc1 is greater than or equal to rsrc2, and to 0 otherwise. Signed.
    """ 
    def __init__(self, rdest, rsrc1, rsrc2 ):
        super(Sge, self).__init__('sge', rdest, rsrc1, rsrc2)


class Sgeu(IType):
    """
    Set greater than equal: Set register rdest to 1 if register rsrc1 is greater than or equal to rsrc2, and to 0 otherwise. Unsigned.
    """ 
    def __init__(self, rdest, rsrc1, rsrc2 ):
        super(Sgeu, self).__init__('sgeu', rdest, rsrc1, rsrc2)


class Sgt(IType): 
    """
    Set greater than: Set register rdest to 1 if register rsrc1 is greater than rsrc2, and to 0 otherwise. Signed.
    """
    def __init__(self, rdest, rsrc1, rsrc2 ):
        super(Sgt, self).__init__('sgt', rdest, rsrc1, rsrc2)


class Sgtu(IType): 
    """
    Set greater than: Set register rdest to 1 if register rsrc1 is greater than rsrc2, and to 0 otherwise. Unsigned.
    """
    def __init__(self, rdest, rsrc1, rsrc2 ):
        super(Sgtu, self).__init__('sgtu', rdest, rsrc1, rsrc2)


class Sle(IType): 
    """
    Set less than equal: Set register rdest to 1 if register rsrc1 is less than or equal to rsrc2, and to 0 otherwise. Signed.
    """
    def __init__(self, rdest, rsrc1, rsrc2 ):
        super(Sle, self).__init__('sle', rdest, rsrc1, rsrc2)


class Sleu(IType):
    """
    Set less than equal: Set register rdest to 1 if register rsrc1 is less than or equal to rsrc2, and to 0 otherwise. Unsigned.
    """
    def __init__(self, rdest, rsrc1, rsrc2 ):
        super(Sleu, self).__init__('sleu', rdest, rsrc1, rsrc2)


####### MOVE INSTRUCTIONS #######

class Move(IType):
    """
    Move register  rsrc to  rdest.
    """
    def __init__(self, rdest, rsrc):
        super(Move, self).__init__('move', rdest, rsrc)


class Mfhi(IType):
    """
    Move from the register hi to the rd register.
    """ 
    def __init__(self, rd):
        super(Mfhi, self).__init__('mfhi', rd)


class Mflo(IType): 
    """
    Move from the register lo to the rd register.
    """ 
    def __init__(self, rd):
        super(Mflo, self).__init__('mflo' , rd)


class Mthi(IType):
    """
    Move register rs to the hi register.
    """ 
    def __init__(self):
        super(Mthi, self).__init__('mthi')


class Mtlo(IType): 
    """
    Move register rs to the lo register.
    """ 
    def __init__(self):
        super(Mtlo, self).__init__('mtlo')



############################### EXCEPTION AND INTERRUPT INSTRUCTIONS ##############################      

class Rfe(IType):
    """
    Return from exception: Restore the Status register.
    """
    def __init__(self):
        super(Rfe, self).__init__('rfe')


class Syscall(IType):
    """
    System call: Register $v0 contains the number of the system call (see Figure A.17) provided by SPIM.
    """
    def __init__(self):
        super(Syscall, self).__init__('syscall')


class Break(IType):
    """
    Break: Cause exception code. Exception 1 is reserved for the debugger.
    """
    def __init__(self):
        super(Break, self).__init__('break')


class Nop(IType):
    """
    No operation: Do nothing.
    """
    def __init__(self):
        super(Nop, self).__init__('nop')