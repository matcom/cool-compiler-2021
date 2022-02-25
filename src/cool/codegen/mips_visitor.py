from .mipsgen import BaseMips
from ..utils import visitor
from .utils.tools import SymbolTable, AddrDescriptor, RegisterDescriptor, AddrType
from ..semantic.helpers import VariableInfo
from ..semantic.types import VOID_NAME
from .utils.ast_cil import *


class MipsVisitor(BaseMips):
    @visitor.on('node')
    def visit(self, node):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node: ProgramNode):
        self.code.append('# debug: ProgramNode')
        for type_ in node.type_node:
            self.visit(type_)

        self.save_meth_addr(node.func_node)
        self.data_code.append(f"type_Void: .asciiz \"Void\"")
        self.save_types_addr(node.type_node)

        for d in node.data:
            self.visit(d)

        for code in node.func_node:
            self.visit(code)

        self.get_runtime_errors()

        return self.data_code, self.code

    @visitor.when(TypeNode)
    def visit(self, node: TypeNode):
        self.code.append('# debug: TypeNode')
        self.obj_table.add_entry(node.name, node.methods, node.attributes)
        self.data_code.append(
            f"type_{node.name}: .asciiz \"{node.name}\"")

    @visitor.when(DataNode)
    def visit(self, node: DataNode):
        self.code.append('# debug: DataNode')
        self.data_code.append(f"{node.name}: .asciiz \"{node.value}\"")

    @visitor.when(FunctionNode)
    def visit(self, node: FunctionNode):
        self.code.append('# debug: FunctionNode')
        self.code.append('')
        self.code.append(f'{node.name}:')
        self.locals = 0
        self.code.append('# Gets the params from the stack')
        self.code.append(f'move $fp, $sp')  # gets the frame pointer from the stack
        n = len(node.params)
        for i, param in enumerate(node.params, 1):  # gets the params from the stack
            self.visit(param, i, n)
        self.code.append('# Gets the frame pointer from the stack')
        for i, var in enumerate(node.localvars, len(node.params)):
            self.visit(var, i)
        self.locals = len(node.params) + len(node.localvars)
        blocks = self.get_basic_blocks(node.instructions)
        self.next_use = self.next_use(blocks)

        for block in blocks:
            self.block = block
            for inst in block:
                self.inst = inst
                self.get_reg(inst)
                self.visit(inst)
            inst = block[-1]
            if not (isinstance(inst, GotoNode) or isinstance(inst, GotoIfNode) or isinstance(inst, ReturnNode) \
                    or isinstance(inst, StaticCallNode) or isinstance(inst, DynamicCallNode)):
                self.empty_registers()

    @visitor.when(ParamNode)
    def visit(self, node: ParamNode, idx: int, length: int):
        self.code.append('# debug: ParamNode')
        self.symbol_table.insert_name(node.name)
        self.var_address[node.name] = self.get_type(node.type)
        self.code.append(f'# Pops the register with the param value {node.name}')
        self.code.append('addiu $fp, $fp, 4')
        self.addr_desc.insert_var(node.name, length - idx)

    @visitor.when(LocalNode)
    def visit(self, node: LocalNode, idx: int):
        self.code.append('# debug: LocalNode')
        self.symbol_table.insert_name(node.name)
        self.addr_desc.insert_var(node.name, idx)
        self.code.append(f'# Updates stack pointer pushing {node.name} to the stack')
        self.code.append(f'addiu $sp, $sp, -4')

    @visitor.when(AssignNode)
    def visit(self, node: AssignNode):
        self.code.append('# debug: AssignNode')
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

    @visitor.when(NotNode)
    def visit(self, node: NotNode):
        self.code.append('#debug: NotNode')
        rdest = self.addr_desc.get_var_reg(node.dest)
        rsrc = self.save_to_register(node.expr)
        self.code.append(f'# {node.dest} <- ~{node.expr}')
        self.code.append(f'not ${rdest}, ${rsrc}')
        self.code.append(f'addi ${rdest}, ${rdest}, 1')
        self.var_address[node.dest] = AddrType.INT

    @visitor.when(LogicalNotNode)
    def visit(self, node: LogicalNotNode):
        self.code.append('#debug: LogicalNotNode')
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

    @visitor.when(PlusNode)
    def visit(self, node: PlusNode):
        self.code.append('#debug: PlusNode')
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

    @visitor.when(MinusNode)
    def visit(self, node: MinusNode):
        self.code.append('#debug: MinusNode')
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
                self.code.append(f"li ${rdest}, {node.left - node.right}")
            elif self.is_variable(node.right):
                rright = self.addr_desc.get_var_reg(node.right)
                self.code.append(f"sub $t9, $zero, {rright}")
                self.code.append(f"addi ${rdest}, {node.left}, $t9")
        self.var_address[node.dest] = AddrType.INT

    @visitor.when(StarNode)
    def visit(self, node: StarNode):
        self.code.append('#debug: StartNode')
        self.code.append(f'# {node.dest} <- {node.left} * {node.right}')
        self._code_to_mult_div(node, op='mult', func_op=lambda x, y: x * y)

    @visitor.when(DivNode)
    def visit(self, node: DivNode):
        self.code.append('#debug: DivNode')
        self.code.append(f'# {node.dest} <- {node.left} / {node.right}')
        self._code_to_mult_div(node, op='div', func_op=lambda x, y: int(x / y))

    def _code_to_mult_div(self, node, op: str, func_op):
        rdest = self.addr_desc.get_var_reg(node.dest)
        if self.is_int(node.left) and self.is_int(node.right):
            try:
                self.code.append(f"li ${rdest}, {func_op(node.left, node.right)}")
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
                # right es una variable porque falló el primer if
                rright = self.addr_desc.get_var_reg(node.right)
                self.code.append(f"li $t9, {node.left}")
                rleft = 't9'
            if op == 'div':
                self.code.append('la $a0, zero_error')
                self.code.append(f'beqz ${rright}, .raise')
            self.code.append(f"{op} ${rleft}, ${rright}")
            self.code.append(f"mflo ${rdest}")
        self.var_address[node.dest] = AddrType.INT

    @visitor.when(LessNode)
    def visit(self, node: LessNode):
        self.code.append('#debug: LessNode')
        self.code.append(f'# {node.dest} <- {node.left} < {node.right}')
        self._code_to_comp(node, 'slt', lambda x, y: x < y)

    @visitor.when(LessEqNode)
    def visit(self, node: LessEqNode):
        self.code.append('#debug: LessEqNode')
        self.code.append(f'# {node.dest} <- {node.left} <= {node.right}')
        self._code_to_comp(node, 'sle', lambda x, y: x <= y)

    @visitor.when(EqualNode)
    def visit(self, node: EqualNode):
        self.code.append('#debug: EqualNode')
        self.code.append(f'# {node.dest} <- {node.left} = {node.right}')
        if self.is_variable(node.left) and self.is_variable(node.right) and self.var_address[
            node.left] == AddrType.STR and self.var_address[node.right] == AddrType.STR:
            self.compare_strings(node)
        else:
            self._code_to_comp(node, 'seq', lambda x, y: x == y)

    def _code_to_comp(self, node, op, func_op):
        rdest = self.addr_desc.get_var_reg(node.dest)
        if self.is_variable(node.left):
            rleft = self.addr_desc.get_var_reg(node.left)
            if self.is_variable(node.right):
                rright = self.addr_desc.get_var_reg(node.right)
                self.code.append(f"{op} ${rdest}, ${rleft}, ${rright}")
            elif self.is_int(node.right):
                self.code.append(f"li $t9, {node.right}")
                self.code.append(f"{op} ${rdest}, ${rleft}, $t9")
        elif self.is_int(node.left):
            if self.is_int(node.right):
                self.code.append(f"li ${rdest}, {int(func_op(node.left, node.right))}")
            elif self.is_variable(node.right):
                rright = self.addr_desc.get_var_reg(node.right)
                self.code.append(f"li $t9, {node.left}")
                self.code.append(f"{op} ${rdest}, $t9, ${rright}")
        self.var_address[node.dest] = AddrType.BOOL

    @visitor.when(GetAttribNode)
    def visit(self, node: GetAttribNode):
        self.code.append('#debug: GetAttribNode')
        self.code.append(f'# {node.dest} <- GET {node.obj} . {node.attr}')
        rdest = self.addr_desc.get_var_reg(node.dest)
        self.var_address[node.dest] = self.get_type(node.attr_type)
        rsrc = self.addr_desc.get_var_reg(node.obj)
        attr_offset = 4 * self.get_attr_offset(node.attr, node.type_name)
        self.code.append(f'lw ${rdest}, {attr_offset}(${rsrc})')

    @visitor.when(SetAttribNode)
    def visit(self, node: SetAttribNode):
        self.code.append('#debug: SetAttribNode')
        self.code.append(f'# {node.obj} . {node.attr} <- SET {node.value}')
        rdest = self.addr_desc.get_var_reg(node.obj)
        attr_offset = 4 * self.get_attr_offset(node.attr, node.type_name)
        if self.is_variable(node.value):
            rsrc = self.addr_desc.get_var_reg(node.value)
        elif self.is_int(node.value):
            self.code.append(f'li $t9, {node.value}')
            rsrc = 't9'
        elif self.is_void(node.value):
            self.code.append(f'la $t9, type_{VOID_NAME}')
            rsrc = 't9'
        self.code.append(f'sw ${rsrc}, {attr_offset}(${rdest})')  # saves the new value in the attr offset

    @visitor.when(AllocateNode)
    def visit(self, node: AllocateNode):
        self.code.append('#debug: AllocateNode')
        rdest = self.addr_desc.get_var_reg(node.dest)
        size = 4 * self.obj_table.size_of_entry(node.type)
        self.var_address[node.dest] = AddrType.REF

        self.code.append('# Syscall to allocate memory of the object entry in heap')
        self.code.append('li $v0, 9')
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
        self.code.append(f'lw $v0, {4 * idx}($t8)')
        self.code.append(f'sw $v0, 8(${rdest})')

    @visitor.when(TypeOfNode)
    def visit(self, node: TypeOfNode):
        self.code.append('#debug: TypeOfNode')
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

    @visitor.when(LabelNode)
    def visit(self, node: LabelNode):
        self.code.append('#debug: LabelNode')
        self.code.append(f'{node.label}:')

    @visitor.when(GotoNode)
    def visit(self, node: GotoNode):
        self.code.append('#debug: GotoNode')
        self.empty_registers()
        self.code.append(f'j {node.label}')

    @visitor.when(GotoIfNode)
    def visit(self, node: GotoIfNode):
        self.code.append('#debug: GotoIfNode')
        reg = self.save_to_register(node.cond)
        self.code.append(f'# If {node.cond} goto {node.label}')
        self.empty_registers()
        self.code.append(f'bnez ${reg}, {node.label}')

    @visitor.when(GotoIfFalseNode)
    def visit(self, node: GotoIfNode):
        self.code.append('#debug: GotoIfFalseNode')
        reg = self.save_to_register(node.cond)
        self.code.append(f'# If not {node.cond} goto {node.label}')
        self.empty_registers()
        self.code.append(f'beqz ${reg}, {node.label}')

    @visitor.when(StaticCallNode)
    def visit(self, node: StaticCallNode):
        self.code.append('#debug: StaticCallNode')
        function = self.dispatch_table.find_full_name(node.type, node.function)
        self.code.append(f'# Static Dispatch of the method {node.function}')
        self._code_to_function_call(node.args, function, node.dest)

        self.var_address[node.dest] = self.get_type(node.return_type)

    @visitor.when(DynamicCallNode)
    def visit(self, node: DynamicCallNode):
        self.code.append('#debug: DynamicCallNode')
        self.code.append('# Find the actual name in the dispatch table')
        reg = self.addr_desc.get_var_reg(node.obj)
        self.code.append('# Gets in a0 the actual direction of the dispatch table')
        self.code.append(f'lw $t9, 8(${reg})')
        self.code.append('lw $a0, 8($t9)')
        function = self.dispatch_table.find_full_name(node.type, node.method)
        index = 4 * self.dispatch_table.get_offset(node.type, function) + 4
        self.code.append(f'# Saves in t8 the direction of {function}')
        self.code.append(f'lw $t8, {index}($a0)')
        self._code_to_function_call(node.args, '$t8', node.dest, function)

        self.var_address[node.dest] = self.get_type(node.return_type)

    def _code_to_function_call(self, args, function, dest, function_name=None):
        self.push_register('fp')
        self.push_register('ra')
        self.code.append('# Push the arguments to the stack')
        for arg in reversed(args):
            self.visit(arg)
        self.code.append('# Empty all used registers and saves them to memory')
        self.empty_registers()
        self.code.append('# This function will consume the arguments')
        self.code.append(f'jal {function}')
        self.code.append('# Pop ra register of return function of the stack')
        self.pop_register('ra')
        self.code.append('# Pop fp register from the stack')
        self.pop_register('fp')
        if dest is not None:
            self.get_reg_var(dest)
            rdest = self.addr_desc.get_var_reg(dest)
            self.code.append('# saves the return value')
            self.code.append(f'move ${rdest}, $v0')

    @visitor.when(ArgNode)
    def visit(self, node: ArgNode):
        self.code.append('#debug: ArgNode')
        self.code.append('# The rest of the arguments are push into the stack')
        if self.is_variable(node.dest):
            self.get_reg_var(node.dest)
            reg = self.addr_desc.get_var_reg(node.dest)
            self.code.append(f'sw ${reg}, ($sp)')
        elif self.is_int(node.dest):
            self.code.append(f'li $t9, {node.dest}')
            self.code.append(f'sw $t9, ($sp)')
        self.code.append('addiu $sp, $sp, -4')

    @visitor.when(ReturnNode)
    def visit(self, node: ReturnNode):
        self.code.append('#debug: ReturnNode')
        if self.is_variable(node.value):
            rdest = self.addr_desc.get_var_reg(node.value)
            self.code.append(f'move $v0, ${rdest}')
        elif self.is_int(node.value):
            self.code.append(f'li $v0, {node.value}')
        self.code.append('# Empty all used registers and saves them to memory')
        self.empty_registers()
        self.code.append('# Removing all locals from stack')
        self.code.append(f'addiu $sp, $sp, {self.locals * 4}')
        self.code.append(f'jr $ra')
        self.code.append('')

    @visitor.when(LoadNode)
    def visit(self, node: LoadNode):
        self.code.append('#debug: LoadNode')
        rdest = self.addr_desc.get_var_reg(node.dest)
        self.code.append(f'# Saves in {node.dest} {node.msg}')
        self.var_address[node.dest] = AddrType.STR
        self.code.append(f'la ${rdest}, {node.msg}')

    @visitor.when(LengthNode)
    def visit(self, node: LengthNode):
        self.code.append('#debug: LengthNode')
        rdest = self.addr_desc.get_var_reg(node.dest)
        reg = self.addr_desc.get_var_reg(node.arg)
        loop = f'loop_{self.loop_idx}'
        end = f'end_{self.loop_idx}'
        self.code.append(f'move $t8, ${reg}')
        self.code.append('# Get length of a string')
        self.code.append(f'{loop}:')
        self.code.append(f'lb $t9, 0($t8)')
        self.code.append(f'beq $t9, $zero, {end}')
        self.code.append(f'addi $t8, $t8, 1')
        self.code.append(f'j {loop}')
        self.code.append(f'{end}:')
        self.code.append(f'sub ${rdest}, $t8, ${reg}')
        self.loop_idx += 1

    @visitor.when(ConcatNode)
    def visit(self, node: ConcatNode):
        self.code.append('#debug: ConcatFNode')
        rdest = self.addr_desc.get_var_reg(node.dest)
        self.code.append('# Allocating memory for the buffer')
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
            self.code.append('# Concatenate second string on result buffer')
            self.code.append(f'move $a0, ${rsrc2}')
            self.code.append(f'move $a1, $v0')
            self.code.append('jal strcopier')
        self.code.append('sb $0, 0($v0)')
        self.pop_register('ra')
        self.code.append(f'j finish_{self.loop_idx}')

        if self.first_defined['strcopier']:
            self.code.append('# Definition of strcopier')
            self.code.append('strcopier:')
            self.code.append('# In a0 is the source and in a1 is the destination')
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

    @visitor.when(SubstringNode)
    def visit(self, node: SubstringNode):
        self.code.append('#debug: SubstringNode')
        rdest = self.addr_desc.get_var_reg(node.dest)
        self.code.append('# Allocating memory for the buffer')
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

        self.code.append("# Getting the substring of a node")
        start = f'start_{self.loop_idx}'
        error = f'error_{self.loop_idx}'
        end_lp = f'end_len_{self.loop_idx}'
        self.code.append('# Move to the first position in the string')
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
        self.code.append('# Saving dest to iterate over him')
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

    @visitor.when(OutStringNode)
    def visit(self, node: OutStringNode):
        self.code.append('#debug: OutStringNode')
        reg = self.addr_desc.get_var_reg(node.value)
        self.code.append('# Printing a string')
        self.code.append('li $v0, 4')
        self.code.append(f'move $a0, ${reg}')
        self.code.append('syscall')

    @visitor.when(OutIntNode)
    def visit(self, node: OutIntNode):
        self.code.append('#debug: OutIntNode')
        if self.is_variable(node.value):
            reg = self.addr_desc.get_var_reg(node.value)
        elif self.is_int(node.value):
            reg = 't8'
            self.code.append(f'li $t8, ${node.value}')

        self.code.append('# Printing an int')
        self.code.append('li $v0, 1')
        self.code.append(f'move $a0, ${reg}')
        self.code.append('syscall')

    @visitor.when(ReadStringNode)
    def visit(self, node: ReadStringNode):
        self.code.append('#debug: ReadStringNode')
        rdest = self.addr_desc.get_var_reg(node.dest)
        self.code.append('# Allocating memory for the buffer')
        self.code.append('li $a0, 356')
        self.code.append('li $v0, 9')
        self.code.append('syscall')
        self.code.append(f'move ${rdest}, $v0')
        self.code.append('# Reading a string')
        var = self.save_reg_if_occupied('a1')
        self.code.append('# Putting buffer in a0')
        self.code.append(f'move $a0, ${rdest}')  # Get length of the string
        self.code.append('# Putting length of string in a1')
        self.code.append(f'li $a1, 356')
        self.code.append('li $v0, 8')
        self.code.append('syscall')
        start = f'start_{self.loop_idx}'
        end = f'end_{self.loop_idx}'

        self.code.append(f'move $t9, ${rdest}')
        self.code.append(f'{start}:')
        self.code.append('lb $t8, 0($t9)')
        self.code.append(f"beqz $t8, {end}")
        self.code.append('add $t9, $t9, 1')
        self.code.append(f'j {start}')
        self.code.append(f'{end}:')
        self.code.append('addiu $t9, $t9, -1')
        self.code.append('sb $0, ($t9)')
        self.loop_idx += 1
        self.load_var_if_occupied(var)

    @visitor.when(ReadIntNode)
    def visit(self, node: ReadIntNode):
        self.code.append('#debug: ReadIntNode')
        rdest = self.addr_desc.get_var_reg(node.dest)
        self.code.append('# Reading a int')
        self.code.append('li $v0, 5')
        self.code.append('syscall')
        self.code.append(f'move ${rdest}, $v0')

    @visitor.when(ExitNode)
    def visit(self, node: ExitNode):
        self.code.append('#debug: ExitNode')
        self.code.append('# Exiting the program')
        if self.is_variable(node.value):
            reg = self.addr_desc.get_var_reg(node.value)
        elif self.is_int(node.value):
            reg = 't8'
            self.code.append(f'li $t8, {node.value}')

        rself = self.addr_desc.get_var_reg(node.classx)
        if self.var_address[node.classx] == AddrType.REF:
            self.code.append('# Printing abort message')
            self.code.append('li $v0, 4')
            self.code.append(f'la $a0, abort_msg')
            self.code.append('syscall')
            self.code.append('li $v0, 4')
            self.code.append(f'lw $a0, 0(${rself})')
            self.code.append('syscall')
            self.code.append('li $v0, 4')
            self.code.append(f'la $a0, new_line')
            self.code.append('syscall')

        self.code.append('li $v0, 17')
        self.code.append(f'move $a0, ${reg}')
        self.code.append('syscall')

    @visitor.when(CopyNode)
    def visit(self, node: CopyNode):
        self.code.append('#debug: CopyNode')

        rdest = self.addr_desc.get_var_reg(node.dest)
        rsrc = self.addr_desc.get_var_reg(node.source)

        self.code.append(f'lw $t9, 4(${rsrc})')
        self.code.append('# Syscall to allocate memory of the object entry in heap')
        self.code.append('li $v0, 9')
        self.code.append(f'move $a0, $t9')
        self.code.append('syscall')
        self.code.append(f'move ${rdest}, $v0')
        self.code.append('# Loop to copy every field of the previous object')
        self.code.append('# t8 the register to loop')
        self.code.append('li $t8, 0')
        self.code.append(f'loop_{self.loop_idx}:')
        self.code.append('# In t9 is stored the size of the object')
        self.code.append(f'bge $t8, $t9, exit_{self.loop_idx}')
        self.code.append(f'lw $a0, (${rsrc})')
        self.code.append('sw $a0, ($v0)')
        self.code.append('addi $v0, $v0, 4')
        self.code.append(f'addi ${rsrc}, ${rsrc}, 4')
        self.code.append('# Increase loop counter')
        self.code.append('addi $t8, $t8, 4')
        self.code.append(f'j loop_{self.loop_idx}')
        self.code.append(f'exit_{self.loop_idx}:')
        self.loop_idx += 1

    @visitor.when(ConformsNode)
    def visit(self, node: ConformsNode):
        self.code.append('#debug: ConformsNode')
        rdest = self.addr_desc.get_var_reg(node.dest)
        if self.is_variable(node.expr):
            rsrc = self.addr_desc.get_var_reg(node.expr)
            if self.var_address[node.expr] == AddrType.REF:
                self.conforms_to(rsrc, rdest, node.type)
            elif self.var_address[node.expr] == AddrType.STR:
                self.value_conforms_to_obj(rdest, 'String', node.type)
            elif self.var_address[node.expr] == AddrType.INT:
                self.value_conforms_to_obj(rdest, 'Int', node.type)
            elif self.var_address[node.expr] == AddrType.BOOL:
                self.value_conforms_to_obj(rdest, 'Bool', node.type)
        elif self.is_int(node.expr):
            self.value_conforms_to_obj(rdest, 'Int', node.type)

    @visitor.when(ErrorNode)
    def visit(self, node: ErrorNode):
        self.code.append('#debug: ErrorNode')
        self.code.append(f'la $a0, {node.type}')
        self.code.append('j .raise')

    @visitor.when(VoidConstantNode)
    def visit(self, node: VoidConstantNode):
        self.code.append('#debug: VoidConstantNode')
        rdest = self.addr_desc.get_var_reg(node.out)
        self.code.append('# Initialize void node')
        self.code.append(f'li $a0, 4')
        self.code.append('li $v0, 9')
        self.code.append('syscall')
        self.code.append('# Loads the name of the variable and saves the name like the first field')
        self.code.append(f'la $t9, type_{VOID_NAME}')
        self.code.append('sw $t9, 0($v0)')
        self.code.append(f'move ${rdest}, $v0')
        self.var_address[node.obj] = AddrType.REF

    @visitor.when(BoxingNode)
    def visit(self, node: BoxingNode):
        self.code.append('#debug: BoxingNode')
        rdest = self.addr_desc.get_var_reg(node.dest)
        self.code.append('# Initialize new node')
        self.code.append('li $a0, 12')
        self.code.append('li $v0, 9')
        self.code.append('syscall')
        self.code.append(f'la $t9, type_{node.type}')
        self.code.append('sw $t9, 0($v0)')
        self.code.append('li $t9, 12')
        self.code.append('sw $t9, 4($v0)')
        self.code.append(f'move ${rdest}, $v0')
        self.code.append('# Saving the methods of object')
        idx = self.types.index('Object')
        self.code.append('# Adding Type Info addr')
        self.code.append('la $t8, types')
        self.code.append(f'lw $v0, {4 * idx}($t8)')
        self.code.append(f'sw $v0, 8(${rdest})')
        self.var_address[node.dest] = AddrType.REF
