	.data
	.align 4
type: .word 8

	.data
_Board: .asciiz "Board\n"
	.data
	.align 4
Board: .word 16 _Board Init_Board abort_Object type_name_Object copy_Object out_string_IO out_int_IO in_string_IO in_int_IO size_of_board_Board board_init_Board

	.data
_CellularAutomaton: .asciiz "CellularAutomaton\n"
	.data
	.align 4
CellularAutomaton: .word 20 _CellularAutomaton Init_CellularAutomaton abort_Object type_name_Object copy_Object out_string_IO out_int_IO in_string_IO in_int_IO size_of_board_Board board_init_Board init_CellularAutomaton print_CellularAutomaton num_cells_CellularAutomaton cell_CellularAutomaton north_CellularAutomaton south_CellularAutomaton east_CellularAutomaton west_CellularAutomaton northwest_CellularAutomaton northeast_CellularAutomaton southeast_CellularAutomaton southwest_CellularAutomaton neighbors_CellularAutomaton cell_at_next_evolution_CellularAutomaton evolve_CellularAutomaton option_CellularAutomaton prompt_CellularAutomaton prompt2_CellularAutomaton

	.data
_Main: .asciiz "Main\n"
	.data
	.align 4
Main: .word 24 _Main Init_Main abort_Object type_name_Object copy_Object out_string_IO out_int_IO in_string_IO in_int_IO size_of_board_Board board_init_Board init_CellularAutomaton print_CellularAutomaton num_cells_CellularAutomaton cell_CellularAutomaton north_CellularAutomaton south_CellularAutomaton east_CellularAutomaton west_CellularAutomaton northwest_CellularAutomaton northeast_CellularAutomaton southeast_CellularAutomaton southwest_CellularAutomaton neighbors_CellularAutomaton cell_at_next_evolution_CellularAutomaton evolve_CellularAutomaton option_CellularAutomaton prompt_CellularAutomaton prompt2_CellularAutomaton main_Main

	.data
_Object: .asciiz "Object\n"
	.data
	.align 4
Object: .word 4 _Object Init_Object abort_Object type_name_Object copy_Object

	.data
_Int: .asciiz "Int\n"
	.data
	.align 4
Int: .word 8 _Int Init_Int abort_Object type_name_Object copy_Object

	.data
_String: .asciiz "String\n"
	.data
	.align 4
String: .word 8 _String Init_String abort_Object type_name_Object copy_Object length_String concat_String substr_String

	.data
_Bool: .asciiz "Bool\n"
	.data
	.align 4
Bool: .word 8 _Bool Init_Bool abort_Object type_name_Object copy_Object

	.data
_IO: .asciiz "IO\n"
	.data
	.align 4
IO: .word 4 _IO Init_IO abort_Object type_name_Object copy_Object out_string_IO out_int_IO in_string_IO in_int_IO

	.data
ObjectAbortMessage : .asciiz "Abort called from class "
	.data
IO_Buffer : .space 1001
	.data
str_empty: .asciiz ""

	.data
str_0: .asciiz "\n"

	.data
str_1: .asciiz "\n"

	.data
str_2: .asciiz "\n"

	.data
str_3: .asciiz " "

	.data
str_4: .asciiz " "

	.data
str_5: .asciiz " "

	.data
str_6: .asciiz " "

	.data
str_7: .asciiz " "

	.data
str_8: .asciiz " "

	.data
str_9: .asciiz " "

	.data
str_10: .asciiz " "

	.data
str_11: .asciiz " "

	.data
str_12: .asciiz " "

	.data
str_13: .asciiz " "

	.data
str_14: .asciiz " "

	.data
str_15: .asciiz " "

	.data
str_16: .asciiz " "

	.data
str_17: .asciiz "X"

	.data
str_18: .asciiz "X"

	.data
str_19: .asciiz "X"

	.data
str_20: .asciiz "X"

	.data
str_21: .asciiz "X"

	.data
str_22: .asciiz "X"

	.data
str_23: .asciiz "X"

	.data
str_24: .asciiz "X"

	.data
str_25: .asciiz "-"

	.data
str_26: .asciiz "X"

	.data
str_27: .asciiz "-"

	.data
str_28: .asciiz "X"

	.data
str_29: .asciiz "X"

	.data
str_30: .asciiz "\nPlease chose a number:\n"

	.data
str_31: .asciiz "\t1: A cross\n"

	.data
str_32: .asciiz "\t2: A slash from the upper left to lower right\n"

	.data
str_33: .asciiz "\t3: A slash from the upper right to lower left\n"

	.data
str_34: .asciiz "\t4: An X\n"

	.data
str_35: .asciiz "\t5: A greater than sign \n"

	.data
str_36: .asciiz "\t6: A less than sign\n"

	.data
str_37: .asciiz "\t7: Two greater than signs\n"

	.data
str_38: .asciiz "\t8: Two less than signs\n"

	.data
str_39: .asciiz "\t9: A 'V'\n"

	.data
str_40: .asciiz "\t10: An inverse 'V'\n"

	.data
str_41: .asciiz "\t11: Numbers 9 and 10 combined\n"

	.data
str_42: .asciiz "\t12: A full grid\n"

	.data
str_43: .asciiz "\t13: A 'T'\n"

	.data
str_44: .asciiz "\t14: A plus '+'\n"

	.data
str_45: .asciiz "\t15: A 'W'\n"

	.data
str_46: .asciiz "\t16: An 'M'\n"

	.data
str_47: .asciiz "\t17: An 'E'\n"

	.data
str_48: .asciiz "\t18: A '3'\n"

	.data
str_49: .asciiz "\t19: An 'O'\n"

	.data
str_50: .asciiz "\t20: An '8'\n"

	.data
str_51: .asciiz "\t21: An 'S'\n"

	.data
str_52: .asciiz "Your choice => "

	.data
str_53: .asciiz "\n"

	.data
str_54: .asciiz "                         "

	.data
str_55: .asciiz " XXXX   X    XX    X   XXXX "

	.data
str_56: .asciiz " XX X  XX  X XX X  XX  X XX "

	.data
str_57: .asciiz " XX X  XX  X XX "

	.data
str_58: .asciiz "XXX    X   X  X    X   XXXX "

	.data
str_59: .asciiz "XXXXX   X   XXXXX   X   XXXX"

	.data
str_60: .asciiz "  X X   X X X X     X"

	.data
str_61: .asciiz "X     X X X X   X X  "

	.data
str_62: .asciiz "  X    X  XXXXX  X    X  "

	.data
str_63: .asciiz "XXXXX  X    X    X    X  "

	.data
str_64: .asciiz "XXXXXXXXXXXXXXXXXXXXXXXXX"

	.data
str_65: .asciiz "X X X X X X X X"

	.data
str_66: .asciiz "  X   X X X   X"

	.data
str_67: .asciiz "X   X X X   X  "

	.data
str_68: .asciiz " X  XX  X  X  X     "

	.data
str_69: .asciiz "X  X  X  XX  X      "

	.data
str_70: .asciiz "    X   X   X     X     X"

	.data
str_71: .asciiz "X     X     X   X   X    "

	.data
str_72: .asciiz "X   X X X   X   X X X   X"

	.data
str_73: .asciiz "X     X     X     X     X"

	.data
str_74: .asciiz "    X   X   X   X   X    "

	.data
str_75: .asciiz " XX  XXXX XXXX  XX  "

	.data
str_76: .asciiz "Would you like to continue with the next generation? \n"

	.data
str_77: .asciiz "Please use lowercase y or n for your answer [y]: "

	.data
str_78: .asciiz "\n"

	.data
str_79: .asciiz "n"

	.data
str_80: .asciiz "\n\n"

	.data
str_81: .asciiz "Would you like to choose a background pattern? \n"

	.data
str_82: .asciiz "Please use lowercase y or n for your answer [n]: "

	.data
str_83: .asciiz "y"

	.data
str_84: .asciiz "Welcome to the Game of Life.\n"

	.data
