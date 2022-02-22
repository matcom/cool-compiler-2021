from __future__ import annotations

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
        self.data = {}
        self.types = {}
        self.functions = {}
        self.cur_function = None

        self.function_names = {}

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
        print("function_name: ProgramNode")
        for f in node.dot_code:
            self.collect_function_names(f)

    @visitor.when(cil.FunctionNode)
    def collect_function_names(self, node: cil.FunctionNode):
        print("function_name: FunctionNode")
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

        defaults = (
            []
            if node.name == "String"
            else [("value", "default_str"), ("len", "type_4_proto")]
        )
        print(methods, defaults)

        type_ = mips.Type(
            type_label,
            new_label,
            list(node.attributes),
            methods,
            len(self.types),
            defaults,
        )

        self.types[node.name] = type_

    @visitor.when(cil.DataNode)
    def visit(self, node: cil.DataNode):
        print(f"DataNode {node.name} {node.value}")
        data_label = self.data_label_gen.next()
        self.data[node.name] = mips.StringNode(data_label, node.value)

    @visitor.when(cil.FunctionNode)
    def visit(self, node: cil.FunctionNode):
        print(
            f"FunctionNode {node.name} {node.params} {node.local_vars} {node.instructions}"
        )
        function_label = self.function_names[node.name]
        params = [x.name for x in node.params]
        local_vars = [x.name for x in node.local_vars]

        local_vars_size = len(local_vars) * registers.DW

        function_node = mips.FunctionNode(function_label, params, local_vars)
        self.functions[node.name] = function_node
        self.cur_function = function_node
        self.labels = {}

        instructions = [f"# code for function {self.function_names[node.name]}..."]

        for instruction in node.instructions:
            instructions.extend(self.visit(instruction))

        function_node.instructions = instructions
        self.cur_function = None
        return instructions

    @visitor.when(cil.AllocateNode)
    def visit(self, node: cil.AllocateNode):
        print(f"AllocateNode {node.type} {node.dest}")

        # TODO: Finish this
        print(self.types)
        # type_ = node.type if isinstance(node.type, int) else self.types[node.type].index

        reg_t0 = registers.T[0]
        reg_t1 = registers.T[1]
        v0 = registers.V0

        # li = mips.LINode(reg_t0, type_)
        # sw = mips.SWNode(
        #     v0,
        # )

        instructions = ["# allocate instructions..."]

        return instructions

    @visitor.when(cil.ReturnNode)
    def visit(self, node: cil.ReturnNode):
        value = 0 if node.value is None else node.value

        return [mips.LINode(registers.V0, value)]

    @visitor.when(cil.PrintIntNode)
    def visit(self, node: cil.PrintIntNode):
        print(f"PrintIntNode {node.addr}")

        return ["# print int instructions"]

    @visitor.when(cil.PrintStringNode)
    def visit(self, node: cil.PrintStringNode):
        print(f"PrintStringNode {node.addr}")
        return ["# print string instructions"]

    @visitor.when(cil.DynamicCallNode)
    def visit(self, node: cil.DynamicCallNode):
        print(f"DynamicCallNode {node.method} {node.type} {node.dest}")
        return ["# dynamic call instructions"]
