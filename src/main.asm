.data
	type_Object: .word 4
	type_Object_inherits_from: .word 0
	type_Object_attributes: .word 0
	type_Object_name: .asciiz "Object"
	
	type_IO: .word 4
	type_IO_inherits_from: .word type_Object
	type_IO_attributes: .word 0
	type_IO_name: .asciiz "IO"
	
	type_Int: .word 4
	type_Int_inherits_from: .word type_Object
	type_Int_attributes: .word 0
	type_Int_name: .asciiz "Int"
	
	type_String: .word 4
	type_String_inherits_from: .word type_Object
	type_String_attributes: .word 0
	type_String_name: .asciiz "String"
	
	type_Bool: .word 4
	type_Bool_inherits_from: .word type_Object
	type_Bool_attributes: .word 0
	type_Bool_name: .asciiz "Bool"
	
	type_Main: .word 8
	type_Main_inherits_from: .word type_IO
	type_Main_attributes: .word 1
	type_Main_name: .asciiz "Main"
	

.text
	function___init___at_Object:
		# Function parameters
		#   $ra = 4($sp)
		#   self = 0($sp)
		
		# Loading return value in $v1
		lw $v1, 0($sp)
		
		jr $ra
		
	function_abort_at_Object:
		# Function parameters
		#   $ra = 4($sp)
		#   self = 0($sp)
		
		
		jr $ra
		
	function_type_name_at_Object:
		# Function parameters
		#   $ra = 8($sp)
		#   self = 4($sp)
		
		# Reserving space for local variables
		addi $sp, $sp, -4
		
		
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
		
		
		# Loading return value in $v1
		lw $v1, 4($sp)
		
		jr $ra
		
	function_out_int_at_IO:
		# Function parameters
		#   $ra = 8($sp)
		#   self = 4($sp)
		#   x = 0($sp)
		
		
		# Loading return value in $v1
		lw $v1, 4($sp)
		
		jr $ra
		
	function_in_string_at_IO:
		# Function parameters
		#   $ra = 8($sp)
		#   self = 4($sp)
		
		# Reserving space for local variables
		addi $sp, $sp, -4
		
		
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
		#   $ra = 4($sp)
		#   self = 0($sp)
		
		jr $ra
		
	function_plus_at_Main:
		# Function parameters
		#   $ra = 16($sp)
		#   self = 12($sp)
		#   a = 8($sp)
		#   b = 4($sp)
		
		# Reserving space for local variables
		addi $sp, $sp, -4
		
		# addition operation
		lw $t0, 8($sp) # Save in $t0 the left operand
		lw $t1, 4($sp) # Save in $t1 the right operand
		add $t0, $t0, $t1 # $t0 = $t0 + $t1
		sw $t0, 0($sp) # Storing result of addition
		
		# Loading return value in $v1
		lw $v1, 0($sp)
		
		# Freeing space for local variables
		addi $sp, $sp, 4
		
		jr $ra
		
	function_minus_at_Main:
		# Function parameters
		#   $ra = 16($sp)
		#   self = 12($sp)
		#   a = 8($sp)
		#   b = 4($sp)
		
		# Reserving space for local variables
		addi $sp, $sp, -4
		
		# Subtraction operation
		lw $t0, 8($sp) # Save in $t0 the left operand
		lw $t1, 4($sp) # Save in $t1 the right operand
		sub $t0, $t0, $t1 # $t0 = $t0 - $t1
		sw $t0, 0($sp) # Store result of subtraction
		
		# Loading return value in $v1
		lw $v1, 0($sp)
		
		# Freeing space for local variables
		addi $sp, $sp, 4
		
		jr $ra
		
	function_mult_at_Main:
		# Function parameters
		#   $ra = 16($sp)
		#   self = 12($sp)
		#   a = 8($sp)
		#   b = 4($sp)
		
		# Reserving space for local variables
		addi $sp, $sp, -4
		
		# Multiplication operation
		lw $t0, 8($sp) # Save in $t0 the left operand
		lw $t1, 4($sp) # Save in $t1 the right operand
		mult $t0, $t1 # $t0 = $t0 * $t1
		mflo $t0
		sw $t0, 0($sp) # Store result of multiplication
		
		# Loading return value in $v1
		lw $v1, 0($sp)
		
		# Freeing space for local variables
		addi $sp, $sp, 4
		
		jr $ra
		
	function_div_at_Main:
		# Function parameters
		#   $ra = 16($sp)
		#   self = 12($sp)
		#   a = 8($sp)
		#   b = 4($sp)
		
		# Reserving space for local variables
		addi $sp, $sp, -4
		
		# Division operation
		lw $t0, 8($sp) # Save in $t0 the left operand
		lw $t1, 4($sp) # Save in $t1 the right operand
		div $t0, $t1 # $t0 = $t0 / $t1
		mflo $t0
		sw $t0, 0($sp) # Store result of division
		
		# Loading return value in $v1
		lw $v1, 0($sp)
		
		# Freeing space for local variables
		addi $sp, $sp, 4
		
		jr $ra
		
	main: