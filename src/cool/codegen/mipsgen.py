from .utils.tools import *
from typing import List
from ..semantic.helpers import VariableInfo
from ..semantic.types import Attribute
from .utils.ast_cil import *


class BaseMips:
    def __init__(self, inherit_graph):
        self.code: list = ['.text', '.globl main', 'main:']
        self.data_code = ['.data']
        self.symbol_table = SymbolTable()
        self.reg_desc = RegisterDescriptor()
        self.addr_desc = AddrDescriptor()
        self.dispatch_table: DispatchTable = DispatchTable()
        self.obj_table: ObjTable = ObjTable(self.dispatch_table)
        self.initialize_methods()
        self.get_abort_messages()
        self.var_address = {'self': AddrType.REF}
        self.loop_idx = 0
        self.first_defined = {'strcopier': True}
        self.inherit_graph = inherit_graph
        self.space_idx = 0

    def initialize_methods(self):
        self.methods = []
        for entry in self.obj_table:
            entry: ObjTabEntry
            self.methods.extend(entry.dispatch_table_entry)

    def get_runtime_errors(self):
        self.code.append('# Raise exception method')
        self.code.append('.raise:')
        self.code.append('li $v0, 4')
        self.code.append('syscall')
        self.code.append('li $v0, 17')
        self.code.append('li $a0, 1')
        self.code.append('syscall\n')
        self.data_code.append('zero_error: .asciiz \"Division by zero error\n\"')
        self.data_code.append('case_void_error: .asciiz \"Case on void error\n\"')
        self.data_code.append('dispatch_error: .asciiz \"Dispatch on void error\n\"')
        self.data_code.append('case_error: .asciiz \"Case statement without a matching branch error\n\"')
        self.data_code.append('index_error: .asciiz \"Substring out of range error\n\"')
        self.data_code.append('heap_error: .asciiz \"Heap overflow error\n\"')

    def get_abort_messages(self):
        self.data_code.append("abort_msg: .asciiz \"Abort called from class \"")
        self.data_code.append(f"new_line: .asciiz \"\n\"")
        self.data_code.append('string_abort: .asciiz \"Abort called from class String\n\"')
        self.data_code.append('int_abort: .asciiz \"Abort called from class Int\n\"')
        self.data_code.append('bool_abort: .asciiz \"Abort called from class Bool\n\"')

    def get_basic_blocks(self, instructions: List[InstructionNode]):
        leaders = self.find_leaders(instructions)
        blocks = [instructions[leaders[i - 1]:leaders[i]] for i in range(1, len(leaders))]
        return blocks

    def find_leaders(self, instructions: List[InstructionNode]):
        leaders = {0, len(instructions)}
        for i, inst in enumerate(instructions):
            if isinstance(inst, GotoNode) or isinstance(inst, GotoIfNode) or isinstance(inst, ReturnNode) \
                    or isinstance(inst, StaticCallNode) or isinstance(inst, DynamicCallNode):
                leaders.add(i + 1)
            elif isinstance(inst, LabelNode) or isinstance(inst, FunctionNode):
                leaders.add(i)
        return sorted(list(leaders))

    def is_variable(self, expr):
        return isinstance(expr, str)

    def is_int(self, expr):
        return isinstance(expr, int)

    def is_void(self, expr):
        return isinstance(expr, VoidConstantNode)

    def add_entry_symb_tab(self, name):
        self.symbol_table.insert(name)

    def next_use(self, basic_blocks: List[List[InstructionNode]]):
        next_use = {}
        for basic_block in basic_blocks:
            for x in self.symbol_table:
                self.symbol_table[x].is_live = False
                self.symbol_table[x].next_use = None

            for inst in reversed(basic_block):
                in1 = inst.in1 if self.is_variable(inst.in1) else None
                in2 = inst.in2 if self.is_variable(inst.in2) else None
                out = inst.out if self.is_variable(inst.out) else None

                in1nextuse, in2nextuse, outnextuse = None, None, None
                in1islive, in2islive, outislive = False, False, False

                entry_in1 = self.symbol_table.lookup(in1)
                entry_in2 = self.symbol_table.lookup(in2)
                entry_out = self.symbol_table.lookup(out)
                if out is not None:
                    if entry_out is not None:
                        outnextuse = entry_out.next_use
                        outislive = entry_out.is_live
                    else:
                        entry_out = SymbolTabEntry(out)
                    entry_out.next_use = None
                    entry_out.is_live = False
                    self.symbol_table.insert(entry_out)
                if in1 is not None:
                    if entry_in1 is not None:
                        in1nextuse = entry_in1.next_use
                        in1islive = entry_in1.is_live
                    else:
                        entry_in1 = SymbolTabEntry(out)
                    entry_in1.next_use = inst.index
                    entry_in1.is_live = True
                    self.symbol_table.insert(entry_in1)
                if in2 is not None:
                    if entry_in2 is not None:
                        in2nextuse = entry_in2.next_use
                        in2islive = entry_in2.is_live
                    else:
                        entry_in2 = SymbolTabEntry(in2)
                    entry_in2.next_use = inst.index
                    entry_in2.is_live = True

                    self.symbol_table.insert(entry_in2)

                n_entry = NextUseEntry(in1, in2, out, in1nextuse, in2nextuse, outnextuse, in1islive, in2islive,
                                       outislive)
                next_use[inst.index] = n_entry
        return next_use

    def get_reg(self, inst: InstructionNode):
        if self.is_variable(inst.in1):
            in1_reg = self.get_reg_var(inst.in1)
        if self.is_variable(inst.in2):
            in2_reg = self.get_reg_var(inst.in2)

        nu_entry = self.next_use[inst.index]
        if nu_entry.in1islive and nu_entry.in1nextuse < inst.index:
            self.update_register(inst.out, in1_reg)
            return
        if nu_entry.in2islive and nu_entry.in2nextuse < inst.index:
            self.update_register(inst.out, in2_reg)
            return
        if self.is_variable(inst.out):
            self.get_reg_var(inst.out)

    def get_reg_var(self, var):
        curr_inst = self.inst
        register = self.addr_desc.get_var_reg(var)
        if register is not None:
            return register

        register = self.reg_desc.find_empty_reg()
        if register is not None:
            self.update_register(var, register)
            self.load_var_code(var)
            return register

        next_use = self.next_use[curr_inst.index]
        score = self.initialize_score()
        for inst in self.block[1:]:
            inst: InstructionNode
            if self.is_variable(inst.in1) and inst.in1 not in [curr_inst.in1, curr_inst.in2,
                                                               curr_inst.out] and next_use.in1islive:
                self._update_score(score, inst.in1)
            if self.is_variable(inst.in2) and inst.in2 not in [curr_inst.in1, curr_inst.in2,
                                                               curr_inst.out] and next_use.in2islive:
                self._update_score(score, inst.in2)
            if self.is_variable(inst.out) and inst.out not in [curr_inst.in1, curr_inst.in2,
                                                               curr_inst.out] and next_use.outislive:
                self._update_score(score, inst.out)

        register = min(score, key=lambda x: score[x])

        self.update_register(var, register)
        self.load_var_code(var)
        return register

    def initialize_score(self):
        score = {}
        for reg in self.reg_desc.registers:
            score[reg] = 0
        try:
            reg = self.addr_desc.get_var_reg(self.inst.in1)
            if reg:
                score[reg] = 999
        except:
            pass
        try:
            reg = self.addr_desc.get_var_reg(self.inst.in2)
            if reg:
                score[reg] = 999
        except:
            pass
        try:
            reg = self.addr_desc.get_var_reg(self.inst.out)
            if reg:
                score[reg] = 999
        except:
            pass
        return score

    def _update_score(self, score, var):
        reg = self.addr_desc.get_var_reg(var)
        if reg is None:
            return
        try:
            score[reg] += 1
        except:
            score[reg] = 1

    def update_register(self, var, register):
        content = self.reg_desc.get_content(register)
        if content is not None:
            self.save_var_code(content)
            self.addr_desc.set_var_reg(content, None)
        self.reg_desc.insert_register(register, var)
        self.addr_desc.set_var_reg(var, register)

    def save_var_code(self, var):
        memory, register, _ = self.addr_desc.get_var_storage(var)
        self.code.append(f"sw ${register}, -{memory}($fp)")

    def load_var_code(self, var):
        memory, register, _ = self.addr_desc.get_var_storage(var)
        self.code.append(f'lw ${register}, -{memory}($fp)')

    def load_used_reg(self, registers):
        for reg in registers:
            self.code.append('addiu $sp, $sp, 4')
            self.code.append(f'lw ${reg}, ($sp)')

    def empty_registers(self, save=True):
        registers = self.reg_desc.used_registers()
        for reg, var in registers:
            if save:
                self.save_var_code(var)
            self.addr_desc.set_var_reg(var, None)
            self.reg_desc.insert_register(reg, None)

    def push_register(self, register):
        self.code.append(f'sw ${register}, ($sp)')
        self.code.append('addiu $sp, $sp, -4')

    def pop_register(self, register):
        self.code.append('addiu $sp, $sp, 4')
        self.code.append(f'lw ${register}, ($sp)')

    def save_to_register(self, expr):
        if self.is_int(expr):
            self.code.append(f'li $t9, {expr}')
            return 't9'
        elif self.is_variable(expr):
            return self.addr_desc.get_var_reg(expr)

    def get_attr_offset(self, attr_name: str, type_name: str):
        return self.obj_table[type_name].attr_offset(attr_name)

    def get_method_offset(self, type_name, method_name):
        self.obj_table[type_name].method_offset(method_name)

    def save_meth_addr(self, func_nodes: List[FunctionNode]):
        self.methods += [funct.name for funct in func_nodes]
        words = 'methods: .word ' + ', '.join(map(lambda x: '0', self.methods))
        self.data_code.append(words)
        self.code.append('# Save method directions in the methods array')
        self.code.append('la $v0, methods')
        for i, meth in enumerate(self.methods):
            self.code.append(f'la $t9, {meth}')
            self.code.append(f'sw $t9, {4 * i}($v0)')

    def save_types_addr(self, type_nodes: List[FunctionNode]):
        words = 'types: .word ' + ', '.join(map(lambda x: '0', self.inherit_graph))
        self.data_code.append(words)
        self.code.append('# Save types directions in the types array')
        self.code.append('la $t9, types')
        self.types = []
        self.code.append('# Save space to locate the type info')
        for i, (ntype, nparent) in enumerate(self.inherit_graph.items()):
            self.code.append('# Allocating memory')
            self.code.append('li $v0, 9')
            self.code.append(f'li $a0, 12')
            self.code.append('syscall')
            self.types.append(ntype)
            self.code.append('# Filling table methods')
            self.code.append(f'la $t8, type_{ntype}')
            self.code.append(f'sw $t8, 0($v0)')
            self.code.append('# Copying direction to array')
            self.code.append(f'sw $v0, {4 * i}($t9)')
            self.code.append('# Table addr is now stored in t8')
            self.code.append('move $t8, $v0')
            self.code.append('# Creating the dispatch table')
            self.create_dispatch_table(ntype)  # table addr is stored in $v0
            self.code.append('sw $v0, 8($t8)')

        self.code.append('# Copying parents')
        for i, ntype in enumerate(self.types):
            self.code.append(f'lw $v0, {4 * i}($t9)')
            nparent = self.inherit_graph[ntype]
            if nparent is not None:
                parent_idx = self.types.index(nparent)

                self.code.append(f'lw $t8, {4 * parent_idx}($t9)')
            else:
                self.code.append('li $t8, 0')
            self.code.append('sw $t8, 4($v0)')

    def create_dispatch_table(self, type_name):
        methods = self.dispatch_table.get_methods(type_name)
        self.code.append('# Allocate dispatch table in the heap')
        self.code.append('li $v0, 9')  # code to request memory
        dispatch_table_size = 4 * len(methods)
        self.code.append(f'li $a0, {dispatch_table_size + 4}')
        self.code.append('syscall')

        var = self.save_reg_if_occupied('v1')

        self.code.append(f'# I save the offset of every one of the methods of this type')
        self.code.append('# Save the direction of methods')
        self.code.append('la $v1, methods')
        for i, meth in enumerate(methods, 1):
            offset = 4 * self.methods.index(meth)
            self.code.append(f'# Save the direction of the method {meth} in a0')
            self.code.append(f'lw $a0, {offset}($v1)')
            self.code.append('# Save the direction of the method in his position in the dispatch table')
            self.code.append(
                f'sw $a0, {4 * i}($v0)')
        self.load_var_if_occupied(var)

    def get_type(self, xtype):
        if xtype == 'Int':
            return AddrType.INT
        elif xtype == 'Bool':
            return AddrType.BOOL
        elif xtype == 'String':
            return AddrType.STR
        return AddrType.REF

    def save_reg_if_occupied(self, reg):
        var = self.reg_desc.get_content(reg)
        if var is not None:
            self.code.append(f'# Saving content of {reg} to memory to use that register')
            self.save_var_code(var)
        return var

    def load_var_if_occupied(self, var):
        if var is not None:
            self.code.append(f'# Restore the variable of {var}')
            self.load_var_code(var)

    def compare_strings(self, node: EqualNode):
        rdest = self.addr_desc.get_var_reg(node.dest)
        rleft = self.addr_desc.get_var_reg(node.left)
        rright = self.addr_desc.get_var_reg(node.right)

        var = self.save_reg_if_occupied('a1')
        loop_idx = self.loop_idx

        self.code.append(f'move $t8, ${rleft}')  # counter
        self.code.append(f'move $t9, ${rright}')
        self.code.append(f'loop_{loop_idx}:')
        self.code.append(f'lb $a0, ($t8)')
        self.code.append(f'lb $a1, ($t9)')
        self.code.append(f'beqz $a0, check_{loop_idx}')
        self.code.append(f'beqz $a1, mismatch_{loop_idx}')
        self.code.append('seq $v0, $a0, $a1')
        self.code.append(f'beqz $v0, mismatch_{loop_idx}')
        self.code.append('addi $t8, $t8, 1')
        self.code.append('addi $t9, $t9, 1')
        self.code.append(f'j loop_{loop_idx}')
        self.code.append(f'mismatch_{loop_idx}:')
        self.code.append('li $v0, 0')
        self.code.append(f'j end_{loop_idx}')
        self.code.append(f'check_{loop_idx}:')
        self.code.append(f'bnez $a1, mismatch_{loop_idx}')
        self.code.append('li $v0, 1')
        self.code.append(f'end_{loop_idx}:')
        self.code.append(f'move ${rdest}, $v0')
        self.load_var_if_occupied(var)
        self.loop_idx += 1

    def conforms_to(self, rsrc, rdest, type_name):
        self.code.append(f'la $t9, type_{type_name}')

        loop_idx = self.loop_idx
        self.code.append(f'lw $v0, 8(${rsrc})')
        self.code.append(f'loop_{loop_idx}:')
        self.code.append(f'move $t8, $v0')
        self.code.append(f'beqz $t8, false_{loop_idx}')
        self.code.append('lw $v1, 0($t8)')
        self.code.append(f'beq $t9, $v1, true_{loop_idx}')
        self.code.append('lw $v0, 4($t8)')
        self.code.append(f'j loop_{loop_idx}')

        self.code.append(f'true_{loop_idx}:')
        self.code.append(f'li ${rdest}, 1')
        self.code.append(f'j end_{loop_idx}')
        self.code.append(f'false_{loop_idx}:')
        self.code.append(f'li ${rdest}, 0')
        self.code.append(f'end_{loop_idx}:')
        self.loop_idx += 1

    def value_conforms_to_obj(self, rdest, typex, branch_type):
        self.code.append('# Comparing value types in case node')
        true_label = f'true_{self.loop_idx}'
        end_label = f'end_{self.loop_idx}'
        self.code.append('la $t9, type_Object')
        self.code.append(f'la $t8, type_{branch_type}')
        self.code.append(f'beq $t9, $t8, {true_label}')
        self.code.append(f'la $t9, type_{typex}')
        self.code.append(f'beq $t9, $t8, {true_label}')
        self.code.append(f'li ${rdest}, 0')
        self.code.append(f'j {end_label}')
        self.code.append(f'{true_label}:')
        self.code.append(f'li ${rdest}, 1')
        self.code.append(f'{end_label}:')
        self.loop_idx += 1
