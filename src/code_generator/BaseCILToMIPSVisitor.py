from cil_ast import *
from typing import List, Dict
from enum import Enum

class BaseCILToMIPSVisitor:
    def __init__(self, inherit_graph):
        self.code: list = ['.text', '.globl main', 'main:']
        self.initialize_data_code()
        self.symbol_table = SymbolTable()
        self.reg_desc = RegisterDescriptor()
        self.addr_desc = AddressDescriptor()
        
        self.obj_table: ObjTable = ObjTable(self.dispatch_table)
        self.initialize_methods()
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

    def get_basic_blocks(self, instructions):
        leaders = self.find_leaders(instructions)
        blocks = [instructions[leaders[i-1]:leaders[i]] for i in range(1, len(leaders))]
        return blocks

    def is_variable(self, expr):
        return isinstance(expr, str)

    def construct_next_use(self, basic_blocks):
        next_use = {}
        for basic_block in basic_blocks:
            for x in self.symbol_table:
                self.symbol_table[x].is_live = False
                self.symbol_table[x].next_use = None

            for inst in reversed(basic_block):
                in1 = inst.in1 if self.is_variable(inst.in1) else None
                in2 = inst.in2 if self.is_variable(inst.in2) else None
                out = inst.out if self.is_variable(inst.out) else None
        
                in1nextuse = None
                in2nextuse = None
                outnextuse = None
                in1islive = False
                in2islive = False
                outislive = False

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

                n_entry = NextUseEntry(in1, in2, out, in1nextuse, in2nextuse, outnextuse, in1islive, in2islive, outislive)
                next_use[inst.index] = n_entry
        return next_use


    def get_reg(self, inst):
        if self.is_variable(inst.in1):
            in1_reg = self.get_reg_var(inst.in1)
        if self.is_variable(inst.in2):
            in2_reg = self.get_reg_var(inst.in2)

    def used_registers(self):
        return [(k, v) for k, v in self.registers.items() if v is not None]

    def save_var_code(self, var):
        memory, register, _= self.addr_desc.get_var_storage(var)
        self.code.append(f"sw ${register}, -{memory}($fp)")

    def insert_register(self, register, content):
        self.registers[register] = content

    def empty_registers(self, save=True):
        registers = self.reg_desc.used_registers()
        for reg, var in registers: 
            if save:
                self.save_var_code(var)
            self.addr_desc.set_var_reg(var, None)
            self.reg_desc.insert_register(reg, None)

    def get_type(self, xtype):
        if xtype == 'Int':
            return AddrType.INT
        elif xtype == 'Bool':
            return AddrType.BOOL
        elif xtype == 'String':
            return AddrType.STR
        return AddrType.REF

    
    def is_int(self, expr):
        return isinstance(expr, int)

    def save_to_register(self, expr):
        if self.is_int(expr):
            self.code.append(f'li $t9, {expr}')
            return 't9'
        elif self.is_variable(expr):
            return self.addr_desc.get_var_reg(expr)


class AddrType(Enum):
    REF = 1,
    STR = 2,
    BOOL = 3,
    INT = 4,
    VOID = 5


class NextUseEntry:
	def __init__(self, in1, in2, out, in1nextuse, in2nextuse, outnextuse, in1islive, in2islive, outislive):
		self.in1 = in1
		self.in2 = in2
		self.out = out
		self.in1nextuse = in1nextuse
		self.in2nextuse = in2nextuse
		self.outnextuse = outnextuse
		self.in1islive = in1islive
		self.in2islive = in2islive
		self.outislive = outislive


class ObjTabEntry:
    def __init__(self, name, methods, attrs):   
        self.class_tag: str = name
        self.size: int = 3 + len(attrs)
        self.dispatch_table_size = len(methods)
        self.dispatch_table_entry = methods
        self.attrs = attrs
    
    @property
    def class_tag_offset(self):
        return 0

    @property
    def size_offset(self):
        return 1

    @property
    def dispatch_ptr_offset(self):
        return 2

    def attr_offset(self, attr):
        return self.attrs.index(attr) + 3

    def method_offset(self, meth):
        return self.dispatch_table_entry.index(meth)


class ObjTable:
    def __init__(self, dispatch_table):
        self.objects: Dict[str, ObjTabEntry] = {}
        self.dispatch_table = dispatch_table

    def initialize_built_in(self):
        object_methods = [
            'function_abort_Object', 
            'function_type_name_Object', 
            'function_copy_Object']
        io_methods = [
            'function_out_string_IO',
            'function_out_int_IO',
            'function_in_string_IO',
            'function_in_int_IO']
        str_methods = [
            'function_length_String', 
            'function_concat_String', 
            'function_substr_String' ]
        return {
            'Int': ObjTabEntry('Int', [], []), 
            'Bool': ObjTabEntry('Bool', [], []),
            'IO': ObjTabEntry('IO', io_methods, []),
            'String': ObjTabEntry('String', str_methods, []),
            'Object': ObjTabEntry('Object', object_methods, [])
        }

    def add_entry(self, name, methods, attrs):
        methods = [y for x, y in methods]
        attrs = [x for x, y in attrs]
        self.objects[name] = ObjTabEntry(name, methods, attrs)
        self.dispatch_table.add_class(name, methods)

    def size_of_entry(self, name):
        return self.objects[name].size

    def __getitem__(self, item) -> ObjTabEntry:
        return self.objects[item]

    def __iter__(self):
        return iter(self.objects.values())

class RegisterDescriptor:
    def __init__(self):
        registers = ['t0', 't1', 't2', 't3', 't4', 't5', 't6', 't7', 'a1', 'a2', 'a3', \
                    's0', 's1', 's2', 's3', 's4', 's5', 's6', 's7', 'v1']
        self.registers = {reg: None for reg in registers}

    def insert_register(self, register:str, content:str):
        self.registers[register] = content

    def get_content(self, register: str):
        return self.registers[register]

    def find_empty_reg(self):
        for k, v in self.registers.items():
            if v is None:
                return k

    def used_registers(self):
        return [(k, v) for k, v in self.registers.items() if v is not None]

    def empty_registers(self):
        for k in self.registers:
            self.registers[k] = None


class AddressDescriptor:
    def __init__(self):
        self.vars = {}

    def insert_var(self, name, address, register=None, stack=None):
        if address is not None:
            self.vars[name] = [4*address, register, stack]
        else:
            self.vars[name] = [address, register, stack]
            
    def get_var_addr(self, name):
        return self.vars[name][0]

    def set_var_addr(self, name, addr):
        self.vars[name][0] = 4*addr

    def get_var_reg(self, var):
        return self.vars[var][1]

    def set_var_reg(self, name, reg):
        self.vars[name][1] = reg

    def get_var_stack(self, name):
        return self.vars[name][2]

    def set_var_stack(self, name, stack_pos):
        self.vars[name][1] = stack_pos

    def get_var_storage(self, name):
        return self.vars[name]




class SymbolTabEntry:
    def __init__(self, name, is_live=False, next_use=None):
        self.name = name
        self.is_live = is_live
        self.next_use = next_use

class SymbolTable:
    def __init__(self, entries = None):
        values = entries if entries is not None else []
        self.entries = {v.name: v for v in values}

    def lookup(self, entry_name: str) -> SymbolTabEntry:
        if entry_name != None:
            if entry_name in self.entries.keys():
                return self.entries[entry_name]
           
    def insert(self, entry):
        self.entries[entry.name] = entry

    def insert_name(self, name):
        self.entries[name] = SymbolTabEntry(name)

    def __getitem__(self, item):
        return self.entries[item]

    def __iter__(self):
        return iter(self.entries)