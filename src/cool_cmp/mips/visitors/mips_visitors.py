from typing import List
from mips.ast.mips_ast import *
import cmp.visitor as visitor
import cool.ast.cil_ast as cil
from mips.error.errors import MetaCILInvalidError
from mips.registers import Reg

class MIPSPrintVisitor():

    def __init__(self) -> None:
        self.lines = []
    
    def add_comments(self, node:Node):
        if node.comment:
            if isinstance(node.comment, str):
                self.add_line(f"# {node.comment}")
            else:
                for comment in node.comment:
                    self.add_line(f"# {comment}")
    
    def add_line(self, line=""):
        self.lines.append(line)
    
    @visitor.on('node')
    def visit(self, node):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node:ProgramNode):
        self.add_comments(node)
        self.add_line(".text")
        for n in node.instructions:
            self.add_comments(n)
            instr = self.visit(n)
            self.add_line(instr)
        self.add_line(".data")
        for n in node.data:
            self.add_comments(n)
            instr = self.visit(n)
            self.add_line(instr)
        return '\n'.join(self.lines)
    
    @visitor.when(DataNode)
    def visit(self, node:DataNode):
        return f"{node.name}: {node.type} {', '.join([str(x) for x in node.values])}"
    
    @visitor.when(AddNode)
    def visit(self, node:AddNode):
        return f"add {node.result}, {node.first_arg}, {node.second_arg}"
    
    @visitor.when(SubstractNode)
    def visit(self, node:SubstractNode):
        return f"sub {node.result}, {node.first_arg}, {node.second_arg}"
    
    @visitor.when(AddImmediateNode)
    def visit(self, node:AddImmediateNode):
        return f"addi {node.result}, {node.first_arg}, {node.second_arg}"
    
    @visitor.when(AddUnsignedNode)
    def visit(self, node:AddUnsignedNode):
        return f"addu {node.result}, {node.first_arg}, {node.second_arg}"
    
    @visitor.when(SubstractUnsignedNode)
    def visit(self, node:SubstractUnsignedNode):
        return f"subu {node.result}, {node.first_arg}, {node.second_arg}"
    
    @visitor.when(AddImmediateUnsignedNode)
    def visit(self, node:AddImmediateUnsignedNode):
        return f"addiu {node.result}, {node.first_arg}, {node.second_arg}"
    
    @visitor.when(MultiplyNoOverflowNode)
    def visit(self, node:MultiplyNoOverflowNode):
        return f"mul {node.result}, {node.first_arg}, {node.second_arg}"
    
    @visitor.when(AndNode)
    def visit(self, node:AndNode):
        return f"and {node.result}, {node.first_arg}, {node.second_arg}"
    
    @visitor.when(OrNode)
    def visit(self, node:OrNode):
        return f"or {node.result}, {node.first_arg}, {node.second_arg}"
    
    @visitor.when(AndImmediateNode)
    def visit(self, node:AndImmediateNode):
        return f"andi {node.result}, {node.first_arg}, {node.second_arg}"
    
    @visitor.when(OrImmediateNode)
    def visit(self, node:OrImmediateNode):
        return f"ori {node.result}, {node.first_arg}, {node.second_arg}"
    
    @visitor.when(ShiftLeftNode)
    def visit(self, node:ShiftLeftNode):
        return f"sll {node.result}, {node.first_arg}, {node.second_arg}"
    
    @visitor.when(ShiftRightNode)
    def visit(self, node:ShiftLeftNode):
        return f"srl {node.result}, {node.first_arg}, {node.second_arg}"
    
    @visitor.when(MultiplyOverflowNode)
    def visit(self, node:MultiplyOverflowNode):
        return f"mult {node.first_arg}, {node.second_arg}"
    
    @visitor.when(DivideOverflowNode)
    def visit(self, node:DivideOverflowNode):
        return f"div {node.first_arg}, {node.second_arg}"
    
    @visitor.when(LoadWordNode)
    def visit(self, node:LoadWordNode):
        return f"lw {node.dest}, {node.offset}({node.base_source_dir})"
    
    @visitor.when(StoreWordNode)
    def visit(self, node:StoreWordNode):
        return f"sw {node.source}, {node.offset}({node.base_dest_dir})"

    @visitor.when(LoadAddressNode)
    def visit(self, node:LoadAddressNode):
        return f"la {node.dest}, {node.label}"

    @visitor.when(LoadImmediateNode)
    def visit(self, node:LoadImmediateNode):
        return f"li {node.dest}, {node.value}"
    
    @visitor.when(MoveFromHiNode)
    def visit(self, node:MoveFromHiNode):
        return f"mfhi {node.dest}"
    
    @visitor.when(MoveFromLoNode)
    def visit(self, node:MoveFromLoNode):
        return f"mflo {node.dest}"
    
    @visitor.when(MoveNode)
    def visit(self, node:MoveNode):
        return f"move {node.dest}, {node.source}"
    
    @visitor.when(BranchEqualNode)
    def visit(self, node:BranchEqualNode):
        return f"beq {node.first_arg}, {node.second_arg}, {node.address}"
    
    @visitor.when(BranchNotEqualNode)
    def visit(self, node:BranchNotEqualNode):
        return f"bne {node.first_arg}, {node.second_arg}, {node.address}"
    
    @visitor.when(BranchGreaterNode)
    def visit(self, node:BranchGreaterNode):
        return f"bgt {node.first_arg}, {node.second_arg}, {node.address}"
    
    @visitor.when(BranchGreaterEqualNode)
    def visit(self, node:BranchGreaterEqualNode):
        return f"bge {node.first_arg}, {node.second_arg}, {node.address}"
    
    @visitor.when(BranchLessNode)
    def visit(self, node:BranchLessNode):
        return f"blt {node.first_arg}, {node.second_arg}, {node.address}"
    
    @visitor.when(BranchLessEqualNode)
    def visit(self, node:BranchLessEqualNode):
        return f"ble {node.first_arg}, {node.second_arg}, {node.address}"
    
    @visitor.when(SetLessThanNode)
    def visit(self, node:SetLessThanNode):
        return f"slt {node.first_arg}, {node.second_arg}, {node.result}"
    
    @visitor.when(SetLessThanImmediateNode)
    def visit(self, node:SetLessThanNode):
        return f"slti {node.first_arg}, {node.second_arg}, {node.result}"
    
    @visitor.when(JumpNode)
    def visit(self, node:JumpNode):
        return f"j {node.address}"
    
    @visitor.when(JumpRegisterNode)
    def visit(self, node:JumpRegisterNode):
        return f"jr {node.register}"
    
    @visitor.when(JumpAndLinkNode)
    def visit(self, node:JumpAndLinkNode):
        return f"jal {node.address}"

    @visitor.when(SyscallNode)
    def visit(self, node:SyscallNode):
        return f"syscall"
    
    @visitor.when(LabelNode)
    def visit(self, node:LabelNode):
        return f"{node.label}:"
    
    # @visitor.when(PrintIntNode)
    # def visit(self, node:PrintIntNode):
    #     return f"print_int"
    
    # @visitor.when(PrintStringNode)
    # def visit(self, node:PrintStringNode):
    #     return f"print_string"
    
    # @visitor.when(ReadIntNode)
    # def visit(self, node:ReadIntNode):
    #     return f"read_int"
    
    # @visitor.when(ReadStringNode)
    # def visit(self, node:ReadStringNode):
    #     return f"read_string"
    
    # @visitor.when(ExitNode)
    # def visit(self, node:ExitNode):
    #     return f"exit2"

