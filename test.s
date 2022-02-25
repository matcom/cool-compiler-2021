.globl main

.data

msg: .asciiz "hello"

data_0_abort_msg: .asciiz "Program Halted!"
data_1_abort_msg: .asciiz "Program Halted!"
data_2_type_name_Object: .asciiz "Object"
data_3_type_name_Int: .asciiz "Int"
data_4_type_name_Bool: .asciiz "Bool"
data_5_type_name_String: .asciiz "String"
data_6_type_name_IO: .asciiz "IO"
data_7_type_name_Main: .asciiz "Main"
data_8_string: .asciiz "Hello, World.\n"
Object: .word Object_abort,Object_type_name,Object_copy
Int: .word Object_abort,Int_type_name,Object_copy
Bool: .word Object_abort,Bool_type_name,Object_copy
String: .word Object_abort,String_type_name,Object_copy,String_length,String_concat,String_substr
IO: .word Object_abort,IO_type_name,Object_copy,IO_out_string,IO_out_int,IO_in_string,IO_in_int
Main: .word Object_abort,Main_type_name,Object_copy,IO_out_string,IO_out_int,IO_in_string,IO_in_int,Main_main

.text

main:
    la $t0, Main
    lw $t1, 12($t0)
    jalr $t1

	li $v0, 10
	syscall


F1:
	li $v0, 10
	syscall
IO_out_string:
	li $v0, 4
	la $a0, msg
	syscall
    jr $ra


Object_abort:
	move $t2, $fp 	#save previous FP value
	move $fp, $sp 	#FP <- SP
	addi $sp,  $sp, 4 	#push local vars
	la $t0, data_0_abort_msg 	#LOAD
	sw $t0, 0($fp) 	#Save loaded value in destination
	li $v0, 4 	#PRINT
	lw $a0, 0($fp) 	#
	syscall 	#
	li $v0, 10 	#EXIT
	syscall 	#
Object_copy:
	move $t9, $fp 	#save previous FP value
	move $fp, $sp 	#FP <- SP
	addi $sp,  $sp, 4 	#push local vars
	la $t3, data_1_abort_msg 	#LOAD
	sw $t3, 0($fp) 	#Save loaded value in destination
	li $v0, 4 	#PRINT
	lw $a0, 0($fp) 	#
	syscall 	#
	li $v0, 10 	#EXIT
	syscall 	#
Object_type_name:
	move $t7, $fp 	#save previous FP value
	move $fp, $sp 	#FP <- SP
	addi $sp,  $sp, 8 	#push local vars
	la $t0, data_2_type_name_Object 	#LOAD
	sw $t0, 0($fp) 	#Save loaded value in destination
	lw $t2, 0($fp) 	#Obtain alue of Arg
	sw $t2, 0($sp) 	#Save Arg in Stack
	addi $sp,  $sp, 4 	#Move Stack
	jal String_init 	#Jump to function and save link
	lw $t0, 0($sp) 	#
	sw $t0, 4($fp) 	#
	addi $sp,  $sp, -4 	#Remove args from stack
	lw $t2, 4($fp) 	#Obtain return value
	addi $sp,  $sp, -8 	#Remove locals from Stack
	sw $t2, 0($sp) 	#Save return value in Stack
	move $fp, $t7 	#restore FP
	jr $ra 	#RETURN
Int_type_name:
	move $t7, $fp 	#save previous FP value
	move $fp, $sp 	#FP <- SP
	addi $sp,  $sp, 8 	#push local vars
	la $t0, data_3_type_name_Int 	#LOAD
	sw $t0, 0($fp) 	#Save loaded value in destination
	lw $t7, 0($fp) 	#Obtain alue of Arg
	sw $t7, 0($sp) 	#Save Arg in Stack
	addi $sp,  $sp, 4 	#Move Stack
	jal String_init 	#Jump to function and save link
	lw $t0, 0($sp) 	#
	sw $t0, 4($fp) 	#
	addi $sp,  $sp, -4 	#Remove args from stack
	lw $t8, 4($fp) 	#Obtain return value
	addi $sp,  $sp, -8 	#Remove locals from Stack
	sw $t8, 0($sp) 	#Save return value in Stack
	move $fp, $t7 	#restore FP
	jr $ra 	#RETURN
