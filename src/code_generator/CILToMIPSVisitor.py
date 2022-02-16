from BaseCILToMIPSVisitor import *
from utils import visitor
import cil_ast as cil

class CILToMIPSVisitor(BaseCILToMIPSVisitor):
    @visitor.on('node')
    def visit(self, node):
        pass

    @visitor.when(cil.ProgramNode)
    def visit(self, node):
        #.TYPE
        for type_ in node.dottypes:
            self.visit(type_)
        self.save_meth_addr(node.dotcode)
        self.data_code.append(f"type_Void: .asciiz \"Void\"")
        self.save_types_addr(node.dottypes)
        #.DATA
        for data in node.dotdata:
            self.visit(data)
        #.CODE
        for code in node.dotcode:
            self.visit(code)
        self.initialize_runtime_errors()
        return self.data_code, self.code

    @visitor.when(cil.TypeNode)
    def visit(self, node):
        self.obj_table.add_entry(node.name, node.methods, node.attributes)
        self.data_code.append(f"type_{node.name}: .asciiz \"{node.name}\"")

    @visitor.when(cil.DataNode)
    def visit(self, node):
        self.data_code.append(f"{node.name}: .asciiz \"{node.value}\"")

    @visitor.when(cil.FunctionNode)
    def visit(self, node):
        self.code.append('')
        self.code.append(f'{node.name}:')
        self.locals = 0
        self.code.append('# Gets the params from the stack')
        self.code.append(f'move $fp, $sp')
        n = len(node.params)
        for i, param in enumerate(node.params, 1):
            self.visit(param, i, n)
        self.code.append('# Gets the frame pointer from the stack')
        for i, var in enumerate(node.localvars, len(node.params)):
            self.visit(var, i)
        self.locals = len(node.params) + len(node.localvars)
        blocks = self.get_basic_blocks(node.instructions)
        self.next_use = self.construct_next_use(blocks)
        for block in blocks:
            self.block = block
            for inst in block:
                self.inst = inst
                self.get_reg(inst)
                self.visit(inst)
            inst = block[-1]
            if not (isinstance(inst, cil.GoToNode) or isinstance(inst, cil.IfGoToNode) or isinstance(inst, cil.ReturnNode) \
                or isinstance(inst, cil.CallNode) or isinstance(inst, cil.VCallNode)):
                self.empty_registers()

    @visitor.when(cil.ParamNode)
    def visit(self, node, idx, length):        
        self.symbol_table.insert_name(node.name)
        self.var_address[node.name] = self.get_type(node.type)
        self.code.append(f'# Pops the register with the param value {node.name}')
        self.code.append('addiu $fp, $fp, 4') 
        self.addr_desc.insert_var(node.name, length-idx)            

    @visitor.when(cil.LocalNode)
    def visit(self, node, idx):
        self.symbol_table.insert_name(node.name)
        self.addr_desc.insert_var(node.name, idx)
        self.code.append(f'# Updates stack pointer pushing {node.name} to the stack')
        self.code.append(f'addiu $sp, $sp, -4')

    @visitor.when(cil.AssignNode)
    def visit(self, node):
        rdest = self.addr_desc.get_var_reg(node.dest)
        self.code.append(f'# Moving {node.source} to {node.dest}')
        if self.is_variable(node.source):
            rsrc = self.addr_desc.get_var_reg(node.source)
            self.code.append(f'move ${rdest}, ${rsrc}') 
            self.var_address[node.dest] = self.var_address[node.source]
        elif self.is_int(node.source):
            self.code.append(f'li ${rdest}, {node.source}')
            self.var_address[node.dest] = AddrType.INT
        self.save_var_code(node.dest)

    @visitor.when(cil.PlusNode)
    def visit(self, node):
        rdest = self.addr_desc.get_var_reg(node.dest)
        self.code.append(f'# {node.dest} <- {node.left} + {node.right}')
        if self.is_variable(node.left):
            rleft = self.addr_desc.get_var_reg(node.left)
            if self.is_variable(node.right):
                rright = self.addr_desc.get_var_reg(node.right)
                self.code.append(f"add ${rdest}, ${rleft}, ${rright}")
            elif self.is_int(node.right):
                self.code.append(f"addi ${rdest}, ${rleft}, {node.right}")
        elif self.is_int(node.left):
            if self.is_int(node.right):
                self.code.append(f"li ${rdest}, {node.left + node.right}")
            elif self.is_variable(node.right):
                rright = self.addr_desc.get_var_reg(node.right)
                self.code.append(f"addi ${rdest}, ${rright}, {node.left}")
        self.var_address[node.dest] = AddrType.INT

    @visitor.when(cil.MinusNode)
    def visit(self, node):
        rdest = self.addr_desc.get_var_reg(node.dest)
        self.code.append(f'# {node.dest} <- {node.left} - {node.right}')
        if self.is_variable(node.left):
            rleft = self.addr_desc.get_var_reg(node.left)
            if self.is_variable(node.right):
                rright = self.addr_desc.get_var_reg(node.right)
                self.code.append(f"sub ${rdest}, ${rleft}, ${rright}")
            elif self.is_int(node.right):
                self.code.append(f"addi ${rdest}, ${rleft}, -{node.right}")
        elif self.is_int(node.left):
            if self.is_int(node.right):
                self.code.append(f"li ${rdest}, {node.left-node.right}")
            elif self.is_variable(node.right):
                rright = self.addr_desc.get_var_reg(node.right)
                self.code.append(f"sub $t9, $zero, {rright}")
                self.code.append(f"addi ${rdest}, {node.left}, $t9")
        self.var_address[node.dest] = AddrType.INT

    @visitor.when(cil.StarNode)
    def visit(self, node):
        self.code.append(f'# {node.dest} <- {node.left} * {node.right}')
        rdest = self.addr_desc.get_var_reg(node.dest)
        if self.is_int(node.left) and self.is_int(node.right):
            self.code.append(f"li ${rdest}, {node.left*node.right}")
        else:
            if self.is_variable(node.left):
                rleft = self.addr_desc.get_var_reg(node.left)
                if self.is_variable(node.right):
                    rright = self.addr_desc.get_var_reg(node.right)
                elif self.is_int(node.right):
                    self.code.append(f"li $t9, {node.right}")
                    rright = 't9'
            elif self.is_int(node.left):
                rright = self.addr_desc.get_var_reg(node.right)
                self.code.append(f"li $t9, {node.left}")
                rleft = 't9'
            self.code.append(f"mult ${rleft}, ${rright}")
            self.code.append(f"mflo ${rdest}")
        self.var_address[node.dest] = AddrType.INT
        
    @visitor.when(cil.DivNode)
    def visit(self, node):
        self.code.append(f'# {node.dest} <- {node.left} / {node.right}')
        rdest = self.addr_desc.get_var_reg(node.dest)
        if self.is_int(node.left) and self.is_int(node.right):
            try:
                self.code.append(f"li ${rdest}, {node.left/node.right}")
            except ZeroDivisionError:
                self.code.append('la $a0, zero_error')
                self.code.append('j .raise')
        else:
            if self.is_variable(node.left):
                rleft = self.addr_desc.get_var_reg(node.left)
                if self.is_variable(node.right):
                    rright = self.addr_desc.get_var_reg(node.right)
                elif self.is_int(node.right):
                    self.code.append(f"li $t9, {node.right}")
                    rright = 't9'
            elif self.is_int(node.left):
                rright = self.addr_desc.get_var_reg(node.right)
                self.code.append(f"li $t9, {node.left}")
                rleft = 't9'
            self.code.append('la $a0, zero_error')
            self.code.append(f'beqz ${rright}, .raise')
            self.code.append(f"div ${rleft}, ${rright}")
            self.code.append(f"mflo ${rdest}")
        self.var_address[node.dest] = AddrType.INT

    @visitor.when(cil.LessNode)
    def visit(self, node):
        self.code.append(f'# {node.dest} <- {node.left} < {node.right}')
        rdest = self.addr_desc.get_var_reg(node.dest)
        if self.is_variable(node.left):
            rleft = self.addr_desc.get_var_reg(node.left)
            if self.is_variable(node.right):
                rright = self.addr_desc.get_var_reg(node.right)
                self.code.append(f"slt ${rdest}, ${rleft}, ${rright}")
            elif self.is_int(node.right):
                self.code.append(f"li $t9, {node.right}")
                self.code.append(f"slt ${rdest}, ${rleft}, $t9")
        elif self.is_int(node.left):
            if self.is_int(node.right):
                self.code.append(f"li ${rdest}, {int(node.left < node.right)}")
            elif self.is_variable(node.right):
                rright = self.addr_desc.get_var_reg(node.right)
                self.code.append(f"li $t9, {node.left}")
                self.code.append(f"slt ${rdest}, $t9, ${rright}")
        self.var_address[node.dest] = AddrType.BOOL

    @visitor.when(cil.LessEqualNode)
    def visit(self, node):
        self.code.append(f'# {node.dest} <- {node.left} <= {node.right}')
        rdest = self.addr_desc.get_var_reg(node.dest)
        if self.is_variable(node.left):
            rleft = self.addr_desc.get_var_reg(node.left)
            if self.is_variable(node.right):
                rright = self.addr_desc.get_var_reg(node.right)
                self.code.append(f"sle ${rdest}, ${rleft}, ${rright}")
            elif self.is_int(node.right):
                self.code.append(f"li $t9, {node.right}")
                self.code.append(f"sle ${rdest}, ${rleft}, $t9")
        elif self.is_int(node.left):
            if self.is_int(node.right):
                self.code.append(f"li ${rdest}, {int(node.left <= node.right)}")
            elif self.is_variable(node.right):
                rright = self.addr_desc.get_var_reg(node.right)
                self.code.append(f"li $t9, {node.left}")
                self.code.append(f"sle ${rdest}, $t9, ${rright}")
        self.var_address[node.dest] = AddrType.BOOL

    @visitor.when(cil.EqualNode)
    def visit(self, node):
        self.code.append(f'# {node.dest} <- {node.left} = {node.right}')
        if self.is_variable(node.left) and self.is_variable(node.right) and self.var_address[node.left] == AddrType.STR and self.var_address[node.right] == AddrType.STR:
            self.compare_strings(node)
        else:
            rdest = self.addr_desc.get_var_reg(node.dest)
            if self.is_variable(node.left):
                rleft = self.addr_desc.get_var_reg(node.left)
                if self.is_variable(node.right):
                    rright = self.addr_desc.get_var_reg(node.right)
                    self.code.append(f"seq ${rdest}, ${rleft}, ${rright}")
                elif self.is_int(node.right):
                    self.code.append(f"li $t9, {node.right}")
                    self.code.append(f"seq ${rdest}, ${rleft}, $t9")
            elif self.is_int(node.left):
                if self.is_int(node.right):
                    self.code.append(f"li ${rdest}, {int(node.left == node.right)}")
                elif self.is_variable(node.right):
                    rright = self.addr_desc.get_var_reg(node.right)
                    self.code.append(f"li $t9, {node.left}")
                    self.code.append(f"seq ${rdest}, $t9, ${rright}")
            self.var_address[node.dest] = AddrType.BOOL

    @visitor.when(cil.NotNode)
    def visit(self, node):
        rdest = self.addr_desc.get_var_reg(node.dest)
        rsrc = self.save_to_register(node.expr)
        self.code.append(f'# {node.dest} <- not {node.expr}')
        self.code.append(f'beqz ${rsrc}, false_{self.loop_idx}')
        self.code.append(f'li ${rdest}, 0')
        self.code.append(f'j end_{self.loop_idx}')
        self.code.append(f'false_{self.loop_idx}:')
        self.code.append(f'li ${rdest}, 1')
        self.code.append(f'end_{self.loop_idx}:')
        self.loop_idx += 1
        self.var_address[node.dest] = AddrType.BOOL

    @visitor.when(cil.GetAttrNode)
    def visit(self, node):
        self.code.append(f'# {node.dest} <- GET {node.obj} . {node.attr}')
        rdest = self.addr_desc.get_var_reg(node.dest)
        self.var_address[node.dest] = self.get_type(node.attr_type)
        rsrc = self.addr_desc.get_var_reg(node.obj)
        attr_offset = 4*self.get_attr_offset(node.attr, node.type_name)
        self.code.append(f'lw ${rdest}, {attr_offset}(${rsrc})')

    @visitor.when(cil.SetAttrNode)
    def visit(self, node):
        self.code.append(f'# {node.obj} . {node.attr} <- SET {node.value}')
        rdest = self.addr_desc.get_var_reg(node.obj)
        attr_offset = 4*self.get_attr_offset(node.attr, node.type_name)
        if self.is_variable(node.value):
            rsrc = self.addr_desc.get_var_reg(node.value)
        elif self.is_int(node.value):
            self.code.append(f'li $t9, {node.value}')
            rsrc = 't9'
        elif self.is_void(node.value):
            self.code.append(f'la $t9, type_{VOID_NAME}')
            rsrc = 't9'
        self.code.append(f'sw ${rsrc}, {attr_offset}(${rdest})')

    @visitor.when(cil.AllocateNode)
    def visit(self, node):
        rdest = self.addr_desc.get_var_reg(node.dest)
        self.var_address[node.dest] = AddrType.REF
        self.code.append('# Syscall to allocate memory of the object entry in heap')
        self.code.append('li $v0, 9')
        size = 4*self.obj_table.size_of_entry(node.type)
        self.code.append(f'li $a0, {size}')
        self.code.append('syscall')
        addrs_stack = self.addr_desc.get_var_addr(node.dest)
        self.code.append('# Loads the name of the variable and saves the name like the first field')
        self.code.append(f'la $t9, type_{node.type}')
        self.code.append(f'sw $t9, 0($v0)')
        self.code.append(f'# Saves the size of the node')
        self.code.append(f'li $t9, {size}')
        self.code.append(f'sw $t9, 4($v0)')
        self.code.append(f'move ${rdest}, $v0')   
        idx = self.types.index(node.type)
        self.code.append('# Adding Type Info addr')
        self.code.append('la $t8, types')
        self.code.append(f'lw $v0, {4*idx}($t8)')
        self.code.append(f'sw $v0, 8(${rdest})')

    @visitor.when(cil.TypeOfNode)
    def visit(self, node):
        rdest = self.addr_desc.get_var_reg(node.dest)
        self.code.append(f'# {node.dest} <- Type of {node.obj}')
        if self.is_variable(node.obj):
            rsrc = self.addr_desc.get_var_reg(node.obj)
            if self.var_address[node.obj] == AddrType.REF:
                self.code.append(f'lw ${rdest}, 0(${rsrc})')
            elif self.var_address[node.obj] == AddrType.STR:
                self.code.append(f'la ${rdest}, type_String')
            elif self.var_address[node.obj] == AddrType.INT:
                self.code.append(f'la ${rdest}, type_Int')
            elif self.var_address[node.obj] == AddrType.BOOL:
                self.code.append(f'la ${rdest}, type_Bool')
        elif self.is_int(node.obj):
            self.code.append(f'la ${rdest}, type_Int')
        self.var_address[node.dest] = AddrType.STR

    @visitor.when(cil.LabelNode)
    def visit(self, node):
        self.code.append(f'{node.label}:')

    @visitor.when(cil.GoToNode)
    def visit(self, node):
        self.empty_registers()
        self.code.append(f'j {node.label}')

    @visitor.when(cil.IfGoToNode)
    def visit(self, node):
        reg = self.save_to_register(node.cond)
        self.code.append(f'# If {node.cond} goto {node.label}')
        self.empty_registers()
        self.code.append(f'bnez ${reg}, {node.label}')

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
        self.code.append('# Gets in a0 the actual direction of the dispatch table')
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



