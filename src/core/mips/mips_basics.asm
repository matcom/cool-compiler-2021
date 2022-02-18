
# Args:
# $a0 size to alloc
# Return:
# $v0 address of allocated block


# v1 address of empty memory
# a0 size to alloc
# v0 return memory address

#TODO Parametros en la pila
malloc:
    move $v0 $v1
    add $v1 $a0 $v1

    jr $ra


# COPY
# $a0 address from
# $a1 address to
# $a2 size

copy:
    addiu $sp $sp -16                                # Save content of registers in sp
    sw $a0 0($sp)
    sw $a1 4($sp)
    sw $a2 8($sp)
    sw $t0 12($sp)

copy_loop:
    beq $a2 $zero copy_end                           # Copy finished (copy size is 0)
    lw $t0 0($a0)                                    # Load in t0 content of source address a0
    sw $t0 0($a1)                                    # Save in destiny a1 content of t0
    addiu $a0 $a0 4                                  # Increase source address a0
    addiu $a1 $a1 4                                  # Increase destiny addres a1
    addi $a2 $a2 -4                                  # Decrease copy size
    j copy_loop

copy_end:
    lw $a0 0($sp)                                    # Return original content to registers
    lw $a1 4($sp)
    lw $a2 8($sp)
    lw $t0 12($sp)
    addiu $sp $sp 16

    jr $ra




# LEN
# a0 begin address
# return size in v0
length:
    # Save content of registers
    addiu $sp $sp -8
    sw $t0 0($sp)
    sw $t1 4($sp)

    move $t0 $a0                                     # Move to t0 the address to begin
    move $v0 $zero                                   # Set v0 to zero

len_loop:
    lb $t1 0($t0)                                    # Save in t1 first byte of address
    beq $t1 $zero len_end                            # Finish object if t1 is zero
    addi $v0 $v0 1                                   # Increase count in v0
    addiu $t0 $t0 1                                  # Increase address pointer
    j len_loop                                       # Finish loop

len_end:
    # Return original content to registers
    lw $t0 0($sp)
    lw $t1 4($sp)
    addiu $sp $sp 8

    jr $ra


# TODO: Necesita tambien un puntero al indice del substring en a1
# SUBSTRING
# a0 Pointer to beginning of string
# a1 Pointer to beginning of substring
# a2 Size of substring


substr:
    # Save content of registers
    addiu $sp $sp -32
    sw $t0 0($sp)
    sw $t1 4($sp)
    sw $t2 8($sp)
    sw $t3 12($sp)
    sw $a0 16($sp)
    sw $a1 20($sp)
    sw $a2 24($sp)
    sw $ra 28($sp)

    move $t0 $a0                                     # t0 points to beginning o string
    add $t0 $t0 $a1
    li $t1 4                                         # t1 Word size

    div $a2 $t1                                      # Size of substring / wordsize
    mfhi $t2                                         # t2 holds remainder of division

    bne $t2 $zero substr_allign_size                 # Branch if division is not exact
    move $t1 $a2                                     # t1 size of substring
    j substr_new_block

substr_allign_size:
    sub $t1 $t1 $t2                                  # Convert t1 to multiple of 4 to...
    add $t1 $t1 $a2                                  # reserve memory via malloc

substr_new_block:
    move $a0 $t1                                     # Store in a0 size of space to reserve via malloc
    jal malloc                                       # Malloc
    move $t3 $v0                                     # Pointer to beginning of reserved space
    move $t1 $zero                                   # Count

substr_copy_loop:
    beq $t1 $a2 substr_end                           # Copy finished
    lb $t2 0($t0)                                    # Load byte from string into t2 temporal
    sb $t2 0($t3)                                    # Savebyte from t2 into t3
    addiu $t0 $t0 1                                  # Increase pointer to string
    addiu $t3 $t3 1                                  # Increase pointer to reserved space
    addiu $t1 $t1 1                                  # Increase count
    j substr_copy_loop

substr_end:
    sb $zero 0($t3)                                  # Set next byte of substring to zero

    # Return original values to registers
    lw $t0 0($sp)
    lw $t1 4($sp)
    lw $t2 8($sp)
    lw $t3 12($sp)
    lw $a0 16($sp)
    lw $a1 20($sp)
    lw $a2 24($sp)
    lw $ra 28($sp)
    addiu $sp $sp 32

    jr $ra



# CONCAT
# a0 pointer to string 1
# a1 pointer to string 2
# a2 size of string 1 + size of string 2

