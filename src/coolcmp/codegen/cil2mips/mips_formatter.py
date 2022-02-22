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
        functions = "\n# functions\n" + "\n".join(self.visit(f) for f in node.functions)
        return data + "\n" + functions

    @visitor.when(mips.FunctionNode)
    def visit(self, node: mips.FunctionNode):
        return f"{node.name}:\n\t" + f"\n\t".join(
            self.visit(ins) for ins in node.instructions
        )

    @visitor.when(str)
    def visit(self, node: str):
        return node

    @visitor.when(int)
    def visit(self, node: int):
        return node

    @visitor.when(registers.Register)
    def visit(self, node: registers.Register):
        return node.name

    @visitor.when(mips.StringNode)
    def visit(self, node: mips.StringNode):
        return f"{node.label}: .asciiz {node.value}"

    @visitor.when(mips.LINode)
    def visit(self, node: mips.LINode):
        register = self.visit(node.reg)
        value = self.visit(node.value)
        return f"li {register} {value}"
