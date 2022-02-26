import re
from enum import Enum
from typing import List, Dict
from collections import OrderedDict

from utils import visitor
from code_generation.cil.nodes import *
from semantic.types import Attribute
from semantic.tools import VariableInfo
from constants import INT, IO, VISITOR_NODE, BOOL, STRING, OBJECT, SELF_LOWERCASE


class SymbolNode:
    def __init__(self, name, is_live=False, next_use=None):
        self.name = name
        self.is_live = is_live
        self.next_use = next_use

class SymbolTab:
    def __init__(self, entries:List[SymbolNode]=None):
        values = entries if entries is not None else []
        self.entries = {v.name: v for v in values}

    def get_symbols(self, entry_name: str) -> SymbolNode:
        if entry_name != None:
            if entry_name in self.entries.keys():
                return self.entries[entry_name]
           
    def set_symbol(self, entry: SymbolNode):
        self.entries[entry.name] = entry

    def set_text_symbol(self, name):
        self.entries[name] = SymbolNode(name)

    def __getitem__(self, item):
        return self.entries[item]

    def __iter__(self):
        return iter(self.entries)

class NextStep:
	def __init__(self, input1, input2, output, in1nextuse, in2nextuse, outnextuse, in1islive, in2islive, outislive):
		self.input1 = input1
		self.input2 = input2
		self.output = output
		self.in1nextuse = in1nextuse
		self.in2nextuse = in2nextuse
		self.outnextuse = outnextuse
		self.in1islive = in1islive
		self.in2islive = in2islive
		self.outislive = outislive

class AddrType(Enum):
    REF = 1,
    STR = 2,
    BOOL = 3,
    INT = 4,
    VOID = 5

class AddrDescriptor:
    def __init__(self):
        self.vars = {}

    def set_variable(self, name, address, register=None, stack=None):
        if address is not None:
            self.vars[name] = [4*address, register, stack]
        else:
            self.vars[name] = [address, register, stack]
            
    def get_addr_variable(self, name):
        return self.vars[name][0]

    def get_of_register(self, var):
        return self.vars[var][1]

    def set_of_register(self, name, reg):
        self.vars[name][1] = reg

    def get_of_memory(self, name):
        return self.vars[name]

class RegDescriptor:
    def __init__(self):
        registers = ['t0', 't1', 't2', 't3', 't4', 't5', 't6', 't7', 'a1', 'a2', 'a3', \
                    's0', 's1', 's2', 's3', 's4', 's5', 's6', 's7', 'v1']
        self.registers = {reg: None for reg in registers}

    def set_register(self, register:str, content:str):
        self.registers[register] = content

    def get_reg_context(self, register: str):
        return self.registers[register]

    def get_empty_register(self):
        for k, v in self.registers.items():
            if v is None:
                return k

    def get_busy_register(self):
        return [(k, v) for k, v in self.registers.items() if v is not None]

class DispatchTab:
    def __init__(self):
        self.classes = OrderedDict()
        self.regex = re.compile(r'function_(.+)_\w+')
        
    def set_class(self, type_name, methods):
        self.classes[type_name] = methods

    def get_offset(self, type_name, method):
        return self.classes[type_name].index(method)

    def get_fullname(self, type_name, mth_name):
        for meth in self.classes[type_name]: 
            name = self.regex.search(meth).groups()[0]
            if name == mth_name:
                return meth
        return None

    def get_class(self, type_name):
        return self.classes[type_name]

    def __len__(self):
        return len(self.classes)

class ObjNode:
    def __init__(self, name, methods, attrs):   
        self.class_tag: str = name
        self.size: int = 3 + len(attrs)
        self.dispatch_table_size = len(methods)
        self.dispatch_table_entry = methods
        self.attrs = attrs

    def attr_offset(self, attr):
        return self.attrs.index(attr) + 3

    def method_offset(self, meth):
        return self.dispatch_table_entry.index(meth)

class ObjTab:
    def __init__(self, dispatch_table: DispatchTab):
        self.objects: Dict[str, ObjNode] = {}
        self.dispatch_table = dispatch_table

    def set_element(self, name, methods, attrs):
        methods = [y for x, y in methods]
        attrs = [x for x, y in attrs]
        self.objects[name] = ObjNode(name, methods, attrs)
        self.dispatch_table.set_class(name, methods)

    def element_length(self, name):
        return self.objects[name].size

    def __getitem__(self, item) -> ObjNode:
        return self.objects[item]

    def __iter__(self):
        return iter(self.objects.values())

