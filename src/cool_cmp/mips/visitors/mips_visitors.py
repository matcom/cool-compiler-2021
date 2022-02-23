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
        self.add_line(".text ")
        for n in node.instructions:
            self.add_comments(n)
            instr = self.visit(n)
            self.add_line(instr)
        self.add_line(".data ")
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
    
    @visitor.when(NorNode)
    def visit(self, node:NorNode):
        return f"nor {node.result}, {node.first_arg}, {node.second_arg}"
    
    @visitor.when(XorNode)
    def visit(self, node: XorNode):
        return f"xor {node.result}, {node.first_arg}, {node.second_arg}"
    
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
    
    @visitor.when(LoadByteNode)
    def visit(self, node:LoadByteNode):
        return f"lb {node.dest}, {node.offset}({node.base_source_dir})"
    
    @visitor.when(StoreWordNode)
    def visit(self, node:StoreWordNode):
        return f"sw {node.source}, {node.offset}({node.base_dest_dir})"

    @visitor.when(StoreByteNode)
    def visit(self, node:StoreByteNode):
        return f"sb {node.source}, {node.offset}({node.base_dest_dir})"

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
        return f"slt {node.result}, {node.first_arg}, {node.second_arg}"
    
    @visitor.when(SetLessOrEqualThanNode)
    def visit(self, node:SetLessOrEqualThanNode):
        return f"sle {node.result}, {node.first_arg}, {node.second_arg}"
    
    @visitor.when(SetLessThanImmediateNode)
    def visit(self, node:SetLessThanNode):
        return f"slti {node.result}, {node.first_arg}, {node.second_arg}"
    
    @visitor.when(SetGreaterThanNode)
    def visit(self, node:SetGreaterThanNode):
        return f"sgt {node.result}, {node.first_arg}, {node.second_arg}"
    
    @visitor.when(SetGreaterOrEqualThanNode)
    def visit(self, node:SetGreaterOrEqualThanNode):
        return f"sge {node.result}, {node.first_arg}, {node.second_arg}"
    
    @visitor.when(SetEqualToNode)
    def visit(self, node:SetEqualToNode):
        return f"seq {node.result}, {node.first_arg}, {node.second_arg}"
    
    @visitor.when(SetNotEqualToNode)
    def visit(self, node:SetNotEqualToNode):
        return f"sne {node.result}, {node.first_arg}, {node.second_arg}"

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
    TO_METHODS_OFFSET = 12 # 4 Father, 4 Instance Size, 4 Type Name address, METHODS
    TYPE_NAME_OFFSET = 8 # 4 Father, 4 Instance Size, Type Name address
    MAX_STRING_LENGTH = 1024 # Max amount reserved when a read system call is made
    STRING_EMPTY = None # Stores the data address for the "" string
    
    def __init__(self, errors=[]) -> None:
        self.errors = errors
        self.program_node = None
        self.current_function = None
        self.method_dict_name = {} # Maps Type and COOL Method name to CIL function name
        self.local_variable_offset = {} # Maps CIL local variable frame pointer offset 
        self.type_method_dict_list = {} # Maps Type name to list of tuple(COOL Name, CIL Name)
 
    def _push(self, registers: List[str],row=None,column = None, comment= None):
        """
        Push the registers in order into the stack
        """
        self._allocate_stack_space(4*len(registers), row, column, comment)
        for i,reg in enumerate(registers):
            self.add_instruction(StoreWordNode(reg, i*4, Reg.sp(), row=row, column=column, comment=comment))

    def _pop(self, registers: List[str],row=None,column = None, comment= None):
        """
        Pop the registers in order from the stack
        """
        for i,reg in enumerate(registers):
            self.add_instruction(LoadWordNode(
                reg, i*4, Reg.sp(), row, column, comment))
        self._deallocate_stack_space(4*len(registers), row, column, comment)
    
    def _allocate_stack_space(self, bytes_amount: int, row=None, column=None, comment=None):
        self.add_instruction(AddImmediateNode(Reg.sp(), Reg.sp(), -bytes_amount, row, column, comment))

    def _deallocate_stack_space(self, bytes_amount: int, row=None, column=None, comment=None):
        self.add_instruction(AddImmediateNode(Reg.sp(), Reg.sp(), bytes_amount, row, column, comment))

    def _load_local_variable(self, dest, name, row=None, column=None, comment=None):
        try:
            value = int(name)
            self.add_instruction(LoadImmediateNode(dest, name, row, column, comment))
        except ValueError:
            self.add_instruction(LoadWordNode(dest, self.local_variable_offset[name], Reg.fp(),row,column,comment)) # Stack address for local variable

    def _load_type_variable(self, dest, name, row=None, column=None, comment=None):
        """
        Store into dest the type address of name.

        name can be a type name or can be an address to a type address

        name = IO

        local = IO
        name = local
        """
        if isinstance(name, cil.TypeNode):
            name = name.name
        if name[0].isupper():
            self.add_instruction(LoadAddressNode(dest, name,row,column,comment))
        else:
            self._load_local_variable(dest, name, row, column, comment)

    def _store_local_variable(self, source, name_or_value, row=None, column=None, comment=None):
        try:
            # Int literal
            int_value = int(name_or_value)
            self.add_instruction(AddImmediateNode(source, Reg.zero(), int_value, row, column, comment))
        except ValueError:
            # Variable
            self.add_instruction(StoreWordNode(source, self.local_variable_offset[name_or_value], Reg.fp(),row,column,comment)) # Stores allocated memory address in destination variable

    def _call_with_register(self, register, row=None, column=None, comment=None):
        self.add_instruction(JumpRegisterNode(register, row, column, comment))
    
    def _add_abort_instructions(self, row=None, column=None, comment=None):
        """
        Add the abort instructions 
        """
        self.add_instruction(AddImmediateNode(Reg.v(0), Reg.zero(), 10,row,column,comment)) # 10 System call code for abort
        self.add_instruction(SyscallNode(row, column, comment))

    def _add_copy_string_cycle(self, label_prefix, length_reg, string_source, string_dest, temp_reg, add_null=True, row=None, column=None, comment=None):
        """
        Adds the instructions required to copy the string in string_source to string_dest
        using temp_reg to store the individual char values. The length to copy is stored in length_reg.
        """
        
        start_loop = label_prefix + "_start_copy"
        end_loop = label_prefix + "_end_copy"
        self.add_instruction(LabelNode(start_loop, row, column, comment))
        self.add_instruction(BranchLessEqualNode(length_reg, Reg.zero(), end_loop,row,column,comment)) # if length <= 0 then end loop, missing null
        
        self.add_instruction(LoadByteNode(temp_reg, 0, string_source,row,column,comment)) # t3 = char to copy
        self.add_instruction(StoreByteNode(temp_reg, 0, string_dest,row,column,comment)) # copy char to corresponding address position 
        self.add_instruction(AddImmediateNode(string_source, string_source, 1,row,column,comment)) # Next original string address 
        self.add_instruction(AddImmediateNode(string_dest, string_dest, 1,row,column,comment)) # Next copy string address

        self.add_instruction(AddImmediateNode(
            length_reg, length_reg, -1, row, column, comment))  # Decrease amount
        self.add_instruction(JumpNode(start_loop, row, column, comment))

        self.add_instruction(LabelNode(end_loop, row, column, comment))
        
        if add_null:
            self.add_instruction(StoreByteNode(
                Reg.zero(), 0, string_dest, row, column, comment))  # Final null character

    def _add_create_string_instance(self, temp_reg, string_address, row=None, column=None, comment=None):
        """
        Returns in $v0 the new instance of String,Address.
        Uses $a0, $v0
        """
        self.add_instruction(LoadAddressNode(temp_reg, "String", row, column, "Type address into $a0")) # Type address into $a0
        self.add_instruction(LoadImmediateNode(Reg.a(0), self.WORD_SIZE * 2, row, column, "If String the is type and address")) # If String the is type and address
        self._allocate_heap_space(Reg.a(0), row, column)

        self.add_instruction(StoreWordNode(temp_reg, 0, Reg.v(0), row, column, "Store String Type")) # Store String Type
        self.add_instruction(StoreWordNode(string_address, self.WORD_SIZE, Reg.v(0), row, column, "Store String Address")) # Store String Address
        

    def _add_copy_function(self,row=None, column = None, comment=None):
        """
        Function that copies the instance passed in $a0 and returns the copy address
        in $v0 
        """
        
        self.add_instruction(
            LabelNode("__copy", row, column, comment))
        
        self.add_instruction(MoveNode(Reg.t(0), Reg.a(0),row,column,comment)) # t0 = object address
        self.add_instruction(LoadWordNode(Reg.t(1), 0, Reg.t(0),row,column,comment)) # t1 = instance type dir
        self.add_instruction(LoadWordNode(Reg.a(0), self.WORD_SIZE, Reg.t(1),row,column,comment)) # a0 = instance size
        self._allocate_heap_space(Reg.a(0),row,column,comment) # v0 = allocated space
        
        start_label_name = "__start_copy_loop"
        end_label_name = "__end_copy_loop"
        
        self.add_instruction(MoveNode(Reg.t(1), Reg.a(0),row,column,comment)) # t1 = instance size
        # t1 = bytes amount = instance size / 4
        self.add_instruction(ShiftRightNode(
            Reg.t(1), Reg.t(1), 2, row, column, comment))
        # t3 = new object memory address
        self.add_instruction(
            MoveNode(Reg.t(3), Reg.v(0), row, column, comment))
        
        self.add_instruction(LabelNode(start_label_name,row,column,comment))
        self.add_instruction(BranchLessEqualNode(Reg.t(1), Reg.zero(), end_label_name,row,column,comment)) # End cycle condition
        
        # Get value from original object
        self.add_instruction(LoadWordNode(
            Reg.t(2), 0, Reg.t(0), row, column, comment))
        self.add_instruction(StoreWordNode(Reg.t(2), 0, Reg.t(3),row,column,comment)) # Set value copied value into the new object
        self.add_instruction(AddImmediateNode(Reg.t(0), Reg.t(0), 4,row,column,comment)) # Next position old object
        self.add_instruction(AddImmediateNode(Reg.t(3), Reg.t(3), 4,row,column,comment)) # Next position new object
        self.add_instruction(AddImmediateNode(Reg.t(1), Reg.t(1), -1,row,column,comment)) # Copy amount -= 1
        
        self.add_instruction(JumpNode(start_label_name,row,column,comment))
        self.add_instruction(LabelNode(end_label_name, row, column, comment))
        
        # In v0 is the new object address
        self.add_instruction(JumpRegisterNode(Reg.ra(), row, column, comment))
    
    def _add_length_function(self,row=None, column = None, comment=None):
        """
        Function that returns in $v0 the length of the string passed in $a0
        """
        self.add_instruction(LabelNode("__string_length",row,column,comment))

        self.add_instruction(LoadWordNode(Reg.a(0), self.WORD_SIZE, Reg.a(0), row, column, "Actual String address")) # Actual String address

        self.add_instruction(LoadImmediateNode(Reg.v(0), 0, row, column, "v0 = current length")) # v0 = current length
        start_loop = "__string_length_start_loop"
        end_loop = "__string_length_end_loop"
        self.add_instruction(LabelNode(start_loop, row, column, comment))
        self.add_instruction(LoadByteNode(Reg.t(0), 0, Reg.a(0),row,column,comment)) # Load current char
        
        self.add_instruction(BranchEqualNode(Reg.t(0), Reg.zero(), end_loop,row,column,comment)) # Is null char? end

        self.add_instruction(AddImmediateNode(Reg.v(0), Reg.v(0), 1,row,column,comment)) # Increment length
        self.add_instruction(AddImmediateNode(Reg.a(0), Reg.a(0), 1,row,column,comment)) # Next char

        self.add_instruction(JumpNode(start_loop,row,column,comment))
        self.add_instruction(LabelNode(end_loop,row,column,comment))

        # In v0 is the string length
        self.add_instruction(JumpRegisterNode(Reg.ra(), row, column, comment))

    def _add_substring_function(self, row=None, column = None, comment=None):
        """
        Returns in $v0 the result of the substring of $a0 starting in index $a1 with length $a2
        """

        self.add_instruction(LabelNode("__string_substring",row,column,comment))

        saved_register = [Reg.a(0), Reg.a(1), Reg.a(2), Reg.ra()]
        self._push(saved_register, row, column, "Save arguments")  # Save arguments
        self.add_instruction(JumpAndLinkNode("__string_length",row,column,"$v0 = length of string"))
        # $v0 = length of string
        self._pop(saved_register,row,column,"Restore arguments") # Restore arguments

        self.add_instruction(LoadWordNode(Reg.a(0), self.WORD_SIZE, Reg.a(0), row, column, "Actual String address")) # Actual String address

        abort_label = "__string_substring_abort"

        # If index >= length(string) then abort
        self.add_instruction(BranchGreaterEqualNode(Reg.a(1), Reg.v(0), abort_label,row,column, "If index >= length(string) then abort"))

        self.add_instruction(AddNode(Reg.t(0), Reg.a(1), Reg.a(2),row,column, "t0 = index + length")) # t0 = index + length
        # If index + length >= length(string) then abort
        self.add_instruction(BranchGreaterNode(Reg.t(0), Reg.v(0), abort_label,row,column, "If index + length >= length(string) then abort"))
        
        # If 0 < 0 then abort
        self.add_instruction(BranchLessNode(Reg.a(2), Reg.zero(), abort_label,row,column, "If 0 < 0 then abort"))

        # Here the operation can be safetly made
        self.add_instruction(MoveNode(Reg.t(1), Reg.a(0),row,column, "Saving the string address")) # Saving the string address

        self.add_instruction(AddImmediateNode(Reg.a(0), Reg.a(2), 1,row,column, "a0 = length + 1. Extra space for null character")) # a0 = length + 1. Extra space for null character
        self._allocate_heap_space(Reg.a(0),row,column,comment)
        # v0 = new String address

        self.add_instruction(MoveNode(Reg.t(2), Reg.v(0),row,column, "Saving the new string address")) # Saving the new string address
        self.add_instruction(AddImmediateNode(Reg.a(0), Reg.a(0), -1,row,column, "Removing the last null space from copy")) # Removing the last null space from copy

        self.add_instruction(AddNode(Reg.t(1), Reg.t(1), Reg.a(1),row,column, "Advance index positions in original string")) # Advance index positions in original string

        self._add_copy_string_cycle("__string_substring", Reg.a(0), Reg.t(1), Reg.t(2), Reg.t(3),row,column,comment)

        self.add_instruction(MoveNode(Reg.v(1), Reg.v(0), comment="Saving String Address"))
        self._add_create_string_instance(Reg.t(0), Reg.v(1))

        self.add_instruction(JumpRegisterNode(Reg.ra(),row,column, "Return the address of the new String"))

        self.add_instruction(LabelNode(abort_label,row,column,comment))
        self._add_abort_instructions( row, column, comment)

    def _add_type_name_function(self,row=None, column = None, comment=None):
        """
        Returns in $v0 the string address of the type given in $a0
        """

        self.add_instruction(LabelNode("__type_name",row,column,comment))
        # $t0 = type name address
        self.add_instruction(LoadWordNode(Reg.t(0), self.TYPE_NAME_OFFSET, Reg.a(0), row, column, "$t0 = type name address"))
        
        self._add_create_string_instance(Reg.t(1), Reg.t(0))
        
        # Return the address of the String
        self.add_instruction(JumpRegisterNode(Reg.ra(), row, column, "Return the address of the String"))

    def _add_concat_function(self,row=None, column = None, comment=None):
        """
        Returns in $v0 the concatenation of the strings given in $a0 and $a1
        """

        self.add_instruction(LabelNode("__concat", row, column, comment))
        
        saved_register = [Reg.a(0), Reg.a(1), Reg.ra()]
        self._push(saved_register,row,column,comment) # Save arguments
        self.add_instruction(JumpAndLinkNode("__string_length",row,column,comment))
        # $v0 = length of string1
        self._pop(saved_register,row,column,comment) # Restore arguments
        
        self.add_instruction(MoveNode(Reg.t(1), Reg.a(0),row,column,comment)) # t1 = string1
        self.add_instruction(MoveNode(Reg.a(0), Reg.a(1),row,column,comment)) # Passing arguments to __string_length
        # Swap ended a0,a1 = a1,a0
        self.add_instruction(
            MoveNode(Reg.a(1), Reg.t(1), row, column, comment))

        # t0 = length of string1
        self.add_instruction(
            MoveNode(Reg.t(0), Reg.v(0), row, column, comment))

        saved_register = [Reg.a(0), Reg.a(1), Reg.t(0), Reg.ra()]
        self._push(saved_register,row,column,comment) # Save arguments
        self.add_instruction(JumpAndLinkNode("__string_length",row,column,comment))
        # $v0 = length of string2
        self._pop(saved_register, row, column, comment )  # Restore arguments

        # Returning the arguments to the correct order
        self.add_instruction(MoveNode(Reg.t(1), Reg.a(0),row,column,comment)) # t1 = string2
        self.add_instruction(MoveNode(Reg.a(0), Reg.a(1),row,column,comment))
        self.add_instruction(MoveNode(Reg.a(1), Reg.t(1),row,column,comment)) # Swap ended a1,a0 = a1,a0
        
        self.add_instruction(LoadWordNode(Reg.a(0), self.WORD_SIZE, Reg.a(0))) # Actual String address
        self.add_instruction(LoadWordNode(Reg.a(1), self.WORD_SIZE, Reg.a(1))) # Actual String address
     
        self.add_instruction(MoveNode(Reg.t(1), Reg.a(0),row,column,comment)) # t1 = string1, saving arg

        self.add_instruction(AddNode(Reg.t(2), Reg.v(0), Reg.t(0),row,column,comment)) # t2 = length of the concatenated string without null
        self.add_instruction(AddImmediateNode(Reg.a(0), Reg.t(2), 1,row,column,comment)) # a0 = length of the concatenated string with null
        self.add_instruction(MoveNode(Reg.t(2), Reg.v(0),row,column,comment)) # t2 = length of string2

        # Allocates the necessary space
        self._allocate_heap_space(Reg.a(0), row, column, comment)
        # New string address in $v0

        self.add_instruction(MoveNode(Reg.v(1), Reg.v(
            0), row, column, "Save string address"))  # Save string address

        # Copy the string1 from a0 to v0 without the null character. Also increments the v0 address
        # up to the next character.
        self._add_copy_string_cycle("__concat_string1_copy", Reg.t(0), Reg.t(1), Reg.v(1), Reg.t(3), add_null=False,row=row,column=column,comment=comment)
        self._add_copy_string_cycle("__concat_string2_copy", Reg.t(2), Reg.a(1), Reg.v(1), Reg.t(3), add_null=True, row=row,column= column,comment= comment)

        self.add_instruction(MoveNode(Reg.v(1), Reg.v(
            0), row, column, "Save string address"))  # Save string address

        self._add_create_string_instance(Reg.t(0), Reg.v(1))

        self.add_instruction(JumpRegisterNode(Reg.ra(), row, column, "Returns the concatenated string instance in v0"))

    def _add_string_equal_function(self, row=None, column=None, comment=None):
        """
        Returns in v0 if the strings given in a0 and a1 are equal
        """
        # TODO 
        self.add_instruction(LabelNode("__string_equal"))
 
        start_compare_loop = "__string_equal_start_loop"
        end_compare_loop = "__string_equal_end_loop"
        
        self.add_instruction(LoadWordNode(Reg.t(0), self.WORD_SIZE, Reg.a(0), row, column, "Actual String address")) # Actual String address
        self.add_instruction(LoadWordNode(Reg.t(1), self.WORD_SIZE, Reg.a(1), row, column, "Actual String address")) # Actual String address
        
        self.add_instruction(LabelNode(start_compare_loop))
        self.add_instruction(LoadByteNode(Reg.t(2), 0, Reg.t(0), comment="Load string1 char"))
        self.add_instruction(LoadByteNode(Reg.t(3), 0, Reg.t(1), comment="Load string2 char"))
        self.add_instruction(SetEqualToNode(Reg.t(4), Reg.t(2), Reg.t(3), comment="Equal chars?"))
        self.add_instruction(BranchEqualNode(Reg.t(4), Reg.zero(), end_compare_loop, comment="If not equal then")) # If not equal then  

        # Chars are equal to null? => End
        self.add_instruction(BranchEqualNode(Reg.t(2), Reg.zero(), end_compare_loop, comment="Both strings ended"))
        
        # Next char
        self.add_instruction(AddImmediateNode(Reg.t(0), Reg.t(0), 1, comment="Next char"))
        self.add_instruction(AddImmediateNode(Reg.t(1), Reg.t(1), 1, comment="Next char"))
        
        self.add_instruction(JumpNode(start_compare_loop))
        
        self.add_instruction(LabelNode(end_compare_loop))
        self.add_instruction(MoveNode(Reg.v(0), Reg.t(4), comment="Assign return value"))
        self.add_instruction(JumpRegisterNode(Reg.ra()))
    
    def _add_obj_equal_function(self, row=None, column=None, comment=None):
        """
        Returns in v0 if the objects given in a0 and a1 are equal
        """
        self.add_instruction(LabelNode("__object_equal"))
        
        obj_cmp_label = "__object_equal_label"
        obj_end_cmp_label = "__object_equal_end"
        
        self.add_instruction(SetEqualToNode(Reg.v(0), Reg.a(0), Reg.a(1), comment="Compare obj by address"))
        self.add_instruction(BranchNotEqualNode(Reg.v(0), Reg.zero(), obj_end_cmp_label, comment="Equal Address or Value obj are equal"))
                
        self.add_instruction(MoveNode(Reg.t(0), Reg.a(0), comment="t0 = left object"))
        self.add_instruction(MoveNode(Reg.t(1), Reg.a(1), comment="t1 = right object"))

        
        
        self.add_instruction(LoadWordNode(Reg.t(0), 0, Reg.t(0), comment="t0=left objType"))
        self.add_instruction(LoadWordNode(Reg.t(1), 0, Reg.t(1), comment="t1=right objType"))
        
        self._load_type_variable(Reg.t(2), "String", comment="Loading String type address for comparison")
        
        self.add_instruction(SetEqualToNode(Reg.t(0), Reg.t(0), Reg.t(2), comment="t0 = left type == String"))
        self.add_instruction(SetEqualToNode(Reg.t(1), Reg.t(1), Reg.t(2), comment="t1 = right type == String"))
        self.add_instruction(AndNode(Reg.t(0), Reg.t(0), Reg.t(1), comment="Both types are equal to String"))
        
        self.add_instruction(BranchEqualNode(Reg.t(0), Reg.zero(), obj_cmp_label, comment="If not equal return 0"))
        
        self._push([Reg.ra(), Reg.a(0), Reg.a(1)])
        self.add_instruction(JumpAndLinkNode("__string_equal"))
        # In $v0 if equal or not
        self._pop([Reg.ra(), Reg.a(0), Reg.a(1)])
        
        self.add_instruction(JumpNode(obj_end_cmp_label))
        self.add_instruction(LabelNode(obj_cmp_label, comment="Do Obj cmp"))

        self.add_instruction(MoveNode(Reg.v(0), Reg.zero(), comment="Not equal objects"))            
                
        self.add_instruction(LabelNode(obj_end_cmp_label, comment="End cmp"))   
        
        self.add_instruction(JumpRegisterNode(Reg.ra()))

    def _add_get_ra_function(self,row=None,column=None,comment=None):
        """
        Adds a function that returns in $v0 2 instructions after the caller instruction
        """
        self.add_instruction(LabelNode("__get_ra",row,column,comment))
        self.add_instruction(MoveNode(Reg.v(0), Reg.ra(),row,column,comment))
        self.add_instruction(AddImmediateNode(Reg.v(0), Reg.v(0), 2*self.WORD_SIZE,row,column,comment))
        self.add_instruction(JumpRegisterNode(Reg.ra(),row,column,comment))
    
    def _load_value(self, dest1, value1,row=None,column=None,comment=None):
        """
        Returns in register `dest1` the value of `value1`
        """
        try:
            value = int(value1)
            self.add_instruction(LoadImmediateNode(
                dest1, value, row, column, comment))
        except ValueError:
            try:
                self._load_local_variable(dest1, value1,row,column,comment)
            except KeyError:
                self._load_type_variable(dest1, value1, row, column, comment)
    
    def _binary_operation(self, node: cil.ArithmeticNode, instruction_type, reg1, reg2, temp_reg, row=None, column=None, comment=None):        
        self._load_value(reg1, node.left,row,column,comment)
        self._load_value(reg2, node.right,row,column,comment)
        self.add_instruction(instruction_type(temp_reg, reg1, reg2, row, column, comment))
        self._store_local_variable(temp_reg, node.dest,row,column,comment)
    
    def _allocate_heap_space(self, reg_with_amount,row=None,column=None,comment=None):
        """
        Stores in `a0` the `reg_with_amount` and makes a system call
        to reserve space. The reserve space address will be in `v0`
        """
        if reg_with_amount != Reg.a(0):
            self.add_instruction(MoveNode(Reg.a(0), reg_with_amount,row,column,comment)) # Saves in $a0 the bytes size for current type
        self.add_instruction(LoadImmediateNode(Reg.v(0), 9,row,column,comment)) # Reserve space arg
        self.add_instruction(SyscallNode(row,column,comment)) # Returns in $v0 the allocated memory

    def _attribute_index_to_offset(self, index):
        """
        Returns the offset for the given attribute's index in the object memory space 
        """
        return self.WORD_SIZE + index * self.WORD_SIZE # Object Type address first and then the attributes

    def _get_array_index(self, dest_reg, aux_reg, index, row=None, column=None, comment=None):
        """
        Returns in `dest_reg` the actual offset for `index` in an array, `aux_reg` is used
        for computing this value.
        """
        try:
            offset = int(index) * self.WORD_SIZE
            self._load_value(dest_reg, offset, row, column,
                             comment)  # Offset in dest_reg
        except ValueError:
            self._load_value(aux_reg, index, row, column, comment)
            self.add_instruction(LoadImmediateNode(dest_reg, self.WORD_SIZE,row,column,comment))
            self.add_instruction(MultiplyNoOverflowNode(dest_reg, dest_reg, aux_reg,row,column,comment)) # Offset in dest_reg


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

        for data in node.dotdata: # Register data nodes
            self.visit(data)
        self.visit(cil.DataNode("__empty_string", '""', 0, 0, "Register empty string data")) # Register empty string data
        self.STRING_EMPTY = self.program_node.data[-1].name

        self._add_get_ra_function(node.row,node.column,node.comment)
        self._add_copy_function(node.row,node.column,node.comment)
        self._add_length_function( node.row,node.column,node.comment)
        self._add_substring_function( node.row,node.column,node.comment)
        self._add_type_name_function( node.row,node.column,node.comment)
        self._add_concat_function( node.row,node.column,node.comment)
        self._add_string_equal_function(node.row,node.column, "String Equal Function")
        self._add_obj_equal_function(node.row,node.column, "Object Equal Function")

        for function in node.dotcode:
            self.current_function = function
            self.visit(function)
        
        self.current_function = None
        
        for typex in node.dottypes:
            self.visit(typex)

        return program

    @visitor.when(cil.FunctionNode)
    def visit(self, node:cil.FunctionNode):
        
        self.local_variable_offset = {}
        
        self.add_instruction(LabelNode(node.name, node.row, node.column, node.comment))
        allocated_space = len(node.localvars) * self.WORD_SIZE # When a function is called the stack already contains all the params 
        self._allocate_stack_space(
            allocated_space,node.row, node.column, node.comment)
        offset = 0
        
        for local in node.localvars + node.params[::-1]: # Params in reverse order
            self.local_variable_offset[local.name] = offset
            offset += self.WORD_SIZE
            
        self.add_instruction(MoveNode(Reg.t(0), Reg.sp(),node.row, node.column,node.comment)) # Temporary save fp
        saved_registers = [Reg.ra(), Reg.fp()] # + [Reg.s(i) for i in range(8)]
        self._push(saved_registers, node.row, node.column, node.comment)
        # Set fp to value that matches with the offsets
        self.add_instruction(MoveNode(Reg.fp(), Reg.t(
            0), node.row, node.column, node.comment))

        for instr in node.instructions:
            self.visit(instr)
        
        self._pop(saved_registers, node.row, node.column, node.comment)
        self._deallocate_stack_space(allocated_space + len(node.params) * self.WORD_SIZE,
                                     node.row, node.column, node.comment)  # Deallocate also the params
        self.add_instruction(JumpRegisterNode(
            Reg.ra(), node.row, node.column, node.comment))
    
    @visitor.when(cil.ReturnNode)
    def visit(self, node:cil.ReturnNode):
        if node.value:
            self._load_value(Reg.v(0), node.value, node.row,
                             node.column, node.comment)
    
    @visitor.when(cil.AllocateNode)
    def visit(self, node:cil.AllocateNode):
        if node.type in ["Int", "Bool"]:
            
            self._store_local_variable(Reg.zero(), node.dest, node.row, node.column, node.comment) # Default value for Int and Bool is 0
            return

        if node.type[0].isupper(): # Is a Type name
            self.add_instruction(LoadAddressNode(Reg.a(
                0), node.type, node.row, node.column, node.comment))  # Type address into $a0
        else:
            self._load_local_variable(Reg.a(0), node.type, node.row, node.column, node.comment)
        if node.type == "String":
            self.add_instruction(LoadImmediateNode(Reg.a(0), self.WORD_SIZE * 2, node.row, node.column, node.comment)) # If String the is type and address
        else:
            self.add_instruction(LoadWordNode(Reg.a(0), self.WORD_SIZE, Reg.a(0), node.row, node.column, node.comment)) # Saves in $a0 the bytes size for current type
        self._allocate_heap_space(Reg.a(0), node.row, node.column)
        self._store_local_variable(Reg.v(0), node.dest, node.row, node.column)

    @visitor.when(cil.AbortNode)
    def visit(self, node:cil.AbortNode):
        self._add_abort_instructions( node.row, node.column, node.comment)
    
    @visitor.when(cil.StaticCallNode)
    def visit(self, node:cil.StaticCallNode):
        self.add_instruction(JumpAndLinkNode(node.function,node.row, node.column, node.comment)) # Jumps to label
        self._store_local_variable(
            Reg.v(0), node.dest, node.row, node.column, node.comment)
        
    @visitor.when(cil.DynamicCallNode)
    def visit(self, node:cil.DynamicCallNode):
        type_name = None
        if node.type[0].isupper(): # Is a Type name
            type_name = node.type
        elif node.base_type: # Is a variable name or SELF_TYPE
            type_name = node.base_type.name

        self._load_type_variable(
            Reg.t(0), node.type, node.row, node.column, node.comment)  # t0 = TypeAddress
        # Override of methods leave the new method in the same position as the overriden method 
        offset = next(offset * self.WORD_SIZE + self.TO_METHODS_OFFSET for offset, (cool_method,cil_method) in enumerate(self.type_method_dict_list[type_name]) if cool_method == node.method)
        self.add_instruction(LoadWordNode(Reg.t(0), offset, Reg.t(0),node.row, node.column, node.comment)) # t0 = method direction
        self.add_instruction(JumpAndLinkNode("__get_ra",node.row, node.column, node.comment))
        self.add_instruction(MoveNode(Reg.ra(), Reg.v(0),node.row, node.column, node.comment))
        self.add_instruction(JumpRegisterNode(Reg.t(0),node.row, node.column, node.comment))
        self._store_local_variable(Reg.v(0), node.dest,node.row, node.column, node.comment)
        
    @visitor.when(cil.DataNode)
    def visit(self, node:cil.DataNode):
        self.add_data(ASCIIZNode(node.name, node.value))

    @visitor.when(cil.TypeNode)
    def visit(self, node:cil.TypeNode):
        name = f"{node.name}"
        data_type = MipsTypes.word

        # Father address
        values = [node.parent if node.parent is not None else 0] # If no parent VOID

        # Allocate attribute amount plus type address
        values.append((len(node.attributes)+1)*self.WORD_SIZE)
        
        # Type name address
        values.append(node.name_data)
        
        # Methods
        values.extend([x[1] for x in node.methods])
        
        data_node = DataNode(name, data_type, values,
                             node.row, node.column, node.comment)
        
        self.add_data(data_node)
        
        return data_node
    
    @visitor.when(cil.ArgNode)
    def visit(self, node:cil.ArgNode):
        self._load_value(Reg.t(0), node.name, node.row,
                         node.column, node.comment)
        self._push([Reg.t(0)], node.row, node.column, node.comment)
        
    @visitor.when(cil.AssignNode)
    def visit(self, node:cil.AssignNode):
        self._load_value(Reg.t(0), node.source,node.row, node.column, node.comment)
        self._store_local_variable(
            Reg.t(0), node.dest, node.row, node.column, node.comment)
    
    @visitor.when(cil.DivNode)
    def visit(self, node:cil.DivNode):
        self._load_value(Reg.t(0), node.left,node.row, node.column, node.comment)
        self._load_value(Reg.t(1), node.right,node.row, node.column, node.comment)
        self.add_instruction(DivideOverflowNode(
            Reg.t(0), Reg.t(1), node.row, node.column, node.comment))
        self.add_instruction(MoveFromLoNode(Reg.t(0), node.row, node.column, "Getting quotient"))
        self._store_local_variable(
            Reg.t(0), node.dest, node.row, node.column, "Stores the quotient")  # Stores the quotient
    
    @visitor.when(cil.StarNode)
    def visit(self, node:cil.StarNode):
        self._binary_operation(node, MultiplyNoOverflowNode, Reg.t(
            0), Reg.t(1), Reg.t(2), node.row, node.column, node.comment)

    @visitor.when(cil.MinusNode)
    def visit(self, node:cil.MinusNode):
        self._binary_operation(node, SubstractNode, Reg.t(0), Reg.t(1), Reg.t(2),node.row, node.column, node.comment)

    @visitor.when(cil.PlusNode)
    def visit(self, node:cil.PlusNode):
        self._binary_operation(node, AddNode, Reg.t(0), Reg.t(
            1), Reg.t(2), node.row, node.column, node.comment)

    @visitor.when(cil.ObjEqualNode)
    def visit(self, node:cil.ObjEqualNode):
        if node.value_compare:
            self._binary_operation(node, SetEqualToNode, Reg.t(0), Reg.t(1), Reg.t(2),node.row, node.column, node.comment)
        else:
            self._load_local_variable(Reg.a(0), node.left, node.row, node.column, "a0 = left object")
            self._load_local_variable(Reg.a(1), node.right, node.row, node.column, "a1 = right object")
            self._push([Reg.ra()])
            self.add_instruction(JumpAndLinkNode("__object_equal"))
            self._pop([Reg.ra()])
            self._store_local_variable(Reg.v(0), node.dest, comment="Saving equal result")

    @visitor.when(cil.EqualNode)
    def visit(self, node:cil.EqualNode):
        self._binary_operation(node, SetEqualToNode, Reg.t(0), Reg.t(1), Reg.t(2),node.row, node.column, node.comment)

    @visitor.when(cil.GreaterNode)
    def visit(self, node:cil.GreaterNode):
        self._binary_operation(node, SetGreaterThanNode, Reg.t(0), Reg.t(1), Reg.t(2),node.row, node.column, node.comment)

    @visitor.when(cil.LesserNode)
    def visit(self, node:cil.LesserNode):
        self._binary_operation(node, SetLessThanNode, Reg.t(0), Reg.t(1), Reg.t(2),node.row, node.column, node.comment)

    @visitor.when(cil.NotNode)
    def visit(self, node:cil.NotNode):
        self._load_value(Reg.t(0), node.value,node.row, node.column, node.comment)
        self.add_instruction(SetEqualToNode(Reg.t(0),Reg.t(0),Reg.zero(),node.row, node.column, node.comment))
        #self.add_instruction(XorNode(Reg.t(0), Reg.t(0),1,node.row, node.column, node.comment)) # Not equivalent for 0 and 1
        self._store_local_variable(Reg.t(0), node.dest,node.row, node.column, node.comment)

    @visitor.when(cil.TypeOfNode)
    def visit(self, node:cil.TypeOfNode):
        self._load_local_variable(Reg.t(0), node.obj,node.row, node.column, node.comment)
        self.add_instruction(LoadWordNode(Reg.t(0), 0, Reg.t(0),node.row, node.column, node.comment)) # First word in instance is type address
        self._store_local_variable(
            Reg.t(0), node.dest, node.row, node.column, node.comment)

    @visitor.when(cil.ParamNode)
    def visit(self, node:cil.ParamNode):
        pass # Function Node already do this work
    
    @visitor.when(cil.ArrayNode)
    def visit(self, node:cil.ArrayNode):
        # Calculating Length
        self._get_array_index(Reg.a(0), Reg.t(
            0), node.length, node.row, node.column, node.comment)
        # $a0 = Array Length
        
        self._allocate_heap_space(Reg.a(0),node.row, node.column, node.comment) # Allocated address in $v0
        self._store_local_variable(
            Reg.v(0), node.dest, node.row, node.column, node.comment)
    
    @visitor.when(cil.GetIndexNode)
    def visit(self, node:cil.GetIndexNode):
        # Calculating Offset
        self._get_array_index(Reg.t(2), Reg.t(0), node.index,node.row, node.column, node.comment) # Offset in t2

        self._load_value(Reg.t(1), node.source,node.row, node.column, node.comment) # Load array direction into t1
        
        self.add_instruction(AddNode(Reg.t(1), Reg.t(1), Reg.t(2),node.row, node.column, node.comment)) # t1 is at the index position
        
        self.add_instruction(LoadWordNode(Reg.t(2), 0, Reg.t(1),node.row, node.column, node.comment))
        self._store_local_variable(
            Reg.t(2), node.dest, node.row, node.column, node.comment)
        
    @visitor.when(cil.SetIndexNode)
    def visit(self, node:cil.SetIndexNode):
        # Calculating Offset
        self._get_array_index(Reg.t(2), Reg.t(0), node.index,node.row, node.column, node.comment) # Offset in t2

        self._load_value(Reg.t(3), node.value,node.row, node.column, node.comment) # Set value in t3

        self._load_value(Reg.t(1), node.source,node.row, node.column, node.comment) # Array address in t1
        
        self.add_instruction(AddNode(Reg.t(1), Reg.t(1), Reg.t(2),node.row, node.column, node.comment)) # t1 is at the index position
        
        self.add_instruction(StoreWordNode(
            Reg.t(3), 0, Reg.t(1), node.row, node.column, node.comment))

    @visitor.when(cil.CopyNode)
    def visit(self, node:cil.CopyNode):
        self._load_value(Reg.a(0), node.instance,node.row, node.column, node.comment) # t0 = instance
        # Function Node already saves all register information
        self.add_instruction(JumpAndLinkNode("__copy",node.row, node.column, node.comment))
        self._store_local_variable(
            Reg.v(0), node.result, node.row, node.column, node.comment)
    
    @visitor.when(cil.LengthNode)
    def visit(self, node:cil.LengthNode):
        self._load_value(Reg.a(0), node.string_var,node.row, node.column, node.comment) # a0 = instance
        # Function Node already saves all register information
        self.add_instruction(JumpAndLinkNode("__string_length",node.row, node.column, node.comment))
        self._store_local_variable(Reg.v(0), node.dest,node.row, node.column, node.comment)

    @visitor.when(cil.SubstringNode)
    def visit(self, node:cil.SubstringNode):
        self._load_value(Reg.a(0), node.string,node.row, node.column, node.comment)
        self._load_value(Reg.a(1), node.index,node.row, node.column, node.comment)
        self._load_value(Reg.a(2), node.length,node.row, node.column, node.comment)
        # Function Node already saves all register information
        self.add_instruction(JumpAndLinkNode("__string_substring",node.row, node.column, node.comment))
        self._store_local_variable(
            Reg.v(0), node.dest, node.row, node.column, node.comment)

    @visitor.when(cil.TypeNameNode)
    def visit(self, node:cil.TypeNameNode):
        self._load_type_variable(Reg.a(0), node.type,node.row, node.column, node.comment)
        # Function Node already saves all register information
        self.add_instruction(JumpAndLinkNode("__type_name",node.row, node.column, node.comment))
        self._store_local_variable(Reg.v(0), node.dest,node.row, node.column, node.comment)

    @visitor.when(cil.ConcatNode)
    def visit(self, node:cil.ConcatNode):
        self._load_local_variable(Reg.a(0), node.string1,node.row, node.column, node.comment)
        self._load_local_variable(Reg.a(1), node.string2,node.row, node.column, node.comment)

        # Function Node already saves all register information
        self.add_instruction(JumpAndLinkNode("__concat",node.row, node.column, node.comment))

        self._store_local_variable(
            Reg.v(0), node.dest, node.row, node.column, node.comment)

    @visitor.when(cil.VoidNode)
    def visit(self, node:cil.VoidNode):
        self._store_local_variable(Reg.zero(), node.dest,node.row, node.column, node.comment)

    @visitor.when(cil.GotoNode)
    def visit(self, node:cil.GotoNode):
        self.add_instruction(
            JumpNode(node.label, node.row, node.column, node.comment))
    
    @visitor.when(cil.LabelNode)
    def visit(self, node:cil.LabelNode):
        self.add_instruction(
            LabelNode(node.label, node.row, node.column, node.comment))
    
    @visitor.when(cil.GetFatherNode)
    def visit(self, node:cil.GetFatherNode):
        self._load_type_variable(Reg.t(0), node.variable,node.row, node.column, node.comment) # t0 = Type Address
        self.add_instruction(LoadWordNode(Reg.t(0), 0, Reg.t(0),node.row, node.column, node.comment)) # t0 = t0[0] -> FatherAddress
        self._store_local_variable(
            Reg.t(0), node.dest, node.row, node.column, node.comment)
    
    @visitor.when(cil.PrintNode)
    def visit(self, node:cil.PrintNode):
        self._load_value(Reg.a(0), node.str_addr, node.row, node.column, node.comment)
        self.add_instruction(LoadWordNode(Reg.a(0), self.WORD_SIZE, Reg.a(0), node.row, node.column, "Getting the String address")) # Getting the String address
        self.add_instruction(AddImmediateNode(Reg.v(0), Reg.zero(), 4, node.row, node.column, "4 System call code for print string")) # 4 System call code for print string
        self.add_instruction(SyscallNode())
        
    
    @visitor.when(cil.PrintIntNode)
    def visit(self, node:cil.PrintIntNode):
        self._load_value(Reg.a(0), node.int_addr,node.row, node.column, node.comment)
        self.add_instruction(AddImmediateNode(Reg.v(0), Reg.zero(), 1,node.row, node.column, node.comment)) # 1 System call code for print int
        self.add_instruction(SyscallNode(node.row, node.column, node.comment))
        
      
    
    @visitor.when(cil.ReadNode)
    def visit(self, node:cil.ReadNode):
        self.add_instruction(LoadImmediateNode(Reg.a(1), self.MAX_STRING_LENGTH, node.row, node.column, "a1 = Allocated length Save the length in a1")) # a1 = Allocated length Save the length in a1
        self._allocate_heap_space(Reg.a(1), node.row, node.column, "Allocates 1024 bytes and return the address un v0") # Allocates 1024 bytes and return the address un v0
        self.add_instruction(MoveNode(Reg.a(0), Reg.v(0), node.row, node.column, "a0 = v0 Save the address in a0")) # a0 = v0 Save the address in a0
        self.add_instruction(AddImmediateNode(Reg.v(0), Reg.zero(), 8, node.row, node.column, "8 System call code for read string")) # 8 System call code for read string
        self.add_instruction(SyscallNode(node.row, node.column, "Fills the address in a0 with the string")) # Fills the address in a0 with the string
        self.add_instruction(MoveNode(Reg.a(1), Reg.a(0), node.row, node.column, "a1 = a0 Save the address in a1")) # a1 = a0 Save the address in a1
        self._add_create_string_instance(Reg.t(0), Reg.a(1)) # Create String, Address instance 
        self._store_local_variable(Reg.v(0), node.dest, node.row, node.column, "Save the address in the final destination") # Save the address in the final destination
    
    @visitor.when(cil.ReadIntNode)
    def visit(self, node:cil.ReadIntNode):
        self.add_instruction(AddImmediateNode(Reg.v(0), Reg.zero(), 5,node.row, node.column, node.comment)) # 5 System call code for read int
        self.add_instruction(SyscallNode(node.row, node.column, node.comment)) # Returns the read integer in v0
        self._store_local_variable(Reg.v(0), node.dest,node.row, node.column, node.comment) 

    @visitor.when(cil.InitInstance)
    def visit(self, node:cil.InitInstance):
        self._load_local_variable(Reg.t(0), node.source) # Load object address in t0
        self._load_type_variable(Reg.t(1), node.instance_type) # Load type in t1
        self.add_instruction(StoreWordNode(Reg.t(1), 0, Reg.t(0))) # Assing type to first position in object address
        if node.instance_type == "String":
            self.add_instruction(LoadAddressNode(Reg.t(1), self.STRING_EMPTY)) # Init String with empty value
            self.add_instruction(StoreWordNode(Reg.t(1), self.WORD_SIZE, Reg.t(0))) # Save empty string address in value slot for String


    @visitor.when(cil.LoadNode)
    def visit(self, node:cil.LoadNode):
        self.add_instruction(LoadAddressNode(Reg.t(0), node.msg, node.row, node.column, node.comment))

        self._add_create_string_instance(Reg.t(1), Reg.t(0)) # Create String instance

        self._store_local_variable(Reg.v(0), node.dest, node.row, node.column, "Save string instance")
    
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
    
    
    @visitor.when(cil.GetAttribNode)
    def visit(self, node:cil.GetAttribNode):
        self._load_value(Reg.t(0), node.source,node.row, node.column, node.comment)  # Load the object address
        # Get the attribute offset
        attr_offset = self._attribute_index_to_offset(node.attribute_index)
        # Fetch the attribute value
        self.add_instruction(LoadWordNode(Reg.t(0), attr_offset, Reg.t(0),node.row, node.column, node.comment))
        # Assign attribute value
        self._store_local_variable(Reg.t(0), node.dest,node.row, node.column, node.comment)
    
    @visitor.when(cil.SetAttribNode)
    def visit(self, node:cil.SetAttribNode):
        self._load_value(Reg.t(0), node.source,node.row, node.column, node.comment)  # Load the object address
        # Get the attribute offset
        attr_offset = self._attribute_index_to_offset(node.attribute_index)
        # Load the value to be setted into t1
        self._load_value(Reg.t(1), node.value,node.row, node.column, node.comment)
        # Save the attribute value
        self.add_instruction(StoreWordNode(Reg.t(1), attr_offset, Reg.t(0),node.row, node.column, node.comment))

    
    @visitor.when(cil.GotoIfNode)
    def visit(self, node:cil.GotoIfNode):
        self._load_value(Reg.t(0), node.condition_value,node.row, node.column, node.comment) # Load condition value
        self.add_instruction(BranchNotEqualNode(Reg.t(0), Reg.zero(
        ), node.label, node.row, node.column, node.comment))  # Not 0 is True. If not zero jump to label
