from __future__ import annotations
from audioop import add
from typing import Dict

from coolcmp.utils import cil, visitor
from coolcmp.utils import mips, registers
from coolcmp.utils import extract_class_name
from coolcmp.utils.registers import (
    t0,
    t1,
    t2,

    s0,
    s1,
    s2,

    a0,
    a1,
    a2,
    dw,

    v0,
    fp,
    sp,
    ra,
    zero
)


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
                return (i + 2) * 4
        raise ValueError(f"Unexpected method: {name}")

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
        for func in node.dot_code:
            if func.name == 'main':
                self.visit(func)
        for func in node.dot_code:
            if func.name != 'main':
                self.visit(func)

        return mips.ProgramNode(
            list(self.data.values()),
            list(self.types.values()),
            list(self.functions.values()),
        )

    @visitor.when(cil.TypeNode)
    def visit(self, node: cil.TypeNode):
        type_ = mips.Type(
            label=node.name,
            parent=node.parent,
            attrs=list(node.attributes),
            methods=node.methods,
            total_methods=node.total_methods,
            index=len(self.types),
        )

        self.types[node.name] = type_

    @visitor.when(cil.InitNode)
    def visit(self, node: cil.InitNode):
        dest = self.get_address(node.dest)
        self.add_inst(
            mips.LWNode(a0, node.type_name),
            mips.JALNode('malloc'),
            mips.LANode(t0, node.type_name)     .with_comm(f"Get pointer to type {node.type_name}"),
            mips.SWNode(t0, 0, v0)              .with_comm(f"Set type pointer as attr"),
            mips.SWNode(v0, dest, fp),
        )

    @visitor.when(cil.DataNode)
    def visit(self, node: cil.DataNode):
        self.data[node.name] = mips.StringNode(node.name, f"{node.value}")

    @visitor.when(cil.FunctionNode)
    def visit(self, node: cil.FunctionNode):
        params = [x.name for x in node.params]
        local_vars = [x.name for x in node.local_vars]

        local_vars_size = len(local_vars) * dw

        self.cur_function = mips.FunctionNode(node.name, params, local_vars)
        self.functions[node.name] = self.cur_function

        # Push local vars
        push_instructions = (
            mips.push_register_instructions(ra)
            + mips.push_register_instructions(fp)
            + [mips.ADDINode(fp, sp, 8)]
            + [mips.ADDINode(sp, sp, -local_vars_size)]
        )

        self.add_inst(
            mips.CommentNode(f"<function:{node.name}>"),
            *push_instructions,
        )

        for instruction in node.instructions:
            self.visit(instruction)

        # Pop local vars
        pop_instructions = (
            [mips.ADDINode(sp, sp, local_vars_size)]
            + mips.pop_register_instructions(fp)
            + mips.pop_register_instructions(ra)
        )

        return_instructions = (
            [mips.LINode(v0, 10), mips.SysCallNode()]
            if self.cur_function.name == "main"
            else [mips.JRNode(ra)]
        )

        self.add_inst(
            *pop_instructions,
            *return_instructions,
            mips.CommentNode(f"</function:{node.name}>"),
        )

    @visitor.when(cil.SetAttrNode)
    def visit(self, node: cil.SetAttrNode):
        if node.value == 'void':
            load_value_inst = mips.LWNode(t0, 'void')
        elif isinstance(node.value, int):
            load_value_inst = mips.LINode(t0, node.value)
        else:
            value_address = self.get_address(node.value)
            load_value_inst = mips.LWNode(t0, (value_address, fp))

        instance = self.get_address(node.instance)

        self.add_inst(
            mips.CommentNode(f"<setattribute:{node.attr.name}-{node.instance}>"),
            # sum 1 to attr index because at offset 0 is the type pointer
            load_value_inst,
            mips.LWNode(t1, (instance, fp)),
            mips.SWNode(t0, 4 * (node.attr.index + 1), t1)      .with_comm(f"Set attr '{node.attr}' of {node.instance} = {node.value}"),
            mips.CommentNode(f"</setattribute:{node.attr.name}-{node.instance}>"),
        )

    @visitor.when(cil.GetAttrNode)
    def visit(self, node: cil.GetAttrNode):
        dest_offset = self.get_address(node.dest)
        src_offset = self.get_address(node.src)
        class_ = extract_class_name(node.attr)
        attr_offset = self.types[class_].get_attr_index(node.attr) * 4

        self.add_inst(
            mips.CommentNode(f"<getattribute:{node.attr}-{node.src}>"),
            mips.LWNode(t0, (src_offset, fp))       .with_comm(f"Get instance: {node.src}"),
            mips.LWNode(t0, (attr_offset, t0))      .with_comm(f"Get attribute: {node.attr}"),
            mips.SWNode(t0, dest_offset, fp)        .with_comm(f"Store attribute in local {node.dest}"),
            mips.CommentNode(f"</getattribute:{node.attr}-{node.src}>"),
        )

    @visitor.when(cil.PrintIntNode)
    def visit(self, node: cil.PrintIntNode):
        address = self.get_address(node.addr)
        self_address = self.get_address('self')

        self.add_inst(
            mips.CommentNode(f"<printint:{node.addr}>"),
            mips.LWNode(t0, (address, fp)),
            mips.ADDUNode(a0, t0, 4),
            mips.LINode(v0, 1),
            mips.LWNode(a0, (0, a0)),
            mips.SysCallNode(),
            mips.LWNode(v0, (self_address, fp)),
            mips.CommentNode(f"</printint:{node.addr}>"),
        )

    @visitor.when(cil.PrintStringNode)
    def visit(self, node: cil.PrintStringNode):
        address = self.get_address(node.addr)
        self_address = self.get_address('self')

        self.add_inst(
            mips.CommentNode(f"<printstring:{node.addr}>"),
            mips.LWNode(t0, (address, fp)),
            mips.ADDUNode(a0, t0, 4),
            mips.LINode(v0, 4),
            mips.LWNode(a0, (0, a0)),
            mips.SysCallNode(),
            mips.LWNode(v0, (self_address, fp)),
            mips.CommentNode(f"</printstring:{node.addr}>"),
        )

    @visitor.when(cil.ReadIntNode)
    def visit(self, node: cil.ReadIntNode):
        address = self.get_address(node.dest)

        self.add_inst(
            mips.CommentNode(f"<readint:{node.dest}>"),
            mips.LINode(v0, 5),
            mips.SysCallNode(),
            mips.MoveNode(t2, v0)
        )

        self.visit(cil.StaticCallNode("Int__init", node.dest))

        self.add_inst(
            mips.LWNode(t1, (address, fp)),
            mips.SWNode(t2, 4, t1),
            mips.LWNode(v0, (address, fp)),
            mips.CommentNode(f"</readint:{node.dest}>")
        )

    @visitor.when(cil.DynamicCallNode)
    def visit(self, node: cil.DynamicCallNode):
        obj_address = self.get_address(node.obj)
        meth_offset = self.get_method_index(node.method)
        dest_address = self.get_address(node.dest)
        args_space = self.cil_root.get_function(f"{node.dtype}_{node.method}").args_space

        self.add_inst(
            mips.CommentNode(f"<dynamiccall:{node.obj}-{node.method}-{node.dest}>"),
            mips.LWNode(t0, (obj_address, fp))      .with_comm("Get instance pointer"),
            mips.LWNode(t0, (0, t0))                .with_comm("Get type pointer at offset 0"),
            mips.LWNode(t0, (meth_offset, t0))      .with_comm(f"Get method: {node.method}"),
            mips.JALRNode(t0)                       .with_comm(f"Jump to {node.method}"),
            mips.SWNode(v0, dest_address, fp),
            mips.ADDINode(sp, sp, args_space)       .with_comm("Pop args pushed"),
            mips.CommentNode(f"</dynamiccall:{node.obj}-{node.method}-{node.dest}>"),
        )

    @visitor.when(cil.StaticCallNode)
    def visit(self, node: cil.StaticCallNode):
        dest = self.get_address(node.dest)

        self.add_inst(
            mips.CommentNode(f"<staticcall:{node.function}-{node.dest}>"),
            mips.JALNode(node.function),
            mips.SWNode(v0, dest, fp),
            mips.CommentNode(f"</staticcall:{node.function}-{node.dest}>"),
        )

    @visitor.when(cil.ArgNode)
    def visit(self, node: cil.ArgNode):
        print(self.cur_function.name, [p for p in self.cur_function.params], [l for l in self.cur_function.local_vars])
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
        left_offset = self.get_address(node.left)
        right_offset = self.get_address(node.right)
        dest_offset = self.get_address(node.dest)

        self.add_inst(
            mips.CommentNode(f"<plus:{node.dest}<-{node.left}+{node.right}>"),
            mips.LWNode(t0, (left_offset, fp))      .with_comm(f"Load Int {node.left}"),
            mips.LWNode(t0, (4, t0))                .with_comm('Load Int_value at offset 4'),
            mips.LWNode(t1, (right_offset, fp))     .with_comm(f"Load Int {node.right}"),
            mips.LWNode(t1, (4, t1))                .with_comm('Load Int_value at offset 4'),
            mips.ADDNode(t2, t0, t1)                .with_comm('Add the integer values'),
        )

        self.visit(cil.StaticCallNode('Int__init', node.dest))

        self.add_inst(
            mips.LWNode(t1, (dest_offset, fp)),
            mips.SWNode(t2, 4, t1),
            mips.CommentNode(f"</plus:{node.dest}<-{node.left}+{node.right}>"),
        )

    @visitor.when(cil.MinusNode)
    def visit(self, node: cil.MinusNode):
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

        self.visit(cil.StaticCallNode('Int__init', node.dest))

        self.add_inst(
            mips.LWNode(t1, (dest_offset, fp)),
            mips.SWNode(t2, 4, t1),
            mips.CommentNode(f"</minus:{node.dest}<-{node.left}-{node.right}>"),
        )

    @visitor.when(cil.StarNode)
    def visit(self, node: cil.StarNode):
        left_offset = self.get_address(node.left)
        right_offset = self.get_address(node.right)
        dest_offset = self.get_address(node.dest)

        self.add_inst(
            mips.CommentNode(f"<star:{node.dest}<-{node.left}-{node.right}>"),
            mips.LWNode(t0, (left_offset, fp)),  # load Int_value at offset 4
            mips.LWNode(t0, (4, t0)),
            mips.LWNode(t1, (right_offset, fp)),  # load Int_value at offset 4
            mips.LWNode(t1, (4, t1)),
            mips.MULTNode(t2, t0, t1),  # multiply the integer values
        )

        self.visit(cil.StaticCallNode('Int__init', node.dest))

        self.add_inst(
            mips.LWNode(t1, (dest_offset, fp)),
            mips.SWNode(t2, 4, t1),
            mips.CommentNode(f"</star:{node.dest}<-{node.left}-{node.right}>"),
        )
    
    @visitor.when(cil.DivNode)
    def visit(self, node: cil.DivNode):
        left_offset = self.get_address(node.left)
        right_offset = self.get_address(node.right)
        dest_offset = self.get_address(node.dest)

        self.add_inst(
            mips.CommentNode(f"<divide:{node.dest}<-{node.left}-{node.right}>"),
            mips.LWNode(t0, (left_offset, fp)),  # load Int_value at offset 4
            mips.LWNode(t0, (4, t0)),
            mips.LWNode(t1, (right_offset, fp)),  # load Int_value at offset 4
            mips.LWNode(t1, (4, t1)),
            mips.DIVNode(t2, t0, t1),  # divide the integer values
        )

        self.visit(cil.StaticCallNode('Int__init', node.dest))

        self.add_inst(
            mips.LWNode(t1, (dest_offset, fp)),
            mips.SWNode(t2, 4, t1),
            mips.CommentNode(f"</divide:{node.dest}<-{node.left}-{node.right}>"),
        )

    @visitor.when(cil.NegationNode)
    def visit(self, node: cil.NegationNode):
        src_offset = self.get_address(node.src)
        dest_offset = self.get_address(node.dest)

        self.add_inst(
            mips.CommentNode(f"<negate:{node.dest}<-~{node.src}>"),
            mips.LWNode(t0, (src_offset, fp)),
            mips.LWNode(t0, (4, t0)),
            mips.XORINode(t1, t0, 1)
        )

        self.visit(cil.StaticCallNode('Bool__init', node.dest))

        self.add_inst(
            mips.LWNode(t0, (dest_offset, fp)),
            mips.SWNode(t1, 4, t0),
            mips.CommentNode(f"</negate:{node.dest}<-~{node.src}>"),
        )


    @visitor.when(cil.LoadNode)
    def visit(self, node: cil.LoadNode):
        dest_address = self.cur_function.variable_address(node.dest)

        self.add_inst(
            mips.CommentNode(f"<loadnode:{node.dest}-{node.msg}>"),
            mips.LANode(t0, self.data[node.msg].label),
            mips.SWNode(t0, dest_address, fp),
            mips.CommentNode(f"</loadnode:{node.dest}-{node.msg}>"),
        )
 
    @visitor.when(cil.AssignNode)
    def visit(self, node: cil.AssignNode):
        dest = self.get_address(node.dest)

        if isinstance(node.source, int):
            load_inst = mips.LINode(t0, node.source)
        elif node.source == "void":
            load_inst = mips.LANode(t0, "void")
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
        self.add_inst(mips.CommentNode(f"<substr:>{node.dest}[{node.index}:{node.length}]"))

        self.visit(cil.StaticCallNode('String__init', node.dest))

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

    @visitor.when(cil.LengthNode)
    def visit(self, node: cil.LengthNode):
        self.add_inst(mips.CommentNode(f"<length:{node.dest}=len({node.src})>"))

        self.visit(cil.StaticCallNode("Int__init", node.dest))

        src_address = self.get_address(node.src)
        dest_address = self.get_address(node.dest)

        self.add_inst(
            mips.LWNode(a0, (src_address, fp)),
            mips.LWNode(a0, (4, a0)),
            mips.JALNode('length'),

            mips.LWNode(t1, (dest_address, fp)),
            mips.SWNode(v0, 4, t1),
        )

        self.add_inst(mips.CommentNode(f"</length:{node.dest}=len({node.src})>"))

    @visitor.when(cil.ConcatNode)
    def visit(self, node: cil.ConcatNode):
        self.add_inst(mips.CommentNode(f"<concat:{node.dest}={node.str1}+{node.str2}>"))

        self.visit(cil.StaticCallNode("String__init", node.dest))

        str1_address = self.get_address(node.str1)
        str2_address = self.get_address(node.str2)
        dest_address = self.get_address(node.dest)

        # Calc length of str1 and save it in t0
        length_of_str1 = (
            mips.LWNode(a0, (str1_address, fp)),
            mips.LWNode(a0, (4, a0)),
            mips.JALNode('length'),
            mips.MoveNode(t0, v0)
        )
        # Calc length of str2 and save it in t1
        length_of_str2 = (
            mips.LWNode(a0, (str2_address, fp)),
            mips.LWNode(a0, (4, a0)),
            mips.JALNode('length'),
            mips.MoveNode(t1, v0)
        )

        push_str1 = (
            mips.LWNode(a0, (str1_address, fp)),
            mips.LWNode(a0, (4, a0))
        )
        push_str2 = (
            mips.LWNode(a1, (str2_address, fp)),
            mips.LWNode(a1, (4, a1))
        )
        push_length = (
            mips.ADDNode(a2, t0, t1),
        )

        self.add_inst(
            *length_of_str1,
            *length_of_str2,
            *push_str1,
            *push_str2,
            *push_length,
            mips.JALNode('concat'),
        )

        self.add_inst(
            mips.LWNode(t1, (dest_address, fp)),
            mips.SWNode(v0, 4, t1)
        )

        self.add_inst(mips.CommentNode(f"</concat:{node.dest}={node.str1}+{node.str2}>"))

    @visitor.when(cil.TypeNameNode)
    def visit(self, node: cil.TypeNameNode):
        name_offset = self.types['Object'].name_offset
        src_offset = self.get_address(node.src)

        self.add_inst(
            mips.CommentNode(f"<typename:{node.dest}-{node.src}>"),
        )

        self.visit(cil.StaticCallNode('String__init', node.dest))

        self.add_inst(
            mips.LWNode(t0, (src_offset, fp))       .with_comm('Load pointer to self'),
            mips.LWNode(t0, (0, t0))                .with_comm('Load pointer to type of self'),
            mips.ADDINode(t0, t0, name_offset)      .with_comm('Point to name of type'),
            mips.SWNode(t0, 4, v0)                  .with_comm('Save name of the type in the new string'),
            mips.CommentNode(f"</typename:{node.dest}-{node.src}>"),
        )

    @visitor.when(cil.IsVoidNode)
    def visit(self, node: cil.IsVoidNode):
        src = self.get_address(node.src)
        dest = self.get_address(node.dest)

        self.add_inst(
            mips.CommentNode(f"<isvoid:{node.dest}-{node.src}>"),
        )

        self.visit(cil.StaticCallNode('Bool__init', node.dest))

        self.add_inst(
            mips.LWNode(a0, (src, fp))      .with_comm('Push instance pointer'),
            mips.JALNode('isvoid'),
            mips.LWNode(t0, (dest, fp))     .with_comm('Load Bool pointer'),
            mips.SWNode(v0, 4, t0)          .with_comm('Save isvoid result as value of Bool'),
            mips.CommentNode(f"</isvoid:{node.dest}-{node.src}>"),
        )

    @visitor.when(cil.LabelNode)
    def visit(self, node: cil.LabelNode):
        self.add_inst(
            mips.LabelNode(node.name),
        )

    @visitor.when(cil.GotoNode)
    def visit(self, node: cil.GotoNode):
        self.add_inst(
            mips.JNode(node.label),
        )

    @visitor.when(cil.GotoIfNode)
    def visit(self, node: cil.GotoIfNode):
        condition = self.get_address(node.condition)

        self.add_inst(
            mips.CommentNode(f"<gotoif:{node.condition}-{node.label}>"),
            mips.LWNode(t0, (condition, fp)),
            mips.LWNode(t0, (4, t0)),
            mips.LINode(t1, 1),
            mips.BEQNode(t0, t1, node.label),
            mips.CommentNode(f"</gotoif:{node.condition}-{node.label}>"),
        )

    @visitor.when(cil.LessThanNode)
    def visit(self, node: cil.LessThanNode):
        left = self.get_address(node.left)
        right = self.get_address(node.right)
        dest = self.get_address(node.dest)

        self.add_inst(
            mips.CommentNode(f"<less than: {node.dest} <- {node.left} < {node.right}>"),
        )

        self.visit(cil.StaticCallNode("Bool__init", node.dest))

        self.add_inst(
            mips.LWNode(a0, (left, fp)),
            mips.LWNode(a1, (right, fp)),
            mips.JALNode("less_than"),
            mips.LWNode(t0, (dest, fp)),
            mips.SWNode(v0, 4, t0),
            mips.CommentNode(f"</less than: {node.dest} <- {node.left} < {node.right}>"),
        )

    @visitor.when(cil.LessEqualNode)
    def visit(self, node: cil.LessEqualNode):
        left = self.get_address(node.left)
        right = self.get_address(node.right)
        dest = self.get_address(node.dest)

        self.add_inst(
            mips.CommentNode(f"<less equal: {node.dest} <- {node.left} <= {node.right}>"),
        )

        self.visit(cil.StaticCallNode("Bool__init", node.dest))

        self.add_inst(
            mips.LWNode(a0, (left, fp)),
            mips.LWNode(a1, (right, fp)),
            mips.JALNode("less_equal"),
            mips.LWNode(t0, (dest, fp)),
            mips.SWNode(v0, 4, t0),
            mips.CommentNode(f"</less equal: {node.dest} <- {node.left} <= {node.right}>"),
        )

    @visitor.when(cil.EqualNode)
    def visit(self, node: cil.EqualNode):
        left = self.get_address(node.left)
        right = self.get_address(node.right)
        dest = self.get_address(node.dest)

        self.add_inst(
            mips.CommentNode(f"<equal: {node.dest} <- {node.left} = {node.right}>"),
        )

        self.visit(cil.StaticCallNode("Bool__init", node.dest))

        self.add_inst(
            mips.LWNode(a0, (left, fp)),
            mips.LWNode(a1, (right, fp)),
            mips.JALNode("equal"),
            mips.LWNode(t0, (dest, fp)),
            mips.SWNode(v0, 4, t0),
            mips.CommentNode(f"<equal: {node.dest} <- {node.left} = {node.right}>"),
        )

    @visitor.when(cil.AbortNode)
    def visit(self, node: cil.AbortNode):
        type_name_address = self.get_address('typename')

        self.add_inst(
            mips.CommentNode("<abort>"),
            # "Abort called from class "
            mips.LINode(v0, 4),
            mips.LANode(a0, "s2"),
            mips.SysCallNode(),
        )

        self.visit(cil.TypeNameNode('typename', 'self'))

        self.add_inst(
            # Typename
            mips.LWNode(a0, (type_name_address, fp)),
            mips.LWNode(a0, (4, a0)),
            mips.LINode(v0, 4),
            mips.SysCallNode(),

            # \n
            mips.LINode(v0, 4),
            mips.LANode(a0, 's3'),
            mips.SysCallNode(),

            # Abort
            mips.LINode(v0, 10) .with_comm("Finish program execution"),
            mips.SysCallNode(),
            mips.CommentNode("</abort>")
        )

    @visitor.when(cil.ReadStringNode)
    def visit(self, node: cil.ReadStringNode):
        self.add_inst(mips.CommentNode(f"<readstring:{node.dest}>"))
        
        address = self.get_address(node.dest)

        self.add_inst(
            mips.LINode(a0, 512), # TODO: Dynamic string length
            mips.JALNode('malloc'),
            mips.MoveNode(t2, v0)
        )
        self.add_inst(
            mips.MoveNode(a0, t2),
            mips.LINode(a1, 512),
            mips.LINode(v0, 8),
            mips.SysCallNode(),
        )
        self.visit(cil.StaticCallNode('String__init', node.dest))
        self.add_inst(
            mips.LWNode(t0, (address, fp)),
            mips.SWNode(t2, 4, t0)
        )

        # Remove eol
        self.add_inst(
            mips.MoveNode(a0, t2),
            mips.JALNode('remove_eol')
        )

        self.add_inst(mips.CommentNode(f"</readstring:{node.dest}>"))

    @visitor.when(cil.ComplementNode)
    def visit(self, node: cil.ComplementNode):
        src = self.get_address(node.src)
        dest = self.get_address(node.dest)

        self.add_inst(
            mips.CommentNode(f"</complement:{node.dest}>"),
        )

        self.visit(cil.StaticCallNode('Int__init', node.dest))

        self.add_inst(
            mips.LWNode(t0, (src, fp)),
            mips.LWNode(t0, (4, t0)),
            mips.NOTNode(t0, t0),
            mips.LWNode(t1, (dest, fp)),
            mips.SWNode(t0, 4, t1),
            mips.CommentNode(f"</complement:{node.dest}>"),
        )

    @visitor.when(cil.CaseMatchRuntimeErrorNode)
    def visit(self, node: cil.CaseMatchRuntimeErrorNode):
        self.add_inst(
            mips.CommentNode(f"<case-match-runtime-error>"),
            mips.LINode(v0, 4),
            mips.LANode(a0, 's4'),
            mips.SysCallNode(),
            mips.LINode(v0, 10),
            mips.SysCallNode(),
            mips.CommentNode(f"</case-match-runtime-error>"),
        )

    @visitor.when(cil.ExprVoidRuntimeErrorNode)
    def visit(self, node: cil.ExprVoidRuntimeErrorNode):
        self.add_inst(
            mips.CommentNode(f"<expr-void-runtime-error>"),
            mips.LINode(v0, 4),
            mips.LANode(a0, 's5'),
            mips.SysCallNode(),
            mips.LINode(v0, 10),
            mips.SysCallNode(),
            mips.CommentNode(f"</expr-void-runtime-error>")
        )

    @visitor.when(cil.ConformsNode)
    def visit(self, node: cil.ConformsNode):
        left_offset = self.get_address(node.left)
        right_offset = self.get_address(node.right)
        dest_offset = self.get_address(node.dest)

        self.add_inst(
            mips.CommentNode(f"<conforms:{node.dest}<-{node.left}-{node.right}>"),
        )

        # Get the left type
        self.add_inst(
            mips.LWNode(t0, (left_offset, fp))      .with_comm("Load left pointer to self"),
            mips.LWNode(a0, (0, t0))                .with_comm("Load left pointer to type of self"),

            mips.LWNode(t0, (right_offset, fp))      .with_comm("Load left pointer to self"),
            mips.LWNode(a1, (0, t0))                .with_comm("Load left pointer to type of self"),
            mips.JALNode('conforms'),
            mips.MoveNode(s0, v0)
        )

        self.visit(cil.StaticCallNode('Bool__init', node.dest))

        self.add_inst(
            mips.LWNode(t0, (dest_offset, fp)),
            mips.SWNode(s0, 4, t0),
            mips.CommentNode(f"</conforms:{node.dest}<-{node.left}-{node.right}>"),
        )
