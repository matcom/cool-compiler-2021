from typing import List

from coolcmp.utils import visitor
from coolcmp.utils import mips
from coolcmp.utils import registers
from coolcmp.codegen.cil2mips.templates import load_templates


def generate_type_labels(types: List[mips.Type]):
    type_label_lines = [f"\t.word \t\t prototype_{t.label}" for t in types]
    return f"{mips.PROTOTYPES}:\n" + "\n".join(type_label_lines) + "\n"


class MIPSFormatter:
    def __init__(self):
        pass

    @visitor.on("node")
    def visit(self, node):
        pass

    @visitor.when(mips.ProgramNode)
    def visit(self, node: mips.ProgramNode):
        data = "\n# data\n.data\n" + "\n".join(self.visit(d) for d in node.data)

        template_code = load_templates()
        type_labels = generate_type_labels(node.types)
        type_defs = "\n\n".join([self.visit(t) for t in node.types])

        functions = "\n# functions\n.text\n" + "\n".join(
            self.visit(f) for f in node.functions
        )
        return "\n".join([data, type_labels, type_defs, functions, template_code])

    @visitor.when(mips.Type)
    def visit(self, node: mips.Type):
        methods = "\n".join(f"\t.word\t {i}" for i in node.methods)
        dispatch_labels = f"dispatch_{node.label}:\n{methods}"

        proto_begin = f"prototype_{node.label}:\n\t.word\t{node.index}\n\t.word\t{node.length()}\n\t.word\tdispatch_{node.label}"
        proto_attr = "\n".join([f"\t.word\t0" for _ in node.attrs])
        proto_end = f"\t.word\t-1"
        proto = (
            f"{proto_begin}\n{proto_attr}\n{proto_end}"
            if proto_attr != ""
            else f"{proto_begin}\n{proto_end}"
        )

        return f"{dispatch_labels}\n\n{proto}"

    @visitor.when(mips.FunctionNode)
    def visit(self, node: mips.FunctionNode):
        return f"{node.name}:\n\t" + f"\n\t".join(
            self.visit(ins) for ins in node.instructions
        )

    @visitor.when(mips.JALNode)
    def visit(self, node: mips.JALNode):
        return f"jal {self.visit(node.dest)}"

    @visitor.when(mips.SLLNode)
    def visit(self, node: mips.SLLNode):
        return f"sll {self.visit(node.dest)}, {self.visit(node.src)}, {self.visit(node.bits)}"

    @visitor.when(mips.MoveNode)
    def visit(self, node: mips.MoveNode):
        return f"move {self.visit(node.reg1)}, {self.visit(node.reg2)}"

    @visitor.when(str)
    def visit(self, node: str):
        return node

    @visitor.when(int)
    def visit(self, node: int):
        return node

    @visitor.when(mips.StringNode)
    def visit(self, node: mips.StringNode):
        return f"{node.label}: .asciiz {repr(node.value)[1:-1]}"

    @visitor.when(registers.Register)
    def visit(self, node: registers.Register):
        return f"${node.name}"

    @visitor.when(mips.LINode)
    def visit(self, node: mips.LINode):
        return f"li {self.visit(node.reg)}, {node.value}"

    @visitor.when(mips.LANode)
    def visit(self, node: mips.LANode):
        return f"la {self.visit(node.reg)}, {node.label}"

    @visitor.when(mips.SysCallNode)
    def visit(self, node: mips.SysCallNode):
        return "syscall"

    @visitor.when(mips.JRNode)
    def visit(self, node: mips.JRNode):
        return f"jr {self.visit(node.dest)}"

    @visitor.when(mips.LWNode)
    def visit(self, node: mips.LWNode):
        return f"lw {self.visit(node.dest)}, {node.offset}({self.visit(node.src)})"

    @visitor.when(mips.SWNode)
    def visit(self, node: mips.SWNode):
        return f"sw {self.visit(node.dest)}, {node.offset}({self.visit(node.src)})"

    @visitor.when(mips.ADDNode)
    def visit(self, node: mips.ADDNode):
        return f"add {self.visit(node.dest)} {self.visit(node.src1)} {self.visit(node.src2)}"

    @visitor.when(mips.ADDINode)
    def visit(self, node: mips.ADDINode):
        return f"addi {self.visit(node.dest)}, {self.visit(node.src)}, {self.visit(node.isrc)}"
