string_operations ='''
len:
    addiu $sp $sp -8
    sw $t0 0($sp)
    sw $t1 4($sp)

    move $t0 $a0
    move $v0 $zero

len_loop:
    lb $t1 0($t0)
    beq $t1 $zero len_end
    addi $v0 $v0 1
    addiu $t0 $t0 1
    j len_loop

len_end:
    lw $t0 0($sp)
    lw $t1 4($sp)
    addiu $sp $sp 8

    jr $ra

concat:
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
    addiu $a0 $a2 1

concat_size_alligned:
    jal malloc
    move $t2 $v0
    j concat_copy_first_loop

concat_allign_size:
    sub $t2 $t2 $a0
    add $a0 $a2 $t2
    addiu $a0 $a0 1
    j concat_size_alligned

concat_copy_first_loop:
    lb $a0 0($t0)
    beq $a0 $zero concat_copy_second_loop
    sb $a0 0($t2)
    addiu $t0 $t0 1
    addiu $t2 $t2 1
    j concat_copy_first_loop

concat_copy_second_loop:
    lb $a0 0($t1)
    beq $a0 $zero concat_end
    sb $a0 0($t2)
    addiu $t1 $t1 1
    addiu $t2 $t2 1
    j concat_copy_second_loop

concat_end:
    sb $zero 0($t2)
    lw $t0 0($sp)
    lw $t1 4($sp)
    lw $t2 8($sp)
    lw $a0 12($sp)
    lw $a1 16($sp)
    lw $ra 20($sp)
    addiu $sp $sp 24

    jr $ra


substr:
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
    bne $t2 $zero substr_allign_size
    move $t1 $t3
    j substr_new_block

substr_allign_size:
    sub $t1 $t1 $t2
    add $t1 $t1 $t3

substr_new_block:
    move $a0 $t1
    jal malloc
    move $t3 $v0
    move $t1 $zero
    addu $t0 $t0 $a1

substr_copy_loop:
    beq $t1 $a2 substr_end
    lb $t2 0($t0)
    sb $t2 0($t3)
    addiu $t0 $t0 1
    addiu $t3 $t3 1
    addiu $t1 $t1 1
    j substr_copy_loop

substr_end:
    sb $zero 0($t3)
    lw $t0 0($sp)
    lw $t1 4($sp)
    lw $t2 8($sp)
    lw $t3 12($sp)
    lw $a0 16($sp)
    lw $ra 20($sp)
    addiu $sp $sp 24

    jr $ra


equal_str:
    addiu $sp $sp -16
    sw $t0 0($sp)
    sw $t1 4($sp)
    sw $t2 8($sp)
    sw $t3 12($sp)

    move $t0 $a0
    move $t1 $a1

equal_str_loop:
    lb $t2 0($t0)
    lb $t3 0($t1)
    bne $t2 $t3 equal_str_not_equal
    beq $t2 $zero equal_str_equal

    addiu $t0 $t0 1
    addiu $t1 $t1 1
    j equal_str_loop

equal_str_not_equal:
    move $v0 $zero
    j equal_str_end

equal_str_equal:
    li $v0 1

equal_str_end:
    lw $t0 0($sp)
    lw $t1 4($sp)
    lw $t2 8($sp)
    lw $t3 12($sp)
    addiu $sp $sp 16

    jr $ra
    '''