Bool_type_name:
	move $t4, $fp 	#save previous FP value
	move $fp, $sp 	#FP <- SP
	addi $sp,  $sp, 8 	#push local vars
	la $t3, data_4_type_name_Bool 	#LOAD
	sw $t3, 0($fp) 	#Save loaded value in destination
	lw $t9, 0($fp) 	#Obtain alue of Arg
	sw $t9, 0($sp) 	#Save Arg in Stack
	addi $sp,  $sp, 4 	#Move Stack
	jal String_init 	#Jump to function and save link
	lw $t9, 0($sp) 	#
	sw $t9, 4($fp) 	#
	addi $sp,  $sp, -4 	#Remove args from stack
	lw $t6, 4($fp) 	#Obtain return value
	addi $sp,  $sp, -8 	#Remove locals from Stack
	sw $t6, 0($sp) 	#Save return value in Stack
	move $fp, $t4 	#restore FP
	jr $ra 	#RETURN
String_type_name:
	move $t3, $fp 	#save previous FP value
	move $fp, $sp 	#FP <- SP
	addi $sp,  $sp, 8 	#push local vars
	la $t7, data_5_type_name_String 	#LOAD
	sw $t7, 0($fp) 	#Save loaded value in destination
	lw $t4, 0($fp) 	#Obtain alue of Arg
	sw $t4, 0($sp) 	#Save Arg in Stack
	addi $sp,  $sp, 4 	#Move Stack
	jal String_init 	#Jump to function and save link
	lw $t8, 0($sp) 	#
	sw $t8, 4($fp) 	#
	addi $sp,  $sp, -4 	#Remove args from stack
	lw $t2, 4($fp) 	#Obtain return value
	addi $sp,  $sp, -8 	#Remove locals from Stack
	sw $t2, 0($sp) 	#Save return value in Stack
	move $fp, $t3 	#restore FP
	jr $ra 	#RETURN
IO_type_name:
	move $t3, $fp 	#save previous FP value
	move $fp, $sp 	#FP <- SP
	addi $sp,  $sp, 8 	#push local vars
	la $t2, data_6_type_name_IO 	#LOAD
	sw $t2, 0($fp) 	#Save loaded value in destination
	lw $t3, 0($fp) 	#Obtain alue of Arg
	sw $t3, 0($sp) 	#Save Arg in Stack
	addi $sp,  $sp, 4 	#Move Stack
	jal String_init 	#Jump to function and save link
	lw $t0, 0($sp) 	#
	sw $t0, 4($fp) 	#
	addi $sp,  $sp, -4 	#Remove args from stack
	lw $t8, 4($fp) 	#Obtain return value
	addi $sp,  $sp, -8 	#Remove locals from Stack
	sw $t8, 0($sp) 	#Save return value in Stack
	move $fp, $t3 	#restore FP
	jr $ra 	#RETURN
Main_type_name:
	move $t1, $fp 	#save previous FP value
	move $fp, $sp 	#FP <- SP
	addi $sp,  $sp, 8 	#push local vars
	la $t4, data_7_type_name_Main 	#LOAD
	sw $t4, 0($fp) 	#Save loaded value in destination
	lw $t3, 0($fp) 	#Obtain alue of Arg
	sw $t3, 0($sp) 	#Save Arg in Stack
	addi $sp,  $sp, 4 	#Move Stack
	jal String_init 	#Jump to function and save link
	lw $t0, 0($sp) 	#
	sw $t0, 4($fp) 	#
	addi $sp,  $sp, -4 	#Remove args from stack
	lw $t3, 4($fp) 	#Obtain return value
	addi $sp,  $sp, -8 	#Remove locals from Stack
	sw $t3, 0($sp) 	#Save return value in Stack
	move $fp, $t1 	#restore FP
	jr $ra 	#RETURN
IO_out_int:
	move $t2, $fp 	#save previous FP value
	move $fp, $sp 	#FP <- SP
	addi $sp,  $sp, 0 	#push local vars
	li $v0, 1 	#PRINT
	lw $a0, -8($fp) 	#
	syscall 	#
	lw $t2, -4($fp) 	#Obtain return value
	addi $sp,  $sp, 0 	#Remove locals from Stack
	sw $t2, 0($sp) 	#Save return value in Stack
	move $fp, $t2 	#restore FP
	jr $ra 	#RETURN
