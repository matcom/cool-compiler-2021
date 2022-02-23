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
        function = self.dispatch_table.find_full_name(node.type, node.function)
        self.code.append(f'# Static Dispatch of the method {node.function}')
        self.push_register('fp')
        self.push_register('ra')
        self.code.append('# Push the arguments to the stack')
        for arg in reversed(node.args):
            self.visit(arg)
        self.code.append('# Empty all used registers and saves them to memory')
        self.empty_registers()
        self.code.append('# This function will consume the arguments')
        self.code.append(f'jal {function}')
        self.code.append('# Pop ra register of return function of the stack')
        self.pop_register('ra')
        self.code.append('# Pop fp register from the stack')
        self.pop_register('fp')
        if node.dest is not None:
            self.get_reg_var(node.dest)
            rdest = self.addr_desc.get_var_reg(node.dest)
            self.code.append('# saves the return value')
            self.code.append(f'move ${rdest}, $v0')
        self.var_address[node.dest] = self.get_type(node.return_type)

    @visitor.when(cil.VCallNode)
    def visit(self, node):
        self.code.append('# Find the actual name in the dispatch table')
        reg = self.addr_desc.get_var_reg(node.obj)
        self.code.append(
            '# Gets in a0 the actual direction of the dispatch table')
        self.code.append(f'lw $t9, 8(${reg})')
        self.code.append('lw $a0, 8($t9)')
        function = self.dispatch_table.find_full_name(node.type, node.method)
        index = 4*self.dispatch_table.get_offset(node.type, function) + 4
        self.code.append(f'# Saves in t8 the direction of {function}')
        self.code.append(f'lw $t8, {index}($a0)')
        self.push_register('fp')
        self.push_register('ra')
        self.code.append('# Push the arguments to the stack')
        for arg in reversed(node.args):
            self.visit(arg)
        self.code.append('# Empty all used registers and saves them to memory')
        self.empty_registers()
        self.code.append('# This function will consume the arguments')
        self.code.append(f'jal $t8')
        self.code.append('# Pop ra register of return function of the stack')
        self.pop_register('ra')
        self.code.append('# Pop fp register from the stack')
        self.pop_register('fp')
        if node.dest is not None:
            self.get_reg_var(node.dest)
            rdest = self.addr_desc.get_var_reg(node.dest)
            self.code.append('# saves the return value')
            self.code.append(f'move ${rdest}, $v0')
        self.var_address[node.dest] = self.get_type(node.return_type)

    @visitor.when(cil.ArgNode)
    def visit(self, node):
        self.code.append('# The rest of the arguments are push into the stack')
        if self.is_variable(node.dest):
            self.get_reg_var(node.dest)
            reg = self.addr_desc.get_var_reg(node.dest)
            self.code.append(f'sw ${reg}, ($sp)')
        elif self.is_int(node.dest):
            self.code.append(f'li $t9, {node.dest}')
            self.code.append(f'sw $t9, ($sp)')
        self.code.append('addiu $sp, $sp, -4')

    @visitor.when(cil.ReturnNode)
    def visit(self, node):
        if self.is_variable(node.value):
            rdest = self.addr_desc.get_var_reg(node.value)
            self.code.append(f'move $v0, ${rdest}')
        elif self.is_int(node.value):
            self.code.append(f'li $v0, {node.value}')
        self.code.append('# Empty all used registers and saves them to memory')
        self.empty_registers()
        self.code.append('# Removing all locals from stack')
        self.code.append(f'addiu $sp, $sp, {self.locals*4}')
        self.code.append(f'jr $ra')
        self.code.append('')

    @visitor.when(cil.LoadNode)
    def visit(self, node):
        rdest = self.addr_desc.get_var_reg(node.dest)
        self.code.append(f'# Saves in {node.dest} {node.msg}')
        self.var_address[node.dest] = AddrType.STR
        self.code.append(f'la ${rdest}, {node.msg}')

    @visitor.when(cil.LengthNode)
    def visit(self, node):
        rdest = self.addr_desc.get_var_reg(node.dest)
        reg = self.addr_desc.get_var_reg(node.arg)
        loop = f'loop_{self.loop_idx}'
        end = f'end_{self.loop_idx}'
        self.code.append(f'move $t8, ${reg}')
        self.code.append('# Determining the length of a string')
        self.code.append(f'{loop}:')
        self.code.append(f'lb $t9, 0($t8)')
        self.code.append(f'beq $t9, $zero, {end}')
        self.code.append(f'addi $t8, $t8, 1')
        self.code.append(f'j {loop}')
        self.code.append(f'{end}:')
        self.code.append(f'sub ${rdest}, $t8, ${reg}')
        self.loop_idx += 1

    @visitor.when(cil.ConcatNode)
    def visit(self, node):
        rdest = self.addr_desc.get_var_reg(node.dest)
        self.code.append('# Allocating memory for buffer')
        self.code.append('li $a0, 356')
        self.code.append('li $v0, 9')
        self.code.append('syscall')
        self.code.append(f'move ${rdest}, $v0')
        rsrc1 = self.addr_desc.get_var_reg(node.arg1)
        if node.arg2 is not None:
            rsrc2 = self.addr_desc.get_var_reg(node.arg2)
        self.code.append('# Copy the first string to dest')
        var = self.save_reg_if_occupied('a1')
        self.code.append(f'move $a0, ${rsrc1}')
        self.code.append(f'move $a1, ${rdest}')
        self.push_register('ra')
        self.code.append('jal strcopier')
        if node.arg2 is not None:
            self.code.append('# Concat second string on buffers result')
            self.code.append(f'move $a0, ${rsrc2}')
            self.code.append(f'move $a1, $v0')
            self.code.append('jal strcopier')
        self.code.append('sb $0, 0($v0)')
        self.pop_register('ra')
        self.code.append(f'j finish_{self.loop_idx}')
        if self.first_defined['strcopier']:
            self.code.append('# Definition of strcopier')
            self.code.append('strcopier:')
            self.code.append('# In a0 is source and in a1 is dest')
            self.code.append(f'loop_{self.loop_idx}:')
            self.code.append('lb $t8, ($a0)')
            self.code.append(f'beq $t8, $zero, end_{self.loop_idx}')
            self.code.append('addiu $a0, $a0, 1')
            self.code.append('sb $t8, ($a1)')
            self.code.append('addiu $a1, $a1, 1')
            self.code.append(f'b loop_{self.loop_idx}')
            self.code.append(f'end_{self.loop_idx}:')
            self.code.append('move $v0, $a1')
            self.code.append('jr $ra')
            self.first_defined['strcopier'] = False
        self.code.append(f'finish_{self.loop_idx}:')
        self.load_var_if_occupied(var)
        self.loop_idx += 1

    @visitor.when(cil.SubstringNode)
    def visit(self, node):
        rdest = self.addr_desc.get_var_reg(node.dest)
        self.code.append('# Allocating memory for buffer')
        self.code.append('li $a0, 356')
        self.code.append('li $v0, 9')
        self.code.append('syscall')
        self.code.append(f'move ${rdest}, $v0')
        if self.is_variable(node.begin):
            rstart = self.addr_desc.get_var_reg(node.begin)
        elif self.is_int(node.begin):
            rstart = 't8'
            self.code.append(f'li $t8, {node.begin}')
        if self.is_variable(node.end):
            rend = self.addr_desc.get_var_reg(node.end)
            var = None
        elif self.is_int(node.end):
            var = self.save_reg_if_occupied('a3')
            rend = 'a3'
            self.code.append(f'li $a3, {node.end}')
        self.get_reg_var(node.word)
        rself = self.addr_desc.get_var_reg(node.word)
        self.code.append("# Getting substring")
        start = f'start_{self.loop_idx}'
        error = f'error_{self.loop_idx}'
        end_lp = f'end_len_{self.loop_idx}'
        self.code.append('# Move to the begining')
        self.code.append('li $v0, 0')
        self.code.append(f'move $t8, ${rself}')
        self.code.append(f'{start}:')
        self.code.append('lb $t9, 0($t8)')
        self.code.append(f'beqz $t9, {error}')
        self.code.append('addi $v0, 1')
        self.code.append(f'bgt $v0, ${rstart}, {end_lp}')
        self.code.append(f'addi $t8, 1')
        self.code.append(f'j {start}')
        self.code.append(f'{end_lp}:')
        self.code.append('# Saving dest')
        self.code.append(f'move $v0, ${rdest}')
        loop = f'loop_{self.loop_idx}'
        end = f'end_{self.loop_idx}'
        self.code.append(f'{loop}:')
        self.code.append(f'sub $t9, $v0, ${rdest}')
        self.code.append(f'beq $t9, ${rend}, {end}')
        self.code.append(f'lb $t9, 0($t8)')
        self.code.append(f'beqz $t9, {error}')
        self.code.append(f'sb $t9, 0($v0)')
        self.code.append('addi $t8, $t8, 1')
        self.code.append(f'addi $v0, $v0, 1')
        self.code.append(f'j {loop}')
        self.code.append(f'{error}:')
        self.code.append('la $a0, index_error')
        self.code.append('li $v0, 4')
        self.code.append(f'move $a0, ${rself}')
        self.code.append('syscall')
        self.code.append('li $v0, 1')
        self.code.append(f'move $a0, ${rstart}')
        self.code.append('syscall')
        self.code.append('li $v0, 1')
        self.code.append(f'move $a0, ${rend}')
        self.code.append('syscall')
        self.code.append('j .raise')
        self.code.append(f'{end}:')
        self.code.append('sb $0, 0($v0)')
        self.load_var_if_occupied(var)
        self.loop_idx += 1