class CILToMIPSVisitor(): # TODO Complete the transition
    
    WORD_SIZE = 4
    TO_METHODS_OFFSET = 8 # 4 Father, 4 Instance Size, METHODS
    MAX_STRING_LENGTH = 1024 # Max amount reserved when a read system call is made
    
    def __init__(self, errors=[]) -> None:
        self.errors = errors
        self.program_node = None
        self.current_function = None
        self.method_dict_name = {} # Maps Type and COOL Method name to CIL function name
        self.local_variable_offset = {} # Maps CIL local variable frame pointer offset 
        self.type_method_dict_list = {} # Maps Type name to list of tuple(COOL Name, CIL Name)
 
    def _push(self, registers: List[str]):
        """
        Push the registers in order into the stack
        """
        self._allocate_stack_space(4*len(registers))
        for i,reg in enumerate(registers):
            self.add_instruction(StoreWordNode(reg, i*4, Reg.sp()))

    def _pop(self, registers: List[str]):
        """
        Pop the registers in order from the stack
        """
        for i,reg in enumerate(registers):
            self.add_instruction(LoadWordNode(reg, i*4, Reg.sp()))
        self._deallocate_stack_space(4*len(registers))
    
    def _allocate_stack_space(self, bytes_amount: int):
        self.add_instruction(AddImmediateUnsignedNode(Reg.sp(), Reg.sp(), -bytes_amount))

    def _deallocate_stack_space(self, bytes_amount: int):
        self.add_instruction(AddImmediateUnsignedNode(Reg.sp(), Reg.sp(), bytes_amount))

    def _load_local_variable(self, dest, name):
        self.add_instruction(LoadWordNode(dest, self.local_variable_offset[name], Reg.fp())) # Stack address for local variable

    def _load_type_variable(self, dest, name):
        self.add_instruction(LoadAddressNode(dest, name))

    def _store_local_variable(self, source, name_or_value):
        try:
            # Int literal
            int_value = int(name_or_value)
            self.add_instruction(AddImmediateNode(source, Reg.zero(), int_value))
        except ValueError:
            # Variable
            self.add_instruction(StoreWordNode(source, self.local_variable_offset[name_or_value], Reg.fp())) # Stores allocated memory address in destination variable

    def _call_with_register(self, register):
        self.add_instruction(JumpRegisterNode(register))
    
    def _add_copy_function(self):
        """
        Function that copies the instance passed in $a0 and returns the copy address
        in $v0 
        """
        
        self.add_instruction(LabelNode("__copy"))
        
        self.add_instruction(MoveNode(Reg.t(0), Reg.a(0)))
        self.add_instruction(LoadWordNode(Reg.t(1), 0, Reg.t(0))) # t1 = instance type dir
        self.add_instruction(LoadWordNode(Reg.a(0), self.WORD_SIZE, Reg.t(1))) # a0 = instance size
        self._allocate_heap_space(Reg.a(0)) # v0 = allocated space
        
        start_label_name = "__start_copy_loop"
        end_label_name = "__end_copy_loop"
        
        self.add_instruction(MoveNode(Reg.t(1), Reg.a(0)))
        self.add_instruction(MoveNode(Reg.t(3), Reg.v(0)))
        
        self.add_instruction(LabelNode(start_label_name))
        self.add_instruction(BranchLessEqualNode(Reg.t(1), Reg.zero(), end_label_name))
        
        self.add_instruction(LoadWordNode(Reg.t(2), 0, Reg.t(0)))
        self.add_instruction(StoreWordNode(Reg.t(2), 0, Reg.t(3)))
        self.add_instruction(AddImmediateNode(Reg.t(0), Reg.t(0), 4))
        self.add_instruction(AddImmediateNode(Reg.t(3), Reg.t(3), 4))
        self.add_instruction(AddImmediateNode(Reg.t(1), Reg.t(1), -1))
        
        self.add_instruction(JumpNode(start_label_name))
        self.add_instruction(LabelNode(end_label_name))
        
        self.add_instruction(JumpRegisterNode(Reg.ra()))
        
    def _add_get_ra_function(self):
        """
        Adds a function that returns in $v0 2 instructions after the caller instruction
        """
        self.add_instruction(LabelNode("__get_ra"))
        self.add_instruction(MoveNode(Reg.v(0), Reg.ra()))
        self.add_instruction(AddImmediateNode(Reg.v(0), Reg.v(0), 2*self.WORD_SIZE))
        self.add_instruction(JumpRegisterNode(Reg.ra()))
    
    def _load_value(self, dest1, value1):
        """
        Returns in register `dest1` the value of `value1`
        """
        try:
            value = int(value1)
            self.add_instruction(LoadImmediateNode(dest1, value))
        except ValueError:
            try:
                self._load_local_variable(dest1, value1)
            except KeyError:
                self._load_type_variable(dest1, value1)
    
    def _binary_operation(self, node: cil.ArithmeticNode, instruction_type, reg1, reg2, temp_reg):        
        self._load_value(reg1, node.left)
        self._load_value(reg2, node.right)
        self.add_instruction(instruction_type(temp_reg, reg1, reg2))
        self._store_local_variable(temp_reg, node.dest)
    
    def _allocate_heap_space(self, reg_with_amount):
        """
        Stores in `a0` the `reg_with_amount` and makes a system call
        to reserve space. The reserve space address will be in `v0`
        """
        if reg_with_amount != Reg.a(0):
            self.add_instruction(MoveNode(Reg.a(0), reg_with_amount)) # Saves in $a0 the bytes size for current type
        self.add_instruction(LoadImmediateNode(Reg.v(0), 9)) # Reserve space arg
        self.add_instruction(SyscallNode()) # Returns in $v0 the allocated memory
    
    def add_instruction(self, instr:Node):
        self.program_node.instructions.append(instr)
    
    def add_data(self, data: DataNode):
        self.program_node.data.append(data)
    
    @visitor.on('node')
    def visit(self, node):
        pass
    
    @visitor.when(cil.ProgramNode)
    def visit(self, node:cil.ProgramNode):
     
        for type_node in node.dottypes:
            self.type_method_dict_list[type_node.name] = type_node.methods.copy()
            for method,static_method in type_node.methods:
                self.method_dict_name[type_node.name, method] = static_method
        
        program = ProgramNode("Genereted MIPS")
        self.program_node = program

        self._add_get_ra_function()
        self._add_copy_function()

        for function in node.dotcode:
            self.current_function = function
            self.visit(function)
        
        self.current_function = None
        
        for typex in node.dottypes:
            self.visit(typex)

        for data in node.dotdata:
            self.visit(data)

        return program

    @visitor.when(cil.FunctionNode)
    def visit(self, node:cil.FunctionNode):
        
        self.local_variable_offset = {}
        
        self.add_instruction(LabelNode(node.name))
        allocated_space = len(node.localvars) * self.WORD_SIZE # When a function is called the stack already contains all the params 
        self._allocate_stack_space(allocated_space)
        offset = 0
        
        for local in node.localvars + node.params[::-1]: # Params in reverse order
            self.local_variable_offset[local.name] = offset
            offset += self.WORD_SIZE
            
        self.add_instruction(MoveNode(Reg.t(0), Reg.sp())) # Temporary save fp
        saved_registers = [Reg.ra(), Reg.fp()] # + [Reg.s(i) for i in range(8)]
        self._push(saved_registers)
        self.add_instruction(MoveNode(Reg.fp(), Reg.t(0))) # Set fp to value that matches with the offsets

        for instr in node.instructions:
            self.visit(instr)
        
        self._pop(saved_registers)
        self._deallocate_stack_space(allocated_space + len(node.params) * self.WORD_SIZE) # Deallocate also the params
        self.add_instruction(JumpRegisterNode(Reg.ra()))
    
    @visitor.when(cil.ReturnNode)
    def visit(self, node:cil.ReturnNode):
        if node.value:
            self._store_local_variable(Reg.v(0), node.value)
    
    @visitor.when(cil.AllocateNode)
    def visit(self, node:cil.AllocateNode):
        if node.type[0].isupper(): # Is a Type name
            self.add_instruction(LoadAddressNode(Reg.a(0), node.type)) # Type address into $a0
        else:
            self._load_local_variable(Reg.a(0), node.type)
        self.add_instruction(LoadWordNode(Reg.a(0), self.WORD_SIZE, Reg.a(0))) # Saves in $a0 the bytes size for current type
        self._allocate_heap_space(Reg.a(0))
        self._store_local_variable(Reg.v(0), node.dest)

    @visitor.when(cil.AbortNode)
    def visit(self, node:cil.AbortNode):
        self.add_instruction(AddImmediateNode(Reg.v(0), Reg.zero(), 10)) # 10 System call code for abort
        self.add_instruction(SyscallNode())
    
    @visitor.when(cil.StaticCallNode)
    def visit(self, node:cil.StaticCallNode):
        self.add_instruction(JumpAndLinkNode(node.function)) # Jumps to label
        self._store_local_variable(Reg.v(0), node.dest)
        
    @visitor.when(cil.DynamicCallNode)
    def visit(self, node:cil.DynamicCallNode):
        type_name = None
        if node.type[0].isupper(): # Is a Type name
            type_name = node.type
            self.add_instruction(LoadAddressNode(Reg.t(0), type_name)) # t0 = Class Definition Address
        else: # Is a variable name
            type_name = node.base_type.name
            self._load_local_variable(Reg.t(0), node.type) # t0 = Class Instance
            self.add_instruction(StoreWordNode(Reg.t(0), 0, Reg.t(0))) # t0 = Class Definition Address
        offset = next(offset * self.WORD_SIZE + self.TO_METHODS_OFFSET for offset, (cool_method,cil_method) in enumerate(self.type_method_dict_list[type_name]) if cool_method == node.method)
        self.add_instruction(StoreWordNode(Reg.t(0), offset, Reg.t(0))) # t0 = method direction
        self.add_instruction(JumpAndLinkNode("__get_ra"))
        self.add_instruction(MoveNode(Reg.ra(), Reg.v(0)))
        self.add_instruction(JumpRegisterNode(Reg.t(0)))
        self._store_local_variable(Reg.v(0), node.dest)
        
    @visitor.when(cil.DataNode)
    def visit(self, node:cil.DataNode):
        self.add_data(ASCIIZNode(node.name, node.value))

    @visitor.when(cil.TypeNode)
    def visit(self, node:cil.TypeNode):
        name = f"{node.name}"
        data_type = MipsTypes.word
        values = [node.parent if node.parent is not None else 0] # If no parent VOID

        # Allocate attribute amount plus type address
        values.append((len(node.attributes)+1)*self.WORD_SIZE)
        
        values.extend([x[1] for x in node.methods])
        
        data_node = DataNode(name, data_type, values)
        
        self.add_data(data_node)
        
        return data_node
    
    @visitor.when(cil.ArgNode)
    def visit(self, node:cil.ArgNode):
        self._store_local_variable(Reg.t(0), node.name)
        self._push([Reg.t(0)])
        
    @visitor.when(cil.AssignNode)
    def visit(self, node:cil.AssignNode):
        self._load_value(Reg.t(0), node.source)
        self._store_local_variable(Reg.t(0), node.dest)
    
    @visitor.when(cil.DivNode)
    def visit(self, node:cil.DivNode):
        self._load_value(Reg.t(0), node.left)
        self._load_value(Reg.t(1), node.right)
        self.add_instruction(DivideOverflowNode(Reg.t(0), Reg.t(1)))
        self._store_local_variable(Reg.low(), node.dest) # Stores the quotient
    
    @visitor.when(cil.StarNode)
    def visit(self, node:cil.StarNode):
        self._binary_operation(node, MultiplyNoOverflowNode, Reg.t(0), Reg.t(1), Reg.t(2))

    @visitor.when(cil.MinusNode)
    def visit(self, node:cil.MinusNode):
        self._binary_operation(node, SubstractNode, Reg.t(0), Reg.t(1), Reg.t(2))

    @visitor.when(cil.PlusNode)
    def visit(self, node:cil.PlusNode):
        self._binary_operation(node, AddNode, Reg.t(0), Reg.t(1), Reg.t(2))

    @visitor.when(cil.TypeOfNode)
    def visit(self, node:cil.TypeOfNode):
        self._load_local_variable(Reg.t(0), node.obj)
        self.add_instruction(LoadWordNode(Reg.t(0), 0, Reg.t(0))) # First word in instance is type address
        self._store_local_variable(Reg.t(0), node.dest)

    @visitor.when(cil.ParamNode)
    def visit(self, node:cil.ParamNode):
        pass # Function Node already do this work
    
    @visitor.when(cil.ArrayNode)
    def visit(self, node:cil.ArrayNode):
        self._load_value(Reg.a(0), node.length) # Saves in $a0 the array's byte size
        self._allocate_heap_space(Reg.a(0))
        self._store_local_variable(Reg.v(0), node.dest)
    
    @visitor.when(cil.GetIndexNode)
    def visit(self, node:cil.GetIndexNode):
        self._load_value(Reg.t(0), node.index)
        self._load_value(Reg.t(1), node.source)
        
        # Calculating Offset
        self.add_instruction(LoadImmediateNode(Reg.t(2), self.WORD_SIZE))
        self.add_instruction(MultiplyNoOverflowNode(Reg.t(2), Reg.t(2), Reg.t(0))) # Offset in t2
        
        self.add_instruction(LoadWordNode(Reg.t(1), 0, Reg.t(1))) # t1 is at the array's first position
        self.add_instruction(AddNode(Reg.t(1), Reg.t(2), Reg.t(1))) # t1 is at the index position
        
        self._store_local_variable(Reg.t(1), node.dest)
        
    @visitor.when(cil.SetIndexNode)
    def visit(self, node:cil.SetIndexNode):
        self._load_value(Reg.t(0), node.index)
        self._load_value(Reg.t(1), node.source)
        self._load_value(Reg.t(3), node.value)
        
        # Calculating Offset
        self.add_instruction(LoadImmediateNode(Reg.t(2), self.WORD_SIZE))
        self.add_instruction(MultiplyNoOverflowNode(Reg.t(2), Reg.t(2), Reg.t(0))) # Offset in t2
        
        self.add_instruction(LoadWordNode(Reg.t(1), 0, Reg.t(1))) # t1 is at the array's first position
        self.add_instruction(AddNode(Reg.t(1), Reg.t(2), Reg.t(1))) # t1 is at the index position
        
        self.add_instruction(StoreWordNode(Reg.t(3), 0, Reg.t(1)))
        
    @visitor.when(cil.CopyNode)
    def visit(self, node:cil.CopyNode):
        self._load_value(Reg.a(0), node.instance) # t0 = instance
        self.add_instruction(JumpAndLinkNode("__copy"))
        self._store_local_variable(Reg.v(0), node.result)
    
    @visitor.when(cil.GotoNode)
    def visit(self, node:cil.GotoNode):
        self.add_instruction(JumpNode(node.label))
    
    @visitor.when(cil.LabelNode)
    def visit(self, node:cil.LabelNode):
        self.add_instruction(LabelNode(node.label))
    
    @visitor.when(cil.GetFatherNode)
    def visit(self, node:cil.GetFatherNode):
        self._load_value(Reg.t(0), node.type) # t0 = Type Address
        # TODO CHECK IF THE INSTRUCTION BELOW IS REQUIRED
        # self.add_instruction(LoadWordNode(Reg.t(0), 0, Reg.t(0))) # t0 = t0[0] -> FatherAddress
        self._store_local_variable(Reg.t(0), node.dest)
    
    @visitor.when(cil.PrintNode)
    def visit(self, node:cil.PrintNode):
        self._load_value(Reg.t(0), node.str_addr)
        self.add_instruction(AddImmediateNode(Reg.v(0), Reg.zero(), 4)) # 4 System call code for print string
        self.add_instruction(SyscallNode())
        self._store_local_variable(Reg.a(0), node.str_addr)
    
    @visitor.when(cil.PrintIntNode)
    def visit(self, node:cil.PrintIntNode):
        self._load_value(Reg.t(0), node.int_addr)
        self.add_instruction(AddImmediateNode(Reg.v(0), Reg.zero(), 1)) # 1 System call code for print int
        self.add_instruction(SyscallNode())
        self._store_local_variable(Reg.a(0), node.int_addr)
      
    
    @visitor.when(cil.ReadNode)
    def visit(self, node:cil.ReadNode):
        self.add_instruction(AddImmediateNode(Reg.v(0), Reg.zero(), 8)) # 8 System call code for read string
        self.add_instruction(LoadImmediateNode(Reg.a(1), self.MAX_STRING_LENGTH)) # a1 = Allocated lenght Save the lenght in a1
        self._allocate_heap_space(Reg.a(1)) # Allocates 1024 bytes and return the address un v0
        self.add_instruction(MoveNode(Reg.a(0), Reg.v(0), comment="HERE")) # a0 = v0 Save the address in a0
        self.add_instruction(SyscallNode()) # Fills the address in a0 with the string
        self._store_local_variable(Reg.a(0), node.dest) # Save the address in the final destination
    
    @visitor.when(cil.ReadIntNode)
    def visit(self, node:cil.ReadIntNode):
        self.add_instruction(AddImmediateNode(Reg.v(0), Reg.zero(), 5)) # 5 System call code for read int
        self.add_instruction(SyscallNode()) # Returns the read integer in v0
        self._store_local_variable(Reg.v(0), node.dest) 
    
    @visitor.when(cil.ObjectCopyNode)
    def visit(self, node:cil.ObjectCopyNode):
        raise MetaCILInvalidError()
    
    @visitor.when(cil.ObjectAbortNode)
    def visit(self, node:cil.ObjectAbortNode):
        raise MetaCILInvalidError()
    
    @visitor.when(cil.ObjectTypeNameNode)
    def visit(self, node:cil.ObjectTypeNameNode):
        raise MetaCILInvalidError()
    
    @visitor.when(cil.StringConcatNode)
    def visit(self, node:cil.IOInIntNode):
        raise MetaCILInvalidError()
    
    @visitor.when(cil.StringLengthNode)
    def visit(self, node:cil.StringLengthNode):
        raise MetaCILInvalidError()
    
    @visitor.when(cil.StringSubstringNode)
    def visit(self, node:cil.StringSubstringNode):
        raise MetaCILInvalidError()
    
    @visitor.when(cil.IOInIntNode)
    def visit(self, node:cil.IOInIntNode):
        raise MetaCILInvalidError()
    
    @visitor.when(cil.IOInStringNode)
    def visit(self, node:cil.IOInStringNode):
        raise MetaCILInvalidError()

    @visitor.when(cil.IOOutIntNode)
    def visit(self, node:cil.IOOutIntNode):
        raise MetaCILInvalidError()
    
    @visitor.when(cil.IOOutStringNode)
    def visit(self, node:cil.IOOutStringNode):
        raise MetaCILInvalidError()
    
    # TODO
    
    @visitor.when(cil.GetAttribNode)
    def visit(self, node:cil.GetAttribNode):
        pass
    
    @visitor.when(cil.SetAttribNode)
    def visit(self, node:cil.SetAttribNode):
        pass
    
    @visitor.when(cil.GotoIfNode)
    def visit(self, node:cil.GotoIfNode):
        pass
    
    @visitor.when(cil.ConcatNode)
    def visit(self, node:cil.ConcatNode):
        pass
