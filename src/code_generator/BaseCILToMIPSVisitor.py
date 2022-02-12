from cil_ast import *

class BaseCILToMIPSVisitor:
    def __init__(self, inherit_graph):
        self.code: list = ['.text', '.globl main', 'main:']
        self.initialize_data_code()
        self.symbol_table = SymbolTable()
        self.reg_desc = RegisterDescriptor()
        self.addr_desc = AddressDescriptor()
        
        self.obj_table: ObjTable = ObjTable(self.dispatch_table)
        self.initialize_methods()
        self.load_abort_messages()
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

    def initialize_data_code(self):
        self.data_code = ['.data'] 

    def initialize_runtime_errors(self):
        self.code.append('# Raise exception method')
        self.code.append('.raise:')
        self.code.append('li $v0, 4')
        self.code.append('syscall')
        self.code.append('li $v0, 17')
        self.code.append('li $a0, 1')
        self.code.append('syscall\n')
        self.data_code.append('zero_error: .asciiz \"Division by zero error\n\"')
        self.data_code.append('case_void_error: .asciiz \"Case on void error\n\"')
        self.data_code.append('dispatch_error: .asciiz \"Dispatch on void error\n\"'  )
        self.data_code.append('case_error: .asciiz \"Case statement without a matching branch error\n\"'  )
        self.data_code.append('index_error: .asciiz \"Substring out of range error\n\"')
        self.data_code.append('heap_error: .asciiz \"Heap overflow error\n\"')


    def get_basic_blocks(self, instructions):
        leaders = self.find_leaders(instructions)
        blocks = [instructions[leaders[i-1]:leaders[i]] for i in range(1, len(leaders))]
        return blocks


    def find_leaders(self, instructions):
        leaders = {0, len(instructions)}
        for i, inst in enumerate(instructions):
            if isinstance(inst, GoToNode) or isinstance(inst, IfGoToNode) or isinstance(inst, ReturnNode) \
                or isinstance(inst, CallNode) or isinstance(inst, VCallNode):
                leaders.add(i+1)
            elif isinstance(inst, LabelNode) or isinstance(inst, FunctionNode):
                leaders.add(i)
        return sorted(list(leaders))

    def is_variable(self, expr):
        return isinstance(expr, str)

    def is_int(self, expr):
        return isinstance(expr, int)

    def get_reg(self, inst):
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

        var_st = self.symbol_table.lookup(var)
        register = self.reg_desc.find_empty_reg()
        if register is not None:
            self.update_register(var, register)
            self.load_var_code(var)
            return register

        next_use = self.next_use[curr_inst.index]
        score = self.initialize_score()
        for inst in self.block[1:]:
            inst: InstructionNode
            if self.is_variable(inst.in1) and inst.in1 not in [curr_inst.in1, curr_inst.in2, curr_inst.out] and next_use.in1islive:
                self._update_score(score, inst.in1)  
            if self.is_variable(inst.in2) and inst.in2 not in [curr_inst.in1, curr_inst.in2, curr_inst.out] and next_use.in2islive:
                self._update_score(score, inst.in2)
            if self.is_variable(inst.out) and inst.out not in [curr_inst.in1, curr_inst.in2, curr_inst.out] and next_use.outislive:
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
        except: pass
        try:
            reg = self.addr_desc.get_var_reg(self.inst.in2) 
            if reg:
                score[reg] = 999
        except: pass
        try:
            reg = self.addr_desc.get_var_reg(self.inst.out) 
            if reg:
                score[reg] = 999
        except: pass
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
        memory, register, _= self.addr_desc.get_var_storage(var)
        self.code.append(f"sw ${register}, -{memory}($fp)")

    def load_var_code(self, var):
        memory, register, _ = self.addr_desc.get_var_storage(var)
        self.code.append(f'lw ${register}, -{memory}($fp)')
       
    def load_used_reg(self, used_reg):
        for reg in used_reg:
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

    def get_attr_offset(self, attr_name:str, type_name:str):
        return self.obj_table[type_name].attr_offset(attr_name)

    def get_method_offset(self, type_name, method_name):
        self.obj_table[type_name].method_offset(method_name)

    def save_meth_addr(self, func_nodes):
        self.methods += [funct.name for funct in func_nodes]
        words = 'methods: .word ' + ', '.join(map(lambda x: '0', self.methods))
        self.data_code.append(words)
        self.code.append('# Save method directions in the methods array')
        self.code.append('la $v0, methods')
        for i, meth in enumerate(self.methods):
            self.code.append(f'la $t9, {meth}')
            self.code.append(f'sw $t9, {4*i}($v0)')

    def save_types_addr(self, type_nodes):
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
            self.code.append(f'sw $v0, {4*i}($t9)')
            
            self.code.append('# Table addr is now stored in t8')
            self.code.append('move $t8, $v0')
            self.code.append('# Creating the dispatch table')
            self.create_dispatch_table(ntype)
            self.code.append('sw $v0, 8($t8)')


        self.code.append('# Copying parents')
        for i, ntype in enumerate(self.types):
            self.code.append(f'lw $v0, {4*i}($t9)')
            nparent = self.inherit_graph[ntype]
            if nparent is not None:
                parent_idx = self.types.index(nparent)

                self.code.append(f'lw $t8, {4*parent_idx}($t9)')
            else:
                self.code.append('li $t8, 0')
            self.code.append('sw $t8, 4($v0)')
