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
addi $sp, $sp, -16
sw $a0, 0($sp)
sw $a1, 4($sp)
sw $a2, 8($sp)
sw $ra, 12($sp)
jal __string_length
lw $a0, 0($sp)
lw $a1, 4($sp)
lw $a2, 8($sp)
lw $ra, 12($sp)
addi $sp, $sp, 16
bge $a1, $v0, __string_substring_abort
add $t0, $a1, $a2
bgt $t0, $v0, __string_substring_abort
blt $a2, $zero, __string_substring_abort
move $t1, $a0
addi $a0, $a2, 1
li $v0, 9
syscall
move $t2, $v0
addi $a0, $a0, -1
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
sb $zero, 0($t2)
jr $ra
__string_substring_abort:
addi $v0, $zero, 10
syscall
__type_name:
lw $v0, 8($a0)
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
move $t1, $a0
add $t2, $v0, $t0
addi $a0, $t2, 1
move $t2, $v0
li $v0, 9
syscall
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
jr $ra
main:
addi $sp, $sp, -12
move $t0, $sp
addi $sp, $sp, -8
sw $ra, 0($sp)
sw $fp, 4($sp)
move $fp, $t0
la $a0, Main
lw $a0, 4($a0)
li $v0, 9
syscall
sw $v0, 8($fp)
lw $t0, 8($fp)
addi $sp, $sp, -4
sw $t0, 0($sp)
jal __init_Main_type
sw $v0, 8($fp)
lw $t0, 8($fp)
addi $sp, $sp, -4
sw $t0, 0($sp)
jal function_main_at_Main
sw $v0, 4($fp)
li $v0, 0
lw $ra, 0($sp)
lw $fp, 4($sp)
addi $sp, $sp, 8
addi $sp, $sp, 12
jr $ra
type_distance:
addi $sp, $sp, -16
move $t0, $sp
addi $sp, $sp, -8
sw $ra, 0($sp)
sw $fp, 4($sp)
move $fp, $t0
sw $zero, 12($fp)
li $t0, 0
sw $t0, 0($fp)
distance_label_0:
lw $t0, 20($fp)
lw $t1, 16($fp)
seq $t2, $t0, $t1
sw $t2, 4($fp)
lw $t0, 4($fp)
bne $t0, $zero, distance_label_1
lw $t0, 20($fp)
lw $t0, 0($t0)
sw $t0, 20($fp)
lw $t0, 20($fp)
lw $t1, 12($fp)
seq $t2, $t0, $t1
sw $t2, 8($fp)
lw $t0, 8($fp)
bne $t0, $zero, distance_label_2
lw $t0, 0($fp)
li $t1, 1
add $t2, $t0, $t1
sw $t2, 0($fp)
j distance_label_0
distance_label_2:
li $t0, -1
sw $t0, 0($fp)
distance_label_1:
lw $v0, 0($fp)
lw $ra, 0($sp)
lw $fp, 4($sp)
addi $sp, $sp, 8
addi $sp, $sp, 24
jr $ra
__init_Object_type:
addi $sp, $sp, 0
move $t0, $sp
addi $sp, $sp, -8
sw $ra, 0($sp)
sw $fp, 4($sp)
move $fp, $t0
lw $t0, 0($fp)
la $t1, Object
sw $t1, 0($t0)
lw $v0, 0($fp)
lw $ra, 0($sp)
lw $fp, 4($sp)
addi $sp, $sp, 8
addi $sp, $sp, 4
jr $ra
function_abort_at_Object:
addi $sp, $sp, 0
move $t0, $sp
addi $sp, $sp, -8
sw $ra, 0($sp)
sw $fp, 4($sp)
move $fp, $t0
addi $v0, $zero, 10
syscall
li $v0, 0
lw $ra, 0($sp)
lw $fp, 4($sp)
addi $sp, $sp, 8
addi $sp, $sp, 4
jr $ra
function_type_name_at_Object:
addi $sp, $sp, -4
move $t0, $sp
addi $sp, $sp, -8
sw $ra, 0($sp)
sw $fp, 4($sp)
move $fp, $t0
lw $t0, 4($fp)
lw $t0, 0($t0)
sw $t0, 0($fp)
lw $a0, 0($fp)
jal __type_name
sw $v0, 0($fp)
lw $v0, 0($fp)
lw $ra, 0($sp)
lw $fp, 4($sp)
addi $sp, $sp, 8
addi $sp, $sp, 8
jr $ra
function_copy_at_Object:
addi $sp, $sp, -4
move $t0, $sp
addi $sp, $sp, -8
sw $ra, 0($sp)
sw $fp, 4($sp)
move $fp, $t0
lw $a0, 4($fp)
jal __copy
sw $v0, 0($fp)
lw $v0, 0($fp)
lw $ra, 0($sp)
lw $fp, 4($sp)
addi $sp, $sp, 8
addi $sp, $sp, 8
jr $ra
__init_String_type:
addi $sp, $sp, 0
move $t0, $sp
addi $sp, $sp, -8
sw $ra, 0($sp)
sw $fp, 4($sp)
move $fp, $t0
lw $t0, 0($fp)
la $t1, String
sw $t1, 0($t0)
lw $v0, 0($fp)
lw $ra, 0($sp)
lw $fp, 4($sp)
addi $sp, $sp, 8
addi $sp, $sp, 4
jr $ra
function_length_at_String:
addi $sp, $sp, -4
move $t0, $sp
addi $sp, $sp, -8
sw $ra, 0($sp)
sw $fp, 4($sp)
move $fp, $t0
lw $a0, 4($fp)
jal __string_length
sw $v0, 0($fp)
lw $v0, 0($fp)
lw $ra, 0($sp)
lw $fp, 4($sp)
addi $sp, $sp, 8
addi $sp, $sp, 8
jr $ra
function_concat_at_String:
addi $sp, $sp, -4
move $t0, $sp
addi $sp, $sp, -8
sw $ra, 0($sp)
sw $fp, 4($sp)
move $fp, $t0
lw $a0, 8($fp)
lw $a1, 4($fp)
jal __concat
sw $v0, 0($fp)
lw $v0, 0($fp)
lw $ra, 0($sp)
lw $fp, 4($sp)
addi $sp, $sp, 8
addi $sp, $sp, 12
jr $ra
function_substr_at_String:
addi $sp, $sp, -4
move $t0, $sp
addi $sp, $sp, -8
sw $ra, 0($sp)
sw $fp, 4($sp)
move $fp, $t0
lw $a0, 12($fp)
lw $a1, 8($fp)
lw $a2, 4($fp)
jal __string_substring
sw $v0, 0($fp)
lw $v0, 0($fp)
lw $ra, 0($sp)
lw $fp, 4($sp)
addi $sp, $sp, 8
addi $sp, $sp, 16
jr $ra
__init_Bool_type:
addi $sp, $sp, 0
move $t0, $sp
addi $sp, $sp, -8
sw $ra, 0($sp)
sw $fp, 4($sp)
move $fp, $t0
lw $t0, 0($fp)
la $t1, Bool
sw $t1, 0($t0)
lw $v0, 0($fp)
lw $ra, 0($sp)
lw $fp, 4($sp)
addi $sp, $sp, 8
addi $sp, $sp, 4
jr $ra
__init_Int_type:
addi $sp, $sp, 0
move $t0, $sp
addi $sp, $sp, -8
sw $ra, 0($sp)
sw $fp, 4($sp)
move $fp, $t0
lw $t0, 0($fp)
la $t1, Int
sw $t1, 0($t0)
lw $v0, 0($fp)
lw $ra, 0($sp)
lw $fp, 4($sp)
addi $sp, $sp, 8
addi $sp, $sp, 4
jr $ra
__init_IO_type:
addi $sp, $sp, 0
move $t0, $sp
addi $sp, $sp, -8
sw $ra, 0($sp)
sw $fp, 4($sp)
move $fp, $t0
lw $t0, 0($fp)
la $t1, IO
sw $t1, 0($t0)
lw $v0, 0($fp)
lw $ra, 0($sp)
lw $fp, 4($sp)
addi $sp, $sp, 8
addi $sp, $sp, 4
jr $ra
function_out_string_at_IO:
addi $sp, $sp, 0
move $t0, $sp
addi $sp, $sp, -8
sw $ra, 0($sp)
sw $fp, 4($sp)
move $fp, $t0
lw $a0, 0($fp)
addi $v0, $zero, 4
syscall
li $v0, 0
lw $ra, 0($sp)
lw $fp, 4($sp)
addi $sp, $sp, 8
addi $sp, $sp, 8
jr $ra
function_out_int_at_IO:
addi $sp, $sp, 0
move $t0, $sp
addi $sp, $sp, -8
sw $ra, 0($sp)
sw $fp, 4($sp)
move $fp, $t0
lw $a0, 0($fp)
addi $v0, $zero, 1
syscall
li $v0, 0
lw $ra, 0($sp)
lw $fp, 4($sp)
addi $sp, $sp, 8
addi $sp, $sp, 8
jr $ra
function_in_string_at_IO:
addi $sp, $sp, -4
move $t0, $sp
addi $sp, $sp, -8
sw $ra, 0($sp)
sw $fp, 4($sp)
move $fp, $t0
li $a1, 1024
move $a0, $a1
li $v0, 9
syscall
# HERE
move $a0, $v0
addi $v0, $zero, 8
syscall
sw $a0, 0($fp)
lw $v0, 0($fp)
lw $ra, 0($sp)
lw $fp, 4($sp)
addi $sp, $sp, 8
addi $sp, $sp, 8
jr $ra
function_in_int_at_IO:
addi $sp, $sp, -4
move $t0, $sp
addi $sp, $sp, -8
sw $ra, 0($sp)
sw $fp, 4($sp)
move $fp, $t0
addi $v0, $zero, 5
syscall
sw $v0, 0($fp)
lw $v0, 0($fp)
lw $ra, 0($sp)
lw $fp, 4($sp)
addi $sp, $sp, 8
addi $sp, $sp, 8
jr $ra
__init_Main_type:
addi $sp, $sp, 0
move $t0, $sp
addi $sp, $sp, -8
sw $ra, 0($sp)
sw $fp, 4($sp)
move $fp, $t0
lw $t0, 0($fp)
la $t1, Main
sw $t1, 0($t0)
lw $v0, 0($fp)
lw $ra, 0($sp)
lw $fp, 4($sp)
addi $sp, $sp, 8
addi $sp, $sp, 4
jr $ra
function_main_at_Main:
addi $sp, $sp, -16
move $t0, $sp
addi $sp, $sp, -8
sw $ra, 0($sp)
sw $fp, 4($sp)
move $fp, $t0
la $t0, data_6
sw $t0, 0($fp)
la $t0, data_7
sw $t0, 4($fp)
lw $t0, 0($fp)
addi $sp, $sp, -4
sw $t0, 0($sp)
lw $t0, 4($fp)
addi $sp, $sp, -4
sw $t0, 0($sp)
jal function_concat_at_String
sw $v0, 8($fp)
lw $t0, 16($fp)
addi $sp, $sp, -4
sw $t0, 0($sp)
lw $t0, 8($fp)
addi $sp, $sp, -4
sw $t0, 0($sp)
jal function_out_string_at_IO
sw $v0, 12($fp)
lw $v0, 12($fp)
lw $ra, 0($sp)
lw $fp, 4($sp)
addi $sp, $sp, 8
addi $sp, $sp, 20
jr $ra
.data
Object: .word 0, 4, data_0, function_abort_at_Object, function_type_name_at_Object, function_copy_at_Object, __init_Object_type
String: .word Object, 4, data_1, function_abort_at_Object, function_type_name_at_Object, function_copy_at_Object, function_length_at_String, function_concat_at_String, function_substr_at_String, __init_String_type
Bool: .word Object, 4, data_2, function_abort_at_Object, function_type_name_at_Object, function_copy_at_Object, __init_Bool_type
Int: .word Object, 4, data_3, function_abort_at_Object, function_type_name_at_Object, function_copy_at_Object, __init_Int_type
IO: .word Object, 4, data_4, function_abort_at_Object, function_type_name_at_Object, function_copy_at_Object, function_out_string_at_IO, function_out_int_at_IO, function_in_string_at_IO, function_in_int_at_IO, __init_IO_type
Main: .word IO, 4, data_5, function_abort_at_Object, function_type_name_at_Object, function_copy_at_Object, function_out_string_at_IO, function_out_int_at_IO, function_in_string_at_IO, function_in_int_at_IO, function_main_at_Main, __init_Main_type
data_0: .asciiz "Object"
data_1: .asciiz "String"
data_2: .asciiz "Bool"
data_3: .asciiz "Int"
data_4: .asciiz "IO"
data_5: .asciiz "Main"
data_6: .asciiz "Hello "
data_7: .asciiz "World!"