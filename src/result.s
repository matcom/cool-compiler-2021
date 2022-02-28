	.data
_Main: .asciiz "Main"
	.data
	.align 4
Main: .word 4 _Main Init_Main abort_Object type_name_Object copy_Object out_string_IO out_int_IO in_string_IO in_int_IO main_Main

	.data
_Complex: .asciiz "Complex"
	.data
	.align 4
Complex: .word 12 _Complex Init_Complex abort_Object type_name_Object copy_Object out_string_IO out_int_IO in_string_IO in_int_IO init_Complex print_Complex reflect_0_Complex reflect_X_Complex reflect_Y_Complex equal_Complex x_value_Complex y_value_Complex

	.data
_Object: .asciiz "Object"
	.data
	.align 4
Object: .word 4 _Object Init_Object abort_Object type_name_Object copy_Object

	.data
_Int: .asciiz "Int"
	.data
	.align 4
Int: .word 8 _Int Init_Int abort_Object type_name_Object copy_Object

	.data
_String: .asciiz "String"
	.data
	.align 4
String: .word 8 _String Init_String abort_Object type_name_Object copy_Object length_String concat_String substr_String

	.data
_Bool: .asciiz "Bool"
	.data
	.align 4
Bool: .word 8 _Bool Init_Bool abort_Object type_name_Object copy_Object

	.data
_IO: .asciiz "IO"
	.data
	.align 4
IO: .word 4 _IO Init_IO abort_Object type_name_Object copy_Object out_string_IO out_int_IO in_string_IO in_int_IO

	.data
ObjectAbortMessage : .asciiz "Abort called from class "
	.data
IO_Buffer : .space 1001
	.data
str_0: .asciiz "=(\n"

	.data
str_1: .asciiz "=)\n"

	.data
str_2: .asciiz "+"

	.data
str_3: .asciiz "I"

	.text
