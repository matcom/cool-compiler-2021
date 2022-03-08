memory_operations='''
header_size = 12 #in bytes
header_size_slot = 0
header_next_slot = 4
header_reachable_slot = 8
alloc_size       = 2048
total_alloc_size =  2060 #alloc_size + header_size
neg_header_size = -12 #-header_size
free_list = 0
used_list = header_size
state_size = 4
stack_base = -4
init_alloc_size = 28 #(header_size*2) +  state_size
object_mark = -1
meta_data_object_size = 4   #in words
object_expanded = -2
reachable = 1
new_line = 10
str_size_treshold = 1024
int_type = 0
string_type = 0
type_number = 0

free_block:
    addiu $sp $sp -28
    sw $t0 0($sp)
    sw $t1 4($sp)
    sw $t2 8($sp)
    sw $a0 12($sp)
    sw $ra 16($sp)
    sw $t3 20($sp)
    sw $t4 24($sp)

    move $t0 $a0
    
    addiu $t1 $gp free_list        

    addiu $t3 $gp used_list         

free_block_loop_used_list:         
    beq $t4 $t0 free_block_loop_free_list
    move $t3 $t4
    j free_block_loop_used_list


free_block_loop_free_list:         
    lw $t2 header_next_slot($t1)
    beq $t2 $zero free_block_founded_prev
    bge $t2 $t0 free_block_founded_prev
    move $t1 $t2
    j free_block_loop_free_list

free_block_founded_prev:        
    # Remove the block from the used-list
    lw $t4 header_next_slot($t0)
    sw $t4 header_next_slot($t3)
    
    # Add the block to the free-list
    sw $t2 header_next_slot($t0)
    sw $t0 header_next_slot($t1)

free_block_end:
   
    move $a0 $t0
    jal expand_block
    move $a0 $t1
    jal expand_block

    lw $t0 0($sp)
    lw $t1 4($sp)
    lw $t2 8($sp)
    lw $a0 12($sp)
    lw $ra 16($sp)
    lw $t3 20($sp)
    lw $t4 24($sp)
    addiu $sp $sp 28

    jr $ra


expand_block:
    addiu $sp $sp -16
    sw $t0 0($sp)
    sw $t1 4($sp)
    sw $t2 8($sp)
    sw $t3 12($sp)

    
    addiu $t0 $gp free_list    

    beq $t0 $a0 expand_block_end  
    move $t0 $a0

   
    lw $t1 header_next_slot($t0)
    lw $t2 header_size_slot($t0)
    move $t3 $t2
    addiu $t2 $t2 header_size
    addu $t2 $t2 $t0
    beq $t2 $t1 expand_block_expand
    j expand_block_end

expand_block_expand:    
    lw $t2 header_size_slot($t1)
    addi $t2 $t2 header_size
    add $t2 $t2 $t3
    sw $t2 header_size_slot($t0)
    lw $t1 header_next_slot($t1)
    sw $t1 header_next_slot($t0)
    
expand_block_end:
    lw $t0 0($sp)
    lw $t1 4($sp)
    lw $t2 8($sp)
    lw $t3 12($sp)
    addiu $sp $sp 16

    jr $ra


extend_heap:
    addiu $sp $sp -12
    sw $a0 0($sp)
    sw $a1 4($sp)
    sw $t0 8($sp)

    
    li $v0 9
    addiu $a0 $a1 header_size
    syscall
    
    
    move $t0 $a1 
    sw $t0 header_size_slot($v0)
    sw $zero header_next_slot($v0)
    sw $zero header_reachable_slot($v0)

    
    lw $t0, 0($sp)
    sw $v0 header_next_slot($t0)

    move $a0 $t0
    lw $a1 4($sp)
    lw $t0 8($sp)
    addiu $sp $sp 12

    jr $ra


  
split_block:
    addiu $sp $sp -16
    sw $t0 0($sp)
    sw $t1 4($sp)
    sw $a0 8($sp)
    sw $a1 12($sp)

   
    lw $t0 header_size_slot($a0)
    bgt $a1 $t0 split_block_error_small
    
    
    sub $t0 $t0 $a1
    li $t1 header_size
    ble $t0 $t1 split_block_same_size

    
    addu $t0 $a0 $a1
    addiu $t0 $t0 header_size     

    #Update headers of the two blocks
    lw $t1 header_next_slot($a0)    
    sw $t1 header_next_slot($t0)
    sw $t0 header_next_slot($a0)

    lw $t1 header_size_slot($a0)    
    sub $t1 $t1 $a1

    addi $t1 $t1 neg_header_size
    sw $t1 header_size_slot($t0)
    sw $a1 header_size_slot($a0)
    move $v0 $a0
    j split_block_end

split_block_same_size:
    move $v0 $a0
    j split_block_end

split_block_error_small:
    j split_block_end

split_block_end:
    lw $t0 0($sp)
    lw $t1 4($sp)
    lw $a0 8($sp)
    lw $a1 12($sp)
    addiu $sp $sp 16

    jr $ra

malloc:
    move $v0 $zero
    addiu $sp $sp -28
    sw $t1 0($sp)
    sw $t0 4($sp)
    sw $a0 8($sp)
    sw $a1 12($sp)
    sw $ra 16($sp)
    sw $t2 20($sp)
    sw $t3 24($sp)
    
    addiu $t0 $gp free_list
    j malloc_loop

malloc_end:

    move $a0 $v0
    lw $a1 8($sp)                  
    jal split_block

    lw $t1 header_next_slot($v0)
    sw $t1 header_next_slot($t3)

    addiu $t1 $gp used_list
    lw $a0 header_next_slot($t1)

    sw $a0 header_next_slot($v0)
    sw $v0 header_next_slot($t1)
    
    addiu $v0 $v0 header_size

    lw $t3 24($sp)
    lw $t2 20($sp)
    lw $ra 16($sp)
    lw $a1 12($sp)
    lw $a0 8($sp)
    lw $t0 4($sp)
    lw $t1 0($sp)
    addiu $sp $sp 28

    jr $ra

malloc_loop:
    move $t2 $t0                        
    lw $t0 header_next_slot($t0)        
    beq $t0 $zero malloc_search_end     
    j malloc_check_valid_block

malloc_search_end:
    beq $v0 $zero malloc_alloc_new_block  
    j malloc_end

malloc_alloc_new_block:
    li $t1 alloc_size               
    move $t3 $t2
    move $a1 $a0                    
    move $a0 $t2                    
    bge $a1 $t1 malloc_big_block   
    li $a1 alloc_size         
    jal extend_heap
    
    j malloc_end

malloc_big_block:
    #addiu $a1 $a1 header_size              
    jal extend_heap
    j malloc_end



malloc_check_valid_block:
    lw $t1 header_size_slot($t0)      
    bge $t1 $a0 malloc_valid_block    
    j malloc_loop

malloc_valid_block:
    beq $v0 $zero malloc_first_valid_block  
    bge $t1 $v1 malloc_loop                 
    move $v0 $t0                        
    move $v1 $t1                        
    move $t3 $t2
    j malloc_loop


malloc_first_valid_block:
    move $v0 $t0                        
    move $v1 $t1                        
    move $t3 $t2 
    j malloc_loop


copy:
    addiu $sp $sp -16
    sw $a0 0($sp)
    sw $a1 4($sp)
    sw $a2 8($sp)
    sw $t0 12($sp)

copy_loop:
    beq $a2 $zero copy_end
    lw $t0 0($a0)
    sw $t0 0($a1)
    addiu $a0 $a0 4
    addiu $a1 $a1 4
    addi $a2 $a2 -4
    j copy_loop 

copy_end:
    lw $a0 0($sp)
    lw $a1 4($sp)
    lw $a2 8($sp)
    lw $t0 12($sp)
    addiu $sp $sp 16

    jr $ra


use_block:
    addiu $sp $sp -12
    sw $t0 0($sp)
    sw $t1 4($sp)
    sw $t2 8($sp)

    addiu $t0 $gp free_list

use_block_loop:
    move $t1 $t0
    lw $t0 header_next_slot($t0)
    beq $t0 $zero use_block_end
    beq $t0 $a0 use_block_founded
    j use_block_loop

use_block_founded:
    lw $t2 header_next_slot($t0)
    sw $t2 header_next_slot($t1)

    addiu $t1 $gp used_list
    lw $t2 header_next_slot($t1)
    sw $t0 header_next_slot($t1)
    sw $t2 header_next_slot($t0)

use_block_end:
    lw $t0 0($sp)
    lw $t1 4($sp)
    lw $t2 8($sp)
    addiu $sp $sp 12

    jr $ra
'''