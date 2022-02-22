from CIL.ast import *
from Tools.utils import *
import Tools.visitor as visitor

class MIPS:
    def __init__(self, inherit_graph):
        self.code: list = ['\t.text', '\t.globl main', 'main:']
        self.initialize_data_code()
        self.symbol_table = SymbolTable()
        self.reg_desc = RegisterDescriptor()
        self.addr_desc = AddressDescriptor()
        
        self.dispatch_table = DispatchTable()
        self.obj_table: ObjTable = ObjTable(self.dispatch_table)
        self.initialize_methods()
        self.load_abort_messages()
        self.var_address = {'self': AddrType.REF}
       
        self.loop_idx = 0
        self.first_defined = {'strcopier': True}  
        self.inherit_graph = inherit_graph
        self.space_idx = 0

    @visitor.on('node')
    def visit(self, node):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node: ProgramNode):
        for type_ in node.dottypes:
            self.visit(type_)
        self.save_meth_addr(node.dotcode)
        self.data_code.append(f"type_Void: .asciiz \"Void\"")                   
        self.save_types_addr(node.dottypes)
        for data in node.dotdata:
            self.visit(data)
        for code in node.dotcode:
            self.visit(code)
        self.initialize_runtime_errors()
        return self.data_code, self.code

    @visitor.when(TypeNode)
    def visit(self, node:TypeNode):
        self.obj_table.add_entry(node.name, node.methods, node.attributes)
        self.data_code.append(f"type_{node.name}: .asciiz \"{node.name}\"")           

    @visitor.when(DataNode)
    def visit(self, node:DataNode):
        self.data_code.append(f"{node.name}: .asciiz \"{node.value}\"")     

    @visitor.when(FunctionNode)
    def visit(self, node:FunctionNode):
        self.code.append('')
        self.code.append(f'{node.name}:')
        self.locals = 0 
        self.code.append(f'\tmove $fp, $sp')
        n = len(node.params)
        for i, param in enumerate(node.params, 1):
            self.visit(param, i, n)
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
            if not (isinstance(inst, GotoNode) or isinstance(inst, GotoIfNode) or isinstance(inst, ReturnNode) \
                or isinstance(inst, StaticCallNode) or isinstance(inst, DynamicCallNode)):
                self.empty_registers()            

    @visitor.when(ParamNode)
    def visit(self, node:ParamNode, idx:int, length:int):        
        self.symbol_table.insert_name(node.name)
        self.var_address[node.name] = self.get_type(node.type)
        self.code.append('\taddiu $fp, $fp, 4')      
        self.addr_desc.insert_var(node.name, length-idx)

    @visitor.when(LocalNode)
    def visit(self, node:LocalNode, idx:int):
        self.symbol_table.insert_name(node.name)
        self.addr_desc.insert_var(node.name, idx)
        self.code.append(f'\taddiu $sp, $sp, -4')

    @visitor.when(AssignNode)
    def visit(self, node:AssignNode):
        rdest = self.addr_desc.get_var_reg(node.dest)
        if self.is_variable(node.source):
            rsrc = self.addr_desc.get_var_reg(node.source)
            self.code.append(f'\tmove ${rdest}, ${rsrc}') 
            self.var_address[node.dest] = self.var_address[node.source]
        elif self.is_int(node.source):
            self.code.append(f'\tli ${rdest}, {node.source}')
            self.var_address[node.dest] = AddrType.INT
        self.save_var_code(node.dest)

        
    @visitor.when(NotNode)
    def visit(self, node:NotNode):
        rdest = self.addr_desc.get_var_reg(node.dest)
        rsrc = self.save_to_register(node.expr)
        self.code.append(f'\tnot ${rdest}, ${rsrc}')
        self.code.append(f'\taddi ${rdest}, ${rdest}, 1')
        self.var_address[node.dest] = AddrType.INT
    
    @visitor.when(LogicalNotNode)
    def visit(self, node:LogicalNotNode):
        rdest = self.addr_desc.get_var_reg(node.dest)
        rsrc = self.save_to_register(node.expr)
        self.code.append(f'\tbeqz ${rsrc}, false_{self.loop_idx}')
        self.code.append(f'\tli ${rdest}, 0')
        self.code.append(f'\tj end_{self.loop_idx}')
        self.code.append(f'false_{self.loop_idx}:')
        self.code.append(f'\tli ${rdest}, 1')
        self.code.append(f'end_{self.loop_idx}:')
        self.loop_idx += 1
        self.var_address[node.dest] = AddrType.BOOL
   
    @visitor.when(PlusNode)
    def visit(self, node:PlusNode):
        rdest = self.addr_desc.get_var_reg(node.dest)
        if self.is_variable(node.left):
            rleft = self.addr_desc.get_var_reg(node.left)
            if self.is_variable(node.right):
                rright = self.addr_desc.get_var_reg(node.right)
                self.code.append(f"\tadd ${rdest}, ${rleft}, ${rright}")
            elif self.is_int(node.right):
                self.code.append(f"\taddi ${rdest}, ${rleft}, {node.right}")
        elif self.is_int(node.left):
            if self.is_int(node.right):
                self.code.append(f"\tli ${rdest}, {node.left + node.right}")
            elif self.is_variable(node.right):
                rright = self.addr_desc.get_var_reg(node.right)
                self.code.append(f"\taddi ${rdest}, ${rright}, {node.left}")
        self.var_address[node.dest] = AddrType.INT
   
    @visitor.when(MinusNode)
    def visit(self, node:MinusNode):
        rdest = self.addr_desc.get_var_reg(node.dest)
        if self.is_variable(node.left):
            rleft = self.addr_desc.get_var_reg(node.left)
            if self.is_variable(node.right):
                rright = self.addr_desc.get_var_reg(node.right)
                self.code.append(f"\tsub ${rdest}, ${rleft}, ${rright}")
            elif self.is_int(node.right):
                self.code.append(f"\taddi ${rdest}, ${rleft}, -{node.right}")
        elif self.is_int(node.left):
            if self.is_int(node.right):
                self.code.append(f"\tli ${rdest}, {node.left-node.right}")
            elif self.is_variable(node.right):
                rright = self.addr_desc.get_var_reg(node.right)
                self.code.append(f"\tsub $t9, $zero, {rright}")
                self.code.append(f"\taddi ${rdest}, {node.left}, $t9")
        self.var_address[node.dest] = AddrType.INT

    @visitor.when(StarNode)
    def visit(self, node:StarNode):
        rdest = self.addr_desc.get_var_reg(node.dest)
        if self.is_int(node.left) and self.is_int(node.right):
            try:
                self.code.append(f"\tli ${rdest}, {node.left * node.right}")
            except ZeroDivisionError:
                self.code.append('\tla $a0, zero_error')
                self.code.append('\tj .raise')
        else:
            if self.is_variable(node.left):
                rleft = self.addr_desc.get_var_reg(node.left)
                if self.is_variable(node.right):
                    rright = self.addr_desc.get_var_reg(node.right)
                elif self.is_int(node.right):
                    self.code.append(f"\tli $t9, {node.right}")
                    rright = 't9'
            elif self.is_int(node.left):
                rright = self.addr_desc.get_var_reg(node.right)
                self.code.append(f"\tli $t9, {node.left}")
                rleft = 't9'
            self.code.append(f"\tmult ${rleft}, ${rright}")
            self.code.append(f"\tmflo ${rdest}")
        self.var_address[node.dest] = AddrType.INT

    @visitor.when(DivNode)
    def visit(self, node:DivNode):
        rdest = self.addr_desc.get_var_reg(node.dest)
        if self.is_int(node.left) and self.is_int(node.right):
            try:
                self.code.append(f"\tli ${rdest}, {node.left / node.right}")
            except ZeroDivisionError:
                self.code.append('\tla $a0, zero_error')
                self.code.append('\tj .raise')
        else:
            if self.is_variable(node.left):
                rleft = self.addr_desc.get_var_reg(node.left)
                if self.is_variable(node.right):
                    rright = self.addr_desc.get_var_reg(node.right)
                elif self.is_int(node.right):
                    self.code.append(f"\tli $t9, {node.right}")
                    rright = 't9'
            elif self.is_int(node.left):
                rright = self.addr_desc.get_var_reg(node.right)
                self.code.append(f"\tli $t9, {node.left}")
                rleft = 't9'
            self.code.append('\tla $a0, zero_error')
            self.code.append(f'\tbeqz ${rright}, .raise')
            self.code.append(f"\tdiv ${rleft}, ${rright}")
            self.code.append(f"\tmflo ${rdest}")
        self.var_address[node.dest] = AddrType.INT

    @visitor.when(LessNode)
    def visit(self, node:LessNode):
        rdest = self.addr_desc.get_var_reg(node.dest)
        if self.is_variable(node.left):
            rleft = self.addr_desc.get_var_reg(node.left)
            if self.is_variable(node.right):
                rright = self.addr_desc.get_var_reg(node.right)
                self.code.append(f"\tslt ${rdest}, ${rleft}, ${rright}")
            elif self.is_int(node.right):
                self.code.append(f"\tli $t9, {node.right}")
                self.code.append(f"\tslt ${rdest}, ${rleft}, $t9")
        elif self.is_int(node.left):
            if self.is_int(node.right):
                self.code.append(f"\tli ${rdest}, {int(node.left < node.right)}")
            elif self.is_variable(node.right):
                rright = self.addr_desc.get_var_reg(node.right)
                self.code.append(f"\tli $t9, {node.left}")
                self.code.append(f"\tslt ${rdest}, $t9, ${rright}")
        self.var_address[node.dest] = AddrType.BOOL

    @visitor.when(LessEqNode)
    def visit(self, node:MinusNode):
        rdest = self.addr_desc.get_var_reg(node.dest)
        if self.is_variable(node.left):
            rleft = self.addr_desc.get_var_reg(node.left)
            if self.is_variable(node.right):
                rright = self.addr_desc.get_var_reg(node.right)
                self.code.append(f"\tsle ${rdest}, ${rleft}, ${rright}")
            elif self.is_int(node.right):
                self.code.append(f"\tli $t9, {node.right}")
                self.code.append(f"\tsle ${rdest}, ${rleft}, $t9")
        elif self.is_int(node.left):
            if self.is_int(node.right):
                self.code.append(f"\tli ${rdest}, {int(node.left <= node.right)}")
            elif self.is_variable(node.right):
                rright = self.addr_desc.get_var_reg(node.right)
                self.code.append(f"\tli $t9, {node.left}")
                self.code.append(f"\tsle ${rdest}, $t9, ${rright}")
        self.var_address[node.dest] = AddrType.BOOL

    @visitor.when(EqualNode)
    def visit(self, node:MinusNode):
        if self.is_variable(node.left) and self.is_variable(node.right) and self.var_address[node.left] == AddrType.STR and self.var_address[node.right] == AddrType.STR:
            self.compare_strings(node)
        else:
            rdest = self.addr_desc.get_var_reg(node.dest)
            if self.is_variable(node.left):
                rleft = self.addr_desc.get_var_reg(node.left)
                if self.is_variable(node.right):
                    rright = self.addr_desc.get_var_reg(node.right)
                    self.code.append(f"\tseq ${rdest}, ${rleft}, ${rright}")
                elif self.is_int(node.right):
                    self.code.append(f"\tli $t9, {node.right}")
                    self.code.append(f"\tseq ${rdest}, ${rleft}, $t9")
            elif self.is_int(node.left):
                if self.is_int(node.right):
                    self.code.append(f"\tli ${rdest}, {int(node.left == node.right)}")
                elif self.is_variable(node.right):
                    rright = self.addr_desc.get_var_reg(node.right)
                    self.code.append(f"\tli $t9, {node.left}")
                    self.code.append(f"\tseq ${rdest}, $t9, ${rright}")
            self.var_address[node.dest] = AddrType.BOOL  

    @visitor.when(GetAttribNode)
    def visit(self, node:GetAttribNode):
        rdest = self.addr_desc.get_var_reg(node.dest)
        self.var_address[node.dest] = self.get_type(node.attr_type)
        rsrc = self.addr_desc.get_var_reg(node.obj)
        attr_offset = 4*self.get_attr_offset(node.attr, node.type_name)
        self.code.append(f'\tlw ${rdest}, {attr_offset}(${rsrc})')

    @visitor.when(SetAttribNode)
    def visit(self, node:SetAttribNode):
        rdest = self.addr_desc.get_var_reg(node.obj)
        attr_offset = 4*self.get_attr_offset(node.attr, node.type_name)
        if self.is_variable(node.value):
            rsrc = self.addr_desc.get_var_reg(node.value)
        elif self.is_int(node.value):
            self.code.append(f'\tli $t9, {node.value}')
            rsrc = 't9'
        elif self.is_void(node.value):
            self.code.append(f'\tla $t9, type_Void')
            rsrc = 't9'
        self.code.append(f'\tsw ${rsrc}, {attr_offset}(${rdest})')
        
    @visitor.when(AllocateNode)
    def visit(self, node:AllocateNode):
        rdest = self.addr_desc.get_var_reg(node.dest)
        size = 4*self.obj_table.size_of_entry(node.type)
        self.var_address[node.dest] = AddrType.REF
        self.code.append('\tli $v0, 9')
        self.code.append(f'\tli $a0, {size}')
        self.code.append('\tsyscall')
        addrs_stack = self.addr_desc.get_var_addr(node.dest)
        self.code.append(f'\tla $t9, type_{node.type}')
        self.code.append(f'\tsw $t9, 0($v0)')
        self.code.append(f'\tli $t9, {size}')
        self.code.append(f'\tsw $t9, 4($v0)')
        self.code.append(f'\tmove ${rdest}, $v0')
        idx = self.types.index(node.type)
        self.code.append('\tla $t8, types')
        self.code.append(f'\tlw $v0, {4*idx}($t8)')
        self.code.append(f'\tsw $v0, 8(${rdest})')

    @visitor.when(TypeOfNode)
    def visit(self, node:TypeOfNode):
        rdest = self.addr_desc.get_var_reg(node.dest)
        if self.is_variable(node.obj):
            rsrc = self.addr_desc.get_var_reg(node.obj)
            if self.var_address[node.obj] == AddrType.REF:
                self.code.append(f'\tlw ${rdest}, 0(${rsrc})')
            elif self.var_address[node.obj] == AddrType.STR:
                self.code.append(f'\tla ${rdest}, type_String')
            elif self.var_address[node.obj] == AddrType.INT:
                self.code.append(f'\tla ${rdest}, type_Int')
            elif self.var_address[node.obj] == AddrType.BOOL:
                self.code.append(f'\tla ${rdest}, type_Bool')
        elif self.is_int(node.obj):
            self.code.append(f'\tla ${rdest}, type_Int')
        self.var_address[node.dest] = AddrType.STR

    @visitor.when(LabelNode)
    def visit(self, node:LabelNode):
        self.code.append(f'{node.label}:')

    @visitor.when(GotoNode)
    def visit(self, node:GotoNode):
        self.empty_registers()
        self.code.append(f'\tj {node.label}')

    @visitor.when(GotoIfNode)
    def visit(self, node:GotoIfNode):
        reg = self.save_to_register(node.cond)
        self.empty_registers()
        self.code.append(f'\tbnez ${reg}, {node.label}')

    @visitor.when(GotoIfFalseNode)
    def visit(self, node:GotoIfNode):
        reg = self.save_to_register(node.cond)
        self.empty_registers()
        self.code.append(f'\tbeqz ${reg}, {node.label}')

    @visitor.when(StaticCallNode)
    def visit(self, node:StaticCallNode):
        function = self.dispatch_table.find_full_name(node.type, node.function)
        self.push_register('fp')
        self.push_register('ra')
        for arg in reversed(node.args):
            self.visit(arg)
        self.empty_registers()
        self.code.append(f'\tjal {function}')
        self.pop_register('ra')
        self.pop_register('fp')
        if node.dest is not None:
            self.get_reg_var(node.dest)
            rdest = self.addr_desc.get_var_reg(node.dest)
            self.code.append(f'\tmove ${rdest}, $v0')
        self.var_address[node.dest] = self.get_type(node.return_type)

    @visitor.when(DynamicCallNode)
    def visit(self, node:DynamicCallNode):
        reg = self.addr_desc.get_var_reg(node.obj)
        self.code.append(f'\tlw $t9, 8(${reg})')
        self.code.append('\tlw $a0, 8($t9)')
        function = self.dispatch_table.find_full_name(node.type, node.method)       
        index = 4*self.dispatch_table.get_offset(node.type, function) + 4
        self.code.append(f'\tlw $t8, {index}($a0)')
        self.push_register('fp')
        self.push_register('ra')
        for arg in reversed(node.args):
            self.visit(arg)
        self.empty_registers()
        self.code.append(f'\tjal $t8')
        self.pop_register('ra')
        self.pop_register('fp')
        if node.dest is not None:
            self.get_reg_var(node.dest)
            rdest = self.addr_desc.get_var_reg(node.dest)
            self.code.append(f'\tmove ${rdest}, $v0')       
        self.var_address[node.dest] = self.get_type(node.return_type)

    @visitor.when(ArgNode)
    def visit(self, node:ArgNode):
        if self.is_variable(node.dest):
            self.get_reg_var(node.dest)
            reg = self.addr_desc.get_var_reg(node.dest)
            self.code.append(f'\tsw ${reg}, ($sp)')
        elif self.is_int(node.dest):
            self.code.append(f'\tli $t9, {node.dest}')
            self.code.append(f'\tsw $t9, ($sp)')
        self.code.append('\taddiu $sp, $sp, -4')
       
    @visitor.when(ReturnNode)
    def visit(self, node:ReturnNode):
        if self.is_variable(node.value): 
            rdest = self.addr_desc.get_var_reg(node.value)
            self.code.append(f'\tmove $v0, ${rdest}')
        elif self.is_int(node.value):
            self.code.append(f'\tli $v0, {node.value}')
        self.empty_registers()
        self.code.append(f'\taddiu $sp, $sp, {self.locals*4}')
        self.code.append(f'\tjr $ra')
        self.code.append('')

    @visitor.when(LoadNode)
    def visit(self, node:LoadNode):
        rdest = self.addr_desc.get_var_reg(node.dest)
        self.var_address[node.dest] = AddrType.STR
        self.code.append(f'\tla ${rdest}, {node.msg}')
    
    @visitor.when(LengthNode)
    def visit(self, node: LengthNode):
        rdest = self.addr_desc.get_var_reg(node.dest)
        reg = self.addr_desc.get_var_reg(node.arg)
        loop = f'loop_{self.loop_idx}'
        end = f'end_{self.loop_idx}'
        self.code.append(f'\tmove $t8, ${reg}')
        self.code.append(f'{loop}:')
        self.code.append(f'\tlb $t9, 0($t8)')
        self.code.append(f'\tbeq $t9, $zero, {end}')
        self.code.append(f'\taddi $t8, $t8, 1')
        self.code.append(f'\tj {loop}')
        self.code.append(f'{end}:')
        self.code.append(f'\tsub ${rdest}, $t8, ${reg}')
        self.loop_idx += 1

    @visitor.when(ConcatNode)
    def visit(self, node: ConcatNode):
        rdest = self.addr_desc.get_var_reg(node.dest)
        self.code.append('\tli $a0, 356')
        self.code.append('\tli $v0, 9')
        self.code.append('\tsyscall')
        self.code.append(f'\tmove ${rdest}, $v0')
        rsrc1 = self.addr_desc.get_var_reg(node.arg1)
        if node.arg2 is not None:
            rsrc2 = self.addr_desc.get_var_reg(node.arg2)
        var = self.save_reg_if_occupied('a1')
        self.code.append(f'\tmove $a0, ${rsrc1}')
        self.code.append(f'\tmove $a1, ${rdest}')
        self.push_register('ra')
        self.code.append('\tjal strcopier')
        if node.arg2 is not None:
            self.code.append(f'\tmove $a0, ${rsrc2}')
            self.code.append(f'\tmove $a1, $v0')
            self.code.append('\tjal strcopier')
        self.code.append('\tsb $0, 0($v0)')
        self.pop_register('ra')
        self.code.append(f'\tj finish_{self.loop_idx}')

        if self.first_defined['strcopier']:
            self.code.append('strcopier:')
            self.code.append(f'loop_{self.loop_idx}:')
            self.code.append('\tlb $t8, ($a0)')
            self.code.append(f'\tbeq $t8, $zero, end_{self.loop_idx}')
            self.code.append('\taddiu $a0, $a0, 1')
            self.code.append('\tsb $t8, ($a1)')
            self.code.append('\taddiu $a1, $a1, 1')
            self.code.append(f'\tb loop_{self.loop_idx}')
            self.code.append(f'end_{self.loop_idx}:')
            self.code.append('\tmove $v0, $a1')
            self.code.append('\tjr $ra')
            self.first_defined['strcopier'] = False 
        self.code.append(f'finish_{self.loop_idx}:')
        self.load_var_if_occupied(var)
        self.loop_idx += 1

    @visitor.when(SubstringNode)
    def visit(self, node: SubstringNode):
        rdest = self.addr_desc.get_var_reg(node.dest)
        self.code.append('\tli $a0, 356')
        self.code.append('\tli $v0, 9')
        self.code.append('\tsyscall')
        self.code.append(f'\tmove ${rdest}, $v0')
        if self.is_variable(node.begin):
            rstart = self.addr_desc.get_var_reg(node.begin)
        elif self.is_int(node.begin):
            rstart = 't8'
            self.code.append(f'\tli $t8, {node.begin}')
        if self.is_variable(node.end):
            rend = self.addr_desc.get_var_reg(node.end)
            var = None
        elif self.is_int(node.end):
            var = self.save_reg_if_occupied('a3')
            rend = 'a3'
            self.code.append(f'\tli $a3, {node.end}')
        self.get_reg_var(node.word)
        rself = self.addr_desc.get_var_reg(node.word)        
        start = f'start_{self.loop_idx}'
        error = f'error_{self.loop_idx}'
        end_lp = f'end_len_{self.loop_idx}'        
        self.code.append('\tli $v0, 0')
        self.code.append(f'\tmove $t8, ${rself}')
        self.code.append(f'{start}:')
        self.code.append('\tlb $t9, 0($t8)')
        self.code.append(f'\tbeqz $t9, {error}')
        self.code.append('\taddi $v0, 1')
        self.code.append(f'\tbgt $v0, ${rstart}, {end_lp}')
        self.code.append(f'\taddi $t8, 1')
        self.code.append(f'\tj {start}')
        self.code.append(f'{end_lp}:')        
        self.code.append(f'\tmove $v0, ${rdest}')
        loop = f'loop_{self.loop_idx}'
        end = f'end_{self.loop_idx}'        
        self.code.append(f'{loop}:')
        self.code.append(f'\tsub $t9, $v0, ${rdest}') 
        self.code.append(f'\tbeq $t9, ${rend}, {end}')
        self.code.append(f'\tlb $t9, 0($t8)')
        self.code.append(f'\tbeqz $t9, {error}')        
        self.code.append(f'\tsb $t9, 0($v0)')
        self.code.append('\taddi $t8, $t8, 1')
        self.code.append(f'\taddi $v0, $v0, 1')
        self.code.append(f'\tj {loop}')
        self.code.append(f'{error}:')
        self.code.append('\tla $a0, index_error')        
        self.code.append('\tli $v0, 4')
        self.code.append(f'\tmove $a0, ${rself}')
        self.code.append('\tsyscall')        
        self.code.append('\tli $v0, 1')
        self.code.append(f'\tmove $a0, ${rstart}')
        self.code.append('\tsyscall')        
        self.code.append('\tli $v0, 1')
        self.code.append(f'\tmove $a0, ${rend}')
        self.code.append('\tsyscall')        
        self.code.append('\tj .raise')
        self.code.append(f'{end}:')
        self.code.append('\tsb $0, 0($v0)')
        self.load_var_if_occupied(var)
        self.loop_idx += 1

    @visitor.when(OutStringNode)
    def visit(self, node: OutStringNode):
        reg = self.addr_desc.get_var_reg(node.value)        
        self.code.append('\tli $v0, 4')
        self.code.append(f'\tmove $a0, ${reg}')
        self.code.append('\tsyscall')

    @visitor.when(OutIntNode)
    def visit(self, node: OutIntNode):
        if self.is_variable(node.value):
            reg = self.addr_desc.get_var_reg(node.value)
        elif self.is_int(node.value):
            reg = 't8'
            self.code.append(f'\tli $t8, ${node.value}')
        self.code.append('\tli $v0, 1')
        self.code.append(f'\tmove $a0, ${reg}')
        self.code.append('\tsyscall')
    
    @visitor.when(ReadStringNode)
    def visit(self, node: ReadStringNode):      
        rdest = self.addr_desc.get_var_reg(node.dest)       
        self.code.append('\tli $a0, 356')
        self.code.append('\tli $v0, 9')
        self.code.append('\tsyscall')
        self.code.append(f'\tmove ${rdest}, $v0')       
        var = self.save_reg_if_occupied('a1')        
        self.code.append(f'\tmove $a0, ${rdest}')        
        self.code.append(f'\tli $a1, 356')             
        self.code.append('\tli $v0, 8')
        self.code.append('\tsyscall')     
        start = f'start_{self.loop_idx}'
        end = f'end_{self.loop_idx}'
        self.code.append(f'\tmove $t9, ${rdest}')
        self.code.append(f'{start}:')
        self.code.append('\tlb $t8, 0($t9)')
        self.code.append(f"\tbeqz $t8, {end}")
        self.code.append('\tadd $t9, $t9, 1')
        self.code.append(f'\tj {start}')
        self.code.append(f'{end}:')
        self.code.append('\taddiu $t9, $t9, -1')
        self.code.append('\tsb $0, ($t9)')
        self.loop_idx += 1
        self.load_var_if_occupied(var)

    @visitor.when(ReadIntNode)
    def visit(self, node: ReadIntNode):
        rdest = self.addr_desc.get_var_reg(node.dest)   
        self.code.append('\tli $v0, 5')
        self.code.append('\tsyscall')
        self.code.append(f'\tmove ${rdest}, $v0')

    @visitor.when(ExitNode)
    def visit(self, node: ExitNode):
        if self.is_variable(node.value):
            reg = self.addr_desc.get_var_reg(node.value)
        elif self.is_int(node.value):
            reg = 't8'
            self.code.append(f'\tli $t8, {node.value}')
        rself = self.addr_desc.get_var_reg(node.classx)
        if self.var_address[node.classx] == AddrType.REF:        
            self.code.append('\tli $v0, 4')
            self.code.append(f'\tla $a0, abort_msg')
            self.code.append('\tsyscall')
            self.code.append('\tli $v0, 4')
            self.code.append(f'\tlw $a0, 0(${rself})')
            self.code.append('\tsyscall')    
            self.code.append('\tli $v0, 4')
            self.code.append(f'\tla $a0, new_line')
            self.code.append('\tsyscall')      
        self.code.append('\tli $v0, 17')
        self.code.append(f'\tmove $a0, ${reg}')
        self.code.append('\tsyscall')

    @visitor.when(CopyNode)
    def visit(self, node: CopyNode):
        rdest = self.addr_desc.get_var_reg(node.dest)
        rsrc = self.addr_desc.get_var_reg(node.source)
        self.code.append(f'\tlw $t9, 4(${rsrc})')
        self.code.append('\tli $v0, 9')
        self.code.append(f'\tmove $a0, $t9')
        self.code.append('\tsyscall')
        self.code.append(f'\tmove ${rdest}, $v0')
        self.code.append('\tli $t8, 0')
        self.code.append(f'loop_{self.loop_idx}:')
        self.code.append(f'\tbge $t8, $t9, exit_{self.loop_idx}')
        self.code.append(f'\tlw $a0, (${rsrc})')
        self.code.append('\tsw $a0, ($v0)')
        self.code.append('\taddi $v0, $v0, 4')
        self.code.append(f'\taddi ${rsrc}, ${rsrc}, 4')
        self.code.append('\taddi $t8, $t8, 4')
        self.code.append(f'\tj loop_{self.loop_idx}')
        self.code.append(f'exit_{self.loop_idx}:')
        self.loop_idx += 1

    @visitor.when(ConformsNode)
    def visit(self, node: ConformsNode):
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
        self.code.append(f'\tla $a0, {node.type}')
        self.code.append('\tj .raise')

    @visitor.when(VoidConstantNode)
    def visit(self, node:VoidConstantNode):
        rdest = self.addr_desc.get_var_reg(node.out)
        self.code.append(f'\tli $a0, 4')
        self.code.append('\tli $v0, 9')
        self.code.append('\tsyscall')
        self.code.append(f'\tla $t9, type_Void')
        self.code.append('\tsw $t9, 0($v0)')
        self.code.append(f'\tmove ${rdest}, $v0')
        self.var_address[node.obj] = AddrType.REF
     
    @visitor.when(BoxingNode)
    def visit(self, node:BoxingNode):
        "Node to convert a value type into object"
        rdest = self.addr_desc.get_var_reg(node.dest)
        self.code.append('\tli $a0, 12')
        self.code.append('\tli $v0, 9')
        self.code.append('\tsyscall')
        self.code.append(f'\tla $t9, type_{node.type}')
        self.code.append('\tsw $t9, 0($v0)')
        self.code.append('\tli $t9, 12')
        self.code.append('\tsw $t9, 4($v0)')
        self.code.append(f'\tmove ${rdest}, $v0')
        idx = self.types.index('Object')
        self.code.append('\tla $t8, types')
        self.code.append(f'\tlw $v0, {4*idx}($t8)')
        self.code.append(f'\tsw $v0, 8(${rdest})')
        self.var_address[node.dest] = AddrType.REF

    def initialize_methods(self):
        self.methods = [] 
        for entry in self.obj_table:
            entry: ObjTabEntry
            self.methods.extend(entry.dispatch_table_entry)

    def initialize_data_code(self):
        self.data_code = ['\t.data'] 

    def initialize_runtime_errors(self):
        self.code.append('.raise:')
        self.code.append('\tli $v0, 4')
        self.code.append('\tsyscall')
        self.code.append('\tli $v0, 17')
        self.code.append('\tli $a0, 1')
        self.code.append('\tsyscall\n')

        self.data_code.append('zero_error: .asciiz \"Division by zero error\\n\"')
        self.data_code.append('case_void_error: .asciiz \"Case on void error\\n\"')
        self.data_code.append('dispatch_error: .asciiz \"Dispatch on void error\\n\"'  )
        self.data_code.append('case_error: .asciiz \"Case statement without a matching branch error\\n\"'  )
        self.data_code.append('index_error: .asciiz \"Substring out of range error\\n\"')
        self.data_code.append('heap_error: .asciiz \"Heap overflow error\n\"')


    def load_abort_messages(self):
        self.data_code.append("abort_msg: .asciiz \"Abort called from class \"")                    
        self.data_code.append(f"new_line: .asciiz \"\\n\"")                   
        self.data_code.append('string_abort: .asciiz \"Abort called from class String\\n\"')
        self.data_code.append('int_abort: .asciiz \"Abort called from class Int\\n\"')
        self.data_code.append('bool_abort: .asciiz \"Abort called from class Bool\\n\"')


    def get_basic_blocks(self, instructions: List[InstructionNode]):
        leaders = self.find_leaders(instructions)
        blocks = [instructions[leaders[i-1]:leaders[i]] for i in range(1, len(leaders))]
        return blocks


    def find_leaders(self, instructions: List[InstructionNode]):
        leaders = {0, len(instructions)}
        for i, inst in enumerate(instructions):
            if isinstance(inst, GotoNode) or isinstance(inst, GotoIfNode) or isinstance(inst, ReturnNode) \
                or isinstance(inst, StaticCallNode) or isinstance(inst, DynamicCallNode):
                leaders.add(i+1)
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

    def construct_next_use(self, basic_blocks: List[List[InstructionNode]]):
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
        var_st = self.symbol_table.lookup(var)
        register = self.reg_desc.find_empty_reg()
        if register is not None:
            self.update_register(var, register)
            self.load_var_code(var)
            return register
        next_use = self.next_use[inst.index]
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
        "Code to save a variable to memory"
        memory, register, _= self.addr_desc.get_var_storage(var)
        self.code.append(f"\tsw ${register}, -{memory}($fp)")

    def load_var_code(self, var):
        "Code to load a variable from memory"
        memory, register, _ = self.addr_desc.get_var_storage(var)
        self.code.append(f'\tlw ${register}, -{memory}($fp)')

    def empty_registers(self, save=True):
        registers = self.reg_desc.used_registers()
        for reg, var in registers: 
            if save:
                self.save_var_code(var)
            self.addr_desc.set_var_reg(var, None)
            self.reg_desc.insert_register(reg, None)     

    def push_register(self, register):
        self.code.append(f'\tsw ${register}, ($sp)')    
        self.code.append('\taddiu $sp, $sp, -4')

    def pop_register(self, register):
        self.code.append('\taddiu $sp, $sp, 4')   
        self.code.append(f'\tlw ${register}, ($sp)')    

    def save_to_register(self, expr):
        if self.is_int(expr):
            self.code.append(f'\tli $t9, {expr}')
            return 't9'
        elif self.is_variable(expr):
            return self.addr_desc.get_var_reg(expr)

    def get_attr_offset(self, attr_name:str, type_name:str):
        return self.obj_table[type_name].attr_offset(attr_name)

    def get_method_offset(self, type_name, method_name):
        self.obj_table[type_name].method_offset(method_name)

    def save_meth_addr(self, func_nodes: List[FunctionNode]):
        self.methods += [funct.name for funct in func_nodes]
        words = 'methods: .word ' + ', '.join(map(lambda x: '0', self.methods))
        self.data_code.append(words)
        self.code.append('\tla $v0, methods')
        for i, meth in enumerate(self.methods):
            self.code.append(f'\tla $t9, {meth}')
            self.code.append(f'\tsw $t9, {4*i}($v0)')

    def save_types_addr(self, type_nodes: List[FunctionNode]):
        words = 'types: .word ' + ', '.join(map(lambda x: '0', self.inherit_graph))
        self.data_code.append(words)
        self.code.append('\tla $t9, types')
        self.types = []
        for i, (ntype, nparent) in enumerate(self.inherit_graph.items()):
            self.code.append('\tli $v0, 9')
            self.code.append(f'\tli $a0, 12')      
            self.code.append('\tsyscall')
            self.types.append(ntype)
            self.code.append(f'\tla $t8, type_{ntype}')
            self.code.append(f'\tsw $t8, 0($v0)')
            self.code.append(f'\tsw $v0, {4*i}($t9)')
            self.code.append('\tmove $t8, $v0')
            self.create_dispatch_table(ntype)
            self.code.append('\tsw $v0, 8($t8)')
        for i, ntype in enumerate(self.types):
            self.code.append(f'\tlw $v0, {4*i}($t9)')
            nparent = self.inherit_graph[ntype]
            if nparent is not None:
                parent_idx = self.types.index(nparent)

                self.code.append(f'\tlw $t8, {4*parent_idx}($t9)')
            else:
                self.code.append('\tli $t8, 0')
            self.code.append('\tsw $t8, 4($v0)')

    def create_dispatch_table(self, type_name):
        methods = self.dispatch_table.get_methods(type_name)
        self.code.append('\tli $v0, 9')
        dispatch_table_size = 4*len(methods)
        self.code.append(f'\tli $a0, {dispatch_table_size+4}')
        self.code.append('\tsyscall')
        
        var = self.save_reg_if_occupied('v1')

        self.code.append('\tla $v1, methods')
        for i, meth in enumerate(methods, 1):
            offset = 4*self.methods.index(meth)
            self.code.append(f'\tlw $a0, {offset}($v1)')
            self.code.append(f'\tsw $a0, {4*i}($v0)')       
        self.load_var_if_occupied(var)

    def get_type(self, xtype):
        'Return the var address type according to its static type'
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
            self.save_var_code(var)
        return var
    
    def load_var_if_occupied(self, var):
        if var is not None:
            self.load_var_code(var)

    def compare_strings(self, node: EqualNode):
        rdest = self.addr_desc.get_var_reg(node.dest)
        rleft = self.addr_desc.get_var_reg(node.left)
        rright = self.addr_desc.get_var_reg(node.right)

        var = self.save_reg_if_occupied('a1')
        loop_idx = self.loop_idx
        
        self.code.append(f'\tmove $t8, ${rleft}')
        self.code.append(f'\tmove $t9, ${rright}')
        self.code.append(f'loop_{loop_idx}:')
        self.code.append(f'\tlb $a0, ($t8)')
        self.code.append(f'\tlb $a1, ($t9)')
        self.code.append(f'\tbeqz $a0, check_{loop_idx}') 
        self.code.append(f'\tbeqz $a1, mismatch_{loop_idx}')
        self.code.append('\tseq $v0, $a0, $a1')
        self.code.append(f'\tbeqz $v0, mismatch_{loop_idx}')
        self.code.append('\taddi $t8, $t8, 1')
        self.code.append('\taddi $t9, $t9, 1')                        
        self.code.append(f'\tj loop_{loop_idx}')
        
        self.code.append(f'mismatch_{loop_idx}:')
        self.code.append('\tli $v0, 0')
        self.code.append(f'\tj end_{loop_idx}')
        self.code.append(f'check_{loop_idx}:')
        self.code.append(f'\tbnez $a1, mismatch_{loop_idx}')
        self.code.append('\tli $v0, 1')
        self.code.append(f'end_{loop_idx}:')
        self.code.append(f'\tmove ${rdest}, $v0')
        self.load_var_if_occupied(var)
        self.loop_idx += 1

    def conforms_to(self, rsrc, rdest, type_name):
        "Returns if the object in rsrc conforms to type_name"
        self.code.append(f'\tla $t9, type_{type_name}')

        loop_idx = self.loop_idx
        self.code.append(f'\tlw $v0, 8(${rsrc})')
        self.code.append(f'loop_{loop_idx}:')
        self.code.append(f'\tmove $t8, $v0')
        self.code.append(f'\tbeqz $t8, false_{loop_idx}')
        self.code.append('\tlw $v1, 0($t8)')
        self.code.append(f'\tbeq $t9, $v1, true_{loop_idx}')
        self.code.append('\tlw $v0, 4($t8)')
        self.code.append(f'\tj loop_{loop_idx}')

        self.code.append(f'true_{loop_idx}:')
        self.code.append(f'\tli ${rdest}, 1')
        self.code.append(f'\tj end_{loop_idx}')
        self.code.append(f'false_{loop_idx}:')
        self.code.append(f'\tli ${rdest}, 0')
        self.code.append(f'end_{loop_idx}:')
        self.loop_idx += 1

    def value_conforms_to_obj(self, rdest, typex, branch_type):
        true_label = f'true_{self.loop_idx}'
        end_label = f'end_{self.loop_idx}'
        self.code.append('\tla $t9, type_Object')
        self.code.append(f'\tla $t8, type_{branch_type}')
        self.code.append(f'beq $t9, $t8, {true_label}')
        self.code.append(f'\tla $t9, type_{typex}')
        self.code.append(f'beq $t9, $t8, {true_label}')
        self.code.append(f'\tli ${rdest}, 0')
        self.code.append(f'\tj {end_label}')
        self.code.append(f'{true_label}:')
        self.code.append(f'\tli ${rdest}, 1')
        self.code.append(f'{end_label}:')
        self.loop_idx += 1