IO_in_string:
	move $t3, $fp 	#save previous FP value
	move $fp, $sp 	#FP <- SP
	addi $sp,  $sp, 4 	#push local vars
	li $v0, 5 	#READ
	syscall 	#
	sw $a0, 0($fp) 	#Save readed value
	lw $t8, 0($fp) 	#Obtain return value
	addi $sp,  $sp, -4 	#Remove locals from Stack
	sw $t8, 0($sp) 	#Save return value in Stack
	move $fp, $t3 	#restore FP
	jr $ra 	#RETURN
IO_in_int:
	move $t3, $fp 	#save previous FP value
	move $fp, $sp 	#FP <- SP
	addi $sp,  $sp, 4 	#push local vars
	li $v0, 8 	#READ
	syscall 	#
	sw $a0, 0($fp) 	#Save readed value
	lw $t7, 0($fp) 	#Obtain return value
	addi $sp,  $sp, -4 	#Remove locals from Stack
	sw $t7, 0($sp) 	#Save return value in Stack
	move $fp, $t3 	#restore FP
	jr $ra 	#RETURN
String_length:
	move $t0, $fp 	#save previous FP value
	move $fp, $sp 	#FP <- SP
	addi $sp,  $sp, 8 	#push local vars
	la $a0, 0($fp) 	#Calculate Lenght
	li $t3, 0 	#
loop1:
	lb $t9, 0($a0) 	#
	beqz $t9, exit1 	#
	addi $a0,  $a0, 1 	#
	addi $t3,  $t3, 1 	#
	j loop1 	#
exit1:
	sw $t3, -4($fp) 	#Save Calculated Length
	lw $t6, 0($fp) 	#Obtain alue of Arg
	sw $t6, 0($sp) 	#Save Arg in Stack
	addi $sp,  $sp, 4 	#Move Stack
	jal Int_init 	#Jump to function and save link
	lw $t8, 0($sp) 	#
	sw $t8, 4($fp) 	#
	addi $sp,  $sp, -4 	#Remove args from stack
	lw $t9, 4($fp) 	#Obtain return value
	addi $sp,  $sp, -8 	#Remove locals from Stack
	sw $t9, 0($sp) 	#Save return value in Stack
	move $fp, $t0 	#restore FP
	jr $ra 	#RETURN
String_concat:
	move $t8, $fp 	#save previous FP value
	move $fp, $sp 	#FP <- SP
	addi $sp,  $sp, 20 	#push local vars
	la $a0, -4($fp) 	#Calculate Lenght
	li $t5, 0 	#
loop2:
	lb $t8, 0($a0) 	#
	beqz $t8, exit2 	#
	addi $a0,  $a0, 1 	#
	addi $t5,  $t5, 1 	#
	j loop2 	#
exit2:
	sw $t5, 4($fp) 	#Save Calculated Length
	la $a0, -8($fp) 	#Calculate Lenght
	li $t7, 0 	#
loop3:
	lb $t4, 0($a0) 	#
	beqz $t4, exit3 	#
	addi $a0,  $a0, 1 	#
	addi $t7,  $t7, 1 	#
	j loop3 	#
exit3:
	sw $t7, 8($fp) 	#Save Calculated Length
	sw $t6, 4($fp) 	#Value is string
	sw $t2, 8($fp) 	#Value is string
	add $t8,  $t6, $t2 	#Plus
	sw $t8, 12($fp) 	#Save result of plus
	lw $t9, 12($fp) 	#Concat two Strings
	li $v0, 9 	#
	move $a0, $t9 	#
	syscall 	#
	la $t3, 0($a0) 	#
	la $a1, -4($fp) 	#
	la $a2, -8($fp) 	#
loop4:
	lb $t9, 0($a1) 	#
	lb $t9, 0($a0) 	#
	beqz $a1, exit4 	#
	addi $a0,  $a0, 1 	#
	addi $a1,  $a1, 1 	#
	j loop4 	#
exit4:
loop5:
	lb $t9, 0($a2) 	#
	lb $t9, 0($a0) 	#
	beqz $a2, exit5 	#
	addi $a0,  $a0, 1 	#
	addi $a2,  $a2, 1 	#
	j loop5 	#