main:
	# save the return address and frame pointer
	# push $ra to the stack
	sw $ra, 0($sp)
	addi $sp $sp -4
	
	# push $fp to the stack
	sw $fp, 0($sp)
	addi $sp $sp -4
	
	# update the frame pointer and allocate the frame in the stack
	move $fp $sp
	subu $sp $sp 12
	
	# assign (add here the expr.to_string) to m0
	li $a0, 4
	li $v0, 9
	syscall
	la $a0, Main
	sw $a0,  0($v0)
	sw $v0, -0($fp)
	
	lw $v0, -0($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	# assign (add here the expr.to_string) to m1
	# calling the method Init_Main of type Main
	#load the variable m0
	lw $v0, -0($fp)
	lw $v0, 0($v0)
	lw $v1, 8($v0)
	jal $v1
	# pop the top of the stack to $v1
	addi $sp $sp 4
	lw $v1, 0($sp)
	
	sw $v0, -4($fp)
	
	lw $v0, -4($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	# assign (add here the expr.to_string) to m2
	# calling the method main of type Main
	#load the variable m1
	lw $v0, -4($fp)
	lw $v0, 0($v0)
	lw $v1, 40($v0)
	jal $v1
	# pop the top of the stack to $v1
	addi $sp $sp 4
	lw $v1, 0($sp)
	
	sw $v0, -8($fp)
	
	# return the value of the function in the register $v0
	#load the variable m2
	lw $v0, -8($fp)
	move $v0, $v0
	
	# restore the stack pointer, frame pointer y return address
	addu $sp $sp 12
	# pop the top of the stack to $fp
	addi $sp $sp 4
	lw $fp, 0($sp)
	
	# pop the top of the stack to $ra
	addi $sp $sp 4
	lw $ra, 0($sp)
	
	li $v0, 10
	syscall
	
	.text
main_Main:
	# save the return address and frame pointer
	# push $ra to the stack
	sw $ra, 0($sp)
	addi $sp $sp -4
	
	# push $fp to the stack
	sw $fp, 0($sp)
	addi $sp $sp -4
	
	# update the frame pointer and allocate the frame in the stack
	move $fp $sp
	subu $sp $sp 84
	
	# assign (add here the expr.to_string) to t_1
	li $a0, 12
	li $v0, 9
	syscall
	la $a0, Complex
	sw $a0,  0($v0)
	sw $v0, -4($fp)
	
	lw $v0, -4($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	# assign (add here the expr.to_string) to t_2
	# calling the method Init_Complex of type Complex
	#load the variable t_1
	lw $v0, -4($fp)
	lw $v0, 0($v0)
	lw $v1, 8($v0)
	jal $v1
	# pop the top of the stack to $v1
	addi $sp $sp 4
	lw $v1, 0($sp)
	
	sw $v0, -8($fp)
	
	# assign (add here the expr.to_string) to t_3
	#load the variable t_2
	lw $v0, -8($fp)
	sw $v0, -12($fp)
	
	# assign (add here the expr.to_string) to t_4
	# Creating Int instance for atomic 1
	li $a0, 8
	li $v0, 9
	syscall
	la $t0, Int
	li $t1, 1
	sw $t0, 0($v0)
	sw $t1, 4($v0)
	
	sw $v0, -16($fp)
	
	# assign (add here the expr.to_string) to t_5
	# Creating Int instance for atomic 1
	li $a0, 8
	li $v0, 9
	syscall
	la $t0, Int
	li $t1, 1
	sw $t0, 0($v0)
	sw $t1, 4($v0)
	
	sw $v0, -20($fp)
	
	lw $v0, -12($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	lw $v0, -16($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	lw $v0, -20($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	# assign (add here the expr.to_string) to t_6
	# calling the method init of type Complex
	#load the variable t_3
	lw $v0, -12($fp)
	lw $v0, 0($v0)
	lw $v1, 40($v0)
	jal $v1
	# pop the top of the stack to $v1
	addi $sp $sp 4
	lw $v1, 0($sp)
	
	# pop the top of the stack to $v1
	addi $sp $sp 4
	lw $v1, 0($sp)
	
	# pop the top of the stack to $v1
	addi $sp $sp 4
	lw $v1, 0($sp)
	
	sw $v0, -24($fp)
	
	# assign (add here the expr.to_string) to c_0
	#load the variable t_6
	lw $v0, -24($fp)
	sw $v0, -0($fp)
	
	# assign (add here the expr.to_string) to t_7
	#load the variable c_0
	lw $v0, -0($fp)
	sw $v0, -28($fp)
	
	lw $v0, -28($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	# assign (add here the expr.to_string) to t_8
	# calling the method reflect_X of type Complex
	#load the variable t_7
	lw $v0, -28($fp)
	lw $v0, 0($v0)
	lw $v1, 52($v0)
	jal $v1
	# pop the top of the stack to $v1
	addi $sp $sp 4
	lw $v1, 0($sp)
	
	sw $v0, -32($fp)
	
	# assign (add here the expr.to_string) to t_9
	#load the variable c_0
	lw $v0, -0($fp)
	sw $v0, -36($fp)
	
	lw $v0, -36($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	# assign (add here the expr.to_string) to t_10
	# calling the method reflect_0 of type Complex
	#load the variable t_9
	lw $v0, -36($fp)
	lw $v0, 0($v0)
	lw $v1, 48($v0)
	jal $v1
	# pop the top of the stack to $v1
	addi $sp $sp 4
	lw $v1, 0($sp)
	
	sw $v0, -40($fp)
	
	# assign (add here the expr.to_string) to t_11
	#load the variable t_8
	lw $v0, -32($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	#load the variable t_10
	lw $v0, -40($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	jal compare
	# pop the top of the stack to $t0
	addi $sp $sp 4
	lw $t0, 0($sp)
	
	# pop the top of the stack to $t0
	addi $sp $sp 4
	lw $t0, 0($sp)
	
	sw $v0, -44($fp)
	
	# assign (add here the expr.to_string) to t_12
	#load the variable t_11
	lw $v0, -44($fp)
	sw $v0, -48($fp)
	
	lw $t1, -48($fp)
	lw $t0, 4($t1)
	bne $t0, $zero, then_0
	# assign (add here the expr.to_string) to t_14
	#load the string str_0
	li $a0, 8
	li $v0, 9
	syscall
	la $v1, String
	sw $v1, 0($v0)
	la $v1, str_0
	sw $v1, 4($v0)
	sw $v0, -56($fp)
	
	# assign (add here the expr.to_string) to t_15
	#load the variable t_14
	lw $v0, -56($fp)
	sw $v0, -60($fp)
	
	lw $v0, 12($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	lw $v0, -60($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	# assign (add here the expr.to_string) to t_16
	# calling the method out_string of type Main
	#load the variable self_Main
	lw $v0, 12($fp)
	lw $v0, 0($v0)
	lw $v1, 24($v0)
	jal $v1
	# pop the top of the stack to $v1
	addi $sp $sp 4
	lw $v1, 0($sp)
	
	# pop the top of the stack to $v1
	addi $sp $sp 4
	lw $v1, 0($sp)
	
	sw $v0, -64($fp)
	
	# assign (add here the expr.to_string) to t_13
	#load the variable t_16
	lw $v0, -64($fp)
	sw $v0, -52($fp)
	
	j ifend_0
	then_0:
	# assign (add here the expr.to_string) to t_17
	#load the string str_1
	li $a0, 8
	li $v0, 9
	syscall
	la $v1, String
	sw $v1, 0($v0)
	la $v1, str_1
	sw $v1, 4($v0)
	sw $v0, -68($fp)
	
	# assign (add here the expr.to_string) to t_18
	#load the variable t_17
	lw $v0, -68($fp)
	sw $v0, -72($fp)
	
	lw $v0, 12($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	lw $v0, -72($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	# assign (add here the expr.to_string) to t_19
	# calling the method out_string of type Main
	#load the variable self_Main
	lw $v0, 12($fp)
	lw $v0, 0($v0)
	lw $v1, 24($v0)
	jal $v1
	# pop the top of the stack to $v1
	addi $sp $sp 4
	lw $v1, 0($sp)
	
	# pop the top of the stack to $v1
	addi $sp $sp 4
	lw $v1, 0($sp)
	
	sw $v0, -76($fp)
	
	# assign (add here the expr.to_string) to t_13
	#load the variable t_19
	lw $v0, -76($fp)
	sw $v0, -52($fp)
	
	ifend_0:
	# assign (add here the expr.to_string) to t_20
	#load the variable t_13
	lw $v0, -52($fp)
	sw $v0, -80($fp)
	
	# return the value of the function in the register $v0
	#load the variable t_20
	lw $v0, -80($fp)
	move $v0, $v0
	
	# restore the stack pointer, frame pointer y return address
	addu $sp $sp 84
	# pop the top of the stack to $fp
	addi $sp $sp 4
	lw $fp, 0($sp)
	
	# pop the top of the stack to $ra
	addi $sp $sp 4
	lw $ra, 0($sp)
	
	jr $ra
	
	.text
Init_Main:
	# save the return address and frame pointer
	# push $ra to the stack
	sw $ra, 0($sp)
	addi $sp $sp -4
	
	# push $fp to the stack
	sw $fp, 0($sp)
	addi $sp $sp -4
	
	# update the frame pointer and allocate the frame in the stack
	move $fp $sp
	subu $sp $sp 0
	
	lw $v0, 12($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	# assign (add here the expr.to_string) to self_Main
	jal Init_IO
	# pop the top of the stack to $v1
	addi $sp $sp 4
	lw $v1, 0($sp)
	
	sw $v0, 12($fp)
	
	# return the value of the function in the register $v0
	#load the variable self_Main
	lw $v0, 12($fp)
	move $v0, $v0
	
	# restore the stack pointer, frame pointer y return address
	addu $sp $sp 0
	# pop the top of the stack to $fp
	addi $sp $sp 4
	lw $fp, 0($sp)
	
	# pop the top of the stack to $ra
	addi $sp $sp 4
	lw $ra, 0($sp)
	
	jr $ra
	
	.text
init_Complex:
	# save the return address and frame pointer
	# push $ra to the stack
	sw $ra, 0($sp)
	addi $sp $sp -4
	
	# push $fp to the stack
	sw $fp, 0($sp)
	addi $sp $sp -4
	
	# update the frame pointer and allocate the frame in the stack
	move $fp $sp
	subu $sp $sp 20
	
	# assign (add here the expr.to_string) to t_23
	lw $v1, 20($fp)
	lw $v0, 4($v1)
	sw $v0, -0($fp)
	
	# assign (add here the expr.to_string) to t_24
	#load the variable t_23
	lw $v0, -0($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	#load the variable a_21
	lw $v0, 16($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	jal compare
	# pop the top of the stack to $t0
	addi $sp $sp 4
	lw $t0, 0($sp)
	
	# pop the top of the stack to $t0
	addi $sp $sp 4
	lw $t0, 0($sp)
	
	sw $v0, -4($fp)
	
	# assign (add here the expr.to_string) to t_25
	lw $v1, 20($fp)
	lw $v0, 8($v1)
	sw $v0, -8($fp)
	
	# assign (add here the expr.to_string) to t_26
	#load the variable t_25
	lw $v0, -8($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	#load the variable b_22
	lw $v0, 12($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	jal compare
	# pop the top of the stack to $t0
	addi $sp $sp 4
	lw $t0, 0($sp)
	
	# pop the top of the stack to $t0
	addi $sp $sp 4
	lw $t0, 0($sp)
	
	sw $v0, -12($fp)
	
	# assign (add here the expr.to_string) to t_27
	#load the variable self_Complex
	lw $v0, 20($fp)
	sw $v0, -16($fp)
	
	# return the value of the function in the register $v0
	#load the variable t_27
	lw $v0, -16($fp)
	move $v0, $v0
	
	# restore the stack pointer, frame pointer y return address
	addu $sp $sp 20
	# pop the top of the stack to $fp
	addi $sp $sp 4
	lw $fp, 0($sp)
	
	# pop the top of the stack to $ra
	addi $sp $sp 4
	lw $ra, 0($sp)
	
	jr $ra
	
	.text
print_Complex:
	# save the return address and frame pointer
	# push $ra to the stack
	sw $ra, 0($sp)
	addi $sp $sp -4
	
	# push $fp to the stack
	sw $fp, 0($sp)
	addi $sp $sp -4
	
	# update the frame pointer and allocate the frame in the stack
	move $fp $sp
	subu $sp $sp 92
	
	# assign (add here the expr.to_string) to t_28
	lw $v1, 12($fp)
	lw $v0, 8($v1)
	sw $v0, -0($fp)
	
	# assign (add here the expr.to_string) to t_29
	#load the variable t_28
	lw $v0, -0($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	# Creating Int instance for atomic 0
	li $a0, 8
	li $v0, 9
	syscall
	la $t0, Int
	li $t1, 0
	sw $t0, 0($v0)
	sw $t1, 4($v0)
	
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	jal compare
	# pop the top of the stack to $t0
	addi $sp $sp 4
	lw $t0, 0($sp)
	
	# pop the top of the stack to $t0
	addi $sp $sp 4
	lw $t0, 0($sp)
	
	sw $v0, -4($fp)
	
	# assign (add here the expr.to_string) to t_30
	#load the variable t_29
	lw $v0, -4($fp)
	sw $v0, -8($fp)
	
	lw $t1, -8($fp)
	lw $t0, 4($t1)
	bne $t0, $zero, then_1
	# assign (add here the expr.to_string) to t_32
	lw $v1, 12($fp)
	lw $v0, 4($v1)
	sw $v0, -16($fp)
	
	# assign (add here the expr.to_string) to t_33
	#load the variable t_32
	lw $v0, -16($fp)
	sw $v0, -20($fp)
	
	lw $v0, 12($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	lw $v0, -20($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	# assign (add here the expr.to_string) to t_34
	# calling the method out_int of type Complex
	#load the variable self_Complex
	lw $v0, 12($fp)
	lw $v0, 0($v0)
	lw $v1, 28($v0)
	jal $v1
	# pop the top of the stack to $v1
	addi $sp $sp 4
	lw $v1, 0($sp)
	
	# pop the top of the stack to $v1
	addi $sp $sp 4
	lw $v1, 0($sp)
	
	sw $v0, -24($fp)
	
	# assign (add here the expr.to_string) to t_35
	#load the variable t_34
	lw $v0, -24($fp)
	sw $v0, -28($fp)
	
	# assign (add here the expr.to_string) to t_36
	#load the string str_2
	li $a0, 8
	li $v0, 9
	syscall
	la $v1, String
	sw $v1, 0($v0)
	la $v1, str_2
	sw $v1, 4($v0)
	sw $v0, -32($fp)
	
	# assign (add here the expr.to_string) to t_37
	#load the variable t_36
	lw $v0, -32($fp)
	sw $v0, -36($fp)
	
	lw $v0, -28($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	lw $v0, -36($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	# assign (add here the expr.to_string) to t_38
	# calling the method out_string of type Complex
	#load the variable t_35
	lw $v0, -28($fp)
	lw $v0, 0($v0)
	lw $v1, 24($v0)
	jal $v1
	# pop the top of the stack to $v1
	addi $sp $sp 4
	lw $v1, 0($sp)
	
	# pop the top of the stack to $v1
	addi $sp $sp 4
	lw $v1, 0($sp)
	
	sw $v0, -40($fp)
	
	# assign (add here the expr.to_string) to t_39
	#load the variable t_38
	lw $v0, -40($fp)
	sw $v0, -44($fp)
	
	# assign (add here the expr.to_string) to t_40
	lw $v1, 12($fp)
	lw $v0, 8($v1)
	sw $v0, -48($fp)
	
	# assign (add here the expr.to_string) to t_41
	#load the variable t_40
	lw $v0, -48($fp)
	sw $v0, -52($fp)
	
	lw $v0, -44($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	lw $v0, -52($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	# assign (add here the expr.to_string) to t_42
	# calling the method out_int of type Complex
	#load the variable t_39
	lw $v0, -44($fp)
	lw $v0, 0($v0)
	lw $v1, 28($v0)
	jal $v1
	# pop the top of the stack to $v1
	addi $sp $sp 4
	lw $v1, 0($sp)
	
	# pop the top of the stack to $v1
	addi $sp $sp 4
	lw $v1, 0($sp)
	
	sw $v0, -56($fp)
	
	# assign (add here the expr.to_string) to t_43
	#load the variable t_42
	lw $v0, -56($fp)
	sw $v0, -60($fp)
	
	# assign (add here the expr.to_string) to t_44
	#load the string str_3
	li $a0, 8
	li $v0, 9
	syscall
	la $v1, String
	sw $v1, 0($v0)
	la $v1, str_3
	sw $v1, 4($v0)
	sw $v0, -64($fp)
	
	# assign (add here the expr.to_string) to t_45
	#load the variable t_44
	lw $v0, -64($fp)
	sw $v0, -68($fp)
	
	lw $v0, -60($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	lw $v0, -68($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	# assign (add here the expr.to_string) to t_46
	# calling the method out_string of type Complex
	#load the variable t_43
	lw $v0, -60($fp)
	lw $v0, 0($v0)
	lw $v1, 24($v0)
	jal $v1
	# pop the top of the stack to $v1
	addi $sp $sp 4
	lw $v1, 0($sp)
	
	# pop the top of the stack to $v1
	addi $sp $sp 4
	lw $v1, 0($sp)
	
	sw $v0, -72($fp)
	
	# assign (add here the expr.to_string) to t_31
	#load the variable t_46
	lw $v0, -72($fp)
	sw $v0, -12($fp)
	
	j ifend_1
	then_1:
	# assign (add here the expr.to_string) to t_47
	lw $v1, 12($fp)
	lw $v0, 4($v1)
	sw $v0, -76($fp)
	
	# assign (add here the expr.to_string) to t_48
	#load the variable t_47
	lw $v0, -76($fp)
	sw $v0, -80($fp)
	
	lw $v0, 12($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	lw $v0, -80($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	# assign (add here the expr.to_string) to t_49
	# calling the method out_int of type Complex
	#load the variable self_Complex
	lw $v0, 12($fp)
	lw $v0, 0($v0)
	lw $v1, 28($v0)
	jal $v1
	# pop the top of the stack to $v1
	addi $sp $sp 4
	lw $v1, 0($sp)
	
	# pop the top of the stack to $v1
	addi $sp $sp 4
	lw $v1, 0($sp)
	
	sw $v0, -84($fp)
	
	# assign (add here the expr.to_string) to t_31
	#load the variable t_49
	lw $v0, -84($fp)
	sw $v0, -12($fp)
	
	ifend_1:
	# assign (add here the expr.to_string) to t_50
	#load the variable t_31
	lw $v0, -12($fp)
	sw $v0, -88($fp)
	
	# return the value of the function in the register $v0
	#load the variable t_50
	lw $v0, -88($fp)
	move $v0, $v0
	
	# restore the stack pointer, frame pointer y return address
	addu $sp $sp 92
	# pop the top of the stack to $fp
	addi $sp $sp 4
	lw $fp, 0($sp)
	
	# pop the top of the stack to $ra
	addi $sp $sp 4
	lw $ra, 0($sp)
	
	jr $ra
	
	.text
reflect_0_Complex:
	# save the return address and frame pointer
	# push $ra to the stack
	sw $ra, 0($sp)
	addi $sp $sp -4
	
	# push $fp to the stack
	sw $fp, 0($sp)
	addi $sp $sp -4
	
	# update the frame pointer and allocate the frame in the stack
	move $fp $sp
	subu $sp $sp 44
	
	# assign (add here the expr.to_string) to t_51
	lw $v1, 12($fp)
	lw $v0, 4($v1)
	sw $v0, -0($fp)
	
	# assign (add here the expr.to_string) to t_52
	lw $v1, 12($fp)
	lw $v0, 4($v1)
	sw $v0, -4($fp)
	
	# assign (add here the expr.to_string) to t_53
	#load the variable t_52
	lw $v0, -4($fp)
	sw $v0, -8($fp)
	
	# assign (add here the expr.to_string) to t_54
	# computes the sub of (node.left.to_string) and (node.right.to_string) and stores it at $v0
	# Creating Int instance for atomic 0
	li $a0, 8
	li $v0, 9
	syscall
	la $t0, Int
	li $t1, 0
	sw $t0, 0($v0)
	sw $t1, 4($v0)
	
	lw $t0, 4($v0)
	# push $t0 to the stack
	sw $t0, 0($sp)
	addi $sp $sp -4
	
	#load the variable t_53
	lw $v0, -8($fp)
	lw $t1, 4($v0)
	# pop the top of the stack to $t0
	addi $sp $sp 4
	lw $t0, 0($sp)
	
	sub $t0, $t0, $t1
	li $a0, 8
	li $v0, 9
	syscall
	la $t1, Int
	sw $t1, 0($v0)
	sw $t0, 4($v0)
	sw $v0, -12($fp)
	
	# assign (add here the expr.to_string) to t_55
	#load the variable t_51
	lw $v0, -0($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	#load the variable t_54
	lw $v0, -12($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	jal compare
	# pop the top of the stack to $t0
	addi $sp $sp 4
	lw $t0, 0($sp)
	
	# pop the top of the stack to $t0
	addi $sp $sp 4
	lw $t0, 0($sp)
	
	sw $v0, -16($fp)
	
	# assign (add here the expr.to_string) to t_56
	lw $v1, 12($fp)
	lw $v0, 8($v1)
	sw $v0, -20($fp)
	
	# assign (add here the expr.to_string) to t_57
	lw $v1, 12($fp)
	lw $v0, 8($v1)
	sw $v0, -24($fp)
	
	# assign (add here the expr.to_string) to t_58
	#load the variable t_57
	lw $v0, -24($fp)
	sw $v0, -28($fp)
	
	# assign (add here the expr.to_string) to t_59
	# computes the sub of (node.left.to_string) and (node.right.to_string) and stores it at $v0
	# Creating Int instance for atomic 0
	li $a0, 8
	li $v0, 9
	syscall
	la $t0, Int
	li $t1, 0
	sw $t0, 0($v0)
	sw $t1, 4($v0)
	
	lw $t0, 4($v0)
	# push $t0 to the stack
	sw $t0, 0($sp)
	addi $sp $sp -4
	
	#load the variable t_58
	lw $v0, -28($fp)
	lw $t1, 4($v0)
	# pop the top of the stack to $t0
	addi $sp $sp 4
	lw $t0, 0($sp)
	
	sub $t0, $t0, $t1
	li $a0, 8
	li $v0, 9
	syscall
	la $t1, Int
	sw $t1, 0($v0)
	sw $t0, 4($v0)
	sw $v0, -32($fp)
	
	# assign (add here the expr.to_string) to t_60
	#load the variable t_56
	lw $v0, -20($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	#load the variable t_59
	lw $v0, -32($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	jal compare
	# pop the top of the stack to $t0
	addi $sp $sp 4
	lw $t0, 0($sp)
	
	# pop the top of the stack to $t0
	addi $sp $sp 4
	lw $t0, 0($sp)
	
	sw $v0, -36($fp)
	
	# assign (add here the expr.to_string) to t_61
	#load the variable self_Complex
	lw $v0, 12($fp)
	sw $v0, -40($fp)
	
	# return the value of the function in the register $v0
	#load the variable t_61
	lw $v0, -40($fp)
	move $v0, $v0
	
	# restore the stack pointer, frame pointer y return address
	addu $sp $sp 44
	# pop the top of the stack to $fp
	addi $sp $sp 4
	lw $fp, 0($sp)
	
	# pop the top of the stack to $ra
	addi $sp $sp 4
	lw $ra, 0($sp)
	
	jr $ra
	
	.text
reflect_X_Complex:
	# save the return address and frame pointer
	# push $ra to the stack
	sw $ra, 0($sp)
	addi $sp $sp -4
	
	# push $fp to the stack
	sw $fp, 0($sp)
	addi $sp $sp -4
	
	# update the frame pointer and allocate the frame in the stack
	move $fp $sp
	subu $sp $sp 24
	
	# assign (add here the expr.to_string) to t_62
	lw $v1, 12($fp)
	lw $v0, 8($v1)
	sw $v0, -0($fp)
	
	# assign (add here the expr.to_string) to t_63
	lw $v1, 12($fp)
	lw $v0, 8($v1)
	sw $v0, -4($fp)
	
	# assign (add here the expr.to_string) to t_64
	#load the variable t_63
	lw $v0, -4($fp)
	sw $v0, -8($fp)
	
	# assign (add here the expr.to_string) to t_65
	# computes the sub of (node.left.to_string) and (node.right.to_string) and stores it at $v0
	# Creating Int instance for atomic 0
	li $a0, 8
	li $v0, 9
	syscall
	la $t0, Int
	li $t1, 0
	sw $t0, 0($v0)
	sw $t1, 4($v0)
	
	lw $t0, 4($v0)
	# push $t0 to the stack
	sw $t0, 0($sp)
	addi $sp $sp -4
	
	#load the variable t_64
	lw $v0, -8($fp)
	lw $t1, 4($v0)
	# pop the top of the stack to $t0
	addi $sp $sp 4
	lw $t0, 0($sp)
	
	sub $t0, $t0, $t1
	li $a0, 8
	li $v0, 9
	syscall
	la $t1, Int
	sw $t1, 0($v0)
	sw $t0, 4($v0)
	sw $v0, -12($fp)
	
	# assign (add here the expr.to_string) to t_66
	#load the variable t_62
	lw $v0, -0($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	#load the variable t_65
	lw $v0, -12($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	jal compare
	# pop the top of the stack to $t0
	addi $sp $sp 4
	lw $t0, 0($sp)
	
	# pop the top of the stack to $t0
	addi $sp $sp 4
	lw $t0, 0($sp)
	
	sw $v0, -16($fp)
	
	# assign (add here the expr.to_string) to t_67
	#load the variable self_Complex
	lw $v0, 12($fp)
	sw $v0, -20($fp)
	
	# return the value of the function in the register $v0
	#load the variable t_67
	lw $v0, -20($fp)
	move $v0, $v0
	
	# restore the stack pointer, frame pointer y return address
	addu $sp $sp 24
	# pop the top of the stack to $fp
	addi $sp $sp 4
	lw $fp, 0($sp)
	
	# pop the top of the stack to $ra
	addi $sp $sp 4
	lw $ra, 0($sp)
	
	jr $ra
	
	.text
reflect_Y_Complex:
	# save the return address and frame pointer
	# push $ra to the stack
	sw $ra, 0($sp)
	addi $sp $sp -4
	
	# push $fp to the stack
	sw $fp, 0($sp)
	addi $sp $sp -4
	
	# update the frame pointer and allocate the frame in the stack
	move $fp $sp
	subu $sp $sp 24
	
	# assign (add here the expr.to_string) to t_68
	lw $v1, 12($fp)
	lw $v0, 4($v1)
	sw $v0, -0($fp)
	
	# assign (add here the expr.to_string) to t_69
	lw $v1, 12($fp)
	lw $v0, 4($v1)
	sw $v0, -4($fp)
	
	# assign (add here the expr.to_string) to t_70
	#load the variable t_69
	lw $v0, -4($fp)
	sw $v0, -8($fp)
	
	# assign (add here the expr.to_string) to t_71
	# computes the sub of (node.left.to_string) and (node.right.to_string) and stores it at $v0
	# Creating Int instance for atomic 0
	li $a0, 8
	li $v0, 9
	syscall
	la $t0, Int
	li $t1, 0
	sw $t0, 0($v0)
	sw $t1, 4($v0)
	
	lw $t0, 4($v0)
	# push $t0 to the stack
	sw $t0, 0($sp)
	addi $sp $sp -4
	
	#load the variable t_70
	lw $v0, -8($fp)
	lw $t1, 4($v0)
	# pop the top of the stack to $t0
	addi $sp $sp 4
	lw $t0, 0($sp)
	
	sub $t0, $t0, $t1
	li $a0, 8
	li $v0, 9
	syscall
	la $t1, Int
	sw $t1, 0($v0)
	sw $t0, 4($v0)
	sw $v0, -12($fp)
	
	# assign (add here the expr.to_string) to t_72
	#load the variable t_68
	lw $v0, -0($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	#load the variable t_71
	lw $v0, -12($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	jal compare
	# pop the top of the stack to $t0
	addi $sp $sp 4
	lw $t0, 0($sp)
	
	# pop the top of the stack to $t0
	addi $sp $sp 4
	lw $t0, 0($sp)
	
	sw $v0, -16($fp)
	
	# assign (add here the expr.to_string) to t_73
	#load the variable self_Complex
	lw $v0, 12($fp)
	sw $v0, -20($fp)
	
	# return the value of the function in the register $v0
	#load the variable t_73
	lw $v0, -20($fp)
	move $v0, $v0
	
	# restore the stack pointer, frame pointer y return address
	addu $sp $sp 24
	# pop the top of the stack to $fp
	addi $sp $sp 4
	lw $fp, 0($sp)
	
	# pop the top of the stack to $ra
	addi $sp $sp 4
	lw $ra, 0($sp)
	
	jr $ra
	
	.text
equal_Complex:
	# save the return address and frame pointer
	# push $ra to the stack
	sw $ra, 0($sp)
	addi $sp $sp -4
	
	# push $fp to the stack
	sw $fp, 0($sp)
	addi $sp $sp -4
	
	# update the frame pointer and allocate the frame in the stack
	move $fp $sp
	subu $sp $sp 64
	
	# assign (add here the expr.to_string) to t_75
	lw $v1, 16($fp)
	lw $v0, 4($v1)
	sw $v0, -0($fp)
	
	# assign (add here the expr.to_string) to t_76
	#load the variable d_74
	lw $v0, 12($fp)
	sw $v0, -4($fp)
	
	lw $v0, -4($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	# assign (add here the expr.to_string) to t_77
	# calling the method x_value of type Complex
	#load the variable t_76
	lw $v0, -4($fp)
	lw $v0, 0($v0)
	lw $v1, 64($v0)
	jal $v1
	# pop the top of the stack to $v1
	addi $sp $sp 4
	lw $v1, 0($sp)
	
	sw $v0, -8($fp)
	
	# assign (add here the expr.to_string) to t_78
	#load the variable t_75
	lw $v0, -0($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	#load the variable t_77
	lw $v0, -8($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	jal compare
	# pop the top of the stack to $t0
	addi $sp $sp 4
	lw $t0, 0($sp)
	
	# pop the top of the stack to $t0
	addi $sp $sp 4
	lw $t0, 0($sp)
	
	sw $v0, -12($fp)
	
	# assign (add here the expr.to_string) to t_79
	#load the variable t_78
	lw $v0, -12($fp)
	sw $v0, -16($fp)
	
	lw $t1, -16($fp)
	lw $t0, 4($t1)
	bne $t0, $zero, then_2
	# assign (add here the expr.to_string) to t_81
	# Creating Int instance for atomic 0
	li $a0, 8
	li $v0, 9
	syscall
	la $t0, Int
	li $t1, 0
	sw $t0, 0($v0)
	sw $t1, 4($v0)
	
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	# Creating Int instance for atomic 1
	li $a0, 8
	li $v0, 9
	syscall
	la $t0, Int
	li $t1, 1
	sw $t0, 0($v0)
	sw $t1, 4($v0)
	
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	jal compare
	# pop the top of the stack to $t0
	addi $sp $sp 4
	lw $t0, 0($sp)
	
	# pop the top of the stack to $t0
	addi $sp $sp 4
	lw $t0, 0($sp)
	
	sw $v0, -24($fp)
	
	# assign (add here the expr.to_string) to t_80
	#load the variable t_81
	lw $v0, -24($fp)
	sw $v0, -20($fp)
	
	j ifend_2
	then_2:
	# assign (add here the expr.to_string) to t_82
	lw $v1, 16($fp)
	lw $v0, 8($v1)
	sw $v0, -28($fp)
	
	# assign (add here the expr.to_string) to t_83
	#load the variable d_74
	lw $v0, 12($fp)
	sw $v0, -32($fp)
	
	lw $v0, -32($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	# assign (add here the expr.to_string) to t_84
	# calling the method y_value of type Complex
	#load the variable t_83
	lw $v0, -32($fp)
	lw $v0, 0($v0)
	lw $v1, 68($v0)
	jal $v1
	# pop the top of the stack to $v1
	addi $sp $sp 4
	lw $v1, 0($sp)
	
	sw $v0, -36($fp)
	
	# assign (add here the expr.to_string) to t_85
	#load the variable t_82
	lw $v0, -28($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	#load the variable t_84
	lw $v0, -36($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	jal compare
	# pop the top of the stack to $t0
	addi $sp $sp 4
	lw $t0, 0($sp)
	
	# pop the top of the stack to $t0
	addi $sp $sp 4
	lw $t0, 0($sp)
	
	sw $v0, -40($fp)
	
	# assign (add here the expr.to_string) to t_86
	#load the variable t_85
	lw $v0, -40($fp)
	sw $v0, -44($fp)
	
	lw $t1, -44($fp)
	lw $t0, 4($t1)
	bne $t0, $zero, then_3
	# assign (add here the expr.to_string) to t_88
	# Creating Int instance for atomic 0
	li $a0, 8
	li $v0, 9
	syscall
	la $t0, Int
	li $t1, 0
	sw $t0, 0($v0)
	sw $t1, 4($v0)
	
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	# Creating Int instance for atomic 1
	li $a0, 8
	li $v0, 9
	syscall
	la $t0, Int
	li $t1, 1
	sw $t0, 0($v0)
	sw $t1, 4($v0)
	
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	jal compare
	# pop the top of the stack to $t0
	addi $sp $sp 4
	lw $t0, 0($sp)
	
	# pop the top of the stack to $t0
	addi $sp $sp 4
	lw $t0, 0($sp)
	
	sw $v0, -52($fp)
	
	# assign (add here the expr.to_string) to t_87
	#load the variable t_88
	lw $v0, -52($fp)
	sw $v0, -48($fp)
	
	j ifend_3
	then_3:
	# assign (add here the expr.to_string) to t_89
	# Creating Int instance for atomic 0
	li $a0, 8
	li $v0, 9
	syscall
	la $t0, Int
	li $t1, 0
	sw $t0, 0($v0)
	sw $t1, 4($v0)
	
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	# Creating Int instance for atomic 0
	li $a0, 8
	li $v0, 9
	syscall
	la $t0, Int
	li $t1, 0
	sw $t0, 0($v0)
	sw $t1, 4($v0)
	
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	jal compare
	# pop the top of the stack to $t0
	addi $sp $sp 4
	lw $t0, 0($sp)
	
	# pop the top of the stack to $t0
	addi $sp $sp 4
	lw $t0, 0($sp)
	
	sw $v0, -56($fp)
	
	# assign (add here the expr.to_string) to t_87
	#load the variable t_89
	lw $v0, -56($fp)
	sw $v0, -48($fp)
	
	ifend_3:
	# assign (add here the expr.to_string) to t_80
	#load the variable t_87
	lw $v0, -48($fp)
	sw $v0, -20($fp)
	
	ifend_2:
	# assign (add here the expr.to_string) to t_90
	#load the variable t_80
	lw $v0, -20($fp)
	sw $v0, -60($fp)
	
	# return the value of the function in the register $v0
	#load the variable t_90
	lw $v0, -60($fp)
	move $v0, $v0
	
	# restore the stack pointer, frame pointer y return address
	addu $sp $sp 64
	# pop the top of the stack to $fp
	addi $sp $sp 4
	lw $fp, 0($sp)
	
	# pop the top of the stack to $ra
	addi $sp $sp 4
	lw $ra, 0($sp)
	
	jr $ra
	
	.text
x_value_Complex:
	# save the return address and frame pointer
	# push $ra to the stack
	sw $ra, 0($sp)
	addi $sp $sp -4
	
	# push $fp to the stack
	sw $fp, 0($sp)
	addi $sp $sp -4
	
	# update the frame pointer and allocate the frame in the stack
	move $fp $sp
	subu $sp $sp 8
	
	# assign (add here the expr.to_string) to t_91
	lw $v1, 12($fp)
	lw $v0, 4($v1)
	sw $v0, -0($fp)
	
	# assign (add here the expr.to_string) to t_92
	#load the variable t_91
	lw $v0, -0($fp)
	sw $v0, -4($fp)
	
	# return the value of the function in the register $v0
	#load the variable t_92
	lw $v0, -4($fp)
	move $v0, $v0
	
	# restore the stack pointer, frame pointer y return address
	addu $sp $sp 8
	# pop the top of the stack to $fp
	addi $sp $sp 4
	lw $fp, 0($sp)
	
	# pop the top of the stack to $ra
	addi $sp $sp 4
	lw $ra, 0($sp)
	
	jr $ra
	
	.text
y_value_Complex:
	# save the return address and frame pointer
	# push $ra to the stack
	sw $ra, 0($sp)
	addi $sp $sp -4
	
	# push $fp to the stack
	sw $fp, 0($sp)
	addi $sp $sp -4
	
	# update the frame pointer and allocate the frame in the stack
	move $fp $sp
	subu $sp $sp 8
	
	# assign (add here the expr.to_string) to t_93
	lw $v1, 12($fp)
	lw $v0, 8($v1)
	sw $v0, -0($fp)
	
	# assign (add here the expr.to_string) to t_94
	#load the variable t_93
	lw $v0, -0($fp)
	sw $v0, -4($fp)
	
	# return the value of the function in the register $v0
	#load the variable t_94
	lw $v0, -4($fp)
	move $v0, $v0
	
	# restore the stack pointer, frame pointer y return address
	addu $sp $sp 8
	# pop the top of the stack to $fp
	addi $sp $sp 4
	lw $fp, 0($sp)
	
	# pop the top of the stack to $ra
	addi $sp $sp 4
	lw $ra, 0($sp)
	
	jr $ra
	
	.text
Init_Complex:
	# save the return address and frame pointer
	# push $ra to the stack
	sw $ra, 0($sp)
	addi $sp $sp -4
	
	# push $fp to the stack
	sw $fp, 0($sp)
	addi $sp $sp -4
	
	# update the frame pointer and allocate the frame in the stack
	move $fp $sp
	subu $sp $sp 0
	
	lw $v0, 12($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	# assign (add here the expr.to_string) to self_Complex
	jal Init_IO
	# pop the top of the stack to $v1
	addi $sp $sp 4
	lw $v1, 0($sp)
	
	sw $v0, 12($fp)
	
	# return the value of the function in the register $v0
	#load the variable self_Complex
	lw $v0, 12($fp)
	move $v0, $v0
	
	# restore the stack pointer, frame pointer y return address
	addu $sp $sp 0
	# pop the top of the stack to $fp
	addi $sp $sp 4
	lw $fp, 0($sp)
	
	# pop the top of the stack to $ra
	addi $sp $sp 4
	lw $ra, 0($sp)
	
	jr $ra
	
	.text
Init_Object:
	# save the return address and frame pointer
	# push $ra to the stack
	sw $ra, 0($sp)
	addi $sp $sp -4
	
	# push $fp to the stack
	sw $fp, 0($sp)
	addi $sp $sp -4
	
	# update the frame pointer and allocate the frame in the stack
	move $fp $sp
	subu $sp $sp 0
	
	# return the value of the function in the register $v0
	#load the variable self
	lw $v0, 12($fp)
	move $v0, $v0
	
	# restore the stack pointer, frame pointer y return address
	addu $sp $sp 0
	# pop the top of the stack to $fp
	addi $sp $sp 4
	lw $fp, 0($sp)
	
	# pop the top of the stack to $ra
	addi $sp $sp 4
	lw $ra, 0($sp)
	
	jr $ra
	
	.text
Init_Int:
	# save the return address and frame pointer
	# push $ra to the stack
	sw $ra, 0($sp)
	addi $sp $sp -4
	
	# push $fp to the stack
	sw $fp, 0($sp)
	addi $sp $sp -4
	
	# update the frame pointer and allocate the frame in the stack
	move $fp $sp
	subu $sp $sp 0
	
	# Setting value of the attribute value in the instance self to v
	#load the variable v
	lw $v0, 12($fp)
	move $s2, $v0
	lw $v1, 16($fp)
	sw $s2, 4($v1)
	
	# return the value of the function in the register $v0
	#load the variable self
	lw $v0, 16($fp)
	move $v0, $v0
	
	# restore the stack pointer, frame pointer y return address
	addu $sp $sp 0
	# pop the top of the stack to $fp
	addi $sp $sp 4
	lw $fp, 0($sp)
	
	# pop the top of the stack to $ra
	addi $sp $sp 4
	lw $ra, 0($sp)
	
	jr $ra
	
	.text
Init_String:
	# save the return address and frame pointer
	# push $ra to the stack
	sw $ra, 0($sp)
	addi $sp $sp -4
	
	# push $fp to the stack
	sw $fp, 0($sp)
	addi $sp $sp -4
	
	# update the frame pointer and allocate the frame in the stack
	move $fp $sp
	subu $sp $sp 0
	
	# Setting value of the attribute value in the instance self to v
	#load the variable v
	lw $v0, 12($fp)
	move $s2, $v0
	lw $v1, 16($fp)
	sw $s2, 4($v1)
	
	# return the value of the function in the register $v0
	#load the variable self
	lw $v0, 16($fp)
	move $v0, $v0
	
	# restore the stack pointer, frame pointer y return address
	addu $sp $sp 0
	# pop the top of the stack to $fp
	addi $sp $sp 4
	lw $fp, 0($sp)
	
	# pop the top of the stack to $ra
	addi $sp $sp 4
	lw $ra, 0($sp)
	
	jr $ra
	
	.text
Init_Bool:
	# save the return address and frame pointer
	# push $ra to the stack
	sw $ra, 0($sp)
	addi $sp $sp -4
	
	# push $fp to the stack
	sw $fp, 0($sp)
	addi $sp $sp -4
	
	# update the frame pointer and allocate the frame in the stack
	move $fp $sp
	subu $sp $sp 0
	
	# Setting value of the attribute value in the instance self to v
	#load the variable v
	lw $v0, 12($fp)
	move $s2, $v0
	lw $v1, 16($fp)
	sw $s2, 4($v1)
	
	# return the value of the function in the register $v0
	#load the variable self
	lw $v0, 16($fp)
	move $v0, $v0
	
	# restore the stack pointer, frame pointer y return address
	addu $sp $sp 0
	# pop the top of the stack to $fp
	addi $sp $sp 4
	lw $fp, 0($sp)
	
	# pop the top of the stack to $ra
	addi $sp $sp 4
	lw $ra, 0($sp)
	
	jr $ra
	
	.text
Init_IO:
	# save the return address and frame pointer
	# push $ra to the stack
	sw $ra, 0($sp)
	addi $sp $sp -4
	
	# push $fp to the stack
	sw $fp, 0($sp)
	addi $sp $sp -4
	
	# update the frame pointer and allocate the frame in the stack
	move $fp $sp
	subu $sp $sp 0
	
	# return the value of the function in the register $v0
	#load the variable self
	lw $v0, 12($fp)
	move $v0, $v0
	
	# restore the stack pointer, frame pointer y return address
	addu $sp $sp 0
	# pop the top of the stack to $fp
	addi $sp $sp 4
	lw $fp, 0($sp)
	
	# pop the top of the stack to $ra
	addi $sp $sp 4
	lw $ra, 0($sp)
	
	jr $ra
	
abort_Object:
        # calling conventions
        sw $ra, 0($sp)
        addi $sp, $sp, -4
        sw $fp, 0($sp)
        addi $sp, $sp, -4
        move $fp, $sp
		
		la $a0, ObjectAbortMessage
		li $v0, 4
		syscall

		lw $t0, 12($fp)
		lw $t0, 0($t0)
		lw $t0, 4($t0)

		move $a0, $t0
		li $v0, 4
		syscall
		
        li $v0, 10
        syscall

        # calling conventions
        addi $sp, $sp, 4
        lw $fp, 0($sp)
        addi $sp, $sp, 4
        lw $ra, 0($sp)
       
        jr $ra



out_string_IO:
        # calling conventions
        sw $ra, 0($sp)
        addi $sp, $sp, -4
        sw $fp, 0($sp)
        addi $sp, $sp, -4
        move $fp, $sp


        lw $a1, 12($fp) # reference to string object
        lw $a0, 4($a1) # get the address of the value of the string 
        li $v0, 4
        syscall

        lw $v0, 16($fp)
        
        # calling conventions
        addi $sp, $sp, 4
        lw $fp, 0($sp)
        addi $sp, $sp, 4
        lw $ra, 0($sp)
       
        jr $ra

out_int_IO:
        # calling conventions
        sw $ra, 0($sp)
        addi $sp, $sp, -4
        sw $fp, 0($sp)
        addi $sp, $sp, -4
        move $fp, $sp

        lw $v1, 12($fp)
        lw $a0, 4($v1)
        li $v0, 1
        syscall
        
        # calling conventions
        addi $sp, $sp, 4
        lw $fp, 0($sp)
        addi $sp, $sp, 4
        lw $ra, 0($sp)
       
        jr $ra

in_string_IO:
        # calling conventions
        sw $ra, 0($sp)
        addi $sp, $sp, -4
        sw $fp, 0($sp)
        addi $sp, $sp, -4
        move $fp, $sp

        # Read the string to the buffer
        la $a0, IO_Buffer
        li $a1, 1000
        li $v0, 8
        syscall

        # get the length of the string to allocate the memory
        la $t0, IO_Buffer
        sw $t0, 0($sp)
        addi $sp, $sp, -4
		jal strlen
        addi $sp, $sp, 4
        lw $t0, 0($sp) # the length is now in $v0

        addi $v0, $v0, 1
        move $a0, $v0
        li $v0, 9
        syscall # in $v0 is the address of the value string
                
        la $t1, IO_Buffer # copy the string value from the buffer to the heap
        move $t2, $v0
        in_string_IO_loop:
        lb $t3, 0($t1)
        sb $t3, 0($t2)
        addi $t1, $t1, 1
        addi $t2, $t2, 1
        bgtz $t3, in_string_IO_loop
        addi $t2, $t2, -2
        li $t3, 0
        sb $t3, 0($t2)

        move $t0, $v0

        li $a0, 8
        li $v0, 9
        syscall

        la $t1, String
        sw $t0, 4($v0)
        sw $t1, 0($v0)


        # calling conventions
        addi $sp, $sp, 4
        lw $fp, 0($sp)
        addi $sp, $sp, 4
        lw $ra, 0($sp)
       
        jr $ra

in_int_IO:
        # calling conventions
        sw $ra, 0($sp)
        addi $sp, $sp, -4
        sw $fp, 0($sp)
        addi $sp, $sp, -4
        move $fp, $sp

        li $v0, 5
        syscall
        move $t0, $v0

        li $v0, 9
        li $a0, 8
        syscall

        la $t1, Int
        sw $t1, 0($v0)
        sw $t0, 4($v0)


        # calling conventions
        addi $sp, $sp, 4
        lw $fp, 0($sp)
        addi $sp, $sp, 4
        lw $ra, 0($sp)
       
        jr $ra
		






		



type_name_Object:
        # calling conventions
        sw $ra, 0($sp)
        addi $sp, $sp, -4
        sw $fp, 0($sp)
        addi $sp, $sp, -4
        move $fp, $sp

        lw $t7, 12($fp) # get the instance address
        lw $t6, 0($t7) # get the type info address
        lw $t5, 4($t6) # get the type name

        # create the String class instance to return
        li $a0, 8
        li $v0, 9
        syscall   

        la $t1, String
        sw $t1, 0($v0)
        sw $t5, 4($v0)
        
        # calling conventions
        addi $sp, $sp, 4
        lw $fp, 0($sp)
        addi $sp, $sp, 4
        lw $ra, 0($sp)
        
        jr $ra

substr_String:
        # calling conventions
        sw $ra, 0($sp)
        addi $sp, $sp, -4
        sw $fp, 0($sp)
        addi $sp, $sp, -4
        move $fp, $sp

        lw $t7, 20($fp) # get the String instance address
        lw $t0, 4($t7) # get the value of the source String

        lw $t7, 16($fp) # get the start parameter Int instance address
        lw $t1, 4($t7) # get the value of the Int

        lw $t7, 12($fp) # get the length perameter Int instance address
        lw $t2, 4($t7) # get the value of the Int

        move $a0, $t2
        li $v0, 9	
        syscall # allocate memory for the substring value
        

        li $t3, 0 # current pos in the string

        substr_String_loop1:
        beq $t3, $t1, substr_String_eloop1 # if the current pos == start pos break
        # else move the current pos
        addi $t0, $t0, 1
        addi $t3, $t3, 1
        j substr_String_loop1

        substr_String_eloop1:

        li $t3, 0
        move $t4, $v0 # move the substring address to $t4

        substr_String_loop2:
        beq $t3, $t2, substr_String_eloop2
        lb $t7, 0($t0)
        sb $t7, 0($t4)
        addi $t0, $t0, 1
        addi $t4, $t4, 1
        addi $t3, $t3, 1
        j substr_String_loop2

        substr_String_eloop2:

        move $t0, $v0
        la $t1, String
        
        li $a0, 8
        li $v0, 9
        syscall

        sw $t1, 0($v0)
        sw $t0, 4($v0)


        # calling conventions
        addi $sp, $sp, 4
        lw $fp, 0($sp)
        addi $sp, $sp, 4
        lw $ra, 0($sp)
        
        jr $ra


isvoid:
        # calling conventions
        sw $ra, 0($sp)
        addi $sp, $sp, -4
        sw $fp, 0($sp)
        addi $sp, $sp, -4
        move $fp, $sp

        lw $t0, 12($fp)
        li $t1, 0
        beq $t0, $t1, isvoid_end
        li $t0, 1
        isvoid_end:
                
        li $a0, 8
        li $v0, 9
        syscall

        la $t1, Bool
        sw $t1, 0($v0)
        sw $t0, 4($v0)

        # calling conventions
        addi $sp, $sp, 4
        lw $fp, 0($sp)
        addi $sp, $sp, 4
        lw $ra, 0($sp)
        
        jr $ra

# function to get the length of a string value
strlen:
        # calling conventions
        sw $ra, 0($sp)
        addi $sp, $sp, -4
        sw $fp, 0($sp)
        addi $sp, $sp, -4
        move $fp, $sp


        lw $a0, 12($fp)
        li $t0, 0
strlen_loop:
        lb $t1, 0($a0)
        beqz $t1, strlen_exit
        addu $a0, $a0, 1
        addu $t0, $t0, 1
        j strlen_loop
        strlen_exit:
        move $v0, $t0
        
        
        # calling conventions
        addi $sp, $sp, 4
        lw $fp, 0($sp)
        addi $sp, $sp, 4
        lw $ra, 0($sp)
        
        jr $ra


length_String:
        # calling conventions
        sw $ra, 0($sp)
        addi $sp, $sp, -4
        sw $fp, 0($sp)
        addi $sp, $sp, -4
        move $fp, $sp

        lw $v0, 12($fp) # get the string instance address
        lw $v1, 4($v0) # get the string value address

        # push the instace in the stack
        sw $v1, 0($sp)
        addi $sp, $sp, -4

        jal strlen # length at v0
        
        addi $sp, $sp, 4
        lw $t0, 0($sp)


        move $t0, $v0

        # allocate space for the Int instace
        li $a0, 8
        li $v0, 9
        syscall

        la $t1, Int
        sw $t1, 0($v0)
        sw $t0, 4($v0)
      
        # calling conventions
        addi $sp, $sp, 4
        lw $fp, 0($sp)
        addi $sp, $sp, 4
        lw $ra, 0($sp)
        
        jr $ra

	
compare:
        # calling conventions
        sw $ra, 0($sp)
        addi $sp, $sp, -4
        sw $fp, 0($sp)
        addi $sp, $sp, -4
        move $fp, $sp

		lw $t0, 12($fp)
		lw $t1, 16($fp)

		lw $t3, 0($t0)

		la $t4, Int
		beq $t3, $t4, compare_branch1

		la $t4, Bool
		beq $t3, $t4, compare_branch1

		la $t4, String
		beq $t3, $t4, compare_branch2

		j compare_values

		compare_branch1:
		lw $t0, 4($t0)
		lw $t1, 4($t1)
		
		compare_values:
		beq $t0, $t1, compare_true
		j compare_false

		
		compare_branch2:
		lw $t0, 4($t0)
		lw $t1, 4($t1)
		compare_str_loop:
		lb $t3, 0($t0)
		lb $t4, 0($t1)
		bne $t3, $t4, compare_false
		beq $t3, $zero, compare_true
		addi $t0, $t0, 1
		addi $t1, $t1, 1
		j compare_str_loop

		compare_true:
		li $t0, 1
		j compare_end

		compare_false:
		li $t0, 0

		compare_end:

		li $a0, 8
		li $v0, 9
		syscall
		la $t1, Bool
		sw $t1, 0($v0)
		sw $t0, 4($v0)


        # calling conventions
        addi $sp, $sp, 4
        lw $fp, 0($sp)
        addi $sp, $sp, 4
        lw $ra, 0($sp)
        
        jr $ra


concat_String:
        # calling conventions
        sw $ra, 0($sp)
        addi $sp, $sp, -4
        sw $fp, 0($sp)
        addi $sp, $sp, -4
        move $fp, $sp
		













