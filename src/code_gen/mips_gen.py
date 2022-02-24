from asts.mips_ast import (
    Add,
    Addi,
    Addu,
    BranchOnEqual,
    BranchOnNotEqual,
    Constant,
    Jump,
    JumpAndLink,
    JumpRegister,
    Label,
    LabelDeclaration,
    LoadAddress,
    LoadImmediate,
    MIPSProgram,
    MemoryIndexNode,
    Move,
    Multiply,
    MultiplyOpNode,
    RegisterNode,
    Sub,
    Subu,
    Syscall,
    TextNode,
    DataNode,
    WordDirective,
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
        return f"\tjal {node.address}"

    @visitor.when(Jump)
    def visit(self, node: Jump) -> str:
        return f"\tj {node.address}"

    @visitor.when(JumpRegister)
    def visit(self, node: JumpRegister) -> str:
        return f"\tj {node.register}"

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
        return f"\tsubu {node.left}, {node.middle}, {node.right}"

    @visitor.when(Sub)
    def visit(self, node: Sub) -> str:
        return f"\tsub {node.left}, {node.middle}, {node.right}"

    @visitor.when(Addu)
    def visit(self, node: Addu) -> str:
        return f"\taddu {node.left}, {node.middle}, {node.right}"

    @visitor.when(LoadAddress)
    def visit(self, node: LoadAddress) -> str:
        return f"\tla {node.left},  {node.right}"

    @visitor.when(LoadImmediate)
    def visit(self, node: LoadImmediate) -> str:
        return f"\tli {node.left},  {node.right}"

    @visitor.when(Syscall)
    def visit(self, node: Syscall) -> str:
        return f"\tsyscall"

    @visitor.when(Add)
    def visit(self, node: Add) -> str:
        return f"\tadd {node.left}, {node.middle}, {node.right}"

    @visitor.when(Addi)
    def visit(self, node: Addi) -> str:
        return f"\taddi {node.left}, {node.middle}, {node.right}"

    @visitor.when(Multiply)
    def visit(self, node: Multiply) -> str:

    @visitor.when(BranchOnEqual)
    def visit(self, node: BranchOnEqual) -> str:
        return f"\tbeq {node.left}, {node.middle}, {node.right}"

    @visitor.when(BranchOnEqual)
    def visit(self, node: BranchOnNotEqual) -> str:
        return f"\tbne {node.left}, {node.middle}, {node.right}"