exit5:
	sw $t3, 0($fp) 	#Save concated Strings
	lw $t6, 0($fp) 	#Obtain alue of Arg
	sw $t6, 0($sp) 	#Save Arg in Stack
	addi $sp,  $sp, 4 	#Move Stack
	jal String_init 	#Jump to function and save link
	lw $t3, 0($sp) 	#
	sw $t3, 16($fp) 	#
	addi $sp,  $sp, -4 	#Remove args from stack
	lw $t2, 16($fp) 	#Obtain return value
	addi $sp,  $sp, -20 	#Remove locals from Stack
	sw $t2, 0($sp) 	#Save return value in Stack
	move $fp, $t8 	#restore FP
	jr $ra 	#RETURN
String_substr:
	move $t7, $fp 	#save previous FP value
	move $fp, $sp 	#FP <- SP
	addi $sp,  $sp, 4 	#push local vars
	lw $t7, -12($fp) 	#Obtain substring
	lw $t4, -8($fp) 	#
	li $v0, 9 	#
	move $a0, $t1 	#
	syscall 	#
	la $t0, 0($a0) 	#
	la $a1, -4($fp) 	#
	add $a1,  $a1, $t7 	#
loop6:
	lb $t1, 0($a1) 	#
	lb $t1, 0($a0) 	#
	beqz $t7, exit6 	#
	addi $a0,  $a0, 1 	#
	addi $a1,  $a1, 1 	#
	addi $t7,  $t7, 1 	#
	j loop6 	#
exit6:
	sw $t0, 0($fp) 	#Save substring
	lw $t5, 0($fp) 	#Obtain return value
	addi $sp,  $sp, -4 	#Remove locals from Stack
	sw $t5, 0($sp) 	#Save return value in Stack
	move $fp, $t7 	#restore FP
	jr $ra 	#RETURN
Object_init:
	move $t7, $fp 	#save previous FP value
	move $fp, $sp 	#FP <- SP
	addi $sp,  $sp, 4 	#push local vars
	li $v0, 9 	#Allocating instance of type Object
	li $a0, 4 	#Save 4 bytes
	syscall 	#
	la $t3, Object 	#Save type address in register
	sw $t3, 0($v0) 	#Save type address in firts position of memory allocated
	addi $v0,  $v0, 4 	#Move offset of instance (type addres is in index -1)
	sw $v0, 0($fp) 	#Save instance address in destination
	lw $t5, 0($fp) 	#Obtain return value
	addi $sp,  $sp, -4 	#Remove locals from Stack
	sw $t5, 0($sp) 	#Save return value in Stack
	move $fp, $t7 	#restore FP
	jr $ra 	#RETURN
Int_init:
	move $t7, $fp 	#save previous FP value
	move $fp, $sp 	#FP <- SP
	addi $sp,  $sp, 4 	#push local vars
	li $v0, 9 	#Allocating instance of type Int
	li $a0, 4 	#Save 4 bytes
	syscall 	#
	la $t0, Int 	#Save type address in register
	sw $t0, 0($v0) 	#Save type address in firts position of memory allocated
	addi $v0,  $v0, 4 	#Move offset of instance (type addres is in index -1)
	sw $v0, 0($fp) 	#Save instance address in destination
	lw $t1, -4($fp) 	#Dir of instance of attribute to set
	lw $t2, 0($fp) 	#Obtain value from source dir
	sw $t1, 0($t2) 	#Save value in attribute of index 0
	lw $t3, 0($fp) 	#Obtain return value
	addi $sp,  $sp, -4 	#Remove locals from Stack
	sw $t3, 0($sp) 	#Save return value in Stack
	move $fp, $t7 	#restore FP
	jr $ra 	#RETURN
