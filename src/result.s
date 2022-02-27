	.data
_List: .asciiz "List"
	.data
	.align 4
List: .word 4 _List Init_List abort_Object type_name_Object copy_Object isNil_List head_List tail_List cons_List

	.data
_Cons: .asciiz "Cons"
	.data
	.align 4
Cons: .word 12 _Cons Init_Cons abort_Object type_name_Object copy_Object isNil_Cons head_Cons tail_Cons cons_List init_Cons

	.data
_Main: .asciiz "Main"
	.data
	.align 4
Main: .word 8 _Main Init_Main abort_Object type_name_Object copy_Object out_string_IO out_int_IO in_string_IO in_int_IO print_list_Main main_Main

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
str_0: .asciiz " "

	.data
str_1: .asciiz "\n"

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
	li $a0, 8
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
	lw $v1, 44($v0)
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
isNil_List:
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
	
	# assign (add here the expr.to_string) to t_0
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
	
	sw $v0, -0($fp)
	
	# assign (add here the expr.to_string) to t_1
	#load the variable t_0
	lw $v0, -0($fp)
	sw $v0, -4($fp)
	
	# return the value of the function in the register $v0
	#load the variable t_1
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
head_List:
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
	
	lw $v0, 12($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	# assign (add here the expr.to_string) to t_2
	# calling the method abort of type List
	#load the variable self_List
	lw $v0, 12($fp)
	lw $v0, 0($v0)
	lw $v1, 12($v0)
	jal $v1
	# pop the top of the stack to $v1
	addi $sp $sp 4
	lw $v1, 0($sp)
	
	sw $v0, -0($fp)
	
	# assign (add here the expr.to_string) to t_3
	# Creating Int instance for atomic 0
	li $a0, 8
	li $v0, 9
	syscall
	la $t0, Int
	li $t1, 0
	sw $t0, 0($v0)
	sw $t1, 4($v0)
	
	sw $v0, -4($fp)
	
	# return the value of the function in the register $v0
	#load the variable t_3
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
tail_List:
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
	
	lw $v0, 12($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	# assign (add here the expr.to_string) to t_4
	# calling the method abort of type List
	#load the variable self_List
	lw $v0, 12($fp)
	lw $v0, 0($v0)
	lw $v1, 12($v0)
	jal $v1
	# pop the top of the stack to $v1
	addi $sp $sp 4
	lw $v1, 0($sp)
	
	sw $v0, -0($fp)
	
	# assign (add here the expr.to_string) to t_5
	#load the variable self_List
	lw $v0, 12($fp)
	sw $v0, -4($fp)
	
	# return the value of the function in the register $v0
	#load the variable t_5
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
cons_List:
	# save the return address and frame pointer
	# push $ra to the stack
	sw $ra, 0($sp)
	addi $sp $sp -4
	
	# push $fp to the stack
	sw $fp, 0($sp)
	addi $sp $sp -4
	
	# update the frame pointer and allocate the frame in the stack
	move $fp $sp
	subu $sp $sp 28
	
	# assign (add here the expr.to_string) to t_7
	li $a0, 12
	li $v0, 9
	syscall
	la $a0, Cons
	sw $a0,  0($v0)
	sw $v0, -0($fp)
	
	lw $v0, -0($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	# assign (add here the expr.to_string) to t_8
	# calling the method Init_Cons of type Cons
	#load the variable t_7
	lw $v0, -0($fp)
	lw $v0, 0($v0)
	lw $v1, 8($v0)
	jal $v1
	# pop the top of the stack to $v1
	addi $sp $sp 4
	lw $v1, 0($sp)
	
	sw $v0, -4($fp)
	
	# assign (add here the expr.to_string) to t_9
	#load the variable t_8
	lw $v0, -4($fp)
	sw $v0, -8($fp)
	
	# assign (add here the expr.to_string) to t_10
	#load the variable i_6
	lw $v0, 12($fp)
	sw $v0, -12($fp)
	
	# assign (add here the expr.to_string) to t_11
	#load the variable self_List
	lw $v0, 16($fp)
	sw $v0, -16($fp)
	
	lw $v0, -8($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	lw $v0, -12($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	lw $v0, -16($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	# assign (add here the expr.to_string) to t_12
	# calling the method init of type Cons
	#load the variable t_9
	lw $v0, -8($fp)
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
	
	sw $v0, -20($fp)
	
	# assign (add here the expr.to_string) to t_13
	#load the variable t_12
	lw $v0, -20($fp)
	sw $v0, -24($fp)
	
	# return the value of the function in the register $v0
	#load the variable t_13
	lw $v0, -24($fp)
	move $v0, $v0
	
	# restore the stack pointer, frame pointer y return address
	addu $sp $sp 28
	# pop the top of the stack to $fp
	addi $sp $sp 4
	lw $fp, 0($sp)
	
	# pop the top of the stack to $ra
	addi $sp $sp 4
	lw $ra, 0($sp)
	
	jr $ra
	
	.text
Init_List:
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
isNil_Cons:
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
	
	# assign (add here the expr.to_string) to t_14
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
	
	sw $v0, -0($fp)
	
	# assign (add here the expr.to_string) to t_15
	#load the variable t_14
	lw $v0, -0($fp)
	sw $v0, -4($fp)
	
	# return the value of the function in the register $v0
	#load the variable t_15
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
head_Cons:
	# save the return address and frame pointer
	# push $ra to the stack
	sw $ra, 0($sp)
	addi $sp $sp -4
	
	# push $fp to the stack
	sw $fp, 0($sp)
	addi $sp $sp -4
	
	# update the frame pointer and allocate the frame in the stack
	move $fp $sp
	subu $sp $sp 4
	
	# assign (add here the expr.to_string) to t_16
	lw $v1, 12($fp)
	lw $v0, 4($v1)
	sw $v0, -0($fp)
	
	# return the value of the function in the register $v0
	#load the variable t_16
	lw $v0, -0($fp)
	move $v0, $v0
	
	# restore the stack pointer, frame pointer y return address
	addu $sp $sp 4
	# pop the top of the stack to $fp
	addi $sp $sp 4
	lw $fp, 0($sp)
	
	# pop the top of the stack to $ra
	addi $sp $sp 4
	lw $ra, 0($sp)
	
	jr $ra
	
	.text
tail_Cons:
	# save the return address and frame pointer
	# push $ra to the stack
	sw $ra, 0($sp)
	addi $sp $sp -4
	
	# push $fp to the stack
	sw $fp, 0($sp)
	addi $sp $sp -4
	
	# update the frame pointer and allocate the frame in the stack
	move $fp $sp
	subu $sp $sp 4
	
	# assign (add here the expr.to_string) to t_17
	lw $v1, 12($fp)
	lw $v0, 8($v1)
	sw $v0, -0($fp)
	
	# return the value of the function in the register $v0
	#load the variable t_17
	lw $v0, -0($fp)
	move $v0, $v0
	
	# restore the stack pointer, frame pointer y return address
	addu $sp $sp 4
	# pop the top of the stack to $fp
	addi $sp $sp 4
	lw $fp, 0($sp)
	
	# pop the top of the stack to $ra
	addi $sp $sp 4
	lw $ra, 0($sp)
	
	jr $ra
	
	.text
init_Cons:
	# save the return address and frame pointer
	# push $ra to the stack
	sw $ra, 0($sp)
	addi $sp $sp -4
	
	# push $fp to the stack
	sw $fp, 0($sp)
	addi $sp $sp -4
	
	# update the frame pointer and allocate the frame in the stack
	move $fp $sp
	subu $sp $sp 4
	
	# Setting value of the attribute car in the instance self_Cons to i_18
	#load the variable i_18
	lw $v0, 16($fp)
	move $s2, $v0
	lw $v1, 20($fp)
	sw $s2, 4($v1)
	
	# Setting value of the attribute cdr in the instance self_Cons to rest_19
	#load the variable rest_19
	lw $v0, 12($fp)
	move $s2, $v0
	lw $v1, 20($fp)
	sw $s2, 8($v1)
	
	# assign (add here the expr.to_string) to t_20
	#load the variable self_Cons
	lw $v0, 20($fp)
	sw $v0, -0($fp)
	
	# return the value of the function in the register $v0
	#load the variable t_20
	lw $v0, -0($fp)
	move $v0, $v0
	
	# restore the stack pointer, frame pointer y return address
	addu $sp $sp 4
	# pop the top of the stack to $fp
	addi $sp $sp 4
	lw $fp, 0($sp)
	
	# pop the top of the stack to $ra
	addi $sp $sp 4
	lw $ra, 0($sp)
	
	jr $ra
	
	.text
Init_Cons:
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
	
	# assign (add here the expr.to_string) to self
	jal Init_List
	# pop the top of the stack to $v1
	addi $sp $sp 4
	lw $v1, 0($sp)
	
	sw $v0, 12($fp)
	
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
print_list_Main:
	# save the return address and frame pointer
	# push $ra to the stack
	sw $ra, 0($sp)
	addi $sp $sp -4
	
	# push $fp to the stack
	sw $fp, 0($sp)
	addi $sp $sp -4
	
	# update the frame pointer and allocate the frame in the stack
	move $fp $sp
	subu $sp $sp 76
	
	# assign (add here the expr.to_string) to t_22
	#load the variable l_21
	lw $v0, 12($fp)
	sw $v0, -0($fp)
	
	lw $v0, -0($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	# assign (add here the expr.to_string) to t_23
	# calling the method isNil of type List
	#load the variable t_22
	lw $v0, -0($fp)
	lw $v0, 0($v0)
	lw $v1, 24($v0)
	jal $v1
	# pop the top of the stack to $v1
	addi $sp $sp 4
	lw $v1, 0($sp)
	
	sw $v0, -4($fp)
	
	# assign (add here the expr.to_string) to t_24
	#load the variable t_23
	lw $v0, -4($fp)
	sw $v0, -8($fp)
	
	lw $t1, -8($fp)
	lw $t0, 4($t1)
	bne $t0, $zero, then_0
	# assign (add here the expr.to_string) to t_26
	#load the variable l_21
	lw $v0, 12($fp)
	sw $v0, -16($fp)
	
	lw $v0, -16($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	# assign (add here the expr.to_string) to t_27
	# calling the method head of type List
	#load the variable t_26
	lw $v0, -16($fp)
	lw $v0, 0($v0)
	lw $v1, 28($v0)
	jal $v1
	# pop the top of the stack to $v1
	addi $sp $sp 4
	lw $v1, 0($sp)
	
	sw $v0, -20($fp)
	
	# assign (add here the expr.to_string) to t_28
	#load the variable t_27
	lw $v0, -20($fp)
	sw $v0, -24($fp)
	
	lw $v0, 16($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	lw $v0, -24($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	# assign (add here the expr.to_string) to t_29
	# calling the method out_int of type Main
	#load the variable self_Main
	lw $v0, 16($fp)
	lw $v0, 0($v0)
	lw $v1, 28($v0)
	jal $v1
	# pop the top of the stack to $v1
	addi $sp $sp 4
	lw $v1, 0($sp)
	
	# pop the top of the stack to $v1
	addi $sp $sp 4
	lw $v1, 0($sp)
	
	sw $v0, -28($fp)
	
	# assign (add here the expr.to_string) to t_30
	#load the string str_0
	li $a0, 8
	li $v0, 9
	syscall
	la $v1, String
	sw $v1, 0($v0)
	la $v1, str_0
	sw $v1, 4($v0)
	sw $v0, -32($fp)
	
	# assign (add here the expr.to_string) to t_31
	#load the variable t_30
	lw $v0, -32($fp)
	sw $v0, -36($fp)
	
	lw $v0, 16($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	lw $v0, -36($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	# assign (add here the expr.to_string) to t_32
	# calling the method out_string of type Main
	#load the variable self_Main
	lw $v0, 16($fp)
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
	
	# assign (add here the expr.to_string) to t_33
	#load the variable l_21
	lw $v0, 12($fp)
	sw $v0, -44($fp)
	
	lw $v0, -44($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	# assign (add here the expr.to_string) to t_34
	# calling the method tail of type List
	#load the variable t_33
	lw $v0, -44($fp)
	lw $v0, 0($v0)
	lw $v1, 32($v0)
	jal $v1
	# pop the top of the stack to $v1
	addi $sp $sp 4
	lw $v1, 0($sp)
	
	sw $v0, -48($fp)
	
	# assign (add here the expr.to_string) to t_35
	#load the variable t_34
	lw $v0, -48($fp)
	sw $v0, -52($fp)
	
	lw $v0, 16($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	lw $v0, -52($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	# assign (add here the expr.to_string) to t_36
	# calling the method print_list of type Main
	#load the variable self_Main
	lw $v0, 16($fp)
	lw $v0, 0($v0)
	lw $v1, 40($v0)
	jal $v1
	# pop the top of the stack to $v1
	addi $sp $sp 4
	lw $v1, 0($sp)
	
	# pop the top of the stack to $v1
	addi $sp $sp 4
	lw $v1, 0($sp)
	
	sw $v0, -56($fp)
	
	# assign (add here the expr.to_string) to t_25
	#load the variable t_36
	lw $v0, -56($fp)
	sw $v0, -12($fp)
	
	j ifend_0
	then_0:
	# assign (add here the expr.to_string) to t_37
	#load the string str_1
	li $a0, 8
	li $v0, 9
	syscall
	la $v1, String
	sw $v1, 0($v0)
	la $v1, str_1
	sw $v1, 4($v0)
	sw $v0, -60($fp)
	
	# assign (add here the expr.to_string) to t_38
	#load the variable t_37
	lw $v0, -60($fp)
	sw $v0, -64($fp)
	
	lw $v0, 16($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	lw $v0, -64($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	# assign (add here the expr.to_string) to t_39
	# calling the method out_string of type Main
	#load the variable self_Main
	lw $v0, 16($fp)
	lw $v0, 0($v0)
	lw $v1, 24($v0)
	jal $v1
	# pop the top of the stack to $v1
	addi $sp $sp 4
	lw $v1, 0($sp)
	
	# pop the top of the stack to $v1
	addi $sp $sp 4
	lw $v1, 0($sp)
	
	sw $v0, -68($fp)
	
	# assign (add here the expr.to_string) to t_25
	#load the variable t_39
	lw $v0, -68($fp)
	sw $v0, -12($fp)
	
	ifend_0:
	# assign (add here the expr.to_string) to t_40
	#load the variable t_25
	lw $v0, -12($fp)
	sw $v0, -72($fp)
	
	# return the value of the function in the register $v0
	#load the variable t_40
	lw $v0, -72($fp)
	move $v0, $v0
	
	# restore the stack pointer, frame pointer y return address
	addu $sp $sp 76
	# pop the top of the stack to $fp
	addi $sp $sp 4
	lw $fp, 0($sp)
	
	# pop the top of the stack to $ra
	addi $sp $sp 4
	lw $ra, 0($sp)
	
	jr $ra
	
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
	subu $sp $sp 112
	
	# assign (add here the expr.to_string) to t_41
	li $a0, 4
	li $v0, 9
	syscall
	la $a0, List
	sw $a0,  0($v0)
	sw $v0, -0($fp)
	
	lw $v0, -0($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	# assign (add here the expr.to_string) to t_42
	# calling the method Init_List of type List
	#load the variable t_41
	lw $v0, -0($fp)
	lw $v0, 0($v0)
	lw $v1, 8($v0)
	jal $v1
	# pop the top of the stack to $v1
	addi $sp $sp 4
	lw $v1, 0($sp)
	
	sw $v0, -4($fp)
	
	# assign (add here the expr.to_string) to t_43
	#load the variable t_42
	lw $v0, -4($fp)
	sw $v0, -8($fp)
	
	# assign (add here the expr.to_string) to t_44
	# Creating Int instance for atomic 1
	li $a0, 8
	li $v0, 9
	syscall
	la $t0, Int
	li $t1, 1
	sw $t0, 0($v0)
	sw $t1, 4($v0)
	
	sw $v0, -12($fp)
	
	lw $v0, -8($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	lw $v0, -12($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	# assign (add here the expr.to_string) to t_45
	# calling the method cons of type List
	#load the variable t_43
	lw $v0, -8($fp)
	lw $v0, 0($v0)
	lw $v1, 36($v0)
	jal $v1
	# pop the top of the stack to $v1
	addi $sp $sp 4
	lw $v1, 0($sp)
	
	# pop the top of the stack to $v1
	addi $sp $sp 4
	lw $v1, 0($sp)
	
	sw $v0, -16($fp)
	
	# assign (add here the expr.to_string) to t_46
	#load the variable t_45
	lw $v0, -16($fp)
	sw $v0, -20($fp)
	
	# assign (add here the expr.to_string) to t_47
	# Creating Int instance for atomic 2
	li $a0, 8
	li $v0, 9
	syscall
	la $t0, Int
	li $t1, 2
	sw $t0, 0($v0)
	sw $t1, 4($v0)
	
	sw $v0, -24($fp)
	
	lw $v0, -20($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	lw $v0, -24($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	# assign (add here the expr.to_string) to t_48
	# calling the method cons of type List
	#load the variable t_46
	lw $v0, -20($fp)
	lw $v0, 0($v0)
	lw $v1, 36($v0)
	jal $v1
	# pop the top of the stack to $v1
	addi $sp $sp 4
	lw $v1, 0($sp)
	
	# pop the top of the stack to $v1
	addi $sp $sp 4
	lw $v1, 0($sp)
	
	sw $v0, -28($fp)
	
	# assign (add here the expr.to_string) to t_49
	#load the variable t_48
	lw $v0, -28($fp)
	sw $v0, -32($fp)
	
	# assign (add here the expr.to_string) to t_50
	# Creating Int instance for atomic 3
	li $a0, 8
	li $v0, 9
	syscall
	la $t0, Int
	li $t1, 3
	sw $t0, 0($v0)
	sw $t1, 4($v0)
	
	sw $v0, -36($fp)
	
	lw $v0, -32($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	lw $v0, -36($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	# assign (add here the expr.to_string) to t_51
	# calling the method cons of type List
	#load the variable t_49
	lw $v0, -32($fp)
	lw $v0, 0($v0)
	lw $v1, 36($v0)
	jal $v1
	# pop the top of the stack to $v1
	addi $sp $sp 4
	lw $v1, 0($sp)
	
	# pop the top of the stack to $v1
	addi $sp $sp 4
	lw $v1, 0($sp)
	
	sw $v0, -40($fp)
	
	# assign (add here the expr.to_string) to t_52
	#load the variable t_51
	lw $v0, -40($fp)
	sw $v0, -44($fp)
	
	# assign (add here the expr.to_string) to t_53
	# Creating Int instance for atomic 4
	li $a0, 8
	li $v0, 9
	syscall
	la $t0, Int
	li $t1, 4
	sw $t0, 0($v0)
	sw $t1, 4($v0)
	
	sw $v0, -48($fp)
	
	lw $v0, -44($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	lw $v0, -48($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	# assign (add here the expr.to_string) to t_54
	# calling the method cons of type List
	#load the variable t_52
	lw $v0, -44($fp)
	lw $v0, 0($v0)
	lw $v1, 36($v0)
	jal $v1
	# pop the top of the stack to $v1
	addi $sp $sp 4
	lw $v1, 0($sp)
	
	# pop the top of the stack to $v1
	addi $sp $sp 4
	lw $v1, 0($sp)
	
	sw $v0, -52($fp)
	
	# assign (add here the expr.to_string) to t_55
	#load the variable t_54
	lw $v0, -52($fp)
	sw $v0, -56($fp)
	
	# assign (add here the expr.to_string) to t_56
	# Creating Int instance for atomic 5
	li $a0, 8
	li $v0, 9
	syscall
	la $t0, Int
	li $t1, 5
	sw $t0, 0($v0)
	sw $t1, 4($v0)
	
	sw $v0, -60($fp)
	
	lw $v0, -56($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	lw $v0, -60($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	# assign (add here the expr.to_string) to t_57
	# calling the method cons of type List
	#load the variable t_55
	lw $v0, -56($fp)
	lw $v0, 0($v0)
	lw $v1, 36($v0)
	jal $v1
	# pop the top of the stack to $v1
	addi $sp $sp 4
	lw $v1, 0($sp)
	
	# pop the top of the stack to $v1
	addi $sp $sp 4
	lw $v1, 0($sp)
	
	sw $v0, -64($fp)
	
	# Setting value of the attribute mylist in the instance self_Main to t_57
	#load the variable t_57
	lw $v0, -64($fp)
	move $s2, $v0
	lw $v1, 12($fp)
	sw $s2, 4($v1)
	
	while_0:
	# assign (add here the expr.to_string) to t_58
	lw $v1, 12($fp)
	lw $v0, 4($v1)
	sw $v0, -68($fp)
	
	lw $v0, -68($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	# assign (add here the expr.to_string) to t_59
	# calling the method isNil of type List
	#load the variable t_58
	lw $v0, -68($fp)
	lw $v0, 0($v0)
	lw $v1, 24($v0)
	jal $v1
	# pop the top of the stack to $v1
	addi $sp $sp 4
	lw $v1, 0($sp)
	
	sw $v0, -72($fp)
	
	# assign (add here the expr.to_string) to t_60
	#load the variable t_59
	lw $v0, -72($fp)
	sw $v0, -76($fp)
	
	# assign (add here the expr.to_string) to t_61
	#load the variable t_60
	lw $v0, -76($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	# Creating Int instance for atomic 0
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
	
	lw $t0, 4($v0)
	li $t1, 1
	xor $t0, $t0, $t1
	andi $t0, $t0, 0x01
	sw $t0, 4($v0)
	sw $v0, -80($fp)
	
	# assign (add here the expr.to_string) to t_62
	#load the variable t_61
	lw $v0, -80($fp)
	sw $v0, -84($fp)
	
	lw $t1, -84($fp)
	lw $t0, 4($t1)
	bne $t0, $zero, body_0
	j pool_0
	body_0:
	# assign (add here the expr.to_string) to t_64
	lw $v1, 12($fp)
	lw $v0, 4($v1)
	sw $v0, -92($fp)
	
	lw $v0, 12($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	lw $v0, -92($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	# assign (add here the expr.to_string) to t_65
	# calling the method print_list of type Main
	#load the variable self_Main
	lw $v0, 12($fp)
	lw $v0, 0($v0)
	lw $v1, 40($v0)
	jal $v1
	# pop the top of the stack to $v1
	addi $sp $sp 4
	lw $v1, 0($sp)
	
	# pop the top of the stack to $v1
	addi $sp $sp 4
	lw $v1, 0($sp)
	
	sw $v0, -96($fp)
	
	# assign (add here the expr.to_string) to t_66
	lw $v1, 12($fp)
	lw $v0, 4($v1)
	sw $v0, -100($fp)
	
	lw $v0, -100($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	# assign (add here the expr.to_string) to t_67
	# calling the method tail of type List
	#load the variable t_66
	lw $v0, -100($fp)
	lw $v0, 0($v0)
	lw $v1, 32($v0)
	jal $v1
	# pop the top of the stack to $v1
	addi $sp $sp 4
	lw $v1, 0($sp)
	
	sw $v0, -104($fp)
	
	# Setting value of the attribute mylist in the instance self_Main to t_67
	#load the variable t_67
	lw $v0, -104($fp)
	move $s2, $v0
	lw $v1, 12($fp)
	sw $s2, 4($v1)
	
	# assign (add here the expr.to_string) to t_63
	#load the variable t_67
	lw $v0, -104($fp)
	sw $v0, -88($fp)
	
	j while_0
	pool_0:
	# assign (add here the expr.to_string) to t_68
	#load the variable t_63
	lw $v0, -88($fp)
	sw $v0, -108($fp)
	
	# return the value of the function in the register $v0
	#load the variable t_68
	lw $v0, -108($fp)
	move $v0, $v0
	
	# restore the stack pointer, frame pointer y return address
	addu $sp $sp 112
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
	
	# assign (add here the expr.to_string) to self
	jal Init_IO
	# pop the top of the stack to $v1
	addi $sp $sp 4
	lw $v1, 0($sp)
	
	sw $v0, 12($fp)
	
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













