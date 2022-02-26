.data
	type_Object: .word 8
	type_Object_inherits_from: .word 0
	type_Object_attributes: .word 0
	type_Object_name_size: .word 6
	type_Object_name: .asciiz "Object"
	
	type_IO: .word 8
	type_IO_inherits_from: .word type_Object
	type_IO_attributes: .word 0
	type_IO_name_size: .word 2
	type_IO_name: .asciiz "IO"
	
	type_Int: .word 8
	type_Int_inherits_from: .word type_Object
	type_Int_attributes: .word 0
	type_Int_name_size: .word 3
	type_Int_name: .asciiz "Int"
	
	type_String: .word 8
	type_String_inherits_from: .word type_Object
	type_String_attributes: .word 0
	type_String_name_size: .word 6
	type_String_name: .asciiz "String"
	
	type_Bool: .word 8
	type_Bool_inherits_from: .word type_Object
	type_Bool_attributes: .word 0
	type_Bool_name_size: .word 4
	type_Bool_name: .asciiz "Bool"
	
	type_List: .word 8
	type_List_inherits_from: .word type_IO
	type_List_attributes: .word 0
	type_List_name_size: .word 4
	type_List_name: .asciiz "List"
	
	type_Cons: .word 16
	type_Cons_inherits_from: .word type_List
	type_Cons_attributes: .word 2
	type_Cons_name_size: .word 4
	type_Cons_name: .asciiz "Cons"
	
	type_Nil: .word 8
	type_Nil_inherits_from: .word type_List
	type_Nil_attributes: .word 0
	type_Nil_name_size: .word 3
	type_Nil_name: .asciiz "Nil"
	
	type_Main: .word 12
	type_Main_inherits_from: .word type_IO
	type_Main_attributes: .word 1
	type_Main_name_size: .word 4
	type_Main_name: .asciiz "Main"
	
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
		
	function___init___at_Int:
		# Function parameters
		#   $ra = 4($sp)
		#   self = 0($sp)
		
		# Allocating Int 0
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Int # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 0
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 0($sp) # self = address of allocated object Int
		
		# Loading return value in $v1
		lw $v1, 0($sp)
		
		jr $ra
		
	function___init___at_Bool:
		# Function parameters
		#   $ra = 4($sp)
		#   self = 0($sp)
		
		# Allocating Bool 0
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Bool # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 0
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 0($sp) # self = address of allocated object Int
		
		# Loading return value in $v1
		lw $v1, 0($sp)
		
		jr $ra
		
	function___init___at_List:
		# Function parameters
		#   $ra = 4($sp)
		#   self = 0($sp)
		
		# Loading return value in $v1
		lw $v1, 0($sp)
		
		jr $ra
		
	function_isNil_at_List:
		# Function parameters
		#   $ra = 12($sp)
		#   self = 8($sp)
		
		# Reserving space for local variables
		addi $sp, $sp, -8
		
		# Passing function arguments
		addi $sp, $sp, -8 # Reserving space for arguments
		sw $ra, 4($sp) # Storing return address
		
		# Argument self
		lw $t0, 16($sp)
		sw $t0, 0($sp) # Storing self
		
		# Calling function function_abort_at_Object
		jal function_abort_at_Object
		lw $ra, 4($sp)
		sw $v1, 12($sp) # internal_0 = result of function_abort_at_Object
		addi $sp, $sp, 8 # Freeing space for arguments
		
		# Allocating Bool 1
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Bool # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 1
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 0($sp) # internal_1 = address of allocated object Int
		
		# Loading return value in $v1
		lw $v1, 0($sp)
		
		# Freeing space for local variables
		addi $sp, $sp, 8
		
		jr $ra
		
	function_cons_at_List:
		# Function parameters
		#   $ra = 20($sp)
		#   self = 16($sp)
		#   hd = 12($sp)
		
		# Reserving space for local variables
		addi $sp, $sp, -12
		
		# Allocating Cons
		li $v0, 9
		lw $a0, type_Cons
		syscall
		la $t0, type_Cons # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of th object
		sw $a0, 4($v0) # Setting size in the second word of th object
		sw $v0, 4($sp) # internal_1 = address of allocated object Cons
		
		# Passing function arguments
		addi $sp, $sp, -8 # Reserving space for arguments
		sw $ra, 4($sp) # Storing return address
		
		# Argument internal_1
		lw $t0, 12($sp)
		sw $t0, 0($sp) # Storing internal_1
		
		# Calling function function___init___at_Cons
		jal function___init___at_Cons
		lw $ra, 4($sp)
		sw $v1, 12($sp) # internal_1 = result of function___init___at_Cons
		addi $sp, $sp, 8 # Freeing space for arguments
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument new_cell
		lw $t0, 20($sp)
		sw $t0, 4($sp) # Storing new_cell
		
		# Argument internal_1
		lw $t0, 16($sp)
		sw $t0, 0($sp) # Storing internal_1
		
		# Calling function function_assign
		jal function_assign
		lw $ra, 8($sp)
		sw $v1, 20($sp) # new_cell = result of function_assign
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# Passing function arguments
		addi $sp, $sp, -16 # Reserving space for arguments
		sw $ra, 12($sp) # Storing return address
		
		# Argument new_cell
		lw $t0, 24($sp)
		sw $t0, 8($sp) # Storing new_cell
		
		# Argument hd
		lw $t0, 28($sp)
		sw $t0, 4($sp) # Storing hd
		
		# Argument self
		lw $t0, 32($sp)
		sw $t0, 0($sp) # Storing self
		
		# Calling function function_init_at_Cons
		jal function_init_at_Cons
		lw $ra, 12($sp)
		sw $v1, 16($sp) # internal_2 = result of function_init_at_Cons
		addi $sp, $sp, 16 # Freeing space for arguments
		
		# Loading return value in $v1
		lw $v1, 0($sp)
		
		# Freeing space for local variables
		addi $sp, $sp, 12
		
		jr $ra
		
	function_car_at_List:
		# Function parameters
		#   $ra = 12($sp)
		#   self = 8($sp)
		
		# Reserving space for local variables
		addi $sp, $sp, -8
		
		# Passing function arguments
		addi $sp, $sp, -8 # Reserving space for arguments
		sw $ra, 4($sp) # Storing return address
		
		# Argument self
		lw $t0, 16($sp)
		sw $t0, 0($sp) # Storing self
		
		# Calling function function_abort_at_Object
		jal function_abort_at_Object
		lw $ra, 4($sp)
		sw $v1, 12($sp) # internal_0 = result of function_abort_at_Object
		addi $sp, $sp, 8 # Freeing space for arguments
		
		# Allocating Int
		li $v0, 9
		lw $a0, type_Int
		syscall
		la $t0, type_Int # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of th object
		sw $a0, 4($v0) # Setting size in the second word of th object
		sw $v0, 0($sp) # internal_1 = address of allocated object Int
		
		# Passing function arguments
		addi $sp, $sp, -8 # Reserving space for arguments
		sw $ra, 4($sp) # Storing return address
		
		# Argument internal_1
		lw $t0, 8($sp)
		sw $t0, 0($sp) # Storing internal_1
		
		# Calling function function___init___at_Int
		jal function___init___at_Int
		lw $ra, 4($sp)
		sw $v1, 8($sp) # internal_1 = result of function___init___at_Int
		addi $sp, $sp, 8 # Freeing space for arguments
		
		# Loading return value in $v1
		lw $v1, 0($sp)
		
		# Freeing space for local variables
		addi $sp, $sp, 8
		
		jr $ra
		
	function_cdr_at_List:
		# Function parameters
		#   $ra = 12($sp)
		#   self = 8($sp)
		
		# Reserving space for local variables
		addi $sp, $sp, -8
		
		# Passing function arguments
		addi $sp, $sp, -8 # Reserving space for arguments
		sw $ra, 4($sp) # Storing return address
		
		# Argument self
		lw $t0, 16($sp)
		sw $t0, 0($sp) # Storing self
		
		# Calling function function_abort_at_Object
		jal function_abort_at_Object
		lw $ra, 4($sp)
		sw $v1, 12($sp) # internal_0 = result of function_abort_at_Object
		addi $sp, $sp, 8 # Freeing space for arguments
		
		# Allocating List
		li $v0, 9
		lw $a0, type_List
		syscall
		la $t0, type_List # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of th object
		sw $a0, 4($v0) # Setting size in the second word of th object
		sw $v0, 0($sp) # internal_1 = address of allocated object List
		
		# Passing function arguments
		addi $sp, $sp, -8 # Reserving space for arguments
		sw $ra, 4($sp) # Storing return address
		
		# Argument internal_1
		lw $t0, 8($sp)
		sw $t0, 0($sp) # Storing internal_1
		
		# Calling function function___init___at_List
		jal function___init___at_List
		lw $ra, 4($sp)
		sw $v1, 8($sp) # internal_1 = result of function___init___at_List
		addi $sp, $sp, 8 # Freeing space for arguments
		
		# Loading return value in $v1
		lw $v1, 0($sp)
		
		# Freeing space for local variables
		addi $sp, $sp, 8
		
		jr $ra
		
	function_rev_at_List:
		# Function parameters
		#   $ra = 8($sp)
		#   self = 4($sp)
		
		# Reserving space for local variables
		addi $sp, $sp, -4
		
		# Passing function arguments
		addi $sp, $sp, -8 # Reserving space for arguments
		sw $ra, 4($sp) # Storing return address
		
		# Argument self
		lw $t0, 12($sp)
		sw $t0, 0($sp) # Storing self
		
		# Calling function function_cdr_at_List
		jal function_cdr_at_List
		lw $ra, 4($sp)
		sw $v1, 8($sp) # internal_0 = result of function_cdr_at_List
		addi $sp, $sp, 8 # Freeing space for arguments
		
		# Loading return value in $v1
		lw $v1, 0($sp)
		
		# Freeing space for local variables
		addi $sp, $sp, 4
		
		jr $ra
		
	function_sort_at_List:
		# Function parameters
		#   $ra = 8($sp)
		#   self = 4($sp)
		
		# Reserving space for local variables
		addi $sp, $sp, -4
		
		# Passing function arguments
		addi $sp, $sp, -8 # Reserving space for arguments
		sw $ra, 4($sp) # Storing return address
		
		# Argument self
		lw $t0, 12($sp)
		sw $t0, 0($sp) # Storing self
		
		# Calling function function_cdr_at_List
		jal function_cdr_at_List
		lw $ra, 4($sp)
		sw $v1, 8($sp) # internal_0 = result of function_cdr_at_List
		addi $sp, $sp, 8 # Freeing space for arguments
		
		# Loading return value in $v1
		lw $v1, 0($sp)
		
		# Freeing space for local variables
		addi $sp, $sp, 4
		
		jr $ra
		
	function_insert_at_List:
		# Function parameters
		#   $ra = 12($sp)
		#   self = 8($sp)
		#   i = 4($sp)
		
		# Reserving space for local variables
		addi $sp, $sp, -4
		
		# Passing function arguments
		addi $sp, $sp, -8 # Reserving space for arguments
		sw $ra, 4($sp) # Storing return address
		
		# Argument self
		lw $t0, 16($sp)
		sw $t0, 0($sp) # Storing self
		
		# Calling function function_cdr_at_List
		jal function_cdr_at_List
		lw $ra, 4($sp)
		sw $v1, 8($sp) # internal_0 = result of function_cdr_at_List
		addi $sp, $sp, 8 # Freeing space for arguments
		
		# Loading return value in $v1
		lw $v1, 0($sp)
		
		# Freeing space for local variables
		addi $sp, $sp, 4
		
		jr $ra
		
	function_rcons_at_List:
		# Function parameters
		#   $ra = 12($sp)
		#   self = 8($sp)
		#   i = 4($sp)
		
		# Reserving space for local variables
		addi $sp, $sp, -4
		
		# Passing function arguments
		addi $sp, $sp, -8 # Reserving space for arguments
		sw $ra, 4($sp) # Storing return address
		
		# Argument self
		lw $t0, 16($sp)
		sw $t0, 0($sp) # Storing self
		
		# Calling function function_cdr_at_List
		jal function_cdr_at_List
		lw $ra, 4($sp)
		sw $v1, 8($sp) # internal_0 = result of function_cdr_at_List
		addi $sp, $sp, 8 # Freeing space for arguments
		
		# Loading return value in $v1
		lw $v1, 0($sp)
		
		# Freeing space for local variables
		addi $sp, $sp, 4
		
		jr $ra
		
	function_print_list_at_List:
		# Function parameters
		#   $ra = 8($sp)
		#   self = 4($sp)
		
		# Reserving space for local variables
		addi $sp, $sp, -4
		
		# Passing function arguments
		addi $sp, $sp, -8 # Reserving space for arguments
		sw $ra, 4($sp) # Storing return address
		
		# Argument self
		lw $t0, 12($sp)
		sw $t0, 0($sp) # Storing self
		
		# Calling function function_abort_at_Object
		jal function_abort_at_Object
		lw $ra, 4($sp)
		sw $v1, 8($sp) # internal_0 = result of function_abort_at_Object
		addi $sp, $sp, 8 # Freeing space for arguments
		
		# Loading return value in $v1
		lw $v1, 0($sp)
		
		# Freeing space for local variables
		addi $sp, $sp, 4
		
		jr $ra
		
	function___init___at_Cons:
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
		
		# Set attribute xcar of self
		lw $t0, 8($sp) # $t0 = self
		lw $t1, 4($sp) # $t1 = internal_0
		beq $t1, $zero, object_set_attribute_8750086222246
		lw $t2, 0($t1)
		la $t3, type_Int
		la $t4, type_Bool
		addi $t5, $zero, 1
		seq $t6, $t2, $t3
		beq $t6, $t5, int_set_attribute_8750086222246
		seq $t6, $t2, $t4
		beq $t6, $t5, bool_set_attribute_8750086222246
		j object_set_attribute_8750086222246
		int_set_attribute_8750086222246:
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		sw $t3, 0($v0)
		sw $a0, 4($v0)
		lw $t5, 8($t1)
		sw $t5, 8($v0)
		sw $v0, 8($t0) # self.xcar = internal_0
		j end_set_attribute_8750086222246
		bool_set_attribute_8750086222246:
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		sw $t4, 0($v0)
		sw $a0, 4($v0)
		lw $t5, 8($t1)
		sw $t5, 8($v0)
		sw $v0, 8($t0) # self.xcar = internal_0
		j end_set_attribute_8750086222246
		object_set_attribute_8750086222246:
		sw $t1, 8($t0) # self.xcar = internal_0
		end_set_attribute_8750086222246:
		
		# Allocating NUll to internal_1
		sw $zero, 0($sp) # internal_1 = 0
		
		# Set attribute xcdr of self
		lw $t0, 8($sp) # $t0 = self
		lw $t1, 0($sp) # $t1 = internal_1
		beq $t1, $zero, object_set_attribute_8750086222267
		lw $t2, 0($t1)
		la $t3, type_Int
		la $t4, type_Bool
		addi $t5, $zero, 1
		seq $t6, $t2, $t3
		beq $t6, $t5, int_set_attribute_8750086222267
		seq $t6, $t2, $t4
		beq $t6, $t5, bool_set_attribute_8750086222267
		j object_set_attribute_8750086222267
		int_set_attribute_8750086222267:
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		sw $t3, 0($v0)
		sw $a0, 4($v0)
		lw $t5, 8($t1)
		sw $t5, 8($v0)
		sw $v0, 12($t0) # self.xcdr = internal_1
		j end_set_attribute_8750086222267
		bool_set_attribute_8750086222267:
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		sw $t4, 0($v0)
		sw $a0, 4($v0)
		lw $t5, 8($t1)
		sw $t5, 8($v0)
		sw $v0, 12($t0) # self.xcdr = internal_1
		j end_set_attribute_8750086222267
		object_set_attribute_8750086222267:
		sw $t1, 12($t0) # self.xcdr = internal_1
		end_set_attribute_8750086222267:
		
		# Loading return value in $v1
		lw $v1, 8($sp)
		
		# Freeing space for local variables
		addi $sp, $sp, 8
		
		jr $ra
		
	function_isNil_at_Cons:
		# Function parameters
		#   $ra = 8($sp)
		#   self = 4($sp)
		
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
		
		# Loading return value in $v1
		lw $v1, 0($sp)
		
		# Freeing space for local variables
		addi $sp, $sp, 4
		
		jr $ra
		
	function_init_at_Cons:
		# Function parameters
		#   $ra = 12($sp)
		#   self = 8($sp)
		#   hd = 4($sp)
		#   tl = 0($sp)
		
		# Set attribute xcar of self
		lw $t0, 8($sp) # $t0 = self
		lw $t1, 4($sp) # $t1 = hd
		beq $t1, $zero, object_set_attribute_8750086190608
		lw $t2, 0($t1)
		la $t3, type_Int
		la $t4, type_Bool
		addi $t5, $zero, 1
		seq $t6, $t2, $t3
		beq $t6, $t5, int_set_attribute_8750086190608
		seq $t6, $t2, $t4
		beq $t6, $t5, bool_set_attribute_8750086190608
		j object_set_attribute_8750086190608
		int_set_attribute_8750086190608:
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		sw $t3, 0($v0)
		sw $a0, 4($v0)
		lw $t5, 8($t1)
		sw $t5, 8($v0)
		sw $v0, 8($t0) # self.xcar = hd
		j end_set_attribute_8750086190608
		bool_set_attribute_8750086190608:
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		sw $t4, 0($v0)
		sw $a0, 4($v0)
		lw $t5, 8($t1)
		sw $t5, 8($v0)
		sw $v0, 8($t0) # self.xcar = hd
		j end_set_attribute_8750086190608
		object_set_attribute_8750086190608:
		sw $t1, 8($t0) # self.xcar = hd
		end_set_attribute_8750086190608:
		
		# Set attribute xcdr of self
		lw $t0, 8($sp) # $t0 = self
		lw $t1, 0($sp) # $t1 = tl
		beq $t1, $zero, object_set_attribute_8750086190617
		lw $t2, 0($t1)
		la $t3, type_Int
		la $t4, type_Bool
		addi $t5, $zero, 1
		seq $t6, $t2, $t3
		beq $t6, $t5, int_set_attribute_8750086190617
		seq $t6, $t2, $t4
		beq $t6, $t5, bool_set_attribute_8750086190617
		j object_set_attribute_8750086190617
		int_set_attribute_8750086190617:
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		sw $t3, 0($v0)
		sw $a0, 4($v0)
		lw $t5, 8($t1)
		sw $t5, 8($v0)
		sw $v0, 12($t0) # self.xcdr = tl
		j end_set_attribute_8750086190617
		bool_set_attribute_8750086190617:
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		sw $t4, 0($v0)
		sw $a0, 4($v0)
		lw $t5, 8($t1)
		sw $t5, 8($v0)
		sw $v0, 12($t0) # self.xcdr = tl
		j end_set_attribute_8750086190617
		object_set_attribute_8750086190617:
		sw $t1, 12($t0) # self.xcdr = tl
		end_set_attribute_8750086190617:
		
		# Loading return value in $v1
		lw $v1, 8($sp)
		
		jr $ra
		
	function_car_at_Cons:
		# Function parameters
		#   $ra = 8($sp)
		#   self = 4($sp)
		
		# Reserving space for local variables
		addi $sp, $sp, -4
		
		# Get attribute xcar of self
		lw $t0, 4($sp) # Get the address of self
		lw $t1, 8($t0) # Get the attribute 'xcar' from the instance
		lw $t2, 0($t1)
		la $t3, type_Int
		la $t4, type_Bool
		addi $t5, $zero, 1
		seq $t6, $t2, $t3
		beq $t6, $t5, int_get_attribute_8750086190629
		seq $t6, $t2, $t4
		beq $t6, $t5, bool_get_attribute_8750086190629
		j object_get_attribute_8750086190629
		int_get_attribute_8750086190629:
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		sw $t3, 0($v0)
		sw $a0, 4($v0)
		lw $t5, 8($t1)
		sw $t5, 8($v0)
		sw $v0, 0($sp) # internal_0 = self.xcar
		j end_get_attribute_8750086190629
		bool_get_attribute_8750086190629:
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		sw $t4, 0($v0)
		sw $a0, 4($v0)
		lw $t5, 8($t1)
		sw $t5, 8($v0)
		sw $v0, 0($sp) # internal_0 = self.xcar
		j end_get_attribute_8750086190629
		object_get_attribute_8750086190629:
		sw $t1, 0($sp) # internal_0 = xcar
		end_get_attribute_8750086190629:
		
		# Loading return value in $v1
		lw $v1, 0($sp)
		
		# Freeing space for local variables
		addi $sp, $sp, 4
		
		jr $ra
		
	function_cdr_at_Cons:
		# Function parameters
		#   $ra = 8($sp)
		#   self = 4($sp)
		
		# Reserving space for local variables
		addi $sp, $sp, -4
		
		# Get attribute xcdr of self
		lw $t0, 4($sp) # Get the address of self
		lw $t1, 12($t0) # Get the attribute 'xcdr' from the instance
		lw $t2, 0($t1)
		la $t3, type_Int
		la $t4, type_Bool
		addi $t5, $zero, 1
		seq $t6, $t2, $t3
		beq $t6, $t5, int_get_attribute_8750086211368
		seq $t6, $t2, $t4
		beq $t6, $t5, bool_get_attribute_8750086211368
		j object_get_attribute_8750086211368
		int_get_attribute_8750086211368:
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		sw $t3, 0($v0)
		sw $a0, 4($v0)
		lw $t5, 8($t1)
		sw $t5, 8($v0)
		sw $v0, 0($sp) # internal_0 = self.xcdr
		j end_get_attribute_8750086211368
		bool_get_attribute_8750086211368:
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		sw $t4, 0($v0)
		sw $a0, 4($v0)
		lw $t5, 8($t1)
		sw $t5, 8($v0)
		sw $v0, 0($sp) # internal_0 = self.xcdr
		j end_get_attribute_8750086211368
		object_get_attribute_8750086211368:
		sw $t1, 0($sp) # internal_0 = xcdr
		end_get_attribute_8750086211368:
		
		# Loading return value in $v1
		lw $v1, 0($sp)
		
		# Freeing space for local variables
		addi $sp, $sp, 4
		
		jr $ra
		
	function_rev_at_Cons:
		# Function parameters
		#   $ra = 20($sp)
		#   self = 16($sp)
		
		# Reserving space for local variables
		addi $sp, $sp, -16
		
		# Get attribute xcdr of self
		lw $t0, 16($sp) # Get the address of self
		lw $t1, 12($t0) # Get the attribute 'xcdr' from the instance
		lw $t2, 0($t1)
		la $t3, type_Int
		la $t4, type_Bool
		addi $t5, $zero, 1
		seq $t6, $t2, $t3
		beq $t6, $t5, int_get_attribute_8750086210618
		seq $t6, $t2, $t4
		beq $t6, $t5, bool_get_attribute_8750086210618
		j object_get_attribute_8750086210618
		int_get_attribute_8750086210618:
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		sw $t3, 0($v0)
		sw $a0, 4($v0)
		lw $t5, 8($t1)
		sw $t5, 8($v0)
		sw $v0, 12($sp) # internal_0 = self.xcdr
		j end_get_attribute_8750086210618
		bool_get_attribute_8750086210618:
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		sw $t4, 0($v0)
		sw $a0, 4($v0)
		lw $t5, 8($t1)
		sw $t5, 8($v0)
		sw $v0, 12($sp) # internal_0 = self.xcdr
		j end_get_attribute_8750086210618
		object_get_attribute_8750086210618:
		sw $t1, 12($sp) # internal_0 = xcdr
		end_get_attribute_8750086210618:
		
		# Passing function arguments
		addi $sp, $sp, -8 # Reserving space for arguments
		sw $ra, 4($sp) # Storing return address
		
		# Argument internal_0
		lw $t0, 20($sp)
		sw $t0, 0($sp) # Storing internal_0
		
		# Calling function function_rev_at_List
		jal function_rev_at_List
		lw $ra, 4($sp)
		sw $v1, 16($sp) # internal_1 = result of function_rev_at_List
		addi $sp, $sp, 8 # Freeing space for arguments
		
		# Get attribute xcar of self
		lw $t0, 16($sp) # Get the address of self
		lw $t1, 8($t0) # Get the attribute 'xcar' from the instance
		lw $t2, 0($t1)
		la $t3, type_Int
		la $t4, type_Bool
		addi $t5, $zero, 1
		seq $t6, $t2, $t3
		beq $t6, $t5, int_get_attribute_8750086210621
		seq $t6, $t2, $t4
		beq $t6, $t5, bool_get_attribute_8750086210621
		j object_get_attribute_8750086210621
		int_get_attribute_8750086210621:
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		sw $t3, 0($v0)
		sw $a0, 4($v0)
		lw $t5, 8($t1)
		sw $t5, 8($v0)
		sw $v0, 4($sp) # internal_2 = self.xcar
		j end_get_attribute_8750086210621
		bool_get_attribute_8750086210621:
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		sw $t4, 0($v0)
		sw $a0, 4($v0)
		lw $t5, 8($t1)
		sw $t5, 8($v0)
		sw $v0, 4($sp) # internal_2 = self.xcar
		j end_get_attribute_8750086210621
		object_get_attribute_8750086210621:
		sw $t1, 4($sp) # internal_2 = xcar
		end_get_attribute_8750086210621:
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument internal_1
		lw $t0, 20($sp)
		sw $t0, 4($sp) # Storing internal_1
		
		# Argument internal_2
		lw $t0, 16($sp)
		sw $t0, 0($sp) # Storing internal_2
		
		# Calling function function_rcons_at_List
		jal function_rcons_at_List
		lw $ra, 8($sp)
		sw $v1, 12($sp) # internal_3 = result of function_rcons_at_List
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# Loading return value in $v1
		lw $v1, 0($sp)
		
		# Freeing space for local variables
		addi $sp, $sp, 16
		
		jr $ra
		
	function_sort_at_Cons:
		# Function parameters
		#   $ra = 20($sp)
		#   self = 16($sp)
		
		# Reserving space for local variables
		addi $sp, $sp, -16
		
		# Get attribute xcdr of self
		lw $t0, 16($sp) # Get the address of self
		lw $t1, 12($t0) # Get the attribute 'xcdr' from the instance
		lw $t2, 0($t1)
		la $t3, type_Int
		la $t4, type_Bool
		addi $t5, $zero, 1
		seq $t6, $t2, $t3
		beq $t6, $t5, int_get_attribute_8750086210564
		seq $t6, $t2, $t4
		beq $t6, $t5, bool_get_attribute_8750086210564
		j object_get_attribute_8750086210564
		int_get_attribute_8750086210564:
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		sw $t3, 0($v0)
		sw $a0, 4($v0)
		lw $t5, 8($t1)
		sw $t5, 8($v0)
		sw $v0, 12($sp) # internal_0 = self.xcdr
		j end_get_attribute_8750086210564
		bool_get_attribute_8750086210564:
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		sw $t4, 0($v0)
		sw $a0, 4($v0)
		lw $t5, 8($t1)
		sw $t5, 8($v0)
		sw $v0, 12($sp) # internal_0 = self.xcdr
		j end_get_attribute_8750086210564
		object_get_attribute_8750086210564:
		sw $t1, 12($sp) # internal_0 = xcdr
		end_get_attribute_8750086210564:
		
		# Passing function arguments
		addi $sp, $sp, -8 # Reserving space for arguments
		sw $ra, 4($sp) # Storing return address
		
		# Argument internal_0
		lw $t0, 20($sp)
		sw $t0, 0($sp) # Storing internal_0
		
		# Calling function function_sort_at_List
		jal function_sort_at_List
		lw $ra, 4($sp)
		sw $v1, 16($sp) # internal_1 = result of function_sort_at_List
		addi $sp, $sp, 8 # Freeing space for arguments
		
		# Get attribute xcar of self
		lw $t0, 16($sp) # Get the address of self
		lw $t1, 8($t0) # Get the attribute 'xcar' from the instance
		lw $t2, 0($t1)
		la $t3, type_Int
		la $t4, type_Bool
		addi $t5, $zero, 1
		seq $t6, $t2, $t3
		beq $t6, $t5, int_get_attribute_8750086208618
		seq $t6, $t2, $t4
		beq $t6, $t5, bool_get_attribute_8750086208618
		j object_get_attribute_8750086208618
		int_get_attribute_8750086208618:
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		sw $t3, 0($v0)
		sw $a0, 4($v0)
		lw $t5, 8($t1)
		sw $t5, 8($v0)
		sw $v0, 4($sp) # internal_2 = self.xcar
		j end_get_attribute_8750086208618
		bool_get_attribute_8750086208618:
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		sw $t4, 0($v0)
		sw $a0, 4($v0)
		lw $t5, 8($t1)
		sw $t5, 8($v0)
		sw $v0, 4($sp) # internal_2 = self.xcar
		j end_get_attribute_8750086208618
		object_get_attribute_8750086208618:
		sw $t1, 4($sp) # internal_2 = xcar
		end_get_attribute_8750086208618:
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument internal_1
		lw $t0, 20($sp)
		sw $t0, 4($sp) # Storing internal_1
		
		# Argument internal_2
		lw $t0, 16($sp)
		sw $t0, 0($sp) # Storing internal_2
		
		# Calling function function_insert_at_List
		jal function_insert_at_List
		lw $ra, 8($sp)
		sw $v1, 12($sp) # internal_3 = result of function_insert_at_List
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# Loading return value in $v1
		lw $v1, 0($sp)
		
		# Freeing space for local variables
		addi $sp, $sp, 16
		
		jr $ra
		
	function_insert_at_Cons:
		# Function parameters
		#   $ra = 52($sp)
		#   self = 48($sp)
		#   i = 44($sp)
		
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
		
		# Get attribute xcar of self
		lw $t0, 48($sp) # Get the address of self
		lw $t1, 8($t0) # Get the attribute 'xcar' from the instance
		lw $t2, 0($t1)
		la $t3, type_Int
		la $t4, type_Bool
		addi $t5, $zero, 1
		seq $t6, $t2, $t3
		beq $t6, $t5, int_get_attribute_8750086208690
		seq $t6, $t2, $t4
		beq $t6, $t5, bool_get_attribute_8750086208690
		j object_get_attribute_8750086208690
		int_get_attribute_8750086208690:
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		sw $t3, 0($v0)
		sw $a0, 4($v0)
		lw $t5, 8($t1)
		sw $t5, 8($v0)
		sw $v0, 32($sp) # internal_2 = self.xcar
		j end_get_attribute_8750086208690
		bool_get_attribute_8750086208690:
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		sw $t4, 0($v0)
		sw $a0, 4($v0)
		lw $t5, 8($t1)
		sw $t5, 8($v0)
		sw $v0, 32($sp) # internal_2 = self.xcar
		j end_get_attribute_8750086208690
		object_get_attribute_8750086208690:
		sw $t1, 32($sp) # internal_2 = xcar
		end_get_attribute_8750086208690:
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument i
		lw $t0, 56($sp)
		sw $t0, 4($sp) # Storing i
		
		# Argument internal_2
		lw $t0, 44($sp)
		sw $t0, 0($sp) # Storing internal_2
		
		# Calling function function_less_than
		jal function_less_than
		lw $ra, 8($sp)
		sw $v1, 40($sp) # internal_3 = result of function_less_than
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# internal_1 = internal_3
		lw $t0, 28($sp)
		sw $t0, 36($sp)
		
		# If internal_1 then goto then_8750086234655
		lw $t0, 36($sp) # Loading the address of the condition
		lw $t0, 8($t0) # Loading the value of the condition
		addi $t1, $zero, 1 # Setting the value to 1 for comparison
		beq $t0, $t1, then_8750086234655
		
		# Jumping to else_8750086234655
		j else_8750086234655
		
		then_8750086234655:
		
		# Allocating Cons
		li $v0, 9
		lw $a0, type_Cons
		syscall
		la $t0, type_Cons # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of th object
		sw $a0, 4($v0) # Setting size in the second word of th object
		sw $v0, 24($sp) # internal_4 = address of allocated object Cons
		
		# Passing function arguments
		addi $sp, $sp, -8 # Reserving space for arguments
		sw $ra, 4($sp) # Storing return address
		
		# Argument internal_4
		lw $t0, 32($sp)
		sw $t0, 0($sp) # Storing internal_4
		
		# Calling function function___init___at_Cons
		jal function___init___at_Cons
		lw $ra, 4($sp)
		sw $v1, 32($sp) # internal_4 = result of function___init___at_Cons
		addi $sp, $sp, 8 # Freeing space for arguments
		
		# Passing function arguments
		addi $sp, $sp, -16 # Reserving space for arguments
		sw $ra, 12($sp) # Storing return address
		
		# Argument internal_4
		lw $t0, 40($sp)
		sw $t0, 8($sp) # Storing internal_4
		
		# Argument i
		lw $t0, 60($sp)
		sw $t0, 4($sp) # Storing i
		
		# Argument self
		lw $t0, 64($sp)
		sw $t0, 0($sp) # Storing self
		
		# Calling function function_init_at_Cons
		jal function_init_at_Cons
		lw $ra, 12($sp)
		sw $v1, 36($sp) # internal_5 = result of function_init_at_Cons
		addi $sp, $sp, 16 # Freeing space for arguments
		
		# internal_0 = internal_5
		lw $t0, 20($sp)
		sw $t0, 40($sp)
		
		# Jumping to endif_8750086234655
		j endif_8750086234655
		
		else_8750086234655:
		
		# Allocating Cons
		li $v0, 9
		lw $a0, type_Cons
		syscall
		la $t0, type_Cons # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of th object
		sw $a0, 4($v0) # Setting size in the second word of th object
		sw $v0, 16($sp) # internal_6 = address of allocated object Cons
		
		# Passing function arguments
		addi $sp, $sp, -8 # Reserving space for arguments
		sw $ra, 4($sp) # Storing return address
		
		# Argument internal_6
		lw $t0, 24($sp)
		sw $t0, 0($sp) # Storing internal_6
		
		# Calling function function___init___at_Cons
		jal function___init___at_Cons
		lw $ra, 4($sp)
		sw $v1, 24($sp) # internal_6 = result of function___init___at_Cons
		addi $sp, $sp, 8 # Freeing space for arguments
		
		# Get attribute xcar of self
		lw $t0, 48($sp) # Get the address of self
		lw $t1, 8($t0) # Get the attribute 'xcar' from the instance
		lw $t2, 0($t1)
		la $t3, type_Int
		la $t4, type_Bool
		addi $t5, $zero, 1
		seq $t6, $t2, $t3
		beq $t6, $t5, int_get_attribute_8750086210058
		seq $t6, $t2, $t4
		beq $t6, $t5, bool_get_attribute_8750086210058
		j object_get_attribute_8750086210058
		int_get_attribute_8750086210058:
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		sw $t3, 0($v0)
		sw $a0, 4($v0)
		lw $t5, 8($t1)
		sw $t5, 8($v0)
		sw $v0, 12($sp) # internal_7 = self.xcar
		j end_get_attribute_8750086210058
		bool_get_attribute_8750086210058:
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		sw $t4, 0($v0)
		sw $a0, 4($v0)
		lw $t5, 8($t1)
		sw $t5, 8($v0)
		sw $v0, 12($sp) # internal_7 = self.xcar
		j end_get_attribute_8750086210058
		object_get_attribute_8750086210058:
		sw $t1, 12($sp) # internal_7 = xcar
		end_get_attribute_8750086210058:
		
		# Get attribute xcdr of self
		lw $t0, 48($sp) # Get the address of self
		lw $t1, 12($t0) # Get the attribute 'xcdr' from the instance
		lw $t2, 0($t1)
		la $t3, type_Int
		la $t4, type_Bool
		addi $t5, $zero, 1
		seq $t6, $t2, $t3
		beq $t6, $t5, int_get_attribute_8750086207735
		seq $t6, $t2, $t4
		beq $t6, $t5, bool_get_attribute_8750086207735
		j object_get_attribute_8750086207735
		int_get_attribute_8750086207735:
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		sw $t3, 0($v0)
		sw $a0, 4($v0)
		lw $t5, 8($t1)
		sw $t5, 8($v0)
		sw $v0, 8($sp) # internal_8 = self.xcdr
		j end_get_attribute_8750086207735
		bool_get_attribute_8750086207735:
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		sw $t4, 0($v0)
		sw $a0, 4($v0)
		lw $t5, 8($t1)
		sw $t5, 8($v0)
		sw $v0, 8($sp) # internal_8 = self.xcdr
		j end_get_attribute_8750086207735
		object_get_attribute_8750086207735:
		sw $t1, 8($sp) # internal_8 = xcdr
		end_get_attribute_8750086207735:
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument internal_8
		lw $t0, 20($sp)
		sw $t0, 4($sp) # Storing internal_8
		
		# Argument i
		lw $t0, 56($sp)
		sw $t0, 0($sp) # Storing i
		
		# Calling function function_insert_at_List
		jal function_insert_at_List
		lw $ra, 8($sp)
		sw $v1, 16($sp) # internal_9 = result of function_insert_at_List
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# Passing function arguments
		addi $sp, $sp, -16 # Reserving space for arguments
		sw $ra, 12($sp) # Storing return address
		
		# Argument internal_6
		lw $t0, 32($sp)
		sw $t0, 8($sp) # Storing internal_6
		
		# Argument internal_7
		lw $t0, 28($sp)
		sw $t0, 4($sp) # Storing internal_7
		
		# Argument internal_9
		lw $t0, 20($sp)
		sw $t0, 0($sp) # Storing internal_9
		
		# Calling function function_init_at_Cons
		jal function_init_at_Cons
		lw $ra, 12($sp)
		sw $v1, 16($sp) # internal_10 = result of function_init_at_Cons
		addi $sp, $sp, 16 # Freeing space for arguments
		
		# internal_0 = internal_10
		lw $t0, 0($sp)
		sw $t0, 40($sp)
		
		# Jumping to endif_8750086234655
		j endif_8750086234655
		
		endif_8750086234655:
		
		# Loading return value in $v1
		lw $v1, 40($sp)
		
		# Freeing space for local variables
		addi $sp, $sp, 44
		
		jr $ra
		
	function_rcons_at_Cons:
		# Function parameters
		#   $ra = 28($sp)
		#   self = 24($sp)
		#   i = 20($sp)
		
		# Reserving space for local variables
		addi $sp, $sp, -20
		
		# Allocating Cons
		li $v0, 9
		lw $a0, type_Cons
		syscall
		la $t0, type_Cons # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of th object
		sw $a0, 4($v0) # Setting size in the second word of th object
		sw $v0, 16($sp) # internal_0 = address of allocated object Cons
		
		# Passing function arguments
		addi $sp, $sp, -8 # Reserving space for arguments
		sw $ra, 4($sp) # Storing return address
		
		# Argument internal_0
		lw $t0, 24($sp)
		sw $t0, 0($sp) # Storing internal_0
		
		# Calling function function___init___at_Cons
		jal function___init___at_Cons
		lw $ra, 4($sp)
		sw $v1, 24($sp) # internal_0 = result of function___init___at_Cons
		addi $sp, $sp, 8 # Freeing space for arguments
		
		# Get attribute xcar of self
		lw $t0, 24($sp) # Get the address of self
		lw $t1, 8($t0) # Get the attribute 'xcar' from the instance
		lw $t2, 0($t1)
		la $t3, type_Int
		la $t4, type_Bool
		addi $t5, $zero, 1
		seq $t6, $t2, $t3
		beq $t6, $t5, int_get_attribute_8750086190746
		seq $t6, $t2, $t4
		beq $t6, $t5, bool_get_attribute_8750086190746
		j object_get_attribute_8750086190746
		int_get_attribute_8750086190746:
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		sw $t3, 0($v0)
		sw $a0, 4($v0)
		lw $t5, 8($t1)
		sw $t5, 8($v0)
		sw $v0, 12($sp) # internal_1 = self.xcar
		j end_get_attribute_8750086190746
		bool_get_attribute_8750086190746:
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		sw $t4, 0($v0)
		sw $a0, 4($v0)
		lw $t5, 8($t1)
		sw $t5, 8($v0)
		sw $v0, 12($sp) # internal_1 = self.xcar
		j end_get_attribute_8750086190746
		object_get_attribute_8750086190746:
		sw $t1, 12($sp) # internal_1 = xcar
		end_get_attribute_8750086190746:
		
		# Get attribute xcdr of self
		lw $t0, 24($sp) # Get the address of self
		lw $t1, 12($t0) # Get the attribute 'xcdr' from the instance
		lw $t2, 0($t1)
		la $t3, type_Int
		la $t4, type_Bool
		addi $t5, $zero, 1
		seq $t6, $t2, $t3
		beq $t6, $t5, int_get_attribute_8750086190770
		seq $t6, $t2, $t4
		beq $t6, $t5, bool_get_attribute_8750086190770
		j object_get_attribute_8750086190770
		int_get_attribute_8750086190770:
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		sw $t3, 0($v0)
		sw $a0, 4($v0)
		lw $t5, 8($t1)
		sw $t5, 8($v0)
		sw $v0, 8($sp) # internal_2 = self.xcdr
		j end_get_attribute_8750086190770
		bool_get_attribute_8750086190770:
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		sw $t4, 0($v0)
		sw $a0, 4($v0)
		lw $t5, 8($t1)
		sw $t5, 8($v0)
		sw $v0, 8($sp) # internal_2 = self.xcdr
		j end_get_attribute_8750086190770
		object_get_attribute_8750086190770:
		sw $t1, 8($sp) # internal_2 = xcdr
		end_get_attribute_8750086190770:
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument internal_2
		lw $t0, 20($sp)
		sw $t0, 4($sp) # Storing internal_2
		
		# Argument i
		lw $t0, 32($sp)
		sw $t0, 0($sp) # Storing i
		
		# Calling function function_rcons_at_List
		jal function_rcons_at_List
		lw $ra, 8($sp)
		sw $v1, 16($sp) # internal_3 = result of function_rcons_at_List
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# Passing function arguments
		addi $sp, $sp, -16 # Reserving space for arguments
		sw $ra, 12($sp) # Storing return address
		
		# Argument internal_0
		lw $t0, 32($sp)
		sw $t0, 8($sp) # Storing internal_0
		
		# Argument internal_1
		lw $t0, 28($sp)
		sw $t0, 4($sp) # Storing internal_1
		
		# Argument internal_3
		lw $t0, 20($sp)
		sw $t0, 0($sp) # Storing internal_3
		
		# Calling function function_init_at_Cons
		jal function_init_at_Cons
		lw $ra, 12($sp)
		sw $v1, 16($sp) # internal_4 = result of function_init_at_Cons
		addi $sp, $sp, 16 # Freeing space for arguments
		
		# Loading return value in $v1
		lw $v1, 0($sp)
		
		# Freeing space for local variables
		addi $sp, $sp, 20
		
		jr $ra
		
	function_print_list_at_Cons:
		# Function parameters
		#   $ra = 28($sp)
		#   self = 24($sp)
		
		# Reserving space for local variables
		addi $sp, $sp, -24
		
		# Get attribute xcar of self
		lw $t0, 24($sp) # Get the address of self
		lw $t1, 8($t0) # Get the attribute 'xcar' from the instance
		lw $t2, 0($t1)
		la $t3, type_Int
		la $t4, type_Bool
		addi $t5, $zero, 1
		seq $t6, $t2, $t3
		beq $t6, $t5, int_get_attribute_8750086190861
		seq $t6, $t2, $t4
		beq $t6, $t5, bool_get_attribute_8750086190861
		j object_get_attribute_8750086190861
		int_get_attribute_8750086190861:
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		sw $t3, 0($v0)
		sw $a0, 4($v0)
		lw $t5, 8($t1)
		sw $t5, 8($v0)
		sw $v0, 20($sp) # internal_0 = self.xcar
		j end_get_attribute_8750086190861
		bool_get_attribute_8750086190861:
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		sw $t4, 0($v0)
		sw $a0, 4($v0)
		lw $t5, 8($t1)
		sw $t5, 8($v0)
		sw $v0, 20($sp) # internal_0 = self.xcar
		j end_get_attribute_8750086190861
		object_get_attribute_8750086190861:
		sw $t1, 20($sp) # internal_0 = xcar
		end_get_attribute_8750086190861:
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument self
		lw $t0, 36($sp)
		sw $t0, 4($sp) # Storing self
		
		# Argument internal_0
		lw $t0, 32($sp)
		sw $t0, 0($sp) # Storing internal_0
		
		# Calling function function_out_int_at_IO
		jal function_out_int_at_IO
		lw $ra, 8($sp)
		sw $v1, 28($sp) # internal_1 = result of function_out_int_at_IO
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
		sb $t0, 8($v0) # internal_2[0] = '\n'
		
		sb $zero, 9($v0) # Null-terminator at the end of the string
		
		sw $v0, 12($sp) # internal_2 = "\n"
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument self
		lw $t0, 36($sp)
		sw $t0, 4($sp) # Storing self
		
		# Argument internal_2
		lw $t0, 24($sp)
		sw $t0, 0($sp) # Storing internal_2
		
		# Calling function function_out_string_at_IO
		jal function_out_string_at_IO
		lw $ra, 8($sp)
		sw $v1, 20($sp) # internal_3 = result of function_out_string_at_IO
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# Get attribute xcdr of self
		lw $t0, 24($sp) # Get the address of self
		lw $t1, 12($t0) # Get the attribute 'xcdr' from the instance
		lw $t2, 0($t1)
		la $t3, type_Int
		la $t4, type_Bool
		addi $t5, $zero, 1
		seq $t6, $t2, $t3
		beq $t6, $t5, int_get_attribute_8750086190930
		seq $t6, $t2, $t4
		beq $t6, $t5, bool_get_attribute_8750086190930
		j object_get_attribute_8750086190930
		int_get_attribute_8750086190930:
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		sw $t3, 0($v0)
		sw $a0, 4($v0)
		lw $t5, 8($t1)
		sw $t5, 8($v0)
		sw $v0, 4($sp) # internal_4 = self.xcdr
		j end_get_attribute_8750086190930
		bool_get_attribute_8750086190930:
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		sw $t4, 0($v0)
		sw $a0, 4($v0)
		lw $t5, 8($t1)
		sw $t5, 8($v0)
		sw $v0, 4($sp) # internal_4 = self.xcdr
		j end_get_attribute_8750086190930
		object_get_attribute_8750086190930:
		sw $t1, 4($sp) # internal_4 = xcdr
		end_get_attribute_8750086190930:
		
		# Passing function arguments
		addi $sp, $sp, -8 # Reserving space for arguments
		sw $ra, 4($sp) # Storing return address
		
		# Argument internal_4
		lw $t0, 12($sp)
		sw $t0, 0($sp) # Storing internal_4
		
		# Calling function function_print_list_at_List
		jal function_print_list_at_List
		lw $ra, 4($sp)
		sw $v1, 8($sp) # internal_5 = result of function_print_list_at_List
		addi $sp, $sp, 8 # Freeing space for arguments
		
		# Loading return value in $v1
		lw $v1, 0($sp)
		
		# Freeing space for local variables
		addi $sp, $sp, 24
		
		jr $ra
		
	function___init___at_Nil:
		# Function parameters
		#   $ra = 4($sp)
		#   self = 0($sp)
		
		# Loading return value in $v1
		lw $v1, 0($sp)
		
		jr $ra
		
	function_isNil_at_Nil:
		# Function parameters
		#   $ra = 8($sp)
		#   self = 4($sp)
		
		# Reserving space for local variables
		addi $sp, $sp, -4
		
		# Allocating Bool 1
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Bool # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 1
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 0($sp) # internal_0 = address of allocated object Int
		
		# Loading return value in $v1
		lw $v1, 0($sp)
		
		# Freeing space for local variables
		addi $sp, $sp, 4
		
		jr $ra
		
	function_rev_at_Nil:
		# Function parameters
		#   $ra = 4($sp)
		#   self = 0($sp)
		
		# Loading return value in $v1
		lw $v1, 0($sp)
		
		jr $ra
		
	function_sort_at_Nil:
		# Function parameters
		#   $ra = 4($sp)
		#   self = 0($sp)
		
		# Loading return value in $v1
		lw $v1, 0($sp)
		
		jr $ra
		
	function_insert_at_Nil:
		# Function parameters
		#   $ra = 12($sp)
		#   self = 8($sp)
		#   i = 4($sp)
		
		# Reserving space for local variables
		addi $sp, $sp, -4
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument self
		lw $t0, 20($sp)
		sw $t0, 4($sp) # Storing self
		
		# Argument i
		lw $t0, 16($sp)
		sw $t0, 0($sp) # Storing i
		
		# Calling function function_rcons_at_Nil
		jal function_rcons_at_Nil
		lw $ra, 8($sp)
		sw $v1, 12($sp) # internal_0 = result of function_rcons_at_Nil
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# Loading return value in $v1
		lw $v1, 0($sp)
		
		# Freeing space for local variables
		addi $sp, $sp, 4
		
		jr $ra
		
	function_rcons_at_Nil:
		# Function parameters
		#   $ra = 16($sp)
		#   self = 12($sp)
		#   i = 8($sp)
		
		# Reserving space for local variables
		addi $sp, $sp, -8
		
		# Allocating Cons
		li $v0, 9
		lw $a0, type_Cons
		syscall
		la $t0, type_Cons # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of th object
		sw $a0, 4($v0) # Setting size in the second word of th object
		sw $v0, 4($sp) # internal_0 = address of allocated object Cons
		
		# Passing function arguments
		addi $sp, $sp, -8 # Reserving space for arguments
		sw $ra, 4($sp) # Storing return address
		
		# Argument internal_0
		lw $t0, 12($sp)
		sw $t0, 0($sp) # Storing internal_0
		
		# Calling function function___init___at_Cons
		jal function___init___at_Cons
		lw $ra, 4($sp)
		sw $v1, 12($sp) # internal_0 = result of function___init___at_Cons
		addi $sp, $sp, 8 # Freeing space for arguments
		
		# Passing function arguments
		addi $sp, $sp, -16 # Reserving space for arguments
		sw $ra, 12($sp) # Storing return address
		
		# Argument internal_0
		lw $t0, 20($sp)
		sw $t0, 8($sp) # Storing internal_0
		
		# Argument i
		lw $t0, 24($sp)
		sw $t0, 4($sp) # Storing i
		
		# Argument self
		lw $t0, 28($sp)
		sw $t0, 0($sp) # Storing self
		
		# Calling function function_init_at_Cons
		jal function_init_at_Cons
		lw $ra, 12($sp)
		sw $v1, 16($sp) # internal_1 = result of function_init_at_Cons
		addi $sp, $sp, 16 # Freeing space for arguments
		
		# Loading return value in $v1
		lw $v1, 0($sp)
		
		# Freeing space for local variables
		addi $sp, $sp, 8
		
		jr $ra
		
	function_print_list_at_Nil:
		# Function parameters
		#   $ra = 8($sp)
		#   self = 4($sp)
		
		# Reserving space for local variables
		addi $sp, $sp, -4
		
		# Allocating Bool 1
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Bool # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 1
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 0($sp) # internal_0 = address of allocated object Int
		
		# Loading return value in $v1
		lw $v1, 0($sp)
		
		# Freeing space for local variables
		addi $sp, $sp, 4
		
		jr $ra
		
	function___init___at_Main:
		# Function parameters
		#   $ra = 8($sp)
		#   self = 4($sp)
		
		# Reserving space for local variables
		addi $sp, $sp, -4
		
		# Allocating NUll to internal_0
		sw $zero, 0($sp) # internal_0 = 0
		
		# Set attribute l of self
		lw $t0, 4($sp) # $t0 = self
		lw $t1, 0($sp) # $t1 = internal_0
		beq $t1, $zero, object_set_attribute_8750086191734
		lw $t2, 0($t1)
		la $t3, type_Int
		la $t4, type_Bool
		addi $t5, $zero, 1
		seq $t6, $t2, $t3
		beq $t6, $t5, int_set_attribute_8750086191734
		seq $t6, $t2, $t4
		beq $t6, $t5, bool_set_attribute_8750086191734
		j object_set_attribute_8750086191734
		int_set_attribute_8750086191734:
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		sw $t3, 0($v0)
		sw $a0, 4($v0)
		lw $t5, 8($t1)
		sw $t5, 8($v0)
		sw $v0, 8($t0) # self.l = internal_0
		j end_set_attribute_8750086191734
		bool_set_attribute_8750086191734:
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		sw $t4, 0($v0)
		sw $a0, 4($v0)
		lw $t5, 8($t1)
		sw $t5, 8($v0)
		sw $v0, 8($t0) # self.l = internal_0
		j end_set_attribute_8750086191734
		object_set_attribute_8750086191734:
		sw $t1, 8($t0) # self.l = internal_0
		end_set_attribute_8750086191734:
		
		# Loading return value in $v1
		lw $v1, 4($sp)
		
		# Freeing space for local variables
		addi $sp, $sp, 4
		
		jr $ra
		
	function_iota_at_Main:
		# Function parameters
		#   $ra = 48($sp)
		#   self = 44($sp)
		#   i = 40($sp)
		
		# Reserving space for local variables
		addi $sp, $sp, -40
		
		# Allocating Nil
		li $v0, 9
		lw $a0, type_Nil
		syscall
		la $t0, type_Nil # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of th object
		sw $a0, 4($v0) # Setting size in the second word of th object
		sw $v0, 36($sp) # internal_0 = address of allocated object Nil
		
		# Passing function arguments
		addi $sp, $sp, -8 # Reserving space for arguments
		sw $ra, 4($sp) # Storing return address
		
		# Argument internal_0
		lw $t0, 44($sp)
		sw $t0, 0($sp) # Storing internal_0
		
		# Calling function function___init___at_Nil
		jal function___init___at_Nil
		lw $ra, 4($sp)
		sw $v1, 44($sp) # internal_0 = result of function___init___at_Nil
		addi $sp, $sp, 8 # Freeing space for arguments
		
		# Set attribute l of self
		lw $t0, 44($sp) # $t0 = self
		lw $t1, 36($sp) # $t1 = internal_0
		beq $t1, $zero, object_set_attribute_8750086191779
		lw $t2, 0($t1)
		la $t3, type_Int
		la $t4, type_Bool
		addi $t5, $zero, 1
		seq $t6, $t2, $t3
		beq $t6, $t5, int_set_attribute_8750086191779
		seq $t6, $t2, $t4
		beq $t6, $t5, bool_set_attribute_8750086191779
		j object_set_attribute_8750086191779
		int_set_attribute_8750086191779:
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		sw $t3, 0($v0)
		sw $a0, 4($v0)
		lw $t5, 8($t1)
		sw $t5, 8($v0)
		sw $v0, 8($t0) # self.l = internal_0
		j end_set_attribute_8750086191779
		bool_set_attribute_8750086191779:
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		sw $t4, 0($v0)
		sw $a0, 4($v0)
		lw $t5, 8($t1)
		sw $t5, 8($v0)
		sw $v0, 8($t0) # self.l = internal_0
		j end_set_attribute_8750086191779
		object_set_attribute_8750086191779:
		sw $t1, 8($t0) # self.l = internal_0
		end_set_attribute_8750086191779:
		
		# Allocating Int 0
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Int # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 0
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 28($sp) # internal_2 = address of allocated object Int
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument j
		lw $t0, 44($sp)
		sw $t0, 4($sp) # Storing j
		
		# Argument internal_2
		lw $t0, 40($sp)
		sw $t0, 0($sp) # Storing internal_2
		
		# Calling function function_assign
		jal function_assign
		lw $ra, 8($sp)
		sw $v1, 44($sp) # j = result of function_assign
		addi $sp, $sp, 12 # Freeing space for arguments
		
		while_start_8750086235432:
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument j
		lw $t0, 44($sp)
		sw $t0, 4($sp) # Storing j
		
		# Argument i
		lw $t0, 52($sp)
		sw $t0, 0($sp) # Storing i
		
		# Calling function function_less_than
		jal function_less_than
		lw $ra, 8($sp)
		sw $v1, 36($sp) # internal_3 = result of function_less_than
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# If internal_3 then goto while_body_8750086235432
		lw $t0, 24($sp) # Loading the address of the condition
		lw $t0, 8($t0) # Loading the value of the condition
		addi $t1, $zero, 1 # Setting the value to 1 for comparison
		beq $t0, $t1, while_body_8750086235432
		
		# Jumping to while_end_8750086235432
		j while_end_8750086235432
		
		while_body_8750086235432:
		
		# Allocating Cons
		li $v0, 9
		lw $a0, type_Cons
		syscall
		la $t0, type_Cons # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of th object
		sw $a0, 4($v0) # Setting size in the second word of th object
		sw $v0, 20($sp) # internal_4 = address of allocated object Cons
		
		# Passing function arguments
		addi $sp, $sp, -8 # Reserving space for arguments
		sw $ra, 4($sp) # Storing return address
		
		# Argument internal_4
		lw $t0, 28($sp)
		sw $t0, 0($sp) # Storing internal_4
		
		# Calling function function___init___at_Cons
		jal function___init___at_Cons
		lw $ra, 4($sp)
		sw $v1, 28($sp) # internal_4 = result of function___init___at_Cons
		addi $sp, $sp, 8 # Freeing space for arguments
		
		# Get attribute l of self
		lw $t0, 44($sp) # Get the address of self
		lw $t1, 8($t0) # Get the attribute 'l' from the instance
		lw $t2, 0($t1)
		la $t3, type_Int
		la $t4, type_Bool
		addi $t5, $zero, 1
		seq $t6, $t2, $t3
		beq $t6, $t5, int_get_attribute_8750086190222
		seq $t6, $t2, $t4
		beq $t6, $t5, bool_get_attribute_8750086190222
		j object_get_attribute_8750086190222
		int_get_attribute_8750086190222:
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		sw $t3, 0($v0)
		sw $a0, 4($v0)
		lw $t5, 8($t1)
		sw $t5, 8($v0)
		sw $v0, 16($sp) # internal_5 = self.l
		j end_get_attribute_8750086190222
		bool_get_attribute_8750086190222:
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		sw $t4, 0($v0)
		sw $a0, 4($v0)
		lw $t5, 8($t1)
		sw $t5, 8($v0)
		sw $v0, 16($sp) # internal_5 = self.l
		j end_get_attribute_8750086190222
		object_get_attribute_8750086190222:
		sw $t1, 16($sp) # internal_5 = l
		end_get_attribute_8750086190222:
		
		# Passing function arguments
		addi $sp, $sp, -16 # Reserving space for arguments
		sw $ra, 12($sp) # Storing return address
		
		# Argument internal_4
		lw $t0, 36($sp)
		sw $t0, 8($sp) # Storing internal_4
		
		# Argument j
		lw $t0, 48($sp)
		sw $t0, 4($sp) # Storing j
		
		# Argument internal_5
		lw $t0, 32($sp)
		sw $t0, 0($sp) # Storing internal_5
		
		# Calling function function_init_at_Cons
		jal function_init_at_Cons
		lw $ra, 12($sp)
		sw $v1, 28($sp) # internal_6 = result of function_init_at_Cons
		addi $sp, $sp, 16 # Freeing space for arguments
		
		# Set attribute l of self
		lw $t0, 44($sp) # $t0 = self
		lw $t1, 12($sp) # $t1 = internal_6
		beq $t1, $zero, object_set_attribute_8750086190171
		lw $t2, 0($t1)
		la $t3, type_Int
		la $t4, type_Bool
		addi $t5, $zero, 1
		seq $t6, $t2, $t3
		beq $t6, $t5, int_set_attribute_8750086190171
		seq $t6, $t2, $t4
		beq $t6, $t5, bool_set_attribute_8750086190171
		j object_set_attribute_8750086190171
		int_set_attribute_8750086190171:
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		sw $t3, 0($v0)
		sw $a0, 4($v0)
		lw $t5, 8($t1)
		sw $t5, 8($v0)
		sw $v0, 8($t0) # self.l = internal_6
		j end_set_attribute_8750086190171
		bool_set_attribute_8750086190171:
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		sw $t4, 0($v0)
		sw $a0, 4($v0)
		lw $t5, 8($t1)
		sw $t5, 8($v0)
		sw $v0, 8($t0) # self.l = internal_6
		j end_set_attribute_8750086190171
		object_set_attribute_8750086190171:
		sw $t1, 8($t0) # self.l = internal_6
		end_set_attribute_8750086190171:
		
		# Allocating Int 1
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		
		la $t0, type_Int # $t0 = address of the type
		sw $t0, 0($v0) # Setting type in the first word of the object
		sw $a0, 4($v0) # Setting size in the second word of the object
		addi $t0, $zero, 1
		sw $t0, 8($v0) # Setting value in the third word of the object
		sw $v0, 8($sp) # internal_7 = address of allocated object Int
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument j
		lw $t0, 44($sp)
		sw $t0, 4($sp) # Storing j
		
		# Argument internal_7
		lw $t0, 20($sp)
		sw $t0, 0($sp) # Storing internal_7
		
		# Calling function function_add
		jal function_add
		lw $ra, 8($sp)
		sw $v1, 16($sp) # internal_8 = result of function_add
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument j
		lw $t0, 44($sp)
		sw $t0, 4($sp) # Storing j
		
		# Argument internal_8
		lw $t0, 16($sp)
		sw $t0, 0($sp) # Storing internal_8
		
		# Calling function function_assign
		jal function_assign
		lw $ra, 8($sp)
		sw $v1, 44($sp) # j = result of function_assign
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# Jumping to while_start_8750086235432
		j while_start_8750086235432
		
		while_end_8750086235432:
		
		# Get attribute l of self
		lw $t0, 44($sp) # Get the address of self
		lw $t1, 8($t0) # Get the attribute 'l' from the instance
		lw $t2, 0($t1)
		la $t3, type_Int
		la $t4, type_Bool
		addi $t5, $zero, 1
		seq $t6, $t2, $t3
		beq $t6, $t5, int_get_attribute_8750086191854
		seq $t6, $t2, $t4
		beq $t6, $t5, bool_get_attribute_8750086191854
		j object_get_attribute_8750086191854
		int_get_attribute_8750086191854:
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		sw $t3, 0($v0)
		sw $a0, 4($v0)
		lw $t5, 8($t1)
		sw $t5, 8($v0)
		sw $v0, 0($sp) # internal_9 = self.l
		j end_get_attribute_8750086191854
		bool_get_attribute_8750086191854:
		li $v0, 9
		addi $a0, $zero, 12
		syscall
		sw $t4, 0($v0)
		sw $a0, 4($v0)
		lw $t5, 8($t1)
		sw $t5, 8($v0)
		sw $v0, 0($sp) # internal_9 = self.l
		j end_get_attribute_8750086191854
		object_get_attribute_8750086191854:
		sw $t1, 0($sp) # internal_9 = l
		end_get_attribute_8750086191854:
		
		# Loading return value in $v1
		lw $v1, 0($sp)
		
		# Freeing space for local variables
		addi $sp, $sp, 40
		
		jr $ra
		
	function_main_at_Main:
		# Function parameters
		#   $ra = 32($sp)
		#   self = 28($sp)
		
		# Reserving space for local variables
		addi $sp, $sp, -28
		
		# Allocating String
		li $v0, 9
		addi $a0, $zero, 35 # $a0 = length of string + 9 for 4 bytes for the type, 4 bytes for the length of the string and 1 byte for null-terminator
		syscall
		
		la $t0, type_String
		sw $t0, 0($v0) # Setting type in the first word of the object
		
		addi $t0, $zero, 35
		sw $t0, 4($v0) # Setting length of the string in the second word of the object
		
		addi $t0, $zero, 72
		sb $t0, 8($v0) # internal_0[0] = 'H'
		
		addi $t0, $zero, 111
		sb $t0, 9($v0) # internal_0[1] = 'o'
		
		addi $t0, $zero, 119
		sb $t0, 10($v0) # internal_0[2] = 'w'
		
		addi $t0, $zero, 32
		sb $t0, 11($v0) # internal_0[3] = ' '
		
		addi $t0, $zero, 109
		sb $t0, 12($v0) # internal_0[4] = 'm'
		
		addi $t0, $zero, 97
		sb $t0, 13($v0) # internal_0[5] = 'a'
		
		addi $t0, $zero, 110
		sb $t0, 14($v0) # internal_0[6] = 'n'
		
		addi $t0, $zero, 121
		sb $t0, 15($v0) # internal_0[7] = 'y'
		
		addi $t0, $zero, 32
		sb $t0, 16($v0) # internal_0[8] = ' '
		
		addi $t0, $zero, 110
		sb $t0, 17($v0) # internal_0[9] = 'n'
		
		addi $t0, $zero, 117
		sb $t0, 18($v0) # internal_0[10] = 'u'
		
		addi $t0, $zero, 109
		sb $t0, 19($v0) # internal_0[11] = 'm'
		
		addi $t0, $zero, 98
		sb $t0, 20($v0) # internal_0[12] = 'b'
		
		addi $t0, $zero, 101
		sb $t0, 21($v0) # internal_0[13] = 'e'
		
		addi $t0, $zero, 114
		sb $t0, 22($v0) # internal_0[14] = 'r'
		
		addi $t0, $zero, 115
		sb $t0, 23($v0) # internal_0[15] = 's'
		
		addi $t0, $zero, 32
		sb $t0, 24($v0) # internal_0[16] = ' '
		
		addi $t0, $zero, 116
		sb $t0, 25($v0) # internal_0[17] = 't'
		
		addi $t0, $zero, 111
		sb $t0, 26($v0) # internal_0[18] = 'o'
		
		addi $t0, $zero, 32
		sb $t0, 27($v0) # internal_0[19] = ' '
		
		addi $t0, $zero, 115
		sb $t0, 28($v0) # internal_0[20] = 's'
		
		addi $t0, $zero, 111
		sb $t0, 29($v0) # internal_0[21] = 'o'
		
		addi $t0, $zero, 114
		sb $t0, 30($v0) # internal_0[22] = 'r'
		
		addi $t0, $zero, 116
		sb $t0, 31($v0) # internal_0[23] = 't'
		
		addi $t0, $zero, 63
		sb $t0, 32($v0) # internal_0[24] = '?'
		
		addi $t0, $zero, 32
		sb $t0, 33($v0) # internal_0[25] = ' '
		
		sb $zero, 34($v0) # Null-terminator at the end of the string
		
		sw $v0, 24($sp) # internal_0 = "How many numbers to sort? "
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument self
		lw $t0, 40($sp)
		sw $t0, 4($sp) # Storing self
		
		# Argument internal_0
		lw $t0, 36($sp)
		sw $t0, 0($sp) # Storing internal_0
		
		# Calling function function_out_string_at_IO
		jal function_out_string_at_IO
		lw $ra, 8($sp)
		sw $v1, 32($sp) # internal_1 = result of function_out_string_at_IO
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# Passing function arguments
		addi $sp, $sp, -8 # Reserving space for arguments
		sw $ra, 4($sp) # Storing return address
		
		# Argument self
		lw $t0, 36($sp)
		sw $t0, 0($sp) # Storing self
		
		# Calling function function_in_int_at_IO
		jal function_in_int_at_IO
		lw $ra, 4($sp)
		sw $v1, 24($sp) # internal_2 = result of function_in_int_at_IO
		addi $sp, $sp, 8 # Freeing space for arguments
		
		# Passing function arguments
		addi $sp, $sp, -12 # Reserving space for arguments
		sw $ra, 8($sp) # Storing return address
		
		# Argument self
		lw $t0, 40($sp)
		sw $t0, 4($sp) # Storing self
		
		# Argument internal_2
		lw $t0, 28($sp)
		sw $t0, 0($sp) # Storing internal_2
		
		# Calling function function_iota_at_Main
		jal function_iota_at_Main
		lw $ra, 8($sp)
		sw $v1, 24($sp) # internal_3 = result of function_iota_at_Main
		addi $sp, $sp, 12 # Freeing space for arguments
		
		# Passing function arguments
		addi $sp, $sp, -8 # Reserving space for arguments
		sw $ra, 4($sp) # Storing return address
		
		# Argument internal_3
		lw $t0, 20($sp)
		sw $t0, 0($sp) # Storing internal_3
		
		# Calling function function_rev_at_List
		jal function_rev_at_List
		lw $ra, 4($sp)
		sw $v1, 16($sp) # internal_4 = result of function_rev_at_List
		addi $sp, $sp, 8 # Freeing space for arguments
		
		# Passing function arguments
		addi $sp, $sp, -8 # Reserving space for arguments
		sw $ra, 4($sp) # Storing return address
		
		# Argument internal_4
		lw $t0, 16($sp)
		sw $t0, 0($sp) # Storing internal_4
		
		# Calling function function_sort_at_List
		jal function_sort_at_List
		lw $ra, 4($sp)
		sw $v1, 12($sp) # internal_5 = result of function_sort_at_List
		addi $sp, $sp, 8 # Freeing space for arguments
		
		# Passing function arguments
		addi $sp, $sp, -8 # Reserving space for arguments
		sw $ra, 4($sp) # Storing return address
		
		# Argument internal_5
		lw $t0, 12($sp)
		sw $t0, 0($sp) # Storing internal_5
		
		# Calling function function_print_list_at_List
		jal function_print_list_at_List
		lw $ra, 4($sp)
		sw $v1, 8($sp) # internal_6 = result of function_print_list_at_List
		addi $sp, $sp, 8 # Freeing space for arguments
		
		# Loading return value in $v1
		lw $v1, 0($sp)
		
		# Freeing space for local variables
		addi $sp, $sp, 28
		
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
		
		