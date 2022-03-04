from __future__ import annotations
from typing import Dict

import reg as reg

from coolcmp.utils import cil, visitor
from coolcmp.utils import mips, registers
from coolcmp.utils import extract_class_name

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
        self.data[node.name] = mips.StringNode(node.name, f"{node.value}")

    @visitor.when(cil.FunctionNode)
    def visit(self, node: cil.FunctionNode):
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
        elif isinstance(node.value, int):
            load_value_inst = mips.LINode(t0, node.value)
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

    @visitor.when(cil.GetAttrNode)
    def visit(self, node: cil.GetAttrNode):
        t0, fp = registers.T[0], registers.FP

        dest_offset = self.get_address(node.dest)
        src_offset = self.get_address(node.src)
        class_ = extract_class_name(node.attr)
        attr_offset = self.types[class_].get_attr_index(node.attr) * 4

        self.add_inst(
            mips.CommentNode(f"<getattribute:{node.attr}-{node.src}>"),
            mips.LWNode(t0, (src_offset, fp)),
            mips.LWNode(t0, (attr_offset, t0)),
            mips.SWNode(t0, dest_offset, fp),
            mips.CommentNode(f"</getattribute:{node.attr}-{node.src}>"),
        )

    @visitor.when(cil.PrintIntNode)
    def visit(self, node: cil.PrintIntNode):
        t0 = registers.T[0]
        a0, v0, fp = registers.ARG[0], registers.V0, registers.FP
        address = self.get_address(node.addr)

        self.add_inst(
            mips.CommentNode(f"<printint:{node.addr}>"),
            mips.LWNode(t0, (address, fp)),
            mips.ADDUNode(a0, t0, 4),
            mips.LINode(registers.V0, 1),
            mips.LWNode(a0, (0, a0)),
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
            mips.LWNode(registers.T[0], (address, registers.FP)),
            mips.ADDUNode(registers.A0, registers.T[0], 4),
            mips.LINode(registers.V0, 4),
            mips.LWNode(registers.A0, (0, registers.A0)),
            mips.SysCallNode(),
            mips.CommentNode(f"</printstring:{node.addr}>"),
        )

    @visitor.when(cil.DynamicCallNode)
    def visit(self, node: cil.DynamicCallNode):
        t0 = registers.T[0]
        fp, v0 = registers.FP, registers.V0

        obj_address = self.get_address(node.obj)
        meth_offset = self.get_method_index(node.method)
        dest_address = self.get_address(node.dest)

        self.add_inst(
            mips.CommentNode(f"<dynamiccall:{node.obj}-{node.method}-{node.dest}>"),
            mips.LWNode(t0, (obj_address, fp)),     # get instance pointer
            mips.LWNode(t0, (0, t0)),               # get instance type pointer at offset 0
            mips.LWNode(t0, (meth_offset, t0)),     # get method
            mips.JALRNode(t0)                       .with_comm(f'Jump to {node.method}'),
            mips.SWNode(v0, dest_address, fp),
            mips.CommentNode(f"</dynamiccall:{node.obj}-{node.method}-{node.dest}>"),
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

    @visitor.when(cil.PlusNode)
    def visit(self, node: cil.PlusNode):
        """
        assuming left and right operands are ints
        """
        t0, t1, t2 = registers.T[0], registers.T[1], registers.T[2]
        fp = registers.FP

        left_offset = self.get_address(node.left)
        right_offset = self.get_address(node.right)
        dest_offset = self.get_address(node.dest)

        self.add_inst(mips.CommentNode(f"<sum:{node.dest}<-{node.left}+{node.right}>"))

        self.add_inst(
            mips.CommentNode(f"<plus:{node.dest}<-{node.left}+{node.right}>"),
            mips.LWNode(t0, (left_offset, fp)) .with_comm(' load Int_value at offset 4'),
            mips.LWNode(t0, (4, t0)),
            mips.LWNode(t1, (right_offset, fp)) .with_comm('load Int_value at offset 4'),
            mips.LWNode(t1, (4, t1)),
            mips.ADDNode(t2, t0, t1) .with_comm('subtract the integer values'),
        )

        self.visit(cil.AllocateNode('Int', node.dest))

        self.add_inst(
            mips.LWNode(t1, (dest_offset, fp)),
            mips.SWNode(t2, 4, t1),
            mips.CommentNode(f"</plus:{node.dest}<-{node.left}+{node.right}>"),
        )

    @visitor.when(cil.MinusNode)
    def visit(self, node: cil.MinusNode):
        t0, t1, t2 = registers.T[0], registers.T[1], registers.T[2]
        fp = registers.FP
        left_offset = self.get_address(node.left)
        right_offset = self.get_address(node.right)
        dest_offset = self.get_address(node.dest)

        self.add_inst(
            mips.CommentNode(f"<minus:{node.dest}<-{node.left}-{node.right}>"),
            mips.LWNode(t0, (left_offset, fp)),  # load Int_value at offset 4
            mips.LWNode(t0, (4, t0)),
            mips.LWNode(t1, (right_offset, fp)),  # load Int_value at offset 4
            mips.LWNode(t1, (4, t1)),
            mips.SUBNode(t2, t0, t1),  # subtract the integer values
        )

        self.visit(cil.AllocateNode('Int', node.dest))

        self.add_inst(
            mips.LWNode(t1, (dest_offset, fp)),
            mips.SWNode(t2, 4, t1),
            mips.CommentNode(f"</minus:{node.dest}<-{node.left}-{node.right}>"),
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
        t0, fp = registers.T[0], registers.FP
        dest = self.get_address(node.dest)

        if isinstance(node.source, int):
            load_inst = mips.LINode(t0, node.source)
        else:
            src = self.get_address(node.source)
            load_inst = mips.LWNode(t0, (src, fp))

        self.add_inst(
            mips.CommentNode(f"<assignode:{node.dest}-{node.source}>"),
            load_inst,
            mips.SWNode(t0, dest, fp),
            mips.CommentNode(f"</assignode:{node.dest}-{node.source}>"),
        )

    @visitor.when(cil.ReturnNode)
    def visit(self, node: cil.ReturnNode):
        v0, fp = registers.V0, registers.FP

        if node.value is not None:
            if isinstance(node.value, int):
                load_to_v0 = mips.LINode(v0, node.value)
            else:
                dest_offset = self.get_address(node.value)
                load_to_v0 = mips.LWNode(v0, (dest_offset, fp))

            self.add_inst(
                mips.CommentNode(f"<return:{node.value}>"),
                load_to_v0,
                mips.CommentNode(f"</return:{node.value}>"),
            )

    @visitor.when(cil.SubstringNode)
    def visit(self, node: cil.SubstringNode):
        t1 = registers.T[1]
        fp = registers.FP
        a0, a1, a2 = registers.ARG[0], registers.ARG[1], registers.ARG[2]
        v0 = registers.V0

        self.add_inst(mips.CommentNode(f"<substr:>{node.dest}[{node.index}:{node.length}]"))

        self.visit(cil.AllocateNode('String', node.dest))

        src_address = self.get_address('self')
        dest_address = self.get_address(node.dest)
        index_address = self.get_address(node.index)
        length_address = self.get_address(node.length)

        push_src = (
            mips.LWNode(a0, (src_address, fp)),
            mips.LWNode(a0, (4, a0))
        )
        push_length = (
            mips.LWNode(a1, (length_address, fp)),
            mips.LWNode(a1, (4, a1))
        )
        push_index = (
            mips.LWNode(a2, (index_address, fp)),
            mips.LWNode(a2, (4, a2))
        )

        self.add_inst(
            *push_src,
            *push_length,
            *push_index,
            mips.JALNode('substr'),
        )

        self.add_inst(
            mips.LWNode(t1, (dest_address, fp)),
            mips.SWNode(v0, 4, t1),
            mips.CommentNode(f"</substr:>{node.dest}[{node.index}:{node.length}]")
        )

    @visitor.when(cil.TypeNameNode)
    def visit(self, node: cil.TypeNameNode):
        t0, fp, v0 = registers.T[0], registers.FP, registers.V0

        name_offset = self.types['Object'].name_offset
        src_offset = self.get_address(node.src)

        self.add_inst(
            mips.CommentNode(f"</typename:{node.dest}-{node.src}>"),
        )

        self.visit(cil.AllocateNode('String', node.dest))

        self.add_inst(
            mips.LWNode(t0, (src_offset, fp))       .with_comm('Load pointer to self'),
            mips.LWNode(t0, (0, t0))                .with_comm('Load pointer to type of self'),
            mips.ADDINode(t0, t0, name_offset)      .with_comm('Point to name of type'),
            mips.SWNode(t0, 4, v0)                  .with_comm('Save name of the type in the new string'),
            mips.CommentNode(f"</typename:{node.dest}-{node.src}>"),
        )

    @visitor.when(cil.IsVoidNode)
    def visit(self, node: cil.IsVoidNode):
        t0 = registers.T[0]
        a0 = registers.ARG[0]
        fp, v0 = registers.FP, registers.V0

        src = self.get_address(node.src)
        dest = self.get_address(node.dest)

        self.add_inst(
            mips.CommentNode(f"<isvoid:{node.dest}-{node.src}>"),
        )

        self.visit(cil.AllocateNode('Bool', node.dest))

        self.add_inst(
            mips.LWNode(a0, (src, fp))      .with_comm('Push instance pointer'),
            mips.JALNode('isvoid'),
            mips.LWNode(t0, (dest, fp))     .with_comm('Load Bool pointer'),
            mips.SWNode(v0, 4, t0)          .with_comm('Save isvoid result as value of Bool'),
            mips.CommentNode(f"</isvoid:{node.dest}-{node.src}>"),
        )
