from mips.ast.mips_ast import *
import cmp.visitor as visitor
import cool.ast.cil_ast as cil
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
        return f"{node.name}: {node.type} {node.value}"
    
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
    
    def __init__(self, errors=[]) -> None:
        self.errors = errors
        self.program_node = None
    
    def add_instruction(self, instr:Node):
        self.program_node.instructions.append(instr)
    
    def add_data(self, data: DataNode):
        self.program_node.data.append(data)
    
    @visitor.on('node')
    def visit(self, node):
        pass
    
    @visitor.when(cil.ProgramNode)
    def visit(self, node:cil.ProgramNode):
        # EXAMPLE HELLO WORLD

        program = ProgramNode("TODO Change this message for a meaningful one")
        self.program_node = program
        self.add_instruction(LabelNode("main",comment="Entry function"))
        self.add_instruction(LoadAddressNode(Reg.a(0), "hello_world",comment="Load message direction"))
        self.add_instruction(AddImmediateNode(Reg.v(0), Reg.zero(), 4, comment="$v0 = 4 For printing string"))
        self.add_instruction(SyscallNode(comment="Prints Hello world"))
        self.add_instruction(AddImmediateNode(Reg.v(0), Reg.zero(), 10, comment="$v0 = 10 For exit"))
        self.add_instruction(SyscallNode(comment="Exit"))
        self.add_data(ASCIIZNode("hello_world", '"Hello World\\n"', comment="Message to print"))
        
        return program
