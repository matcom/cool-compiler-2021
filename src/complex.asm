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
	
	type_Main: .word 8
	type_Main_inherits_from: .word type_IO
	type_Main_attributes: .word 0
	type_Main_name_size: .word 4
	type_Main_name: .asciiz "Main"
	type_Main_abort_message: .asciiz "Abort called from class Main\n"
	
	type_Complex: .word 16
	type_Complex_inherits_from: .word type_IO
	type_Complex_attributes: .word 2
	type_Complex_name_size: .word 7
	type_Complex_name: .asciiz "Complex"
	type_Complex_abort_message: .asciiz "Abort called from class Complex\n"
	
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
		
	function___init___at_Main:
		# Function parameters
		#   $ra = 4($sp)
		#   self = 0($sp)
		
		# Loading return value in $v1
		lw $v1, 0($sp)
		
		jr $ra
		
	function_main_at_Main:
		# Function parameters
		#   $ra = 64($sp)
		#   self = 60($sp)
		
		# Reserving space for local variables
		addi $sp, $sp, -60
		
		# Allocating Complex
		li $v0, 9
		lw $a0, type_Complex
		syscall
		la $t0, type_Complex # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of th object
		sw $a0, 4($v0) # Setting size in the second word of th object
		sw $v0, 52($sp) # internal_1 = address of allocated object Complex
		
		# Passing function arguments
		addi $sp, $sp, -8 # Reserving space for arguments
		sw $ra, 4($sp) # Storing return address
		
		# Argument internal_1
		lw $t0, 60($sp)
		sw $t0, 0($sp) # Storing internal_1
		
		# Calling function function___init___at_Complex
		jal function___init___at_Complex
		lw $ra, 4($sp)
		sw $v1, 60($sp) # internal_1 = result of function___init___at_Complex
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
		sw $v0, 48($sp) # internal_2 = address of allocated object Int
		
		# Allocating Int 1
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Int # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 1
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 44($sp) # internal_3 = address of allocated object Int
		
		# Passing function arguments
		addi $sp, $sp, -16 # Reserving space for arguments
		sw $ra, 12($sp) # Storing return address
		
		# Argument internal_1
		lw $t0, 68($sp)
		sw $t0, 8($sp) # Storing internal_1
		
		# Argument internal_2
		lw $t0, 64($sp)
		sw $t0, 4($sp) # Storing internal_2
		
		# Argument internal_3
		lw $t0, 60($sp)
		sw $t0, 0($sp) # Storing internal_3
		
		# Calling function function_init_at_Complex
		jal function_init_at_Complex
		lw $ra, 12($sp)
		sw $v1, 56($sp) # internal_4 = result of function_init_at_Complex
		addi $sp, $sp, 16 # Freeing space for arguments
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument c
		lw $t0, 68($sp)
		sw $t0, 4($sp) # Storing c
		
		# Argument internal_4
		lw $t0, 52($sp)
		sw $t0, 0($sp) # Storing internal_4
		
		# Calling function function_assign
		jal function_assign
		lw $ra, 8($sp)
		sw $v1, 68($sp) # c = result of function_assign
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
		sw $v0, 32($sp) # internal_6 = address of allocated object Int
		
		# Passing function arguments
		addi $sp, $sp, -8 # Reserving space for arguments
		sw $ra, 4($sp) # Storing return address
		
		# Argument c
		lw $t0, 64($sp)
		sw $t0, 0($sp) # Storing c
		
		# Calling function function_reflect_X_at_Complex
		jal function_reflect_X_at_Complex
		lw $ra, 4($sp)
		sw $v1, 36($sp) # internal_7 = result of function_reflect_X_at_Complex
		addi $sp, $sp, 8 # Freeing space for arguments
		
		# Passing function arguments
		addi $sp, $sp, -8 # Reserving space for arguments
		sw $ra, 4($sp) # Storing return address
		
		# Argument internal_7
		lw $t0, 36($sp)
		sw $t0, 0($sp) # Storing internal_7
		
		# Calling function function_reflect_Y_at_Complex
		jal function_reflect_Y_at_Complex
		lw $ra, 4($sp)
		sw $v1, 32($sp) # internal_8 = result of function_reflect_Y_at_Complex
		addi $sp, $sp, 8 # Freeing space for arguments
		
		# Passing function arguments
		addi $sp, $sp, -8 # Reserving space for arguments
		sw $ra, 4($sp) # Storing return address
		
		# Argument c
		lw $t0, 64($sp)
		sw $t0, 0($sp) # Storing c
		
		# Calling function function_reflect_0_at_Complex
		jal function_reflect_0_at_Complex
		lw $ra, 4($sp)
		sw $v1, 28($sp) # internal_9 = result of function_reflect_0_at_Complex
		addi $sp, $sp, 8 # Freeing space for arguments
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument internal_8
		lw $t0, 36($sp)
		sw $t0, 4($sp) # Storing internal_8
		
		# Argument internal_9
		lw $t0, 32($sp)
		sw $t0, 0($sp) # Storing internal_9
		
		# Calling function function_equal
		jal function_equal
		lw $ra, 8($sp)
		sw $v1, 28($sp) # internal_10 = result of function_equal
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# internal_6 = internal_10
		lw $t0, 16($sp)
		sw $t0, 32($sp)
		
		# If internal_6 then goto then_8741814694660
		lw $t0, 32($sp) # Loading the address of the condition
		lw $t0, 8($t0) # Loading the value of the condition
		addi $t1, $zero, 1 # Setting the value to 1 for comparison
		beq $t0, $t1, then_8741814694660
		
		# Jumping to else_8741814694660
		j else_8741814694660
		
		then_8741814694660:
		
		# Allocating String
		li $v0, 9
		addi $a0, $zero, 12 # $a0 = length of string + 9 for 4 bytes for the type, 4 bytes for the length of the string and 1 byte for null-terminator
		syscall
		
		la $t0, type_String
		sw $t0, 0($v0) # Setting type in the first word of the object
		
		addi $t0, $zero, 12
		sw $t0, 4($v0) # Setting length of the string in the second word of the object
		
		addi $t0, $zero, 61
		sb $t0, 8($v0) # internal_11[0] = '='
		
		addi $t0, $zero, 41
		sb $t0, 9($v0) # internal_11[1] = ')'
		
		addi $t0, $zero, 10
		sb $t0, 10($v0) # internal_11[2] = '\n'
		
		sb $zero, 11($v0) # Null-terminator at the end of the string
		
		sw $v0, 12($sp) # internal_11 = "=)\n"
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument self
		lw $t0, 72($sp)
		sw $t0, 4($sp) # Storing self
		
		# Argument internal_11
		lw $t0, 24($sp)
		sw $t0, 0($sp) # Storing internal_11
		
		# Calling function function_out_string_at_IO
		jal function_out_string_at_IO
		lw $ra, 8($sp)
		sw $v1, 20($sp) # internal_12 = result of function_out_string_at_IO
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# internal_5 = internal_12
		lw $t0, 8($sp)
		sw $t0, 36($sp)
		
		# Jumping to endif_8741814694660
		j endif_8741814694660
		
		else_8741814694660:
		
		# Allocating String
		li $v0, 9
		addi $a0, $zero, 12 # $a0 = length of string + 9 for 4 bytes for the type, 4 bytes for the length of the string and 1 byte for null-terminator
		syscall
		
		la $t0, type_String
		sw $t0, 0($v0) # Setting type in the first word of the object
		
		addi $t0, $zero, 12
		sw $t0, 4($v0) # Setting length of the string in the second word of the object
		
		addi $t0, $zero, 61
		sb $t0, 8($v0) # internal_13[0] = '='
		
		addi $t0, $zero, 40
		sb $t0, 9($v0) # internal_13[1] = '('
		
		addi $t0, $zero, 10
		sb $t0, 10($v0) # internal_13[2] = '\n'
		
		sb $zero, 11($v0) # Null-terminator at the end of the string
		
		sw $v0, 4($sp) # internal_13 = "=(\n"
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument self
		lw $t0, 72($sp)
		sw $t0, 4($sp) # Storing self
		
		# Argument internal_13
		lw $t0, 16($sp)
		sw $t0, 0($sp) # Storing internal_13
		
		# Calling function function_out_string_at_IO
		jal function_out_string_at_IO
		lw $ra, 8($sp)
		sw $v1, 12($sp) # internal_14 = result of function_out_string_at_IO
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# internal_5 = internal_14
		lw $t0, 0($sp)
		sw $t0, 36($sp)
		
		# Jumping to endif_8741814694660
		j endif_8741814694660
		
		endif_8741814694660:
		
		# Loading return value in $v1
		lw $v1, 36($sp)
		
		# Freeing space for local variables
		addi $sp, $sp, 60
		
		jr $ra
		
	function___init___at_Complex:
		# Function parameters
		#   $ra = 12($sp)
		#   self = 8($sp)
		
		# Reserving space for local variables
		addi $sp, $sp, -8
		
		# Allocating Int 0
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Int # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 0
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 4($sp) # internal_0 = address of allocated object Int
		
		# Set attribute x of self
		lw $t0, 8($sp) # $t0 = self
		lw $t1, 4($sp) # $t1 = internal_0
		beq $t1, $zero, object_set_attribute_8741814676447
		lw $t2, 0($t1)
		la $t3, type_Int
		la $t4, type_Bool
		addi $t5, $zero, 1
		seq $t6, $t2, $t3
		beq $t6, $t5, int_set_attribute_8741814676447
		seq $t6, $t2, $t4
		beq $t6, $t5, bool_set_attribute_8741814676447
		j object_set_attribute_8741814676447
		int_set_attribute_8741814676447:
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		sw $t3, 0($v0)
		sw $a0, 4($v0)
		lw $t5, 8($t1)
		sw $t5, 8($v0)
		sw $v0, 8($t0) # self.x = internal_0
		j end_set_attribute_8741814676447
		bool_set_attribute_8741814676447:
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		sw $t4, 0($v0)
		sw $a0, 4($v0)
		lw $t5, 8($t1)
		sw $t5, 8($v0)
		sw $v0, 8($t0) # self.x = internal_0
		j end_set_attribute_8741814676447
		object_set_attribute_8741814676447:
		sw $t1, 8($t0) # self.x = internal_0
		end_set_attribute_8741814676447:
		
		# Allocating Int 0
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Int # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 0
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 0($sp) # internal_1 = address of allocated object Int
		
		# Set attribute y of self
		lw $t0, 8($sp) # $t0 = self
		lw $t1, 0($sp) # $t1 = internal_1
		beq $t1, $zero, object_set_attribute_8741814676468
		lw $t2, 0($t1)
		la $t3, type_Int
		la $t4, type_Bool
		addi $t5, $zero, 1
		seq $t6, $t2, $t3
		beq $t6, $t5, int_set_attribute_8741814676468
		seq $t6, $t2, $t4
		beq $t6, $t5, bool_set_attribute_8741814676468
		j object_set_attribute_8741814676468
		int_set_attribute_8741814676468:
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		sw $t3, 0($v0)
		sw $a0, 4($v0)
		lw $t5, 8($t1)
		sw $t5, 8($v0)
		sw $v0, 12($t0) # self.y = internal_1
		j end_set_attribute_8741814676468
		bool_set_attribute_8741814676468:
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		sw $t4, 0($v0)
		sw $a0, 4($v0)
		lw $t5, 8($t1)
		sw $t5, 8($v0)
		sw $v0, 12($t0) # self.y = internal_1
		j end_set_attribute_8741814676468
		object_set_attribute_8741814676468:
		sw $t1, 12($t0) # self.y = internal_1
		end_set_attribute_8741814676468:
		
		# Loading return value in $v1
		lw $v1, 8($sp)
		
		# Freeing space for local variables
		addi $sp, $sp, 8
		
		jr $ra
		
	function_init_at_Complex:
		# Function parameters
		#   $ra = 28($sp)
		#   self = 24($sp)
		#   a = 20($sp)
		#   b = 16($sp)
		
		# Reserving space for local variables
		addi $sp, $sp, -16
		
		# Get attribute x of self
		lw $t0, 24($sp) # Get the address of self
		lw $t1, 8($t0) # Get the attribute 'x' from the instance
		lw $t2, 0($t1)
		la $t3, type_Int
		la $t4, type_Bool
		addi $t5, $zero, 1
		seq $t6, $t2, $t3
		beq $t6, $t5, int_get_attribute_8741814677815
		seq $t6, $t2, $t4
		beq $t6, $t5, bool_get_attribute_8741814677815
		j object_get_attribute_8741814677815
		int_get_attribute_8741814677815:
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		sw $t3, 0($v0)
		sw $a0, 4($v0)
		lw $t5, 8($t1)
		sw $t5, 8($v0)
		sw $v0, 12($sp) # internal_0 = self.x
		j end_get_attribute_8741814677815
		bool_get_attribute_8741814677815:
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		sw $t4, 0($v0)
		sw $a0, 4($v0)
		lw $t5, 8($t1)
		sw $t5, 8($v0)
		sw $v0, 12($sp) # internal_0 = self.x
		j end_get_attribute_8741814677815
		object_get_attribute_8741814677815:
		sw $t1, 12($sp) # internal_0 = x
		end_get_attribute_8741814677815:
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument internal_0
		lw $t0, 24($sp)
		sw $t0, 4($sp) # Storing internal_0
		
		# Argument a
		lw $t0, 32($sp)
		sw $t0, 0($sp) # Storing a
		
		# Calling function function_equal
		jal function_equal
		lw $ra, 8($sp)
		sw $v1, 20($sp) # internal_1 = result of function_equal
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# Get attribute y of self
		lw $t0, 24($sp) # Get the address of self
		lw $t1, 12($t0) # Get the attribute 'y' from the instance
		lw $t2, 0($t1)
		la $t3, type_Int
		la $t4, type_Bool
		addi $t5, $zero, 1
		seq $t6, $t2, $t3
		beq $t6, $t5, int_get_attribute_8741814677854
		seq $t6, $t2, $t4
		beq $t6, $t5, bool_get_attribute_8741814677854
		j object_get_attribute_8741814677854
		int_get_attribute_8741814677854:
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		sw $t3, 0($v0)
		sw $a0, 4($v0)
		lw $t5, 8($t1)
		sw $t5, 8($v0)
		sw $v0, 4($sp) # internal_2 = self.y
		j end_get_attribute_8741814677854
		bool_get_attribute_8741814677854:
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		sw $t4, 0($v0)
		sw $a0, 4($v0)
		lw $t5, 8($t1)
		sw $t5, 8($v0)
		sw $v0, 4($sp) # internal_2 = self.y
		j end_get_attribute_8741814677854
		object_get_attribute_8741814677854:
		sw $t1, 4($sp) # internal_2 = y
		end_get_attribute_8741814677854:
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument internal_2
		lw $t0, 16($sp)
		sw $t0, 4($sp) # Storing internal_2
		
		# Argument b
		lw $t0, 28($sp)
		sw $t0, 0($sp) # Storing b
		
		# Calling function function_equal
		jal function_equal
		lw $ra, 8($sp)
		sw $v1, 12($sp) # internal_3 = result of function_equal
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# Loading return value in $v1
		lw $v1, 24($sp)
		
		# Freeing space for local variables
		addi $sp, $sp, 16
		
		jr $ra
		
	function_print_at_Complex:
		# Function parameters
		#   $ra = 64($sp)
		#   self = 60($sp)
		
		# Reserving space for local variables
		addi $sp, $sp, -60
		
		# Allocating Bool 0
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Bool # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 0
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 52($sp) # internal_1 = address of allocated object Int
		
		# Get attribute y of self
		lw $t0, 60($sp) # Get the address of self
		lw $t1, 12($t0) # Get the attribute 'y' from the instance
		lw $t2, 0($t1)
		la $t3, type_Int
		la $t4, type_Bool
		addi $t5, $zero, 1
		seq $t6, $t2, $t3
		beq $t6, $t5, int_get_attribute_8741814677932
		seq $t6, $t2, $t4
		beq $t6, $t5, bool_get_attribute_8741814677932
		j object_get_attribute_8741814677932
		int_get_attribute_8741814677932:
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		sw $t3, 0($v0)
		sw $a0, 4($v0)
		lw $t5, 8($t1)
		sw $t5, 8($v0)
		sw $v0, 48($sp) # internal_2 = self.y
		j end_get_attribute_8741814677932
		bool_get_attribute_8741814677932:
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		sw $t4, 0($v0)
		sw $a0, 4($v0)
		lw $t5, 8($t1)
		sw $t5, 8($v0)
		sw $v0, 48($sp) # internal_2 = self.y
		j end_get_attribute_8741814677932
		object_get_attribute_8741814677932:
		sw $t1, 48($sp) # internal_2 = y
		end_get_attribute_8741814677932:
		
		# Allocating Int 0
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Int # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 0
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 44($sp) # internal_3 = address of allocated object Int
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument internal_2
		lw $t0, 60($sp)
		sw $t0, 4($sp) # Storing internal_2
		
		# Argument internal_3
		lw $t0, 56($sp)
		sw $t0, 0($sp) # Storing internal_3
		
		# Calling function function_equal
		jal function_equal
		lw $ra, 8($sp)
		sw $v1, 52($sp) # internal_4 = result of function_equal
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# internal_1 = internal_4
		lw $t0, 40($sp)
		sw $t0, 52($sp)
		
		# If internal_1 then goto then_8741814694807
		lw $t0, 52($sp) # Loading the address of the condition
		lw $t0, 8($t0) # Loading the value of the condition
		addi $t1, $zero, 1 # Setting the value to 1 for comparison
		beq $t0, $t1, then_8741814694807
		
		# Jumping to else_8741814694807
		j else_8741814694807
		
		then_8741814694807:
		
		# Get attribute x of self
		lw $t0, 60($sp) # Get the address of self
		lw $t1, 8($t0) # Get the attribute 'x' from the instance
		lw $t2, 0($t1)
		la $t3, type_Int
		la $t4, type_Bool
		addi $t5, $zero, 1
		seq $t6, $t2, $t3
		beq $t6, $t5, int_get_attribute_8741814678013
		seq $t6, $t2, $t4
		beq $t6, $t5, bool_get_attribute_8741814678013
		j object_get_attribute_8741814678013
		int_get_attribute_8741814678013:
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		sw $t3, 0($v0)
		sw $a0, 4($v0)
		lw $t5, 8($t1)
		sw $t5, 8($v0)
		sw $v0, 36($sp) # internal_5 = self.x
		j end_get_attribute_8741814678013
		bool_get_attribute_8741814678013:
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		sw $t4, 0($v0)
		sw $a0, 4($v0)
		lw $t5, 8($t1)
		sw $t5, 8($v0)
		sw $v0, 36($sp) # internal_5 = self.x
		j end_get_attribute_8741814678013
		object_get_attribute_8741814678013:
		sw $t1, 36($sp) # internal_5 = x
		end_get_attribute_8741814678013:
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument self
		lw $t0, 72($sp)
		sw $t0, 4($sp) # Storing self
		
		# Argument internal_5
		lw $t0, 48($sp)
		sw $t0, 0($sp) # Storing internal_5
		
		# Calling function function_out_int_at_IO
		jal function_out_int_at_IO
		lw $ra, 8($sp)
		sw $v1, 44($sp) # internal_6 = result of function_out_int_at_IO
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# internal_0 = internal_6
		lw $t0, 32($sp)
		sw $t0, 56($sp)
		
		# Jumping to endif_8741814694807
		j endif_8741814694807
		
		else_8741814694807:
		
		# Get attribute x of self
		lw $t0, 60($sp) # Get the address of self
		lw $t1, 8($t0) # Get the attribute 'x' from the instance
		lw $t2, 0($t1)
		la $t3, type_Int
		la $t4, type_Bool
		addi $t5, $zero, 1
		seq $t6, $t2, $t3
		beq $t6, $t5, int_get_attribute_8741814676574
		seq $t6, $t2, $t4
		beq $t6, $t5, bool_get_attribute_8741814676574
		j object_get_attribute_8741814676574
		int_get_attribute_8741814676574:
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		sw $t3, 0($v0)
		sw $a0, 4($v0)
		lw $t5, 8($t1)
		sw $t5, 8($v0)
		sw $v0, 28($sp) # internal_7 = self.x
		j end_get_attribute_8741814676574
		bool_get_attribute_8741814676574:
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		sw $t4, 0($v0)
		sw $a0, 4($v0)
		lw $t5, 8($t1)
		sw $t5, 8($v0)
		sw $v0, 28($sp) # internal_7 = self.x
		j end_get_attribute_8741814676574
		object_get_attribute_8741814676574:
		sw $t1, 28($sp) # internal_7 = x
		end_get_attribute_8741814676574:
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument self
		lw $t0, 72($sp)
		sw $t0, 4($sp) # Storing self
		
		# Argument internal_7
		lw $t0, 40($sp)
		sw $t0, 0($sp) # Storing internal_7
		
		# Calling function function_out_int_at_IO
		jal function_out_int_at_IO
		lw $ra, 8($sp)
		sw $v1, 36($sp) # internal_8 = result of function_out_int_at_IO
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# Allocating String
		li $v0, 9
		addi $a0, $zero, 10 # $a0 = length of string + 9 for 4 bytes for the type, 4 bytes for the length of the string and 1 byte for null-terminator
		syscall
		
		la $t0, type_String
		sw $t0, 0($v0) # Setting type in the first word of the object
		
		addi $t0, $zero, 10
		sw $t0, 4($v0) # Setting length of the string in the second word of the object
		
		addi $t0, $zero, 43
		sb $t0, 8($v0) # internal_9[0] = '+'
		
		sb $zero, 9($v0) # Null-terminator at the end of the string
		
		sw $v0, 20($sp) # internal_9 = "+"
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument internal_8
		lw $t0, 36($sp)
		sw $t0, 4($sp) # Storing internal_8
		
		# Argument internal_9
		lw $t0, 32($sp)
		sw $t0, 0($sp) # Storing internal_9
		
		# Calling function function_out_string_at_IO
		jal function_out_string_at_IO
		lw $ra, 8($sp)
		sw $v1, 28($sp) # internal_10 = result of function_out_string_at_IO
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# Get attribute y of self
		lw $t0, 60($sp) # Get the address of self
		lw $t1, 12($t0) # Get the attribute 'y' from the instance
		lw $t2, 0($t1)
		la $t3, type_Int
		la $t4, type_Bool
		addi $t5, $zero, 1
		seq $t6, $t2, $t3
		beq $t6, $t5, int_get_attribute_8741814676622
		seq $t6, $t2, $t4
		beq $t6, $t5, bool_get_attribute_8741814676622
		j object_get_attribute_8741814676622
		int_get_attribute_8741814676622:
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		sw $t3, 0($v0)
		sw $a0, 4($v0)
		lw $t5, 8($t1)
		sw $t5, 8($v0)
		sw $v0, 12($sp) # internal_11 = self.y
		j end_get_attribute_8741814676622
		bool_get_attribute_8741814676622:
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		sw $t4, 0($v0)
		sw $a0, 4($v0)
		lw $t5, 8($t1)
		sw $t5, 8($v0)
		sw $v0, 12($sp) # internal_11 = self.y
		j end_get_attribute_8741814676622
		object_get_attribute_8741814676622:
		sw $t1, 12($sp) # internal_11 = y
		end_get_attribute_8741814676622:
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument internal_10
		lw $t0, 28($sp)
		sw $t0, 4($sp) # Storing internal_10
		
		# Argument internal_11
		lw $t0, 24($sp)
		sw $t0, 0($sp) # Storing internal_11
		
		# Calling function function_out_int_at_IO
		jal function_out_int_at_IO
		lw $ra, 8($sp)
		sw $v1, 20($sp) # internal_12 = result of function_out_int_at_IO
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# Allocating String
		li $v0, 9
		addi $a0, $zero, 10 # $a0 = length of string + 9 for 4 bytes for the type, 4 bytes for the length of the string and 1 byte for null-terminator
		syscall
		
		la $t0, type_String
		sw $t0, 0($v0) # Setting type in the first word of the object
		
		addi $t0, $zero, 10
		sw $t0, 4($v0) # Setting length of the string in the second word of the object
		
		addi $t0, $zero, 73
		sb $t0, 8($v0) # internal_13[0] = 'I'
		
		sb $zero, 9($v0) # Null-terminator at the end of the string
		
		sw $v0, 4($sp) # internal_13 = "I"
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument internal_12
		lw $t0, 20($sp)
		sw $t0, 4($sp) # Storing internal_12
		
		# Argument internal_13
		lw $t0, 16($sp)
		sw $t0, 0($sp) # Storing internal_13
		
		# Calling function function_out_string_at_IO
		jal function_out_string_at_IO
		lw $ra, 8($sp)
		sw $v1, 12($sp) # internal_14 = result of function_out_string_at_IO
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# internal_0 = internal_14
		lw $t0, 0($sp)
		sw $t0, 56($sp)
		
		# Jumping to endif_8741814694807
		j endif_8741814694807
		
		endif_8741814694807:
		
		# Loading return value in $v1
		lw $v1, 56($sp)
		
		# Freeing space for local variables
		addi $sp, $sp, 60
		
		jr $ra
		
	function_reflect_0_at_Complex:
		# Function parameters
		#   $ra = 52($sp)
		#   self = 48($sp)
		
		# Reserving space for local variables
		addi $sp, $sp, -48
		
		# Get attribute x of self
		lw $t0, 48($sp) # Get the address of self
		lw $t1, 8($t0) # Get the attribute 'x' from the instance
		lw $t2, 0($t1)
		la $t3, type_Int
		la $t4, type_Bool
		addi $t5, $zero, 1
		seq $t6, $t2, $t3
		beq $t6, $t5, int_get_attribute_8741814676721
		seq $t6, $t2, $t4
		beq $t6, $t5, bool_get_attribute_8741814676721
		j object_get_attribute_8741814676721
		int_get_attribute_8741814676721:
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		sw $t3, 0($v0)
		sw $a0, 4($v0)
		lw $t5, 8($t1)
		sw $t5, 8($v0)
		sw $v0, 44($sp) # internal_0 = self.x
		j end_get_attribute_8741814676721
		bool_get_attribute_8741814676721:
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		sw $t4, 0($v0)
		sw $a0, 4($v0)
		lw $t5, 8($t1)
		sw $t5, 8($v0)
		sw $v0, 44($sp) # internal_0 = self.x
		j end_get_attribute_8741814676721
		object_get_attribute_8741814676721:
		sw $t1, 44($sp) # internal_0 = x
		end_get_attribute_8741814676721:
		
		# Get attribute x of self
		lw $t0, 48($sp) # Get the address of self
		lw $t1, 8($t0) # Get the attribute 'x' from the instance
		lw $t2, 0($t1)
		la $t3, type_Int
		la $t4, type_Bool
		addi $t5, $zero, 1
		seq $t6, $t2, $t3
		beq $t6, $t5, int_get_attribute_8741814678541
		seq $t6, $t2, $t4
		beq $t6, $t5, bool_get_attribute_8741814678541
		j object_get_attribute_8741814678541
		int_get_attribute_8741814678541:
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		sw $t3, 0($v0)
		sw $a0, 4($v0)
		lw $t5, 8($t1)
		sw $t5, 8($v0)
		sw $v0, 40($sp) # internal_1 = self.x
		j end_get_attribute_8741814678541
		bool_get_attribute_8741814678541:
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		sw $t4, 0($v0)
		sw $a0, 4($v0)
		lw $t5, 8($t1)
		sw $t5, 8($v0)
		sw $v0, 40($sp) # internal_1 = self.x
		j end_get_attribute_8741814678541
		object_get_attribute_8741814678541:
		sw $t1, 40($sp) # internal_1 = x
		end_get_attribute_8741814678541:
		
		# Allocating Int 1
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Int # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 1
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 36($sp) # internal_2 = address of allocated object Int
		
		# Allocating Int 4294967295
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Int # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 4294967295
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 32($sp) # internal_3 = address of allocated object Int
		
		# Allocating Int 0
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Int # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 0
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 28($sp) # internal_4 = address of allocated object Int
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument internal_1
		lw $t0, 52($sp)
		sw $t0, 4($sp) # Storing internal_1
		
		# Argument internal_3
		lw $t0, 44($sp)
		sw $t0, 0($sp) # Storing internal_3
		
		# Calling function function_xor
		jal function_xor
		lw $ra, 8($sp)
		sw $v1, 40($sp) # internal_4 = result of function_xor
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument internal_4
		lw $t0, 40($sp)
		sw $t0, 4($sp) # Storing internal_4
		
		# Argument internal_2
		lw $t0, 48($sp)
		sw $t0, 0($sp) # Storing internal_2
		
		# Calling function function_add
		jal function_add
		lw $ra, 8($sp)
		sw $v1, 40($sp) # internal_4 = result of function_add
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument internal_0
		lw $t0, 56($sp)
		sw $t0, 4($sp) # Storing internal_0
		
		# Argument internal_4
		lw $t0, 40($sp)
		sw $t0, 0($sp) # Storing internal_4
		
		# Calling function function_equal
		jal function_equal
		lw $ra, 8($sp)
		sw $v1, 36($sp) # internal_5 = result of function_equal
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# Get attribute y of self
		lw $t0, 48($sp) # Get the address of self
		lw $t1, 12($t0) # Get the attribute 'y' from the instance
		lw $t2, 0($t1)
		la $t3, type_Int
		la $t4, type_Bool
		addi $t5, $zero, 1
		seq $t6, $t2, $t3
		beq $t6, $t5, int_get_attribute_8741814678640
		seq $t6, $t2, $t4
		beq $t6, $t5, bool_get_attribute_8741814678640
		j object_get_attribute_8741814678640
		int_get_attribute_8741814678640:
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		sw $t3, 0($v0)
		sw $a0, 4($v0)
		lw $t5, 8($t1)
		sw $t5, 8($v0)
		sw $v0, 20($sp) # internal_6 = self.y
		j end_get_attribute_8741814678640
		bool_get_attribute_8741814678640:
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		sw $t4, 0($v0)
		sw $a0, 4($v0)
		lw $t5, 8($t1)
		sw $t5, 8($v0)
		sw $v0, 20($sp) # internal_6 = self.y
		j end_get_attribute_8741814678640
		object_get_attribute_8741814678640:
		sw $t1, 20($sp) # internal_6 = y
		end_get_attribute_8741814678640:
		
		# Get attribute y of self
		lw $t0, 48($sp) # Get the address of self
		lw $t1, 12($t0) # Get the attribute 'y' from the instance
		lw $t2, 0($t1)
		la $t3, type_Int
		la $t4, type_Bool
		addi $t5, $zero, 1
		seq $t6, $t2, $t3
		beq $t6, $t5, int_get_attribute_8741814678664
		seq $t6, $t2, $t4
		beq $t6, $t5, bool_get_attribute_8741814678664
		j object_get_attribute_8741814678664
		int_get_attribute_8741814678664:
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		sw $t3, 0($v0)
		sw $a0, 4($v0)
		lw $t5, 8($t1)
		sw $t5, 8($v0)
		sw $v0, 16($sp) # internal_7 = self.y
		j end_get_attribute_8741814678664
		bool_get_attribute_8741814678664:
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		sw $t4, 0($v0)
		sw $a0, 4($v0)
		lw $t5, 8($t1)
		sw $t5, 8($v0)
		sw $v0, 16($sp) # internal_7 = self.y
		j end_get_attribute_8741814678664
		object_get_attribute_8741814678664:
		sw $t1, 16($sp) # internal_7 = y
		end_get_attribute_8741814678664:
		
		# Allocating Int 1
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Int # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 1
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 12($sp) # internal_8 = address of allocated object Int
		
		# Allocating Int 4294967295
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Int # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 4294967295
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 8($sp) # internal_9 = address of allocated object Int
		
		# Allocating Int 0
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Int # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 0
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 4($sp) # internal_10 = address of allocated object Int
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument internal_7
		lw $t0, 28($sp)
		sw $t0, 4($sp) # Storing internal_7
		
		# Argument internal_9
		lw $t0, 20($sp)
		sw $t0, 0($sp) # Storing internal_9
		
		# Calling function function_xor
		jal function_xor
		lw $ra, 8($sp)
		sw $v1, 16($sp) # internal_10 = result of function_xor
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument internal_10
		lw $t0, 16($sp)
		sw $t0, 4($sp) # Storing internal_10
		
		# Argument internal_8
		lw $t0, 24($sp)
		sw $t0, 0($sp) # Storing internal_8
		
		# Calling function function_add
		jal function_add
		lw $ra, 8($sp)
		sw $v1, 16($sp) # internal_10 = result of function_add
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument internal_6
		lw $t0, 32($sp)
		sw $t0, 4($sp) # Storing internal_6
		
		# Argument internal_10
		lw $t0, 16($sp)
		sw $t0, 0($sp) # Storing internal_10
		
		# Calling function function_equal
		jal function_equal
		lw $ra, 8($sp)
		sw $v1, 12($sp) # internal_11 = result of function_equal
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# Loading return value in $v1
		lw $v1, 48($sp)
		
		# Freeing space for local variables
		addi $sp, $sp, 48
		
		jr $ra
		
	function_reflect_X_at_Complex:
		# Function parameters
		#   $ra = 28($sp)
		#   self = 24($sp)
		
		# Reserving space for local variables
		addi $sp, $sp, -24
		
		# Get attribute y of self
		lw $t0, 24($sp) # Get the address of self
		lw $t1, 12($t0) # Get the attribute 'y' from the instance
		lw $t2, 0($t1)
		la $t3, type_Int
		la $t4, type_Bool
		addi $t5, $zero, 1
		seq $t6, $t2, $t3
		beq $t6, $t5, int_get_attribute_8741814678781
		seq $t6, $t2, $t4
		beq $t6, $t5, bool_get_attribute_8741814678781
		j object_get_attribute_8741814678781
		int_get_attribute_8741814678781:
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		sw $t3, 0($v0)
		sw $a0, 4($v0)
		lw $t5, 8($t1)
		sw $t5, 8($v0)
		sw $v0, 20($sp) # internal_0 = self.y
		j end_get_attribute_8741814678781
		bool_get_attribute_8741814678781:
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		sw $t4, 0($v0)
		sw $a0, 4($v0)
		lw $t5, 8($t1)
		sw $t5, 8($v0)
		sw $v0, 20($sp) # internal_0 = self.y
		j end_get_attribute_8741814678781
		object_get_attribute_8741814678781:
		sw $t1, 20($sp) # internal_0 = y
		end_get_attribute_8741814678781:
		
		# Get attribute y of self
		lw $t0, 24($sp) # Get the address of self
		lw $t1, 12($t0) # Get the attribute 'y' from the instance
		lw $t2, 0($t1)
		la $t3, type_Int
		la $t4, type_Bool
		addi $t5, $zero, 1
		seq $t6, $t2, $t3
		beq $t6, $t5, int_get_attribute_8741814679321
		seq $t6, $t2, $t4
		beq $t6, $t5, bool_get_attribute_8741814679321
		j object_get_attribute_8741814679321
		int_get_attribute_8741814679321:
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		sw $t3, 0($v0)
		sw $a0, 4($v0)
		lw $t5, 8($t1)
		sw $t5, 8($v0)
		sw $v0, 16($sp) # internal_1 = self.y
		j end_get_attribute_8741814679321
		bool_get_attribute_8741814679321:
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		sw $t4, 0($v0)
		sw $a0, 4($v0)
		lw $t5, 8($t1)
		sw $t5, 8($v0)
		sw $v0, 16($sp) # internal_1 = self.y
		j end_get_attribute_8741814679321
		object_get_attribute_8741814679321:
		sw $t1, 16($sp) # internal_1 = y
		end_get_attribute_8741814679321:
		
		# Allocating Int 1
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Int # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 1
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 12($sp) # internal_2 = address of allocated object Int
		
		# Allocating Int 4294967295
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Int # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 4294967295
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 8($sp) # internal_3 = address of allocated object Int
		
		# Allocating Int 0
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Int # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 0
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 4($sp) # internal_4 = address of allocated object Int
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument internal_1
		lw $t0, 28($sp)
		sw $t0, 4($sp) # Storing internal_1
		
		# Argument internal_3
		lw $t0, 20($sp)
		sw $t0, 0($sp) # Storing internal_3
		
		# Calling function function_xor
		jal function_xor
		lw $ra, 8($sp)
		sw $v1, 16($sp) # internal_4 = result of function_xor
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument internal_4
		lw $t0, 16($sp)
		sw $t0, 4($sp) # Storing internal_4
		
		# Argument internal_2
		lw $t0, 24($sp)
		sw $t0, 0($sp) # Storing internal_2
		
		# Calling function function_add
		jal function_add
		lw $ra, 8($sp)
		sw $v1, 16($sp) # internal_4 = result of function_add
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument internal_0
		lw $t0, 32($sp)
		sw $t0, 4($sp) # Storing internal_0
		
		# Argument internal_4
		lw $t0, 16($sp)
		sw $t0, 0($sp) # Storing internal_4
		
		# Calling function function_equal
		jal function_equal
		lw $ra, 8($sp)
		sw $v1, 12($sp) # internal_5 = result of function_equal
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# Loading return value in $v1
		lw $v1, 24($sp)
		
		# Freeing space for local variables
		addi $sp, $sp, 24
		
		jr $ra
		
	function_reflect_Y_at_Complex:
		# Function parameters
		#   $ra = 28($sp)
		#   self = 24($sp)
		
		# Reserving space for local variables
		addi $sp, $sp, -24
		
		# Get attribute x of self
		lw $t0, 24($sp) # Get the address of self
		lw $t1, 8($t0) # Get the attribute 'x' from the instance
		lw $t2, 0($t1)
		la $t3, type_Int
		la $t4, type_Bool
		addi $t5, $zero, 1
		seq $t6, $t2, $t3
		beq $t6, $t5, int_get_attribute_8741814679438
		seq $t6, $t2, $t4
		beq $t6, $t5, bool_get_attribute_8741814679438
		j object_get_attribute_8741814679438
		int_get_attribute_8741814679438:
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		sw $t3, 0($v0)
		sw $a0, 4($v0)
		lw $t5, 8($t1)
		sw $t5, 8($v0)
		sw $v0, 20($sp) # internal_0 = self.x
		j end_get_attribute_8741814679438
		bool_get_attribute_8741814679438:
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		sw $t4, 0($v0)
		sw $a0, 4($v0)
		lw $t5, 8($t1)
		sw $t5, 8($v0)
		sw $v0, 20($sp) # internal_0 = self.x
		j end_get_attribute_8741814679438
		object_get_attribute_8741814679438:
		sw $t1, 20($sp) # internal_0 = x
		end_get_attribute_8741814679438:
		
		# Get attribute x of self
		lw $t0, 24($sp) # Get the address of self
		lw $t1, 8($t0) # Get the attribute 'x' from the instance
		lw $t2, 0($t1)
		la $t3, type_Int
		la $t4, type_Bool
		addi $t5, $zero, 1
		seq $t6, $t2, $t3
		beq $t6, $t5, int_get_attribute_8741814679462
		seq $t6, $t2, $t4
		beq $t6, $t5, bool_get_attribute_8741814679462
		j object_get_attribute_8741814679462
		int_get_attribute_8741814679462:
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		sw $t3, 0($v0)
		sw $a0, 4($v0)
		lw $t5, 8($t1)
		sw $t5, 8($v0)
		sw $v0, 16($sp) # internal_1 = self.x
		j end_get_attribute_8741814679462
		bool_get_attribute_8741814679462:
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		sw $t4, 0($v0)
		sw $a0, 4($v0)
		lw $t5, 8($t1)
		sw $t5, 8($v0)
		sw $v0, 16($sp) # internal_1 = self.x
		j end_get_attribute_8741814679462
		object_get_attribute_8741814679462:
		sw $t1, 16($sp) # internal_1 = x
		end_get_attribute_8741814679462:
		
		# Allocating Int 1
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Int # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 1
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 12($sp) # internal_2 = address of allocated object Int
		
		# Allocating Int 4294967295
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Int # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 4294967295
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 8($sp) # internal_3 = address of allocated object Int
		
		# Allocating Int 0
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Int # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 0
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 4($sp) # internal_4 = address of allocated object Int
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument internal_1
		lw $t0, 28($sp)
		sw $t0, 4($sp) # Storing internal_1
		
		# Argument internal_3
		lw $t0, 20($sp)
		sw $t0, 0($sp) # Storing internal_3
		
		# Calling function function_xor
		jal function_xor
		lw $ra, 8($sp)
		sw $v1, 16($sp) # internal_4 = result of function_xor
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument internal_4
		lw $t0, 16($sp)
		sw $t0, 4($sp) # Storing internal_4
		
		# Argument internal_2
		lw $t0, 24($sp)
		sw $t0, 0($sp) # Storing internal_2
		
		# Calling function function_add
		jal function_add
		lw $ra, 8($sp)
		sw $v1, 16($sp) # internal_4 = result of function_add
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument internal_0
		lw $t0, 32($sp)
		sw $t0, 4($sp) # Storing internal_0
		
		# Argument internal_4
		lw $t0, 16($sp)
		sw $t0, 0($sp) # Storing internal_4
		
		# Calling function function_equal
		jal function_equal
		lw $ra, 8($sp)
		sw $v1, 12($sp) # internal_5 = result of function_equal
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# Loading return value in $v1
		lw $v1, 24($sp)
		
		# Freeing space for local variables
		addi $sp, $sp, 24
		
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
		
		