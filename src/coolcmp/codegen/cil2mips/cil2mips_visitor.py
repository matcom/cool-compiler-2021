from __future__ import annotations
from typing import Dict, Set

from coolcmp.utils import cil, visitor
from coolcmp.utils import mips, registers


class CILToMipsVisitor:
    def __init__(self):
        self.data: Dict[str, mips.Node] = {}
        self.types: Dict[str, mips.Type] = {}
        self.functions: Dict[str, mips.FunctionNode] = {}
        self.cur_function: mips.FunctionNode = None

        self.labels = {}

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
            node.name,
            node.name,
            list(node.attributes),
            node.methods,
            len(self.types),
            [],
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

        function_node = mips.FunctionNode(node.name, params, local_vars)
        self.functions[node.name] = function_node
        self.cur_function = function_node
        self.labels = {}

        instructions = [f"# <function:{node.name}>"]

        # Push local vars
        push_instructions = (
            mips.push_register_instructions(registers.RA)
            + mips.push_register_instructions(registers.FP)
            + [mips.ADDINode(registers.FP, registers.SP, 8)]
            + [mips.ADDINode(registers.SP, registers.SP, -local_vars_size)]
        )
        instructions.extend(push_instructions)

        for instruction in node.instructions:
            instructions.extend(self.visit(instruction))

        # Pop local vars
        pop_instructions = (
            [mips.ADDINode(registers.SP, registers.SP, local_vars_size)]
            + mips.pop_register_instructions(registers.FP)
            + mips.pop_register_instructions(registers.RA)
        )
        instructions.extend(pop_instructions)

        return_instructions = (
            [mips.LINode(registers.V0, 10), mips.SysCallNode()]
            if self.cur_function.name == "main"
            else [mips.JRNode(registers.RA)]
        )
        instructions.extend(return_instructions)

        function_node.instructions = instructions
        self.cur_function = None

        instructions.extend([f"# </function:{node.name}>"])
        return instructions

    @visitor.when(cil.AllocateNode)
    def visit(self, node: cil.AllocateNode):
        print(f"AllocateNode {node.type} {node.dest}")

        # TODO: Finish this
        type_ = self.types[node.type].index

        t0 = registers.T[0]
        t1 = registers.T[1]

        instructions = [f"# <allocate:{node.type}-{node.dest}>"]
        instructions.append(mips.LINode(t0, type_))
        allocate_object_instructions = mips.create_object_instructions(t0, t1)
        instructions.extend(allocate_object_instructions)
        instructions.extend(self.visit(node.dest))

        address = self.cur_function.variable_address(node.dest)
        instructions.append(mips.SWNode(registers.V0, address, registers.FP))

        instructions.append(f"# </allocate:{node.type}-{node.dest}>")

        return instructions

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

        return ["# <return>", "# </return>"]

    @visitor.when(cil.PrintIntNode)
    def visit(self, node: cil.PrintIntNode):
        print(f"PrintIntNode {node.addr}")
        instructions = [f"# <printint:{node.addr}>"]

        instructions.append(mips.LINode(registers.V0, 1))

        address = self.cur_function.variable_address(node.addr)

        print(self.cur_function.variable_address(node.addr))
        input()

        instructions.append(mips.LWNode(registers.ARG[0], address, registers.FP))
        instructions.append(mips.SysCallNode())

        instructions.append(f"# </printint:{node.addr}>")
        return instructions

    @visitor.when(cil.PrintStringNode)
    def visit(self, node: cil.PrintStringNode):
        """ """
        li = mips.LINode(registers.V0, 4)
        address = self.cur_function.variable_address(node.addr)
        lw = mips.LWNode(registers.ARG[0], address, registers.FP)
        # la = mips.LANode(registers.A0, node.addr)
        syscall = mips.SysCallNode()

        return [
            f"# <printstring:{node.addr}>",
            li,
            lw,
            syscall,
            f"# </printstring:{node.addr}>",
        ]

    @visitor.when(cil.DynamicCallNode)
    def visit(self, node: cil.DynamicCallNode):
        print(f"DynamicCallNode {node.method} {node.type} {node.dest}")
        instructions = []
        node.type

        # print(self.types)
        # type_ = self.types[node.type]

        return [
            f"# <dynamiccall:{node.type}>",
            # f"{type_}",
            f"# </dynamiccall:{node.type}>",
        ]

    @visitor.when(cil.TypeOfNode)
    def visit(self, node: cil.TypeOfNode):
        return [f"# <typeof:{node.obj}>", f"# </typeof:{node.obj}>"]
        instructions = []

        r1, r2 = registers.T[0], registers.T[1]

        # instructions.extend(self.visit(node.obj))
        # instruc

    @visitor.when(cil.PlusNode)
    def visit(self, node: cil.PlusNode):
        """
        assuming left and right operands are ints
        """
        instructions = [f"<sum:{node.dest}<-{node.left}+{node.right}>"]
        t0, t1, t2 = registers.T[0], registers.T[1], registers.T[2]

        instructions.extend(
            [
                mips.LINode(t0, node.left),
                mips.LINode(t1, node.right),
                mips.ADDNode(t2, t0, t1),
            ]
        )

        instructions.append(f"</sum:{node.dest}<-{node.left}+{node.right}>")

        return instructions

    @visitor.when(cil.LoadNode)
    def visit(self, node: cil.LoadNode):
        instructions = [f"# <loadnode:{node.dest}-{node.msg}>"]

        t0 = registers.T[0]
        data = self.data[node.msg]

        instructions.append(mips.LANode(t0, data.label))
        if isinstance(node.dest, cil.Node):
            instructions.extend(self.visit(node.dest))

        address = self.cur_function.variable_address(node.dest)
        instructions.append(mips.SWNode(t0, address, registers.FP))

        instructions.append(f"# </loadnode:{node.dest}-{node.msg}>")

        return instructions
