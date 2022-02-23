#registers
class registers:

    zero = '$zero' # constant 0
    
    # arguments 1, 2, 3, 4
    a0 = '$a0'
    a1 = '$a1'
    a2 = '$a2'
    a3 = '$a3'
    
    # expression evaluation and result of a function
    v0 = '$v0' 
    v1 = '$v1'
    
    # saved temporary (preserved across call)
    s0 = '$s0'
    s1 = '$s1'
    s2 = '$s2'
    s3 = '$s3'
    s4 = '$s4'
    s5 = '$s5'
    s6 = '$s6'
    s7 = '$s7'
    
    # temporary (not preserved across call)
    t0 = '$t0'
    t1 = '$t1'
    t2 = '$t2'
    t3 = '$t3'
    t4 = '$t4'
    t5 = '$t5'
    t6 = '$t6'
    t7 = '$t7'
    t8 = '$t8'
    t9 = '$t9'

    gp = '$gp' # pointer to global area
    sp = '$sp' # stack pointer
    fp = '$fp' # frame pointer
    ra = '$ra' # return address

#operations 
class operations:

    la = 'la' # la rdest, address -> load computed address (not the content of the location) into rdest  
    lb = 'lb' # lb rt, address -> load the byte at address into rt
    lbu = 'lbu' # lbu rt, address -> lb unsigned
    lh = 'lh' # lh rt, address -> load the 16-bit quantity (halfword) at address into rt 
    lhu = 'lhu' # lhu rt, address -> lh unsigned
    lw = 'lw' # lw rt, address -> load the word at address into rt
    lwcz = 'lwcz' # lwcz rt, address -> load the word at address into rt of coprocessor z (0-3)
    lwl = 'lwl' # lwl rt, address -> load the left bytes from the word at the possibly unaligned address into rt
    lwr = 'lwr' # lwr rt, address -> load the right bytes from the word at the possibly unaligned address into rt
    ld = 'ld' # ld rdest, address -> load the 64-bit quantity at address into rdest and rdest + 1
    ulh = 'ulh' # ulh rdest, address -> load the 16-bit quantity (halfword) at the possibly unaligned address into rdest
    ulhu = 'ulhu' # ulhu rdest, address -> ulh unsigned
    ulw = 'ulw' # ulw rdest, address -> load the 32-bit quantity (word) at the possibly unaligned address into rdest
    sb = 'sb' # sb rt, address -> store the low byte from rt at address
    sh = 'sh' # sh rt, address -> store the low halfword from rt at address
    sw = 'sw' # sw rt, address -> store the word from rt at address
    swcz = 'swcz' # swcz rt, address -> store the word from rt of coprocessor z at address
    swl = 'swl' # swl rt, address -> store the left bytes from rt at the possibly unaligned address
    swr = 'swr' # swr rt, address -> store the right bytes from rt at the possibly unaligned address
    sd = 'sd' # sd rsrc, address -> store the 64-bit quantity in registers rsrc and rsrc + 1 at address
    ush = 'ush' # ush rsrc, address -> stores the low halfword from rsrc at the possibly unaligned address
    usw = 'usw' # usw rsrc, address -> stores the word from rsrc at the possibly unaligned address

    abs = 'abs'  # abs rdest, rsrc -> put absolute value of rsrc into rdest
    add = 'add' # add rd, rs, rt -> put sum of rs and rt into rd (with overflow)
    addu = 'addu' # addu rd, rs, rt -> add  without overflow
    addi = 'addi' # add rt, rs, imm -> put the sum of rs and sign-extended imm into rt (with overflow)
    addiu = 'addiu' # add rt, rs, imm -> addi without overflow
    and_bw = 'and' # and rd, rs, rt -> put the logical AND of rs and rt into rd
    andi = 'andi' # andi rt, rs, imm -> put the logical AND of rs and the zero-extended imm into rt
    div = 'div' # div rs, rt -> divide rs by rt. leaves quotient in register lo and reminder in register hi (with overflow)
    divu = 'divu' # divu rdest, rsrc1, src2 -> put the quotient of register rsrc1 and src2 into rdest (without overflow) 
    mult = 'mult' # mult rs, rt -> multiply rs and rt. leaves the low-order word in lo and high-order word in hi
    multu = 'multu' # multu rs, rt -> multiply rs and rt. leaves the low-order word in lo and high-order word in hi (unsigned)
    mul = 'mul' # mul rdest, rsrc1, src2 -> put the product of the register rsrc1 and src2 into rdest (without overflow)
    mulo = 'mulo' # mul rdest, rsrc1, src2 -> mul with overflow
    mulou = 'mulou' # mul rdest, rsrc1, src2 -> mulo unsigned
    mulu = 'mulu' # 
    neg = 'neg' # neg rdest, rsrc -> put the negative of register rsrc into rdest (with overflow)
    negu = 'negu' # negu rdest, rsrc -> neg without overflow
    nor = 'nor' # nor rd, rs, rt -> put the logical NOR of registers rs and rt into register rd
    not_bw = 'not' # not rdest, rsrc -> put the bitwise logical negation of the register rsrc into register rdest
    or_bw = 'or' # or rd, rs, rt -> put the logical OR of registers rs and rt into register rd revisar
    ori = 'ori' # ori rt, rs, imm -> put the logical OR of register rs and the zero-extended imm into register rt
    rem = 'rem' # rem rdest, rsrc1, rsrc2 -> put the reminder of divide rsrc1 and rsrc2 into rdest
    remu = 'remu' # remu rdest, rsrc1, rsrc2 -> put the reminder of divide rsrc1 and rsrc2 int rdest (unsigned)
    sll = 'sll' # sll rd, rt, shamt -> shift register rt left by the distance indicated by shamt and put result in rd
    sllv = 'sllv' # sllv rd, rt, rs -> shift register rt left by the distance indicated by rs and put result in rd
    sra = 'sra' # sra rd, rt, shamt -> shift register rt right by the distance indicated by shamt and put result in rd
    srav = 'srav' # srav rd, rt, rs -> shift register rt right by the distance indicated by rs and put result in rd
    srl = 'srl' # srl rd, rt, shamt -> shift register rt right by the distance indicated by shamt and put result in rd
    srlv = 'srlv' # srlv rd, rt, rs -> shift register rt right by the distance indicated by rs and put result in rd
    rol = 'rol' # rol rdest, rsrc1, rsrc2 -> rotate register rsrc1 left by the distance rsrc2 and put the result in rdest
    ror = 'ror' # ror rdest, rsrc1, rsrc2 -> rotate register rsrc1 right by the distance rsrc2 and put the result in rdest
    sub = 'sub' # sub rd, rs, rt -> put the difference of registers rs and rt into register rd (with overflow)
    subu = 'subu' # subu rd, rs, rt -> sub without overflow
    xor = 'xor' # xor rd, rs, rt -> put the logical XOR of registers rs and rt into register rd
    xori = 'xori' # xor rt, rs, imm -> put the logical XOR of register rs and the zero-extended imm into register rt

    lui = 'lui' # lui rt, imm -> load the lower halfword of imm into the upper halfword of rt, the lower bits of rt are set to 0
    li = 'li' # li rdest, imm -> move the imm into the register rdest
    lid = 'li.d'
    lis = 'li.s'

    slt = 'slt' # slt rd, rs, rt -> set rd to 1 if rs is less than rt, and to 0 otherwise
    sltu = 'sltu' # sltu rd, rs, rt -> slt unsigned
    slti = 'slti' # slt rd, rs, imm -> set rd to 1 if rs is less than the signed-extended imm, and to 0 otherwise
    sltiu = 'sltiu' # sltiu rd, rs, imm -> slti unsigned
    seq = 'seq' # seq rdest, rsrc1, rsrc2 -> set rdest to 1 if rsrc1 equals to rsrc2, 0 otherwise
    sge = 'sge' # sge rdest, rsrc1, rsrc2 -> set rdest to 1 if rsrc1 greater than or equals to rsrc2, 0 otherwise
    sgeu = 'sgeu' # sgeu rdest, rsrc1, rsrc2 -> sge unsigned
    sgt = 'sgt' # sgt rdest, rsrc1, rsrc2 -> set rdest to 1 if rsrc1 greater than to rsrc2, 0 otherwise
    sgtu = 'sgtu' # sgtu rdest, rsrc1, rsrc2 -> sgt unsigned
    sle = 'sle' # sle rdest, rsrc1, rsrc2 -> set rdest to 1 if rsrc1 less than or equal to rsrc2, 0 otherwise
    sleu = 'sleu' # sleu rdest, rsrc1, rsrc2 -> sle unsigned
    sne = 'sne' # sne rdest, rsrc1, rsrc2 -> set rdest to 1 if rsrc1 not equal to rsrc2, 0 otherwise

    b = 'b' # b label -> unconditionally branch to the instruction at the label
    bczt = 'bczt' # bczt offset -> conditionally branch the number of instructions specified by the offset if z's condition flag is true. z is 0, 1, 2, or 3.
    bczf = 'bczf' # bczf offset -> conditionally branch the number of instructions specified by the offset if z's condition flag is false. z is 0, 1, 2, or 3.
    beq = 'beq' # beq rs, rt, offset -> conditionally branch  the number of instructions specified by the offset if rs is equal rt
    bgez = 'bgez' # bgez rs, offset -> conditionally branch the number of instructions specified by the offset if rs is greater than or equal to 0
    bgezal = 'bgezal' # bgezal rs, offset -> conditionally branch the number of instructions specified by the offset if rs is greater than or equal to 0. save the address of next instruction in register 31
    bgtz = 'bgtz' # bgtz rs, offset -> conditionally branch the number of instructions specified by the offset if rs is greater than 0
    blez = 'blez' # blez rs, offset -> conditionally branch the number of instructions specified by the offset if rs is less than or equal to 0
    bltzal = 'bltzal' # bltzal rs, offset -> conditionally branch the number of instructions specified by the offset if rs is less than 0. save the address of next instruction in register 31
    bltz = 'bltz' # bltz rs, offset -> conditionally branch the number of instructions specified by the offset if rs is less than 0
    bne = 'bne' # bne rs, rt, offset -> conditionally branch the number of instructions specified by the offset if rs is not equal to rt

    beqz = 'beqz' # beqz rsrc, label -> conditionally branch to the label if rsrc equals to 0
    bge = 'bge' # bge rsrc1, rsrc2, label -> conditionally branch to the label if rsrc1 is greater than or equal to rsrc2
    bgeu = 'bgeu' # bgeu rsrc1, rsrc2, label -> bge unsigned
    bgt = 'bgt' # bgt rsrc1, rsrc2, label -> conditionally branch to the label if rsrc1 is greater than rsrc2
    bgtu = 'bgtu' # bgtu rsrc1, rsrc2, label -> bgt unsigned
    ble = 'ble' # ble rsrc1, rsrc2, label -> conditionally branch to the label if rsrc1 is less than or equal to rsrc2
    bleu = 'bleu' # bleu rsrc1, rsrc2, label -> ble unsigned
    blt = 'blt' # blt rsrc1, rsrc2, label -> conditionally branch to the label if rsrc1 is less than rsrc2
    bltu = 'bltu' # bltu rsrc1, rsrc2, label -> blt unsigned
    bnez = 'bnez' # bnez rsrc, label -> conditionally branch to the label if rsrc1 is not equal to 0

    j = 'j' # j target -> unconditionally jumps to target
    jal = 'jal' # jal target, rd -> unconditionally jumps to target. Save the address of next instruction in rd
    jalr = 'jalr' # jalr rs, rd -> unconditionally jumps to the instruction whose address is in rs. save the address of next instruction in rd (defaults is 31)
    jr = 'jr' # jr rs-> unconditionally jumps to the instruction whose address is in rs.

    move = 'move' # move rdest, rsrc -> move rsrc to rdest 
    mfhi = 'mfhi' # mfhi rd -> move the hi register to rd
    mflo = 'mflo' # mflo rd -> move the lo register to rd
    mthi = 'mthi' # mthi rs -> move the rs register to hi
    mtlo = 'mtlo' # mtlo rs -> move the rs register to lo
    mfcz = 'mfcz' # mfcz rt, rd -> move coprocessor z's register rt to CPU register rt
    mfc1d = 'mfc1.d' # mfc1.d rdest, frsrc1 -> move floating-point registers frsrc1 and frsrc1 + 1 to CPU registers rdest and rdest + 1
    mtcz = 'mtcz' # mtcz rd, rt -> move CPU register rt to coprocessor z's register rd

    rfe = 'rfe' # rfe -> restore the status register
    syscall = 'syscall' # register $v0 contains the number of the system call provided by spim
    brk = 'break' # break cause exception code. Exception 1 is reserved for the debugger
    nop = 'nop' # nop -> do nothing :)

#types
class datatype:
    ascii = '.ascii'
    asciiz = '.asciiz'
    space = '.space'
    align = '.align'
    byte = '.byte'
    word = '.word'
    half = '.half'
    double = '.double'
    floatt = '.float'
    