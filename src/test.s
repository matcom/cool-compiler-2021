.data
bool: .word  1

.text
main:
li $v0 , 1
li $t0 ,-1
lw $t2 , bool
addi $t1 , $t2 ,-1
mul $a0	, $t1	,-1		# $t0 * $t1 = Hi and Lo registers

syscall

li $v0 ,10
syscall
