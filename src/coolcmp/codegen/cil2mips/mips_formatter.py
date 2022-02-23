from coolcmp.utils import visitor
from coolcmp.utils import mips
from coolcmp.utils import registers


class MIPSFormatter:
    def __init__(self):
        pass

    @visitor.on("node")
    def visit(self, node):
        pass

    @visitor.when(mips.ProgramNode)
    def visit(self, node: mips.ProgramNode):
        data = "\n# data\n.data\n" + "\n".join(self.visit(d) for d in node.data)
        functions = "\n# functions\n.text\n" + "\n".join(
            self.visit(f) for f in node.functions
        )
        return data + "\n" + functions

    @visitor.when(mips.FunctionNode)
    def visit(self, node: mips.FunctionNode):
        print(node.name, node.instructions)
        return f"{node.name}:\n\t" + f"\n\t".join(
            self.visit(ins) for ins in node.instructions
        )

    @visitor.when(str)
    def visit(self, node: str):
        return node

    @visitor.when(int)
    def visit(self, node: int):
        return node

    @visitor.when(mips.StringNode)
    def visit(self, node: mips.StringNode):
        return f"{node.label}: .asciiz {node.value}"

    @visitor.when(registers.Register)
    def visit(self, node: registers.Register):
        return f"${node.name}"

    @visitor.when(mips.LINode)
    def visit(self, node: mips.LINode):
        return f"li {self.visit(node.reg)}, {node.value}"

    @visitor.when(mips.LANode)
    def visit(self, node: mips.LANode):
        return f"la {self.visit(node.reg)}, {node.value}"

    @visitor.when(mips.SysCallNode)
    def visit(self, node: mips.SysCallNode):
        return "syscall"

    @visitor.when(mips.JRNode)
    def visit(self, node: mips.JRNode):
        return "jr $ra"

    @visitor.when(mips.LWNode)
    def visit(self, node: mips.LWNode):
        return f"lw {self.visit(node.dest)}, {node.offset}({self.visit(node.src)})"

    @visitor.when(mips.SWNode)
    def visit(self, node: mips.SWNode):
        return f"sw {self.visit(node.dest)}, {node.offset}({self.visit(node.src)})"

    @visitor.when(mips.ADDINode)
    def visit(self, node: mips.ADDINode):
        return f"addi {self.visit(node.dest)}, {self.visit(node.src)}, {self.visit(node.isrc)}"