class MipsVisitor:
    def __init__(self, graph):
        self.code: list = ['.text', '.globl main', 'main:']
        self.set_data()
        self.symbol_tab = SymbolTab()
        self.reg_descriptor = RegDescriptor()
        self.addr_descriptor = AddrDescriptor()
        
        self.dispatch: DispatchTab = DispatchTab()
        self.obj: ObjTab = ObjTab(self.dispatch)
        self.set_methods()
        self.abort_messages()
        self.addr_variable = {SELF_LOWERCASE: AddrType.REF}
       
        self.loop_idx = 0   
        self.definition1 = {'strcopier': True}  
        self.graph = graph

    def set_methods(self):
        self.methods = [] 
        for elem in self.obj:
            elem: ObjNode
            self.methods.extend(elem.dispatch_table_entry)

    def set_data(self):
        self.data_code = ['.data'] 

    def set_runtime_errors(self):
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
        self.data_code.append('index_error: .asciiz \"Substring output of range error\n\"')
        self.data_code.append('heap_error: .asciiz \"Heap overflow error\n\"')    

    def abort_messages(self):
        self.data_code.append("abort_msg: .asciiz \"Abort called from class \"")     
        self.data_code.append(f"new_line: .asciiz \"\n\"")                       
        self.data_code.append('string_abort: .asciiz \"Abort called from class String\n\"')
        self.data_code.append('int_abort: .asciiz \"Abort called from class Int\n\"')
        self.data_code.append('bool_abort: .asciiz \"Abort called from class Bool\n\"')

    def get_blocks(self, instructions: List[CILInstructionNode]):
        l = self.find_leads(instructions)
        b = [instructions[l[i-1]:l[i]] for i in range(1, len(l))]
        return b

    def find_leads(self, instructions: List[CILInstructionNode]):
        l = {0, len(instructions)}
        for i, inst in enumerate(instructions):
            if isinstance(inst, CILGotoNode) or isinstance(inst, CILGotoIfNode) or isinstance(inst, CILReturnNode) or isinstance(inst, CILStaticCallNode) or isinstance(inst, CILDynamicCallNode):
                l.add(i+1)
            elif isinstance(inst, CILLabelNode) or isinstance(inst, CILFunctionNode):
                l.add(i)
        return sorted(list(l))

    def is_var(self, expr):
        return isinstance(expr, str)

    def is_int(self, expr):
        return isinstance(expr, int)

    def is_void(self, expr):
        return isinstance(expr, CILVoidConstantNode)

    def flush_symbol_table_next(self, basic_blocks: List[List[CILInstructionNode]]):
        result = {}
        for b in basic_blocks:
            for x in self.symbol_tab:
                self.symbol_tab[x].is_live = False
                self.symbol_tab[x].next_use = None

            for inst in reversed(b):
                in1 = inst.input1 if self.is_var(inst.input1) else None
                in2 = inst.input2 if self.is_var(inst.input2) else None
                out = inst.output if self.is_var(inst.output) else None
        
                in1ns = None
                in2ns = None
                outns = None
                in1a = False
                in2a = False
                outa = False

                symbol_in1 = self.symbol_tab.get_symbols(in1)
                symbol_in2 = self.symbol_tab.get_symbols(in2)
                symbol_out = self.symbol_tab.get_symbols(out)
                if out is not None:
                    if symbol_out is not None:
                        outns = symbol_out.next_use
                        outa = symbol_out.is_live
                    symbol_out.next_use = None
                    symbol_out.is_live = False
                    self.symbol_tab.set_symbol(symbol_out)
                if in1 is not None:
                    if symbol_in1 is not None:
                        in1ns = symbol_in1.next_use
                        in1a = symbol_in1.is_live
                    symbol_in1.next_use = inst.index
                    symbol_in1.is_live = True
                    self.symbol_tab.set_symbol(symbol_in1)
                if in2 is not None:
                    if symbol_in2 is not None:
                        in2ns = symbol_in2.next_use
                        in2a = symbol_in2.is_live
                    symbol_in2.next_use = inst.index
                    symbol_in2.is_live = True
                    self.symbol_tab.set_symbol(symbol_in2)

                next_symbols = NextStep(in1, in2, out, in1ns, in2ns, outns, in1a, in2a, outa)
                result[inst.index] = next_symbols
        return result

    def get_register(self, instruction: CILInstructionNode):
        if self.is_var(instruction.input1):
            in1 = self._get_register(instruction.input1)
        if self.is_var(instruction.input2):
            in2 = self._get_register(instruction.input2) 
        
        next_symbols = self.next_use[instruction.index]
        if next_symbols.in1islive and next_symbols.in1nextuse < instruction.index:
            self.update_register(instruction.output, in1)
            return  
        if next_symbols.in2islive and next_symbols.in2nextuse < instruction.index:
            self.update_register(instruction.output, in2)
            return 

        if self.is_var(instruction.output):
            self._get_register(instruction.output) 

    def _get_register(self, var):
        curr_inst = self.inst
        r = self.addr_descriptor.get_of_register(var)
        if r is not None:   
            return r

        var_st = self.symbol_tab.get_symbols(var)
        r = self.reg_descriptor.get_empty_register()
        if r is not None:
            self.update_register(var, r)
            self.load_code(var)
            return r

        next_symbol = self.next_use[inst.index]
        score = self.init_score()          
        for inst in self.block[1:]:
            inst: CILInstructionNode
            if self.is_var(inst.input1) and inst.input1 not in [curr_inst.input1, curr_inst.input2, curr_inst.output] and next_symbol.in1islive:
                self.update_score(score, inst.input1)  
            if self.is_var(inst.input2) and inst.input2 not in [curr_inst.input1, curr_inst.input2, curr_inst.output] and next_symbol.in2islive:
                self.update_score(score, inst.input2)
            if self.is_var(inst.output) and inst.output not in [curr_inst.input1, curr_inst.input2, curr_inst.output] and next_symbol.outislive:
                self.update_score(score, inst.output)
        
        r = min(score, key=lambda x: score[x])

        self.update_register(var, r)
        self.load_code(var)
        return r

    def init_score(self):
        score = {}
        for r in self.reg_descriptor.registers:
            score[r] = 0
        try:
            r = self.addr_descriptor.get_of_register(self.inst.input1) 
            if r:
                score[r] = 999
        except: pass
        try:
            r = self.addr_descriptor.get_of_register(self.inst.input2) 
            if r:
                score[r] = 999
        except: pass
        try:
            r = self.addr_descriptor.get_of_register(self.inst.output) 
            if r:
                score[r] = 999
        except: pass
        return score        

    def update_score(self, score, var):
        r = self.addr_descriptor.get_of_register(var) 
        if r is None:
            return
        try:
            score[r] += 1
        except:
            score[r] = 1

    def update_register(self, var, register):
        tmp = self.reg_descriptor.get_reg_context(register)
        if tmp is not None:
            self.save_variable(tmp)
            self.addr_descriptor.set_of_register(tmp, None)
        self.reg_descriptor.set_register(register, var)
        self.addr_descriptor.set_of_register(var, register)

    def save_variable(self, var):
        memory, register, _= self.addr_descriptor.get_of_memory(var)
        self.code.append(f"sw ${register}, -{memory}($fp)")

    def load_code(self, var):
        memory, register, _ = self.addr_descriptor.get_of_memory(var)
        self.code.append(f'lw ${register}, -{memory}($fp)')

    def clean_registers(self, save=True):
        registers = self.reg_descriptor.get_busy_register()
        for r, var in registers: 
            if save:
                self.save_variable(var)
            self.addr_descriptor.set_of_register(var, None)
            self.reg_descriptor.set_register(r, None)     

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
        elif self.is_var(expr):
            return self.addr_descriptor.get_of_register(expr)

    def get_attr_offset(self, attr_name:str, type_name:str):
        return self.obj[type_name].attr_offset(attr_name)

    def get_method_offset(self, type_name, method_name):
        self.obj[type_name].method_offset(method_name)

    def set_method_direction(self, f_nodes: List[CILFunctionNode]):
        self.methods += [f.name for f in f_nodes]
        words = 'methods: .word ' + ', '.join(map(lambda x: '0', self.methods))
        self.data_code.append(words)
        self.code.append('# Save method directions in the methods array')
        self.code.append('la $v0, methods')
        for i, m in enumerate(self.methods):
            self.code.append(f'la $t9, {m}')
            self.code.append(f'sw $t9, {4*i}($v0)')

    def set_type_direction(self, type_nodes: List[CILFunctionNode]):
        words = 'types: .word ' + ', '.join(map(lambda x: '0', self.graph))
        self.data_code.append(words)
        self.code.append('# Save types directions in the types array')
        self.code.append('la $t9, types')
        self.types = []
        self.code.append('# Save space to locate the type info')
        for i, (ntype, nparent) in enumerate(self.graph.items()):
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
            self.init_dispatch(ntype)   
            self.code.append('sw $v0, 8($t8)')

        self.code.append('# Copying parents')
        for i, ntype in enumerate(self.types):
            self.code.append(f'lw $v0, {4*i}($t9)')
            nparent = self.graph[ntype]
            if nparent is not None:
                parent_idx = self.types.index(nparent)
                self.code.append(f'lw $t8, {4*parent_idx}($t9)')
            else:
                self.code.append('li $t8, 0')
            self.code.append('sw $t8, 4($v0)')

    def init_dispatch(self, type_name):
        methods = self.dispatch.get_class(type_name)
        self.code.append('# Allocate dispatch table in the heap')
        self.code.append('li $v0, 9')                       
        dispatch_table_size = 4*len(methods)
        self.code.append(f'li $a0, {dispatch_table_size+4}')
        self.code.append('syscall')       
        var = self.save_data_register('v1')
        self.code.append(f'# I save the offset of every one of the methods of this type')
        self.code.append('# Save the direction of methods')
        self.code.append('la $v1, methods')             
        for i, meth in enumerate(methods, 1):
            offset = 4*self.methods.index(meth)
            self.code.append(f'# Save the direction of the method {meth} in a0')
            self.code.append(f'lw $a0, {offset}($v1)')      
            self.code.append('# Save the direction of the method in his position in the dispatch table')
            self.code.append(f'sw $a0, {4*i}($v0)')                 
        self.load_variable(var)

    def get_type(self, xtype):
        if xtype == INT:
            return AddrType.INT
        elif xtype == BOOL:
            return AddrType.BOOL
        elif xtype == STRING:
            return AddrType.STR
        return AddrType.REF

    def save_data_register(self, reg):
        var = self.reg_descriptor.get_reg_context(reg)
        if var is not None:
            self.code.append(f'# Saving content of {reg} to memory to use that register')
            self.save_variable(var)
        return var
    
    def load_variable(self, var):
        if var is not None:
            self.code.append(f'# Restore the variable of {var}')
            self.load_code(var)

    def compare_strings(self, node: CILEqualNode):
        destination = self.addr_descriptor.get_of_register(node.dest)
        left = self.addr_descriptor.get_of_register(node.left)
        right = self.addr_descriptor.get_of_register(node.right)

        var = self.save_data_register('a1')
        loop_idx = self.loop_idx
        
        self.code.append(f'move $t8, ${left}')                  
        self.code.append(f'move $t9, ${right}')
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
        self.code.append(f'move ${destination}, $v0')
        self.load_variable(var)
        self.loop_idx += 1

    def conforms_to(self, source, destination, type_name):
        self.code.append(f'la $t9, type_{type_name}')
        loop_idx = self.loop_idx
        self.code.append(f'lw $v0, 8(${source})')     
        self.code.append(f'loop_{loop_idx}:')
        self.code.append(f'move $t8, $v0')         
        self.code.append(f'beqz $t8, false_{loop_idx}')
        self.code.append('lw $v1, 0($t8)')
        self.code.append(f'beq $t9, $v1, true_{loop_idx}')
        self.code.append('lw $v0, 4($t8)')
        self.code.append(f'j loop_{loop_idx}')

        self.code.append(f'true_{loop_idx}:')
        self.code.append(f'li ${destination}, 1')
        self.code.append(f'j end_{loop_idx}')
        self.code.append(f'false_{loop_idx}:')
        self.code.append(f'li ${destination}, 0')
        self.code.append(f'end_{loop_idx}:')
        self.loop_idx += 1

    def conforms_value(self, destination, typex, branch_type):
        self.code.append('# Comparing value types in case node')
        true_label = f'true_{self.loop_idx}'
        end_label = f'end_{self.loop_idx}'
        self.code.append('la $t9, type_Object')         
        self.code.append(f'la $t8, type_{branch_type}')
        self.code.append(f'beq $t9, $t8, {true_label}')
        self.code.append(f'la $t9, type_{typex}')     
        self.code.append(f'beq $t9, $t8, {true_label}')
        self.code.append(f'li ${destination}, 0')
        self.code.append(f'j {end_label}')
        self.code.append(f'{true_label}:')
        self.code.append(f'li ${destination}, 1')
        self.code.append(f'{end_label}:')
        self.loop_idx += 1


