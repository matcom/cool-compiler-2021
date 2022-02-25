from asts.mips_ast import (
    Add,
    Addi,
    Addu,
    BranchOnEqual,
    BranchOnNotEqual,
    Constant,
    Div,
    Equal,
    Jump,
    JumpAndLink,
    JumpRegister,
    Label,
    LabelDeclaration,
    Less,
    LessOrEqual,
    LoadAddress,
    LoadImmediate,
    MIPSProgram,
    MemoryIndexNode,
    Move,
    Multiply,
    Not,
    RegisterNode,
    Sub,
    Subu,
    Syscall,
    TextNode,
    DataNode,
    WordDirective,
    Xori,
)
from utils import visitor


class MIPSGenerator:
    """
    This class uses the visitor pattern to convert MIPS AST to a .mips program
    """

    def __init__(self) -> None:
        pass

    @visitor.on("node")
    def visit(self, node):
        pass

    @visitor.when(MIPSProgram)
    def visit(self, node: MIPSProgram) -> str:
        global_main = "\t.globl main"
        text_section = "\t.text\n" + self.visit(node.text_section)
        data_section = "\t.data\n" + self.visit(node.data_section)
        return f"{global_main}\n{text_section}\n{data_section}"

    @visitor.when(TextNode)
    def visit(self, node: TextNode) -> str:
        return "\n".join(self.visit(instruction) for instruction in node.instructions)

    @visitor.when(DataNode)
    def visit(self, node: DataNode) -> str:
        data_section = ""
        for label_decl, directive in node.data:
            data_section += f"{self.visit(label_decl)} {self.visit(directive)}\n"
        return data_section

    @visitor.when(RegisterNode)
    def visit(self, node: RegisterNode) -> str:
        return f"${node.number}"

    @visitor.when(Constant)
    def visit(self, node: Constant) -> str:
        return str(node.value)

    @visitor.when(LabelDeclaration)
    def visit(self, node: LabelDeclaration) -> str:
        return f"{node.idx}:"

    @visitor.when(Label)
    def visit(self, node: Label) -> str:
        return str(node.idx)

    @visitor.when(JumpAndLink)
    def visit(self, node: JumpAndLink) -> str:
        return f"\tjal {self.visit(node.address)}"

    @visitor.when(Jump)
    def visit(self, node: Jump) -> str:
        return f"\tj {self.visit(node.address)}"

    @visitor.when(JumpRegister)
    def visit(self, node: JumpRegister) -> str:
        return f"\tj {self.visit(node.register)}"

    @visitor.when(MemoryIndexNode)
    def visit(self, node: MemoryIndexNode) -> str:
        return f"{self.visit(node.address)}({self.visit(node.index)})"

    @visitor.when(WordDirective)
    def visit(self, node: WordDirective) -> str:
        return ".word " + (" ".join(self.visit(i) for i in node.list))

    @visitor.when(Move)
    def visit(self, node: Move) -> str:
        return f"\tmove {self.visit(node.left)}, {self.visit(node.right)}"

    @visitor.when(Subu)
    def visit(self, node: Subu) -> str:
        return f"\tsubu {self.visit(node.left)}, {self.visit(node.middle)}, {self.visit(node.right)}"

    @visitor.when(Sub)
    def visit(self, node: Sub) -> str:
        return f"\tsub {self.visit(node.left)}, {self.visit(node.middle)}, {self.visit(node.right)}"

    @visitor.when(Addu)
    def visit(self, node: Addu) -> str:
        return f"\taddu {self.visit(node.left)}, {self.visit(node.middle)}, {self.visit(node.right)}"

    @visitor.when(LoadAddress)
    def visit(self, node: LoadAddress) -> str:
        return f"\tla {self.visit(node.left)},  {self.visit(node.right)}"

    @visitor.when(LoadImmediate)
    def visit(self, node: LoadImmediate) -> str:
        return f"\tli {self.visit(node.left)},  {self.visit(node.right)}"

    @visitor.when(Syscall)
    def visit(self, node: Syscall) -> str:
        return f"\tsyscall"

    @visitor.when(Add)
    def visit(self, node: Add) -> str:
        return f"\tadd {self.visit(node.left)}, {self.visit(node.middle)}, {self.visit(node.right)}"

    @visitor.when(Addi)
    def visit(self, node: Addi) -> str:
        return f"\taddi {self.visit(node.left)}, {self.visit(node.middle)}, {self.visit(node.right)}"

    @visitor.when(Multiply)
    def visit(self, node: Multiply) -> str:
        return f"\tmul {self.visit(node.left)}, {self.visit(node.middle)}, {self.visit(node.right)}"

    @visitor.when(Div)
    def visit(self, node: Div) -> str:
        return f"\tdiv {self.visit(node.left)}, {self.visit(node.right)}"

    @visitor.when(BranchOnEqual)
    def visit(self, node: BranchOnEqual) -> str:
        return f"\tbeq {self.visit(node.left)}, {self.visit(node.middle)}, {self.visit(node.right)}"

    @visitor.when(BranchOnEqual)
    def visit(self, node: BranchOnNotEqual) -> str:
        return f"\tbne {self.visit(node.left)}, {self.visit(node.middle)}, {self.visit(node.right)}"

    @visitor.when(Less)
    def visit(self, node: Less) -> str:
        return f"\tslt {self.visit(node.left)}, {self.visit(node.middle)}, {self.visit(node.right)}"

    @visitor.when(LessOrEqual)
    def visit(self, node: LessOrEqual) -> str:
        return f"\tsle {self.visit(node.left)}, {self.visit(node.middle)}, {self.visit(node.right)}"

    @visitor.when(Equal)
    def visit(self, node: Equal) -> str:
        return f"\tseq {self.visit(node.left)}, {self.visit(node.middle)}, {self.visit(node.right)}"

    @visitor.when(Xori)
    def visit(self, node: Xori) -> str:
        return f"\txori {self.visit(node.left)}, {self.visit(node.middle)}, {self.visit(node.right)}"

    @visitor.when(Not)
    def visit(self, node: Not) -> str:
        return f"\tnot {self.visit(node.left)}, {self.visit(node.right)}"
