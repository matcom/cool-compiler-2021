from __future__ import annotations
from typing import Dict

from coolcmp.utils import cil, visitor
from coolcmp.utils import mips, registers


class CILToMipsVisitor:
    def __init__(self):
        self.cil_root: cil.ProgramNode | None = None
        self.data: Dict[str, mips.Node] = {}
        self.types: Dict[str, mips.Type] = {}
        self.functions: Dict[str, mips.FunctionNode] = {}
        self.cur_function: mips.FunctionNode | None = None

    def add_inst(self, *inst: mips.InstructionNode) -> None:
        self.cur_function.instructions.extend(inst)

    def get_address(self, var_name: str):
        return self.cur_function.variable_address(var_name)

    def get_method_index(self, name: str):
        for i, method in enumerate(self.cil_root.all_methods):
            if method == name:
                return (i + 1) * 4
        raise ValueError(f"Unexpected method: {name}")

    def build_init(self, node: cil.TypeNode) -> list[mips.InstructionNode]:
        t0 = registers.T[0]
        a0, v0, sp, fp, ra = registers.A0, registers.V0, registers.SP, registers.FP, registers.RA

        return [
            mips.SUBUNode(sp, sp, 24),
            mips.SWNode(ra, 8, sp),
            mips.SWNode(fp, 4, sp),
            mips.ADDUNode(fp, sp, 20),

            mips.LWNode(a0, node.name),
            mips.JALNode('malloc'),
            mips.LANode(t0, node.name),
            mips.SWNode(t0, 0, v0),

            mips.LWNode(ra, (8, sp)),
            mips.LWNode(fp, (4, sp)),
            mips.ADDUNode(sp, sp, 24),
            mips.JRNode(ra),
        ]

    @visitor.on("node")
    def visit(self, node):
        pass

    @visitor.when(cil.ProgramNode)
    def visit(self, node: cil.ProgramNode):
        print("ProgramNode")

        node.update_method_indexes()
        self.cil_root = node

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

        type_ = mips.Type(
            label=node.name,
            attrs=list(node.attributes),
            methods=node.methods,
            total_methods=node.total_methods,
            index=len(self.types),
            init=self.build_init(node)
        )

        self.types[node.name] = type_

    @visitor.when(cil.DataNode)
    def visit(self, node: cil.DataNode):
        print(f"DataNode {node.name} {node.value}")
        self.data[node.name] = mips.StringNode(node.name, f"{node.value}")

    @visitor.when(cil.FunctionNode)
    def visit(self, node: cil.FunctionNode):
        print(f"FunctionNode {node.name}")

        sp = registers.SP

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

        stack_occupied = 0
        for instruction in node.instructions:
            self.visit(instruction)
            if isinstance(instruction, cil.ArgNode):
                stack_occupied += 4

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

        if stack_occupied:
            self.add_inst(
                mips.CommentNode('Pop args pushed'),
                mips.ADDINode(sp, sp, stack_occupied),
            )

        self.add_inst(
            *pop_instructions,
            *return_instructions,
            mips.CommentNode(f"</function:{node.name}>"),
        )

    @visitor.when(cil.AllocateNode)
    def visit(self, node: cil.AllocateNode):
        print(f"AllocateNode {node.type} {node.dest}")

        dest_address = self.get_address(node.dest)

        self.add_inst(
            mips.CommentNode(f"<allocate:{node.type}-{node.dest}>"),
            mips.JALNode(f"_{node.type}_init"),
            mips.SWNode(registers.V0, dest_address, registers.FP),
            mips.CommentNode(f"</allocate:{node.type}-{node.dest}>"),
        )

    @visitor.when(cil.SetAttrNode)
    def visit(self, node: cil.SetAttrNode):
        t0 = registers.T[0]
        v0, fp = registers.V0, registers.FP

        # inst_address = self.get_address(node.instance)
        if node.value == 'void':
            load_value_inst = mips.LWNode(t0, 'void')
        else:
            value_address = self.get_address(node.value)
            load_value_inst = mips.LWNode(t0, (value_address, fp))

        self.add_inst(
            mips.CommentNode(f"<setattribute:{node.attr.name}-{node.instance}>"),
            # sum 1 to attr index because at offset 0 is the type pointer
            load_value_inst,
            mips.SWNode(t0, 4 * (node.attr.index + 1), v0),
            mips.CommentNode(f"</setattribute:{node.attr.name}-{node.instance}>"),
        )

    @visitor.when(cil.PrintIntNode)
    def visit(self, node: cil.PrintIntNode):
        print(f"PrintIntNode {node.addr}")
        self.add_inst(
            mips.CommentNode(f"<printint:{node.addr}>"),
            mips.LINode(registers.V0, 1),
        )

        if isinstance(node.addr, int):
            self.add_inst(
                mips.LINode(registers.ARG[0], node.addr),
                mips.SysCallNode(),
                mips.CommentNode(f"</printint:{node.addr}>"),
            )
            return

        address = self.cur_function.variable_address(node.addr)

        self.add_inst(
            mips.LWNode(registers.ARG[0], (address, registers.FP)),
            mips.SysCallNode(),
            mips.CommentNode(f"</printint:{node.addr}>"),
        )

    @visitor.when(cil.PrintStringNode)
    def visit(self, node: cil.PrintStringNode):
        """ """
        t0 = registers.T[0]
        a0, v0, fp = registers.ARG[0], registers.V0, registers.FP
        address = self.get_address(node.addr)

        self.add_inst(
            mips.CommentNode(f"<printstring:{node.addr}>"),
            mips.LWNode(registers.T[0], (4, registers.FP)),
            mips.ADDUNode(registers.A0, registers.T[0], 4),
            mips.LINode(registers.V0, 4),
            mips.SysCallNode(),
            mips.CommentNode(f"</printstring:{node.addr}>"),
        )

    @visitor.when(cil.DynamicCallNode)
    def visit(self, node: cil.DynamicCallNode):
        print(f"DynamicCallNode {node.method} {node.obj} {node.dest}")

        t0 = registers.T[0]
        fp, v0 = registers.FP, registers.V0

        obj_address = self.get_address(node.obj)
        meth_offset = self.get_method_index(node.method)
        dest_address = self.get_address(node.dest)

        self.add_inst(
            mips.CommentNode(f"<dynamiccall:{node.obj}>"),
            mips.LWNode(t0, (obj_address, fp)),     # get instance pointer
            mips.LWNode(t0, (0, t0)),               # get instance type pointer at offset 0
            mips.LWNode(t0, (meth_offset, t0)),     # get method
            mips.JALNode(t0),
            mips.SWNode(v0, dest_address, fp),
            mips.CommentNode(f"</dynamiccall:{node.obj}>"),
        )

    @visitor.when(cil.ArgNode)
    def visit(self, node: cil.ArgNode):
        t0 = registers.T[0]
        sp, fp = registers.SP, registers.FP

        address = self.get_address(node.name)

        self.add_inst(
            mips.CommentNode(f"<arg:{node.name}>"),
            mips.LWNode(t0, (address, fp)),
            mips.ADDINode(sp, sp, -4),
            mips.SWNode(t0, 0, sp),
            mips.CommentNode(f"</arg:{node.name}>"),
        )

    # @visitor.when(cil.TypeOfNode)
    # def visit(self, node: cil.TypeOfNode):
    #     t0, t1 = registers.T[0], registers.T[1]
    #     fp = registers.FP
    #
    #     self.add_inst(
    #         mips.CommentNode(f"<typeof:{node.obj}>"),
    #         mips.CommentNode(f"</typeof:{node.obj}>"),
    #     )

    @visitor.when(cil.PlusNode)
    def visit(self, node: cil.PlusNode):
        """
        assuming left and right operands are ints
        """
        t0, t1, t2 = registers.T[0], registers.T[1], registers.T[2]
        dest_address = self.cur_function.variable_address(node.dest)

        self.visit(node.left)
        self.visit(node.right)

        def handle_set_register_value(reg: registers.Register, value: int | str):
            if isinstance(value, int):
                self.add_inst(mips.LINode(reg, value))
            else:
                address = self.cur_function.variable_address(value)
                self.add_inst(mips.LWNode(reg, (address, registers.FP)))

        self.add_inst(mips.CommentNode(f"<sum:{node.dest}<-{node.left}+{node.right}>"))
        handle_set_register_value(t0, node.left)
        handle_set_register_value(t1, node.right)
        self.add_inst(
            mips.ADDNode(t2, t0, t1),
            mips.SWNode(t2, dest_address, registers.FP),
            mips.CommentNode(f"</sum:{node.dest}<-{node.left}+{node.right}>"),
        )

    @visitor.when(cil.MinusNode)
    def visit(self, node: cil.MinusNode):
        t0, t1, t2 = registers.T[0], registers.T[1], registers.T[2]

        self.add_inst(
            mips.CommentNode(f"<minus:{node.dest}<-{node.left}+{node.right}>"),
            mips.LWNode(t0, (4, node.left)),  # load Int_value at offset 4
            mips.LWNode(t1, (4, node.right)),  # load Int_value at offset 4
            mips.SUBNode(t2, t0, t1),  # subtract the integer values
            # allocate here new Int with the value in t0 as Int_value
            mips.CommentNode(f"</minus:{node.dest}<-{node.left}+{node.right}>"),
        )

    @visitor.when(cil.LoadNode)
    def visit(self, node: cil.LoadNode):
        t0 = registers.T[0]
        dest_address = self.cur_function.variable_address(node.dest)

        self.add_inst(
            mips.CommentNode(f"<loadnode:{node.dest}-{node.msg}>"),
            mips.LANode(t0, self.data[node.msg].label),
            mips.SWNode(t0, dest_address, registers.FP),
            mips.CommentNode(f"</loadnode:{node.dest}-{node.msg}>"),
        )

    @visitor.when(cil.AssignNode)
    def visit(self, node: cil.AssignNode):
        t0 = registers.T[0]
        dest_address = self.cur_function.variable_address(node.dest)

        self.add_inst(mips.CommentNode(f"<assignode:{node.dest}-{node.source}>"))

        if isinstance(node.source, int):
            self.add_inst(
                mips.LINode(t0, node.source),
                mips.SWNode(t0, dest_address, registers.FP),
            )
        else:
            self.visit(node.source)
            source_address = self.cur_function.variable_address(node.source)
            self.add_inst(
                mips.LWNode(t0, (source_address, registers.FP)),
                mips.SWNode(t0, dest_address, registers.FP),
            )
        self.add_inst(
            mips.CommentNode(f"</assignode:{node.dest}-{node.source}>"),
        )

    @visitor.when(cil.ReturnNode)
    def visit(self, node: cil.ReturnNode):
        if isinstance(node.value, int):
            self.add_inst(mips.LINode(registers.V0, node.value))
        elif node.value is None:
            pass
            # self.visit(node.value)
            # address = self.cur_function.variable_address(node.value)
            # self.add_inst(mips.LWNode(registers.V0, (address, registers.FP)))