Bool_init:
	move $t0, $fp 	#save previous FP value
	move $fp, $sp 	#FP <- SP
	addi $sp,  $sp, 4 	#push local vars
	li $v0, 9 	#Allocating instance of type Bool
	li $a0, 4 	#Save 4 bytes
	syscall 	#
	la $t9, Bool 	#Save type address in register
	sw $t9, 0($v0) 	#Save type address in firts position of memory allocated
	addi $v0,  $v0, 4 	#Move offset of instance (type addres is in index -1)
	sw $v0, 0($fp) 	#Save instance address in destination
	lw $t3, -4($fp) 	#Dir of instance of attribute to set
	lw $t7, 0($fp) 	#Obtain value from source dir
	sw $t3, 0($t7) 	#Save value in attribute of index 0
	lw $t2, 0($fp) 	#Obtain return value
	addi $sp,  $sp, -4 	#Remove locals from Stack
	sw $t2, 0($sp) 	#Save return value in Stack
	move $fp, $t0 	#restore FP
	jr $ra 	#RETURN
String_init:
	move $t5, $fp 	#save previous FP value
	move $fp, $sp 	#FP <- SP
	addi $sp,  $sp, 4 	#push local vars
	li $v0, 9 	#Allocating instance of type String
	li $a0, 4 	#Save 4 bytes
	syscall 	#
	la $t9, String 	#Save type address in register
	sw $t9, 0($v0) 	#Save type address in firts position of memory allocated
	addi $v0,  $v0, 4 	#Move offset of instance (type addres is in index -1)
	sw $v0, 0($fp) 	#Save instance address in destination
	lw $t8, -4($fp) 	#Dir of instance of attribute to set
	lw $t5, 0($fp) 	#Obtain value from source dir
	sw $t8, 0($t5) 	#Save value in attribute of index 0
	lw $t4, 0($fp) 	#Obtain return value
	addi $sp,  $sp, -4 	#Remove locals from Stack
	sw $t4, 0($sp) 	#Save return value in Stack
	move $fp, $t5 	#restore FP
	jr $ra 	#RETURN
Main_init:
	move $t3, $fp 	#save previous FP value
	move $fp, $sp 	#FP <- SP
	addi $sp,  $sp, 4 	#push local vars
	li $v0, 9 	#Allocating instance of type Main
	li $a0, 4 	#Save 4 bytes
	syscall 	#
	la $t5, Main 	#Save type address in register
	sw $t5, 0($v0) 	#Save type address in firts position of memory allocated
	addi $v0,  $v0, 4 	#Move offset of instance (type addres is in index -1)
	sw $v0, 0($fp) 	#Save instance address in destination
	lw $t6, 0($fp) 	#Obtain return value
	addi $sp,  $sp, -4 	#Remove locals from Stack
	sw $t6, 0($sp) 	#Save return value in Stack
	move $fp, $t3 	#restore FP
	jr $ra 	#RETURN
Main_main:
	move $t5, $fp 	#save previous FP value
	move $fp, $sp 	#FP <- SP
	addi $sp,  $sp, 16 	#push local vars
	la $t4, data_8_string 	#LOAD
	sw $t4, 4($fp) 	#Save loaded value in destination
	lw $t8, 4($fp) 	#Obtain alue of Arg
	sw $t8, 0($sp) 	#Save Arg in Stack
	addi $sp,  $sp, 4 	#Move Stack
	jal String_init 	#Jump to function and save link
	lw $t4, 0($sp) 	#
	sw $t4, 8($fp) 	#
	addi $sp,  $sp, -4 	#Remove args from stack
	lw $t1, -4($fp) 	#Typeof
	lw $t6, -4($t1) 	#
	sw $t6, 12($fp) 	#Save type value in destination
	lw $t9, -4($fp) 	#Obtain alue of Arg
	sw $t9, 0($sp) 	#Save Arg in Stack
	addi $sp,  $sp, 4 	#Move Stack
	lw $t5, 8($fp) 	#Obtain alue of Arg
	sw $t5, 0($sp) 	#Save Arg in Stack
	addi $sp,  $sp, 4 	#Move Stack
	lw $t6, 12($fp) 	#get type dir for Dynamic Call
    la $t6, IO
	lw $t0, 12($t6) 	#Get method of index 3
	jalr $t0 	#Jump to function
	lw $t6, 0($sp) 	#Obtain return value from stack
	sw $t6, 0($fp) 	#Save return value in destination
	addi $sp,  $sp, -8 	#Remove Args from Stack
	lw $t1, 0($fp) 	#Obtain return value
	addi $sp,  $sp, -16 	#Remove locals from Stack
	sw $t1, 0($sp) 	#Save return value in Stack
	move $fp, $t5 	#restore FP
	jr $ra 	#RETURN
