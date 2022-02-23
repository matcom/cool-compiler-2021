# Genereted MIPS
.text 
__get_ra:
move $v0, $ra
addi $v0, $v0, 8
jr $ra
__copy:
move $t0, $a0
lw $t1, 0($t0)
lw $a0, 4($t1)
li $v0, 9
syscall
move $t1, $a0
srl $t1, $t1, 2
move $t3, $v0
__start_copy_loop:
ble $t1, $zero, __end_copy_loop
lw $t2, 0($t0)
sw $t2, 0($t3)
addi $t0, $t0, 4
addi $t3, $t3, 4
addi $t1, $t1, -1
j __start_copy_loop
__end_copy_loop:
jr $ra
__string_length:
# Actual String address
lw $a0, 4($a0)
# v0 = current length
li $v0, 0
__string_length_start_loop:
lb $t0, 0($a0)
beq $t0, $zero, __string_length_end_loop
addi $v0, $v0, 1
addi $a0, $a0, 1
j __string_length_start_loop
__string_length_end_loop:
jr $ra
__string_substring:
# Save arguments
addi $sp, $sp, -16
# Save arguments
sw $a0, 0($sp)
# Save arguments
sw $a1, 4($sp)
# Save arguments
sw $a2, 8($sp)
# Save arguments
sw $ra, 12($sp)
# $v0 = length of string
jal __string_length
# Restore arguments
lw $a0, 0($sp)
# Restore arguments
lw $a1, 4($sp)
# Restore arguments
lw $a2, 8($sp)
# Restore arguments
lw $ra, 12($sp)
# Restore arguments
addi $sp, $sp, 16
# Actual String address
lw $a0, 4($a0)
# If index >= length(string) then abort
bge $a1, $v0, __string_substring_abort
# t0 = index + length
add $t0, $a1, $a2
# If index + length >= length(string) then abort
bgt $t0, $v0, __string_substring_abort
# If 0 < 0 then abort
blt $a2, $zero, __string_substring_abort
# Saving the string address
move $t1, $a0
# a0 = length + 1. Extra space for null character
addi $a0, $a2, 1
li $v0, 9
syscall
# Saving the new string address
move $t2, $v0
# Removing the last null space from copy
addi $a0, $a0, -1
# Advance index positions in original string
add $t1, $t1, $a1
__string_substring_start_copy:
ble $a0, $zero, __string_substring_end_copy
lb $t3, 0($t1)
sb $t3, 0($t2)
addi $t1, $t1, 1
addi $t2, $t2, 1
addi $a0, $a0, -1
j __string_substring_start_copy
__string_substring_end_copy:
# Saving String Address
move $v1, $v0
# Type address into $a0
la $t0, String
# If String the is type and address
li $a0, 8
li $v0, 9
syscall
# Store String Type
sw $t0, 0($v0)
# Store String Address
sw $v1, 4($v0)
# Return the address of the new String
jr $ra
__string_substring_abort:
addi $v0, $zero, 10
syscall
__type_name:
# $t0 = type name address
lw $t0, 8($a0)
# Type address into $a0
la $t1, String
# If String the is type and address
li $a0, 8
li $v0, 9
syscall
# Store String Type
sw $t1, 0($v0)
# Store String Address
sw $t0, 4($v0)
# Return the address of the String
jr $ra
__concat:
addi $sp, $sp, -12
sw $a0, 0($sp)
sw $a1, 4($sp)
sw $ra, 8($sp)
jal __string_length
lw $a0, 0($sp)
lw $a1, 4($sp)
lw $ra, 8($sp)
addi $sp, $sp, 12
move $t1, $a0
move $a0, $a1
move $a1, $t1
move $t0, $v0
addi $sp, $sp, -16
sw $a0, 0($sp)
sw $a1, 4($sp)
sw $t0, 8($sp)
sw $ra, 12($sp)
jal __string_length
lw $a0, 0($sp)
lw $a1, 4($sp)
lw $t0, 8($sp)
lw $ra, 12($sp)
addi $sp, $sp, 16
move $t1, $a0
move $a0, $a1
move $a1, $t1
lw $a0, 4($a0)
lw $a1, 4($a1)
move $t1, $a0
add $t2, $v0, $t0
addi $a0, $t2, 1
move $t2, $v0
li $v0, 9
syscall
# Save string address
move $v1, $v0
__concat_string1_copy_start_copy:
ble $t0, $zero, __concat_string1_copy_end_copy
lb $t3, 0($t1)
sb $t3, 0($v1)
addi $t1, $t1, 1
addi $v1, $v1, 1
addi $t0, $t0, -1
j __concat_string1_copy_start_copy
__concat_string1_copy_end_copy:
__concat_string2_copy_start_copy:
ble $t2, $zero, __concat_string2_copy_end_copy
lb $t3, 0($a1)
sb $t3, 0($v1)
addi $a1, $a1, 1
addi $v1, $v1, 1
addi $t2, $t2, -1
j __concat_string2_copy_start_copy
__concat_string2_copy_end_copy:
sb $zero, 0($v1)
# Save string address
move $v1, $v0
# Type address into $a0
la $t0, String
# If String the is type and address
li $a0, 8
li $v0, 9
syscall
# Store String Type
sw $t0, 0($v0)
# Store String Address
sw $v1, 4($v0)
# Returns the concatenated string instance in v0
jr $ra
__string_equal:
# Actual String address
lw $t0, 4($a0)
# Actual String address
lw $t1, 4($a1)
__string_equal_start_loop:
# Load string1 char
lb $t2, 0($t0)
# Load string2 char
lb $t3, 0($t1)
# Equal chars?
seq $t4, $t2, $t3
# If not equal then
beq $t4, $zero, __string_equal_end_loop
# Both strings ended
beq $t2, $zero, __string_equal_end_loop
# Next char
addi $t0, $t0, 1
# Next char
addi $t1, $t1, 1
j __string_equal_start_loop
__string_equal_end_loop:
# Assign return value
move $v0, $t4
jr $ra
__object_equal:
# Compare obj by address
seq $v0, $a0, $a1
# Equal Address or Value obj are equal
bne $v0, $zero, __object_equal_end
# t0 = left object
move $t0, $a0
# t1 = right object
move $t1, $a1
# t0=left objType
lw $t0, 0($t0)
# t1=right objType
lw $t1, 0($t1)
# Loading String type address for comparison
la $t2, String
# t0 = left type == String
seq $t0, $t0, $t2
# t1 = right type == String
seq $t1, $t1, $t2
# Both types are equal to String
and $t0, $t0, $t1
# If not equal return 0
beq $t0, $zero, __object_equal_label
addi $sp, $sp, -12
sw $ra, 0($sp)
sw $a0, 4($sp)
sw $a1, 8($sp)
jal __string_equal
lw $ra, 0($sp)
lw $a0, 4($sp)
lw $a1, 8($sp)
addi $sp, $sp, 12
j __object_equal_end
# Do Obj cmp
__object_equal_label:
# Not equal objects
move $v0, $zero
# End cmp
__object_equal_end:
jr $ra
# Remove Final Char
__remove_last_char:
# Actual String address
lw $t0, 4($a0)
# Initial loop
__remove_last_char_start:
# Get current char
lb $t1, 0($t0)
# if char is null then break
beq $t1, $zero, __remove_last_char_end
# Increment address
addi $t0, $t0, 1
j __remove_last_char_start
# End loop, removing last char
__remove_last_char_end:
# Back one char to last one
addi $t0, $t0, -1
# Store null character
sb $zero, 0($t0)
jr $ra
# Program Node
main:
# Program Node
addi $sp, $sp, -12
# Program Node
move $t0, $sp
# Program Node
addi $sp, $sp, -8
# Program Node
sw $ra, 0($sp)
# Program Node
sw $fp, 4($sp)
# Program Node
move $fp, $t0
# Instantiate Node
la $a0, Main
# Instantiate Node
lw $a0, 4($a0)
li $v0, 9
syscall
sw $v0, 8($fp)
# Instantiate Node
lw $t0, 8($fp)
# Instantiate Node
addi $sp, $sp, -4
# Instantiate Node
sw $t0, 0($sp)
# Instantiate Node
jal __init_Main_type
# Instantiate Node
sw $v0, 8($fp)
lw $t0, 8($fp)
addi $sp, $sp, -4
sw $t0, 0($sp)
# Program Node
jal function_main_at_Main
# Program Node
sw $v0, 4($fp)
# Program Node
li $v0, 0
# Program Node
lw $ra, 0($sp)
# Program Node
lw $fp, 4($sp)
# Program Node
addi $sp, $sp, 8
# Program Node
addi $sp, $sp, 12
# Program Node
jr $ra
# Program Node
type_distance:
# Program Node
addi $sp, $sp, -16
# Program Node
move $t0, $sp
# Program Node
addi $sp, $sp, -8
# Program Node
sw $ra, 0($sp)
# Program Node
sw $fp, 4($sp)
# Program Node
move $fp, $t0
# Program Node
sw $zero, 12($fp)
# Program Node
li $t0, 0
# Program Node
sw $t0, 0($fp)
# Program Node
distance_label_0:
# Program Node
lw $t0, 20($fp)
# Program Node
lw $t1, 16($fp)
# Program Node
seq $t2, $t0, $t1
# Program Node
sw $t2, 4($fp)
# Program Node
lw $t0, 4($fp)
# Program Node
bne $t0, $zero, distance_label_1
# Program Node
lw $t0, 20($fp)
# Program Node
lw $t0, 0($t0)
# Program Node
sw $t0, 20($fp)
# Program Node
lw $t0, 20($fp)
# Program Node
lw $t1, 12($fp)
# Program Node
seq $t2, $t0, $t1
# Program Node
sw $t2, 8($fp)
# Program Node
lw $t0, 8($fp)
# Program Node
bne $t0, $zero, distance_label_2
# Program Node
lw $t0, 0($fp)
# Program Node
li $t1, 1
# Program Node
add $t2, $t0, $t1
# Program Node
sw $t2, 0($fp)
# Program Node
j distance_label_0
# Program Node
distance_label_2:
# Program Node
li $t0, -1
# Program Node
sw $t0, 0($fp)
# Program Node
distance_label_1:
# Program Node
lw $v0, 0($fp)
# Program Node
lw $ra, 0($sp)
# Program Node
lw $fp, 4($sp)
# Program Node
addi $sp, $sp, 8
# Program Node
addi $sp, $sp, 24
# Program Node
jr $ra
# Program Node
function_length_at_String:
# Program Node
addi $sp, $sp, -4
# Program Node
move $t0, $sp
# Program Node
addi $sp, $sp, -8
# Program Node
sw $ra, 0($sp)
# Program Node
sw $fp, 4($sp)
# Program Node
move $fp, $t0
# String Length Node
lw $a0, 4($fp)
# String Length Node
jal __string_length
# String Length Node
sw $v0, 0($fp)
# Func Declaration Node
lw $v0, 0($fp)
# Program Node
lw $ra, 0($sp)
# Program Node
lw $fp, 4($sp)
# Program Node
addi $sp, $sp, 8
# Program Node
addi $sp, $sp, 8
# Program Node
jr $ra
# Program Node
function_concat_at_String:
# Program Node
addi $sp, $sp, -4
# Program Node
move $t0, $sp
# Program Node
addi $sp, $sp, -8
# Program Node
sw $ra, 0($sp)
# Program Node
sw $fp, 4($sp)
# Program Node
move $fp, $t0
# String Concat Node
lw $a0, 8($fp)
# String Concat Node
lw $a1, 4($fp)
# String Concat Node
jal __concat
# String Concat Node
sw $v0, 0($fp)
# Func Declaration Node
lw $v0, 0($fp)
# Program Node
lw $ra, 0($sp)
# Program Node
lw $fp, 4($sp)
# Program Node
addi $sp, $sp, 8
# Program Node
addi $sp, $sp, 12
# Program Node
jr $ra
# Program Node
function_substr_at_String:
# Program Node
addi $sp, $sp, -4
# Program Node
move $t0, $sp
# Program Node
addi $sp, $sp, -8
# Program Node
sw $ra, 0($sp)
# Program Node
sw $fp, 4($sp)
# Program Node
move $fp, $t0
# String Substring Node
lw $a0, 12($fp)
# String Substring Node
lw $a1, 8($fp)
# String Substring Node
lw $a2, 4($fp)
# String Substring Node
jal __string_substring
# String Substring Node
sw $v0, 0($fp)
# Func Declaration Node
lw $v0, 0($fp)
# Program Node
lw $ra, 0($sp)
# Program Node
lw $fp, 4($sp)
# Program Node
addi $sp, $sp, 8
# Program Node
addi $sp, $sp, 16
# Program Node
jr $ra
# Program Node
function_abort_at_Bool:
# Program Node
addi $sp, $sp, -12
# Program Node
move $t0, $sp
# Program Node
addi $sp, $sp, -8
# Program Node
sw $ra, 0($sp)
# Program Node
sw $fp, 4($sp)
# Program Node
move $fp, $t0
la $t0, data_2
# Type address into $a0
la $t1, String
# If String the is type and address
li $a0, 8
li $v0, 9
syscall
# Store String Type
sw $t1, 0($v0)
# Store String Address
sw $t0, 4($v0)
# Save string instance
sw $v0, 0($fp)
la $t0, data_12
# Type address into $a0
la $t1, String
# If String the is type and address
li $a0, 8
li $v0, 9
syscall
# Store String Type
sw $t1, 0($v0)
# Store String Address
sw $t0, 4($v0)
# Save string instance
sw $v0, 4($fp)
# Final abort message
lw $a0, 4($fp)
# Final abort message
lw $a1, 0($fp)
# Final abort message
jal __concat
# Final abort message
sw $v0, 8($fp)
# Print abort info
lw $a0, 8($fp)
# Getting the String address
lw $a0, 4($a0)
# 4 System call code for print string
addi $v0, $zero, 4
syscall
# Object Abort Node Bool
addi $v0, $zero, 10
# Object Abort Node Bool
syscall
# Func Declaration Node
li $v0, 0
# Program Node
lw $ra, 0($sp)
# Program Node
lw $fp, 4($sp)
# Program Node
addi $sp, $sp, 8
# Program Node
addi $sp, $sp, 16
# Program Node
jr $ra
# Program Node
function_type_name_at_Bool:
# Program Node
addi $sp, $sp, -4
# Program Node
move $t0, $sp
# Program Node
addi $sp, $sp, -8
# Program Node
sw $ra, 0($sp)
# Program Node
sw $fp, 4($sp)
# Program Node
move $fp, $t0
la $t0, data_2
# Type address into $a0
la $t1, String
# If String the is type and address
li $a0, 8
li $v0, 9
syscall
# Store String Type
sw $t1, 0($v0)
# Store String Address
sw $t0, 4($v0)
# Save string instance
sw $v0, 0($fp)
# Func Declaration Node
lw $v0, 0($fp)
# Program Node
lw $ra, 0($sp)
# Program Node
lw $fp, 4($sp)
# Program Node
addi $sp, $sp, 8
# Program Node
addi $sp, $sp, 8
# Program Node
jr $ra
# Program Node
function_abort_at_Int:
# Program Node
addi $sp, $sp, -12
# Program Node
move $t0, $sp
# Program Node
addi $sp, $sp, -8
# Program Node
sw $ra, 0($sp)
# Program Node
sw $fp, 4($sp)
# Program Node
move $fp, $t0
la $t0, data_3
# Type address into $a0
la $t1, String
# If String the is type and address
li $a0, 8
li $v0, 9
syscall
# Store String Type
sw $t1, 0($v0)
# Store String Address
sw $t0, 4($v0)
# Save string instance
sw $v0, 0($fp)
la $t0, data_12
# Type address into $a0
la $t1, String
# If String the is type and address
li $a0, 8
li $v0, 9
syscall
# Store String Type
sw $t1, 0($v0)
# Store String Address
sw $t0, 4($v0)
# Save string instance
sw $v0, 4($fp)
# Final abort message
lw $a0, 4($fp)
# Final abort message
lw $a1, 0($fp)
# Final abort message
jal __concat
# Final abort message
sw $v0, 8($fp)
# Print abort info
lw $a0, 8($fp)
# Getting the String address
lw $a0, 4($a0)
# 4 System call code for print string
addi $v0, $zero, 4
syscall
# Object Abort Node Int
addi $v0, $zero, 10
# Object Abort Node Int
syscall
# Func Declaration Node
li $v0, 0
# Program Node
lw $ra, 0($sp)
# Program Node
lw $fp, 4($sp)
# Program Node
addi $sp, $sp, 8
# Program Node
addi $sp, $sp, 16
# Program Node
jr $ra
# Program Node
function_type_name_at_Int:
# Program Node
addi $sp, $sp, -4
# Program Node
move $t0, $sp
# Program Node
addi $sp, $sp, -8
# Program Node
sw $ra, 0($sp)
# Program Node
sw $fp, 4($sp)
# Program Node
move $fp, $t0
la $t0, data_3
# Type address into $a0
la $t1, String
# If String the is type and address
li $a0, 8
li $v0, 9
syscall
# Store String Type
sw $t1, 0($v0)
# Store String Address
sw $t0, 4($v0)
# Save string instance
sw $v0, 0($fp)
# Func Declaration Node
lw $v0, 0($fp)
# Program Node
lw $ra, 0($sp)
# Program Node
lw $fp, 4($sp)
# Program Node
addi $sp, $sp, 8
# Program Node
addi $sp, $sp, 8
# Program Node
jr $ra
# Program Node
function_method6_at_C:
# Program Node
addi $sp, $sp, -24
# Program Node
move $t0, $sp
# Program Node
addi $sp, $sp, -8
# Program Node
sw $ra, 0($sp)
# Program Node
sw $fp, 4($sp)
# Program Node
move $fp, $t0
# Var Declaration Node
li $t0, 0
# Var Declaration Node
sw $t0, 0($fp)
# Roof Node
li $t0, 0
# Roof Node
lw $t1, 24($fp)
# Roof Node
sub $t2, $t0, $t1
# Roof Node
sw $t2, 8($fp)
# Assign Node
lw $t0, 8($fp)
# Assign Node
sw $t0, 0($fp)
# Instantiate Node
la $a0, A
# Instantiate Node
lw $a0, 4($a0)
li $v0, 9
syscall
sw $v0, 12($fp)
# Instantiate Node
lw $t0, 12($fp)
# Instantiate Node
addi $sp, $sp, -4
# Instantiate Node
sw $t0, 0($sp)
# Instantiate Node
jal __init_A_type
# Instantiate Node
sw $v0, 12($fp)
# Call Node
lw $t0, 12($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 0($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 12($fp)
# Call Node
lw $t0, 0($t0)
# Call Node
sw $t0, 20($fp)
# Call Node
lw $t0, 20($fp)
# Call Node
lw $t0, 36($t0)
# Call Node
jal __get_ra
# Call Node
move $ra, $v0
# Call Node
jr $t0
# Call Node
sw $v0, 16($fp)
# Func Declaration Node
lw $v0, 16($fp)
# Program Node
lw $ra, 0($sp)
# Program Node
lw $fp, 4($sp)
# Program Node
addi $sp, $sp, 8
# Program Node
addi $sp, $sp, 32
# Program Node
jr $ra
# Program Node
function_method5_at_C:
# Program Node
addi $sp, $sp, -28
# Program Node
move $t0, $sp
# Program Node
addi $sp, $sp, -8
# Program Node
sw $ra, 0($sp)
# Program Node
sw $fp, 4($sp)
# Program Node
move $fp, $t0
# Var Declaration Node
li $t0, 0
# Var Declaration Node
sw $t0, 0($fp)
# Star Node
lw $t0, 28($fp)
# Star Node
lw $t1, 28($fp)
# Star Node
mul $t2, $t0, $t1
# Star Node
sw $t2, 8($fp)
# Star Node
lw $t0, 8($fp)
# Star Node
lw $t1, 28($fp)
# Star Node
mul $t2, $t0, $t1
# Star Node
sw $t2, 12($fp)
# Assign Node
lw $t0, 12($fp)
# Assign Node
sw $t0, 0($fp)
# Instantiate Node
la $a0, E
# Instantiate Node
lw $a0, 4($a0)
li $v0, 9
syscall
sw $v0, 16($fp)
# Instantiate Node
lw $t0, 16($fp)
# Instantiate Node
addi $sp, $sp, -4
# Instantiate Node
sw $t0, 0($sp)
# Instantiate Node
jal __init_E_type
# Instantiate Node
sw $v0, 16($fp)
# Call Node
lw $t0, 16($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 0($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 16($fp)
# Call Node
lw $t0, 0($t0)
# Call Node
sw $t0, 24($fp)
# Call Node
lw $t0, 24($fp)
# Call Node
lw $t0, 36($t0)
# Call Node
jal __get_ra
# Call Node
move $ra, $v0
# Call Node
jr $t0
# Call Node
sw $v0, 20($fp)
# Func Declaration Node
lw $v0, 20($fp)
# Program Node
lw $ra, 0($sp)
# Program Node
lw $fp, 4($sp)
# Program Node
addi $sp, $sp, 8
# Program Node
addi $sp, $sp, 36
# Program Node
jr $ra
# Init var at A
__init_var_at_A:
# Init var at A
addi $sp, $sp, 0
# Init var at A
move $t0, $sp
# Init var at A
addi $sp, $sp, -8
# Init var at A
sw $ra, 0($sp)
# Init var at A
sw $fp, 4($sp)
# Init var at A
move $fp, $t0
# Attr Declaration Node
lw $t0, 0($fp)
# Attr Declaration Node
li $t1, 0
# Attr Declaration Node
sw $t1, 4($t0)
# Init var at A
lw $ra, 0($sp)
# Init var at A
lw $fp, 4($sp)
# Init var at A
addi $sp, $sp, 8
# Init var at A
addi $sp, $sp, 4
# Init var at A
jr $ra
# Program Node
function_value_at_A:
# Program Node
addi $sp, $sp, -4
# Program Node
move $t0, $sp
# Program Node
addi $sp, $sp, -8
# Program Node
sw $ra, 0($sp)
# Program Node
sw $fp, 4($sp)
# Program Node
move $fp, $t0
# Variable Node
lw $t0, 4($fp)
# Variable Node
lw $t0, 4($t0)
# Variable Node
sw $t0, 0($fp)
# Func Declaration Node
lw $v0, 0($fp)
# Program Node
lw $ra, 0($sp)
# Program Node
lw $fp, 4($sp)
# Program Node
addi $sp, $sp, 8
# Program Node
addi $sp, $sp, 8
# Program Node
jr $ra
# Program Node
function_set_var_at_A:
# Program Node
addi $sp, $sp, -4
# Program Node
move $t0, $sp
# Program Node
addi $sp, $sp, -8
# Program Node
sw $ra, 0($sp)
# Program Node
sw $fp, 4($sp)
# Program Node
move $fp, $t0
# Assign Node
lw $t0, 8($fp)
# Assign Node
lw $t1, 4($fp)
# Assign Node
sw $t1, 4($t0)
# Func Declaration Node
lw $v0, 8($fp)
# Program Node
lw $ra, 0($sp)
# Program Node
lw $fp, 4($sp)
# Program Node
addi $sp, $sp, 8
# Program Node
addi $sp, $sp, 12
# Program Node
jr $ra
# Program Node
function_method1_at_A:
# Program Node
addi $sp, $sp, 0
# Program Node
move $t0, $sp
# Program Node
addi $sp, $sp, -8
# Program Node
sw $ra, 0($sp)
# Program Node
sw $fp, 4($sp)
# Program Node
move $fp, $t0
# Func Declaration Node
lw $v0, 4($fp)
# Program Node
lw $ra, 0($sp)
# Program Node
lw $fp, 4($sp)
# Program Node
addi $sp, $sp, 8
# Program Node
addi $sp, $sp, 8
# Program Node
jr $ra
# Program Node
function_method2_at_A:
# Program Node
addi $sp, $sp, -24
# Program Node
move $t0, $sp
# Program Node
addi $sp, $sp, -8
# Program Node
sw $ra, 0($sp)
# Program Node
sw $fp, 4($sp)
# Program Node
move $fp, $t0
# Var Declaration Node
li $t0, 0
# Var Declaration Node
sw $t0, 0($fp)
# Plus Node
lw $t0, 28($fp)
# Plus Node
lw $t1, 24($fp)
# Plus Node
add $t2, $t0, $t1
# Plus Node
sw $t2, 8($fp)
# Assign Node
lw $t0, 8($fp)
# Assign Node
sw $t0, 0($fp)
# Instantiate Node
la $a0, B
# Instantiate Node
lw $a0, 4($a0)
li $v0, 9
syscall
sw $v0, 12($fp)
# Instantiate Node
lw $t0, 12($fp)
# Instantiate Node
addi $sp, $sp, -4
# Instantiate Node
sw $t0, 0($sp)
# Instantiate Node
jal __init_B_type
# Instantiate Node
sw $v0, 12($fp)
# Call Node
lw $t0, 12($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 0($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 12($fp)
# Call Node
lw $t0, 0($t0)
# Call Node
sw $t0, 20($fp)
# Call Node
lw $t0, 20($fp)
# Call Node
lw $t0, 36($t0)
# Call Node
jal __get_ra
# Call Node
move $ra, $v0
# Call Node
jr $t0
# Call Node
sw $v0, 16($fp)
# Func Declaration Node
lw $v0, 16($fp)
# Program Node
lw $ra, 0($sp)
# Program Node
lw $fp, 4($sp)
# Program Node
addi $sp, $sp, 8
# Program Node
addi $sp, $sp, 36
# Program Node
jr $ra
# Program Node
function_method3_at_A:
# Program Node
addi $sp, $sp, -24
# Program Node
move $t0, $sp
# Program Node
addi $sp, $sp, -8
# Program Node
sw $ra, 0($sp)
# Program Node
sw $fp, 4($sp)
# Program Node
move $fp, $t0
# Var Declaration Node
li $t0, 0
# Var Declaration Node
sw $t0, 0($fp)
# Roof Node
li $t0, 0
# Roof Node
lw $t1, 24($fp)
# Roof Node
sub $t2, $t0, $t1
# Roof Node
sw $t2, 8($fp)
# Assign Node
lw $t0, 8($fp)
# Assign Node
sw $t0, 0($fp)
# Instantiate Node
la $a0, C
# Instantiate Node
lw $a0, 4($a0)
li $v0, 9
syscall
sw $v0, 12($fp)
# Instantiate Node
lw $t0, 12($fp)
# Instantiate Node
addi $sp, $sp, -4
# Instantiate Node
sw $t0, 0($sp)
# Instantiate Node
jal __init_C_type
# Instantiate Node
sw $v0, 12($fp)
# Call Node
lw $t0, 12($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 0($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 12($fp)
# Call Node
lw $t0, 0($t0)
# Call Node
sw $t0, 20($fp)
# Call Node
lw $t0, 20($fp)
# Call Node
lw $t0, 36($t0)
# Call Node
jal __get_ra
# Call Node
move $ra, $v0
# Call Node
jr $t0
# Call Node
sw $v0, 16($fp)
# Func Declaration Node
lw $v0, 16($fp)
# Program Node
lw $ra, 0($sp)
# Program Node
lw $fp, 4($sp)
# Program Node
addi $sp, $sp, 8
# Program Node
addi $sp, $sp, 32
# Program Node
jr $ra
# Program Node
function_method4_at_A:
# Program Node
addi $sp, $sp, -56
# Program Node
move $t0, $sp
# Program Node
addi $sp, $sp, -8
# Program Node
sw $ra, 0($sp)
# Program Node
sw $fp, 4($sp)
# Program Node
move $fp, $t0
# Lesser Node
lw $t0, 56($fp)
# Lesser Node
lw $t1, 60($fp)
# Lesser Node
slt $t2, $t0, $t1
# Lesser Node
sw $t2, 4($fp)
# Conditional Node
lw $t0, 4($fp)
# Conditional Node
bne $t0, $zero, method4_at_A_label_0
# Var Declaration Node
li $t0, 0
# Var Declaration Node
sw $t0, 8($fp)
# Minus Node
lw $t0, 56($fp)
# Minus Node
lw $t1, 60($fp)
# Minus Node
sub $t2, $t0, $t1
# Minus Node
sw $t2, 16($fp)
# Assign Node
lw $t0, 16($fp)
# Assign Node
sw $t0, 8($fp)
# Instantiate Node
la $a0, D
# Instantiate Node
lw $a0, 4($a0)
li $v0, 9
syscall
sw $v0, 20($fp)
# Instantiate Node
lw $t0, 20($fp)
# Instantiate Node
addi $sp, $sp, -4
# Instantiate Node
sw $t0, 0($sp)
# Instantiate Node
jal __init_D_type
# Instantiate Node
sw $v0, 20($fp)
# Call Node
lw $t0, 20($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 8($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 20($fp)
# Call Node
lw $t0, 0($t0)
# Call Node
sw $t0, 28($fp)
# Call Node
lw $t0, 28($fp)
# Call Node
lw $t0, 36($t0)
# Call Node
jal __get_ra
# Call Node
move $ra, $v0
# Call Node
jr $t0
# Call Node
sw $v0, 24($fp)
# Conditional Node
lw $t0, 24($fp)
# Conditional Node
sw $t0, 0($fp)
# Conditional Node
j method4_at_A_label_1
# Conditional Node
method4_at_A_label_0:
# Var Declaration Node
li $t0, 0
# Var Declaration Node
sw $t0, 32($fp)
# Minus Node
lw $t0, 60($fp)
# Minus Node
lw $t1, 56($fp)
# Minus Node
sub $t2, $t0, $t1
# Minus Node
sw $t2, 40($fp)
# Assign Node
lw $t0, 40($fp)
# Assign Node
sw $t0, 32($fp)
# Instantiate Node
la $a0, D
# Instantiate Node
lw $a0, 4($a0)
li $v0, 9
syscall
sw $v0, 44($fp)
# Instantiate Node
lw $t0, 44($fp)
# Instantiate Node
addi $sp, $sp, -4
# Instantiate Node
sw $t0, 0($sp)
# Instantiate Node
jal __init_D_type
# Instantiate Node
sw $v0, 44($fp)
# Call Node
lw $t0, 44($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 32($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 44($fp)
# Call Node
lw $t0, 0($t0)
# Call Node
sw $t0, 52($fp)
# Call Node
lw $t0, 52($fp)
# Call Node
lw $t0, 36($t0)
# Call Node
jal __get_ra
# Call Node
move $ra, $v0
# Call Node
jr $t0
# Call Node
sw $v0, 48($fp)
# Conditional Node
lw $t0, 48($fp)
# Conditional Node
sw $t0, 0($fp)
# Conditional Node
method4_at_A_label_1:
# Func Declaration Node
lw $v0, 0($fp)
# Program Node
lw $ra, 0($sp)
# Program Node
lw $fp, 4($sp)
# Program Node
addi $sp, $sp, 8
# Program Node
addi $sp, $sp, 68
# Program Node
jr $ra
# Program Node
function_method5_at_A:
# Program Node
addi $sp, $sp, -44
# Program Node
move $t0, $sp
# Program Node
addi $sp, $sp, -8
# Program Node
sw $ra, 0($sp)
# Program Node
sw $fp, 4($sp)
# Program Node
move $fp, $t0
# Var Declaration Node
li $t0, 1
# Var Declaration Node
sw $t0, 0($fp)
# Var Declaration Node
li $t0, 1
# Var Declaration Node
sw $t0, 8($fp)
# Void Node
sw $zero, 12($fp)
# While Node
method5_at_A_label_0:
# LesserEqual Node
lw $t0, 8($fp)
# LesserEqual Node
lw $t1, 44($fp)
# LesserEqual Node
sgt $t2, $t0, $t1
# LesserEqual Node
sw $t2, 16($fp)
# LesserEqual Node
lw $t0, 16($fp)
# LesserEqual Node
seq $t0, $t0, $zero
# LesserEqual Node
sw $t0, 16($fp)
# While Node
lw $t0, 16($fp)
# While Node
bne $t0, $zero, method5_at_A_label_1
# While Node
j method5_at_A_label_2
# While Node
method5_at_A_label_1:
# Star Node
lw $t0, 0($fp)
# Star Node
lw $t1, 8($fp)
# Star Node
mul $t2, $t0, $t1
# Star Node
sw $t2, 24($fp)
# Assign Node
lw $t0, 24($fp)
# Assign Node
sw $t0, 0($fp)
# Plus Node
lw $t0, 8($fp)
# Plus Node
li $t1, 1
# Plus Node
add $t2, $t0, $t1
# Plus Node
sw $t2, 28($fp)
# Assign Node
lw $t0, 28($fp)
# Assign Node
sw $t0, 8($fp)
# While Node
j method5_at_A_label_0
# While Node
method5_at_A_label_2:
# Instantiate Node
la $a0, E
# Instantiate Node
lw $a0, 4($a0)
li $v0, 9
syscall
sw $v0, 32($fp)
# Instantiate Node
lw $t0, 32($fp)
# Instantiate Node
addi $sp, $sp, -4
# Instantiate Node
sw $t0, 0($sp)
# Instantiate Node
jal __init_E_type
# Instantiate Node
sw $v0, 32($fp)
# Call Node
lw $t0, 32($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 0($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 32($fp)
# Call Node
lw $t0, 0($t0)
# Call Node
sw $t0, 40($fp)
# Call Node
lw $t0, 40($fp)
# Call Node
lw $t0, 36($t0)
# Call Node
jal __get_ra
# Call Node
move $ra, $v0
# Call Node
jr $t0
# Call Node
sw $v0, 36($fp)
# Func Declaration Node
lw $v0, 36($fp)
# Program Node
lw $ra, 0($sp)
# Program Node
lw $fp, 4($sp)
# Program Node
addi $sp, $sp, 8
# Program Node
addi $sp, $sp, 52
# Program Node
jr $ra
# Program Node
function_method5_at_B:
# Program Node
addi $sp, $sp, -24
# Program Node
move $t0, $sp
# Program Node
addi $sp, $sp, -8
# Program Node
sw $ra, 0($sp)
# Program Node
sw $fp, 4($sp)
# Program Node
move $fp, $t0
# Var Declaration Node
li $t0, 0
# Var Declaration Node
sw $t0, 0($fp)
# Star Node
lw $t0, 24($fp)
# Star Node
lw $t1, 24($fp)
# Star Node
mul $t2, $t0, $t1
# Star Node
sw $t2, 8($fp)
# Assign Node
lw $t0, 8($fp)
# Assign Node
sw $t0, 0($fp)
# Instantiate Node
la $a0, E
# Instantiate Node
lw $a0, 4($a0)
li $v0, 9
syscall
sw $v0, 12($fp)
# Instantiate Node
lw $t0, 12($fp)
# Instantiate Node
addi $sp, $sp, -4
# Instantiate Node
sw $t0, 0($sp)
# Instantiate Node
jal __init_E_type
# Instantiate Node
sw $v0, 12($fp)
# Call Node
lw $t0, 12($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 0($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 12($fp)
# Call Node
lw $t0, 0($t0)
# Call Node
sw $t0, 20($fp)
# Call Node
lw $t0, 20($fp)
# Call Node
lw $t0, 36($t0)
# Call Node
jal __get_ra
# Call Node
move $ra, $v0
# Call Node
jr $t0
# Call Node
sw $v0, 16($fp)
# Func Declaration Node
lw $v0, 16($fp)
# Program Node
lw $ra, 0($sp)
# Program Node
lw $fp, 4($sp)
# Program Node
addi $sp, $sp, 8
# Program Node
addi $sp, $sp, 32
# Program Node
jr $ra
# Program Node
function_method7_at_D:
# Program Node
addi $sp, $sp, -60
# Program Node
move $t0, $sp
# Program Node
addi $sp, $sp, -8
# Program Node
sw $ra, 0($sp)
# Program Node
sw $fp, 4($sp)
# Program Node
move $fp, $t0
# Var Declaration Node
lw $t0, 60($fp)
# Var Declaration Node
sw $t0, 0($fp)
# Lesser Node
lw $t0, 0($fp)
# Lesser Node
li $t1, 0
# Lesser Node
slt $t2, $t0, $t1
# Lesser Node
sw $t2, 8($fp)
# Conditional Node
lw $t0, 8($fp)
# Conditional Node
bne $t0, $zero, method7_at_D_label_0
# Equal Node
li $t0, 0
# Equal Node
lw $t1, 0($fp)
# Equal Node
seq $t2, $t0, $t1
# Equal Node
sw $t2, 16($fp)
# Conditional Node
lw $t0, 16($fp)
# Conditional Node
bne $t0, $zero, method7_at_D_label_2
# Equal Node
li $t0, 1
# Equal Node
lw $t1, 0($fp)
# Equal Node
seq $t2, $t0, $t1
# Equal Node
sw $t2, 24($fp)
# Conditional Node
lw $t0, 24($fp)
# Conditional Node
bne $t0, $zero, method7_at_D_label_4
# Equal Node
li $t0, 2
# Equal Node
lw $t1, 0($fp)
# Equal Node
seq $t2, $t0, $t1
# Equal Node
sw $t2, 32($fp)
# Conditional Node
lw $t0, 32($fp)
# Conditional Node
bne $t0, $zero, method7_at_D_label_6
# Minus Node
lw $t0, 0($fp)
# Minus Node
li $t1, 3
# Minus Node
sub $t2, $t0, $t1
# Minus Node
sw $t2, 36($fp)
# Call Node
lw $t0, 64($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 36($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 64($fp)
# Call Node
lw $t0, 0($t0)
# Call Node
sw $t0, 44($fp)
# Call Node
lw $t0, 44($fp)
# Call Node
lw $t0, 60($t0)
# Call Node
jal __get_ra
# Call Node
move $ra, $v0
# Call Node
jr $t0
# Call Node
sw $v0, 40($fp)
# Conditional Node
lw $t0, 40($fp)
# Conditional Node
sw $t0, 28($fp)
# Conditional Node
j method7_at_D_label_7
# Conditional Node
method7_at_D_label_6:
# Conditional Node
li $t0, 0
# Conditional Node
sw $t0, 28($fp)
# Conditional Node
method7_at_D_label_7:
# Conditional Node
lw $t0, 28($fp)
# Conditional Node
sw $t0, 20($fp)
# Conditional Node
j method7_at_D_label_5
# Conditional Node
method7_at_D_label_4:
# Conditional Node
li $t0, 0
# Conditional Node
sw $t0, 20($fp)
# Conditional Node
method7_at_D_label_5:
# Conditional Node
lw $t0, 20($fp)
# Conditional Node
sw $t0, 12($fp)
# Conditional Node
j method7_at_D_label_3
# Conditional Node
method7_at_D_label_2:
# Conditional Node
li $t0, 1
# Conditional Node
sw $t0, 12($fp)
# Conditional Node
method7_at_D_label_3:
# Conditional Node
lw $t0, 12($fp)
# Conditional Node
sw $t0, 4($fp)
# Conditional Node
j method7_at_D_label_1
# Conditional Node
method7_at_D_label_0:
# Roof Node
li $t0, 0
# Roof Node
lw $t1, 0($fp)
# Roof Node
sub $t2, $t0, $t1
# Roof Node
sw $t2, 48($fp)
# Call Node
lw $t0, 64($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 48($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 64($fp)
# Call Node
lw $t0, 0($t0)
# Call Node
sw $t0, 56($fp)
# Call Node
lw $t0, 56($fp)
# Call Node
lw $t0, 60($t0)
# Call Node
jal __get_ra
# Call Node
move $ra, $v0
# Call Node
jr $t0
# Call Node
sw $v0, 52($fp)
# Conditional Node
lw $t0, 52($fp)
# Conditional Node
sw $t0, 4($fp)
# Conditional Node
method7_at_D_label_1:
# Func Declaration Node
lw $v0, 4($fp)
# Program Node
lw $ra, 0($sp)
# Program Node
lw $fp, 4($sp)
# Program Node
addi $sp, $sp, 8
# Program Node
addi $sp, $sp, 68
# Program Node
jr $ra
# Program Node
function_method6_at_E:
# Program Node
addi $sp, $sp, -24
# Program Node
move $t0, $sp
# Program Node
addi $sp, $sp, -8
# Program Node
sw $ra, 0($sp)
# Program Node
sw $fp, 4($sp)
# Program Node
move $fp, $t0
# Var Declaration Node
li $t0, 0
# Var Declaration Node
sw $t0, 0($fp)
# Div Node
lw $t0, 24($fp)
# Div Node
li $t1, 8
# Div Node
div $t0, $t1
# Getting quotient
mflo $t0
# Stores the quotient
sw $t0, 8($fp)
# Assign Node
lw $t0, 8($fp)
# Assign Node
sw $t0, 0($fp)
# Instantiate Node
la $a0, A
# Instantiate Node
lw $a0, 4($a0)
li $v0, 9
syscall
sw $v0, 12($fp)
# Instantiate Node
lw $t0, 12($fp)
# Instantiate Node
addi $sp, $sp, -4
# Instantiate Node
sw $t0, 0($sp)
# Instantiate Node
jal __init_A_type
# Instantiate Node
sw $v0, 12($fp)
# Call Node
lw $t0, 12($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 0($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 12($fp)
# Call Node
lw $t0, 0($t0)
# Call Node
sw $t0, 20($fp)
# Call Node
lw $t0, 20($fp)
# Call Node
lw $t0, 36($t0)
# Call Node
jal __get_ra
# Call Node
move $ra, $v0
# Call Node
jr $t0
# Call Node
sw $v0, 16($fp)
# Func Declaration Node
lw $v0, 16($fp)
# Program Node
lw $ra, 0($sp)
# Program Node
lw $fp, 4($sp)
# Program Node
addi $sp, $sp, 8
# Program Node
addi $sp, $sp, 32
# Program Node
jr $ra
# Program Node
function_c2i_at_A2I:
# Program Node
addi $sp, $sp, -132
# Program Node
move $t0, $sp
# Program Node
addi $sp, $sp, -8
# Program Node
sw $ra, 0($sp)
# Program Node
sw $fp, 4($sp)
# Program Node
move $fp, $t0
# String Node
la $t0, data_13
# Type address into $a0
la $t1, String
# If String the is type and address
li $a0, 8
li $v0, 9
syscall
# Store String Type
sw $t1, 0($v0)
# Store String Address
sw $t0, 4($v0)
# Save string instance
sw $v0, 8($fp)
# a0 = left object
lw $a0, 132($fp)
# a1 = right object
lw $a1, 8($fp)
addi $sp, $sp, -4
sw $ra, 0($sp)
jal __object_equal
lw $ra, 0($sp)
addi $sp, $sp, 4
# Saving equal result
sw $v0, 4($fp)
# Conditional Node
lw $t0, 4($fp)
# Conditional Node
bne $t0, $zero, c2i_at_A2I_label_0
# String Node
la $t0, data_14
# Type address into $a0
la $t1, String
# If String the is type and address
li $a0, 8
li $v0, 9
syscall
# Store String Type
sw $t1, 0($v0)
# Store String Address
sw $t0, 4($v0)
# Save string instance
sw $v0, 20($fp)
# a0 = left object
lw $a0, 132($fp)
# a1 = right object
lw $a1, 20($fp)
addi $sp, $sp, -4
sw $ra, 0($sp)
jal __object_equal
lw $ra, 0($sp)
addi $sp, $sp, 4
# Saving equal result
sw $v0, 16($fp)
# Conditional Node
lw $t0, 16($fp)
# Conditional Node
bne $t0, $zero, c2i_at_A2I_label_2
# String Node
la $t0, data_15
# Type address into $a0
la $t1, String
# If String the is type and address
li $a0, 8
li $v0, 9
syscall
# Store String Type
sw $t1, 0($v0)
# Store String Address
sw $t0, 4($v0)
# Save string instance
sw $v0, 32($fp)
# a0 = left object
lw $a0, 132($fp)
# a1 = right object
lw $a1, 32($fp)
addi $sp, $sp, -4
sw $ra, 0($sp)
jal __object_equal
lw $ra, 0($sp)
addi $sp, $sp, 4
# Saving equal result
sw $v0, 28($fp)
# Conditional Node
lw $t0, 28($fp)
# Conditional Node
bne $t0, $zero, c2i_at_A2I_label_4
# String Node
la $t0, data_16
# Type address into $a0
la $t1, String
# If String the is type and address
li $a0, 8
li $v0, 9
syscall
# Store String Type
sw $t1, 0($v0)
# Store String Address
sw $t0, 4($v0)
# Save string instance
sw $v0, 44($fp)
# a0 = left object
lw $a0, 132($fp)
# a1 = right object
lw $a1, 44($fp)
addi $sp, $sp, -4
sw $ra, 0($sp)
jal __object_equal
lw $ra, 0($sp)
addi $sp, $sp, 4
# Saving equal result
sw $v0, 40($fp)
# Conditional Node
lw $t0, 40($fp)
# Conditional Node
bne $t0, $zero, c2i_at_A2I_label_6
# String Node
la $t0, data_17
# Type address into $a0
la $t1, String
# If String the is type and address
li $a0, 8
li $v0, 9
syscall
# Store String Type
sw $t1, 0($v0)
# Store String Address
sw $t0, 4($v0)
# Save string instance
sw $v0, 56($fp)
# a0 = left object
lw $a0, 132($fp)
# a1 = right object
lw $a1, 56($fp)
addi $sp, $sp, -4
sw $ra, 0($sp)
jal __object_equal
lw $ra, 0($sp)
addi $sp, $sp, 4
# Saving equal result
sw $v0, 52($fp)
# Conditional Node
lw $t0, 52($fp)
# Conditional Node
bne $t0, $zero, c2i_at_A2I_label_8
# String Node
la $t0, data_18
# Type address into $a0
la $t1, String
# If String the is type and address
li $a0, 8
li $v0, 9
syscall
# Store String Type
sw $t1, 0($v0)
# Store String Address
sw $t0, 4($v0)
# Save string instance
sw $v0, 68($fp)
# a0 = left object
lw $a0, 132($fp)
# a1 = right object
lw $a1, 68($fp)
addi $sp, $sp, -4
sw $ra, 0($sp)
jal __object_equal
lw $ra, 0($sp)
addi $sp, $sp, 4
# Saving equal result
sw $v0, 64($fp)
# Conditional Node
lw $t0, 64($fp)
# Conditional Node
bne $t0, $zero, c2i_at_A2I_label_10
# String Node
la $t0, data_19
# Type address into $a0
la $t1, String
# If String the is type and address
li $a0, 8
li $v0, 9
syscall
# Store String Type
sw $t1, 0($v0)
# Store String Address
sw $t0, 4($v0)
# Save string instance
sw $v0, 80($fp)
# a0 = left object
lw $a0, 132($fp)
# a1 = right object
lw $a1, 80($fp)
addi $sp, $sp, -4
sw $ra, 0($sp)
jal __object_equal
lw $ra, 0($sp)
addi $sp, $sp, 4
# Saving equal result
sw $v0, 76($fp)
# Conditional Node
lw $t0, 76($fp)
# Conditional Node
bne $t0, $zero, c2i_at_A2I_label_12
# String Node
la $t0, data_20
# Type address into $a0
la $t1, String
# If String the is type and address
li $a0, 8
li $v0, 9
syscall
# Store String Type
sw $t1, 0($v0)
# Store String Address
sw $t0, 4($v0)
# Save string instance
sw $v0, 92($fp)
# a0 = left object
lw $a0, 132($fp)
# a1 = right object
lw $a1, 92($fp)
addi $sp, $sp, -4
sw $ra, 0($sp)
jal __object_equal
lw $ra, 0($sp)
addi $sp, $sp, 4
# Saving equal result
sw $v0, 88($fp)
# Conditional Node
lw $t0, 88($fp)
# Conditional Node
bne $t0, $zero, c2i_at_A2I_label_14
# String Node
la $t0, data_21
# Type address into $a0
la $t1, String
# If String the is type and address
li $a0, 8
li $v0, 9
syscall
# Store String Type
sw $t1, 0($v0)
# Store String Address
sw $t0, 4($v0)
# Save string instance
sw $v0, 104($fp)
# a0 = left object
lw $a0, 132($fp)
# a1 = right object
lw $a1, 104($fp)
addi $sp, $sp, -4
sw $ra, 0($sp)
jal __object_equal
lw $ra, 0($sp)
addi $sp, $sp, 4
# Saving equal result
sw $v0, 100($fp)
# Conditional Node
lw $t0, 100($fp)
# Conditional Node
bne $t0, $zero, c2i_at_A2I_label_16
# String Node
la $t0, data_22
# Type address into $a0
la $t1, String
# If String the is type and address
li $a0, 8
li $v0, 9
syscall
# Store String Type
sw $t1, 0($v0)
# Store String Address
sw $t0, 4($v0)
# Save string instance
sw $v0, 116($fp)
# a0 = left object
lw $a0, 132($fp)
# a1 = right object
lw $a1, 116($fp)
addi $sp, $sp, -4
sw $ra, 0($sp)
jal __object_equal
lw $ra, 0($sp)
addi $sp, $sp, 4
# Saving equal result
sw $v0, 112($fp)
# Conditional Node
lw $t0, 112($fp)
# Conditional Node
bne $t0, $zero, c2i_at_A2I_label_18
# Call Node
lw $t0, 136($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 136($fp)
# Call Node
lw $t0, 0($t0)
# Call Node
sw $t0, 128($fp)
# Call Node
lw $t0, 128($fp)
# Call Node
lw $t0, 16($t0)
# Call Node
jal __get_ra
# Call Node
move $ra, $v0
# Call Node
jr $t0
# Call Node
sw $v0, 124($fp)
# Conditional Node
li $t0, 0
# Conditional Node
sw $t0, 108($fp)
# Conditional Node
j c2i_at_A2I_label_19
# Conditional Node
c2i_at_A2I_label_18:
# Conditional Node
li $t0, 9
# Conditional Node
sw $t0, 108($fp)
# Conditional Node
c2i_at_A2I_label_19:
# Conditional Node
lw $t0, 108($fp)
# Conditional Node
sw $t0, 96($fp)
# Conditional Node
j c2i_at_A2I_label_17
# Conditional Node
c2i_at_A2I_label_16:
# Conditional Node
li $t0, 8
# Conditional Node
sw $t0, 96($fp)
# Conditional Node
c2i_at_A2I_label_17:
# Conditional Node
lw $t0, 96($fp)
# Conditional Node
sw $t0, 84($fp)
# Conditional Node
j c2i_at_A2I_label_15
# Conditional Node
c2i_at_A2I_label_14:
# Conditional Node
li $t0, 7
# Conditional Node
sw $t0, 84($fp)
# Conditional Node
c2i_at_A2I_label_15:
# Conditional Node
lw $t0, 84($fp)
# Conditional Node
sw $t0, 72($fp)
# Conditional Node
j c2i_at_A2I_label_13
# Conditional Node
c2i_at_A2I_label_12:
# Conditional Node
li $t0, 6
# Conditional Node
sw $t0, 72($fp)
# Conditional Node
c2i_at_A2I_label_13:
# Conditional Node
lw $t0, 72($fp)
# Conditional Node
sw $t0, 60($fp)
# Conditional Node
j c2i_at_A2I_label_11
# Conditional Node
c2i_at_A2I_label_10:
# Conditional Node
li $t0, 5
# Conditional Node
sw $t0, 60($fp)
# Conditional Node
c2i_at_A2I_label_11:
# Conditional Node
lw $t0, 60($fp)
# Conditional Node
sw $t0, 48($fp)
# Conditional Node
j c2i_at_A2I_label_9
# Conditional Node
c2i_at_A2I_label_8:
# Conditional Node
li $t0, 4
# Conditional Node
sw $t0, 48($fp)
# Conditional Node
c2i_at_A2I_label_9:
# Conditional Node
lw $t0, 48($fp)
# Conditional Node
sw $t0, 36($fp)
# Conditional Node
j c2i_at_A2I_label_7
# Conditional Node
c2i_at_A2I_label_6:
# Conditional Node
li $t0, 3
# Conditional Node
sw $t0, 36($fp)
# Conditional Node
c2i_at_A2I_label_7:
# Conditional Node
lw $t0, 36($fp)
# Conditional Node
sw $t0, 24($fp)
# Conditional Node
j c2i_at_A2I_label_5
# Conditional Node
c2i_at_A2I_label_4:
# Conditional Node
li $t0, 2
# Conditional Node
sw $t0, 24($fp)
# Conditional Node
c2i_at_A2I_label_5:
# Conditional Node
lw $t0, 24($fp)
# Conditional Node
sw $t0, 12($fp)
# Conditional Node
j c2i_at_A2I_label_3
# Conditional Node
c2i_at_A2I_label_2:
# Conditional Node
li $t0, 1
# Conditional Node
sw $t0, 12($fp)
# Conditional Node
c2i_at_A2I_label_3:
# Conditional Node
lw $t0, 12($fp)
# Conditional Node
sw $t0, 0($fp)
# Conditional Node
j c2i_at_A2I_label_1
# Conditional Node
c2i_at_A2I_label_0:
# Conditional Node
li $t0, 0
# Conditional Node
sw $t0, 0($fp)
# Conditional Node
c2i_at_A2I_label_1:
# Func Declaration Node
lw $v0, 0($fp)
# Program Node
lw $ra, 0($sp)
# Program Node
lw $fp, 4($sp)
# Program Node
addi $sp, $sp, 8
# Program Node
addi $sp, $sp, 140
# Program Node
jr $ra
# Program Node
function_i2c_at_A2I:
# Program Node
addi $sp, $sp, -136
# Program Node
move $t0, $sp
# Program Node
addi $sp, $sp, -8
# Program Node
sw $ra, 0($sp)
# Program Node
sw $fp, 4($sp)
# Program Node
move $fp, $t0
# Equal Node
lw $t0, 136($fp)
# Equal Node
li $t1, 0
# Equal Node
seq $t2, $t0, $t1
# Equal Node
sw $t2, 4($fp)
# Conditional Node
lw $t0, 4($fp)
# Conditional Node
bne $t0, $zero, i2c_at_A2I_label_0
# Equal Node
lw $t0, 136($fp)
# Equal Node
li $t1, 1
# Equal Node
seq $t2, $t0, $t1
# Equal Node
sw $t2, 12($fp)
# Conditional Node
lw $t0, 12($fp)
# Conditional Node
bne $t0, $zero, i2c_at_A2I_label_2
# Equal Node
lw $t0, 136($fp)
# Equal Node
li $t1, 2
# Equal Node
seq $t2, $t0, $t1
# Equal Node
sw $t2, 20($fp)
# Conditional Node
lw $t0, 20($fp)
# Conditional Node
bne $t0, $zero, i2c_at_A2I_label_4
# Equal Node
lw $t0, 136($fp)
# Equal Node
li $t1, 3
# Equal Node
seq $t2, $t0, $t1
# Equal Node
sw $t2, 28($fp)
# Conditional Node
lw $t0, 28($fp)
# Conditional Node
bne $t0, $zero, i2c_at_A2I_label_6
# Equal Node
lw $t0, 136($fp)
# Equal Node
li $t1, 4
# Equal Node
seq $t2, $t0, $t1
# Equal Node
sw $t2, 36($fp)
# Conditional Node
lw $t0, 36($fp)
# Conditional Node
bne $t0, $zero, i2c_at_A2I_label_8
# Equal Node
lw $t0, 136($fp)
# Equal Node
li $t1, 5
# Equal Node
seq $t2, $t0, $t1
# Equal Node
sw $t2, 44($fp)
# Conditional Node
lw $t0, 44($fp)
# Conditional Node
bne $t0, $zero, i2c_at_A2I_label_10
# Equal Node
lw $t0, 136($fp)
# Equal Node
li $t1, 6
# Equal Node
seq $t2, $t0, $t1
# Equal Node
sw $t2, 52($fp)
# Conditional Node
lw $t0, 52($fp)
# Conditional Node
bne $t0, $zero, i2c_at_A2I_label_12
# Equal Node
lw $t0, 136($fp)
# Equal Node
li $t1, 7
# Equal Node
seq $t2, $t0, $t1
# Equal Node
sw $t2, 60($fp)
# Conditional Node
lw $t0, 60($fp)
# Conditional Node
bne $t0, $zero, i2c_at_A2I_label_14
# Equal Node
lw $t0, 136($fp)
# Equal Node
li $t1, 8
# Equal Node
seq $t2, $t0, $t1
# Equal Node
sw $t2, 68($fp)
# Conditional Node
lw $t0, 68($fp)
# Conditional Node
bne $t0, $zero, i2c_at_A2I_label_16
# Equal Node
lw $t0, 136($fp)
# Equal Node
li $t1, 9
# Equal Node
seq $t2, $t0, $t1
# Equal Node
sw $t2, 76($fp)
# Conditional Node
lw $t0, 76($fp)
# Conditional Node
bne $t0, $zero, i2c_at_A2I_label_18
# Call Node
lw $t0, 140($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 140($fp)
# Call Node
lw $t0, 0($t0)
# Call Node
sw $t0, 88($fp)
# Call Node
lw $t0, 88($fp)
# Call Node
lw $t0, 16($t0)
# Call Node
jal __get_ra
# Call Node
move $ra, $v0
# Call Node
jr $t0
# Call Node
sw $v0, 84($fp)
# String Node
la $t0, data_23
# Type address into $a0
la $t1, String
# If String the is type and address
li $a0, 8
li $v0, 9
syscall
# Store String Type
sw $t1, 0($v0)
# Store String Address
sw $t0, 4($v0)
# Save string instance
sw $v0, 92($fp)
# Conditional Node
lw $t0, 92($fp)
# Conditional Node
sw $t0, 72($fp)
# Conditional Node
j i2c_at_A2I_label_19
# Conditional Node
i2c_at_A2I_label_18:
# String Node
la $t0, data_24
# Type address into $a0
la $t1, String
# If String the is type and address
li $a0, 8
li $v0, 9
syscall
# Store String Type
sw $t1, 0($v0)
# Store String Address
sw $t0, 4($v0)
# Save string instance
sw $v0, 96($fp)
# Conditional Node
lw $t0, 96($fp)
# Conditional Node
sw $t0, 72($fp)
# Conditional Node
i2c_at_A2I_label_19:
# Conditional Node
lw $t0, 72($fp)
# Conditional Node
sw $t0, 64($fp)
# Conditional Node
j i2c_at_A2I_label_17
# Conditional Node
i2c_at_A2I_label_16:
# String Node
la $t0, data_25
# Type address into $a0
la $t1, String
# If String the is type and address
li $a0, 8
li $v0, 9
syscall
# Store String Type
sw $t1, 0($v0)
# Store String Address
sw $t0, 4($v0)
# Save string instance
sw $v0, 100($fp)
# Conditional Node
lw $t0, 100($fp)
# Conditional Node
sw $t0, 64($fp)
# Conditional Node
i2c_at_A2I_label_17:
# Conditional Node
lw $t0, 64($fp)
# Conditional Node
sw $t0, 56($fp)
# Conditional Node
j i2c_at_A2I_label_15
# Conditional Node
i2c_at_A2I_label_14:
# String Node
la $t0, data_26
# Type address into $a0
la $t1, String
# If String the is type and address
li $a0, 8
li $v0, 9
syscall
# Store String Type
sw $t1, 0($v0)
# Store String Address
sw $t0, 4($v0)
# Save string instance
sw $v0, 104($fp)
# Conditional Node
lw $t0, 104($fp)
# Conditional Node
sw $t0, 56($fp)
# Conditional Node
i2c_at_A2I_label_15:
# Conditional Node
lw $t0, 56($fp)
# Conditional Node
sw $t0, 48($fp)
# Conditional Node
j i2c_at_A2I_label_13
# Conditional Node
i2c_at_A2I_label_12:
# String Node
la $t0, data_27
# Type address into $a0
la $t1, String
# If String the is type and address
li $a0, 8
li $v0, 9
syscall
# Store String Type
sw $t1, 0($v0)
# Store String Address
sw $t0, 4($v0)
# Save string instance
sw $v0, 108($fp)
# Conditional Node
lw $t0, 108($fp)
# Conditional Node
sw $t0, 48($fp)
# Conditional Node
i2c_at_A2I_label_13:
# Conditional Node
lw $t0, 48($fp)
# Conditional Node
sw $t0, 40($fp)
# Conditional Node
j i2c_at_A2I_label_11
# Conditional Node
i2c_at_A2I_label_10:
# String Node
la $t0, data_28
# Type address into $a0
la $t1, String
# If String the is type and address
li $a0, 8
li $v0, 9
syscall
# Store String Type
sw $t1, 0($v0)
# Store String Address
sw $t0, 4($v0)
# Save string instance
sw $v0, 112($fp)
# Conditional Node
lw $t0, 112($fp)
# Conditional Node
sw $t0, 40($fp)
# Conditional Node
i2c_at_A2I_label_11:
# Conditional Node
lw $t0, 40($fp)
# Conditional Node
sw $t0, 32($fp)
# Conditional Node
j i2c_at_A2I_label_9
# Conditional Node
i2c_at_A2I_label_8:
# String Node
la $t0, data_29
# Type address into $a0
la $t1, String
# If String the is type and address
li $a0, 8
li $v0, 9
syscall
# Store String Type
sw $t1, 0($v0)
# Store String Address
sw $t0, 4($v0)
# Save string instance
sw $v0, 116($fp)
# Conditional Node
lw $t0, 116($fp)
# Conditional Node
sw $t0, 32($fp)
# Conditional Node
i2c_at_A2I_label_9:
# Conditional Node
lw $t0, 32($fp)
# Conditional Node
sw $t0, 24($fp)
# Conditional Node
j i2c_at_A2I_label_7
# Conditional Node
i2c_at_A2I_label_6:
# String Node
la $t0, data_30
# Type address into $a0
la $t1, String
# If String the is type and address
li $a0, 8
li $v0, 9
syscall
# Store String Type
sw $t1, 0($v0)
# Store String Address
sw $t0, 4($v0)
# Save string instance
sw $v0, 120($fp)
# Conditional Node
lw $t0, 120($fp)
# Conditional Node
sw $t0, 24($fp)
# Conditional Node
i2c_at_A2I_label_7:
# Conditional Node
lw $t0, 24($fp)
# Conditional Node
sw $t0, 16($fp)
# Conditional Node
j i2c_at_A2I_label_5
# Conditional Node
i2c_at_A2I_label_4:
# String Node
la $t0, data_31
# Type address into $a0
la $t1, String
# If String the is type and address
li $a0, 8
li $v0, 9
syscall
# Store String Type
sw $t1, 0($v0)
# Store String Address
sw $t0, 4($v0)
# Save string instance
sw $v0, 124($fp)
# Conditional Node
lw $t0, 124($fp)
# Conditional Node
sw $t0, 16($fp)
# Conditional Node
i2c_at_A2I_label_5:
# Conditional Node
lw $t0, 16($fp)
# Conditional Node
sw $t0, 8($fp)
# Conditional Node
j i2c_at_A2I_label_3
# Conditional Node
i2c_at_A2I_label_2:
# String Node
la $t0, data_32
# Type address into $a0
la $t1, String
# If String the is type and address
li $a0, 8
li $v0, 9
syscall
# Store String Type
sw $t1, 0($v0)
# Store String Address
sw $t0, 4($v0)
# Save string instance
sw $v0, 128($fp)
# Conditional Node
lw $t0, 128($fp)
# Conditional Node
sw $t0, 8($fp)
# Conditional Node
i2c_at_A2I_label_3:
# Conditional Node
lw $t0, 8($fp)
# Conditional Node
sw $t0, 0($fp)
# Conditional Node
j i2c_at_A2I_label_1
# Conditional Node
i2c_at_A2I_label_0:
# String Node
la $t0, data_33
# Type address into $a0
la $t1, String
# If String the is type and address
li $a0, 8
li $v0, 9
syscall
# Store String Type
sw $t1, 0($v0)
# Store String Address
sw $t0, 4($v0)
# Save string instance
sw $v0, 132($fp)
# Conditional Node
lw $t0, 132($fp)
# Conditional Node
sw $t0, 0($fp)
# Conditional Node
i2c_at_A2I_label_1:
# Func Declaration Node
lw $v0, 0($fp)
# Program Node
lw $ra, 0($sp)
# Program Node
lw $fp, 4($sp)
# Program Node
addi $sp, $sp, 8
# Program Node
addi $sp, $sp, 144
# Program Node
jr $ra
# Program Node
function_a2i_at_A2I:
# Program Node
addi $sp, $sp, -124
# Program Node
move $t0, $sp
# Program Node
addi $sp, $sp, -8
# Program Node
sw $ra, 0($sp)
# Program Node
sw $fp, 4($sp)
# Program Node
move $fp, $t0
# Call Node
lw $t0, 124($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 124($fp)
# Call Node
lw $t0, 0($t0)
# Call Node
sw $t0, 12($fp)
# Call Node
lw $t0, 12($fp)
# Call Node
lw $t0, 28($t0)
# Call Node
jal __get_ra
# Call Node
move $ra, $v0
# Call Node
jr $t0
# Call Node
sw $v0, 8($fp)
# Equal Node
lw $t0, 8($fp)
# Equal Node
li $t1, 0
# Equal Node
seq $t2, $t0, $t1
# Equal Node
sw $t2, 4($fp)
# Conditional Node
lw $t0, 4($fp)
# Conditional Node
bne $t0, $zero, a2i_at_A2I_label_0
# Call Node
lw $t0, 124($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
li $t0, 0
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
li $t0, 1
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 124($fp)
# Call Node
lw $t0, 0($t0)
# Call Node
sw $t0, 28($fp)
# Call Node
lw $t0, 28($fp)
# Call Node
lw $t0, 36($t0)
# Call Node
jal __get_ra
# Call Node
move $ra, $v0
# Call Node
jr $t0
# Call Node
sw $v0, 24($fp)
# String Node
la $t0, data_34
# Type address into $a0
la $t1, String
# If String the is type and address
li $a0, 8
li $v0, 9
syscall
# Store String Type
sw $t1, 0($v0)
# Store String Address
sw $t0, 4($v0)
# Save string instance
sw $v0, 32($fp)
# a0 = left object
lw $a0, 24($fp)
# a1 = right object
lw $a1, 32($fp)
addi $sp, $sp, -4
sw $ra, 0($sp)
jal __object_equal
lw $ra, 0($sp)
addi $sp, $sp, 4
# Saving equal result
sw $v0, 20($fp)
# Conditional Node
lw $t0, 20($fp)
# Conditional Node
bne $t0, $zero, a2i_at_A2I_label_2
# Call Node
lw $t0, 124($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
li $t0, 0
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
li $t0, 1
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 124($fp)
# Call Node
lw $t0, 0($t0)
# Call Node
sw $t0, 48($fp)
# Call Node
lw $t0, 48($fp)
# Call Node
lw $t0, 36($t0)
# Call Node
jal __get_ra
# Call Node
move $ra, $v0
# Call Node
jr $t0
# Call Node
sw $v0, 44($fp)
# String Node
la $t0, data_35
# Type address into $a0
la $t1, String
# If String the is type and address
li $a0, 8
li $v0, 9
syscall
# Store String Type
sw $t1, 0($v0)
# Store String Address
sw $t0, 4($v0)
# Save string instance
sw $v0, 52($fp)
# a0 = left object
lw $a0, 44($fp)
# a1 = right object
lw $a1, 52($fp)
addi $sp, $sp, -4
sw $ra, 0($sp)
jal __object_equal
lw $ra, 0($sp)
addi $sp, $sp, 4
# Saving equal result
sw $v0, 40($fp)
# Conditional Node
lw $t0, 40($fp)
# Conditional Node
bne $t0, $zero, a2i_at_A2I_label_4
# Call Node
lw $t0, 128($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 124($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 128($fp)
# Call Node
lw $t0, 0($t0)
# Call Node
sw $t0, 60($fp)
# Call Node
lw $t0, 60($fp)
# Call Node
lw $t0, 40($t0)
# Call Node
jal __get_ra
# Call Node
move $ra, $v0
# Call Node
jr $t0
# Call Node
sw $v0, 56($fp)
# Conditional Node
lw $t0, 56($fp)
# Conditional Node
sw $t0, 36($fp)
# Conditional Node
j a2i_at_A2I_label_5
# Conditional Node
a2i_at_A2I_label_4:
# Call Node
lw $t0, 124($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 124($fp)
# Call Node
lw $t0, 0($t0)
# Call Node
sw $t0, 68($fp)
# Call Node
lw $t0, 68($fp)
# Call Node
lw $t0, 28($t0)
# Call Node
jal __get_ra
# Call Node
move $ra, $v0
# Call Node
jr $t0
# Call Node
sw $v0, 64($fp)
# Minus Node
lw $t0, 64($fp)
# Minus Node
li $t1, 1
# Minus Node
sub $t2, $t0, $t1
# Minus Node
sw $t2, 72($fp)
# Call Node
lw $t0, 124($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
li $t0, 1
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 72($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 124($fp)
# Call Node
lw $t0, 0($t0)
# Call Node
sw $t0, 80($fp)
# Call Node
lw $t0, 80($fp)
# Call Node
lw $t0, 36($t0)
# Call Node
jal __get_ra
# Call Node
move $ra, $v0
# Call Node
jr $t0
# Call Node
sw $v0, 76($fp)
# Call Node
lw $t0, 128($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 76($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 128($fp)
# Call Node
lw $t0, 0($t0)
# Call Node
sw $t0, 88($fp)
# Call Node
lw $t0, 88($fp)
# Call Node
lw $t0, 40($t0)
# Call Node
jal __get_ra
# Call Node
move $ra, $v0
# Call Node
jr $t0
# Call Node
sw $v0, 84($fp)
# Conditional Node
lw $t0, 84($fp)
# Conditional Node
sw $t0, 36($fp)
# Conditional Node
a2i_at_A2I_label_5:
# Conditional Node
lw $t0, 36($fp)
# Conditional Node
sw $t0, 16($fp)
# Conditional Node
j a2i_at_A2I_label_3
# Conditional Node
a2i_at_A2I_label_2:
# Call Node
lw $t0, 124($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 124($fp)
# Call Node
lw $t0, 0($t0)
# Call Node
sw $t0, 100($fp)
# Call Node
lw $t0, 100($fp)
# Call Node
lw $t0, 28($t0)
# Call Node
jal __get_ra
# Call Node
move $ra, $v0
# Call Node
jr $t0
# Call Node
sw $v0, 96($fp)
# Minus Node
lw $t0, 96($fp)
# Minus Node
li $t1, 1
# Minus Node
sub $t2, $t0, $t1
# Minus Node
sw $t2, 104($fp)
# Call Node
lw $t0, 124($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
li $t0, 1
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 104($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 124($fp)
# Call Node
lw $t0, 0($t0)
# Call Node
sw $t0, 112($fp)
# Call Node
lw $t0, 112($fp)
# Call Node
lw $t0, 36($t0)
# Call Node
jal __get_ra
# Call Node
move $ra, $v0
# Call Node
jr $t0
# Call Node
sw $v0, 108($fp)
# Call Node
lw $t0, 128($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 108($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 128($fp)
# Call Node
lw $t0, 0($t0)
# Call Node
sw $t0, 120($fp)
# Call Node
lw $t0, 120($fp)
# Call Node
lw $t0, 40($t0)
# Call Node
jal __get_ra
# Call Node
move $ra, $v0
# Call Node
jr $t0
# Call Node
sw $v0, 116($fp)
# Roof Node
li $t0, 0
# Roof Node
lw $t1, 116($fp)
# Roof Node
sub $t2, $t0, $t1
# Roof Node
sw $t2, 92($fp)
# Conditional Node
lw $t0, 92($fp)
# Conditional Node
sw $t0, 16($fp)
# Conditional Node
a2i_at_A2I_label_3:
# Conditional Node
lw $t0, 16($fp)
# Conditional Node
sw $t0, 0($fp)
# Conditional Node
j a2i_at_A2I_label_1
# Conditional Node
a2i_at_A2I_label_0:
# Conditional Node
li $t0, 0
# Conditional Node
sw $t0, 0($fp)
# Conditional Node
a2i_at_A2I_label_1:
# Func Declaration Node
lw $v0, 0($fp)
# Program Node
lw $ra, 0($sp)
# Program Node
lw $fp, 4($sp)
# Program Node
addi $sp, $sp, 8
# Program Node
addi $sp, $sp, 132
# Program Node
jr $ra
# Program Node
function_a2i_aux_at_A2I:
# Program Node
addi $sp, $sp, -64
# Program Node
move $t0, $sp
# Program Node
addi $sp, $sp, -8
# Program Node
sw $ra, 0($sp)
# Program Node
sw $fp, 4($sp)
# Program Node
move $fp, $t0
# Var Declaration Node
li $t0, 0
# Var Declaration Node
sw $t0, 0($fp)
# Call Node
lw $t0, 64($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 64($fp)
# Call Node
lw $t0, 0($t0)
# Call Node
sw $t0, 16($fp)
# Call Node
lw $t0, 16($fp)
# Call Node
lw $t0, 28($t0)
# Call Node
jal __get_ra
# Call Node
move $ra, $v0
# Call Node
jr $t0
# Call Node
sw $v0, 12($fp)
# Var Declaration Node
lw $t0, 12($fp)
# Var Declaration Node
sw $t0, 8($fp)
# Var Declaration Node
li $t0, 0
# Var Declaration Node
sw $t0, 20($fp)
# Void Node
sw $zero, 24($fp)
# While Node
a2i_aux_at_A2I_label_0:
# Lesser Node
lw $t0, 20($fp)
# Lesser Node
lw $t1, 8($fp)
# Lesser Node
slt $t2, $t0, $t1
# Lesser Node
sw $t2, 28($fp)
# While Node
lw $t0, 28($fp)
# While Node
bne $t0, $zero, a2i_aux_at_A2I_label_1
# While Node
j a2i_aux_at_A2I_label_2
# While Node
a2i_aux_at_A2I_label_1:
# Star Node
lw $t0, 0($fp)
# Star Node
li $t1, 10
# Star Node
mul $t2, $t0, $t1
# Star Node
sw $t2, 36($fp)
# Call Node
lw $t0, 64($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 20($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
li $t0, 1
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 64($fp)
# Call Node
lw $t0, 0($t0)
# Call Node
sw $t0, 44($fp)
# Call Node
lw $t0, 44($fp)
# Call Node
lw $t0, 36($t0)
# Call Node
jal __get_ra
# Call Node
move $ra, $v0
# Call Node
jr $t0
# Call Node
sw $v0, 40($fp)
# Call Node
lw $t0, 68($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 40($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 68($fp)
# Call Node
lw $t0, 0($t0)
# Call Node
sw $t0, 52($fp)
# Call Node
lw $t0, 52($fp)
# Call Node
lw $t0, 28($t0)
# Call Node
jal __get_ra
# Call Node
move $ra, $v0
# Call Node
jr $t0
# Call Node
sw $v0, 48($fp)
# Plus Node
lw $t0, 36($fp)
# Plus Node
lw $t1, 48($fp)
# Plus Node
add $t2, $t0, $t1
# Plus Node
sw $t2, 56($fp)
# Assign Node
lw $t0, 56($fp)
# Assign Node
sw $t0, 0($fp)
# Plus Node
lw $t0, 20($fp)
# Plus Node
li $t1, 1
# Plus Node
add $t2, $t0, $t1
# Plus Node
sw $t2, 60($fp)
# Assign Node
lw $t0, 60($fp)
# Assign Node
sw $t0, 20($fp)
# While Node
j a2i_aux_at_A2I_label_0
# While Node
a2i_aux_at_A2I_label_2:
# Func Declaration Node
lw $v0, 0($fp)
# Program Node
lw $ra, 0($sp)
# Program Node
lw $fp, 4($sp)
# Program Node
addi $sp, $sp, 8
# Program Node
addi $sp, $sp, 72
# Program Node
jr $ra
# Program Node
function_i2a_at_A2I:
# Program Node
addi $sp, $sp, -56
# Program Node
move $t0, $sp
# Program Node
addi $sp, $sp, -8
# Program Node
sw $ra, 0($sp)
# Program Node
sw $fp, 4($sp)
# Program Node
move $fp, $t0
# Equal Node
lw $t0, 56($fp)
# Equal Node
li $t1, 0
# Equal Node
seq $t2, $t0, $t1
# Equal Node
sw $t2, 4($fp)
# Conditional Node
lw $t0, 4($fp)
# Conditional Node
bne $t0, $zero, i2a_at_A2I_label_0
# Lesser Node
li $t0, 0
# Lesser Node
lw $t1, 56($fp)
# Lesser Node
slt $t2, $t0, $t1
# Lesser Node
sw $t2, 12($fp)
# Conditional Node
lw $t0, 12($fp)
# Conditional Node
bne $t0, $zero, i2a_at_A2I_label_2
# String Node
la $t0, data_36
# Type address into $a0
la $t1, String
# If String the is type and address
li $a0, 8
li $v0, 9
syscall
# Store String Type
sw $t1, 0($v0)
# Store String Address
sw $t0, 4($v0)
# Save string instance
sw $v0, 16($fp)
# Roof Node
li $t0, 0
# Roof Node
li $t1, 1
# Roof Node
sub $t2, $t0, $t1
# Roof Node
sw $t2, 20($fp)
# Star Node
lw $t0, 56($fp)
# Star Node
lw $t1, 20($fp)
# Star Node
mul $t2, $t0, $t1
# Star Node
sw $t2, 24($fp)
# Call Node
lw $t0, 60($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 24($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 60($fp)
# Call Node
lw $t0, 0($t0)
# Call Node
sw $t0, 32($fp)
# Call Node
lw $t0, 32($fp)
# Call Node
lw $t0, 48($t0)
# Call Node
jal __get_ra
# Call Node
move $ra, $v0
# Call Node
jr $t0
# Call Node
sw $v0, 28($fp)
# Call Node
lw $t0, 16($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 28($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 16($fp)
# Call Node
lw $t0, 0($t0)
# Call Node
sw $t0, 40($fp)
# Call Node
lw $t0, 40($fp)
# Call Node
lw $t0, 32($t0)
# Call Node
jal __get_ra
# Call Node
move $ra, $v0
# Call Node
jr $t0
# Call Node
sw $v0, 36($fp)
# Conditional Node
lw $t0, 36($fp)
# Conditional Node
sw $t0, 8($fp)
# Conditional Node
j i2a_at_A2I_label_3
# Conditional Node
i2a_at_A2I_label_2:
# Call Node
lw $t0, 60($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 56($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 60($fp)
# Call Node
lw $t0, 0($t0)
# Call Node
sw $t0, 48($fp)
# Call Node
lw $t0, 48($fp)
# Call Node
lw $t0, 48($t0)
# Call Node
jal __get_ra
# Call Node
move $ra, $v0
# Call Node
jr $t0
# Call Node
sw $v0, 44($fp)
# Conditional Node
lw $t0, 44($fp)
# Conditional Node
sw $t0, 8($fp)
# Conditional Node
i2a_at_A2I_label_3:
# Conditional Node
lw $t0, 8($fp)
# Conditional Node
sw $t0, 0($fp)
# Conditional Node
j i2a_at_A2I_label_1
# Conditional Node
i2a_at_A2I_label_0:
# String Node
la $t0, data_37
# Type address into $a0
la $t1, String
# If String the is type and address
li $a0, 8
li $v0, 9
syscall
# Store String Type
sw $t1, 0($v0)
# Store String Address
sw $t0, 4($v0)
# Save string instance
sw $v0, 52($fp)
# Conditional Node
lw $t0, 52($fp)
# Conditional Node
sw $t0, 0($fp)
# Conditional Node
i2a_at_A2I_label_1:
# Func Declaration Node
lw $v0, 0($fp)
# Program Node
lw $ra, 0($sp)
# Program Node
lw $fp, 4($sp)
# Program Node
addi $sp, $sp, 8
# Program Node
addi $sp, $sp, 64
# Program Node
jr $ra
# Program Node
function_i2a_aux_at_A2I:
# Program Node
addi $sp, $sp, -52
# Program Node
move $t0, $sp
# Program Node
addi $sp, $sp, -8
# Program Node
sw $ra, 0($sp)
# Program Node
sw $fp, 4($sp)
# Program Node
move $fp, $t0
# Equal Node
lw $t0, 52($fp)
# Equal Node
li $t1, 0
# Equal Node
seq $t2, $t0, $t1
# Equal Node
sw $t2, 4($fp)
# Conditional Node
lw $t0, 4($fp)
# Conditional Node
bne $t0, $zero, i2a_aux_at_A2I_label_0
# Div Node
lw $t0, 52($fp)
# Div Node
li $t1, 10
# Div Node
div $t0, $t1
# Getting quotient
mflo $t0
# Stores the quotient
sw $t0, 12($fp)
# Var Declaration Node
lw $t0, 12($fp)
# Var Declaration Node
sw $t0, 8($fp)
# Call Node
lw $t0, 56($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 8($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 56($fp)
# Call Node
lw $t0, 0($t0)
# Call Node
sw $t0, 20($fp)
# Call Node
lw $t0, 20($fp)
# Call Node
lw $t0, 48($t0)
# Call Node
jal __get_ra
# Call Node
move $ra, $v0
# Call Node
jr $t0
# Call Node
sw $v0, 16($fp)
# Star Node
lw $t0, 8($fp)
# Star Node
li $t1, 10
# Star Node
mul $t2, $t0, $t1
# Star Node
sw $t2, 24($fp)
# Minus Node
lw $t0, 52($fp)
# Minus Node
lw $t1, 24($fp)
# Minus Node
sub $t2, $t0, $t1
# Minus Node
sw $t2, 28($fp)
# Call Node
lw $t0, 56($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 28($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 56($fp)
# Call Node
lw $t0, 0($t0)
# Call Node
sw $t0, 36($fp)
# Call Node
lw $t0, 36($fp)
# Call Node
lw $t0, 32($t0)
# Call Node
jal __get_ra
# Call Node
move $ra, $v0
# Call Node
jr $t0
# Call Node
sw $v0, 32($fp)
# Call Node
lw $t0, 16($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 32($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 16($fp)
# Call Node
lw $t0, 0($t0)
# Call Node
sw $t0, 44($fp)
# Call Node
lw $t0, 44($fp)
# Call Node
lw $t0, 32($t0)
# Call Node
jal __get_ra
# Call Node
move $ra, $v0
# Call Node
jr $t0
# Call Node
sw $v0, 40($fp)
# Conditional Node
lw $t0, 40($fp)
# Conditional Node
sw $t0, 0($fp)
# Conditional Node
j i2a_aux_at_A2I_label_1
# Conditional Node
i2a_aux_at_A2I_label_0:
# String Node
la $t0, data_38
# Type address into $a0
la $t1, String
# If String the is type and address
li $a0, 8
li $v0, 9
syscall
# Store String Type
sw $t1, 0($v0)
# Store String Address
sw $t0, 4($v0)
# Save string instance
sw $v0, 48($fp)
# Conditional Node
lw $t0, 48($fp)
# Conditional Node
sw $t0, 0($fp)
# Conditional Node
i2a_aux_at_A2I_label_1:
# Func Declaration Node
lw $v0, 0($fp)
# Program Node
lw $ra, 0($sp)
# Program Node
lw $fp, 4($sp)
# Program Node
addi $sp, $sp, 8
# Program Node
addi $sp, $sp, 60
# Program Node
jr $ra
# Program Node
function_abort_at_Object:
# Program Node
addi $sp, $sp, -16
# Program Node
move $t0, $sp
# Program Node
addi $sp, $sp, -8
# Program Node
sw $ra, 0($sp)
# Program Node
sw $fp, 4($sp)
# Program Node
move $fp, $t0
# Assign object type
lw $t0, 16($fp)
# Assign object type
lw $t0, 0($t0)
# Assign object type
sw $t0, 0($fp)
# Get type name
lw $a0, 0($fp)
# Get type name
jal __type_name
# Get type name
sw $v0, 4($fp)
la $t0, data_12
# Type address into $a0
la $t1, String
# If String the is type and address
li $a0, 8
li $v0, 9
syscall
# Store String Type
sw $t1, 0($v0)
# Store String Address
sw $t0, 4($v0)
# Save string instance
sw $v0, 8($fp)
# Final abort message
lw $a0, 8($fp)
# Final abort message
lw $a1, 4($fp)
# Final abort message
jal __concat
# Final abort message
sw $v0, 12($fp)
# Print abort info
lw $a0, 12($fp)
# Getting the String address
lw $a0, 4($a0)
# 4 System call code for print string
addi $v0, $zero, 4
syscall
# Object Abort Node
addi $v0, $zero, 10
# Object Abort Node
syscall
# Func Declaration Node
li $v0, 0
# Program Node
lw $ra, 0($sp)
# Program Node
lw $fp, 4($sp)
# Program Node
addi $sp, $sp, 8
# Program Node
addi $sp, $sp, 20
# Program Node
jr $ra
# Program Node
function_type_name_at_Object:
# Program Node
addi $sp, $sp, -4
# Program Node
move $t0, $sp
# Program Node
addi $sp, $sp, -8
# Program Node
sw $ra, 0($sp)
# Program Node
sw $fp, 4($sp)
# Program Node
move $fp, $t0
# Object Type Name Node
lw $t0, 4($fp)
# Object Type Name Node
lw $t0, 0($t0)
# Object Type Name Node
sw $t0, 0($fp)
# Object Type Name Node
lw $a0, 0($fp)
# Object Type Name Node
jal __type_name
# Object Type Name Node
sw $v0, 0($fp)
# Func Declaration Node
lw $v0, 0($fp)
# Program Node
lw $ra, 0($sp)
# Program Node
lw $fp, 4($sp)
# Program Node
addi $sp, $sp, 8
# Program Node
addi $sp, $sp, 8
# Program Node
jr $ra
# Program Node
function_copy_at_Object:
# Program Node
addi $sp, $sp, -4
# Program Node
move $t0, $sp
# Program Node
addi $sp, $sp, -8
# Program Node
sw $ra, 0($sp)
# Program Node
sw $fp, 4($sp)
# Program Node
move $fp, $t0
# Object Copy Node
lw $a0, 4($fp)
# Object Copy Node
jal __copy
# Object Copy Node
sw $v0, 0($fp)
# Func Declaration Node
lw $v0, 0($fp)
# Program Node
lw $ra, 0($sp)
# Program Node
lw $fp, 4($sp)
# Program Node
addi $sp, $sp, 8
# Program Node
addi $sp, $sp, 8
# Program Node
jr $ra
# Program Node
function_out_string_at_IO:
# Program Node
addi $sp, $sp, 0
# Program Node
move $t0, $sp
# Program Node
addi $sp, $sp, -8
# Program Node
sw $ra, 0($sp)
# Program Node
sw $fp, 4($sp)
# Program Node
move $fp, $t0
# IO Out String Node
lw $a0, 0($fp)
# Getting the String address
lw $a0, 4($a0)
# 4 System call code for print string
addi $v0, $zero, 4
syscall
# Func Declaration Node
lw $v0, 4($fp)
# Program Node
lw $ra, 0($sp)
# Program Node
lw $fp, 4($sp)
# Program Node
addi $sp, $sp, 8
# Program Node
addi $sp, $sp, 8
# Program Node
jr $ra
# Program Node
function_out_int_at_IO:
# Program Node
addi $sp, $sp, 0
# Program Node
move $t0, $sp
# Program Node
addi $sp, $sp, -8
# Program Node
sw $ra, 0($sp)
# Program Node
sw $fp, 4($sp)
# Program Node
move $fp, $t0
# IO Out Int Node
lw $a0, 0($fp)
# IO Out Int Node
addi $v0, $zero, 1
# IO Out Int Node
syscall
# Func Declaration Node
lw $v0, 4($fp)
# Program Node
lw $ra, 0($sp)
# Program Node
lw $fp, 4($sp)
# Program Node
addi $sp, $sp, 8
# Program Node
addi $sp, $sp, 8
# Program Node
jr $ra
# Program Node
function_in_string_at_IO:
# Program Node
addi $sp, $sp, -4
# Program Node
move $t0, $sp
# Program Node
addi $sp, $sp, -8
# Program Node
sw $ra, 0($sp)
# Program Node
sw $fp, 4($sp)
# Program Node
move $fp, $t0
# a1 = Allocated length Save the length in a1
li $a1, 1024
# Allocates 1024 bytes and return the address un v0
move $a0, $a1
# Allocates 1024 bytes and return the address un v0
li $v0, 9
# Allocates 1024 bytes and return the address un v0
syscall
# a0 = v0 Save the address in a0
move $a0, $v0
# 8 System call code for read string
addi $v0, $zero, 8
# Fills the address in a0 with the string
syscall
# a1 = a0 Save the address in a1
move $a1, $a0
# Type address into $a0
la $t0, String
# If String the is type and address
li $a0, 8
li $v0, 9
syscall
# Store String Type
sw $t0, 0($v0)
# Store String Address
sw $a1, 4($v0)
# a0 = v0 Get the string instance address
move $a0, $v0
addi $sp, $sp, -4
sw $ra, 0($sp)
# Remove last char
jal __remove_last_char
lw $ra, 0($sp)
addi $sp, $sp, 4
# Save the address in the final destination
sw $v0, 0($fp)
# Func Declaration Node
lw $v0, 0($fp)
# Program Node
lw $ra, 0($sp)
# Program Node
lw $fp, 4($sp)
# Program Node
addi $sp, $sp, 8
# Program Node
addi $sp, $sp, 8
# Program Node
jr $ra
# Program Node
function_in_int_at_IO:
# Program Node
addi $sp, $sp, -4
# Program Node
move $t0, $sp
# Program Node
addi $sp, $sp, -8
# Program Node
sw $ra, 0($sp)
# Program Node
sw $fp, 4($sp)
# Program Node
move $fp, $t0
# IO In Int Node
addi $v0, $zero, 5
# IO In Int Node
syscall
# IO In Int Node
sw $v0, 0($fp)
# Func Declaration Node
lw $v0, 0($fp)
# Program Node
lw $ra, 0($sp)
# Program Node
lw $fp, 4($sp)
# Program Node
addi $sp, $sp, 8
# Program Node
addi $sp, $sp, 8
# Program Node
jr $ra
# Init char at Main
__init_char_at_Main:
# Init char at Main
addi $sp, $sp, -4
# Init char at Main
move $t0, $sp
# Init char at Main
addi $sp, $sp, -8
# Init char at Main
sw $ra, 0($sp)
# Init char at Main
sw $fp, 4($sp)
# Init char at Main
move $fp, $t0
# String Node
la $t0, data_39
# Type address into $a0
la $t1, String
# If String the is type and address
li $a0, 8
li $v0, 9
syscall
# Store String Type
sw $t1, 0($v0)
# Store String Address
sw $t0, 4($v0)
# Save string instance
sw $v0, 0($fp)
# Attr Declaration Node
lw $t0, 4($fp)
# Attr Declaration Node
lw $t1, 0($fp)
# Attr Declaration Node
sw $t1, 4($t0)
# Init char at Main
lw $ra, 0($sp)
# Init char at Main
lw $fp, 4($sp)
# Init char at Main
addi $sp, $sp, 8
# Init char at Main
addi $sp, $sp, 8
# Init char at Main
jr $ra
# Init avar at Main
__init_avar_at_Main:
# Init avar at Main
addi $sp, $sp, -4
# Init avar at Main
move $t0, $sp
# Init avar at Main
addi $sp, $sp, -8
# Init avar at Main
sw $ra, 0($sp)
# Init avar at Main
sw $fp, 4($sp)
# Init avar at Main
move $fp, $t0
# Instantiate Node
sw $zero, 0($fp)
# Attr Declaration Node
lw $t0, 4($fp)
# Attr Declaration Node
lw $t1, 0($fp)
# Attr Declaration Node
sw $t1, 8($t0)
# Init avar at Main
lw $ra, 0($sp)
# Init avar at Main
lw $fp, 4($sp)
# Init avar at Main
addi $sp, $sp, 8
# Init avar at Main
addi $sp, $sp, 8
# Init avar at Main
jr $ra
# Init a_var at Main
__init_a_var_at_Main:
# Init a_var at Main
addi $sp, $sp, -4
# Init a_var at Main
move $t0, $sp
# Init a_var at Main
addi $sp, $sp, -8
# Init a_var at Main
sw $ra, 0($sp)
# Init a_var at Main
sw $fp, 4($sp)
# Init a_var at Main
move $fp, $t0
# Instantiate Node
sw $zero, 0($fp)
# Attr Declaration Node
lw $t0, 4($fp)
# Attr Declaration Node
lw $t1, 0($fp)
# Attr Declaration Node
sw $t1, 12($t0)
# Init a_var at Main
lw $ra, 0($sp)
# Init a_var at Main
lw $fp, 4($sp)
# Init a_var at Main
addi $sp, $sp, 8
# Init a_var at Main
addi $sp, $sp, 8
# Init a_var at Main
jr $ra
# Init flag at Main
__init_flag_at_Main:
# Init flag at Main
addi $sp, $sp, 0
# Init flag at Main
move $t0, $sp
# Init flag at Main
addi $sp, $sp, -8
# Init flag at Main
sw $ra, 0($sp)
# Init flag at Main
sw $fp, 4($sp)
# Init flag at Main
move $fp, $t0
# Attr Declaration Node
lw $t0, 0($fp)
# Attr Declaration Node
li $t1, 1
# Attr Declaration Node
sw $t1, 16($t0)
# Init flag at Main
lw $ra, 0($sp)
# Init flag at Main
lw $fp, 4($sp)
# Init flag at Main
addi $sp, $sp, 8
# Init flag at Main
addi $sp, $sp, 4
# Init flag at Main
jr $ra
# Program Node
function_menu_at_Main:
# Program Node
addi $sp, $sp, -324
# Program Node
move $t0, $sp
# Program Node
addi $sp, $sp, -8
# Program Node
sw $ra, 0($sp)
# Program Node
sw $fp, 4($sp)
# Program Node
move $fp, $t0
# String Node
la $t0, data_40
# Type address into $a0
la $t1, String
# If String the is type and address
li $a0, 8
li $v0, 9
syscall
# Store String Type
sw $t1, 0($v0)
# Store String Address
sw $t0, 4($v0)
# Save string instance
sw $v0, 4($fp)
# Call Node
lw $t0, 324($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 4($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 324($fp)
# Call Node
lw $t0, 0($t0)
# Call Node
sw $t0, 12($fp)
# Call Node
lw $t0, 12($fp)
# Call Node
lw $t0, 28($t0)
# Call Node
jal __get_ra
# Call Node
move $ra, $v0
# Call Node
jr $t0
# Call Node
sw $v0, 8($fp)
# Variable Node
lw $t0, 324($fp)
# Variable Node
lw $t0, 8($t0)
# Variable Node
sw $t0, 16($fp)
# Call Node
lw $t0, 324($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 16($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 324($fp)
# Call Node
lw $t0, 0($t0)
# Call Node
sw $t0, 24($fp)
# Call Node
lw $t0, 24($fp)
# Call Node
lw $t0, 80($t0)
# Call Node
jal __get_ra
# Call Node
move $ra, $v0
# Call Node
jr $t0
# Call Node
sw $v0, 20($fp)
# String Node
la $t0, data_41
# Type address into $a0
la $t1, String
# If String the is type and address
li $a0, 8
li $v0, 9
syscall
# Store String Type
sw $t1, 0($v0)
# Store String Address
sw $t0, 4($v0)
# Save string instance
sw $v0, 28($fp)
# Call Node
lw $t0, 324($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 28($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 324($fp)
# Call Node
lw $t0, 0($t0)
# Call Node
sw $t0, 36($fp)
# Call Node
lw $t0, 36($fp)
# Call Node
lw $t0, 28($t0)
# Call Node
jal __get_ra
# Call Node
move $ra, $v0
# Call Node
jr $t0
# Call Node
sw $v0, 32($fp)
# String Node
la $t0, data_42
# Type address into $a0
la $t1, String
# If String the is type and address
li $a0, 8
li $v0, 9
syscall
# Store String Type
sw $t1, 0($v0)
# Store String Address
sw $t0, 4($v0)
# Save string instance
sw $v0, 40($fp)
# Call Node
lw $t0, 324($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 40($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 324($fp)
# Call Node
lw $t0, 0($t0)
# Call Node
sw $t0, 48($fp)
# Call Node
lw $t0, 48($fp)
# Call Node
lw $t0, 28($t0)
# Call Node
jal __get_ra
# Call Node
move $ra, $v0
# Call Node
jr $t0
# Call Node
sw $v0, 44($fp)
# Variable Node
lw $t0, 324($fp)
# Variable Node
lw $t0, 8($t0)
# Variable Node
sw $t0, 52($fp)
# Call Node
lw $t0, 324($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 52($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 324($fp)
# Call Node
lw $t0, 0($t0)
# Call Node
sw $t0, 60($fp)
# Call Node
lw $t0, 60($fp)
# Call Node
lw $t0, 80($t0)
# Call Node
jal __get_ra
# Call Node
move $ra, $v0
# Call Node
jr $t0
# Call Node
sw $v0, 56($fp)
# String Node
la $t0, data_43
# Type address into $a0
la $t1, String
# If String the is type and address
li $a0, 8
li $v0, 9
syscall
# Store String Type
sw $t1, 0($v0)
# Store String Address
sw $t0, 4($v0)
# Save string instance
sw $v0, 64($fp)
# Call Node
lw $t0, 324($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 64($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 324($fp)
# Call Node
lw $t0, 0($t0)
# Call Node
sw $t0, 72($fp)
# Call Node
lw $t0, 72($fp)
# Call Node
lw $t0, 28($t0)
# Call Node
jal __get_ra
# Call Node
move $ra, $v0
# Call Node
jr $t0
# Call Node
sw $v0, 68($fp)
# String Node
la $t0, data_44
# Type address into $a0
la $t1, String
# If String the is type and address
li $a0, 8
li $v0, 9
syscall
# Store String Type
sw $t1, 0($v0)
# Store String Address
sw $t0, 4($v0)
# Save string instance
sw $v0, 76($fp)
# Call Node
lw $t0, 324($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 76($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 324($fp)
# Call Node
lw $t0, 0($t0)
# Call Node
sw $t0, 84($fp)
# Call Node
lw $t0, 84($fp)
# Call Node
lw $t0, 28($t0)
# Call Node
jal __get_ra
# Call Node
move $ra, $v0
# Call Node
jr $t0
# Call Node
sw $v0, 80($fp)
# Variable Node
lw $t0, 324($fp)
# Variable Node
lw $t0, 8($t0)
# Variable Node
sw $t0, 88($fp)
# Call Node
lw $t0, 324($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 88($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 324($fp)
# Call Node
lw $t0, 0($t0)
# Call Node
sw $t0, 96($fp)
# Call Node
lw $t0, 96($fp)
# Call Node
lw $t0, 80($t0)
# Call Node
jal __get_ra
# Call Node
move $ra, $v0
# Call Node
jr $t0
# Call Node
sw $v0, 92($fp)
# String Node
la $t0, data_45
# Type address into $a0
la $t1, String
# If String the is type and address
li $a0, 8
li $v0, 9
syscall
# Store String Type
sw $t1, 0($v0)
# Store String Address
sw $t0, 4($v0)
# Save string instance
sw $v0, 100($fp)
# Call Node
lw $t0, 324($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 100($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 324($fp)
# Call Node
lw $t0, 0($t0)
# Call Node
sw $t0, 108($fp)
# Call Node
lw $t0, 108($fp)
# Call Node
lw $t0, 28($t0)
# Call Node
jal __get_ra
# Call Node
move $ra, $v0
# Call Node
jr $t0
# Call Node
sw $v0, 104($fp)
# String Node
la $t0, data_46
# Type address into $a0
la $t1, String
# If String the is type and address
li $a0, 8
li $v0, 9
syscall
# Store String Type
sw $t1, 0($v0)
# Store String Address
sw $t0, 4($v0)
# Save string instance
sw $v0, 112($fp)
# Call Node
lw $t0, 324($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 112($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 324($fp)
# Call Node
lw $t0, 0($t0)
# Call Node
sw $t0, 120($fp)
# Call Node
lw $t0, 120($fp)
# Call Node
lw $t0, 28($t0)
# Call Node
jal __get_ra
# Call Node
move $ra, $v0
# Call Node
jr $t0
# Call Node
sw $v0, 116($fp)
# Variable Node
lw $t0, 324($fp)
# Variable Node
lw $t0, 8($t0)
# Variable Node
sw $t0, 124($fp)
# Call Node
lw $t0, 324($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 124($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 324($fp)
# Call Node
lw $t0, 0($t0)
# Call Node
sw $t0, 132($fp)
# Call Node
lw $t0, 132($fp)
# Call Node
lw $t0, 80($t0)
# Call Node
jal __get_ra
# Call Node
move $ra, $v0
# Call Node
jr $t0
# Call Node
sw $v0, 128($fp)
# String Node
la $t0, data_47
# Type address into $a0
la $t1, String
# If String the is type and address
li $a0, 8
li $v0, 9
syscall
# Store String Type
sw $t1, 0($v0)
# Store String Address
sw $t0, 4($v0)
# Save string instance
sw $v0, 136($fp)
# Call Node
lw $t0, 324($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 136($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 324($fp)
# Call Node
lw $t0, 0($t0)
# Call Node
sw $t0, 144($fp)
# Call Node
lw $t0, 144($fp)
# Call Node
lw $t0, 28($t0)
# Call Node
jal __get_ra
# Call Node
move $ra, $v0
# Call Node
jr $t0
# Call Node
sw $v0, 140($fp)
# String Node
la $t0, data_48
# Type address into $a0
la $t1, String
# If String the is type and address
li $a0, 8
li $v0, 9
syscall
# Store String Type
sw $t1, 0($v0)
# Store String Address
sw $t0, 4($v0)
# Save string instance
sw $v0, 148($fp)
# Call Node
lw $t0, 324($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 148($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 324($fp)
# Call Node
lw $t0, 0($t0)
# Call Node
sw $t0, 156($fp)
# Call Node
lw $t0, 156($fp)
# Call Node
lw $t0, 28($t0)
# Call Node
jal __get_ra
# Call Node
move $ra, $v0
# Call Node
jr $t0
# Call Node
sw $v0, 152($fp)
# Variable Node
lw $t0, 324($fp)
# Variable Node
lw $t0, 8($t0)
# Variable Node
sw $t0, 160($fp)
# Call Node
lw $t0, 324($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 160($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 324($fp)
# Call Node
lw $t0, 0($t0)
# Call Node
sw $t0, 168($fp)
# Call Node
lw $t0, 168($fp)
# Call Node
lw $t0, 80($t0)
# Call Node
jal __get_ra
# Call Node
move $ra, $v0
# Call Node
jr $t0
# Call Node
sw $v0, 164($fp)
# String Node
la $t0, data_49
# Type address into $a0
la $t1, String
# If String the is type and address
li $a0, 8
li $v0, 9
syscall
# Store String Type
sw $t1, 0($v0)
# Store String Address
sw $t0, 4($v0)
# Save string instance
sw $v0, 172($fp)
# Call Node
lw $t0, 324($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 172($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 324($fp)
# Call Node
lw $t0, 0($t0)
# Call Node
sw $t0, 180($fp)
# Call Node
lw $t0, 180($fp)
# Call Node
lw $t0, 28($t0)
# Call Node
jal __get_ra
# Call Node
move $ra, $v0
# Call Node
jr $t0
# Call Node
sw $v0, 176($fp)
# String Node
la $t0, data_50
# Type address into $a0
la $t1, String
# If String the is type and address
li $a0, 8
li $v0, 9
syscall
# Store String Type
sw $t1, 0($v0)
# Store String Address
sw $t0, 4($v0)
# Save string instance
sw $v0, 184($fp)
# Call Node
lw $t0, 324($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 184($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 324($fp)
# Call Node
lw $t0, 0($t0)
# Call Node
sw $t0, 192($fp)
# Call Node
lw $t0, 192($fp)
# Call Node
lw $t0, 28($t0)
# Call Node
jal __get_ra
# Call Node
move $ra, $v0
# Call Node
jr $t0
# Call Node
sw $v0, 188($fp)
# Variable Node
lw $t0, 324($fp)
# Variable Node
lw $t0, 8($t0)
# Variable Node
sw $t0, 196($fp)
# Call Node
lw $t0, 324($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 196($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 324($fp)
# Call Node
lw $t0, 0($t0)
# Call Node
sw $t0, 204($fp)
# Call Node
lw $t0, 204($fp)
# Call Node
lw $t0, 80($t0)
# Call Node
jal __get_ra
# Call Node
move $ra, $v0
# Call Node
jr $t0
# Call Node
sw $v0, 200($fp)
# String Node
la $t0, data_51
# Type address into $a0
la $t1, String
# If String the is type and address
li $a0, 8
li $v0, 9
syscall
# Store String Type
sw $t1, 0($v0)
# Store String Address
sw $t0, 4($v0)
# Save string instance
sw $v0, 208($fp)
# Call Node
lw $t0, 324($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 208($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 324($fp)
# Call Node
lw $t0, 0($t0)
# Call Node
sw $t0, 216($fp)
# Call Node
lw $t0, 216($fp)
# Call Node
lw $t0, 28($t0)
# Call Node
jal __get_ra
# Call Node
move $ra, $v0
# Call Node
jr $t0
# Call Node
sw $v0, 212($fp)
# String Node
la $t0, data_52
# Type address into $a0
la $t1, String
# If String the is type and address
li $a0, 8
li $v0, 9
syscall
# Store String Type
sw $t1, 0($v0)
# Store String Address
sw $t0, 4($v0)
# Save string instance
sw $v0, 220($fp)
# Call Node
lw $t0, 324($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 220($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 324($fp)
# Call Node
lw $t0, 0($t0)
# Call Node
sw $t0, 228($fp)
# Call Node
lw $t0, 228($fp)
# Call Node
lw $t0, 28($t0)
# Call Node
jal __get_ra
# Call Node
move $ra, $v0
# Call Node
jr $t0
# Call Node
sw $v0, 224($fp)
# Variable Node
lw $t0, 324($fp)
# Variable Node
lw $t0, 8($t0)
# Variable Node
sw $t0, 232($fp)
# Call Node
lw $t0, 324($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 232($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 324($fp)
# Call Node
lw $t0, 0($t0)
# Call Node
sw $t0, 240($fp)
# Call Node
lw $t0, 240($fp)
# Call Node
lw $t0, 80($t0)
# Call Node
jal __get_ra
# Call Node
move $ra, $v0
# Call Node
jr $t0
# Call Node
sw $v0, 236($fp)
# String Node
la $t0, data_53
# Type address into $a0
la $t1, String
# If String the is type and address
li $a0, 8
li $v0, 9
syscall
# Store String Type
sw $t1, 0($v0)
# Store String Address
sw $t0, 4($v0)
# Save string instance
sw $v0, 244($fp)
# Call Node
lw $t0, 324($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 244($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 324($fp)
# Call Node
lw $t0, 0($t0)
# Call Node
sw $t0, 252($fp)
# Call Node
lw $t0, 252($fp)
# Call Node
lw $t0, 28($t0)
# Call Node
jal __get_ra
# Call Node
move $ra, $v0
# Call Node
jr $t0
# Call Node
sw $v0, 248($fp)
# String Node
la $t0, data_54
# Type address into $a0
la $t1, String
# If String the is type and address
li $a0, 8
li $v0, 9
syscall
# Store String Type
sw $t1, 0($v0)
# Store String Address
sw $t0, 4($v0)
# Save string instance
sw $v0, 256($fp)
# Call Node
lw $t0, 324($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 256($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 324($fp)
# Call Node
lw $t0, 0($t0)
# Call Node
sw $t0, 264($fp)
# Call Node
lw $t0, 264($fp)
# Call Node
lw $t0, 28($t0)
# Call Node
jal __get_ra
# Call Node
move $ra, $v0
# Call Node
jr $t0
# Call Node
sw $v0, 260($fp)
# Variable Node
lw $t0, 324($fp)
# Variable Node
lw $t0, 8($t0)
# Variable Node
sw $t0, 268($fp)
# Call Node
lw $t0, 324($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 268($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 324($fp)
# Call Node
lw $t0, 0($t0)
# Call Node
sw $t0, 276($fp)
# Call Node
lw $t0, 276($fp)
# Call Node
lw $t0, 80($t0)
# Call Node
jal __get_ra
# Call Node
move $ra, $v0
# Call Node
jr $t0
# Call Node
sw $v0, 272($fp)
# String Node
la $t0, data_55
# Type address into $a0
la $t1, String
# If String the is type and address
li $a0, 8
li $v0, 9
syscall
# Store String Type
sw $t1, 0($v0)
# Store String Address
sw $t0, 4($v0)
# Save string instance
sw $v0, 280($fp)
# Call Node
lw $t0, 324($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 280($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 324($fp)
# Call Node
lw $t0, 0($t0)
# Call Node
sw $t0, 288($fp)
# Call Node
lw $t0, 288($fp)
# Call Node
lw $t0, 28($t0)
# Call Node
jal __get_ra
# Call Node
move $ra, $v0
# Call Node
jr $t0
# Call Node
sw $v0, 284($fp)
# String Node
la $t0, data_56
# Type address into $a0
la $t1, String
# If String the is type and address
li $a0, 8
li $v0, 9
syscall
# Store String Type
sw $t1, 0($v0)
# Store String Address
sw $t0, 4($v0)
# Save string instance
sw $v0, 292($fp)
# Call Node
lw $t0, 324($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 292($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 324($fp)
# Call Node
lw $t0, 0($t0)
# Call Node
sw $t0, 300($fp)
# Call Node
lw $t0, 300($fp)
# Call Node
lw $t0, 28($t0)
# Call Node
jal __get_ra
# Call Node
move $ra, $v0
# Call Node
jr $t0
# Call Node
sw $v0, 296($fp)
# String Node
la $t0, data_57
# Type address into $a0
la $t1, String
# If String the is type and address
li $a0, 8
li $v0, 9
syscall
# Store String Type
sw $t1, 0($v0)
# Store String Address
sw $t0, 4($v0)
# Save string instance
sw $v0, 304($fp)
# Call Node
lw $t0, 324($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 304($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 324($fp)
# Call Node
lw $t0, 0($t0)
# Call Node
sw $t0, 312($fp)
# Call Node
lw $t0, 312($fp)
# Call Node
lw $t0, 28($t0)
# Call Node
jal __get_ra
# Call Node
move $ra, $v0
# Call Node
jr $t0
# Call Node
sw $v0, 308($fp)
# Call Node
lw $t0, 324($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 324($fp)
# Call Node
lw $t0, 0($t0)
# Call Node
sw $t0, 320($fp)
# Call Node
lw $t0, 320($fp)
# Call Node
lw $t0, 36($t0)
# Call Node
jal __get_ra
# Call Node
move $ra, $v0
# Call Node
jr $t0
# Call Node
sw $v0, 316($fp)
# Func Declaration Node
lw $v0, 316($fp)
# Program Node
lw $ra, 0($sp)
# Program Node
lw $fp, 4($sp)
# Program Node
addi $sp, $sp, 8
# Program Node
addi $sp, $sp, 328
# Program Node
jr $ra
# Program Node
function_prompt_at_Main:
# Program Node
addi $sp, $sp, -36
# Program Node
move $t0, $sp
# Program Node
addi $sp, $sp, -8
# Program Node
sw $ra, 0($sp)
# Program Node
sw $fp, 4($sp)
# Program Node
move $fp, $t0
# String Node
la $t0, data_58
# Type address into $a0
la $t1, String
# If String the is type and address
li $a0, 8
li $v0, 9
syscall
# Store String Type
sw $t1, 0($v0)
# Store String Address
sw $t0, 4($v0)
# Save string instance
sw $v0, 4($fp)
# Call Node
lw $t0, 36($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 4($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 36($fp)
# Call Node
lw $t0, 0($t0)
# Call Node
sw $t0, 12($fp)
# Call Node
lw $t0, 12($fp)
# Call Node
lw $t0, 28($t0)
# Call Node
jal __get_ra
# Call Node
move $ra, $v0
# Call Node
jr $t0
# Call Node
sw $v0, 8($fp)
# String Node
la $t0, data_59
# Type address into $a0
la $t1, String
# If String the is type and address
li $a0, 8
li $v0, 9
syscall
# Store String Type
sw $t1, 0($v0)
# Store String Address
sw $t0, 4($v0)
# Save string instance
sw $v0, 16($fp)
# Call Node
lw $t0, 36($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 16($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 36($fp)
# Call Node
lw $t0, 0($t0)
# Call Node
sw $t0, 24($fp)
# Call Node
lw $t0, 24($fp)
# Call Node
lw $t0, 28($t0)
# Call Node
jal __get_ra
# Call Node
move $ra, $v0
# Call Node
jr $t0
# Call Node
sw $v0, 20($fp)
# Call Node
lw $t0, 36($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 36($fp)
# Call Node
lw $t0, 0($t0)
# Call Node
sw $t0, 32($fp)
# Call Node
lw $t0, 32($fp)
# Call Node
lw $t0, 36($t0)
# Call Node
jal __get_ra
# Call Node
move $ra, $v0
# Call Node
jr $t0
# Call Node
sw $v0, 28($fp)
# Func Declaration Node
lw $v0, 28($fp)
# Program Node
lw $ra, 0($sp)
# Program Node
lw $fp, 4($sp)
# Program Node
addi $sp, $sp, 8
# Program Node
addi $sp, $sp, 40
# Program Node
jr $ra
# Program Node
function_get_int_at_Main:
# Program Node
addi $sp, $sp, -32
# Program Node
move $t0, $sp
# Program Node
addi $sp, $sp, -8
# Program Node
sw $ra, 0($sp)
# Program Node
sw $fp, 4($sp)
# Program Node
move $fp, $t0
# Instantiate Node
la $a0, A2I
# Instantiate Node
lw $a0, 4($a0)
li $v0, 9
syscall
sw $v0, 8($fp)
# Instantiate Node
lw $t0, 8($fp)
# Instantiate Node
addi $sp, $sp, -4
# Instantiate Node
sw $t0, 0($sp)
# Instantiate Node
jal __init_A2I_type
# Instantiate Node
sw $v0, 8($fp)
# Var Declaration Node
lw $t0, 8($fp)
# Var Declaration Node
sw $t0, 4($fp)
# Call Node
lw $t0, 32($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 32($fp)
# Call Node
lw $t0, 0($t0)
# Call Node
sw $t0, 20($fp)
# Call Node
lw $t0, 20($fp)
# Call Node
lw $t0, 64($t0)
# Call Node
jal __get_ra
# Call Node
move $ra, $v0
# Call Node
jr $t0
# Call Node
sw $v0, 16($fp)
# Var Declaration Node
lw $t0, 16($fp)
# Var Declaration Node
sw $t0, 12($fp)
# Call Node
lw $t0, 4($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 12($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 4($fp)
# Call Node
lw $t0, 0($t0)
# Call Node
sw $t0, 28($fp)
# Call Node
lw $t0, 28($fp)
# Call Node
lw $t0, 36($t0)
# Call Node
jal __get_ra
# Call Node
move $ra, $v0
# Call Node
jr $t0
# Call Node
sw $v0, 24($fp)
# Func Declaration Node
lw $v0, 24($fp)
# Program Node
lw $ra, 0($sp)
# Program Node
lw $fp, 4($sp)
# Program Node
addi $sp, $sp, 8
# Program Node
addi $sp, $sp, 36
# Program Node
jr $ra
# Program Node
function_is_even_at_Main:
# Program Node
addi $sp, $sp, -52
# Program Node
move $t0, $sp
# Program Node
addi $sp, $sp, -8
# Program Node
sw $ra, 0($sp)
# Program Node
sw $fp, 4($sp)
# Program Node
move $fp, $t0
# Var Declaration Node
lw $t0, 52($fp)
# Var Declaration Node
sw $t0, 0($fp)
# Lesser Node
lw $t0, 0($fp)
# Lesser Node
li $t1, 0
# Lesser Node
slt $t2, $t0, $t1
# Lesser Node
sw $t2, 8($fp)
# Conditional Node
lw $t0, 8($fp)
# Conditional Node
bne $t0, $zero, is_even_at_Main_label_0
# Equal Node
li $t0, 0
# Equal Node
lw $t1, 0($fp)
# Equal Node
seq $t2, $t0, $t1
# Equal Node
sw $t2, 16($fp)
# Conditional Node
lw $t0, 16($fp)
# Conditional Node
bne $t0, $zero, is_even_at_Main_label_2
# Equal Node
li $t0, 1
# Equal Node
lw $t1, 0($fp)
# Equal Node
seq $t2, $t0, $t1
# Equal Node
sw $t2, 24($fp)
# Conditional Node
lw $t0, 24($fp)
# Conditional Node
bne $t0, $zero, is_even_at_Main_label_4
# Minus Node
lw $t0, 0($fp)
# Minus Node
li $t1, 2
# Minus Node
sub $t2, $t0, $t1
# Minus Node
sw $t2, 28($fp)
# Call Node
lw $t0, 56($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 28($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 56($fp)
# Call Node
lw $t0, 0($t0)
# Call Node
sw $t0, 36($fp)
# Call Node
lw $t0, 36($fp)
# Call Node
lw $t0, 72($t0)
# Call Node
jal __get_ra
# Call Node
move $ra, $v0
# Call Node
jr $t0
# Call Node
sw $v0, 32($fp)
# Conditional Node
lw $t0, 32($fp)
# Conditional Node
sw $t0, 20($fp)
# Conditional Node
j is_even_at_Main_label_5
# Conditional Node
is_even_at_Main_label_4:
# Conditional Node
li $t0, 0
# Conditional Node
sw $t0, 20($fp)
# Conditional Node
is_even_at_Main_label_5:
# Conditional Node
lw $t0, 20($fp)
# Conditional Node
sw $t0, 12($fp)
# Conditional Node
j is_even_at_Main_label_3
# Conditional Node
is_even_at_Main_label_2:
# Conditional Node
li $t0, 1
# Conditional Node
sw $t0, 12($fp)
# Conditional Node
is_even_at_Main_label_3:
# Conditional Node
lw $t0, 12($fp)
# Conditional Node
sw $t0, 4($fp)
# Conditional Node
j is_even_at_Main_label_1
# Conditional Node
is_even_at_Main_label_0:
# Roof Node
li $t0, 0
# Roof Node
lw $t1, 0($fp)
# Roof Node
sub $t2, $t0, $t1
# Roof Node
sw $t2, 40($fp)
# Call Node
lw $t0, 56($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 40($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 56($fp)
# Call Node
lw $t0, 0($t0)
# Call Node
sw $t0, 48($fp)
# Call Node
lw $t0, 48($fp)
# Call Node
lw $t0, 72($t0)
# Call Node
jal __get_ra
# Call Node
move $ra, $v0
# Call Node
jr $t0
# Call Node
sw $v0, 44($fp)
# Conditional Node
lw $t0, 44($fp)
# Conditional Node
sw $t0, 4($fp)
# Conditional Node
is_even_at_Main_label_1:
# Func Declaration Node
lw $v0, 4($fp)
# Program Node
lw $ra, 0($sp)
# Program Node
lw $fp, 4($sp)
# Program Node
addi $sp, $sp, 8
# Program Node
addi $sp, $sp, 60
# Program Node
jr $ra
# Program Node
function_class_type_at_Main:
# Program Node
addi $sp, $sp, -144
# Program Node
move $t0, $sp
# Program Node
addi $sp, $sp, -8
# Program Node
sw $ra, 0($sp)
# Program Node
sw $fp, 4($sp)
# Program Node
move $fp, $t0
# Case Node typeof value
lw $t0, 144($fp)
# Case Node typeof value
lw $t0, 0($t0)
# Case Node typeof value
sw $t0, 4($fp)
# Case Node array declaration
li $a0, 24
# Case Node array declaration
li $v0, 9
# Case Node array declaration
syscall
# Case Node array declaration
sw $v0, 8($fp)
# Case Node array setindex 0
li $t2, 0
# Case Node array setindex 0
la $t3, A
# Case Node array setindex 0
lw $t1, 8($fp)
# Case Node array setindex 0
add $t1, $t1, $t2
# Case Node array setindex 0
sw $t3, 0($t1)
# Case Node array setindex 1
li $t2, 4
# Case Node array setindex 1
la $t3, B
# Case Node array setindex 1
lw $t1, 8($fp)
# Case Node array setindex 1
add $t1, $t1, $t2
# Case Node array setindex 1
sw $t3, 0($t1)
# Case Node array setindex 2
li $t2, 8
# Case Node array setindex 2
la $t3, C
# Case Node array setindex 2
lw $t1, 8($fp)
# Case Node array setindex 2
add $t1, $t1, $t2
# Case Node array setindex 2
sw $t3, 0($t1)
# Case Node array setindex 3
li $t2, 12
# Case Node array setindex 3
la $t3, D
# Case Node array setindex 3
lw $t1, 8($fp)
# Case Node array setindex 3
add $t1, $t1, $t2
# Case Node array setindex 3
sw $t3, 0($t1)
# Case Node array setindex 4
li $t2, 16
# Case Node array setindex 4
la $t3, E
# Case Node array setindex 4
lw $t1, 8($fp)
# Case Node array setindex 4
add $t1, $t1, $t2
# Case Node array setindex 4
sw $t3, 0($t1)
# Case Node array setindex 5
li $t2, 20
# Case Node array setindex 5
la $t3, Object
# Case Node array setindex 5
lw $t1, 8($fp)
# Case Node array setindex 5
add $t1, $t1, $t2
# Case Node array setindex 5
sw $t3, 0($t1)
# Case Node assign index -1
li $t0, -1
# Case Node assign index -1
sw $t0, 12($fp)
# Case Node assign minim -2
li $t0, -2
# Case Node assign minim -2
sw $t0, 20($fp)
# Case Node start label
class_type_at_Main_label_0:
# Case Node plus index 1
lw $t0, 12($fp)
# Case Node plus index 1
li $t1, 1
# Case Node plus index 1
add $t2, $t0, $t1
# Case Node plus index 1
sw $t2, 12($fp)
# Case Node equal stop_for index checks
lw $t0, 12($fp)
# Case Node equal stop_for index checks
li $t1, 6
# Case Node equal stop_for index checks
seq $t2, $t0, $t1
# Case Node equal stop_for index checks
sw $t2, 32($fp)
# Case Node gotoif stop_for end_label
lw $t0, 32($fp)
# Case Node gotoif stop_for end_label
bne $t0, $zero, class_type_at_Main_label_2
# Case Node get_index array_types index
lw $t0, 12($fp)
# Case Node get_index array_types index
li $t2, 4
# Case Node get_index array_types index
mul $t2, $t2, $t0
# Case Node get_index array_types index
lw $t1, 8($fp)
# Case Node get_index array_types index
add $t1, $t1, $t2
# Case Node get_index array_types index
lw $t2, 0($t1)
# Case Node get_index array_types index
sw $t2, 28($fp)
# Case Node arg type_value
lw $t0, 4($fp)
# Case Node arg type_value
addi $sp, $sp, -4
# Case Node arg type_value
sw $t0, 0($sp)
# Case Node arg current_type
lw $t0, 28($fp)
# Case Node arg current_type
addi $sp, $sp, -4
# Case Node arg current_type
sw $t0, 0($sp)
# Case Node static_call type_distance
jal type_distance
# Case Node static_call type_distance
sw $v0, 24($fp)
# Case Node equal not_valid_distance distance -1
lw $t0, 24($fp)
# Case Node equal not_valid_distance distance -1
li $t1, -1
# Case Node equal not_valid_distance distance -1
seq $t2, $t0, $t1
# Case Node equal not_valid_distance distance -1
sw $t2, 36($fp)
# Case Node gotoif not_valid_distance start_label
lw $t0, 36($fp)
# Case Node gotoif not_valid_distance start_label
bne $t0, $zero, class_type_at_Main_label_0
# Case Node equal minim_cond minim -2
lw $t0, 20($fp)
# Case Node equal minim_cond minim -2
li $t1, -2
# Case Node equal minim_cond minim -2
seq $t2, $t0, $t1
# Case Node equal minim_cond minim -2
sw $t2, 40($fp)
# Case Node gotoif minim_cond minim_label
lw $t0, 40($fp)
# Case Node gotoif minim_cond minim_label
bne $t0, $zero, class_type_at_Main_label_1
# Case Node greater minim_cond minim distance
lw $t0, 20($fp)
# Case Node greater minim_cond minim distance
lw $t1, 24($fp)
# Case Node greater minim_cond minim distance
sgt $t2, $t0, $t1
# Case Node greater minim_cond minim distance
sw $t2, 40($fp)
# Case Node gotoif minim_cond minim_label
lw $t0, 40($fp)
# Case Node gotoif minim_cond minim_label
bne $t0, $zero, class_type_at_Main_label_1
# Case Node goto start_label
j class_type_at_Main_label_0
# Case Node minim label
class_type_at_Main_label_1:
# Case Node assign minim distance
lw $t0, 24($fp)
# Case Node assign minim distance
sw $t0, 20($fp)
# Case Node assign minim_index index
lw $t0, 12($fp)
# Case Node assign minim_index index
sw $t0, 16($fp)
# Case Node goto start_label
j class_type_at_Main_label_0
# Case Node end label
class_type_at_Main_label_2:
# Case Node equal minim_cond minim -2
lw $t0, 20($fp)
# Case Node equal minim_cond minim -2
li $t1, -2
# Case Node equal minim_cond minim -2
seq $t2, $t0, $t1
# Case Node equal minim_cond minim -2
sw $t2, 40($fp)
# Case Node gotoif minim_cond abort_label
lw $t0, 40($fp)
# Case Node gotoif minim_cond abort_label
bne $t0, $zero, class_type_at_Main_label_3
# Case Node get_index array_types minim_index
lw $t0, 16($fp)
# Case Node get_index array_types minim_index
li $t2, 4
# Case Node get_index array_types minim_index
mul $t2, $t2, $t0
# Case Node get_index array_types minim_index
lw $t1, 8($fp)
# Case Node get_index array_types minim_index
add $t1, $t1, $t2
# Case Node get_index array_types minim_index
lw $t2, 0($t1)
# Case Node get_index array_types minim_index
sw $t2, 28($fp)
# Case Node equal not_equal_types param.type.name current_type
la $t0, A
# Case Node equal not_equal_types param.type.name current_type
lw $t1, 28($fp)
# Case Node equal not_equal_types param.type.name current_type
seq $t2, $t0, $t1
# Case Node equal not_equal_types param.type.name current_type
sw $t2, 44($fp)
# Case Node not not_equal_types not_equal_types
lw $t0, 44($fp)
# Case Node not not_equal_types not_equal_types
seq $t0, $t0, $zero
# Case Node not not_equal_types not_equal_types
sw $t0, 44($fp)
# Case Node gotoif not_equal_types lbl.label
lw $t0, 44($fp)
# Case Node gotoif not_equal_types lbl.label
bne $t0, $zero, class_type_at_Main_label_5
# Check Node
lw $t0, 144($fp)
# Check Node
sw $t0, 48($fp)
# String Node
la $t0, data_60
# Type address into $a0
la $t1, String
# If String the is type and address
li $a0, 8
li $v0, 9
syscall
# Store String Type
sw $t1, 0($v0)
# Store String Address
sw $t0, 4($v0)
# Save string instance
sw $v0, 52($fp)
# Call Node
lw $t0, 148($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 52($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 148($fp)
# Call Node
lw $t0, 0($t0)
# Call Node
sw $t0, 60($fp)
# Call Node
lw $t0, 60($fp)
# Call Node
lw $t0, 28($t0)
# Call Node
jal __get_ra
# Call Node
move $ra, $v0
# Call Node
jr $t0
# Call Node
sw $v0, 56($fp)
# Case Node assign final_result result
lw $t0, 56($fp)
# Case Node assign final_result result
sw $t0, 0($fp)
# Case Node goto final_label
j class_type_at_Main_label_4
# Case Node end_label <cool.ast.cool_ast.CheckNode object at 0x0000020832620748>
class_type_at_Main_label_5:
# Case Node equal not_equal_types param.type.name current_type
la $t0, B
# Case Node equal not_equal_types param.type.name current_type
lw $t1, 28($fp)
# Case Node equal not_equal_types param.type.name current_type
seq $t2, $t0, $t1
# Case Node equal not_equal_types param.type.name current_type
sw $t2, 44($fp)
# Case Node not not_equal_types not_equal_types
lw $t0, 44($fp)
# Case Node not not_equal_types not_equal_types
seq $t0, $t0, $zero
# Case Node not not_equal_types not_equal_types
sw $t0, 44($fp)
# Case Node gotoif not_equal_types lbl.label
lw $t0, 44($fp)
# Case Node gotoif not_equal_types lbl.label
bne $t0, $zero, class_type_at_Main_label_6
# Check Node
lw $t0, 144($fp)
# Check Node
sw $t0, 64($fp)
# String Node
la $t0, data_61
# Type address into $a0
la $t1, String
# If String the is type and address
li $a0, 8
li $v0, 9
syscall
# Store String Type
sw $t1, 0($v0)
# Store String Address
sw $t0, 4($v0)
# Save string instance
sw $v0, 68($fp)
# Call Node
lw $t0, 148($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 68($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 148($fp)
# Call Node
lw $t0, 0($t0)
# Call Node
sw $t0, 76($fp)
# Call Node
lw $t0, 76($fp)
# Call Node
lw $t0, 28($t0)
# Call Node
jal __get_ra
# Call Node
move $ra, $v0
# Call Node
jr $t0
# Call Node
sw $v0, 72($fp)
# Case Node assign final_result result
lw $t0, 72($fp)
# Case Node assign final_result result
sw $t0, 0($fp)
# Case Node goto final_label
j class_type_at_Main_label_4
# Case Node end_label <cool.ast.cool_ast.CheckNode object at 0x00000208326207B8>
class_type_at_Main_label_6:
# Case Node equal not_equal_types param.type.name current_type
la $t0, C
# Case Node equal not_equal_types param.type.name current_type
lw $t1, 28($fp)
# Case Node equal not_equal_types param.type.name current_type
seq $t2, $t0, $t1
# Case Node equal not_equal_types param.type.name current_type
sw $t2, 44($fp)
# Case Node not not_equal_types not_equal_types
lw $t0, 44($fp)
# Case Node not not_equal_types not_equal_types
seq $t0, $t0, $zero
# Case Node not not_equal_types not_equal_types
sw $t0, 44($fp)
# Case Node gotoif not_equal_types lbl.label
lw $t0, 44($fp)
# Case Node gotoif not_equal_types lbl.label
bne $t0, $zero, class_type_at_Main_label_7
# Check Node
lw $t0, 144($fp)
# Check Node
sw $t0, 80($fp)
# String Node
la $t0, data_62
# Type address into $a0
la $t1, String
# If String the is type and address
li $a0, 8
li $v0, 9
syscall
# Store String Type
sw $t1, 0($v0)
# Store String Address
sw $t0, 4($v0)
# Save string instance
sw $v0, 84($fp)
# Call Node
lw $t0, 148($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 84($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 148($fp)
# Call Node
lw $t0, 0($t0)
# Call Node
sw $t0, 92($fp)
# Call Node
lw $t0, 92($fp)
# Call Node
lw $t0, 28($t0)
# Call Node
jal __get_ra
# Call Node
move $ra, $v0
# Call Node
jr $t0
# Call Node
sw $v0, 88($fp)
# Case Node assign final_result result
lw $t0, 88($fp)
# Case Node assign final_result result
sw $t0, 0($fp)
# Case Node goto final_label
j class_type_at_Main_label_4
# Case Node end_label <cool.ast.cool_ast.CheckNode object at 0x00000208326207F0>
class_type_at_Main_label_7:
# Case Node equal not_equal_types param.type.name current_type
la $t0, D
# Case Node equal not_equal_types param.type.name current_type
lw $t1, 28($fp)
# Case Node equal not_equal_types param.type.name current_type
seq $t2, $t0, $t1
# Case Node equal not_equal_types param.type.name current_type
sw $t2, 44($fp)
# Case Node not not_equal_types not_equal_types
lw $t0, 44($fp)
# Case Node not not_equal_types not_equal_types
seq $t0, $t0, $zero
# Case Node not not_equal_types not_equal_types
sw $t0, 44($fp)
# Case Node gotoif not_equal_types lbl.label
lw $t0, 44($fp)
# Case Node gotoif not_equal_types lbl.label
bne $t0, $zero, class_type_at_Main_label_8
# Check Node
lw $t0, 144($fp)
# Check Node
sw $t0, 96($fp)
# String Node
la $t0, data_63
# Type address into $a0
la $t1, String
# If String the is type and address
li $a0, 8
li $v0, 9
syscall
# Store String Type
sw $t1, 0($v0)
# Store String Address
sw $t0, 4($v0)
# Save string instance
sw $v0, 100($fp)
# Call Node
lw $t0, 148($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 100($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 148($fp)
# Call Node
lw $t0, 0($t0)
# Call Node
sw $t0, 108($fp)
# Call Node
lw $t0, 108($fp)
# Call Node
lw $t0, 28($t0)
# Call Node
jal __get_ra
# Call Node
move $ra, $v0
# Call Node
jr $t0
# Call Node
sw $v0, 104($fp)
# Case Node assign final_result result
lw $t0, 104($fp)
# Case Node assign final_result result
sw $t0, 0($fp)
# Case Node goto final_label
j class_type_at_Main_label_4
# Case Node end_label <cool.ast.cool_ast.CheckNode object at 0x0000020832620860>
class_type_at_Main_label_8:
# Case Node equal not_equal_types param.type.name current_type
la $t0, E
# Case Node equal not_equal_types param.type.name current_type
lw $t1, 28($fp)
# Case Node equal not_equal_types param.type.name current_type
seq $t2, $t0, $t1
# Case Node equal not_equal_types param.type.name current_type
sw $t2, 44($fp)
# Case Node not not_equal_types not_equal_types
lw $t0, 44($fp)
# Case Node not not_equal_types not_equal_types
seq $t0, $t0, $zero
# Case Node not not_equal_types not_equal_types
sw $t0, 44($fp)
# Case Node gotoif not_equal_types lbl.label
lw $t0, 44($fp)
# Case Node gotoif not_equal_types lbl.label
bne $t0, $zero, class_type_at_Main_label_9
# Check Node
lw $t0, 144($fp)
# Check Node
sw $t0, 112($fp)
# String Node
la $t0, data_64
# Type address into $a0
la $t1, String
# If String the is type and address
li $a0, 8
li $v0, 9
syscall
# Store String Type
sw $t1, 0($v0)
# Store String Address
sw $t0, 4($v0)
# Save string instance
sw $v0, 116($fp)
# Call Node
lw $t0, 148($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 116($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 148($fp)
# Call Node
lw $t0, 0($t0)
# Call Node
sw $t0, 124($fp)
# Call Node
lw $t0, 124($fp)
# Call Node
lw $t0, 28($t0)
# Call Node
jal __get_ra
# Call Node
move $ra, $v0
# Call Node
jr $t0
# Call Node
sw $v0, 120($fp)
# Case Node assign final_result result
lw $t0, 120($fp)
# Case Node assign final_result result
sw $t0, 0($fp)
# Case Node goto final_label
j class_type_at_Main_label_4
# Case Node end_label <cool.ast.cool_ast.CheckNode object at 0x0000020832620908>
class_type_at_Main_label_9:
# Case Node equal not_equal_types param.type.name current_type
la $t0, Object
# Case Node equal not_equal_types param.type.name current_type
lw $t1, 28($fp)
# Case Node equal not_equal_types param.type.name current_type
seq $t2, $t0, $t1
# Case Node equal not_equal_types param.type.name current_type
sw $t2, 44($fp)
# Case Node not not_equal_types not_equal_types
lw $t0, 44($fp)
# Case Node not not_equal_types not_equal_types
seq $t0, $t0, $zero
# Case Node not not_equal_types not_equal_types
sw $t0, 44($fp)
# Case Node gotoif not_equal_types lbl.label
lw $t0, 44($fp)
# Case Node gotoif not_equal_types lbl.label
bne $t0, $zero, class_type_at_Main_label_10
# Check Node
lw $t0, 144($fp)
# Check Node
sw $t0, 128($fp)
# String Node
la $t0, data_65
# Type address into $a0
la $t1, String
# If String the is type and address
li $a0, 8
li $v0, 9
syscall
# Store String Type
sw $t1, 0($v0)
# Store String Address
sw $t0, 4($v0)
# Save string instance
sw $v0, 132($fp)
# Call Node
lw $t0, 148($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 132($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 148($fp)
# Call Node
lw $t0, 0($t0)
# Call Node
sw $t0, 140($fp)
# Call Node
lw $t0, 140($fp)
# Call Node
lw $t0, 28($t0)
# Call Node
jal __get_ra
# Call Node
move $ra, $v0
# Call Node
jr $t0
# Call Node
sw $v0, 136($fp)
# Case Node assign final_result result
lw $t0, 136($fp)
# Case Node assign final_result result
sw $t0, 0($fp)
# Case Node goto final_label
j class_type_at_Main_label_4
# Case Node end_label <cool.ast.cool_ast.CheckNode object at 0x0000020832620FD0>
class_type_at_Main_label_10:
# Case Node abort label
class_type_at_Main_label_3:
# Case Node abort
addi $v0, $zero, 10
# Case Node abort
syscall
# Case Node final_label
class_type_at_Main_label_4:
# Func Declaration Node
lw $v0, 0($fp)
# Program Node
lw $ra, 0($sp)
# Program Node
lw $fp, 4($sp)
# Program Node
addi $sp, $sp, 8
# Program Node
addi $sp, $sp, 152
# Program Node
jr $ra
# Program Node
function_print_at_Main:
# Program Node
addi $sp, $sp, -48
# Program Node
move $t0, $sp
# Program Node
addi $sp, $sp, -8
# Program Node
sw $ra, 0($sp)
# Program Node
sw $fp, 4($sp)
# Program Node
move $fp, $t0
# Instantiate Node
la $a0, A2I
# Instantiate Node
lw $a0, 4($a0)
li $v0, 9
syscall
sw $v0, 4($fp)
# Instantiate Node
lw $t0, 4($fp)
# Instantiate Node
addi $sp, $sp, -4
# Instantiate Node
sw $t0, 0($sp)
# Instantiate Node
jal __init_A2I_type
# Instantiate Node
sw $v0, 4($fp)
# Var Declaration Node
lw $t0, 4($fp)
# Var Declaration Node
sw $t0, 0($fp)
# Call Node
lw $t0, 48($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 48($fp)
# Call Node
lw $t0, 0($t0)
# Call Node
sw $t0, 16($fp)
# Call Node
lw $t0, 16($fp)
# Call Node
lw $t0, 32($t0)
# Call Node
jal __get_ra
# Call Node
move $ra, $v0
# Call Node
jr $t0
# Call Node
sw $v0, 12($fp)
# Call Node
lw $t0, 0($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 12($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 0($fp)
# Call Node
lw $t0, 0($t0)
# Call Node
sw $t0, 24($fp)
# Call Node
lw $t0, 24($fp)
# Call Node
lw $t0, 44($t0)
# Call Node
jal __get_ra
# Call Node
move $ra, $v0
# Call Node
jr $t0
# Call Node
sw $v0, 20($fp)
# Call Node
lw $t0, 52($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 20($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 52($fp)
# Call Node
lw $t0, 0($t0)
# Call Node
sw $t0, 32($fp)
# Call Node
lw $t0, 32($fp)
# Call Node
lw $t0, 28($t0)
# Call Node
jal __get_ra
# Call Node
move $ra, $v0
# Call Node
jr $t0
# Call Node
sw $v0, 28($fp)
# String Node
la $t0, data_66
# Type address into $a0
la $t1, String
# If String the is type and address
li $a0, 8
li $v0, 9
syscall
# Store String Type
sw $t1, 0($v0)
# Store String Address
sw $t0, 4($v0)
# Save string instance
sw $v0, 36($fp)
# Call Node
lw $t0, 52($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 36($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 52($fp)
# Call Node
lw $t0, 0($t0)
# Call Node
sw $t0, 44($fp)
# Call Node
lw $t0, 44($fp)
# Call Node
lw $t0, 28($t0)
# Call Node
jal __get_ra
# Call Node
move $ra, $v0
# Call Node
jr $t0
# Call Node
sw $v0, 40($fp)
# Func Declaration Node
lw $v0, 40($fp)
# Program Node
lw $ra, 0($sp)
# Program Node
lw $fp, 4($sp)
# Program Node
addi $sp, $sp, 8
# Program Node
addi $sp, $sp, 56
# Program Node
jr $ra
# Program Node
function_main_at_Main:
# Program Node
addi $sp, $sp, -876
# Program Node
move $t0, $sp
# Program Node
addi $sp, $sp, -8
# Program Node
sw $ra, 0($sp)
# Program Node
sw $fp, 4($sp)
# Program Node
move $fp, $t0
# Instantiate Node
la $a0, A
# Instantiate Node
lw $a0, 4($a0)
li $v0, 9
syscall
sw $v0, 4($fp)
# Instantiate Node
lw $t0, 4($fp)
# Instantiate Node
addi $sp, $sp, -4
# Instantiate Node
sw $t0, 0($sp)
# Instantiate Node
jal __init_A_type
# Instantiate Node
sw $v0, 4($fp)
# Assign Node
lw $t0, 876($fp)
# Assign Node
lw $t1, 4($fp)
# Assign Node
sw $t1, 8($t0)
# Void Node
sw $zero, 8($fp)
# While Node
main_at_Main_label_0:
# Variable Node
lw $t0, 876($fp)
# Variable Node
lw $t0, 16($t0)
# Variable Node
sw $t0, 12($fp)
# While Node
lw $t0, 12($fp)
# While Node
bne $t0, $zero, main_at_Main_label_1
# While Node
j main_at_Main_label_2
# While Node
main_at_Main_label_1:
# String Node
la $t0, data_67
# Type address into $a0
la $t1, String
# If String the is type and address
li $a0, 8
li $v0, 9
syscall
# Store String Type
sw $t1, 0($v0)
# Store String Address
sw $t0, 4($v0)
# Save string instance
sw $v0, 20($fp)
# Call Node
lw $t0, 876($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 20($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 876($fp)
# Call Node
lw $t0, 0($t0)
# Call Node
sw $t0, 28($fp)
# Call Node
lw $t0, 28($fp)
# Call Node
lw $t0, 28($t0)
# Call Node
jal __get_ra
# Call Node
move $ra, $v0
# Call Node
jr $t0
# Call Node
sw $v0, 24($fp)
# Variable Node
lw $t0, 876($fp)
# Variable Node
lw $t0, 8($t0)
# Variable Node
sw $t0, 32($fp)
# Call Node
lw $t0, 876($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 32($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 876($fp)
# Call Node
lw $t0, 0($t0)
# Call Node
sw $t0, 40($fp)
# Call Node
lw $t0, 40($fp)
# Call Node
lw $t0, 80($t0)
# Call Node
jal __get_ra
# Call Node
move $ra, $v0
# Call Node
jr $t0
# Call Node
sw $v0, 36($fp)
# Variable Node
lw $t0, 876($fp)
# Variable Node
lw $t0, 8($t0)
# Variable Node
sw $t0, 48($fp)
# Call Node
lw $t0, 48($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 48($fp)
# Call Node
lw $t0, 0($t0)
# Call Node
sw $t0, 56($fp)
# Call Node
lw $t0, 56($fp)
# Call Node
lw $t0, 32($t0)
# Call Node
jal __get_ra
# Call Node
move $ra, $v0
# Call Node
jr $t0
# Call Node
sw $v0, 52($fp)
# Call Node
lw $t0, 876($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 52($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 876($fp)
# Call Node
lw $t0, 0($t0)
# Call Node
sw $t0, 64($fp)
# Call Node
lw $t0, 64($fp)
# Call Node
lw $t0, 72($t0)
# Call Node
jal __get_ra
# Call Node
move $ra, $v0
# Call Node
jr $t0
# Call Node
sw $v0, 60($fp)
# Conditional Node
lw $t0, 60($fp)
# Conditional Node
bne $t0, $zero, main_at_Main_label_3
# String Node
la $t0, data_68
# Type address into $a0
la $t1, String
# If String the is type and address
li $a0, 8
li $v0, 9
syscall
# Store String Type
sw $t1, 0($v0)
# Store String Address
sw $t0, 4($v0)
# Save string instance
sw $v0, 68($fp)
# Call Node
lw $t0, 876($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 68($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 876($fp)
# Call Node
lw $t0, 0($t0)
# Call Node
sw $t0, 76($fp)
# Call Node
lw $t0, 76($fp)
# Call Node
lw $t0, 28($t0)
# Call Node
jal __get_ra
# Call Node
move $ra, $v0
# Call Node
jr $t0
# Call Node
sw $v0, 72($fp)
# Conditional Node
lw $t0, 72($fp)
# Conditional Node
sw $t0, 44($fp)
# Conditional Node
j main_at_Main_label_4
# Conditional Node
main_at_Main_label_3:
# String Node
la $t0, data_69
# Type address into $a0
la $t1, String
# If String the is type and address
li $a0, 8
li $v0, 9
syscall
# Store String Type
sw $t1, 0($v0)
# Store String Address
sw $t0, 4($v0)
# Save string instance
sw $v0, 80($fp)
# Call Node
lw $t0, 876($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 80($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 876($fp)
# Call Node
lw $t0, 0($t0)
# Call Node
sw $t0, 88($fp)
# Call Node
lw $t0, 88($fp)
# Call Node
lw $t0, 28($t0)
# Call Node
jal __get_ra
# Call Node
move $ra, $v0
# Call Node
jr $t0
# Call Node
sw $v0, 84($fp)
# Conditional Node
lw $t0, 84($fp)
# Conditional Node
sw $t0, 44($fp)
# Conditional Node
main_at_Main_label_4:
# Variable Node
lw $t0, 876($fp)
# Variable Node
lw $t0, 8($t0)
# Variable Node
sw $t0, 92($fp)
# Call Node
lw $t0, 876($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 92($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 876($fp)
# Call Node
lw $t0, 0($t0)
# Call Node
sw $t0, 100($fp)
# Call Node
lw $t0, 100($fp)
# Call Node
lw $t0, 76($t0)
# Call Node
jal __get_ra
# Call Node
move $ra, $v0
# Call Node
jr $t0
# Call Node
sw $v0, 96($fp)
# Call Node
lw $t0, 876($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 876($fp)
# Call Node
lw $t0, 0($t0)
# Call Node
sw $t0, 108($fp)
# Call Node
lw $t0, 108($fp)
# Call Node
lw $t0, 60($t0)
# Call Node
jal __get_ra
# Call Node
move $ra, $v0
# Call Node
jr $t0
# Call Node
sw $v0, 104($fp)
# Assign Node
lw $t0, 876($fp)
# Assign Node
lw $t1, 104($fp)
# Assign Node
sw $t1, 4($t0)
# Variable Node
lw $t0, 876($fp)
# Variable Node
lw $t0, 4($t0)
# Variable Node
sw $t0, 120($fp)
# String Node
la $t0, data_70
# Type address into $a0
la $t1, String
# If String the is type and address
li $a0, 8
li $v0, 9
syscall
# Store String Type
sw $t1, 0($v0)
# Store String Address
sw $t0, 4($v0)
# Save string instance
sw $v0, 124($fp)
# a0 = left object
lw $a0, 120($fp)
# a1 = right object
lw $a1, 124($fp)
addi $sp, $sp, -4
sw $ra, 0($sp)
jal __object_equal
lw $ra, 0($sp)
addi $sp, $sp, 4
# Saving equal result
sw $v0, 116($fp)
# Conditional Node
lw $t0, 116($fp)
# Conditional Node
bne $t0, $zero, main_at_Main_label_5
# Variable Node
lw $t0, 876($fp)
# Variable Node
lw $t0, 4($t0)
# Variable Node
sw $t0, 136($fp)
# String Node
la $t0, data_71
# Type address into $a0
la $t1, String
# If String the is type and address
li $a0, 8
li $v0, 9
syscall
# Store String Type
sw $t1, 0($v0)
# Store String Address
sw $t0, 4($v0)
# Save string instance
sw $v0, 140($fp)
# a0 = left object
lw $a0, 136($fp)
# a1 = right object
lw $a1, 140($fp)
addi $sp, $sp, -4
sw $ra, 0($sp)
jal __object_equal
lw $ra, 0($sp)
addi $sp, $sp, 4
# Saving equal result
sw $v0, 132($fp)
# Conditional Node
lw $t0, 132($fp)
# Conditional Node
bne $t0, $zero, main_at_Main_label_7
# Variable Node
lw $t0, 876($fp)
# Variable Node
lw $t0, 4($t0)
# Variable Node
sw $t0, 152($fp)
# String Node
la $t0, data_72
# Type address into $a0
la $t1, String
# If String the is type and address
li $a0, 8
li $v0, 9
syscall
# Store String Type
sw $t1, 0($v0)
# Store String Address
sw $t0, 4($v0)
# Save string instance
sw $v0, 156($fp)
# a0 = left object
lw $a0, 152($fp)
# a1 = right object
lw $a1, 156($fp)
addi $sp, $sp, -4
sw $ra, 0($sp)
jal __object_equal
lw $ra, 0($sp)
addi $sp, $sp, 4
# Saving equal result
sw $v0, 148($fp)
# Conditional Node
lw $t0, 148($fp)
# Conditional Node
bne $t0, $zero, main_at_Main_label_9
# Variable Node
lw $t0, 876($fp)
# Variable Node
lw $t0, 4($t0)
# Variable Node
sw $t0, 168($fp)
# String Node
la $t0, data_73
# Type address into $a0
la $t1, String
# If String the is type and address
li $a0, 8
li $v0, 9
syscall
# Store String Type
sw $t1, 0($v0)
# Store String Address
sw $t0, 4($v0)
# Save string instance
sw $v0, 172($fp)
# a0 = left object
lw $a0, 168($fp)
# a1 = right object
lw $a1, 172($fp)
addi $sp, $sp, -4
sw $ra, 0($sp)
jal __object_equal
lw $ra, 0($sp)
addi $sp, $sp, 4
# Saving equal result
sw $v0, 164($fp)
# Conditional Node
lw $t0, 164($fp)
# Conditional Node
bne $t0, $zero, main_at_Main_label_11
# Variable Node
lw $t0, 876($fp)
# Variable Node
lw $t0, 4($t0)
# Variable Node
sw $t0, 184($fp)
# String Node
la $t0, data_74
# Type address into $a0
la $t1, String
# If String the is type and address
li $a0, 8
li $v0, 9
syscall
# Store String Type
sw $t1, 0($v0)
# Store String Address
sw $t0, 4($v0)
# Save string instance
sw $v0, 188($fp)
# a0 = left object
lw $a0, 184($fp)
# a1 = right object
lw $a1, 188($fp)
addi $sp, $sp, -4
sw $ra, 0($sp)
jal __object_equal
lw $ra, 0($sp)
addi $sp, $sp, 4
# Saving equal result
sw $v0, 180($fp)
# Conditional Node
lw $t0, 180($fp)
# Conditional Node
bne $t0, $zero, main_at_Main_label_13
# Variable Node
lw $t0, 876($fp)
# Variable Node
lw $t0, 4($t0)
# Variable Node
sw $t0, 200($fp)
# String Node
la $t0, data_75
# Type address into $a0
la $t1, String
# If String the is type and address
li $a0, 8
li $v0, 9
syscall
# Store String Type
sw $t1, 0($v0)
# Store String Address
sw $t0, 4($v0)
# Save string instance
sw $v0, 204($fp)
# a0 = left object
lw $a0, 200($fp)
# a1 = right object
lw $a1, 204($fp)
addi $sp, $sp, -4
sw $ra, 0($sp)
jal __object_equal
lw $ra, 0($sp)
addi $sp, $sp, 4
# Saving equal result
sw $v0, 196($fp)
# Conditional Node
lw $t0, 196($fp)
# Conditional Node
bne $t0, $zero, main_at_Main_label_15
# Variable Node
lw $t0, 876($fp)
# Variable Node
lw $t0, 4($t0)
# Variable Node
sw $t0, 216($fp)
# String Node
la $t0, data_76
# Type address into $a0
la $t1, String
# If String the is type and address
li $a0, 8
li $v0, 9
syscall
# Store String Type
sw $t1, 0($v0)
# Store String Address
sw $t0, 4($v0)
# Save string instance
sw $v0, 220($fp)
# a0 = left object
lw $a0, 216($fp)
# a1 = right object
lw $a1, 220($fp)
addi $sp, $sp, -4
sw $ra, 0($sp)
jal __object_equal
lw $ra, 0($sp)
addi $sp, $sp, 4
# Saving equal result
sw $v0, 212($fp)
# Conditional Node
lw $t0, 212($fp)
# Conditional Node
bne $t0, $zero, main_at_Main_label_17
# Variable Node
lw $t0, 876($fp)
# Variable Node
lw $t0, 4($t0)
# Variable Node
sw $t0, 232($fp)
# String Node
la $t0, data_77
# Type address into $a0
la $t1, String
# If String the is type and address
li $a0, 8
li $v0, 9
syscall
# Store String Type
sw $t1, 0($v0)
# Store String Address
sw $t0, 4($v0)
# Save string instance
sw $v0, 236($fp)
# a0 = left object
lw $a0, 232($fp)
# a1 = right object
lw $a1, 236($fp)
addi $sp, $sp, -4
sw $ra, 0($sp)
jal __object_equal
lw $ra, 0($sp)
addi $sp, $sp, 4
# Saving equal result
sw $v0, 228($fp)
# Conditional Node
lw $t0, 228($fp)
# Conditional Node
bne $t0, $zero, main_at_Main_label_19
# Variable Node
lw $t0, 876($fp)
# Variable Node
lw $t0, 4($t0)
# Variable Node
sw $t0, 248($fp)
# String Node
la $t0, data_78
# Type address into $a0
la $t1, String
# If String the is type and address
li $a0, 8
li $v0, 9
syscall
# Store String Type
sw $t1, 0($v0)
# Store String Address
sw $t0, 4($v0)
# Save string instance
sw $v0, 252($fp)
# a0 = left object
lw $a0, 248($fp)
# a1 = right object
lw $a1, 252($fp)
addi $sp, $sp, -4
sw $ra, 0($sp)
jal __object_equal
lw $ra, 0($sp)
addi $sp, $sp, 4
# Saving equal result
sw $v0, 244($fp)
# Conditional Node
lw $t0, 244($fp)
# Conditional Node
bne $t0, $zero, main_at_Main_label_21
# Variable Node
lw $t0, 876($fp)
# Variable Node
lw $t0, 4($t0)
# Variable Node
sw $t0, 264($fp)
# String Node
la $t0, data_79
# Type address into $a0
la $t1, String
# If String the is type and address
li $a0, 8
li $v0, 9
syscall
# Store String Type
sw $t1, 0($v0)
# Store String Address
sw $t0, 4($v0)
# Save string instance
sw $v0, 268($fp)
# a0 = left object
lw $a0, 264($fp)
# a1 = right object
lw $a1, 268($fp)
addi $sp, $sp, -4
sw $ra, 0($sp)
jal __object_equal
lw $ra, 0($sp)
addi $sp, $sp, 4
# Saving equal result
sw $v0, 260($fp)
# Conditional Node
lw $t0, 260($fp)
# Conditional Node
bne $t0, $zero, main_at_Main_label_23
# Instantiate Node
la $a0, A
# Instantiate Node
lw $a0, 4($a0)
li $v0, 9
syscall
sw $v0, 272($fp)
# Instantiate Node
lw $t0, 272($fp)
# Instantiate Node
addi $sp, $sp, -4
# Instantiate Node
sw $t0, 0($sp)
# Instantiate Node
jal __init_A_type
# Instantiate Node
sw $v0, 272($fp)
# Variable Node
lw $t0, 876($fp)
# Variable Node
lw $t0, 8($t0)
# Variable Node
sw $t0, 276($fp)
# Call Node
lw $t0, 276($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 276($fp)
# Call Node
lw $t0, 0($t0)
# Call Node
sw $t0, 284($fp)
# Call Node
lw $t0, 284($fp)
# Call Node
lw $t0, 32($t0)
# Call Node
jal __get_ra
# Call Node
move $ra, $v0
# Call Node
jr $t0
# Call Node
sw $v0, 280($fp)
# Call Node
lw $t0, 272($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 280($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 272($fp)
# Call Node
lw $t0, 0($t0)
# Call Node
sw $t0, 292($fp)
# Call Node
lw $t0, 292($fp)
# Call Node
lw $t0, 40($t0)
# Call Node
jal __get_ra
# Call Node
move $ra, $v0
# Call Node
jr $t0
# Call Node
sw $v0, 288($fp)
# Assign Node
lw $t0, 876($fp)
# Assign Node
lw $t1, 288($fp)
# Assign Node
sw $t1, 8($t0)
# Conditional Node
lw $t0, 288($fp)
# Conditional Node
sw $t0, 256($fp)
# Conditional Node
j main_at_Main_label_24
# Conditional Node
main_at_Main_label_23:
# Assign Node
lw $t0, 876($fp)
# Assign Node
li $t1, 0
# Assign Node
sw $t1, 16($t0)
# Conditional Node
li $t0, 0
# Conditional Node
sw $t0, 256($fp)
# Conditional Node
main_at_Main_label_24:
# Conditional Node
lw $t0, 256($fp)
# Conditional Node
sw $t0, 240($fp)
# Conditional Node
j main_at_Main_label_22
# Conditional Node
main_at_Main_label_21:
# Instantiate Node
la $a0, A
# Instantiate Node
lw $a0, 4($a0)
li $v0, 9
syscall
sw $v0, 296($fp)
# Instantiate Node
lw $t0, 296($fp)
# Instantiate Node
addi $sp, $sp, -4
# Instantiate Node
sw $t0, 0($sp)
# Instantiate Node
jal __init_A_type
# Instantiate Node
sw $v0, 296($fp)
# Assign Node
lw $t0, 876($fp)
# Assign Node
lw $t1, 296($fp)
# Assign Node
sw $t1, 8($t0)
# Conditional Node
lw $t0, 296($fp)
# Conditional Node
sw $t0, 240($fp)
# Conditional Node
main_at_Main_label_22:
# Conditional Node
lw $t0, 240($fp)
# Conditional Node
sw $t0, 224($fp)
# Conditional Node
j main_at_Main_label_20
# Conditional Node
main_at_Main_label_19:
# Instantiate Node
sw $zero, 304($fp)
# Var Declaration Node
lw $t0, 304($fp)
# Var Declaration Node
sw $t0, 300($fp)
# Instantiate Node
la $a0, E
# Instantiate Node
lw $a0, 4($a0)
li $v0, 9
syscall
sw $v0, 312($fp)
# Instantiate Node
lw $t0, 312($fp)
# Instantiate Node
addi $sp, $sp, -4
# Instantiate Node
sw $t0, 0($sp)
# Instantiate Node
jal __init_E_type
# Instantiate Node
sw $v0, 312($fp)
# Variable Node
lw $t0, 876($fp)
# Variable Node
lw $t0, 8($t0)
# Variable Node
sw $t0, 316($fp)
# Call Node
lw $t0, 316($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 316($fp)
# Call Node
lw $t0, 0($t0)
# Call Node
sw $t0, 324($fp)
# Call Node
lw $t0, 324($fp)
# Call Node
lw $t0, 32($t0)
# Call Node
jal __get_ra
# Call Node
move $ra, $v0
# Call Node
jr $t0
# Call Node
sw $v0, 320($fp)
# Call Node
lw $t0, 312($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 320($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 312($fp)
# Call Node
lw $t0, 0($t0)
# Call Node
sw $t0, 332($fp)
# Call Node
lw $t0, 332($fp)
# Call Node
lw $t0, 64($t0)
# Call Node
jal __get_ra
# Call Node
move $ra, $v0
# Call Node
jr $t0
# Call Node
sw $v0, 328($fp)
# Assign Node
lw $t0, 328($fp)
# Assign Node
sw $t0, 300($fp)
# Variable Node
lw $t0, 876($fp)
# Variable Node
lw $t0, 8($t0)
# Variable Node
sw $t0, 340($fp)
# Call Node
lw $t0, 340($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 340($fp)
# Call Node
lw $t0, 0($t0)
# Call Node
sw $t0, 348($fp)
# Call Node
lw $t0, 348($fp)
# Call Node
lw $t0, 32($t0)
# Call Node
jal __get_ra
# Call Node
move $ra, $v0
# Call Node
jr $t0
# Call Node
sw $v0, 344($fp)
# Call Node
lw $t0, 300($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 300($fp)
# Call Node
lw $t0, 0($t0)
# Call Node
sw $t0, 356($fp)
# Call Node
lw $t0, 356($fp)
# Call Node
lw $t0, 32($t0)
# Call Node
jal __get_ra
# Call Node
move $ra, $v0
# Call Node
jr $t0
# Call Node
sw $v0, 352($fp)
# Star Node
lw $t0, 352($fp)
# Star Node
li $t1, 8
# Star Node
mul $t2, $t0, $t1
# Star Node
sw $t2, 360($fp)
# Minus Node
lw $t0, 344($fp)
# Minus Node
lw $t1, 360($fp)
# Minus Node
sub $t2, $t0, $t1
# Minus Node
sw $t2, 364($fp)
# Var Declaration Node
lw $t0, 364($fp)
# Var Declaration Node
sw $t0, 336($fp)
# String Node
la $t0, data_80
# Type address into $a0
la $t1, String
# If String the is type and address
li $a0, 8
li $v0, 9
syscall
# Store String Type
sw $t1, 0($v0)
# Store String Address
sw $t0, 4($v0)
# Save string instance
sw $v0, 372($fp)
# Call Node
lw $t0, 876($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 372($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 876($fp)
# Call Node
lw $t0, 0($t0)
# Call Node
sw $t0, 380($fp)
# Call Node
lw $t0, 380($fp)
# Call Node
lw $t0, 28($t0)
# Call Node
jal __get_ra
# Call Node
move $ra, $v0
# Call Node
jr $t0
# Call Node
sw $v0, 376($fp)
# Variable Node
lw $t0, 876($fp)
# Variable Node
lw $t0, 8($t0)
# Variable Node
sw $t0, 384($fp)
# Call Node
lw $t0, 876($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 384($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 876($fp)
# Call Node
lw $t0, 0($t0)
# Call Node
sw $t0, 392($fp)
# Call Node
lw $t0, 392($fp)
# Call Node
lw $t0, 80($t0)
# Call Node
jal __get_ra
# Call Node
move $ra, $v0
# Call Node
jr $t0
# Call Node
sw $v0, 388($fp)
# String Node
la $t0, data_81
# Type address into $a0
la $t1, String
# If String the is type and address
li $a0, 8
li $v0, 9
syscall
# Store String Type
sw $t1, 0($v0)
# Store String Address
sw $t0, 4($v0)
# Save string instance
sw $v0, 396($fp)
# Call Node
lw $t0, 876($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 396($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 876($fp)
# Call Node
lw $t0, 0($t0)
# Call Node
sw $t0, 404($fp)
# Call Node
lw $t0, 404($fp)
# Call Node
lw $t0, 28($t0)
# Call Node
jal __get_ra
# Call Node
move $ra, $v0
# Call Node
jr $t0
# Call Node
sw $v0, 400($fp)
# Call Node
lw $t0, 876($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 300($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 876($fp)
# Call Node
lw $t0, 0($t0)
# Call Node
sw $t0, 412($fp)
# Call Node
lw $t0, 412($fp)
# Call Node
lw $t0, 80($t0)
# Call Node
jal __get_ra
# Call Node
move $ra, $v0
# Call Node
jr $t0
# Call Node
sw $v0, 408($fp)
# String Node
la $t0, data_82
# Type address into $a0
la $t1, String
# If String the is type and address
li $a0, 8
li $v0, 9
syscall
# Store String Type
sw $t1, 0($v0)
# Store String Address
sw $t0, 4($v0)
# Save string instance
sw $v0, 416($fp)
# Call Node
lw $t0, 876($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 416($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 876($fp)
# Call Node
lw $t0, 0($t0)
# Call Node
sw $t0, 424($fp)
# Call Node
lw $t0, 424($fp)
# Call Node
lw $t0, 28($t0)
# Call Node
jal __get_ra
# Call Node
move $ra, $v0
# Call Node
jr $t0
# Call Node
sw $v0, 420($fp)
# Instantiate Node
la $a0, A2I
# Instantiate Node
lw $a0, 4($a0)
li $v0, 9
syscall
sw $v0, 432($fp)
# Instantiate Node
lw $t0, 432($fp)
# Instantiate Node
addi $sp, $sp, -4
# Instantiate Node
sw $t0, 0($sp)
# Instantiate Node
jal __init_A2I_type
# Instantiate Node
sw $v0, 432($fp)
# Var Declaration Node
lw $t0, 432($fp)
# Var Declaration Node
sw $t0, 428($fp)
# Call Node
lw $t0, 428($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 336($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 428($fp)
# Call Node
lw $t0, 0($t0)
# Call Node
sw $t0, 444($fp)
# Call Node
lw $t0, 444($fp)
# Call Node
lw $t0, 44($t0)
# Call Node
jal __get_ra
# Call Node
move $ra, $v0
# Call Node
jr $t0
# Call Node
sw $v0, 440($fp)
# Call Node
lw $t0, 876($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 440($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 876($fp)
# Call Node
lw $t0, 0($t0)
# Call Node
sw $t0, 452($fp)
# Call Node
lw $t0, 452($fp)
# Call Node
lw $t0, 28($t0)
# Call Node
jal __get_ra
# Call Node
move $ra, $v0
# Call Node
jr $t0
# Call Node
sw $v0, 448($fp)
# String Node
la $t0, data_83
# Type address into $a0
la $t1, String
# If String the is type and address
li $a0, 8
li $v0, 9
syscall
# Store String Type
sw $t1, 0($v0)
# Store String Address
sw $t0, 4($v0)
# Save string instance
sw $v0, 456($fp)
# Call Node
lw $t0, 876($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 456($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 876($fp)
# Call Node
lw $t0, 0($t0)
# Call Node
sw $t0, 464($fp)
# Call Node
lw $t0, 464($fp)
# Call Node
lw $t0, 28($t0)
# Call Node
jal __get_ra
# Call Node
move $ra, $v0
# Call Node
jr $t0
# Call Node
sw $v0, 460($fp)
# Assign Node
lw $t0, 876($fp)
# Assign Node
lw $t1, 300($fp)
# Assign Node
sw $t1, 8($t0)
# Conditional Node
lw $t0, 300($fp)
# Conditional Node
sw $t0, 224($fp)
# Conditional Node
main_at_Main_label_20:
# Conditional Node
lw $t0, 224($fp)
# Conditional Node
sw $t0, 208($fp)
# Conditional Node
j main_at_Main_label_18
# Conditional Node
main_at_Main_label_17:
# Instantiate Node
la $a0, D
# Instantiate Node
lw $a0, 4($a0)
li $v0, 9
syscall
sw $v0, 472($fp)
# Instantiate Node
lw $t0, 472($fp)
# Instantiate Node
addi $sp, $sp, -4
# Instantiate Node
sw $t0, 0($sp)
# Instantiate Node
jal __init_D_type
# Instantiate Node
sw $v0, 472($fp)
# Variable Node
lw $t0, 876($fp)
# Variable Node
lw $t0, 8($t0)
# Variable Node
sw $t0, 476($fp)
# Call Node
lw $t0, 476($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 476($fp)
# Call Node
lw $t0, 0($t0)
# Call Node
sw $t0, 484($fp)
# Call Node
lw $t0, 484($fp)
# Call Node
lw $t0, 32($t0)
# Call Node
jal __get_ra
# Call Node
move $ra, $v0
# Call Node
jr $t0
# Call Node
sw $v0, 480($fp)
# Call Node
lw $t0, 472($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 480($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 472($fp)
# Call Node
lw $t0, 0($t0)
# Call Node
sw $t0, 492($fp)
# Call Node
lw $t0, 492($fp)
# Call Node
lw $t0, 60($t0)
# Call Node
jal __get_ra
# Call Node
move $ra, $v0
# Call Node
jr $t0
# Call Node
sw $v0, 488($fp)
# Conditional Node
lw $t0, 488($fp)
# Conditional Node
bne $t0, $zero, main_at_Main_label_25
# String Node
la $t0, data_84
# Type address into $a0
la $t1, String
# If String the is type and address
li $a0, 8
li $v0, 9
syscall
# Store String Type
sw $t1, 0($v0)
# Store String Address
sw $t0, 4($v0)
# Save string instance
sw $v0, 500($fp)
# Call Node
lw $t0, 876($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 500($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 876($fp)
# Call Node
lw $t0, 0($t0)
# Call Node
sw $t0, 508($fp)
# Call Node
lw $t0, 508($fp)
# Call Node
lw $t0, 28($t0)
# Call Node
jal __get_ra
# Call Node
move $ra, $v0
# Call Node
jr $t0
# Call Node
sw $v0, 504($fp)
# Variable Node
lw $t0, 876($fp)
# Variable Node
lw $t0, 8($t0)
# Variable Node
sw $t0, 512($fp)
# Call Node
lw $t0, 876($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 512($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 876($fp)
# Call Node
lw $t0, 0($t0)
# Call Node
sw $t0, 520($fp)
# Call Node
lw $t0, 520($fp)
# Call Node
lw $t0, 80($t0)
# Call Node
jal __get_ra
# Call Node
move $ra, $v0
# Call Node
jr $t0
# Call Node
sw $v0, 516($fp)
# String Node
la $t0, data_85
# Type address into $a0
la $t1, String
# If String the is type and address
li $a0, 8
li $v0, 9
syscall
# Store String Type
sw $t1, 0($v0)
# Store String Address
sw $t0, 4($v0)
# Save string instance
sw $v0, 524($fp)
# Call Node
lw $t0, 876($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 524($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 876($fp)
# Call Node
lw $t0, 0($t0)
# Call Node
sw $t0, 532($fp)
# Call Node
lw $t0, 532($fp)
# Call Node
lw $t0, 28($t0)
# Call Node
jal __get_ra
# Call Node
move $ra, $v0
# Call Node
jr $t0
# Call Node
sw $v0, 528($fp)
# Conditional Node
lw $t0, 528($fp)
# Conditional Node
sw $t0, 468($fp)
# Conditional Node
j main_at_Main_label_26
# Conditional Node
main_at_Main_label_25:
# String Node
la $t0, data_86
# Type address into $a0
la $t1, String
# If String the is type and address
li $a0, 8
li $v0, 9
syscall
# Store String Type
sw $t1, 0($v0)
# Store String Address
sw $t0, 4($v0)
# Save string instance
sw $v0, 540($fp)
# Call Node
lw $t0, 876($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 540($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 876($fp)
# Call Node
lw $t0, 0($t0)
# Call Node
sw $t0, 548($fp)
# Call Node
lw $t0, 548($fp)
# Call Node
lw $t0, 28($t0)
# Call Node
jal __get_ra
# Call Node
move $ra, $v0
# Call Node
jr $t0
# Call Node
sw $v0, 544($fp)
# Variable Node
lw $t0, 876($fp)
# Variable Node
lw $t0, 8($t0)
# Variable Node
sw $t0, 552($fp)
# Call Node
lw $t0, 876($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 552($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 876($fp)
# Call Node
lw $t0, 0($t0)
# Call Node
sw $t0, 560($fp)
# Call Node
lw $t0, 560($fp)
# Call Node
lw $t0, 80($t0)
# Call Node
jal __get_ra
# Call Node
move $ra, $v0
# Call Node
jr $t0
# Call Node
sw $v0, 556($fp)
# String Node
la $t0, data_87
# Type address into $a0
la $t1, String
# If String the is type and address
li $a0, 8
li $v0, 9
syscall
# Store String Type
sw $t1, 0($v0)
# Store String Address
sw $t0, 4($v0)
# Save string instance
sw $v0, 564($fp)
# Call Node
lw $t0, 876($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 564($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 876($fp)
# Call Node
lw $t0, 0($t0)
# Call Node
sw $t0, 572($fp)
# Call Node
lw $t0, 572($fp)
# Call Node
lw $t0, 28($t0)
# Call Node
jal __get_ra
# Call Node
move $ra, $v0
# Call Node
jr $t0
# Call Node
sw $v0, 568($fp)
# Conditional Node
lw $t0, 568($fp)
# Conditional Node
sw $t0, 468($fp)
# Conditional Node
main_at_Main_label_26:
# Conditional Node
lw $t0, 468($fp)
# Conditional Node
sw $t0, 208($fp)
# Conditional Node
main_at_Main_label_18:
# Conditional Node
lw $t0, 208($fp)
# Conditional Node
sw $t0, 192($fp)
# Conditional Node
j main_at_Main_label_16
# Conditional Node
main_at_Main_label_15:
# Instantiate Node
la $a0, C
# Instantiate Node
lw $a0, 4($a0)
li $v0, 9
syscall
sw $v0, 576($fp)
# Instantiate Node
lw $t0, 576($fp)
# Instantiate Node
addi $sp, $sp, -4
# Instantiate Node
sw $t0, 0($sp)
# Instantiate Node
jal __init_C_type
# Instantiate Node
sw $v0, 576($fp)
# Variable Node
lw $t0, 876($fp)
# Variable Node
lw $t0, 8($t0)
# Variable Node
sw $t0, 580($fp)
# Call Node
lw $t0, 580($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 580($fp)
# Call Node
lw $t0, 0($t0)
# Call Node
sw $t0, 588($fp)
# Call Node
lw $t0, 588($fp)
# Call Node
lw $t0, 32($t0)
# Call Node
jal __get_ra
# Call Node
move $ra, $v0
# Call Node
jr $t0
# Call Node
sw $v0, 584($fp)
# Call Node
lw $t0, 576($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 584($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
jal function_method5_at_C
# Call Node
sw $v0, 592($fp)
# Assign Node
lw $t0, 876($fp)
# Assign Node
lw $t1, 592($fp)
# Assign Node
sw $t1, 8($t0)
# Conditional Node
lw $t0, 592($fp)
# Conditional Node
sw $t0, 192($fp)
# Conditional Node
main_at_Main_label_16:
# Conditional Node
lw $t0, 192($fp)
# Conditional Node
sw $t0, 176($fp)
# Conditional Node
j main_at_Main_label_14
# Conditional Node
main_at_Main_label_13:
# Instantiate Node
la $a0, C
# Instantiate Node
lw $a0, 4($a0)
li $v0, 9
syscall
sw $v0, 596($fp)
# Instantiate Node
lw $t0, 596($fp)
# Instantiate Node
addi $sp, $sp, -4
# Instantiate Node
sw $t0, 0($sp)
# Instantiate Node
jal __init_C_type
# Instantiate Node
sw $v0, 596($fp)
# Variable Node
lw $t0, 876($fp)
# Variable Node
lw $t0, 8($t0)
# Variable Node
sw $t0, 600($fp)
# Call Node
lw $t0, 600($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 600($fp)
# Call Node
lw $t0, 0($t0)
# Call Node
sw $t0, 608($fp)
# Call Node
lw $t0, 608($fp)
# Call Node
lw $t0, 32($t0)
# Call Node
jal __get_ra
# Call Node
move $ra, $v0
# Call Node
jr $t0
# Call Node
sw $v0, 604($fp)
# Call Node
lw $t0, 596($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 604($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
jal function_method5_at_B
# Call Node
sw $v0, 612($fp)
# Assign Node
lw $t0, 876($fp)
# Assign Node
lw $t1, 612($fp)
# Assign Node
sw $t1, 8($t0)
# Conditional Node
lw $t0, 612($fp)
# Conditional Node
sw $t0, 176($fp)
# Conditional Node
main_at_Main_label_14:
# Conditional Node
lw $t0, 176($fp)
# Conditional Node
sw $t0, 160($fp)
# Conditional Node
j main_at_Main_label_12
# Conditional Node
main_at_Main_label_11:
# Instantiate Node
la $a0, C
# Instantiate Node
lw $a0, 4($a0)
li $v0, 9
syscall
sw $v0, 616($fp)
# Instantiate Node
lw $t0, 616($fp)
# Instantiate Node
addi $sp, $sp, -4
# Instantiate Node
sw $t0, 0($sp)
# Instantiate Node
jal __init_C_type
# Instantiate Node
sw $v0, 616($fp)
# Variable Node
lw $t0, 876($fp)
# Variable Node
lw $t0, 8($t0)
# Variable Node
sw $t0, 620($fp)
# Call Node
lw $t0, 620($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 620($fp)
# Call Node
lw $t0, 0($t0)
# Call Node
sw $t0, 628($fp)
# Call Node
lw $t0, 628($fp)
# Call Node
lw $t0, 32($t0)
# Call Node
jal __get_ra
# Call Node
move $ra, $v0
# Call Node
jr $t0
# Call Node
sw $v0, 624($fp)
# Call Node
lw $t0, 616($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 624($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
jal function_method5_at_A
# Call Node
sw $v0, 632($fp)
# Assign Node
lw $t0, 876($fp)
# Assign Node
lw $t1, 632($fp)
# Assign Node
sw $t1, 8($t0)
# Conditional Node
lw $t0, 632($fp)
# Conditional Node
sw $t0, 160($fp)
# Conditional Node
main_at_Main_label_12:
# Conditional Node
lw $t0, 160($fp)
# Conditional Node
sw $t0, 144($fp)
# Conditional Node
j main_at_Main_label_10
# Conditional Node
main_at_Main_label_9:
# Instantiate Node
la $a0, A
# Instantiate Node
lw $a0, 4($a0)
li $v0, 9
syscall
sw $v0, 640($fp)
# Instantiate Node
lw $t0, 640($fp)
# Instantiate Node
addi $sp, $sp, -4
# Instantiate Node
sw $t0, 0($sp)
# Instantiate Node
jal __init_A_type
# Instantiate Node
sw $v0, 640($fp)
# Call Node
lw $t0, 876($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 876($fp)
# Call Node
lw $t0, 0($t0)
# Call Node
sw $t0, 648($fp)
# Call Node
lw $t0, 648($fp)
# Call Node
lw $t0, 68($t0)
# Call Node
jal __get_ra
# Call Node
move $ra, $v0
# Call Node
jr $t0
# Call Node
sw $v0, 644($fp)
# Call Node
lw $t0, 640($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 644($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 640($fp)
# Call Node
lw $t0, 0($t0)
# Call Node
sw $t0, 656($fp)
# Call Node
lw $t0, 656($fp)
# Call Node
lw $t0, 36($t0)
# Call Node
jal __get_ra
# Call Node
move $ra, $v0
# Call Node
jr $t0
# Call Node
sw $v0, 652($fp)
# Assign Node
lw $t0, 876($fp)
# Assign Node
lw $t1, 652($fp)
# Assign Node
sw $t1, 12($t0)
# Instantiate Node
la $a0, D
# Instantiate Node
lw $a0, 4($a0)
li $v0, 9
syscall
sw $v0, 660($fp)
# Instantiate Node
lw $t0, 660($fp)
# Instantiate Node
addi $sp, $sp, -4
# Instantiate Node
sw $t0, 0($sp)
# Instantiate Node
jal __init_D_type
# Instantiate Node
sw $v0, 660($fp)
# Variable Node
lw $t0, 876($fp)
# Variable Node
lw $t0, 8($t0)
# Variable Node
sw $t0, 664($fp)
# Call Node
lw $t0, 664($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 664($fp)
# Call Node
lw $t0, 0($t0)
# Call Node
sw $t0, 672($fp)
# Call Node
lw $t0, 672($fp)
# Call Node
lw $t0, 32($t0)
# Call Node
jal __get_ra
# Call Node
move $ra, $v0
# Call Node
jr $t0
# Call Node
sw $v0, 668($fp)
# Variable Node
lw $t0, 876($fp)
# Variable Node
lw $t0, 12($t0)
# Variable Node
sw $t0, 676($fp)
# Call Node
lw $t0, 676($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 676($fp)
# Call Node
lw $t0, 0($t0)
# Call Node
sw $t0, 684($fp)
# Call Node
lw $t0, 684($fp)
# Call Node
lw $t0, 32($t0)
# Call Node
jal __get_ra
# Call Node
move $ra, $v0
# Call Node
jr $t0
# Call Node
sw $v0, 680($fp)
# Call Node
lw $t0, 660($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 668($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 680($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 660($fp)
# Call Node
lw $t0, 0($t0)
# Call Node
sw $t0, 692($fp)
# Call Node
lw $t0, 692($fp)
# Call Node
lw $t0, 52($t0)
# Call Node
jal __get_ra
# Call Node
move $ra, $v0
# Call Node
jr $t0
# Call Node
sw $v0, 688($fp)
# Assign Node
lw $t0, 876($fp)
# Assign Node
lw $t1, 688($fp)
# Assign Node
sw $t1, 8($t0)
# Conditional Node
lw $t0, 688($fp)
# Conditional Node
sw $t0, 144($fp)
# Conditional Node
main_at_Main_label_10:
# Conditional Node
lw $t0, 144($fp)
# Conditional Node
sw $t0, 128($fp)
# Conditional Node
j main_at_Main_label_8
# Conditional Node
main_at_Main_label_7:
# Variable Node
lw $t0, 876($fp)
# Variable Node
lw $t0, 8($t0)
# Variable Node
sw $t0, 696($fp)
# Case Node typeof value
lw $t0, 696($fp)
# Case Node typeof value
lw $t0, 0($t0)
# Case Node typeof value
sw $t0, 704($fp)
# Case Node array declaration
li $a0, 12
# Case Node array declaration
li $v0, 9
# Case Node array declaration
syscall
# Case Node array declaration
sw $v0, 708($fp)
# Case Node array setindex 0
li $t2, 0
# Case Node array setindex 0
la $t3, C
# Case Node array setindex 0
lw $t1, 708($fp)
# Case Node array setindex 0
add $t1, $t1, $t2
# Case Node array setindex 0
sw $t3, 0($t1)
# Case Node array setindex 1
li $t2, 4
# Case Node array setindex 1
la $t3, A
# Case Node array setindex 1
lw $t1, 708($fp)
# Case Node array setindex 1
add $t1, $t1, $t2
# Case Node array setindex 1
sw $t3, 0($t1)
# Case Node array setindex 2
li $t2, 8
# Case Node array setindex 2
la $t3, Object
# Case Node array setindex 2
lw $t1, 708($fp)
# Case Node array setindex 2
add $t1, $t1, $t2
# Case Node array setindex 2
sw $t3, 0($t1)
# Case Node assign index -1
li $t0, -1
# Case Node assign index -1
sw $t0, 712($fp)
# Case Node assign minim -2
li $t0, -2
# Case Node assign minim -2
sw $t0, 720($fp)
# Case Node start label
main_at_Main_label_27:
# Case Node plus index 1
lw $t0, 712($fp)
# Case Node plus index 1
li $t1, 1
# Case Node plus index 1
add $t2, $t0, $t1
# Case Node plus index 1
sw $t2, 712($fp)
# Case Node equal stop_for index checks
lw $t0, 712($fp)
# Case Node equal stop_for index checks
li $t1, 3
# Case Node equal stop_for index checks
seq $t2, $t0, $t1
# Case Node equal stop_for index checks
sw $t2, 732($fp)
# Case Node gotoif stop_for end_label
lw $t0, 732($fp)
# Case Node gotoif stop_for end_label
bne $t0, $zero, main_at_Main_label_29
# Case Node get_index array_types index
lw $t0, 712($fp)
# Case Node get_index array_types index
li $t2, 4
# Case Node get_index array_types index
mul $t2, $t2, $t0
# Case Node get_index array_types index
lw $t1, 708($fp)
# Case Node get_index array_types index
add $t1, $t1, $t2
# Case Node get_index array_types index
lw $t2, 0($t1)
# Case Node get_index array_types index
sw $t2, 728($fp)
# Case Node arg type_value
lw $t0, 704($fp)
# Case Node arg type_value
addi $sp, $sp, -4
# Case Node arg type_value
sw $t0, 0($sp)
# Case Node arg current_type
lw $t0, 728($fp)
# Case Node arg current_type
addi $sp, $sp, -4
# Case Node arg current_type
sw $t0, 0($sp)
# Case Node static_call type_distance
jal type_distance
# Case Node static_call type_distance
sw $v0, 724($fp)
# Case Node equal not_valid_distance distance -1
lw $t0, 724($fp)
# Case Node equal not_valid_distance distance -1
li $t1, -1
# Case Node equal not_valid_distance distance -1
seq $t2, $t0, $t1
# Case Node equal not_valid_distance distance -1
sw $t2, 736($fp)
# Case Node gotoif not_valid_distance start_label
lw $t0, 736($fp)
# Case Node gotoif not_valid_distance start_label
bne $t0, $zero, main_at_Main_label_27
# Case Node equal minim_cond minim -2
lw $t0, 720($fp)
# Case Node equal minim_cond minim -2
li $t1, -2
# Case Node equal minim_cond minim -2
seq $t2, $t0, $t1
# Case Node equal minim_cond minim -2
sw $t2, 740($fp)
# Case Node gotoif minim_cond minim_label
lw $t0, 740($fp)
# Case Node gotoif minim_cond minim_label
bne $t0, $zero, main_at_Main_label_28
# Case Node greater minim_cond minim distance
lw $t0, 720($fp)
# Case Node greater minim_cond minim distance
lw $t1, 724($fp)
# Case Node greater minim_cond minim distance
sgt $t2, $t0, $t1
# Case Node greater minim_cond minim distance
sw $t2, 740($fp)
# Case Node gotoif minim_cond minim_label
lw $t0, 740($fp)
# Case Node gotoif minim_cond minim_label
bne $t0, $zero, main_at_Main_label_28
# Case Node goto start_label
j main_at_Main_label_27
# Case Node minim label
main_at_Main_label_28:
# Case Node assign minim distance
lw $t0, 724($fp)
# Case Node assign minim distance
sw $t0, 720($fp)
# Case Node assign minim_index index
lw $t0, 712($fp)
# Case Node assign minim_index index
sw $t0, 716($fp)
# Case Node goto start_label
j main_at_Main_label_27
# Case Node end label
main_at_Main_label_29:
# Case Node equal minim_cond minim -2
lw $t0, 720($fp)
# Case Node equal minim_cond minim -2
li $t1, -2
# Case Node equal minim_cond minim -2
seq $t2, $t0, $t1
# Case Node equal minim_cond minim -2
sw $t2, 740($fp)
# Case Node gotoif minim_cond abort_label
lw $t0, 740($fp)
# Case Node gotoif minim_cond abort_label
bne $t0, $zero, main_at_Main_label_30
# Case Node get_index array_types minim_index
lw $t0, 716($fp)
# Case Node get_index array_types minim_index
li $t2, 4
# Case Node get_index array_types minim_index
mul $t2, $t2, $t0
# Case Node get_index array_types minim_index
lw $t1, 708($fp)
# Case Node get_index array_types minim_index
add $t1, $t1, $t2
# Case Node get_index array_types minim_index
lw $t2, 0($t1)
# Case Node get_index array_types minim_index
sw $t2, 728($fp)
# Case Node equal not_equal_types param.type.name current_type
la $t0, C
# Case Node equal not_equal_types param.type.name current_type
lw $t1, 728($fp)
# Case Node equal not_equal_types param.type.name current_type
seq $t2, $t0, $t1
# Case Node equal not_equal_types param.type.name current_type
sw $t2, 744($fp)
# Case Node not not_equal_types not_equal_types
lw $t0, 744($fp)
# Case Node not not_equal_types not_equal_types
seq $t0, $t0, $zero
# Case Node not not_equal_types not_equal_types
sw $t0, 744($fp)
# Case Node gotoif not_equal_types lbl.label
lw $t0, 744($fp)
# Case Node gotoif not_equal_types lbl.label
bne $t0, $zero, main_at_Main_label_32
# Check Node
lw $t0, 696($fp)
# Check Node
sw $t0, 748($fp)
# Call Node
lw $t0, 748($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 748($fp)
# Call Node
lw $t0, 0($t0)
# Call Node
sw $t0, 756($fp)
# Call Node
lw $t0, 756($fp)
# Call Node
lw $t0, 32($t0)
# Call Node
jal __get_ra
# Call Node
move $ra, $v0
# Call Node
jr $t0
# Call Node
sw $v0, 752($fp)
# Call Node
lw $t0, 748($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 752($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 748($fp)
# Call Node
lw $t0, 0($t0)
# Call Node
sw $t0, 764($fp)
# Call Node
lw $t0, 764($fp)
# Call Node
lw $t0, 60($t0)
# Call Node
jal __get_ra
# Call Node
move $ra, $v0
# Call Node
jr $t0
# Call Node
sw $v0, 760($fp)
# Assign Node
lw $t0, 876($fp)
# Assign Node
lw $t1, 760($fp)
# Assign Node
sw $t1, 8($t0)
# Case Node assign final_result result
lw $t0, 760($fp)
# Case Node assign final_result result
sw $t0, 700($fp)
# Case Node goto final_label
j main_at_Main_label_31
# Case Node end_label <cool.ast.cool_ast.CheckNode object at 0x0000020832620CC0>
main_at_Main_label_32:
# Case Node equal not_equal_types param.type.name current_type
la $t0, A
# Case Node equal not_equal_types param.type.name current_type
lw $t1, 728($fp)
# Case Node equal not_equal_types param.type.name current_type
seq $t2, $t0, $t1
# Case Node equal not_equal_types param.type.name current_type
sw $t2, 744($fp)
# Case Node not not_equal_types not_equal_types
lw $t0, 744($fp)
# Case Node not not_equal_types not_equal_types
seq $t0, $t0, $zero
# Case Node not not_equal_types not_equal_types
sw $t0, 744($fp)
# Case Node gotoif not_equal_types lbl.label
lw $t0, 744($fp)
# Case Node gotoif not_equal_types lbl.label
bne $t0, $zero, main_at_Main_label_33
# Check Node
lw $t0, 696($fp)
# Check Node
sw $t0, 768($fp)
# Call Node
lw $t0, 768($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 768($fp)
# Call Node
lw $t0, 0($t0)
# Call Node
sw $t0, 776($fp)
# Call Node
lw $t0, 776($fp)
# Call Node
lw $t0, 32($t0)
# Call Node
jal __get_ra
# Call Node
move $ra, $v0
# Call Node
jr $t0
# Call Node
sw $v0, 772($fp)
# Call Node
lw $t0, 768($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 772($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 768($fp)
# Call Node
lw $t0, 0($t0)
# Call Node
sw $t0, 784($fp)
# Call Node
lw $t0, 784($fp)
# Call Node
lw $t0, 48($t0)
# Call Node
jal __get_ra
# Call Node
move $ra, $v0
# Call Node
jr $t0
# Call Node
sw $v0, 780($fp)
# Assign Node
lw $t0, 876($fp)
# Assign Node
lw $t1, 780($fp)
# Assign Node
sw $t1, 8($t0)
# Case Node assign final_result result
lw $t0, 780($fp)
# Case Node assign final_result result
sw $t0, 700($fp)
# Case Node goto final_label
j main_at_Main_label_31
# Case Node end_label <cool.ast.cool_ast.CheckNode object at 0x0000020832620CF8>
main_at_Main_label_33:
# Case Node equal not_equal_types param.type.name current_type
la $t0, Object
# Case Node equal not_equal_types param.type.name current_type
lw $t1, 728($fp)
# Case Node equal not_equal_types param.type.name current_type
seq $t2, $t0, $t1
# Case Node equal not_equal_types param.type.name current_type
sw $t2, 744($fp)
# Case Node not not_equal_types not_equal_types
lw $t0, 744($fp)
# Case Node not not_equal_types not_equal_types
seq $t0, $t0, $zero
# Case Node not not_equal_types not_equal_types
sw $t0, 744($fp)
# Case Node gotoif not_equal_types lbl.label
lw $t0, 744($fp)
# Case Node gotoif not_equal_types lbl.label
bne $t0, $zero, main_at_Main_label_34
# Check Node
lw $t0, 696($fp)
# Check Node
sw $t0, 788($fp)
# String Node
la $t0, data_88
# Type address into $a0
la $t1, String
# If String the is type and address
li $a0, 8
li $v0, 9
syscall
# Store String Type
sw $t1, 0($v0)
# Store String Address
sw $t0, 4($v0)
# Save string instance
sw $v0, 796($fp)
# Call Node
lw $t0, 876($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 796($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 876($fp)
# Call Node
lw $t0, 0($t0)
# Call Node
sw $t0, 804($fp)
# Call Node
lw $t0, 804($fp)
# Call Node
lw $t0, 28($t0)
# Call Node
jal __get_ra
# Call Node
move $ra, $v0
# Call Node
jr $t0
# Call Node
sw $v0, 800($fp)
# Call Node
lw $t0, 876($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 876($fp)
# Call Node
lw $t0, 0($t0)
# Call Node
sw $t0, 812($fp)
# Call Node
lw $t0, 812($fp)
# Call Node
lw $t0, 16($t0)
# Call Node
jal __get_ra
# Call Node
move $ra, $v0
# Call Node
jr $t0
# Call Node
sw $v0, 808($fp)
# Case Node assign final_result result
li $t0, 0
# Case Node assign final_result result
sw $t0, 700($fp)
# Case Node goto final_label
j main_at_Main_label_31
# Case Node end_label <cool.ast.cool_ast.CheckNode object at 0x0000020832620E10>
main_at_Main_label_34:
# Case Node abort label
main_at_Main_label_30:
# Case Node abort
addi $v0, $zero, 10
# Case Node abort
syscall
# Case Node final_label
main_at_Main_label_31:
# Conditional Node
lw $t0, 700($fp)
# Conditional Node
sw $t0, 128($fp)
# Conditional Node
main_at_Main_label_8:
# Conditional Node
lw $t0, 128($fp)
# Conditional Node
sw $t0, 112($fp)
# Conditional Node
j main_at_Main_label_6
# Conditional Node
main_at_Main_label_5:
# Instantiate Node
la $a0, A
# Instantiate Node
lw $a0, 4($a0)
li $v0, 9
syscall
sw $v0, 820($fp)
# Instantiate Node
lw $t0, 820($fp)
# Instantiate Node
addi $sp, $sp, -4
# Instantiate Node
sw $t0, 0($sp)
# Instantiate Node
jal __init_A_type
# Instantiate Node
sw $v0, 820($fp)
# Call Node
lw $t0, 876($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 876($fp)
# Call Node
lw $t0, 0($t0)
# Call Node
sw $t0, 828($fp)
# Call Node
lw $t0, 828($fp)
# Call Node
lw $t0, 68($t0)
# Call Node
jal __get_ra
# Call Node
move $ra, $v0
# Call Node
jr $t0
# Call Node
sw $v0, 824($fp)
# Call Node
lw $t0, 820($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 824($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 820($fp)
# Call Node
lw $t0, 0($t0)
# Call Node
sw $t0, 836($fp)
# Call Node
lw $t0, 836($fp)
# Call Node
lw $t0, 36($t0)
# Call Node
jal __get_ra
# Call Node
move $ra, $v0
# Call Node
jr $t0
# Call Node
sw $v0, 832($fp)
# Assign Node
lw $t0, 876($fp)
# Assign Node
lw $t1, 832($fp)
# Assign Node
sw $t1, 12($t0)
# Instantiate Node
la $a0, B
# Instantiate Node
lw $a0, 4($a0)
li $v0, 9
syscall
sw $v0, 840($fp)
# Instantiate Node
lw $t0, 840($fp)
# Instantiate Node
addi $sp, $sp, -4
# Instantiate Node
sw $t0, 0($sp)
# Instantiate Node
jal __init_B_type
# Instantiate Node
sw $v0, 840($fp)
# Variable Node
lw $t0, 876($fp)
# Variable Node
lw $t0, 8($t0)
# Variable Node
sw $t0, 844($fp)
# Call Node
lw $t0, 844($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 844($fp)
# Call Node
lw $t0, 0($t0)
# Call Node
sw $t0, 852($fp)
# Call Node
lw $t0, 852($fp)
# Call Node
lw $t0, 32($t0)
# Call Node
jal __get_ra
# Call Node
move $ra, $v0
# Call Node
jr $t0
# Call Node
sw $v0, 848($fp)
# Variable Node
lw $t0, 876($fp)
# Variable Node
lw $t0, 12($t0)
# Variable Node
sw $t0, 856($fp)
# Call Node
lw $t0, 856($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 856($fp)
# Call Node
lw $t0, 0($t0)
# Call Node
sw $t0, 864($fp)
# Call Node
lw $t0, 864($fp)
# Call Node
lw $t0, 32($t0)
# Call Node
jal __get_ra
# Call Node
move $ra, $v0
# Call Node
jr $t0
# Call Node
sw $v0, 860($fp)
# Call Node
lw $t0, 840($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 848($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 860($fp)
# Call Node
addi $sp, $sp, -4
# Call Node
sw $t0, 0($sp)
# Call Node
lw $t0, 840($fp)
# Call Node
lw $t0, 0($t0)
# Call Node
sw $t0, 872($fp)
# Call Node
lw $t0, 872($fp)
# Call Node
lw $t0, 44($t0)
# Call Node
jal __get_ra
# Call Node
move $ra, $v0
# Call Node
jr $t0
# Call Node
sw $v0, 868($fp)
# Assign Node
lw $t0, 876($fp)
# Assign Node
lw $t1, 868($fp)
# Assign Node
sw $t1, 8($t0)
# Conditional Node
lw $t0, 868($fp)
# Conditional Node
sw $t0, 112($fp)
# Conditional Node
main_at_Main_label_6:
# While Node
j main_at_Main_label_0
# While Node
main_at_Main_label_2:
# Func Declaration Node
lw $v0, 8($fp)
# Program Node
lw $ra, 0($sp)
# Program Node
lw $fp, 4($sp)
# Program Node
addi $sp, $sp, 8
# Program Node
addi $sp, $sp, 880
# Program Node
jr $ra
# Class Declaration Node
__init_Object_type:
# Class Declaration Node
addi $sp, $sp, 0
# Class Declaration Node
move $t0, $sp
# Class Declaration Node
addi $sp, $sp, -8
# Class Declaration Node
sw $ra, 0($sp)
# Class Declaration Node
sw $fp, 4($sp)
# Class Declaration Node
move $fp, $t0
lw $t0, 0($fp)
la $t1, Object
sw $t1, 0($t0)
# return node
lw $v0, 0($fp)
# Class Declaration Node
lw $ra, 0($sp)
# Class Declaration Node
lw $fp, 4($sp)
# Class Declaration Node
addi $sp, $sp, 8
# Class Declaration Node
addi $sp, $sp, 4
# Class Declaration Node
jr $ra
# Class Declaration Node
__init_String_type:
# Class Declaration Node
addi $sp, $sp, 0
# Class Declaration Node
move $t0, $sp
# Class Declaration Node
addi $sp, $sp, -8
# Class Declaration Node
sw $ra, 0($sp)
# Class Declaration Node
sw $fp, 4($sp)
# Class Declaration Node
move $fp, $t0
# Calling father init function
lw $t0, 0($fp)
# Calling father init function
addi $sp, $sp, -4
# Calling father init function
sw $t0, 0($sp)
jal __init_Object_type
sw $v0, 0($fp)
lw $t0, 0($fp)
la $t1, String
sw $t1, 0($t0)
la $t1, __empty_string
sw $t1, 4($t0)
# return node
lw $v0, 0($fp)
# Class Declaration Node
lw $ra, 0($sp)
# Class Declaration Node
lw $fp, 4($sp)
# Class Declaration Node
addi $sp, $sp, 8
# Class Declaration Node
addi $sp, $sp, 4
# Class Declaration Node
jr $ra
# Class Declaration Node
__init_Bool_type:
# Class Declaration Node
addi $sp, $sp, 0
# Class Declaration Node
move $t0, $sp
# Class Declaration Node
addi $sp, $sp, -8
# Class Declaration Node
sw $ra, 0($sp)
# Class Declaration Node
sw $fp, 4($sp)
# Class Declaration Node
move $fp, $t0
# Calling father init function
lw $t0, 0($fp)
# Calling father init function
addi $sp, $sp, -4
# Calling father init function
sw $t0, 0($sp)
jal __init_Object_type
sw $v0, 0($fp)
lw $t0, 0($fp)
la $t1, Bool
sw $t1, 0($t0)
# return node
lw $v0, 0($fp)
# Class Declaration Node
lw $ra, 0($sp)
# Class Declaration Node
lw $fp, 4($sp)
# Class Declaration Node
addi $sp, $sp, 8
# Class Declaration Node
addi $sp, $sp, 4
# Class Declaration Node
jr $ra
# Class Declaration Node
__init_Int_type:
# Class Declaration Node
addi $sp, $sp, 0
# Class Declaration Node
move $t0, $sp
# Class Declaration Node
addi $sp, $sp, -8
# Class Declaration Node
sw $ra, 0($sp)
# Class Declaration Node
sw $fp, 4($sp)
# Class Declaration Node
move $fp, $t0
# Calling father init function
lw $t0, 0($fp)
# Calling father init function
addi $sp, $sp, -4
# Calling father init function
sw $t0, 0($sp)
jal __init_Object_type
sw $v0, 0($fp)
lw $t0, 0($fp)
la $t1, Int
sw $t1, 0($t0)
# return node
lw $v0, 0($fp)
# Class Declaration Node
lw $ra, 0($sp)
# Class Declaration Node
lw $fp, 4($sp)
# Class Declaration Node
addi $sp, $sp, 8
# Class Declaration Node
addi $sp, $sp, 4
# Class Declaration Node
jr $ra
# Class Declaration Node
__init_IO_type:
# Class Declaration Node
addi $sp, $sp, 0
# Class Declaration Node
move $t0, $sp
# Class Declaration Node
addi $sp, $sp, -8
# Class Declaration Node
sw $ra, 0($sp)
# Class Declaration Node
sw $fp, 4($sp)
# Class Declaration Node
move $fp, $t0
# Calling father init function
lw $t0, 0($fp)
# Calling father init function
addi $sp, $sp, -4
# Calling father init function
sw $t0, 0($sp)
jal __init_Object_type
sw $v0, 0($fp)
lw $t0, 0($fp)
la $t1, IO
sw $t1, 0($t0)
# return node
lw $v0, 0($fp)
# Class Declaration Node
lw $ra, 0($sp)
# Class Declaration Node
lw $fp, 4($sp)
# Class Declaration Node
addi $sp, $sp, 8
# Class Declaration Node
addi $sp, $sp, 4
# Class Declaration Node
jr $ra
# Class Declaration Node
__init_A_type:
# Class Declaration Node
addi $sp, $sp, -4
# Class Declaration Node
move $t0, $sp
# Class Declaration Node
addi $sp, $sp, -8
# Class Declaration Node
sw $ra, 0($sp)
# Class Declaration Node
sw $fp, 4($sp)
# Class Declaration Node
move $fp, $t0
# Calling father init function
lw $t0, 4($fp)
# Calling father init function
addi $sp, $sp, -4
# Calling father init function
sw $t0, 0($sp)
jal __init_Object_type
sw $v0, 4($fp)
lw $t0, 4($fp)
la $t1, A
sw $t1, 0($t0)
# arg node
lw $t0, 4($fp)
# arg node
addi $sp, $sp, -4
# arg node
sw $t0, 0($sp)
# Initialize arg function
jal __init_var_at_A
# Initialize arg function
sw $v0, 0($fp)
# return node
lw $v0, 4($fp)
# Class Declaration Node
lw $ra, 0($sp)
# Class Declaration Node
lw $fp, 4($sp)
# Class Declaration Node
addi $sp, $sp, 8
# Class Declaration Node
addi $sp, $sp, 8
# Class Declaration Node
jr $ra
# Class Declaration Node
__init_B_type:
# Class Declaration Node
addi $sp, $sp, 0
# Class Declaration Node
move $t0, $sp
# Class Declaration Node
addi $sp, $sp, -8
# Class Declaration Node
sw $ra, 0($sp)
# Class Declaration Node
sw $fp, 4($sp)
# Class Declaration Node
move $fp, $t0
# Calling father init function
lw $t0, 0($fp)
# Calling father init function
addi $sp, $sp, -4
# Calling father init function
sw $t0, 0($sp)
jal __init_A_type
sw $v0, 0($fp)
lw $t0, 0($fp)
la $t1, B
sw $t1, 0($t0)
# return node
lw $v0, 0($fp)
# Class Declaration Node
lw $ra, 0($sp)
# Class Declaration Node
lw $fp, 4($sp)
# Class Declaration Node
addi $sp, $sp, 8
# Class Declaration Node
addi $sp, $sp, 4
# Class Declaration Node
jr $ra
# Class Declaration Node
__init_C_type:
# Class Declaration Node
addi $sp, $sp, 0
# Class Declaration Node
move $t0, $sp
# Class Declaration Node
addi $sp, $sp, -8
# Class Declaration Node
sw $ra, 0($sp)
# Class Declaration Node
sw $fp, 4($sp)
# Class Declaration Node
move $fp, $t0
# Calling father init function
lw $t0, 0($fp)
# Calling father init function
addi $sp, $sp, -4
# Calling father init function
sw $t0, 0($sp)
jal __init_B_type
sw $v0, 0($fp)
lw $t0, 0($fp)
la $t1, C
sw $t1, 0($t0)
# return node
lw $v0, 0($fp)
# Class Declaration Node
lw $ra, 0($sp)
# Class Declaration Node
lw $fp, 4($sp)
# Class Declaration Node
addi $sp, $sp, 8
# Class Declaration Node
addi $sp, $sp, 4
# Class Declaration Node
jr $ra
# Class Declaration Node
__init_D_type:
# Class Declaration Node
addi $sp, $sp, 0
# Class Declaration Node
move $t0, $sp
# Class Declaration Node
addi $sp, $sp, -8
# Class Declaration Node
sw $ra, 0($sp)
# Class Declaration Node
sw $fp, 4($sp)
# Class Declaration Node
move $fp, $t0
# Calling father init function
lw $t0, 0($fp)
# Calling father init function
addi $sp, $sp, -4
# Calling father init function
sw $t0, 0($sp)
jal __init_B_type
sw $v0, 0($fp)
lw $t0, 0($fp)
la $t1, D
sw $t1, 0($t0)
# return node
lw $v0, 0($fp)
# Class Declaration Node
lw $ra, 0($sp)
# Class Declaration Node
lw $fp, 4($sp)
# Class Declaration Node
addi $sp, $sp, 8
# Class Declaration Node
addi $sp, $sp, 4
# Class Declaration Node
jr $ra
# Class Declaration Node
__init_E_type:
# Class Declaration Node
addi $sp, $sp, 0
# Class Declaration Node
move $t0, $sp
# Class Declaration Node
addi $sp, $sp, -8
# Class Declaration Node
sw $ra, 0($sp)
# Class Declaration Node
sw $fp, 4($sp)
# Class Declaration Node
move $fp, $t0
# Calling father init function
lw $t0, 0($fp)
# Calling father init function
addi $sp, $sp, -4
# Calling father init function
sw $t0, 0($sp)
jal __init_D_type
sw $v0, 0($fp)
lw $t0, 0($fp)
la $t1, E
sw $t1, 0($t0)
# return node
lw $v0, 0($fp)
# Class Declaration Node
lw $ra, 0($sp)
# Class Declaration Node
lw $fp, 4($sp)
# Class Declaration Node
addi $sp, $sp, 8
# Class Declaration Node
addi $sp, $sp, 4
# Class Declaration Node
jr $ra
# Class Declaration Node
__init_A2I_type:
# Class Declaration Node
addi $sp, $sp, 0
# Class Declaration Node
move $t0, $sp
# Class Declaration Node
addi $sp, $sp, -8
# Class Declaration Node
sw $ra, 0($sp)
# Class Declaration Node
sw $fp, 4($sp)
# Class Declaration Node
move $fp, $t0
# Calling father init function
lw $t0, 0($fp)
# Calling father init function
addi $sp, $sp, -4
# Calling father init function
sw $t0, 0($sp)
jal __init_Object_type
sw $v0, 0($fp)
lw $t0, 0($fp)
la $t1, A2I
sw $t1, 0($t0)
# return node
lw $v0, 0($fp)
# Class Declaration Node
lw $ra, 0($sp)
# Class Declaration Node
lw $fp, 4($sp)
# Class Declaration Node
addi $sp, $sp, 8
# Class Declaration Node
addi $sp, $sp, 4
# Class Declaration Node
jr $ra
# Class Declaration Node
__init_Main_type:
# Class Declaration Node
addi $sp, $sp, -16
# Class Declaration Node
move $t0, $sp
# Class Declaration Node
addi $sp, $sp, -8
# Class Declaration Node
sw $ra, 0($sp)
# Class Declaration Node
sw $fp, 4($sp)
# Class Declaration Node
move $fp, $t0
# Calling father init function
lw $t0, 16($fp)
# Calling father init function
addi $sp, $sp, -4
# Calling father init function
sw $t0, 0($sp)
jal __init_IO_type
sw $v0, 16($fp)
lw $t0, 16($fp)
la $t1, Main
sw $t1, 0($t0)
# arg node
lw $t0, 16($fp)
# arg node
addi $sp, $sp, -4
# arg node
sw $t0, 0($sp)
# Initialize arg function
jal __init_char_at_Main
# Initialize arg function
sw $v0, 0($fp)
# arg node
lw $t0, 16($fp)
# arg node
addi $sp, $sp, -4
# arg node
sw $t0, 0($sp)
# Initialize arg function
jal __init_avar_at_Main
# Initialize arg function
sw $v0, 4($fp)
# arg node
lw $t0, 16($fp)
# arg node
addi $sp, $sp, -4
# arg node
sw $t0, 0($sp)
# Initialize arg function
jal __init_a_var_at_Main
# Initialize arg function
sw $v0, 8($fp)
# arg node
lw $t0, 16($fp)
# arg node
addi $sp, $sp, -4
# arg node
sw $t0, 0($sp)
# Initialize arg function
jal __init_flag_at_Main
# Initialize arg function
sw $v0, 12($fp)
# return node
lw $v0, 16($fp)
# Class Declaration Node
lw $ra, 0($sp)
# Class Declaration Node
lw $fp, 4($sp)
# Class Declaration Node
addi $sp, $sp, 8
# Class Declaration Node
addi $sp, $sp, 20
# Class Declaration Node
jr $ra
.data 
data_0: .asciiz "Object"
data_1: .asciiz "String"
data_2: .asciiz "Bool"
data_3: .asciiz "Int"
data_4: .asciiz "IO"
data_5: .asciiz "A"
data_6: .asciiz "B"
data_7: .asciiz "C"
data_8: .asciiz "D"
data_9: .asciiz "E"
data_10: .asciiz "A2I"
data_11: .asciiz "Main"
data_12: .asciiz "Abort called from class "
data_13: .asciiz "0"
data_14: .asciiz "1"
data_15: .asciiz "2"
data_16: .asciiz "3"
data_17: .asciiz "4"
data_18: .asciiz "5"
data_19: .asciiz "6"
data_20: .asciiz "7"
data_21: .asciiz "8"
data_22: .asciiz "9"
data_23: .asciiz ""
data_24: .asciiz "9"
data_25: .asciiz "8"
data_26: .asciiz "7"
data_27: .asciiz "6"
data_28: .asciiz "5"
data_29: .asciiz "4"
data_30: .asciiz "3"
data_31: .asciiz "2"
data_32: .asciiz "1"
data_33: .asciiz "0"
data_34: .asciiz "-"
data_35: .asciiz "+"
data_36: .asciiz "-"
data_37: .asciiz "0"
data_38: .asciiz ""
data_39: .asciiz ""
data_40: .asciiz "\n\tTo add a number to "
data_41: .asciiz "...enter a:\n"
data_42: .asciiz "\tTo negate "
data_43: .asciiz "...enter b:\n"
data_44: .asciiz "\tTo find the difference between "
data_45: .asciiz "and another number...enter c:\n"
data_46: .asciiz "\tTo find the factorial of "
data_47: .asciiz "...enter d:\n"
data_48: .asciiz "\tTo square "
data_49: .asciiz "...enter e:\n"
data_50: .asciiz "\tTo cube "
data_51: .asciiz "...enter f:\n"
data_52: .asciiz "\tTo find out if "
data_53: .asciiz "is a multiple of 3...enter g:\n"
data_54: .asciiz "\tTo divide "
data_55: .asciiz "by 8...enter h:\n"
data_56: .asciiz "\tTo get a new number...enter j:\n"
data_57: .asciiz "\tTo quit...enter q:\n\n"
data_58: .asciiz "\n"
data_59: .asciiz "Please enter a number...  "
data_60: .asciiz "Class type is now A\n"
data_61: .asciiz "Class type is now B\n"
data_62: .asciiz "Class type is now C\n"
data_63: .asciiz "Class type is now D\n"
data_64: .asciiz "Class type is now E\n"
data_65: .asciiz "Oooops\n"
data_66: .asciiz " "
data_67: .asciiz "number "
data_68: .asciiz "is odd!\n"
data_69: .asciiz "is even!\n"
data_70: .asciiz "a"
data_71: .asciiz "b"
data_72: .asciiz "c"
data_73: .asciiz "d"
data_74: .asciiz "e"
data_75: .asciiz "f"
data_76: .asciiz "g"
data_77: .asciiz "h"
data_78: .asciiz "j"
data_79: .asciiz "q"
data_80: .asciiz "number "
data_81: .asciiz "is equal to "
data_82: .asciiz "times 8 with a remainder of "
data_83: .asciiz "\n"
data_84: .asciiz "number "
data_85: .asciiz "is not divisible by 3.\n"
data_86: .asciiz "number "
data_87: .asciiz "is divisible by 3.\n"
data_88: .asciiz "Oooops\n"
__empty_string: .asciiz ""
# Program Node
Object: .word 0, 4, data_0, __init_Object_type, function_abort_at_Object, function_type_name_at_Object, function_copy_at_Object
# Program Node
String: .word Object, 4, data_1, __init_String_type, function_abort_at_Object, function_type_name_at_Object, function_copy_at_Object, function_length_at_String, function_concat_at_String, function_substr_at_String
# Program Node
Bool: .word Object, 4, data_2, __init_Bool_type, function_abort_at_Bool, function_type_name_at_Bool, function_copy_at_Object
# Program Node
Int: .word Object, 4, data_3, __init_Int_type, function_abort_at_Int, function_type_name_at_Int, function_copy_at_Object
# Program Node
IO: .word Object, 4, data_4, __init_IO_type, function_abort_at_Object, function_type_name_at_Object, function_copy_at_Object, function_out_string_at_IO, function_out_int_at_IO, function_in_string_at_IO, function_in_int_at_IO
# Program Node
A: .word Object, 8, data_5, __init_A_type, function_abort_at_Object, function_type_name_at_Object, function_copy_at_Object, __init_var_at_A, function_value_at_A, function_set_var_at_A, function_method1_at_A, function_method2_at_A, function_method3_at_A, function_method4_at_A, function_method5_at_A
# Program Node
B: .word A, 8, data_6, __init_B_type, function_abort_at_Object, function_type_name_at_Object, function_copy_at_Object, __init_var_at_A, function_value_at_A, function_set_var_at_A, function_method1_at_A, function_method2_at_A, function_method3_at_A, function_method4_at_A, function_method5_at_B
# Program Node
C: .word B, 8, data_7, __init_C_type, function_abort_at_Object, function_type_name_at_Object, function_copy_at_Object, __init_var_at_A, function_value_at_A, function_set_var_at_A, function_method1_at_A, function_method2_at_A, function_method3_at_A, function_method4_at_A, function_method5_at_C, function_method6_at_C
# Program Node
D: .word B, 8, data_8, __init_D_type, function_abort_at_Object, function_type_name_at_Object, function_copy_at_Object, __init_var_at_A, function_value_at_A, function_set_var_at_A, function_method1_at_A, function_method2_at_A, function_method3_at_A, function_method4_at_A, function_method5_at_B, function_method7_at_D
# Program Node
E: .word D, 8, data_9, __init_E_type, function_abort_at_Object, function_type_name_at_Object, function_copy_at_Object, __init_var_at_A, function_value_at_A, function_set_var_at_A, function_method1_at_A, function_method2_at_A, function_method3_at_A, function_method4_at_A, function_method5_at_B, function_method7_at_D, function_method6_at_E
# Program Node
A2I: .word Object, 4, data_10, __init_A2I_type, function_abort_at_Object, function_type_name_at_Object, function_copy_at_Object, function_c2i_at_A2I, function_i2c_at_A2I, function_a2i_at_A2I, function_a2i_aux_at_A2I, function_i2a_at_A2I, function_i2a_aux_at_A2I
# Program Node
Main: .word IO, 20, data_11, __init_Main_type, function_abort_at_Object, function_type_name_at_Object, function_copy_at_Object, function_out_string_at_IO, function_out_int_at_IO, function_in_string_at_IO, function_in_int_at_IO, __init_char_at_Main, __init_avar_at_Main, __init_a_var_at_Main, __init_flag_at_Main, function_menu_at_Main, function_prompt_at_Main, function_get_int_at_Main, function_is_even_at_Main, function_class_type_at_Main, function_print_at_Main, function_main_at_Main