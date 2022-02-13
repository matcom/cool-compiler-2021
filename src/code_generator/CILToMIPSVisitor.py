from codegen.BaseCILToMIPSVisitor import *
from utils import visitor
import cil_ast as cil

class COOLToCILVisitor(BaseCILToMIPSVisitor):
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

#this works with a address that I need to do like the Micro
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
        self._code_to_mult_div(node,'mult', func_op=lambda x, y: x*y)

    @visitor.when(cil.DivNode)
    def visit(self, node):
        self.code.append(f'# {node.dest} <- {node.left} / {node.right}')
        self._code_to_mult_div(node,'div', func_op=lambda x, y: int(x / y))

    def _code_to_mult_div(self, node, op, func_op):
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
                rright = self.addr_desc.get_var_reg(node.right)
                self.code.append(f"li $t9, {node.left}")
                rleft = 't9'
            if op == 'div':
                self.code.append('la $a0, zero_error')
                self.code.append(f'beqz ${rright}, .raise')
            self.code.append(f"{op} ${rleft}, ${rright}")
            self.code.append(f"mflo ${rdest}")
        self.var_address[node.dest] = AddrType.INT

    @visitor.when(cil.LessNode)
    def visit(self, node):
        self.code.append(f'# {node.dest} <- {node.left} < {node.right}')
        self._code_to_comp(node, 'slt', lambda x, y: x < y)

    @visitor.when(cil.LessEqNode)
    def visit(self, node):
        self.code.append(f'# {node.dest} <- {node.left} <= {node.right}')
        self._code_to_comp(node, 'sle', lambda x, y: x <= y)

    @visitor.when(cil.EqualNode)
    def visit(self, node):
        self.code.append(f'# {node.dest} <- {node.left} = {node.right}')
        if self.is_variable(node.left) and self.is_variable(node.right) and self.var_address[node.left] == AddrType.STR and self.var_address[node.right] == AddrType.STR:
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