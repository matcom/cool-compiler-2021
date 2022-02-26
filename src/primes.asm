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
	
	type_Main: .word 28
	type_Main_inherits_from: .word type_IO
	type_Main_attributes: .word 5
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
		#   $ra = 40($sp)
		#   a = 36($sp)
		#   b = 32($sp)
		
		# Reserving space for local variables
		addi $sp, $sp, -32
		
		# Allocating Bool 0
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Bool # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 0
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 28($sp) # internal_0 = address of allocated object Int
		
		# internal_1 = typeof a that is the first word of the object
		lw $t0, 36($sp)
		lw $t0, 0($t0)
		sw $t0, 24($sp)
		
		# internal_2 = direction of Int
		la $t0, type_Int
		sw $t0, 20($sp)
		
		# internal_3 = direction of Bool
		la $t0, type_Bool
		sw $t0, 16($sp)
		
		# internal_4 = direction of String
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
		sw $v0, 8($sp) # internal_5 = address of allocated object Int
		
		# Allocating Bool 0
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Bool # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 0
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 4($sp) # internal_6 = address of allocated object Int
		
		# Allocating Bool 0
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Bool # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 0
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 0($sp) # internal_7 = address of allocated object Int
		
		# internal_5 = EqualAddress(internal_1, internal_2)
		lw $t0, 24($sp)
		lw $t1, 20($sp)
		seq $t2, $t0, $t1
		lw $t0, 8($sp)
		sw $t2, 8($t0)
		
		# internal_6 = EqualAddress(internal_1, internal_3)
		lw $t0, 24($sp)
		lw $t1, 16($sp)
		seq $t2, $t0, $t1
		lw $t0, 4($sp)
		sw $t2, 8($t0)
		
		# internal_7 = EqualAddress(internal_1, internal_4)
		lw $t0, 24($sp)
		lw $t1, 12($sp)
		seq $t2, $t0, $t1
		lw $t0, 0($sp)
		sw $t2, 8($t0)
		
		# If internal_5 then goto a_is_type_int_or_bool
		lw $t0, 8($sp) # Loading the address of the condition
		lw $t0, 8($t0) # Loading the value of the condition
		addi $t1, $zero, 1 # Setting the value to 1 for comparison
		beq $t0, $t1, a_is_type_int_or_bool
		
		# If internal_6 then goto a_is_type_int_or_bool
		lw $t0, 4($sp) # Loading the address of the condition
		lw $t0, 8($t0) # Loading the value of the condition
		addi $t1, $zero, 1 # Setting the value to 1 for comparison
		beq $t0, $t1, a_is_type_int_or_bool
		
		# If internal_7 then goto a_is_type_string
		lw $t0, 0($sp) # Loading the address of the condition
		lw $t0, 8($t0) # Loading the value of the condition
		addi $t1, $zero, 1 # Setting the value to 1 for comparison
		beq $t0, $t1, a_is_type_string
		
		# Jumping to a_is_type_object
		j a_is_type_object
		
		a_is_type_int_or_bool:
		
		# internal_0 = EqualInt(a, b)
		lw $t0, 36($sp)
		lw $t0, 8($t0)
		lw $t1, 32($sp)
		lw $t1, 8($t1)
		seq $t2, $t0, $t1
		lw $t0, 28($sp)
		sw $t2, 8($t0)
		
		# Jumping to end_of_equal
		j end_of_equal
		
		a_is_type_string:
		
		# internal_0 = EqualStr(a, b)
		lw $t0, 36($sp)
		lw $t1, 32($sp)
		addi $t0, $t0, 8
		addi $t1, $t1, 8
		
		# By default we assume the strings are equals
		addi $t4, $zero, 1
		lw $t5, 28($sp)
		sw $t4, 8($t5)
		
		while_compare_strings_start:
		lb $t2, 0($t0)
		lb $t3, 0($t1)
		beq $t2, $t3, while_compare_strings_update
		
		# The strings are no equals
		lw $t5, 28($sp)
		sw $zero, 8($t5)
		j while_compare_strings_end
		
		while_compare_strings_update:
		addi $t0, $t0, 1
		addi $t1, $t1, 1
		beq $t2, $zero, while_compare_strings_end
		j while_compare_strings_start
		while_compare_strings_end:
		
		# Jumping to end_of_equal
		j end_of_equal
		
		a_is_type_object:
		
		# Equal operation
		lw $t0, 36($sp) # Save in $t0 the left operand address
		lw $t1, 32($sp) # Save in $t1 the right operand address
		seq $t2, $t0, $t1 # $t2 = $t0 == $t1
		
		lw $t0, 28($sp) # $t0 = internal_0
		sw $t2, 8($t0) # Setting value in the third word of the Bool object
		
		# Jumping to end_of_equal
		j end_of_equal
		
		end_of_equal:
		
		# Loading return value in $v1
		lw $v1, 28($sp)
		
		# Freeing space for local variables
		addi $sp, $sp, 32
		
		jr $ra
		
	function_assign:
		# Function parameters
		#   $ra = 28($sp)
		#   dest = 24($sp)
		#   source = 20($sp)
		
		# Reserving space for local variables
		addi $sp, $sp, -20
		
		# internal_0 = typeof source that is the first word of the object
		lw $t0, 20($sp)
		lw $t0, 0($t0)
		sw $t0, 16($sp)
		
		# internal_1 = direction of Int
		la $t0, type_Int
		sw $t0, 12($sp)
		
		# internal_2 = direction of Bool
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
		sw $v0, 4($sp) # internal_3 = address of allocated object Int
		
		# Allocating Bool 0
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Bool # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 0
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 0($sp) # internal_4 = address of allocated object Int
		
		# internal_3 = EqualAddress(internal_1, internal_1)
		lw $t0, 12($sp)
		lw $t1, 12($sp)
		seq $t2, $t0, $t1
		lw $t0, 4($sp)
		sw $t2, 8($t0)
		
		# internal_4 = EqualAddress(internal_1, internal_2)
		lw $t0, 12($sp)
		lw $t1, 8($sp)
		seq $t2, $t0, $t1
		lw $t0, 0($sp)
		sw $t2, 8($t0)
		
		# If internal_3 then goto source_is_type_int_or_bool
		lw $t0, 4($sp) # Loading the address of the condition
		lw $t0, 8($t0) # Loading the value of the condition
		addi $t1, $zero, 1 # Setting the value to 1 for comparison
		beq $t0, $t1, source_is_type_int_or_bool
		
		# If internal_4 then goto source_is_type_int_or_bool
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
		lw $t0, 20($sp) # Pointer to source
		lw $t1, 0($t0) # $t1 = type of source
		lw $t2, 8($t0) # $t2 = value of source
		sw $t1, 0($v0) # Save type of dest
		sw $a0, 4($v0) # Save size of dest
		sw $t2, 8($v0) # Save value of dest
		sw $v0, 24($sp)
		
		# Jumping to source_end_of_equal
		j source_end_of_equal
		
		source_is_type_object:
		
		# dest = source
		lw $t0, 20($sp)
		sw $t0, 24($sp)
		
		# Jumping to source_end_of_equal
		j source_end_of_equal
		
		source_end_of_equal:
		
		# Loading return value in $v1
		lw $v1, 24($sp)
		
		# Freeing space for local variables
		addi $sp, $sp, 20
		
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
		addi $a0, $zero, 18 # $a0 = length of string + 9 for 4 bytes for the type, 4 bytes for the length of the string and 1 byte for null-terminator
		syscall
		
		la $t0, type_String
		sw $t0, 0($v0) # Setting type in the first word of the object
		
		addi $t0, $zero, 18
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
		
		addi $t0, $zero, 105
		sb $t0, 14($v0) # internal_0[6] = 'i'
		
		addi $t0, $zero, 110
		sb $t0, 15($v0) # internal_0[7] = 'n'
		
		addi $t0, $zero, 32
		sb $t0, 16($v0) # internal_0[8] = ' '
		
		sb $zero, 17($v0) # Null-terminator at the end of the string
		
		sw $v0, 12($sp) # internal_0 = "Abort in "
		
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
		lw $t1, buffer_input($t0) # Loading the byte
		beq $t1, $zero, while_read_end
		addi $t0, $t0, 1 # Incrementing counter
		j while_read_start
		while_read_end:
		
		addi $t0, $t0, 9 # Adding space for the type, the size and the null byte
		li $v0, 9
		move $a0, $t0
		syscall
		la $t2, type_String
		sw $t2, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting length in the second word of the object
		
		addi $t3, $v0, 8 # Pointer to the first character of the string
		xor $t4, $t4, $t4 # Initializing counter
		
		while_copy_from_buffer_start:
		beq $t4, $t0, while_copy_from_buffer_end
		lw $t5, buffer_input($t4) # Loading the byte
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
		
		# internal_0 = length of self
		lw $t0, 4($sp)
		lw $t1, 4($t0)
		addi $t1, $t1, -9 # Subtracting 9 for the type, length, and null-terminator
		sw $t1, 0($sp)
		
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
		lw $t2, 8($sp) # $t2 = start of the substring
		lw $t3, 4($sp) # $t3 = length of the substring
		add $t4, $t2, $t3 # $t4 = start of the substring + length of the substring
		
		bge $t4, $t1, substring_out_of_bounds
		
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
		#   $ra = 228($sp)
		#   self = 224($sp)
		
		# Reserving space for local variables
		addi $sp, $sp, -224
		
		# Allocating String
		li $v0, 9
		addi $a0, $zero, 31 # $a0 = length of string + 9 for 4 bytes for the type, 4 bytes for the length of the string and 1 byte for null-terminator
		syscall
		
		la $t0, type_String
		sw $t0, 0($v0) # Setting type in the first word of the object
		
		addi $t0, $zero, 31
		sw $t0, 4($v0) # Setting length of the string in the second word of the object
		
		addi $t0, $zero, 50
		sb $t0, 8($v0) # internal_0[0] = '2'
		
		addi $t0, $zero, 32
		sb $t0, 9($v0) # internal_0[1] = ' '
		
		addi $t0, $zero, 105
		sb $t0, 10($v0) # internal_0[2] = 'i'
		
		addi $t0, $zero, 115
		sb $t0, 11($v0) # internal_0[3] = 's'
		
		addi $t0, $zero, 32
		sb $t0, 12($v0) # internal_0[4] = ' '
		
		addi $t0, $zero, 116
		sb $t0, 13($v0) # internal_0[5] = 't'
		
		addi $t0, $zero, 114
		sb $t0, 14($v0) # internal_0[6] = 'r'
		
		addi $t0, $zero, 105
		sb $t0, 15($v0) # internal_0[7] = 'i'
		
		addi $t0, $zero, 118
		sb $t0, 16($v0) # internal_0[8] = 'v'
		
		addi $t0, $zero, 105
		sb $t0, 17($v0) # internal_0[9] = 'i'
		
		addi $t0, $zero, 97
		sb $t0, 18($v0) # internal_0[10] = 'a'
		
		addi $t0, $zero, 108
		sb $t0, 19($v0) # internal_0[11] = 'l'
		
		addi $t0, $zero, 108
		sb $t0, 20($v0) # internal_0[12] = 'l'
		
		addi $t0, $zero, 121
		sb $t0, 21($v0) # internal_0[13] = 'y'
		
		addi $t0, $zero, 32
		sb $t0, 22($v0) # internal_0[14] = ' '
		
		addi $t0, $zero, 112
		sb $t0, 23($v0) # internal_0[15] = 'p'
		
		addi $t0, $zero, 114
		sb $t0, 24($v0) # internal_0[16] = 'r'
		
		addi $t0, $zero, 105
		sb $t0, 25($v0) # internal_0[17] = 'i'
		
		addi $t0, $zero, 109
		sb $t0, 26($v0) # internal_0[18] = 'm'
		
		addi $t0, $zero, 101
		sb $t0, 27($v0) # internal_0[19] = 'e'
		
		addi $t0, $zero, 46
		sb $t0, 28($v0) # internal_0[20] = '.'
		
		addi $t0, $zero, 10
		sb $t0, 29($v0) # internal_0[21] = '\n'
		
		sb $zero, 30($v0) # Null-terminator at the end of the string
		
		sw $v0, 220($sp) # internal_0 = "2 is trivially prime.\n"
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument self
		lw $t0, 236($sp)
		sw $t0, 4($sp) # Storing self
		
		# Argument internal_0
		lw $t0, 232($sp)
		sw $t0, 0($sp) # Storing internal_0
		
		# Calling function function_out_string_at_IO
		jal function_out_string_at_IO
		lw $ra, 8($sp)
		sw $v1, 228($sp) # internal_1 = result of function_out_string_at_IO
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# Allocating Int 2
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Int # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 2
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 212($sp) # internal_2 = address of allocated object Int
		
		# Set attribute out of self
		lw $t0, 224($sp) # $t0 = self
		lw $t1, 212($sp) # $t1 = internal_2
		sw $t1, 8($t0) # self.out = internal_2
		
		# Get attribute out of self
		lw $t0, 224($sp) # Get the address of self
		lw $t1, 8($t0) # Get the attribute 'out' from the instance
		sw $t1, 208($sp) # internal_3 = out
		
		# Set attribute testee of self
		lw $t0, 224($sp) # $t0 = self
		lw $t1, 208($sp) # $t1 = internal_3
		sw $t1, 12($t0) # self.testee = internal_3
		
		# Allocating Int 0
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Int # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 0
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 204($sp) # internal_4 = address of allocated object Int
		
		# Set attribute divisor of self
		lw $t0, 224($sp) # $t0 = self
		lw $t1, 204($sp) # $t1 = internal_4
		sw $t1, 16($t0) # self.divisor = internal_4
		
		# Allocating Int 500
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Int # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 500
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 200($sp) # internal_5 = address of allocated object Int
		
		# Set attribute stop of self
		lw $t0, 224($sp) # $t0 = self
		lw $t1, 200($sp) # $t1 = internal_5
		sw $t1, 20($t0) # self.stop = internal_5
		
		
		while_start_8783432246748:
		
		# Allocating Bool 1
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Bool # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 1
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 196($sp) # internal_6 = address of allocated object Int
		
		# If internal_6 then goto while_body_8783432246748
		lw $t0, 196($sp) # Loading the address of the condition
		lw $t0, 8($t0) # Loading the value of the condition
		addi $t1, $zero, 1 # Setting the value to 1 for comparison
		beq $t0, $t1, while_body_8783432246748
		
		# Jumping to while_end_8783432246748
		j while_end_8783432246748
		
		while_body_8783432246748:
		
		# Get attribute testee of self
		lw $t0, 224($sp) # Get the address of self
		lw $t1, 12($t0) # Get the attribute 'testee' from the instance
		sw $t1, 192($sp) # internal_7 = testee
		
		# Allocating Int 1
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Int # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 1
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 188($sp) # internal_8 = address of allocated object Int
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument internal_7
		lw $t0, 204($sp)
		sw $t0, 4($sp) # Storing internal_7
		
		# Argument internal_8
		lw $t0, 200($sp)
		sw $t0, 0($sp) # Storing internal_8
		
		# Calling function function_add
		jal function_add
		lw $ra, 8($sp)
		sw $v1, 196($sp) # internal_9 = result of function_add
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# Set attribute testee of self
		lw $t0, 224($sp) # $t0 = self
		lw $t1, 184($sp) # $t1 = internal_9
		sw $t1, 12($t0) # self.testee = internal_9
		
		# Allocating Int 2
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Int # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 2
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 180($sp) # internal_10 = address of allocated object Int
		
		# Set attribute divisor of self
		lw $t0, 224($sp) # $t0 = self
		lw $t1, 180($sp) # $t1 = internal_10
		sw $t1, 16($t0) # self.divisor = internal_10
		
		
		while_start_8783432246616:
		
		
		# Allocating Bool 0
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Bool # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 0
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 172($sp) # internal_12 = address of allocated object Int
		
		# Get attribute testee of self
		lw $t0, 224($sp) # Get the address of self
		lw $t1, 12($t0) # Get the attribute 'testee' from the instance
		sw $t1, 168($sp) # internal_13 = testee
		
		# Get attribute divisor of self
		lw $t0, 224($sp) # Get the address of self
		lw $t1, 16($t0) # Get the attribute 'divisor' from the instance
		sw $t1, 164($sp) # internal_14 = divisor
		
		# Get attribute divisor of self
		lw $t0, 224($sp) # Get the address of self
		lw $t1, 16($t0) # Get the attribute 'divisor' from the instance
		sw $t1, 160($sp) # internal_15 = divisor
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument internal_14
		lw $t0, 176($sp)
		sw $t0, 4($sp) # Storing internal_14
		
		# Argument internal_15
		lw $t0, 172($sp)
		sw $t0, 0($sp) # Storing internal_15
		
		# Calling function function_mult
		jal function_mult
		lw $ra, 8($sp)
		sw $v1, 168($sp) # internal_16 = result of function_mult
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument internal_13
		lw $t0, 180($sp)
		sw $t0, 4($sp) # Storing internal_13
		
		# Argument internal_16
		lw $t0, 168($sp)
		sw $t0, 0($sp) # Storing internal_16
		
		# Calling function function_less_than
		jal function_less_than
		lw $ra, 8($sp)
		sw $v1, 164($sp) # internal_17 = result of function_less_than
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# internal_12 = internal_17
		lw $t0, 152($sp)
		sw $t0, 172($sp)
		
		# If internal_12 then goto then_8783432246592
		lw $t0, 172($sp) # Loading the address of the condition
		lw $t0, 8($t0) # Loading the value of the condition
		addi $t1, $zero, 1 # Setting the value to 1 for comparison
		beq $t0, $t1, then_8783432246592
		
		# Jumping to else_8783432246592
		j else_8783432246592
		
		then_8783432246592:
		
		# Allocating Bool 0
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Bool # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 0
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 148($sp) # internal_18 = address of allocated object Int
		
		# internal_11 = internal_18
		lw $t0, 148($sp)
		sw $t0, 176($sp)
		
		# Jumping to endif_8783432246592
		j endif_8783432246592
		
		else_8783432246592:
		
		
		# Allocating Bool 0
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Bool # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 0
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 140($sp) # internal_20 = address of allocated object Int
		
		# Get attribute testee of self
		lw $t0, 224($sp) # Get the address of self
		lw $t1, 12($t0) # Get the attribute 'testee' from the instance
		sw $t1, 136($sp) # internal_21 = testee
		
		# Get attribute divisor of self
		lw $t0, 224($sp) # Get the address of self
		lw $t1, 16($t0) # Get the attribute 'divisor' from the instance
		sw $t1, 132($sp) # internal_22 = divisor
		
		# Get attribute testee of self
		lw $t0, 224($sp) # Get the address of self
		lw $t1, 12($t0) # Get the attribute 'testee' from the instance
		sw $t1, 128($sp) # internal_23 = testee
		
		# Get attribute divisor of self
		lw $t0, 224($sp) # Get the address of self
		lw $t1, 16($t0) # Get the attribute 'divisor' from the instance
		sw $t1, 124($sp) # internal_24 = divisor
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument internal_23
		lw $t0, 140($sp)
		sw $t0, 4($sp) # Storing internal_23
		
		# Argument internal_24
		lw $t0, 136($sp)
		sw $t0, 0($sp) # Storing internal_24
		
		# Calling function function_div
		jal function_div
		lw $ra, 8($sp)
		sw $v1, 132($sp) # internal_25 = result of function_div
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument internal_22
		lw $t0, 144($sp)
		sw $t0, 4($sp) # Storing internal_22
		
		# Argument internal_25
		lw $t0, 132($sp)
		sw $t0, 0($sp) # Storing internal_25
		
		# Calling function function_mult
		jal function_mult
		lw $ra, 8($sp)
		sw $v1, 128($sp) # internal_26 = result of function_mult
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument internal_21
		lw $t0, 148($sp)
		sw $t0, 4($sp) # Storing internal_21
		
		# Argument internal_26
		lw $t0, 128($sp)
		sw $t0, 0($sp) # Storing internal_26
		
		# Calling function function_sub
		jal function_sub
		lw $ra, 8($sp)
		sw $v1, 124($sp) # internal_27 = result of function_sub
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
		sw $v0, 108($sp) # internal_28 = address of allocated object Int
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument internal_27
		lw $t0, 124($sp)
		sw $t0, 4($sp) # Storing internal_27
		
		# Argument internal_28
		lw $t0, 120($sp)
		sw $t0, 0($sp) # Storing internal_28
		
		# Calling function function_equal
		jal function_equal
		lw $ra, 8($sp)
		sw $v1, 116($sp) # internal_29 = result of function_equal
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# internal_20 = internal_29
		lw $t0, 104($sp)
		sw $t0, 140($sp)
		
		# If internal_20 then goto then_8783432246586
		lw $t0, 140($sp) # Loading the address of the condition
		lw $t0, 8($t0) # Loading the value of the condition
		addi $t1, $zero, 1 # Setting the value to 1 for comparison
		beq $t0, $t1, then_8783432246586
		
		# Jumping to else_8783432246586
		j else_8783432246586
		
		then_8783432246586:
		
		# Allocating Bool 0
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Bool # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 0
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 100($sp) # internal_30 = address of allocated object Int
		
		# internal_19 = internal_30
		lw $t0, 100($sp)
		sw $t0, 144($sp)
		
		# Jumping to endif_8783432246586
		j endif_8783432246586
		
		else_8783432246586:
		
		# Allocating Bool 1
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Bool # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 1
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 96($sp) # internal_31 = address of allocated object Int
		
		# internal_19 = internal_31
		lw $t0, 96($sp)
		sw $t0, 144($sp)
		
		# Jumping to endif_8783432246586
		j endif_8783432246586
		
		endif_8783432246586:
		
		# internal_11 = internal_19
		lw $t0, 144($sp)
		sw $t0, 176($sp)
		
		# Jumping to endif_8783432246592
		j endif_8783432246592
		
		endif_8783432246592:
		
		# If internal_11 then goto while_body_8783432246616
		lw $t0, 176($sp) # Loading the address of the condition
		lw $t0, 8($t0) # Loading the value of the condition
		addi $t1, $zero, 1 # Setting the value to 1 for comparison
		beq $t0, $t1, while_body_8783432246616
		
		# Jumping to while_end_8783432246616
		j while_end_8783432246616
		
		while_body_8783432246616:
		
		# Get attribute divisor of self
		lw $t0, 224($sp) # Get the address of self
		lw $t1, 16($t0) # Get the attribute 'divisor' from the instance
		sw $t1, 92($sp) # internal_32 = divisor
		
		# Allocating Int 1
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Int # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 1
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 88($sp) # internal_33 = address of allocated object Int
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument internal_32
		lw $t0, 104($sp)
		sw $t0, 4($sp) # Storing internal_32
		
		# Argument internal_33
		lw $t0, 100($sp)
		sw $t0, 0($sp) # Storing internal_33
		
		# Calling function function_add
		jal function_add
		lw $ra, 8($sp)
		sw $v1, 96($sp) # internal_34 = result of function_add
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# Set attribute divisor of self
		lw $t0, 224($sp) # $t0 = self
		lw $t1, 84($sp) # $t1 = internal_34
		sw $t1, 16($t0) # self.divisor = internal_34
		
		# Jumping to while_start_8783432246616
		j while_start_8783432246616
		
		while_end_8783432246616:
		
		
		# Allocating Bool 0
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Bool # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 0
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 76($sp) # internal_36 = address of allocated object Int
		
		# Get attribute testee of self
		lw $t0, 224($sp) # Get the address of self
		lw $t1, 12($t0) # Get the attribute 'testee' from the instance
		sw $t1, 72($sp) # internal_37 = testee
		
		# Get attribute divisor of self
		lw $t0, 224($sp) # Get the address of self
		lw $t1, 16($t0) # Get the attribute 'divisor' from the instance
		sw $t1, 68($sp) # internal_38 = divisor
		
		# Get attribute divisor of self
		lw $t0, 224($sp) # Get the address of self
		lw $t1, 16($t0) # Get the attribute 'divisor' from the instance
		sw $t1, 64($sp) # internal_39 = divisor
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument internal_38
		lw $t0, 80($sp)
		sw $t0, 4($sp) # Storing internal_38
		
		# Argument internal_39
		lw $t0, 76($sp)
		sw $t0, 0($sp) # Storing internal_39
		
		# Calling function function_mult
		jal function_mult
		lw $ra, 8($sp)
		sw $v1, 72($sp) # internal_40 = result of function_mult
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument internal_37
		lw $t0, 84($sp)
		sw $t0, 4($sp) # Storing internal_37
		
		# Argument internal_40
		lw $t0, 72($sp)
		sw $t0, 0($sp) # Storing internal_40
		
		# Calling function function_less_than
		jal function_less_than
		lw $ra, 8($sp)
		sw $v1, 68($sp) # internal_41 = result of function_less_than
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# internal_36 = internal_41
		lw $t0, 56($sp)
		sw $t0, 76($sp)
		
		# If internal_36 then goto then_8783432246682
		lw $t0, 76($sp) # Loading the address of the condition
		lw $t0, 8($t0) # Loading the value of the condition
		addi $t1, $zero, 1 # Setting the value to 1 for comparison
		beq $t0, $t1, then_8783432246682
		
		# Jumping to else_8783432246682
		j else_8783432246682
		
		then_8783432246682:
		
		# Get attribute testee of self
		lw $t0, 224($sp) # Get the address of self
		lw $t1, 12($t0) # Get the attribute 'testee' from the instance
		sw $t1, 52($sp) # internal_42 = testee
		
		# Set attribute out of self
		lw $t0, 224($sp) # $t0 = self
		lw $t1, 52($sp) # $t1 = internal_42
		sw $t1, 8($t0) # self.out = internal_42
		
		# Get attribute out of self
		lw $t0, 224($sp) # Get the address of self
		lw $t1, 8($t0) # Get the attribute 'out' from the instance
		sw $t1, 48($sp) # internal_43 = out
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument self
		lw $t0, 236($sp)
		sw $t0, 4($sp) # Storing self
		
		# Argument internal_43
		lw $t0, 60($sp)
		sw $t0, 0($sp) # Storing internal_43
		
		# Calling function function_out_int_at_IO
		jal function_out_int_at_IO
		lw $ra, 8($sp)
		sw $v1, 56($sp) # internal_44 = result of function_out_int_at_IO
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# Allocating String
		li $v0, 9
		addi $a0, $zero, 20 # $a0 = length of string + 9 for 4 bytes for the type, 4 bytes for the length of the string and 1 byte for null-terminator
		syscall
		
		la $t0, type_String
		sw $t0, 0($v0) # Setting type in the first word of the object
		
		addi $t0, $zero, 20
		sw $t0, 4($v0) # Setting length of the string in the second word of the object
		
		addi $t0, $zero, 32
		sb $t0, 8($v0) # internal_45[0] = ' '
		
		addi $t0, $zero, 105
		sb $t0, 9($v0) # internal_45[1] = 'i'
		
		addi $t0, $zero, 115
		sb $t0, 10($v0) # internal_45[2] = 's'
		
		addi $t0, $zero, 32
		sb $t0, 11($v0) # internal_45[3] = ' '
		
		addi $t0, $zero, 112
		sb $t0, 12($v0) # internal_45[4] = 'p'
		
		addi $t0, $zero, 114
		sb $t0, 13($v0) # internal_45[5] = 'r'
		
		addi $t0, $zero, 105
		sb $t0, 14($v0) # internal_45[6] = 'i'
		
		addi $t0, $zero, 109
		sb $t0, 15($v0) # internal_45[7] = 'm'
		
		addi $t0, $zero, 101
		sb $t0, 16($v0) # internal_45[8] = 'e'
		
		addi $t0, $zero, 46
		sb $t0, 17($v0) # internal_45[9] = '.'
		
		addi $t0, $zero, 10
		sb $t0, 18($v0) # internal_45[10] = '\n'
		
		sb $zero, 19($v0) # Null-terminator at the end of the string
		
		sw $v0, 40($sp) # internal_45 = " is prime.\n"
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument self
		lw $t0, 236($sp)
		sw $t0, 4($sp) # Storing self
		
		# Argument internal_45
		lw $t0, 52($sp)
		sw $t0, 0($sp) # Storing internal_45
		
		# Calling function function_out_string_at_IO
		jal function_out_string_at_IO
		lw $ra, 8($sp)
		sw $v1, 48($sp) # internal_46 = result of function_out_string_at_IO
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# internal_35 = internal_46
		lw $t0, 36($sp)
		sw $t0, 80($sp)
		
		# Jumping to endif_8783432246682
		j endif_8783432246682
		
		else_8783432246682:
		
		# Allocating Int 0
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Int # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 0
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 32($sp) # internal_47 = address of allocated object Int
		
		# internal_35 = internal_47
		lw $t0, 32($sp)
		sw $t0, 80($sp)
		
		# Jumping to endif_8783432246682
		j endif_8783432246682
		
		endif_8783432246682:
		
		
		# Allocating Bool 0
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Bool # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 0
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 24($sp) # internal_49 = address of allocated object Int
		
		# Get attribute stop of self
		lw $t0, 224($sp) # Get the address of self
		lw $t1, 20($t0) # Get the attribute 'stop' from the instance
		sw $t1, 20($sp) # internal_50 = stop
		
		# Get attribute testee of self
		lw $t0, 224($sp) # Get the address of self
		lw $t1, 12($t0) # Get the attribute 'testee' from the instance
		sw $t1, 16($sp) # internal_51 = testee
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument internal_50
		lw $t0, 32($sp)
		sw $t0, 4($sp) # Storing internal_50
		
		# Argument internal_51
		lw $t0, 28($sp)
		sw $t0, 0($sp) # Storing internal_51
		
		# Calling function function_less_than_or_equal
		jal function_less_than_or_equal
		lw $ra, 8($sp)
		sw $v1, 24($sp) # internal_52 = result of function_less_than_or_equal
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# internal_49 = internal_52
		lw $t0, 12($sp)
		sw $t0, 24($sp)
		
		# If internal_49 then goto then_8783432246730
		lw $t0, 24($sp) # Loading the address of the condition
		lw $t0, 8($t0) # Loading the value of the condition
		addi $t1, $zero, 1 # Setting the value to 1 for comparison
		beq $t0, $t1, then_8783432246730
		
		# Jumping to else_8783432246730
		j else_8783432246730
		
		then_8783432246730:
		
		# Allocating String
		li $v0, 9
		addi $a0, $zero, 13 # $a0 = length of string + 9 for 4 bytes for the type, 4 bytes for the length of the string and 1 byte for null-terminator
		syscall
		
		la $t0, type_String
		sw $t0, 0($v0) # Setting type in the first word of the object
		
		addi $t0, $zero, 13
		sw $t0, 4($v0) # Setting length of the string in the second word of the object
		
		addi $t0, $zero, 104
		sb $t0, 8($v0) # internal_53[0] = 'h'
		
		addi $t0, $zero, 97
		sb $t0, 9($v0) # internal_53[1] = 'a'
		
		addi $t0, $zero, 108
		sb $t0, 10($v0) # internal_53[2] = 'l'
		
		addi $t0, $zero, 116
		sb $t0, 11($v0) # internal_53[3] = 't'
		
		sb $zero, 12($v0) # Null-terminator at the end of the string
		
		sw $v0, 8($sp) # internal_53 = "halt"
		
		# Passing function arguments
		addi $sp, $sp, -8 # Reserving space for arguments
		sw $ra, 4($sp) # Storing return address
		
		# Argument internal_53
		lw $t0, 16($sp)
		sw $t0, 0($sp) # Storing internal_53
		
		# Calling function function_abort_at_Object
		jal function_abort_at_Object
		lw $ra, 4($sp)
		sw $v1, 12($sp) # internal_54 = result of function_abort_at_Object
		addi $sp, $sp, 8 # Freeing space for arguments
		
		# internal_48 = internal_54
		lw $t0, 4($sp)
		sw $t0, 28($sp)
		
		# Jumping to endif_8783432246730
		j endif_8783432246730
		
		else_8783432246730:
		
		# Allocating String
		li $v0, 9
		addi $a0, $zero, 17 # $a0 = length of string + 9 for 4 bytes for the type, 4 bytes for the length of the string and 1 byte for null-terminator
		syscall
		
		la $t0, type_String
		sw $t0, 0($v0) # Setting type in the first word of the object
		
		addi $t0, $zero, 17
		sw $t0, 4($v0) # Setting length of the string in the second word of the object
		
		addi $t0, $zero, 99
		sb $t0, 8($v0) # internal_55[0] = 'c'
		
		addi $t0, $zero, 111
		sb $t0, 9($v0) # internal_55[1] = 'o'
		
		addi $t0, $zero, 110
		sb $t0, 10($v0) # internal_55[2] = 'n'
		
		addi $t0, $zero, 116
		sb $t0, 11($v0) # internal_55[3] = 't'
		
		addi $t0, $zero, 105
		sb $t0, 12($v0) # internal_55[4] = 'i'
		
		addi $t0, $zero, 110
		sb $t0, 13($v0) # internal_55[5] = 'n'
		
		addi $t0, $zero, 117
		sb $t0, 14($v0) # internal_55[6] = 'u'
		
		addi $t0, $zero, 101
		sb $t0, 15($v0) # internal_55[7] = 'e'
		
		sb $zero, 16($v0) # Null-terminator at the end of the string
		
		sw $v0, 0($sp) # internal_55 = "continue"
		
		# internal_48 = internal_55
		lw $t0, 0($sp)
		sw $t0, 28($sp)
		
		# Jumping to endif_8783432246730
		j endif_8783432246730
		
		endif_8783432246730:
		
		# Jumping to while_start_8783432246748
		j while_start_8783432246748
		
		while_end_8783432246748:
		
		# Set attribute m of self
		lw $t0, 224($sp) # $t0 = self
		addi $t1, $zero, 0 # $t1 0
		sw $t1, 24($t0) # Set the attribute m of self
		
		# Loading return value in $v1
		lw $v1, 224($sp)
		
		# Freeing space for local variables
		addi $sp, $sp, 224
		
		jr $ra
		
	function_main_at_Main:
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
		
		# Loading return value in $v1
		lw $v1, 0($sp)
		
		# Freeing space for local variables
		addi $sp, $sp, 4
		
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
		
		