concat:
    # Save content of registers
    addiu $sp $sp -24
    sw $t0 0($sp)
    sw $t1 4($sp)
    sw $t2 8($sp)
    sw $a0 12($sp)
    sw $a1 16($sp)
    sw $ra 20($sp)

move $t0 $a0                                         # t0 pointer to string 1
    move $t1 $a1                                     # t1 pointer to string 2


    addiu $a0 $a2 1                                  # Save in a0 size in a2 + 1
    li $t2 4                                         # t2 = 4
    div $a0 $t2                                      # a0 / t2
    mfhi $a0                                         # a0 remainder of division
    bne $a0 $zero concat_allign_size                 # Branch if size is multiple of 4
    addiu $a0 $a2 1                                  # Add 1 t size

concat_allign_size:
    sub $t2 $t2 $a0                                  # Convert t1 to multiple of 4 to...
    add $a0 $a2 $t2                                  # reserve memory via malloc
    addiu $a0 $a0 1                                  # Add 1 t size
    j concat_size_alligned

concat_size_alligned:
    jal malloc                                       # a0 stores size to reserve
    move $t2 $a1                                     # t2 is pointer to empty space
    j concat_copy_first_loop

concat_copy_first_loop:
    lb $a0 0($t0)                                    # move to a0 content of t0
    beq $a0 $zero concat_copy_second_loop            # a0 == 0 finish
    sb $a0 0($t2)                                    # move to t2 content of a0
    addiu $t0 $t0 1                                  # Increase t0 pointer
    addiu $t2 $t2 1                                  # Increase t2 pointer
    j concat_copy_first_loop

concat_copy_second_loop:
    lb $a0 0($t1)                                    # move to a0 content of t1
    beq $a0 $zero concat_end                         # a0 == 0 finish
    sb $a0 0($t2)                                    # move to t2 content of a0
    addiu $t1 $t1 1                                  # Increase t1 pointer
    addiu $t2 $t2 1                                  # Increase t2 pointer
    j concat_copy_second_loop

concat_end:
    # Return original values to regiters
    sb $zero 0($t2)
    lw $t0 0($sp)
    lw $t1 4($sp)
    lw $t2 8($sp)
    lw $a0 12($sp)
    lw $a1 16($sp)
    lw $ra 20($sp)
    addiu $sp $sp 24

    jr $ra

read_string:
    addiu $sp $sp -4
    sw $ra 0($sp)

    move $t0 $v1
    move $t1 $zero
    move $t2 $t0
    li $t3 10

    read_loop:

    li $v0 8
    move $a0 $t0
    li $a1 4
    syscall
    addiu $t2 $t2 4

    check_newline_loop:

    lb $t1 0($t0)
    addiu $t0 $t0 1

    beq $t1 $t3 read_loop_continue
    beq $t0 $t2 check_newline_loop_continue
    j check_newline_loop
    check_newline_loop_continue:
    j read_loop

    read_loop_continue:

    bne $t0 $t2 null_terminated
    addiu $t2 $t2 4
    null_terminated:

    move $v0 $v1
    move $v1 $t2

    lw $ra 0($sp)
    addiu $sp $sp 4
    jr $ra




# EQUAL STRING

equal_str:
    # a0 pointer to string 1
    # a1 pointer to string 2
    # v0 answer

    # Save content of registers
    addiu $sp $sp -24
    sw $t0 0($sp)
    sw $t1 4($sp)
    sw $a0 8($sp)
    sw $a1 12($sp)
    sw $t2 16($sp)
    sw $t3 20($sp)

    move $t0 $a0
    move $t1 $a1

equal_str_loop:
    lb $t2 0($t0)
    lb $t3 0($t1)
    bne $t2 $t3 equal_str_different_strings
    beq $t2 $zero equal_str_finished_first
    beq $t3 $zero equal_str_finished_second
    addi $t1 $t1 1
    addi $t0 $t0 1
    j equal_str_loop

equal_str_different_strings:
    move $v0 $zero
    j equal_str_end

equal_str_finished_first:
    beq $t1 $zero equal_str_finished_second
    move $v0 $zero
    j equal_str_end

equal_str_finished_second:
    li $v0 1

equal_str_end:
    lw $t0 0($sp)
    lw $t1 4($sp)
    lw $a0 8($sp)
    lw $a1 12($sp)
    lw $t2 16($sp)
    lw $t3 20($sp)
    addiu $sp $sp 24

    jr $ra