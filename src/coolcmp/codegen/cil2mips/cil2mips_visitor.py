from __future__ import annotations
from typing import Dict

from coolcmp.utils import cil, visitor
from coolcmp.utils import mips, registers


class LabelUUID:
    """
    Class for generating unique labels
    """

    def __init__(self, name: str):
        self.name = name
        self.counter = 0

    def next(self):
        label = f"{self.name}_{self.counter}"
        self.counter += 1
        return label


class CILToMipsVisitor:
    def __init__(self):
        self.data: Dict[str, mips.Node] = {}
        self.types: Dict[str, mips.Type] = {}
        self.functions: Dict[str, mips.FunctionNode] = {}
        self.cur_function: mips.FunctionNode = None

        self.function_names: Dict[str, str] = {}

        self.data_label_gen = LabelUUID("data")
        self.types_label_gen = LabelUUID("type")
        self.code_label_gen = LabelUUID("code")

        self.labels = {}

    @visitor.on("node")
    def visit(self, node):
        pass

    @visitor.on("node")
    def collect_function_names(self, node):
        pass

    @visitor.when(cil.ProgramNode)
    def collect_function_names(self, node: cil.ProgramNode):
        for f in node.dot_code:
            self.collect_function_names(f)

    @visitor.when(cil.FunctionNode)
    def collect_function_names(self, node: cil.FunctionNode):
        self.function_names[node.name] = "main" if node.name == "entry" else node.name

    @visitor.when(cil.ProgramNode)
    def visit(self, node: cil.ProgramNode):
        print("ProgramNode")
        self.collect_function_names(node)

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
        new_label = self.data_label_gen.next()
        self.data[node.name] = mips.StringNode(new_label, f'"{node.name}"')

        type_label = self.types_label_gen.next()
        methods = [
            self.function_names[i]
            for i in node.methods.values()
            if self.function_names.get(i)
        ]

        type_ = mips.Type(
            type_label,
            new_label,
            list(node.attributes),
            methods,
            len(self.types),
            [],
        )

        self.types[node.name] = type_

    @visitor.when(cil.DataNode)
    def visit(self, node: cil.DataNode):
        print(f"DataNode {node.name} {node.value}")
        data_label = self.data_label_gen.next()
        self.data[node.name] = mips.StringNode(data_label, node.value)

    @visitor.when(cil.FunctionNode)
    def visit(self, node: cil.FunctionNode):
        print(f"FunctionNode {node.name}")
        function_label = self.function_names[node.name]
        params = [x.name for x in node.params]
        local_vars = [x.name for x in node.local_vars]

        local_vars_size = len(local_vars) * registers.DW

        function_node = mips.FunctionNode(function_label, params, local_vars)
        self.functions[node.name] = function_node
        self.cur_function = function_node
        self.labels = {}

        instructions = [f"# <function:{self.function_names[node.name]}>"]

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

        instructions.extend([f"# </function:{self.function_names[node.name]}>"])
        return instructions

    @visitor.when(cil.AllocateNode)
    def visit(self, node: cil.AllocateNode):
        print(f"AllocateNode {node.type} {node.dest}")

        # TODO: Finish this
        type_ = node.type if isinstance(node.type, int) else self.types[node.type].index

        reg_t0 = registers.T[0]
        reg_t1 = registers.T[1]
        v0 = registers.V0

        li = mips.LINode(reg_t0, type_)
        # sw = mips.SWNode(
        #     v0,
        # )

        instructions = ["# <allocate>", "# </allocate>"]

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

        return [f"# <printint:{node.addr}>", f"# <printint:{node.addr}"]

    @visitor.when(cil.PrintStringNode)
    def visit(self, node: cil.PrintStringNode):
        """
        li $v0, 4
        la $a0, str
        syscall
        """
        li = mips.LINode(registers.V0, 4)
        la = mips.LANode(registers.A0, node.addr)
        syscall = mips.SysCallNode()

        return [
            f"# <printstring:{node.addr}>",
            li,
            la,
            syscall,
            f"# </printstring:{node.addr}>",
        ]

    @visitor.when(cil.DynamicCallNode)
    def visit(self, node: cil.DynamicCallNode):
        print(f"DynamicCallNode {node.method} {node.type} {node.dest}")
        instructions = []

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
