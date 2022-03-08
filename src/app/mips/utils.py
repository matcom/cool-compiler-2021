auxiliar_functions='''
equals:
    beq $a0 $a1 equals_equal
    li $v0 0
    j equals_end
    
equals_equal:
    li $v0 1

equals_end:
    jr $ra

less_equal:
    ble $a0 $a1 less_equal_true
    li $v0 0
    j less_equal_end

less_equal_true:
    li $v0 1

less_equal_end:
    jr $ra

    
less:
    blt $a0 $a1 less_true
    li $v0 0
    j less_end

less_true:
    li $v0 1

less_end:
    jr $ra

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

read_str:
    addiu $sp $sp -36
    sw $t0 0($sp)
    sw $t1 4($sp)
    sw $t2 8($sp)
    sw $t3 12($sp)
	sw $t4 16($sp)
	sw $t5 20($sp)
    sw $a0 24($sp)
    sw $a1 28($sp)
    sw $ra 32($sp)
	
    addiu $t0 $gp free_list
    move $t1 $zero
    move $t2 $t0

read_str_larger_block_loop:
    lw $t0 header_next_slot($t0)
    beq $t0 $zero read_str_reading
    lw $t3 header_size_slot($t0)
    bge $t1 $t3 read_str_larger_block_loop
    move $t1 $t3
    move $t2 $t0
    j read_str_larger_block_loop

read_str_reading:
    beq $t1 $zero read_str_new_block
    move $a1 $t1
    li $v0 8
    addiu $a0 $t2 header_size
    syscall
    move $t0 $a0
    move $t1 $zero

read_str_look_nl:
    lb $t2 0($t0)
    beq $t2 new_line read_str_nl_founded
    beq $t2 $zero read_str_zero_founded#read_str_no_nl
    addi $t1 $t1 1
    addi $t0 $t0 1
    j read_str_look_nl

read_str_zero_founded:
    blt $t1 $t3 read_str_nl_founded
    j read_str_no_nl

read_str_nl_founded:
    sb $zero 0($t0)
    addi $t1 $t1 1
	li $t2 4
	div $t1 $t2
	mfhi $t3
	beq $t3 $zero read_str_nl_founded_alligned
	sub $t2 $t2 $t3
	add $t1 $t1 $t2
read_str_nl_founded_alligned:
    move $a1 $t1
    addiu $a0 $a0 neg_header_size
    jal split_block
    jal use_block

    addiu $v0 $a0 header_size
	j read_str_end


read_str_no_nl:
	addi $t1 $t1 1
    blt $t1 str_size_treshold read_str_dup
	addi $t1 $t1 alloc_size
	j read_str_extend_heap
read_str_dup:
	sll $t1 $t1 1
read_str_extend_heap:
	move $a1 $t1
	move $t0 $a0
	addiu $a0 $gp free_list

read_str_last_block_loop:
	lw $t1 header_next_slot($a0)
	beq $t1 $zero read_str_last_block_founded
	lw $a0 header_next_slot($a0)
	j read_str_last_block_loop

read_str_last_block_founded:
	jal extend_heap
	jal expand_block
	lw $t1 header_next_slot($a0)
	bne $t1 $zero read_str_copy_prev
	move $t1 $a0

read_str_copy_prev:
	lw $t3 header_size_slot($t1)
	move $t2 $zero
	move $t5 $t1
	addiu $t1 $t1 header_size

read_str_copy_loop:
	lb $t4 0($t0)
	beq $t4 $zero read_str_copy_end
	sb $t4 0($t1)
	addi $t2 $t2 1
	addi $t0 $t0 1
	addi $t1 $t1 1
	j read_str_copy_loop

read_str_copy_end:
	sub $t3 $t3 $t2
	move $a0 $t1
	move $a1 $t3
	li $v0 8
	syscall
	move $t0 $a0
	move $t1 $t2
	addiu $a0 $t5 header_size
	j read_str_look_nl

	
read_str_end:
    lw $t0 0($sp)
    lw $t1 4($sp)
    lw $t2 8($sp)
    lw $t3 12($sp)
	lw $t4 16($sp)
	lw $t5 20($sp)
    lw $a0 24($sp)
    lw $a1 28($sp)
    lw $ra 32($sp)
    addiu $sp $sp 36

    jr $ra
        '''