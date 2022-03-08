boolean_operations ='''equals:
    beq $a0 $a1 equals_equal
    li $v0 0
    j equals_end
    
equals_equal:
    li $v0 1

equals_end:
    jr $ra



less_equal:
    ble $a0 $a1 less_equal_true
    li $v0 0
    j less_equal_end

less_equal_true:
    li $v0 1

less_equal_end:
    jr $ra


less:
    blt $a0 $a1 less_true
    li $v0 0
    j less_end

less_true:
    li $v0 1

less_end:
    jr $ra'''