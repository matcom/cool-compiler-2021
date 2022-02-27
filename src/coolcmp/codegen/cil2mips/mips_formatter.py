from typing import List

from coolcmp.utils import visitor
from coolcmp.utils import mips
from coolcmp.codegen.cil2mips.templates import load_templates


def generate_type_labels(types: List[mips.Type]):
    type_label_lines = [f"\t.word \t\t {t.label}" for t in types]
    return f"{mips.PROTOTYPES}:\n" + "\n".join(type_label_lines) + "\n"


class MIPSFormatter:
    def __init__(self):
        pass

    @visitor.on("node")
    def visit(self, node):
        pass

    @visitor.when(mips.ProgramNode)
    def visit(self, node: mips.ProgramNode):
        data = "# data\n.data\n" + "\n".join(self.visit(d) for d in node.data)
        type_defs = f"\n{mips.TYPES_LABELS}:\n" + "\n\n".join(
            [self.visit(t) for t in node.types]
        )
        functions = "\n# functions\n.text\n" + "\n".join(
            self.visit(f) for f in node.functions
        )
        inits_seg = ""
        for type_ in node.types:
            inits_seg += (f"_{type_.label}_init:\n\t" +
                          "\n\t".join(str(inst) for inst in type_.init) +
                          "\n")
        template_code = load_templates()

        return "\n".join([data, type_defs, functions, inits_seg, template_code])

    @visitor.when(mips.Type)
    def visit(self, node: mips.Type):
        method_labels = "\n".join(f"\t.word\t{i}" for i in node.methods)
        typename_label = f'\t.asciiz\t"{node.label}"'

        lines = [
            f"{node.label}:",
            f"\t.word\t{(node.length() + 1) * 4}",
            method_labels,
            typename_label,
        ]
        return "\n".join(lines).replace("\n\n", "\n")

    @visitor.when(mips.FunctionNode)
    def visit(self, node: mips.FunctionNode):
        return f"{node.name}:\n\t" + f"\n\t".join(
            self.visit(ins) for ins in node.instructions
        )

    @visitor.when(mips.Node)
    def visit(self, node: mips.Node):
        return str(node)

    # @visitor.when(mips.JALNode)
    # def visit(self, node: mips.JALNode):
    #     return f"jal {node.dest}"
    #
    # @visitor.when(mips.SLLNode)
    # def visit(self, node: mips.SLLNode):
    #     return f"sll {node.dest}, {node.src}, {node.bits}"
    #
    # @visitor.when(mips.MoveNode)
    # def visit(self, node: mips.MoveNode):
    #     return f"move {node.reg1}, {node.reg2}"
    #
    # @visitor.when(str)
    # def visit(self, node: str):
    #     return node
    #
    # @visitor.when(int)
    # def visit(self, node: int):
    #     return node
    #
    # @visitor.when(mips.StringNode)
    # def visit(self, node: mips.StringNode):
    #     return f"{node.label}: .asciiz {repr(node.value)[1:-1]}"
    #
    # @visitor.when(mips.LINode)
    # def visit(self, node: mips.LINode):
    #     return f"li {node.reg}, {node.value}"
    #
    # @visitor.when(mips.LANode)
    # def visit(self, node: mips.LANode):
    #     return f"la {node.reg}, {node.label}"
    #
    # @visitor.when(mips.SysCallNode)
    # def visit(self, _: mips.SysCallNode):
    #     return "syscall"
    #
    # @visitor.when(mips.JRNode)
    # def visit(self, node: mips.JRNode):
    #     return f"jr {node.dest}"
    #
    # @visitor.when(mips.LWNode)
    # def visit(self, node: mips.LWNode):
    #     return str(node)
    #
    # @visitor.when(mips.SWNode)
    # def visit(self, node: mips.SWNode):
    #     return f"sw {node.dest}, {node.offset}({node.src})"
    #
    # @visitor.when(mips.ADDNode)
    # def visit(self, node: mips.ADDNode):
    #     return f"add {node.dest} {node.src1} {node.src2}"
    #
    # @visitor.when(mips.ADDINode)
    # def visit(self, node: mips.ADDINode):
    #     return f"addi {node.dest}, {node.src}, {node.isrc}"
    #
    # @visitor.when(mips.CommentNode)
    # def visit(self, node: mips.CommentNode):
    #     return f"# {node.text}"
    #
    # @visitor.when(mips.SUBNode)
    # def visit(self, node: mips.SUBNode):
    #     return f"sub {node.rdest}, {node.r1}, {node.r2},"
