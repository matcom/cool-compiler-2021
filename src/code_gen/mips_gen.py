from asts.mips_ast import (
    Label,
    LabelDeclaration,
    MIPSProgram,
    MemoryIndexNode,
    Move,
    RegisterNode,
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
        return "\n".join(self.visit(instruction) for instruction in node.instructions)

    @visitor.when(RegisterNode)
    def visit(self, node: RegisterNode) -> str:
        return f"${node.number}"

    @visitor.when(LabelDeclaration)
    def visit(self, node: LabelDeclaration) -> str:
        return f"{node.idx}:"

    @visitor.when(Label)
    def visit(self, node: Label) -> str:
        return str(node.idx)

    @visitor.when(MemoryIndexNode)
    def visit(self, node: MemoryIndexNode) -> str:
        return f"{self.visit(node.address)}({self.visit(node.index)})"

    @visitor.when(WordDirective)
    def visit(self, node: WordDirective) -> str:
        return ".word " + " ".join(self.visit(i) for i in node.list)

    @visitor.when(Move)
    def visit(self, node: Move) -> str:
        return f"\tmove {self.visit(node.left)}, {self.visit(node.right)}"
