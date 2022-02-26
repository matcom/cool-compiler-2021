.data
	type_Object: .word 8
	type_Object_inherits_from: .word 0
	type_Object_attributes: .word 0
	type_Object_name_size: .word 6
	type_Object_name: .asciiz "Object"
	type_Object_abort_message: .asciiz "Abort called from class Object\n"
	
	type_IO: .word 8
	type_IO_inherits_from: .word type_Object
	type_IO_attributes: .word 0
	type_IO_name_size: .word 2
	type_IO_name: .asciiz "IO"
	type_IO_abort_message: .asciiz "Abort called from class IO\n"
	
	type_Int: .word 8
	type_Int_inherits_from: .word type_Object
	type_Int_attributes: .word 0
	type_Int_name_size: .word 3
	type_Int_name: .asciiz "Int"
	type_Int_abort_message: .asciiz "Abort called from class Int\n"
	
	type_String: .word 8
	type_String_inherits_from: .word type_Object
	type_String_attributes: .word 0
	type_String_name_size: .word 6
	type_String_name: .asciiz "String"
	type_String_abort_message: .asciiz "Abort called from class String\n"
	
	type_Bool: .word 8
	type_Bool_inherits_from: .word type_Object
	type_Bool_attributes: .word 0
	type_Bool_name_size: .word 4
	type_Bool_name: .asciiz "Bool"
	type_Bool_abort_message: .asciiz "Abort called from class Bool\n"
	
	type_A: .word 12
	type_A_inherits_from: .word type_Object
	type_A_attributes: .word 1
	type_A_name_size: .word 1
	type_A_name: .asciiz "A"
	type_A_abort_message: .asciiz "Abort called from class A\n"
	
	type_B: .word 12
	type_B_inherits_from: .word type_A
	type_B_attributes: .word 1
	type_B_name_size: .word 1
	type_B_name: .asciiz "B"
	type_B_abort_message: .asciiz "Abort called from class B\n"
	
	type_C: .word 12
	type_C_inherits_from: .word type_B
	type_C_attributes: .word 1
	type_C_name_size: .word 1
	type_C_name: .asciiz "C"
	type_C_abort_message: .asciiz "Abort called from class C\n"
	
	type_D: .word 12
	type_D_inherits_from: .word type_B
	type_D_attributes: .word 1
	type_D_name_size: .word 1
	type_D_name: .asciiz "D"
	type_D_abort_message: .asciiz "Abort called from class D\n"
	
	type_E: .word 12
	type_E_inherits_from: .word type_D
	type_E_attributes: .word 1
	type_E_name_size: .word 1
	type_E_name: .asciiz "E"
	type_E_abort_message: .asciiz "Abort called from class E\n"
	
	type_A2I: .word 8
	type_A2I_inherits_from: .word type_Object
	type_A2I_attributes: .word 0
	type_A2I_name_size: .word 3
	type_A2I_name: .asciiz "A2I"
	type_A2I_abort_message: .asciiz "Abort called from class A2I\n"
	
	type_Main: .word 24
	type_Main_inherits_from: .word type_IO
	type_Main_attributes: .word 4
	type_Main_name_size: .word 4
	type_Main_name: .asciiz "Main"
	type_Main_abort_message: .asciiz "Abort called from class Main\n"
	
	buffer_input: .space 1024
	debug_log: .asciiz "debug_log\n"

.text
	function_add:
		# Function parameters
		#   $ra = 12($sp)
		#   a = 8($sp)
		#   b = 4($sp)
		
		# Reserving space for local variables
		addi $sp, $sp, -4
		
		# Allocating Int 0
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Int # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 0
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 0($sp) # internal_0 = address of allocated object Int
		
		# Addition operation
		lw $t0, 8($sp) # Save in $t0 the left operand address
		lw $t0, 8($t0) # Save in $t0 the left operand value
		lw $t1, 4($sp) # Save in $t1 the right operand address
		lw $t1, 8($t1) # Save in $t1 the rigth operand value
		add $t2, $t0, $t1 # $t2 = $t0 + $t1
		
		lw $t0, 0($sp) # $t0 = internal_0
		sw $t2, 8($t0) # Setting value in the third word of the Int object
		
		# Loading return value in $v1
		lw $v1, 0($sp)
		
		# Freeing space for local variables
		addi $sp, $sp, 4
		
		jr $ra
		
	function_sub:
		# Function parameters
		#   $ra = 12($sp)
		#   a = 8($sp)
		#   b = 4($sp)
		
		# Reserving space for local variables
		addi $sp, $sp, -4
		
		# Allocating Int 0
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Int # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 0
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 0($sp) # internal_0 = address of allocated object Int
		
		# Subtraction operation
		lw $t0, 8($sp) # Save in $t0 the left operand address
		lw $t0, 8($t0) # Save in $t0 the left operand value
		lw $t1, 4($sp) # Save in $t1 the right operand address
		lw $t1, 8($t1) # Save in $t1 the rigth operand value
		sub $t2, $t0, $t1 # $t2 = $t0 - $t1
		
		lw $t0, 0($sp) # $t0 = internal_0
		sw $t2, 8($t0) # Setting value in the third word of the Int object
		
		# Loading return value in $v1
		lw $v1, 0($sp)
		
		# Freeing space for local variables
		addi $sp, $sp, 4
		
		jr $ra
		
	function_mult:
		# Function parameters
		#   $ra = 12($sp)
		#   a = 8($sp)
		#   b = 4($sp)
		
		# Reserving space for local variables
		addi $sp, $sp, -4
		
		# Allocating Int 0
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Int # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 0
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 0($sp) # internal_0 = address of allocated object Int
		
		# Multiplication operation
		lw $t0, 8($sp) # Save in $t0 the left operand address
		lw $t0, 8($t0) # Save in $t0 the left operand value
		lw $t1, 4($sp) # Save in $t1 the right operand address
		lw $t1, 8($t1) # Save in $t1 the rigth operand value
		mult $t0, $t1 # $t2 = $t0 * $t1
		mflo $t2
		
		lw $t0, 0($sp) # $t0 = internal_0
		sw $t2, 8($t0) # Setting value in the third word of the Int object
		
		# Loading return value in $v1
		lw $v1, 0($sp)
		
		# Freeing space for local variables
		addi $sp, $sp, 4
		
		jr $ra
		
	function_div:
		# Function parameters
		#   $ra = 12($sp)
		#   a = 8($sp)
		#   b = 4($sp)
		
		# Reserving space for local variables
		addi $sp, $sp, -4
		
		# Allocating Int 0
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Int # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 0
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 0($sp) # internal_0 = address of allocated object Int
		
		# Division operation
		lw $t0, 8($sp) # Save in $t0 the left operand address
		lw $t0, 8($t0) # Save in $t0 the left operand value
		lw $t1, 4($sp) # Save in $t1 the right operand address
		lw $t1, 8($t1) # Save in $t1 the rigth operand value
		div $t0, $t1 # $t2 = $t0 / $t1
		mflo $t2
		
		lw $t0, 0($sp) # $t0 = internal_0
		sw $t2, 8($t0) # Setting value in the third word of the Int object
		
		# Loading return value in $v1
		lw $v1, 0($sp)
		
		# Freeing space for local variables
		addi $sp, $sp, 4
		
		jr $ra
		
	function_xor:
		# Function parameters
		#   $ra = 12($sp)
		#   a = 8($sp)
		#   b = 4($sp)
		
		# Reserving space for local variables
		addi $sp, $sp, -4
		
		# Allocating Int 0
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Int # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 0
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 0($sp) # internal_0 = address of allocated object Int
		
		# Xor operation
		lw $t0, 8($sp) # Save in $t0 the left operand address
		lw $t0, 8($t0) # Save in $t0 the left operand value
		lw $t1, 4($sp) # Save in $t1 the right operand address
		lw $t1, 8($t1) # Save in $t1 the rigth operand value
		xor $t2, $t0, $t1 # $t0 = $t0 ^ $t1
		
		lw $t0, 0($sp) # $t0 = internal_0
		sw $t2, 8($t0) # Setting value in the third word of the Int object
		
		# Loading return value in $v1
		lw $v1, 0($sp)
		
		# Freeing space for local variables
		addi $sp, $sp, 4
		
		jr $ra
		
	function_less_than:
		# Function parameters
		#   $ra = 12($sp)
		#   a = 8($sp)
		#   b = 4($sp)
		
		# Reserving space for local variables
		addi $sp, $sp, -4
		
		# Allocating Bool 0
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Bool # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 0
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 0($sp) # internal_0 = address of allocated object Int
		
		# Less than operation
		lw $t0, 8($sp) # Save in $t0 the left operand address
		lw $t0, 8($t0) # Save in $t0 the left operand value
		lw $t1, 4($sp) # Save in $t1 the right operand address
		lw $t1, 8($t1) # Save in $t1 the rigth operand value
		slt $t2, $t0, $t1 # $t2 = $t0 < $t1
		
		lw $t0, 0($sp) # $t0 = internal_0
		sw $t2, 8($t0) # Setting value in the third word of the Bool object
		
		# Loading return value in $v1
		lw $v1, 0($sp)
		
		# Freeing space for local variables
		addi $sp, $sp, 4
		
		jr $ra
		
	function_less_than_or_equal:
		# Function parameters
		#   $ra = 12($sp)
		#   a = 8($sp)
		#   b = 4($sp)
		
		# Reserving space for local variables
		addi $sp, $sp, -4
		
		# Allocating Bool 0
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Bool # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 0
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 0($sp) # internal_0 = address of allocated object Int
		
		# Less than operation
		lw $t0, 8($sp) # Save in $t0 the left operand address
		lw $t0, 8($t0) # Save in $t0 the left operand value
		lw $t1, 4($sp) # Save in $t1 the right operand address
		lw $t1, 8($t1) # Save in $t1 the rigth operand value
		sle $t2, $t0, $t1 # $t2 = $t0 <= $t1
		
		lw $t0, 0($sp) # $t0 = internal_0
		sw $t2, 8($t0) # Setting value in the third word of the Bool object
		
		# Loading return value in $v1
		lw $v1, 0($sp)
		
		# Freeing space for local variables
		addi $sp, $sp, 4
		
		jr $ra
		
	function_equal:
		# Function parameters
		#   $ra = 48($sp)
		#   a = 44($sp)
		#   b = 40($sp)
		
		# Reserving space for local variables
		addi $sp, $sp, -40
		
		# Allocating Bool 0
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Bool # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 0
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 36($sp) # internal_0 = address of allocated object Int
		
		# Allocating NUll to internal_1
		sw $zero, 32($sp) # internal_1 = 0
		
		# Allocating Bool 0
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Bool # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 0
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 28($sp) # internal_2 = address of allocated object Int
		
		# internal_2 = EqualAddress(a, internal_1)
		lw $t0, 44($sp)
		lw $t1, 32($sp)
		seq $t2, $t0, $t1
		lw $t0, 28($sp)
		sw $t2, 8($t0)
		
		# internal_2 = EqualAddress(b, internal_1)
		lw $t0, 40($sp)
		lw $t1, 32($sp)
		seq $t2, $t0, $t1
		lw $t0, 28($sp)
		sw $t2, 8($t0)
		
		# If internal_2 then goto a_is_type_object
		lw $t0, 28($sp) # Loading the address of the condition
		lw $t0, 8($t0) # Loading the value of the condition
		addi $t1, $zero, 1 # Setting the value to 1 for comparison
		beq $t0, $t1, a_is_type_object
		
		# internal_3 = typeof a that is the first word of the object
		lw $t0, 44($sp)
		lw $t0, 0($t0)
		sw $t0, 24($sp)
		
		# internal_4 = direction of Int
		la $t0, type_Int
		sw $t0, 20($sp)
		
		# internal_5 = direction of Bool
		la $t0, type_Bool
		sw $t0, 16($sp)
		
		# internal_6 = direction of String
		la $t0, type_String
		sw $t0, 12($sp)
		
		# Allocating Bool 0
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Bool # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 0
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 8($sp) # internal_7 = address of allocated object Int
		
		# Allocating Bool 0
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Bool # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 0
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 4($sp) # internal_8 = address of allocated object Int
		
		# Allocating Bool 0
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Bool # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 0
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 0($sp) # internal_9 = address of allocated object Int
		
		# internal_7 = EqualAddress(internal_3, internal_4)
		lw $t0, 24($sp)
		lw $t1, 20($sp)
		seq $t2, $t0, $t1
		lw $t0, 8($sp)
		sw $t2, 8($t0)
		
		# internal_8 = EqualAddress(internal_3, internal_5)
		lw $t0, 24($sp)
		lw $t1, 16($sp)
		seq $t2, $t0, $t1
		lw $t0, 4($sp)
		sw $t2, 8($t0)
		
		# internal_9 = EqualAddress(internal_3, internal_6)
		lw $t0, 24($sp)
		lw $t1, 12($sp)
		seq $t2, $t0, $t1
		lw $t0, 0($sp)
		sw $t2, 8($t0)
		
		# If internal_7 then goto a_is_type_int_or_bool
		lw $t0, 8($sp) # Loading the address of the condition
		lw $t0, 8($t0) # Loading the value of the condition
		addi $t1, $zero, 1 # Setting the value to 1 for comparison
		beq $t0, $t1, a_is_type_int_or_bool
		
		# If internal_8 then goto a_is_type_int_or_bool
		lw $t0, 4($sp) # Loading the address of the condition
		lw $t0, 8($t0) # Loading the value of the condition
		addi $t1, $zero, 1 # Setting the value to 1 for comparison
		beq $t0, $t1, a_is_type_int_or_bool
		
		# If internal_9 then goto a_is_type_string
		lw $t0, 0($sp) # Loading the address of the condition
		lw $t0, 8($t0) # Loading the value of the condition
		addi $t1, $zero, 1 # Setting the value to 1 for comparison
		beq $t0, $t1, a_is_type_string
		
		# Jumping to a_is_type_object
		j a_is_type_object
		
		a_is_type_int_or_bool:
		
		# internal_0 = EqualInt(a, b)
		lw $t0, 44($sp)
		lw $t0, 8($t0)
		lw $t1, 40($sp)
		lw $t1, 8($t1)
		seq $t2, $t0, $t1
		lw $t0, 36($sp)
		sw $t2, 8($t0)
		
		# Jumping to end_of_equal
		j end_of_equal
		
		a_is_type_string:
		
		# internal_0 = EqualStr(a, b)
		lw $t0, 44($sp)
		lw $t1, 40($sp)
		addi $t0, $t0, 8
		addi $t1, $t1, 8
		
		# By default we assume the strings are equals
		addi $t4, $zero, 1
		lw $t5, 36($sp)
		sw $t4, 8($t5)
		
		while_compare_strings_start:
		lb $t2, 0($t0)
		lb $t3, 0($t1)
		beq $t2, $t3, while_compare_strings_update
		
		# The strings are no equals
		lw $t5, 36($sp)
		sw $zero, 8($t5)
		j while_compare_strings_end
		
		while_compare_strings_update:
		addi $t0, $t0, 1
		addi $t1, $t1, 1
		beq $t2, $zero, while_compare_strings_end
		beq $t3, $zero, while_compare_strings_end
		j while_compare_strings_start
		while_compare_strings_end:
		
		# Jumping to end_of_equal
		j end_of_equal
		
		a_is_type_object:
		
		# Equal operation
		lw $t0, 44($sp) # Save in $t0 the left operand address
		lw $t1, 40($sp) # Save in $t1 the right operand address
		seq $t2, $t0, $t1 # $t2 = $t0 == $t1
		
		lw $t0, 36($sp) # $t0 = internal_0
		sw $t2, 8($t0) # Setting value in the third word of the Bool object
		
		# Jumping to end_of_equal
		j end_of_equal
		
		end_of_equal:
		
		# Loading return value in $v1
		lw $v1, 36($sp)
		
		# Freeing space for local variables
		addi $sp, $sp, 40
		
		jr $ra
		
	function_assign:
		# Function parameters
		#   $ra = 36($sp)
		#   dest = 32($sp)
		#   source = 28($sp)
		
		# Reserving space for local variables
		addi $sp, $sp, -28
		
		# Allocating NUll to internal_0
		sw $zero, 24($sp) # internal_0 = 0
		
		# Allocating Bool 0
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Bool # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 0
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 20($sp) # internal_1 = address of allocated object Int
		
		# internal_1 = EqualAddress(source, internal_0)
		lw $t0, 28($sp)
		lw $t1, 24($sp)
		seq $t2, $t0, $t1
		lw $t0, 20($sp)
		sw $t2, 8($t0)
		
		# internal_1 = EqualAddress(dest, internal_0)
		lw $t0, 32($sp)
		lw $t1, 24($sp)
		seq $t2, $t0, $t1
		lw $t0, 20($sp)
		sw $t2, 8($t0)
		
		# If internal_1 then goto source_is_type_object
		lw $t0, 20($sp) # Loading the address of the condition
		lw $t0, 8($t0) # Loading the value of the condition
		addi $t1, $zero, 1 # Setting the value to 1 for comparison
		beq $t0, $t1, source_is_type_object
		
		# internal_2 = typeof source that is the first word of the object
		lw $t0, 28($sp)
		lw $t0, 0($t0)
		sw $t0, 16($sp)
		
		# internal_3 = direction of Int
		la $t0, type_Int
		sw $t0, 12($sp)
		
		# internal_4 = direction of Bool
		la $t0, type_Bool
		sw $t0, 8($sp)
		
		# Allocating Bool 0
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Bool # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 0
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 4($sp) # internal_5 = address of allocated object Int
		
		# Allocating Bool 0
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Bool # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 0
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 0($sp) # internal_6 = address of allocated object Int
		
		# internal_5 = EqualAddress(internal_2, internal_3)
		lw $t0, 16($sp)
		lw $t1, 12($sp)
		seq $t2, $t0, $t1
		lw $t0, 4($sp)
		sw $t2, 8($t0)
		
		# internal_6 = EqualAddress(internal_2, internal_4)
		lw $t0, 16($sp)
		lw $t1, 8($sp)
		seq $t2, $t0, $t1
		lw $t0, 0($sp)
		sw $t2, 8($t0)
		
		# If internal_5 then goto source_is_type_int_or_bool
		lw $t0, 4($sp) # Loading the address of the condition
		lw $t0, 8($t0) # Loading the value of the condition
		addi $t1, $zero, 1 # Setting the value to 1 for comparison
		beq $t0, $t1, source_is_type_int_or_bool
		
		# If internal_6 then goto source_is_type_int_or_bool
		lw $t0, 0($sp) # Loading the address of the condition
		lw $t0, 8($t0) # Loading the value of the condition
		addi $t1, $zero, 1 # Setting the value to 1 for comparison
		beq $t0, $t1, source_is_type_int_or_bool
		
		# Jumping to source_is_type_object
		j source_is_type_object
		
		source_is_type_int_or_bool:
		
		# dest = source where source is an integer
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		lw $t0, 28($sp) # Pointer to source
		lw $t1, 0($t0) # $t1 = type of source
		lw $t2, 8($t0) # $t2 = value of source
		sw $t1, 0($v0) # Save type of dest
		sw $a0, 4($v0) # Save size of dest
		sw $t2, 8($v0) # Save value of dest
		sw $v0, 32($sp)
		
		# Jumping to source_end_of_equal
		j source_end_of_equal
		
		source_is_type_object:
		
		# dest = source
		lw $t0, 28($sp)
		sw $t0, 32($sp)
		
		# Jumping to source_end_of_equal
		j source_end_of_equal
		
		source_end_of_equal:
		
		# Loading return value in $v1
		lw $v1, 32($sp)
		
		# Freeing space for local variables
		addi $sp, $sp, 28
		
		jr $ra
		
	function___init___at_Object:
		# Function parameters
		#   $ra = 4($sp)
		#   self = 0($sp)
		
		# Loading return value in $v1
		lw $v1, 0($sp)
		
		jr $ra
		
	function_abort_at_Object:
		# Function parameters
		#   $ra = 20($sp)
		#   self = 16($sp)
		
		# Reserving space for local variables
		addi $sp, $sp, -16
		
		# Allocating String
		li $v0, 9
		addi $a0, $zero, 33 # $a0 = length of string + 9 for 4 bytes for the type, 4 bytes for the length of the string and 1 byte for null-terminator
		syscall
		
		la $t0, type_String
		sw $t0, 0($v0) # Setting type in the first word of the object
		
		addi $t0, $zero, 33
		sw $t0, 4($v0) # Setting length of the string in the second word of the object
		
		addi $t0, $zero, 65
		sb $t0, 8($v0) # internal_0[0] = 'A'
		
		addi $t0, $zero, 98
		sb $t0, 9($v0) # internal_0[1] = 'b'
		
		addi $t0, $zero, 111
		sb $t0, 10($v0) # internal_0[2] = 'o'
		
		addi $t0, $zero, 114
		sb $t0, 11($v0) # internal_0[3] = 'r'
		
		addi $t0, $zero, 116
		sb $t0, 12($v0) # internal_0[4] = 't'
		
		addi $t0, $zero, 32
		sb $t0, 13($v0) # internal_0[5] = ' '
		
		addi $t0, $zero, 99
		sb $t0, 14($v0) # internal_0[6] = 'c'
		
		addi $t0, $zero, 97
		sb $t0, 15($v0) # internal_0[7] = 'a'
		
		addi $t0, $zero, 108
		sb $t0, 16($v0) # internal_0[8] = 'l'
		
		addi $t0, $zero, 108
		sb $t0, 17($v0) # internal_0[9] = 'l'
		
		addi $t0, $zero, 101
		sb $t0, 18($v0) # internal_0[10] = 'e'
		
		addi $t0, $zero, 100
		sb $t0, 19($v0) # internal_0[11] = 'd'
		
		addi $t0, $zero, 32
		sb $t0, 20($v0) # internal_0[12] = ' '
		
		addi $t0, $zero, 102
		sb $t0, 21($v0) # internal_0[13] = 'f'
		
		addi $t0, $zero, 114
		sb $t0, 22($v0) # internal_0[14] = 'r'
		
		addi $t0, $zero, 111
		sb $t0, 23($v0) # internal_0[15] = 'o'
		
		addi $t0, $zero, 109
		sb $t0, 24($v0) # internal_0[16] = 'm'
		
		addi $t0, $zero, 32
		sb $t0, 25($v0) # internal_0[17] = ' '
		
		addi $t0, $zero, 99
		sb $t0, 26($v0) # internal_0[18] = 'c'
		
		addi $t0, $zero, 108
		sb $t0, 27($v0) # internal_0[19] = 'l'
		
		addi $t0, $zero, 97
		sb $t0, 28($v0) # internal_0[20] = 'a'
		
		addi $t0, $zero, 115
		sb $t0, 29($v0) # internal_0[21] = 's'
		
		addi $t0, $zero, 115
		sb $t0, 30($v0) # internal_0[22] = 's'
		
		addi $t0, $zero, 32
		sb $t0, 31($v0) # internal_0[23] = ' '
		
		sb $zero, 32($v0) # Null-terminator at the end of the string
		
		sw $v0, 12($sp) # internal_0 = "Abort called from class "
		
		# Allocating String
		li $v0, 9
		addi $a0, $zero, 10 # $a0 = length of string + 9 for 4 bytes for the type, 4 bytes for the length of the string and 1 byte for null-terminator
		syscall
		
		la $t0, type_String
		sw $t0, 0($v0) # Setting type in the first word of the object
		
		addi $t0, $zero, 10
		sw $t0, 4($v0) # Setting length of the string in the second word of the object
		
		addi $t0, $zero, 10
		sb $t0, 8($v0) # internal_2[0] = '\n'
		
		sb $zero, 9($v0) # Null-terminator at the end of the string
		
		sw $v0, 4($sp) # internal_2 = "\n"
		
		# Passing function arguments
		addi $sp, $sp, -8 # Reserving space for arguments
		sw $ra, 4($sp) # Storing return address
		
		# Argument self
		lw $t0, 24($sp)
		sw $t0, 0($sp) # Storing self
		
		# Calling function function_type_name_at_Object
		jal function_type_name_at_Object
		lw $ra, 4($sp)
		sw $v1, 16($sp) # internal_1 = result of function_type_name_at_Object
		addi $sp, $sp, 8 # Freeing space for arguments
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument internal_0
		lw $t0, 24($sp)
		sw $t0, 4($sp) # Storing internal_0
		
		# Argument internal_1
		lw $t0, 20($sp)
		sw $t0, 0($sp) # Storing internal_1
		
		# Calling function function_concat_at_String
		jal function_concat_at_String
		lw $ra, 8($sp)
		sw $v1, 12($sp) # internal_3 = result of function_concat_at_String
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument internal_3
		lw $t0, 12($sp)
		sw $t0, 4($sp) # Storing internal_3
		
		# Argument internal_2
		lw $t0, 16($sp)
		sw $t0, 0($sp) # Storing internal_2
		
		# Calling function function_concat_at_String
		jal function_concat_at_String
		lw $ra, 8($sp)
		sw $v1, 12($sp) # internal_3 = result of function_concat_at_String
		addi $sp, $sp, 12 # Freeing space for arguments
		
		lw $t0, 0($sp) # $t0 = internal_3
		addi $t0, $t0, 8 # Pointer to the first character of the string
		
		# Printing the string internal_3
		li $v0, 4
		move $a0, $t0
		syscall
		
		# Exit program
		li $v0, 10
		syscall
		
		# Loading return value in $v1
		lw $v1, 16($sp)
		
		# Freeing space for local variables
		addi $sp, $sp, 16
		
		jr $ra
		
	function_type_name_at_Object:
		# Function parameters
		#   $ra = 8($sp)
		#   self = 4($sp)
		
		# Reserving space for local variables
		addi $sp, $sp, -4
		
		# internal_0 = name of self
		lw $t0, 4($sp) # $t0 = self
		lw $t1, 0($t0) # $t1 = type of self
		lw $t2, 12($t1) # $t1 = length of the name of self
		la $t3, 16($t1) # $t1 = name of self
		
		addi $t2, $t2, 9 # Setting space for the type, the size and the null byte
		li $v0, 9
		move $a0, $t2
		syscall
		addi $t2, $t2, -9 # Restoring space for the type, the size and the null byte
		
		la $t4, type_String
		sw $t4, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting length in the second word of the object
		
		addi $t4, $v0, 0 # $t4 = direction of the new string
		addi $t4, $t4, 8 # Pointer to the first character of the string
		xor $t5, $t5, $t5 # Initializing counter
		while_copy_name_start:
		beq $t5, $t2, while_copy_name_end
		lb $t6, 0($t3) # Loading the character
		sb $t6, 0($t4)
		addi $t4, $t4, 1 # Incrementing the pointer to the new string
		addi $t3, $t3, 1 # Incrementing the pointer to the string in self
		addi $t5, $t5, 1 # Incrementing counter
		j while_copy_name_start
		while_copy_name_end:
		
		sb $zero, 0($t4) # Setting the null byte
		
		sw $v0, 0($sp) # Storing the new string in internal_0
		
		# Loading return value in $v1
		lw $v1, 0($sp)
		
		# Freeing space for local variables
		addi $sp, $sp, 4
		
		jr $ra
		
	function_copy_at_Object:
		# Function parameters
		#   $ra = 8($sp)
		#   self = 4($sp)
		
		# Reserving space for local variables
		addi $sp, $sp, -4
		
		# internal_0 = copy of self
		lw $t0, 4($sp) # $t0 = self
		lw $t1, 0($t0) # $t1 = type of self
		lw $t2, 4($t0) # $t2 = length of self in bytes
		
		# Allocating space for the new object
		li $v0, 9
		move $a0, $t2
		syscall
		move $t3, $v0 # $t3 = direction of the new object
		sw $t1, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting length in the second word of the object
		
		# Initializing the variable of the loop
		addi $t0, $t0, 8 # Pointer to the first character of the object
		addi $t3, $t3, 8 # Pointer to the first character of the object
		addi $t2, $2, -8 # Decrementing in 8 the length of the object
		xor $t4, $t4, $t4 # Initializing counter
		
		# Loop copying the object
		while_copy_start:
		beq $t4, $t2, while_copy_end
		lb $t5, 0($t0) # Loading the byte
		sb $t5, 0($t3) # Storing the byte
		addi $t0, $t0, 1 # Incrementing the pointer to the object
		addi $t3, $t3, 1 # Incrementing the pointer to the new object
		addi $t4, $t4, 1 # Incrementing counter
		j while_copy_start
		while_copy_end:
		sw $v0, 0($sp) # Storing the new object in internal_0
		
		# Loading return value in $v1
		lw $v1, 0($sp)
		
		# Freeing space for local variables
		addi $sp, $sp, 4
		
		jr $ra
		
	function___init___at_IO:
		# Function parameters
		#   $ra = 4($sp)
		#   self = 0($sp)
		
		# Loading return value in $v1
		lw $v1, 0($sp)
		
		jr $ra
		
	function_out_string_at_IO:
		# Function parameters
		#   $ra = 8($sp)
		#   self = 4($sp)
		#   x = 0($sp)
		
		lw $t0, 0($sp) # $t0 = x
		addi $t0, $t0, 8 # Pointer to the first character of the string
		
		# Printing the string x
		li $v0, 4
		move $a0, $t0
		syscall
		
		# Loading return value in $v1
		lw $v1, 4($sp)
		
		jr $ra
		
	function_out_int_at_IO:
		# Function parameters
		#   $ra = 8($sp)
		#   self = 4($sp)
		#   x = 0($sp)
		
		# Printing the string x
		li $v0, 1
		lw $a0, 0($sp)
		lw $a0, 8($a0)
		syscall
		
		# Loading return value in $v1
		lw $v1, 4($sp)
		
		jr $ra
		
	function_in_string_at_IO:
		# Function parameters
		#   $ra = 8($sp)
		#   self = 4($sp)
		
		# Reserving space for local variables
		addi $sp, $sp, -4
		
		li $v0, 8
		la $a0, buffer_input
		li $a1, 1024
		syscall
		
		xor $t0, $t0, $t0 # Initializing counter
		while_read_start:
		lb $t1, buffer_input($t0) # Loading the byte
		beq $t1, $zero, while_read_end
		addi $t0, $t0, 1 # Incrementing counter
		j while_read_start
		while_read_end:
		addi $t0, $t0, -1 # Decrementing counter to eliminate the '\n'
		
		addi $t0, $t0, 9 # Adding space for the type, the size and the null byte
		li $v0, 9
		move $a0, $t0
		syscall
		addi $t0, $t0, -9 # Adding space for the type, the size and the null byte
		la $t2, type_String
		sw $t2, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting length in the second word of the object
		
		addi $t3, $v0, 8 # Pointer to the first character of the string
		xor $t4, $t4, $t4 # Initializing counter
		
		while_copy_from_buffer_start:
		beq $t4, $t0, while_copy_from_buffer_end
		lb $t5, buffer_input($t4) # Loading the byte
		sb $t5, 0($t3) # Storing the byte
		addi $t3, $t3, 1 # Imcremeenting pointer
		addi $t4, $t4, 1 # Incrementing counter
		j while_copy_from_buffer_start
		while_copy_from_buffer_end:
		
		sb $zero, 0($t3) # Storing the null byte
		
		sw $v0, 0($sp) # Storing the new object in internal_0
		
		# Loading return value in $v1
		lw $v1, 0($sp)
		
		# Freeing space for local variables
		addi $sp, $sp, 4
		
		jr $ra
		
	function_in_int_at_IO:
		# Function parameters
		#   $ra = 8($sp)
		#   self = 4($sp)
		
		# Reserving space for local variables
		addi $sp, $sp, -4
		
		# Allocating Int 0
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Int # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 0
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 0($sp) # internal_0 = address of allocated object Int
		
		li $v0, 5
		syscall
		lw $t0, 0($sp)
		sw $v0, 8($t0)
		
		# Loading return value in $v1
		lw $v1, 0($sp)
		
		# Freeing space for local variables
		addi $sp, $sp, 4
		
		jr $ra
		
	function___init___at_String:
		# Function parameters
		#   $ra = 4($sp)
		#   self = 0($sp)
		
		# Loading return value in $v1
		lw $v1, 0($sp)
		
		jr $ra
		
	function_length_at_String:
		# Function parameters
		#   $ra = 8($sp)
		#   self = 4($sp)
		
		# Reserving space for local variables
		addi $sp, $sp, -4
		
		# Allocating Int 0
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Int # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 0
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 0($sp) # internal_0 = address of allocated object Int
		
		# internal_0 = length of self
		lw $t0, 4($sp)
		lw $t1, 4($t0)
		addi $t1, $t1, -9 # Subtracting 9 for the type, length, and null-terminator
		lw $t0, 0($sp)
		sw $t1, 8($t0)
		
		# Loading return value in $v1
		lw $v1, 0($sp)
		
		# Freeing space for local variables
		addi $sp, $sp, 4
		
		jr $ra
		
	function_concat_at_String:
		# Function parameters
		#   $ra = 12($sp)
		#   self = 8($sp)
		#   s = 4($sp)
		
		# Reserving space for local variables
		addi $sp, $sp, -4
		
		# internal_0 = self + s
		lw $t0, 8($sp)
		lw $t1, 4($sp)
		lw $t2, 4($t0) # $t2 = length of str1
		lw $t3, 4($t1) # $t3 = length of str2
		addi $t2, $t2, -9
		addi $t3, $t3, -9
		add $t4, $t2, $t3 # $t4 = length of str1 + str2
		addi $t4, $t4, 9 # Adding the space for the type (4bytes), the length(4bytes) and the null-terminator(1byte)
		
		li $v0, 9
		move $a0, $t4
		syscall
		addi $t4, $t4, -9 # Restoring $t4 = length of str1 + str2
		add $t5, $zero, $v0 # $t5 = address of the new string object
		addi $t5, $t5, 8 # $t5 = address of the first byte of the new string
		
		la $t8, type_String
		sw $t8, 0($v0) # Setting type in the first word of th object
		
		sw $a0, 4($v0) # Setting length of the string in the second word of the object
		
		# Copying str1 to the new string
		xor $t6, $t6, $t6 # $t6 = 0 Initializing counter
		while_copy_str1_start:
		beq $t6, $t2, while_copy_str1_end
		lb $t7, 8($t0)
		sb $t7, 0($t5)
		add $t0, $t0, 1 # $t0 = $t0 + 1 Incrementing the address of str1
		add $t5, $t5, 1 # $t5 = $t5 + 1 Incrementing the address of the new string
		addi $t6, $t6, 1 # $t6 = $t6 + 1 Incrementing counter
		j while_copy_str1_start
		while_copy_str1_end:
		
		# Copying str2 to the new string
		while_copy_str2_start:
		beq $t6, $t4, while_copy_str2_end
		lb $t7, 8($t1)
		sb $t7, 0($t5)
		add $t1, $t1, 1 # $t0 = $t0 + 1 Incrementing the address of str1
		add $t5, $t5, 1 # $t5 = $t5 + 1 Incrementing the address of the new string
		addi $t6, $t6, 1 # $t6 = $t6 + 1 Incrementing counter
		j while_copy_str2_start
		while_copy_str2_end:
		
		sb $zero, 0($t5) # Setting the null-terminator
		
		sw $v0, 0($sp) # internal_0 = self + s
		
		# Loading return value in $v1
		lw $v1, 0($sp)
		
		# Freeing space for local variables
		addi $sp, $sp, 4
		
		jr $ra
		
	function_substr_at_String:
		# Function parameters
		#   $ra = 16($sp)
		#   self = 12($sp)
		#   i = 8($sp)
		#   l = 4($sp)
		
		# Reserving space for local variables
		addi $sp, $sp, -4
		
		# internal_0 = self[i:i + l]
		lw $t0, 12($sp) # $t0 = address of the string
		lw $t1, 4($t0) # $t1 = length of the string
		addi $t1, $t1, -9 # $t1 = length of the string + 9
		lw $t2, 8($sp) # $t2 = start of the substring
		lw $t2, 8($t2)
		lw $t3, 4($sp) # $t3 = length of the substring
		lw $t3, 8($t3)
		add $t4, $t2, $t3 # $t4 = start of the substring + length of the substring
		
		bgt $t4, $t1, substring_out_of_bounds
		
		addi $t3, $t3, 9
		li $v0, 9
		move $a0, $t3
		syscall
		addi $t3, $t3, -9
		
		la $t5, type_String
		sw $t5, 0($v0) # Setting type in the first word of the object
		
		sw $a0, 4($v0) # Setting length in the second word of the object
		
		addi $t0, $t0, 8 # pointing to the first byte of the string
		add $t0, $t0, $t2 # pointing to the first byte of the substring
		move $t5, $v0 # $t5 = address of the new string
		add $t5, $t5, 8 # pointing to the first byte of the string
		xor $t6, $t6, $t6 # $t6 = 0 Initializing counter
		while_copy_substr_start:
		beq $t6, $t3, while_copy_substr_end
		lb $t7, 0($t0)
		sb $t7, 0($t5)
		addi $t0, $t0, 1 # $t0 = $t0 + 1 Incrementing the address of the string
		add $t5, $t5, 1 # $t5 = $t5 + 1 Incrementing the address of the new string
		addi $t6, $t6, 1 # $t6 = $t6 + 1 Incrementing counter
		j while_copy_substr_start
		while_copy_substr_end:
		
		sb $zero, 0($t5) # Setting the null-terminator
		
		sw $v0, 0($sp) # internal_0 = self[i:i + l]
		j substring_not_out_of_bounds
		
		substring_out_of_bounds:
		li $v0, 17
		addi $a0, $zero, 1
		syscall
		
		substring_not_out_of_bounds:
		
		# Loading return value in $v1
		lw $v1, 0($sp)
		
		# Freeing space for local variables
		addi $sp, $sp, 4
		
		jr $ra
		
	function___init___at_A:
		# Function parameters
		#   $ra = 8($sp)
		#   self = 4($sp)
		
		# Reserving space for local variables
		addi $sp, $sp, -4
		
		# Allocating Int 0
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Int # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 0
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 0($sp) # internal_0 = address of allocated object Int
		
		# Set attribute var of self
		lw $t0, 4($sp) # $t0 = self
		lw $t1, 0($sp) # $t1 = internal_0
		beq $t1, $zero, object_set_attribute_8781702292580
		lw $t2, 0($t1)
		la $t3, type_Int
		la $t4, type_Bool
		addi $t5, $zero, 1
		seq $t6, $t2, $t3
		beq $t6, $t5, int_set_attribute_8781702292580
		seq $t6, $t2, $t4
		beq $t6, $t5, bool_set_attribute_8781702292580
		j object_set_attribute_8781702292580
		int_set_attribute_8781702292580:
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		sw $t3, 0($v0)
		sw $a0, 4($v0)
		lw $t5, 8($t1)
		sw $t5, 8($v0)
		sw $v0, 8($t0) # self.var = internal_0
		j end_set_attribute_8781702292580
		bool_set_attribute_8781702292580:
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		sw $t4, 0($v0)
		sw $a0, 4($v0)
		lw $t5, 8($t1)
		sw $t5, 8($v0)
		sw $v0, 8($t0) # self.var = internal_0
		j end_set_attribute_8781702292580
		object_set_attribute_8781702292580:
		sw $t1, 8($t0) # self.var = internal_0
		end_set_attribute_8781702292580:
		
		# Loading return value in $v1
		lw $v1, 4($sp)
		
		# Freeing space for local variables
		addi $sp, $sp, 4
		
		jr $ra
		
	function_value_at_A:
		# Function parameters
		#   $ra = 8($sp)
		#   self = 4($sp)
		
		# Reserving space for local variables
		addi $sp, $sp, -4
		
		# Get attribute var of self
		lw $t0, 4($sp) # Get the address of self
		lw $t1, 8($t0) # Get the attribute 'var' from the instance
		lw $t2, 0($t1)
		la $t3, type_Int
		la $t4, type_Bool
		addi $t5, $zero, 1
		seq $t6, $t2, $t3
		beq $t6, $t5, int_get_attribute_8781702292604
		seq $t6, $t2, $t4
		beq $t6, $t5, bool_get_attribute_8781702292604
		j object_get_attribute_8781702292604
		int_get_attribute_8781702292604:
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		sw $t3, 0($v0)
		sw $a0, 4($v0)
		lw $t5, 8($t1)
		sw $t5, 8($v0)
		sw $v0, 0($sp) # internal_0 = self.var
		j end_get_attribute_8781702292604
		bool_get_attribute_8781702292604:
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		sw $t4, 0($v0)
		sw $a0, 4($v0)
		lw $t5, 8($t1)
		sw $t5, 8($v0)
		sw $v0, 0($sp) # internal_0 = self.var
		j end_get_attribute_8781702292604
		object_get_attribute_8781702292604:
		sw $t1, 0($sp) # internal_0 = var
		end_get_attribute_8781702292604:
		
		# Loading return value in $v1
		lw $v1, 0($sp)
		
		# Freeing space for local variables
		addi $sp, $sp, 4
		
		jr $ra
		
	function_set_var_at_A:
		# Function parameters
		#   $ra = 8($sp)
		#   self = 4($sp)
		#   num = 0($sp)
		
		# Set attribute var of self
		lw $t0, 4($sp) # $t0 = self
		lw $t1, 0($sp) # $t1 = num
		beq $t1, $zero, object_set_attribute_8781702292655
		lw $t2, 0($t1)
		la $t3, type_Int
		la $t4, type_Bool
		addi $t5, $zero, 1
		seq $t6, $t2, $t3
		beq $t6, $t5, int_set_attribute_8781702292655
		seq $t6, $t2, $t4
		beq $t6, $t5, bool_set_attribute_8781702292655
		j object_set_attribute_8781702292655
		int_set_attribute_8781702292655:
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		sw $t3, 0($v0)
		sw $a0, 4($v0)
		lw $t5, 8($t1)
		sw $t5, 8($v0)
		sw $v0, 8($t0) # self.var = num
		j end_set_attribute_8781702292655
		bool_set_attribute_8781702292655:
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		sw $t4, 0($v0)
		sw $a0, 4($v0)
		lw $t5, 8($t1)
		sw $t5, 8($v0)
		sw $v0, 8($t0) # self.var = num
		j end_set_attribute_8781702292655
		object_set_attribute_8781702292655:
		sw $t1, 8($t0) # self.var = num
		end_set_attribute_8781702292655:
		
		# Loading return value in $v1
		lw $v1, 4($sp)
		
		jr $ra
		
	function_method1_at_A:
		# Function parameters
		#   $ra = 8($sp)
		#   self = 4($sp)
		#   num = 0($sp)
		
		# Loading return value in $v1
		lw $v1, 4($sp)
		
		jr $ra
		
	function_method2_at_A:
		# Function parameters
		#   $ra = 28($sp)
		#   self = 24($sp)
		#   num1 = 20($sp)
		#   num2 = 16($sp)
		
		# Reserving space for local variables
		addi $sp, $sp, -16
		
		# Allocating Int 0
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Int # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 0
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 12($sp) # x = address of allocated object Int
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument num1
		lw $t0, 32($sp)
		sw $t0, 4($sp) # Storing num1
		
		# Argument num2
		lw $t0, 28($sp)
		sw $t0, 0($sp) # Storing num2
		
		# Calling function function_add
		jal function_add
		lw $ra, 8($sp)
		sw $v1, 20($sp) # internal_1 = result of function_add
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument x
		lw $t0, 24($sp)
		sw $t0, 4($sp) # Storing x
		
		# Argument internal_1
		lw $t0, 20($sp)
		sw $t0, 0($sp) # Storing internal_1
		
		# Calling function function_assign
		jal function_assign
		lw $ra, 8($sp)
		sw $v1, 24($sp) # x = result of function_assign
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# Allocating B
		li $v0, 9
		lw $a0, type_B
		syscall
		la $t0, type_B # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of th object
		sw $a0, 4($v0) # Setting size in the second word of th object
		sw $v0, 4($sp) # internal_2 = address of allocated object B
		
		# Passing function arguments
		addi $sp, $sp, -8 # Reserving space for arguments
		sw $ra, 4($sp) # Storing return address
		
		# Argument internal_2
		lw $t0, 12($sp)
		sw $t0, 0($sp) # Storing internal_2
		
		# Calling function function___init___at_B
		jal function___init___at_B
		lw $ra, 4($sp)
		sw $v1, 12($sp) # internal_2 = result of function___init___at_B
		addi $sp, $sp, 8 # Freeing space for arguments
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument internal_2
		lw $t0, 16($sp)
		sw $t0, 4($sp) # Storing internal_2
		
		# Argument x
		lw $t0, 24($sp)
		sw $t0, 0($sp) # Storing x
		
		# Calling function function_set_var_at_A
		jal function_set_var_at_A
		lw $ra, 8($sp)
		sw $v1, 12($sp) # internal_3 = result of function_set_var_at_A
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# Loading return value in $v1
		lw $v1, 0($sp)
		
		# Freeing space for local variables
		addi $sp, $sp, 16
		
		jr $ra
		
	function_method3_at_A:
		# Function parameters
		#   $ra = 32($sp)
		#   self = 28($sp)
		#   num = 24($sp)
		
		# Reserving space for local variables
		addi $sp, $sp, -24
		
		# Allocating Int 0
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Int # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 0
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 20($sp) # x = address of allocated object Int
		
		# Allocating Int 1
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Int # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 1
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 16($sp) # internal_1 = address of allocated object Int
		
		# Allocating Int 4294967295
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Int # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 4294967295
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 12($sp) # internal_2 = address of allocated object Int
		
		# Allocating Int 0
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Int # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 0
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 8($sp) # internal_3 = address of allocated object Int
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument num
		lw $t0, 36($sp)
		sw $t0, 4($sp) # Storing num
		
		# Argument internal_2
		lw $t0, 24($sp)
		sw $t0, 0($sp) # Storing internal_2
		
		# Calling function function_xor
		jal function_xor
		lw $ra, 8($sp)
		sw $v1, 20($sp) # internal_3 = result of function_xor
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument internal_3
		lw $t0, 20($sp)
		sw $t0, 4($sp) # Storing internal_3
		
		# Argument internal_1
		lw $t0, 28($sp)
		sw $t0, 0($sp) # Storing internal_1
		
		# Calling function function_add
		jal function_add
		lw $ra, 8($sp)
		sw $v1, 20($sp) # internal_3 = result of function_add
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument x
		lw $t0, 32($sp)
		sw $t0, 4($sp) # Storing x
		
		# Argument internal_3
		lw $t0, 20($sp)
		sw $t0, 0($sp) # Storing internal_3
		
		# Calling function function_assign
		jal function_assign
		lw $ra, 8($sp)
		sw $v1, 32($sp) # x = result of function_assign
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# Allocating C
		li $v0, 9
		lw $a0, type_C
		syscall
		la $t0, type_C # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of th object
		sw $a0, 4($v0) # Setting size in the second word of th object
		sw $v0, 4($sp) # internal_4 = address of allocated object C
		
		# Passing function arguments
		addi $sp, $sp, -8 # Reserving space for arguments
		sw $ra, 4($sp) # Storing return address
		
		# Argument internal_4
		lw $t0, 12($sp)
		sw $t0, 0($sp) # Storing internal_4
		
		# Calling function function___init___at_C
		jal function___init___at_C
		lw $ra, 4($sp)
		sw $v1, 12($sp) # internal_4 = result of function___init___at_C
		addi $sp, $sp, 8 # Freeing space for arguments
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument internal_4
		lw $t0, 16($sp)
		sw $t0, 4($sp) # Storing internal_4
		
		# Argument x
		lw $t0, 32($sp)
		sw $t0, 0($sp) # Storing x
		
		# Calling function function_set_var_at_A
		jal function_set_var_at_A
		lw $ra, 8($sp)
		sw $v1, 12($sp) # internal_5 = result of function_set_var_at_A
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# Loading return value in $v1
		lw $v1, 0($sp)
		
		# Freeing space for local variables
		addi $sp, $sp, 24
		
		jr $ra
		
	function_method4_at_A:
		# Function parameters
		#   $ra = 56($sp)
		#   self = 52($sp)
		#   num1 = 48($sp)
		#   num2 = 44($sp)
		
		# Reserving space for local variables
		addi $sp, $sp, -44
		
		# Allocating Bool 0
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Bool # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 0
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 36($sp) # internal_1 = address of allocated object Int
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument num2
		lw $t0, 56($sp)
		sw $t0, 4($sp) # Storing num2
		
		# Argument num1
		lw $t0, 60($sp)
		sw $t0, 0($sp) # Storing num1
		
		# Calling function function_less_than
		jal function_less_than
		lw $ra, 8($sp)
		sw $v1, 44($sp) # internal_2 = result of function_less_than
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# internal_1 = internal_2
		lw $t0, 32($sp)
		sw $t0, 36($sp)
		
		# If internal_1 then goto then_8781702322008
		lw $t0, 36($sp) # Loading the address of the condition
		lw $t0, 8($t0) # Loading the value of the condition
		addi $t1, $zero, 1 # Setting the value to 1 for comparison
		beq $t0, $t1, then_8781702322008
		
		# Jumping to else_8781702322008
		j else_8781702322008
		
		then_8781702322008:
		
		# Allocating Int 0
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Int # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 0
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 28($sp) # x = address of allocated object Int
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument num1
		lw $t0, 60($sp)
		sw $t0, 4($sp) # Storing num1
		
		# Argument num2
		lw $t0, 56($sp)
		sw $t0, 0($sp) # Storing num2
		
		# Calling function function_sub
		jal function_sub
		lw $ra, 8($sp)
		sw $v1, 36($sp) # internal_4 = result of function_sub
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument x
		lw $t0, 40($sp)
		sw $t0, 4($sp) # Storing x
		
		# Argument internal_4
		lw $t0, 36($sp)
		sw $t0, 0($sp) # Storing internal_4
		
		# Calling function function_assign
		jal function_assign
		lw $ra, 8($sp)
		sw $v1, 40($sp) # x = result of function_assign
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# Allocating D
		li $v0, 9
		lw $a0, type_D
		syscall
		la $t0, type_D # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of th object
		sw $a0, 4($v0) # Setting size in the second word of th object
		sw $v0, 20($sp) # internal_5 = address of allocated object D
		
		# Passing function arguments
		addi $sp, $sp, -8 # Reserving space for arguments
		sw $ra, 4($sp) # Storing return address
		
		# Argument internal_5
		lw $t0, 28($sp)
		sw $t0, 0($sp) # Storing internal_5
		
		# Calling function function___init___at_D
		jal function___init___at_D
		lw $ra, 4($sp)
		sw $v1, 28($sp) # internal_5 = result of function___init___at_D
		addi $sp, $sp, 8 # Freeing space for arguments
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument internal_5
		lw $t0, 32($sp)
		sw $t0, 4($sp) # Storing internal_5
		
		# Argument x
		lw $t0, 40($sp)
		sw $t0, 0($sp) # Storing x
		
		# Calling function function_set_var_at_A
		jal function_set_var_at_A
		lw $ra, 8($sp)
		sw $v1, 28($sp) # internal_6 = result of function_set_var_at_A
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# internal_0 = internal_6
		lw $t0, 16($sp)
		sw $t0, 40($sp)
		
		# Jumping to endif_8781702322008
		j endif_8781702322008
		
		else_8781702322008:
		
		# Allocating Int 0
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Int # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 0
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 28($sp) # x = address of allocated object Int
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument num2
		lw $t0, 56($sp)
		sw $t0, 4($sp) # Storing num2
		
		# Argument num1
		lw $t0, 60($sp)
		sw $t0, 0($sp) # Storing num1
		
		# Calling function function_sub
		jal function_sub
		lw $ra, 8($sp)
		sw $v1, 20($sp) # internal_8 = result of function_sub
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument x
		lw $t0, 40($sp)
		sw $t0, 4($sp) # Storing x
		
		# Argument internal_8
		lw $t0, 20($sp)
		sw $t0, 0($sp) # Storing internal_8
		
		# Calling function function_assign
		jal function_assign
		lw $ra, 8($sp)
		sw $v1, 40($sp) # x = result of function_assign
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# Allocating D
		li $v0, 9
		lw $a0, type_D
		syscall
		la $t0, type_D # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of th object
		sw $a0, 4($v0) # Setting size in the second word of th object
		sw $v0, 4($sp) # internal_9 = address of allocated object D
		
		# Passing function arguments
		addi $sp, $sp, -8 # Reserving space for arguments
		sw $ra, 4($sp) # Storing return address
		
		# Argument internal_9
		lw $t0, 12($sp)
		sw $t0, 0($sp) # Storing internal_9
		
		# Calling function function___init___at_D
		jal function___init___at_D
		lw $ra, 4($sp)
		sw $v1, 12($sp) # internal_9 = result of function___init___at_D
		addi $sp, $sp, 8 # Freeing space for arguments
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument internal_9
		lw $t0, 16($sp)
		sw $t0, 4($sp) # Storing internal_9
		
		# Argument x
		lw $t0, 40($sp)
		sw $t0, 0($sp) # Storing x
		
		# Calling function function_set_var_at_A
		jal function_set_var_at_A
		lw $ra, 8($sp)
		sw $v1, 12($sp) # internal_10 = result of function_set_var_at_A
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# internal_0 = internal_10
		lw $t0, 0($sp)
		sw $t0, 40($sp)
		
		# Jumping to endif_8781702322008
		j endif_8781702322008
		
		endif_8781702322008:
		
		# Loading return value in $v1
		lw $v1, 40($sp)
		
		# Freeing space for local variables
		addi $sp, $sp, 44
		
		jr $ra
		
	function_method5_at_A:
		# Function parameters
		#   $ra = 48($sp)
		#   self = 44($sp)
		#   num = 40($sp)
		
		# Reserving space for local variables
		addi $sp, $sp, -40
		
		# Allocating Int 1
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Int # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 1
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 32($sp) # internal_1 = address of allocated object Int
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument x
		lw $t0, 48($sp)
		sw $t0, 4($sp) # Storing x
		
		# Argument internal_1
		lw $t0, 44($sp)
		sw $t0, 0($sp) # Storing internal_1
		
		# Calling function function_assign
		jal function_assign
		lw $ra, 8($sp)
		sw $v1, 48($sp) # x = result of function_assign
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# Allocating Int 1
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Int # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 1
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 24($sp) # internal_3 = address of allocated object Int
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument y
		lw $t0, 40($sp)
		sw $t0, 4($sp) # Storing y
		
		# Argument internal_3
		lw $t0, 36($sp)
		sw $t0, 0($sp) # Storing internal_3
		
		# Calling function function_assign
		jal function_assign
		lw $ra, 8($sp)
		sw $v1, 40($sp) # y = result of function_assign
		addi $sp, $sp, 12 # Freeing space for arguments
		
		while_start_8781702322092:
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument y
		lw $t0, 40($sp)
		sw $t0, 4($sp) # Storing y
		
		# Argument num
		lw $t0, 52($sp)
		sw $t0, 0($sp) # Storing num
		
		# Calling function function_less_than_or_equal
		jal function_less_than_or_equal
		lw $ra, 8($sp)
		sw $v1, 32($sp) # internal_4 = result of function_less_than_or_equal
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# If internal_4 then goto while_body_8781702322092
		lw $t0, 20($sp) # Loading the address of the condition
		lw $t0, 8($t0) # Loading the value of the condition
		addi $t1, $zero, 1 # Setting the value to 1 for comparison
		beq $t0, $t1, while_body_8781702322092
		
		# Jumping to while_end_8781702322092
		j while_end_8781702322092
		
		while_body_8781702322092:
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument x
		lw $t0, 48($sp)
		sw $t0, 4($sp) # Storing x
		
		# Argument y
		lw $t0, 40($sp)
		sw $t0, 0($sp) # Storing y
		
		# Calling function function_mult
		jal function_mult
		lw $ra, 8($sp)
		sw $v1, 28($sp) # internal_5 = result of function_mult
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument x
		lw $t0, 48($sp)
		sw $t0, 4($sp) # Storing x
		
		# Argument internal_5
		lw $t0, 28($sp)
		sw $t0, 0($sp) # Storing internal_5
		
		# Calling function function_assign
		jal function_assign
		lw $ra, 8($sp)
		sw $v1, 48($sp) # x = result of function_assign
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# Allocating Int 1
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Int # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 1
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 12($sp) # internal_6 = address of allocated object Int
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument y
		lw $t0, 40($sp)
		sw $t0, 4($sp) # Storing y
		
		# Argument internal_6
		lw $t0, 24($sp)
		sw $t0, 0($sp) # Storing internal_6
		
		# Calling function function_add
		jal function_add
		lw $ra, 8($sp)
		sw $v1, 20($sp) # internal_7 = result of function_add
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument y
		lw $t0, 40($sp)
		sw $t0, 4($sp) # Storing y
		
		# Argument internal_7
		lw $t0, 20($sp)
		sw $t0, 0($sp) # Storing internal_7
		
		# Calling function function_assign
		jal function_assign
		lw $ra, 8($sp)
		sw $v1, 40($sp) # y = result of function_assign
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# Jumping to while_start_8781702322092
		j while_start_8781702322092
		
		while_end_8781702322092:
		
		# Allocating E
		li $v0, 9
		lw $a0, type_E
		syscall
		la $t0, type_E # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of th object
		sw $a0, 4($v0) # Setting size in the second word of th object
		sw $v0, 4($sp) # internal_8 = address of allocated object E
		
		# Passing function arguments
		addi $sp, $sp, -8 # Reserving space for arguments
		sw $ra, 4($sp) # Storing return address
		
		# Argument internal_8
		lw $t0, 12($sp)
		sw $t0, 0($sp) # Storing internal_8
		
		# Calling function function___init___at_E
		jal function___init___at_E
		lw $ra, 4($sp)
		sw $v1, 12($sp) # internal_8 = result of function___init___at_E
		addi $sp, $sp, 8 # Freeing space for arguments
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument internal_8
		lw $t0, 16($sp)
		sw $t0, 4($sp) # Storing internal_8
		
		# Argument x
		lw $t0, 48($sp)
		sw $t0, 0($sp) # Storing x
		
		# Calling function function_set_var_at_A
		jal function_set_var_at_A
		lw $ra, 8($sp)
		sw $v1, 12($sp) # internal_9 = result of function_set_var_at_A
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# Loading return value in $v1
		lw $v1, 0($sp)
		
		# Freeing space for local variables
		addi $sp, $sp, 40
		
		jr $ra
		
	function___init___at_B:
		# Function parameters
		#   $ra = 8($sp)
		#   self = 4($sp)
		
		# Reserving space for local variables
		addi $sp, $sp, -4
		
		# Allocating Int 0
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Int # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 0
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 0($sp) # internal_0 = address of allocated object Int
		
		# Set attribute var of self
		lw $t0, 4($sp) # $t0 = self
		lw $t1, 0($sp) # $t1 = internal_0
		beq $t1, $zero, object_set_attribute_8781702264089
		lw $t2, 0($t1)
		la $t3, type_Int
		la $t4, type_Bool
		addi $t5, $zero, 1
		seq $t6, $t2, $t3
		beq $t6, $t5, int_set_attribute_8781702264089
		seq $t6, $t2, $t4
		beq $t6, $t5, bool_set_attribute_8781702264089
		j object_set_attribute_8781702264089
		int_set_attribute_8781702264089:
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		sw $t3, 0($v0)
		sw $a0, 4($v0)
		lw $t5, 8($t1)
		sw $t5, 8($v0)
		sw $v0, 8($t0) # self.var = internal_0
		j end_set_attribute_8781702264089
		bool_set_attribute_8781702264089:
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		sw $t4, 0($v0)
		sw $a0, 4($v0)
		lw $t5, 8($t1)
		sw $t5, 8($v0)
		sw $v0, 8($t0) # self.var = internal_0
		j end_set_attribute_8781702264089
		object_set_attribute_8781702264089:
		sw $t1, 8($t0) # self.var = internal_0
		end_set_attribute_8781702264089:
		
		# Loading return value in $v1
		lw $v1, 4($sp)
		
		# Freeing space for local variables
		addi $sp, $sp, 4
		
		jr $ra
		
	function_method5_at_B:
		# Function parameters
		#   $ra = 24($sp)
		#   self = 20($sp)
		#   num = 16($sp)
		
		# Reserving space for local variables
		addi $sp, $sp, -16
		
		# Allocating Int 0
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Int # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 0
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 12($sp) # x = address of allocated object Int
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument num
		lw $t0, 28($sp)
		sw $t0, 4($sp) # Storing num
		
		# Argument num
		lw $t0, 28($sp)
		sw $t0, 0($sp) # Storing num
		
		# Calling function function_mult
		jal function_mult
		lw $ra, 8($sp)
		sw $v1, 20($sp) # internal_1 = result of function_mult
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument x
		lw $t0, 24($sp)
		sw $t0, 4($sp) # Storing x
		
		# Argument internal_1
		lw $t0, 20($sp)
		sw $t0, 0($sp) # Storing internal_1
		
		# Calling function function_assign
		jal function_assign
		lw $ra, 8($sp)
		sw $v1, 24($sp) # x = result of function_assign
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# Allocating E
		li $v0, 9
		lw $a0, type_E
		syscall
		la $t0, type_E # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of th object
		sw $a0, 4($v0) # Setting size in the second word of th object
		sw $v0, 4($sp) # internal_2 = address of allocated object E
		
		# Passing function arguments
		addi $sp, $sp, -8 # Reserving space for arguments
		sw $ra, 4($sp) # Storing return address
		
		# Argument internal_2
		lw $t0, 12($sp)
		sw $t0, 0($sp) # Storing internal_2
		
		# Calling function function___init___at_E
		jal function___init___at_E
		lw $ra, 4($sp)
		sw $v1, 12($sp) # internal_2 = result of function___init___at_E
		addi $sp, $sp, 8 # Freeing space for arguments
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument internal_2
		lw $t0, 16($sp)
		sw $t0, 4($sp) # Storing internal_2
		
		# Argument x
		lw $t0, 24($sp)
		sw $t0, 0($sp) # Storing x
		
		# Calling function function_set_var_at_A
		jal function_set_var_at_A
		lw $ra, 8($sp)
		sw $v1, 12($sp) # internal_3 = result of function_set_var_at_A
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# Loading return value in $v1
		lw $v1, 0($sp)
		
		# Freeing space for local variables
		addi $sp, $sp, 16
		
		jr $ra
		
	function___init___at_C:
		# Function parameters
		#   $ra = 8($sp)
		#   self = 4($sp)
		
		# Reserving space for local variables
		addi $sp, $sp, -4
		
		# Allocating Int 0
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Int # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 0
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 0($sp) # internal_0 = address of allocated object Int
		
		# Set attribute var of self
		lw $t0, 4($sp) # $t0 = self
		lw $t1, 0($sp) # $t1 = internal_0
		beq $t1, $zero, object_set_attribute_8781702264272
		lw $t2, 0($t1)
		la $t3, type_Int
		la $t4, type_Bool
		addi $t5, $zero, 1
		seq $t6, $t2, $t3
		beq $t6, $t5, int_set_attribute_8781702264272
		seq $t6, $t2, $t4
		beq $t6, $t5, bool_set_attribute_8781702264272
		j object_set_attribute_8781702264272
		int_set_attribute_8781702264272:
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		sw $t3, 0($v0)
		sw $a0, 4($v0)
		lw $t5, 8($t1)
		sw $t5, 8($v0)
		sw $v0, 8($t0) # self.var = internal_0
		j end_set_attribute_8781702264272
		bool_set_attribute_8781702264272:
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		sw $t4, 0($v0)
		sw $a0, 4($v0)
		lw $t5, 8($t1)
		sw $t5, 8($v0)
		sw $v0, 8($t0) # self.var = internal_0
		j end_set_attribute_8781702264272
		object_set_attribute_8781702264272:
		sw $t1, 8($t0) # self.var = internal_0
		end_set_attribute_8781702264272:
		
		# Loading return value in $v1
		lw $v1, 4($sp)
		
		# Freeing space for local variables
		addi $sp, $sp, 4
		
		jr $ra
		
	function_method6_at_C:
		# Function parameters
		#   $ra = 32($sp)
		#   self = 28($sp)
		#   num = 24($sp)
		
		# Reserving space for local variables
		addi $sp, $sp, -24
		
		# Allocating Int 0
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Int # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 0
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 20($sp) # x = address of allocated object Int
		
		# Allocating Int 1
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Int # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 1
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 16($sp) # internal_1 = address of allocated object Int
		
		# Allocating Int 4294967295
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Int # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 4294967295
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 12($sp) # internal_2 = address of allocated object Int
		
		# Allocating Int 0
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Int # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 0
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 8($sp) # internal_3 = address of allocated object Int
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument num
		lw $t0, 36($sp)
		sw $t0, 4($sp) # Storing num
		
		# Argument internal_2
		lw $t0, 24($sp)
		sw $t0, 0($sp) # Storing internal_2
		
		# Calling function function_xor
		jal function_xor
		lw $ra, 8($sp)
		sw $v1, 20($sp) # internal_3 = result of function_xor
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument internal_3
		lw $t0, 20($sp)
		sw $t0, 4($sp) # Storing internal_3
		
		# Argument internal_1
		lw $t0, 28($sp)
		sw $t0, 0($sp) # Storing internal_1
		
		# Calling function function_add
		jal function_add
		lw $ra, 8($sp)
		sw $v1, 20($sp) # internal_3 = result of function_add
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument x
		lw $t0, 32($sp)
		sw $t0, 4($sp) # Storing x
		
		# Argument internal_3
		lw $t0, 20($sp)
		sw $t0, 0($sp) # Storing internal_3
		
		# Calling function function_assign
		jal function_assign
		lw $ra, 8($sp)
		sw $v1, 32($sp) # x = result of function_assign
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# Allocating A
		li $v0, 9
		lw $a0, type_A
		syscall
		la $t0, type_A # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of th object
		sw $a0, 4($v0) # Setting size in the second word of th object
		sw $v0, 4($sp) # internal_4 = address of allocated object A
		
		# Passing function arguments
		addi $sp, $sp, -8 # Reserving space for arguments
		sw $ra, 4($sp) # Storing return address
		
		# Argument internal_4
		lw $t0, 12($sp)
		sw $t0, 0($sp) # Storing internal_4
		
		# Calling function function___init___at_A
		jal function___init___at_A
		lw $ra, 4($sp)
		sw $v1, 12($sp) # internal_4 = result of function___init___at_A
		addi $sp, $sp, 8 # Freeing space for arguments
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument internal_4
		lw $t0, 16($sp)
		sw $t0, 4($sp) # Storing internal_4
		
		# Argument x
		lw $t0, 32($sp)
		sw $t0, 0($sp) # Storing x
		
		# Calling function function_set_var_at_A
		jal function_set_var_at_A
		lw $ra, 8($sp)
		sw $v1, 12($sp) # internal_5 = result of function_set_var_at_A
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# Loading return value in $v1
		lw $v1, 0($sp)
		
		# Freeing space for local variables
		addi $sp, $sp, 24
		
		jr $ra
		
	function_method5_at_C:
		# Function parameters
		#   $ra = 28($sp)
		#   self = 24($sp)
		#   num = 20($sp)
		
		# Reserving space for local variables
		addi $sp, $sp, -20
		
		# Allocating Int 0
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Int # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 0
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 16($sp) # x = address of allocated object Int
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument num
		lw $t0, 32($sp)
		sw $t0, 4($sp) # Storing num
		
		# Argument num
		lw $t0, 32($sp)
		sw $t0, 0($sp) # Storing num
		
		# Calling function function_mult
		jal function_mult
		lw $ra, 8($sp)
		sw $v1, 24($sp) # internal_1 = result of function_mult
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument internal_1
		lw $t0, 24($sp)
		sw $t0, 4($sp) # Storing internal_1
		
		# Argument num
		lw $t0, 32($sp)
		sw $t0, 0($sp) # Storing num
		
		# Calling function function_mult
		jal function_mult
		lw $ra, 8($sp)
		sw $v1, 20($sp) # internal_2 = result of function_mult
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument x
		lw $t0, 28($sp)
		sw $t0, 4($sp) # Storing x
		
		# Argument internal_2
		lw $t0, 20($sp)
		sw $t0, 0($sp) # Storing internal_2
		
		# Calling function function_assign
		jal function_assign
		lw $ra, 8($sp)
		sw $v1, 28($sp) # x = result of function_assign
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# Allocating E
		li $v0, 9
		lw $a0, type_E
		syscall
		la $t0, type_E # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of th object
		sw $a0, 4($v0) # Setting size in the second word of th object
		sw $v0, 4($sp) # internal_3 = address of allocated object E
		
		# Passing function arguments
		addi $sp, $sp, -8 # Reserving space for arguments
		sw $ra, 4($sp) # Storing return address
		
		# Argument internal_3
		lw $t0, 12($sp)
		sw $t0, 0($sp) # Storing internal_3
		
		# Calling function function___init___at_E
		jal function___init___at_E
		lw $ra, 4($sp)
		sw $v1, 12($sp) # internal_3 = result of function___init___at_E
		addi $sp, $sp, 8 # Freeing space for arguments
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument internal_3
		lw $t0, 16($sp)
		sw $t0, 4($sp) # Storing internal_3
		
		# Argument x
		lw $t0, 28($sp)
		sw $t0, 0($sp) # Storing x
		
		# Calling function function_set_var_at_A
		jal function_set_var_at_A
		lw $ra, 8($sp)
		sw $v1, 12($sp) # internal_4 = result of function_set_var_at_A
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# Loading return value in $v1
		lw $v1, 0($sp)
		
		# Freeing space for local variables
		addi $sp, $sp, 20
		
		jr $ra
		
	function___init___at_D:
		# Function parameters
		#   $ra = 8($sp)
		#   self = 4($sp)
		
		# Reserving space for local variables
		addi $sp, $sp, -4
		
		# Allocating Int 0
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Int # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 0
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 0($sp) # internal_0 = address of allocated object Int
		
		# Set attribute var of self
		lw $t0, 4($sp) # $t0 = self
		lw $t1, 0($sp) # $t1 = internal_0
		beq $t1, $zero, object_set_attribute_8781702265441
		lw $t2, 0($t1)
		la $t3, type_Int
		la $t4, type_Bool
		addi $t5, $zero, 1
		seq $t6, $t2, $t3
		beq $t6, $t5, int_set_attribute_8781702265441
		seq $t6, $t2, $t4
		beq $t6, $t5, bool_set_attribute_8781702265441
		j object_set_attribute_8781702265441
		int_set_attribute_8781702265441:
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		sw $t3, 0($v0)
		sw $a0, 4($v0)
		lw $t5, 8($t1)
		sw $t5, 8($v0)
		sw $v0, 8($t0) # self.var = internal_0
		j end_set_attribute_8781702265441
		bool_set_attribute_8781702265441:
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		sw $t4, 0($v0)
		sw $a0, 4($v0)
		lw $t5, 8($t1)
		sw $t5, 8($v0)
		sw $v0, 8($t0) # self.var = internal_0
		j end_set_attribute_8781702265441
		object_set_attribute_8781702265441:
		sw $t1, 8($t0) # self.var = internal_0
		end_set_attribute_8781702265441:
		
		# Loading return value in $v1
		lw $v1, 4($sp)
		
		# Freeing space for local variables
		addi $sp, $sp, 4
		
		jr $ra
		
	function_method7_at_D:
		# Function parameters
		#   $ra = 116($sp)
		#   self = 112($sp)
		#   num = 108($sp)
		
		# Reserving space for local variables
		addi $sp, $sp, -108
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument x
		lw $t0, 116($sp)
		sw $t0, 4($sp) # Storing x
		
		# Argument num
		lw $t0, 120($sp)
		sw $t0, 0($sp) # Storing num
		
		# Calling function function_assign
		jal function_assign
		lw $ra, 8($sp)
		sw $v1, 116($sp) # x = result of function_assign
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# Allocating Bool 0
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Bool # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 0
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 96($sp) # internal_2 = address of allocated object Int
		
		# Allocating Int 0
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Int # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 0
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 92($sp) # internal_3 = address of allocated object Int
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument x
		lw $t0, 116($sp)
		sw $t0, 4($sp) # Storing x
		
		# Argument internal_3
		lw $t0, 104($sp)
		sw $t0, 0($sp) # Storing internal_3
		
		# Calling function function_less_than
		jal function_less_than
		lw $ra, 8($sp)
		sw $v1, 100($sp) # internal_4 = result of function_less_than
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# internal_2 = internal_4
		lw $t0, 88($sp)
		sw $t0, 96($sp)
		
		# If internal_2 then goto then_8781702323502
		lw $t0, 96($sp) # Loading the address of the condition
		lw $t0, 8($t0) # Loading the value of the condition
		addi $t1, $zero, 1 # Setting the value to 1 for comparison
		beq $t0, $t1, then_8781702323502
		
		# Jumping to else_8781702323502
		j else_8781702323502
		
		then_8781702323502:
		
		# Allocating Int 1
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Int # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 1
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 84($sp) # internal_5 = address of allocated object Int
		
		# Allocating Int 4294967295
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Int # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 4294967295
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 80($sp) # internal_6 = address of allocated object Int
		
		# Allocating Int 0
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Int # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 0
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 76($sp) # internal_7 = address of allocated object Int
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument x
		lw $t0, 116($sp)
		sw $t0, 4($sp) # Storing x
		
		# Argument internal_6
		lw $t0, 92($sp)
		sw $t0, 0($sp) # Storing internal_6
		
		# Calling function function_xor
		jal function_xor
		lw $ra, 8($sp)
		sw $v1, 88($sp) # internal_7 = result of function_xor
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument internal_7
		lw $t0, 88($sp)
		sw $t0, 4($sp) # Storing internal_7
		
		# Argument internal_5
		lw $t0, 96($sp)
		sw $t0, 0($sp) # Storing internal_5
		
		# Calling function function_add
		jal function_add
		lw $ra, 8($sp)
		sw $v1, 88($sp) # internal_7 = result of function_add
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument self
		lw $t0, 124($sp)
		sw $t0, 4($sp) # Storing self
		
		# Argument internal_7
		lw $t0, 88($sp)
		sw $t0, 0($sp) # Storing internal_7
		
		# Calling function function_method7_at_D
		jal function_method7_at_D
		lw $ra, 8($sp)
		sw $v1, 84($sp) # internal_8 = result of function_method7_at_D
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# internal_1 = internal_8
		lw $t0, 72($sp)
		sw $t0, 100($sp)
		
		# Jumping to endif_8781702323502
		j endif_8781702323502
		
		else_8781702323502:
		
		# Allocating Bool 0
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Bool # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 0
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 64($sp) # internal_10 = address of allocated object Int
		
		# Allocating Int 0
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Int # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 0
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 60($sp) # internal_11 = address of allocated object Int
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument internal_11
		lw $t0, 72($sp)
		sw $t0, 4($sp) # Storing internal_11
		
		# Argument x
		lw $t0, 116($sp)
		sw $t0, 0($sp) # Storing x
		
		# Calling function function_equal
		jal function_equal
		lw $ra, 8($sp)
		sw $v1, 68($sp) # internal_12 = result of function_equal
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# internal_10 = internal_12
		lw $t0, 56($sp)
		sw $t0, 64($sp)
		
		# If internal_10 then goto then_8781702323481
		lw $t0, 64($sp) # Loading the address of the condition
		lw $t0, 8($t0) # Loading the value of the condition
		addi $t1, $zero, 1 # Setting the value to 1 for comparison
		beq $t0, $t1, then_8781702323481
		
		# Jumping to else_8781702323481
		j else_8781702323481
		
		then_8781702323481:
		
		# Allocating Bool 1
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Bool # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 1
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 52($sp) # internal_13 = address of allocated object Int
		
		# internal_9 = internal_13
		lw $t0, 52($sp)
		sw $t0, 68($sp)
		
		# Jumping to endif_8781702323481
		j endif_8781702323481
		
		else_8781702323481:
		
		# Allocating Bool 0
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Bool # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 0
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 44($sp) # internal_15 = address of allocated object Int
		
		# Allocating Int 1
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Int # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 1
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 40($sp) # internal_16 = address of allocated object Int
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument internal_16
		lw $t0, 52($sp)
		sw $t0, 4($sp) # Storing internal_16
		
		# Argument x
		lw $t0, 116($sp)
		sw $t0, 0($sp) # Storing x
		
		# Calling function function_equal
		jal function_equal
		lw $ra, 8($sp)
		sw $v1, 48($sp) # internal_17 = result of function_equal
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# internal_15 = internal_17
		lw $t0, 36($sp)
		sw $t0, 44($sp)
		
		# If internal_15 then goto then_8781702323484
		lw $t0, 44($sp) # Loading the address of the condition
		lw $t0, 8($t0) # Loading the value of the condition
		addi $t1, $zero, 1 # Setting the value to 1 for comparison
		beq $t0, $t1, then_8781702323484
		
		# Jumping to else_8781702323484
		j else_8781702323484
		
		then_8781702323484:
		
		# Allocating Bool 0
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Bool # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 0
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 32($sp) # internal_18 = address of allocated object Int
		
		# internal_14 = internal_18
		lw $t0, 32($sp)
		sw $t0, 48($sp)
		
		# Jumping to endif_8781702323484
		j endif_8781702323484
		
		else_8781702323484:
		
		# Allocating Bool 0
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Bool # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 0
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 24($sp) # internal_20 = address of allocated object Int
		
		# Allocating Int 2
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Int # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 2
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 20($sp) # internal_21 = address of allocated object Int
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument internal_21
		lw $t0, 32($sp)
		sw $t0, 4($sp) # Storing internal_21
		
		# Argument x
		lw $t0, 116($sp)
		sw $t0, 0($sp) # Storing x
		
		# Calling function function_equal
		jal function_equal
		lw $ra, 8($sp)
		sw $v1, 28($sp) # internal_22 = result of function_equal
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# internal_20 = internal_22
		lw $t0, 16($sp)
		sw $t0, 24($sp)
		
		# If internal_20 then goto then_8781702323490
		lw $t0, 24($sp) # Loading the address of the condition
		lw $t0, 8($t0) # Loading the value of the condition
		addi $t1, $zero, 1 # Setting the value to 1 for comparison
		beq $t0, $t1, then_8781702323490
		
		# Jumping to else_8781702323490
		j else_8781702323490
		
		then_8781702323490:
		
		# Allocating Bool 0
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Bool # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 0
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 12($sp) # internal_23 = address of allocated object Int
		
		# internal_19 = internal_23
		lw $t0, 12($sp)
		sw $t0, 28($sp)
		
		# Jumping to endif_8781702323490
		j endif_8781702323490
		
		else_8781702323490:
		
		# Allocating Int 3
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Int # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 3
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 8($sp) # internal_24 = address of allocated object Int
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument x
		lw $t0, 116($sp)
		sw $t0, 4($sp) # Storing x
		
		# Argument internal_24
		lw $t0, 20($sp)
		sw $t0, 0($sp) # Storing internal_24
		
		# Calling function function_sub
		jal function_sub
		lw $ra, 8($sp)
		sw $v1, 16($sp) # internal_25 = result of function_sub
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument self
		lw $t0, 124($sp)
		sw $t0, 4($sp) # Storing self
		
		# Argument internal_25
		lw $t0, 16($sp)
		sw $t0, 0($sp) # Storing internal_25
		
		# Calling function function_method7_at_D
		jal function_method7_at_D
		lw $ra, 8($sp)
		sw $v1, 12($sp) # internal_26 = result of function_method7_at_D
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# internal_19 = internal_26
		lw $t0, 0($sp)
		sw $t0, 28($sp)
		
		# Jumping to endif_8781702323490
		j endif_8781702323490
		
		endif_8781702323490:
		
		# internal_14 = internal_19
		lw $t0, 28($sp)
		sw $t0, 48($sp)
		
		# Jumping to endif_8781702323484
		j endif_8781702323484
		
		endif_8781702323484:
		
		# internal_9 = internal_14
		lw $t0, 48($sp)
		sw $t0, 68($sp)
		
		# Jumping to endif_8781702323481
		j endif_8781702323481
		
		endif_8781702323481:
		
		# internal_1 = internal_9
		lw $t0, 68($sp)
		sw $t0, 100($sp)
		
		# Jumping to endif_8781702323502
		j endif_8781702323502
		
		endif_8781702323502:
		
		# Loading return value in $v1
		lw $v1, 100($sp)
		
		# Freeing space for local variables
		addi $sp, $sp, 108
		
		jr $ra
		
	function___init___at_E:
		# Function parameters
		#   $ra = 8($sp)
		#   self = 4($sp)
		
		# Reserving space for local variables
		addi $sp, $sp, -4
		
		# Allocating Int 0
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Int # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 0
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 0($sp) # internal_0 = address of allocated object Int
		
		# Set attribute var of self
		lw $t0, 4($sp) # $t0 = self
		lw $t1, 0($sp) # $t1 = internal_0
		beq $t1, $zero, object_set_attribute_8781702267046
		lw $t2, 0($t1)
		la $t3, type_Int
		la $t4, type_Bool
		addi $t5, $zero, 1
		seq $t6, $t2, $t3
		beq $t6, $t5, int_set_attribute_8781702267046
		seq $t6, $t2, $t4
		beq $t6, $t5, bool_set_attribute_8781702267046
		j object_set_attribute_8781702267046
		int_set_attribute_8781702267046:
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		sw $t3, 0($v0)
		sw $a0, 4($v0)
		lw $t5, 8($t1)
		sw $t5, 8($v0)
		sw $v0, 8($t0) # self.var = internal_0
		j end_set_attribute_8781702267046
		bool_set_attribute_8781702267046:
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		sw $t4, 0($v0)
		sw $a0, 4($v0)
		lw $t5, 8($t1)
		sw $t5, 8($v0)
		sw $v0, 8($t0) # self.var = internal_0
		j end_set_attribute_8781702267046
		object_set_attribute_8781702267046:
		sw $t1, 8($t0) # self.var = internal_0
		end_set_attribute_8781702267046:
		
		# Loading return value in $v1
		lw $v1, 4($sp)
		
		# Freeing space for local variables
		addi $sp, $sp, 4
		
		jr $ra
		
	function_method6_at_E:
		# Function parameters
		#   $ra = 28($sp)
		#   self = 24($sp)
		#   num = 20($sp)
		
		# Reserving space for local variables
		addi $sp, $sp, -20
		
		# Allocating Int 0
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Int # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 0
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 16($sp) # x = address of allocated object Int
		
		# Allocating Int 8
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Int # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 8
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 12($sp) # internal_1 = address of allocated object Int
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument num
		lw $t0, 32($sp)
		sw $t0, 4($sp) # Storing num
		
		# Argument internal_1
		lw $t0, 24($sp)
		sw $t0, 0($sp) # Storing internal_1
		
		# Calling function function_div
		jal function_div
		lw $ra, 8($sp)
		sw $v1, 20($sp) # internal_2 = result of function_div
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument x
		lw $t0, 28($sp)
		sw $t0, 4($sp) # Storing x
		
		# Argument internal_2
		lw $t0, 20($sp)
		sw $t0, 0($sp) # Storing internal_2
		
		# Calling function function_assign
		jal function_assign
		lw $ra, 8($sp)
		sw $v1, 28($sp) # x = result of function_assign
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# Allocating A
		li $v0, 9
		lw $a0, type_A
		syscall
		la $t0, type_A # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of th object
		sw $a0, 4($v0) # Setting size in the second word of th object
		sw $v0, 4($sp) # internal_3 = address of allocated object A
		
		# Passing function arguments
		addi $sp, $sp, -8 # Reserving space for arguments
		sw $ra, 4($sp) # Storing return address
		
		# Argument internal_3
		lw $t0, 12($sp)
		sw $t0, 0($sp) # Storing internal_3
		
		# Calling function function___init___at_A
		jal function___init___at_A
		lw $ra, 4($sp)
		sw $v1, 12($sp) # internal_3 = result of function___init___at_A
		addi $sp, $sp, 8 # Freeing space for arguments
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument internal_3
		lw $t0, 16($sp)
		sw $t0, 4($sp) # Storing internal_3
		
		# Argument x
		lw $t0, 28($sp)
		sw $t0, 0($sp) # Storing x
		
		# Calling function function_set_var_at_A
		jal function_set_var_at_A
		lw $ra, 8($sp)
		sw $v1, 12($sp) # internal_4 = result of function_set_var_at_A
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# Loading return value in $v1
		lw $v1, 0($sp)
		
		# Freeing space for local variables
		addi $sp, $sp, 20
		
		jr $ra
		
	function___init___at_A2I:
		# Function parameters
		#   $ra = 4($sp)
		#   self = 0($sp)
		
		# Loading return value in $v1
		lw $v1, 0($sp)
		
		jr $ra
		
	function_c2i_at_A2I:
		# Function parameters
		#   $ra = 216($sp)
		#   self = 212($sp)
		#   char = 208($sp)
		
		# Reserving space for local variables
		addi $sp, $sp, -208
		
		# Allocating Bool 0
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Bool # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 0
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 200($sp) # internal_1 = address of allocated object Int
		
		# Allocating String
		li $v0, 9
		addi $a0, $zero, 10 # $a0 = length of string + 9 for 4 bytes for the type, 4 bytes for the length of the string and 1 byte for null-terminator
		syscall
		
		la $t0, type_String
		sw $t0, 0($v0) # Setting type in the first word of the object
		
		addi $t0, $zero, 10
		sw $t0, 4($v0) # Setting length of the string in the second word of the object
		
		addi $t0, $zero, 48
		sb $t0, 8($v0) # internal_2[0] = '0'
		
		sb $zero, 9($v0) # Null-terminator at the end of the string
		
		sw $v0, 196($sp) # internal_2 = "0"
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument char
		lw $t0, 220($sp)
		sw $t0, 4($sp) # Storing char
		
		# Argument internal_2
		lw $t0, 208($sp)
		sw $t0, 0($sp) # Storing internal_2
		
		# Calling function function_equal
		jal function_equal
		lw $ra, 8($sp)
		sw $v1, 204($sp) # internal_3 = result of function_equal
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# internal_1 = internal_3
		lw $t0, 192($sp)
		sw $t0, 200($sp)
		
		# If internal_1 then goto then_8781702324152
		lw $t0, 200($sp) # Loading the address of the condition
		lw $t0, 8($t0) # Loading the value of the condition
		addi $t1, $zero, 1 # Setting the value to 1 for comparison
		beq $t0, $t1, then_8781702324152
		
		# Jumping to else_8781702324152
		j else_8781702324152
		
		then_8781702324152:
		
		# Allocating Int 0
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Int # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 0
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 188($sp) # internal_4 = address of allocated object Int
		
		# internal_0 = internal_4
		lw $t0, 188($sp)
		sw $t0, 204($sp)
		
		# Jumping to endif_8781702324152
		j endif_8781702324152
		
		else_8781702324152:
		
		# Allocating Bool 0
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Bool # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 0
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 180($sp) # internal_6 = address of allocated object Int
		
		# Allocating String
		li $v0, 9
		addi $a0, $zero, 10 # $a0 = length of string + 9 for 4 bytes for the type, 4 bytes for the length of the string and 1 byte for null-terminator
		syscall
		
		la $t0, type_String
		sw $t0, 0($v0) # Setting type in the first word of the object
		
		addi $t0, $zero, 10
		sw $t0, 4($v0) # Setting length of the string in the second word of the object
		
		addi $t0, $zero, 49
		sb $t0, 8($v0) # internal_7[0] = '1'
		
		sb $zero, 9($v0) # Null-terminator at the end of the string
		
		sw $v0, 176($sp) # internal_7 = "1"
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument char
		lw $t0, 220($sp)
		sw $t0, 4($sp) # Storing char
		
		# Argument internal_7
		lw $t0, 188($sp)
		sw $t0, 0($sp) # Storing internal_7
		
		# Calling function function_equal
		jal function_equal
		lw $ra, 8($sp)
		sw $v1, 184($sp) # internal_8 = result of function_equal
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# internal_6 = internal_8
		lw $t0, 172($sp)
		sw $t0, 180($sp)
		
		# If internal_6 then goto then_8781702324146
		lw $t0, 180($sp) # Loading the address of the condition
		lw $t0, 8($t0) # Loading the value of the condition
		addi $t1, $zero, 1 # Setting the value to 1 for comparison
		beq $t0, $t1, then_8781702324146
		
		# Jumping to else_8781702324146
		j else_8781702324146
		
		then_8781702324146:
		
		# Allocating Int 1
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Int # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 1
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 168($sp) # internal_9 = address of allocated object Int
		
		# internal_5 = internal_9
		lw $t0, 168($sp)
		sw $t0, 184($sp)
		
		# Jumping to endif_8781702324146
		j endif_8781702324146
		
		else_8781702324146:
		
		# Allocating Bool 0
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Bool # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 0
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 160($sp) # internal_11 = address of allocated object Int
		
		# Allocating String
		li $v0, 9
		addi $a0, $zero, 10 # $a0 = length of string + 9 for 4 bytes for the type, 4 bytes for the length of the string and 1 byte for null-terminator
		syscall
		
		la $t0, type_String
		sw $t0, 0($v0) # Setting type in the first word of the object
		
		addi $t0, $zero, 10
		sw $t0, 4($v0) # Setting length of the string in the second word of the object
		
		addi $t0, $zero, 50
		sb $t0, 8($v0) # internal_12[0] = '2'
		
		sb $zero, 9($v0) # Null-terminator at the end of the string
		
		sw $v0, 156($sp) # internal_12 = "2"
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument char
		lw $t0, 220($sp)
		sw $t0, 4($sp) # Storing char
		
		# Argument internal_12
		lw $t0, 168($sp)
		sw $t0, 0($sp) # Storing internal_12
		
		# Calling function function_equal
		jal function_equal
		lw $ra, 8($sp)
		sw $v1, 164($sp) # internal_13 = result of function_equal
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# internal_11 = internal_13
		lw $t0, 152($sp)
		sw $t0, 160($sp)
		
		# If internal_11 then goto then_8781702324140
		lw $t0, 160($sp) # Loading the address of the condition
		lw $t0, 8($t0) # Loading the value of the condition
		addi $t1, $zero, 1 # Setting the value to 1 for comparison
		beq $t0, $t1, then_8781702324140
		
		# Jumping to else_8781702324140
		j else_8781702324140
		
		then_8781702324140:
		
		# Allocating Int 2
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Int # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 2
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 148($sp) # internal_14 = address of allocated object Int
		
		# internal_10 = internal_14
		lw $t0, 148($sp)
		sw $t0, 164($sp)
		
		# Jumping to endif_8781702324140
		j endif_8781702324140
		
		else_8781702324140:
		
		# Allocating Bool 0
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Bool # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 0
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 140($sp) # internal_16 = address of allocated object Int
		
		# Allocating String
		li $v0, 9
		addi $a0, $zero, 10 # $a0 = length of string + 9 for 4 bytes for the type, 4 bytes for the length of the string and 1 byte for null-terminator
		syscall
		
		la $t0, type_String
		sw $t0, 0($v0) # Setting type in the first word of the object
		
		addi $t0, $zero, 10
		sw $t0, 4($v0) # Setting length of the string in the second word of the object
		
		addi $t0, $zero, 51
		sb $t0, 8($v0) # internal_17[0] = '3'
		
		sb $zero, 9($v0) # Null-terminator at the end of the string
		
		sw $v0, 136($sp) # internal_17 = "3"
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument char
		lw $t0, 220($sp)
		sw $t0, 4($sp) # Storing char
		
		# Argument internal_17
		lw $t0, 148($sp)
		sw $t0, 0($sp) # Storing internal_17
		
		# Calling function function_equal
		jal function_equal
		lw $ra, 8($sp)
		sw $v1, 144($sp) # internal_18 = result of function_equal
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# internal_16 = internal_18
		lw $t0, 132($sp)
		sw $t0, 140($sp)
		
		# If internal_16 then goto then_8781702324134
		lw $t0, 140($sp) # Loading the address of the condition
		lw $t0, 8($t0) # Loading the value of the condition
		addi $t1, $zero, 1 # Setting the value to 1 for comparison
		beq $t0, $t1, then_8781702324134
		
		# Jumping to else_8781702324134
		j else_8781702324134
		
		then_8781702324134:
		
		# Allocating Int 3
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Int # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 3
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 128($sp) # internal_19 = address of allocated object Int
		
		# internal_15 = internal_19
		lw $t0, 128($sp)
		sw $t0, 144($sp)
		
		# Jumping to endif_8781702324134
		j endif_8781702324134
		
		else_8781702324134:
		
		# Allocating Bool 0
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Bool # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 0
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 120($sp) # internal_21 = address of allocated object Int
		
		# Allocating String
		li $v0, 9
		addi $a0, $zero, 10 # $a0 = length of string + 9 for 4 bytes for the type, 4 bytes for the length of the string and 1 byte for null-terminator
		syscall
		
		la $t0, type_String
		sw $t0, 0($v0) # Setting type in the first word of the object
		
		addi $t0, $zero, 10
		sw $t0, 4($v0) # Setting length of the string in the second word of the object
		
		addi $t0, $zero, 52
		sb $t0, 8($v0) # internal_22[0] = '4'
		
		sb $zero, 9($v0) # Null-terminator at the end of the string
		
		sw $v0, 116($sp) # internal_22 = "4"
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument char
		lw $t0, 220($sp)
		sw $t0, 4($sp) # Storing char
		
		# Argument internal_22
		lw $t0, 128($sp)
		sw $t0, 0($sp) # Storing internal_22
		
		# Calling function function_equal
		jal function_equal
		lw $ra, 8($sp)
		sw $v1, 124($sp) # internal_23 = result of function_equal
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# internal_21 = internal_23
		lw $t0, 112($sp)
		sw $t0, 120($sp)
		
		# If internal_21 then goto then_8781702324128
		lw $t0, 120($sp) # Loading the address of the condition
		lw $t0, 8($t0) # Loading the value of the condition
		addi $t1, $zero, 1 # Setting the value to 1 for comparison
		beq $t0, $t1, then_8781702324128
		
		# Jumping to else_8781702324128
		j else_8781702324128
		
		then_8781702324128:
		
		# Allocating Int 4
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Int # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 4
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 108($sp) # internal_24 = address of allocated object Int
		
		# internal_20 = internal_24
		lw $t0, 108($sp)
		sw $t0, 124($sp)
		
		# Jumping to endif_8781702324128
		j endif_8781702324128
		
		else_8781702324128:
		
		# Allocating Bool 0
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Bool # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 0
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 100($sp) # internal_26 = address of allocated object Int
		
		# Allocating String
		li $v0, 9
		addi $a0, $zero, 10 # $a0 = length of string + 9 for 4 bytes for the type, 4 bytes for the length of the string and 1 byte for null-terminator
		syscall
		
		la $t0, type_String
		sw $t0, 0($v0) # Setting type in the first word of the object
		
		addi $t0, $zero, 10
		sw $t0, 4($v0) # Setting length of the string in the second word of the object
		
		addi $t0, $zero, 53
		sb $t0, 8($v0) # internal_27[0] = '5'
		
		sb $zero, 9($v0) # Null-terminator at the end of the string
		
		sw $v0, 96($sp) # internal_27 = "5"
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument char
		lw $t0, 220($sp)
		sw $t0, 4($sp) # Storing char
		
		# Argument internal_27
		lw $t0, 108($sp)
		sw $t0, 0($sp) # Storing internal_27
		
		# Calling function function_equal
		jal function_equal
		lw $ra, 8($sp)
		sw $v1, 104($sp) # internal_28 = result of function_equal
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# internal_26 = internal_28
		lw $t0, 92($sp)
		sw $t0, 100($sp)
		
		# If internal_26 then goto then_8781702324122
		lw $t0, 100($sp) # Loading the address of the condition
		lw $t0, 8($t0) # Loading the value of the condition
		addi $t1, $zero, 1 # Setting the value to 1 for comparison
		beq $t0, $t1, then_8781702324122
		
		# Jumping to else_8781702324122
		j else_8781702324122
		
		then_8781702324122:
		
		# Allocating Int 5
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Int # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 5
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 88($sp) # internal_29 = address of allocated object Int
		
		# internal_25 = internal_29
		lw $t0, 88($sp)
		sw $t0, 104($sp)
		
		# Jumping to endif_8781702324122
		j endif_8781702324122
		
		else_8781702324122:
		
		# Allocating Bool 0
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Bool # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 0
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 80($sp) # internal_31 = address of allocated object Int
		
		# Allocating String
		li $v0, 9
		addi $a0, $zero, 10 # $a0 = length of string + 9 for 4 bytes for the type, 4 bytes for the length of the string and 1 byte for null-terminator
		syscall
		
		la $t0, type_String
		sw $t0, 0($v0) # Setting type in the first word of the object
		
		addi $t0, $zero, 10
		sw $t0, 4($v0) # Setting length of the string in the second word of the object
		
		addi $t0, $zero, 54
		sb $t0, 8($v0) # internal_32[0] = '6'
		
		sb $zero, 9($v0) # Null-terminator at the end of the string
		
		sw $v0, 76($sp) # internal_32 = "6"
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument char
		lw $t0, 220($sp)
		sw $t0, 4($sp) # Storing char
		
		# Argument internal_32
		lw $t0, 88($sp)
		sw $t0, 0($sp) # Storing internal_32
		
		# Calling function function_equal
		jal function_equal
		lw $ra, 8($sp)
		sw $v1, 84($sp) # internal_33 = result of function_equal
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# internal_31 = internal_33
		lw $t0, 72($sp)
		sw $t0, 80($sp)
		
		# If internal_31 then goto then_8781702324116
		lw $t0, 80($sp) # Loading the address of the condition
		lw $t0, 8($t0) # Loading the value of the condition
		addi $t1, $zero, 1 # Setting the value to 1 for comparison
		beq $t0, $t1, then_8781702324116
		
		# Jumping to else_8781702324116
		j else_8781702324116
		
		then_8781702324116:
		
		# Allocating Int 6
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Int # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 6
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 68($sp) # internal_34 = address of allocated object Int
		
		# internal_30 = internal_34
		lw $t0, 68($sp)
		sw $t0, 84($sp)
		
		# Jumping to endif_8781702324116
		j endif_8781702324116
		
		else_8781702324116:
		
		# Allocating Bool 0
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Bool # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 0
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 60($sp) # internal_36 = address of allocated object Int
		
		# Allocating String
		li $v0, 9
		addi $a0, $zero, 10 # $a0 = length of string + 9 for 4 bytes for the type, 4 bytes for the length of the string and 1 byte for null-terminator
		syscall
		
		la $t0, type_String
		sw $t0, 0($v0) # Setting type in the first word of the object
		
		addi $t0, $zero, 10
		sw $t0, 4($v0) # Setting length of the string in the second word of the object
		
		addi $t0, $zero, 55
		sb $t0, 8($v0) # internal_37[0] = '7'
		
		sb $zero, 9($v0) # Null-terminator at the end of the string
		
		sw $v0, 56($sp) # internal_37 = "7"
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument char
		lw $t0, 220($sp)
		sw $t0, 4($sp) # Storing char
		
		# Argument internal_37
		lw $t0, 68($sp)
		sw $t0, 0($sp) # Storing internal_37
		
		# Calling function function_equal
		jal function_equal
		lw $ra, 8($sp)
		sw $v1, 64($sp) # internal_38 = result of function_equal
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# internal_36 = internal_38
		lw $t0, 52($sp)
		sw $t0, 60($sp)
		
		# If internal_36 then goto then_8781702324110
		lw $t0, 60($sp) # Loading the address of the condition
		lw $t0, 8($t0) # Loading the value of the condition
		addi $t1, $zero, 1 # Setting the value to 1 for comparison
		beq $t0, $t1, then_8781702324110
		
		# Jumping to else_8781702324110
		j else_8781702324110
		
		then_8781702324110:
		
		# Allocating Int 7
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Int # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 7
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 48($sp) # internal_39 = address of allocated object Int
		
		# internal_35 = internal_39
		lw $t0, 48($sp)
		sw $t0, 64($sp)
		
		# Jumping to endif_8781702324110
		j endif_8781702324110
		
		else_8781702324110:
		
		# Allocating Bool 0
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Bool # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 0
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 40($sp) # internal_41 = address of allocated object Int
		
		# Allocating String
		li $v0, 9
		addi $a0, $zero, 10 # $a0 = length of string + 9 for 4 bytes for the type, 4 bytes for the length of the string and 1 byte for null-terminator
		syscall
		
		la $t0, type_String
		sw $t0, 0($v0) # Setting type in the first word of the object
		
		addi $t0, $zero, 10
		sw $t0, 4($v0) # Setting length of the string in the second word of the object
		
		addi $t0, $zero, 56
		sb $t0, 8($v0) # internal_42[0] = '8'
		
		sb $zero, 9($v0) # Null-terminator at the end of the string
		
		sw $v0, 36($sp) # internal_42 = "8"
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument char
		lw $t0, 220($sp)
		sw $t0, 4($sp) # Storing char
		
		# Argument internal_42
		lw $t0, 48($sp)
		sw $t0, 0($sp) # Storing internal_42
		
		# Calling function function_equal
		jal function_equal
		lw $ra, 8($sp)
		sw $v1, 44($sp) # internal_43 = result of function_equal
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# internal_41 = internal_43
		lw $t0, 32($sp)
		sw $t0, 40($sp)
		
		# If internal_41 then goto then_8781702324104
		lw $t0, 40($sp) # Loading the address of the condition
		lw $t0, 8($t0) # Loading the value of the condition
		addi $t1, $zero, 1 # Setting the value to 1 for comparison
		beq $t0, $t1, then_8781702324104
		
		# Jumping to else_8781702324104
		j else_8781702324104
		
		then_8781702324104:
		
		# Allocating Int 8
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Int # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 8
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 28($sp) # internal_44 = address of allocated object Int
		
		# internal_40 = internal_44
		lw $t0, 28($sp)
		sw $t0, 44($sp)
		
		# Jumping to endif_8781702324104
		j endif_8781702324104
		
		else_8781702324104:
		
		# Allocating Bool 0
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Bool # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 0
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 20($sp) # internal_46 = address of allocated object Int
		
		# Allocating String
		li $v0, 9
		addi $a0, $zero, 10 # $a0 = length of string + 9 for 4 bytes for the type, 4 bytes for the length of the string and 1 byte for null-terminator
		syscall
		
		la $t0, type_String
		sw $t0, 0($v0) # Setting type in the first word of the object
		
		addi $t0, $zero, 10
		sw $t0, 4($v0) # Setting length of the string in the second word of the object
		
		addi $t0, $zero, 57
		sb $t0, 8($v0) # internal_47[0] = '9'
		
		sb $zero, 9($v0) # Null-terminator at the end of the string
		
		sw $v0, 16($sp) # internal_47 = "9"
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument char
		lw $t0, 220($sp)
		sw $t0, 4($sp) # Storing char
		
		# Argument internal_47
		lw $t0, 28($sp)
		sw $t0, 0($sp) # Storing internal_47
		
		# Calling function function_equal
		jal function_equal
		lw $ra, 8($sp)
		sw $v1, 24($sp) # internal_48 = result of function_equal
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# internal_46 = internal_48
		lw $t0, 12($sp)
		sw $t0, 20($sp)
		
		# If internal_46 then goto then_8781702324083
		lw $t0, 20($sp) # Loading the address of the condition
		lw $t0, 8($t0) # Loading the value of the condition
		addi $t1, $zero, 1 # Setting the value to 1 for comparison
		beq $t0, $t1, then_8781702324083
		
		# Jumping to else_8781702324083
		j else_8781702324083
		
		then_8781702324083:
		
		# Allocating Int 9
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Int # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 9
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 8($sp) # internal_49 = address of allocated object Int
		
		# internal_45 = internal_49
		lw $t0, 8($sp)
		sw $t0, 24($sp)
		
		# Jumping to endif_8781702324083
		j endif_8781702324083
		
		else_8781702324083:
		
		# Passing function arguments
		addi $sp, $sp, -8 # Reserving space for arguments
		sw $ra, 4($sp) # Storing return address
		
		# Argument self
		lw $t0, 220($sp)
		sw $t0, 0($sp) # Storing self
		
		# Calling function function_abort_at_Object
		jal function_abort_at_Object
		lw $ra, 4($sp)
		sw $v1, 12($sp) # internal_50 = result of function_abort_at_Object
		addi $sp, $sp, 8 # Freeing space for arguments
		
		# Allocating Int 0
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Int # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 0
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 0($sp) # internal_51 = address of allocated object Int
		
		# internal_45 = internal_51
		lw $t0, 0($sp)
		sw $t0, 24($sp)
		
		# Jumping to endif_8781702324083
		j endif_8781702324083
		
		endif_8781702324083:
		
		# internal_40 = internal_45
		lw $t0, 24($sp)
		sw $t0, 44($sp)
		
		# Jumping to endif_8781702324104
		j endif_8781702324104
		
		endif_8781702324104:
		
		# internal_35 = internal_40
		lw $t0, 44($sp)
		sw $t0, 64($sp)
		
		# Jumping to endif_8781702324110
		j endif_8781702324110
		
		endif_8781702324110:
		
		# internal_30 = internal_35
		lw $t0, 64($sp)
		sw $t0, 84($sp)
		
		# Jumping to endif_8781702324116
		j endif_8781702324116
		
		endif_8781702324116:
		
		# internal_25 = internal_30
		lw $t0, 84($sp)
		sw $t0, 104($sp)
		
		# Jumping to endif_8781702324122
		j endif_8781702324122
		
		endif_8781702324122:
		
		# internal_20 = internal_25
		lw $t0, 104($sp)
		sw $t0, 124($sp)
		
		# Jumping to endif_8781702324128
		j endif_8781702324128
		
		endif_8781702324128:
		
		# internal_15 = internal_20
		lw $t0, 124($sp)
		sw $t0, 144($sp)
		
		# Jumping to endif_8781702324134
		j endif_8781702324134
		
		endif_8781702324134:
		
		# internal_10 = internal_15
		lw $t0, 144($sp)
		sw $t0, 164($sp)
		
		# Jumping to endif_8781702324140
		j endif_8781702324140
		
		endif_8781702324140:
		
		# internal_5 = internal_10
		lw $t0, 164($sp)
		sw $t0, 184($sp)
		
		# Jumping to endif_8781702324146
		j endif_8781702324146
		
		endif_8781702324146:
		
		# internal_0 = internal_5
		lw $t0, 184($sp)
		sw $t0, 204($sp)
		
		# Jumping to endif_8781702324152
		j endif_8781702324152
		
		endif_8781702324152:
		
		# Loading return value in $v1
		lw $v1, 204($sp)
		
		# Freeing space for local variables
		addi $sp, $sp, 208
		
		jr $ra
		
	function_i2c_at_A2I:
		# Function parameters
		#   $ra = 216($sp)
		#   self = 212($sp)
		#   i = 208($sp)
		
		# Reserving space for local variables
		addi $sp, $sp, -208
		
		# Allocating Bool 0
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Bool # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 0
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 200($sp) # internal_1 = address of allocated object Int
		
		# Allocating Int 0
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Int # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 0
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 196($sp) # internal_2 = address of allocated object Int
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument i
		lw $t0, 220($sp)
		sw $t0, 4($sp) # Storing i
		
		# Argument internal_2
		lw $t0, 208($sp)
		sw $t0, 0($sp) # Storing internal_2
		
		# Calling function function_equal
		jal function_equal
		lw $ra, 8($sp)
		sw $v1, 204($sp) # internal_3 = result of function_equal
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# internal_1 = internal_3
		lw $t0, 192($sp)
		sw $t0, 200($sp)
		
		# If internal_1 then goto then_8781702324730
		lw $t0, 200($sp) # Loading the address of the condition
		lw $t0, 8($t0) # Loading the value of the condition
		addi $t1, $zero, 1 # Setting the value to 1 for comparison
		beq $t0, $t1, then_8781702324730
		
		# Jumping to else_8781702324730
		j else_8781702324730
		
		then_8781702324730:
		
		# Allocating String
		li $v0, 9
		addi $a0, $zero, 10 # $a0 = length of string + 9 for 4 bytes for the type, 4 bytes for the length of the string and 1 byte for null-terminator
		syscall
		
		la $t0, type_String
		sw $t0, 0($v0) # Setting type in the first word of the object
		
		addi $t0, $zero, 10
		sw $t0, 4($v0) # Setting length of the string in the second word of the object
		
		addi $t0, $zero, 48
		sb $t0, 8($v0) # internal_4[0] = '0'
		
		sb $zero, 9($v0) # Null-terminator at the end of the string
		
		sw $v0, 188($sp) # internal_4 = "0"
		
		# internal_0 = internal_4
		lw $t0, 188($sp)
		sw $t0, 204($sp)
		
		# Jumping to endif_8781702324730
		j endif_8781702324730
		
		else_8781702324730:
		
		# Allocating Bool 0
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Bool # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 0
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 180($sp) # internal_6 = address of allocated object Int
		
		# Allocating Int 1
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Int # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 1
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 176($sp) # internal_7 = address of allocated object Int
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument i
		lw $t0, 220($sp)
		sw $t0, 4($sp) # Storing i
		
		# Argument internal_7
		lw $t0, 188($sp)
		sw $t0, 0($sp) # Storing internal_7
		
		# Calling function function_equal
		jal function_equal
		lw $ra, 8($sp)
		sw $v1, 184($sp) # internal_8 = result of function_equal
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# internal_6 = internal_8
		lw $t0, 172($sp)
		sw $t0, 180($sp)
		
		# If internal_6 then goto then_8781702324724
		lw $t0, 180($sp) # Loading the address of the condition
		lw $t0, 8($t0) # Loading the value of the condition
		addi $t1, $zero, 1 # Setting the value to 1 for comparison
		beq $t0, $t1, then_8781702324724
		
		# Jumping to else_8781702324724
		j else_8781702324724
		
		then_8781702324724:
		
		# Allocating String
		li $v0, 9
		addi $a0, $zero, 10 # $a0 = length of string + 9 for 4 bytes for the type, 4 bytes for the length of the string and 1 byte for null-terminator
		syscall
		
		la $t0, type_String
		sw $t0, 0($v0) # Setting type in the first word of the object
		
		addi $t0, $zero, 10
		sw $t0, 4($v0) # Setting length of the string in the second word of the object
		
		addi $t0, $zero, 49
		sb $t0, 8($v0) # internal_9[0] = '1'
		
		sb $zero, 9($v0) # Null-terminator at the end of the string
		
		sw $v0, 168($sp) # internal_9 = "1"
		
		# internal_5 = internal_9
		lw $t0, 168($sp)
		sw $t0, 184($sp)
		
		# Jumping to endif_8781702324724
		j endif_8781702324724
		
		else_8781702324724:
		
		# Allocating Bool 0
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Bool # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 0
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 160($sp) # internal_11 = address of allocated object Int
		
		# Allocating Int 2
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Int # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 2
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 156($sp) # internal_12 = address of allocated object Int
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument i
		lw $t0, 220($sp)
		sw $t0, 4($sp) # Storing i
		
		# Argument internal_12
		lw $t0, 168($sp)
		sw $t0, 0($sp) # Storing internal_12
		
		# Calling function function_equal
		jal function_equal
		lw $ra, 8($sp)
		sw $v1, 164($sp) # internal_13 = result of function_equal
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# internal_11 = internal_13
		lw $t0, 152($sp)
		sw $t0, 160($sp)
		
		# If internal_11 then goto then_8781702324718
		lw $t0, 160($sp) # Loading the address of the condition
		lw $t0, 8($t0) # Loading the value of the condition
		addi $t1, $zero, 1 # Setting the value to 1 for comparison
		beq $t0, $t1, then_8781702324718
		
		# Jumping to else_8781702324718
		j else_8781702324718
		
		then_8781702324718:
		
		# Allocating String
		li $v0, 9
		addi $a0, $zero, 10 # $a0 = length of string + 9 for 4 bytes for the type, 4 bytes for the length of the string and 1 byte for null-terminator
		syscall
		
		la $t0, type_String
		sw $t0, 0($v0) # Setting type in the first word of the object
		
		addi $t0, $zero, 10
		sw $t0, 4($v0) # Setting length of the string in the second word of the object
		
		addi $t0, $zero, 50
		sb $t0, 8($v0) # internal_14[0] = '2'
		
		sb $zero, 9($v0) # Null-terminator at the end of the string
		
		sw $v0, 148($sp) # internal_14 = "2"
		
		# internal_10 = internal_14
		lw $t0, 148($sp)
		sw $t0, 164($sp)
		
		# Jumping to endif_8781702324718
		j endif_8781702324718
		
		else_8781702324718:
		
		# Allocating Bool 0
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Bool # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 0
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 140($sp) # internal_16 = address of allocated object Int
		
		# Allocating Int 3
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Int # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 3
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 136($sp) # internal_17 = address of allocated object Int
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument i
		lw $t0, 220($sp)
		sw $t0, 4($sp) # Storing i
		
		# Argument internal_17
		lw $t0, 148($sp)
		sw $t0, 0($sp) # Storing internal_17
		
		# Calling function function_equal
		jal function_equal
		lw $ra, 8($sp)
		sw $v1, 144($sp) # internal_18 = result of function_equal
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# internal_16 = internal_18
		lw $t0, 132($sp)
		sw $t0, 140($sp)
		
		# If internal_16 then goto then_8781702324712
		lw $t0, 140($sp) # Loading the address of the condition
		lw $t0, 8($t0) # Loading the value of the condition
		addi $t1, $zero, 1 # Setting the value to 1 for comparison
		beq $t0, $t1, then_8781702324712
		
		# Jumping to else_8781702324712
		j else_8781702324712
		
		then_8781702324712:
		
		# Allocating String
		li $v0, 9
		addi $a0, $zero, 10 # $a0 = length of string + 9 for 4 bytes for the type, 4 bytes for the length of the string and 1 byte for null-terminator
		syscall
		
		la $t0, type_String
		sw $t0, 0($v0) # Setting type in the first word of the object
		
		addi $t0, $zero, 10
		sw $t0, 4($v0) # Setting length of the string in the second word of the object
		
		addi $t0, $zero, 51
		sb $t0, 8($v0) # internal_19[0] = '3'
		
		sb $zero, 9($v0) # Null-terminator at the end of the string
		
		sw $v0, 128($sp) # internal_19 = "3"
		
		# internal_15 = internal_19
		lw $t0, 128($sp)
		sw $t0, 144($sp)
		
		# Jumping to endif_8781702324712
		j endif_8781702324712
		
		else_8781702324712:
		
		# Allocating Bool 0
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Bool # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 0
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 120($sp) # internal_21 = address of allocated object Int
		
		# Allocating Int 4
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Int # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 4
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 116($sp) # internal_22 = address of allocated object Int
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument i
		lw $t0, 220($sp)
		sw $t0, 4($sp) # Storing i
		
		# Argument internal_22
		lw $t0, 128($sp)
		sw $t0, 0($sp) # Storing internal_22
		
		# Calling function function_equal
		jal function_equal
		lw $ra, 8($sp)
		sw $v1, 124($sp) # internal_23 = result of function_equal
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# internal_21 = internal_23
		lw $t0, 112($sp)
		sw $t0, 120($sp)
		
		# If internal_21 then goto then_8781702324706
		lw $t0, 120($sp) # Loading the address of the condition
		lw $t0, 8($t0) # Loading the value of the condition
		addi $t1, $zero, 1 # Setting the value to 1 for comparison
		beq $t0, $t1, then_8781702324706
		
		# Jumping to else_8781702324706
		j else_8781702324706
		
		then_8781702324706:
		
		# Allocating String
		li $v0, 9
		addi $a0, $zero, 10 # $a0 = length of string + 9 for 4 bytes for the type, 4 bytes for the length of the string and 1 byte for null-terminator
		syscall
		
		la $t0, type_String
		sw $t0, 0($v0) # Setting type in the first word of the object
		
		addi $t0, $zero, 10
		sw $t0, 4($v0) # Setting length of the string in the second word of the object
		
		addi $t0, $zero, 52
		sb $t0, 8($v0) # internal_24[0] = '4'
		
		sb $zero, 9($v0) # Null-terminator at the end of the string
		
		sw $v0, 108($sp) # internal_24 = "4"
		
		# internal_20 = internal_24
		lw $t0, 108($sp)
		sw $t0, 124($sp)
		
		# Jumping to endif_8781702324706
		j endif_8781702324706
		
		else_8781702324706:
		
		# Allocating Bool 0
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Bool # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 0
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 100($sp) # internal_26 = address of allocated object Int
		
		# Allocating Int 5
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Int # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 5
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 96($sp) # internal_27 = address of allocated object Int
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument i
		lw $t0, 220($sp)
		sw $t0, 4($sp) # Storing i
		
		# Argument internal_27
		lw $t0, 108($sp)
		sw $t0, 0($sp) # Storing internal_27
		
		# Calling function function_equal
		jal function_equal
		lw $ra, 8($sp)
		sw $v1, 104($sp) # internal_28 = result of function_equal
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# internal_26 = internal_28
		lw $t0, 92($sp)
		sw $t0, 100($sp)
		
		# If internal_26 then goto then_8781702324700
		lw $t0, 100($sp) # Loading the address of the condition
		lw $t0, 8($t0) # Loading the value of the condition
		addi $t1, $zero, 1 # Setting the value to 1 for comparison
		beq $t0, $t1, then_8781702324700
		
		# Jumping to else_8781702324700
		j else_8781702324700
		
		then_8781702324700:
		
		# Allocating String
		li $v0, 9
		addi $a0, $zero, 10 # $a0 = length of string + 9 for 4 bytes for the type, 4 bytes for the length of the string and 1 byte for null-terminator
		syscall
		
		la $t0, type_String
		sw $t0, 0($v0) # Setting type in the first word of the object
		
		addi $t0, $zero, 10
		sw $t0, 4($v0) # Setting length of the string in the second word of the object
		
		addi $t0, $zero, 53
		sb $t0, 8($v0) # internal_29[0] = '5'
		
		sb $zero, 9($v0) # Null-terminator at the end of the string
		
		sw $v0, 88($sp) # internal_29 = "5"
		
		# internal_25 = internal_29
		lw $t0, 88($sp)
		sw $t0, 104($sp)
		
		# Jumping to endif_8781702324700
		j endif_8781702324700
		
		else_8781702324700:
		
		# Allocating Bool 0
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Bool # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 0
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 80($sp) # internal_31 = address of allocated object Int
		
		# Allocating Int 6
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Int # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 6
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 76($sp) # internal_32 = address of allocated object Int
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument i
		lw $t0, 220($sp)
		sw $t0, 4($sp) # Storing i
		
		# Argument internal_32
		lw $t0, 88($sp)
		sw $t0, 0($sp) # Storing internal_32
		
		# Calling function function_equal
		jal function_equal
		lw $ra, 8($sp)
		sw $v1, 84($sp) # internal_33 = result of function_equal
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# internal_31 = internal_33
		lw $t0, 72($sp)
		sw $t0, 80($sp)
		
		# If internal_31 then goto then_8781702324694
		lw $t0, 80($sp) # Loading the address of the condition
		lw $t0, 8($t0) # Loading the value of the condition
		addi $t1, $zero, 1 # Setting the value to 1 for comparison
		beq $t0, $t1, then_8781702324694
		
		# Jumping to else_8781702324694
		j else_8781702324694
		
		then_8781702324694:
		
		# Allocating String
		li $v0, 9
		addi $a0, $zero, 10 # $a0 = length of string + 9 for 4 bytes for the type, 4 bytes for the length of the string and 1 byte for null-terminator
		syscall
		
		la $t0, type_String
		sw $t0, 0($v0) # Setting type in the first word of the object
		
		addi $t0, $zero, 10
		sw $t0, 4($v0) # Setting length of the string in the second word of the object
		
		addi $t0, $zero, 54
		sb $t0, 8($v0) # internal_34[0] = '6'
		
		sb $zero, 9($v0) # Null-terminator at the end of the string
		
		sw $v0, 68($sp) # internal_34 = "6"
		
		# internal_30 = internal_34
		lw $t0, 68($sp)
		sw $t0, 84($sp)
		
		# Jumping to endif_8781702324694
		j endif_8781702324694
		
		else_8781702324694:
		
		# Allocating Bool 0
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Bool # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 0
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 60($sp) # internal_36 = address of allocated object Int
		
		# Allocating Int 7
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Int # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 7
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 56($sp) # internal_37 = address of allocated object Int
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument i
		lw $t0, 220($sp)
		sw $t0, 4($sp) # Storing i
		
		# Argument internal_37
		lw $t0, 68($sp)
		sw $t0, 0($sp) # Storing internal_37
		
		# Calling function function_equal
		jal function_equal
		lw $ra, 8($sp)
		sw $v1, 64($sp) # internal_38 = result of function_equal
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# internal_36 = internal_38
		lw $t0, 52($sp)
		sw $t0, 60($sp)
		
		# If internal_36 then goto then_8781702324688
		lw $t0, 60($sp) # Loading the address of the condition
		lw $t0, 8($t0) # Loading the value of the condition
		addi $t1, $zero, 1 # Setting the value to 1 for comparison
		beq $t0, $t1, then_8781702324688
		
		# Jumping to else_8781702324688
		j else_8781702324688
		
		then_8781702324688:
		
		# Allocating String
		li $v0, 9
		addi $a0, $zero, 10 # $a0 = length of string + 9 for 4 bytes for the type, 4 bytes for the length of the string and 1 byte for null-terminator
		syscall
		
		la $t0, type_String
		sw $t0, 0($v0) # Setting type in the first word of the object
		
		addi $t0, $zero, 10
		sw $t0, 4($v0) # Setting length of the string in the second word of the object
		
		addi $t0, $zero, 55
		sb $t0, 8($v0) # internal_39[0] = '7'
		
		sb $zero, 9($v0) # Null-terminator at the end of the string
		
		sw $v0, 48($sp) # internal_39 = "7"
		
		# internal_35 = internal_39
		lw $t0, 48($sp)
		sw $t0, 64($sp)
		
		# Jumping to endif_8781702324688
		j endif_8781702324688
		
		else_8781702324688:
		
		# Allocating Bool 0
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Bool # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 0
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 40($sp) # internal_41 = address of allocated object Int
		
		# Allocating Int 8
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Int # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 8
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 36($sp) # internal_42 = address of allocated object Int
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument i
		lw $t0, 220($sp)
		sw $t0, 4($sp) # Storing i
		
		# Argument internal_42
		lw $t0, 48($sp)
		sw $t0, 0($sp) # Storing internal_42
		
		# Calling function function_equal
		jal function_equal
		lw $ra, 8($sp)
		sw $v1, 44($sp) # internal_43 = result of function_equal
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# internal_41 = internal_43
		lw $t0, 32($sp)
		sw $t0, 40($sp)
		
		# If internal_41 then goto then_8781702324682
		lw $t0, 40($sp) # Loading the address of the condition
		lw $t0, 8($t0) # Loading the value of the condition
		addi $t1, $zero, 1 # Setting the value to 1 for comparison
		beq $t0, $t1, then_8781702324682
		
		# Jumping to else_8781702324682
		j else_8781702324682
		
		then_8781702324682:
		
		# Allocating String
		li $v0, 9
		addi $a0, $zero, 10 # $a0 = length of string + 9 for 4 bytes for the type, 4 bytes for the length of the string and 1 byte for null-terminator
		syscall
		
		la $t0, type_String
		sw $t0, 0($v0) # Setting type in the first word of the object
		
		addi $t0, $zero, 10
		sw $t0, 4($v0) # Setting length of the string in the second word of the object
		
		addi $t0, $zero, 56
		sb $t0, 8($v0) # internal_44[0] = '8'
		
		sb $zero, 9($v0) # Null-terminator at the end of the string
		
		sw $v0, 28($sp) # internal_44 = "8"
		
		# internal_40 = internal_44
		lw $t0, 28($sp)
		sw $t0, 44($sp)
		
		# Jumping to endif_8781702324682
		j endif_8781702324682
		
		else_8781702324682:
		
		# Allocating Bool 0
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Bool # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 0
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 20($sp) # internal_46 = address of allocated object Int
		
		# Allocating Int 9
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Int # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 9
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 16($sp) # internal_47 = address of allocated object Int
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument i
		lw $t0, 220($sp)
		sw $t0, 4($sp) # Storing i
		
		# Argument internal_47
		lw $t0, 28($sp)
		sw $t0, 0($sp) # Storing internal_47
		
		# Calling function function_equal
		jal function_equal
		lw $ra, 8($sp)
		sw $v1, 24($sp) # internal_48 = result of function_equal
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# internal_46 = internal_48
		lw $t0, 12($sp)
		sw $t0, 20($sp)
		
		# If internal_46 then goto then_8781702324661
		lw $t0, 20($sp) # Loading the address of the condition
		lw $t0, 8($t0) # Loading the value of the condition
		addi $t1, $zero, 1 # Setting the value to 1 for comparison
		beq $t0, $t1, then_8781702324661
		
		# Jumping to else_8781702324661
		j else_8781702324661
		
		then_8781702324661:
		
		# Allocating String
		li $v0, 9
		addi $a0, $zero, 10 # $a0 = length of string + 9 for 4 bytes for the type, 4 bytes for the length of the string and 1 byte for null-terminator
		syscall
		
		la $t0, type_String
		sw $t0, 0($v0) # Setting type in the first word of the object
		
		addi $t0, $zero, 10
		sw $t0, 4($v0) # Setting length of the string in the second word of the object
		
		addi $t0, $zero, 57
		sb $t0, 8($v0) # internal_49[0] = '9'
		
		sb $zero, 9($v0) # Null-terminator at the end of the string
		
		sw $v0, 8($sp) # internal_49 = "9"
		
		# internal_45 = internal_49
		lw $t0, 8($sp)
		sw $t0, 24($sp)
		
		# Jumping to endif_8781702324661
		j endif_8781702324661
		
		else_8781702324661:
		
		# Passing function arguments
		addi $sp, $sp, -8 # Reserving space for arguments
		sw $ra, 4($sp) # Storing return address
		
		# Argument self
		lw $t0, 220($sp)
		sw $t0, 0($sp) # Storing self
		
		# Calling function function_abort_at_Object
		jal function_abort_at_Object
		lw $ra, 4($sp)
		sw $v1, 12($sp) # internal_50 = result of function_abort_at_Object
		addi $sp, $sp, 8 # Freeing space for arguments
		
		# Allocating String
		li $v0, 9
		addi $a0, $zero, 9 # $a0 = length of string + 9 for 4 bytes for the type, 4 bytes for the length of the string and 1 byte for null-terminator
		syscall
		
		la $t0, type_String
		sw $t0, 0($v0) # Setting type in the first word of the object
		
		addi $t0, $zero, 9
		sw $t0, 4($v0) # Setting length of the string in the second word of the object
		
		sb $zero, 8($v0) # Null-terminator at the end of the string
		
		sw $v0, 0($sp) # internal_51 = ""
		
		# internal_45 = internal_51
		lw $t0, 0($sp)
		sw $t0, 24($sp)
		
		# Jumping to endif_8781702324661
		j endif_8781702324661
		
		endif_8781702324661:
		
		# internal_40 = internal_45
		lw $t0, 24($sp)
		sw $t0, 44($sp)
		
		# Jumping to endif_8781702324682
		j endif_8781702324682
		
		endif_8781702324682:
		
		# internal_35 = internal_40
		lw $t0, 44($sp)
		sw $t0, 64($sp)
		
		# Jumping to endif_8781702324688
		j endif_8781702324688
		
		endif_8781702324688:
		
		# internal_30 = internal_35
		lw $t0, 64($sp)
		sw $t0, 84($sp)
		
		# Jumping to endif_8781702324694
		j endif_8781702324694
		
		endif_8781702324694:
		
		# internal_25 = internal_30
		lw $t0, 84($sp)
		sw $t0, 104($sp)
		
		# Jumping to endif_8781702324700
		j endif_8781702324700
		
		endif_8781702324700:
		
		# internal_20 = internal_25
		lw $t0, 104($sp)
		sw $t0, 124($sp)
		
		# Jumping to endif_8781702324706
		j endif_8781702324706
		
		endif_8781702324706:
		
		# internal_15 = internal_20
		lw $t0, 124($sp)
		sw $t0, 144($sp)
		
		# Jumping to endif_8781702324712
		j endif_8781702324712
		
		endif_8781702324712:
		
		# internal_10 = internal_15
		lw $t0, 144($sp)
		sw $t0, 164($sp)
		
		# Jumping to endif_8781702324718
		j endif_8781702324718
		
		endif_8781702324718:
		
		# internal_5 = internal_10
		lw $t0, 164($sp)
		sw $t0, 184($sp)
		
		# Jumping to endif_8781702324724
		j endif_8781702324724
		
		endif_8781702324724:
		
		# internal_0 = internal_5
		lw $t0, 184($sp)
		sw $t0, 204($sp)
		
		# Jumping to endif_8781702324730
		j endif_8781702324730
		
		endif_8781702324730:
		
		# Loading return value in $v1
		lw $v1, 204($sp)
		
		# Freeing space for local variables
		addi $sp, $sp, 208
		
		jr $ra
		
	function_a2i_at_A2I:
		# Function parameters
		#   $ra = 152($sp)
		#   self = 148($sp)
		#   s = 144($sp)
		
		# Reserving space for local variables
		addi $sp, $sp, -144
		
		# Allocating Bool 0
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Bool # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 0
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 136($sp) # internal_1 = address of allocated object Int
		
		# Passing function arguments
		addi $sp, $sp, -8 # Reserving space for arguments
		sw $ra, 4($sp) # Storing return address
		
		# Argument s
		lw $t0, 152($sp)
		sw $t0, 0($sp) # Storing s
		
		# Calling function function_length_at_String
		jal function_length_at_String
		lw $ra, 4($sp)
		sw $v1, 140($sp) # internal_2 = result of function_length_at_String
		addi $sp, $sp, 8 # Freeing space for arguments
		
		# Allocating Int 0
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Int # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 0
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 128($sp) # internal_3 = address of allocated object Int
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument internal_2
		lw $t0, 144($sp)
		sw $t0, 4($sp) # Storing internal_2
		
		# Argument internal_3
		lw $t0, 140($sp)
		sw $t0, 0($sp) # Storing internal_3
		
		# Calling function function_equal
		jal function_equal
		lw $ra, 8($sp)
		sw $v1, 136($sp) # internal_4 = result of function_equal
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# internal_1 = internal_4
		lw $t0, 124($sp)
		sw $t0, 136($sp)
		
		# If internal_1 then goto then_8781702325176
		lw $t0, 136($sp) # Loading the address of the condition
		lw $t0, 8($t0) # Loading the value of the condition
		addi $t1, $zero, 1 # Setting the value to 1 for comparison
		beq $t0, $t1, then_8781702325176
		
		# Jumping to else_8781702325176
		j else_8781702325176
		
		then_8781702325176:
		
		# Allocating Int 0
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Int # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 0
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 120($sp) # internal_5 = address of allocated object Int
		
		# internal_0 = internal_5
		lw $t0, 120($sp)
		sw $t0, 140($sp)
		
		# Jumping to endif_8781702325176
		j endif_8781702325176
		
		else_8781702325176:
		
		# Allocating Bool 0
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Bool # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 0
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 112($sp) # internal_7 = address of allocated object Int
		
		# Allocating Int 0
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Int # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 0
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 108($sp) # internal_8 = address of allocated object Int
		
		# Allocating Int 1
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Int # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 1
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 104($sp) # internal_9 = address of allocated object Int
		
		# Passing function arguments
		addi $sp, $sp, -16 # Reserving space for arguments
		sw $ra, 12($sp) # Storing return address
		
		# Argument s
		lw $t0, 160($sp)
		sw $t0, 8($sp) # Storing s
		
		# Argument internal_8
		lw $t0, 124($sp)
		sw $t0, 4($sp) # Storing internal_8
		
		# Argument internal_9
		lw $t0, 120($sp)
		sw $t0, 0($sp) # Storing internal_9
		
		# Calling function function_substr_at_String
		jal function_substr_at_String
		lw $ra, 12($sp)
		sw $v1, 116($sp) # internal_10 = result of function_substr_at_String
		addi $sp, $sp, 16 # Freeing space for arguments
		
		# Allocating String
		li $v0, 9
		addi $a0, $zero, 10 # $a0 = length of string + 9 for 4 bytes for the type, 4 bytes for the length of the string and 1 byte for null-terminator
		syscall
		
		la $t0, type_String
		sw $t0, 0($v0) # Setting type in the first word of the object
		
		addi $t0, $zero, 10
		sw $t0, 4($v0) # Setting length of the string in the second word of the object
		
		addi $t0, $zero, 45
		sb $t0, 8($v0) # internal_11[0] = '-'
		
		sb $zero, 9($v0) # Null-terminator at the end of the string
		
		sw $v0, 96($sp) # internal_11 = "-"
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument internal_10
		lw $t0, 112($sp)
		sw $t0, 4($sp) # Storing internal_10
		
		# Argument internal_11
		lw $t0, 108($sp)
		sw $t0, 0($sp) # Storing internal_11
		
		# Calling function function_equal
		jal function_equal
		lw $ra, 8($sp)
		sw $v1, 104($sp) # internal_12 = result of function_equal
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# internal_7 = internal_12
		lw $t0, 92($sp)
		sw $t0, 112($sp)
		
		# If internal_7 then goto then_8781702325191
		lw $t0, 112($sp) # Loading the address of the condition
		lw $t0, 8($t0) # Loading the value of the condition
		addi $t1, $zero, 1 # Setting the value to 1 for comparison
		beq $t0, $t1, then_8781702325191
		
		# Jumping to else_8781702325191
		j else_8781702325191
		
		then_8781702325191:
		
		# Allocating Int 1
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Int # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 1
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 88($sp) # internal_13 = address of allocated object Int
		
		# Passing function arguments
		addi $sp, $sp, -8 # Reserving space for arguments
		sw $ra, 4($sp) # Storing return address
		
		# Argument s
		lw $t0, 152($sp)
		sw $t0, 0($sp) # Storing s
		
		# Calling function function_length_at_String
		jal function_length_at_String
		lw $ra, 4($sp)
		sw $v1, 92($sp) # internal_14 = result of function_length_at_String
		addi $sp, $sp, 8 # Freeing space for arguments
		
		# Allocating Int 1
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Int # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 1
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 80($sp) # internal_15 = address of allocated object Int
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument internal_14
		lw $t0, 96($sp)
		sw $t0, 4($sp) # Storing internal_14
		
		# Argument internal_15
		lw $t0, 92($sp)
		sw $t0, 0($sp) # Storing internal_15
		
		# Calling function function_sub
		jal function_sub
		lw $ra, 8($sp)
		sw $v1, 88($sp) # internal_16 = result of function_sub
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# Passing function arguments
		addi $sp, $sp, -16 # Reserving space for arguments
		sw $ra, 12($sp) # Storing return address
		
		# Argument s
		lw $t0, 160($sp)
		sw $t0, 8($sp) # Storing s
		
		# Argument internal_13
		lw $t0, 104($sp)
		sw $t0, 4($sp) # Storing internal_13
		
		# Argument internal_16
		lw $t0, 92($sp)
		sw $t0, 0($sp) # Storing internal_16
		
		# Calling function function_substr_at_String
		jal function_substr_at_String
		lw $ra, 12($sp)
		sw $v1, 88($sp) # internal_17 = result of function_substr_at_String
		addi $sp, $sp, 16 # Freeing space for arguments
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument self
		lw $t0, 160($sp)
		sw $t0, 4($sp) # Storing self
		
		# Argument internal_17
		lw $t0, 84($sp)
		sw $t0, 0($sp) # Storing internal_17
		
		# Calling function function_a2i_aux_at_A2I
		jal function_a2i_aux_at_A2I
		lw $ra, 8($sp)
		sw $v1, 80($sp) # internal_18 = result of function_a2i_aux_at_A2I
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# Allocating Int 1
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Int # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 1
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 64($sp) # internal_19 = address of allocated object Int
		
		# Allocating Int 4294967295
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Int # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 4294967295
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 60($sp) # internal_20 = address of allocated object Int
		
		# Allocating Int 0
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Int # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 0
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 56($sp) # internal_21 = address of allocated object Int
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument internal_18
		lw $t0, 80($sp)
		sw $t0, 4($sp) # Storing internal_18
		
		# Argument internal_20
		lw $t0, 72($sp)
		sw $t0, 0($sp) # Storing internal_20
		
		# Calling function function_xor
		jal function_xor
		lw $ra, 8($sp)
		sw $v1, 68($sp) # internal_21 = result of function_xor
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument internal_21
		lw $t0, 68($sp)
		sw $t0, 4($sp) # Storing internal_21
		
		# Argument internal_19
		lw $t0, 76($sp)
		sw $t0, 0($sp) # Storing internal_19
		
		# Calling function function_add
		jal function_add
		lw $ra, 8($sp)
		sw $v1, 68($sp) # internal_21 = result of function_add
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# internal_6 = internal_21
		lw $t0, 56($sp)
		sw $t0, 116($sp)
		
		# Jumping to endif_8781702325191
		j endif_8781702325191
		
		else_8781702325191:
		
		# Allocating Bool 0
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Bool # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 0
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 48($sp) # internal_23 = address of allocated object Int
		
		# Allocating Int 0
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Int # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 0
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 44($sp) # internal_24 = address of allocated object Int
		
		# Allocating Int 1
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Int # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 1
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 40($sp) # internal_25 = address of allocated object Int
		
		# Passing function arguments
		addi $sp, $sp, -16 # Reserving space for arguments
		sw $ra, 12($sp) # Storing return address
		
		# Argument s
		lw $t0, 160($sp)
		sw $t0, 8($sp) # Storing s
		
		# Argument internal_24
		lw $t0, 60($sp)
		sw $t0, 4($sp) # Storing internal_24
		
		# Argument internal_25
		lw $t0, 56($sp)
		sw $t0, 0($sp) # Storing internal_25
		
		# Calling function function_substr_at_String
		jal function_substr_at_String
		lw $ra, 12($sp)
		sw $v1, 52($sp) # internal_26 = result of function_substr_at_String
		addi $sp, $sp, 16 # Freeing space for arguments
		
		# Allocating String
		li $v0, 9
		addi $a0, $zero, 10 # $a0 = length of string + 9 for 4 bytes for the type, 4 bytes for the length of the string and 1 byte for null-terminator
		syscall
		
		la $t0, type_String
		sw $t0, 0($v0) # Setting type in the first word of the object
		
		addi $t0, $zero, 10
		sw $t0, 4($v0) # Setting length of the string in the second word of the object
		
		addi $t0, $zero, 43
		sb $t0, 8($v0) # internal_27[0] = '+'
		
		sb $zero, 9($v0) # Null-terminator at the end of the string
		
		sw $v0, 32($sp) # internal_27 = "+"
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument internal_26
		lw $t0, 48($sp)
		sw $t0, 4($sp) # Storing internal_26
		
		# Argument internal_27
		lw $t0, 44($sp)
		sw $t0, 0($sp) # Storing internal_27
		
		# Calling function function_equal
		jal function_equal
		lw $ra, 8($sp)
		sw $v1, 40($sp) # internal_28 = result of function_equal
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# internal_23 = internal_28
		lw $t0, 28($sp)
		sw $t0, 48($sp)
		
		# If internal_23 then goto then_8781702325185
		lw $t0, 48($sp) # Loading the address of the condition
		lw $t0, 8($t0) # Loading the value of the condition
		addi $t1, $zero, 1 # Setting the value to 1 for comparison
		beq $t0, $t1, then_8781702325185
		
		# Jumping to else_8781702325185
		j else_8781702325185
		
		then_8781702325185:
		
		# Allocating Int 1
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Int # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 1
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 24($sp) # internal_29 = address of allocated object Int
		
		# Passing function arguments
		addi $sp, $sp, -8 # Reserving space for arguments
		sw $ra, 4($sp) # Storing return address
		
		# Argument s
		lw $t0, 152($sp)
		sw $t0, 0($sp) # Storing s
		
		# Calling function function_length_at_String
		jal function_length_at_String
		lw $ra, 4($sp)
		sw $v1, 28($sp) # internal_30 = result of function_length_at_String
		addi $sp, $sp, 8 # Freeing space for arguments
		
		# Allocating Int 1
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Int # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 1
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 16($sp) # internal_31 = address of allocated object Int
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument internal_30
		lw $t0, 32($sp)
		sw $t0, 4($sp) # Storing internal_30
		
		# Argument internal_31
		lw $t0, 28($sp)
		sw $t0, 0($sp) # Storing internal_31
		
		# Calling function function_sub
		jal function_sub
		lw $ra, 8($sp)
		sw $v1, 24($sp) # internal_32 = result of function_sub
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# Passing function arguments
		addi $sp, $sp, -16 # Reserving space for arguments
		sw $ra, 12($sp) # Storing return address
		
		# Argument s
		lw $t0, 160($sp)
		sw $t0, 8($sp) # Storing s
		
		# Argument internal_29
		lw $t0, 40($sp)
		sw $t0, 4($sp) # Storing internal_29
		
		# Argument internal_32
		lw $t0, 28($sp)
		sw $t0, 0($sp) # Storing internal_32
		
		# Calling function function_substr_at_String
		jal function_substr_at_String
		lw $ra, 12($sp)
		sw $v1, 24($sp) # internal_33 = result of function_substr_at_String
		addi $sp, $sp, 16 # Freeing space for arguments
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument self
		lw $t0, 160($sp)
		sw $t0, 4($sp) # Storing self
		
		# Argument internal_33
		lw $t0, 20($sp)
		sw $t0, 0($sp) # Storing internal_33
		
		# Calling function function_a2i_aux_at_A2I
		jal function_a2i_aux_at_A2I
		lw $ra, 8($sp)
		sw $v1, 16($sp) # internal_34 = result of function_a2i_aux_at_A2I
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# internal_22 = internal_34
		lw $t0, 4($sp)
		sw $t0, 52($sp)
		
		# Jumping to endif_8781702325185
		j endif_8781702325185
		
		else_8781702325185:
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument self
		lw $t0, 160($sp)
		sw $t0, 4($sp) # Storing self
		
		# Argument s
		lw $t0, 156($sp)
		sw $t0, 0($sp) # Storing s
		
		# Calling function function_a2i_aux_at_A2I
		jal function_a2i_aux_at_A2I
		lw $ra, 8($sp)
		sw $v1, 12($sp) # internal_35 = result of function_a2i_aux_at_A2I
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# internal_22 = internal_35
		lw $t0, 0($sp)
		sw $t0, 52($sp)
		
		# Jumping to endif_8781702325185
		j endif_8781702325185
		
		endif_8781702325185:
		
		# internal_6 = internal_22
		lw $t0, 52($sp)
		sw $t0, 116($sp)
		
		# Jumping to endif_8781702325191
		j endif_8781702325191
		
		endif_8781702325191:
		
		# internal_0 = internal_6
		lw $t0, 116($sp)
		sw $t0, 140($sp)
		
		# Jumping to endif_8781702325176
		j endif_8781702325176
		
		endif_8781702325176:
		
		# Loading return value in $v1
		lw $v1, 140($sp)
		
		# Freeing space for local variables
		addi $sp, $sp, 144
		
		jr $ra
		
	function_a2i_aux_at_A2I:
		# Function parameters
		#   $ra = 68($sp)
		#   self = 64($sp)
		#   s = 60($sp)
		
		# Reserving space for local variables
		addi $sp, $sp, -60
		
		# Allocating Int 0
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Int # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 0
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 52($sp) # internal_1 = address of allocated object Int
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument int
		lw $t0, 68($sp)
		sw $t0, 4($sp) # Storing int
		
		# Argument internal_1
		lw $t0, 64($sp)
		sw $t0, 0($sp) # Storing internal_1
		
		# Calling function function_assign
		jal function_assign
		lw $ra, 8($sp)
		sw $v1, 68($sp) # int = result of function_assign
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# Passing function arguments
		addi $sp, $sp, -8 # Reserving space for arguments
		sw $ra, 4($sp) # Storing return address
		
		# Argument s
		lw $t0, 68($sp)
		sw $t0, 0($sp) # Storing s
		
		# Calling function function_length_at_String
		jal function_length_at_String
		lw $ra, 4($sp)
		sw $v1, 52($sp) # internal_3 = result of function_length_at_String
		addi $sp, $sp, 8 # Freeing space for arguments
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument j
		lw $t0, 60($sp)
		sw $t0, 4($sp) # Storing j
		
		# Argument internal_3
		lw $t0, 56($sp)
		sw $t0, 0($sp) # Storing internal_3
		
		# Calling function function_assign
		jal function_assign
		lw $ra, 8($sp)
		sw $v1, 60($sp) # j = result of function_assign
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# Allocating Int 0
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Int # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 0
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 36($sp) # internal_5 = address of allocated object Int
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument i
		lw $t0, 52($sp)
		sw $t0, 4($sp) # Storing i
		
		# Argument internal_5
		lw $t0, 48($sp)
		sw $t0, 0($sp) # Storing internal_5
		
		# Calling function function_assign
		jal function_assign
		lw $ra, 8($sp)
		sw $v1, 52($sp) # i = result of function_assign
		addi $sp, $sp, 12 # Freeing space for arguments
		
		while_start_8781702325589:
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument i
		lw $t0, 52($sp)
		sw $t0, 4($sp) # Storing i
		
		# Argument j
		lw $t0, 60($sp)
		sw $t0, 0($sp) # Storing j
		
		# Calling function function_less_than
		jal function_less_than
		lw $ra, 8($sp)
		sw $v1, 44($sp) # internal_6 = result of function_less_than
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# If internal_6 then goto while_body_8781702325589
		lw $t0, 32($sp) # Loading the address of the condition
		lw $t0, 8($t0) # Loading the value of the condition
		addi $t1, $zero, 1 # Setting the value to 1 for comparison
		beq $t0, $t1, while_body_8781702325589
		
		# Jumping to while_end_8781702325589
		j while_end_8781702325589
		
		while_body_8781702325589:
		
		# Allocating Int 10
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Int # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 10
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 28($sp) # internal_7 = address of allocated object Int
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument int
		lw $t0, 68($sp)
		sw $t0, 4($sp) # Storing int
		
		# Argument internal_7
		lw $t0, 40($sp)
		sw $t0, 0($sp) # Storing internal_7
		
		# Calling function function_mult
		jal function_mult
		lw $ra, 8($sp)
		sw $v1, 36($sp) # internal_8 = result of function_mult
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# Allocating Int 1
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Int # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 1
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 20($sp) # internal_9 = address of allocated object Int
		
		# Passing function arguments
		addi $sp, $sp, -16 # Reserving space for arguments
		sw $ra, 12($sp) # Storing return address
		
		# Argument s
		lw $t0, 76($sp)
		sw $t0, 8($sp) # Storing s
		
		# Argument i
		lw $t0, 56($sp)
		sw $t0, 4($sp) # Storing i
		
		# Argument internal_9
		lw $t0, 36($sp)
		sw $t0, 0($sp) # Storing internal_9
		
		# Calling function function_substr_at_String
		jal function_substr_at_String
		lw $ra, 12($sp)
		sw $v1, 32($sp) # internal_10 = result of function_substr_at_String
		addi $sp, $sp, 16 # Freeing space for arguments
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument self
		lw $t0, 76($sp)
		sw $t0, 4($sp) # Storing self
		
		# Argument internal_10
		lw $t0, 28($sp)
		sw $t0, 0($sp) # Storing internal_10
		
		# Calling function function_c2i_at_A2I
		jal function_c2i_at_A2I
		lw $ra, 8($sp)
		sw $v1, 24($sp) # internal_11 = result of function_c2i_at_A2I
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument internal_8
		lw $t0, 36($sp)
		sw $t0, 4($sp) # Storing internal_8
		
		# Argument internal_11
		lw $t0, 24($sp)
		sw $t0, 0($sp) # Storing internal_11
		
		# Calling function function_add
		jal function_add
		lw $ra, 8($sp)
		sw $v1, 20($sp) # internal_12 = result of function_add
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument int
		lw $t0, 68($sp)
		sw $t0, 4($sp) # Storing int
		
		# Argument internal_12
		lw $t0, 20($sp)
		sw $t0, 0($sp) # Storing internal_12
		
		# Calling function function_assign
		jal function_assign
		lw $ra, 8($sp)
		sw $v1, 68($sp) # int = result of function_assign
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# Allocating Int 1
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Int # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 1
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 4($sp) # internal_13 = address of allocated object Int
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument i
		lw $t0, 52($sp)
		sw $t0, 4($sp) # Storing i
		
		# Argument internal_13
		lw $t0, 16($sp)
		sw $t0, 0($sp) # Storing internal_13
		
		# Calling function function_add
		jal function_add
		lw $ra, 8($sp)
		sw $v1, 12($sp) # internal_14 = result of function_add
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument i
		lw $t0, 52($sp)
		sw $t0, 4($sp) # Storing i
		
		# Argument internal_14
		lw $t0, 12($sp)
		sw $t0, 0($sp) # Storing internal_14
		
		# Calling function function_assign
		jal function_assign
		lw $ra, 8($sp)
		sw $v1, 52($sp) # i = result of function_assign
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# Jumping to while_start_8781702325589
		j while_start_8781702325589
		
		while_end_8781702325589:
		
		# Loading return value in $v1
		lw $v1, 56($sp)
		
		# Freeing space for local variables
		addi $sp, $sp, 60
		
		jr $ra
		
	function_i2a_at_A2I:
		# Function parameters
		#   $ra = 80($sp)
		#   self = 76($sp)
		#   i = 72($sp)
		
		# Reserving space for local variables
		addi $sp, $sp, -72
		
		# Allocating Bool 0
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Bool # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 0
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 64($sp) # internal_1 = address of allocated object Int
		
		# Allocating Int 0
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Int # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 0
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 60($sp) # internal_2 = address of allocated object Int
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument i
		lw $t0, 84($sp)
		sw $t0, 4($sp) # Storing i
		
		# Argument internal_2
		lw $t0, 72($sp)
		sw $t0, 0($sp) # Storing internal_2
		
		# Calling function function_equal
		jal function_equal
		lw $ra, 8($sp)
		sw $v1, 68($sp) # internal_3 = result of function_equal
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# internal_1 = internal_3
		lw $t0, 56($sp)
		sw $t0, 64($sp)
		
		# If internal_1 then goto then_8781702325718
		lw $t0, 64($sp) # Loading the address of the condition
		lw $t0, 8($t0) # Loading the value of the condition
		addi $t1, $zero, 1 # Setting the value to 1 for comparison
		beq $t0, $t1, then_8781702325718
		
		# Jumping to else_8781702325718
		j else_8781702325718
		
		then_8781702325718:
		
		# Allocating String
		li $v0, 9
		addi $a0, $zero, 10 # $a0 = length of string + 9 for 4 bytes for the type, 4 bytes for the length of the string and 1 byte for null-terminator
		syscall
		
		la $t0, type_String
		sw $t0, 0($v0) # Setting type in the first word of the object
		
		addi $t0, $zero, 10
		sw $t0, 4($v0) # Setting length of the string in the second word of the object
		
		addi $t0, $zero, 48
		sb $t0, 8($v0) # internal_4[0] = '0'
		
		sb $zero, 9($v0) # Null-terminator at the end of the string
		
		sw $v0, 52($sp) # internal_4 = "0"
		
		# internal_0 = internal_4
		lw $t0, 52($sp)
		sw $t0, 68($sp)
		
		# Jumping to endif_8781702325718
		j endif_8781702325718
		
		else_8781702325718:
		
		# Allocating Bool 0
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Bool # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 0
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 44($sp) # internal_6 = address of allocated object Int
		
		# Allocating Int 0
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Int # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 0
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 40($sp) # internal_7 = address of allocated object Int
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument internal_7
		lw $t0, 52($sp)
		sw $t0, 4($sp) # Storing internal_7
		
		# Argument i
		lw $t0, 84($sp)
		sw $t0, 0($sp) # Storing i
		
		# Calling function function_less_than
		jal function_less_than
		lw $ra, 8($sp)
		sw $v1, 48($sp) # internal_8 = result of function_less_than
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# internal_6 = internal_8
		lw $t0, 36($sp)
		sw $t0, 44($sp)
		
		# If internal_6 then goto then_8781702325724
		lw $t0, 44($sp) # Loading the address of the condition
		lw $t0, 8($t0) # Loading the value of the condition
		addi $t1, $zero, 1 # Setting the value to 1 for comparison
		beq $t0, $t1, then_8781702325724
		
		# Jumping to else_8781702325724
		j else_8781702325724
		
		then_8781702325724:
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument self
		lw $t0, 88($sp)
		sw $t0, 4($sp) # Storing self
		
		# Argument i
		lw $t0, 84($sp)
		sw $t0, 0($sp) # Storing i
		
		# Calling function function_i2a_aux_at_A2I
		jal function_i2a_aux_at_A2I
		lw $ra, 8($sp)
		sw $v1, 44($sp) # internal_9 = result of function_i2a_aux_at_A2I
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# internal_5 = internal_9
		lw $t0, 32($sp)
		sw $t0, 48($sp)
		
		# Jumping to endif_8781702325724
		j endif_8781702325724
		
		else_8781702325724:
		
		# Allocating String
		li $v0, 9
		addi $a0, $zero, 10 # $a0 = length of string + 9 for 4 bytes for the type, 4 bytes for the length of the string and 1 byte for null-terminator
		syscall
		
		la $t0, type_String
		sw $t0, 0($v0) # Setting type in the first word of the object
		
		addi $t0, $zero, 10
		sw $t0, 4($v0) # Setting length of the string in the second word of the object
		
		addi $t0, $zero, 45
		sb $t0, 8($v0) # internal_10[0] = '-'
		
		sb $zero, 9($v0) # Null-terminator at the end of the string
		
		sw $v0, 28($sp) # internal_10 = "-"
		
		# Allocating Int 1
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Int # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 1
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 24($sp) # internal_11 = address of allocated object Int
		
		# Allocating Int 1
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Int # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 1
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 20($sp) # internal_12 = address of allocated object Int
		
		# Allocating Int 4294967295
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Int # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 4294967295
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 16($sp) # internal_13 = address of allocated object Int
		
		# Allocating Int 0
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Int # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 0
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 12($sp) # internal_14 = address of allocated object Int
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument internal_11
		lw $t0, 36($sp)
		sw $t0, 4($sp) # Storing internal_11
		
		# Argument internal_13
		lw $t0, 28($sp)
		sw $t0, 0($sp) # Storing internal_13
		
		# Calling function function_xor
		jal function_xor
		lw $ra, 8($sp)
		sw $v1, 24($sp) # internal_14 = result of function_xor
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument internal_14
		lw $t0, 24($sp)
		sw $t0, 4($sp) # Storing internal_14
		
		# Argument internal_12
		lw $t0, 32($sp)
		sw $t0, 0($sp) # Storing internal_12
		
		# Calling function function_add
		jal function_add
		lw $ra, 8($sp)
		sw $v1, 24($sp) # internal_14 = result of function_add
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument i
		lw $t0, 84($sp)
		sw $t0, 4($sp) # Storing i
		
		# Argument internal_14
		lw $t0, 24($sp)
		sw $t0, 0($sp) # Storing internal_14
		
		# Calling function function_mult
		jal function_mult
		lw $ra, 8($sp)
		sw $v1, 20($sp) # internal_15 = result of function_mult
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument self
		lw $t0, 88($sp)
		sw $t0, 4($sp) # Storing self
		
		# Argument internal_15
		lw $t0, 20($sp)
		sw $t0, 0($sp) # Storing internal_15
		
		# Calling function function_i2a_aux_at_A2I
		jal function_i2a_aux_at_A2I
		lw $ra, 8($sp)
		sw $v1, 16($sp) # internal_16 = result of function_i2a_aux_at_A2I
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument internal_10
		lw $t0, 40($sp)
		sw $t0, 4($sp) # Storing internal_10
		
		# Argument internal_16
		lw $t0, 16($sp)
		sw $t0, 0($sp) # Storing internal_16
		
		# Calling function function_concat_at_String
		jal function_concat_at_String
		lw $ra, 8($sp)
		sw $v1, 12($sp) # internal_17 = result of function_concat_at_String
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# internal_5 = internal_17
		lw $t0, 0($sp)
		sw $t0, 48($sp)
		
		# Jumping to endif_8781702325724
		j endif_8781702325724
		
		endif_8781702325724:
		
		# internal_0 = internal_5
		lw $t0, 48($sp)
		sw $t0, 68($sp)
		
		# Jumping to endif_8781702325718
		j endif_8781702325718
		
		endif_8781702325718:
		
		# Loading return value in $v1
		lw $v1, 68($sp)
		
		# Freeing space for local variables
		addi $sp, $sp, 72
		
		jr $ra
		
	function_i2a_aux_at_A2I:
		# Function parameters
		#   $ra = 64($sp)
		#   self = 60($sp)
		#   i = 56($sp)
		
		# Reserving space for local variables
		addi $sp, $sp, -56
		
		# Allocating Bool 0
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Bool # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 0
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 48($sp) # internal_1 = address of allocated object Int
		
		# Allocating Int 0
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Int # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 0
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 44($sp) # internal_2 = address of allocated object Int
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument i
		lw $t0, 68($sp)
		sw $t0, 4($sp) # Storing i
		
		# Argument internal_2
		lw $t0, 56($sp)
		sw $t0, 0($sp) # Storing internal_2
		
		# Calling function function_equal
		jal function_equal
		lw $ra, 8($sp)
		sw $v1, 52($sp) # internal_3 = result of function_equal
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# internal_1 = internal_3
		lw $t0, 40($sp)
		sw $t0, 48($sp)
		
		# If internal_1 then goto then_8781702326348
		lw $t0, 48($sp) # Loading the address of the condition
		lw $t0, 8($t0) # Loading the value of the condition
		addi $t1, $zero, 1 # Setting the value to 1 for comparison
		beq $t0, $t1, then_8781702326348
		
		# Jumping to else_8781702326348
		j else_8781702326348
		
		then_8781702326348:
		
		# Allocating String
		li $v0, 9
		addi $a0, $zero, 9 # $a0 = length of string + 9 for 4 bytes for the type, 4 bytes for the length of the string and 1 byte for null-terminator
		syscall
		
		la $t0, type_String
		sw $t0, 0($v0) # Setting type in the first word of the object
		
		addi $t0, $zero, 9
		sw $t0, 4($v0) # Setting length of the string in the second word of the object
		
		sb $zero, 8($v0) # Null-terminator at the end of the string
		
		sw $v0, 36($sp) # internal_4 = ""
		
		# internal_0 = internal_4
		lw $t0, 36($sp)
		sw $t0, 52($sp)
		
		# Jumping to endif_8781702326348
		j endif_8781702326348
		
		else_8781702326348:
		
		# Allocating Int 10
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Int # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 10
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 28($sp) # internal_6 = address of allocated object Int
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument i
		lw $t0, 68($sp)
		sw $t0, 4($sp) # Storing i
		
		# Argument internal_6
		lw $t0, 40($sp)
		sw $t0, 0($sp) # Storing internal_6
		
		# Calling function function_div
		jal function_div
		lw $ra, 8($sp)
		sw $v1, 36($sp) # internal_7 = result of function_div
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument next
		lw $t0, 44($sp)
		sw $t0, 4($sp) # Storing next
		
		# Argument internal_7
		lw $t0, 36($sp)
		sw $t0, 0($sp) # Storing internal_7
		
		# Calling function function_assign
		jal function_assign
		lw $ra, 8($sp)
		sw $v1, 44($sp) # next = result of function_assign
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument self
		lw $t0, 72($sp)
		sw $t0, 4($sp) # Storing self
		
		# Argument next
		lw $t0, 44($sp)
		sw $t0, 0($sp) # Storing next
		
		# Calling function function_i2a_aux_at_A2I
		jal function_i2a_aux_at_A2I
		lw $ra, 8($sp)
		sw $v1, 32($sp) # internal_8 = result of function_i2a_aux_at_A2I
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# Allocating Int 10
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Int # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 10
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 16($sp) # internal_9 = address of allocated object Int
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument next
		lw $t0, 44($sp)
		sw $t0, 4($sp) # Storing next
		
		# Argument internal_9
		lw $t0, 28($sp)
		sw $t0, 0($sp) # Storing internal_9
		
		# Calling function function_mult
		jal function_mult
		lw $ra, 8($sp)
		sw $v1, 24($sp) # internal_10 = result of function_mult
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument i
		lw $t0, 68($sp)
		sw $t0, 4($sp) # Storing i
		
		# Argument internal_10
		lw $t0, 24($sp)
		sw $t0, 0($sp) # Storing internal_10
		
		# Calling function function_sub
		jal function_sub
		lw $ra, 8($sp)
		sw $v1, 20($sp) # internal_11 = result of function_sub
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument self
		lw $t0, 72($sp)
		sw $t0, 4($sp) # Storing self
		
		# Argument internal_11
		lw $t0, 20($sp)
		sw $t0, 0($sp) # Storing internal_11
		
		# Calling function function_i2c_at_A2I
		jal function_i2c_at_A2I
		lw $ra, 8($sp)
		sw $v1, 16($sp) # internal_12 = result of function_i2c_at_A2I
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument internal_8
		lw $t0, 32($sp)
		sw $t0, 4($sp) # Storing internal_8
		
		# Argument internal_12
		lw $t0, 16($sp)
		sw $t0, 0($sp) # Storing internal_12
		
		# Calling function function_concat_at_String
		jal function_concat_at_String
		lw $ra, 8($sp)
		sw $v1, 12($sp) # internal_13 = result of function_concat_at_String
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# internal_0 = internal_13
		lw $t0, 0($sp)
		sw $t0, 52($sp)
		
		# Jumping to endif_8781702326348
		j endif_8781702326348
		
		endif_8781702326348:
		
		# Loading return value in $v1
		lw $v1, 52($sp)
		
		# Freeing space for local variables
		addi $sp, $sp, 56
		
		jr $ra
		
	function___init___at_Main:
		# Function parameters
		#   $ra = 20($sp)
		#   self = 16($sp)
		
		# Reserving space for local variables
		addi $sp, $sp, -16
		
		# Allocating String
		li $v0, 9
		addi $a0, $zero, 9 # $a0 = length of string + 9 for 4 bytes for the type, 4 bytes for the length of the string and 1 byte for null-terminator
		syscall
		
		la $t0, type_String
		sw $t0, 0($v0) # Setting type in the first word of the object
		
		addi $t0, $zero, 9
		sw $t0, 4($v0) # Setting length of the string in the second word of the object
		
		sb $zero, 8($v0) # Null-terminator at the end of the string
		
		sw $v0, 12($sp) # internal_0 = ""
		
		# Set attribute char of self
		lw $t0, 16($sp) # $t0 = self
		lw $t1, 12($sp) # $t1 = internal_0
		beq $t1, $zero, object_set_attribute_8781702246202
		lw $t2, 0($t1)
		la $t3, type_Int
		la $t4, type_Bool
		addi $t5, $zero, 1
		seq $t6, $t2, $t3
		beq $t6, $t5, int_set_attribute_8781702246202
		seq $t6, $t2, $t4
		beq $t6, $t5, bool_set_attribute_8781702246202
		j object_set_attribute_8781702246202
		int_set_attribute_8781702246202:
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		sw $t3, 0($v0)
		sw $a0, 4($v0)
		lw $t5, 8($t1)
		sw $t5, 8($v0)
		sw $v0, 8($t0) # self.char = internal_0
		j end_set_attribute_8781702246202
		bool_set_attribute_8781702246202:
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		sw $t4, 0($v0)
		sw $a0, 4($v0)
		lw $t5, 8($t1)
		sw $t5, 8($v0)
		sw $v0, 8($t0) # self.char = internal_0
		j end_set_attribute_8781702246202
		object_set_attribute_8781702246202:
		sw $t1, 8($t0) # self.char = internal_0
		end_set_attribute_8781702246202:
		
		# Allocating NUll to internal_1
		sw $zero, 8($sp) # internal_1 = 0
		
		# Set attribute avar of self
		lw $t0, 16($sp) # $t0 = self
		lw $t1, 8($sp) # $t1 = internal_1
		beq $t1, $zero, object_set_attribute_8781702246223
		lw $t2, 0($t1)
		la $t3, type_Int
		la $t4, type_Bool
		addi $t5, $zero, 1
		seq $t6, $t2, $t3
		beq $t6, $t5, int_set_attribute_8781702246223
		seq $t6, $t2, $t4
		beq $t6, $t5, bool_set_attribute_8781702246223
		j object_set_attribute_8781702246223
		int_set_attribute_8781702246223:
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		sw $t3, 0($v0)
		sw $a0, 4($v0)
		lw $t5, 8($t1)
		sw $t5, 8($v0)
		sw $v0, 12($t0) # self.avar = internal_1
		j end_set_attribute_8781702246223
		bool_set_attribute_8781702246223:
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		sw $t4, 0($v0)
		sw $a0, 4($v0)
		lw $t5, 8($t1)
		sw $t5, 8($v0)
		sw $v0, 12($t0) # self.avar = internal_1
		j end_set_attribute_8781702246223
		object_set_attribute_8781702246223:
		sw $t1, 12($t0) # self.avar = internal_1
		end_set_attribute_8781702246223:
		
		# Allocating NUll to internal_2
		sw $zero, 4($sp) # internal_2 = 0
		
		# Set attribute a_var of self
		lw $t0, 16($sp) # $t0 = self
		lw $t1, 4($sp) # $t1 = internal_2
		beq $t1, $zero, object_set_attribute_8781702246244
		lw $t2, 0($t1)
		la $t3, type_Int
		la $t4, type_Bool
		addi $t5, $zero, 1
		seq $t6, $t2, $t3
		beq $t6, $t5, int_set_attribute_8781702246244
		seq $t6, $t2, $t4
		beq $t6, $t5, bool_set_attribute_8781702246244
		j object_set_attribute_8781702246244
		int_set_attribute_8781702246244:
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		sw $t3, 0($v0)
		sw $a0, 4($v0)
		lw $t5, 8($t1)
		sw $t5, 8($v0)
		sw $v0, 16($t0) # self.a_var = internal_2
		j end_set_attribute_8781702246244
		bool_set_attribute_8781702246244:
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		sw $t4, 0($v0)
		sw $a0, 4($v0)
		lw $t5, 8($t1)
		sw $t5, 8($v0)
		sw $v0, 16($t0) # self.a_var = internal_2
		j end_set_attribute_8781702246244
		object_set_attribute_8781702246244:
		sw $t1, 16($t0) # self.a_var = internal_2
		end_set_attribute_8781702246244:
		
		# Allocating Bool 1
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Bool # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 1
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 0($sp) # internal_3 = address of allocated object Int
		
		# Set attribute flag of self
		lw $t0, 16($sp) # $t0 = self
		lw $t1, 0($sp) # $t1 = internal_3
		beq $t1, $zero, object_set_attribute_8781702246265
		lw $t2, 0($t1)
		la $t3, type_Int
		la $t4, type_Bool
		addi $t5, $zero, 1
		seq $t6, $t2, $t3
		beq $t6, $t5, int_set_attribute_8781702246265
		seq $t6, $t2, $t4
		beq $t6, $t5, bool_set_attribute_8781702246265
		j object_set_attribute_8781702246265
		int_set_attribute_8781702246265:
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		sw $t3, 0($v0)
		sw $a0, 4($v0)
		lw $t5, 8($t1)
		sw $t5, 8($v0)
		sw $v0, 20($t0) # self.flag = internal_3
		j end_set_attribute_8781702246265
		bool_set_attribute_8781702246265:
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		sw $t4, 0($v0)
		sw $a0, 4($v0)
		lw $t5, 8($t1)
		sw $t5, 8($v0)
		sw $v0, 20($t0) # self.flag = internal_3
		j end_set_attribute_8781702246265
		object_set_attribute_8781702246265:
		sw $t1, 20($t0) # self.flag = internal_3
		end_set_attribute_8781702246265:
		
		# Loading return value in $v1
		lw $v1, 16($sp)
		
		# Freeing space for local variables
		addi $sp, $sp, 16
		
		jr $ra
		
	function_menu_at_Main:
		# Function parameters
		#   $ra = 216($sp)
		#   self = 212($sp)
		
		# Reserving space for local variables
		addi $sp, $sp, -212
		
		# Allocating String
		li $v0, 9
		addi $a0, $zero, 30 # $a0 = length of string + 9 for 4 bytes for the type, 4 bytes for the length of the string and 1 byte for null-terminator
		syscall
		
		la $t0, type_String
		sw $t0, 0($v0) # Setting type in the first word of the object
		
		addi $t0, $zero, 30
		sw $t0, 4($v0) # Setting length of the string in the second word of the object
		
		addi $t0, $zero, 10
		sb $t0, 8($v0) # internal_0[0] = '\n'
		
		addi $t0, $zero, 9
		sb $t0, 9($v0) # internal_0[1] = '\t'
		
		addi $t0, $zero, 84
		sb $t0, 10($v0) # internal_0[2] = 'T'
		
		addi $t0, $zero, 111
		sb $t0, 11($v0) # internal_0[3] = 'o'
		
		addi $t0, $zero, 32
		sb $t0, 12($v0) # internal_0[4] = ' '
		
		addi $t0, $zero, 97
		sb $t0, 13($v0) # internal_0[5] = 'a'
		
		addi $t0, $zero, 100
		sb $t0, 14($v0) # internal_0[6] = 'd'
		
		addi $t0, $zero, 100
		sb $t0, 15($v0) # internal_0[7] = 'd'
		
		addi $t0, $zero, 32
		sb $t0, 16($v0) # internal_0[8] = ' '
		
		addi $t0, $zero, 97
		sb $t0, 17($v0) # internal_0[9] = 'a'
		
		addi $t0, $zero, 32
		sb $t0, 18($v0) # internal_0[10] = ' '
		
		addi $t0, $zero, 110
		sb $t0, 19($v0) # internal_0[11] = 'n'
		
		addi $t0, $zero, 117
		sb $t0, 20($v0) # internal_0[12] = 'u'
		
		addi $t0, $zero, 109
		sb $t0, 21($v0) # internal_0[13] = 'm'
		
		addi $t0, $zero, 98
		sb $t0, 22($v0) # internal_0[14] = 'b'
		
		addi $t0, $zero, 101
		sb $t0, 23($v0) # internal_0[15] = 'e'
		
		addi $t0, $zero, 114
		sb $t0, 24($v0) # internal_0[16] = 'r'
		
		addi $t0, $zero, 32
		sb $t0, 25($v0) # internal_0[17] = ' '
		
		addi $t0, $zero, 116
		sb $t0, 26($v0) # internal_0[18] = 't'
		
		addi $t0, $zero, 111
		sb $t0, 27($v0) # internal_0[19] = 'o'
		
		addi $t0, $zero, 32
		sb $t0, 28($v0) # internal_0[20] = ' '
		
		sb $zero, 29($v0) # Null-terminator at the end of the string
		
		sw $v0, 208($sp) # internal_0 = "\n\tTo add a number to "
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument self
		lw $t0, 224($sp)
		sw $t0, 4($sp) # Storing self
		
		# Argument internal_0
		lw $t0, 220($sp)
		sw $t0, 0($sp) # Storing internal_0
		
		# Calling function function_out_string_at_IO
		jal function_out_string_at_IO
		lw $ra, 8($sp)
		sw $v1, 216($sp) # internal_1 = result of function_out_string_at_IO
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# Get attribute avar of self
		lw $t0, 212($sp) # Get the address of self
		lw $t1, 12($t0) # Get the attribute 'avar' from the instance
		lw $t2, 0($t1)
		la $t3, type_Int
		la $t4, type_Bool
		addi $t5, $zero, 1
		seq $t6, $t2, $t3
		beq $t6, $t5, int_get_attribute_8781702246355
		seq $t6, $t2, $t4
		beq $t6, $t5, bool_get_attribute_8781702246355
		j object_get_attribute_8781702246355
		int_get_attribute_8781702246355:
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		sw $t3, 0($v0)
		sw $a0, 4($v0)
		lw $t5, 8($t1)
		sw $t5, 8($v0)
		sw $v0, 200($sp) # internal_2 = self.avar
		j end_get_attribute_8781702246355
		bool_get_attribute_8781702246355:
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		sw $t4, 0($v0)
		sw $a0, 4($v0)
		lw $t5, 8($t1)
		sw $t5, 8($v0)
		sw $v0, 200($sp) # internal_2 = self.avar
		j end_get_attribute_8781702246355
		object_get_attribute_8781702246355:
		sw $t1, 200($sp) # internal_2 = avar
		end_get_attribute_8781702246355:
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument self
		lw $t0, 224($sp)
		sw $t0, 4($sp) # Storing self
		
		# Argument internal_2
		lw $t0, 212($sp)
		sw $t0, 0($sp) # Storing internal_2
		
		# Calling function function_print_at_Main
		jal function_print_at_Main
		lw $ra, 8($sp)
		sw $v1, 208($sp) # internal_3 = result of function_print_at_Main
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# Allocating String
		li $v0, 9
		addi $a0, $zero, 21 # $a0 = length of string + 9 for 4 bytes for the type, 4 bytes for the length of the string and 1 byte for null-terminator
		syscall
		
		la $t0, type_String
		sw $t0, 0($v0) # Setting type in the first word of the object
		
		addi $t0, $zero, 21
		sw $t0, 4($v0) # Setting length of the string in the second word of the object
		
		addi $t0, $zero, 46
		sb $t0, 8($v0) # internal_4[0] = '.'
		
		addi $t0, $zero, 46
		sb $t0, 9($v0) # internal_4[1] = '.'
		
		addi $t0, $zero, 46
		sb $t0, 10($v0) # internal_4[2] = '.'
		
		addi $t0, $zero, 101
		sb $t0, 11($v0) # internal_4[3] = 'e'
		
		addi $t0, $zero, 110
		sb $t0, 12($v0) # internal_4[4] = 'n'
		
		addi $t0, $zero, 116
		sb $t0, 13($v0) # internal_4[5] = 't'
		
		addi $t0, $zero, 101
		sb $t0, 14($v0) # internal_4[6] = 'e'
		
		addi $t0, $zero, 114
		sb $t0, 15($v0) # internal_4[7] = 'r'
		
		addi $t0, $zero, 32
		sb $t0, 16($v0) # internal_4[8] = ' '
		
		addi $t0, $zero, 97
		sb $t0, 17($v0) # internal_4[9] = 'a'
		
		addi $t0, $zero, 58
		sb $t0, 18($v0) # internal_4[10] = ':'
		
		addi $t0, $zero, 10
		sb $t0, 19($v0) # internal_4[11] = '\n'
		
		sb $zero, 20($v0) # Null-terminator at the end of the string
		
		sw $v0, 192($sp) # internal_4 = "...enter a:\n"
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument self
		lw $t0, 224($sp)
		sw $t0, 4($sp) # Storing self
		
		# Argument internal_4
		lw $t0, 204($sp)
		sw $t0, 0($sp) # Storing internal_4
		
		# Calling function function_out_string_at_IO
		jal function_out_string_at_IO
		lw $ra, 8($sp)
		sw $v1, 200($sp) # internal_5 = result of function_out_string_at_IO
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# Allocating String
		li $v0, 9
		addi $a0, $zero, 20 # $a0 = length of string + 9 for 4 bytes for the type, 4 bytes for the length of the string and 1 byte for null-terminator
		syscall
		
		la $t0, type_String
		sw $t0, 0($v0) # Setting type in the first word of the object
		
		addi $t0, $zero, 20
		sw $t0, 4($v0) # Setting length of the string in the second word of the object
		
		addi $t0, $zero, 9
		sb $t0, 8($v0) # internal_6[0] = '\t'
		
		addi $t0, $zero, 84
		sb $t0, 9($v0) # internal_6[1] = 'T'
		
		addi $t0, $zero, 111
		sb $t0, 10($v0) # internal_6[2] = 'o'
		
		addi $t0, $zero, 32
		sb $t0, 11($v0) # internal_6[3] = ' '
		
		addi $t0, $zero, 110
		sb $t0, 12($v0) # internal_6[4] = 'n'
		
		addi $t0, $zero, 101
		sb $t0, 13($v0) # internal_6[5] = 'e'
		
		addi $t0, $zero, 103
		sb $t0, 14($v0) # internal_6[6] = 'g'
		
		addi $t0, $zero, 97
		sb $t0, 15($v0) # internal_6[7] = 'a'
		
		addi $t0, $zero, 116
		sb $t0, 16($v0) # internal_6[8] = 't'
		
		addi $t0, $zero, 101
		sb $t0, 17($v0) # internal_6[9] = 'e'
		
		addi $t0, $zero, 32
		sb $t0, 18($v0) # internal_6[10] = ' '
		
		sb $zero, 19($v0) # Null-terminator at the end of the string
		
		sw $v0, 184($sp) # internal_6 = "\tTo negate "
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument self
		lw $t0, 224($sp)
		sw $t0, 4($sp) # Storing self
		
		# Argument internal_6
		lw $t0, 196($sp)
		sw $t0, 0($sp) # Storing internal_6
		
		# Calling function function_out_string_at_IO
		jal function_out_string_at_IO
		lw $ra, 8($sp)
		sw $v1, 192($sp) # internal_7 = result of function_out_string_at_IO
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# Get attribute avar of self
		lw $t0, 212($sp) # Get the address of self
		lw $t1, 12($t0) # Get the attribute 'avar' from the instance
		lw $t2, 0($t1)
		la $t3, type_Int
		la $t4, type_Bool
		addi $t5, $zero, 1
		seq $t6, $t2, $t3
		beq $t6, $t5, int_get_attribute_8781702246979
		seq $t6, $t2, $t4
		beq $t6, $t5, bool_get_attribute_8781702246979
		j object_get_attribute_8781702246979
		int_get_attribute_8781702246979:
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		sw $t3, 0($v0)
		sw $a0, 4($v0)
		lw $t5, 8($t1)
		sw $t5, 8($v0)
		sw $v0, 176($sp) # internal_8 = self.avar
		j end_get_attribute_8781702246979
		bool_get_attribute_8781702246979:
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		sw $t4, 0($v0)
		sw $a0, 4($v0)
		lw $t5, 8($t1)
		sw $t5, 8($v0)
		sw $v0, 176($sp) # internal_8 = self.avar
		j end_get_attribute_8781702246979
		object_get_attribute_8781702246979:
		sw $t1, 176($sp) # internal_8 = avar
		end_get_attribute_8781702246979:
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument self
		lw $t0, 224($sp)
		sw $t0, 4($sp) # Storing self
		
		# Argument internal_8
		lw $t0, 188($sp)
		sw $t0, 0($sp) # Storing internal_8
		
		# Calling function function_print_at_Main
		jal function_print_at_Main
		lw $ra, 8($sp)
		sw $v1, 184($sp) # internal_9 = result of function_print_at_Main
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# Allocating String
		li $v0, 9
		addi $a0, $zero, 21 # $a0 = length of string + 9 for 4 bytes for the type, 4 bytes for the length of the string and 1 byte for null-terminator
		syscall
		
		la $t0, type_String
		sw $t0, 0($v0) # Setting type in the first word of the object
		
		addi $t0, $zero, 21
		sw $t0, 4($v0) # Setting length of the string in the second word of the object
		
		addi $t0, $zero, 46
		sb $t0, 8($v0) # internal_10[0] = '.'
		
		addi $t0, $zero, 46
		sb $t0, 9($v0) # internal_10[1] = '.'
		
		addi $t0, $zero, 46
		sb $t0, 10($v0) # internal_10[2] = '.'
		
		addi $t0, $zero, 101
		sb $t0, 11($v0) # internal_10[3] = 'e'
		
		addi $t0, $zero, 110
		sb $t0, 12($v0) # internal_10[4] = 'n'
		
		addi $t0, $zero, 116
		sb $t0, 13($v0) # internal_10[5] = 't'
		
		addi $t0, $zero, 101
		sb $t0, 14($v0) # internal_10[6] = 'e'
		
		addi $t0, $zero, 114
		sb $t0, 15($v0) # internal_10[7] = 'r'
		
		addi $t0, $zero, 32
		sb $t0, 16($v0) # internal_10[8] = ' '
		
		addi $t0, $zero, 98
		sb $t0, 17($v0) # internal_10[9] = 'b'
		
		addi $t0, $zero, 58
		sb $t0, 18($v0) # internal_10[10] = ':'
		
		addi $t0, $zero, 10
		sb $t0, 19($v0) # internal_10[11] = '\n'
		
		sb $zero, 20($v0) # Null-terminator at the end of the string
		
		sw $v0, 168($sp) # internal_10 = "...enter b:\n"
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument self
		lw $t0, 224($sp)
		sw $t0, 4($sp) # Storing self
		
		# Argument internal_10
		lw $t0, 180($sp)
		sw $t0, 0($sp) # Storing internal_10
		
		# Calling function function_out_string_at_IO
		jal function_out_string_at_IO
		lw $ra, 8($sp)
		sw $v1, 176($sp) # internal_11 = result of function_out_string_at_IO
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# Allocating String
		li $v0, 9
		addi $a0, $zero, 41 # $a0 = length of string + 9 for 4 bytes for the type, 4 bytes for the length of the string and 1 byte for null-terminator
		syscall
		
		la $t0, type_String
		sw $t0, 0($v0) # Setting type in the first word of the object
		
		addi $t0, $zero, 41
		sw $t0, 4($v0) # Setting length of the string in the second word of the object
		
		addi $t0, $zero, 9
		sb $t0, 8($v0) # internal_12[0] = '\t'
		
		addi $t0, $zero, 84
		sb $t0, 9($v0) # internal_12[1] = 'T'
		
		addi $t0, $zero, 111
		sb $t0, 10($v0) # internal_12[2] = 'o'
		
		addi $t0, $zero, 32
		sb $t0, 11($v0) # internal_12[3] = ' '
		
		addi $t0, $zero, 102
		sb $t0, 12($v0) # internal_12[4] = 'f'
		
		addi $t0, $zero, 105
		sb $t0, 13($v0) # internal_12[5] = 'i'
		
		addi $t0, $zero, 110
		sb $t0, 14($v0) # internal_12[6] = 'n'
		
		addi $t0, $zero, 100
		sb $t0, 15($v0) # internal_12[7] = 'd'
		
		addi $t0, $zero, 32
		sb $t0, 16($v0) # internal_12[8] = ' '
		
		addi $t0, $zero, 116
		sb $t0, 17($v0) # internal_12[9] = 't'
		
		addi $t0, $zero, 104
		sb $t0, 18($v0) # internal_12[10] = 'h'
		
		addi $t0, $zero, 101
		sb $t0, 19($v0) # internal_12[11] = 'e'
		
		addi $t0, $zero, 32
		sb $t0, 20($v0) # internal_12[12] = ' '
		
		addi $t0, $zero, 100
		sb $t0, 21($v0) # internal_12[13] = 'd'
		
		addi $t0, $zero, 105
		sb $t0, 22($v0) # internal_12[14] = 'i'
		
		addi $t0, $zero, 102
		sb $t0, 23($v0) # internal_12[15] = 'f'
		
		addi $t0, $zero, 102
		sb $t0, 24($v0) # internal_12[16] = 'f'
		
		addi $t0, $zero, 101
		sb $t0, 25($v0) # internal_12[17] = 'e'
		
		addi $t0, $zero, 114
		sb $t0, 26($v0) # internal_12[18] = 'r'
		
		addi $t0, $zero, 101
		sb $t0, 27($v0) # internal_12[19] = 'e'
		
		addi $t0, $zero, 110
		sb $t0, 28($v0) # internal_12[20] = 'n'
		
		addi $t0, $zero, 99
		sb $t0, 29($v0) # internal_12[21] = 'c'
		
		addi $t0, $zero, 101
		sb $t0, 30($v0) # internal_12[22] = 'e'
		
		addi $t0, $zero, 32
		sb $t0, 31($v0) # internal_12[23] = ' '
		
		addi $t0, $zero, 98
		sb $t0, 32($v0) # internal_12[24] = 'b'
		
		addi $t0, $zero, 101
		sb $t0, 33($v0) # internal_12[25] = 'e'
		
		addi $t0, $zero, 116
		sb $t0, 34($v0) # internal_12[26] = 't'
		
		addi $t0, $zero, 119
		sb $t0, 35($v0) # internal_12[27] = 'w'
		
		addi $t0, $zero, 101
		sb $t0, 36($v0) # internal_12[28] = 'e'
		
		addi $t0, $zero, 101
		sb $t0, 37($v0) # internal_12[29] = 'e'
		
		addi $t0, $zero, 110
		sb $t0, 38($v0) # internal_12[30] = 'n'
		
		addi $t0, $zero, 32
		sb $t0, 39($v0) # internal_12[31] = ' '
		
		sb $zero, 40($v0) # Null-terminator at the end of the string
		
		sw $v0, 160($sp) # internal_12 = "\tTo find the difference between "
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument self
		lw $t0, 224($sp)
		sw $t0, 4($sp) # Storing self
		
		# Argument internal_12
		lw $t0, 172($sp)
		sw $t0, 0($sp) # Storing internal_12
		
		# Calling function function_out_string_at_IO
		jal function_out_string_at_IO
		lw $ra, 8($sp)
		sw $v1, 168($sp) # internal_13 = result of function_out_string_at_IO
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# Get attribute avar of self
		lw $t0, 212($sp) # Get the address of self
		lw $t1, 12($t0) # Get the attribute 'avar' from the instance
		lw $t2, 0($t1)
		la $t3, type_Int
		la $t4, type_Bool
		addi $t5, $zero, 1
		seq $t6, $t2, $t3
		beq $t6, $t5, int_get_attribute_8781702247087
		seq $t6, $t2, $t4
		beq $t6, $t5, bool_get_attribute_8781702247087
		j object_get_attribute_8781702247087
		int_get_attribute_8781702247087:
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		sw $t3, 0($v0)
		sw $a0, 4($v0)
		lw $t5, 8($t1)
		sw $t5, 8($v0)
		sw $v0, 152($sp) # internal_14 = self.avar
		j end_get_attribute_8781702247087
		bool_get_attribute_8781702247087:
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		sw $t4, 0($v0)
		sw $a0, 4($v0)
		lw $t5, 8($t1)
		sw $t5, 8($v0)
		sw $v0, 152($sp) # internal_14 = self.avar
		j end_get_attribute_8781702247087
		object_get_attribute_8781702247087:
		sw $t1, 152($sp) # internal_14 = avar
		end_get_attribute_8781702247087:
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument self
		lw $t0, 224($sp)
		sw $t0, 4($sp) # Storing self
		
		# Argument internal_14
		lw $t0, 164($sp)
		sw $t0, 0($sp) # Storing internal_14
		
		# Calling function function_print_at_Main
		jal function_print_at_Main
		lw $ra, 8($sp)
		sw $v1, 160($sp) # internal_15 = result of function_print_at_Main
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# Allocating String
		li $v0, 9
		addi $a0, $zero, 39 # $a0 = length of string + 9 for 4 bytes for the type, 4 bytes for the length of the string and 1 byte for null-terminator
		syscall
		
		la $t0, type_String
		sw $t0, 0($v0) # Setting type in the first word of the object
		
		addi $t0, $zero, 39
		sw $t0, 4($v0) # Setting length of the string in the second word of the object
		
		addi $t0, $zero, 97
		sb $t0, 8($v0) # internal_16[0] = 'a'
		
		addi $t0, $zero, 110
		sb $t0, 9($v0) # internal_16[1] = 'n'
		
		addi $t0, $zero, 100
		sb $t0, 10($v0) # internal_16[2] = 'd'
		
		addi $t0, $zero, 32
		sb $t0, 11($v0) # internal_16[3] = ' '
		
		addi $t0, $zero, 97
		sb $t0, 12($v0) # internal_16[4] = 'a'
		
		addi $t0, $zero, 110
		sb $t0, 13($v0) # internal_16[5] = 'n'
		
		addi $t0, $zero, 111
		sb $t0, 14($v0) # internal_16[6] = 'o'
		
		addi $t0, $zero, 116
		sb $t0, 15($v0) # internal_16[7] = 't'
		
		addi $t0, $zero, 104
		sb $t0, 16($v0) # internal_16[8] = 'h'
		
		addi $t0, $zero, 101
		sb $t0, 17($v0) # internal_16[9] = 'e'
		
		addi $t0, $zero, 114
		sb $t0, 18($v0) # internal_16[10] = 'r'
		
		addi $t0, $zero, 32
		sb $t0, 19($v0) # internal_16[11] = ' '
		
		addi $t0, $zero, 110
		sb $t0, 20($v0) # internal_16[12] = 'n'
		
		addi $t0, $zero, 117
		sb $t0, 21($v0) # internal_16[13] = 'u'
		
		addi $t0, $zero, 109
		sb $t0, 22($v0) # internal_16[14] = 'm'
		
		addi $t0, $zero, 98
		sb $t0, 23($v0) # internal_16[15] = 'b'
		
		addi $t0, $zero, 101
		sb $t0, 24($v0) # internal_16[16] = 'e'
		
		addi $t0, $zero, 114
		sb $t0, 25($v0) # internal_16[17] = 'r'
		
		addi $t0, $zero, 46
		sb $t0, 26($v0) # internal_16[18] = '.'
		
		addi $t0, $zero, 46
		sb $t0, 27($v0) # internal_16[19] = '.'
		
		addi $t0, $zero, 46
		sb $t0, 28($v0) # internal_16[20] = '.'
		
		addi $t0, $zero, 101
		sb $t0, 29($v0) # internal_16[21] = 'e'
		
		addi $t0, $zero, 110
		sb $t0, 30($v0) # internal_16[22] = 'n'
		
		addi $t0, $zero, 116
		sb $t0, 31($v0) # internal_16[23] = 't'
		
		addi $t0, $zero, 101
		sb $t0, 32($v0) # internal_16[24] = 'e'
		
		addi $t0, $zero, 114
		sb $t0, 33($v0) # internal_16[25] = 'r'
		
		addi $t0, $zero, 32
		sb $t0, 34($v0) # internal_16[26] = ' '
		
		addi $t0, $zero, 99
		sb $t0, 35($v0) # internal_16[27] = 'c'
		
		addi $t0, $zero, 58
		sb $t0, 36($v0) # internal_16[28] = ':'
		
		addi $t0, $zero, 10
		sb $t0, 37($v0) # internal_16[29] = '\n'
		
		sb $zero, 38($v0) # Null-terminator at the end of the string
		
		sw $v0, 144($sp) # internal_16 = "and another number...enter c:\n"
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument self
		lw $t0, 224($sp)
		sw $t0, 4($sp) # Storing self
		
		# Argument internal_16
		lw $t0, 156($sp)
		sw $t0, 0($sp) # Storing internal_16
		
		# Calling function function_out_string_at_IO
		jal function_out_string_at_IO
		lw $ra, 8($sp)
		sw $v1, 152($sp) # internal_17 = result of function_out_string_at_IO
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# Allocating String
		li $v0, 9
		addi $a0, $zero, 35 # $a0 = length of string + 9 for 4 bytes for the type, 4 bytes for the length of the string and 1 byte for null-terminator
		syscall
		
		la $t0, type_String
		sw $t0, 0($v0) # Setting type in the first word of the object
		
		addi $t0, $zero, 35
		sw $t0, 4($v0) # Setting length of the string in the second word of the object
		
		addi $t0, $zero, 9
		sb $t0, 8($v0) # internal_18[0] = '\t'
		
		addi $t0, $zero, 84
		sb $t0, 9($v0) # internal_18[1] = 'T'
		
		addi $t0, $zero, 111
		sb $t0, 10($v0) # internal_18[2] = 'o'
		
		addi $t0, $zero, 32
		sb $t0, 11($v0) # internal_18[3] = ' '
		
		addi $t0, $zero, 102
		sb $t0, 12($v0) # internal_18[4] = 'f'
		
		addi $t0, $zero, 105
		sb $t0, 13($v0) # internal_18[5] = 'i'
		
		addi $t0, $zero, 110
		sb $t0, 14($v0) # internal_18[6] = 'n'
		
		addi $t0, $zero, 100
		sb $t0, 15($v0) # internal_18[7] = 'd'
		
		addi $t0, $zero, 32
		sb $t0, 16($v0) # internal_18[8] = ' '
		
		addi $t0, $zero, 116
		sb $t0, 17($v0) # internal_18[9] = 't'
		
		addi $t0, $zero, 104
		sb $t0, 18($v0) # internal_18[10] = 'h'
		
		addi $t0, $zero, 101
		sb $t0, 19($v0) # internal_18[11] = 'e'
		
		addi $t0, $zero, 32
		sb $t0, 20($v0) # internal_18[12] = ' '
		
		addi $t0, $zero, 102
		sb $t0, 21($v0) # internal_18[13] = 'f'
		
		addi $t0, $zero, 97
		sb $t0, 22($v0) # internal_18[14] = 'a'
		
		addi $t0, $zero, 99
		sb $t0, 23($v0) # internal_18[15] = 'c'
		
		addi $t0, $zero, 116
		sb $t0, 24($v0) # internal_18[16] = 't'
		
		addi $t0, $zero, 111
		sb $t0, 25($v0) # internal_18[17] = 'o'
		
		addi $t0, $zero, 114
		sb $t0, 26($v0) # internal_18[18] = 'r'
		
		addi $t0, $zero, 105
		sb $t0, 27($v0) # internal_18[19] = 'i'
		
		addi $t0, $zero, 97
		sb $t0, 28($v0) # internal_18[20] = 'a'
		
		addi $t0, $zero, 108
		sb $t0, 29($v0) # internal_18[21] = 'l'
		
		addi $t0, $zero, 32
		sb $t0, 30($v0) # internal_18[22] = ' '
		
		addi $t0, $zero, 111
		sb $t0, 31($v0) # internal_18[23] = 'o'
		
		addi $t0, $zero, 102
		sb $t0, 32($v0) # internal_18[24] = 'f'
		
		addi $t0, $zero, 32
		sb $t0, 33($v0) # internal_18[25] = ' '
		
		sb $zero, 34($v0) # Null-terminator at the end of the string
		
		sw $v0, 136($sp) # internal_18 = "\tTo find the factorial of "
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument self
		lw $t0, 224($sp)
		sw $t0, 4($sp) # Storing self
		
		# Argument internal_18
		lw $t0, 148($sp)
		sw $t0, 0($sp) # Storing internal_18
		
		# Calling function function_out_string_at_IO
		jal function_out_string_at_IO
		lw $ra, 8($sp)
		sw $v1, 144($sp) # internal_19 = result of function_out_string_at_IO
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# Get attribute avar of self
		lw $t0, 212($sp) # Get the address of self
		lw $t1, 12($t0) # Get the attribute 'avar' from the instance
		lw $t2, 0($t1)
		la $t3, type_Int
		la $t4, type_Bool
		addi $t5, $zero, 1
		seq $t6, $t2, $t3
		beq $t6, $t5, int_get_attribute_8781702247711
		seq $t6, $t2, $t4
		beq $t6, $t5, bool_get_attribute_8781702247711
		j object_get_attribute_8781702247711
		int_get_attribute_8781702247711:
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		sw $t3, 0($v0)
		sw $a0, 4($v0)
		lw $t5, 8($t1)
		sw $t5, 8($v0)
		sw $v0, 128($sp) # internal_20 = self.avar
		j end_get_attribute_8781702247711
		bool_get_attribute_8781702247711:
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		sw $t4, 0($v0)
		sw $a0, 4($v0)
		lw $t5, 8($t1)
		sw $t5, 8($v0)
		sw $v0, 128($sp) # internal_20 = self.avar
		j end_get_attribute_8781702247711
		object_get_attribute_8781702247711:
		sw $t1, 128($sp) # internal_20 = avar
		end_get_attribute_8781702247711:
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument self
		lw $t0, 224($sp)
		sw $t0, 4($sp) # Storing self
		
		# Argument internal_20
		lw $t0, 140($sp)
		sw $t0, 0($sp) # Storing internal_20
		
		# Calling function function_print_at_Main
		jal function_print_at_Main
		lw $ra, 8($sp)
		sw $v1, 136($sp) # internal_21 = result of function_print_at_Main
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# Allocating String
		li $v0, 9
		addi $a0, $zero, 21 # $a0 = length of string + 9 for 4 bytes for the type, 4 bytes for the length of the string and 1 byte for null-terminator
		syscall
		
		la $t0, type_String
		sw $t0, 0($v0) # Setting type in the first word of the object
		
		addi $t0, $zero, 21
		sw $t0, 4($v0) # Setting length of the string in the second word of the object
		
		addi $t0, $zero, 46
		sb $t0, 8($v0) # internal_22[0] = '.'
		
		addi $t0, $zero, 46
		sb $t0, 9($v0) # internal_22[1] = '.'
		
		addi $t0, $zero, 46
		sb $t0, 10($v0) # internal_22[2] = '.'
		
		addi $t0, $zero, 101
		sb $t0, 11($v0) # internal_22[3] = 'e'
		
		addi $t0, $zero, 110
		sb $t0, 12($v0) # internal_22[4] = 'n'
		
		addi $t0, $zero, 116
		sb $t0, 13($v0) # internal_22[5] = 't'
		
		addi $t0, $zero, 101
		sb $t0, 14($v0) # internal_22[6] = 'e'
		
		addi $t0, $zero, 114
		sb $t0, 15($v0) # internal_22[7] = 'r'
		
		addi $t0, $zero, 32
		sb $t0, 16($v0) # internal_22[8] = ' '
		
		addi $t0, $zero, 100
		sb $t0, 17($v0) # internal_22[9] = 'd'
		
		addi $t0, $zero, 58
		sb $t0, 18($v0) # internal_22[10] = ':'
		
		addi $t0, $zero, 10
		sb $t0, 19($v0) # internal_22[11] = '\n'
		
		sb $zero, 20($v0) # Null-terminator at the end of the string
		
		sw $v0, 120($sp) # internal_22 = "...enter d:\n"
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument self
		lw $t0, 224($sp)
		sw $t0, 4($sp) # Storing self
		
		# Argument internal_22
		lw $t0, 132($sp)
		sw $t0, 0($sp) # Storing internal_22
		
		# Calling function function_out_string_at_IO
		jal function_out_string_at_IO
		lw $ra, 8($sp)
		sw $v1, 128($sp) # internal_23 = result of function_out_string_at_IO
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# Allocating String
		li $v0, 9
		addi $a0, $zero, 20 # $a0 = length of string + 9 for 4 bytes for the type, 4 bytes for the length of the string and 1 byte for null-terminator
		syscall
		
		la $t0, type_String
		sw $t0, 0($v0) # Setting type in the first word of the object
		
		addi $t0, $zero, 20
		sw $t0, 4($v0) # Setting length of the string in the second word of the object
		
		addi $t0, $zero, 9
		sb $t0, 8($v0) # internal_24[0] = '\t'
		
		addi $t0, $zero, 84
		sb $t0, 9($v0) # internal_24[1] = 'T'
		
		addi $t0, $zero, 111
		sb $t0, 10($v0) # internal_24[2] = 'o'
		
		addi $t0, $zero, 32
		sb $t0, 11($v0) # internal_24[3] = ' '
		
		addi $t0, $zero, 115
		sb $t0, 12($v0) # internal_24[4] = 's'
		
		addi $t0, $zero, 113
		sb $t0, 13($v0) # internal_24[5] = 'q'
		
		addi $t0, $zero, 117
		sb $t0, 14($v0) # internal_24[6] = 'u'
		
		addi $t0, $zero, 97
		sb $t0, 15($v0) # internal_24[7] = 'a'
		
		addi $t0, $zero, 114
		sb $t0, 16($v0) # internal_24[8] = 'r'
		
		addi $t0, $zero, 101
		sb $t0, 17($v0) # internal_24[9] = 'e'
		
		addi $t0, $zero, 32
		sb $t0, 18($v0) # internal_24[10] = ' '
		
		sb $zero, 19($v0) # Null-terminator at the end of the string
		
		sw $v0, 112($sp) # internal_24 = "\tTo square "
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument self
		lw $t0, 224($sp)
		sw $t0, 4($sp) # Storing self
		
		# Argument internal_24
		lw $t0, 124($sp)
		sw $t0, 0($sp) # Storing internal_24
		
		# Calling function function_out_string_at_IO
		jal function_out_string_at_IO
		lw $ra, 8($sp)
		sw $v1, 120($sp) # internal_25 = result of function_out_string_at_IO
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# Get attribute avar of self
		lw $t0, 212($sp) # Get the address of self
		lw $t1, 12($t0) # Get the attribute 'avar' from the instance
		lw $t2, 0($t1)
		la $t3, type_Int
		la $t4, type_Bool
		addi $t5, $zero, 1
		seq $t6, $t2, $t3
		beq $t6, $t5, int_get_attribute_8781702247819
		seq $t6, $t2, $t4
		beq $t6, $t5, bool_get_attribute_8781702247819
		j object_get_attribute_8781702247819
		int_get_attribute_8781702247819:
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		sw $t3, 0($v0)
		sw $a0, 4($v0)
		lw $t5, 8($t1)
		sw $t5, 8($v0)
		sw $v0, 104($sp) # internal_26 = self.avar
		j end_get_attribute_8781702247819
		bool_get_attribute_8781702247819:
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		sw $t4, 0($v0)
		sw $a0, 4($v0)
		lw $t5, 8($t1)
		sw $t5, 8($v0)
		sw $v0, 104($sp) # internal_26 = self.avar
		j end_get_attribute_8781702247819
		object_get_attribute_8781702247819:
		sw $t1, 104($sp) # internal_26 = avar
		end_get_attribute_8781702247819:
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument self
		lw $t0, 224($sp)
		sw $t0, 4($sp) # Storing self
		
		# Argument internal_26
		lw $t0, 116($sp)
		sw $t0, 0($sp) # Storing internal_26
		
		# Calling function function_print_at_Main
		jal function_print_at_Main
		lw $ra, 8($sp)
		sw $v1, 112($sp) # internal_27 = result of function_print_at_Main
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# Allocating String
		li $v0, 9
		addi $a0, $zero, 21 # $a0 = length of string + 9 for 4 bytes for the type, 4 bytes for the length of the string and 1 byte for null-terminator
		syscall
		
		la $t0, type_String
		sw $t0, 0($v0) # Setting type in the first word of the object
		
		addi $t0, $zero, 21
		sw $t0, 4($v0) # Setting length of the string in the second word of the object
		
		addi $t0, $zero, 46
		sb $t0, 8($v0) # internal_28[0] = '.'
		
		addi $t0, $zero, 46
		sb $t0, 9($v0) # internal_28[1] = '.'
		
		addi $t0, $zero, 46
		sb $t0, 10($v0) # internal_28[2] = '.'
		
		addi $t0, $zero, 101
		sb $t0, 11($v0) # internal_28[3] = 'e'
		
		addi $t0, $zero, 110
		sb $t0, 12($v0) # internal_28[4] = 'n'
		
		addi $t0, $zero, 116
		sb $t0, 13($v0) # internal_28[5] = 't'
		
		addi $t0, $zero, 101
		sb $t0, 14($v0) # internal_28[6] = 'e'
		
		addi $t0, $zero, 114
		sb $t0, 15($v0) # internal_28[7] = 'r'
		
		addi $t0, $zero, 32
		sb $t0, 16($v0) # internal_28[8] = ' '
		
		addi $t0, $zero, 101
		sb $t0, 17($v0) # internal_28[9] = 'e'
		
		addi $t0, $zero, 58
		sb $t0, 18($v0) # internal_28[10] = ':'
		
		addi $t0, $zero, 10
		sb $t0, 19($v0) # internal_28[11] = '\n'
		
		sb $zero, 20($v0) # Null-terminator at the end of the string
		
		sw $v0, 96($sp) # internal_28 = "...enter e:\n"
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument self
		lw $t0, 224($sp)
		sw $t0, 4($sp) # Storing self
		
		# Argument internal_28
		lw $t0, 108($sp)
		sw $t0, 0($sp) # Storing internal_28
		
		# Calling function function_out_string_at_IO
		jal function_out_string_at_IO
		lw $ra, 8($sp)
		sw $v1, 104($sp) # internal_29 = result of function_out_string_at_IO
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# Allocating String
		li $v0, 9
		addi $a0, $zero, 18 # $a0 = length of string + 9 for 4 bytes for the type, 4 bytes for the length of the string and 1 byte for null-terminator
		syscall
		
		la $t0, type_String
		sw $t0, 0($v0) # Setting type in the first word of the object
		
		addi $t0, $zero, 18
		sw $t0, 4($v0) # Setting length of the string in the second word of the object
		
		addi $t0, $zero, 9
		sb $t0, 8($v0) # internal_30[0] = '\t'
		
		addi $t0, $zero, 84
		sb $t0, 9($v0) # internal_30[1] = 'T'
		
		addi $t0, $zero, 111
		sb $t0, 10($v0) # internal_30[2] = 'o'
		
		addi $t0, $zero, 32
		sb $t0, 11($v0) # internal_30[3] = ' '
		
		addi $t0, $zero, 99
		sb $t0, 12($v0) # internal_30[4] = 'c'
		
		addi $t0, $zero, 117
		sb $t0, 13($v0) # internal_30[5] = 'u'
		
		addi $t0, $zero, 98
		sb $t0, 14($v0) # internal_30[6] = 'b'
		
		addi $t0, $zero, 101
		sb $t0, 15($v0) # internal_30[7] = 'e'
		
		addi $t0, $zero, 32
		sb $t0, 16($v0) # internal_30[8] = ' '
		
		sb $zero, 17($v0) # Null-terminator at the end of the string
		
		sw $v0, 88($sp) # internal_30 = "\tTo cube "
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument self
		lw $t0, 224($sp)
		sw $t0, 4($sp) # Storing self
		
		# Argument internal_30
		lw $t0, 100($sp)
		sw $t0, 0($sp) # Storing internal_30
		
		# Calling function function_out_string_at_IO
		jal function_out_string_at_IO
		lw $ra, 8($sp)
		sw $v1, 96($sp) # internal_31 = result of function_out_string_at_IO
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# Get attribute avar of self
		lw $t0, 212($sp) # Get the address of self
		lw $t1, 12($t0) # Get the attribute 'avar' from the instance
		lw $t2, 0($t1)
		la $t3, type_Int
		la $t4, type_Bool
		addi $t5, $zero, 1
		seq $t6, $t2, $t3
		beq $t6, $t5, int_get_attribute_8781702247927
		seq $t6, $t2, $t4
		beq $t6, $t5, bool_get_attribute_8781702247927
		j object_get_attribute_8781702247927
		int_get_attribute_8781702247927:
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		sw $t3, 0($v0)
		sw $a0, 4($v0)
		lw $t5, 8($t1)
		sw $t5, 8($v0)
		sw $v0, 80($sp) # internal_32 = self.avar
		j end_get_attribute_8781702247927
		bool_get_attribute_8781702247927:
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		sw $t4, 0($v0)
		sw $a0, 4($v0)
		lw $t5, 8($t1)
		sw $t5, 8($v0)
		sw $v0, 80($sp) # internal_32 = self.avar
		j end_get_attribute_8781702247927
		object_get_attribute_8781702247927:
		sw $t1, 80($sp) # internal_32 = avar
		end_get_attribute_8781702247927:
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument self
		lw $t0, 224($sp)
		sw $t0, 4($sp) # Storing self
		
		# Argument internal_32
		lw $t0, 92($sp)
		sw $t0, 0($sp) # Storing internal_32
		
		# Calling function function_print_at_Main
		jal function_print_at_Main
		lw $ra, 8($sp)
		sw $v1, 88($sp) # internal_33 = result of function_print_at_Main
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# Allocating String
		li $v0, 9
		addi $a0, $zero, 21 # $a0 = length of string + 9 for 4 bytes for the type, 4 bytes for the length of the string and 1 byte for null-terminator
		syscall
		
		la $t0, type_String
		sw $t0, 0($v0) # Setting type in the first word of the object
		
		addi $t0, $zero, 21
		sw $t0, 4($v0) # Setting length of the string in the second word of the object
		
		addi $t0, $zero, 46
		sb $t0, 8($v0) # internal_34[0] = '.'
		
		addi $t0, $zero, 46
		sb $t0, 9($v0) # internal_34[1] = '.'
		
		addi $t0, $zero, 46
		sb $t0, 10($v0) # internal_34[2] = '.'
		
		addi $t0, $zero, 101
		sb $t0, 11($v0) # internal_34[3] = 'e'
		
		addi $t0, $zero, 110
		sb $t0, 12($v0) # internal_34[4] = 'n'
		
		addi $t0, $zero, 116
		sb $t0, 13($v0) # internal_34[5] = 't'
		
		addi $t0, $zero, 101
		sb $t0, 14($v0) # internal_34[6] = 'e'
		
		addi $t0, $zero, 114
		sb $t0, 15($v0) # internal_34[7] = 'r'
		
		addi $t0, $zero, 32
		sb $t0, 16($v0) # internal_34[8] = ' '
		
		addi $t0, $zero, 102
		sb $t0, 17($v0) # internal_34[9] = 'f'
		
		addi $t0, $zero, 58
		sb $t0, 18($v0) # internal_34[10] = ':'
		
		addi $t0, $zero, 10
		sb $t0, 19($v0) # internal_34[11] = '\n'
		
		sb $zero, 20($v0) # Null-terminator at the end of the string
		
		sw $v0, 72($sp) # internal_34 = "...enter f:\n"
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument self
		lw $t0, 224($sp)
		sw $t0, 4($sp) # Storing self
		
		# Argument internal_34
		lw $t0, 84($sp)
		sw $t0, 0($sp) # Storing internal_34
		
		# Calling function function_out_string_at_IO
		jal function_out_string_at_IO
		lw $ra, 8($sp)
		sw $v1, 80($sp) # internal_35 = result of function_out_string_at_IO
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# Allocating String
		li $v0, 9
		addi $a0, $zero, 25 # $a0 = length of string + 9 for 4 bytes for the type, 4 bytes for the length of the string and 1 byte for null-terminator
		syscall
		
		la $t0, type_String
		sw $t0, 0($v0) # Setting type in the first word of the object
		
		addi $t0, $zero, 25
		sw $t0, 4($v0) # Setting length of the string in the second word of the object
		
		addi $t0, $zero, 9
		sb $t0, 8($v0) # internal_36[0] = '\t'
		
		addi $t0, $zero, 84
		sb $t0, 9($v0) # internal_36[1] = 'T'
		
		addi $t0, $zero, 111
		sb $t0, 10($v0) # internal_36[2] = 'o'
		
		addi $t0, $zero, 32
		sb $t0, 11($v0) # internal_36[3] = ' '
		
		addi $t0, $zero, 102
		sb $t0, 12($v0) # internal_36[4] = 'f'
		
		addi $t0, $zero, 105
		sb $t0, 13($v0) # internal_36[5] = 'i'
		
		addi $t0, $zero, 110
		sb $t0, 14($v0) # internal_36[6] = 'n'
		
		addi $t0, $zero, 100
		sb $t0, 15($v0) # internal_36[7] = 'd'
		
		addi $t0, $zero, 32
		sb $t0, 16($v0) # internal_36[8] = ' '
		
		addi $t0, $zero, 111
		sb $t0, 17($v0) # internal_36[9] = 'o'
		
		addi $t0, $zero, 117
		sb $t0, 18($v0) # internal_36[10] = 'u'
		
		addi $t0, $zero, 116
		sb $t0, 19($v0) # internal_36[11] = 't'
		
		addi $t0, $zero, 32
		sb $t0, 20($v0) # internal_36[12] = ' '
		
		addi $t0, $zero, 105
		sb $t0, 21($v0) # internal_36[13] = 'i'
		
		addi $t0, $zero, 102
		sb $t0, 22($v0) # internal_36[14] = 'f'
		
		addi $t0, $zero, 32
		sb $t0, 23($v0) # internal_36[15] = ' '
		
		sb $zero, 24($v0) # Null-terminator at the end of the string
		
		sw $v0, 64($sp) # internal_36 = "\tTo find out if "
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument self
		lw $t0, 224($sp)
		sw $t0, 4($sp) # Storing self
		
		# Argument internal_36
		lw $t0, 76($sp)
		sw $t0, 0($sp) # Storing internal_36
		
		# Calling function function_out_string_at_IO
		jal function_out_string_at_IO
		lw $ra, 8($sp)
		sw $v1, 72($sp) # internal_37 = result of function_out_string_at_IO
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# Get attribute avar of self
		lw $t0, 212($sp) # Get the address of self
		lw $t1, 12($t0) # Get the attribute 'avar' from the instance
		lw $t2, 0($t1)
		la $t3, type_Int
		la $t4, type_Bool
		addi $t5, $zero, 1
		seq $t6, $t2, $t3
		beq $t6, $t5, int_get_attribute_8781702248039
		seq $t6, $t2, $t4
		beq $t6, $t5, bool_get_attribute_8781702248039
		j object_get_attribute_8781702248039
		int_get_attribute_8781702248039:
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		sw $t3, 0($v0)
		sw $a0, 4($v0)
		lw $t5, 8($t1)
		sw $t5, 8($v0)
		sw $v0, 56($sp) # internal_38 = self.avar
		j end_get_attribute_8781702248039
		bool_get_attribute_8781702248039:
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		sw $t4, 0($v0)
		sw $a0, 4($v0)
		lw $t5, 8($t1)
		sw $t5, 8($v0)
		sw $v0, 56($sp) # internal_38 = self.avar
		j end_get_attribute_8781702248039
		object_get_attribute_8781702248039:
		sw $t1, 56($sp) # internal_38 = avar
		end_get_attribute_8781702248039:
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument self
		lw $t0, 224($sp)
		sw $t0, 4($sp) # Storing self
		
		# Argument internal_38
		lw $t0, 68($sp)
		sw $t0, 0($sp) # Storing internal_38
		
		# Calling function function_print_at_Main
		jal function_print_at_Main
		lw $ra, 8($sp)
		sw $v1, 64($sp) # internal_39 = result of function_print_at_Main
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# Allocating String
		li $v0, 9
		addi $a0, $zero, 39 # $a0 = length of string + 9 for 4 bytes for the type, 4 bytes for the length of the string and 1 byte for null-terminator
		syscall
		
		la $t0, type_String
		sw $t0, 0($v0) # Setting type in the first word of the object
		
		addi $t0, $zero, 39
		sw $t0, 4($v0) # Setting length of the string in the second word of the object
		
		addi $t0, $zero, 105
		sb $t0, 8($v0) # internal_40[0] = 'i'
		
		addi $t0, $zero, 115
		sb $t0, 9($v0) # internal_40[1] = 's'
		
		addi $t0, $zero, 32
		sb $t0, 10($v0) # internal_40[2] = ' '
		
		addi $t0, $zero, 97
		sb $t0, 11($v0) # internal_40[3] = 'a'
		
		addi $t0, $zero, 32
		sb $t0, 12($v0) # internal_40[4] = ' '
		
		addi $t0, $zero, 109
		sb $t0, 13($v0) # internal_40[5] = 'm'
		
		addi $t0, $zero, 117
		sb $t0, 14($v0) # internal_40[6] = 'u'
		
		addi $t0, $zero, 108
		sb $t0, 15($v0) # internal_40[7] = 'l'
		
		addi $t0, $zero, 116
		sb $t0, 16($v0) # internal_40[8] = 't'
		
		addi $t0, $zero, 105
		sb $t0, 17($v0) # internal_40[9] = 'i'
		
		addi $t0, $zero, 112
		sb $t0, 18($v0) # internal_40[10] = 'p'
		
		addi $t0, $zero, 108
		sb $t0, 19($v0) # internal_40[11] = 'l'
		
		addi $t0, $zero, 101
		sb $t0, 20($v0) # internal_40[12] = 'e'
		
		addi $t0, $zero, 32
		sb $t0, 21($v0) # internal_40[13] = ' '
		
		addi $t0, $zero, 111
		sb $t0, 22($v0) # internal_40[14] = 'o'
		
		addi $t0, $zero, 102
		sb $t0, 23($v0) # internal_40[15] = 'f'
		
		addi $t0, $zero, 32
		sb $t0, 24($v0) # internal_40[16] = ' '
		
		addi $t0, $zero, 51
		sb $t0, 25($v0) # internal_40[17] = '3'
		
		addi $t0, $zero, 46
		sb $t0, 26($v0) # internal_40[18] = '.'
		
		addi $t0, $zero, 46
		sb $t0, 27($v0) # internal_40[19] = '.'
		
		addi $t0, $zero, 46
		sb $t0, 28($v0) # internal_40[20] = '.'
		
		addi $t0, $zero, 101
		sb $t0, 29($v0) # internal_40[21] = 'e'
		
		addi $t0, $zero, 110
		sb $t0, 30($v0) # internal_40[22] = 'n'
		
		addi $t0, $zero, 116
		sb $t0, 31($v0) # internal_40[23] = 't'
		
		addi $t0, $zero, 101
		sb $t0, 32($v0) # internal_40[24] = 'e'
		
		addi $t0, $zero, 114
		sb $t0, 33($v0) # internal_40[25] = 'r'
		
		addi $t0, $zero, 32
		sb $t0, 34($v0) # internal_40[26] = ' '
		
		addi $t0, $zero, 103
		sb $t0, 35($v0) # internal_40[27] = 'g'
		
		addi $t0, $zero, 58
		sb $t0, 36($v0) # internal_40[28] = ':'
		
		addi $t0, $zero, 10
		sb $t0, 37($v0) # internal_40[29] = '\n'
		
		sb $zero, 38($v0) # Null-terminator at the end of the string
		
		sw $v0, 48($sp) # internal_40 = "is a multiple of 3...enter g:\n"
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument self
		lw $t0, 224($sp)
		sw $t0, 4($sp) # Storing self
		
		# Argument internal_40
		lw $t0, 60($sp)
		sw $t0, 0($sp) # Storing internal_40
		
		# Calling function function_out_string_at_IO
		jal function_out_string_at_IO
		lw $ra, 8($sp)
		sw $v1, 56($sp) # internal_41 = result of function_out_string_at_IO
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# Allocating String
		li $v0, 9
		addi $a0, $zero, 20 # $a0 = length of string + 9 for 4 bytes for the type, 4 bytes for the length of the string and 1 byte for null-terminator
		syscall
		
		la $t0, type_String
		sw $t0, 0($v0) # Setting type in the first word of the object
		
		addi $t0, $zero, 20
		sw $t0, 4($v0) # Setting length of the string in the second word of the object
		
		addi $t0, $zero, 9
		sb $t0, 8($v0) # internal_42[0] = '\t'
		
		addi $t0, $zero, 84
		sb $t0, 9($v0) # internal_42[1] = 'T'
		
		addi $t0, $zero, 111
		sb $t0, 10($v0) # internal_42[2] = 'o'
		
		addi $t0, $zero, 32
		sb $t0, 11($v0) # internal_42[3] = ' '
		
		addi $t0, $zero, 100
		sb $t0, 12($v0) # internal_42[4] = 'd'
		
		addi $t0, $zero, 105
		sb $t0, 13($v0) # internal_42[5] = 'i'
		
		addi $t0, $zero, 118
		sb $t0, 14($v0) # internal_42[6] = 'v'
		
		addi $t0, $zero, 105
		sb $t0, 15($v0) # internal_42[7] = 'i'
		
		addi $t0, $zero, 100
		sb $t0, 16($v0) # internal_42[8] = 'd'
		
		addi $t0, $zero, 101
		sb $t0, 17($v0) # internal_42[9] = 'e'
		
		addi $t0, $zero, 32
		sb $t0, 18($v0) # internal_42[10] = ' '
		
		sb $zero, 19($v0) # Null-terminator at the end of the string
		
		sw $v0, 40($sp) # internal_42 = "\tTo divide "
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument self
		lw $t0, 224($sp)
		sw $t0, 4($sp) # Storing self
		
		# Argument internal_42
		lw $t0, 52($sp)
		sw $t0, 0($sp) # Storing internal_42
		
		# Calling function function_out_string_at_IO
		jal function_out_string_at_IO
		lw $ra, 8($sp)
		sw $v1, 48($sp) # internal_43 = result of function_out_string_at_IO
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# Get attribute avar of self
		lw $t0, 212($sp) # Get the address of self
		lw $t1, 12($t0) # Get the attribute 'avar' from the instance
		lw $t2, 0($t1)
		la $t3, type_Int
		la $t4, type_Bool
		addi $t5, $zero, 1
		seq $t6, $t2, $t3
		beq $t6, $t5, int_get_attribute_8781702248147
		seq $t6, $t2, $t4
		beq $t6, $t5, bool_get_attribute_8781702248147
		j object_get_attribute_8781702248147
		int_get_attribute_8781702248147:
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		sw $t3, 0($v0)
		sw $a0, 4($v0)
		lw $t5, 8($t1)
		sw $t5, 8($v0)
		sw $v0, 32($sp) # internal_44 = self.avar
		j end_get_attribute_8781702248147
		bool_get_attribute_8781702248147:
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		sw $t4, 0($v0)
		sw $a0, 4($v0)
		lw $t5, 8($t1)
		sw $t5, 8($v0)
		sw $v0, 32($sp) # internal_44 = self.avar
		j end_get_attribute_8781702248147
		object_get_attribute_8781702248147:
		sw $t1, 32($sp) # internal_44 = avar
		end_get_attribute_8781702248147:
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument self
		lw $t0, 224($sp)
		sw $t0, 4($sp) # Storing self
		
		# Argument internal_44
		lw $t0, 44($sp)
		sw $t0, 0($sp) # Storing internal_44
		
		# Calling function function_print_at_Main
		jal function_print_at_Main
		lw $ra, 8($sp)
		sw $v1, 40($sp) # internal_45 = result of function_print_at_Main
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# Allocating String
		li $v0, 9
		addi $a0, $zero, 25 # $a0 = length of string + 9 for 4 bytes for the type, 4 bytes for the length of the string and 1 byte for null-terminator
		syscall
		
		la $t0, type_String
		sw $t0, 0($v0) # Setting type in the first word of the object
		
		addi $t0, $zero, 25
		sw $t0, 4($v0) # Setting length of the string in the second word of the object
		
		addi $t0, $zero, 98
		sb $t0, 8($v0) # internal_46[0] = 'b'
		
		addi $t0, $zero, 121
		sb $t0, 9($v0) # internal_46[1] = 'y'
		
		addi $t0, $zero, 32
		sb $t0, 10($v0) # internal_46[2] = ' '
		
		addi $t0, $zero, 56
		sb $t0, 11($v0) # internal_46[3] = '8'
		
		addi $t0, $zero, 46
		sb $t0, 12($v0) # internal_46[4] = '.'
		
		addi $t0, $zero, 46
		sb $t0, 13($v0) # internal_46[5] = '.'
		
		addi $t0, $zero, 46
		sb $t0, 14($v0) # internal_46[6] = '.'
		
		addi $t0, $zero, 101
		sb $t0, 15($v0) # internal_46[7] = 'e'
		
		addi $t0, $zero, 110
		sb $t0, 16($v0) # internal_46[8] = 'n'
		
		addi $t0, $zero, 116
		sb $t0, 17($v0) # internal_46[9] = 't'
		
		addi $t0, $zero, 101
		sb $t0, 18($v0) # internal_46[10] = 'e'
		
		addi $t0, $zero, 114
		sb $t0, 19($v0) # internal_46[11] = 'r'
		
		addi $t0, $zero, 32
		sb $t0, 20($v0) # internal_46[12] = ' '
		
		addi $t0, $zero, 104
		sb $t0, 21($v0) # internal_46[13] = 'h'
		
		addi $t0, $zero, 58
		sb $t0, 22($v0) # internal_46[14] = ':'
		
		addi $t0, $zero, 10
		sb $t0, 23($v0) # internal_46[15] = '\n'
		
		sb $zero, 24($v0) # Null-terminator at the end of the string
		
		sw $v0, 24($sp) # internal_46 = "by 8...enter h:\n"
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument self
		lw $t0, 224($sp)
		sw $t0, 4($sp) # Storing self
		
		# Argument internal_46
		lw $t0, 36($sp)
		sw $t0, 0($sp) # Storing internal_46
		
		# Calling function function_out_string_at_IO
		jal function_out_string_at_IO
		lw $ra, 8($sp)
		sw $v1, 32($sp) # internal_47 = result of function_out_string_at_IO
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# Allocating String
		li $v0, 9
		addi $a0, $zero, 41 # $a0 = length of string + 9 for 4 bytes for the type, 4 bytes for the length of the string and 1 byte for null-terminator
		syscall
		
		la $t0, type_String
		sw $t0, 0($v0) # Setting type in the first word of the object
		
		addi $t0, $zero, 41
		sw $t0, 4($v0) # Setting length of the string in the second word of the object
		
		addi $t0, $zero, 9
		sb $t0, 8($v0) # internal_48[0] = '\t'
		
		addi $t0, $zero, 84
		sb $t0, 9($v0) # internal_48[1] = 'T'
		
		addi $t0, $zero, 111
		sb $t0, 10($v0) # internal_48[2] = 'o'
		
		addi $t0, $zero, 32
		sb $t0, 11($v0) # internal_48[3] = ' '
		
		addi $t0, $zero, 103
		sb $t0, 12($v0) # internal_48[4] = 'g'
		
		addi $t0, $zero, 101
		sb $t0, 13($v0) # internal_48[5] = 'e'
		
		addi $t0, $zero, 116
		sb $t0, 14($v0) # internal_48[6] = 't'
		
		addi $t0, $zero, 32
		sb $t0, 15($v0) # internal_48[7] = ' '
		
		addi $t0, $zero, 97
		sb $t0, 16($v0) # internal_48[8] = 'a'
		
		addi $t0, $zero, 32
		sb $t0, 17($v0) # internal_48[9] = ' '
		
		addi $t0, $zero, 110
		sb $t0, 18($v0) # internal_48[10] = 'n'
		
		addi $t0, $zero, 101
		sb $t0, 19($v0) # internal_48[11] = 'e'
		
		addi $t0, $zero, 119
		sb $t0, 20($v0) # internal_48[12] = 'w'
		
		addi $t0, $zero, 32
		sb $t0, 21($v0) # internal_48[13] = ' '
		
		addi $t0, $zero, 110
		sb $t0, 22($v0) # internal_48[14] = 'n'
		
		addi $t0, $zero, 117
		sb $t0, 23($v0) # internal_48[15] = 'u'
		
		addi $t0, $zero, 109
		sb $t0, 24($v0) # internal_48[16] = 'm'
		
		addi $t0, $zero, 98
		sb $t0, 25($v0) # internal_48[17] = 'b'
		
		addi $t0, $zero, 101
		sb $t0, 26($v0) # internal_48[18] = 'e'
		
		addi $t0, $zero, 114
		sb $t0, 27($v0) # internal_48[19] = 'r'
		
		addi $t0, $zero, 46
		sb $t0, 28($v0) # internal_48[20] = '.'
		
		addi $t0, $zero, 46
		sb $t0, 29($v0) # internal_48[21] = '.'
		
		addi $t0, $zero, 46
		sb $t0, 30($v0) # internal_48[22] = '.'
		
		addi $t0, $zero, 101
		sb $t0, 31($v0) # internal_48[23] = 'e'
		
		addi $t0, $zero, 110
		sb $t0, 32($v0) # internal_48[24] = 'n'
		
		addi $t0, $zero, 116
		sb $t0, 33($v0) # internal_48[25] = 't'
		
		addi $t0, $zero, 101
		sb $t0, 34($v0) # internal_48[26] = 'e'
		
		addi $t0, $zero, 114
		sb $t0, 35($v0) # internal_48[27] = 'r'
		
		addi $t0, $zero, 32
		sb $t0, 36($v0) # internal_48[28] = ' '
		
		addi $t0, $zero, 106
		sb $t0, 37($v0) # internal_48[29] = 'j'
		
		addi $t0, $zero, 58
		sb $t0, 38($v0) # internal_48[30] = ':'
		
		addi $t0, $zero, 10
		sb $t0, 39($v0) # internal_48[31] = '\n'
		
		sb $zero, 40($v0) # Null-terminator at the end of the string
		
		sw $v0, 16($sp) # internal_48 = "\tTo get a new number...enter j:\n"
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument self
		lw $t0, 224($sp)
		sw $t0, 4($sp) # Storing self
		
		# Argument internal_48
		lw $t0, 28($sp)
		sw $t0, 0($sp) # Storing internal_48
		
		# Calling function function_out_string_at_IO
		jal function_out_string_at_IO
		lw $ra, 8($sp)
		sw $v1, 24($sp) # internal_49 = result of function_out_string_at_IO
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# Allocating String
		li $v0, 9
		addi $a0, $zero, 30 # $a0 = length of string + 9 for 4 bytes for the type, 4 bytes for the length of the string and 1 byte for null-terminator
		syscall
		
		la $t0, type_String
		sw $t0, 0($v0) # Setting type in the first word of the object
		
		addi $t0, $zero, 30
		sw $t0, 4($v0) # Setting length of the string in the second word of the object
		
		addi $t0, $zero, 9
		sb $t0, 8($v0) # internal_50[0] = '\t'
		
		addi $t0, $zero, 84
		sb $t0, 9($v0) # internal_50[1] = 'T'
		
		addi $t0, $zero, 111
		sb $t0, 10($v0) # internal_50[2] = 'o'
		
		addi $t0, $zero, 32
		sb $t0, 11($v0) # internal_50[3] = ' '
		
		addi $t0, $zero, 113
		sb $t0, 12($v0) # internal_50[4] = 'q'
		
		addi $t0, $zero, 117
		sb $t0, 13($v0) # internal_50[5] = 'u'
		
		addi $t0, $zero, 105
		sb $t0, 14($v0) # internal_50[6] = 'i'
		
		addi $t0, $zero, 116
		sb $t0, 15($v0) # internal_50[7] = 't'
		
		addi $t0, $zero, 46
		sb $t0, 16($v0) # internal_50[8] = '.'
		
		addi $t0, $zero, 46
		sb $t0, 17($v0) # internal_50[9] = '.'
		
		addi $t0, $zero, 46
		sb $t0, 18($v0) # internal_50[10] = '.'
		
		addi $t0, $zero, 101
		sb $t0, 19($v0) # internal_50[11] = 'e'
		
		addi $t0, $zero, 110
		sb $t0, 20($v0) # internal_50[12] = 'n'
		
		addi $t0, $zero, 116
		sb $t0, 21($v0) # internal_50[13] = 't'
		
		addi $t0, $zero, 101
		sb $t0, 22($v0) # internal_50[14] = 'e'
		
		addi $t0, $zero, 114
		sb $t0, 23($v0) # internal_50[15] = 'r'
		
		addi $t0, $zero, 32
		sb $t0, 24($v0) # internal_50[16] = ' '
		
		addi $t0, $zero, 113
		sb $t0, 25($v0) # internal_50[17] = 'q'
		
		addi $t0, $zero, 58
		sb $t0, 26($v0) # internal_50[18] = ':'
		
		addi $t0, $zero, 10
		sb $t0, 27($v0) # internal_50[19] = '\n'
		
		addi $t0, $zero, 10
		sb $t0, 28($v0) # internal_50[20] = '\n'
		
		sb $zero, 29($v0) # Null-terminator at the end of the string
		
		sw $v0, 8($sp) # internal_50 = "\tTo quit...enter q:\n\n"
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument self
		lw $t0, 224($sp)
		sw $t0, 4($sp) # Storing self
		
		# Argument internal_50
		lw $t0, 20($sp)
		sw $t0, 0($sp) # Storing internal_50
		
		# Calling function function_out_string_at_IO
		jal function_out_string_at_IO
		lw $ra, 8($sp)
		sw $v1, 16($sp) # internal_51 = result of function_out_string_at_IO
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# Passing function arguments
		addi $sp, $sp, -8 # Reserving space for arguments
		sw $ra, 4($sp) # Storing return address
		
		# Argument self
		lw $t0, 220($sp)
		sw $t0, 0($sp) # Storing self
		
		# Calling function function_in_string_at_IO
		jal function_in_string_at_IO
		lw $ra, 4($sp)
		sw $v1, 8($sp) # internal_52 = result of function_in_string_at_IO
		addi $sp, $sp, 8 # Freeing space for arguments
		
		# Loading return value in $v1
		lw $v1, 0($sp)
		
		# Freeing space for local variables
		addi $sp, $sp, 212
		
		jr $ra
		
	function_prompt_at_Main:
		# Function parameters
		#   $ra = 24($sp)
		#   self = 20($sp)
		
		# Reserving space for local variables
		addi $sp, $sp, -20
		
		# Allocating String
		li $v0, 9
		addi $a0, $zero, 10 # $a0 = length of string + 9 for 4 bytes for the type, 4 bytes for the length of the string and 1 byte for null-terminator
		syscall
		
		la $t0, type_String
		sw $t0, 0($v0) # Setting type in the first word of the object
		
		addi $t0, $zero, 10
		sw $t0, 4($v0) # Setting length of the string in the second word of the object
		
		addi $t0, $zero, 10
		sb $t0, 8($v0) # internal_0[0] = '\n'
		
		sb $zero, 9($v0) # Null-terminator at the end of the string
		
		sw $v0, 16($sp) # internal_0 = "\n"
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument self
		lw $t0, 32($sp)
		sw $t0, 4($sp) # Storing self
		
		# Argument internal_0
		lw $t0, 28($sp)
		sw $t0, 0($sp) # Storing internal_0
		
		# Calling function function_out_string_at_IO
		jal function_out_string_at_IO
		lw $ra, 8($sp)
		sw $v1, 24($sp) # internal_1 = result of function_out_string_at_IO
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# Allocating String
		li $v0, 9
		addi $a0, $zero, 35 # $a0 = length of string + 9 for 4 bytes for the type, 4 bytes for the length of the string and 1 byte for null-terminator
		syscall
		
		la $t0, type_String
		sw $t0, 0($v0) # Setting type in the first word of the object
		
		addi $t0, $zero, 35
		sw $t0, 4($v0) # Setting length of the string in the second word of the object
		
		addi $t0, $zero, 80
		sb $t0, 8($v0) # internal_2[0] = 'P'
		
		addi $t0, $zero, 108
		sb $t0, 9($v0) # internal_2[1] = 'l'
		
		addi $t0, $zero, 101
		sb $t0, 10($v0) # internal_2[2] = 'e'
		
		addi $t0, $zero, 97
		sb $t0, 11($v0) # internal_2[3] = 'a'
		
		addi $t0, $zero, 115
		sb $t0, 12($v0) # internal_2[4] = 's'
		
		addi $t0, $zero, 101
		sb $t0, 13($v0) # internal_2[5] = 'e'
		
		addi $t0, $zero, 32
		sb $t0, 14($v0) # internal_2[6] = ' '
		
		addi $t0, $zero, 101
		sb $t0, 15($v0) # internal_2[7] = 'e'
		
		addi $t0, $zero, 110
		sb $t0, 16($v0) # internal_2[8] = 'n'
		
		addi $t0, $zero, 116
		sb $t0, 17($v0) # internal_2[9] = 't'
		
		addi $t0, $zero, 101
		sb $t0, 18($v0) # internal_2[10] = 'e'
		
		addi $t0, $zero, 114
		sb $t0, 19($v0) # internal_2[11] = 'r'
		
		addi $t0, $zero, 32
		sb $t0, 20($v0) # internal_2[12] = ' '
		
		addi $t0, $zero, 97
		sb $t0, 21($v0) # internal_2[13] = 'a'
		
		addi $t0, $zero, 32
		sb $t0, 22($v0) # internal_2[14] = ' '
		
		addi $t0, $zero, 110
		sb $t0, 23($v0) # internal_2[15] = 'n'
		
		addi $t0, $zero, 117
		sb $t0, 24($v0) # internal_2[16] = 'u'
		
		addi $t0, $zero, 109
		sb $t0, 25($v0) # internal_2[17] = 'm'
		
		addi $t0, $zero, 98
		sb $t0, 26($v0) # internal_2[18] = 'b'
		
		addi $t0, $zero, 101
		sb $t0, 27($v0) # internal_2[19] = 'e'
		
		addi $t0, $zero, 114
		sb $t0, 28($v0) # internal_2[20] = 'r'
		
		addi $t0, $zero, 46
		sb $t0, 29($v0) # internal_2[21] = '.'
		
		addi $t0, $zero, 46
		sb $t0, 30($v0) # internal_2[22] = '.'
		
		addi $t0, $zero, 46
		sb $t0, 31($v0) # internal_2[23] = '.'
		
		addi $t0, $zero, 32
		sb $t0, 32($v0) # internal_2[24] = ' '
		
		addi $t0, $zero, 32
		sb $t0, 33($v0) # internal_2[25] = ' '
		
		sb $zero, 34($v0) # Null-terminator at the end of the string
		
		sw $v0, 8($sp) # internal_2 = "Please enter a number...  "
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument self
		lw $t0, 32($sp)
		sw $t0, 4($sp) # Storing self
		
		# Argument internal_2
		lw $t0, 20($sp)
		sw $t0, 0($sp) # Storing internal_2
		
		# Calling function function_out_string_at_IO
		jal function_out_string_at_IO
		lw $ra, 8($sp)
		sw $v1, 16($sp) # internal_3 = result of function_out_string_at_IO
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# Passing function arguments
		addi $sp, $sp, -8 # Reserving space for arguments
		sw $ra, 4($sp) # Storing return address
		
		# Argument self
		lw $t0, 28($sp)
		sw $t0, 0($sp) # Storing self
		
		# Calling function function_in_string_at_IO
		jal function_in_string_at_IO
		lw $ra, 4($sp)
		sw $v1, 8($sp) # internal_4 = result of function_in_string_at_IO
		addi $sp, $sp, 8 # Freeing space for arguments
		
		# Loading return value in $v1
		lw $v1, 0($sp)
		
		# Freeing space for local variables
		addi $sp, $sp, 20
		
		jr $ra
		
	function_get_int_at_Main:
		# Function parameters
		#   $ra = 24($sp)
		#   self = 20($sp)
		
		# Reserving space for local variables
		addi $sp, $sp, -20
		
		# Allocating A2I
		li $v0, 9
		lw $a0, type_A2I
		syscall
		la $t0, type_A2I # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of th object
		sw $a0, 4($v0) # Setting size in the second word of th object
		sw $v0, 12($sp) # internal_1 = address of allocated object A2I
		
		# Passing function arguments
		addi $sp, $sp, -8 # Reserving space for arguments
		sw $ra, 4($sp) # Storing return address
		
		# Argument internal_1
		lw $t0, 20($sp)
		sw $t0, 0($sp) # Storing internal_1
		
		# Calling function function___init___at_A2I
		jal function___init___at_A2I
		lw $ra, 4($sp)
		sw $v1, 20($sp) # internal_1 = result of function___init___at_A2I
		addi $sp, $sp, 8 # Freeing space for arguments
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument z
		lw $t0, 28($sp)
		sw $t0, 4($sp) # Storing z
		
		# Argument internal_1
		lw $t0, 24($sp)
		sw $t0, 0($sp) # Storing internal_1
		
		# Calling function function_assign
		jal function_assign
		lw $ra, 8($sp)
		sw $v1, 28($sp) # z = result of function_assign
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# Passing function arguments
		addi $sp, $sp, -8 # Reserving space for arguments
		sw $ra, 4($sp) # Storing return address
		
		# Argument self
		lw $t0, 28($sp)
		sw $t0, 0($sp) # Storing self
		
		# Calling function function_prompt_at_Main
		jal function_prompt_at_Main
		lw $ra, 4($sp)
		sw $v1, 12($sp) # internal_3 = result of function_prompt_at_Main
		addi $sp, $sp, 8 # Freeing space for arguments
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument s
		lw $t0, 20($sp)
		sw $t0, 4($sp) # Storing s
		
		# Argument internal_3
		lw $t0, 16($sp)
		sw $t0, 0($sp) # Storing internal_3
		
		# Calling function function_assign
		jal function_assign
		lw $ra, 8($sp)
		sw $v1, 20($sp) # s = result of function_assign
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument z
		lw $t0, 28($sp)
		sw $t0, 4($sp) # Storing z
		
		# Argument s
		lw $t0, 20($sp)
		sw $t0, 0($sp) # Storing s
		
		# Calling function function_a2i_at_A2I
		jal function_a2i_at_A2I
		lw $ra, 8($sp)
		sw $v1, 12($sp) # internal_4 = result of function_a2i_at_A2I
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# Loading return value in $v1
		lw $v1, 0($sp)
		
		# Freeing space for local variables
		addi $sp, $sp, 20
		
		jr $ra
		
	function_is_even_at_Main:
		# Function parameters
		#   $ra = 96($sp)
		#   self = 92($sp)
		#   num = 88($sp)
		
		# Reserving space for local variables
		addi $sp, $sp, -88
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument x
		lw $t0, 96($sp)
		sw $t0, 4($sp) # Storing x
		
		# Argument num
		lw $t0, 100($sp)
		sw $t0, 0($sp) # Storing num
		
		# Calling function function_assign
		jal function_assign
		lw $ra, 8($sp)
		sw $v1, 96($sp) # x = result of function_assign
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# Allocating Bool 0
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Bool # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 0
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 76($sp) # internal_2 = address of allocated object Int
		
		# Allocating Int 0
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Int # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 0
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 72($sp) # internal_3 = address of allocated object Int
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument x
		lw $t0, 96($sp)
		sw $t0, 4($sp) # Storing x
		
		# Argument internal_3
		lw $t0, 84($sp)
		sw $t0, 0($sp) # Storing internal_3
		
		# Calling function function_less_than
		jal function_less_than
		lw $ra, 8($sp)
		sw $v1, 80($sp) # internal_4 = result of function_less_than
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# internal_2 = internal_4
		lw $t0, 68($sp)
		sw $t0, 76($sp)
		
		# If internal_2 then goto then_8781702295071
		lw $t0, 76($sp) # Loading the address of the condition
		lw $t0, 8($t0) # Loading the value of the condition
		addi $t1, $zero, 1 # Setting the value to 1 for comparison
		beq $t0, $t1, then_8781702295071
		
		# Jumping to else_8781702295071
		j else_8781702295071
		
		then_8781702295071:
		
		# Allocating Int 1
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Int # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 1
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 64($sp) # internal_5 = address of allocated object Int
		
		# Allocating Int 4294967295
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Int # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 4294967295
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 60($sp) # internal_6 = address of allocated object Int
		
		# Allocating Int 0
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Int # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 0
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 56($sp) # internal_7 = address of allocated object Int
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument x
		lw $t0, 96($sp)
		sw $t0, 4($sp) # Storing x
		
		# Argument internal_6
		lw $t0, 72($sp)
		sw $t0, 0($sp) # Storing internal_6
		
		# Calling function function_xor
		jal function_xor
		lw $ra, 8($sp)
		sw $v1, 68($sp) # internal_7 = result of function_xor
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument internal_7
		lw $t0, 68($sp)
		sw $t0, 4($sp) # Storing internal_7
		
		# Argument internal_5
		lw $t0, 76($sp)
		sw $t0, 0($sp) # Storing internal_5
		
		# Calling function function_add
		jal function_add
		lw $ra, 8($sp)
		sw $v1, 68($sp) # internal_7 = result of function_add
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument self
		lw $t0, 104($sp)
		sw $t0, 4($sp) # Storing self
		
		# Argument internal_7
		lw $t0, 68($sp)
		sw $t0, 0($sp) # Storing internal_7
		
		# Calling function function_is_even_at_Main
		jal function_is_even_at_Main
		lw $ra, 8($sp)
		sw $v1, 64($sp) # internal_8 = result of function_is_even_at_Main
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# internal_1 = internal_8
		lw $t0, 52($sp)
		sw $t0, 80($sp)
		
		# Jumping to endif_8781702295071
		j endif_8781702295071
		
		else_8781702295071:
		
		# Allocating Bool 0
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Bool # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 0
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 44($sp) # internal_10 = address of allocated object Int
		
		# Allocating Int 0
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Int # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 0
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 40($sp) # internal_11 = address of allocated object Int
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument internal_11
		lw $t0, 52($sp)
		sw $t0, 4($sp) # Storing internal_11
		
		# Argument x
		lw $t0, 96($sp)
		sw $t0, 0($sp) # Storing x
		
		# Calling function function_equal
		jal function_equal
		lw $ra, 8($sp)
		sw $v1, 48($sp) # internal_12 = result of function_equal
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# internal_10 = internal_12
		lw $t0, 36($sp)
		sw $t0, 44($sp)
		
		# If internal_10 then goto then_8781702295074
		lw $t0, 44($sp) # Loading the address of the condition
		lw $t0, 8($t0) # Loading the value of the condition
		addi $t1, $zero, 1 # Setting the value to 1 for comparison
		beq $t0, $t1, then_8781702295074
		
		# Jumping to else_8781702295074
		j else_8781702295074
		
		then_8781702295074:
		
		# Allocating Bool 1
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Bool # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 1
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 32($sp) # internal_13 = address of allocated object Int
		
		# internal_9 = internal_13
		lw $t0, 32($sp)
		sw $t0, 48($sp)
		
		# Jumping to endif_8781702295074
		j endif_8781702295074
		
		else_8781702295074:
		
		# Allocating Bool 0
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Bool # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 0
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 24($sp) # internal_15 = address of allocated object Int
		
		# Allocating Int 1
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Int # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 1
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 20($sp) # internal_16 = address of allocated object Int
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument internal_16
		lw $t0, 32($sp)
		sw $t0, 4($sp) # Storing internal_16
		
		# Argument x
		lw $t0, 96($sp)
		sw $t0, 0($sp) # Storing x
		
		# Calling function function_equal
		jal function_equal
		lw $ra, 8($sp)
		sw $v1, 28($sp) # internal_17 = result of function_equal
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# internal_15 = internal_17
		lw $t0, 16($sp)
		sw $t0, 24($sp)
		
		# If internal_15 then goto then_8781702295080
		lw $t0, 24($sp) # Loading the address of the condition
		lw $t0, 8($t0) # Loading the value of the condition
		addi $t1, $zero, 1 # Setting the value to 1 for comparison
		beq $t0, $t1, then_8781702295080
		
		# Jumping to else_8781702295080
		j else_8781702295080
		
		then_8781702295080:
		
		# Allocating Bool 0
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Bool # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 0
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 12($sp) # internal_18 = address of allocated object Int
		
		# internal_14 = internal_18
		lw $t0, 12($sp)
		sw $t0, 28($sp)
		
		# Jumping to endif_8781702295080
		j endif_8781702295080
		
		else_8781702295080:
		
		# Allocating Int 2
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Int # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 2
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 8($sp) # internal_19 = address of allocated object Int
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument x
		lw $t0, 96($sp)
		sw $t0, 4($sp) # Storing x
		
		# Argument internal_19
		lw $t0, 20($sp)
		sw $t0, 0($sp) # Storing internal_19
		
		# Calling function function_sub
		jal function_sub
		lw $ra, 8($sp)
		sw $v1, 16($sp) # internal_20 = result of function_sub
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument self
		lw $t0, 104($sp)
		sw $t0, 4($sp) # Storing self
		
		# Argument internal_20
		lw $t0, 16($sp)
		sw $t0, 0($sp) # Storing internal_20
		
		# Calling function function_is_even_at_Main
		jal function_is_even_at_Main
		lw $ra, 8($sp)
		sw $v1, 12($sp) # internal_21 = result of function_is_even_at_Main
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# internal_14 = internal_21
		lw $t0, 0($sp)
		sw $t0, 28($sp)
		
		# Jumping to endif_8781702295080
		j endif_8781702295080
		
		endif_8781702295080:
		
		# internal_9 = internal_14
		lw $t0, 28($sp)
		sw $t0, 48($sp)
		
		# Jumping to endif_8781702295074
		j endif_8781702295074
		
		endif_8781702295074:
		
		# internal_1 = internal_9
		lw $t0, 48($sp)
		sw $t0, 80($sp)
		
		# Jumping to endif_8781702295071
		j endif_8781702295071
		
		endif_8781702295071:
		
		# Loading return value in $v1
		lw $v1, 80($sp)
		
		# Freeing space for local variables
		addi $sp, $sp, 88
		
		jr $ra
		
	function_class_type_at_Main:
		# Function parameters
		#   $ra = 300($sp)
		#   self = 296($sp)
		#   var = 292($sp)
		
		# Reserving space for local variables
		addi $sp, $sp, -292
		
		# Allocating Int 0
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Int # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 0
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 288($sp) # internal_0 = address of allocated object Int
		
		# Allocating Int 1
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Int # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 1
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 284($sp) # internal_1 = address of allocated object Int
		
		# Allocating Int 6
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Int # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 6
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 280($sp) # internal_2 = address of allocated object Int
		
		# Allocating NUll to internal_3
		sw $zero, 276($sp) # internal_3 = 0
		
		# Allocating Int 0
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Int # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 0
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 272($sp) # internal_4 = address of allocated object Int
		
		# Allocating Bool 0
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Bool # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 0
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 260($sp) # internal_7 = address of allocated object Int
		
		# internal_5 = typeof var that is the first word of the object
		lw $t0, 292($sp)
		lw $t0, 0($t0)
		sw $t0, 268($sp)
		
		# internal_6 = internal_5
		lw $t0, 268($sp)
		sw $t0, 264($sp)
		
		while_start_8781702295173:
		
		# internal_7 = EqualAddress(internal_6, internal_3)
		lw $t0, 264($sp)
		lw $t1, 276($sp)
		seq $t2, $t0, $t1
		lw $t0, 260($sp)
		sw $t2, 8($t0)
		
		# If internal_7 then goto while_end_8781702295173
		lw $t0, 260($sp) # Loading the address of the condition
		lw $t0, 8($t0) # Loading the value of the condition
		addi $t1, $zero, 1 # Setting the value to 1 for comparison
		beq $t0, $t1, while_end_8781702295173
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument internal_4
		lw $t0, 284($sp)
		sw $t0, 4($sp) # Storing internal_4
		
		# Argument internal_1
		lw $t0, 296($sp)
		sw $t0, 0($sp) # Storing internal_1
		
		# Calling function function_add
		jal function_add
		lw $ra, 8($sp)
		sw $v1, 284($sp) # internal_4 = result of function_add
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# internal_6 = ancestor of internal_6
		lw $t0, 264($sp)
		lw $t0, 4($t0)
		sw $t0, 264($sp)
		
		# Jumping to while_start_8781702295173
		j while_start_8781702295173
		
		while_end_8781702295173:
		
		# internal_6 = internal_5
		lw $t0, 268($sp)
		sw $t0, 264($sp)
		
		# initialize Array [internal_4]
		lw $t0, 272($sp) # $t0 = internal_4
		lw $t0, 8($t0) # $t0 = value of the size
		addi $t1, $zero, 4 # $t1 = 4
		mult $t0, $t1 # $t0 = $t0 * 4
		mflo $t0
		li $v0, 9
		move $a0, $t0
		syscall
		sw $v0, 256($sp) # internal_8 = new Array[internal_4]
		
		# Allocating Int 0
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Int # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 0
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 252($sp) # internal_9 = address of allocated object Int
		
		# Allocating Bool 0
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Bool # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 0
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 248($sp) # internal_10 = address of allocated object Int
		
		foreach_start_8781702295173:
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument internal_9
		lw $t0, 264($sp)
		sw $t0, 4($sp) # Storing internal_9
		
		# Argument internal_4
		lw $t0, 284($sp)
		sw $t0, 0($sp) # Storing internal_4
		
		# Calling function function_less_than
		jal function_less_than
		lw $ra, 8($sp)
		sw $v1, 260($sp) # internal_10 = result of function_less_than
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# If internal_10 then goto foreach_body_8781702295173
		lw $t0, 248($sp) # Loading the address of the condition
		lw $t0, 8($t0) # Loading the value of the condition
		addi $t1, $zero, 1 # Setting the value to 1 for comparison
		beq $t0, $t1, foreach_body_8781702295173
		
		# Jumping to foreach_end_8781702295173
		j foreach_end_8781702295173
		
		foreach_body_8781702295173:
		
		# array internal_8[4 * internal_9] = internal_6
		lw $t0, 252($sp) # $t0 = internal_9
		lw $t0, 8($t0) # $t0 = value of the index
		addi $t1, $zero, 4 # $t1 = 4
		mult $t0, $t1 # $t0 = $t0 * 4
		mflo $t0
		lw $t1, 256($sp) # $t1 = internal_8
		add $t1, $t1, $t0 # Move the pointer to the index
		lw $t0, 264($sp)
		sw $t0, 0($t1)
		
		# internal_6 = ancestor of internal_6
		lw $t0, 264($sp)
		lw $t0, 4($t0)
		sw $t0, 264($sp)
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument internal_9
		lw $t0, 264($sp)
		sw $t0, 4($sp) # Storing internal_9
		
		# Argument internal_1
		lw $t0, 296($sp)
		sw $t0, 0($sp) # Storing internal_1
		
		# Calling function function_add
		jal function_add
		lw $ra, 8($sp)
		sw $v1, 264($sp) # internal_9 = result of function_add
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# Jumping to foreach_start_8781702295173
		j foreach_start_8781702295173
		
		foreach_end_8781702295173:
		
		# initialize Array [internal_2]
		lw $t0, 280($sp) # $t0 = internal_2
		lw $t0, 8($t0) # $t0 = value of the size
		addi $t1, $zero, 4 # $t1 = 4
		mult $t0, $t1 # $t0 = $t0 * 4
		mflo $t0
		li $v0, 9
		move $a0, $t0
		syscall
		sw $v0, 244($sp) # internal_11 = new Array[internal_2]
		
		# initialize Array [internal_2]
		lw $t0, 280($sp) # $t0 = internal_2
		lw $t0, 8($t0) # $t0 = value of the size
		addi $t1, $zero, 4 # $t1 = 4
		mult $t0, $t1 # $t0 = $t0 * 4
		mflo $t0
		li $v0, 9
		move $a0, $t0
		syscall
		sw $v0, 240($sp) # internal_12 = new Array[internal_2]
		
		# Allocating Int 0
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Int # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 0
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 232($sp) # internal_14 = address of allocated object Int
		
		# internal_13 = direction of A
		la $t0, type_A
		sw $t0, 236($sp)
		
		# array internal_11[4 * internal_14] = internal_13
		lw $t0, 232($sp) # $t0 = internal_14
		lw $t0, 8($t0) # $t0 = value of the index
		addi $t1, $zero, 4 # $t1 = 4
		mult $t0, $t1 # $t0 = $t0 * 4
		mflo $t0
		lw $t1, 244($sp) # $t1 = internal_11
		add $t1, $t1, $t0 # Move the pointer to the index
		lw $t0, 236($sp)
		sw $t0, 0($t1)
		
		# array internal_12[4 * internal_14] = internal_4
		lw $t0, 232($sp) # $t0 = internal_14
		lw $t0, 8($t0) # $t0 = value of the index
		addi $t1, $zero, 4 # $t1 = 4
		mult $t0, $t1 # $t0 = $t0 * 4
		mflo $t0
		lw $t1, 240($sp) # $t1 = internal_12
		add $t1, $t1, $t0 # Move the pointer to the index
		lw $t0, 272($sp)
		lw $t0, 8($t0)
		sw $t0, 0($t1)
		
		# Allocating Int 1
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Int # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 1
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 224($sp) # internal_16 = address of allocated object Int
		
		# internal_15 = direction of B
		la $t0, type_B
		sw $t0, 228($sp)
		
		# array internal_11[4 * internal_16] = internal_15
		lw $t0, 224($sp) # $t0 = internal_16
		lw $t0, 8($t0) # $t0 = value of the index
		addi $t1, $zero, 4 # $t1 = 4
		mult $t0, $t1 # $t0 = $t0 * 4
		mflo $t0
		lw $t1, 244($sp) # $t1 = internal_11
		add $t1, $t1, $t0 # Move the pointer to the index
		lw $t0, 228($sp)
		sw $t0, 0($t1)
		
		# array internal_12[4 * internal_16] = internal_4
		lw $t0, 224($sp) # $t0 = internal_16
		lw $t0, 8($t0) # $t0 = value of the index
		addi $t1, $zero, 4 # $t1 = 4
		mult $t0, $t1 # $t0 = $t0 * 4
		mflo $t0
		lw $t1, 240($sp) # $t1 = internal_12
		add $t1, $t1, $t0 # Move the pointer to the index
		lw $t0, 272($sp)
		lw $t0, 8($t0)
		sw $t0, 0($t1)
		
		# Allocating Int 2
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Int # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 2
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 216($sp) # internal_18 = address of allocated object Int
		
		# internal_17 = direction of C
		la $t0, type_C
		sw $t0, 220($sp)
		
		# array internal_11[4 * internal_18] = internal_17
		lw $t0, 216($sp) # $t0 = internal_18
		lw $t0, 8($t0) # $t0 = value of the index
		addi $t1, $zero, 4 # $t1 = 4
		mult $t0, $t1 # $t0 = $t0 * 4
		mflo $t0
		lw $t1, 244($sp) # $t1 = internal_11
		add $t1, $t1, $t0 # Move the pointer to the index
		lw $t0, 220($sp)
		sw $t0, 0($t1)
		
		# array internal_12[4 * internal_18] = internal_4
		lw $t0, 216($sp) # $t0 = internal_18
		lw $t0, 8($t0) # $t0 = value of the index
		addi $t1, $zero, 4 # $t1 = 4
		mult $t0, $t1 # $t0 = $t0 * 4
		mflo $t0
		lw $t1, 240($sp) # $t1 = internal_12
		add $t1, $t1, $t0 # Move the pointer to the index
		lw $t0, 272($sp)
		lw $t0, 8($t0)
		sw $t0, 0($t1)
		
		# Allocating Int 3
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Int # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 3
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 208($sp) # internal_20 = address of allocated object Int
		
		# internal_19 = direction of D
		la $t0, type_D
		sw $t0, 212($sp)
		
		# array internal_11[4 * internal_20] = internal_19
		lw $t0, 208($sp) # $t0 = internal_20
		lw $t0, 8($t0) # $t0 = value of the index
		addi $t1, $zero, 4 # $t1 = 4
		mult $t0, $t1 # $t0 = $t0 * 4
		mflo $t0
		lw $t1, 244($sp) # $t1 = internal_11
		add $t1, $t1, $t0 # Move the pointer to the index
		lw $t0, 212($sp)
		sw $t0, 0($t1)
		
		# array internal_12[4 * internal_20] = internal_4
		lw $t0, 208($sp) # $t0 = internal_20
		lw $t0, 8($t0) # $t0 = value of the index
		addi $t1, $zero, 4 # $t1 = 4
		mult $t0, $t1 # $t0 = $t0 * 4
		mflo $t0
		lw $t1, 240($sp) # $t1 = internal_12
		add $t1, $t1, $t0 # Move the pointer to the index
		lw $t0, 272($sp)
		lw $t0, 8($t0)
		sw $t0, 0($t1)
		
		# Allocating Int 4
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Int # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 4
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 200($sp) # internal_22 = address of allocated object Int
		
		# internal_21 = direction of E
		la $t0, type_E
		sw $t0, 204($sp)
		
		# array internal_11[4 * internal_22] = internal_21
		lw $t0, 200($sp) # $t0 = internal_22
		lw $t0, 8($t0) # $t0 = value of the index
		addi $t1, $zero, 4 # $t1 = 4
		mult $t0, $t1 # $t0 = $t0 * 4
		mflo $t0
		lw $t1, 244($sp) # $t1 = internal_11
		add $t1, $t1, $t0 # Move the pointer to the index
		lw $t0, 204($sp)
		sw $t0, 0($t1)
		
		# array internal_12[4 * internal_22] = internal_4
		lw $t0, 200($sp) # $t0 = internal_22
		lw $t0, 8($t0) # $t0 = value of the index
		addi $t1, $zero, 4 # $t1 = 4
		mult $t0, $t1 # $t0 = $t0 * 4
		mflo $t0
		lw $t1, 240($sp) # $t1 = internal_12
		add $t1, $t1, $t0 # Move the pointer to the index
		lw $t0, 272($sp)
		lw $t0, 8($t0)
		sw $t0, 0($t1)
		
		# Allocating Int 5
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Int # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 5
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 192($sp) # internal_24 = address of allocated object Int
		
		# internal_23 = direction of Object
		la $t0, type_Object
		sw $t0, 196($sp)
		
		# array internal_11[4 * internal_24] = internal_23
		lw $t0, 192($sp) # $t0 = internal_24
		lw $t0, 8($t0) # $t0 = value of the index
		addi $t1, $zero, 4 # $t1 = 4
		mult $t0, $t1 # $t0 = $t0 * 4
		mflo $t0
		lw $t1, 244($sp) # $t1 = internal_11
		add $t1, $t1, $t0 # Move the pointer to the index
		lw $t0, 196($sp)
		sw $t0, 0($t1)
		
		# array internal_12[4 * internal_24] = internal_4
		lw $t0, 192($sp) # $t0 = internal_24
		lw $t0, 8($t0) # $t0 = value of the index
		addi $t1, $zero, 4 # $t1 = 4
		mult $t0, $t1 # $t0 = $t0 * 4
		mflo $t0
		lw $t1, 240($sp) # $t1 = internal_12
		add $t1, $t1, $t0 # Move the pointer to the index
		lw $t0, 272($sp)
		lw $t0, 8($t0)
		sw $t0, 0($t1)
		
		# Allocating Int 0
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Int # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 0
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 188($sp) # internal_25 = address of allocated object Int
		
		# Allocating Bool 0
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Bool # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 0
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 184($sp) # internal_26 = address of allocated object Int
		
		# Allocating Int 0
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Int # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 0
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 176($sp) # internal_28 = address of allocated object Int
		
		# Allocating Bool 0
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Bool # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 0
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 172($sp) # internal_29 = address of allocated object Int
		
		# Allocating Bool 0
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Bool # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 0
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 164($sp) # internal_31 = address of allocated object Int
		
		foreach_type_start_8781702295173:
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument internal_25
		lw $t0, 200($sp)
		sw $t0, 4($sp) # Storing internal_25
		
		# Argument internal_2
		lw $t0, 292($sp)
		sw $t0, 0($sp) # Storing internal_2
		
		# Calling function function_less_than
		jal function_less_than
		lw $ra, 8($sp)
		sw $v1, 196($sp) # internal_26 = result of function_less_than
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# If internal_26 then goto foreach_type_body_8781702295173
		lw $t0, 184($sp) # Loading the address of the condition
		lw $t0, 8($t0) # Loading the value of the condition
		addi $t1, $zero, 1 # Setting the value to 1 for comparison
		beq $t0, $t1, foreach_type_body_8781702295173
		
		# Jumping to foreach_type_end_8781702295173
		j foreach_type_end_8781702295173
		
		foreach_type_body_8781702295173:
		
		# internal_27 = array internal_11[4 * internal_25]
		lw $t0, 188($sp) # $t0 = internal_25
		lw $t0, 8($t0) # $t0 = value of the index
		addi $t1, $zero, 4 # $t1 = 4
		mult $t0, $t1 # $t0 = $t0 * 4
		mflo $t0
		lw $t1, 244($sp) # $t1 = internal_11
		add $t1, $t1, $t0 # Move the pointer to the index
		lw $t0, 0($t1) # $t1 = value in the position
		sw $t0, 180($sp) # internal_27 = array internal_11[4 * internal_25]
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument internal_28
		lw $t0, 188($sp)
		sw $t0, 4($sp) # Storing internal_28
		
		# Argument internal_0
		lw $t0, 300($sp)
		sw $t0, 0($sp) # Storing internal_0
		
		# Calling function function_assign
		jal function_assign
		lw $ra, 8($sp)
		sw $v1, 188($sp) # internal_28 = result of function_assign
		addi $sp, $sp, 12 # Freeing space for arguments
		
		foreach_ancestor_start_8781702295173:
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument internal_28
		lw $t0, 188($sp)
		sw $t0, 4($sp) # Storing internal_28
		
		# Argument internal_4
		lw $t0, 284($sp)
		sw $t0, 0($sp) # Storing internal_4
		
		# Calling function function_less_than
		jal function_less_than
		lw $ra, 8($sp)
		sw $v1, 184($sp) # internal_29 = result of function_less_than
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# If internal_29 then goto foreach_ancestor_body_8781702295173
		lw $t0, 172($sp) # Loading the address of the condition
		lw $t0, 8($t0) # Loading the value of the condition
		addi $t1, $zero, 1 # Setting the value to 1 for comparison
		beq $t0, $t1, foreach_ancestor_body_8781702295173
		
		# Jumping to foreach_ancestor_end_8781702295173
		j foreach_ancestor_end_8781702295173
		
		foreach_ancestor_body_8781702295173:
		
		# internal_30 = array internal_8[4 * internal_28]
		lw $t0, 176($sp) # $t0 = internal_28
		lw $t0, 8($t0) # $t0 = value of the index
		addi $t1, $zero, 4 # $t1 = 4
		mult $t0, $t1 # $t0 = $t0 * 4
		mflo $t0
		lw $t1, 256($sp) # $t1 = internal_8
		add $t1, $t1, $t0 # Move the pointer to the index
		lw $t0, 0($t1) # $t1 = value in the position
		sw $t0, 168($sp) # internal_30 = array internal_8[4 * internal_28]
		
		# internal_31 = EqualAddress(internal_27, internal_30)
		lw $t0, 180($sp)
		lw $t1, 168($sp)
		seq $t2, $t0, $t1
		lw $t0, 164($sp)
		sw $t2, 8($t0)
		
		# If internal_31 then goto foreach_ancestor_end_8781702295173
		lw $t0, 164($sp) # Loading the address of the condition
		lw $t0, 8($t0) # Loading the value of the condition
		addi $t1, $zero, 1 # Setting the value to 1 for comparison
		beq $t0, $t1, foreach_ancestor_end_8781702295173
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument internal_28
		lw $t0, 188($sp)
		sw $t0, 4($sp) # Storing internal_28
		
		# Argument internal_1
		lw $t0, 296($sp)
		sw $t0, 0($sp) # Storing internal_1
		
		# Calling function function_add
		jal function_add
		lw $ra, 8($sp)
		sw $v1, 188($sp) # internal_28 = result of function_add
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# Jumping to foreach_ancestor_start_8781702295173
		j foreach_ancestor_start_8781702295173
		
		foreach_ancestor_end_8781702295173:
		
		# array internal_12[4 * internal_25] = internal_28
		lw $t0, 188($sp) # $t0 = internal_25
		lw $t0, 8($t0) # $t0 = value of the index
		addi $t1, $zero, 4 # $t1 = 4
		mult $t0, $t1 # $t0 = $t0 * 4
		mflo $t0
		lw $t1, 240($sp) # $t1 = internal_12
		add $t1, $t1, $t0 # Move the pointer to the index
		lw $t0, 176($sp)
		lw $t0, 8($t0)
		sw $t0, 0($t1)
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument internal_25
		lw $t0, 200($sp)
		sw $t0, 4($sp) # Storing internal_25
		
		# Argument internal_1
		lw $t0, 296($sp)
		sw $t0, 0($sp) # Storing internal_1
		
		# Calling function function_add
		jal function_add
		lw $ra, 8($sp)
		sw $v1, 200($sp) # internal_25 = result of function_add
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# Jumping to foreach_type_start_8781702295173
		j foreach_type_start_8781702295173
		
		foreach_type_end_8781702295173:
		
		# Allocating String
		li $v0, 9
		addi $a0, $zero, 10 # $a0 = length of string + 9 for 4 bytes for the type, 4 bytes for the length of the string and 1 byte for null-terminator
		syscall
		
		la $t0, type_String
		sw $t0, 0($v0) # Setting type in the first word of the object
		
		addi $t0, $zero, 10
		sw $t0, 4($v0) # Setting length of the string in the second word of the object
		
		addi $t0, $zero, 10
		sb $t0, 8($v0) # internal_37[0] = '\n'
		
		sb $zero, 9($v0) # Null-terminator at the end of the string
		
		sw $v0, 140($sp) # internal_37 = "\n"
		
		# Allocating String
		li $v0, 9
		addi $a0, $zero, 10 # $a0 = length of string + 9 for 4 bytes for the type, 4 bytes for the length of the string and 1 byte for null-terminator
		syscall
		
		la $t0, type_String
		sw $t0, 0($v0) # Setting type in the first word of the object
		
		addi $t0, $zero, 10
		sw $t0, 4($v0) # Setting length of the string in the second word of the object
		
		addi $t0, $zero, 32
		sb $t0, 8($v0) # internal_38[0] = ' '
		
		sb $zero, 9($v0) # Null-terminator at the end of the string
		
		sw $v0, 136($sp) # internal_38 = " "
		
		# Allocating Int 0
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Int # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 0
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 160($sp) # internal_32 = address of allocated object Int
		
		# Allocating Int 0
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Int # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 0
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 156($sp) # internal_33 = address of allocated object Int
		
		# Allocating Int 0
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Int # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 0
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 152($sp) # internal_34 = address of allocated object Int
		
		# Allocating Int 0
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Int # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 0
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 148($sp) # internal_35 = address of allocated object Int
		
		# Allocating Bool 0
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Bool # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 0
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 144($sp) # internal_36 = address of allocated object Int
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument internal_35
		lw $t0, 160($sp)
		sw $t0, 4($sp) # Storing internal_35
		
		# Argument internal_4
		lw $t0, 284($sp)
		sw $t0, 0($sp) # Storing internal_4
		
		# Calling function function_assign
		jal function_assign
		lw $ra, 8($sp)
		sw $v1, 160($sp) # internal_35 = result of function_assign
		addi $sp, $sp, 12 # Freeing space for arguments
		
		foreach_min_start_8781702295173:
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument internal_32
		lw $t0, 172($sp)
		sw $t0, 4($sp) # Storing internal_32
		
		# Argument internal_2
		lw $t0, 292($sp)
		sw $t0, 0($sp) # Storing internal_2
		
		# Calling function function_less_than
		jal function_less_than
		lw $ra, 8($sp)
		sw $v1, 156($sp) # internal_36 = result of function_less_than
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# If internal_36 then goto foreach_min_body_8781702295173
		lw $t0, 144($sp) # Loading the address of the condition
		lw $t0, 8($t0) # Loading the value of the condition
		addi $t1, $zero, 1 # Setting the value to 1 for comparison
		beq $t0, $t1, foreach_min_body_8781702295173
		
		# Jumping to foreach_min_end_8781702295173
		j foreach_min_end_8781702295173
		
		foreach_min_body_8781702295173:
		
		# internal_34 = array internal_12[4 * internal_32]
		lw $t0, 160($sp) # $t0 = internal_32
		lw $t0, 8($t0) # $t0 = value of the index
		addi $t1, $zero, 4 # $t1 = 4
		mult $t0, $t1 # $t0 = $t0 * 4
		mflo $t0
		lw $t1, 240($sp) # $t1 = internal_12
		add $t1, $t1, $t0 # Move the pointer to the index
		lw $t0, 0($t1) # $t1 = value in the position
		lw $t2, 152($sp) # internal_34 = array internal_12[4 * internal_32]
		sw $t0, 8($t2)
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument internal_34
		lw $t0, 164($sp)
		sw $t0, 4($sp) # Storing internal_34
		
		# Argument internal_35
		lw $t0, 160($sp)
		sw $t0, 0($sp) # Storing internal_35
		
		# Calling function function_less_than
		jal function_less_than
		lw $ra, 8($sp)
		sw $v1, 156($sp) # internal_36 = result of function_less_than
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# If internal_36 then goto update_min_8781702295173
		lw $t0, 144($sp) # Loading the address of the condition
		lw $t0, 8($t0) # Loading the value of the condition
		addi $t1, $zero, 1 # Setting the value to 1 for comparison
		beq $t0, $t1, update_min_8781702295173
		
		# Jumping to update_min_end_8781702295173
		j update_min_end_8781702295173
		
		update_min_8781702295173:
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument internal_35
		lw $t0, 160($sp)
		sw $t0, 4($sp) # Storing internal_35
		
		# Argument internal_34
		lw $t0, 164($sp)
		sw $t0, 0($sp) # Storing internal_34
		
		# Calling function function_assign
		jal function_assign
		lw $ra, 8($sp)
		sw $v1, 160($sp) # internal_35 = result of function_assign
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument internal_33
		lw $t0, 168($sp)
		sw $t0, 4($sp) # Storing internal_33
		
		# Argument internal_32
		lw $t0, 172($sp)
		sw $t0, 0($sp) # Storing internal_32
		
		# Calling function function_assign
		jal function_assign
		lw $ra, 8($sp)
		sw $v1, 168($sp) # internal_33 = result of function_assign
		addi $sp, $sp, 12 # Freeing space for arguments
		
		update_min_end_8781702295173:
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument internal_32
		lw $t0, 172($sp)
		sw $t0, 4($sp) # Storing internal_32
		
		# Argument internal_1
		lw $t0, 296($sp)
		sw $t0, 0($sp) # Storing internal_1
		
		# Calling function function_add
		jal function_add
		lw $ra, 8($sp)
		sw $v1, 172($sp) # internal_32 = result of function_add
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# Jumping to foreach_min_start_8781702295173
		j foreach_min_start_8781702295173
		
		foreach_min_end_8781702295173:
		
		# initialize Array [internal_2]
		lw $t0, 280($sp) # $t0 = internal_2
		lw $t0, 8($t0) # $t0 = value of the size
		addi $t1, $zero, 4 # $t1 = 4
		mult $t0, $t1 # $t0 = $t0 * 4
		mflo $t0
		li $v0, 9
		move $a0, $t0
		syscall
		sw $v0, 132($sp) # internal_39 = new Array[internal_2]
		
		# Allocating Int 0
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Int # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 0
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 128($sp) # internal_40 = address of allocated object Int
		
		# array internal_39[4 * internal_40] = internal_0
		lw $t0, 128($sp) # $t0 = internal_40
		lw $t0, 8($t0) # $t0 = value of the index
		addi $t1, $zero, 4 # $t1 = 4
		mult $t0, $t1 # $t0 = $t0 * 4
		mflo $t0
		lw $t1, 132($sp) # $t1 = internal_39
		add $t1, $t1, $t0 # Move the pointer to the index
		lw $t0, 288($sp)
		lw $t0, 8($t0)
		sw $t0, 0($t1)
		
		# Allocating Int 1
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Int # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 1
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 124($sp) # internal_41 = address of allocated object Int
		
		# array internal_39[4 * internal_41] = internal_0
		lw $t0, 124($sp) # $t0 = internal_41
		lw $t0, 8($t0) # $t0 = value of the index
		addi $t1, $zero, 4 # $t1 = 4
		mult $t0, $t1 # $t0 = $t0 * 4
		mflo $t0
		lw $t1, 132($sp) # $t1 = internal_39
		add $t1, $t1, $t0 # Move the pointer to the index
		lw $t0, 288($sp)
		lw $t0, 8($t0)
		sw $t0, 0($t1)
		
		# Allocating Int 2
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Int # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 2
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 120($sp) # internal_42 = address of allocated object Int
		
		# array internal_39[4 * internal_42] = internal_0
		lw $t0, 120($sp) # $t0 = internal_42
		lw $t0, 8($t0) # $t0 = value of the index
		addi $t1, $zero, 4 # $t1 = 4
		mult $t0, $t1 # $t0 = $t0 * 4
		mflo $t0
		lw $t1, 132($sp) # $t1 = internal_39
		add $t1, $t1, $t0 # Move the pointer to the index
		lw $t0, 288($sp)
		lw $t0, 8($t0)
		sw $t0, 0($t1)
		
		# Allocating Int 3
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Int # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 3
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 116($sp) # internal_43 = address of allocated object Int
		
		# array internal_39[4 * internal_43] = internal_0
		lw $t0, 116($sp) # $t0 = internal_43
		lw $t0, 8($t0) # $t0 = value of the index
		addi $t1, $zero, 4 # $t1 = 4
		mult $t0, $t1 # $t0 = $t0 * 4
		mflo $t0
		lw $t1, 132($sp) # $t1 = internal_39
		add $t1, $t1, $t0 # Move the pointer to the index
		lw $t0, 288($sp)
		lw $t0, 8($t0)
		sw $t0, 0($t1)
		
		# Allocating Int 4
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Int # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 4
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 112($sp) # internal_44 = address of allocated object Int
		
		# array internal_39[4 * internal_44] = internal_0
		lw $t0, 112($sp) # $t0 = internal_44
		lw $t0, 8($t0) # $t0 = value of the index
		addi $t1, $zero, 4 # $t1 = 4
		mult $t0, $t1 # $t0 = $t0 * 4
		mflo $t0
		lw $t1, 132($sp) # $t1 = internal_39
		add $t1, $t1, $t0 # Move the pointer to the index
		lw $t0, 288($sp)
		lw $t0, 8($t0)
		sw $t0, 0($t1)
		
		# Allocating Int 5
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Int # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 5
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 108($sp) # internal_45 = address of allocated object Int
		
		# array internal_39[4 * internal_45] = internal_0
		lw $t0, 108($sp) # $t0 = internal_45
		lw $t0, 8($t0) # $t0 = value of the index
		addi $t1, $zero, 4 # $t1 = 4
		mult $t0, $t1 # $t0 = $t0 * 4
		mflo $t0
		lw $t1, 132($sp) # $t1 = internal_39
		add $t1, $t1, $t0 # Move the pointer to the index
		lw $t0, 288($sp)
		lw $t0, 8($t0)
		sw $t0, 0($t1)
		
		# Allocating Bool 0
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Bool # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 0
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 104($sp) # internal_46 = address of allocated object Int
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument internal_35
		lw $t0, 160($sp)
		sw $t0, 4($sp) # Storing internal_35
		
		# Argument internal_4
		lw $t0, 284($sp)
		sw $t0, 0($sp) # Storing internal_4
		
		# Calling function function_equal
		jal function_equal
		lw $ra, 8($sp)
		sw $v1, 116($sp) # internal_46 = result of function_equal
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# If internal_46 then goto error_branch_8781702295173
		lw $t0, 104($sp) # Loading the address of the condition
		lw $t0, 8($t0) # Loading the value of the condition
		addi $t1, $zero, 1 # Setting the value to 1 for comparison
		beq $t0, $t1, error_branch_8781702295173
		
		# array internal_39[4 * internal_33] = internal_1
		lw $t0, 156($sp) # $t0 = internal_33
		lw $t0, 8($t0) # $t0 = value of the index
		addi $t1, $zero, 4 # $t1 = 4
		mult $t0, $t1 # $t0 = $t0 * 4
		mflo $t0
		lw $t1, 132($sp) # $t1 = internal_39
		add $t1, $t1, $t0 # Move the pointer to the index
		lw $t0, 284($sp)
		lw $t0, 8($t0)
		sw $t0, 0($t1)
		
		# Allocating Bool 0
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Bool # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 0
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 100($sp) # internal_47 = address of allocated object Int
		
		# Allocating Int 0
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Int # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 0
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 96($sp) # internal_48 = address of allocated object Int
		
		# internal_47 = array internal_39[4 * internal_48]
		lw $t0, 96($sp) # $t0 = internal_48
		lw $t0, 8($t0) # $t0 = value of the index
		addi $t1, $zero, 4 # $t1 = 4
		mult $t0, $t1 # $t0 = $t0 * 4
		mflo $t0
		lw $t1, 132($sp) # $t1 = internal_39
		add $t1, $t1, $t0 # Move the pointer to the index
		lw $t0, 0($t1) # $t1 = value in the position
		lw $t2, 100($sp) # internal_47 = array internal_39[4 * internal_48]
		sw $t0, 8($t2)
		
		# If internal_47 then goto branch_A_8781702295173
		lw $t0, 100($sp) # Loading the address of the condition
		lw $t0, 8($t0) # Loading the value of the condition
		addi $t1, $zero, 1 # Setting the value to 1 for comparison
		beq $t0, $t1, branch_A_8781702295173
		
		# Allocating Int 1
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Int # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 1
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 92($sp) # internal_49 = address of allocated object Int
		
		# internal_47 = array internal_39[4 * internal_49]
		lw $t0, 92($sp) # $t0 = internal_49
		lw $t0, 8($t0) # $t0 = value of the index
		addi $t1, $zero, 4 # $t1 = 4
		mult $t0, $t1 # $t0 = $t0 * 4
		mflo $t0
		lw $t1, 132($sp) # $t1 = internal_39
		add $t1, $t1, $t0 # Move the pointer to the index
		lw $t0, 0($t1) # $t1 = value in the position
		lw $t2, 100($sp) # internal_47 = array internal_39[4 * internal_49]
		sw $t0, 8($t2)
		
		# If internal_47 then goto branch_B_8781702295173
		lw $t0, 100($sp) # Loading the address of the condition
		lw $t0, 8($t0) # Loading the value of the condition
		addi $t1, $zero, 1 # Setting the value to 1 for comparison
		beq $t0, $t1, branch_B_8781702295173
		
		# Allocating Int 2
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Int # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 2
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 88($sp) # internal_50 = address of allocated object Int
		
		# internal_47 = array internal_39[4 * internal_50]
		lw $t0, 88($sp) # $t0 = internal_50
		lw $t0, 8($t0) # $t0 = value of the index
		addi $t1, $zero, 4 # $t1 = 4
		mult $t0, $t1 # $t0 = $t0 * 4
		mflo $t0
		lw $t1, 132($sp) # $t1 = internal_39
		add $t1, $t1, $t0 # Move the pointer to the index
		lw $t0, 0($t1) # $t1 = value in the position
		lw $t2, 100($sp) # internal_47 = array internal_39[4 * internal_50]
		sw $t0, 8($t2)
		
		# If internal_47 then goto branch_C_8781702295173
		lw $t0, 100($sp) # Loading the address of the condition
		lw $t0, 8($t0) # Loading the value of the condition
		addi $t1, $zero, 1 # Setting the value to 1 for comparison
		beq $t0, $t1, branch_C_8781702295173
		
		# Allocating Int 3
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Int # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 3
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 84($sp) # internal_51 = address of allocated object Int
		
		# internal_47 = array internal_39[4 * internal_51]
		lw $t0, 84($sp) # $t0 = internal_51
		lw $t0, 8($t0) # $t0 = value of the index
		addi $t1, $zero, 4 # $t1 = 4
		mult $t0, $t1 # $t0 = $t0 * 4
		mflo $t0
		lw $t1, 132($sp) # $t1 = internal_39
		add $t1, $t1, $t0 # Move the pointer to the index
		lw $t0, 0($t1) # $t1 = value in the position
		lw $t2, 100($sp) # internal_47 = array internal_39[4 * internal_51]
		sw $t0, 8($t2)
		
		# If internal_47 then goto branch_D_8781702295173
		lw $t0, 100($sp) # Loading the address of the condition
		lw $t0, 8($t0) # Loading the value of the condition
		addi $t1, $zero, 1 # Setting the value to 1 for comparison
		beq $t0, $t1, branch_D_8781702295173
		
		# Allocating Int 4
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Int # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 4
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 80($sp) # internal_52 = address of allocated object Int
		
		# internal_47 = array internal_39[4 * internal_52]
		lw $t0, 80($sp) # $t0 = internal_52
		lw $t0, 8($t0) # $t0 = value of the index
		addi $t1, $zero, 4 # $t1 = 4
		mult $t0, $t1 # $t0 = $t0 * 4
		mflo $t0
		lw $t1, 132($sp) # $t1 = internal_39
		add $t1, $t1, $t0 # Move the pointer to the index
		lw $t0, 0($t1) # $t1 = value in the position
		lw $t2, 100($sp) # internal_47 = array internal_39[4 * internal_52]
		sw $t0, 8($t2)
		
		# If internal_47 then goto branch_E_8781702295173
		lw $t0, 100($sp) # Loading the address of the condition
		lw $t0, 8($t0) # Loading the value of the condition
		addi $t1, $zero, 1 # Setting the value to 1 for comparison
		beq $t0, $t1, branch_E_8781702295173
		
		# Allocating Int 5
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Int # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 5
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 76($sp) # internal_53 = address of allocated object Int
		
		# internal_47 = array internal_39[4 * internal_53]
		lw $t0, 76($sp) # $t0 = internal_53
		lw $t0, 8($t0) # $t0 = value of the index
		addi $t1, $zero, 4 # $t1 = 4
		mult $t0, $t1 # $t0 = $t0 * 4
		mflo $t0
		lw $t1, 132($sp) # $t1 = internal_39
		add $t1, $t1, $t0 # Move the pointer to the index
		lw $t0, 0($t1) # $t1 = value in the position
		lw $t2, 100($sp) # internal_47 = array internal_39[4 * internal_53]
		sw $t0, 8($t2)
		
		# If internal_47 then goto branch_Object_8781702295173
		lw $t0, 100($sp) # Loading the address of the condition
		lw $t0, 8($t0) # Loading the value of the condition
		addi $t1, $zero, 1 # Setting the value to 1 for comparison
		beq $t0, $t1, branch_Object_8781702295173
		
		branch_A_8781702295173:
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument a
		lw $t0, 80($sp)
		sw $t0, 4($sp) # Storing a
		
		# Argument var
		lw $t0, 304($sp)
		sw $t0, 0($sp) # Storing var
		
		# Calling function function_assign
		jal function_assign
		lw $ra, 8($sp)
		sw $v1, 80($sp) # a = result of function_assign
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# Allocating String
		li $v0, 9
		addi $a0, $zero, 29 # $a0 = length of string + 9 for 4 bytes for the type, 4 bytes for the length of the string and 1 byte for null-terminator
		syscall
		
		la $t0, type_String
		sw $t0, 0($v0) # Setting type in the first word of the object
		
		addi $t0, $zero, 29
		sw $t0, 4($v0) # Setting length of the string in the second word of the object
		
		addi $t0, $zero, 67
		sb $t0, 8($v0) # internal_56[0] = 'C'
		
		addi $t0, $zero, 108
		sb $t0, 9($v0) # internal_56[1] = 'l'
		
		addi $t0, $zero, 97
		sb $t0, 10($v0) # internal_56[2] = 'a'
		
		addi $t0, $zero, 115
		sb $t0, 11($v0) # internal_56[3] = 's'
		
		addi $t0, $zero, 115
		sb $t0, 12($v0) # internal_56[4] = 's'
		
		addi $t0, $zero, 32
		sb $t0, 13($v0) # internal_56[5] = ' '
		
		addi $t0, $zero, 116
		sb $t0, 14($v0) # internal_56[6] = 't'
		
		addi $t0, $zero, 121
		sb $t0, 15($v0) # internal_56[7] = 'y'
		
		addi $t0, $zero, 112
		sb $t0, 16($v0) # internal_56[8] = 'p'
		
		addi $t0, $zero, 101
		sb $t0, 17($v0) # internal_56[9] = 'e'
		
		addi $t0, $zero, 32
		sb $t0, 18($v0) # internal_56[10] = ' '
		
		addi $t0, $zero, 105
		sb $t0, 19($v0) # internal_56[11] = 'i'
		
		addi $t0, $zero, 115
		sb $t0, 20($v0) # internal_56[12] = 's'
		
		addi $t0, $zero, 32
		sb $t0, 21($v0) # internal_56[13] = ' '
		
		addi $t0, $zero, 110
		sb $t0, 22($v0) # internal_56[14] = 'n'
		
		addi $t0, $zero, 111
		sb $t0, 23($v0) # internal_56[15] = 'o'
		
		addi $t0, $zero, 119
		sb $t0, 24($v0) # internal_56[16] = 'w'
		
		addi $t0, $zero, 32
		sb $t0, 25($v0) # internal_56[17] = ' '
		
		addi $t0, $zero, 65
		sb $t0, 26($v0) # internal_56[18] = 'A'
		
		addi $t0, $zero, 10
		sb $t0, 27($v0) # internal_56[19] = '\n'
		
		sb $zero, 28($v0) # Null-terminator at the end of the string
		
		sw $v0, 64($sp) # internal_56 = "Class type is now A\n"
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument self
		lw $t0, 308($sp)
		sw $t0, 4($sp) # Storing self
		
		# Argument internal_56
		lw $t0, 76($sp)
		sw $t0, 0($sp) # Storing internal_56
		
		# Calling function function_out_string_at_IO
		jal function_out_string_at_IO
		lw $ra, 8($sp)
		sw $v1, 72($sp) # internal_57 = result of function_out_string_at_IO
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument internal_54
		lw $t0, 84($sp)
		sw $t0, 4($sp) # Storing internal_54
		
		# Argument internal_57
		lw $t0, 72($sp)
		sw $t0, 0($sp) # Storing internal_57
		
		# Calling function function_assign
		jal function_assign
		lw $ra, 8($sp)
		sw $v1, 84($sp) # internal_54 = result of function_assign
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# internal_54 = internal_57
		lw $t0, 60($sp)
		sw $t0, 72($sp)
		
		# Jumping to branch_end_8781702295173
		j branch_end_8781702295173
		
		branch_B_8781702295173:
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument b
		lw $t0, 68($sp)
		sw $t0, 4($sp) # Storing b
		
		# Argument var
		lw $t0, 304($sp)
		sw $t0, 0($sp) # Storing var
		
		# Calling function function_assign
		jal function_assign
		lw $ra, 8($sp)
		sw $v1, 68($sp) # b = result of function_assign
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# Allocating String
		li $v0, 9
		addi $a0, $zero, 29 # $a0 = length of string + 9 for 4 bytes for the type, 4 bytes for the length of the string and 1 byte for null-terminator
		syscall
		
		la $t0, type_String
		sw $t0, 0($v0) # Setting type in the first word of the object
		
		addi $t0, $zero, 29
		sw $t0, 4($v0) # Setting length of the string in the second word of the object
		
		addi $t0, $zero, 67
		sb $t0, 8($v0) # internal_59[0] = 'C'
		
		addi $t0, $zero, 108
		sb $t0, 9($v0) # internal_59[1] = 'l'
		
		addi $t0, $zero, 97
		sb $t0, 10($v0) # internal_59[2] = 'a'
		
		addi $t0, $zero, 115
		sb $t0, 11($v0) # internal_59[3] = 's'
		
		addi $t0, $zero, 115
		sb $t0, 12($v0) # internal_59[4] = 's'
		
		addi $t0, $zero, 32
		sb $t0, 13($v0) # internal_59[5] = ' '
		
		addi $t0, $zero, 116
		sb $t0, 14($v0) # internal_59[6] = 't'
		
		addi $t0, $zero, 121
		sb $t0, 15($v0) # internal_59[7] = 'y'
		
		addi $t0, $zero, 112
		sb $t0, 16($v0) # internal_59[8] = 'p'
		
		addi $t0, $zero, 101
		sb $t0, 17($v0) # internal_59[9] = 'e'
		
		addi $t0, $zero, 32
		sb $t0, 18($v0) # internal_59[10] = ' '
		
		addi $t0, $zero, 105
		sb $t0, 19($v0) # internal_59[11] = 'i'
		
		addi $t0, $zero, 115
		sb $t0, 20($v0) # internal_59[12] = 's'
		
		addi $t0, $zero, 32
		sb $t0, 21($v0) # internal_59[13] = ' '
		
		addi $t0, $zero, 110
		sb $t0, 22($v0) # internal_59[14] = 'n'
		
		addi $t0, $zero, 111
		sb $t0, 23($v0) # internal_59[15] = 'o'
		
		addi $t0, $zero, 119
		sb $t0, 24($v0) # internal_59[16] = 'w'
		
		addi $t0, $zero, 32
		sb $t0, 25($v0) # internal_59[17] = ' '
		
		addi $t0, $zero, 66
		sb $t0, 26($v0) # internal_59[18] = 'B'
		
		addi $t0, $zero, 10
		sb $t0, 27($v0) # internal_59[19] = '\n'
		
		sb $zero, 28($v0) # Null-terminator at the end of the string
		
		sw $v0, 52($sp) # internal_59 = "Class type is now B\n"
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument self
		lw $t0, 308($sp)
		sw $t0, 4($sp) # Storing self
		
		# Argument internal_59
		lw $t0, 64($sp)
		sw $t0, 0($sp) # Storing internal_59
		
		# Calling function function_out_string_at_IO
		jal function_out_string_at_IO
		lw $ra, 8($sp)
		sw $v1, 60($sp) # internal_60 = result of function_out_string_at_IO
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument internal_54
		lw $t0, 84($sp)
		sw $t0, 4($sp) # Storing internal_54
		
		# Argument internal_60
		lw $t0, 60($sp)
		sw $t0, 0($sp) # Storing internal_60
		
		# Calling function function_assign
		jal function_assign
		lw $ra, 8($sp)
		sw $v1, 84($sp) # internal_54 = result of function_assign
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# internal_54 = internal_60
		lw $t0, 48($sp)
		sw $t0, 72($sp)
		
		# Jumping to branch_end_8781702295173
		j branch_end_8781702295173
		
		branch_C_8781702295173:
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument c
		lw $t0, 56($sp)
		sw $t0, 4($sp) # Storing c
		
		# Argument var
		lw $t0, 304($sp)
		sw $t0, 0($sp) # Storing var
		
		# Calling function function_assign
		jal function_assign
		lw $ra, 8($sp)
		sw $v1, 56($sp) # c = result of function_assign
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# Allocating String
		li $v0, 9
		addi $a0, $zero, 29 # $a0 = length of string + 9 for 4 bytes for the type, 4 bytes for the length of the string and 1 byte for null-terminator
		syscall
		
		la $t0, type_String
		sw $t0, 0($v0) # Setting type in the first word of the object
		
		addi $t0, $zero, 29
		sw $t0, 4($v0) # Setting length of the string in the second word of the object
		
		addi $t0, $zero, 67
		sb $t0, 8($v0) # internal_62[0] = 'C'
		
		addi $t0, $zero, 108
		sb $t0, 9($v0) # internal_62[1] = 'l'
		
		addi $t0, $zero, 97
		sb $t0, 10($v0) # internal_62[2] = 'a'
		
		addi $t0, $zero, 115
		sb $t0, 11($v0) # internal_62[3] = 's'
		
		addi $t0, $zero, 115
		sb $t0, 12($v0) # internal_62[4] = 's'
		
		addi $t0, $zero, 32
		sb $t0, 13($v0) # internal_62[5] = ' '
		
		addi $t0, $zero, 116
		sb $t0, 14($v0) # internal_62[6] = 't'
		
		addi $t0, $zero, 121
		sb $t0, 15($v0) # internal_62[7] = 'y'
		
		addi $t0, $zero, 112
		sb $t0, 16($v0) # internal_62[8] = 'p'
		
		addi $t0, $zero, 101
		sb $t0, 17($v0) # internal_62[9] = 'e'
		
		addi $t0, $zero, 32
		sb $t0, 18($v0) # internal_62[10] = ' '
		
		addi $t0, $zero, 105
		sb $t0, 19($v0) # internal_62[11] = 'i'
		
		addi $t0, $zero, 115
		sb $t0, 20($v0) # internal_62[12] = 's'
		
		addi $t0, $zero, 32
		sb $t0, 21($v0) # internal_62[13] = ' '
		
		addi $t0, $zero, 110
		sb $t0, 22($v0) # internal_62[14] = 'n'
		
		addi $t0, $zero, 111
		sb $t0, 23($v0) # internal_62[15] = 'o'
		
		addi $t0, $zero, 119
		sb $t0, 24($v0) # internal_62[16] = 'w'
		
		addi $t0, $zero, 32
		sb $t0, 25($v0) # internal_62[17] = ' '
		
		addi $t0, $zero, 67
		sb $t0, 26($v0) # internal_62[18] = 'C'
		
		addi $t0, $zero, 10
		sb $t0, 27($v0) # internal_62[19] = '\n'
		
		sb $zero, 28($v0) # Null-terminator at the end of the string
		
		sw $v0, 40($sp) # internal_62 = "Class type is now C\n"
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument self
		lw $t0, 308($sp)
		sw $t0, 4($sp) # Storing self
		
		# Argument internal_62
		lw $t0, 52($sp)
		sw $t0, 0($sp) # Storing internal_62
		
		# Calling function function_out_string_at_IO
		jal function_out_string_at_IO
		lw $ra, 8($sp)
		sw $v1, 48($sp) # internal_63 = result of function_out_string_at_IO
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument internal_54
		lw $t0, 84($sp)
		sw $t0, 4($sp) # Storing internal_54
		
		# Argument internal_63
		lw $t0, 48($sp)
		sw $t0, 0($sp) # Storing internal_63
		
		# Calling function function_assign
		jal function_assign
		lw $ra, 8($sp)
		sw $v1, 84($sp) # internal_54 = result of function_assign
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# internal_54 = internal_63
		lw $t0, 36($sp)
		sw $t0, 72($sp)
		
		# Jumping to branch_end_8781702295173
		j branch_end_8781702295173
		
		branch_D_8781702295173:
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument d
		lw $t0, 44($sp)
		sw $t0, 4($sp) # Storing d
		
		# Argument var
		lw $t0, 304($sp)
		sw $t0, 0($sp) # Storing var
		
		# Calling function function_assign
		jal function_assign
		lw $ra, 8($sp)
		sw $v1, 44($sp) # d = result of function_assign
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# Allocating String
		li $v0, 9
		addi $a0, $zero, 29 # $a0 = length of string + 9 for 4 bytes for the type, 4 bytes for the length of the string and 1 byte for null-terminator
		syscall
		
		la $t0, type_String
		sw $t0, 0($v0) # Setting type in the first word of the object
		
		addi $t0, $zero, 29
		sw $t0, 4($v0) # Setting length of the string in the second word of the object
		
		addi $t0, $zero, 67
		sb $t0, 8($v0) # internal_65[0] = 'C'
		
		addi $t0, $zero, 108
		sb $t0, 9($v0) # internal_65[1] = 'l'
		
		addi $t0, $zero, 97
		sb $t0, 10($v0) # internal_65[2] = 'a'
		
		addi $t0, $zero, 115
		sb $t0, 11($v0) # internal_65[3] = 's'
		
		addi $t0, $zero, 115
		sb $t0, 12($v0) # internal_65[4] = 's'
		
		addi $t0, $zero, 32
		sb $t0, 13($v0) # internal_65[5] = ' '
		
		addi $t0, $zero, 116
		sb $t0, 14($v0) # internal_65[6] = 't'
		
		addi $t0, $zero, 121
		sb $t0, 15($v0) # internal_65[7] = 'y'
		
		addi $t0, $zero, 112
		sb $t0, 16($v0) # internal_65[8] = 'p'
		
		addi $t0, $zero, 101
		sb $t0, 17($v0) # internal_65[9] = 'e'
		
		addi $t0, $zero, 32
		sb $t0, 18($v0) # internal_65[10] = ' '
		
		addi $t0, $zero, 105
		sb $t0, 19($v0) # internal_65[11] = 'i'
		
		addi $t0, $zero, 115
		sb $t0, 20($v0) # internal_65[12] = 's'
		
		addi $t0, $zero, 32
		sb $t0, 21($v0) # internal_65[13] = ' '
		
		addi $t0, $zero, 110
		sb $t0, 22($v0) # internal_65[14] = 'n'
		
		addi $t0, $zero, 111
		sb $t0, 23($v0) # internal_65[15] = 'o'
		
		addi $t0, $zero, 119
		sb $t0, 24($v0) # internal_65[16] = 'w'
		
		addi $t0, $zero, 32
		sb $t0, 25($v0) # internal_65[17] = ' '
		
		addi $t0, $zero, 68
		sb $t0, 26($v0) # internal_65[18] = 'D'
		
		addi $t0, $zero, 10
		sb $t0, 27($v0) # internal_65[19] = '\n'
		
		sb $zero, 28($v0) # Null-terminator at the end of the string
		
		sw $v0, 28($sp) # internal_65 = "Class type is now D\n"
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument self
		lw $t0, 308($sp)
		sw $t0, 4($sp) # Storing self
		
		# Argument internal_65
		lw $t0, 40($sp)
		sw $t0, 0($sp) # Storing internal_65
		
		# Calling function function_out_string_at_IO
		jal function_out_string_at_IO
		lw $ra, 8($sp)
		sw $v1, 36($sp) # internal_66 = result of function_out_string_at_IO
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument internal_54
		lw $t0, 84($sp)
		sw $t0, 4($sp) # Storing internal_54
		
		# Argument internal_66
		lw $t0, 36($sp)
		sw $t0, 0($sp) # Storing internal_66
		
		# Calling function function_assign
		jal function_assign
		lw $ra, 8($sp)
		sw $v1, 84($sp) # internal_54 = result of function_assign
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# internal_54 = internal_66
		lw $t0, 24($sp)
		sw $t0, 72($sp)
		
		# Jumping to branch_end_8781702295173
		j branch_end_8781702295173
		
		branch_E_8781702295173:
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument e
		lw $t0, 32($sp)
		sw $t0, 4($sp) # Storing e
		
		# Argument var
		lw $t0, 304($sp)
		sw $t0, 0($sp) # Storing var
		
		# Calling function function_assign
		jal function_assign
		lw $ra, 8($sp)
		sw $v1, 32($sp) # e = result of function_assign
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# Allocating String
		li $v0, 9
		addi $a0, $zero, 29 # $a0 = length of string + 9 for 4 bytes for the type, 4 bytes for the length of the string and 1 byte for null-terminator
		syscall
		
		la $t0, type_String
		sw $t0, 0($v0) # Setting type in the first word of the object
		
		addi $t0, $zero, 29
		sw $t0, 4($v0) # Setting length of the string in the second word of the object
		
		addi $t0, $zero, 67
		sb $t0, 8($v0) # internal_68[0] = 'C'
		
		addi $t0, $zero, 108
		sb $t0, 9($v0) # internal_68[1] = 'l'
		
		addi $t0, $zero, 97
		sb $t0, 10($v0) # internal_68[2] = 'a'
		
		addi $t0, $zero, 115
		sb $t0, 11($v0) # internal_68[3] = 's'
		
		addi $t0, $zero, 115
		sb $t0, 12($v0) # internal_68[4] = 's'
		
		addi $t0, $zero, 32
		sb $t0, 13($v0) # internal_68[5] = ' '
		
		addi $t0, $zero, 116
		sb $t0, 14($v0) # internal_68[6] = 't'
		
		addi $t0, $zero, 121
		sb $t0, 15($v0) # internal_68[7] = 'y'
		
		addi $t0, $zero, 112
		sb $t0, 16($v0) # internal_68[8] = 'p'
		
		addi $t0, $zero, 101
		sb $t0, 17($v0) # internal_68[9] = 'e'
		
		addi $t0, $zero, 32
		sb $t0, 18($v0) # internal_68[10] = ' '
		
		addi $t0, $zero, 105
		sb $t0, 19($v0) # internal_68[11] = 'i'
		
		addi $t0, $zero, 115
		sb $t0, 20($v0) # internal_68[12] = 's'
		
		addi $t0, $zero, 32
		sb $t0, 21($v0) # internal_68[13] = ' '
		
		addi $t0, $zero, 110
		sb $t0, 22($v0) # internal_68[14] = 'n'
		
		addi $t0, $zero, 111
		sb $t0, 23($v0) # internal_68[15] = 'o'
		
		addi $t0, $zero, 119
		sb $t0, 24($v0) # internal_68[16] = 'w'
		
		addi $t0, $zero, 32
		sb $t0, 25($v0) # internal_68[17] = ' '
		
		addi $t0, $zero, 69
		sb $t0, 26($v0) # internal_68[18] = 'E'
		
		addi $t0, $zero, 10
		sb $t0, 27($v0) # internal_68[19] = '\n'
		
		sb $zero, 28($v0) # Null-terminator at the end of the string
		
		sw $v0, 16($sp) # internal_68 = "Class type is now E\n"
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument self
		lw $t0, 308($sp)
		sw $t0, 4($sp) # Storing self
		
		# Argument internal_68
		lw $t0, 28($sp)
		sw $t0, 0($sp) # Storing internal_68
		
		# Calling function function_out_string_at_IO
		jal function_out_string_at_IO
		lw $ra, 8($sp)
		sw $v1, 24($sp) # internal_69 = result of function_out_string_at_IO
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument internal_54
		lw $t0, 84($sp)
		sw $t0, 4($sp) # Storing internal_54
		
		# Argument internal_69
		lw $t0, 24($sp)
		sw $t0, 0($sp) # Storing internal_69
		
		# Calling function function_assign
		jal function_assign
		lw $ra, 8($sp)
		sw $v1, 84($sp) # internal_54 = result of function_assign
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# internal_54 = internal_69
		lw $t0, 12($sp)
		sw $t0, 72($sp)
		
		# Jumping to branch_end_8781702295173
		j branch_end_8781702295173
		
		branch_Object_8781702295173:
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument o
		lw $t0, 20($sp)
		sw $t0, 4($sp) # Storing o
		
		# Argument var
		lw $t0, 304($sp)
		sw $t0, 0($sp) # Storing var
		
		# Calling function function_assign
		jal function_assign
		lw $ra, 8($sp)
		sw $v1, 20($sp) # o = result of function_assign
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# Allocating String
		li $v0, 9
		addi $a0, $zero, 16 # $a0 = length of string + 9 for 4 bytes for the type, 4 bytes for the length of the string and 1 byte for null-terminator
		syscall
		
		la $t0, type_String
		sw $t0, 0($v0) # Setting type in the first word of the object
		
		addi $t0, $zero, 16
		sw $t0, 4($v0) # Setting length of the string in the second word of the object
		
		addi $t0, $zero, 79
		sb $t0, 8($v0) # internal_71[0] = 'O'
		
		addi $t0, $zero, 111
		sb $t0, 9($v0) # internal_71[1] = 'o'
		
		addi $t0, $zero, 111
		sb $t0, 10($v0) # internal_71[2] = 'o'
		
		addi $t0, $zero, 111
		sb $t0, 11($v0) # internal_71[3] = 'o'
		
		addi $t0, $zero, 112
		sb $t0, 12($v0) # internal_71[4] = 'p'
		
		addi $t0, $zero, 115
		sb $t0, 13($v0) # internal_71[5] = 's'
		
		addi $t0, $zero, 10
		sb $t0, 14($v0) # internal_71[6] = '\n'
		
		sb $zero, 15($v0) # Null-terminator at the end of the string
		
		sw $v0, 4($sp) # internal_71 = "Oooops\n"
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument self
		lw $t0, 308($sp)
		sw $t0, 4($sp) # Storing self
		
		# Argument internal_71
		lw $t0, 16($sp)
		sw $t0, 0($sp) # Storing internal_71
		
		# Calling function function_out_string_at_IO
		jal function_out_string_at_IO
		lw $ra, 8($sp)
		sw $v1, 12($sp) # internal_72 = result of function_out_string_at_IO
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument internal_54
		lw $t0, 84($sp)
		sw $t0, 4($sp) # Storing internal_54
		
		# Argument internal_72
		lw $t0, 12($sp)
		sw $t0, 0($sp) # Storing internal_72
		
		# Calling function function_assign
		jal function_assign
		lw $ra, 8($sp)
		sw $v1, 84($sp) # internal_54 = result of function_assign
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# internal_54 = internal_72
		lw $t0, 0($sp)
		sw $t0, 72($sp)
		
		# Jumping to branch_end_8781702295173
		j branch_end_8781702295173
		
		error_branch_8781702295173:
		
		branch_end_8781702295173:
		
		# Loading return value in $v1
		lw $v1, 72($sp)
		
		# Freeing space for local variables
		addi $sp, $sp, 292
		
		jr $ra
		
	function_print_at_Main:
		# Function parameters
		#   $ra = 36($sp)
		#   self = 32($sp)
		#   var = 28($sp)
		
		# Reserving space for local variables
		addi $sp, $sp, -28
		
		# Allocating A2I
		li $v0, 9
		lw $a0, type_A2I
		syscall
		la $t0, type_A2I # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of th object
		sw $a0, 4($v0) # Setting size in the second word of th object
		sw $v0, 20($sp) # internal_1 = address of allocated object A2I
		
		# Passing function arguments
		addi $sp, $sp, -8 # Reserving space for arguments
		sw $ra, 4($sp) # Storing return address
		
		# Argument internal_1
		lw $t0, 28($sp)
		sw $t0, 0($sp) # Storing internal_1
		
		# Calling function function___init___at_A2I
		jal function___init___at_A2I
		lw $ra, 4($sp)
		sw $v1, 28($sp) # internal_1 = result of function___init___at_A2I
		addi $sp, $sp, 8 # Freeing space for arguments
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument z
		lw $t0, 36($sp)
		sw $t0, 4($sp) # Storing z
		
		# Argument internal_1
		lw $t0, 32($sp)
		sw $t0, 0($sp) # Storing internal_1
		
		# Calling function function_assign
		jal function_assign
		lw $ra, 8($sp)
		sw $v1, 36($sp) # z = result of function_assign
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# Passing function arguments
		addi $sp, $sp, -8 # Reserving space for arguments
		sw $ra, 4($sp) # Storing return address
		
		# Argument var
		lw $t0, 36($sp)
		sw $t0, 0($sp) # Storing var
		
		# Calling function function_value_at_A
		jal function_value_at_A
		lw $ra, 4($sp)
		sw $v1, 24($sp) # internal_2 = result of function_value_at_A
		addi $sp, $sp, 8 # Freeing space for arguments
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument z
		lw $t0, 36($sp)
		sw $t0, 4($sp) # Storing z
		
		# Argument internal_2
		lw $t0, 28($sp)
		sw $t0, 0($sp) # Storing internal_2
		
		# Calling function function_i2a_at_A2I
		jal function_i2a_at_A2I
		lw $ra, 8($sp)
		sw $v1, 24($sp) # internal_3 = result of function_i2a_at_A2I
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument self
		lw $t0, 44($sp)
		sw $t0, 4($sp) # Storing self
		
		# Argument internal_3
		lw $t0, 24($sp)
		sw $t0, 0($sp) # Storing internal_3
		
		# Calling function function_out_string_at_IO
		jal function_out_string_at_IO
		lw $ra, 8($sp)
		sw $v1, 20($sp) # internal_4 = result of function_out_string_at_IO
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# Allocating String
		li $v0, 9
		addi $a0, $zero, 10 # $a0 = length of string + 9 for 4 bytes for the type, 4 bytes for the length of the string and 1 byte for null-terminator
		syscall
		
		la $t0, type_String
		sw $t0, 0($v0) # Setting type in the first word of the object
		
		addi $t0, $zero, 10
		sw $t0, 4($v0) # Setting length of the string in the second word of the object
		
		addi $t0, $zero, 32
		sb $t0, 8($v0) # internal_5[0] = ' '
		
		sb $zero, 9($v0) # Null-terminator at the end of the string
		
		sw $v0, 4($sp) # internal_5 = " "
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument self
		lw $t0, 44($sp)
		sw $t0, 4($sp) # Storing self
		
		# Argument internal_5
		lw $t0, 16($sp)
		sw $t0, 0($sp) # Storing internal_5
		
		# Calling function function_out_string_at_IO
		jal function_out_string_at_IO
		lw $ra, 8($sp)
		sw $v1, 12($sp) # internal_6 = result of function_out_string_at_IO
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# Loading return value in $v1
		lw $v1, 0($sp)
		
		# Freeing space for local variables
		addi $sp, $sp, 28
		
		jr $ra
		
	function_main_at_Main:
		# Function parameters
		#   $ra = 820($sp)
		#   self = 816($sp)
		
		# Reserving space for local variables
		addi $sp, $sp, -816
		
		# Allocating A
		li $v0, 9
		lw $a0, type_A
		syscall
		la $t0, type_A # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of th object
		sw $a0, 4($v0) # Setting size in the second word of th object
		sw $v0, 812($sp) # internal_0 = address of allocated object A
		
		# Passing function arguments
		addi $sp, $sp, -8 # Reserving space for arguments
		sw $ra, 4($sp) # Storing return address
		
		# Argument internal_0
		lw $t0, 820($sp)
		sw $t0, 0($sp) # Storing internal_0
		
		# Calling function function___init___at_A
		jal function___init___at_A
		lw $ra, 4($sp)
		sw $v1, 820($sp) # internal_0 = result of function___init___at_A
		addi $sp, $sp, 8 # Freeing space for arguments
		
		# Set attribute avar of self
		lw $t0, 816($sp) # $t0 = self
		lw $t1, 812($sp) # $t1 = internal_0
		beq $t1, $zero, object_set_attribute_8781702253951
		lw $t2, 0($t1)
		la $t3, type_Int
		la $t4, type_Bool
		addi $t5, $zero, 1
		seq $t6, $t2, $t3
		beq $t6, $t5, int_set_attribute_8781702253951
		seq $t6, $t2, $t4
		beq $t6, $t5, bool_set_attribute_8781702253951
		j object_set_attribute_8781702253951
		int_set_attribute_8781702253951:
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		sw $t3, 0($v0)
		sw $a0, 4($v0)
		lw $t5, 8($t1)
		sw $t5, 8($v0)
		sw $v0, 12($t0) # self.avar = internal_0
		j end_set_attribute_8781702253951
		bool_set_attribute_8781702253951:
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		sw $t4, 0($v0)
		sw $a0, 4($v0)
		lw $t5, 8($t1)
		sw $t5, 8($v0)
		sw $v0, 12($t0) # self.avar = internal_0
		j end_set_attribute_8781702253951
		object_set_attribute_8781702253951:
		sw $t1, 12($t0) # self.avar = internal_0
		end_set_attribute_8781702253951:
		
		while_start_8781702298224:
		
		# Get attribute flag of self
		lw $t0, 816($sp) # Get the address of self
		lw $t1, 20($t0) # Get the attribute 'flag' from the instance
		lw $t2, 0($t1)
		la $t3, type_Int
		la $t4, type_Bool
		addi $t5, $zero, 1
		seq $t6, $t2, $t3
		beq $t6, $t5, int_get_attribute_8781702254011
		seq $t6, $t2, $t4
		beq $t6, $t5, bool_get_attribute_8781702254011
		j object_get_attribute_8781702254011
		int_get_attribute_8781702254011:
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		sw $t3, 0($v0)
		sw $a0, 4($v0)
		lw $t5, 8($t1)
		sw $t5, 8($v0)
		sw $v0, 808($sp) # internal_1 = self.flag
		j end_get_attribute_8781702254011
		bool_get_attribute_8781702254011:
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		sw $t4, 0($v0)
		sw $a0, 4($v0)
		lw $t5, 8($t1)
		sw $t5, 8($v0)
		sw $v0, 808($sp) # internal_1 = self.flag
		j end_get_attribute_8781702254011
		object_get_attribute_8781702254011:
		sw $t1, 808($sp) # internal_1 = flag
		end_get_attribute_8781702254011:
		
		# If internal_1 then goto while_body_8781702298224
		lw $t0, 808($sp) # Loading the address of the condition
		lw $t0, 8($t0) # Loading the value of the condition
		addi $t1, $zero, 1 # Setting the value to 1 for comparison
		beq $t0, $t1, while_body_8781702298224
		
		# Jumping to while_end_8781702298224
		j while_end_8781702298224
		
		while_body_8781702298224:
		
		# Allocating String
		li $v0, 9
		addi $a0, $zero, 16 # $a0 = length of string + 9 for 4 bytes for the type, 4 bytes for the length of the string and 1 byte for null-terminator
		syscall
		
		la $t0, type_String
		sw $t0, 0($v0) # Setting type in the first word of the object
		
		addi $t0, $zero, 16
		sw $t0, 4($v0) # Setting length of the string in the second word of the object
		
		addi $t0, $zero, 110
		sb $t0, 8($v0) # internal_2[0] = 'n'
		
		addi $t0, $zero, 117
		sb $t0, 9($v0) # internal_2[1] = 'u'
		
		addi $t0, $zero, 109
		sb $t0, 10($v0) # internal_2[2] = 'm'
		
		addi $t0, $zero, 98
		sb $t0, 11($v0) # internal_2[3] = 'b'
		
		addi $t0, $zero, 101
		sb $t0, 12($v0) # internal_2[4] = 'e'
		
		addi $t0, $zero, 114
		sb $t0, 13($v0) # internal_2[5] = 'r'
		
		addi $t0, $zero, 32
		sb $t0, 14($v0) # internal_2[6] = ' '
		
		sb $zero, 15($v0) # Null-terminator at the end of the string
		
		sw $v0, 804($sp) # internal_2 = "number "
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument self
		lw $t0, 828($sp)
		sw $t0, 4($sp) # Storing self
		
		# Argument internal_2
		lw $t0, 816($sp)
		sw $t0, 0($sp) # Storing internal_2
		
		# Calling function function_out_string_at_IO
		jal function_out_string_at_IO
		lw $ra, 8($sp)
		sw $v1, 812($sp) # internal_3 = result of function_out_string_at_IO
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# Get attribute avar of self
		lw $t0, 816($sp) # Get the address of self
		lw $t1, 12($t0) # Get the attribute 'avar' from the instance
		lw $t2, 0($t1)
		la $t3, type_Int
		la $t4, type_Bool
		addi $t5, $zero, 1
		seq $t6, $t2, $t3
		beq $t6, $t5, int_get_attribute_8781702254370
		seq $t6, $t2, $t4
		beq $t6, $t5, bool_get_attribute_8781702254370
		j object_get_attribute_8781702254370
		int_get_attribute_8781702254370:
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		sw $t3, 0($v0)
		sw $a0, 4($v0)
		lw $t5, 8($t1)
		sw $t5, 8($v0)
		sw $v0, 796($sp) # internal_4 = self.avar
		j end_get_attribute_8781702254370
		bool_get_attribute_8781702254370:
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		sw $t4, 0($v0)
		sw $a0, 4($v0)
		lw $t5, 8($t1)
		sw $t5, 8($v0)
		sw $v0, 796($sp) # internal_4 = self.avar
		j end_get_attribute_8781702254370
		object_get_attribute_8781702254370:
		sw $t1, 796($sp) # internal_4 = avar
		end_get_attribute_8781702254370:
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument self
		lw $t0, 828($sp)
		sw $t0, 4($sp) # Storing self
		
		# Argument internal_4
		lw $t0, 808($sp)
		sw $t0, 0($sp) # Storing internal_4
		
		# Calling function function_print_at_Main
		jal function_print_at_Main
		lw $ra, 8($sp)
		sw $v1, 804($sp) # internal_5 = result of function_print_at_Main
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# Allocating Bool 0
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Bool # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 0
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 784($sp) # internal_7 = address of allocated object Int
		
		# Get attribute avar of self
		lw $t0, 816($sp) # Get the address of self
		lw $t1, 12($t0) # Get the attribute 'avar' from the instance
		lw $t2, 0($t1)
		la $t3, type_Int
		la $t4, type_Bool
		addi $t5, $zero, 1
		seq $t6, $t2, $t3
		beq $t6, $t5, int_get_attribute_8781702254454
		seq $t6, $t2, $t4
		beq $t6, $t5, bool_get_attribute_8781702254454
		j object_get_attribute_8781702254454
		int_get_attribute_8781702254454:
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		sw $t3, 0($v0)
		sw $a0, 4($v0)
		lw $t5, 8($t1)
		sw $t5, 8($v0)
		sw $v0, 780($sp) # internal_8 = self.avar
		j end_get_attribute_8781702254454
		bool_get_attribute_8781702254454:
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		sw $t4, 0($v0)
		sw $a0, 4($v0)
		lw $t5, 8($t1)
		sw $t5, 8($v0)
		sw $v0, 780($sp) # internal_8 = self.avar
		j end_get_attribute_8781702254454
		object_get_attribute_8781702254454:
		sw $t1, 780($sp) # internal_8 = avar
		end_get_attribute_8781702254454:
		
		# Passing function arguments
		addi $sp, $sp, -8 # Reserving space for arguments
		sw $ra, 4($sp) # Storing return address
		
		# Argument internal_8
		lw $t0, 788($sp)
		sw $t0, 0($sp) # Storing internal_8
		
		# Calling function function_value_at_A
		jal function_value_at_A
		lw $ra, 4($sp)
		sw $v1, 784($sp) # internal_9 = result of function_value_at_A
		addi $sp, $sp, 8 # Freeing space for arguments
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument self
		lw $t0, 828($sp)
		sw $t0, 4($sp) # Storing self
		
		# Argument internal_9
		lw $t0, 788($sp)
		sw $t0, 0($sp) # Storing internal_9
		
		# Calling function function_is_even_at_Main
		jal function_is_even_at_Main
		lw $ra, 8($sp)
		sw $v1, 784($sp) # internal_10 = result of function_is_even_at_Main
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# internal_7 = internal_10
		lw $t0, 772($sp)
		sw $t0, 784($sp)
		
		# If internal_7 then goto then_8781702295290
		lw $t0, 784($sp) # Loading the address of the condition
		lw $t0, 8($t0) # Loading the value of the condition
		addi $t1, $zero, 1 # Setting the value to 1 for comparison
		beq $t0, $t1, then_8781702295290
		
		# Jumping to else_8781702295290
		j else_8781702295290
		
		then_8781702295290:
		
		# Allocating String
		li $v0, 9
		addi $a0, $zero, 18 # $a0 = length of string + 9 for 4 bytes for the type, 4 bytes for the length of the string and 1 byte for null-terminator
		syscall
		
		la $t0, type_String
		sw $t0, 0($v0) # Setting type in the first word of the object
		
		addi $t0, $zero, 18
		sw $t0, 4($v0) # Setting length of the string in the second word of the object
		
		addi $t0, $zero, 105
		sb $t0, 8($v0) # internal_11[0] = 'i'
		
		addi $t0, $zero, 115
		sb $t0, 9($v0) # internal_11[1] = 's'
		
		addi $t0, $zero, 32
		sb $t0, 10($v0) # internal_11[2] = ' '
		
		addi $t0, $zero, 101
		sb $t0, 11($v0) # internal_11[3] = 'e'
		
		addi $t0, $zero, 118
		sb $t0, 12($v0) # internal_11[4] = 'v'
		
		addi $t0, $zero, 101
		sb $t0, 13($v0) # internal_11[5] = 'e'
		
		addi $t0, $zero, 110
		sb $t0, 14($v0) # internal_11[6] = 'n'
		
		addi $t0, $zero, 33
		sb $t0, 15($v0) # internal_11[7] = '!'
		
		addi $t0, $zero, 10
		sb $t0, 16($v0) # internal_11[8] = '\n'
		
		sb $zero, 17($v0) # Null-terminator at the end of the string
		
		sw $v0, 768($sp) # internal_11 = "is even!\n"
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument self
		lw $t0, 828($sp)
		sw $t0, 4($sp) # Storing self
		
		# Argument internal_11
		lw $t0, 780($sp)
		sw $t0, 0($sp) # Storing internal_11
		
		# Calling function function_out_string_at_IO
		jal function_out_string_at_IO
		lw $ra, 8($sp)
		sw $v1, 776($sp) # internal_12 = result of function_out_string_at_IO
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# internal_6 = internal_12
		lw $t0, 764($sp)
		sw $t0, 788($sp)
		
		# Jumping to endif_8781702295290
		j endif_8781702295290
		
		else_8781702295290:
		
		# Allocating String
		li $v0, 9
		addi $a0, $zero, 17 # $a0 = length of string + 9 for 4 bytes for the type, 4 bytes for the length of the string and 1 byte for null-terminator
		syscall
		
		la $t0, type_String
		sw $t0, 0($v0) # Setting type in the first word of the object
		
		addi $t0, $zero, 17
		sw $t0, 4($v0) # Setting length of the string in the second word of the object
		
		addi $t0, $zero, 105
		sb $t0, 8($v0) # internal_13[0] = 'i'
		
		addi $t0, $zero, 115
		sb $t0, 9($v0) # internal_13[1] = 's'
		
		addi $t0, $zero, 32
		sb $t0, 10($v0) # internal_13[2] = ' '
		
		addi $t0, $zero, 111
		sb $t0, 11($v0) # internal_13[3] = 'o'
		
		addi $t0, $zero, 100
		sb $t0, 12($v0) # internal_13[4] = 'd'
		
		addi $t0, $zero, 100
		sb $t0, 13($v0) # internal_13[5] = 'd'
		
		addi $t0, $zero, 33
		sb $t0, 14($v0) # internal_13[6] = '!'
		
		addi $t0, $zero, 10
		sb $t0, 15($v0) # internal_13[7] = '\n'
		
		sb $zero, 16($v0) # Null-terminator at the end of the string
		
		sw $v0, 760($sp) # internal_13 = "is odd!\n"
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument self
		lw $t0, 828($sp)
		sw $t0, 4($sp) # Storing self
		
		# Argument internal_13
		lw $t0, 772($sp)
		sw $t0, 0($sp) # Storing internal_13
		
		# Calling function function_out_string_at_IO
		jal function_out_string_at_IO
		lw $ra, 8($sp)
		sw $v1, 768($sp) # internal_14 = result of function_out_string_at_IO
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# internal_6 = internal_14
		lw $t0, 756($sp)
		sw $t0, 788($sp)
		
		# Jumping to endif_8781702295290
		j endif_8781702295290
		
		endif_8781702295290:
		
		# Get attribute avar of self
		lw $t0, 816($sp) # Get the address of self
		lw $t1, 12($t0) # Get the attribute 'avar' from the instance
		lw $t2, 0($t1)
		la $t3, type_Int
		la $t4, type_Bool
		addi $t5, $zero, 1
		seq $t6, $t2, $t3
		beq $t6, $t5, int_get_attribute_8781702254629
		seq $t6, $t2, $t4
		beq $t6, $t5, bool_get_attribute_8781702254629
		j object_get_attribute_8781702254629
		int_get_attribute_8781702254629:
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		sw $t3, 0($v0)
		sw $a0, 4($v0)
		lw $t5, 8($t1)
		sw $t5, 8($v0)
		sw $v0, 752($sp) # internal_15 = self.avar
		j end_get_attribute_8781702254629
		bool_get_attribute_8781702254629:
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		sw $t4, 0($v0)
		sw $a0, 4($v0)
		lw $t5, 8($t1)
		sw $t5, 8($v0)
		sw $v0, 752($sp) # internal_15 = self.avar
		j end_get_attribute_8781702254629
		object_get_attribute_8781702254629:
		sw $t1, 752($sp) # internal_15 = avar
		end_get_attribute_8781702254629:
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument self
		lw $t0, 828($sp)
		sw $t0, 4($sp) # Storing self
		
		# Argument internal_15
		lw $t0, 764($sp)
		sw $t0, 0($sp) # Storing internal_15
		
		# Calling function function_class_type_at_Main
		jal function_class_type_at_Main
		lw $ra, 8($sp)
		sw $v1, 760($sp) # internal_16 = result of function_class_type_at_Main
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# Passing function arguments
		addi $sp, $sp, -8 # Reserving space for arguments
		sw $ra, 4($sp) # Storing return address
		
		# Argument self
		lw $t0, 824($sp)
		sw $t0, 0($sp) # Storing self
		
		# Calling function function_menu_at_Main
		jal function_menu_at_Main
		lw $ra, 4($sp)
		sw $v1, 752($sp) # internal_17 = result of function_menu_at_Main
		addi $sp, $sp, 8 # Freeing space for arguments
		
		# Set attribute char of self
		lw $t0, 816($sp) # $t0 = self
		lw $t1, 744($sp) # $t1 = internal_17
		beq $t1, $zero, object_set_attribute_8781702254650
		lw $t2, 0($t1)
		la $t3, type_Int
		la $t4, type_Bool
		addi $t5, $zero, 1
		seq $t6, $t2, $t3
		beq $t6, $t5, int_set_attribute_8781702254650
		seq $t6, $t2, $t4
		beq $t6, $t5, bool_set_attribute_8781702254650
		j object_set_attribute_8781702254650
		int_set_attribute_8781702254650:
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		sw $t3, 0($v0)
		sw $a0, 4($v0)
		lw $t5, 8($t1)
		sw $t5, 8($v0)
		sw $v0, 8($t0) # self.char = internal_17
		j end_set_attribute_8781702254650
		bool_set_attribute_8781702254650:
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		sw $t4, 0($v0)
		sw $a0, 4($v0)
		lw $t5, 8($t1)
		sw $t5, 8($v0)
		sw $v0, 8($t0) # self.char = internal_17
		j end_set_attribute_8781702254650
		object_set_attribute_8781702254650:
		sw $t1, 8($t0) # self.char = internal_17
		end_set_attribute_8781702254650:
		
		# Allocating Bool 0
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Bool # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 0
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 736($sp) # internal_19 = address of allocated object Int
		
		# Get attribute char of self
		lw $t0, 816($sp) # Get the address of self
		lw $t1, 8($t0) # Get the attribute 'char' from the instance
		lw $t2, 0($t1)
		la $t3, type_Int
		la $t4, type_Bool
		addi $t5, $zero, 1
		seq $t6, $t2, $t3
		beq $t6, $t5, int_get_attribute_8781702254725
		seq $t6, $t2, $t4
		beq $t6, $t5, bool_get_attribute_8781702254725
		j object_get_attribute_8781702254725
		int_get_attribute_8781702254725:
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		sw $t3, 0($v0)
		sw $a0, 4($v0)
		lw $t5, 8($t1)
		sw $t5, 8($v0)
		sw $v0, 732($sp) # internal_20 = self.char
		j end_get_attribute_8781702254725
		bool_get_attribute_8781702254725:
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		sw $t4, 0($v0)
		sw $a0, 4($v0)
		lw $t5, 8($t1)
		sw $t5, 8($v0)
		sw $v0, 732($sp) # internal_20 = self.char
		j end_get_attribute_8781702254725
		object_get_attribute_8781702254725:
		sw $t1, 732($sp) # internal_20 = char
		end_get_attribute_8781702254725:
		
		# Allocating String
		li $v0, 9
		addi $a0, $zero, 10 # $a0 = length of string + 9 for 4 bytes for the type, 4 bytes for the length of the string and 1 byte for null-terminator
		syscall
		
		la $t0, type_String
		sw $t0, 0($v0) # Setting type in the first word of the object
		
		addi $t0, $zero, 10
		sw $t0, 4($v0) # Setting length of the string in the second word of the object
		
		addi $t0, $zero, 97
		sb $t0, 8($v0) # internal_21[0] = 'a'
		
		sb $zero, 9($v0) # Null-terminator at the end of the string
		
		sw $v0, 728($sp) # internal_21 = "a"
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument internal_20
		lw $t0, 744($sp)
		sw $t0, 4($sp) # Storing internal_20
		
		# Argument internal_21
		lw $t0, 740($sp)
		sw $t0, 0($sp) # Storing internal_21
		
		# Calling function function_equal
		jal function_equal
		lw $ra, 8($sp)
		sw $v1, 736($sp) # internal_22 = result of function_equal
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# internal_19 = internal_22
		lw $t0, 724($sp)
		sw $t0, 736($sp)
		
		# If internal_19 then goto then_8781702298209
		lw $t0, 736($sp) # Loading the address of the condition
		lw $t0, 8($t0) # Loading the value of the condition
		addi $t1, $zero, 1 # Setting the value to 1 for comparison
		beq $t0, $t1, then_8781702298209
		
		# Jumping to else_8781702298209
		j else_8781702298209
		
		then_8781702298209:
		
		# Allocating A
		li $v0, 9
		lw $a0, type_A
		syscall
		la $t0, type_A # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of th object
		sw $a0, 4($v0) # Setting size in the second word of th object
		sw $v0, 720($sp) # internal_23 = address of allocated object A
		
		# Passing function arguments
		addi $sp, $sp, -8 # Reserving space for arguments
		sw $ra, 4($sp) # Storing return address
		
		# Argument internal_23
		lw $t0, 728($sp)
		sw $t0, 0($sp) # Storing internal_23
		
		# Calling function function___init___at_A
		jal function___init___at_A
		lw $ra, 4($sp)
		sw $v1, 728($sp) # internal_23 = result of function___init___at_A
		addi $sp, $sp, 8 # Freeing space for arguments
		
		# Passing function arguments
		addi $sp, $sp, -8 # Reserving space for arguments
		sw $ra, 4($sp) # Storing return address
		
		# Argument self
		lw $t0, 824($sp)
		sw $t0, 0($sp) # Storing self
		
		# Calling function function_get_int_at_Main
		jal function_get_int_at_Main
		lw $ra, 4($sp)
		sw $v1, 724($sp) # internal_24 = result of function_get_int_at_Main
		addi $sp, $sp, 8 # Freeing space for arguments
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument internal_23
		lw $t0, 732($sp)
		sw $t0, 4($sp) # Storing internal_23
		
		# Argument internal_24
		lw $t0, 728($sp)
		sw $t0, 0($sp) # Storing internal_24
		
		# Calling function function_set_var_at_A
		jal function_set_var_at_A
		lw $ra, 8($sp)
		sw $v1, 724($sp) # internal_25 = result of function_set_var_at_A
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# Set attribute a_var of self
		lw $t0, 816($sp) # $t0 = self
		lw $t1, 712($sp) # $t1 = internal_25
		beq $t1, $zero, object_set_attribute_8781702254806
		lw $t2, 0($t1)
		la $t3, type_Int
		la $t4, type_Bool
		addi $t5, $zero, 1
		seq $t6, $t2, $t3
		beq $t6, $t5, int_set_attribute_8781702254806
		seq $t6, $t2, $t4
		beq $t6, $t5, bool_set_attribute_8781702254806
		j object_set_attribute_8781702254806
		int_set_attribute_8781702254806:
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		sw $t3, 0($v0)
		sw $a0, 4($v0)
		lw $t5, 8($t1)
		sw $t5, 8($v0)
		sw $v0, 16($t0) # self.a_var = internal_25
		j end_set_attribute_8781702254806
		bool_set_attribute_8781702254806:
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		sw $t4, 0($v0)
		sw $a0, 4($v0)
		lw $t5, 8($t1)
		sw $t5, 8($v0)
		sw $v0, 16($t0) # self.a_var = internal_25
		j end_set_attribute_8781702254806
		object_set_attribute_8781702254806:
		sw $t1, 16($t0) # self.a_var = internal_25
		end_set_attribute_8781702254806:
		
		# Allocating B
		li $v0, 9
		lw $a0, type_B
		syscall
		la $t0, type_B # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of th object
		sw $a0, 4($v0) # Setting size in the second word of th object
		sw $v0, 708($sp) # internal_26 = address of allocated object B
		
		# Passing function arguments
		addi $sp, $sp, -8 # Reserving space for arguments
		sw $ra, 4($sp) # Storing return address
		
		# Argument internal_26
		lw $t0, 716($sp)
		sw $t0, 0($sp) # Storing internal_26
		
		# Calling function function___init___at_B
		jal function___init___at_B
		lw $ra, 4($sp)
		sw $v1, 716($sp) # internal_26 = result of function___init___at_B
		addi $sp, $sp, 8 # Freeing space for arguments
		
		# Get attribute avar of self
		lw $t0, 816($sp) # Get the address of self
		lw $t1, 12($t0) # Get the attribute 'avar' from the instance
		lw $t2, 0($t1)
		la $t3, type_Int
		la $t4, type_Bool
		addi $t5, $zero, 1
		seq $t6, $t2, $t3
		beq $t6, $t5, int_get_attribute_8781702255204
		seq $t6, $t2, $t4
		beq $t6, $t5, bool_get_attribute_8781702255204
		j object_get_attribute_8781702255204
		int_get_attribute_8781702255204:
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		sw $t3, 0($v0)
		sw $a0, 4($v0)
		lw $t5, 8($t1)
		sw $t5, 8($v0)
		sw $v0, 704($sp) # internal_27 = self.avar
		j end_get_attribute_8781702255204
		bool_get_attribute_8781702255204:
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		sw $t4, 0($v0)
		sw $a0, 4($v0)
		lw $t5, 8($t1)
		sw $t5, 8($v0)
		sw $v0, 704($sp) # internal_27 = self.avar
		j end_get_attribute_8781702255204
		object_get_attribute_8781702255204:
		sw $t1, 704($sp) # internal_27 = avar
		end_get_attribute_8781702255204:
		
		# Passing function arguments
		addi $sp, $sp, -8 # Reserving space for arguments
		sw $ra, 4($sp) # Storing return address
		
		# Argument internal_27
		lw $t0, 712($sp)
		sw $t0, 0($sp) # Storing internal_27
		
		# Calling function function_value_at_A
		jal function_value_at_A
		lw $ra, 4($sp)
		sw $v1, 708($sp) # internal_28 = result of function_value_at_A
		addi $sp, $sp, 8 # Freeing space for arguments
		
		# Get attribute a_var of self
		lw $t0, 816($sp) # Get the address of self
		lw $t1, 16($t0) # Get the attribute 'a_var' from the instance
		lw $t2, 0($t1)
		la $t3, type_Int
		la $t4, type_Bool
		addi $t5, $zero, 1
		seq $t6, $t2, $t3
		beq $t6, $t5, int_get_attribute_8781702255234
		seq $t6, $t2, $t4
		beq $t6, $t5, bool_get_attribute_8781702255234
		j object_get_attribute_8781702255234
		int_get_attribute_8781702255234:
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		sw $t3, 0($v0)
		sw $a0, 4($v0)
		lw $t5, 8($t1)
		sw $t5, 8($v0)
		sw $v0, 696($sp) # internal_29 = self.a_var
		j end_get_attribute_8781702255234
		bool_get_attribute_8781702255234:
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		sw $t4, 0($v0)
		sw $a0, 4($v0)
		lw $t5, 8($t1)
		sw $t5, 8($v0)
		sw $v0, 696($sp) # internal_29 = self.a_var
		j end_get_attribute_8781702255234
		object_get_attribute_8781702255234:
		sw $t1, 696($sp) # internal_29 = a_var
		end_get_attribute_8781702255234:
		
		# Passing function arguments
		addi $sp, $sp, -8 # Reserving space for arguments
		sw $ra, 4($sp) # Storing return address
		
		# Argument internal_29
		lw $t0, 704($sp)
		sw $t0, 0($sp) # Storing internal_29
		
		# Calling function function_value_at_A
		jal function_value_at_A
		lw $ra, 4($sp)
		sw $v1, 700($sp) # internal_30 = result of function_value_at_A
		addi $sp, $sp, 8 # Freeing space for arguments
		
		# Passing function arguments
		addi $sp, $sp, -16 # Reserving space for arguments
		sw $ra, 12($sp) # Storing return address
		
		# Argument internal_26
		lw $t0, 724($sp)
		sw $t0, 8($sp) # Storing internal_26
		
		# Argument internal_28
		lw $t0, 716($sp)
		sw $t0, 4($sp) # Storing internal_28
		
		# Argument internal_30
		lw $t0, 708($sp)
		sw $t0, 0($sp) # Storing internal_30
		
		# Calling function function_method2_at_A
		jal function_method2_at_A
		lw $ra, 12($sp)
		sw $v1, 704($sp) # internal_31 = result of function_method2_at_A
		addi $sp, $sp, 16 # Freeing space for arguments
		
		# Set attribute avar of self
		lw $t0, 816($sp) # $t0 = self
		lw $t1, 688($sp) # $t1 = internal_31
		beq $t1, $zero, object_set_attribute_8781702255144
		lw $t2, 0($t1)
		la $t3, type_Int
		la $t4, type_Bool
		addi $t5, $zero, 1
		seq $t6, $t2, $t3
		beq $t6, $t5, int_set_attribute_8781702255144
		seq $t6, $t2, $t4
		beq $t6, $t5, bool_set_attribute_8781702255144
		j object_set_attribute_8781702255144
		int_set_attribute_8781702255144:
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		sw $t3, 0($v0)
		sw $a0, 4($v0)
		lw $t5, 8($t1)
		sw $t5, 8($v0)
		sw $v0, 12($t0) # self.avar = internal_31
		j end_set_attribute_8781702255144
		bool_set_attribute_8781702255144:
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		sw $t4, 0($v0)
		sw $a0, 4($v0)
		lw $t5, 8($t1)
		sw $t5, 8($v0)
		sw $v0, 12($t0) # self.avar = internal_31
		j end_set_attribute_8781702255144
		object_set_attribute_8781702255144:
		sw $t1, 12($t0) # self.avar = internal_31
		end_set_attribute_8781702255144:
		
		# internal_18 = internal_31
		lw $t0, 688($sp)
		sw $t0, 740($sp)
		
		# Jumping to endif_8781702298209
		j endif_8781702298209
		
		else_8781702298209:
		
		# Allocating Bool 0
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Bool # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 0
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 680($sp) # internal_33 = address of allocated object Int
		
		# Get attribute char of self
		lw $t0, 816($sp) # Get the address of self
		lw $t1, 8($t0) # Get the attribute 'char' from the instance
		lw $t2, 0($t1)
		la $t3, type_Int
		la $t4, type_Bool
		addi $t5, $zero, 1
		seq $t6, $t2, $t3
		beq $t6, $t5, int_get_attribute_8781702255318
		seq $t6, $t2, $t4
		beq $t6, $t5, bool_get_attribute_8781702255318
		j object_get_attribute_8781702255318
		int_get_attribute_8781702255318:
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		sw $t3, 0($v0)
		sw $a0, 4($v0)
		lw $t5, 8($t1)
		sw $t5, 8($v0)
		sw $v0, 676($sp) # internal_34 = self.char
		j end_get_attribute_8781702255318
		bool_get_attribute_8781702255318:
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		sw $t4, 0($v0)
		sw $a0, 4($v0)
		lw $t5, 8($t1)
		sw $t5, 8($v0)
		sw $v0, 676($sp) # internal_34 = self.char
		j end_get_attribute_8781702255318
		object_get_attribute_8781702255318:
		sw $t1, 676($sp) # internal_34 = char
		end_get_attribute_8781702255318:
		
		# Allocating String
		li $v0, 9
		addi $a0, $zero, 10 # $a0 = length of string + 9 for 4 bytes for the type, 4 bytes for the length of the string and 1 byte for null-terminator
		syscall
		
		la $t0, type_String
		sw $t0, 0($v0) # Setting type in the first word of the object
		
		addi $t0, $zero, 10
		sw $t0, 4($v0) # Setting length of the string in the second word of the object
		
		addi $t0, $zero, 98
		sb $t0, 8($v0) # internal_35[0] = 'b'
		
		sb $zero, 9($v0) # Null-terminator at the end of the string
		
		sw $v0, 672($sp) # internal_35 = "b"
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument internal_34
		lw $t0, 688($sp)
		sw $t0, 4($sp) # Storing internal_34
		
		# Argument internal_35
		lw $t0, 684($sp)
		sw $t0, 0($sp) # Storing internal_35
		
		# Calling function function_equal
		jal function_equal
		lw $ra, 8($sp)
		sw $v1, 680($sp) # internal_36 = result of function_equal
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# internal_33 = internal_36
		lw $t0, 668($sp)
		sw $t0, 680($sp)
		
		# If internal_33 then goto then_8781702298203
		lw $t0, 680($sp) # Loading the address of the condition
		lw $t0, 8($t0) # Loading the value of the condition
		addi $t1, $zero, 1 # Setting the value to 1 for comparison
		beq $t0, $t1, then_8781702298203
		
		# Jumping to else_8781702298203
		j else_8781702298203
		
		then_8781702298203:
		
		# Get attribute avar of self
		lw $t0, 816($sp) # Get the address of self
		lw $t1, 12($t0) # Get the attribute 'avar' from the instance
		lw $t2, 0($t1)
		la $t3, type_Int
		la $t4, type_Bool
		addi $t5, $zero, 1
		seq $t6, $t2, $t3
		beq $t6, $t5, int_get_attribute_8781702255915
		seq $t6, $t2, $t4
		beq $t6, $t5, bool_get_attribute_8781702255915
		j object_get_attribute_8781702255915
		int_get_attribute_8781702255915:
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		sw $t3, 0($v0)
		sw $a0, 4($v0)
		lw $t5, 8($t1)
		sw $t5, 8($v0)
		sw $v0, 664($sp) # internal_37 = self.avar
		j end_get_attribute_8781702255915
		bool_get_attribute_8781702255915:
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		sw $t4, 0($v0)
		sw $a0, 4($v0)
		lw $t5, 8($t1)
		sw $t5, 8($v0)
		sw $v0, 664($sp) # internal_37 = self.avar
		j end_get_attribute_8781702255915
		object_get_attribute_8781702255915:
		sw $t1, 664($sp) # internal_37 = avar
		end_get_attribute_8781702255915:
		
		# Allocating Int 0
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Int # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 0
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 660($sp) # internal_38 = address of allocated object Int
		
		# Allocating Int 1
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Int # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 1
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 656($sp) # internal_39 = address of allocated object Int
		
		# Allocating Int 3
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Int # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 3
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 652($sp) # internal_40 = address of allocated object Int
		
		# Allocating NUll to internal_41
		sw $zero, 648($sp) # internal_41 = 0
		
		# Allocating Int 0
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Int # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 0
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 644($sp) # internal_42 = address of allocated object Int
		
		# Allocating Bool 0
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Bool # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 0
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 632($sp) # internal_45 = address of allocated object Int
		
		# internal_43 = typeof internal_37 that is the first word of the object
		lw $t0, 664($sp)
		lw $t0, 0($t0)
		sw $t0, 640($sp)
		
		# internal_44 = internal_43
		lw $t0, 640($sp)
		sw $t0, 636($sp)
		
		while_start_8781702296263:
		
		# internal_45 = EqualAddress(internal_44, internal_41)
		lw $t0, 636($sp)
		lw $t1, 648($sp)
		seq $t2, $t0, $t1
		lw $t0, 632($sp)
		sw $t2, 8($t0)
		
		# If internal_45 then goto while_end_8781702296263
		lw $t0, 632($sp) # Loading the address of the condition
		lw $t0, 8($t0) # Loading the value of the condition
		addi $t1, $zero, 1 # Setting the value to 1 for comparison
		beq $t0, $t1, while_end_8781702296263
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument internal_42
		lw $t0, 656($sp)
		sw $t0, 4($sp) # Storing internal_42
		
		# Argument internal_39
		lw $t0, 668($sp)
		sw $t0, 0($sp) # Storing internal_39
		
		# Calling function function_add
		jal function_add
		lw $ra, 8($sp)
		sw $v1, 656($sp) # internal_42 = result of function_add
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# internal_44 = ancestor of internal_44
		lw $t0, 636($sp)
		lw $t0, 4($t0)
		sw $t0, 636($sp)
		
		# Jumping to while_start_8781702296263
		j while_start_8781702296263
		
		while_end_8781702296263:
		
		# internal_44 = internal_43
		lw $t0, 640($sp)
		sw $t0, 636($sp)
		
		# initialize Array [internal_42]
		lw $t0, 644($sp) # $t0 = internal_42
		lw $t0, 8($t0) # $t0 = value of the size
		addi $t1, $zero, 4 # $t1 = 4
		mult $t0, $t1 # $t0 = $t0 * 4
		mflo $t0
		li $v0, 9
		move $a0, $t0
		syscall
		sw $v0, 628($sp) # internal_46 = new Array[internal_42]
		
		# Allocating Int 0
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Int # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 0
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 624($sp) # internal_47 = address of allocated object Int
		
		# Allocating Bool 0
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Bool # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 0
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 620($sp) # internal_48 = address of allocated object Int
		
		foreach_start_8781702296263:
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument internal_47
		lw $t0, 636($sp)
		sw $t0, 4($sp) # Storing internal_47
		
		# Argument internal_42
		lw $t0, 656($sp)
		sw $t0, 0($sp) # Storing internal_42
		
		# Calling function function_less_than
		jal function_less_than
		lw $ra, 8($sp)
		sw $v1, 632($sp) # internal_48 = result of function_less_than
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# If internal_48 then goto foreach_body_8781702296263
		lw $t0, 620($sp) # Loading the address of the condition
		lw $t0, 8($t0) # Loading the value of the condition
		addi $t1, $zero, 1 # Setting the value to 1 for comparison
		beq $t0, $t1, foreach_body_8781702296263
		
		# Jumping to foreach_end_8781702296263
		j foreach_end_8781702296263
		
		foreach_body_8781702296263:
		
		# array internal_46[4 * internal_47] = internal_44
		lw $t0, 624($sp) # $t0 = internal_47
		lw $t0, 8($t0) # $t0 = value of the index
		addi $t1, $zero, 4 # $t1 = 4
		mult $t0, $t1 # $t0 = $t0 * 4
		mflo $t0
		lw $t1, 628($sp) # $t1 = internal_46
		add $t1, $t1, $t0 # Move the pointer to the index
		lw $t0, 636($sp)
		sw $t0, 0($t1)
		
		# internal_44 = ancestor of internal_44
		lw $t0, 636($sp)
		lw $t0, 4($t0)
		sw $t0, 636($sp)
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument internal_47
		lw $t0, 636($sp)
		sw $t0, 4($sp) # Storing internal_47
		
		# Argument internal_39
		lw $t0, 668($sp)
		sw $t0, 0($sp) # Storing internal_39
		
		# Calling function function_add
		jal function_add
		lw $ra, 8($sp)
		sw $v1, 636($sp) # internal_47 = result of function_add
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# Jumping to foreach_start_8781702296263
		j foreach_start_8781702296263
		
		foreach_end_8781702296263:
		
		# initialize Array [internal_40]
		lw $t0, 652($sp) # $t0 = internal_40
		lw $t0, 8($t0) # $t0 = value of the size
		addi $t1, $zero, 4 # $t1 = 4
		mult $t0, $t1 # $t0 = $t0 * 4
		mflo $t0
		li $v0, 9
		move $a0, $t0
		syscall
		sw $v0, 616($sp) # internal_49 = new Array[internal_40]
		
		# initialize Array [internal_40]
		lw $t0, 652($sp) # $t0 = internal_40
		lw $t0, 8($t0) # $t0 = value of the size
		addi $t1, $zero, 4 # $t1 = 4
		mult $t0, $t1 # $t0 = $t0 * 4
		mflo $t0
		li $v0, 9
		move $a0, $t0
		syscall
		sw $v0, 612($sp) # internal_50 = new Array[internal_40]
		
		# Allocating Int 0
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Int # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 0
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 604($sp) # internal_52 = address of allocated object Int
		
		# internal_51 = direction of C
		la $t0, type_C
		sw $t0, 608($sp)
		
		# array internal_49[4 * internal_52] = internal_51
		lw $t0, 604($sp) # $t0 = internal_52
		lw $t0, 8($t0) # $t0 = value of the index
		addi $t1, $zero, 4 # $t1 = 4
		mult $t0, $t1 # $t0 = $t0 * 4
		mflo $t0
		lw $t1, 616($sp) # $t1 = internal_49
		add $t1, $t1, $t0 # Move the pointer to the index
		lw $t0, 608($sp)
		sw $t0, 0($t1)
		
		# array internal_50[4 * internal_52] = internal_42
		lw $t0, 604($sp) # $t0 = internal_52
		lw $t0, 8($t0) # $t0 = value of the index
		addi $t1, $zero, 4 # $t1 = 4
		mult $t0, $t1 # $t0 = $t0 * 4
		mflo $t0
		lw $t1, 612($sp) # $t1 = internal_50
		add $t1, $t1, $t0 # Move the pointer to the index
		lw $t0, 644($sp)
		lw $t0, 8($t0)
		sw $t0, 0($t1)
		
		# Allocating Int 1
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Int # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 1
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 596($sp) # internal_54 = address of allocated object Int
		
		# internal_53 = direction of A
		la $t0, type_A
		sw $t0, 600($sp)
		
		# array internal_49[4 * internal_54] = internal_53
		lw $t0, 596($sp) # $t0 = internal_54
		lw $t0, 8($t0) # $t0 = value of the index
		addi $t1, $zero, 4 # $t1 = 4
		mult $t0, $t1 # $t0 = $t0 * 4
		mflo $t0
		lw $t1, 616($sp) # $t1 = internal_49
		add $t1, $t1, $t0 # Move the pointer to the index
		lw $t0, 600($sp)
		sw $t0, 0($t1)
		
		# array internal_50[4 * internal_54] = internal_42
		lw $t0, 596($sp) # $t0 = internal_54
		lw $t0, 8($t0) # $t0 = value of the index
		addi $t1, $zero, 4 # $t1 = 4
		mult $t0, $t1 # $t0 = $t0 * 4
		mflo $t0
		lw $t1, 612($sp) # $t1 = internal_50
		add $t1, $t1, $t0 # Move the pointer to the index
		lw $t0, 644($sp)
		lw $t0, 8($t0)
		sw $t0, 0($t1)
		
		# Allocating Int 2
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Int # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 2
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 588($sp) # internal_56 = address of allocated object Int
		
		# internal_55 = direction of Object
		la $t0, type_Object
		sw $t0, 592($sp)
		
		# array internal_49[4 * internal_56] = internal_55
		lw $t0, 588($sp) # $t0 = internal_56
		lw $t0, 8($t0) # $t0 = value of the index
		addi $t1, $zero, 4 # $t1 = 4
		mult $t0, $t1 # $t0 = $t0 * 4
		mflo $t0
		lw $t1, 616($sp) # $t1 = internal_49
		add $t1, $t1, $t0 # Move the pointer to the index
		lw $t0, 592($sp)
		sw $t0, 0($t1)
		
		# array internal_50[4 * internal_56] = internal_42
		lw $t0, 588($sp) # $t0 = internal_56
		lw $t0, 8($t0) # $t0 = value of the index
		addi $t1, $zero, 4 # $t1 = 4
		mult $t0, $t1 # $t0 = $t0 * 4
		mflo $t0
		lw $t1, 612($sp) # $t1 = internal_50
		add $t1, $t1, $t0 # Move the pointer to the index
		lw $t0, 644($sp)
		lw $t0, 8($t0)
		sw $t0, 0($t1)
		
		# Allocating Int 0
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Int # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 0
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 584($sp) # internal_57 = address of allocated object Int
		
		# Allocating Bool 0
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Bool # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 0
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 580($sp) # internal_58 = address of allocated object Int
		
		# Allocating Int 0
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Int # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 0
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 572($sp) # internal_60 = address of allocated object Int
		
		# Allocating Bool 0
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Bool # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 0
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 568($sp) # internal_61 = address of allocated object Int
		
		# Allocating Bool 0
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Bool # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 0
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 560($sp) # internal_63 = address of allocated object Int
		
		foreach_type_start_8781702296263:
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument internal_57
		lw $t0, 596($sp)
		sw $t0, 4($sp) # Storing internal_57
		
		# Argument internal_40
		lw $t0, 664($sp)
		sw $t0, 0($sp) # Storing internal_40
		
		# Calling function function_less_than
		jal function_less_than
		lw $ra, 8($sp)
		sw $v1, 592($sp) # internal_58 = result of function_less_than
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# If internal_58 then goto foreach_type_body_8781702296263
		lw $t0, 580($sp) # Loading the address of the condition
		lw $t0, 8($t0) # Loading the value of the condition
		addi $t1, $zero, 1 # Setting the value to 1 for comparison
		beq $t0, $t1, foreach_type_body_8781702296263
		
		# Jumping to foreach_type_end_8781702296263
		j foreach_type_end_8781702296263
		
		foreach_type_body_8781702296263:
		
		# internal_59 = array internal_49[4 * internal_57]
		lw $t0, 584($sp) # $t0 = internal_57
		lw $t0, 8($t0) # $t0 = value of the index
		addi $t1, $zero, 4 # $t1 = 4
		mult $t0, $t1 # $t0 = $t0 * 4
		mflo $t0
		lw $t1, 616($sp) # $t1 = internal_49
		add $t1, $t1, $t0 # Move the pointer to the index
		lw $t0, 0($t1) # $t1 = value in the position
		sw $t0, 576($sp) # internal_59 = array internal_49[4 * internal_57]
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument internal_60
		lw $t0, 584($sp)
		sw $t0, 4($sp) # Storing internal_60
		
		# Argument internal_38
		lw $t0, 672($sp)
		sw $t0, 0($sp) # Storing internal_38
		
		# Calling function function_assign
		jal function_assign
		lw $ra, 8($sp)
		sw $v1, 584($sp) # internal_60 = result of function_assign
		addi $sp, $sp, 12 # Freeing space for arguments
		
		foreach_ancestor_start_8781702296263:
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument internal_60
		lw $t0, 584($sp)
		sw $t0, 4($sp) # Storing internal_60
		
		# Argument internal_42
		lw $t0, 656($sp)
		sw $t0, 0($sp) # Storing internal_42
		
		# Calling function function_less_than
		jal function_less_than
		lw $ra, 8($sp)
		sw $v1, 580($sp) # internal_61 = result of function_less_than
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# If internal_61 then goto foreach_ancestor_body_8781702296263
		lw $t0, 568($sp) # Loading the address of the condition
		lw $t0, 8($t0) # Loading the value of the condition
		addi $t1, $zero, 1 # Setting the value to 1 for comparison
		beq $t0, $t1, foreach_ancestor_body_8781702296263
		
		# Jumping to foreach_ancestor_end_8781702296263
		j foreach_ancestor_end_8781702296263
		
		foreach_ancestor_body_8781702296263:
		
		# internal_62 = array internal_46[4 * internal_60]
		lw $t0, 572($sp) # $t0 = internal_60
		lw $t0, 8($t0) # $t0 = value of the index
		addi $t1, $zero, 4 # $t1 = 4
		mult $t0, $t1 # $t0 = $t0 * 4
		mflo $t0
		lw $t1, 628($sp) # $t1 = internal_46
		add $t1, $t1, $t0 # Move the pointer to the index
		lw $t0, 0($t1) # $t1 = value in the position
		sw $t0, 564($sp) # internal_62 = array internal_46[4 * internal_60]
		
		# internal_63 = EqualAddress(internal_59, internal_62)
		lw $t0, 576($sp)
		lw $t1, 564($sp)
		seq $t2, $t0, $t1
		lw $t0, 560($sp)
		sw $t2, 8($t0)
		
		# If internal_63 then goto foreach_ancestor_end_8781702296263
		lw $t0, 560($sp) # Loading the address of the condition
		lw $t0, 8($t0) # Loading the value of the condition
		addi $t1, $zero, 1 # Setting the value to 1 for comparison
		beq $t0, $t1, foreach_ancestor_end_8781702296263
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument internal_60
		lw $t0, 584($sp)
		sw $t0, 4($sp) # Storing internal_60
		
		# Argument internal_39
		lw $t0, 668($sp)
		sw $t0, 0($sp) # Storing internal_39
		
		# Calling function function_add
		jal function_add
		lw $ra, 8($sp)
		sw $v1, 584($sp) # internal_60 = result of function_add
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# Jumping to foreach_ancestor_start_8781702296263
		j foreach_ancestor_start_8781702296263
		
		foreach_ancestor_end_8781702296263:
		
		# array internal_50[4 * internal_57] = internal_60
		lw $t0, 584($sp) # $t0 = internal_57
		lw $t0, 8($t0) # $t0 = value of the index
		addi $t1, $zero, 4 # $t1 = 4
		mult $t0, $t1 # $t0 = $t0 * 4
		mflo $t0
		lw $t1, 612($sp) # $t1 = internal_50
		add $t1, $t1, $t0 # Move the pointer to the index
		lw $t0, 572($sp)
		lw $t0, 8($t0)
		sw $t0, 0($t1)
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument internal_57
		lw $t0, 596($sp)
		sw $t0, 4($sp) # Storing internal_57
		
		# Argument internal_39
		lw $t0, 668($sp)
		sw $t0, 0($sp) # Storing internal_39
		
		# Calling function function_add
		jal function_add
		lw $ra, 8($sp)
		sw $v1, 596($sp) # internal_57 = result of function_add
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# Jumping to foreach_type_start_8781702296263
		j foreach_type_start_8781702296263
		
		foreach_type_end_8781702296263:
		
		# Allocating String
		li $v0, 9
		addi $a0, $zero, 10 # $a0 = length of string + 9 for 4 bytes for the type, 4 bytes for the length of the string and 1 byte for null-terminator
		syscall
		
		la $t0, type_String
		sw $t0, 0($v0) # Setting type in the first word of the object
		
		addi $t0, $zero, 10
		sw $t0, 4($v0) # Setting length of the string in the second word of the object
		
		addi $t0, $zero, 10
		sb $t0, 8($v0) # internal_69[0] = '\n'
		
		sb $zero, 9($v0) # Null-terminator at the end of the string
		
		sw $v0, 536($sp) # internal_69 = "\n"
		
		# Allocating String
		li $v0, 9
		addi $a0, $zero, 10 # $a0 = length of string + 9 for 4 bytes for the type, 4 bytes for the length of the string and 1 byte for null-terminator
		syscall
		
		la $t0, type_String
		sw $t0, 0($v0) # Setting type in the first word of the object
		
		addi $t0, $zero, 10
		sw $t0, 4($v0) # Setting length of the string in the second word of the object
		
		addi $t0, $zero, 32
		sb $t0, 8($v0) # internal_70[0] = ' '
		
		sb $zero, 9($v0) # Null-terminator at the end of the string
		
		sw $v0, 532($sp) # internal_70 = " "
		
		# Allocating Int 0
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Int # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 0
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 556($sp) # internal_64 = address of allocated object Int
		
		# Allocating Int 0
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Int # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 0
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 552($sp) # internal_65 = address of allocated object Int
		
		# Allocating Int 0
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Int # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 0
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 548($sp) # internal_66 = address of allocated object Int
		
		# Allocating Int 0
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Int # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 0
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 544($sp) # internal_67 = address of allocated object Int
		
		# Allocating Bool 0
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Bool # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 0
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 540($sp) # internal_68 = address of allocated object Int
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument internal_67
		lw $t0, 556($sp)
		sw $t0, 4($sp) # Storing internal_67
		
		# Argument internal_42
		lw $t0, 656($sp)
		sw $t0, 0($sp) # Storing internal_42
		
		# Calling function function_assign
		jal function_assign
		lw $ra, 8($sp)
		sw $v1, 556($sp) # internal_67 = result of function_assign
		addi $sp, $sp, 12 # Freeing space for arguments
		
		foreach_min_start_8781702296263:
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument internal_64
		lw $t0, 568($sp)
		sw $t0, 4($sp) # Storing internal_64
		
		# Argument internal_40
		lw $t0, 664($sp)
		sw $t0, 0($sp) # Storing internal_40
		
		# Calling function function_less_than
		jal function_less_than
		lw $ra, 8($sp)
		sw $v1, 552($sp) # internal_68 = result of function_less_than
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# If internal_68 then goto foreach_min_body_8781702296263
		lw $t0, 540($sp) # Loading the address of the condition
		lw $t0, 8($t0) # Loading the value of the condition
		addi $t1, $zero, 1 # Setting the value to 1 for comparison
		beq $t0, $t1, foreach_min_body_8781702296263
		
		# Jumping to foreach_min_end_8781702296263
		j foreach_min_end_8781702296263
		
		foreach_min_body_8781702296263:
		
		# internal_66 = array internal_50[4 * internal_64]
		lw $t0, 556($sp) # $t0 = internal_64
		lw $t0, 8($t0) # $t0 = value of the index
		addi $t1, $zero, 4 # $t1 = 4
		mult $t0, $t1 # $t0 = $t0 * 4
		mflo $t0
		lw $t1, 612($sp) # $t1 = internal_50
		add $t1, $t1, $t0 # Move the pointer to the index
		lw $t0, 0($t1) # $t1 = value in the position
		lw $t2, 548($sp) # internal_66 = array internal_50[4 * internal_64]
		sw $t0, 8($t2)
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument internal_66
		lw $t0, 560($sp)
		sw $t0, 4($sp) # Storing internal_66
		
		# Argument internal_67
		lw $t0, 556($sp)
		sw $t0, 0($sp) # Storing internal_67
		
		# Calling function function_less_than
		jal function_less_than
		lw $ra, 8($sp)
		sw $v1, 552($sp) # internal_68 = result of function_less_than
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# If internal_68 then goto update_min_8781702296263
		lw $t0, 540($sp) # Loading the address of the condition
		lw $t0, 8($t0) # Loading the value of the condition
		addi $t1, $zero, 1 # Setting the value to 1 for comparison
		beq $t0, $t1, update_min_8781702296263
		
		# Jumping to update_min_end_8781702296263
		j update_min_end_8781702296263
		
		update_min_8781702296263:
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument internal_67
		lw $t0, 556($sp)
		sw $t0, 4($sp) # Storing internal_67
		
		# Argument internal_66
		lw $t0, 560($sp)
		sw $t0, 0($sp) # Storing internal_66
		
		# Calling function function_assign
		jal function_assign
		lw $ra, 8($sp)
		sw $v1, 556($sp) # internal_67 = result of function_assign
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument internal_65
		lw $t0, 564($sp)
		sw $t0, 4($sp) # Storing internal_65
		
		# Argument internal_64
		lw $t0, 568($sp)
		sw $t0, 0($sp) # Storing internal_64
		
		# Calling function function_assign
		jal function_assign
		lw $ra, 8($sp)
		sw $v1, 564($sp) # internal_65 = result of function_assign
		addi $sp, $sp, 12 # Freeing space for arguments
		
		update_min_end_8781702296263:
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument internal_64
		lw $t0, 568($sp)
		sw $t0, 4($sp) # Storing internal_64
		
		# Argument internal_39
		lw $t0, 668($sp)
		sw $t0, 0($sp) # Storing internal_39
		
		# Calling function function_add
		jal function_add
		lw $ra, 8($sp)
		sw $v1, 568($sp) # internal_64 = result of function_add
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# Jumping to foreach_min_start_8781702296263
		j foreach_min_start_8781702296263
		
		foreach_min_end_8781702296263:
		
		# initialize Array [internal_40]
		lw $t0, 652($sp) # $t0 = internal_40
		lw $t0, 8($t0) # $t0 = value of the size
		addi $t1, $zero, 4 # $t1 = 4
		mult $t0, $t1 # $t0 = $t0 * 4
		mflo $t0
		li $v0, 9
		move $a0, $t0
		syscall
		sw $v0, 528($sp) # internal_71 = new Array[internal_40]
		
		# Allocating Int 0
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Int # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 0
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 524($sp) # internal_72 = address of allocated object Int
		
		# array internal_71[4 * internal_72] = internal_38
		lw $t0, 524($sp) # $t0 = internal_72
		lw $t0, 8($t0) # $t0 = value of the index
		addi $t1, $zero, 4 # $t1 = 4
		mult $t0, $t1 # $t0 = $t0 * 4
		mflo $t0
		lw $t1, 528($sp) # $t1 = internal_71
		add $t1, $t1, $t0 # Move the pointer to the index
		lw $t0, 660($sp)
		lw $t0, 8($t0)
		sw $t0, 0($t1)
		
		# Allocating Int 1
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Int # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 1
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 520($sp) # internal_73 = address of allocated object Int
		
		# array internal_71[4 * internal_73] = internal_38
		lw $t0, 520($sp) # $t0 = internal_73
		lw $t0, 8($t0) # $t0 = value of the index
		addi $t1, $zero, 4 # $t1 = 4
		mult $t0, $t1 # $t0 = $t0 * 4
		mflo $t0
		lw $t1, 528($sp) # $t1 = internal_71
		add $t1, $t1, $t0 # Move the pointer to the index
		lw $t0, 660($sp)
		lw $t0, 8($t0)
		sw $t0, 0($t1)
		
		# Allocating Int 2
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Int # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 2
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 516($sp) # internal_74 = address of allocated object Int
		
		# array internal_71[4 * internal_74] = internal_38
		lw $t0, 516($sp) # $t0 = internal_74
		lw $t0, 8($t0) # $t0 = value of the index
		addi $t1, $zero, 4 # $t1 = 4
		mult $t0, $t1 # $t0 = $t0 * 4
		mflo $t0
		lw $t1, 528($sp) # $t1 = internal_71
		add $t1, $t1, $t0 # Move the pointer to the index
		lw $t0, 660($sp)
		lw $t0, 8($t0)
		sw $t0, 0($t1)
		
		# Allocating Bool 0
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Bool # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 0
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 512($sp) # internal_75 = address of allocated object Int
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument internal_67
		lw $t0, 556($sp)
		sw $t0, 4($sp) # Storing internal_67
		
		# Argument internal_42
		lw $t0, 656($sp)
		sw $t0, 0($sp) # Storing internal_42
		
		# Calling function function_equal
		jal function_equal
		lw $ra, 8($sp)
		sw $v1, 524($sp) # internal_75 = result of function_equal
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# If internal_75 then goto error_branch_8781702296263
		lw $t0, 512($sp) # Loading the address of the condition
		lw $t0, 8($t0) # Loading the value of the condition
		addi $t1, $zero, 1 # Setting the value to 1 for comparison
		beq $t0, $t1, error_branch_8781702296263
		
		# array internal_71[4 * internal_65] = internal_39
		lw $t0, 552($sp) # $t0 = internal_65
		lw $t0, 8($t0) # $t0 = value of the index
		addi $t1, $zero, 4 # $t1 = 4
		mult $t0, $t1 # $t0 = $t0 * 4
		mflo $t0
		lw $t1, 528($sp) # $t1 = internal_71
		add $t1, $t1, $t0 # Move the pointer to the index
		lw $t0, 656($sp)
		lw $t0, 8($t0)
		sw $t0, 0($t1)
		
		# Allocating Bool 0
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Bool # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 0
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 508($sp) # internal_76 = address of allocated object Int
		
		# Allocating Int 0
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Int # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 0
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 504($sp) # internal_77 = address of allocated object Int
		
		# internal_76 = array internal_71[4 * internal_77]
		lw $t0, 504($sp) # $t0 = internal_77
		lw $t0, 8($t0) # $t0 = value of the index
		addi $t1, $zero, 4 # $t1 = 4
		mult $t0, $t1 # $t0 = $t0 * 4
		mflo $t0
		lw $t1, 528($sp) # $t1 = internal_71
		add $t1, $t1, $t0 # Move the pointer to the index
		lw $t0, 0($t1) # $t1 = value in the position
		lw $t2, 508($sp) # internal_76 = array internal_71[4 * internal_77]
		sw $t0, 8($t2)
		
		# If internal_76 then goto branch_C_8781702296263
		lw $t0, 508($sp) # Loading the address of the condition
		lw $t0, 8($t0) # Loading the value of the condition
		addi $t1, $zero, 1 # Setting the value to 1 for comparison
		beq $t0, $t1, branch_C_8781702296263
		
		# Allocating Int 1
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Int # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 1
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 500($sp) # internal_78 = address of allocated object Int
		
		# internal_76 = array internal_71[4 * internal_78]
		lw $t0, 500($sp) # $t0 = internal_78
		lw $t0, 8($t0) # $t0 = value of the index
		addi $t1, $zero, 4 # $t1 = 4
		mult $t0, $t1 # $t0 = $t0 * 4
		mflo $t0
		lw $t1, 528($sp) # $t1 = internal_71
		add $t1, $t1, $t0 # Move the pointer to the index
		lw $t0, 0($t1) # $t1 = value in the position
		lw $t2, 508($sp) # internal_76 = array internal_71[4 * internal_78]
		sw $t0, 8($t2)
		
		# If internal_76 then goto branch_A_8781702296263
		lw $t0, 508($sp) # Loading the address of the condition
		lw $t0, 8($t0) # Loading the value of the condition
		addi $t1, $zero, 1 # Setting the value to 1 for comparison
		beq $t0, $t1, branch_A_8781702296263
		
		# Allocating Int 2
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Int # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 2
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 496($sp) # internal_79 = address of allocated object Int
		
		# internal_76 = array internal_71[4 * internal_79]
		lw $t0, 496($sp) # $t0 = internal_79
		lw $t0, 8($t0) # $t0 = value of the index
		addi $t1, $zero, 4 # $t1 = 4
		mult $t0, $t1 # $t0 = $t0 * 4
		mflo $t0
		lw $t1, 528($sp) # $t1 = internal_71
		add $t1, $t1, $t0 # Move the pointer to the index
		lw $t0, 0($t1) # $t1 = value in the position
		lw $t2, 508($sp) # internal_76 = array internal_71[4 * internal_79]
		sw $t0, 8($t2)
		
		# If internal_76 then goto branch_Object_8781702296263
		lw $t0, 508($sp) # Loading the address of the condition
		lw $t0, 8($t0) # Loading the value of the condition
		addi $t1, $zero, 1 # Setting the value to 1 for comparison
		beq $t0, $t1, branch_Object_8781702296263
		
		branch_C_8781702296263:
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument c
		lw $t0, 500($sp)
		sw $t0, 4($sp) # Storing c
		
		# Argument internal_37
		lw $t0, 676($sp)
		sw $t0, 0($sp) # Storing internal_37
		
		# Calling function function_assign
		jal function_assign
		lw $ra, 8($sp)
		sw $v1, 500($sp) # c = result of function_assign
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# Passing function arguments
		addi $sp, $sp, -8 # Reserving space for arguments
		sw $ra, 4($sp) # Storing return address
		
		# Argument c
		lw $t0, 496($sp)
		sw $t0, 0($sp) # Storing c
		
		# Calling function function_value_at_A
		jal function_value_at_A
		lw $ra, 4($sp)
		sw $v1, 492($sp) # internal_82 = result of function_value_at_A
		addi $sp, $sp, 8 # Freeing space for arguments
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument c
		lw $t0, 500($sp)
		sw $t0, 4($sp) # Storing c
		
		# Argument internal_82
		lw $t0, 496($sp)
		sw $t0, 0($sp) # Storing internal_82
		
		# Calling function function_method6_at_C
		jal function_method6_at_C
		lw $ra, 8($sp)
		sw $v1, 492($sp) # internal_83 = result of function_method6_at_C
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# Set attribute avar of self
		lw $t0, 816($sp) # $t0 = self
		lw $t1, 480($sp) # $t1 = internal_83
		beq $t1, $zero, object_set_attribute_8781702258321
		lw $t2, 0($t1)
		la $t3, type_Int
		la $t4, type_Bool
		addi $t5, $zero, 1
		seq $t6, $t2, $t3
		beq $t6, $t5, int_set_attribute_8781702258321
		seq $t6, $t2, $t4
		beq $t6, $t5, bool_set_attribute_8781702258321
		j object_set_attribute_8781702258321
		int_set_attribute_8781702258321:
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		sw $t3, 0($v0)
		sw $a0, 4($v0)
		lw $t5, 8($t1)
		sw $t5, 8($v0)
		sw $v0, 12($t0) # self.avar = internal_83
		j end_set_attribute_8781702258321
		bool_set_attribute_8781702258321:
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		sw $t4, 0($v0)
		sw $a0, 4($v0)
		lw $t5, 8($t1)
		sw $t5, 8($v0)
		sw $v0, 12($t0) # self.avar = internal_83
		j end_set_attribute_8781702258321
		object_set_attribute_8781702258321:
		sw $t1, 12($t0) # self.avar = internal_83
		end_set_attribute_8781702258321:
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument internal_80
		lw $t0, 504($sp)
		sw $t0, 4($sp) # Storing internal_80
		
		# Argument internal_83
		lw $t0, 492($sp)
		sw $t0, 0($sp) # Storing internal_83
		
		# Calling function function_assign
		jal function_assign
		lw $ra, 8($sp)
		sw $v1, 504($sp) # internal_80 = result of function_assign
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# internal_80 = internal_83
		lw $t0, 480($sp)
		sw $t0, 492($sp)
		
		# Jumping to branch_end_8781702296263
		j branch_end_8781702296263
		
		branch_A_8781702296263:
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument a
		lw $t0, 488($sp)
		sw $t0, 4($sp) # Storing a
		
		# Argument internal_37
		lw $t0, 676($sp)
		sw $t0, 0($sp) # Storing internal_37
		
		# Calling function function_assign
		jal function_assign
		lw $ra, 8($sp)
		sw $v1, 488($sp) # a = result of function_assign
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# Passing function arguments
		addi $sp, $sp, -8 # Reserving space for arguments
		sw $ra, 4($sp) # Storing return address
		
		# Argument a
		lw $t0, 484($sp)
		sw $t0, 0($sp) # Storing a
		
		# Calling function function_value_at_A
		jal function_value_at_A
		lw $ra, 4($sp)
		sw $v1, 480($sp) # internal_85 = result of function_value_at_A
		addi $sp, $sp, 8 # Freeing space for arguments
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument a
		lw $t0, 488($sp)
		sw $t0, 4($sp) # Storing a
		
		# Argument internal_85
		lw $t0, 484($sp)
		sw $t0, 0($sp) # Storing internal_85
		
		# Calling function function_method3_at_A
		jal function_method3_at_A
		lw $ra, 8($sp)
		sw $v1, 480($sp) # internal_86 = result of function_method3_at_A
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# Set attribute avar of self
		lw $t0, 816($sp) # $t0 = self
		lw $t1, 468($sp) # $t1 = internal_86
		beq $t1, $zero, object_set_attribute_8781702258698
		lw $t2, 0($t1)
		la $t3, type_Int
		la $t4, type_Bool
		addi $t5, $zero, 1
		seq $t6, $t2, $t3
		beq $t6, $t5, int_set_attribute_8781702258698
		seq $t6, $t2, $t4
		beq $t6, $t5, bool_set_attribute_8781702258698
		j object_set_attribute_8781702258698
		int_set_attribute_8781702258698:
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		sw $t3, 0($v0)
		sw $a0, 4($v0)
		lw $t5, 8($t1)
		sw $t5, 8($v0)
		sw $v0, 12($t0) # self.avar = internal_86
		j end_set_attribute_8781702258698
		bool_set_attribute_8781702258698:
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		sw $t4, 0($v0)
		sw $a0, 4($v0)
		lw $t5, 8($t1)
		sw $t5, 8($v0)
		sw $v0, 12($t0) # self.avar = internal_86
		j end_set_attribute_8781702258698
		object_set_attribute_8781702258698:
		sw $t1, 12($t0) # self.avar = internal_86
		end_set_attribute_8781702258698:
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument internal_80
		lw $t0, 504($sp)
		sw $t0, 4($sp) # Storing internal_80
		
		# Argument internal_86
		lw $t0, 480($sp)
		sw $t0, 0($sp) # Storing internal_86
		
		# Calling function function_assign
		jal function_assign
		lw $ra, 8($sp)
		sw $v1, 504($sp) # internal_80 = result of function_assign
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# internal_80 = internal_86
		lw $t0, 468($sp)
		sw $t0, 492($sp)
		
		# Jumping to branch_end_8781702296263
		j branch_end_8781702296263
		
		branch_Object_8781702296263:
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument o
		lw $t0, 476($sp)
		sw $t0, 4($sp) # Storing o
		
		# Argument internal_37
		lw $t0, 676($sp)
		sw $t0, 0($sp) # Storing internal_37
		
		# Calling function function_assign
		jal function_assign
		lw $ra, 8($sp)
		sw $v1, 476($sp) # o = result of function_assign
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# Allocating String
		li $v0, 9
		addi $a0, $zero, 16 # $a0 = length of string + 9 for 4 bytes for the type, 4 bytes for the length of the string and 1 byte for null-terminator
		syscall
		
		la $t0, type_String
		sw $t0, 0($v0) # Setting type in the first word of the object
		
		addi $t0, $zero, 16
		sw $t0, 4($v0) # Setting length of the string in the second word of the object
		
		addi $t0, $zero, 79
		sb $t0, 8($v0) # internal_88[0] = 'O'
		
		addi $t0, $zero, 111
		sb $t0, 9($v0) # internal_88[1] = 'o'
		
		addi $t0, $zero, 111
		sb $t0, 10($v0) # internal_88[2] = 'o'
		
		addi $t0, $zero, 111
		sb $t0, 11($v0) # internal_88[3] = 'o'
		
		addi $t0, $zero, 112
		sb $t0, 12($v0) # internal_88[4] = 'p'
		
		addi $t0, $zero, 115
		sb $t0, 13($v0) # internal_88[5] = 's'
		
		addi $t0, $zero, 10
		sb $t0, 14($v0) # internal_88[6] = '\n'
		
		sb $zero, 15($v0) # Null-terminator at the end of the string
		
		sw $v0, 460($sp) # internal_88 = "Oooops\n"
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument self
		lw $t0, 828($sp)
		sw $t0, 4($sp) # Storing self
		
		# Argument internal_88
		lw $t0, 472($sp)
		sw $t0, 0($sp) # Storing internal_88
		
		# Calling function function_out_string_at_IO
		jal function_out_string_at_IO
		lw $ra, 8($sp)
		sw $v1, 468($sp) # internal_89 = result of function_out_string_at_IO
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# Passing function arguments
		addi $sp, $sp, -8 # Reserving space for arguments
		sw $ra, 4($sp) # Storing return address
		
		# Argument self
		lw $t0, 824($sp)
		sw $t0, 0($sp) # Storing self
		
		# Calling function function_abort_at_Object
		jal function_abort_at_Object
		lw $ra, 4($sp)
		sw $v1, 460($sp) # internal_90 = result of function_abort_at_Object
		addi $sp, $sp, 8 # Freeing space for arguments
		
		# Allocating Int 0
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Int # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 0
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 448($sp) # internal_91 = address of allocated object Int
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument internal_80
		lw $t0, 504($sp)
		sw $t0, 4($sp) # Storing internal_80
		
		# Argument internal_91
		lw $t0, 460($sp)
		sw $t0, 0($sp) # Storing internal_91
		
		# Calling function function_assign
		jal function_assign
		lw $ra, 8($sp)
		sw $v1, 504($sp) # internal_80 = result of function_assign
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# internal_80 = internal_91
		lw $t0, 448($sp)
		sw $t0, 492($sp)
		
		# Jumping to branch_end_8781702296263
		j branch_end_8781702296263
		
		error_branch_8781702296263:
		
		branch_end_8781702296263:
		
		# internal_32 = internal_80
		lw $t0, 492($sp)
		sw $t0, 684($sp)
		
		# Jumping to endif_8781702298203
		j endif_8781702298203
		
		else_8781702298203:
		
		# Allocating Bool 0
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Bool # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 0
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 440($sp) # internal_93 = address of allocated object Int
		
		# Get attribute char of self
		lw $t0, 816($sp) # Get the address of self
		lw $t1, 8($t0) # Get the attribute 'char' from the instance
		lw $t2, 0($t1)
		la $t3, type_Int
		la $t4, type_Bool
		addi $t5, $zero, 1
		seq $t6, $t2, $t3
		beq $t6, $t5, int_get_attribute_8781702259493
		seq $t6, $t2, $t4
		beq $t6, $t5, bool_get_attribute_8781702259493
		j object_get_attribute_8781702259493
		int_get_attribute_8781702259493:
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		sw $t3, 0($v0)
		sw $a0, 4($v0)
		lw $t5, 8($t1)
		sw $t5, 8($v0)
		sw $v0, 436($sp) # internal_94 = self.char
		j end_get_attribute_8781702259493
		bool_get_attribute_8781702259493:
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		sw $t4, 0($v0)
		sw $a0, 4($v0)
		lw $t5, 8($t1)
		sw $t5, 8($v0)
		sw $v0, 436($sp) # internal_94 = self.char
		j end_get_attribute_8781702259493
		object_get_attribute_8781702259493:
		sw $t1, 436($sp) # internal_94 = char
		end_get_attribute_8781702259493:
		
		# Allocating String
		li $v0, 9
		addi $a0, $zero, 10 # $a0 = length of string + 9 for 4 bytes for the type, 4 bytes for the length of the string and 1 byte for null-terminator
		syscall
		
		la $t0, type_String
		sw $t0, 0($v0) # Setting type in the first word of the object
		
		addi $t0, $zero, 10
		sw $t0, 4($v0) # Setting length of the string in the second word of the object
		
		addi $t0, $zero, 99
		sb $t0, 8($v0) # internal_95[0] = 'c'
		
		sb $zero, 9($v0) # Null-terminator at the end of the string
		
		sw $v0, 432($sp) # internal_95 = "c"
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument internal_94
		lw $t0, 448($sp)
		sw $t0, 4($sp) # Storing internal_94
		
		# Argument internal_95
		lw $t0, 444($sp)
		sw $t0, 0($sp) # Storing internal_95
		
		# Calling function function_equal
		jal function_equal
		lw $ra, 8($sp)
		sw $v1, 440($sp) # internal_96 = result of function_equal
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# internal_93 = internal_96
		lw $t0, 428($sp)
		sw $t0, 440($sp)
		
		# If internal_93 then goto then_8781702298197
		lw $t0, 440($sp) # Loading the address of the condition
		lw $t0, 8($t0) # Loading the value of the condition
		addi $t1, $zero, 1 # Setting the value to 1 for comparison
		beq $t0, $t1, then_8781702298197
		
		# Jumping to else_8781702298197
		j else_8781702298197
		
		then_8781702298197:
		
		# Allocating A
		li $v0, 9
		lw $a0, type_A
		syscall
		la $t0, type_A # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of th object
		sw $a0, 4($v0) # Setting size in the second word of th object
		sw $v0, 424($sp) # internal_97 = address of allocated object A
		
		# Passing function arguments
		addi $sp, $sp, -8 # Reserving space for arguments
		sw $ra, 4($sp) # Storing return address
		
		# Argument internal_97
		lw $t0, 432($sp)
		sw $t0, 0($sp) # Storing internal_97
		
		# Calling function function___init___at_A
		jal function___init___at_A
		lw $ra, 4($sp)
		sw $v1, 432($sp) # internal_97 = result of function___init___at_A
		addi $sp, $sp, 8 # Freeing space for arguments
		
		# Passing function arguments
		addi $sp, $sp, -8 # Reserving space for arguments
		sw $ra, 4($sp) # Storing return address
		
		# Argument self
		lw $t0, 824($sp)
		sw $t0, 0($sp) # Storing self
		
		# Calling function function_get_int_at_Main
		jal function_get_int_at_Main
		lw $ra, 4($sp)
		sw $v1, 428($sp) # internal_98 = result of function_get_int_at_Main
		addi $sp, $sp, 8 # Freeing space for arguments
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument internal_97
		lw $t0, 436($sp)
		sw $t0, 4($sp) # Storing internal_97
		
		# Argument internal_98
		lw $t0, 432($sp)
		sw $t0, 0($sp) # Storing internal_98
		
		# Calling function function_set_var_at_A
		jal function_set_var_at_A
		lw $ra, 8($sp)
		sw $v1, 428($sp) # internal_99 = result of function_set_var_at_A
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# Set attribute a_var of self
		lw $t0, 816($sp) # $t0 = self
		lw $t1, 416($sp) # $t1 = internal_99
		beq $t1, $zero, object_set_attribute_8781702259574
		lw $t2, 0($t1)
		la $t3, type_Int
		la $t4, type_Bool
		addi $t5, $zero, 1
		seq $t6, $t2, $t3
		beq $t6, $t5, int_set_attribute_8781702259574
		seq $t6, $t2, $t4
		beq $t6, $t5, bool_set_attribute_8781702259574
		j object_set_attribute_8781702259574
		int_set_attribute_8781702259574:
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		sw $t3, 0($v0)
		sw $a0, 4($v0)
		lw $t5, 8($t1)
		sw $t5, 8($v0)
		sw $v0, 16($t0) # self.a_var = internal_99
		j end_set_attribute_8781702259574
		bool_set_attribute_8781702259574:
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		sw $t4, 0($v0)
		sw $a0, 4($v0)
		lw $t5, 8($t1)
		sw $t5, 8($v0)
		sw $v0, 16($t0) # self.a_var = internal_99
		j end_set_attribute_8781702259574
		object_set_attribute_8781702259574:
		sw $t1, 16($t0) # self.a_var = internal_99
		end_set_attribute_8781702259574:
		
		# Allocating D
		li $v0, 9
		lw $a0, type_D
		syscall
		la $t0, type_D # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of th object
		sw $a0, 4($v0) # Setting size in the second word of th object
		sw $v0, 412($sp) # internal_100 = address of allocated object D
		
		# Passing function arguments
		addi $sp, $sp, -8 # Reserving space for arguments
		sw $ra, 4($sp) # Storing return address
		
		# Argument internal_100
		lw $t0, 420($sp)
		sw $t0, 0($sp) # Storing internal_100
		
		# Calling function function___init___at_D
		jal function___init___at_D
		lw $ra, 4($sp)
		sw $v1, 420($sp) # internal_100 = result of function___init___at_D
		addi $sp, $sp, 8 # Freeing space for arguments
		
		# Get attribute avar of self
		lw $t0, 816($sp) # Get the address of self
		lw $t1, 12($t0) # Get the attribute 'avar' from the instance
		lw $t2, 0($t1)
		la $t3, type_Int
		la $t4, type_Bool
		addi $t5, $zero, 1
		seq $t6, $t2, $t3
		beq $t6, $t5, int_get_attribute_8781702259716
		seq $t6, $t2, $t4
		beq $t6, $t5, bool_get_attribute_8781702259716
		j object_get_attribute_8781702259716
		int_get_attribute_8781702259716:
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		sw $t3, 0($v0)
		sw $a0, 4($v0)
		lw $t5, 8($t1)
		sw $t5, 8($v0)
		sw $v0, 408($sp) # internal_101 = self.avar
		j end_get_attribute_8781702259716
		bool_get_attribute_8781702259716:
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		sw $t4, 0($v0)
		sw $a0, 4($v0)
		lw $t5, 8($t1)
		sw $t5, 8($v0)
		sw $v0, 408($sp) # internal_101 = self.avar
		j end_get_attribute_8781702259716
		object_get_attribute_8781702259716:
		sw $t1, 408($sp) # internal_101 = avar
		end_get_attribute_8781702259716:
		
		# Passing function arguments
		addi $sp, $sp, -8 # Reserving space for arguments
		sw $ra, 4($sp) # Storing return address
		
		# Argument internal_101
		lw $t0, 416($sp)
		sw $t0, 0($sp) # Storing internal_101
		
		# Calling function function_value_at_A
		jal function_value_at_A
		lw $ra, 4($sp)
		sw $v1, 412($sp) # internal_102 = result of function_value_at_A
		addi $sp, $sp, 8 # Freeing space for arguments
		
		# Get attribute a_var of self
		lw $t0, 816($sp) # Get the address of self
		lw $t1, 16($t0) # Get the attribute 'a_var' from the instance
		lw $t2, 0($t1)
		la $t3, type_Int
		la $t4, type_Bool
		addi $t5, $zero, 1
		seq $t6, $t2, $t3
		beq $t6, $t5, int_get_attribute_8781702259746
		seq $t6, $t2, $t4
		beq $t6, $t5, bool_get_attribute_8781702259746
		j object_get_attribute_8781702259746
		int_get_attribute_8781702259746:
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		sw $t3, 0($v0)
		sw $a0, 4($v0)
		lw $t5, 8($t1)
		sw $t5, 8($v0)
		sw $v0, 400($sp) # internal_103 = self.a_var
		j end_get_attribute_8781702259746
		bool_get_attribute_8781702259746:
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		sw $t4, 0($v0)
		sw $a0, 4($v0)
		lw $t5, 8($t1)
		sw $t5, 8($v0)
		sw $v0, 400($sp) # internal_103 = self.a_var
		j end_get_attribute_8781702259746
		object_get_attribute_8781702259746:
		sw $t1, 400($sp) # internal_103 = a_var
		end_get_attribute_8781702259746:
		
		# Passing function arguments
		addi $sp, $sp, -8 # Reserving space for arguments
		sw $ra, 4($sp) # Storing return address
		
		# Argument internal_103
		lw $t0, 408($sp)
		sw $t0, 0($sp) # Storing internal_103
		
		# Calling function function_value_at_A
		jal function_value_at_A
		lw $ra, 4($sp)
		sw $v1, 404($sp) # internal_104 = result of function_value_at_A
		addi $sp, $sp, 8 # Freeing space for arguments
		
		# Passing function arguments
		addi $sp, $sp, -16 # Reserving space for arguments
		sw $ra, 12($sp) # Storing return address
		
		# Argument internal_100
		lw $t0, 428($sp)
		sw $t0, 8($sp) # Storing internal_100
		
		# Argument internal_102
		lw $t0, 420($sp)
		sw $t0, 4($sp) # Storing internal_102
		
		# Argument internal_104
		lw $t0, 412($sp)
		sw $t0, 0($sp) # Storing internal_104
		
		# Calling function function_method4_at_A
		jal function_method4_at_A
		lw $ra, 12($sp)
		sw $v1, 408($sp) # internal_105 = result of function_method4_at_A
		addi $sp, $sp, 16 # Freeing space for arguments
		
		# Set attribute avar of self
		lw $t0, 816($sp) # $t0 = self
		lw $t1, 392($sp) # $t1 = internal_105
		beq $t1, $zero, object_set_attribute_8781702259649
		lw $t2, 0($t1)
		la $t3, type_Int
		la $t4, type_Bool
		addi $t5, $zero, 1
		seq $t6, $t2, $t3
		beq $t6, $t5, int_set_attribute_8781702259649
		seq $t6, $t2, $t4
		beq $t6, $t5, bool_set_attribute_8781702259649
		j object_set_attribute_8781702259649
		int_set_attribute_8781702259649:
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		sw $t3, 0($v0)
		sw $a0, 4($v0)
		lw $t5, 8($t1)
		sw $t5, 8($v0)
		sw $v0, 12($t0) # self.avar = internal_105
		j end_set_attribute_8781702259649
		bool_set_attribute_8781702259649:
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		sw $t4, 0($v0)
		sw $a0, 4($v0)
		lw $t5, 8($t1)
		sw $t5, 8($v0)
		sw $v0, 12($t0) # self.avar = internal_105
		j end_set_attribute_8781702259649
		object_set_attribute_8781702259649:
		sw $t1, 12($t0) # self.avar = internal_105
		end_set_attribute_8781702259649:
		
		# internal_92 = internal_105
		lw $t0, 392($sp)
		sw $t0, 444($sp)
		
		# Jumping to endif_8781702298197
		j endif_8781702298197
		
		else_8781702298197:
		
		# Allocating Bool 0
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Bool # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 0
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 384($sp) # internal_107 = address of allocated object Int
		
		# Get attribute char of self
		lw $t0, 816($sp) # Get the address of self
		lw $t1, 8($t0) # Get the attribute 'char' from the instance
		lw $t2, 0($t1)
		la $t3, type_Int
		la $t4, type_Bool
		addi $t5, $zero, 1
		seq $t6, $t2, $t3
		beq $t6, $t5, int_get_attribute_8781702259830
		seq $t6, $t2, $t4
		beq $t6, $t5, bool_get_attribute_8781702259830
		j object_get_attribute_8781702259830
		int_get_attribute_8781702259830:
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		sw $t3, 0($v0)
		sw $a0, 4($v0)
		lw $t5, 8($t1)
		sw $t5, 8($v0)
		sw $v0, 380($sp) # internal_108 = self.char
		j end_get_attribute_8781702259830
		bool_get_attribute_8781702259830:
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		sw $t4, 0($v0)
		sw $a0, 4($v0)
		lw $t5, 8($t1)
		sw $t5, 8($v0)
		sw $v0, 380($sp) # internal_108 = self.char
		j end_get_attribute_8781702259830
		object_get_attribute_8781702259830:
		sw $t1, 380($sp) # internal_108 = char
		end_get_attribute_8781702259830:
		
		# Allocating String
		li $v0, 9
		addi $a0, $zero, 10 # $a0 = length of string + 9 for 4 bytes for the type, 4 bytes for the length of the string and 1 byte for null-terminator
		syscall
		
		la $t0, type_String
		sw $t0, 0($v0) # Setting type in the first word of the object
		
		addi $t0, $zero, 10
		sw $t0, 4($v0) # Setting length of the string in the second word of the object
		
		addi $t0, $zero, 100
		sb $t0, 8($v0) # internal_109[0] = 'd'
		
		sb $zero, 9($v0) # Null-terminator at the end of the string
		
		sw $v0, 376($sp) # internal_109 = "d"
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument internal_108
		lw $t0, 392($sp)
		sw $t0, 4($sp) # Storing internal_108
		
		# Argument internal_109
		lw $t0, 388($sp)
		sw $t0, 0($sp) # Storing internal_109
		
		# Calling function function_equal
		jal function_equal
		lw $ra, 8($sp)
		sw $v1, 384($sp) # internal_110 = result of function_equal
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# internal_107 = internal_110
		lw $t0, 372($sp)
		sw $t0, 384($sp)
		
		# If internal_107 then goto then_8781702298191
		lw $t0, 384($sp) # Loading the address of the condition
		lw $t0, 8($t0) # Loading the value of the condition
		addi $t1, $zero, 1 # Setting the value to 1 for comparison
		beq $t0, $t1, then_8781702298191
		
		# Jumping to else_8781702298191
		j else_8781702298191
		
		then_8781702298191:
		
		# Allocating C
		li $v0, 9
		lw $a0, type_C
		syscall
		la $t0, type_C # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of th object
		sw $a0, 4($v0) # Setting size in the second word of th object
		sw $v0, 368($sp) # internal_111 = address of allocated object C
		
		# Passing function arguments
		addi $sp, $sp, -8 # Reserving space for arguments
		sw $ra, 4($sp) # Storing return address
		
		# Argument internal_111
		lw $t0, 376($sp)
		sw $t0, 0($sp) # Storing internal_111
		
		# Calling function function___init___at_C
		jal function___init___at_C
		lw $ra, 4($sp)
		sw $v1, 376($sp) # internal_111 = result of function___init___at_C
		addi $sp, $sp, 8 # Freeing space for arguments
		
		# Get attribute avar of self
		lw $t0, 816($sp) # Get the address of self
		lw $t1, 12($t0) # Get the attribute 'avar' from the instance
		lw $t2, 0($t1)
		la $t3, type_Int
		la $t4, type_Bool
		addi $t5, $zero, 1
		seq $t6, $t2, $t3
		beq $t6, $t5, int_get_attribute_8781702259959
		seq $t6, $t2, $t4
		beq $t6, $t5, bool_get_attribute_8781702259959
		j object_get_attribute_8781702259959
		int_get_attribute_8781702259959:
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		sw $t3, 0($v0)
		sw $a0, 4($v0)
		lw $t5, 8($t1)
		sw $t5, 8($v0)
		sw $v0, 364($sp) # internal_112 = self.avar
		j end_get_attribute_8781702259959
		bool_get_attribute_8781702259959:
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		sw $t4, 0($v0)
		sw $a0, 4($v0)
		lw $t5, 8($t1)
		sw $t5, 8($v0)
		sw $v0, 364($sp) # internal_112 = self.avar
		j end_get_attribute_8781702259959
		object_get_attribute_8781702259959:
		sw $t1, 364($sp) # internal_112 = avar
		end_get_attribute_8781702259959:
		
		# Passing function arguments
		addi $sp, $sp, -8 # Reserving space for arguments
		sw $ra, 4($sp) # Storing return address
		
		# Argument internal_112
		lw $t0, 372($sp)
		sw $t0, 0($sp) # Storing internal_112
		
		# Calling function function_value_at_A
		jal function_value_at_A
		lw $ra, 4($sp)
		sw $v1, 368($sp) # internal_113 = result of function_value_at_A
		addi $sp, $sp, 8 # Freeing space for arguments
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument internal_111
		lw $t0, 380($sp)
		sw $t0, 4($sp) # Storing internal_111
		
		# Argument internal_113
		lw $t0, 372($sp)
		sw $t0, 0($sp) # Storing internal_113
		
		# Calling function function_method5_at_C
		jal function_method5_at_C
		lw $ra, 8($sp)
		sw $v1, 368($sp) # internal_114 = result of function_method5_at_C
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# Set attribute avar of self
		lw $t0, 816($sp) # $t0 = self
		lw $t1, 356($sp) # $t1 = internal_114
		beq $t1, $zero, object_set_attribute_8781702259896
		lw $t2, 0($t1)
		la $t3, type_Int
		la $t4, type_Bool
		addi $t5, $zero, 1
		seq $t6, $t2, $t3
		beq $t6, $t5, int_set_attribute_8781702259896
		seq $t6, $t2, $t4
		beq $t6, $t5, bool_set_attribute_8781702259896
		j object_set_attribute_8781702259896
		int_set_attribute_8781702259896:
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		sw $t3, 0($v0)
		sw $a0, 4($v0)
		lw $t5, 8($t1)
		sw $t5, 8($v0)
		sw $v0, 12($t0) # self.avar = internal_114
		j end_set_attribute_8781702259896
		bool_set_attribute_8781702259896:
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		sw $t4, 0($v0)
		sw $a0, 4($v0)
		lw $t5, 8($t1)
		sw $t5, 8($v0)
		sw $v0, 12($t0) # self.avar = internal_114
		j end_set_attribute_8781702259896
		object_set_attribute_8781702259896:
		sw $t1, 12($t0) # self.avar = internal_114
		end_set_attribute_8781702259896:
		
		# internal_106 = internal_114
		lw $t0, 356($sp)
		sw $t0, 388($sp)
		
		# Jumping to endif_8781702298191
		j endif_8781702298191
		
		else_8781702298191:
		
		# Allocating Bool 0
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Bool # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 0
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 348($sp) # internal_116 = address of allocated object Int
		
		# Get attribute char of self
		lw $t0, 816($sp) # Get the address of self
		lw $t1, 8($t0) # Get the attribute 'char' from the instance
		lw $t2, 0($t1)
		la $t3, type_Int
		la $t4, type_Bool
		addi $t5, $zero, 1
		seq $t6, $t2, $t3
		beq $t6, $t5, int_get_attribute_8781702260312
		seq $t6, $t2, $t4
		beq $t6, $t5, bool_get_attribute_8781702260312
		j object_get_attribute_8781702260312
		int_get_attribute_8781702260312:
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		sw $t3, 0($v0)
		sw $a0, 4($v0)
		lw $t5, 8($t1)
		sw $t5, 8($v0)
		sw $v0, 344($sp) # internal_117 = self.char
		j end_get_attribute_8781702260312
		bool_get_attribute_8781702260312:
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		sw $t4, 0($v0)
		sw $a0, 4($v0)
		lw $t5, 8($t1)
		sw $t5, 8($v0)
		sw $v0, 344($sp) # internal_117 = self.char
		j end_get_attribute_8781702260312
		object_get_attribute_8781702260312:
		sw $t1, 344($sp) # internal_117 = char
		end_get_attribute_8781702260312:
		
		# Allocating String
		li $v0, 9
		addi $a0, $zero, 10 # $a0 = length of string + 9 for 4 bytes for the type, 4 bytes for the length of the string and 1 byte for null-terminator
		syscall
		
		la $t0, type_String
		sw $t0, 0($v0) # Setting type in the first word of the object
		
		addi $t0, $zero, 10
		sw $t0, 4($v0) # Setting length of the string in the second word of the object
		
		addi $t0, $zero, 101
		sb $t0, 8($v0) # internal_118[0] = 'e'
		
		sb $zero, 9($v0) # Null-terminator at the end of the string
		
		sw $v0, 340($sp) # internal_118 = "e"
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument internal_117
		lw $t0, 356($sp)
		sw $t0, 4($sp) # Storing internal_117
		
		# Argument internal_118
		lw $t0, 352($sp)
		sw $t0, 0($sp) # Storing internal_118
		
		# Calling function function_equal
		jal function_equal
		lw $ra, 8($sp)
		sw $v1, 348($sp) # internal_119 = result of function_equal
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# internal_116 = internal_119
		lw $t0, 336($sp)
		sw $t0, 348($sp)
		
		# If internal_116 then goto then_8781702298185
		lw $t0, 348($sp) # Loading the address of the condition
		lw $t0, 8($t0) # Loading the value of the condition
		addi $t1, $zero, 1 # Setting the value to 1 for comparison
		beq $t0, $t1, then_8781702298185
		
		# Jumping to else_8781702298185
		j else_8781702298185
		
		then_8781702298185:
		
		# Allocating C
		li $v0, 9
		lw $a0, type_C
		syscall
		la $t0, type_C # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of th object
		sw $a0, 4($v0) # Setting size in the second word of th object
		sw $v0, 332($sp) # internal_120 = address of allocated object C
		
		# Passing function arguments
		addi $sp, $sp, -8 # Reserving space for arguments
		sw $ra, 4($sp) # Storing return address
		
		# Argument internal_120
		lw $t0, 340($sp)
		sw $t0, 0($sp) # Storing internal_120
		
		# Calling function function___init___at_C
		jal function___init___at_C
		lw $ra, 4($sp)
		sw $v1, 340($sp) # internal_120 = result of function___init___at_C
		addi $sp, $sp, 8 # Freeing space for arguments
		
		# Get attribute avar of self
		lw $t0, 816($sp) # Get the address of self
		lw $t1, 12($t0) # Get the attribute 'avar' from the instance
		lw $t2, 0($t1)
		la $t3, type_Int
		la $t4, type_Bool
		addi $t5, $zero, 1
		seq $t6, $t2, $t3
		beq $t6, $t5, int_get_attribute_8781702260441
		seq $t6, $t2, $t4
		beq $t6, $t5, bool_get_attribute_8781702260441
		j object_get_attribute_8781702260441
		int_get_attribute_8781702260441:
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		sw $t3, 0($v0)
		sw $a0, 4($v0)
		lw $t5, 8($t1)
		sw $t5, 8($v0)
		sw $v0, 328($sp) # internal_121 = self.avar
		j end_get_attribute_8781702260441
		bool_get_attribute_8781702260441:
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		sw $t4, 0($v0)
		sw $a0, 4($v0)
		lw $t5, 8($t1)
		sw $t5, 8($v0)
		sw $v0, 328($sp) # internal_121 = self.avar
		j end_get_attribute_8781702260441
		object_get_attribute_8781702260441:
		sw $t1, 328($sp) # internal_121 = avar
		end_get_attribute_8781702260441:
		
		# Passing function arguments
		addi $sp, $sp, -8 # Reserving space for arguments
		sw $ra, 4($sp) # Storing return address
		
		# Argument internal_121
		lw $t0, 336($sp)
		sw $t0, 0($sp) # Storing internal_121
		
		# Calling function function_value_at_A
		jal function_value_at_A
		lw $ra, 4($sp)
		sw $v1, 332($sp) # internal_122 = result of function_value_at_A
		addi $sp, $sp, 8 # Freeing space for arguments
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument internal_120
		lw $t0, 344($sp)
		sw $t0, 4($sp) # Storing internal_120
		
		# Argument internal_122
		lw $t0, 336($sp)
		sw $t0, 0($sp) # Storing internal_122
		
		# Calling function function_method5_at_C
		jal function_method5_at_C
		lw $ra, 8($sp)
		sw $v1, 332($sp) # internal_123 = result of function_method5_at_C
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# Set attribute avar of self
		lw $t0, 816($sp) # $t0 = self
		lw $t1, 320($sp) # $t1 = internal_123
		beq $t1, $zero, object_set_attribute_8781702260378
		lw $t2, 0($t1)
		la $t3, type_Int
		la $t4, type_Bool
		addi $t5, $zero, 1
		seq $t6, $t2, $t3
		beq $t6, $t5, int_set_attribute_8781702260378
		seq $t6, $t2, $t4
		beq $t6, $t5, bool_set_attribute_8781702260378
		j object_set_attribute_8781702260378
		int_set_attribute_8781702260378:
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		sw $t3, 0($v0)
		sw $a0, 4($v0)
		lw $t5, 8($t1)
		sw $t5, 8($v0)
		sw $v0, 12($t0) # self.avar = internal_123
		j end_set_attribute_8781702260378
		bool_set_attribute_8781702260378:
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		sw $t4, 0($v0)
		sw $a0, 4($v0)
		lw $t5, 8($t1)
		sw $t5, 8($v0)
		sw $v0, 12($t0) # self.avar = internal_123
		j end_set_attribute_8781702260378
		object_set_attribute_8781702260378:
		sw $t1, 12($t0) # self.avar = internal_123
		end_set_attribute_8781702260378:
		
		# internal_115 = internal_123
		lw $t0, 320($sp)
		sw $t0, 352($sp)
		
		# Jumping to endif_8781702298185
		j endif_8781702298185
		
		else_8781702298185:
		
		# Allocating Bool 0
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Bool # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 0
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 312($sp) # internal_125 = address of allocated object Int
		
		# Get attribute char of self
		lw $t0, 816($sp) # Get the address of self
		lw $t1, 8($t0) # Get the attribute 'char' from the instance
		lw $t2, 0($t1)
		la $t3, type_Int
		la $t4, type_Bool
		addi $t5, $zero, 1
		seq $t6, $t2, $t3
		beq $t6, $t5, int_get_attribute_8781702260794
		seq $t6, $t2, $t4
		beq $t6, $t5, bool_get_attribute_8781702260794
		j object_get_attribute_8781702260794
		int_get_attribute_8781702260794:
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		sw $t3, 0($v0)
		sw $a0, 4($v0)
		lw $t5, 8($t1)
		sw $t5, 8($v0)
		sw $v0, 308($sp) # internal_126 = self.char
		j end_get_attribute_8781702260794
		bool_get_attribute_8781702260794:
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		sw $t4, 0($v0)
		sw $a0, 4($v0)
		lw $t5, 8($t1)
		sw $t5, 8($v0)
		sw $v0, 308($sp) # internal_126 = self.char
		j end_get_attribute_8781702260794
		object_get_attribute_8781702260794:
		sw $t1, 308($sp) # internal_126 = char
		end_get_attribute_8781702260794:
		
		# Allocating String
		li $v0, 9
		addi $a0, $zero, 10 # $a0 = length of string + 9 for 4 bytes for the type, 4 bytes for the length of the string and 1 byte for null-terminator
		syscall
		
		la $t0, type_String
		sw $t0, 0($v0) # Setting type in the first word of the object
		
		addi $t0, $zero, 10
		sw $t0, 4($v0) # Setting length of the string in the second word of the object
		
		addi $t0, $zero, 102
		sb $t0, 8($v0) # internal_127[0] = 'f'
		
		sb $zero, 9($v0) # Null-terminator at the end of the string
		
		sw $v0, 304($sp) # internal_127 = "f"
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument internal_126
		lw $t0, 320($sp)
		sw $t0, 4($sp) # Storing internal_126
		
		# Argument internal_127
		lw $t0, 316($sp)
		sw $t0, 0($sp) # Storing internal_127
		
		# Calling function function_equal
		jal function_equal
		lw $ra, 8($sp)
		sw $v1, 312($sp) # internal_128 = result of function_equal
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# internal_125 = internal_128
		lw $t0, 300($sp)
		sw $t0, 312($sp)
		
		# If internal_125 then goto then_8781702298179
		lw $t0, 312($sp) # Loading the address of the condition
		lw $t0, 8($t0) # Loading the value of the condition
		addi $t1, $zero, 1 # Setting the value to 1 for comparison
		beq $t0, $t1, then_8781702298179
		
		# Jumping to else_8781702298179
		j else_8781702298179
		
		then_8781702298179:
		
		# Allocating C
		li $v0, 9
		lw $a0, type_C
		syscall
		la $t0, type_C # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of th object
		sw $a0, 4($v0) # Setting size in the second word of th object
		sw $v0, 296($sp) # internal_129 = address of allocated object C
		
		# Passing function arguments
		addi $sp, $sp, -8 # Reserving space for arguments
		sw $ra, 4($sp) # Storing return address
		
		# Argument internal_129
		lw $t0, 304($sp)
		sw $t0, 0($sp) # Storing internal_129
		
		# Calling function function___init___at_C
		jal function___init___at_C
		lw $ra, 4($sp)
		sw $v1, 304($sp) # internal_129 = result of function___init___at_C
		addi $sp, $sp, 8 # Freeing space for arguments
		
		# Get attribute avar of self
		lw $t0, 816($sp) # Get the address of self
		lw $t1, 12($t0) # Get the attribute 'avar' from the instance
		lw $t2, 0($t1)
		la $t3, type_Int
		la $t4, type_Bool
		addi $t5, $zero, 1
		seq $t6, $t2, $t3
		beq $t6, $t5, int_get_attribute_8781702260923
		seq $t6, $t2, $t4
		beq $t6, $t5, bool_get_attribute_8781702260923
		j object_get_attribute_8781702260923
		int_get_attribute_8781702260923:
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		sw $t3, 0($v0)
		sw $a0, 4($v0)
		lw $t5, 8($t1)
		sw $t5, 8($v0)
		sw $v0, 292($sp) # internal_130 = self.avar
		j end_get_attribute_8781702260923
		bool_get_attribute_8781702260923:
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		sw $t4, 0($v0)
		sw $a0, 4($v0)
		lw $t5, 8($t1)
		sw $t5, 8($v0)
		sw $v0, 292($sp) # internal_130 = self.avar
		j end_get_attribute_8781702260923
		object_get_attribute_8781702260923:
		sw $t1, 292($sp) # internal_130 = avar
		end_get_attribute_8781702260923:
		
		# Passing function arguments
		addi $sp, $sp, -8 # Reserving space for arguments
		sw $ra, 4($sp) # Storing return address
		
		# Argument internal_130
		lw $t0, 300($sp)
		sw $t0, 0($sp) # Storing internal_130
		
		# Calling function function_value_at_A
		jal function_value_at_A
		lw $ra, 4($sp)
		sw $v1, 296($sp) # internal_131 = result of function_value_at_A
		addi $sp, $sp, 8 # Freeing space for arguments
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument internal_129
		lw $t0, 308($sp)
		sw $t0, 4($sp) # Storing internal_129
		
		# Argument internal_131
		lw $t0, 300($sp)
		sw $t0, 0($sp) # Storing internal_131
		
		# Calling function function_method5_at_C
		jal function_method5_at_C
		lw $ra, 8($sp)
		sw $v1, 296($sp) # internal_132 = result of function_method5_at_C
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# Set attribute avar of self
		lw $t0, 816($sp) # $t0 = self
		lw $t1, 284($sp) # $t1 = internal_132
		beq $t1, $zero, object_set_attribute_8781702260860
		lw $t2, 0($t1)
		la $t3, type_Int
		la $t4, type_Bool
		addi $t5, $zero, 1
		seq $t6, $t2, $t3
		beq $t6, $t5, int_set_attribute_8781702260860
		seq $t6, $t2, $t4
		beq $t6, $t5, bool_set_attribute_8781702260860
		j object_set_attribute_8781702260860
		int_set_attribute_8781702260860:
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		sw $t3, 0($v0)
		sw $a0, 4($v0)
		lw $t5, 8($t1)
		sw $t5, 8($v0)
		sw $v0, 12($t0) # self.avar = internal_132
		j end_set_attribute_8781702260860
		bool_set_attribute_8781702260860:
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		sw $t4, 0($v0)
		sw $a0, 4($v0)
		lw $t5, 8($t1)
		sw $t5, 8($v0)
		sw $v0, 12($t0) # self.avar = internal_132
		j end_set_attribute_8781702260860
		object_set_attribute_8781702260860:
		sw $t1, 12($t0) # self.avar = internal_132
		end_set_attribute_8781702260860:
		
		# internal_124 = internal_132
		lw $t0, 284($sp)
		sw $t0, 316($sp)
		
		# Jumping to endif_8781702298179
		j endif_8781702298179
		
		else_8781702298179:
		
		# Allocating Bool 0
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Bool # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 0
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 276($sp) # internal_134 = address of allocated object Int
		
		# Get attribute char of self
		lw $t0, 816($sp) # Get the address of self
		lw $t1, 8($t0) # Get the attribute 'char' from the instance
		lw $t2, 0($t1)
		la $t3, type_Int
		la $t4, type_Bool
		addi $t5, $zero, 1
		seq $t6, $t2, $t3
		beq $t6, $t5, int_get_attribute_8781702261532
		seq $t6, $t2, $t4
		beq $t6, $t5, bool_get_attribute_8781702261532
		j object_get_attribute_8781702261532
		int_get_attribute_8781702261532:
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		sw $t3, 0($v0)
		sw $a0, 4($v0)
		lw $t5, 8($t1)
		sw $t5, 8($v0)
		sw $v0, 272($sp) # internal_135 = self.char
		j end_get_attribute_8781702261532
		bool_get_attribute_8781702261532:
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		sw $t4, 0($v0)
		sw $a0, 4($v0)
		lw $t5, 8($t1)
		sw $t5, 8($v0)
		sw $v0, 272($sp) # internal_135 = self.char
		j end_get_attribute_8781702261532
		object_get_attribute_8781702261532:
		sw $t1, 272($sp) # internal_135 = char
		end_get_attribute_8781702261532:
		
		# Allocating String
		li $v0, 9
		addi $a0, $zero, 10 # $a0 = length of string + 9 for 4 bytes for the type, 4 bytes for the length of the string and 1 byte for null-terminator
		syscall
		
		la $t0, type_String
		sw $t0, 0($v0) # Setting type in the first word of the object
		
		addi $t0, $zero, 10
		sw $t0, 4($v0) # Setting length of the string in the second word of the object
		
		addi $t0, $zero, 103
		sb $t0, 8($v0) # internal_136[0] = 'g'
		
		sb $zero, 9($v0) # Null-terminator at the end of the string
		
		sw $v0, 268($sp) # internal_136 = "g"
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument internal_135
		lw $t0, 284($sp)
		sw $t0, 4($sp) # Storing internal_135
		
		# Argument internal_136
		lw $t0, 280($sp)
		sw $t0, 0($sp) # Storing internal_136
		
		# Calling function function_equal
		jal function_equal
		lw $ra, 8($sp)
		sw $v1, 276($sp) # internal_137 = result of function_equal
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# internal_134 = internal_137
		lw $t0, 264($sp)
		sw $t0, 276($sp)
		
		# If internal_134 then goto then_8781702298173
		lw $t0, 276($sp) # Loading the address of the condition
		lw $t0, 8($t0) # Loading the value of the condition
		addi $t1, $zero, 1 # Setting the value to 1 for comparison
		beq $t0, $t1, then_8781702298173
		
		# Jumping to else_8781702298173
		j else_8781702298173
		
		then_8781702298173:
		
		# Allocating Bool 0
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Bool # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 0
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 256($sp) # internal_139 = address of allocated object Int
		
		# Allocating D
		li $v0, 9
		lw $a0, type_D
		syscall
		la $t0, type_D # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of th object
		sw $a0, 4($v0) # Setting size in the second word of th object
		sw $v0, 252($sp) # internal_140 = address of allocated object D
		
		# Passing function arguments
		addi $sp, $sp, -8 # Reserving space for arguments
		sw $ra, 4($sp) # Storing return address
		
		# Argument internal_140
		lw $t0, 260($sp)
		sw $t0, 0($sp) # Storing internal_140
		
		# Calling function function___init___at_D
		jal function___init___at_D
		lw $ra, 4($sp)
		sw $v1, 260($sp) # internal_140 = result of function___init___at_D
		addi $sp, $sp, 8 # Freeing space for arguments
		
		# Get attribute avar of self
		lw $t0, 816($sp) # Get the address of self
		lw $t1, 12($t0) # Get the attribute 'avar' from the instance
		lw $t2, 0($t1)
		la $t3, type_Int
		la $t4, type_Bool
		addi $t5, $zero, 1
		seq $t6, $t2, $t3
		beq $t6, $t5, int_get_attribute_8781702261685
		seq $t6, $t2, $t4
		beq $t6, $t5, bool_get_attribute_8781702261685
		j object_get_attribute_8781702261685
		int_get_attribute_8781702261685:
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		sw $t3, 0($v0)
		sw $a0, 4($v0)
		lw $t5, 8($t1)
		sw $t5, 8($v0)
		sw $v0, 248($sp) # internal_141 = self.avar
		j end_get_attribute_8781702261685
		bool_get_attribute_8781702261685:
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		sw $t4, 0($v0)
		sw $a0, 4($v0)
		lw $t5, 8($t1)
		sw $t5, 8($v0)
		sw $v0, 248($sp) # internal_141 = self.avar
		j end_get_attribute_8781702261685
		object_get_attribute_8781702261685:
		sw $t1, 248($sp) # internal_141 = avar
		end_get_attribute_8781702261685:
		
		# Passing function arguments
		addi $sp, $sp, -8 # Reserving space for arguments
		sw $ra, 4($sp) # Storing return address
		
		# Argument internal_141
		lw $t0, 256($sp)
		sw $t0, 0($sp) # Storing internal_141
		
		# Calling function function_value_at_A
		jal function_value_at_A
		lw $ra, 4($sp)
		sw $v1, 252($sp) # internal_142 = result of function_value_at_A
		addi $sp, $sp, 8 # Freeing space for arguments
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument internal_140
		lw $t0, 264($sp)
		sw $t0, 4($sp) # Storing internal_140
		
		# Argument internal_142
		lw $t0, 256($sp)
		sw $t0, 0($sp) # Storing internal_142
		
		# Calling function function_method7_at_D
		jal function_method7_at_D
		lw $ra, 8($sp)
		sw $v1, 252($sp) # internal_143 = result of function_method7_at_D
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# internal_139 = internal_143
		lw $t0, 240($sp)
		sw $t0, 256($sp)
		
		# If internal_139 then goto then_8781702296820
		lw $t0, 256($sp) # Loading the address of the condition
		lw $t0, 8($t0) # Loading the value of the condition
		addi $t1, $zero, 1 # Setting the value to 1 for comparison
		beq $t0, $t1, then_8781702296820
		
		# Jumping to else_8781702296820
		j else_8781702296820
		
		then_8781702296820:
		
		# Allocating String
		li $v0, 9
		addi $a0, $zero, 16 # $a0 = length of string + 9 for 4 bytes for the type, 4 bytes for the length of the string and 1 byte for null-terminator
		syscall
		
		la $t0, type_String
		sw $t0, 0($v0) # Setting type in the first word of the object
		
		addi $t0, $zero, 16
		sw $t0, 4($v0) # Setting length of the string in the second word of the object
		
		addi $t0, $zero, 110
		sb $t0, 8($v0) # internal_144[0] = 'n'
		
		addi $t0, $zero, 117
		sb $t0, 9($v0) # internal_144[1] = 'u'
		
		addi $t0, $zero, 109
		sb $t0, 10($v0) # internal_144[2] = 'm'
		
		addi $t0, $zero, 98
		sb $t0, 11($v0) # internal_144[3] = 'b'
		
		addi $t0, $zero, 101
		sb $t0, 12($v0) # internal_144[4] = 'e'
		
		addi $t0, $zero, 114
		sb $t0, 13($v0) # internal_144[5] = 'r'
		
		addi $t0, $zero, 32
		sb $t0, 14($v0) # internal_144[6] = ' '
		
		sb $zero, 15($v0) # Null-terminator at the end of the string
		
		sw $v0, 236($sp) # internal_144 = "number "
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument self
		lw $t0, 828($sp)
		sw $t0, 4($sp) # Storing self
		
		# Argument internal_144
		lw $t0, 248($sp)
		sw $t0, 0($sp) # Storing internal_144
		
		# Calling function function_out_string_at_IO
		jal function_out_string_at_IO
		lw $ra, 8($sp)
		sw $v1, 244($sp) # internal_145 = result of function_out_string_at_IO
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# Get attribute avar of self
		lw $t0, 816($sp) # Get the address of self
		lw $t1, 12($t0) # Get the attribute 'avar' from the instance
		lw $t2, 0($t1)
		la $t3, type_Int
		la $t4, type_Bool
		addi $t5, $zero, 1
		seq $t6, $t2, $t3
		beq $t6, $t5, int_get_attribute_8781702229553
		seq $t6, $t2, $t4
		beq $t6, $t5, bool_get_attribute_8781702229553
		j object_get_attribute_8781702229553
		int_get_attribute_8781702229553:
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		sw $t3, 0($v0)
		sw $a0, 4($v0)
		lw $t5, 8($t1)
		sw $t5, 8($v0)
		sw $v0, 228($sp) # internal_146 = self.avar
		j end_get_attribute_8781702229553
		bool_get_attribute_8781702229553:
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		sw $t4, 0($v0)
		sw $a0, 4($v0)
		lw $t5, 8($t1)
		sw $t5, 8($v0)
		sw $v0, 228($sp) # internal_146 = self.avar
		j end_get_attribute_8781702229553
		object_get_attribute_8781702229553:
		sw $t1, 228($sp) # internal_146 = avar
		end_get_attribute_8781702229553:
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument self
		lw $t0, 828($sp)
		sw $t0, 4($sp) # Storing self
		
		# Argument internal_146
		lw $t0, 240($sp)
		sw $t0, 0($sp) # Storing internal_146
		
		# Calling function function_print_at_Main
		jal function_print_at_Main
		lw $ra, 8($sp)
		sw $v1, 236($sp) # internal_147 = result of function_print_at_Main
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# Allocating String
		li $v0, 9
		addi $a0, $zero, 28 # $a0 = length of string + 9 for 4 bytes for the type, 4 bytes for the length of the string and 1 byte for null-terminator
		syscall
		
		la $t0, type_String
		sw $t0, 0($v0) # Setting type in the first word of the object
		
		addi $t0, $zero, 28
		sw $t0, 4($v0) # Setting length of the string in the second word of the object
		
		addi $t0, $zero, 105
		sb $t0, 8($v0) # internal_148[0] = 'i'
		
		addi $t0, $zero, 115
		sb $t0, 9($v0) # internal_148[1] = 's'
		
		addi $t0, $zero, 32
		sb $t0, 10($v0) # internal_148[2] = ' '
		
		addi $t0, $zero, 100
		sb $t0, 11($v0) # internal_148[3] = 'd'
		
		addi $t0, $zero, 105
		sb $t0, 12($v0) # internal_148[4] = 'i'
		
		addi $t0, $zero, 118
		sb $t0, 13($v0) # internal_148[5] = 'v'
		
		addi $t0, $zero, 105
		sb $t0, 14($v0) # internal_148[6] = 'i'
		
		addi $t0, $zero, 115
		sb $t0, 15($v0) # internal_148[7] = 's'
		
		addi $t0, $zero, 105
		sb $t0, 16($v0) # internal_148[8] = 'i'
		
		addi $t0, $zero, 98
		sb $t0, 17($v0) # internal_148[9] = 'b'
		
		addi $t0, $zero, 108
		sb $t0, 18($v0) # internal_148[10] = 'l'
		
		addi $t0, $zero, 101
		sb $t0, 19($v0) # internal_148[11] = 'e'
		
		addi $t0, $zero, 32
		sb $t0, 20($v0) # internal_148[12] = ' '
		
		addi $t0, $zero, 98
		sb $t0, 21($v0) # internal_148[13] = 'b'
		
		addi $t0, $zero, 121
		sb $t0, 22($v0) # internal_148[14] = 'y'
		
		addi $t0, $zero, 32
		sb $t0, 23($v0) # internal_148[15] = ' '
		
		addi $t0, $zero, 51
		sb $t0, 24($v0) # internal_148[16] = '3'
		
		addi $t0, $zero, 46
		sb $t0, 25($v0) # internal_148[17] = '.'
		
		addi $t0, $zero, 10
		sb $t0, 26($v0) # internal_148[18] = '\n'
		
		sb $zero, 27($v0) # Null-terminator at the end of the string
		
		sw $v0, 220($sp) # internal_148 = "is divisible by 3.\n"
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument self
		lw $t0, 828($sp)
		sw $t0, 4($sp) # Storing self
		
		# Argument internal_148
		lw $t0, 232($sp)
		sw $t0, 0($sp) # Storing internal_148
		
		# Calling function function_out_string_at_IO
		jal function_out_string_at_IO
		lw $ra, 8($sp)
		sw $v1, 228($sp) # internal_149 = result of function_out_string_at_IO
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# internal_138 = internal_149
		lw $t0, 216($sp)
		sw $t0, 260($sp)
		
		# Jumping to endif_8781702296820
		j endif_8781702296820
		
		else_8781702296820:
		
		# Allocating String
		li $v0, 9
		addi $a0, $zero, 16 # $a0 = length of string + 9 for 4 bytes for the type, 4 bytes for the length of the string and 1 byte for null-terminator
		syscall
		
		la $t0, type_String
		sw $t0, 0($v0) # Setting type in the first word of the object
		
		addi $t0, $zero, 16
		sw $t0, 4($v0) # Setting length of the string in the second word of the object
		
		addi $t0, $zero, 110
		sb $t0, 8($v0) # internal_150[0] = 'n'
		
		addi $t0, $zero, 117
		sb $t0, 9($v0) # internal_150[1] = 'u'
		
		addi $t0, $zero, 109
		sb $t0, 10($v0) # internal_150[2] = 'm'
		
		addi $t0, $zero, 98
		sb $t0, 11($v0) # internal_150[3] = 'b'
		
		addi $t0, $zero, 101
		sb $t0, 12($v0) # internal_150[4] = 'e'
		
		addi $t0, $zero, 114
		sb $t0, 13($v0) # internal_150[5] = 'r'
		
		addi $t0, $zero, 32
		sb $t0, 14($v0) # internal_150[6] = ' '
		
		sb $zero, 15($v0) # Null-terminator at the end of the string
		
		sw $v0, 212($sp) # internal_150 = "number "
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument self
		lw $t0, 828($sp)
		sw $t0, 4($sp) # Storing self
		
		# Argument internal_150
		lw $t0, 224($sp)
		sw $t0, 0($sp) # Storing internal_150
		
		# Calling function function_out_string_at_IO
		jal function_out_string_at_IO
		lw $ra, 8($sp)
		sw $v1, 220($sp) # internal_151 = result of function_out_string_at_IO
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# Get attribute avar of self
		lw $t0, 816($sp) # Get the address of self
		lw $t1, 12($t0) # Get the attribute 'avar' from the instance
		lw $t2, 0($t1)
		la $t3, type_Int
		la $t4, type_Bool
		addi $t5, $zero, 1
		seq $t6, $t2, $t3
		beq $t6, $t5, int_get_attribute_8781702229682
		seq $t6, $t2, $t4
		beq $t6, $t5, bool_get_attribute_8781702229682
		j object_get_attribute_8781702229682
		int_get_attribute_8781702229682:
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		sw $t3, 0($v0)
		sw $a0, 4($v0)
		lw $t5, 8($t1)
		sw $t5, 8($v0)
		sw $v0, 204($sp) # internal_152 = self.avar
		j end_get_attribute_8781702229682
		bool_get_attribute_8781702229682:
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		sw $t4, 0($v0)
		sw $a0, 4($v0)
		lw $t5, 8($t1)
		sw $t5, 8($v0)
		sw $v0, 204($sp) # internal_152 = self.avar
		j end_get_attribute_8781702229682
		object_get_attribute_8781702229682:
		sw $t1, 204($sp) # internal_152 = avar
		end_get_attribute_8781702229682:
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument self
		lw $t0, 828($sp)
		sw $t0, 4($sp) # Storing self
		
		# Argument internal_152
		lw $t0, 216($sp)
		sw $t0, 0($sp) # Storing internal_152
		
		# Calling function function_print_at_Main
		jal function_print_at_Main
		lw $ra, 8($sp)
		sw $v1, 212($sp) # internal_153 = result of function_print_at_Main
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# Allocating String
		li $v0, 9
		addi $a0, $zero, 32 # $a0 = length of string + 9 for 4 bytes for the type, 4 bytes for the length of the string and 1 byte for null-terminator
		syscall
		
		la $t0, type_String
		sw $t0, 0($v0) # Setting type in the first word of the object
		
		addi $t0, $zero, 32
		sw $t0, 4($v0) # Setting length of the string in the second word of the object
		
		addi $t0, $zero, 105
		sb $t0, 8($v0) # internal_154[0] = 'i'
		
		addi $t0, $zero, 115
		sb $t0, 9($v0) # internal_154[1] = 's'
		
		addi $t0, $zero, 32
		sb $t0, 10($v0) # internal_154[2] = ' '
		
		addi $t0, $zero, 110
		sb $t0, 11($v0) # internal_154[3] = 'n'
		
		addi $t0, $zero, 111
		sb $t0, 12($v0) # internal_154[4] = 'o'
		
		addi $t0, $zero, 116
		sb $t0, 13($v0) # internal_154[5] = 't'
		
		addi $t0, $zero, 32
		sb $t0, 14($v0) # internal_154[6] = ' '
		
		addi $t0, $zero, 100
		sb $t0, 15($v0) # internal_154[7] = 'd'
		
		addi $t0, $zero, 105
		sb $t0, 16($v0) # internal_154[8] = 'i'
		
		addi $t0, $zero, 118
		sb $t0, 17($v0) # internal_154[9] = 'v'
		
		addi $t0, $zero, 105
		sb $t0, 18($v0) # internal_154[10] = 'i'
		
		addi $t0, $zero, 115
		sb $t0, 19($v0) # internal_154[11] = 's'
		
		addi $t0, $zero, 105
		sb $t0, 20($v0) # internal_154[12] = 'i'
		
		addi $t0, $zero, 98
		sb $t0, 21($v0) # internal_154[13] = 'b'
		
		addi $t0, $zero, 108
		sb $t0, 22($v0) # internal_154[14] = 'l'
		
		addi $t0, $zero, 101
		sb $t0, 23($v0) # internal_154[15] = 'e'
		
		addi $t0, $zero, 32
		sb $t0, 24($v0) # internal_154[16] = ' '
		
		addi $t0, $zero, 98
		sb $t0, 25($v0) # internal_154[17] = 'b'
		
		addi $t0, $zero, 121
		sb $t0, 26($v0) # internal_154[18] = 'y'
		
		addi $t0, $zero, 32
		sb $t0, 27($v0) # internal_154[19] = ' '
		
		addi $t0, $zero, 51
		sb $t0, 28($v0) # internal_154[20] = '3'
		
		addi $t0, $zero, 46
		sb $t0, 29($v0) # internal_154[21] = '.'
		
		addi $t0, $zero, 10
		sb $t0, 30($v0) # internal_154[22] = '\n'
		
		sb $zero, 31($v0) # Null-terminator at the end of the string
		
		sw $v0, 196($sp) # internal_154 = "is not divisible by 3.\n"
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument self
		lw $t0, 828($sp)
		sw $t0, 4($sp) # Storing self
		
		# Argument internal_154
		lw $t0, 208($sp)
		sw $t0, 0($sp) # Storing internal_154
		
		# Calling function function_out_string_at_IO
		jal function_out_string_at_IO
		lw $ra, 8($sp)
		sw $v1, 204($sp) # internal_155 = result of function_out_string_at_IO
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# internal_138 = internal_155
		lw $t0, 192($sp)
		sw $t0, 260($sp)
		
		# Jumping to endif_8781702296820
		j endif_8781702296820
		
		endif_8781702296820:
		
		# internal_133 = internal_138
		lw $t0, 260($sp)
		sw $t0, 280($sp)
		
		# Jumping to endif_8781702298173
		j endif_8781702298173
		
		else_8781702298173:
		
		# Allocating Bool 0
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Bool # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 0
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 184($sp) # internal_157 = address of allocated object Int
		
		# Get attribute char of self
		lw $t0, 816($sp) # Get the address of self
		lw $t1, 8($t0) # Get the attribute 'char' from the instance
		lw $t2, 0($t1)
		la $t3, type_Int
		la $t4, type_Bool
		addi $t5, $zero, 1
		seq $t6, $t2, $t3
		beq $t6, $t5, int_get_attribute_8781702230062
		seq $t6, $t2, $t4
		beq $t6, $t5, bool_get_attribute_8781702230062
		j object_get_attribute_8781702230062
		int_get_attribute_8781702230062:
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		sw $t3, 0($v0)
		sw $a0, 4($v0)
		lw $t5, 8($t1)
		sw $t5, 8($v0)
		sw $v0, 180($sp) # internal_158 = self.char
		j end_get_attribute_8781702230062
		bool_get_attribute_8781702230062:
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		sw $t4, 0($v0)
		sw $a0, 4($v0)
		lw $t5, 8($t1)
		sw $t5, 8($v0)
		sw $v0, 180($sp) # internal_158 = self.char
		j end_get_attribute_8781702230062
		object_get_attribute_8781702230062:
		sw $t1, 180($sp) # internal_158 = char
		end_get_attribute_8781702230062:
		
		# Allocating String
		li $v0, 9
		addi $a0, $zero, 10 # $a0 = length of string + 9 for 4 bytes for the type, 4 bytes for the length of the string and 1 byte for null-terminator
		syscall
		
		la $t0, type_String
		sw $t0, 0($v0) # Setting type in the first word of the object
		
		addi $t0, $zero, 10
		sw $t0, 4($v0) # Setting length of the string in the second word of the object
		
		addi $t0, $zero, 104
		sb $t0, 8($v0) # internal_159[0] = 'h'
		
		sb $zero, 9($v0) # Null-terminator at the end of the string
		
		sw $v0, 176($sp) # internal_159 = "h"
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument internal_158
		lw $t0, 192($sp)
		sw $t0, 4($sp) # Storing internal_158
		
		# Argument internal_159
		lw $t0, 188($sp)
		sw $t0, 0($sp) # Storing internal_159
		
		# Calling function function_equal
		jal function_equal
		lw $ra, 8($sp)
		sw $v1, 184($sp) # internal_160 = result of function_equal
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# internal_157 = internal_160
		lw $t0, 172($sp)
		sw $t0, 184($sp)
		
		# If internal_157 then goto then_8781702298167
		lw $t0, 184($sp) # Loading the address of the condition
		lw $t0, 8($t0) # Loading the value of the condition
		addi $t1, $zero, 1 # Setting the value to 1 for comparison
		beq $t0, $t1, then_8781702298167
		
		# Jumping to else_8781702298167
		j else_8781702298167
		
		then_8781702298167:
		
		# Allocating NUll to x
		sw $zero, 168($sp) # x = 0
		
		# Allocating E
		li $v0, 9
		lw $a0, type_E
		syscall
		la $t0, type_E # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of th object
		sw $a0, 4($v0) # Setting size in the second word of th object
		sw $v0, 164($sp) # internal_162 = address of allocated object E
		
		# Passing function arguments
		addi $sp, $sp, -8 # Reserving space for arguments
		sw $ra, 4($sp) # Storing return address
		
		# Argument internal_162
		lw $t0, 172($sp)
		sw $t0, 0($sp) # Storing internal_162
		
		# Calling function function___init___at_E
		jal function___init___at_E
		lw $ra, 4($sp)
		sw $v1, 172($sp) # internal_162 = result of function___init___at_E
		addi $sp, $sp, 8 # Freeing space for arguments
		
		# Get attribute avar of self
		lw $t0, 816($sp) # Get the address of self
		lw $t1, 12($t0) # Get the attribute 'avar' from the instance
		lw $t2, 0($t1)
		la $t3, type_Int
		la $t4, type_Bool
		addi $t5, $zero, 1
		seq $t6, $t2, $t3
		beq $t6, $t5, int_get_attribute_8781702230236
		seq $t6, $t2, $t4
		beq $t6, $t5, bool_get_attribute_8781702230236
		j object_get_attribute_8781702230236
		int_get_attribute_8781702230236:
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		sw $t3, 0($v0)
		sw $a0, 4($v0)
		lw $t5, 8($t1)
		sw $t5, 8($v0)
		sw $v0, 160($sp) # internal_163 = self.avar
		j end_get_attribute_8781702230236
		bool_get_attribute_8781702230236:
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		sw $t4, 0($v0)
		sw $a0, 4($v0)
		lw $t5, 8($t1)
		sw $t5, 8($v0)
		sw $v0, 160($sp) # internal_163 = self.avar
		j end_get_attribute_8781702230236
		object_get_attribute_8781702230236:
		sw $t1, 160($sp) # internal_163 = avar
		end_get_attribute_8781702230236:
		
		# Passing function arguments
		addi $sp, $sp, -8 # Reserving space for arguments
		sw $ra, 4($sp) # Storing return address
		
		# Argument internal_163
		lw $t0, 168($sp)
		sw $t0, 0($sp) # Storing internal_163
		
		# Calling function function_value_at_A
		jal function_value_at_A
		lw $ra, 4($sp)
		sw $v1, 164($sp) # internal_164 = result of function_value_at_A
		addi $sp, $sp, 8 # Freeing space for arguments
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument internal_162
		lw $t0, 176($sp)
		sw $t0, 4($sp) # Storing internal_162
		
		# Argument internal_164
		lw $t0, 168($sp)
		sw $t0, 0($sp) # Storing internal_164
		
		# Calling function function_method6_at_E
		jal function_method6_at_E
		lw $ra, 8($sp)
		sw $v1, 164($sp) # internal_165 = result of function_method6_at_E
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument x
		lw $t0, 180($sp)
		sw $t0, 4($sp) # Storing x
		
		# Argument internal_165
		lw $t0, 164($sp)
		sw $t0, 0($sp) # Storing internal_165
		
		# Calling function function_assign
		jal function_assign
		lw $ra, 8($sp)
		sw $v1, 180($sp) # x = result of function_assign
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# Get attribute avar of self
		lw $t0, 816($sp) # Get the address of self
		lw $t1, 12($t0) # Get the attribute 'avar' from the instance
		lw $t2, 0($t1)
		la $t3, type_Int
		la $t4, type_Bool
		addi $t5, $zero, 1
		seq $t6, $t2, $t3
		beq $t6, $t5, int_get_attribute_8781702230330
		seq $t6, $t2, $t4
		beq $t6, $t5, bool_get_attribute_8781702230330
		j object_get_attribute_8781702230330
		int_get_attribute_8781702230330:
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		sw $t3, 0($v0)
		sw $a0, 4($v0)
		lw $t5, 8($t1)
		sw $t5, 8($v0)
		sw $v0, 144($sp) # internal_167 = self.avar
		j end_get_attribute_8781702230330
		bool_get_attribute_8781702230330:
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		sw $t4, 0($v0)
		sw $a0, 4($v0)
		lw $t5, 8($t1)
		sw $t5, 8($v0)
		sw $v0, 144($sp) # internal_167 = self.avar
		j end_get_attribute_8781702230330
		object_get_attribute_8781702230330:
		sw $t1, 144($sp) # internal_167 = avar
		end_get_attribute_8781702230330:
		
		# Passing function arguments
		addi $sp, $sp, -8 # Reserving space for arguments
		sw $ra, 4($sp) # Storing return address
		
		# Argument internal_167
		lw $t0, 152($sp)
		sw $t0, 0($sp) # Storing internal_167
		
		# Calling function function_value_at_A
		jal function_value_at_A
		lw $ra, 4($sp)
		sw $v1, 148($sp) # internal_168 = result of function_value_at_A
		addi $sp, $sp, 8 # Freeing space for arguments
		
		# Passing function arguments
		addi $sp, $sp, -8 # Reserving space for arguments
		sw $ra, 4($sp) # Storing return address
		
		# Argument x
		lw $t0, 176($sp)
		sw $t0, 0($sp) # Storing x
		
		# Calling function function_value_at_A
		jal function_value_at_A
		lw $ra, 4($sp)
		sw $v1, 144($sp) # internal_169 = result of function_value_at_A
		addi $sp, $sp, 8 # Freeing space for arguments
		
		# Allocating Int 8
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Int # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 8
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 132($sp) # internal_170 = address of allocated object Int
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument internal_169
		lw $t0, 148($sp)
		sw $t0, 4($sp) # Storing internal_169
		
		# Argument internal_170
		lw $t0, 144($sp)
		sw $t0, 0($sp) # Storing internal_170
		
		# Calling function function_mult
		jal function_mult
		lw $ra, 8($sp)
		sw $v1, 140($sp) # internal_171 = result of function_mult
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument internal_168
		lw $t0, 152($sp)
		sw $t0, 4($sp) # Storing internal_168
		
		# Argument internal_171
		lw $t0, 140($sp)
		sw $t0, 0($sp) # Storing internal_171
		
		# Calling function function_sub
		jal function_sub
		lw $ra, 8($sp)
		sw $v1, 136($sp) # internal_172 = result of function_sub
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument r
		lw $t0, 160($sp)
		sw $t0, 4($sp) # Storing r
		
		# Argument internal_172
		lw $t0, 136($sp)
		sw $t0, 0($sp) # Storing internal_172
		
		# Calling function function_assign
		jal function_assign
		lw $ra, 8($sp)
		sw $v1, 160($sp) # r = result of function_assign
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# Allocating String
		li $v0, 9
		addi $a0, $zero, 16 # $a0 = length of string + 9 for 4 bytes for the type, 4 bytes for the length of the string and 1 byte for null-terminator
		syscall
		
		la $t0, type_String
		sw $t0, 0($v0) # Setting type in the first word of the object
		
		addi $t0, $zero, 16
		sw $t0, 4($v0) # Setting length of the string in the second word of the object
		
		addi $t0, $zero, 110
		sb $t0, 8($v0) # internal_173[0] = 'n'
		
		addi $t0, $zero, 117
		sb $t0, 9($v0) # internal_173[1] = 'u'
		
		addi $t0, $zero, 109
		sb $t0, 10($v0) # internal_173[2] = 'm'
		
		addi $t0, $zero, 98
		sb $t0, 11($v0) # internal_173[3] = 'b'
		
		addi $t0, $zero, 101
		sb $t0, 12($v0) # internal_173[4] = 'e'
		
		addi $t0, $zero, 114
		sb $t0, 13($v0) # internal_173[5] = 'r'
		
		addi $t0, $zero, 32
		sb $t0, 14($v0) # internal_173[6] = ' '
		
		sb $zero, 15($v0) # Null-terminator at the end of the string
		
		sw $v0, 120($sp) # internal_173 = "number "
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument self
		lw $t0, 828($sp)
		sw $t0, 4($sp) # Storing self
		
		# Argument internal_173
		lw $t0, 132($sp)
		sw $t0, 0($sp) # Storing internal_173
		
		# Calling function function_out_string_at_IO
		jal function_out_string_at_IO
		lw $ra, 8($sp)
		sw $v1, 128($sp) # internal_174 = result of function_out_string_at_IO
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# Get attribute avar of self
		lw $t0, 816($sp) # Get the address of self
		lw $t1, 12($t0) # Get the attribute 'avar' from the instance
		lw $t2, 0($t1)
		la $t3, type_Int
		la $t4, type_Bool
		addi $t5, $zero, 1
		seq $t6, $t2, $t3
		beq $t6, $t5, int_get_attribute_8781702230501
		seq $t6, $t2, $t4
		beq $t6, $t5, bool_get_attribute_8781702230501
		j object_get_attribute_8781702230501
		int_get_attribute_8781702230501:
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		sw $t3, 0($v0)
		sw $a0, 4($v0)
		lw $t5, 8($t1)
		sw $t5, 8($v0)
		sw $v0, 112($sp) # internal_175 = self.avar
		j end_get_attribute_8781702230501
		bool_get_attribute_8781702230501:
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		sw $t4, 0($v0)
		sw $a0, 4($v0)
		lw $t5, 8($t1)
		sw $t5, 8($v0)
		sw $v0, 112($sp) # internal_175 = self.avar
		j end_get_attribute_8781702230501
		object_get_attribute_8781702230501:
		sw $t1, 112($sp) # internal_175 = avar
		end_get_attribute_8781702230501:
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument self
		lw $t0, 828($sp)
		sw $t0, 4($sp) # Storing self
		
		# Argument internal_175
		lw $t0, 124($sp)
		sw $t0, 0($sp) # Storing internal_175
		
		# Calling function function_print_at_Main
		jal function_print_at_Main
		lw $ra, 8($sp)
		sw $v1, 120($sp) # internal_176 = result of function_print_at_Main
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# Allocating String
		li $v0, 9
		addi $a0, $zero, 21 # $a0 = length of string + 9 for 4 bytes for the type, 4 bytes for the length of the string and 1 byte for null-terminator
		syscall
		
		la $t0, type_String
		sw $t0, 0($v0) # Setting type in the first word of the object
		
		addi $t0, $zero, 21
		sw $t0, 4($v0) # Setting length of the string in the second word of the object
		
		addi $t0, $zero, 105
		sb $t0, 8($v0) # internal_177[0] = 'i'
		
		addi $t0, $zero, 115
		sb $t0, 9($v0) # internal_177[1] = 's'
		
		addi $t0, $zero, 32
		sb $t0, 10($v0) # internal_177[2] = ' '
		
		addi $t0, $zero, 101
		sb $t0, 11($v0) # internal_177[3] = 'e'
		
		addi $t0, $zero, 113
		sb $t0, 12($v0) # internal_177[4] = 'q'
		
		addi $t0, $zero, 117
		sb $t0, 13($v0) # internal_177[5] = 'u'
		
		addi $t0, $zero, 97
		sb $t0, 14($v0) # internal_177[6] = 'a'
		
		addi $t0, $zero, 108
		sb $t0, 15($v0) # internal_177[7] = 'l'
		
		addi $t0, $zero, 32
		sb $t0, 16($v0) # internal_177[8] = ' '
		
		addi $t0, $zero, 116
		sb $t0, 17($v0) # internal_177[9] = 't'
		
		addi $t0, $zero, 111
		sb $t0, 18($v0) # internal_177[10] = 'o'
		
		addi $t0, $zero, 32
		sb $t0, 19($v0) # internal_177[11] = ' '
		
		sb $zero, 20($v0) # Null-terminator at the end of the string
		
		sw $v0, 104($sp) # internal_177 = "is equal to "
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument self
		lw $t0, 828($sp)
		sw $t0, 4($sp) # Storing self
		
		# Argument internal_177
		lw $t0, 116($sp)
		sw $t0, 0($sp) # Storing internal_177
		
		# Calling function function_out_string_at_IO
		jal function_out_string_at_IO
		lw $ra, 8($sp)
		sw $v1, 112($sp) # internal_178 = result of function_out_string_at_IO
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument self
		lw $t0, 828($sp)
		sw $t0, 4($sp) # Storing self
		
		# Argument x
		lw $t0, 180($sp)
		sw $t0, 0($sp) # Storing x
		
		# Calling function function_print_at_Main
		jal function_print_at_Main
		lw $ra, 8($sp)
		sw $v1, 108($sp) # internal_179 = result of function_print_at_Main
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# Allocating String
		li $v0, 9
		addi $a0, $zero, 37 # $a0 = length of string + 9 for 4 bytes for the type, 4 bytes for the length of the string and 1 byte for null-terminator
		syscall
		
		la $t0, type_String
		sw $t0, 0($v0) # Setting type in the first word of the object
		
		addi $t0, $zero, 37
		sw $t0, 4($v0) # Setting length of the string in the second word of the object
		
		addi $t0, $zero, 116
		sb $t0, 8($v0) # internal_180[0] = 't'
		
		addi $t0, $zero, 105
		sb $t0, 9($v0) # internal_180[1] = 'i'
		
		addi $t0, $zero, 109
		sb $t0, 10($v0) # internal_180[2] = 'm'
		
		addi $t0, $zero, 101
		sb $t0, 11($v0) # internal_180[3] = 'e'
		
		addi $t0, $zero, 115
		sb $t0, 12($v0) # internal_180[4] = 's'
		
		addi $t0, $zero, 32
		sb $t0, 13($v0) # internal_180[5] = ' '
		
		addi $t0, $zero, 56
		sb $t0, 14($v0) # internal_180[6] = '8'
		
		addi $t0, $zero, 32
		sb $t0, 15($v0) # internal_180[7] = ' '
		
		addi $t0, $zero, 119
		sb $t0, 16($v0) # internal_180[8] = 'w'
		
		addi $t0, $zero, 105
		sb $t0, 17($v0) # internal_180[9] = 'i'
		
		addi $t0, $zero, 116
		sb $t0, 18($v0) # internal_180[10] = 't'
		
		addi $t0, $zero, 104
		sb $t0, 19($v0) # internal_180[11] = 'h'
		
		addi $t0, $zero, 32
		sb $t0, 20($v0) # internal_180[12] = ' '
		
		addi $t0, $zero, 97
		sb $t0, 21($v0) # internal_180[13] = 'a'
		
		addi $t0, $zero, 32
		sb $t0, 22($v0) # internal_180[14] = ' '
		
		addi $t0, $zero, 114
		sb $t0, 23($v0) # internal_180[15] = 'r'
		
		addi $t0, $zero, 101
		sb $t0, 24($v0) # internal_180[16] = 'e'
		
		addi $t0, $zero, 109
		sb $t0, 25($v0) # internal_180[17] = 'm'
		
		addi $t0, $zero, 97
		sb $t0, 26($v0) # internal_180[18] = 'a'
		
		addi $t0, $zero, 105
		sb $t0, 27($v0) # internal_180[19] = 'i'
		
		addi $t0, $zero, 110
		sb $t0, 28($v0) # internal_180[20] = 'n'
		
		addi $t0, $zero, 100
		sb $t0, 29($v0) # internal_180[21] = 'd'
		
		addi $t0, $zero, 101
		sb $t0, 30($v0) # internal_180[22] = 'e'
		
		addi $t0, $zero, 114
		sb $t0, 31($v0) # internal_180[23] = 'r'
		
		addi $t0, $zero, 32
		sb $t0, 32($v0) # internal_180[24] = ' '
		
		addi $t0, $zero, 111
		sb $t0, 33($v0) # internal_180[25] = 'o'
		
		addi $t0, $zero, 102
		sb $t0, 34($v0) # internal_180[26] = 'f'
		
		addi $t0, $zero, 32
		sb $t0, 35($v0) # internal_180[27] = ' '
		
		sb $zero, 36($v0) # Null-terminator at the end of the string
		
		sw $v0, 92($sp) # internal_180 = "times 8 with a remainder of "
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument self
		lw $t0, 828($sp)
		sw $t0, 4($sp) # Storing self
		
		# Argument internal_180
		lw $t0, 104($sp)
		sw $t0, 0($sp) # Storing internal_180
		
		# Calling function function_out_string_at_IO
		jal function_out_string_at_IO
		lw $ra, 8($sp)
		sw $v1, 100($sp) # internal_181 = result of function_out_string_at_IO
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# Allocating A2I
		li $v0, 9
		lw $a0, type_A2I
		syscall
		la $t0, type_A2I # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of th object
		sw $a0, 4($v0) # Setting size in the second word of th object
		sw $v0, 80($sp) # internal_183 = address of allocated object A2I
		
		# Passing function arguments
		addi $sp, $sp, -8 # Reserving space for arguments
		sw $ra, 4($sp) # Storing return address
		
		# Argument internal_183
		lw $t0, 88($sp)
		sw $t0, 0($sp) # Storing internal_183
		
		# Calling function function___init___at_A2I
		jal function___init___at_A2I
		lw $ra, 4($sp)
		sw $v1, 88($sp) # internal_183 = result of function___init___at_A2I
		addi $sp, $sp, 8 # Freeing space for arguments
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument a
		lw $t0, 488($sp)
		sw $t0, 4($sp) # Storing a
		
		# Argument internal_183
		lw $t0, 92($sp)
		sw $t0, 0($sp) # Storing internal_183
		
		# Calling function function_assign
		jal function_assign
		lw $ra, 8($sp)
		sw $v1, 488($sp) # a = result of function_assign
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument a
		lw $t0, 488($sp)
		sw $t0, 4($sp) # Storing a
		
		# Argument r
		lw $t0, 160($sp)
		sw $t0, 0($sp) # Storing r
		
		# Calling function function_i2a_at_A2I
		jal function_i2a_at_A2I
		lw $ra, 8($sp)
		sw $v1, 88($sp) # internal_184 = result of function_i2a_at_A2I
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument self
		lw $t0, 828($sp)
		sw $t0, 4($sp) # Storing self
		
		# Argument internal_184
		lw $t0, 88($sp)
		sw $t0, 0($sp) # Storing internal_184
		
		# Calling function function_out_string_at_IO
		jal function_out_string_at_IO
		lw $ra, 8($sp)
		sw $v1, 84($sp) # internal_185 = result of function_out_string_at_IO
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# Allocating String
		li $v0, 9
		addi $a0, $zero, 10 # $a0 = length of string + 9 for 4 bytes for the type, 4 bytes for the length of the string and 1 byte for null-terminator
		syscall
		
		la $t0, type_String
		sw $t0, 0($v0) # Setting type in the first word of the object
		
		addi $t0, $zero, 10
		sw $t0, 4($v0) # Setting length of the string in the second word of the object
		
		addi $t0, $zero, 10
		sb $t0, 8($v0) # internal_186[0] = '\n'
		
		sb $zero, 9($v0) # Null-terminator at the end of the string
		
		sw $v0, 68($sp) # internal_186 = "\n"
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument self
		lw $t0, 828($sp)
		sw $t0, 4($sp) # Storing self
		
		# Argument internal_186
		lw $t0, 80($sp)
		sw $t0, 0($sp) # Storing internal_186
		
		# Calling function function_out_string_at_IO
		jal function_out_string_at_IO
		lw $ra, 8($sp)
		sw $v1, 76($sp) # internal_187 = result of function_out_string_at_IO
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# Set attribute avar of self
		lw $t0, 816($sp) # $t0 = self
		lw $t1, 168($sp) # $t1 = x
		beq $t1, $zero, object_set_attribute_8781702230420
		lw $t2, 0($t1)
		la $t3, type_Int
		la $t4, type_Bool
		addi $t5, $zero, 1
		seq $t6, $t2, $t3
		beq $t6, $t5, int_set_attribute_8781702230420
		seq $t6, $t2, $t4
		beq $t6, $t5, bool_set_attribute_8781702230420
		j object_set_attribute_8781702230420
		int_set_attribute_8781702230420:
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		sw $t3, 0($v0)
		sw $a0, 4($v0)
		lw $t5, 8($t1)
		sw $t5, 8($v0)
		sw $v0, 12($t0) # self.avar = x
		j end_set_attribute_8781702230420
		bool_set_attribute_8781702230420:
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		sw $t4, 0($v0)
		sw $a0, 4($v0)
		lw $t5, 8($t1)
		sw $t5, 8($v0)
		sw $v0, 12($t0) # self.avar = x
		j end_set_attribute_8781702230420
		object_set_attribute_8781702230420:
		sw $t1, 12($t0) # self.avar = x
		end_set_attribute_8781702230420:
		
		# internal_156 = x
		lw $t0, 168($sp)
		sw $t0, 188($sp)
		
		# Jumping to endif_8781702298167
		j endif_8781702298167
		
		else_8781702298167:
		
		# Allocating Bool 0
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Bool # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 0
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 56($sp) # internal_189 = address of allocated object Int
		
		# Get attribute char of self
		lw $t0, 816($sp) # Get the address of self
		lw $t1, 8($t0) # Get the attribute 'char' from the instance
		lw $t2, 0($t1)
		la $t3, type_Int
		la $t4, type_Bool
		addi $t5, $zero, 1
		seq $t6, $t2, $t3
		beq $t6, $t5, int_get_attribute_8781702231559
		seq $t6, $t2, $t4
		beq $t6, $t5, bool_get_attribute_8781702231559
		j object_get_attribute_8781702231559
		int_get_attribute_8781702231559:
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		sw $t3, 0($v0)
		sw $a0, 4($v0)
		lw $t5, 8($t1)
		sw $t5, 8($v0)
		sw $v0, 52($sp) # internal_190 = self.char
		j end_get_attribute_8781702231559
		bool_get_attribute_8781702231559:
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		sw $t4, 0($v0)
		sw $a0, 4($v0)
		lw $t5, 8($t1)
		sw $t5, 8($v0)
		sw $v0, 52($sp) # internal_190 = self.char
		j end_get_attribute_8781702231559
		object_get_attribute_8781702231559:
		sw $t1, 52($sp) # internal_190 = char
		end_get_attribute_8781702231559:
		
		# Allocating String
		li $v0, 9
		addi $a0, $zero, 10 # $a0 = length of string + 9 for 4 bytes for the type, 4 bytes for the length of the string and 1 byte for null-terminator
		syscall
		
		la $t0, type_String
		sw $t0, 0($v0) # Setting type in the first word of the object
		
		addi $t0, $zero, 10
		sw $t0, 4($v0) # Setting length of the string in the second word of the object
		
		addi $t0, $zero, 106
		sb $t0, 8($v0) # internal_191[0] = 'j'
		
		sb $zero, 9($v0) # Null-terminator at the end of the string
		
		sw $v0, 48($sp) # internal_191 = "j"
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument internal_190
		lw $t0, 64($sp)
		sw $t0, 4($sp) # Storing internal_190
		
		# Argument internal_191
		lw $t0, 60($sp)
		sw $t0, 0($sp) # Storing internal_191
		
		# Calling function function_equal
		jal function_equal
		lw $ra, 8($sp)
		sw $v1, 56($sp) # internal_192 = result of function_equal
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# internal_189 = internal_192
		lw $t0, 44($sp)
		sw $t0, 56($sp)
		
		# If internal_189 then goto then_8781702298161
		lw $t0, 56($sp) # Loading the address of the condition
		lw $t0, 8($t0) # Loading the value of the condition
		addi $t1, $zero, 1 # Setting the value to 1 for comparison
		beq $t0, $t1, then_8781702298161
		
		# Jumping to else_8781702298161
		j else_8781702298161
		
		then_8781702298161:
		
		# Allocating A
		li $v0, 9
		lw $a0, type_A
		syscall
		la $t0, type_A # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of th object
		sw $a0, 4($v0) # Setting size in the second word of th object
		sw $v0, 40($sp) # internal_193 = address of allocated object A
		
		# Passing function arguments
		addi $sp, $sp, -8 # Reserving space for arguments
		sw $ra, 4($sp) # Storing return address
		
		# Argument internal_193
		lw $t0, 48($sp)
		sw $t0, 0($sp) # Storing internal_193
		
		# Calling function function___init___at_A
		jal function___init___at_A
		lw $ra, 4($sp)
		sw $v1, 48($sp) # internal_193 = result of function___init___at_A
		addi $sp, $sp, 8 # Freeing space for arguments
		
		# Set attribute avar of self
		lw $t0, 816($sp) # $t0 = self
		lw $t1, 40($sp) # $t1 = internal_193
		beq $t1, $zero, object_set_attribute_8781702231625
		lw $t2, 0($t1)
		la $t3, type_Int
		la $t4, type_Bool
		addi $t5, $zero, 1
		seq $t6, $t2, $t3
		beq $t6, $t5, int_set_attribute_8781702231625
		seq $t6, $t2, $t4
		beq $t6, $t5, bool_set_attribute_8781702231625
		j object_set_attribute_8781702231625
		int_set_attribute_8781702231625:
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		sw $t3, 0($v0)
		sw $a0, 4($v0)
		lw $t5, 8($t1)
		sw $t5, 8($v0)
		sw $v0, 12($t0) # self.avar = internal_193
		j end_set_attribute_8781702231625
		bool_set_attribute_8781702231625:
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		sw $t4, 0($v0)
		sw $a0, 4($v0)
		lw $t5, 8($t1)
		sw $t5, 8($v0)
		sw $v0, 12($t0) # self.avar = internal_193
		j end_set_attribute_8781702231625
		object_set_attribute_8781702231625:
		sw $t1, 12($t0) # self.avar = internal_193
		end_set_attribute_8781702231625:
		
		# internal_188 = internal_193
		lw $t0, 40($sp)
		sw $t0, 60($sp)
		
		# Jumping to endif_8781702298161
		j endif_8781702298161
		
		else_8781702298161:
		
		# Allocating Bool 0
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Bool # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 0
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 32($sp) # internal_195 = address of allocated object Int
		
		# Get attribute char of self
		lw $t0, 816($sp) # Get the address of self
		lw $t1, 8($t0) # Get the attribute 'char' from the instance
		lw $t2, 0($t1)
		la $t3, type_Int
		la $t4, type_Bool
		addi $t5, $zero, 1
		seq $t6, $t2, $t3
		beq $t6, $t5, int_get_attribute_8781702231727
		seq $t6, $t2, $t4
		beq $t6, $t5, bool_get_attribute_8781702231727
		j object_get_attribute_8781702231727
		int_get_attribute_8781702231727:
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		sw $t3, 0($v0)
		sw $a0, 4($v0)
		lw $t5, 8($t1)
		sw $t5, 8($v0)
		sw $v0, 28($sp) # internal_196 = self.char
		j end_get_attribute_8781702231727
		bool_get_attribute_8781702231727:
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		sw $t4, 0($v0)
		sw $a0, 4($v0)
		lw $t5, 8($t1)
		sw $t5, 8($v0)
		sw $v0, 28($sp) # internal_196 = self.char
		j end_get_attribute_8781702231727
		object_get_attribute_8781702231727:
		sw $t1, 28($sp) # internal_196 = char
		end_get_attribute_8781702231727:
		
		# Allocating String
		li $v0, 9
		addi $a0, $zero, 10 # $a0 = length of string + 9 for 4 bytes for the type, 4 bytes for the length of the string and 1 byte for null-terminator
		syscall
		
		la $t0, type_String
		sw $t0, 0($v0) # Setting type in the first word of the object
		
		addi $t0, $zero, 10
		sw $t0, 4($v0) # Setting length of the string in the second word of the object
		
		addi $t0, $zero, 113
		sb $t0, 8($v0) # internal_197[0] = 'q'
		
		sb $zero, 9($v0) # Null-terminator at the end of the string
		
		sw $v0, 24($sp) # internal_197 = "q"
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument internal_196
		lw $t0, 40($sp)
		sw $t0, 4($sp) # Storing internal_196
		
		# Argument internal_197
		lw $t0, 36($sp)
		sw $t0, 0($sp) # Storing internal_197
		
		# Calling function function_equal
		jal function_equal
		lw $ra, 8($sp)
		sw $v1, 32($sp) # internal_198 = result of function_equal
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# internal_195 = internal_198
		lw $t0, 20($sp)
		sw $t0, 32($sp)
		
		# If internal_195 then goto then_8781702298137
		lw $t0, 32($sp) # Loading the address of the condition
		lw $t0, 8($t0) # Loading the value of the condition
		addi $t1, $zero, 1 # Setting the value to 1 for comparison
		beq $t0, $t1, then_8781702298137
		
		# Jumping to else_8781702298137
		j else_8781702298137
		
		then_8781702298137:
		
		# Allocating Bool 0
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Bool # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 0
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 16($sp) # internal_199 = address of allocated object Int
		
		# Set attribute flag of self
		lw $t0, 816($sp) # $t0 = self
		lw $t1, 16($sp) # $t1 = internal_199
		beq $t1, $zero, object_set_attribute_8781702231793
		lw $t2, 0($t1)
		la $t3, type_Int
		la $t4, type_Bool
		addi $t5, $zero, 1
		seq $t6, $t2, $t3
		beq $t6, $t5, int_set_attribute_8781702231793
		seq $t6, $t2, $t4
		beq $t6, $t5, bool_set_attribute_8781702231793
		j object_set_attribute_8781702231793
		int_set_attribute_8781702231793:
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		sw $t3, 0($v0)
		sw $a0, 4($v0)
		lw $t5, 8($t1)
		sw $t5, 8($v0)
		sw $v0, 20($t0) # self.flag = internal_199
		j end_set_attribute_8781702231793
		bool_set_attribute_8781702231793:
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		sw $t4, 0($v0)
		sw $a0, 4($v0)
		lw $t5, 8($t1)
		sw $t5, 8($v0)
		sw $v0, 20($t0) # self.flag = internal_199
		j end_set_attribute_8781702231793
		object_set_attribute_8781702231793:
		sw $t1, 20($t0) # self.flag = internal_199
		end_set_attribute_8781702231793:
		
		# internal_194 = internal_199
		lw $t0, 16($sp)
		sw $t0, 36($sp)
		
		# Jumping to endif_8781702298137
		j endif_8781702298137
		
		else_8781702298137:
		
		# Allocating A
		li $v0, 9
		lw $a0, type_A
		syscall
		la $t0, type_A # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of th object
		sw $a0, 4($v0) # Setting size in the second word of th object
		sw $v0, 12($sp) # internal_200 = address of allocated object A
		
		# Passing function arguments
		addi $sp, $sp, -8 # Reserving space for arguments
		sw $ra, 4($sp) # Storing return address
		
		# Argument internal_200
		lw $t0, 20($sp)
		sw $t0, 0($sp) # Storing internal_200
		
		# Calling function function___init___at_A
		jal function___init___at_A
		lw $ra, 4($sp)
		sw $v1, 20($sp) # internal_200 = result of function___init___at_A
		addi $sp, $sp, 8 # Freeing space for arguments
		
		# Get attribute avar of self
		lw $t0, 816($sp) # Get the address of self
		lw $t1, 12($t0) # Get the attribute 'avar' from the instance
		lw $t2, 0($t1)
		la $t3, type_Int
		la $t4, type_Bool
		addi $t5, $zero, 1
		seq $t6, $t2, $t3
		beq $t6, $t5, int_get_attribute_8781702232414
		seq $t6, $t2, $t4
		beq $t6, $t5, bool_get_attribute_8781702232414
		j object_get_attribute_8781702232414
		int_get_attribute_8781702232414:
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		sw $t3, 0($v0)
		sw $a0, 4($v0)
		lw $t5, 8($t1)
		sw $t5, 8($v0)
		sw $v0, 8($sp) # internal_201 = self.avar
		j end_get_attribute_8781702232414
		bool_get_attribute_8781702232414:
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		sw $t4, 0($v0)
		sw $a0, 4($v0)
		lw $t5, 8($t1)
		sw $t5, 8($v0)
		sw $v0, 8($sp) # internal_201 = self.avar
		j end_get_attribute_8781702232414
		object_get_attribute_8781702232414:
		sw $t1, 8($sp) # internal_201 = avar
		end_get_attribute_8781702232414:
		
		# Passing function arguments
		addi $sp, $sp, -8 # Reserving space for arguments
		sw $ra, 4($sp) # Storing return address
		
		# Argument internal_201
		lw $t0, 16($sp)
		sw $t0, 0($sp) # Storing internal_201
		
		# Calling function function_value_at_A
		jal function_value_at_A
		lw $ra, 4($sp)
		sw $v1, 12($sp) # internal_202 = result of function_value_at_A
		addi $sp, $sp, 8 # Freeing space for arguments
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument internal_200
		lw $t0, 24($sp)
		sw $t0, 4($sp) # Storing internal_200
		
		# Argument internal_202
		lw $t0, 16($sp)
		sw $t0, 0($sp) # Storing internal_202
		
		# Calling function function_method1_at_A
		jal function_method1_at_A
		lw $ra, 8($sp)
		sw $v1, 12($sp) # internal_203 = result of function_method1_at_A
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# Set attribute avar of self
		lw $t0, 816($sp) # $t0 = self
		lw $t1, 0($sp) # $t1 = internal_203
		beq $t1, $zero, object_set_attribute_8781702232351
		lw $t2, 0($t1)
		la $t3, type_Int
		la $t4, type_Bool
		addi $t5, $zero, 1
		seq $t6, $t2, $t3
		beq $t6, $t5, int_set_attribute_8781702232351
		seq $t6, $t2, $t4
		beq $t6, $t5, bool_set_attribute_8781702232351
		j object_set_attribute_8781702232351
		int_set_attribute_8781702232351:
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		sw $t3, 0($v0)
		sw $a0, 4($v0)
		lw $t5, 8($t1)
		sw $t5, 8($v0)
		sw $v0, 12($t0) # self.avar = internal_203
		j end_set_attribute_8781702232351
		bool_set_attribute_8781702232351:
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		sw $t4, 0($v0)
		sw $a0, 4($v0)
		lw $t5, 8($t1)
		sw $t5, 8($v0)
		sw $v0, 12($t0) # self.avar = internal_203
		j end_set_attribute_8781702232351
		object_set_attribute_8781702232351:
		sw $t1, 12($t0) # self.avar = internal_203
		end_set_attribute_8781702232351:
		
		# internal_194 = internal_203
		lw $t0, 0($sp)
		sw $t0, 36($sp)
		
		# Jumping to endif_8781702298137
		j endif_8781702298137
		
		endif_8781702298137:
		
		# internal_188 = internal_194
		lw $t0, 36($sp)
		sw $t0, 60($sp)
		
		# Jumping to endif_8781702298161
		j endif_8781702298161
		
		endif_8781702298161:
		
		# internal_156 = internal_188
		lw $t0, 60($sp)
		sw $t0, 188($sp)
		
		# Jumping to endif_8781702298167
		j endif_8781702298167
		
		endif_8781702298167:
		
		# internal_133 = internal_156
		lw $t0, 188($sp)
		sw $t0, 280($sp)
		
		# Jumping to endif_8781702298173
		j endif_8781702298173
		
		endif_8781702298173:
		
		# internal_124 = internal_133
		lw $t0, 280($sp)
		sw $t0, 316($sp)
		
		# Jumping to endif_8781702298179
		j endif_8781702298179
		
		endif_8781702298179:
		
		# internal_115 = internal_124
		lw $t0, 316($sp)
		sw $t0, 352($sp)
		
		# Jumping to endif_8781702298185
		j endif_8781702298185
		
		endif_8781702298185:
		
		# internal_106 = internal_115
		lw $t0, 352($sp)
		sw $t0, 388($sp)
		
		# Jumping to endif_8781702298191
		j endif_8781702298191
		
		endif_8781702298191:
		
		# internal_92 = internal_106
		lw $t0, 388($sp)
		sw $t0, 444($sp)
		
		# Jumping to endif_8781702298197
		j endif_8781702298197
		
		endif_8781702298197:
		
		# internal_32 = internal_92
		lw $t0, 444($sp)
		sw $t0, 684($sp)
		
		# Jumping to endif_8781702298203
		j endif_8781702298203
		
		endif_8781702298203:
		
		# internal_18 = internal_32
		lw $t0, 684($sp)
		sw $t0, 740($sp)
		
		# Jumping to endif_8781702298209
		j endif_8781702298209
		
		endif_8781702298209:
		
		# Jumping to while_start_8781702298224
		j while_start_8781702298224
		
		while_end_8781702298224:
		
		# Loading return value in $v1
		addi $v1, $zero, 0
		
		# Freeing space for local variables
		addi $sp, $sp, 816
		
		jr $ra
		
	main:
		# Reserving space for local variables
		addi $sp, $sp, -8
		
		# Allocating Main
		li $v0, 9
		lw $a0, type_Main
		syscall
		la $t0, type_Main # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of th object
		sw $a0, 4($v0) # Setting size in the second word of th object
		sw $v0, 4($sp) # internal_0 = address of allocated object Main
		
		# Passing function arguments
		addi $sp, $sp, -8 # Reserving space for arguments
		sw $ra, 4($sp) # Storing return address
		
		# Argument internal_0
		lw $t0, 12($sp)
		sw $t0, 0($sp) # Storing internal_0
		
		# Calling function function___init___at_Main
		jal function___init___at_Main
		lw $ra, 4($sp)
		sw $v1, 12($sp) # internal_0 = result of function___init___at_Main
		addi $sp, $sp, 8 # Freeing space for arguments
		
		# Passing function arguments
		addi $sp, $sp, -8 # Reserving space for arguments
		sw $ra, 4($sp) # Storing return address
		
		# Argument internal_0
		lw $t0, 12($sp)
		sw $t0, 0($sp) # Storing internal_0
		
		# Calling function function_main_at_Main
		jal function_main_at_Main
		lw $ra, 4($sp)
		sw $v1, 8($sp) # internal_1 = result of function_main_at_Main
		addi $sp, $sp, 8 # Freeing space for arguments
		
		# Exit program
		li $v0, 10
		syscall
		
		