class CilToMips(MipsVisitor):
    @visitor.on(VISITOR_NODE)
    def visit(self, node):
        pass

    @visitor.when(CILProgramNode)
    def visit(self, node: CILProgramNode):
        for type_ in node.cil_types:
            self.visit(type_)
        self.set_method_direction(node.cil_code)
        self.data_code.append(f"type_Void: .asciiz \"Void\"")           
        self.set_type_direction(node.cil_types)
        for d in node.cil_data:
            self.visit(d)
        for c in node.cil_code:
            self.visit(c)        
        self.set_runtime_errors()
        return self.data_code, self.code

    @visitor.when(CILTypeNode)
    def visit(self, node:CILTypeNode):
        self.obj.set_element(node.name, node.methods, node.attributes)
        self.data_code.append(f"type_{node.name}: .asciiz \"{node.name}\"")            

    @visitor.when(CILDataNode)
    def visit(self, node:CILDataNode):
        self.data_code.append(f"{node.name}: .asciiz \"{node.value}\"")     

    @visitor.when(CILFunctionNode)
    def visit(self, node:CILFunctionNode):
        self.code.append('')
        self.code.append(f'{node.name}:')
        self.locals = 0 
        self.code.append('# Gets the params from the stack')
        self.code.append(f'move $fp, $sp')
        n = len(node.params)
        for i, p in enumerate(node.params, 1):
            self.visit(p, i, n)
        self.code.append('# Gets the frame pointer from the stack')
        for i, v in enumerate(node.local_variables, len(node.params)):
            self.visit(v, i)
        self.locals = len(node.params) + len(node.local_variables)
        blocks = self.get_blocks(node.instructions)
        self.next_use = self.flush_symbol_table_next(blocks)
        for b in blocks:
            self.block = b
            for inst in b:
                self.inst = inst
                self.get_register(inst)
                self.visit(inst)
            inst = b[-1]
            if not (isinstance(inst, CILGotoNode) or isinstance(inst, CILGotoIfNode) or isinstance(inst, CILReturnNode) \
                or isinstance(inst, CILStaticCallNode) or isinstance(inst, CILDynamicCallNode)):
                self.clean_registers()      

    @visitor.when(CILParamNode)
    def visit(self, node:CILParamNode, idx:int, length:int):        
        self.symbol_tab.set_text_symbol(node.name)
        self.addr_variable[node.name] = self.get_type(node.type)
        self.code.append(f'# Pops the register with the param value {node.name}')
        self.code.append('addiu $fp, $fp, 4') 
        self.addr_descriptor.set_variable(node.name, length-idx)

    @visitor.when(CILLocalNode)
    def visit(self, node:CILLocalNode, idx:int):
        self.symbol_tab.set_text_symbol(node.name)
        self.addr_descriptor.set_variable(node.name, idx)
        self.code.append(f'# Updates stack pointer pushing {node.name} to the stack')
        self.code.append(f'addiu $sp, $sp, -4')

    @visitor.when(CILAssignNode)
    def visit(self, node:CILAssignNode):
        destination = self.addr_descriptor.get_of_register(node.dest)
        self.code.append(f'# Moving {node.source} to {node.dest}')
        if self.is_var(node.source):
            source = self.addr_descriptor.get_of_register(node.source)
            self.code.append(f'move ${destination}, ${source}') 
            self.addr_variable[node.dest] = self.addr_variable[node.source]
        elif self.is_int(node.source):
            self.code.append(f'li ${destination}, {node.source}')
            self.addr_variable[node.dest] = AddrType.INT
        self.save_variable(node.dest)
        
    @visitor.when(CILNotNode)
    def visit(self, node:CILNotNode):
        destination = self.addr_descriptor.get_of_register(node.dest)
        source = self.save_to_register(node.expr)
        self.code.append(f'# {node.dest} <- ~{node.expr}')
        self.code.append(f'not ${destination}, ${source}')
        self.code.append(f'addi ${destination}, ${destination}, 1')
        self.addr_variable[node.dest] = AddrType.INT
    
    @visitor.when(CILLogicalNotNode)
    def visit(self, node:CILLogicalNotNode):
        destination = self.addr_descriptor.get_of_register(node.dest)
        source = self.save_to_register(node.expr)
        self.code.append(f'# {node.dest} <- not {node.expr}')
        self.code.append(f'beqz ${source}, false_{self.loop_idx}')
        self.code.append(f'li ${destination}, 0')
        self.code.append(f'j end_{self.loop_idx}')
        self.code.append(f'false_{self.loop_idx}:')
        self.code.append(f'li ${destination}, 1')
        self.code.append(f'end_{self.loop_idx}:')
        self.loop_idx += 1
        self.addr_variable[node.dest] = AddrType.BOOL
   
    @visitor.when(CILPlusNode)
    def visit(self, node:CILPlusNode):
        destination = self.addr_descriptor.get_of_register(node.dest)
        self.code.append(f'# {node.dest} <- {node.left} + {node.right}')
        if self.is_var(node.left):
            left = self.addr_descriptor.get_of_register(node.left)
            if self.is_var(node.right):
                right = self.addr_descriptor.get_of_register(node.right)
                self.code.append(f"add ${destination}, ${left}, ${right}")
            elif self.is_int(node.right):
                self.code.append(f"addi ${destination}, ${left}, {node.right}")
        elif self.is_int(node.left):
            if self.is_int(node.right):
                self.code.append(f"li ${destination}, {node.left + node.right}")
            elif self.is_var(node.right):
                right = self.addr_descriptor.get_of_register(node.right)
                self.code.append(f"addi ${destination}, ${right}, {node.left}")
        self.addr_variable[node.dest] = AddrType.INT
   
    @visitor.when(CILMinusNode)
    def visit(self, node:CILMinusNode):
        destination = self.addr_descriptor.get_of_register(node.dest)
        self.code.append(f'# {node.dest} <- {node.left} - {node.right}')
        if self.is_var(node.left):
            left = self.addr_descriptor.get_of_register(node.left)
            if self.is_var(node.right):
                right = self.addr_descriptor.get_of_register(node.right)
                self.code.append(f"sub ${destination}, ${left}, ${right}")
            elif self.is_int(node.right):
                self.code.append(f"addi ${destination}, ${left}, -{node.right}")
        elif self.is_int(node.left):
            if self.is_int(node.right):
                self.code.append(f"li ${destination}, {node.left-node.right}")
            elif self.is_var(node.right):
                right = self.addr_descriptor.get_of_register(node.right)
                self.code.append(f"sub $t9, $zero, {right}")
                self.code.append(f"addi ${destination}, {node.left}, $t9")
        self.addr_variable[node.dest] = AddrType.INT

    @visitor.when(CILStarNode)
    def visit(self, node:CILStarNode):
        self.code.append(f'# {node.dest} <- {node.left} * {node.right}')
        self.code_to_mult_div(node, op='mult', func_op=lambda x, y: x*y)

    @visitor.when(CILDivNode)
    def visit(self, node:CILDivNode):
        self.code.append(f'# {node.dest} <- {node.left} / {node.right}')
        self.code_to_mult_div(node, op='div', func_op=lambda x, y: int(x / y))

    def code_to_mult_div(self, node, op:str, func_op):
        destination = self.addr_descriptor.get_of_register(node.dest)
        if self.is_int(node.left) and self.is_int(node.right):
            try:
                self.code.append(f"li ${destination}, {func_op(node.left, node.right)}")
            except ZeroDivisionError:
                self.code.append('la $a0, zero_error')
                self.code.append('j .raise')
        else:
            if self.is_var(node.left):
                left = self.addr_descriptor.get_of_register(node.left)
                if self.is_var(node.right):
                    right = self.addr_descriptor.get_of_register(node.right)
                elif self.is_int(node.right):
                    self.code.append(f"li $t9, {node.right}")
                    right = 't9'
            elif self.is_int(node.left):
                right = self.addr_descriptor.get_of_register(node.right)
                self.code.append(f"li $t9, {node.left}")
                left = 't9'
            if op == 'div':
                self.code.append('la $a0, zero_error')
                self.code.append(f'beqz ${right}, .raise')
            self.code.append(f"{op} ${left}, ${right}")
            self.code.append(f"mflo ${destination}")
        self.addr_variable[node.dest] = AddrType.INT

    @visitor.when(CILLessNode)
    def visit(self, node:CILLessNode):
        self.code.append(f'# {node.dest} <- {node.left} < {node.right}')
        self.code_to_comp(node, 'slt', lambda x, y: x < y)

    @visitor.when(CILLessEqNode)
    def visit(self, node:CILMinusNode):
        self.code.append(f'# {node.dest} <- {node.left} <= {node.right}')
        self.code_to_comp(node, 'sle', lambda x, y: x <= y)

    @visitor.when(CILEqualNode)
    def visit(self, node:CILMinusNode):
        self.code.append(f'# {node.dest} <- {node.left} = {node.right}')
        if self.is_var(node.left) and self.is_var(node.right) and self.addr_variable[node.left] == AddrType.STR and self.addr_variable[node.right] == AddrType.STR:
            self.compare_strings(node)
        else:
            self.code_to_comp(node, 'seq', lambda x, y: x == y)

    def code_to_comp(self, node, op, func_op):
        destination = self.addr_descriptor.get_of_register(node.dest)
        if self.is_var(node.left):
            left = self.addr_descriptor.get_of_register(node.left)
            if self.is_var(node.right):
                right = self.addr_descriptor.get_of_register(node.right)
                self.code.append(f"{op} ${destination}, ${left}, ${right}")
            elif self.is_int(node.right):
                self.code.append(f"li $t9, {node.right}")
                self.code.append(f"{op} ${destination}, ${left}, $t9")
        elif self.is_int(node.left):
            if self.is_int(node.right):
                self.code.append(f"li ${destination}, {int(func_op(node.left, node.right))}")
            elif self.is_var(node.right):
                right = self.addr_descriptor.get_of_register(node.right)
                self.code.append(f"li $t9, {node.left}")
                self.code.append(f"{op} ${destination}, $t9, ${right}")
        self.addr_variable[node.dest] = AddrType.BOOL

    @visitor.when(CILGetAttribNode)
    def visit(self, node:CILGetAttribNode):
        self.code.append(f'# {node.dest} <- GET {node.obj} . {node.attr}')
        destination = self.addr_descriptor.get_of_register(node.dest)
        self.addr_variable[node.dest] = self.get_type(node.attr_type)
        source = self.addr_descriptor.get_of_register(node.obj)
        attr_offset = 4*self.get_attr_offset(node.attr, node.type_name)
        self.code.append(f'lw ${destination}, {attr_offset}(${source})')


    @visitor.when(CILSetAttribNode)
    def visit(self, node:CILSetAttribNode):
        self.code.append(f'# {node.obj} . {node.attr} <- SET {node.value}')
        destination = self.addr_descriptor.get_of_register(node.obj)
        attr_offset = 4*self.get_attr_offset(node.attr, node.type_name)
        if self.is_var(node.value):
            source = self.addr_descriptor.get_of_register(node.value)
        elif self.is_int(node.value):
            self.code.append(f'li $t9, {node.value}')
            source = 't9'
        elif self.is_void(node.value):
            self.code.append(f'la $t9, type_{"Void"}')
            source = 't9'
        self.code.append(f'sw ${source}, {attr_offset}(${destination})')
        
    @visitor.when(CILAllocateNode)
    def visit(self, node:CILAllocateNode):
        destination = self.addr_descriptor.get_of_register(node.dest)
        size = 4*self.obj.element_length(node.type)     
        self.addr_variable[node.dest] = AddrType.REF
        self.code.append('# Syscall to allocate memory of the object entry in heap')
        self.code.append('li $v0, 9')                         
        self.code.append(f'li $a0, {size}')                   
        self.code.append('syscall')
        addrs_stack = self.addr_descriptor.get_addr_variable(node.dest)
        self.code.append('# Loads the name of the variable and saves the name like the first field')
        self.code.append(f'la $t9, type_{node.type}')       
        self.code.append(f'sw $t9, 0($v0)')               
        self.code.append(f'# Saves the size of the node')
        self.code.append(f'li $t9, {size}')                 
        self.code.append(f'sw $t9, 4($v0)')                 
        self.code.append(f'move ${destination}, $v0')             
      
        idx = self.types.index(node.type)
        self.code.append('# Adding Type Info addr')
        self.code.append('la $t8, types')
        self.code.append(f'lw $v0, {4*idx}($t8)')
        self.code.append(f'sw $v0, 8(${destination})')
      
    @visitor.when(CILTypeOfNode)
    def visit(self, node:CILTypeOfNode):
        destination = self.addr_descriptor.get_of_register(node.dest)
        self.code.append(f'# {node.dest} <- Type of {node.obj}')
        if self.is_var(node.obj):
            source = self.addr_descriptor.get_of_register(node.obj)
            if self.addr_variable[node.obj] == AddrType.REF:
                self.code.append(f'lw ${destination}, 0(${source})')   
            elif self.addr_variable[node.obj] == AddrType.STR:
                self.code.append(f'la ${destination}, type_String')
            elif self.addr_variable[node.obj] == AddrType.INT:
                self.code.append(f'la ${destination}, type_Int')
            elif self.addr_variable[node.obj] == AddrType.BOOL:
                self.code.append(f'la ${destination}, type_Bool')
        elif self.is_int(node.obj):
            self.code.append(f'la ${destination}, type_Int')
        self.addr_variable[node.dest] = AddrType.STR

    @visitor.when(CILLabelNode)
    def visit(self, node:CILLabelNode):
        self.code.append(f'{node.label}:')

    @visitor.when(CILGotoNode)
    def visit(self, node:CILGotoNode):
        self.clean_registers()
        self.code.append(f'j {node.label}')

    @visitor.when(CILGotoIfNode)
    def visit(self, node:CILGotoIfNode):
        reg = self.save_to_register(node.cond)
        self.code.append(f'# If {node.cond} goto {node.label}')
        self.clean_registers()
        self.code.append(f'bnez ${reg}, {node.label}')

    @visitor.when(CILGotoIfFalseNode)
    def visit(self, node:CILGotoIfNode):
        reg = self.save_to_register(node.cond)
        self.code.append(f'# If not {node.cond} goto {node.label}')
        self.clean_registers()
        self.code.append(f'beqz ${reg}, {node.label}')

    @visitor.when(CILStaticCallNode)
    def visit(self, node:CILStaticCallNode):
        function = self.dispatch.get_fullname(node.type, node.function)
        self.code.append(f'# Static Dispatch of the method {node.function}')
        self._code_to_function_call(node.args, function, node.dest)

        self.addr_variable[node.dest] = self.get_type(node.return_type)

    @visitor.when(CILDynamicCallNode)
    def visit(self, node:CILDynamicCallNode):
        self.code.append('# Find the actual name in the dispatch table')
        reg = self.addr_descriptor.get_of_register(node.obj)      
        self.code.append('# Gets in a0 the actual direction of the dispatch table')
        self.code.append(f'lw $t9, 8(${reg})')          
        self.code.append('lw $a0, 8($t9)')
        function = self.dispatch.get_fullname(node.type, node.method)       
        index = 4*self.dispatch.get_offset(node.type, function) + 4     
        self.code.append(f'# Saves in t8 the direction of {function}')
        self.code.append(f'lw $t8, {index}($a0)')      
        self._code_to_function_call(node.args, '$t8', node.dest, function)        
        self.addr_variable[node.dest] = self.get_type(node.return_type)

    def _code_to_function_call(self, args, function, dest, function_name=None):
        self.push_register('fp')                    
        self.push_register('ra')                   
        self.code.append('# Push the arguments to the stack')
        for arg in reversed(args):             
            self.visit(arg)
        self.code.append('# Empty all used registers and saves them to memory')
        self.clean_registers()
        self.code.append('# This function will consume the arguments')
        self.code.append(f'jal {function}')        
        self.code.append('# Pop ra register of return function of the stack')
        self.pop_register('ra')                 
        self.code.append('# Pop fp register from the stack')
        self.pop_register('fp')                    
        if dest is not None:
            self._get_register(dest)
            destination = self.addr_descriptor.get_of_register(dest)
            self.code.append('# saves the return value')
            self.code.append(f'move ${destination}, $v0') 
            
    @visitor.when(CILArgNode)
    def visit(self, node:CILArgNode):
        self.code.append('# The rest of the arguments are push into the stack')
        if self.is_var(node.dest):
            self._get_register(node.dest)
            reg = self.addr_descriptor.get_of_register(node.dest)
            self.code.append(f'sw ${reg}, ($sp)')
        elif self.is_int(node.dest):
            self.code.append(f'li $t9, {node.dest}')
            self.code.append(f'sw $t9, ($sp)')
        self.code.append('addiu $sp, $sp, -4')
       
    @visitor.when(CILReturnNode)
    def visit(self, node:CILReturnNode):
        if self.is_var(node.value): 
            destination = self.addr_descriptor.get_of_register(node.value)
            self.code.append(f'move $v0, ${destination}')
        elif self.is_int(node.value):
            self.code.append(f'li $v0, {node.value}')
        self.code.append('# Empty all used registers and saves them to memory')
        self.clean_registers()           
        self.code.append('# Removing all locals from stack')
        self.code.append(f'addiu $sp, $sp, {self.locals*4}')
        self.code.append(f'jr $ra')

        self.code.append('')

    @visitor.when(CILLoadNode)
    def visit(self, node:CILLoadNode):
        destination = self.addr_descriptor.get_of_register(node.dest)
        self.code.append(f'# Saves in {node.dest} {node.msg}')
        self.addr_variable[node.dest] = AddrType.STR
        self.code.append(f'la ${destination}, {node.msg}')
    
    @visitor.when(CILLengthNode)
    def visit(self, node: CILLengthNode):
        destination = self.addr_descriptor.get_of_register(node.dest)
        reg = self.addr_descriptor.get_of_register(node.arg)
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
        self.code.append(f'sub ${destination}, $t8, ${reg}')
        self.loop_idx += 1

    @visitor.when(CILConcatNode)
    def visit(self, node: CILConcatNode):
        destination = self.addr_descriptor.get_of_register(node.dest)
        self.code.append('# Allocating memory for the buffer')
        self.code.append('li $a0, 356')
        self.code.append('li $v0, 9')
        self.code.append('syscall')
        self.code.append(f'move ${destination}, $v0')
        source1 = self.addr_descriptor.get_of_register(node.arg1)
        if node.arg2 is not None:
            source2 = self.addr_descriptor.get_of_register(node.arg2)
        self.code.append('# Copy the first string to dest')
        var = self.save_data_register('a1')
        self.code.append(f'move $a0, ${source1}')
        self.code.append(f'move $a1, ${destination}')
        self.push_register('ra')
        self.code.append('jal strcopier')

        if node.arg2 is not None:
            self.code.append('# Concatenate second string on result buffer')
            self.code.append(f'move $a0, ${source2}')
            self.code.append(f'move $a1, $v0')
            self.code.append('jal strcopier')
        self.code.append('sb $0, 0($v0)')
        self.pop_register('ra')
        self.code.append(f'j finish_{self.loop_idx}')

        if self.definition1['strcopier']:
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
            self.definition1['strcopier'] = False
        
        self.code.append(f'finish_{self.loop_idx}:')
        self.load_variable(var)
        self.loop_idx += 1

    @visitor.when(CILSubstringNode)
    def visit(self, node: CILSubstringNode):
        destination = self.addr_descriptor.get_of_register(node.dest)
        self.code.append('# Allocating memory for the buffer')
        self.code.append('li $a0, 356')
        self.code.append('li $v0, 9')
        self.code.append('syscall')
        self.code.append(f'move ${destination}, $v0')
        if self.is_var(node.begin):
            rstart = self.addr_descriptor.get_of_register(node.begin)
        elif self.is_int(node.begin):
            rstart = 't8'
            self.code.append(f'li $t8, {node.begin}')
        if self.is_var(node.end):
            rend = self.addr_descriptor.get_of_register(node.end)
            var = None
        elif self.is_int(node.end):
            var = self.save_data_register('a3')
            rend = 'a3'
            self.code.append(f'li $a3, {node.end}')

        self._get_register(node.word)
        rself = self.addr_descriptor.get_of_register(node.word)

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
        self.code.append(f'move $v0, ${destination}')

        loop = f'loop_{self.loop_idx}'
        end = f'end_{self.loop_idx}'
        self.code.append(f'{loop}:')
        self.code.append(f'sub $t9, $v0, ${destination}') 

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
        self.load_variable(var)
        self.loop_idx += 1

    @visitor.when(CILOutStringNode)
    def visit(self, node: CILOutStringNode):
        reg = self.addr_descriptor.get_of_register(node.value)
        self.code.append('# Printing a string')
        self.code.append('li $v0, 4')
        self.code.append(f'move $a0, ${reg}')
        self.code.append('syscall')

    @visitor.when(CILOutIntNode)
    def visit(self, node: CILOutIntNode):
        if self.is_var(node.value):
            reg = self.addr_descriptor.get_of_register(node.value)
        elif self.is_int(node.value):
            reg = 't8'
            self.code.append(f'li $t8, ${node.value}')

        self.code.append('# Printing an int')
        self.code.append('li $v0, 1')
        self.code.append(f'move $a0, ${reg}')
        self.code.append('syscall')
    

    @visitor.when(CILReadStringNode)
    def visit(self, node: CILReadStringNode):
        
        destination = self.addr_descriptor.get_of_register(node.dest)
        self.code.append('# Allocating memory for the buffer')
        self.code.append('li $a0, 356')
        self.code.append('li $v0, 9')
        self.code.append('syscall')
        self.code.append(f'move ${destination}, $v0')
        self.code.append('# Reading a string')
        var = self.save_data_register('a1')
        self.code.append('# Putting buffer in a0')
        self.code.append(f'move $a0, ${destination}')   
        self.code.append('# Putting length of string in a1')
        self.code.append(f'li $a1, 356')             
        self.code.append('li $v0, 8')
        self.code.append('syscall')
        self.code.append('# Walks to eliminate the newline')        
        start = f'start_{self.loop_idx}'
        end = f'end_{self.loop_idx}'
        self.code.append(f'move $t9, ${destination}')
        self.code.append(f'{start}:')       
        self.code.append('lb $t8, 0($t9)')
        self.code.append(f"beqz $t8, {end}")
        self.code.append('add $t9, $t9, 1')
        self.code.append(f'j {start}')
        self.code.append(f'{end}:')
        self.code.append('addiu $t9, $t9, -1')
        self.code.append('sb $0, ($t9)')
        self.loop_idx += 1
        self.load_variable(var)


    @visitor.when(CILReadIntNode)
    def visit(self, node: CILReadIntNode):
        destination = self.addr_descriptor.get_of_register(node.dest)
        self.code.append('# Reading a int')
        self.code.append('li $v0, 5')
        self.code.append('syscall')
        self.code.append(f'move ${destination}, $v0')


    @visitor.when(CILExitNode)
    def visit(self, node: CILExitNode):
        self.code.append('# Exiting the program')
        if self.is_var(node.value):
            reg = self.addr_descriptor.get_of_register(node.value)
        elif self.is_int(node.value):
            reg = 't8'
            self.code.append(f'li $t8, {node.value}')
        rself = self.addr_descriptor.get_of_register(node.classx)
        'Abort called from class String'
        if self.addr_variable[node.classx] == AddrType.REF: 
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

    @visitor.when(CILCopyNode)
    def visit(self, node: CILCopyNode):
        destination = self.addr_descriptor.get_of_register(node.dest)
        source = self.addr_descriptor.get_of_register(node.source)

        self.code.append(f'lw $t9, 4(${source})')             
        self.code.append('# Syscall to allocate memory of the object entry in heap')
        self.code.append('li $v0, 9')                       
        self.code.append(f'move $a0, $t9')                  
        self.code.append('syscall')

        self.code.append(f'move ${destination}, $v0')
        self.code.append('# Loop to copy every field of the previous object')
        self.code.append('# t8 the register to loop')
        self.code.append('li $t8, 0')
        self.code.append(f'loop_{self.loop_idx}:')
        self.code.append('# In t9 is stored the size of the object')
        self.code.append(f'bge $t8, $t9, exit_{self.loop_idx}')
        self.code.append(f'lw $a0, (${source})')
        self.code.append('sw $a0, ($v0)')
        self.code.append('addi $v0, $v0, 4')
        self.code.append(f'addi ${source}, ${source}, 4')
        self.code.append('# Increase loop counter')
        self.code.append('addi $t8, $t8, 4')
        self.code.append(f'j loop_{self.loop_idx}')
        self.code.append(f'exit_{self.loop_idx}:')
        self.loop_idx += 1

    @visitor.when(CILConformsNode)
    def visit(self, node: CILConformsNode):
        destination = self.addr_descriptor.get_of_register(node.dest)
        if self.is_var(node.expr):
            source = self.addr_descriptor.get_of_register(node.expr)
            if self.addr_variable[node.expr] == AddrType.REF:
                self.conforms_to(source, destination, node.type)
            elif self.addr_variable[node.expr] == AddrType.STR:
                self.conforms_value(destination, STRING, node.type)
            elif self.addr_variable[node.expr] == AddrType.INT:
                self.conforms_value(destination, INT, node.type)
            elif self.addr_variable[node.expr] == AddrType.BOOL:
                self.conforms_value(destination, BOOL, node.type)
        elif self.is_int(node.expr):
            self.conforms_value(destination, INT, node.type)

    @visitor.when(CILErrorNode)
    def visit(self, node: CILErrorNode):
        self.code.append(f'la $a0, {node.type}')
        self.code.append('j .raise')

    @visitor.when(CILVoidConstantNode)
    def visit(self, node:CILVoidConstantNode):
        destination = self.addr_descriptor.get_of_register(node.output)
        self.code.append('# Initialize void node')
        self.code.append(f'li $a0, 4')                    
        self.code.append('li $v0, 9')                       
        self.code.append('syscall')
        self.code.append('# Loads the name of the variable and saves the name like the first field')
        self.code.append(f'la $t9, type_{"Void"}')      
        self.code.append('sw $t9, 0($v0)')                 
        self.code.append(f'move ${destination}, $v0')
        self.addr_variable[node.obj] = AddrType.REF
     
    @visitor.when(CILBoxingNode)
    def visit(self, node:CILBoxingNode):
        destination = self.addr_descriptor.get_of_register(node.dest)
        self.code.append('# Initialize new node')
        self.code.append('li $a0, 12')
        self.code.append('li $v0, 9')
        self.code.append('syscall')

        self.code.append(f'la $t9, type_{node.type}')
        self.code.append('sw $t9, 0($v0)')            
        self.code.append('li $t9, 12')
        self.code.append('sw $t9, 4($v0)')           
        self.code.append(f'move ${destination}, $v0')
        
        self.code.append('# Saving the methods of object')
        idx = self.types.index(OBJECT)
        self.code.append('# Adding Type Info addr')
        self.code.append('la $t8, types')
        self.code.append(f'lw $v0, {4*idx}($t8)')
        self.code.append(f'sw $v0, 8(${destination})')
        self.addr_variable[node.dest] = AddrType.REF