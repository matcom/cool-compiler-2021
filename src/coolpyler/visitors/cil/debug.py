import sys

import coolpyler.ast.cil.base as cil
import coolpyler.utils.visitor as visitor


class CILDebug:
    def __init__(self, file=sys.stdout):
        self.types_table = []
        self.location = dict()
        self.file = file

    def print(self, indent_size, inline, *args, **kwargs):
        print(" " * indent_size, file=self.file, end="")
        return print(*args, **kwargs, file=self.file, end=("" if inline else "\n"))

    @visitor.on("node")
    def visit(self, node):
        pass

    @visitor.when(cil.ProgramNode)
    def visit(self, node: cil.ProgramNode, indent=0, inline=False):
        self.print(indent, inline, ".types\n")
        for type in node.dottypes:
            self.visit(type, indent + 2)
        print(file=self.file)

        self.print(indent, inline, ".data\n")
        for type in node.dotdata:
            self.visit(type, indent + 2)
        print(file=self.file)

        self.print(indent, inline, ".code\n")
        for type in node.dotcode:
            self.visit(type, indent + 2)
            print(file=self.file)

        return node

    @visitor.when(cil.TypeNode)
    def visit(self, node: cil.TypeNode, indent=0, inline=False):
        self.print(indent, inline, f"type {node.name} {{")
        for attr in node.attributes:
            self.print(indent + 2, inline, f"attribute {attr};")
        for method in node.methods:
            self.print(indent + 2, inline, f"method {method};")
        self.print(indent, inline, "}")

    @visitor.when(cil.DataNode)
    def visit(self, node: cil.DataNode, indent=0, inline=False):
        self.print(indent, inline, f"{node.name} = {node.value};")

    @visitor.when(cil.FunctionNode)
    def visit(self, node: cil.FunctionNode, indent=0, inline=False):
        self.print(indent, inline, f"function {node.name} {{")
        for param in node.params:
            self.visit(param, indent + 2)
        print(file=self.file)
        for local in node.localvars:
            self.visit(local, indent + 2)
        print(file=self.file)
        for inst in node.instructions:
            self.visit(inst, indent + 2)
        self.print(indent, inline, "}")

    @visitor.when(cil.ParamNode)
    def visit(self, node: cil.ParamNode, indent=0, inline=False):
        self.print(indent, inline, f"PARAM {node.name};")

    @visitor.when(cil.LocalNode)
    def visit(self, node: cil.LocalNode, indent=0, inline=False):
        self.print(indent, inline, f"LOCAL {node.name};")

    @visitor.when(cil.PlusNode)
    def visit(self, node: cil.PlusNode, indent=0, inline=False):
        self.print(indent, inline, f"{node.dest} = {node.left} + {node.right}")

    @visitor.when(cil.MinusNode)
    def visit(self, node: cil.MinusNode, indent=0, inline=False):
        self.print(indent, inline, f"{node.dest} = {node.left} - {node.right}")

    @visitor.when(cil.StarNode)
    def visit(self, node: cil.StarNode, indent=0, inline=False):
        self.print(indent, inline, f"{node.dest} = {node.left} * {node.right}")

    @visitor.when(cil.DivNode)
    def visit(self, node: cil.DivNode, indent=0, inline=False):
        self.print(indent, inline, f"{node.dest} = {node.left} / {node.right}")

    @visitor.when(cil.GetAttrNode)
    def visit(self, node: cil.GetAttrNode, indent=0, inline=False):
        self.print(
            indent, inline, f"{node.dest} = GETATTR {node.instance} {node.attr};"
        )

    @visitor.when(cil.SetAttrNode)
    def visit(self, node: cil.SetAttrNode, indent=0, inline=False):
        self.print(
            indent, inline, f"SETATTR {node.instance} {node.attr} {node.source};"
        )

    @visitor.when(cil.AllocateNode)
    def visit(self, node: cil.AllocateNode, indent=0, inline=False):
        self.print(indent, inline, f"{node.dest} = ALLOCATE {node.type};")

    @visitor.when(cil.TypeOfNode)
    def visit(self, node: cil.TypeOfNode, indent=0, inline=False):
        self.print(indent, inline, f"{node.dest} = TYPEOF {node.obj};")

    @visitor.when(cil.LabelNode)
    def visit(self, node: cil.LabelNode, indent=0, inline=False):
        self.print(indent, inline, f"LABEL {node.name};")

    @visitor.when(cil.GotoNode)
    def visit(self, node: cil.GotoNode, indent=0, inline=False):
        self.print(indent, inline, f"GOTO {node.label};")

    @visitor.when(cil.GotoIfNode)
    def visit(self, node: cil.GotoIfNode, indent=0, inline=False):
        self.print(indent, inline, f"IF {node.cond} GOTO {node.label};")

    @visitor.when(cil.StaticCallNode)
    def visit(self, node: cil.StaticCallNode, indent=0, inline=False):
        self.print(indent, inline, f"{node.dest} = CALL {node.function};")

    @visitor.when(cil.DynamicCallNode)
    def visit(self, node: cil.DynamicCallNode, indent=0, inline=False):
        self.print(indent, inline, f"{node.dest} = VCALL {node.type} {node.method};")

    @visitor.when(cil.ArgNode)
    def visit(self, node: cil.ArgNode, indent=0, inline=False):
        self.print(indent, inline, f"ARG {node.name};")

    @visitor.when(cil.ReturnNode)
    def visit(self, node: cil.ReturnNode, indent=0, inline=False):
        self.print(indent, inline, f"RETURN {node.value};")

    @visitor.when(cil.LoadNode)
    def visit(self, node: cil.LoadNode, indent=0, inline=False):
        self.print(indent, inline, f"{node.dest} = LOAD {node.msg};")

    @visitor.when(cil.LengthNode)
    def visit(self, node: cil.LengthNode, indent=0, inline=False):
        self.print(indent, inline, f"{node.dest} = length({node.string})")

    @visitor.when(cil.ConcatNode)
    def visit(self, node: cil.ConcatNode, indent=0, inline=False):
        self.print(indent, inline, f"{node.dest} = concat({node.string1}, {node.string2}, {node.dest_lenght})")

    @visitor.when(cil.SubstringNode)
    def visit(self, node: cil.SubstringNode, indent=0, inline=False):
        self.print(indent, inline, f"{node.dest} = substr({node.string}, {node.index}, {node.n})")

    @visitor.when(cil.ReadNode)
    def visit(self, node: cil.ReadNode, indent=0, inline=False):
        self.print(indent, inline, f"{node.dest} = read({'str' if node.is_string else 'int'})")

    @visitor.when(cil.PrintNode)
    def visit(self, node: cil.PrintNode, indent=0, inline=False):
        self.print(indent, inline, f"print({'str' if node.is_string else 'int'}, {node.str_addr}")
