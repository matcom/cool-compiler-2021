from BaseCILToMIPSVisitor import *
from utils import visitor
import cil_ast as cil


class CILToMIPSVisitor(BaseCILToMIPSVisitor):
    @visitor.on('node')
    def visit(self, node):
        pass

    @visitor.when(cil.ProgramNode)
    def visit(self, node):
        self.types = node.dottypes
        self.data += 'temp_string: .space 2048\n'
        self.data += 'void: .word 0\n'

        for node_type in node.dottypes.values():
            self.visit(node_type)

        for node_data in node.dotdata.keys():
            self.data += f'{node_data}: .asciiz "{node.dotdata[node_data]}"\n'

        for node_function in node.dotcode:
            self.visit(node_function)

        self.mips_code = '.data\n' + self.data + '.text\n' + self.text
        return self.mips_code.strip()

    @visitor.when(cil.TypeNode)
    def visit(self, node):
        self.data += f'{node.name}_name: .asciiz "{node.name}"\n'
        self.data += f'{node.name}_methods:\n'
        for method in node.methods.values():
            self.data += f'.word {method}\n'

        idx = 0
        self.attr_offset.__setitem__(node.name, {})
        for attr in node.attributes:
            self.attr_offset[node.name][attr] = 4*idx + 16
            idx = idx + 1

        idx = 0
        self.method_offset.__setitem__(node.name, {})
        for met in node.methods:
            self.method_offset[node.name][met] = 4*idx
            idx = idx + 1

    @visitor.when(cil.FunctionNode)
    def visit(self, node):
        self.current_function = node
        self.var_offset.__setitem__(self.current_function.name, {})

        for idx, var in enumerate(self.current_function.localvars + self.current_function.params):
            self.var_offset[self.current_function.name][var.name] = (idx + 1)*4

        self.text += f'{node.name}:\n'
        # save space for locals
        self.text += f'addi $sp, $sp, {-4 * len(node.localvars)}\n'
        self.text += 'addi $sp, $sp, -4\n'  # save return address
        self.text += 'sw $ra, 0($sp)\n'

        for instruction in node.instructions:
            self.visit(instruction)

        self.text += 'lw $ra, 0($sp)\n'  # recover return address
        total = 4 * len(node.localvars) + 4 * len(node.params) + 4
        # pop locals,parameters,return address from the stack
        self.text += f'addi $sp, $sp, {total}\n'
        self.text += 'jr $ra\n'

    @visitor.when(cil.ParamNode)
    def visit(self, node):
        pass

    @visitor.when(cil.LocalNode)
    def visit(self, node, idx):
        pass

    @visitor.when(cil.AssignNode)
    def visit(self, node):
        offset = self.var_offset[self.current_function.name][node.local_dest]
        if node.expr:
            if isinstance(node.expr, int):
                self.text += f'li $t1, {node.expr}\n'
            else:
                right_offset = self.var_offset[self.current_function.name][node.expr]
                self.text += f'lw $t1, {right_offset}($sp)\n'
        else:
            self.text += f'la $t1, void\n'

        self.text += f'sw $t1, {offset}($sp)\n'

    @visitor.when(cil.BinaryOperationNode)
    def visit(self, node):
        mips_comm = self.mips_operators[node.op]
        left_offset = self.var_offset[self.current_function.name][node.lvalue]
        right_offset = self.var_offset[self.current_function.name][node.rvalue]
        self.text += f'lw $a0, {left_offset}($sp)\n'
        self.text += f'lw $t1, {right_offset}($sp)\n'
        if node.op == '/':
            self.text += 'beq $t1, 0, div_zero_error\n'
        self.text += f'{mips_comm} $a0, $a0, $t1\n'
        result_offset = self.var_offset[self.current_function.name][node.local_dest]
        self.text += f'sw $a0, {result_offset}($sp)\n'

    @visitor.when(cil.UnaryOperationNode)
    def visit(self, node):
        expr_offset = self.var_offset[self.current_function.name][node.expr]
        self.text += f'lw $t1, {expr_offset}($sp)\n'
        if node.op == '~':
            self.text += f'xor $a0, $t1, 1\n'
        else:
            self.text += f'neg $a0, $t1 \n'

        result_offset = self.var_offset[self.current_function.name][node.local_dest]
        self.text += f'sw $a0, {result_offset}($sp)\n'

    @visitor.when(cil.GetAttrNode)
    def visit(self, node):
        self_offset = self.var_offset[self.current_function.name][node.instance]
        self.text += f'lw $t0, {self_offset}($sp)\n'

        attr_offset = self.attr_offset[node.static_type][node.attr]
        self.text += f'lw $t1, {attr_offset}($t0)\n'

        result_offset = self.var_offset[self.current_function.name][node.local_dest]
        self.text += f'sw $t1, {result_offset}($sp)\n'

    @visitor.when(cil.SetAttrNode)
    def visit(self, node):
        self_offset = self.var_offset[self.current_function.name][node.instance]
        self.text += f'lw $t0, {self_offset}($sp)\n'

        if node.value:
            value_offset = self.var_offset[self.current_function.name][node.value]
            self.text += f'lw $t1, {value_offset}($sp)\n'
        else:
            self.text += f'la $t1, void\n'

        attr_offset = self.attr_offset[node.static_type][node.attr]
        self.text += f'sw $t1, {attr_offset}($t0)\n'

    @visitor.when(cil.AllocateNode)
    def visit(self, node):
        amount = len(self.types[node.type].attributes) + 4
        self.text += f'li $a0, {amount * 4}\n'
        self.text += f'li $v0, 9\n'
        self.text += f'syscall\n'
        self.text += 'bge $v0, $sp heap_error\n'
        self.text += f'move $t0, $v0\n'

        # Initialize Object
        self.text += f'li $t1, {node.tag}\n'
        self.text += f'sw $t1, 0($t0)\n'
        self.text += f'la $t1, {node.type}_name\n'
        self.text += f'sw $t1, 4($t0)\n'
        self.text += f'li $t1, {amount}\n'
        self.text += f'sw $t1, 8($t0)\n'
        self.text += f'la $t1, {node.type}_methods\n'
        self.text += f'sw $t1, 12($t0)\n'

        offset = self.var_offset[self.current_function.name][node.local_dest]
        self.text += f'sw $t0, {offset}($sp)\n'

    @visitor.when(cil.TypeOfNode)
    def visit(self, node):
        obj_offset = self.var_offset[self.current_function.name][node.instance]
        self.text += f'lw $t0, {obj_offset}($sp)\n'
        self.text += 'lw $t1, 4($t0)\n'
        res_offset = self.var_offset[self.current_function.name][node.local_dest]
        self.text += f'sw $t1, {res_offset}($sp)\n'

    @visitor.when(cil.LabelNode)
    def visit(self, node):
        self.text += f'{node.label}:\n'

    @visitor.when(cil.GoToNode)
    def visit(self, node):
        self.text += f'b {node.label}\n'

    @visitor.when(cil.IfGoToNode)
    def visit(self, node):
        predicate_offset = self.var_offset[self.current_function.name][node.condition]
        self.text += f'lw $t0, {predicate_offset}($sp)\n'
        self.text += f'lw $a0, 16($t0)\n'
        self.text += f'bnez $a0, {node.label}\n'

    @visitor.when(cil.CallNode)
    def visit(self, node):
        self.text += 'move $t0, $sp\n'

        for arg in node.params:
            self.visit(arg)

        self.text += f'jal {node.function}\n'
        result_offset = self.var_offset[self.current_function.name][node.local_dest]
        self.text += f'sw $a1, {result_offset}($sp)\n'

    @visitor.when(cil.VCallNode)
    def visit(self, node):
        self.text += 'move $t0, $sp\n'

        for arg in node.params:
            self.visit(arg)

        value_offset = self.var_offset[self.current_function.name][node.instance]
        self.text += f'lw $t1, {value_offset}($t0)\n'
        self.text += 'la $t0, void\n'
        self.text += 'beq $t1, $t0, dispatch_void_error\n'

        self.text += f'lw $t2, 12($t1)\n'

        method_offset = self.method_offset[node.dynamic_type][node.function]
        self.text += f'lw $t3, {method_offset}($t2)\n'

        self.text += 'jal $t3\n'

        result_offset = self.var_offset[self.current_function.name][node.local_dest]
        self.text += f'sw $a1, {result_offset}($sp)\n'

    @visitor.when(cil.ArgNode)
    def visit(self, node):
        value_offset = self.var_offset[self.current_function.name][node.name]
        self.text += f'lw $t1, {value_offset}($t0)\n'
        self.text += 'addi $sp, $sp, -4\n'
        self.text += 'sw $t1, 0($sp)\n'

    @visitor.when(cil.ReturnNode)
    def visit(self, node):
        if node.value:
            offset = self.var_offset[self.current_function.name][node.value]
            self.text += f'lw $a1, {offset}($sp)\n'
        else:
            self.text += f'move $a1, $zero\n'

    @visitor.when(cil.LoadStringNode)
    def visit(self, node):
        self.text += f'la $t0, {node.msg}\n'
        offset = self.var_offset[self.current_function.name][node.local_dest]
        self.text += f'sw $t0, {offset}($sp)\n'

    @visitor.when(cil.LoadIntNode)
    def visit(self, node):
        self.text += f'li $t0, {node.value}\n'
        offset = self.var_offset[self.current_function.name][node.local_dest]
        self.text += f'sw $t0, {offset}($sp)\n'

    @visitor.when(cil.LengthNode)
    def visit(self, node):
        offset = self.var_offset[self.current_function.name][node.variable]
        self.text += f'lw $t0, {offset}($sp)\n'
        self.text += f'lw $t0, 16($t0)\n'

        self.text += 'li $a0, 0\n'
        self.text += 'count_char:\n'
        self.text += 'lb $t1, 0($t0)\n'
        self.text += 'beqz $t1, finish_chars_count\n'
        self.text += 'addi $t0, $t0, 1\n'
        self.text += 'addi $a0, $a0, 1\n'
        self.text += 'j count_char\n'
        self.text += 'finish_chars_count:\n'

        offset = self.var_offset[self.current_function.name][node.result]
        self.text += f'sw $a0, {offset}($sp)\n'

    @visitor.when(cil.ConcatNode)
    def visit(self, node):
        offset_str1 = self.var_offset[self.current_function.name][node.str1]
        offset_len1 = self.var_offset[self.current_function.name][node.len1]

        offset_str2 = self.var_offset[self.current_function.name][node.str2]
        offset_len2 = self.var_offset[self.current_function.name][node.len2]

        self.text += f'lw $a0, {offset_len1}($sp)\n'
        self.text += f'lw $t0, {offset_len2}($sp)\n'

        self.text += 'add $a0, $a0, $t0\n'
        self.text += 'addi $a0, $a0, 1\n'
        self.text += f'li $v0, 9\n'
        self.text += f'syscall\n'
        self.text += 'bge $v0, $sp heap_error\n'
        self.text += 'move $t3, $v0\n'

        self.text += f'lw $t0, {offset_str1}($sp)\n'
        self.text += f'lw $t1, {offset_str2}($sp)\n'

        self.text += 'copy_str1_char:\n'
        self.text += 'lb $t2, 0($t0)\n'
        self.text += 'sb $t2, 0($v0)\n'
        self.text += 'beqz $t2, concat_str2_char\n'
        self.text += 'addi $t0, $t0, 1\n'
        self.text += 'addi $v0, $v0, 1\n'
        self.text += 'j copy_str1_char\n'

        self.text += 'concat_str2_char:\n'
        self.text += 'lb $t2, 0($t1)\n'
        self.text += 'sb $t2, 0($v0)\n'
        self.text += 'beqz $t2, finish_str2_concat\n'
        self.text += 'addi $t1, $t1, 1\n'
        self.text += 'addi $v0, $v0, 1\n'
        self.text += 'j concat_str2_char\n'
        self.text += 'finish_str2_concat:\n'
        self.text += 'sb $0, ($v0)\n'

        offset = self.var_offset[self.current_function.name][node.result]
        self.text += f'sw $t3, {offset}($sp)\n'

    @visitor.when(cil.SubstringNode)
    def visit(self, node):
        offset_idx = self.var_offset[self.current_function.name][node.i]
        offset_len = self.var_offset[self.current_function.name][node.length]
        offset_str = self.var_offset[self.current_function.name][node.string]

        self.text += f'lw $a0, {offset_len}($sp)\n'
        self.text += 'addi $a0, $a0, 1\n'
        self.text += f'li $v0, 9\n'
        self.text += f'syscall\n'
        self.text += 'bge $v0, $sp heap_error\n'

        self.text += f'lw $t0, {offset_idx}($sp)\n'
        self.text += f'lw $t1, {offset_len}($sp)\n'
        self.text += f'lw $t4, {offset_str}($sp)\n'
        self.text += f'lw $t2, 16($t4)\n'

        self.text += 'bltz $t0, substr_error\n'

        self.text += 'li $a0, 0\n'
        self.text += 'jump_str_char:\n'
        self.text += f'beq $a0, $t0, finish_index_jump\n'
        self.text += 'addi $a0, $a0, 1\n'
        self.text += 'addi $t2, $t2, 1\n'
        self.text += 'beq $t2, $zero, substr_error\n'
        self.text += 'j jump_str_char\n'
        self.text += 'finish_index_jump:\n'
        self.text += 'li $a0, 0\n'
        self.text += 'move $t3, $v0\n'

        self.text += 'copy_substr_char:\n'
        self.text += 'beq $a0, $t1 finish_substr_copy\n'
        self.text += 'li $t0, 0\n'
        self.text += 'lb $t0, 0($t2)\n'
        self.text += 'sb $t0, 0($v0)\n'
        self.text += 'addi $t2, $t2, 1\n'
        self.text += 'beq $t2, $zero, substr_error\n'
        self.text += 'addi $v0, $v0, 1\n'
        self.text += 'addi $a0, $a0, 1\n'
        self.text += 'j copy_substr_char\n'
        self.text += 'finish_substr_copy:\n'
        self.text += 'sb $0, ($v0)\n'

        offset = self.var_offset[self.current_function.name][node.result]
        self.text += f'sw $t3, {offset}($sp)\n'

    @visitor.when(cil.StringEqualsNode)
    def visit(self, node):
        offset_str1 = self.var_offset[self.current_function.name][node.s1]
        offset_str2 = self.var_offset[self.current_function.name][node.s2]

        self.text += f'lw $t1, {offset_str1}($sp)\n'
        self.text += f'lw $t2, {offset_str2}($sp)\n'

        self.text += 'compare_str_char:\n'
        self.text += 'li $t3, 0\n'
        self.text += 'lb $t3, 0($t1)\n'
        self.text += 'li $t4, 0\n'
        self.text += 'lb $t4, 0($t2)\n'
        self.text += 'seq $a0, $t3, $t4\n'
        self.text += 'beqz $a0, finish_compare_str\n'
        self.text += 'beqz $t3, finish_compare_str\n'
        self.text += 'beqz $t4, finish_compare_str\n'
        self.text += 'addi $t1, $t1, 1\n'
        self.text += 'addi $t2, $t2, 1\n'
        self.text += 'j compare_str_char\n'
        self.text += 'finish_compare_str:\n'

        offset = self.var_offset[self.current_function.name][node.result]
        self.text += f'sw $a0, {offset}($sp)\n'
