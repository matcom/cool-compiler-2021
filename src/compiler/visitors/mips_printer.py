from compiler.cmp.mips_ast import *
from compiler.visitors import visitor


class MIPSPrintVisitor:
    @visitor.on("node")
    def visit(self, node):
        pass

    @visitor.when(Register)
    def visit(self, node):
        return f"${node.name}"

    @visitor.when(int)
    def visit(self, node):
        return str(node)

    @visitor.when(str)
    def visit(self, node):
        return node

    @visitor.when(ProgramNode)
    def visit(self, node):
        data_section_header = "\t.data"
        static_strings = "\n".join([self.visit(d) for d in node.data])

        names_table = f"{TYPE_LIST}:\n\t .word " + ", ".join(
            [f"{tp.data_label}" for tp in node.types]
        )
        virtual_table = f"{VIRTUAL_TABLE}:\n\t .word " + ", ".join(
            [f"{tp.type_label}_dispatch" for tp in node.types]
        )

        types = "\n\n".join([self.visit(tp) for tp in node.types])

        code = "\n".join([self.visit(func) for func in node.text])
        return f"{data_section_header}\n{static_strings}\n\n{names_table}\n\n{virtual_table}\n\n{types}\n\n.text\n\t.globl main\n{code}"

    @visitor.when(StringConst)
    def visit(self, node):
        return f'{node.label}: .asciiz "{node.string}"'

    @visitor.when(TypeNode)
    def visit(self, node: TypeNode):
        print(node.data_label, ":")
        print(node.attributes)
        methods = ", ".join([f"{node.methods[m]}" for m in node.methods])
        dispatch_table = f"{node.type_label}_dispatch:\n\t .word {methods}"
        # proto_begin = f"{node.type_label}_proto:\n\t.word\t{node.pos}, {len(node.attributes)*4}, {node.type_label}_dispatch"
        # proto_attr = ", ".join(
        #     [f'{node.defaults.get(attr,"0")}' for attr in node.attributes]
        # )
        # proto_end = f"{-1}"
        # proto = (
        #     f"{proto_begin}, {proto_attr}, {proto_end}"
        #     if proto_attr != ""
        #     else f"{proto_begin}, {proto_end}"
        # )

        # return f"{dispatch_table}\n\n{proto}"
        return f"{dispatch_table}"

    @visitor.when(SyscallNode)
    def visit(self, node):
        return "syscall"

    @visitor.when(LabelRelativeLocation)
    def visit(self, node):
        return f"{node.label} + {node.offset}"

    @visitor.when(RegisterRelativeLocation)
    def visit(self, node):
        return f"{node.offset}({self.visit(node.register)})"

    @visitor.when(FunctionNode)
    def visit(self, node):
        instr = [self.visit(instruction) for instruction in node.instructions]
        # TODO la linea de abajo sobra, es necesaria mientras la traduccion del AST de CIL este incompleta
        instr2 = [inst for inst in instr if type(inst) == str]
        instructions = "\n\t".join(instr2)
        return f"{node.label}:\n\t{instructions}"

    @visitor.when(AddInmediateNode)
    def visit(self, node):
        return f"addi {self.visit(node.dest)}, {self.visit(node.src)}, {self.visit(node.constant_number)}"

    @visitor.when(StoreWordNode)
    def visit(self, node):
        return f"sw {self.visit(node.reg)}, {self.visit(node.addr)}"

    @visitor.when(LoadInmediateNode)
    def visit(self, node):
        return f"li {self.visit(node.reg)}, {self.visit(node.value)}"

    @visitor.when(JumpAndLinkNode)
    def visit(self, node):
        return f"jal {node.label}"

    @visitor.when(JumpRegister)
    def visit(self, node):
        return f"jr {self.visit(node.reg)}"

    @visitor.when(JumpRegisterAndLinkNode)
    def visit(self, node):
        return f"jalr {self.visit(node.reg)}"

    @visitor.when(LoadWordNode)
    def visit(self, node):
        return f"lw {self.visit(node.reg)}, {self.visit(node.addr)}"

    @visitor.when(LoadAddressNode)
    def visit(self, node):
        return f"la {self.visit(node.reg)}, {self.visit(node.label)}"

    @visitor.when(MoveNode)
    def visit(self, node):
        return f"move {self.visit(node.reg1)} {self.visit(node.reg2 )}"

    @visitor.when(ShiftLeftLogicalNode)
    def visit(self, node):
        return f"sll {self.visit(node.dest)} {self.visit(node.src)} {node.bits}"

    @visitor.when(AddInmediateUnsignedNode)
    def visit(self, node):
        return f"addiu {self.visit(node.dest)} {self.visit(node.src)} {self.visit(node.value)}"

    @visitor.when(AddUnsignedNode)
    def visit(self, node):
        return f"addu {self.visit(node.dest)} {self.visit(node.sum1)} {self.visit(node.sum2)}"

    @visitor.when(LabelNode)
    def visit(self, node):
        return f"{node.label}:"

    @visitor.when(BranchOnNotEqualNode)
    def visit(self, node):
        return f"bne {self.visit(node.reg1)} {self.visit(node.reg2)} {node.label}"

    @visitor.when(JumpNode)
    def visit(self, node):
        return f"j {node.label}"

    @visitor.when(AddNode)
    def visit(self, node):
        return f"add {self.visit(node.reg1)} {self.visit(node.reg2)} {self.visit(node.reg3)}"

    @visitor.when(SubNode)
    def visit(self, node):
        return f"sub {self.visit(node.reg1)} {self.visit(node.reg2)} {self.visit(node.reg3)}"

    @visitor.when(MultiplyNode)
    def visit(self, node):
        return f"mul {self.visit(node.reg1)} {self.visit(node.reg2)} {self.visit(node.reg3)}"

    @visitor.when(DivideNode)
    def visit(self, node):
        return f"div {self.visit(node.reg1)} {self.visit(node.reg2)}"

    @visitor.when(ComplementNode)
    def visit(self, node):
        return f"not {self.visit(node.reg1)} {self.visit(node.reg2)}"

    @visitor.when(MoveFromLowNode)
    def visit(self, node):
        return f"mflo {self.visit(node.reg)}"
