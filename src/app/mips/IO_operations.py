IO_operations='''
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


read_str_new_block:
    addiu $t0 $gp free_list

read_str_new_block_search_last:
    lw $t1 header_next_slot($t0)
    beq $t1 $zero read_str_new_block_create
    move $t0 $t1
    j read_str_new_block_search_last

read_str_new_block_create:
    move $a0 $t0
    li $a1 alloc_size
    jal extend_heap
    jal expand_block
    lw $t2 header_next_slot($a0)
    beq $t2 $zero read_str_new_block_expanded
    lw $t1 header_size_slot($t2)
    j read_str_reading

read_str_new_block_expanded:
    move $t2 $a0
    lw $t1 header_size_slot($a0)
    j read_str_reading'''