str_85: .asciiz "There are many initial states to choose from. \n"

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
	li $a0, 24
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
	lw $t0, 0($v0)
	lw $v1, 8($t0)
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
	lw $t0, 0($v0)
	lw $v1, 120($t0)
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
size_of_board_Board:
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
	
	# assign (add here the expr.to_string) to t_1
	#load the variable initial_0
	lw $v0, 12($fp)
	sw $v0, -0($fp)
	
	lw $v0, -0($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	# assign (add here the expr.to_string) to t_2
	# calling the method length of type String
	#load the variable t_1
	lw $v0, -0($fp)
	lw $t0, 0($v0)
	lw $v1, 24($t0)
	jal $v1
	# pop the top of the stack to $v1
	addi $sp $sp 4
	lw $v1, 0($sp)
	
	sw $v0, -4($fp)
	
	# assign (add here the expr.to_string) to t_3
	#load the variable t_2
	lw $v0, -4($fp)
	sw $v0, -8($fp)
	
	# return the value of the function in the register $v0
	#load the variable t_3
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
	
	jr $ra
	
	.text
board_init_Board:
	# save the return address and frame pointer
	# push $ra to the stack
	sw $ra, 0($sp)
	addi $sp $sp -4
	
	# push $fp to the stack
	sw $fp, 0($sp)
	addi $sp $sp -4
	
	# update the frame pointer and allocate the frame in the stack
	move $fp $sp
	subu $sp $sp 88
	
	# assign (add here the expr.to_string) to t_6
	#load the variable start_4
	lw $v0, 12($fp)
	sw $v0, -4($fp)
	
	lw $v0, 16($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	lw $v0, -4($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	# assign (add here the expr.to_string) to t_7
	# calling the method size_of_board of type Board
	#load the variable self_Board
	lw $v0, 16($fp)
	lw $t0, 0($v0)
	lw $v1, 40($t0)
	jal $v1
	# pop the top of the stack to $v1
	addi $sp $sp 4
	lw $v1, 0($sp)
	
	# pop the top of the stack to $v1
	addi $sp $sp 4
	lw $v1, 0($sp)
	
	sw $v0, -8($fp)
	
	# assign (add here the expr.to_string) to size_5
	#load the variable t_7
	lw $v0, -8($fp)
	sw $v0, -0($fp)
	
	# assign (add here the expr.to_string) to t_8
	#load the variable size_5
	lw $v0, -0($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	# Creating Int instance for atomic 15
	li $a0, 8
	li $v0, 9
	syscall
	la $t0, Int
	li $t1, 15
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
	
	sw $v0, -12($fp)
	
	# assign (add here the expr.to_string) to t_9
	#load the variable t_8
	lw $v0, -12($fp)
	sw $v0, -16($fp)
	
	lw $t1, -16($fp)
	lw $t0, 4($t1)
	bne $t0, $zero, then_0
	# assign (add here the expr.to_string) to t_11
	#load the variable size_5
	lw $v0, -0($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	# Creating Int instance for atomic 16
	li $a0, 8
	li $v0, 9
	syscall
	la $t0, Int
	li $t1, 16
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
	
	# assign (add here the expr.to_string) to t_12
	#load the variable t_11
	lw $v0, -24($fp)
	sw $v0, -28($fp)
	
	lw $t1, -28($fp)
	lw $t0, 4($t1)
	bne $t0, $zero, then_1
	# assign (add here the expr.to_string) to t_14
	#load the variable size_5
	lw $v0, -0($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	# Creating Int instance for atomic 20
	li $a0, 8
	li $v0, 9
	syscall
	la $t0, Int
	li $t1, 20
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
	
	sw $v0, -36($fp)
	
	# assign (add here the expr.to_string) to t_15
	#load the variable t_14
	lw $v0, -36($fp)
	sw $v0, -40($fp)
	
	lw $t1, -40($fp)
	lw $t0, 4($t1)
	bne $t0, $zero, then_2
	# assign (add here the expr.to_string) to t_17
	#load the variable size_5
	lw $v0, -0($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	# Creating Int instance for atomic 21
	li $a0, 8
	li $v0, 9
	syscall
	la $t0, Int
	li $t1, 21
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
	
	sw $v0, -48($fp)
	
	# assign (add here the expr.to_string) to t_18
	#load the variable t_17
	lw $v0, -48($fp)
	sw $v0, -52($fp)
	
	lw $t1, -52($fp)
	lw $t0, 4($t1)
	bne $t0, $zero, then_3
	# assign (add here the expr.to_string) to t_20
	#load the variable size_5
	lw $v0, -0($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	# Creating Int instance for atomic 25
	li $a0, 8
	li $v0, 9
	syscall
	la $t0, Int
	li $t1, 25
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
	
	sw $v0, -60($fp)
	
	# assign (add here the expr.to_string) to t_21
	#load the variable t_20
	lw $v0, -60($fp)
	sw $v0, -64($fp)
	
	lw $t1, -64($fp)
	lw $t0, 4($t1)
	bne $t0, $zero, then_4
	# assign (add here the expr.to_string) to t_23
	#load the variable size_5
	lw $v0, -0($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	# Creating Int instance for atomic 28
	li $a0, 8
	li $v0, 9
	syscall
	la $t0, Int
	li $t1, 28
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
	
	sw $v0, -72($fp)
	
	# assign (add here the expr.to_string) to t_24
	#load the variable t_23
	lw $v0, -72($fp)
	sw $v0, -76($fp)
	
	lw $t1, -76($fp)
	lw $t0, 4($t1)
	bne $t0, $zero, then_5
	# Setting value of the attribute rows in the instance self_Board to 5
	# Creating Int instance for atomic 5
	li $a0, 8
	li $v0, 9
	syscall
	la $t0, Int
	li $t1, 5
	sw $t0, 0($v0)
	sw $t1, 4($v0)
	
	move $s2, $v0
	lw $v1, 16($fp)
	sw $s2, 4($v1)
	
	# Setting value of the attribute columns in the instance self_Board to 5
	# Creating Int instance for atomic 5
	li $a0, 8
	li $v0, 9
	syscall
	la $t0, Int
	li $t1, 5
	sw $t0, 0($v0)
	sw $t1, 4($v0)
	
	move $s2, $v0
	lw $v1, 16($fp)
	sw $s2, 8($v1)
	
	# Setting value of the attribute board_size in the instance self_Board to size_5
	#load the variable size_5
	lw $v0, -0($fp)
	move $s2, $v0
	lw $v1, 16($fp)
	sw $s2, 12($v1)
	
	# assign (add here the expr.to_string) to t_25
	#load the variable size_5
	lw $v0, -0($fp)
	sw $v0, -80($fp)
	
	j ifend_5
	then_5:
	# Setting value of the attribute rows in the instance self_Board to 7
	# Creating Int instance for atomic 7
	li $a0, 8
	li $v0, 9
	syscall
	la $t0, Int
	li $t1, 7
	sw $t0, 0($v0)
	sw $t1, 4($v0)
	
	move $s2, $v0
	lw $v1, 16($fp)
	sw $s2, 4($v1)
	
	# Setting value of the attribute columns in the instance self_Board to 4
	# Creating Int instance for atomic 4
	li $a0, 8
	li $v0, 9
	syscall
	la $t0, Int
	li $t1, 4
	sw $t0, 0($v0)
	sw $t1, 4($v0)
	
	move $s2, $v0
	lw $v1, 16($fp)
	sw $s2, 8($v1)
	
	# Setting value of the attribute board_size in the instance self_Board to size_5
	#load the variable size_5
	lw $v0, -0($fp)
	move $s2, $v0
	lw $v1, 16($fp)
	sw $s2, 12($v1)
	
	# assign (add here the expr.to_string) to t_25
	#load the variable size_5
	lw $v0, -0($fp)
	sw $v0, -80($fp)
	
	ifend_5:
	# assign (add here the expr.to_string) to t_22
	#load the variable t_25
	lw $v0, -80($fp)
	sw $v0, -68($fp)
	
	j ifend_4
	then_4:
	# Setting value of the attribute rows in the instance self_Board to 5
	# Creating Int instance for atomic 5
	li $a0, 8
	li $v0, 9
	syscall
	la $t0, Int
	li $t1, 5
	sw $t0, 0($v0)
	sw $t1, 4($v0)
	
	move $s2, $v0
	lw $v1, 16($fp)
	sw $s2, 4($v1)
	
	# Setting value of the attribute columns in the instance self_Board to 5
	# Creating Int instance for atomic 5
	li $a0, 8
	li $v0, 9
	syscall
	la $t0, Int
	li $t1, 5
	sw $t0, 0($v0)
	sw $t1, 4($v0)
	
	move $s2, $v0
	lw $v1, 16($fp)
	sw $s2, 8($v1)
	
	# Setting value of the attribute board_size in the instance self_Board to size_5
	#load the variable size_5
	lw $v0, -0($fp)
	move $s2, $v0
	lw $v1, 16($fp)
	sw $s2, 12($v1)
	
	# assign (add here the expr.to_string) to t_22
	#load the variable size_5
	lw $v0, -0($fp)
	sw $v0, -68($fp)
	
	ifend_4:
	# assign (add here the expr.to_string) to t_19
	#load the variable t_22
	lw $v0, -68($fp)
	sw $v0, -56($fp)
	
	j ifend_3
	then_3:
	# Setting value of the attribute rows in the instance self_Board to 3
	# Creating Int instance for atomic 3
	li $a0, 8
	li $v0, 9
	syscall
	la $t0, Int
	li $t1, 3
	sw $t0, 0($v0)
	sw $t1, 4($v0)
	
	move $s2, $v0
	lw $v1, 16($fp)
	sw $s2, 4($v1)
	
	# Setting value of the attribute columns in the instance self_Board to 7
	# Creating Int instance for atomic 7
	li $a0, 8
	li $v0, 9
	syscall
	la $t0, Int
	li $t1, 7
	sw $t0, 0($v0)
	sw $t1, 4($v0)
	
	move $s2, $v0
	lw $v1, 16($fp)
	sw $s2, 8($v1)
	
	# Setting value of the attribute board_size in the instance self_Board to size_5
	#load the variable size_5
	lw $v0, -0($fp)
	move $s2, $v0
	lw $v1, 16($fp)
	sw $s2, 12($v1)
	
	# assign (add here the expr.to_string) to t_19
	#load the variable size_5
	lw $v0, -0($fp)
	sw $v0, -56($fp)
	
	ifend_3:
	# assign (add here the expr.to_string) to t_16
	#load the variable t_19
	lw $v0, -56($fp)
	sw $v0, -44($fp)
	
	j ifend_2
	then_2:
	# Setting value of the attribute rows in the instance self_Board to 4
	# Creating Int instance for atomic 4
	li $a0, 8
	li $v0, 9
	syscall
	la $t0, Int
	li $t1, 4
	sw $t0, 0($v0)
	sw $t1, 4($v0)
	
	move $s2, $v0
	lw $v1, 16($fp)
	sw $s2, 4($v1)
	
	# Setting value of the attribute columns in the instance self_Board to 5
	# Creating Int instance for atomic 5
	li $a0, 8
	li $v0, 9
	syscall
	la $t0, Int
	li $t1, 5
	sw $t0, 0($v0)
	sw $t1, 4($v0)
	
	move $s2, $v0
	lw $v1, 16($fp)
	sw $s2, 8($v1)
	
	# Setting value of the attribute board_size in the instance self_Board to size_5
	#load the variable size_5
	lw $v0, -0($fp)
	move $s2, $v0
	lw $v1, 16($fp)
	sw $s2, 12($v1)
	
	# assign (add here the expr.to_string) to t_16
	#load the variable size_5
	lw $v0, -0($fp)
	sw $v0, -44($fp)
	
	ifend_2:
	# assign (add here the expr.to_string) to t_13
	#load the variable t_16
	lw $v0, -44($fp)
	sw $v0, -32($fp)
	
	j ifend_1
	then_1:
	# Setting value of the attribute rows in the instance self_Board to 4
	# Creating Int instance for atomic 4
	li $a0, 8
	li $v0, 9
	syscall
	la $t0, Int
	li $t1, 4
	sw $t0, 0($v0)
	sw $t1, 4($v0)
	
	move $s2, $v0
	lw $v1, 16($fp)
	sw $s2, 4($v1)
	
	# Setting value of the attribute columns in the instance self_Board to 4
	# Creating Int instance for atomic 4
	li $a0, 8
	li $v0, 9
	syscall
	la $t0, Int
	li $t1, 4
	sw $t0, 0($v0)
	sw $t1, 4($v0)
	
	move $s2, $v0
	lw $v1, 16($fp)
	sw $s2, 8($v1)
	
	# Setting value of the attribute board_size in the instance self_Board to size_5
	#load the variable size_5
	lw $v0, -0($fp)
	move $s2, $v0
	lw $v1, 16($fp)
	sw $s2, 12($v1)
	
	# assign (add here the expr.to_string) to t_13
	#load the variable size_5
	lw $v0, -0($fp)
	sw $v0, -32($fp)
	
	ifend_1:
	# assign (add here the expr.to_string) to t_10
	#load the variable t_13
	lw $v0, -32($fp)
	sw $v0, -20($fp)
	
	j ifend_0
	then_0:
	# Setting value of the attribute rows in the instance self_Board to 3
	# Creating Int instance for atomic 3
	li $a0, 8
	li $v0, 9
	syscall
	la $t0, Int
	li $t1, 3
	sw $t0, 0($v0)
	sw $t1, 4($v0)
	
	move $s2, $v0
	lw $v1, 16($fp)
	sw $s2, 4($v1)
	
	# Setting value of the attribute columns in the instance self_Board to 5
	# Creating Int instance for atomic 5
	li $a0, 8
	li $v0, 9
	syscall
	la $t0, Int
	li $t1, 5
	sw $t0, 0($v0)
	sw $t1, 4($v0)
	
	move $s2, $v0
	lw $v1, 16($fp)
	sw $s2, 8($v1)
	
	# Setting value of the attribute board_size in the instance self_Board to size_5
	#load the variable size_5
	lw $v0, -0($fp)
	move $s2, $v0
	lw $v1, 16($fp)
	sw $s2, 12($v1)
	
	# assign (add here the expr.to_string) to t_10
	#load the variable size_5
	lw $v0, -0($fp)
	sw $v0, -20($fp)
	
	ifend_0:
	# assign (add here the expr.to_string) to t_26
	#load the variable self_Board
	lw $v0, 16($fp)
	sw $v0, -84($fp)
	
	# return the value of the function in the register $v0
	#load the variable t_26
	lw $v0, -84($fp)
	move $v0, $v0
	
	# restore the stack pointer, frame pointer y return address
	addu $sp $sp 88
	# pop the top of the stack to $fp
	addi $sp $sp 4
	lw $fp, 0($sp)
	
	# pop the top of the stack to $ra
	addi $sp $sp 4
	lw $ra, 0($sp)
	
	jr $ra
	
	.text
Init_Board:
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
	
	# assign (add here the expr.to_string) to self_Board
	jal Init_IO
	# pop the top of the stack to $v1
	addi $sp $sp 4
	lw $v1, 0($sp)
	
	sw $v0, 12($fp)
	
	# Setting value of the attribute rows in the instance self_Board to 0
	# Creating Int instance for atomic 0
	li $a0, 8
	li $v0, 9
	syscall
	la $t0, Int
	li $t1, 0
	sw $t0, 0($v0)
	sw $t1, 4($v0)
	
	move $s2, $v0
	lw $v1, 12($fp)
	sw $s2, 4($v1)
	
	# Setting value of the attribute columns in the instance self_Board to 0
	# Creating Int instance for atomic 0
	li $a0, 8
	li $v0, 9
	syscall
	la $t0, Int
	li $t1, 0
	sw $t0, 0($v0)
	sw $t1, 4($v0)
	
	move $s2, $v0
	lw $v1, 12($fp)
	sw $s2, 8($v1)
	
	# Setting value of the attribute board_size in the instance self_Board to 0
	# Creating Int instance for atomic 0
	li $a0, 8
	li $v0, 9
	syscall
	la $t0, Int
	li $t1, 0
	sw $t0, 0($v0)
	sw $t1, 4($v0)
	
	move $s2, $v0
	lw $v1, 12($fp)
	sw $s2, 12($v1)
	
	# return the value of the function in the register $v0
	#load the variable self_Board
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
init_CellularAutomaton:
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
	
	# Setting value of the attribute population_map in the instance self_CellularAutomaton to map_27
	#load the variable map_27
	lw $v0, 12($fp)
	move $s2, $v0
	lw $v1, 16($fp)
	sw $s2, 16($v1)
	
	# assign (add here the expr.to_string) to t_28
	#load the variable map_27
	lw $v0, 12($fp)
	sw $v0, -0($fp)
	
	lw $v0, 16($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	lw $v0, -0($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	# assign (add here the expr.to_string) to t_29
	# calling the method board_init of type CellularAutomaton
	#load the variable self_CellularAutomaton
	lw $v0, 16($fp)
	lw $t0, 0($v0)
	lw $v1, 44($t0)
	jal $v1
	# pop the top of the stack to $v1
	addi $sp $sp 4
	lw $v1, 0($sp)
	
	# pop the top of the stack to $v1
	addi $sp $sp 4
	lw $v1, 0($sp)
	
	sw $v0, -4($fp)
	
	# assign (add here the expr.to_string) to t_30
	#load the variable self_CellularAutomaton
	lw $v0, 16($fp)
	sw $v0, -8($fp)
	
	# return the value of the function in the register $v0
	#load the variable t_30
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
	
	jr $ra
	
	.text
print_CellularAutomaton:
	# save the return address and frame pointer
	# push $ra to the stack
	sw $ra, 0($sp)
	addi $sp $sp -4
	
	# push $fp to the stack
	sw $fp, 0($sp)
	addi $sp $sp -4
	
	# update the frame pointer and allocate the frame in the stack
	move $fp $sp
	subu $sp $sp 104
	
	# assign (add here the expr.to_string) to i_31
	# Creating Int instance for atomic 0
	li $a0, 8
	li $v0, 9
	syscall
	la $t0, Int
	li $t1, 0
	sw $t0, 0($v0)
	sw $t1, 4($v0)
	
	sw $v0, -0($fp)
	
	# assign (add here the expr.to_string) to t_33
	lw $v1, 12($fp)
	lw $v0, 12($v1)
	sw $v0, -8($fp)
	
	# assign (add here the expr.to_string) to num_32
	#load the variable t_33
	lw $v0, -8($fp)
	sw $v0, -4($fp)
	
	# assign (add here the expr.to_string) to t_34
	#load the string str_0
	li $a0, 8
	li $v0, 9
	syscall
	la $v1, String
	sw $v1, 0($v0)
	la $v1, str_0
	sw $v1, 4($v0)
	sw $v0, -12($fp)
	
	# assign (add here the expr.to_string) to t_35
	#load the variable t_34
	lw $v0, -12($fp)
	sw $v0, -16($fp)
	
	lw $v0, 12($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	lw $v0, -16($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	# assign (add here the expr.to_string) to t_36
	# calling the method out_string of type CellularAutomaton
	#load the variable self_CellularAutomaton
	lw $v0, 12($fp)
	lw $t0, 0($v0)
	lw $v1, 24($t0)
	jal $v1
	# pop the top of the stack to $v1
	addi $sp $sp 4
	lw $v1, 0($sp)
	
	# pop the top of the stack to $v1
	addi $sp $sp 4
	lw $v1, 0($sp)
	
	sw $v0, -20($fp)
	
	while_0:
	# assign (add here the expr.to_string) to t_37
	#load the variable i_31
	lw $v0, -0($fp)
	move $t1, $v0
	lw $t1, 4($t1)
	#load the variable num_32
	lw $v0, -4($fp)
	move $t2, $v0
	lw $t2, 4($t2)
	slt $t3, $t1, $t2
	la $t4, Bool
	li $a0, 8
	li $v0, 9
	syscall
	sw $t4, 0($v0)
	sw $t3, 4($v0)
	sw $v0, -24($fp)
	
	# assign (add here the expr.to_string) to t_38
	#load the variable t_37
	lw $v0, -24($fp)
	sw $v0, -28($fp)
	
	lw $t1, -28($fp)
	lw $t0, 4($t1)
	bne $t0, $zero, body_0
	j pool_0
	body_0:
	# assign (add here the expr.to_string) to t_40
	lw $v1, 12($fp)
	lw $v0, 16($v1)
	sw $v0, -36($fp)
	
	# assign (add here the expr.to_string) to t_41
	#load the variable t_40
	lw $v0, -36($fp)
	sw $v0, -40($fp)
	
	# assign (add here the expr.to_string) to t_42
	#load the variable i_31
	lw $v0, -0($fp)
	sw $v0, -44($fp)
	
	# assign (add here the expr.to_string) to t_43
	lw $v1, 12($fp)
	lw $v0, 8($v1)
	sw $v0, -48($fp)
	
	# assign (add here the expr.to_string) to t_44
	#load the variable t_43
	lw $v0, -48($fp)
	sw $v0, -52($fp)
	
	lw $v0, -40($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	lw $v0, -44($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	lw $v0, -52($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	# assign (add here the expr.to_string) to t_45
	# calling the method substr of type String
	#load the variable t_41
	lw $v0, -40($fp)
	lw $t0, 0($v0)
	lw $v1, 32($t0)
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
	
	sw $v0, -56($fp)
	
	# assign (add here the expr.to_string) to t_46
	#load the variable t_45
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
	
	# assign (add here the expr.to_string) to t_47
	# calling the method out_string of type CellularAutomaton
	#load the variable self_CellularAutomaton
	lw $v0, 12($fp)
	lw $t0, 0($v0)
	lw $v1, 24($t0)
	jal $v1
	# pop the top of the stack to $v1
	addi $sp $sp 4
	lw $v1, 0($sp)
	
	# pop the top of the stack to $v1
	addi $sp $sp 4
	lw $v1, 0($sp)
	
	sw $v0, -64($fp)
	
	# assign (add here the expr.to_string) to t_48
	#load the string str_1
	li $a0, 8
	li $v0, 9
	syscall
	la $v1, String
	sw $v1, 0($v0)
	la $v1, str_1
	sw $v1, 4($v0)
	sw $v0, -68($fp)
	
	# assign (add here the expr.to_string) to t_49
	#load the variable t_48
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
	
	# assign (add here the expr.to_string) to t_50
	# calling the method out_string of type CellularAutomaton
	#load the variable self_CellularAutomaton
	lw $v0, 12($fp)
	lw $t0, 0($v0)
	lw $v1, 24($t0)
	jal $v1
	# pop the top of the stack to $v1
	addi $sp $sp 4
	lw $v1, 0($sp)
	
	# pop the top of the stack to $v1
	addi $sp $sp 4
	lw $v1, 0($sp)
	
	sw $v0, -76($fp)
	
	# assign (add here the expr.to_string) to t_51
	lw $v1, 12($fp)
	lw $v0, 8($v1)
	sw $v0, -80($fp)
	
	# assign (add here the expr.to_string) to t_52
	# computes the sum of (node.left.to_string) and (node.right.to_string) and stores it at $v0
	#load the variable i_31
	lw $v0, -0($fp)
	lw $t0, 4($v0)
	# push $t0 to the stack
	sw $t0, 0($sp)
	addi $sp $sp -4
	
	#load the variable t_51
	lw $v0, -80($fp)
	# pop the top of the stack to $t0
	addi $sp $sp 4
	lw $t0, 0($sp)
	
	lw $t1, 4($v0)
	add $t0, $t0, $t1
	li $a0, 8
	li $v0, 9
	syscall
	la $t1, Int
	sw $t1, 0($v0)
	sw $t0, 4($v0)
	sw $v0, -84($fp)
	
	# assign (add here the expr.to_string) to i_31
	#load the variable t_52
	lw $v0, -84($fp)
	sw $v0, -0($fp)
	
	# assign (add here the expr.to_string) to t_39
	#load the variable i_31
	lw $v0, -0($fp)
	sw $v0, -32($fp)
	
	j while_0
	pool_0:
	# assign (add here the expr.to_string) to t_53
	#load the string str_2
	li $a0, 8
	li $v0, 9
	syscall
	la $v1, String
	sw $v1, 0($v0)
	la $v1, str_2
	sw $v1, 4($v0)
	sw $v0, -88($fp)
	
	# assign (add here the expr.to_string) to t_54
	#load the variable t_53
	lw $v0, -88($fp)
	sw $v0, -92($fp)
	
	lw $v0, 12($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	lw $v0, -92($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	# assign (add here the expr.to_string) to t_55
	# calling the method out_string of type CellularAutomaton
	#load the variable self_CellularAutomaton
	lw $v0, 12($fp)
	lw $t0, 0($v0)
	lw $v1, 24($t0)
	jal $v1
	# pop the top of the stack to $v1
	addi $sp $sp 4
	lw $v1, 0($sp)
	
	# pop the top of the stack to $v1
	addi $sp $sp 4
	lw $v1, 0($sp)
	
	sw $v0, -96($fp)
	
	# assign (add here the expr.to_string) to t_56
	#load the variable self_CellularAutomaton
	lw $v0, 12($fp)
	sw $v0, -100($fp)
	
	# return the value of the function in the register $v0
	#load the variable t_56
	lw $v0, -100($fp)
	move $v0, $v0
	
	# restore the stack pointer, frame pointer y return address
	addu $sp $sp 104
	# pop the top of the stack to $fp
	addi $sp $sp 4
	lw $fp, 0($sp)
	
	# pop the top of the stack to $ra
	addi $sp $sp 4
	lw $ra, 0($sp)
	
	jr $ra
	
	.text
num_cells_CellularAutomaton:
	# save the return address and frame pointer
	# push $ra to the stack
	sw $ra, 0($sp)
	addi $sp $sp -4
	
	# push $fp to the stack
	sw $fp, 0($sp)
	addi $sp $sp -4
	
	# update the frame pointer and allocate the frame in the stack
	move $fp $sp
	subu $sp $sp 16
	
	# assign (add here the expr.to_string) to t_57
	lw $v1, 12($fp)
	lw $v0, 16($v1)
	sw $v0, -0($fp)
	
	# assign (add here the expr.to_string) to t_58
	#load the variable t_57
	lw $v0, -0($fp)
	sw $v0, -4($fp)
	
	lw $v0, -4($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	# assign (add here the expr.to_string) to t_59
	# calling the method length of type String
	#load the variable t_58
	lw $v0, -4($fp)
	lw $t0, 0($v0)
	lw $v1, 24($t0)
	jal $v1
	# pop the top of the stack to $v1
	addi $sp $sp 4
	lw $v1, 0($sp)
	
	sw $v0, -8($fp)
	
	# assign (add here the expr.to_string) to t_60
	#load the variable t_59
	lw $v0, -8($fp)
	sw $v0, -12($fp)
	
	# return the value of the function in the register $v0
	#load the variable t_60
	lw $v0, -12($fp)
	move $v0, $v0
	
	# restore the stack pointer, frame pointer y return address
	addu $sp $sp 16
	# pop the top of the stack to $fp
	addi $sp $sp 4
	lw $fp, 0($sp)
	
	# pop the top of the stack to $ra
	addi $sp $sp 4
	lw $ra, 0($sp)
	
	jr $ra
	
	.text
cell_CellularAutomaton:
	# save the return address and frame pointer
	# push $ra to the stack
	sw $ra, 0($sp)
	addi $sp $sp -4
	
	# push $fp to the stack
	sw $fp, 0($sp)
	addi $sp $sp -4
	
	# update the frame pointer and allocate the frame in the stack
	move $fp $sp
	subu $sp $sp 48
	
	# assign (add here the expr.to_string) to t_62
	lw $v1, 16($fp)
	lw $v0, 12($v1)
	sw $v0, -0($fp)
	
	# assign (add here the expr.to_string) to t_63
	# computes the sub of (node.left.to_string) and (node.right.to_string) and stores it at $v0
	#load the variable t_62
	lw $v0, -0($fp)
	lw $t0, 4($v0)
	# push $t0 to the stack
	sw $t0, 0($sp)
	addi $sp $sp -4
	
	# Creating Int instance for atomic 1
	li $a0, 8
	li $v0, 9
	syscall
	la $t0, Int
	li $t1, 1
	sw $t0, 0($v0)
	sw $t1, 4($v0)
	
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
	sw $v0, -4($fp)
	
	# assign (add here the expr.to_string) to t_64
	#load the variable t_63
	lw $v0, -4($fp)
	move $t1, $v0
	lw $t1, 4($t1)
	#load the variable position_61
	lw $v0, 12($fp)
	move $t2, $v0
	lw $t2, 4($t2)
	slt $t3, $t1, $t2
	la $t4, Bool
	li $a0, 8
	li $v0, 9
	syscall
	sw $t4, 0($v0)
	sw $t3, 4($v0)
	sw $v0, -8($fp)
	
	# assign (add here the expr.to_string) to t_65
	#load the variable t_64
	lw $v0, -8($fp)
	sw $v0, -12($fp)
	
	lw $t1, -12($fp)
	lw $t0, 4($t1)
	bne $t0, $zero, then_6
	# assign (add here the expr.to_string) to t_67
	lw $v1, 16($fp)
	lw $v0, 16($v1)
	sw $v0, -20($fp)
	
	# assign (add here the expr.to_string) to t_68
	#load the variable t_67
	lw $v0, -20($fp)
	sw $v0, -24($fp)
	
	# assign (add here the expr.to_string) to t_69
	#load the variable position_61
	lw $v0, 12($fp)
	sw $v0, -28($fp)
	
	# assign (add here the expr.to_string) to t_70
	# Creating Int instance for atomic 1
	li $a0, 8
	li $v0, 9
	syscall
	la $t0, Int
	li $t1, 1
	sw $t0, 0($v0)
	sw $t1, 4($v0)
	
	sw $v0, -32($fp)
	
	lw $v0, -24($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	lw $v0, -28($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	lw $v0, -32($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	# assign (add here the expr.to_string) to t_71
	# calling the method substr of type String
	#load the variable t_68
	lw $v0, -24($fp)
	lw $t0, 0($v0)
	lw $v1, 32($t0)
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
	
	sw $v0, -36($fp)
	
	# assign (add here the expr.to_string) to t_66
	#load the variable t_71
	lw $v0, -36($fp)
	sw $v0, -16($fp)
	
	j ifend_6
	then_6:
	# assign (add here the expr.to_string) to t_72
	#load the string str_3
	li $a0, 8
	li $v0, 9
	syscall
	la $v1, String
	sw $v1, 0($v0)
	la $v1, str_3
	sw $v1, 4($v0)
	sw $v0, -40($fp)
	
	# assign (add here the expr.to_string) to t_66
	#load the variable t_72
	lw $v0, -40($fp)
	sw $v0, -16($fp)
	
	ifend_6:
	# assign (add here the expr.to_string) to t_73
	#load the variable t_66
	lw $v0, -16($fp)
	sw $v0, -44($fp)
	
	# return the value of the function in the register $v0
	#load the variable t_73
	lw $v0, -44($fp)
	move $v0, $v0
	
	# restore the stack pointer, frame pointer y return address
	addu $sp $sp 48
	# pop the top of the stack to $fp
	addi $sp $sp 4
	lw $fp, 0($sp)
	
	# pop the top of the stack to $ra
	addi $sp $sp 4
	lw $ra, 0($sp)
	
	jr $ra
	
	.text
north_CellularAutomaton:
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
	
	# assign (add here the expr.to_string) to t_75
	lw $v1, 16($fp)
	lw $v0, 8($v1)
	sw $v0, -0($fp)
	
	# assign (add here the expr.to_string) to t_76
	# computes the sub of (node.left.to_string) and (node.right.to_string) and stores it at $v0
	#load the variable position_74
	lw $v0, 12($fp)
	lw $t0, 4($v0)
	# push $t0 to the stack
	sw $t0, 0($sp)
	addi $sp $sp -4
	
	#load the variable t_75
	lw $v0, -0($fp)
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
	sw $v0, -4($fp)
	
	# assign (add here the expr.to_string) to t_77
	#load the variable t_76
	lw $v0, -4($fp)
	move $t1, $v0
	lw $t1, 4($t1)
	# Creating Int instance for atomic 0
	li $a0, 8
	li $v0, 9
	syscall
	la $t0, Int
	li $t1, 0
	sw $t0, 0($v0)
	sw $t1, 4($v0)
	
	move $t2, $v0
	lw $t2, 4($t2)
	slt $t3, $t1, $t2
	la $t4, Bool
	li $a0, 8
	li $v0, 9
	syscall
	sw $t4, 0($v0)
	sw $t3, 4($v0)
	sw $v0, -8($fp)
	
	# assign (add here the expr.to_string) to t_78
	#load the variable t_77
	lw $v0, -8($fp)
	sw $v0, -12($fp)
	
	lw $t1, -12($fp)
	lw $t0, 4($t1)
	bne $t0, $zero, then_7
	# assign (add here the expr.to_string) to t_80
	lw $v1, 16($fp)
	lw $v0, 8($v1)
	sw $v0, -20($fp)
	
	# assign (add here the expr.to_string) to t_81
	# computes the sub of (node.left.to_string) and (node.right.to_string) and stores it at $v0
	#load the variable position_74
	lw $v0, 12($fp)
	lw $t0, 4($v0)
	# push $t0 to the stack
	sw $t0, 0($sp)
	addi $sp $sp -4
	
	#load the variable t_80
	lw $v0, -20($fp)
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
	sw $v0, -24($fp)
	
	# assign (add here the expr.to_string) to t_82
	#load the variable t_81
	lw $v0, -24($fp)
	sw $v0, -28($fp)
	
	lw $v0, 16($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	lw $v0, -28($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	# assign (add here the expr.to_string) to t_83
	# calling the method cell of type CellularAutomaton
	#load the variable self_CellularAutomaton
	lw $v0, 16($fp)
	lw $t0, 0($v0)
	lw $v1, 60($t0)
	jal $v1
	# pop the top of the stack to $v1
	addi $sp $sp 4
	lw $v1, 0($sp)
	
	# pop the top of the stack to $v1
	addi $sp $sp 4
	lw $v1, 0($sp)
	
	sw $v0, -32($fp)
	
	# assign (add here the expr.to_string) to t_79
	#load the variable t_83
	lw $v0, -32($fp)
	sw $v0, -16($fp)
	
	j ifend_7
	then_7:
	# assign (add here the expr.to_string) to t_84
	#load the string str_4
	li $a0, 8
	li $v0, 9
	syscall
	la $v1, String
	sw $v1, 0($v0)
	la $v1, str_4
	sw $v1, 4($v0)
	sw $v0, -36($fp)
	
	# assign (add here the expr.to_string) to t_79
	#load the variable t_84
	lw $v0, -36($fp)
	sw $v0, -16($fp)
	
	ifend_7:
	# assign (add here the expr.to_string) to t_85
	#load the variable t_79
	lw $v0, -16($fp)
	sw $v0, -40($fp)
	
	# return the value of the function in the register $v0
	#load the variable t_85
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
south_CellularAutomaton:
	# save the return address and frame pointer
	# push $ra to the stack
	sw $ra, 0($sp)
	addi $sp $sp -4
	
	# push $fp to the stack
	sw $fp, 0($sp)
	addi $sp $sp -4
	
	# update the frame pointer and allocate the frame in the stack
	move $fp $sp
	subu $sp $sp 48
	
	# assign (add here the expr.to_string) to t_87
	lw $v1, 16($fp)
	lw $v0, 12($v1)
	sw $v0, -0($fp)
	
	# assign (add here the expr.to_string) to t_88
	lw $v1, 16($fp)
	lw $v0, 8($v1)
	sw $v0, -4($fp)
	
	# assign (add here the expr.to_string) to t_89
	# computes the sum of (node.left.to_string) and (node.right.to_string) and stores it at $v0
	#load the variable position_86
	lw $v0, 12($fp)
	lw $t0, 4($v0)
	# push $t0 to the stack
	sw $t0, 0($sp)
	addi $sp $sp -4
	
	#load the variable t_88
	lw $v0, -4($fp)
	# pop the top of the stack to $t0
	addi $sp $sp 4
	lw $t0, 0($sp)
	
	lw $t1, 4($v0)
	add $t0, $t0, $t1
	li $a0, 8
	li $v0, 9
	syscall
	la $t1, Int
	sw $t1, 0($v0)
	sw $t0, 4($v0)
	sw $v0, -8($fp)
	
	# assign (add here the expr.to_string) to t_90
	#load the variable t_87
	lw $v0, -0($fp)
	move $t1, $v0
	lw $t1, 4($t1)
	#load the variable t_89
	lw $v0, -8($fp)
	move $t2, $v0
	lw $t2, 4($t2)
	slt $t3, $t1, $t2
	la $t4, Bool
	li $a0, 8
	li $v0, 9
	syscall
	sw $t4, 0($v0)
	sw $t3, 4($v0)
	sw $v0, -12($fp)
	
	# assign (add here the expr.to_string) to t_91
	#load the variable t_90
	lw $v0, -12($fp)
	sw $v0, -16($fp)
	
	lw $t1, -16($fp)
	lw $t0, 4($t1)
	bne $t0, $zero, then_8
	# assign (add here the expr.to_string) to t_93
	lw $v1, 16($fp)
	lw $v0, 8($v1)
	sw $v0, -24($fp)
	
	# assign (add here the expr.to_string) to t_94
	# computes the sum of (node.left.to_string) and (node.right.to_string) and stores it at $v0
	#load the variable position_86
	lw $v0, 12($fp)
	lw $t0, 4($v0)
	# push $t0 to the stack
	sw $t0, 0($sp)
	addi $sp $sp -4
	
	#load the variable t_93
	lw $v0, -24($fp)
	# pop the top of the stack to $t0
	addi $sp $sp 4
	lw $t0, 0($sp)
	
	lw $t1, 4($v0)
	add $t0, $t0, $t1
	li $a0, 8
	li $v0, 9
	syscall
	la $t1, Int
	sw $t1, 0($v0)
	sw $t0, 4($v0)
	sw $v0, -28($fp)
	
	# assign (add here the expr.to_string) to t_95
	#load the variable t_94
	lw $v0, -28($fp)
	sw $v0, -32($fp)
	
	lw $v0, 16($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	lw $v0, -32($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	# assign (add here the expr.to_string) to t_96
	# calling the method cell of type CellularAutomaton
	#load the variable self_CellularAutomaton
	lw $v0, 16($fp)
	lw $t0, 0($v0)
	lw $v1, 60($t0)
	jal $v1
	# pop the top of the stack to $v1
	addi $sp $sp 4
	lw $v1, 0($sp)
	
	# pop the top of the stack to $v1
	addi $sp $sp 4
	lw $v1, 0($sp)
	
	sw $v0, -36($fp)
	
	# assign (add here the expr.to_string) to t_92
	#load the variable t_96
	lw $v0, -36($fp)
	sw $v0, -20($fp)
	
	j ifend_8
	then_8:
	# assign (add here the expr.to_string) to t_97
	#load the string str_5
	li $a0, 8
	li $v0, 9
	syscall
	la $v1, String
	sw $v1, 0($v0)
	la $v1, str_5
	sw $v1, 4($v0)
	sw $v0, -40($fp)
	
	# assign (add here the expr.to_string) to t_92
	#load the variable t_97
	lw $v0, -40($fp)
	sw $v0, -20($fp)
	
	ifend_8:
	# assign (add here the expr.to_string) to t_98
	#load the variable t_92
	lw $v0, -20($fp)
	sw $v0, -44($fp)
	
	# return the value of the function in the register $v0
	#load the variable t_98
	lw $v0, -44($fp)
	move $v0, $v0
	
	# restore the stack pointer, frame pointer y return address
	addu $sp $sp 48
	# pop the top of the stack to $fp
	addi $sp $sp 4
	lw $fp, 0($sp)
	
	# pop the top of the stack to $ra
	addi $sp $sp 4
	lw $ra, 0($sp)
	
	jr $ra
	
	.text
east_CellularAutomaton:
	# save the return address and frame pointer
	# push $ra to the stack
	sw $ra, 0($sp)
	addi $sp $sp -4
	
	# push $fp to the stack
	sw $fp, 0($sp)
	addi $sp $sp -4
	
	# update the frame pointer and allocate the frame in the stack
	move $fp $sp
	subu $sp $sp 56
	
	# assign (add here the expr.to_string) to t_100
	# computes the sum of (node.left.to_string) and (node.right.to_string) and stores it at $v0
	#load the variable position_99
	lw $v0, 12($fp)
	lw $t0, 4($v0)
	# push $t0 to the stack
	sw $t0, 0($sp)
	addi $sp $sp -4
	
	# Creating Int instance for atomic 1
	li $a0, 8
	li $v0, 9
	syscall
	la $t0, Int
	li $t1, 1
	sw $t0, 0($v0)
	sw $t1, 4($v0)
	
	# pop the top of the stack to $t0
	addi $sp $sp 4
	lw $t0, 0($sp)
	
	lw $t1, 4($v0)
	add $t0, $t0, $t1
	li $a0, 8
	li $v0, 9
	syscall
	la $t1, Int
	sw $t1, 0($v0)
	sw $t0, 4($v0)
	sw $v0, -0($fp)
	
	# assign (add here the expr.to_string) to t_101
	lw $v1, 16($fp)
	lw $v0, 8($v1)
	sw $v0, -4($fp)
	
	# assign (add here the expr.to_string) to t_102
	# computes the sub of (node.left.to_string) and (node.right.to_string) and stores it at $v0
	#load the variable t_100
	lw $v0, -0($fp)
	lw $t0, 4($v0)
	# push $t0 to the stack
	sw $t0, 0($sp)
	addi $sp $sp -4
	
	#load the variable t_101
	lw $v0, -4($fp)
	lw $t1, 4($v0)
	# pop the top of the stack to $t0
	addi $sp $sp 4
	lw $t0, 0($sp)
	
	div $t0, $t1
	mflo $t0
	li $a0, 8
	li $v0, 9
	syscall
	la $t1, Int
	sw $t1, 0($v0)
	sw $t0, 4($v0)
	sw $v0, -8($fp)
	
	# assign (add here the expr.to_string) to t_103
	lw $v1, 16($fp)
	lw $v0, 8($v1)
	sw $v0, -12($fp)
	
	# assign (add here the expr.to_string) to t_104
	# computes the sub of (node.left.to_string) and (node.right.to_string) and stores it at $v0
	#load the variable t_102
	lw $v0, -8($fp)
	lw $t0, 4($v0)
	# push $t0 to the stack
	sw $t0, 0($sp)
	addi $sp $sp -4
	
	#load the variable t_103
	lw $v0, -12($fp)
	lw $t1, 4($v0)
	# pop the top of the stack to $t0
	addi $sp $sp 4
	lw $t0, 0($sp)
	
	mult $t0, $t1
	mflo $t0
	li $a0, 8
	li $v0, 9
	syscall
	la $t1, Int
	sw $t1, 0($v0)
	sw $t0, 4($v0)
	sw $v0, -16($fp)
	
	# assign (add here the expr.to_string) to t_105
	# computes the sum of (node.left.to_string) and (node.right.to_string) and stores it at $v0
	#load the variable position_99
	lw $v0, 12($fp)
	lw $t0, 4($v0)
	# push $t0 to the stack
	sw $t0, 0($sp)
	addi $sp $sp -4
	
	# Creating Int instance for atomic 1
	li $a0, 8
	li $v0, 9
	syscall
	la $t0, Int
	li $t1, 1
	sw $t0, 0($v0)
	sw $t1, 4($v0)
	
	# pop the top of the stack to $t0
	addi $sp $sp 4
	lw $t0, 0($sp)
	
	lw $t1, 4($v0)
	add $t0, $t0, $t1
	li $a0, 8
	li $v0, 9
	syscall
	la $t1, Int
	sw $t1, 0($v0)
	sw $t0, 4($v0)
	sw $v0, -20($fp)
	
	# assign (add here the expr.to_string) to t_106
	#load the variable t_104
	lw $v0, -16($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	#load the variable t_105
	lw $v0, -20($fp)
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
	
	# assign (add here the expr.to_string) to t_107
	#load the variable t_106
	lw $v0, -24($fp)
	sw $v0, -28($fp)
	
	lw $t1, -28($fp)
	lw $t0, 4($t1)
	bne $t0, $zero, then_9
	# assign (add here the expr.to_string) to t_109
	# computes the sum of (node.left.to_string) and (node.right.to_string) and stores it at $v0
	#load the variable position_99
	lw $v0, 12($fp)
	lw $t0, 4($v0)
	# push $t0 to the stack
	sw $t0, 0($sp)
	addi $sp $sp -4
	
	# Creating Int instance for atomic 1
	li $a0, 8
	li $v0, 9
	syscall
	la $t0, Int
	li $t1, 1
	sw $t0, 0($v0)
	sw $t1, 4($v0)
	
	# pop the top of the stack to $t0
	addi $sp $sp 4
	lw $t0, 0($sp)
	
	lw $t1, 4($v0)
	add $t0, $t0, $t1
	li $a0, 8
	li $v0, 9
	syscall
	la $t1, Int
	sw $t1, 0($v0)
	sw $t0, 4($v0)
	sw $v0, -36($fp)
	
	# assign (add here the expr.to_string) to t_110
	#load the variable t_109
	lw $v0, -36($fp)
	sw $v0, -40($fp)
	
	lw $v0, 16($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	lw $v0, -40($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	# assign (add here the expr.to_string) to t_111
	# calling the method cell of type CellularAutomaton
	#load the variable self_CellularAutomaton
	lw $v0, 16($fp)
	lw $t0, 0($v0)
	lw $v1, 60($t0)
	jal $v1
	# pop the top of the stack to $v1
	addi $sp $sp 4
	lw $v1, 0($sp)
	
	# pop the top of the stack to $v1
	addi $sp $sp 4
	lw $v1, 0($sp)
	
	sw $v0, -44($fp)
	
	# assign (add here the expr.to_string) to t_108
	#load the variable t_111
	lw $v0, -44($fp)
	sw $v0, -32($fp)
	
	j ifend_9
	then_9:
	# assign (add here the expr.to_string) to t_112
	#load the string str_6
	li $a0, 8
	li $v0, 9
	syscall
	la $v1, String
	sw $v1, 0($v0)
	la $v1, str_6
	sw $v1, 4($v0)
	sw $v0, -48($fp)
	
	# assign (add here the expr.to_string) to t_108
	#load the variable t_112
	lw $v0, -48($fp)
	sw $v0, -32($fp)
	
	ifend_9:
	# assign (add here the expr.to_string) to t_113
	#load the variable t_108
	lw $v0, -32($fp)
	sw $v0, -52($fp)
	
	# return the value of the function in the register $v0
	#load the variable t_113
	lw $v0, -52($fp)
	move $v0, $v0
	
	# restore the stack pointer, frame pointer y return address
	addu $sp $sp 56
	# pop the top of the stack to $fp
	addi $sp $sp 4
	lw $fp, 0($sp)
	
	# pop the top of the stack to $ra
	addi $sp $sp 4
	lw $ra, 0($sp)
	
	jr $ra
	
	.text
west_CellularAutomaton:
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
	
	# assign (add here the expr.to_string) to t_115
	#load the variable position_114
	lw $v0, 12($fp)
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
	
	# assign (add here the expr.to_string) to t_116
	#load the variable t_115
	lw $v0, -0($fp)
	sw $v0, -4($fp)
	
	lw $t1, -4($fp)
	lw $t0, 4($t1)
	bne $t0, $zero, then_10
	# assign (add here the expr.to_string) to t_118
	lw $v1, 16($fp)
	lw $v0, 8($v1)
	sw $v0, -12($fp)
	
	# assign (add here the expr.to_string) to t_119
	# computes the sub of (node.left.to_string) and (node.right.to_string) and stores it at $v0
	#load the variable position_114
	lw $v0, 12($fp)
	lw $t0, 4($v0)
	# push $t0 to the stack
	sw $t0, 0($sp)
	addi $sp $sp -4
	
	#load the variable t_118
	lw $v0, -12($fp)
	lw $t1, 4($v0)
	# pop the top of the stack to $t0
	addi $sp $sp 4
	lw $t0, 0($sp)
	
	div $t0, $t1
	mflo $t0
	li $a0, 8
	li $v0, 9
	syscall
	la $t1, Int
	sw $t1, 0($v0)
	sw $t0, 4($v0)
	sw $v0, -16($fp)
	
	# assign (add here the expr.to_string) to t_120
	lw $v1, 16($fp)
	lw $v0, 8($v1)
	sw $v0, -20($fp)
	
	# assign (add here the expr.to_string) to t_121
	# computes the sub of (node.left.to_string) and (node.right.to_string) and stores it at $v0
	#load the variable t_119
	lw $v0, -16($fp)
	lw $t0, 4($v0)
	# push $t0 to the stack
	sw $t0, 0($sp)
	addi $sp $sp -4
	
	#load the variable t_120
	lw $v0, -20($fp)
	lw $t1, 4($v0)
	# pop the top of the stack to $t0
	addi $sp $sp 4
	lw $t0, 0($sp)
	
	mult $t0, $t1
	mflo $t0
	li $a0, 8
	li $v0, 9
	syscall
	la $t1, Int
	sw $t1, 0($v0)
	sw $t0, 4($v0)
	sw $v0, -24($fp)
	
	# assign (add here the expr.to_string) to t_122
	#load the variable t_121
	lw $v0, -24($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	#load the variable position_114
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
	
	sw $v0, -28($fp)
	
	# assign (add here the expr.to_string) to t_123
	#load the variable t_122
	lw $v0, -28($fp)
	sw $v0, -32($fp)
	
	lw $t1, -32($fp)
	lw $t0, 4($t1)
	bne $t0, $zero, then_11
	# assign (add here the expr.to_string) to t_125
	# computes the sub of (node.left.to_string) and (node.right.to_string) and stores it at $v0
	#load the variable position_114
	lw $v0, 12($fp)
	lw $t0, 4($v0)
	# push $t0 to the stack
	sw $t0, 0($sp)
	addi $sp $sp -4
	
	# Creating Int instance for atomic 1
	li $a0, 8
	li $v0, 9
	syscall
	la $t0, Int
	li $t1, 1
	sw $t0, 0($v0)
	sw $t1, 4($v0)
	
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
	sw $v0, -40($fp)
	
	# assign (add here the expr.to_string) to t_126
	#load the variable t_125
	lw $v0, -40($fp)
	sw $v0, -44($fp)
	
	lw $v0, 16($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	lw $v0, -44($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	# assign (add here the expr.to_string) to t_127
	# calling the method cell of type CellularAutomaton
	#load the variable self_CellularAutomaton
	lw $v0, 16($fp)
	lw $t0, 0($v0)
	lw $v1, 60($t0)
	jal $v1
	# pop the top of the stack to $v1
	addi $sp $sp 4
	lw $v1, 0($sp)
	
	# pop the top of the stack to $v1
	addi $sp $sp 4
	lw $v1, 0($sp)
	
	sw $v0, -48($fp)
	
	# assign (add here the expr.to_string) to t_124
	#load the variable t_127
	lw $v0, -48($fp)
	sw $v0, -36($fp)
	
	j ifend_11
	then_11:
	# assign (add here the expr.to_string) to t_128
	#load the string str_7
	li $a0, 8
	li $v0, 9
	syscall
	la $v1, String
	sw $v1, 0($v0)
	la $v1, str_7
	sw $v1, 4($v0)
	sw $v0, -52($fp)
	
	# assign (add here the expr.to_string) to t_124
	#load the variable t_128
	lw $v0, -52($fp)
	sw $v0, -36($fp)
	
	ifend_11:
	# assign (add here the expr.to_string) to t_117
	#load the variable t_124
	lw $v0, -36($fp)
	sw $v0, -8($fp)
	
	j ifend_10
	then_10:
	# assign (add here the expr.to_string) to t_129
	#load the string str_8
	li $a0, 8
	li $v0, 9
	syscall
	la $v1, String
	sw $v1, 0($v0)
	la $v1, str_8
	sw $v1, 4($v0)
	sw $v0, -56($fp)
	
	# assign (add here the expr.to_string) to t_117
	#load the variable t_129
	lw $v0, -56($fp)
	sw $v0, -8($fp)
	
	ifend_10:
	# assign (add here the expr.to_string) to t_130
	#load the variable t_117
	lw $v0, -8($fp)
	sw $v0, -60($fp)
	
	# return the value of the function in the register $v0
	#load the variable t_130
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
northwest_CellularAutomaton:
	# save the return address and frame pointer
	# push $ra to the stack
	sw $ra, 0($sp)
	addi $sp $sp -4
	
	# push $fp to the stack
	sw $fp, 0($sp)
	addi $sp $sp -4
	
	# update the frame pointer and allocate the frame in the stack
	move $fp $sp
	subu $sp $sp 72
	
	# assign (add here the expr.to_string) to t_132
	lw $v1, 16($fp)
	lw $v0, 8($v1)
	sw $v0, -0($fp)
	
	# assign (add here the expr.to_string) to t_133
	# computes the sub of (node.left.to_string) and (node.right.to_string) and stores it at $v0
	#load the variable position_131
	lw $v0, 12($fp)
	lw $t0, 4($v0)
	# push $t0 to the stack
	sw $t0, 0($sp)
	addi $sp $sp -4
	
	#load the variable t_132
	lw $v0, -0($fp)
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
	sw $v0, -4($fp)
	
	# assign (add here the expr.to_string) to t_134
	#load the variable t_133
	lw $v0, -4($fp)
	move $t1, $v0
	lw $t1, 4($t1)
	# Creating Int instance for atomic 0
	li $a0, 8
	li $v0, 9
	syscall
	la $t0, Int
	li $t1, 0
	sw $t0, 0($v0)
	sw $t1, 4($v0)
	
	move $t2, $v0
	lw $t2, 4($t2)
	slt $t3, $t1, $t2
	la $t4, Bool
	li $a0, 8
	li $v0, 9
	syscall
	sw $t4, 0($v0)
	sw $t3, 4($v0)
	sw $v0, -8($fp)
	
	# assign (add here the expr.to_string) to t_135
	#load the variable t_134
	lw $v0, -8($fp)
	sw $v0, -12($fp)
	
	lw $t1, -12($fp)
	lw $t0, 4($t1)
	bne $t0, $zero, then_12
	# assign (add here the expr.to_string) to t_137
	lw $v1, 16($fp)
	lw $v0, 8($v1)
	sw $v0, -20($fp)
	
	# assign (add here the expr.to_string) to t_138
	# computes the sub of (node.left.to_string) and (node.right.to_string) and stores it at $v0
	#load the variable position_131
	lw $v0, 12($fp)
	lw $t0, 4($v0)
	# push $t0 to the stack
	sw $t0, 0($sp)
	addi $sp $sp -4
	
	#load the variable t_137
	lw $v0, -20($fp)
	lw $t1, 4($v0)
	# pop the top of the stack to $t0
	addi $sp $sp 4
	lw $t0, 0($sp)
	
	div $t0, $t1
	mflo $t0
	li $a0, 8
	li $v0, 9
	syscall
	la $t1, Int
	sw $t1, 0($v0)
	sw $t0, 4($v0)
	sw $v0, -24($fp)
	
	# assign (add here the expr.to_string) to t_139
	lw $v1, 16($fp)
	lw $v0, 8($v1)
	sw $v0, -28($fp)
	
	# assign (add here the expr.to_string) to t_140
	# computes the sub of (node.left.to_string) and (node.right.to_string) and stores it at $v0
	#load the variable t_138
	lw $v0, -24($fp)
	lw $t0, 4($v0)
	# push $t0 to the stack
	sw $t0, 0($sp)
	addi $sp $sp -4
	
	#load the variable t_139
	lw $v0, -28($fp)
	lw $t1, 4($v0)
	# pop the top of the stack to $t0
	addi $sp $sp 4
	lw $t0, 0($sp)
	
	mult $t0, $t1
	mflo $t0
	li $a0, 8
	li $v0, 9
	syscall
	la $t1, Int
	sw $t1, 0($v0)
	sw $t0, 4($v0)
	sw $v0, -32($fp)
	
	# assign (add here the expr.to_string) to t_141
	#load the variable t_140
	lw $v0, -32($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	#load the variable position_131
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
	
	sw $v0, -36($fp)
	
	# assign (add here the expr.to_string) to t_142
	#load the variable t_141
	lw $v0, -36($fp)
	sw $v0, -40($fp)
	
	lw $t1, -40($fp)
	lw $t0, 4($t1)
	bne $t0, $zero, then_13
	# assign (add here the expr.to_string) to t_144
	# computes the sub of (node.left.to_string) and (node.right.to_string) and stores it at $v0
	#load the variable position_131
	lw $v0, 12($fp)
	lw $t0, 4($v0)
	# push $t0 to the stack
	sw $t0, 0($sp)
	addi $sp $sp -4
	
	# Creating Int instance for atomic 1
	li $a0, 8
	li $v0, 9
	syscall
	la $t0, Int
	li $t1, 1
	sw $t0, 0($v0)
	sw $t1, 4($v0)
	
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
	sw $v0, -48($fp)
	
	# assign (add here the expr.to_string) to t_145
	#load the variable t_144
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
	
	# assign (add here the expr.to_string) to t_146
	# calling the method north of type CellularAutomaton
	#load the variable self_CellularAutomaton
	lw $v0, 16($fp)
	lw $t0, 0($v0)
	lw $v1, 64($t0)
	jal $v1
	# pop the top of the stack to $v1
	addi $sp $sp 4
	lw $v1, 0($sp)
	
	# pop the top of the stack to $v1
	addi $sp $sp 4
	lw $v1, 0($sp)
	
	sw $v0, -56($fp)
	
	# assign (add here the expr.to_string) to t_143
	#load the variable t_146
	lw $v0, -56($fp)
	sw $v0, -44($fp)
	
	j ifend_13
	then_13:
	# assign (add here the expr.to_string) to t_147
	#load the string str_9
	li $a0, 8
	li $v0, 9
	syscall
	la $v1, String
	sw $v1, 0($v0)
	la $v1, str_9
	sw $v1, 4($v0)
	sw $v0, -60($fp)
	
	# assign (add here the expr.to_string) to t_143
	#load the variable t_147
	lw $v0, -60($fp)
	sw $v0, -44($fp)
	
	ifend_13:
	# assign (add here the expr.to_string) to t_136
	#load the variable t_143
	lw $v0, -44($fp)
	sw $v0, -16($fp)
	
	j ifend_12
	then_12:
	# assign (add here the expr.to_string) to t_148
	#load the string str_10
	li $a0, 8
	li $v0, 9
	syscall
	la $v1, String
	sw $v1, 0($v0)
	la $v1, str_10
	sw $v1, 4($v0)
	sw $v0, -64($fp)
	
	# assign (add here the expr.to_string) to t_136
	#load the variable t_148
	lw $v0, -64($fp)
	sw $v0, -16($fp)
	
	ifend_12:
	# assign (add here the expr.to_string) to t_149
	#load the variable t_136
	lw $v0, -16($fp)
	sw $v0, -68($fp)
	
	# return the value of the function in the register $v0
	#load the variable t_149
	lw $v0, -68($fp)
	move $v0, $v0
	
	# restore the stack pointer, frame pointer y return address
	addu $sp $sp 72
	# pop the top of the stack to $fp
	addi $sp $sp 4
	lw $fp, 0($sp)
	
	# pop the top of the stack to $ra
	addi $sp $sp 4
	lw $ra, 0($sp)
	
	jr $ra
	
	.text
northeast_CellularAutomaton:
	# save the return address and frame pointer
	# push $ra to the stack
	sw $ra, 0($sp)
	addi $sp $sp -4
	
	# push $fp to the stack
	sw $fp, 0($sp)
	addi $sp $sp -4
	
	# update the frame pointer and allocate the frame in the stack
	move $fp $sp
	subu $sp $sp 80
	
	# assign (add here the expr.to_string) to t_151
	lw $v1, 16($fp)
	lw $v0, 8($v1)
	sw $v0, -0($fp)
	
	# assign (add here the expr.to_string) to t_152
	# computes the sub of (node.left.to_string) and (node.right.to_string) and stores it at $v0
	#load the variable position_150
	lw $v0, 12($fp)
	lw $t0, 4($v0)
	# push $t0 to the stack
	sw $t0, 0($sp)
	addi $sp $sp -4
	
	#load the variable t_151
	lw $v0, -0($fp)
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
	sw $v0, -4($fp)
	
	# assign (add here the expr.to_string) to t_153
	#load the variable t_152
	lw $v0, -4($fp)
	move $t1, $v0
	lw $t1, 4($t1)
	# Creating Int instance for atomic 0
	li $a0, 8
	li $v0, 9
	syscall
	la $t0, Int
	li $t1, 0
	sw $t0, 0($v0)
	sw $t1, 4($v0)
	
	move $t2, $v0
	lw $t2, 4($t2)
	slt $t3, $t1, $t2
	la $t4, Bool
	li $a0, 8
	li $v0, 9
	syscall
	sw $t4, 0($v0)
	sw $t3, 4($v0)
	sw $v0, -8($fp)
	
	# assign (add here the expr.to_string) to t_154
	#load the variable t_153
	lw $v0, -8($fp)
	sw $v0, -12($fp)
	
	lw $t1, -12($fp)
	lw $t0, 4($t1)
	bne $t0, $zero, then_14
	# assign (add here the expr.to_string) to t_156
	# computes the sum of (node.left.to_string) and (node.right.to_string) and stores it at $v0
	#load the variable position_150
	lw $v0, 12($fp)
	lw $t0, 4($v0)
	# push $t0 to the stack
	sw $t0, 0($sp)
	addi $sp $sp -4
	
	# Creating Int instance for atomic 1
	li $a0, 8
	li $v0, 9
	syscall
	la $t0, Int
	li $t1, 1
	sw $t0, 0($v0)
	sw $t1, 4($v0)
	
	# pop the top of the stack to $t0
	addi $sp $sp 4
	lw $t0, 0($sp)
	
	lw $t1, 4($v0)
	add $t0, $t0, $t1
	li $a0, 8
	li $v0, 9
	syscall
	la $t1, Int
	sw $t1, 0($v0)
	sw $t0, 4($v0)
	sw $v0, -20($fp)
	
	# assign (add here the expr.to_string) to t_157
	lw $v1, 16($fp)
	lw $v0, 8($v1)
	sw $v0, -24($fp)
	
	# assign (add here the expr.to_string) to t_158
	# computes the sub of (node.left.to_string) and (node.right.to_string) and stores it at $v0
	#load the variable t_156
	lw $v0, -20($fp)
	lw $t0, 4($v0)
	# push $t0 to the stack
	sw $t0, 0($sp)
	addi $sp $sp -4
	
	#load the variable t_157
	lw $v0, -24($fp)
	lw $t1, 4($v0)
	# pop the top of the stack to $t0
	addi $sp $sp 4
	lw $t0, 0($sp)
	
	div $t0, $t1
	mflo $t0
	li $a0, 8
	li $v0, 9
	syscall
	la $t1, Int
	sw $t1, 0($v0)
	sw $t0, 4($v0)
	sw $v0, -28($fp)
	
	# assign (add here the expr.to_string) to t_159
	lw $v1, 16($fp)
	lw $v0, 8($v1)
	sw $v0, -32($fp)
	
	# assign (add here the expr.to_string) to t_160
	# computes the sub of (node.left.to_string) and (node.right.to_string) and stores it at $v0
	#load the variable t_158
	lw $v0, -28($fp)
	lw $t0, 4($v0)
	# push $t0 to the stack
	sw $t0, 0($sp)
	addi $sp $sp -4
	
	#load the variable t_159
	lw $v0, -32($fp)
	lw $t1, 4($v0)
	# pop the top of the stack to $t0
	addi $sp $sp 4
	lw $t0, 0($sp)
	
	mult $t0, $t1
	mflo $t0
	li $a0, 8
	li $v0, 9
	syscall
	la $t1, Int
	sw $t1, 0($v0)
	sw $t0, 4($v0)
	sw $v0, -36($fp)
	
	# assign (add here the expr.to_string) to t_161
	# computes the sum of (node.left.to_string) and (node.right.to_string) and stores it at $v0
	#load the variable position_150
	lw $v0, 12($fp)
	lw $t0, 4($v0)
	# push $t0 to the stack
	sw $t0, 0($sp)
	addi $sp $sp -4
	
	# Creating Int instance for atomic 1
	li $a0, 8
	li $v0, 9
	syscall
	la $t0, Int
	li $t1, 1
	sw $t0, 0($v0)
	sw $t1, 4($v0)
	
	# pop the top of the stack to $t0
	addi $sp $sp 4
	lw $t0, 0($sp)
	
	lw $t1, 4($v0)
	add $t0, $t0, $t1
	li $a0, 8
	li $v0, 9
	syscall
	la $t1, Int
	sw $t1, 0($v0)
	sw $t0, 4($v0)
	sw $v0, -40($fp)
	
	# assign (add here the expr.to_string) to t_162
	#load the variable t_160
	lw $v0, -36($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	#load the variable t_161
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
	
	# assign (add here the expr.to_string) to t_163
	#load the variable t_162
	lw $v0, -44($fp)
	sw $v0, -48($fp)
	
	lw $t1, -48($fp)
	lw $t0, 4($t1)
	bne $t0, $zero, then_15
	# assign (add here the expr.to_string) to t_165
	# computes the sum of (node.left.to_string) and (node.right.to_string) and stores it at $v0
	#load the variable position_150
	lw $v0, 12($fp)
	lw $t0, 4($v0)
	# push $t0 to the stack
	sw $t0, 0($sp)
	addi $sp $sp -4
	
	# Creating Int instance for atomic 1
	li $a0, 8
	li $v0, 9
	syscall
	la $t0, Int
	li $t1, 1
	sw $t0, 0($v0)
	sw $t1, 4($v0)
	
	# pop the top of the stack to $t0
	addi $sp $sp 4
	lw $t0, 0($sp)
	
	lw $t1, 4($v0)
	add $t0, $t0, $t1
	li $a0, 8
	li $v0, 9
	syscall
	la $t1, Int
	sw $t1, 0($v0)
	sw $t0, 4($v0)
	sw $v0, -56($fp)
	
	# assign (add here the expr.to_string) to t_166
	#load the variable t_165
	lw $v0, -56($fp)
	sw $v0, -60($fp)
	
	lw $v0, 16($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	lw $v0, -60($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	# assign (add here the expr.to_string) to t_167
	# calling the method north of type CellularAutomaton
	#load the variable self_CellularAutomaton
	lw $v0, 16($fp)
	lw $t0, 0($v0)
	lw $v1, 64($t0)
	jal $v1
	# pop the top of the stack to $v1
	addi $sp $sp 4
	lw $v1, 0($sp)
	
	# pop the top of the stack to $v1
	addi $sp $sp 4
	lw $v1, 0($sp)
	
	sw $v0, -64($fp)
	
	# assign (add here the expr.to_string) to t_164
	#load the variable t_167
	lw $v0, -64($fp)
	sw $v0, -52($fp)
	
	j ifend_15
	then_15:
	# assign (add here the expr.to_string) to t_168
	#load the string str_11
	li $a0, 8
	li $v0, 9
	syscall
	la $v1, String
	sw $v1, 0($v0)
	la $v1, str_11
	sw $v1, 4($v0)
	sw $v0, -68($fp)
	
	# assign (add here the expr.to_string) to t_164
	#load the variable t_168
	lw $v0, -68($fp)
	sw $v0, -52($fp)
	
	ifend_15:
	# assign (add here the expr.to_string) to t_155
	#load the variable t_164
	lw $v0, -52($fp)
	sw $v0, -16($fp)
	
	j ifend_14
	then_14:
	# assign (add here the expr.to_string) to t_169
	#load the string str_12
	li $a0, 8
	li $v0, 9
	syscall
	la $v1, String
	sw $v1, 0($v0)
	la $v1, str_12
	sw $v1, 4($v0)
	sw $v0, -72($fp)
	
	# assign (add here the expr.to_string) to t_155
	#load the variable t_169
	lw $v0, -72($fp)
	sw $v0, -16($fp)
	
	ifend_14:
	# assign (add here the expr.to_string) to t_170
	#load the variable t_155
	lw $v0, -16($fp)
	sw $v0, -76($fp)
	
	# return the value of the function in the register $v0
	#load the variable t_170
	lw $v0, -76($fp)
	move $v0, $v0
	
	# restore the stack pointer, frame pointer y return address
	addu $sp $sp 80
	# pop the top of the stack to $fp
	addi $sp $sp 4
	lw $fp, 0($sp)
	
	# pop the top of the stack to $ra
	addi $sp $sp 4
	lw $ra, 0($sp)
	
	jr $ra
	
	.text
southeast_CellularAutomaton:
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
	
	# assign (add here the expr.to_string) to t_172
	lw $v1, 16($fp)
	lw $v0, 12($v1)
	sw $v0, -0($fp)
	
	# assign (add here the expr.to_string) to t_173
	lw $v1, 16($fp)
	lw $v0, 8($v1)
	sw $v0, -4($fp)
	
	# assign (add here the expr.to_string) to t_174
	# computes the sum of (node.left.to_string) and (node.right.to_string) and stores it at $v0
	#load the variable position_171
	lw $v0, 12($fp)
	lw $t0, 4($v0)
	# push $t0 to the stack
	sw $t0, 0($sp)
	addi $sp $sp -4
	
	#load the variable t_173
	lw $v0, -4($fp)
	# pop the top of the stack to $t0
	addi $sp $sp 4
	lw $t0, 0($sp)
	
	lw $t1, 4($v0)
	add $t0, $t0, $t1
	li $a0, 8
	li $v0, 9
	syscall
	la $t1, Int
	sw $t1, 0($v0)
	sw $t0, 4($v0)
	sw $v0, -8($fp)
	
	# assign (add here the expr.to_string) to t_175
	#load the variable t_172
	lw $v0, -0($fp)
	move $t1, $v0
	lw $t1, 4($t1)
	#load the variable t_174
	lw $v0, -8($fp)
	move $t2, $v0
	lw $t2, 4($t2)
	slt $t3, $t1, $t2
	la $t4, Bool
	li $a0, 8
	li $v0, 9
	syscall
	sw $t4, 0($v0)
	sw $t3, 4($v0)
	sw $v0, -12($fp)
	
	# assign (add here the expr.to_string) to t_176
	#load the variable t_175
	lw $v0, -12($fp)
	sw $v0, -16($fp)
	
	lw $t1, -16($fp)
	lw $t0, 4($t1)
	bne $t0, $zero, then_16
	# assign (add here the expr.to_string) to t_178
	# computes the sum of (node.left.to_string) and (node.right.to_string) and stores it at $v0
	#load the variable position_171
	lw $v0, 12($fp)
	lw $t0, 4($v0)
	# push $t0 to the stack
	sw $t0, 0($sp)
	addi $sp $sp -4
	
	# Creating Int instance for atomic 1
	li $a0, 8
	li $v0, 9
	syscall
	la $t0, Int
	li $t1, 1
	sw $t0, 0($v0)
	sw $t1, 4($v0)
	
	# pop the top of the stack to $t0
	addi $sp $sp 4
	lw $t0, 0($sp)
	
	lw $t1, 4($v0)
	add $t0, $t0, $t1
	li $a0, 8
	li $v0, 9
	syscall
	la $t1, Int
	sw $t1, 0($v0)
	sw $t0, 4($v0)
	sw $v0, -24($fp)
	
	# assign (add here the expr.to_string) to t_179
	lw $v1, 16($fp)
	lw $v0, 8($v1)
	sw $v0, -28($fp)
	
	# assign (add here the expr.to_string) to t_180
	# computes the sub of (node.left.to_string) and (node.right.to_string) and stores it at $v0
	#load the variable t_178
	lw $v0, -24($fp)
	lw $t0, 4($v0)
	# push $t0 to the stack
	sw $t0, 0($sp)
	addi $sp $sp -4
	
	#load the variable t_179
	lw $v0, -28($fp)
	lw $t1, 4($v0)
	# pop the top of the stack to $t0
	addi $sp $sp 4
	lw $t0, 0($sp)
	
	div $t0, $t1
	mflo $t0
	li $a0, 8
	li $v0, 9
	syscall
	la $t1, Int
	sw $t1, 0($v0)
	sw $t0, 4($v0)
	sw $v0, -32($fp)
	
	# assign (add here the expr.to_string) to t_181
	lw $v1, 16($fp)
	lw $v0, 8($v1)
	sw $v0, -36($fp)
	
	# assign (add here the expr.to_string) to t_182
	# computes the sub of (node.left.to_string) and (node.right.to_string) and stores it at $v0
	#load the variable t_180
	lw $v0, -32($fp)
	lw $t0, 4($v0)
	# push $t0 to the stack
	sw $t0, 0($sp)
	addi $sp $sp -4
	
	#load the variable t_181
	lw $v0, -36($fp)
	lw $t1, 4($v0)
	# pop the top of the stack to $t0
	addi $sp $sp 4
	lw $t0, 0($sp)
	
	mult $t0, $t1
	mflo $t0
	li $a0, 8
	li $v0, 9
	syscall
	la $t1, Int
	sw $t1, 0($v0)
	sw $t0, 4($v0)
	sw $v0, -40($fp)
	
	# assign (add here the expr.to_string) to t_183
	# computes the sum of (node.left.to_string) and (node.right.to_string) and stores it at $v0
	#load the variable position_171
	lw $v0, 12($fp)
	lw $t0, 4($v0)
	# push $t0 to the stack
	sw $t0, 0($sp)
	addi $sp $sp -4
	
	# Creating Int instance for atomic 1
	li $a0, 8
	li $v0, 9
	syscall
	la $t0, Int
	li $t1, 1
	sw $t0, 0($v0)
	sw $t1, 4($v0)
	
	# pop the top of the stack to $t0
	addi $sp $sp 4
	lw $t0, 0($sp)
	
	lw $t1, 4($v0)
	add $t0, $t0, $t1
	li $a0, 8
	li $v0, 9
	syscall
	la $t1, Int
	sw $t1, 0($v0)
	sw $t0, 4($v0)
	sw $v0, -44($fp)
	
	# assign (add here the expr.to_string) to t_184
	#load the variable t_182
	lw $v0, -40($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	#load the variable t_183
	lw $v0, -44($fp)
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
	
	sw $v0, -48($fp)
	
	# assign (add here the expr.to_string) to t_185
	#load the variable t_184
	lw $v0, -48($fp)
	sw $v0, -52($fp)
	
	lw $t1, -52($fp)
	lw $t0, 4($t1)
	bne $t0, $zero, then_17
	# assign (add here the expr.to_string) to t_187
	# computes the sum of (node.left.to_string) and (node.right.to_string) and stores it at $v0
	#load the variable position_171
	lw $v0, 12($fp)
	lw $t0, 4($v0)
	# push $t0 to the stack
	sw $t0, 0($sp)
	addi $sp $sp -4
	
	# Creating Int instance for atomic 1
	li $a0, 8
	li $v0, 9
	syscall
	la $t0, Int
	li $t1, 1
	sw $t0, 0($v0)
	sw $t1, 4($v0)
	
	# pop the top of the stack to $t0
	addi $sp $sp 4
	lw $t0, 0($sp)
	
	lw $t1, 4($v0)
	add $t0, $t0, $t1
	li $a0, 8
	li $v0, 9
	syscall
	la $t1, Int
	sw $t1, 0($v0)
	sw $t0, 4($v0)
	sw $v0, -60($fp)
	
	# assign (add here the expr.to_string) to t_188
	#load the variable t_187
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
	
	# assign (add here the expr.to_string) to t_189
	# calling the method south of type CellularAutomaton
	#load the variable self_CellularAutomaton
	lw $v0, 16($fp)
	lw $t0, 0($v0)
	lw $v1, 68($t0)
	jal $v1
	# pop the top of the stack to $v1
	addi $sp $sp 4
	lw $v1, 0($sp)
	
	# pop the top of the stack to $v1
	addi $sp $sp 4
	lw $v1, 0($sp)
	
	sw $v0, -68($fp)
	
	# assign (add here the expr.to_string) to t_186
	#load the variable t_189
	lw $v0, -68($fp)
	sw $v0, -56($fp)
	
	j ifend_17
	then_17:
	# assign (add here the expr.to_string) to t_190
	#load the string str_13
	li $a0, 8
	li $v0, 9
	syscall
	la $v1, String
	sw $v1, 0($v0)
	la $v1, str_13
	sw $v1, 4($v0)
	sw $v0, -72($fp)
	
	# assign (add here the expr.to_string) to t_186
	#load the variable t_190
	lw $v0, -72($fp)
	sw $v0, -56($fp)
	
	ifend_17:
	# assign (add here the expr.to_string) to t_177
	#load the variable t_186
	lw $v0, -56($fp)
	sw $v0, -20($fp)
	
	j ifend_16
	then_16:
	# assign (add here the expr.to_string) to t_191
	#load the string str_14
	li $a0, 8
	li $v0, 9
	syscall
	la $v1, String
	sw $v1, 0($v0)
	la $v1, str_14
	sw $v1, 4($v0)
	sw $v0, -76($fp)
	
	# assign (add here the expr.to_string) to t_177
	#load the variable t_191
	lw $v0, -76($fp)
	sw $v0, -20($fp)
	
	ifend_16:
	# assign (add here the expr.to_string) to t_192
	#load the variable t_177
	lw $v0, -20($fp)
	sw $v0, -80($fp)
	
	# return the value of the function in the register $v0
	#load the variable t_192
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
southwest_CellularAutomaton:
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
	
	# assign (add here the expr.to_string) to t_194
	lw $v1, 16($fp)
	lw $v0, 12($v1)
	sw $v0, -0($fp)
	
	# assign (add here the expr.to_string) to t_195
	lw $v1, 16($fp)
	lw $v0, 8($v1)
	sw $v0, -4($fp)
	
	# assign (add here the expr.to_string) to t_196
	# computes the sum of (node.left.to_string) and (node.right.to_string) and stores it at $v0
	#load the variable position_193
	lw $v0, 12($fp)
	lw $t0, 4($v0)
	# push $t0 to the stack
	sw $t0, 0($sp)
	addi $sp $sp -4
	
	#load the variable t_195
	lw $v0, -4($fp)
	# pop the top of the stack to $t0
	addi $sp $sp 4
	lw $t0, 0($sp)
	
	lw $t1, 4($v0)
	add $t0, $t0, $t1
	li $a0, 8
	li $v0, 9
	syscall
	la $t1, Int
	sw $t1, 0($v0)
	sw $t0, 4($v0)
	sw $v0, -8($fp)
	
	# assign (add here the expr.to_string) to t_197
	#load the variable t_194
	lw $v0, -0($fp)
	move $t1, $v0
	lw $t1, 4($t1)
	#load the variable t_196
	lw $v0, -8($fp)
	move $t2, $v0
	lw $t2, 4($t2)
	slt $t3, $t1, $t2
	la $t4, Bool
	li $a0, 8
	li $v0, 9
	syscall
	sw $t4, 0($v0)
	sw $t3, 4($v0)
	sw $v0, -12($fp)
	
	# assign (add here the expr.to_string) to t_198
	#load the variable t_197
	lw $v0, -12($fp)
	sw $v0, -16($fp)
	
	lw $t1, -16($fp)
	lw $t0, 4($t1)
	bne $t0, $zero, then_18
	# assign (add here the expr.to_string) to t_200
	lw $v1, 16($fp)
	lw $v0, 8($v1)
	sw $v0, -24($fp)
	
	# assign (add here the expr.to_string) to t_201
	# computes the sub of (node.left.to_string) and (node.right.to_string) and stores it at $v0
	#load the variable position_193
	lw $v0, 12($fp)
	lw $t0, 4($v0)
	# push $t0 to the stack
	sw $t0, 0($sp)
	addi $sp $sp -4
	
	#load the variable t_200
	lw $v0, -24($fp)
	lw $t1, 4($v0)
	# pop the top of the stack to $t0
	addi $sp $sp 4
	lw $t0, 0($sp)
	
	div $t0, $t1
	mflo $t0
	li $a0, 8
	li $v0, 9
	syscall
	la $t1, Int
	sw $t1, 0($v0)
	sw $t0, 4($v0)
	sw $v0, -28($fp)
	
	# assign (add here the expr.to_string) to t_202
	lw $v1, 16($fp)
	lw $v0, 8($v1)
	sw $v0, -32($fp)
	
	# assign (add here the expr.to_string) to t_203
	# computes the sub of (node.left.to_string) and (node.right.to_string) and stores it at $v0
	#load the variable t_201
	lw $v0, -28($fp)
	lw $t0, 4($v0)
	# push $t0 to the stack
	sw $t0, 0($sp)
	addi $sp $sp -4
	
	#load the variable t_202
	lw $v0, -32($fp)
	lw $t1, 4($v0)
	# pop the top of the stack to $t0
	addi $sp $sp 4
	lw $t0, 0($sp)
	
	mult $t0, $t1
	mflo $t0
	li $a0, 8
	li $v0, 9
	syscall
	la $t1, Int
	sw $t1, 0($v0)
	sw $t0, 4($v0)
	sw $v0, -36($fp)
	
	# assign (add here the expr.to_string) to t_204
	#load the variable t_203
	lw $v0, -36($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	#load the variable position_193
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
	
	sw $v0, -40($fp)
	
	# assign (add here the expr.to_string) to t_205
	#load the variable t_204
	lw $v0, -40($fp)
	sw $v0, -44($fp)
	
	lw $t1, -44($fp)
	lw $t0, 4($t1)
	bne $t0, $zero, then_19
	# assign (add here the expr.to_string) to t_207
	# computes the sub of (node.left.to_string) and (node.right.to_string) and stores it at $v0
	#load the variable position_193
	lw $v0, 12($fp)
	lw $t0, 4($v0)
	# push $t0 to the stack
	sw $t0, 0($sp)
	addi $sp $sp -4
	
	# Creating Int instance for atomic 1
	li $a0, 8
	li $v0, 9
	syscall
	la $t0, Int
	li $t1, 1
	sw $t0, 0($v0)
	sw $t1, 4($v0)
	
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
	sw $v0, -52($fp)
	
	# assign (add here the expr.to_string) to t_208
	#load the variable t_207
	lw $v0, -52($fp)
	sw $v0, -56($fp)
	
	lw $v0, 16($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	lw $v0, -56($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	# assign (add here the expr.to_string) to t_209
	# calling the method south of type CellularAutomaton
	#load the variable self_CellularAutomaton
	lw $v0, 16($fp)
	lw $t0, 0($v0)
	lw $v1, 68($t0)
	jal $v1
	# pop the top of the stack to $v1
	addi $sp $sp 4
	lw $v1, 0($sp)
	
	# pop the top of the stack to $v1
	addi $sp $sp 4
	lw $v1, 0($sp)
	
	sw $v0, -60($fp)
	
	# assign (add here the expr.to_string) to t_206
	#load the variable t_209
	lw $v0, -60($fp)
	sw $v0, -48($fp)
	
	j ifend_19
	then_19:
	# assign (add here the expr.to_string) to t_210
	#load the string str_15
	li $a0, 8
	li $v0, 9
	syscall
	la $v1, String
	sw $v1, 0($v0)
	la $v1, str_15
	sw $v1, 4($v0)
	sw $v0, -64($fp)
	
	# assign (add here the expr.to_string) to t_206
	#load the variable t_210
	lw $v0, -64($fp)
	sw $v0, -48($fp)
	
	ifend_19:
	# assign (add here the expr.to_string) to t_199
	#load the variable t_206
	lw $v0, -48($fp)
	sw $v0, -20($fp)
	
	j ifend_18
	then_18:
	# assign (add here the expr.to_string) to t_211
	#load the string str_16
	li $a0, 8
	li $v0, 9
	syscall
	la $v1, String
	sw $v1, 0($v0)
	la $v1, str_16
	sw $v1, 4($v0)
	sw $v0, -68($fp)
	
	# assign (add here the expr.to_string) to t_199
	#load the variable t_211
	lw $v0, -68($fp)
	sw $v0, -20($fp)
	
	ifend_18:
	# assign (add here the expr.to_string) to t_212
	#load the variable t_199
	lw $v0, -20($fp)
	sw $v0, -72($fp)
	
	# return the value of the function in the register $v0
	#load the variable t_212
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
neighbors_CellularAutomaton:
	# save the return address and frame pointer
	# push $ra to the stack
	sw $ra, 0($sp)
	addi $sp $sp -4
	
	# push $fp to the stack
	sw $fp, 0($sp)
	addi $sp $sp -4
	
	# update the frame pointer and allocate the frame in the stack
	move $fp $sp
	subu $sp $sp 224
	
	# assign (add here the expr.to_string) to t_214
	#load the variable position_213
	lw $v0, 12($fp)
	sw $v0, -0($fp)
	
	lw $v0, 16($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	lw $v0, -0($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	# assign (add here the expr.to_string) to t_215
	# calling the method north of type CellularAutomaton
	#load the variable self_CellularAutomaton
	lw $v0, 16($fp)
	lw $t0, 0($v0)
	lw $v1, 64($t0)
	jal $v1
	# pop the top of the stack to $v1
	addi $sp $sp 4
	lw $v1, 0($sp)
	
	# pop the top of the stack to $v1
	addi $sp $sp 4
	lw $v1, 0($sp)
	
	sw $v0, -4($fp)
	
	# assign (add here the expr.to_string) to t_216
	#load the string str_17
	li $a0, 8
	li $v0, 9
	syscall
	la $v1, String
	sw $v1, 0($v0)
	la $v1, str_17
	sw $v1, 4($v0)
	sw $v0, -8($fp)
	
	# assign (add here the expr.to_string) to t_217
	#load the variable t_215
	lw $v0, -4($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	#load the variable t_216
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
	
	# assign (add here the expr.to_string) to t_218
	#load the variable t_217
	lw $v0, -12($fp)
	sw $v0, -16($fp)
	
	lw $t1, -16($fp)
	lw $t0, 4($t1)
	bne $t0, $zero, then_20
	# assign (add here the expr.to_string) to t_219
	# Creating Int instance for atomic 0
	li $a0, 8
	li $v0, 9
	syscall
	la $t0, Int
	li $t1, 0
	sw $t0, 0($v0)
	sw $t1, 4($v0)
	
	sw $v0, -20($fp)
	
	j ifend_20
	then_20:
	# assign (add here the expr.to_string) to t_219
	# Creating Int instance for atomic 1
	li $a0, 8
	li $v0, 9
	syscall
	la $t0, Int
	li $t1, 1
	sw $t0, 0($v0)
	sw $t1, 4($v0)
	
	sw $v0, -20($fp)
	
	ifend_20:
	# assign (add here the expr.to_string) to t_220
	#load the variable position_213
	lw $v0, 12($fp)
	sw $v0, -24($fp)
	
	lw $v0, 16($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	lw $v0, -24($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	# assign (add here the expr.to_string) to t_221
	# calling the method south of type CellularAutomaton
	#load the variable self_CellularAutomaton
	lw $v0, 16($fp)
	lw $t0, 0($v0)
	lw $v1, 68($t0)
	jal $v1
	# pop the top of the stack to $v1
	addi $sp $sp 4
	lw $v1, 0($sp)
	
	# pop the top of the stack to $v1
	addi $sp $sp 4
	lw $v1, 0($sp)
	
	sw $v0, -28($fp)
	
	# assign (add here the expr.to_string) to t_222
	#load the string str_18
	li $a0, 8
	li $v0, 9
	syscall
	la $v1, String
	sw $v1, 0($v0)
	la $v1, str_18
	sw $v1, 4($v0)
	sw $v0, -32($fp)
	
	# assign (add here the expr.to_string) to t_223
	#load the variable t_221
	lw $v0, -28($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	#load the variable t_222
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
	
	# assign (add here the expr.to_string) to t_224
	#load the variable t_223
	lw $v0, -36($fp)
	sw $v0, -40($fp)
	
	lw $t1, -40($fp)
	lw $t0, 4($t1)
	bne $t0, $zero, then_21
	# assign (add here the expr.to_string) to t_225
	# Creating Int instance for atomic 0
	li $a0, 8
	li $v0, 9
	syscall
	la $t0, Int
	li $t1, 0
	sw $t0, 0($v0)
	sw $t1, 4($v0)
	
	sw $v0, -44($fp)
	
	j ifend_21
	then_21:
	# assign (add here the expr.to_string) to t_225
	# Creating Int instance for atomic 1
	li $a0, 8
	li $v0, 9
	syscall
	la $t0, Int
	li $t1, 1
	sw $t0, 0($v0)
	sw $t1, 4($v0)
	
	sw $v0, -44($fp)
	
	ifend_21:
	# assign (add here the expr.to_string) to t_226
	# computes the sum of (node.left.to_string) and (node.right.to_string) and stores it at $v0
	#load the variable t_219
	lw $v0, -20($fp)
	lw $t0, 4($v0)
	# push $t0 to the stack
	sw $t0, 0($sp)
	addi $sp $sp -4
	
	#load the variable t_225
	lw $v0, -44($fp)
	# pop the top of the stack to $t0
	addi $sp $sp 4
	lw $t0, 0($sp)
	
	lw $t1, 4($v0)
	add $t0, $t0, $t1
	li $a0, 8
	li $v0, 9
	syscall
	la $t1, Int
	sw $t1, 0($v0)
	sw $t0, 4($v0)
	sw $v0, -48($fp)
	
	# assign (add here the expr.to_string) to t_227
	#load the variable position_213
	lw $v0, 12($fp)
	sw $v0, -52($fp)
	
	lw $v0, 16($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	lw $v0, -52($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	# assign (add here the expr.to_string) to t_228
	# calling the method east of type CellularAutomaton
	#load the variable self_CellularAutomaton
	lw $v0, 16($fp)
	lw $t0, 0($v0)
	lw $v1, 72($t0)
	jal $v1
	# pop the top of the stack to $v1
	addi $sp $sp 4
	lw $v1, 0($sp)
	
	# pop the top of the stack to $v1
	addi $sp $sp 4
	lw $v1, 0($sp)
	
	sw $v0, -56($fp)
	
	# assign (add here the expr.to_string) to t_229
	#load the string str_19
	li $a0, 8
	li $v0, 9
	syscall
	la $v1, String
	sw $v1, 0($v0)
	la $v1, str_19
	sw $v1, 4($v0)
	sw $v0, -60($fp)
	
	# assign (add here the expr.to_string) to t_230
	#load the variable t_228
	lw $v0, -56($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	#load the variable t_229
	lw $v0, -60($fp)
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
	
	sw $v0, -64($fp)
	
	# assign (add here the expr.to_string) to t_231
	#load the variable t_230
	lw $v0, -64($fp)
	sw $v0, -68($fp)
	
	lw $t1, -68($fp)
	lw $t0, 4($t1)
	bne $t0, $zero, then_22
	# assign (add here the expr.to_string) to t_232
	# Creating Int instance for atomic 0
	li $a0, 8
	li $v0, 9
	syscall
	la $t0, Int
	li $t1, 0
	sw $t0, 0($v0)
	sw $t1, 4($v0)
	
	sw $v0, -72($fp)
	
	j ifend_22
	then_22:
	# assign (add here the expr.to_string) to t_232
	# Creating Int instance for atomic 1
	li $a0, 8
	li $v0, 9
	syscall
	la $t0, Int
	li $t1, 1
	sw $t0, 0($v0)
	sw $t1, 4($v0)
	
	sw $v0, -72($fp)
	
	ifend_22:
	# assign (add here the expr.to_string) to t_233
	# computes the sum of (node.left.to_string) and (node.right.to_string) and stores it at $v0
	#load the variable t_226
	lw $v0, -48($fp)
	lw $t0, 4($v0)
	# push $t0 to the stack
	sw $t0, 0($sp)
	addi $sp $sp -4
	
	#load the variable t_232
	lw $v0, -72($fp)
	# pop the top of the stack to $t0
	addi $sp $sp 4
	lw $t0, 0($sp)
	
	lw $t1, 4($v0)
	add $t0, $t0, $t1
	li $a0, 8
	li $v0, 9
	syscall
	la $t1, Int
	sw $t1, 0($v0)
	sw $t0, 4($v0)
	sw $v0, -76($fp)
	
	# assign (add here the expr.to_string) to t_234
	#load the variable position_213
	lw $v0, 12($fp)
	sw $v0, -80($fp)
	
	lw $v0, 16($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	lw $v0, -80($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	# assign (add here the expr.to_string) to t_235
	# calling the method west of type CellularAutomaton
	#load the variable self_CellularAutomaton
	lw $v0, 16($fp)
	lw $t0, 0($v0)
	lw $v1, 76($t0)
	jal $v1
	# pop the top of the stack to $v1
	addi $sp $sp 4
	lw $v1, 0($sp)
	
	# pop the top of the stack to $v1
	addi $sp $sp 4
	lw $v1, 0($sp)
	
	sw $v0, -84($fp)
	
	# assign (add here the expr.to_string) to t_236
	#load the string str_20
	li $a0, 8
	li $v0, 9
	syscall
	la $v1, String
	sw $v1, 0($v0)
	la $v1, str_20
	sw $v1, 4($v0)
	sw $v0, -88($fp)
	
	# assign (add here the expr.to_string) to t_237
	#load the variable t_235
	lw $v0, -84($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	#load the variable t_236
	lw $v0, -88($fp)
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
	
	sw $v0, -92($fp)
	
	# assign (add here the expr.to_string) to t_238
	#load the variable t_237
	lw $v0, -92($fp)
	sw $v0, -96($fp)
	
	lw $t1, -96($fp)
	lw $t0, 4($t1)
	bne $t0, $zero, then_23
	# assign (add here the expr.to_string) to t_239
	# Creating Int instance for atomic 0
	li $a0, 8
	li $v0, 9
	syscall
	la $t0, Int
	li $t1, 0
	sw $t0, 0($v0)
	sw $t1, 4($v0)
	
	sw $v0, -100($fp)
	
	j ifend_23
	then_23:
	# assign (add here the expr.to_string) to t_239
	# Creating Int instance for atomic 1
	li $a0, 8
	li $v0, 9
	syscall
	la $t0, Int
	li $t1, 1
	sw $t0, 0($v0)
	sw $t1, 4($v0)
	
	sw $v0, -100($fp)
	
	ifend_23:
	# assign (add here the expr.to_string) to t_240
	# computes the sum of (node.left.to_string) and (node.right.to_string) and stores it at $v0
	#load the variable t_233
	lw $v0, -76($fp)
	lw $t0, 4($v0)
	# push $t0 to the stack
	sw $t0, 0($sp)
	addi $sp $sp -4
	
	#load the variable t_239
	lw $v0, -100($fp)
	# pop the top of the stack to $t0
	addi $sp $sp 4
	lw $t0, 0($sp)
	
	lw $t1, 4($v0)
	add $t0, $t0, $t1
	li $a0, 8
	li $v0, 9
	syscall
	la $t1, Int
	sw $t1, 0($v0)
	sw $t0, 4($v0)
	sw $v0, -104($fp)
	
	# assign (add here the expr.to_string) to t_241
	#load the variable position_213
	lw $v0, 12($fp)
	sw $v0, -108($fp)
	
	lw $v0, 16($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	lw $v0, -108($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	# assign (add here the expr.to_string) to t_242
	# calling the method northeast of type CellularAutomaton
	#load the variable self_CellularAutomaton
	lw $v0, 16($fp)
	lw $t0, 0($v0)
	lw $v1, 84($t0)
	jal $v1
	# pop the top of the stack to $v1
	addi $sp $sp 4
	lw $v1, 0($sp)
	
	# pop the top of the stack to $v1
	addi $sp $sp 4
	lw $v1, 0($sp)
	
	sw $v0, -112($fp)
	
	# assign (add here the expr.to_string) to t_243
	#load the string str_21
	li $a0, 8
	li $v0, 9
	syscall
	la $v1, String
	sw $v1, 0($v0)
	la $v1, str_21
	sw $v1, 4($v0)
	sw $v0, -116($fp)
	
	# assign (add here the expr.to_string) to t_244
	#load the variable t_242
	lw $v0, -112($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	#load the variable t_243
	lw $v0, -116($fp)
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
	
	sw $v0, -120($fp)
	
	# assign (add here the expr.to_string) to t_245
	#load the variable t_244
	lw $v0, -120($fp)
	sw $v0, -124($fp)
	
	lw $t1, -124($fp)
	lw $t0, 4($t1)
	bne $t0, $zero, then_24
	# assign (add here the expr.to_string) to t_246
	# Creating Int instance for atomic 0
	li $a0, 8
	li $v0, 9
	syscall
	la $t0, Int
	li $t1, 0
	sw $t0, 0($v0)
	sw $t1, 4($v0)
	
	sw $v0, -128($fp)
	
	j ifend_24
	then_24:
	# assign (add here the expr.to_string) to t_246
	# Creating Int instance for atomic 1
	li $a0, 8
	li $v0, 9
	syscall
	la $t0, Int
	li $t1, 1
	sw $t0, 0($v0)
	sw $t1, 4($v0)
	
	sw $v0, -128($fp)
	
	ifend_24:
	# assign (add here the expr.to_string) to t_247
	# computes the sum of (node.left.to_string) and (node.right.to_string) and stores it at $v0
	#load the variable t_240
	lw $v0, -104($fp)
	lw $t0, 4($v0)
	# push $t0 to the stack
	sw $t0, 0($sp)
	addi $sp $sp -4
	
	#load the variable t_246
	lw $v0, -128($fp)
	# pop the top of the stack to $t0
	addi $sp $sp 4
	lw $t0, 0($sp)
	
	lw $t1, 4($v0)
	add $t0, $t0, $t1
	li $a0, 8
	li $v0, 9
	syscall
	la $t1, Int
	sw $t1, 0($v0)
	sw $t0, 4($v0)
	sw $v0, -132($fp)
	
	# assign (add here the expr.to_string) to t_248
	#load the variable position_213
	lw $v0, 12($fp)
	sw $v0, -136($fp)
	
	lw $v0, 16($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	lw $v0, -136($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	# assign (add here the expr.to_string) to t_249
	# calling the method northwest of type CellularAutomaton
	#load the variable self_CellularAutomaton
	lw $v0, 16($fp)
	lw $t0, 0($v0)
	lw $v1, 80($t0)
	jal $v1
	# pop the top of the stack to $v1
	addi $sp $sp 4
	lw $v1, 0($sp)
	
	# pop the top of the stack to $v1
	addi $sp $sp 4
	lw $v1, 0($sp)
	
	sw $v0, -140($fp)
	
	# assign (add here the expr.to_string) to t_250
	#load the string str_22
	li $a0, 8
	li $v0, 9
	syscall
	la $v1, String
	sw $v1, 0($v0)
	la $v1, str_22
	sw $v1, 4($v0)
	sw $v0, -144($fp)
	
	# assign (add here the expr.to_string) to t_251
	#load the variable t_249
	lw $v0, -140($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	#load the variable t_250
	lw $v0, -144($fp)
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
	
	sw $v0, -148($fp)
	
	# assign (add here the expr.to_string) to t_252
	#load the variable t_251
	lw $v0, -148($fp)
	sw $v0, -152($fp)
	
	lw $t1, -152($fp)
	lw $t0, 4($t1)
	bne $t0, $zero, then_25
	# assign (add here the expr.to_string) to t_253
	# Creating Int instance for atomic 0
	li $a0, 8
	li $v0, 9
	syscall
	la $t0, Int
	li $t1, 0
	sw $t0, 0($v0)
	sw $t1, 4($v0)
	
	sw $v0, -156($fp)
	
	j ifend_25
	then_25:
	# assign (add here the expr.to_string) to t_253
	# Creating Int instance for atomic 1
	li $a0, 8
	li $v0, 9
	syscall
	la $t0, Int
	li $t1, 1
	sw $t0, 0($v0)
	sw $t1, 4($v0)
	
	sw $v0, -156($fp)
	
	ifend_25:
	# assign (add here the expr.to_string) to t_254
	# computes the sum of (node.left.to_string) and (node.right.to_string) and stores it at $v0
	#load the variable t_247
	lw $v0, -132($fp)
	lw $t0, 4($v0)
	# push $t0 to the stack
	sw $t0, 0($sp)
	addi $sp $sp -4
	
	#load the variable t_253
	lw $v0, -156($fp)
	# pop the top of the stack to $t0
	addi $sp $sp 4
	lw $t0, 0($sp)
	
	lw $t1, 4($v0)
	add $t0, $t0, $t1
	li $a0, 8
	li $v0, 9
	syscall
	la $t1, Int
	sw $t1, 0($v0)
	sw $t0, 4($v0)
	sw $v0, -160($fp)
	
	# assign (add here the expr.to_string) to t_255
	#load the variable position_213
	lw $v0, 12($fp)
	sw $v0, -164($fp)
	
	lw $v0, 16($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	lw $v0, -164($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	# assign (add here the expr.to_string) to t_256
	# calling the method southeast of type CellularAutomaton
	#load the variable self_CellularAutomaton
	lw $v0, 16($fp)
	lw $t0, 0($v0)
	lw $v1, 88($t0)
	jal $v1
	# pop the top of the stack to $v1
	addi $sp $sp 4
	lw $v1, 0($sp)
	
	# pop the top of the stack to $v1
	addi $sp $sp 4
	lw $v1, 0($sp)
	
	sw $v0, -168($fp)
	
	# assign (add here the expr.to_string) to t_257
	#load the string str_23
	li $a0, 8
	li $v0, 9
	syscall
	la $v1, String
	sw $v1, 0($v0)
	la $v1, str_23
	sw $v1, 4($v0)
	sw $v0, -172($fp)
	
	# assign (add here the expr.to_string) to t_258
	#load the variable t_256
	lw $v0, -168($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	#load the variable t_257
	lw $v0, -172($fp)
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
	
	sw $v0, -176($fp)
	
	# assign (add here the expr.to_string) to t_259
	#load the variable t_258
	lw $v0, -176($fp)
	sw $v0, -180($fp)
	
	lw $t1, -180($fp)
	lw $t0, 4($t1)
	bne $t0, $zero, then_26
	# assign (add here the expr.to_string) to t_260
	# Creating Int instance for atomic 0
	li $a0, 8
	li $v0, 9
	syscall
	la $t0, Int
	li $t1, 0
	sw $t0, 0($v0)
	sw $t1, 4($v0)
	
	sw $v0, -184($fp)
	
	j ifend_26
	then_26:
	# assign (add here the expr.to_string) to t_260
	# Creating Int instance for atomic 1
	li $a0, 8
	li $v0, 9
	syscall
	la $t0, Int
	li $t1, 1
	sw $t0, 0($v0)
	sw $t1, 4($v0)
	
	sw $v0, -184($fp)
	
	ifend_26:
	# assign (add here the expr.to_string) to t_261
	# computes the sum of (node.left.to_string) and (node.right.to_string) and stores it at $v0
	#load the variable t_254
	lw $v0, -160($fp)
	lw $t0, 4($v0)
	# push $t0 to the stack
	sw $t0, 0($sp)
	addi $sp $sp -4
	
	#load the variable t_260
	lw $v0, -184($fp)
	# pop the top of the stack to $t0
	addi $sp $sp 4
	lw $t0, 0($sp)
	
	lw $t1, 4($v0)
	add $t0, $t0, $t1
	li $a0, 8
	li $v0, 9
	syscall
	la $t1, Int
	sw $t1, 0($v0)
	sw $t0, 4($v0)
	sw $v0, -188($fp)
	
	# assign (add here the expr.to_string) to t_262
	#load the variable position_213
	lw $v0, 12($fp)
	sw $v0, -192($fp)
	
	lw $v0, 16($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	lw $v0, -192($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	# assign (add here the expr.to_string) to t_263
	# calling the method southwest of type CellularAutomaton
	#load the variable self_CellularAutomaton
	lw $v0, 16($fp)
	lw $t0, 0($v0)
	lw $v1, 92($t0)
	jal $v1
	# pop the top of the stack to $v1
	addi $sp $sp 4
	lw $v1, 0($sp)
	
	# pop the top of the stack to $v1
	addi $sp $sp 4
	lw $v1, 0($sp)
	
	sw $v0, -196($fp)
	
	# assign (add here the expr.to_string) to t_264
	#load the string str_24
	li $a0, 8
	li $v0, 9
	syscall
	la $v1, String
	sw $v1, 0($v0)
	la $v1, str_24
	sw $v1, 4($v0)
	sw $v0, -200($fp)
	
	# assign (add here the expr.to_string) to t_265
	#load the variable t_263
	lw $v0, -196($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	#load the variable t_264
	lw $v0, -200($fp)
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
	
	sw $v0, -204($fp)
	
	# assign (add here the expr.to_string) to t_266
	#load the variable t_265
	lw $v0, -204($fp)
	sw $v0, -208($fp)
	
	lw $t1, -208($fp)
	lw $t0, 4($t1)
	bne $t0, $zero, then_27
	# assign (add here the expr.to_string) to t_267
	# Creating Int instance for atomic 0
	li $a0, 8
	li $v0, 9
	syscall
	la $t0, Int
	li $t1, 0
	sw $t0, 0($v0)
	sw $t1, 4($v0)
	
	sw $v0, -212($fp)
	
	j ifend_27
	then_27:
	# assign (add here the expr.to_string) to t_267
	# Creating Int instance for atomic 1
	li $a0, 8
	li $v0, 9
	syscall
	la $t0, Int
	li $t1, 1
	sw $t0, 0($v0)
	sw $t1, 4($v0)
	
	sw $v0, -212($fp)
	
	ifend_27:
	# assign (add here the expr.to_string) to t_268
	# computes the sum of (node.left.to_string) and (node.right.to_string) and stores it at $v0
	#load the variable t_261
	lw $v0, -188($fp)
	lw $t0, 4($v0)
	# push $t0 to the stack
	sw $t0, 0($sp)
	addi $sp $sp -4
	
	#load the variable t_267
	lw $v0, -212($fp)
	# pop the top of the stack to $t0
	addi $sp $sp 4
	lw $t0, 0($sp)
	
	lw $t1, 4($v0)
	add $t0, $t0, $t1
	li $a0, 8
	li $v0, 9
	syscall
	la $t1, Int
	sw $t1, 0($v0)
	sw $t0, 4($v0)
	sw $v0, -216($fp)
	
	# assign (add here the expr.to_string) to t_269
	#load the variable t_268
	lw $v0, -216($fp)
	sw $v0, -220($fp)
	
	# return the value of the function in the register $v0
	#load the variable t_269
	lw $v0, -220($fp)
	move $v0, $v0
	
	# restore the stack pointer, frame pointer y return address
	addu $sp $sp 224
	# pop the top of the stack to $fp
	addi $sp $sp 4
	lw $fp, 0($sp)
	
	# pop the top of the stack to $ra
	addi $sp $sp 4
	lw $ra, 0($sp)
	
	jr $ra
	
	.text
cell_at_next_evolution_CellularAutomaton:
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
	
	# assign (add here the expr.to_string) to t_271
	#load the variable position_270
	lw $v0, 12($fp)
	sw $v0, -0($fp)
	
	lw $v0, 16($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	lw $v0, -0($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	# assign (add here the expr.to_string) to t_272
	# calling the method neighbors of type CellularAutomaton
	#load the variable self_CellularAutomaton
	lw $v0, 16($fp)
	lw $t0, 0($v0)
	lw $v1, 96($t0)
	jal $v1
	# pop the top of the stack to $v1
	addi $sp $sp 4
	lw $v1, 0($sp)
	
	# pop the top of the stack to $v1
	addi $sp $sp 4
	lw $v1, 0($sp)
	
	sw $v0, -4($fp)
	
	# assign (add here the expr.to_string) to t_273
	#load the variable t_272
	lw $v0, -4($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	# Creating Int instance for atomic 3
	li $a0, 8
	li $v0, 9
	syscall
	la $t0, Int
	li $t1, 3
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
	
	sw $v0, -8($fp)
	
	# assign (add here the expr.to_string) to t_274
	#load the variable t_273
	lw $v0, -8($fp)
	sw $v0, -12($fp)
	
	lw $t1, -12($fp)
	lw $t0, 4($t1)
	bne $t0, $zero, then_28
	# assign (add here the expr.to_string) to t_276
	#load the variable position_270
	lw $v0, 12($fp)
	sw $v0, -20($fp)
	
	lw $v0, 16($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	lw $v0, -20($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	# assign (add here the expr.to_string) to t_277
	# calling the method neighbors of type CellularAutomaton
	#load the variable self_CellularAutomaton
	lw $v0, 16($fp)
	lw $t0, 0($v0)
	lw $v1, 96($t0)
	jal $v1
	# pop the top of the stack to $v1
	addi $sp $sp 4
	lw $v1, 0($sp)
	
	# pop the top of the stack to $v1
	addi $sp $sp 4
	lw $v1, 0($sp)
	
	sw $v0, -24($fp)
	
	# assign (add here the expr.to_string) to t_278
	#load the variable t_277
	lw $v0, -24($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	# Creating Int instance for atomic 2
	li $a0, 8
	li $v0, 9
	syscall
	la $t0, Int
	li $t1, 2
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
	
	sw $v0, -28($fp)
	
	# assign (add here the expr.to_string) to t_279
	#load the variable t_278
	lw $v0, -28($fp)
	sw $v0, -32($fp)
	
	lw $t1, -32($fp)
	lw $t0, 4($t1)
	bne $t0, $zero, then_29
	# assign (add here the expr.to_string) to t_281
	#load the string str_25
	li $a0, 8
	li $v0, 9
	syscall
	la $v1, String
	sw $v1, 0($v0)
	la $v1, str_25
	sw $v1, 4($v0)
	sw $v0, -40($fp)
	
	# assign (add here the expr.to_string) to t_280
	#load the variable t_281
	lw $v0, -40($fp)
	sw $v0, -36($fp)
	
	j ifend_29
	then_29:
	# assign (add here the expr.to_string) to t_282
	#load the variable position_270
	lw $v0, 12($fp)
	sw $v0, -44($fp)
	
	lw $v0, 16($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	lw $v0, -44($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	# assign (add here the expr.to_string) to t_283
	# calling the method cell of type CellularAutomaton
	#load the variable self_CellularAutomaton
	lw $v0, 16($fp)
	lw $t0, 0($v0)
	lw $v1, 60($t0)
	jal $v1
	# pop the top of the stack to $v1
	addi $sp $sp 4
	lw $v1, 0($sp)
	
	# pop the top of the stack to $v1
	addi $sp $sp 4
	lw $v1, 0($sp)
	
	sw $v0, -48($fp)
	
	# assign (add here the expr.to_string) to t_284
	#load the string str_26
	li $a0, 8
	li $v0, 9
	syscall
	la $v1, String
	sw $v1, 0($v0)
	la $v1, str_26
	sw $v1, 4($v0)
	sw $v0, -52($fp)
	
	# assign (add here the expr.to_string) to t_285
	#load the variable t_283
	lw $v0, -48($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	#load the variable t_284
	lw $v0, -52($fp)
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
	
	# assign (add here the expr.to_string) to t_286
	#load the variable t_285
	lw $v0, -56($fp)
	sw $v0, -60($fp)
	
	lw $t1, -60($fp)
	lw $t0, 4($t1)
	bne $t0, $zero, then_30
	# assign (add here the expr.to_string) to t_288
	#load the string str_27
	li $a0, 8
	li $v0, 9
	syscall
	la $v1, String
	sw $v1, 0($v0)
	la $v1, str_27
	sw $v1, 4($v0)
	sw $v0, -68($fp)
	
	# assign (add here the expr.to_string) to t_287
	#load the variable t_288
	lw $v0, -68($fp)
	sw $v0, -64($fp)
	
	j ifend_30
	then_30:
	# assign (add here the expr.to_string) to t_289
	#load the string str_28
	li $a0, 8
	li $v0, 9
	syscall
	la $v1, String
	sw $v1, 0($v0)
	la $v1, str_28
	sw $v1, 4($v0)
	sw $v0, -72($fp)
	
	# assign (add here the expr.to_string) to t_287
	#load the variable t_289
	lw $v0, -72($fp)
	sw $v0, -64($fp)
	
	ifend_30:
	# assign (add here the expr.to_string) to t_280
	#load the variable t_287
	lw $v0, -64($fp)
	sw $v0, -36($fp)
	
	ifend_29:
	# assign (add here the expr.to_string) to t_275
	#load the variable t_280
	lw $v0, -36($fp)
	sw $v0, -16($fp)
	
	j ifend_28
	then_28:
	# assign (add here the expr.to_string) to t_290
	#load the string str_29
	li $a0, 8
	li $v0, 9
	syscall
	la $v1, String
	sw $v1, 0($v0)
	la $v1, str_29
	sw $v1, 4($v0)
	sw $v0, -76($fp)
	
	# assign (add here the expr.to_string) to t_275
	#load the variable t_290
	lw $v0, -76($fp)
	sw $v0, -16($fp)
	
	ifend_28:
	# assign (add here the expr.to_string) to t_291
	#load the variable t_275
	lw $v0, -16($fp)
	sw $v0, -80($fp)
	
	# return the value of the function in the register $v0
	#load the variable t_291
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
	.globl evolve
evolve_CellularAutomaton:
	# save the return address and frame pointer
	# push $ra to the stack
	sw $ra, 0($sp)
	addi $sp $sp -4
	
	# push $fp to the stack
	sw $fp, 0($sp)
	addi $sp $sp -4
	
	# update the frame pointer and allocate the frame in the stack
	move $fp $sp
	subu $sp $sp 72
	
	# assign (add here the expr.to_string) to position_292
	# Creating Int instance for atomic 0
	li $a0, 8
	li $v0, 9
	syscall
	la $t0, Int
	li $t1, 0
	sw $t0, 0($v0)
	sw $t1, 4($v0)
	
	sw $v0, -0($fp)
	
	lw $v0, 12($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	# assign (add here the expr.to_string) to t_294
	# calling the method num_cells of type CellularAutomaton
	#load the variable self_CellularAutomaton
	lw $v0, 12($fp)
	lw $t0, 0($v0)
	lw $v1, 56($t0)
	jal $v1
	# pop the top of the stack to $v1
	addi $sp $sp 4
	lw $v1, 0($sp)
	
	sw $v0, -8($fp)
	
	# assign (add here the expr.to_string) to num_293
	#load the variable t_294
	lw $v0, -8($fp)
	sw $v0, -4($fp)
	
	# assign (add here the expr.to_string) to temp_295
	#load the string str_empty
	li $a0, 8
	li $v0, 9
	syscall
	la $v1, String
	sw $v1, 0($v0)
	la $v1, str_empty
	sw $v1, 4($v0)
	sw $v0, -12($fp)
	
	while_1:
	# assign (add here the expr.to_string) to t_296
	#load the variable position_292
	lw $v0, -0($fp)
	move $t1, $v0
	lw $t1, 4($t1)
	#load the variable num_293
	lw $v0, -4($fp)
	move $t2, $v0
	lw $t2, 4($t2)
	slt $t3, $t1, $t2
	la $t4, Bool
	li $a0, 8
	li $v0, 9
	syscall
	sw $t4, 0($v0)
	sw $t3, 4($v0)
	sw $v0, -16($fp)
	
	# assign (add here the expr.to_string) to t_297
	#load the variable t_296
	lw $v0, -16($fp)
	sw $v0, -20($fp)
	
	lw $t1, -20($fp)
	lw $t0, 4($t1)
	bne $t0, $zero, body_1
	j pool_1
	body_1:
	# assign (add here the expr.to_string) to t_299
	#load the variable temp_295
	lw $v0, -12($fp)
	sw $v0, -28($fp)
	
	# assign (add here the expr.to_string) to t_300
	#load the variable position_292
	lw $v0, -0($fp)
	sw $v0, -32($fp)
	
	lw $v0, 12($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	lw $v0, -32($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	# assign (add here the expr.to_string) to t_301
	# calling the method cell_at_next_evolution of type CellularAutomaton
	#load the variable self_CellularAutomaton
	lw $v0, 12($fp)
	lw $t0, 0($v0)
	lw $v1, 100($t0)
	jal $v1
	# pop the top of the stack to $v1
	addi $sp $sp 4
	lw $v1, 0($sp)
	
	# pop the top of the stack to $v1
	addi $sp $sp 4
	lw $v1, 0($sp)
	
	sw $v0, -36($fp)
	
	# assign (add here the expr.to_string) to t_302
	#load the variable t_301
	lw $v0, -36($fp)
	sw $v0, -40($fp)
	
	lw $v0, -28($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	lw $v0, -40($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	# assign (add here the expr.to_string) to t_303
	# calling the method concat of type String
	#load the variable t_299
	lw $v0, -28($fp)
	lw $t0, 0($v0)
	lw $v1, 28($t0)
	jal $v1
	# pop the top of the stack to $v1
	addi $sp $sp 4
	lw $v1, 0($sp)
	
	# pop the top of the stack to $v1
	addi $sp $sp 4
	lw $v1, 0($sp)
	
	sw $v0, -44($fp)
	
	# assign (add here the expr.to_string) to temp_295
	#load the variable t_303
	lw $v0, -44($fp)
	sw $v0, -12($fp)
	
	# assign (add here the expr.to_string) to t_304
	#load the variable position_292
	lw $v0, -0($fp)
	sw $v0, -48($fp)
	
	lw $v0, 12($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	lw $v0, -48($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	# assign (add here the expr.to_string) to t_305
	# calling the method out_int of type CellularAutomaton
	#load the variable self_CellularAutomaton
	lw $v0, 12($fp)
	lw $t0, 0($v0)
	lw $v1, 28($t0)
	jal $v1
	# pop the top of the stack to $v1
	addi $sp $sp 4
	lw $v1, 0($sp)
	
	# pop the top of the stack to $v1
	addi $sp $sp 4
	lw $v1, 0($sp)
	
	sw $v0, -52($fp)
	
	# assign (add here the expr.to_string) to t_306
	#load the variable num_293
	lw $v0, -4($fp)
	sw $v0, -56($fp)
	
	lw $v0, 12($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	lw $v0, -56($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	# assign (add here the expr.to_string) to t_307
	# calling the method out_int of type CellularAutomaton
	#load the variable self_CellularAutomaton
	lw $v0, 12($fp)
	lw $t0, 0($v0)
	lw $v1, 28($t0)
	jal $v1
	# pop the top of the stack to $v1
	addi $sp $sp 4
	lw $v1, 0($sp)
	
	# pop the top of the stack to $v1
	addi $sp $sp 4
	lw $v1, 0($sp)
	
	sw $v0, -60($fp)
	
	# assign (add here the expr.to_string) to t_308
	# computes the sum of (node.left.to_string) and (node.right.to_string) and stores it at $v0
	#load the variable position_292
	lw $v0, -0($fp)
	lw $t0, 4($v0)
	# push $t0 to the stack
	sw $t0, 0($sp)
	addi $sp $sp -4
	
	# Creating Int instance for atomic 1
	li $a0, 8
	li $v0, 9
	syscall
	la $t0, Int
	li $t1, 1
	sw $t0, 0($v0)
	sw $t1, 4($v0)
	
	# pop the top of the stack to $t0
	addi $sp $sp 4
	lw $t0, 0($sp)
	
	lw $t1, 4($v0)
	add $t0, $t0, $t1
	li $a0, 8
	li $v0, 9
	syscall
	la $t1, Int
	sw $t1, 0($v0)
	sw $t0, 4($v0)
	sw $v0, -64($fp)
	
	# assign (add here the expr.to_string) to position_292
	#load the variable t_308
	lw $v0, -64($fp)
	sw $v0, -0($fp)
	
	# assign (add here the expr.to_string) to t_298
	#load the variable position_292
	lw $v0, -0($fp)
	sw $v0, -24($fp)
	
	j while_1
	pool_1:
	# Setting value of the attribute population_map in the instance self_CellularAutomaton to temp_295
	#load the variable temp_295
	lw $v0, -12($fp)
	move $s2, $v0
	lw $v1, 12($fp)
	sw $s2, 16($v1)
	
	# assign (add here the expr.to_string) to t_309
	#load the variable self_CellularAutomaton
	lw $v0, 12($fp)
	sw $v0, -68($fp)
	
	# return the value of the function in the register $v0
	#load the variable t_309
	lw $v0, -68($fp)
	move $v0, $v0
	
	# restore the stack pointer, frame pointer y return address
	addu $sp $sp 72
	# pop the top of the stack to $fp
	addi $sp $sp 4
	lw $fp, 0($sp)
	
	# pop the top of the stack to $ra
	addi $sp $sp 4
	lw $ra, 0($sp)
	
	jr $ra
	
	.text
option_CellularAutomaton:
	# save the return address and frame pointer
	# push $ra to the stack
	sw $ra, 0($sp)
	addi $sp $sp -4
	
	# push $fp to the stack
	sw $fp, 0($sp)
	addi $sp $sp -4
	
	# update the frame pointer and allocate the frame in the stack
	move $fp $sp
	subu $sp $sp 640
	
	# assign (add here the expr.to_string) to num_310
	# Creating Int instance for atomic 0
	li $a0, 8
	li $v0, 9
	syscall
	la $t0, Int
	li $t1, 0
	sw $t0, 0($v0)
	sw $t1, 4($v0)
	
	sw $v0, -0($fp)
	
	# assign (add here the expr.to_string) to t_311
	#load the string str_30
	li $a0, 8
	li $v0, 9
	syscall
	la $v1, String
	sw $v1, 0($v0)
	la $v1, str_30
	sw $v1, 4($v0)
	sw $v0, -4($fp)
	
	# assign (add here the expr.to_string) to t_312
	#load the variable t_311
	lw $v0, -4($fp)
	sw $v0, -8($fp)
	
	lw $v0, 12($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	lw $v0, -8($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	# assign (add here the expr.to_string) to t_313
	# calling the method out_string of type CellularAutomaton
	#load the variable self_CellularAutomaton
	lw $v0, 12($fp)
	lw $t0, 0($v0)
	lw $v1, 24($t0)
	jal $v1
	# pop the top of the stack to $v1
	addi $sp $sp 4
	lw $v1, 0($sp)
	
	# pop the top of the stack to $v1
	addi $sp $sp 4
	lw $v1, 0($sp)
	
	sw $v0, -12($fp)
	
	# assign (add here the expr.to_string) to t_314
	#load the string str_31
	li $a0, 8
	li $v0, 9
	syscall
	la $v1, String
	sw $v1, 0($v0)
	la $v1, str_31
	sw $v1, 4($v0)
	sw $v0, -16($fp)
	
	# assign (add here the expr.to_string) to t_315
	#load the variable t_314
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
	
	# assign (add here the expr.to_string) to t_316
	# calling the method out_string of type CellularAutomaton
	#load the variable self_CellularAutomaton
	lw $v0, 12($fp)
	lw $t0, 0($v0)
	lw $v1, 24($t0)
	jal $v1
	# pop the top of the stack to $v1
	addi $sp $sp 4
	lw $v1, 0($sp)
	
	# pop the top of the stack to $v1
	addi $sp $sp 4
	lw $v1, 0($sp)
	
	sw $v0, -24($fp)
	
	# assign (add here the expr.to_string) to t_317
	#load the string str_32
	li $a0, 8
	li $v0, 9
	syscall
	la $v1, String
	sw $v1, 0($v0)
	la $v1, str_32
	sw $v1, 4($v0)
	sw $v0, -28($fp)
	
	# assign (add here the expr.to_string) to t_318
	#load the variable t_317
	lw $v0, -28($fp)
	sw $v0, -32($fp)
	
	lw $v0, 12($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	lw $v0, -32($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	# assign (add here the expr.to_string) to t_319
	# calling the method out_string of type CellularAutomaton
	#load the variable self_CellularAutomaton
	lw $v0, 12($fp)
	lw $t0, 0($v0)
	lw $v1, 24($t0)
	jal $v1
	# pop the top of the stack to $v1
	addi $sp $sp 4
	lw $v1, 0($sp)
	
	# pop the top of the stack to $v1
	addi $sp $sp 4
	lw $v1, 0($sp)
	
	sw $v0, -36($fp)
	
	# assign (add here the expr.to_string) to t_320
	#load the string str_33
	li $a0, 8
	li $v0, 9
	syscall
	la $v1, String
	sw $v1, 0($v0)
	la $v1, str_33
	sw $v1, 4($v0)
	sw $v0, -40($fp)
	
	# assign (add here the expr.to_string) to t_321
	#load the variable t_320
	lw $v0, -40($fp)
	sw $v0, -44($fp)
	
	lw $v0, 12($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	lw $v0, -44($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	# assign (add here the expr.to_string) to t_322
	# calling the method out_string of type CellularAutomaton
	#load the variable self_CellularAutomaton
	lw $v0, 12($fp)
	lw $t0, 0($v0)
	lw $v1, 24($t0)
	jal $v1
	# pop the top of the stack to $v1
	addi $sp $sp 4
	lw $v1, 0($sp)
	
	# pop the top of the stack to $v1
	addi $sp $sp 4
	lw $v1, 0($sp)
	
	sw $v0, -48($fp)
	
	# assign (add here the expr.to_string) to t_323
	#load the string str_34
	li $a0, 8
	li $v0, 9
	syscall
	la $v1, String
	sw $v1, 0($v0)
	la $v1, str_34
	sw $v1, 4($v0)
	sw $v0, -52($fp)
	
	# assign (add here the expr.to_string) to t_324
	#load the variable t_323
	lw $v0, -52($fp)
	sw $v0, -56($fp)
	
	lw $v0, 12($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	lw $v0, -56($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	# assign (add here the expr.to_string) to t_325
	# calling the method out_string of type CellularAutomaton
	#load the variable self_CellularAutomaton
	lw $v0, 12($fp)
	lw $t0, 0($v0)
	lw $v1, 24($t0)
	jal $v1
	# pop the top of the stack to $v1
	addi $sp $sp 4
	lw $v1, 0($sp)
	
	# pop the top of the stack to $v1
	addi $sp $sp 4
	lw $v1, 0($sp)
	
	sw $v0, -60($fp)
	
	# assign (add here the expr.to_string) to t_326
	#load the string str_35
	li $a0, 8
	li $v0, 9
	syscall
	la $v1, String
	sw $v1, 0($v0)
	la $v1, str_35
	sw $v1, 4($v0)
	sw $v0, -64($fp)
	
	# assign (add here the expr.to_string) to t_327
	#load the variable t_326
	lw $v0, -64($fp)
	sw $v0, -68($fp)
	
	lw $v0, 12($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	lw $v0, -68($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	# assign (add here the expr.to_string) to t_328
	# calling the method out_string of type CellularAutomaton
	#load the variable self_CellularAutomaton
	lw $v0, 12($fp)
	lw $t0, 0($v0)
	lw $v1, 24($t0)
	jal $v1
	# pop the top of the stack to $v1
	addi $sp $sp 4
	lw $v1, 0($sp)
	
	# pop the top of the stack to $v1
	addi $sp $sp 4
	lw $v1, 0($sp)
	
	sw $v0, -72($fp)
	
	# assign (add here the expr.to_string) to t_329
	#load the string str_36
	li $a0, 8
	li $v0, 9
	syscall
	la $v1, String
	sw $v1, 0($v0)
	la $v1, str_36
	sw $v1, 4($v0)
	sw $v0, -76($fp)
	
	# assign (add here the expr.to_string) to t_330
	#load the variable t_329
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
	
	# assign (add here the expr.to_string) to t_331
	# calling the method out_string of type CellularAutomaton
	#load the variable self_CellularAutomaton
	lw $v0, 12($fp)
	lw $t0, 0($v0)
	lw $v1, 24($t0)
	jal $v1
	# pop the top of the stack to $v1
	addi $sp $sp 4
	lw $v1, 0($sp)
	
	# pop the top of the stack to $v1
	addi $sp $sp 4
	lw $v1, 0($sp)
	
	sw $v0, -84($fp)
	
	# assign (add here the expr.to_string) to t_332
	#load the string str_37
	li $a0, 8
	li $v0, 9
	syscall
	la $v1, String
	sw $v1, 0($v0)
	la $v1, str_37
	sw $v1, 4($v0)
	sw $v0, -88($fp)
	
	# assign (add here the expr.to_string) to t_333
	#load the variable t_332
	lw $v0, -88($fp)
	sw $v0, -92($fp)
	
	lw $v0, 12($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	lw $v0, -92($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	# assign (add here the expr.to_string) to t_334
	# calling the method out_string of type CellularAutomaton
	#load the variable self_CellularAutomaton
	lw $v0, 12($fp)
	lw $t0, 0($v0)
	lw $v1, 24($t0)
	jal $v1
	# pop the top of the stack to $v1
	addi $sp $sp 4
	lw $v1, 0($sp)
	
	# pop the top of the stack to $v1
	addi $sp $sp 4
	lw $v1, 0($sp)
	
	sw $v0, -96($fp)
	
	# assign (add here the expr.to_string) to t_335
	#load the string str_38
	li $a0, 8
	li $v0, 9
	syscall
	la $v1, String
	sw $v1, 0($v0)
	la $v1, str_38
	sw $v1, 4($v0)
	sw $v0, -100($fp)
	
	# assign (add here the expr.to_string) to t_336
	#load the variable t_335
	lw $v0, -100($fp)
	sw $v0, -104($fp)
	
	lw $v0, 12($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	lw $v0, -104($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	# assign (add here the expr.to_string) to t_337
	# calling the method out_string of type CellularAutomaton
	#load the variable self_CellularAutomaton
	lw $v0, 12($fp)
	lw $t0, 0($v0)
	lw $v1, 24($t0)
	jal $v1
	# pop the top of the stack to $v1
	addi $sp $sp 4
	lw $v1, 0($sp)
	
	# pop the top of the stack to $v1
	addi $sp $sp 4
	lw $v1, 0($sp)
	
	sw $v0, -108($fp)
	
	# assign (add here the expr.to_string) to t_338
	#load the string str_39
	li $a0, 8
	li $v0, 9
	syscall
	la $v1, String
	sw $v1, 0($v0)
	la $v1, str_39
	sw $v1, 4($v0)
	sw $v0, -112($fp)
	
	# assign (add here the expr.to_string) to t_339
	#load the variable t_338
	lw $v0, -112($fp)
	sw $v0, -116($fp)
	
	lw $v0, 12($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	lw $v0, -116($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	# assign (add here the expr.to_string) to t_340
	# calling the method out_string of type CellularAutomaton
	#load the variable self_CellularAutomaton
	lw $v0, 12($fp)
	lw $t0, 0($v0)
	lw $v1, 24($t0)
	jal $v1
	# pop the top of the stack to $v1
	addi $sp $sp 4
	lw $v1, 0($sp)
	
	# pop the top of the stack to $v1
	addi $sp $sp 4
	lw $v1, 0($sp)
	
	sw $v0, -120($fp)
	
	# assign (add here the expr.to_string) to t_341
	#load the string str_40
	li $a0, 8
	li $v0, 9
	syscall
	la $v1, String
	sw $v1, 0($v0)
	la $v1, str_40
	sw $v1, 4($v0)
	sw $v0, -124($fp)
	
	# assign (add here the expr.to_string) to t_342
	#load the variable t_341
	lw $v0, -124($fp)
	sw $v0, -128($fp)
	
	lw $v0, 12($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	lw $v0, -128($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	# assign (add here the expr.to_string) to t_343
	# calling the method out_string of type CellularAutomaton
	#load the variable self_CellularAutomaton
	lw $v0, 12($fp)
	lw $t0, 0($v0)
	lw $v1, 24($t0)
	jal $v1
	# pop the top of the stack to $v1
	addi $sp $sp 4
	lw $v1, 0($sp)
	
	# pop the top of the stack to $v1
	addi $sp $sp 4
	lw $v1, 0($sp)
	
	sw $v0, -132($fp)
	
	# assign (add here the expr.to_string) to t_344
	#load the string str_41
	li $a0, 8
	li $v0, 9
	syscall
	la $v1, String
	sw $v1, 0($v0)
	la $v1, str_41
	sw $v1, 4($v0)
	sw $v0, -136($fp)
	
	# assign (add here the expr.to_string) to t_345
	#load the variable t_344
	lw $v0, -136($fp)
	sw $v0, -140($fp)
	
	lw $v0, 12($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	lw $v0, -140($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	# assign (add here the expr.to_string) to t_346
	# calling the method out_string of type CellularAutomaton
	#load the variable self_CellularAutomaton
	lw $v0, 12($fp)
	lw $t0, 0($v0)
	lw $v1, 24($t0)
	jal $v1
	# pop the top of the stack to $v1
	addi $sp $sp 4
	lw $v1, 0($sp)
	
	# pop the top of the stack to $v1
	addi $sp $sp 4
	lw $v1, 0($sp)
	
	sw $v0, -144($fp)
	
	# assign (add here the expr.to_string) to t_347
	#load the string str_42
	li $a0, 8
	li $v0, 9
	syscall
	la $v1, String
	sw $v1, 0($v0)
	la $v1, str_42
	sw $v1, 4($v0)
	sw $v0, -148($fp)
	
	# assign (add here the expr.to_string) to t_348
	#load the variable t_347
	lw $v0, -148($fp)
	sw $v0, -152($fp)
	
	lw $v0, 12($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	lw $v0, -152($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	# assign (add here the expr.to_string) to t_349
	# calling the method out_string of type CellularAutomaton
	#load the variable self_CellularAutomaton
	lw $v0, 12($fp)
	lw $t0, 0($v0)
	lw $v1, 24($t0)
	jal $v1
	# pop the top of the stack to $v1
	addi $sp $sp 4
	lw $v1, 0($sp)
	
	# pop the top of the stack to $v1
	addi $sp $sp 4
	lw $v1, 0($sp)
	
	sw $v0, -156($fp)
	
	# assign (add here the expr.to_string) to t_350
	#load the string str_43
	li $a0, 8
	li $v0, 9
	syscall
	la $v1, String
	sw $v1, 0($v0)
	la $v1, str_43
	sw $v1, 4($v0)
	sw $v0, -160($fp)
	
	# assign (add here the expr.to_string) to t_351
	#load the variable t_350
	lw $v0, -160($fp)
	sw $v0, -164($fp)
	
	lw $v0, 12($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	lw $v0, -164($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	# assign (add here the expr.to_string) to t_352
	# calling the method out_string of type CellularAutomaton
	#load the variable self_CellularAutomaton
	lw $v0, 12($fp)
	lw $t0, 0($v0)
	lw $v1, 24($t0)
	jal $v1
	# pop the top of the stack to $v1
	addi $sp $sp 4
	lw $v1, 0($sp)
	
	# pop the top of the stack to $v1
	addi $sp $sp 4
	lw $v1, 0($sp)
	
	sw $v0, -168($fp)
	
	# assign (add here the expr.to_string) to t_353
	#load the string str_44
	li $a0, 8
	li $v0, 9
	syscall
	la $v1, String
	sw $v1, 0($v0)
	la $v1, str_44
	sw $v1, 4($v0)
	sw $v0, -172($fp)
	
	# assign (add here the expr.to_string) to t_354
	#load the variable t_353
	lw $v0, -172($fp)
	sw $v0, -176($fp)
	
	lw $v0, 12($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	lw $v0, -176($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	# assign (add here the expr.to_string) to t_355
	# calling the method out_string of type CellularAutomaton
	#load the variable self_CellularAutomaton
	lw $v0, 12($fp)
	lw $t0, 0($v0)
	lw $v1, 24($t0)
	jal $v1
	# pop the top of the stack to $v1
	addi $sp $sp 4
	lw $v1, 0($sp)
	
	# pop the top of the stack to $v1
	addi $sp $sp 4
	lw $v1, 0($sp)
	
	sw $v0, -180($fp)
	
	# assign (add here the expr.to_string) to t_356
	#load the string str_45
	li $a0, 8
	li $v0, 9
	syscall
	la $v1, String
	sw $v1, 0($v0)
	la $v1, str_45
	sw $v1, 4($v0)
	sw $v0, -184($fp)
	
	# assign (add here the expr.to_string) to t_357
	#load the variable t_356
	lw $v0, -184($fp)
	sw $v0, -188($fp)
	
	lw $v0, 12($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	lw $v0, -188($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	# assign (add here the expr.to_string) to t_358
	# calling the method out_string of type CellularAutomaton
	#load the variable self_CellularAutomaton
	lw $v0, 12($fp)
	lw $t0, 0($v0)
	lw $v1, 24($t0)
	jal $v1
	# pop the top of the stack to $v1
	addi $sp $sp 4
	lw $v1, 0($sp)
	
	# pop the top of the stack to $v1
	addi $sp $sp 4
	lw $v1, 0($sp)
	
	sw $v0, -192($fp)
	
	# assign (add here the expr.to_string) to t_359
	#load the string str_46
	li $a0, 8
	li $v0, 9
	syscall
	la $v1, String
	sw $v1, 0($v0)
	la $v1, str_46
	sw $v1, 4($v0)
	sw $v0, -196($fp)
	
	# assign (add here the expr.to_string) to t_360
	#load the variable t_359
	lw $v0, -196($fp)
	sw $v0, -200($fp)
	
	lw $v0, 12($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	lw $v0, -200($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	# assign (add here the expr.to_string) to t_361
	# calling the method out_string of type CellularAutomaton
	#load the variable self_CellularAutomaton
	lw $v0, 12($fp)
	lw $t0, 0($v0)
	lw $v1, 24($t0)
	jal $v1
	# pop the top of the stack to $v1
	addi $sp $sp 4
	lw $v1, 0($sp)
	
	# pop the top of the stack to $v1
	addi $sp $sp 4
	lw $v1, 0($sp)
	
	sw $v0, -204($fp)
	
	# assign (add here the expr.to_string) to t_362
	#load the string str_47
	li $a0, 8
	li $v0, 9
	syscall
	la $v1, String
	sw $v1, 0($v0)
	la $v1, str_47
	sw $v1, 4($v0)
	sw $v0, -208($fp)
	
	# assign (add here the expr.to_string) to t_363
	#load the variable t_362
	lw $v0, -208($fp)
	sw $v0, -212($fp)
	
	lw $v0, 12($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	lw $v0, -212($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	# assign (add here the expr.to_string) to t_364
	# calling the method out_string of type CellularAutomaton
	#load the variable self_CellularAutomaton
	lw $v0, 12($fp)
	lw $t0, 0($v0)
	lw $v1, 24($t0)
	jal $v1
	# pop the top of the stack to $v1
	addi $sp $sp 4
	lw $v1, 0($sp)
	
	# pop the top of the stack to $v1
	addi $sp $sp 4
	lw $v1, 0($sp)
	
	sw $v0, -216($fp)
	
	# assign (add here the expr.to_string) to t_365
	#load the string str_48
	li $a0, 8
	li $v0, 9
	syscall
	la $v1, String
	sw $v1, 0($v0)
	la $v1, str_48
	sw $v1, 4($v0)
	sw $v0, -220($fp)
	
	# assign (add here the expr.to_string) to t_366
	#load the variable t_365
	lw $v0, -220($fp)
	sw $v0, -224($fp)
	
	lw $v0, 12($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	lw $v0, -224($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	# assign (add here the expr.to_string) to t_367
	# calling the method out_string of type CellularAutomaton
	#load the variable self_CellularAutomaton
	lw $v0, 12($fp)
	lw $t0, 0($v0)
	lw $v1, 24($t0)
	jal $v1
	# pop the top of the stack to $v1
	addi $sp $sp 4
	lw $v1, 0($sp)
	
	# pop the top of the stack to $v1
	addi $sp $sp 4
	lw $v1, 0($sp)
	
	sw $v0, -228($fp)
	
	# assign (add here the expr.to_string) to t_368
	#load the string str_49
	li $a0, 8
	li $v0, 9
	syscall
	la $v1, String
	sw $v1, 0($v0)
	la $v1, str_49
	sw $v1, 4($v0)
	sw $v0, -232($fp)
	
	# assign (add here the expr.to_string) to t_369
	#load the variable t_368
	lw $v0, -232($fp)
	sw $v0, -236($fp)
	
	lw $v0, 12($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	lw $v0, -236($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	# assign (add here the expr.to_string) to t_370
	# calling the method out_string of type CellularAutomaton
	#load the variable self_CellularAutomaton
	lw $v0, 12($fp)
	lw $t0, 0($v0)
	lw $v1, 24($t0)
	jal $v1
	# pop the top of the stack to $v1
	addi $sp $sp 4
	lw $v1, 0($sp)
	
	# pop the top of the stack to $v1
	addi $sp $sp 4
	lw $v1, 0($sp)
	
	sw $v0, -240($fp)
	
	# assign (add here the expr.to_string) to t_371
	#load the string str_50
	li $a0, 8
	li $v0, 9
	syscall
	la $v1, String
	sw $v1, 0($v0)
	la $v1, str_50
	sw $v1, 4($v0)
	sw $v0, -244($fp)
	
	# assign (add here the expr.to_string) to t_372
	#load the variable t_371
	lw $v0, -244($fp)
	sw $v0, -248($fp)
	
	lw $v0, 12($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	lw $v0, -248($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	# assign (add here the expr.to_string) to t_373
	# calling the method out_string of type CellularAutomaton
	#load the variable self_CellularAutomaton
	lw $v0, 12($fp)
	lw $t0, 0($v0)
	lw $v1, 24($t0)
	jal $v1
	# pop the top of the stack to $v1
	addi $sp $sp 4
	lw $v1, 0($sp)
	
	# pop the top of the stack to $v1
	addi $sp $sp 4
	lw $v1, 0($sp)
	
	sw $v0, -252($fp)
	
	# assign (add here the expr.to_string) to t_374
	#load the string str_51
	li $a0, 8
	li $v0, 9
	syscall
	la $v1, String
	sw $v1, 0($v0)
	la $v1, str_51
	sw $v1, 4($v0)
	sw $v0, -256($fp)
	
	# assign (add here the expr.to_string) to t_375
	#load the variable t_374
	lw $v0, -256($fp)
	sw $v0, -260($fp)
	
	lw $v0, 12($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	lw $v0, -260($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	# assign (add here the expr.to_string) to t_376
	# calling the method out_string of type CellularAutomaton
	#load the variable self_CellularAutomaton
	lw $v0, 12($fp)
	lw $t0, 0($v0)
	lw $v1, 24($t0)
	jal $v1
	# pop the top of the stack to $v1
	addi $sp $sp 4
	lw $v1, 0($sp)
	
	# pop the top of the stack to $v1
	addi $sp $sp 4
	lw $v1, 0($sp)
	
	sw $v0, -264($fp)
	
	# assign (add here the expr.to_string) to t_377
	#load the string str_52
	li $a0, 8
	li $v0, 9
	syscall
	la $v1, String
	sw $v1, 0($v0)
	la $v1, str_52
	sw $v1, 4($v0)
	sw $v0, -268($fp)
	
	# assign (add here the expr.to_string) to t_378
	#load the variable t_377
	lw $v0, -268($fp)
	sw $v0, -272($fp)
	
	lw $v0, 12($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	lw $v0, -272($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	# assign (add here the expr.to_string) to t_379
	# calling the method out_string of type CellularAutomaton
	#load the variable self_CellularAutomaton
	lw $v0, 12($fp)
	lw $t0, 0($v0)
	lw $v1, 24($t0)
	jal $v1
	# pop the top of the stack to $v1
	addi $sp $sp 4
	lw $v1, 0($sp)
	
	# pop the top of the stack to $v1
	addi $sp $sp 4
	lw $v1, 0($sp)
	
	sw $v0, -276($fp)
	
	lw $v0, 12($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	# assign (add here the expr.to_string) to t_380
	# calling the method in_int of type CellularAutomaton
	#load the variable self_CellularAutomaton
	lw $v0, 12($fp)
	lw $t0, 0($v0)
	lw $v1, 36($t0)
	jal $v1
	# pop the top of the stack to $v1
	addi $sp $sp 4
	lw $v1, 0($sp)
	
	sw $v0, -280($fp)
	
	# assign (add here the expr.to_string) to num_310
	#load the variable t_380
	lw $v0, -280($fp)
	sw $v0, -0($fp)
	
	# assign (add here the expr.to_string) to t_381
	#load the string str_53
	li $a0, 8
	li $v0, 9
	syscall
	la $v1, String
	sw $v1, 0($v0)
	la $v1, str_53
	sw $v1, 4($v0)
	sw $v0, -284($fp)
	
	# assign (add here the expr.to_string) to t_382
	#load the variable t_381
	lw $v0, -284($fp)
	sw $v0, -288($fp)
	
	lw $v0, 12($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	lw $v0, -288($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	# assign (add here the expr.to_string) to t_383
	# calling the method out_string of type CellularAutomaton
	#load the variable self_CellularAutomaton
	lw $v0, 12($fp)
	lw $t0, 0($v0)
	lw $v1, 24($t0)
	jal $v1
	# pop the top of the stack to $v1
	addi $sp $sp 4
	lw $v1, 0($sp)
	
	# pop the top of the stack to $v1
	addi $sp $sp 4
	lw $v1, 0($sp)
	
	sw $v0, -292($fp)
	
	# assign (add here the expr.to_string) to t_384
	#load the variable num_310
	lw $v0, -0($fp)
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
	
	sw $v0, -296($fp)
	
	# assign (add here the expr.to_string) to t_385
	#load the variable t_384
	lw $v0, -296($fp)
	sw $v0, -300($fp)
	
	lw $t1, -300($fp)
	lw $t0, 4($t1)
	bne $t0, $zero, then_31
	# assign (add here the expr.to_string) to t_387
	#load the variable num_310
	lw $v0, -0($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	# Creating Int instance for atomic 2
	li $a0, 8
	li $v0, 9
	syscall
	la $t0, Int
	li $t1, 2
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
	
	sw $v0, -308($fp)
	
	# assign (add here the expr.to_string) to t_388
	#load the variable t_387
	lw $v0, -308($fp)
	sw $v0, -312($fp)
	
	lw $t1, -312($fp)
	lw $t0, 4($t1)
	bne $t0, $zero, then_32
	# assign (add here the expr.to_string) to t_390
	#load the variable num_310
	lw $v0, -0($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	# Creating Int instance for atomic 3
	li $a0, 8
	li $v0, 9
	syscall
	la $t0, Int
	li $t1, 3
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
	
	sw $v0, -320($fp)
	
	# assign (add here the expr.to_string) to t_391
	#load the variable t_390
	lw $v0, -320($fp)
	sw $v0, -324($fp)
	
	lw $t1, -324($fp)
	lw $t0, 4($t1)
	bne $t0, $zero, then_33
	# assign (add here the expr.to_string) to t_393
	#load the variable num_310
	lw $v0, -0($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	# Creating Int instance for atomic 4
	li $a0, 8
	li $v0, 9
	syscall
	la $t0, Int
	li $t1, 4
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
	
	sw $v0, -332($fp)
	
	# assign (add here the expr.to_string) to t_394
	#load the variable t_393
	lw $v0, -332($fp)
	sw $v0, -336($fp)
	
	lw $t1, -336($fp)
	lw $t0, 4($t1)
	bne $t0, $zero, then_34
	# assign (add here the expr.to_string) to t_396
	#load the variable num_310
	lw $v0, -0($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	# Creating Int instance for atomic 5
	li $a0, 8
	li $v0, 9
	syscall
	la $t0, Int
	li $t1, 5
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
	
	sw $v0, -344($fp)
	
	# assign (add here the expr.to_string) to t_397
	#load the variable t_396
	lw $v0, -344($fp)
	sw $v0, -348($fp)
	
	lw $t1, -348($fp)
	lw $t0, 4($t1)
	bne $t0, $zero, then_35
	# assign (add here the expr.to_string) to t_399
	#load the variable num_310
	lw $v0, -0($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	# Creating Int instance for atomic 6
	li $a0, 8
	li $v0, 9
	syscall
	la $t0, Int
	li $t1, 6
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
	
	sw $v0, -356($fp)
	
	# assign (add here the expr.to_string) to t_400
	#load the variable t_399
	lw $v0, -356($fp)
	sw $v0, -360($fp)
	
	lw $t1, -360($fp)
	lw $t0, 4($t1)
	bne $t0, $zero, then_36
	# assign (add here the expr.to_string) to t_402
	#load the variable num_310
	lw $v0, -0($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	# Creating Int instance for atomic 7
	li $a0, 8
	li $v0, 9
	syscall
	la $t0, Int
	li $t1, 7
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
	
	sw $v0, -368($fp)
	
	# assign (add here the expr.to_string) to t_403
	#load the variable t_402
	lw $v0, -368($fp)
	sw $v0, -372($fp)
	
	lw $t1, -372($fp)
	lw $t0, 4($t1)
	bne $t0, $zero, then_37
	# assign (add here the expr.to_string) to t_405
	#load the variable num_310
	lw $v0, -0($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	# Creating Int instance for atomic 8
	li $a0, 8
	li $v0, 9
	syscall
	la $t0, Int
	li $t1, 8
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
	
	sw $v0, -380($fp)
	
	# assign (add here the expr.to_string) to t_406
	#load the variable t_405
	lw $v0, -380($fp)
	sw $v0, -384($fp)
	
	lw $t1, -384($fp)
	lw $t0, 4($t1)
	bne $t0, $zero, then_38
	# assign (add here the expr.to_string) to t_408
	#load the variable num_310
	lw $v0, -0($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	# Creating Int instance for atomic 9
	li $a0, 8
	li $v0, 9
	syscall
	la $t0, Int
	li $t1, 9
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
	
	sw $v0, -392($fp)
	
	# assign (add here the expr.to_string) to t_409
	#load the variable t_408
	lw $v0, -392($fp)
	sw $v0, -396($fp)
	
	lw $t1, -396($fp)
	lw $t0, 4($t1)
	bne $t0, $zero, then_39
	# assign (add here the expr.to_string) to t_411
	#load the variable num_310
	lw $v0, -0($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	# Creating Int instance for atomic 10
	li $a0, 8
	li $v0, 9
	syscall
	la $t0, Int
	li $t1, 10
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
	
	sw $v0, -404($fp)
	
	# assign (add here the expr.to_string) to t_412
	#load the variable t_411
	lw $v0, -404($fp)
	sw $v0, -408($fp)
	
	lw $t1, -408($fp)
	lw $t0, 4($t1)
	bne $t0, $zero, then_40
	# assign (add here the expr.to_string) to t_414
	#load the variable num_310
	lw $v0, -0($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	# Creating Int instance for atomic 11
	li $a0, 8
	li $v0, 9
	syscall
	la $t0, Int
	li $t1, 11
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
	
	sw $v0, -416($fp)
	
	# assign (add here the expr.to_string) to t_415
	#load the variable t_414
	lw $v0, -416($fp)
	sw $v0, -420($fp)
	
	lw $t1, -420($fp)
	lw $t0, 4($t1)
	bne $t0, $zero, then_41
	# assign (add here the expr.to_string) to t_417
	#load the variable num_310
	lw $v0, -0($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	# Creating Int instance for atomic 12
	li $a0, 8
	li $v0, 9
	syscall
	la $t0, Int
	li $t1, 12
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
	
	sw $v0, -428($fp)
	
	# assign (add here the expr.to_string) to t_418
	#load the variable t_417
	lw $v0, -428($fp)
	sw $v0, -432($fp)
	
	lw $t1, -432($fp)
	lw $t0, 4($t1)
	bne $t0, $zero, then_42
	# assign (add here the expr.to_string) to t_420
	#load the variable num_310
	lw $v0, -0($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	# Creating Int instance for atomic 13
	li $a0, 8
	li $v0, 9
	syscall
	la $t0, Int
	li $t1, 13
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
	
	sw $v0, -440($fp)
	
	# assign (add here the expr.to_string) to t_421
	#load the variable t_420
	lw $v0, -440($fp)
	sw $v0, -444($fp)
	
	lw $t1, -444($fp)
	lw $t0, 4($t1)
	bne $t0, $zero, then_43
	# assign (add here the expr.to_string) to t_423
	#load the variable num_310
	lw $v0, -0($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	# Creating Int instance for atomic 14
	li $a0, 8
	li $v0, 9
	syscall
	la $t0, Int
	li $t1, 14
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
	
	sw $v0, -452($fp)
	
	# assign (add here the expr.to_string) to t_424
	#load the variable t_423
	lw $v0, -452($fp)
	sw $v0, -456($fp)
	
	lw $t1, -456($fp)
	lw $t0, 4($t1)
	bne $t0, $zero, then_44
	# assign (add here the expr.to_string) to t_426
	#load the variable num_310
	lw $v0, -0($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	# Creating Int instance for atomic 15
	li $a0, 8
	li $v0, 9
	syscall
	la $t0, Int
	li $t1, 15
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
	
	sw $v0, -464($fp)
	
	# assign (add here the expr.to_string) to t_427
	#load the variable t_426
	lw $v0, -464($fp)
	sw $v0, -468($fp)
	
	lw $t1, -468($fp)
	lw $t0, 4($t1)
	bne $t0, $zero, then_45
	# assign (add here the expr.to_string) to t_429
	#load the variable num_310
	lw $v0, -0($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	# Creating Int instance for atomic 16
	li $a0, 8
	li $v0, 9
	syscall
	la $t0, Int
	li $t1, 16
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
	
	sw $v0, -476($fp)
	
	# assign (add here the expr.to_string) to t_430
	#load the variable t_429
	lw $v0, -476($fp)
	sw $v0, -480($fp)
	
	lw $t1, -480($fp)
	lw $t0, 4($t1)
	bne $t0, $zero, then_46
	# assign (add here the expr.to_string) to t_432
	#load the variable num_310
	lw $v0, -0($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	# Creating Int instance for atomic 17
	li $a0, 8
	li $v0, 9
	syscall
	la $t0, Int
	li $t1, 17
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
	
	sw $v0, -488($fp)
	
	# assign (add here the expr.to_string) to t_433
	#load the variable t_432
	lw $v0, -488($fp)
	sw $v0, -492($fp)
	
	lw $t1, -492($fp)
	lw $t0, 4($t1)
	bne $t0, $zero, then_47
	# assign (add here the expr.to_string) to t_435
	#load the variable num_310
	lw $v0, -0($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	# Creating Int instance for atomic 18
	li $a0, 8
	li $v0, 9
	syscall
	la $t0, Int
	li $t1, 18
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
	
	sw $v0, -500($fp)
	
	# assign (add here the expr.to_string) to t_436
	#load the variable t_435
	lw $v0, -500($fp)
	sw $v0, -504($fp)
	
	lw $t1, -504($fp)
	lw $t0, 4($t1)
	bne $t0, $zero, then_48
	# assign (add here the expr.to_string) to t_438
	#load the variable num_310
	lw $v0, -0($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	# Creating Int instance for atomic 19
	li $a0, 8
	li $v0, 9
	syscall
	la $t0, Int
	li $t1, 19
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
	
	sw $v0, -512($fp)
	
	# assign (add here the expr.to_string) to t_439
	#load the variable t_438
	lw $v0, -512($fp)
	sw $v0, -516($fp)
	
	lw $t1, -516($fp)
	lw $t0, 4($t1)
	bne $t0, $zero, then_49
	# assign (add here the expr.to_string) to t_441
	#load the variable num_310
	lw $v0, -0($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	# Creating Int instance for atomic 20
	li $a0, 8
	li $v0, 9
	syscall
	la $t0, Int
	li $t1, 20
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
	
	sw $v0, -524($fp)
	
	# assign (add here the expr.to_string) to t_442
	#load the variable t_441
	lw $v0, -524($fp)
	sw $v0, -528($fp)
	
	lw $t1, -528($fp)
	lw $t0, 4($t1)
	bne $t0, $zero, then_50
	# assign (add here the expr.to_string) to t_444
	#load the variable num_310
	lw $v0, -0($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	# Creating Int instance for atomic 21
	li $a0, 8
	li $v0, 9
	syscall
	la $t0, Int
	li $t1, 21
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
	
	sw $v0, -536($fp)
	
	# assign (add here the expr.to_string) to t_445
	#load the variable t_444
	lw $v0, -536($fp)
	sw $v0, -540($fp)
	
	lw $t1, -540($fp)
	lw $t0, 4($t1)
	bne $t0, $zero, then_51
	# assign (add here the expr.to_string) to t_447
	#load the string str_54
	li $a0, 8
	li $v0, 9
	syscall
	la $v1, String
	sw $v1, 0($v0)
	la $v1, str_54
	sw $v1, 4($v0)
	sw $v0, -548($fp)
	
	# assign (add here the expr.to_string) to t_446
	#load the variable t_447
	lw $v0, -548($fp)
	sw $v0, -544($fp)
	
	j ifend_51
	then_51:
	# assign (add here the expr.to_string) to t_448
	#load the string str_55
	li $a0, 8
	li $v0, 9
	syscall
	la $v1, String
	sw $v1, 0($v0)
	la $v1, str_55
	sw $v1, 4($v0)
	sw $v0, -552($fp)
	
	# assign (add here the expr.to_string) to t_446
	#load the variable t_448
	lw $v0, -552($fp)
	sw $v0, -544($fp)
	
	ifend_51:
	# assign (add here the expr.to_string) to t_443
	#load the variable t_446
	lw $v0, -544($fp)
	sw $v0, -532($fp)
	
	j ifend_50
	then_50:
	# assign (add here the expr.to_string) to t_449
	#load the string str_56
	li $a0, 8
	li $v0, 9
	syscall
	la $v1, String
	sw $v1, 0($v0)
	la $v1, str_56
	sw $v1, 4($v0)
	sw $v0, -556($fp)
	
	# assign (add here the expr.to_string) to t_443
	#load the variable t_449
	lw $v0, -556($fp)
	sw $v0, -532($fp)
	
	ifend_50:
	# assign (add here the expr.to_string) to t_440
	#load the variable t_443
	lw $v0, -532($fp)
	sw $v0, -520($fp)
	
	j ifend_49
	then_49:
	# assign (add here the expr.to_string) to t_450
	#load the string str_57
	li $a0, 8
	li $v0, 9
	syscall
	la $v1, String
	sw $v1, 0($v0)
	la $v1, str_57
	sw $v1, 4($v0)
	sw $v0, -560($fp)
	
	# assign (add here the expr.to_string) to t_440
	#load the variable t_450
	lw $v0, -560($fp)
	sw $v0, -520($fp)
	
	ifend_49:
	# assign (add here the expr.to_string) to t_437
	#load the variable t_440
	lw $v0, -520($fp)
	sw $v0, -508($fp)
	
	j ifend_48
	then_48:
	# assign (add here the expr.to_string) to t_451
	#load the string str_58
	li $a0, 8
	li $v0, 9
	syscall
	la $v1, String
	sw $v1, 0($v0)
	la $v1, str_58
	sw $v1, 4($v0)
	sw $v0, -564($fp)
	
	# assign (add here the expr.to_string) to t_437
	#load the variable t_451
	lw $v0, -564($fp)
	sw $v0, -508($fp)
	
	ifend_48:
	# assign (add here the expr.to_string) to t_434
	#load the variable t_437
	lw $v0, -508($fp)
	sw $v0, -496($fp)
	
	j ifend_47
	then_47:
	# assign (add here the expr.to_string) to t_452
	#load the string str_59
	li $a0, 8
	li $v0, 9
	syscall
	la $v1, String
	sw $v1, 0($v0)
	la $v1, str_59
	sw $v1, 4($v0)
	sw $v0, -568($fp)
	
	# assign (add here the expr.to_string) to t_434
	#load the variable t_452
	lw $v0, -568($fp)
	sw $v0, -496($fp)
	
	ifend_47:
	# assign (add here the expr.to_string) to t_431
	#load the variable t_434
	lw $v0, -496($fp)
	sw $v0, -484($fp)
	
	j ifend_46
	then_46:
	# assign (add here the expr.to_string) to t_453
	#load the string str_60
	li $a0, 8
	li $v0, 9
	syscall
	la $v1, String
	sw $v1, 0($v0)
	la $v1, str_60
	sw $v1, 4($v0)
	sw $v0, -572($fp)
	
	# assign (add here the expr.to_string) to t_431
	#load the variable t_453
	lw $v0, -572($fp)
	sw $v0, -484($fp)
	
	ifend_46:
	# assign (add here the expr.to_string) to t_428
	#load the variable t_431
	lw $v0, -484($fp)
	sw $v0, -472($fp)
	
	j ifend_45
	then_45:
	# assign (add here the expr.to_string) to t_454
	#load the string str_61
	li $a0, 8
	li $v0, 9
	syscall
	la $v1, String
	sw $v1, 0($v0)
	la $v1, str_61
	sw $v1, 4($v0)
	sw $v0, -576($fp)
	
	# assign (add here the expr.to_string) to t_428
	#load the variable t_454
	lw $v0, -576($fp)
	sw $v0, -472($fp)
	
	ifend_45:
	# assign (add here the expr.to_string) to t_425
	#load the variable t_428
	lw $v0, -472($fp)
	sw $v0, -460($fp)
	
	j ifend_44
	then_44:
	# assign (add here the expr.to_string) to t_455
	#load the string str_62
	li $a0, 8
	li $v0, 9
	syscall
	la $v1, String
	sw $v1, 0($v0)
	la $v1, str_62
	sw $v1, 4($v0)
	sw $v0, -580($fp)
	
	# assign (add here the expr.to_string) to t_425
	#load the variable t_455
	lw $v0, -580($fp)
	sw $v0, -460($fp)
	
	ifend_44:
	# assign (add here the expr.to_string) to t_422
	#load the variable t_425
	lw $v0, -460($fp)
	sw $v0, -448($fp)
	
	j ifend_43
	then_43:
	# assign (add here the expr.to_string) to t_456
	#load the string str_63
	li $a0, 8
	li $v0, 9
	syscall
	la $v1, String
	sw $v1, 0($v0)
	la $v1, str_63
	sw $v1, 4($v0)
	sw $v0, -584($fp)
	
	# assign (add here the expr.to_string) to t_422
	#load the variable t_456
	lw $v0, -584($fp)
	sw $v0, -448($fp)
	
	ifend_43:
	# assign (add here the expr.to_string) to t_419
	#load the variable t_422
	lw $v0, -448($fp)
	sw $v0, -436($fp)
	
	j ifend_42
	then_42:
	# assign (add here the expr.to_string) to t_457
	#load the string str_64
	li $a0, 8
	li $v0, 9
	syscall
	la $v1, String
	sw $v1, 0($v0)
	la $v1, str_64
	sw $v1, 4($v0)
	sw $v0, -588($fp)
	
	# assign (add here the expr.to_string) to t_419
	#load the variable t_457
	lw $v0, -588($fp)
	sw $v0, -436($fp)
	
	ifend_42:
	# assign (add here the expr.to_string) to t_416
	#load the variable t_419
	lw $v0, -436($fp)
	sw $v0, -424($fp)
	
	j ifend_41
	then_41:
	# assign (add here the expr.to_string) to t_458
	#load the string str_65
	li $a0, 8
	li $v0, 9
	syscall
	la $v1, String
	sw $v1, 0($v0)
	la $v1, str_65
	sw $v1, 4($v0)
	sw $v0, -592($fp)
	
	# assign (add here the expr.to_string) to t_416
	#load the variable t_458
	lw $v0, -592($fp)
	sw $v0, -424($fp)
	
	ifend_41:
	# assign (add here the expr.to_string) to t_413
	#load the variable t_416
	lw $v0, -424($fp)
	sw $v0, -412($fp)
	
	j ifend_40
	then_40:
	# assign (add here the expr.to_string) to t_459
	#load the string str_66
	li $a0, 8
	li $v0, 9
	syscall
	la $v1, String
	sw $v1, 0($v0)
	la $v1, str_66
	sw $v1, 4($v0)
	sw $v0, -596($fp)
	
	# assign (add here the expr.to_string) to t_413
	#load the variable t_459
	lw $v0, -596($fp)
	sw $v0, -412($fp)
	
	ifend_40:
	# assign (add here the expr.to_string) to t_410
	#load the variable t_413
	lw $v0, -412($fp)
	sw $v0, -400($fp)
	
	j ifend_39
	then_39:
	# assign (add here the expr.to_string) to t_460
	#load the string str_67
	li $a0, 8
	li $v0, 9
	syscall
	la $v1, String
	sw $v1, 0($v0)
	la $v1, str_67
	sw $v1, 4($v0)
	sw $v0, -600($fp)
	
	# assign (add here the expr.to_string) to t_410
	#load the variable t_460
	lw $v0, -600($fp)
	sw $v0, -400($fp)
	
	ifend_39:
	# assign (add here the expr.to_string) to t_407
	#load the variable t_410
	lw $v0, -400($fp)
	sw $v0, -388($fp)
	
	j ifend_38
	then_38:
	# assign (add here the expr.to_string) to t_461
	#load the string str_68
	li $a0, 8
	li $v0, 9
	syscall
	la $v1, String
	sw $v1, 0($v0)
	la $v1, str_68
	sw $v1, 4($v0)
	sw $v0, -604($fp)
	
	# assign (add here the expr.to_string) to t_407
	#load the variable t_461
	lw $v0, -604($fp)
	sw $v0, -388($fp)
	
	ifend_38:
	# assign (add here the expr.to_string) to t_404
	#load the variable t_407
	lw $v0, -388($fp)
	sw $v0, -376($fp)
	
	j ifend_37
	then_37:
	# assign (add here the expr.to_string) to t_462
	#load the string str_69
	li $a0, 8
	li $v0, 9
	syscall
	la $v1, String
	sw $v1, 0($v0)
	la $v1, str_69
	sw $v1, 4($v0)
	sw $v0, -608($fp)
	
	# assign (add here the expr.to_string) to t_404
	#load the variable t_462
	lw $v0, -608($fp)
	sw $v0, -376($fp)
	
	ifend_37:
	# assign (add here the expr.to_string) to t_401
	#load the variable t_404
	lw $v0, -376($fp)
	sw $v0, -364($fp)
	
	j ifend_36
	then_36:
	# assign (add here the expr.to_string) to t_463
	#load the string str_70
	li $a0, 8
	li $v0, 9
	syscall
	la $v1, String
	sw $v1, 0($v0)
	la $v1, str_70
	sw $v1, 4($v0)
	sw $v0, -612($fp)
	
	# assign (add here the expr.to_string) to t_401
	#load the variable t_463
	lw $v0, -612($fp)
	sw $v0, -364($fp)
	
	ifend_36:
	# assign (add here the expr.to_string) to t_398
	#load the variable t_401
	lw $v0, -364($fp)
	sw $v0, -352($fp)
	
	j ifend_35
	then_35:
	# assign (add here the expr.to_string) to t_464
	#load the string str_71
	li $a0, 8
	li $v0, 9
	syscall
	la $v1, String
	sw $v1, 0($v0)
	la $v1, str_71
	sw $v1, 4($v0)
	sw $v0, -616($fp)
	
	# assign (add here the expr.to_string) to t_398
	#load the variable t_464
	lw $v0, -616($fp)
	sw $v0, -352($fp)
	
	ifend_35:
	# assign (add here the expr.to_string) to t_395
	#load the variable t_398
	lw $v0, -352($fp)
	sw $v0, -340($fp)
	
	j ifend_34
	then_34:
	# assign (add here the expr.to_string) to t_465
	#load the string str_72
	li $a0, 8
	li $v0, 9
	syscall
	la $v1, String
	sw $v1, 0($v0)
	la $v1, str_72
	sw $v1, 4($v0)
	sw $v0, -620($fp)
	
	# assign (add here the expr.to_string) to t_395
	#load the variable t_465
	lw $v0, -620($fp)
	sw $v0, -340($fp)
	
	ifend_34:
	# assign (add here the expr.to_string) to t_392
	#load the variable t_395
	lw $v0, -340($fp)
	sw $v0, -328($fp)
	
	j ifend_33
	then_33:
	# assign (add here the expr.to_string) to t_466
	#load the string str_73
	li $a0, 8
	li $v0, 9
	syscall
	la $v1, String
	sw $v1, 0($v0)
	la $v1, str_73
	sw $v1, 4($v0)
	sw $v0, -624($fp)
	
	# assign (add here the expr.to_string) to t_392
	#load the variable t_466
	lw $v0, -624($fp)
	sw $v0, -328($fp)
	
	ifend_33:
	# assign (add here the expr.to_string) to t_389
	#load the variable t_392
	lw $v0, -328($fp)
	sw $v0, -316($fp)
	
	j ifend_32
	then_32:
	# assign (add here the expr.to_string) to t_467
	#load the string str_74
	li $a0, 8
	li $v0, 9
	syscall
	la $v1, String
	sw $v1, 0($v0)
	la $v1, str_74
	sw $v1, 4($v0)
	sw $v0, -628($fp)
	
	# assign (add here the expr.to_string) to t_389
	#load the variable t_467
	lw $v0, -628($fp)
	sw $v0, -316($fp)
	
	ifend_32:
	# assign (add here the expr.to_string) to t_386
	#load the variable t_389
	lw $v0, -316($fp)
	sw $v0, -304($fp)
	
	j ifend_31
	then_31:
	# assign (add here the expr.to_string) to t_468
	#load the string str_75
	li $a0, 8
	li $v0, 9
	syscall
	la $v1, String
	sw $v1, 0($v0)
	la $v1, str_75
	sw $v1, 4($v0)
	sw $v0, -632($fp)
	
	# assign (add here the expr.to_string) to t_386
	#load the variable t_468
	lw $v0, -632($fp)
	sw $v0, -304($fp)
	
	ifend_31:
	# assign (add here the expr.to_string) to t_469
	#load the variable t_386
	lw $v0, -304($fp)
	sw $v0, -636($fp)
	
	# return the value of the function in the register $v0
	#load the variable t_469
	lw $v0, -636($fp)
	move $v0, $v0
	
	# restore the stack pointer, frame pointer y return address
	addu $sp $sp 640
	# pop the top of the stack to $fp
	addi $sp $sp 4
	lw $fp, 0($sp)
	
	# pop the top of the stack to $ra
	addi $sp $sp 4
	lw $ra, 0($sp)
	
	jr $ra
	
	.text
prompt_CellularAutomaton:
	# save the return address and frame pointer
	# push $ra to the stack
	sw $ra, 0($sp)
	addi $sp $sp -4
	
	# push $fp to the stack
	sw $fp, 0($sp)
	addi $sp $sp -4
	
	# update the frame pointer and allocate the frame in the stack
	move $fp $sp
	subu $sp $sp 72
	
	# assign (add here the expr.to_string) to ans_470
	#load the string str_empty
	li $a0, 8
	li $v0, 9
	syscall
	la $v1, String
	sw $v1, 0($v0)
	la $v1, str_empty
	sw $v1, 4($v0)
	sw $v0, -0($fp)
	
	# assign (add here the expr.to_string) to t_471
	#load the string str_76
	li $a0, 8
	li $v0, 9
	syscall
	la $v1, String
	sw $v1, 0($v0)
	la $v1, str_76
	sw $v1, 4($v0)
	sw $v0, -4($fp)
	
	# assign (add here the expr.to_string) to t_472
	#load the variable t_471
	lw $v0, -4($fp)
	sw $v0, -8($fp)
	
	lw $v0, 12($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	lw $v0, -8($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	# assign (add here the expr.to_string) to t_473
	# calling the method out_string of type CellularAutomaton
	#load the variable self_CellularAutomaton
	lw $v0, 12($fp)
	lw $t0, 0($v0)
	lw $v1, 24($t0)
	jal $v1
	# pop the top of the stack to $v1
	addi $sp $sp 4
	lw $v1, 0($sp)
	
	# pop the top of the stack to $v1
	addi $sp $sp 4
	lw $v1, 0($sp)
	
	sw $v0, -12($fp)
	
	# assign (add here the expr.to_string) to t_474
	#load the string str_77
	li $a0, 8
	li $v0, 9
	syscall
	la $v1, String
	sw $v1, 0($v0)
	la $v1, str_77
	sw $v1, 4($v0)
	sw $v0, -16($fp)
	
	# assign (add here the expr.to_string) to t_475
	#load the variable t_474
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
	
	# assign (add here the expr.to_string) to t_476
	# calling the method out_string of type CellularAutomaton
	#load the variable self_CellularAutomaton
	lw $v0, 12($fp)
	lw $t0, 0($v0)
	lw $v1, 24($t0)
	jal $v1
	# pop the top of the stack to $v1
	addi $sp $sp 4
	lw $v1, 0($sp)
	
	# pop the top of the stack to $v1
	addi $sp $sp 4
	lw $v1, 0($sp)
	
	sw $v0, -24($fp)
	
	lw $v0, 12($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	# assign (add here the expr.to_string) to t_477
	# calling the method in_string of type CellularAutomaton
	#load the variable self_CellularAutomaton
	lw $v0, 12($fp)
	lw $t0, 0($v0)
	lw $v1, 32($t0)
	jal $v1
	# pop the top of the stack to $v1
	addi $sp $sp 4
	lw $v1, 0($sp)
	
	sw $v0, -28($fp)
	
	# assign (add here the expr.to_string) to ans_470
	#load the variable t_477
	lw $v0, -28($fp)
	sw $v0, -0($fp)
	
	# assign (add here the expr.to_string) to t_478
	#load the string str_78
	li $a0, 8
	li $v0, 9
	syscall
	la $v1, String
	sw $v1, 0($v0)
	la $v1, str_78
	sw $v1, 4($v0)
	sw $v0, -32($fp)
	
	# assign (add here the expr.to_string) to t_479
	#load the variable t_478
	lw $v0, -32($fp)
	sw $v0, -36($fp)
	
	lw $v0, 12($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	lw $v0, -36($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	# assign (add here the expr.to_string) to t_480
	# calling the method out_string of type CellularAutomaton
	#load the variable self_CellularAutomaton
	lw $v0, 12($fp)
	lw $t0, 0($v0)
	lw $v1, 24($t0)
	jal $v1
	# pop the top of the stack to $v1
	addi $sp $sp 4
	lw $v1, 0($sp)
	
	# pop the top of the stack to $v1
	addi $sp $sp 4
	lw $v1, 0($sp)
	
	sw $v0, -40($fp)
	
	# assign (add here the expr.to_string) to t_481
	#load the string str_79
	li $a0, 8
	li $v0, 9
	syscall
	la $v1, String
	sw $v1, 0($v0)
	la $v1, str_79
	sw $v1, 4($v0)
	sw $v0, -44($fp)
	
	# assign (add here the expr.to_string) to t_482
	#load the variable ans_470
	lw $v0, -0($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	#load the variable t_481
	lw $v0, -44($fp)
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
	
	sw $v0, -48($fp)
	
	# assign (add here the expr.to_string) to t_483
	#load the variable t_482
	lw $v0, -48($fp)
	sw $v0, -52($fp)
	
	lw $t1, -52($fp)
	lw $t0, 4($t1)
	bne $t0, $zero, then_52
	# assign (add here the expr.to_string) to t_485
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
	
	sw $v0, -60($fp)
	
	# assign (add here the expr.to_string) to t_484
	#load the variable t_485
	lw $v0, -60($fp)
	sw $v0, -56($fp)
	
	j ifend_52
	then_52:
	# assign (add here the expr.to_string) to t_486
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
	
	sw $v0, -64($fp)
	
	# assign (add here the expr.to_string) to t_484
	#load the variable t_486
	lw $v0, -64($fp)
	sw $v0, -56($fp)
	
	ifend_52:
	# assign (add here the expr.to_string) to t_487
	#load the variable t_484
	lw $v0, -56($fp)
	sw $v0, -68($fp)
	
	# return the value of the function in the register $v0
	#load the variable t_487
	lw $v0, -68($fp)
	move $v0, $v0
	
	# restore the stack pointer, frame pointer y return address
	addu $sp $sp 72
	# pop the top of the stack to $fp
	addi $sp $sp 4
	lw $fp, 0($sp)
	
	# pop the top of the stack to $ra
	addi $sp $sp 4
	lw $ra, 0($sp)
	
	jr $ra
	
	.text
prompt2_CellularAutomaton:
	# save the return address and frame pointer
	# push $ra to the stack
	sw $ra, 0($sp)
	addi $sp $sp -4
	
	# push $fp to the stack
	sw $fp, 0($sp)
	addi $sp $sp -4
	
	# update the frame pointer and allocate the frame in the stack
	move $fp $sp
	subu $sp $sp 72
	
	# assign (add here the expr.to_string) to ans_488
	#load the string str_empty
	li $a0, 8
	li $v0, 9
	syscall
	la $v1, String
	sw $v1, 0($v0)
	la $v1, str_empty
	sw $v1, 4($v0)
	sw $v0, -0($fp)
	
	# assign (add here the expr.to_string) to t_489
	#load the string str_80
	li $a0, 8
	li $v0, 9
	syscall
	la $v1, String
	sw $v1, 0($v0)
	la $v1, str_80
	sw $v1, 4($v0)
	sw $v0, -4($fp)
	
	# assign (add here the expr.to_string) to t_490
	#load the variable t_489
	lw $v0, -4($fp)
	sw $v0, -8($fp)
	
	lw $v0, 12($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	lw $v0, -8($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	# assign (add here the expr.to_string) to t_491
	# calling the method out_string of type CellularAutomaton
	#load the variable self_CellularAutomaton
	lw $v0, 12($fp)
	lw $t0, 0($v0)
	lw $v1, 24($t0)
	jal $v1
	# pop the top of the stack to $v1
	addi $sp $sp 4
	lw $v1, 0($sp)
	
	# pop the top of the stack to $v1
	addi $sp $sp 4
	lw $v1, 0($sp)
	
	sw $v0, -12($fp)
	
	# assign (add here the expr.to_string) to t_492
	#load the string str_81
	li $a0, 8
	li $v0, 9
	syscall
	la $v1, String
	sw $v1, 0($v0)
	la $v1, str_81
	sw $v1, 4($v0)
	sw $v0, -16($fp)
	
	# assign (add here the expr.to_string) to t_493
	#load the variable t_492
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
	
	# assign (add here the expr.to_string) to t_494
	# calling the method out_string of type CellularAutomaton
	#load the variable self_CellularAutomaton
	lw $v0, 12($fp)
	lw $t0, 0($v0)
	lw $v1, 24($t0)
	jal $v1
	# pop the top of the stack to $v1
	addi $sp $sp 4
	lw $v1, 0($sp)
	
	# pop the top of the stack to $v1
	addi $sp $sp 4
	lw $v1, 0($sp)
	
	sw $v0, -24($fp)
	
	# assign (add here the expr.to_string) to t_495
	#load the string str_82
	li $a0, 8
	li $v0, 9
	syscall
	la $v1, String
	sw $v1, 0($v0)
	la $v1, str_82
	sw $v1, 4($v0)
	sw $v0, -28($fp)
	
	# assign (add here the expr.to_string) to t_496
	#load the variable t_495
	lw $v0, -28($fp)
	sw $v0, -32($fp)
	
	lw $v0, 12($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	lw $v0, -32($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	# assign (add here the expr.to_string) to t_497
	# calling the method out_string of type CellularAutomaton
	#load the variable self_CellularAutomaton
	lw $v0, 12($fp)
	lw $t0, 0($v0)
	lw $v1, 24($t0)
	jal $v1
	# pop the top of the stack to $v1
	addi $sp $sp 4
	lw $v1, 0($sp)
	
	# pop the top of the stack to $v1
	addi $sp $sp 4
	lw $v1, 0($sp)
	
	sw $v0, -36($fp)
	
	lw $v0, 12($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	# assign (add here the expr.to_string) to t_498
	# calling the method in_string of type CellularAutomaton
	#load the variable self_CellularAutomaton
	lw $v0, 12($fp)
	lw $t0, 0($v0)
	lw $v1, 32($t0)
	jal $v1
	# pop the top of the stack to $v1
	addi $sp $sp 4
	lw $v1, 0($sp)
	
	sw $v0, -40($fp)
	
	# assign (add here the expr.to_string) to ans_488
	#load the variable t_498
	lw $v0, -40($fp)
	sw $v0, -0($fp)
	
	# assign (add here the expr.to_string) to t_499
	#load the string str_83
	li $a0, 8
	li $v0, 9
	syscall
	la $v1, String
	sw $v1, 0($v0)
	la $v1, str_83
	sw $v1, 4($v0)
	sw $v0, -44($fp)
	
	# assign (add here the expr.to_string) to t_500
	#load the variable ans_488
	lw $v0, -0($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	#load the variable t_499
	lw $v0, -44($fp)
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
	
	sw $v0, -48($fp)
	
	# assign (add here the expr.to_string) to t_501
	#load the variable t_500
	lw $v0, -48($fp)
	sw $v0, -52($fp)
	
	lw $t1, -52($fp)
	lw $t0, 4($t1)
	bne $t0, $zero, then_53
	# assign (add here the expr.to_string) to t_503
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
	
	sw $v0, -60($fp)
	
	# assign (add here the expr.to_string) to t_502
	#load the variable t_503
	lw $v0, -60($fp)
	sw $v0, -56($fp)
	
	j ifend_53
	then_53:
	# assign (add here the expr.to_string) to t_504
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
	
	sw $v0, -64($fp)
	
	# assign (add here the expr.to_string) to t_502
	#load the variable t_504
	lw $v0, -64($fp)
	sw $v0, -56($fp)
	
	ifend_53:
	# assign (add here the expr.to_string) to t_505
	#load the variable t_502
	lw $v0, -56($fp)
	sw $v0, -68($fp)
	
	# return the value of the function in the register $v0
	#load the variable t_505
	lw $v0, -68($fp)
	move $v0, $v0
	
	# restore the stack pointer, frame pointer y return address
	addu $sp $sp 72
	# pop the top of the stack to $fp
	addi $sp $sp 4
	lw $fp, 0($sp)
	
	# pop the top of the stack to $ra
	addi $sp $sp 4
	lw $ra, 0($sp)
	
	jr $ra
	
	.text
Init_CellularAutomaton:
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
	
	lw $v0, 12($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	# assign (add here the expr.to_string) to self_CellularAutomaton
	jal Init_Board
	# pop the top of the stack to $v1
	addi $sp $sp 4
	lw $v1, 0($sp)
	
	sw $v0, 12($fp)
	
	# assign (add here the expr.to_string) to t_506
	#load the string str_empty
	li $a0, 8
	li $v0, 9
	syscall
	la $v1, String
	sw $v1, 0($v0)
	la $v1, str_empty
	sw $v1, 4($v0)
	sw $v0, -0($fp)
	
	# Setting value of the attribute population_map in the instance self_CellularAutomaton to t_506
	#load the variable t_506
	lw $v0, -0($fp)
	move $s2, $v0
	lw $v1, 12($fp)
	sw $s2, 16($v1)
	
	# return the value of the function in the register $v0
	#load the variable self_CellularAutomaton
	lw $v0, 12($fp)
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
	subu $sp $sp 136
	
	# assign (add here the expr.to_string) to continue_507
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
	
	# assign (add here the expr.to_string) to choice_508
	#load the string str_empty
	li $a0, 8
	li $v0, 9
	syscall
	la $v1, String
	sw $v1, 0($v0)
	la $v1, str_empty
	sw $v1, 4($v0)
	sw $v0, -4($fp)
	
	# assign (add here the expr.to_string) to t_509
	#load the string str_84
	li $a0, 8
	li $v0, 9
	syscall
	la $v1, String
	sw $v1, 0($v0)
	la $v1, str_84
	sw $v1, 4($v0)
	sw $v0, -8($fp)
	
	# assign (add here the expr.to_string) to t_510
	#load the variable t_509
	lw $v0, -8($fp)
	sw $v0, -12($fp)
	
	lw $v0, 12($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	lw $v0, -12($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	# assign (add here the expr.to_string) to t_511
	# calling the method out_string of type Main
	#load the variable self_Main
	lw $v0, 12($fp)
	lw $t0, 0($v0)
	lw $v1, 24($t0)
	jal $v1
	# pop the top of the stack to $v1
	addi $sp $sp 4
	lw $v1, 0($sp)
	
	# pop the top of the stack to $v1
	addi $sp $sp 4
	lw $v1, 0($sp)
	
	sw $v0, -16($fp)
	
	# assign (add here the expr.to_string) to t_512
	#load the string str_85
	li $a0, 8
	li $v0, 9
	syscall
	la $v1, String
	sw $v1, 0($v0)
	la $v1, str_85
	sw $v1, 4($v0)
	sw $v0, -20($fp)
	
	# assign (add here the expr.to_string) to t_513
	#load the variable t_512
	lw $v0, -20($fp)
	sw $v0, -24($fp)
	
	lw $v0, 12($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	lw $v0, -24($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	# assign (add here the expr.to_string) to t_514
	# calling the method out_string of type Main
	#load the variable self_Main
	lw $v0, 12($fp)
	lw $t0, 0($v0)
	lw $v1, 24($t0)
	jal $v1
	# pop the top of the stack to $v1
	addi $sp $sp 4
	lw $v1, 0($sp)
	
	# pop the top of the stack to $v1
	addi $sp $sp 4
	lw $v1, 0($sp)
	
	sw $v0, -28($fp)
	
	while_2:
	lw $v0, 12($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	# assign (add here the expr.to_string) to t_515
	# calling the method prompt2 of type Main
	#load the variable self_Main
	lw $v0, 12($fp)
	lw $t0, 0($v0)
	lw $v1, 116($t0)
	jal $v1
	# pop the top of the stack to $v1
	addi $sp $sp 4
	lw $v1, 0($sp)
	
	sw $v0, -32($fp)
	
	# assign (add here the expr.to_string) to t_516
	#load the variable t_515
	lw $v0, -32($fp)
	sw $v0, -36($fp)
	
	lw $t1, -36($fp)
	lw $t0, 4($t1)
	bne $t0, $zero, body_2
	j pool_2
	body_2:
	# assign (add here the expr.to_string) to t_518
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
	
	sw $v0, -44($fp)
	
	# assign (add here the expr.to_string) to continue_507
	#load the variable t_518
	lw $v0, -44($fp)
	sw $v0, -0($fp)
	
	lw $v0, 12($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	# assign (add here the expr.to_string) to t_519
	# calling the method option of type Main
	#load the variable self_Main
	lw $v0, 12($fp)
	lw $t0, 0($v0)
	lw $v1, 108($t0)
	jal $v1
	# pop the top of the stack to $v1
	addi $sp $sp 4
	lw $v1, 0($sp)
	
	sw $v0, -48($fp)
	
	# assign (add here the expr.to_string) to choice_508
	#load the variable t_519
	lw $v0, -48($fp)
	sw $v0, -4($fp)
	
	# assign (add here the expr.to_string) to t_520
	li $a0, 20
	li $v0, 9
	syscall
	la $a0, CellularAutomaton
	sw $a0,  0($v0)
	sw $v0, -52($fp)
	
	lw $v0, -52($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	# assign (add here the expr.to_string) to t_521
	# calling the method Init_CellularAutomaton of type CellularAutomaton
	#load the variable t_520
	lw $v0, -52($fp)
	lw $t0, 0($v0)
	lw $v1, 8($t0)
	jal $v1
	# pop the top of the stack to $v1
	addi $sp $sp 4
	lw $v1, 0($sp)
	
	sw $v0, -56($fp)
	
	# assign (add here the expr.to_string) to t_522
	#load the variable t_521
	lw $v0, -56($fp)
	sw $v0, -60($fp)
	
	# assign (add here the expr.to_string) to t_523
	#load the variable choice_508
	lw $v0, -4($fp)
	sw $v0, -64($fp)
	
	lw $v0, -60($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	lw $v0, -64($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	# assign (add here the expr.to_string) to t_524
	# calling the method init of type CellularAutomaton
	#load the variable t_522
	lw $v0, -60($fp)
	lw $t0, 0($v0)
	lw $v1, 48($t0)
	jal $v1
	# pop the top of the stack to $v1
	addi $sp $sp 4
	lw $v1, 0($sp)
	
	# pop the top of the stack to $v1
	addi $sp $sp 4
	lw $v1, 0($sp)
	
	sw $v0, -68($fp)
	
	# Setting value of the attribute cells in the instance self_Main to t_524
	#load the variable t_524
	lw $v0, -68($fp)
	move $s2, $v0
	lw $v1, 12($fp)
	sw $s2, 20($v1)
	
	# assign (add here the expr.to_string) to t_525
	lw $v1, 12($fp)
	lw $v0, 20($v1)
	sw $v0, -72($fp)
	
	# assign (add here the expr.to_string) to t_526
	#load the variable t_525
	lw $v0, -72($fp)
	sw $v0, -76($fp)
	
	lw $v0, -76($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	# assign (add here the expr.to_string) to t_527
	# calling the method print of type CellularAutomaton
	#load the variable t_526
	lw $v0, -76($fp)
	lw $t0, 0($v0)
	lw $v1, 52($t0)
	jal $v1
	# pop the top of the stack to $v1
	addi $sp $sp 4
	lw $v1, 0($sp)
	
	sw $v0, -80($fp)
	
	while_3:
	# assign (add here the expr.to_string) to t_528
	#load the variable continue_507
	lw $v0, -0($fp)
	sw $v0, -84($fp)
	
	lw $t1, -84($fp)
	lw $t0, 4($t1)
	bne $t0, $zero, body_3
	j pool_3
	body_3:
	lw $v0, 12($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	# assign (add here the expr.to_string) to t_530
	# calling the method prompt of type Main
	#load the variable self_Main
	lw $v0, 12($fp)
	lw $t0, 0($v0)
	lw $v1, 112($t0)
	jal $v1
	# pop the top of the stack to $v1
	addi $sp $sp 4
	lw $v1, 0($sp)
	
	sw $v0, -92($fp)
	
	# assign (add here the expr.to_string) to t_531
	#load the variable t_530
	lw $v0, -92($fp)
	sw $v0, -96($fp)
	
	lw $t1, -96($fp)
	lw $t0, 4($t1)
	bne $t0, $zero, then_54
	# assign (add here the expr.to_string) to t_533
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
	
	sw $v0, -104($fp)
	
	# assign (add here the expr.to_string) to continue_507
	#load the variable t_533
	lw $v0, -104($fp)
	sw $v0, -0($fp)
	
	# assign (add here the expr.to_string) to t_532
	#load the variable continue_507
	lw $v0, -0($fp)
	sw $v0, -100($fp)
	
	j ifend_54
	then_54:
	# assign (add here the expr.to_string) to t_534
	lw $v1, 12($fp)
	lw $v0, 20($v1)
	sw $v0, -108($fp)
	
	# assign (add here the expr.to_string) to t_535
	#load the variable t_534
	lw $v0, -108($fp)
	sw $v0, -112($fp)
	
	lw $v0, -112($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4

	.globl test
test:
	# assign (add here the expr.to_string) to t_536
	# calling the method evolve of type CellularAutomaton
	#load the variable t_535
	lw $v0, -112($fp)
	lw $t0, 0($v0)
	lw $v1, 104($t0)
	jal $v1
	# pop the top of the stack to $v1
	addi $sp $sp 4
	lw $v1, 0($sp)
	
	sw $v0, -116($fp)
	
	# assign (add here the expr.to_string) to t_537
	lw $v1, 12($fp)
	lw $v0, 20($v1)
	sw $v0, -120($fp)
	
	# assign (add here the expr.to_string) to t_538
	#load the variable t_537
	lw $v0, -120($fp)
	sw $v0, -124($fp)
	
	lw $v0, -124($fp)
	# push $v0 to the stack
	sw $v0, 0($sp)
	addi $sp $sp -4
	
	# assign (add here the expr.to_string) to t_539
	# calling the method print of type CellularAutomaton
	#load the variable t_538
	lw $v0, -124($fp)
	lw $t0, 0($v0)
	lw $v1, 52($t0)
	jal $v1
	# pop the top of the stack to $v1
	addi $sp $sp 4
	lw $v1, 0($sp)
	
	sw $v0, -128($fp)
	
	# assign (add here the expr.to_string) to t_532
	#load the variable t_539
	lw $v0, -128($fp)
	sw $v0, -100($fp)
	
	ifend_54:
	# assign (add here the expr.to_string) to t_529
	#load the variable t_532
	lw $v0, -100($fp)
	sw $v0, -88($fp)
	
	j while_3
	pool_3:
	# assign (add here the expr.to_string) to t_517
	#load the variable t_529
	lw $v0, -88($fp)
	sw $v0, -40($fp)
	
	j while_2
	pool_2:
	# assign (add here the expr.to_string) to t_540
	#load the variable self_Main
	lw $v0, 12($fp)
	sw $v0, -132($fp)
	
	# return the value of the function in the register $v0
	#load the variable t_540
	lw $v0, -132($fp)
	move $v0, $v0
	
	# restore the stack pointer, frame pointer y return address
	addu $sp $sp 136
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
	jal Init_CellularAutomaton
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

copy_Object:
            # calling conventions
        sw $ra, 0($sp)
        addi $sp, $sp, -4
        sw $fp, 0($sp)
        addi $sp, $sp, -4
        move $fp, $sp


        lw $t7, 12($fp) # load the object address
        lw $t6, 0($t7) # get the type info address
        lw $t5, 0($t6) # get the size of the type

        move $a0, $t5
        li $v0, 9
        syscall
        move $t6, $v0
copy_Object_loop:
        lw $t4, 0($t7)
        sw $t4, 0($t6)
        addu $t7, $t7, 4
        addu $t6, $t6, 4
        addu $t5, $t5, -4
        bgtz $t5, copy_Object_loop              
        
        
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
        lbu $t3, 0($t1)
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


	.globl substr
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
        lbu $t7, 0($t0)
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
        lbu $t1, 0($a0)
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

                la $t4, type
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
		lbu $t3, 0($t0)
		lbu $t4, 0($t1)
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

        lw $t0, 16($fp)
        lw $t0, 4($t0) # the value of the first String instance

        # call strlen with the string
        sw $t0, 0($sp)
        addi $sp, $sp, -4
        jal strlen
        addi $sp, $sp, 4
        lw $t0, 0($sp)

        #save the lenght of the first string
        sw $v0, 0($sp)
        addi $sp, $sp, -4


        lw $t0, 16($fp)
        lw $t0, 4($t0) # the value of the second String instance

        # call strlen with the string
        sw $t0, 0($sp)
        addi $sp, $sp, -4
        jal strlen
        addi $sp, $sp, 4
        lw $t0, 0($sp)

        # pop the lenght of the first string from the stack
        addi $sp, $sp, 4
        lw $t0, 0($sp) 
        
        # get the total space for allocating the new string
        addu $t0, $t0, $v0
        addi $t0, $t0, 1

        move $a0, $t0
        li $v0, 9
        syscall # at $v0 is the result string

        lw $t0, 16($fp)
        lw $t0, 4($t0) # the address of the value of the first String instance
        move $t1, $v0 # the address of the value of the result string
        concat_String_loop1:
        lbu $t3, 0($t0)
        beq $t3, $zero, concat_String_eloop1
        sb $t3, 0($t1)
        addi $t0, $t0, 1
        addi $t1, $t1, 1
        j concat_String_loop1

        concat_String_eloop1:

        lw $t0, 12($fp)
        lw $t0, 4($t0)
        concat_String_loop2:
        lbu $t3, 0($t0)
        beq $t3, $zero, concat_String_eloop2
        sb $t3, 0($t1)
        addi $t0, $t0, 1
        addi $t1, $t1, 1
        j concat_String_loop2
        concat_String_eloop2:
        sb $zero, 0($t1)

        la $t0, String
        move $t1, $v0

        li $a0, 8
        li $v0, 9
        syscall

        sw $t0, 0($v0)
        sw $t1, 4($v0)

        # calling conventions
        addi $sp, $sp, 4
        lw $fp, 0($sp)
        addi $sp, $sp, 4
        lw $ra, 0($sp)
        
        jr $ra











		













