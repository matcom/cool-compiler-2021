from __future__ import annotations
from typing import Dict

from coolcmp.utils import cil, visitor
from coolcmp.utils import mips, registers


class CILToMipsVisitor:
    def __init__(self):
        self.data: Dict[str, mips.Node] = {}
        self.types: Dict[str, mips.Type] = {}
        self.functions: Dict[str, mips.FunctionNode] = {}
        self.cur_function: mips.FunctionNode | None = None

    def add_inst(self, *inst: mips.InstructionNode) -> None:
        self.cur_function.instructions.extend(inst)

    @visitor.on("node")
    def visit(self, node):
        pass

    @visitor.when(cil.ProgramNode)
    def visit(self, node: cil.ProgramNode):
        print("ProgramNode")

        for i in node.dot_types:
            self.visit(i)
        for i in node.dot_data:
            self.visit(i)
        for i in node.dot_code:
            self.visit(i)

        return mips.ProgramNode(
            list(self.data.values()),
            list(self.types.values()),
            list(self.functions.values()),
        )

    @visitor.when(cil.TypeNode)
    def visit(self, node: cil.TypeNode):
        print(f"TypeNode {node.name} {node.methods}")
        self.data[node.name] = mips.StringNode(node.name, f'"{node.name}"')

        type_ = mips.Type(
            label=node.name,
            address=node.name,
            attrs=list(node.attributes),
            methods=node.methods,
            index=len(self.types),
            default=[],
        )

        self.types[node.name] = type_

    @visitor.when(cil.DataNode)
    def visit(self, node: cil.DataNode):
        print(f"DataNode {node.name} {node.value}")
        self.data[node.name] = mips.StringNode(node.name, f"{node.value}")

    @visitor.when(cil.FunctionNode)
    def visit(self, node: cil.FunctionNode):
        print(f"FunctionNode {node.name}")
        params = [x.name for x in node.params]
        local_vars = [x.name for x in node.local_vars]

        local_vars_size = len(local_vars) * registers.DW

        self.cur_function = mips.FunctionNode(node.name, params, local_vars)
        self.functions[node.name] = self.cur_function

        # Push local vars
        push_instructions = (
                mips.push_register_instructions(registers.RA)
                + mips.push_register_instructions(registers.FP)
                + [mips.ADDINode(registers.FP, registers.SP, 8)]
                + [mips.ADDINode(registers.SP, registers.SP, -local_vars_size)]
        )

        self.add_inst(
            mips.CommentNode(f"<function:{node.name}>"),
            *push_instructions,
        )

        for instruction in node.instructions:
            self.visit(instruction)

        # Pop local vars
        pop_instructions = (
                [mips.ADDINode(registers.SP, registers.SP, local_vars_size)]
                + mips.pop_register_instructions(registers.FP)
                + mips.pop_register_instructions(registers.RA)
        )

        return_instructions = (
            [mips.LINode(registers.V0, 10), mips.SysCallNode()]
            if self.cur_function.name == "main"
            else [mips.JRNode(registers.RA)]
        )

        self.add_inst(
            *pop_instructions,
            *return_instructions,
            mips.CommentNode(f"</function:{node.name}>")
        )

    @visitor.when(cil.AllocateNode)
    def visit(self, node: cil.AllocateNode):
        print(f"AllocateNode {node.type} {node.dest}")

        # TODO: Finish this
        type_ = self.types[node.type].index

        t0 = registers.T[0]
        t1 = registers.T[1]

        self.add_inst(
            mips.CommentNode(f"<allocate:{node.type}-{node.dest}>"),
            mips.LINode(t0, type_),
            *mips.create_object_instructions(t0, t1),
        )

        self.visit(node.dest)

        address = self.cur_function.variable_address(node.dest)
        self.add_inst(
            mips.SWNode(registers.V0, address, registers.FP),
            mips.CommentNode(f"</allocate:{node.type}-{node.dest}>")
        )

    @visitor.when(cil.ReturnNode)
    def visit(self, node: cil.ReturnNode):
        value = 0 if node.value is None else node.value

        if node.value is None:
            value = 0
        elif isinstance(node.value, int):
            value = node.value
        else:
            pass
        # TODO: Handle returns

        self.add_inst(
            mips.CommentNode("<return>"),
            mips.CommentNode("</return>"),
        )

    @visitor.when(cil.PrintIntNode)
    def visit(self, node: cil.PrintIntNode):
        print(f"PrintIntNode {node.addr}")
        self.add_inst(
            mips.CommentNode(f"<printint:{node.addr}>"),
            mips.LINode(registers.V0, 1),
        )

        address = self.cur_function.variable_address(node.addr)
        print(self.cur_function.variable_address(node.addr))
        input()

        self.add_inst(
            mips.LWNode(registers.ARG[0], address, registers.FP),
            mips.SysCallNode(),
            mips.CommentNode(f"</printint:{node.addr}>"),
        )

    @visitor.when(cil.PrintStringNode)
    def visit(self, node: cil.PrintStringNode):
        """ """
        address = self.cur_function.variable_address(node.addr)
        self.add_inst(
            mips.CommentNode(f"<printstring:{node.addr}>"),
            mips.LINode(registers.V0, 4),
            mips.LWNode(registers.ARG[0], address, registers.FP),
            mips.LANode(registers.A0, node.addr),
            mips.SysCallNode(),
            mips.CommentNode(f"</printstring:{node.addr}>"),
        )

    @visitor.when(cil.DynamicCallNode)
    def visit(self, node: cil.DynamicCallNode):
        print(f"DynamicCallNode {node.method} {node.type} {node.dest}")

        self.add_inst(
            mips.CommentNode(f"<dynamiccall:{node.type}>"),
            mips.CommentNode(f"</dynamiccall:{node.type}>"),
        )

    @visitor.when(cil.TypeOfNode)
    def visit(self, node: cil.TypeOfNode):
        r1, r2 = registers.T[0], registers.T[1]
        self.add_inst(
            mips.CommentNode(f"<typeof:{node.obj}>"),
            mips.CommentNode(f"</typeof:{node.obj}>"),
        )

    @visitor.when(cil.PlusNode)
    def visit(self, node: cil.PlusNode):
        """
        assuming left and right operands are ints
        """
        t0, t1, t2 = registers.T[0], registers.T[1], registers.T[2]

        self.add_inst(
            mips.CommentNode(f"<sum:{node.dest}<-{node.left}+{node.right}>"),
            mips.LINode(t0, node.left),
            mips.LINode(t1, node.right),
            mips.ADDNode(t2, t0, t1),
            mips.CommentNode(f"</sum:{node.dest}<-{node.left}+{node.right}>"),
        )

    @visitor.when(cil.LoadNode)
    def visit(self, node: cil.LoadNode):

        t0 = registers.T[0]
        dest_address = self.cur_function.variable_address(node.dest)

        self.add_inst(
            mips.CommentNode(f"<loadnode:{node.dest}-{node.msg}>"),
            mips.LANode(t0, node.dest),
            mips.SWNode(t0, dest_address, registers.FP),
            mips.CommentNode(f"</loadnode:{node.dest}-{node.msg}>"),
        )

    @visitor.when(cil.AssignNode)
    def visit(self, node: cil.AssignNode):
        t0 = registers.T[0]

        self.add_inst(
            mips.CommentNode(f"<assignode:{node.dest}-{node.source}>"),
            mips.LWNode(t0, 0, node.source),
            mips.SWNode(t0, 0, node.dest),
            mips.CommentNode(f"</assignode:{node.dest}-{node.source}>"),
        )
