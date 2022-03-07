import itertools as itt

import app.shared.visitor as visitor
import app.cil.ast_cil as cil
from app.mips import mips
from random import choice
from collections import defaultdict


class CILToMIPSVisitor:
    def __init__(self):
        self._types = {}
        self._data_section = {}
        self._functions = {}
        self._actual_function = None
        self._name_func_map = {}
        self._pushed_args = 0
        self._labels_map = {}

    def get_var_location(self, name):
        return self._actual_function.get_var_location(name)

    def register_function(self, name, function):
        self._functions[name] = function

    def init_function(self, function):
        self._actual_function = function
        self._labels_map = {}

    def finish_functions(self):
        self._actual_function = None

    def push_arg(self):
        self._pushed_args += 1

    def clean_pushed_args(self):
        self._pushed_args = 0

    def get_free_reg(self):
        return self._registers_manager.get_free_reg()

    def free_reg(self, reg):
        self._registers_manager.free_reg(reg)

    def in_entry_function(self):
        return self._actual_function.label == 'main'

    def register_label(self, cil_label, mips_label):
        self._labels_map[cil_label] = mips_label

    def get_mips_label(self, label):
        return self._labels_map[label]

    @visitor.on('node')
    def collect_labels_in_func(self, node):
        pass

    @visitor.when(cil.LabelNode)
    def collect_labels_in_func(self, node):
        self.register_label(node.label, f'{self._actual_function.label}_{node.label}')


    @visitor.on('node')
    def visit(self, node):
        pass

    @visitor.when(cil.InstructionNode)
    def visit(self, node):
        print(type(node))

    @visitor.when(cil.ProgramNode)
    def visit(self, node):
        self._data_section["default_str"] = mips.StringConst("default_str", "")
        # Convert CIL ProgramNode to MIPS ProgramNode
        for tp in node.dottypes:
            self.visit(tp)

        for data in node.dotdata:
            self.visit(data)

        for func in node.dotcode:
            self.visit(func)

        return mips.ProgramNode([data for data in self._data_section.values()], [tp for tp in self._types.values()], [func for func in self._functions.values()])

    @visitor.when(cil.TypeNode)
    def visit(self, node):
        self._data_section[node.name] = mips.StringConst(node.name, node.name)


        methods = {key: value
                   for key, value in node.methods}
        defaults = []
        if node.name == "String":
            defaults = [('value', 'default_str'), ('length', 'type_Int_proto')]
        new_type = mips.MIPSType(f"type_{node.name}", node.name, node.attributes, methods, len(
            self._types), default=defaults)

        self._types[node.name] = new_type

    @visitor.when(cil.DataNode)
    def visit(self, node):
        self._data_section[node.name] = mips.StringConst(node.name, node.value)

    @visitor.when(cil.FunctionNode)
    def visit(self, node:cil.FunctionNode):
        if node.name == "init_attr_at_Cons":
            a= 5
        label = "main" if node.name == "entry" else node.name
        params = [param.name for param in node.params]
        localvars = [local.name for local in node.localvars]
        size_for_locals = len(localvars) * mips.ATTR_SIZE

        new_func = mips.FunctionNode(label, params, localvars)
        self.register_function(node.name, new_func)
        self.init_function(new_func)

        for instruction in node.instructions:
            self.collect_labels_in_func(instruction)

        initial_instructions = []
        initial_instructions.extend(mips.push_register(mips.RA_REG))
        initial_instructions.extend(mips.push_register(mips.FP_REG))
        initial_instructions.append(
            mips.AddInmediateNode(mips.FP_REG, mips.SP_REG, 8))
        initial_instructions.append(mips.AddInmediateNode(
            mips.SP_REG, mips.SP_REG, -size_for_locals))

        code_instructions = []

        code_instructions = list(itt.chain.from_iterable(
            [self.visit(instruction) for instruction in node.instructions]))

        final_instructions = []

        final_instructions.append(mips.AddInmediateNode(
            mips.SP_REG, mips.SP_REG, size_for_locals))
        final_instructions.append(mips.AddInmediateNode(mips.FP_REG,mips.SP_REG,-8))
        final_instructions.extend(mips.pop_register(mips.FP_REG))
        final_instructions.extend(mips.pop_register(mips.RA_REG))

        if not self.in_entry_function():
            final_instructions.append(mips.JumpRegister(mips.RA_REG))
        else:
            final_instructions.extend(mips.exit_program())

        func_instructions = list(
            itt.chain(initial_instructions, code_instructions, final_instructions))
        new_func.add_instructions(func_instructions)

        self.finish_functions()

    @visitor.when(cil.ArgNode)
    def visit(self, node):
        self.push_arg()
        instructions = []
        if type(node.name) == int:
            instructions.append(mips.LoadInmediateNode(
                mips.ARG_REGISTERS[0], node.name))
            instructions.extend(mips.push_register(mips.ARG_REGISTERS[0]))
        else:
            reg = mips.ARG_REGISTERS[0]
            instructions.append(mips.LoadWordNode(
                reg, self.get_var_location(node.name)))
            instructions.extend(mips.push_register(reg))
        return instructions

    @visitor.when(cil.StaticCallNode)
    def visit(self, node):
        instructions = []
        label = node.function
        if label == "function_main_at_Main":
            a= 5
        instructions.append(mips.JumpAndLinkNode(label))

        instructions.append(mips.StoreWordNode(
            mips.V0_REG, self.get_var_location(node.dest)))


        if self._pushed_args > 0:
            instructions.append(mips.AddInmediateNode(
                mips.SP_REG, mips.SP_REG, self._pushed_args * mips.ATTR_SIZE))
            self.clean_pushed_args()
        return instructions

    @visitor.when(cil.AssignNode)
    def visit(self, node):
        instructions = []                                             

        reg1 = None
        if type(node.source) == cil.VoidNode:
            reg1 = mips.ZERO_REG
        elif node.source.isnumeric():
            reg1 = mips.ARG_REGISTERS[0]
            instructions.append(mips.LoadInmediateNode(reg1, int(node.source)))
        else:
            reg1 = mips.ARG_REGISTERS[0]
            instructions.append(mips.LoadWordNode(
                reg1, self.get_var_location(node.source)))

        instructions.append(mips.StoreWordNode(
            reg1, self.get_var_location(node.dest)))
        
        return instructions

    @visitor.when(cil.AllocateNode)
    def visit(self, node):
        instructions = []

        tp = 0
        if node.type.isnumeric():
            tp = node.type
        else:
            tp = self._types[node.type].index


        instructions.append(mips.LoadInmediateNode(mips.ARG_REGISTERS[0], tp))

        instructions.extend(mips.create_object(mips.ARG_REGISTERS[0], mips.ARG_REGISTERS[1] ))

        instructions.append(mips.StoreWordNode(
            mips.V0_REG, self.get_var_location(node.dest)))
        
        return instructions

    @visitor.when(cil.ReturnNode)
    def visit(self, node):
        instructions = []

        if node.value is None:
            instructions.append(mips.LoadInmediateNode(mips.V0_REG, 0))
        elif isinstance(node.value, int):
            instructions.append(
                mips.LoadInmediateNode(mips.V0_REG, node.value))
        elif isinstance(node.value, cil.VoidNode):
            instructions.append(mips.LoadInmediateNode(mips.V0_REG, 0))
        else:
            instructions.append(mips.LoadWordNode(
                mips.V0_REG, self.get_var_location(node.value)))
        return instructions

    @visitor.when(cil.LoadNode)
    def visit(self, node):
        instructions = []

        string_location = mips.LabelRelativeLocation(
            node.msg.name, 0)
        instructions.append(mips.LoadAddressNode(
            mips.ARG_REGISTERS[0], string_location))
        instructions.append(mips.StoreWordNode(
            mips.ARG_REGISTERS[0], self.get_var_location(node.dest)))
        
        return instructions

    @visitor.when(cil.PrintIntNode)
    def visit(self, node):
        instructions = []
        instructions.append(mips.LoadInmediateNode(mips.V0_REG, 1))

        instructions.append(mips.LoadWordNode(
            mips.ARG_REGISTERS[0], self.get_var_location(node.value)))
        
        instructions.append(mips.SyscallNode())

        return instructions

    @visitor.when(cil.PrintStrNode)
    def visit(self, node):
        instructions = []
        instructions.append(mips.LoadInmediateNode(mips.V0_REG, 4))

        instructions.append(mips.LoadWordNode(
            mips.ARG_REGISTERS[0], self.get_var_location(node.value)))
        instructions.append(mips.SyscallNode())

        return instructions

    @visitor.when(cil.TypeNameNode)
    def visit(self, node):
        instructions = []

        reg1 = mips.REGISTERS[0]
        instructions.append(mips.LoadWordNode(
            reg1, self.get_var_location(node.source)))
        instructions.append(mips.LoadWordNode(
            mips.ARG_REGISTERS[0], mips.RegisterRelativeLocation(reg1, 0)))
        instructions.append(mips.ShiftLeftLogicalNode(
            mips.ARG_REGISTERS[0], mips.ARG_REGISTERS[0], 2))
        instructions.append(mips.LoadAddressNode(
            mips.ARG_REGISTERS[1], mips.TYPENAMES_TABLE_LABEL))
        instructions.append(mips.AddUnsignedNode(
            mips.ARG_REGISTERS[0], mips.ARG_REGISTERS[0], mips.ARG_REGISTERS[1]))
        instructions.append(mips.LoadWordNode(
            mips.ARG_REGISTERS[0], mips.RegisterRelativeLocation(mips.ARG_REGISTERS[0], 0)))

        
        instructions.append(mips.StoreWordNode(
            mips.ARG_REGISTERS[0], self.get_var_location(node.dest)))

        return instructions

    @visitor.when(cil.ExitNode)
    def visit(self, node):
        instructions = []
        instructions.append(mips.LoadInmediateNode(mips.V0_REG, 10))
        instructions.append(mips.SyscallNode())

        return instructions

    @visitor.when(cil.GetAttribNode)
    def visit(self, node):
        instructions = []

        dest = node.dest if type(node.dest) == str else node.dest.name
        obj = node.obj if type(node.obj) == str else node.obj.name
        comp_type = node.computed_type if type(
            node.computed_type) == str else node.computed_type.name

        reg = mips.ARG_REGISTERS[0]

        instructions.append(mips.LoadWordNode(
            reg, self.get_var_location(obj)))

        tp = self._types[comp_type]
        offset = (tp.attributes.index(node.attr) + 3) * mips.ATTR_SIZE
        instructions.append(mips.LoadWordNode(
            mips.ARG_REGISTERS[1], mips.RegisterRelativeLocation(reg, offset)))

        instructions.append(mips.StoreWordNode(
            mips.ARG_REGISTERS[1], self.get_var_location(dest)))
        return instructions

    @visitor.when(cil.SetAttribNode)
    def visit(self, node):
        instructions = []

        obj = node.obj if type(node.obj) == str else node.obj.name
        comp_type = node.computed_type if type(
            node.computed_type) == str else node.computed_type.name

        tp = self._types[comp_type]
        offset = (tp.attributes.index(node.attr) + 3) * mips.ATTR_SIZE

        reg1 = mips.ARG_REGISTERS[0]
        instructions.append(mips.LoadWordNode(
            mips.ARG_REGISTERS[0], self.get_var_location(obj)))

        reg2 = None
        if type(node.value) == int:
            reg2 = instructions.append(mips.LoadInmediateNode(
                mips.ARG_REGISTERS[1], node.value))
        else:
            word_to_load = self.get_var_location(node.value) if type(node.value).__name__ =='str' else 0
            reg2 = mips.ARG_REGISTERS[1]
            instructions.append(mips.LoadWordNode(
                reg2, word_to_load))

        instructions.append(mips.StoreWordNode(
            reg2, mips.RegisterRelativeLocation(reg1, offset)))

        return instructions

    @visitor.when(cil.CopyNode)
    def visit(self, node):
        instructions = []

        reg = mips.ARG_REGISTERS[0]
        instructions.append(mips.LoadWordNode(
            reg, self.get_var_location(node.source)))

        instructions.extend(mips.copy_object(reg, mips.ARG_REGISTERS[3]))

        instructions.append(mips.StoreWordNode(
            mips.V0_REG, self.get_var_location(node.dest)))
        return instructions

    @visitor.when(cil.EqualNode)
    def visit(self, node):
        instructions = []

        if type(node.left) == int:
            instructions.append(mips.LoadInmediateNode(
                mips.ARG_REGISTERS[0], node.left))
        elif type(node.left) == cil.VoidNode:
            instructions.append(
                mips.LoadInmediateNode(mips.ARG_REGISTERS[0], 0))
        else:
            instructions.append(mips.LoadWordNode(
                mips.ARG_REGISTERS[0], self.get_var_location(node.left)))

        if type(node.right) == int:
            instructions.append(mips.LoadInmediateNode(
                mips.ARG_REGISTERS[1], node.right))
        elif type(node.right) == cil.VoidNode:
            instructions.append(
                mips.LoadInmediateNode(mips.ARG_REGISTERS[1], 0))
        else:
            instructions.append(mips.LoadWordNode(
                mips.ARG_REGISTERS[1], self.get_var_location(node.right)))

        instructions.append(mips.JumpAndLinkNode("equals"))

        instructions.append(mips.StoreWordNode(
            mips.V0_REG, self.get_var_location(node.dest)))
        return instructions

    @visitor.when(cil.EqualStrNode)
    def visit(self, node):
        instructions = []

        instructions.append(mips.LoadWordNode(
            mips.ARG_REGISTERS[0], self.get_var_location(node.left)))
        instructions.append(mips.LoadWordNode(
            mips.ARG_REGISTERS[1], self.get_var_location(node.right)))

        instructions.append(mips.JumpAndLinkNode("equal_str"))

        instructions.append(mips.StoreWordNode(
            mips.V0_REG, self.get_var_location(node.dest)))

        return instructions

    @visitor.when(cil.LabelNode)
    def visit(self, node):
        return [mips.LabelNode(self.get_mips_label(node.label))]

    @visitor.when(cil.GotoIfNode)
    def visit(self, node):
        instructions = []

        mips_label = self.get_mips_label(node.label)

        reg = mips.ARG_REGISTERS[0]
        instructions.append(mips.LoadWordNode(
            mips.ARG_REGISTERS[0], self.get_var_location(node.condition)))

        instructions.append(mips.BranchOnNotEqualNode(
            reg, mips.ZERO_REG, mips_label))

        

        return instructions

    @visitor.when(cil.GotoNode)
    def visit(self, node):
        mips_label = self.get_mips_label(node.label)
        return [mips.JumpNode(mips_label)]

    @visitor.when(cil.TypeOfNode)
    def visit(self, node):
        instructions = []

        reg1 = mips.ARG_REGISTERS[0]
        instructions.append(mips.LoadWordNode(
            reg1, self.get_var_location(node.obj)))

        instructions.append(mips.LoadWordNode(
            mips.ARG_REGISTERS[1], mips.RegisterRelativeLocation(reg1, 0)))
        instructions.append(mips.StoreWordNode(
            mips.ARG_REGISTERS[1], self.get_var_location(node.dest)))
        return instructions

    @visitor.when(cil.DynamicCallNode)
    def visit(self, node):
        instructions = []

        comp_tp = self._types[node.computed_type]
        method_index = list(comp_tp.methods).index(node.method)
        reg = mips.ARG_REGISTERS[0]
        instructions.append(mips.LoadWordNode(
            reg, self.get_var_location(node.type)))

        instructions.append(mips.LoadAddressNode(
            mips.ARG_REGISTERS[1], mips.PROTO_TABLE_LABEL))
        
        instructions.append(mips.ShiftLeftLogicalNode(
            mips.ARG_REGISTERS[2], reg, 2))
        instructions.append(mips.AddUnsignedNode(
            mips.ARG_REGISTERS[1], mips.ARG_REGISTERS[1], mips.ARG_REGISTERS[2]))
        instructions.append(mips.LoadWordNode(
            mips.ARG_REGISTERS[1], mips.RegisterRelativeLocation(mips.ARG_REGISTERS[1], 0)))
        instructions.append(mips.LoadWordNode(
            mips.ARG_REGISTERS[1], mips.RegisterRelativeLocation(mips.ARG_REGISTERS[1], 8)))
        instructions.append(mips.AddInmediateUnsignedNode(
            mips.ARG_REGISTERS[1], mips.ARG_REGISTERS[1], method_index * 4))
        instructions.append(mips.LoadWordNode(
            mips.ARG_REGISTERS[1], mips.RegisterRelativeLocation(mips.ARG_REGISTERS[1], 0)))
        instructions.append(
            mips.JumpRegisterAndLinkNode(mips.ARG_REGISTERS[1]))

        instructions.append(mips.StoreWordNode(
            mips.V0_REG, self.get_var_location(node.dest)))
        if self._pushed_args > 0:
            instructions.append(mips.AddInmediateNode(
                mips.SP_REG, mips.SP_REG, self._pushed_args * mips.ATTR_SIZE))
            self.clean_pushed_args()

        return instructions

    @visitor.when(cil.ErrorNode)
    def visit(self, node):
        instructions = []

        mips_label = self._data_section[node.data_node.name].label

        instructions.append(mips.LoadInmediateNode(mips.V0_REG, 4))
        instructions.append(mips.LoadAddressNode(
            mips.ARG_REGISTERS[0], mips_label))
        instructions.append(mips.SyscallNode())
        instructions.append(mips.LoadInmediateNode(mips.V0_REG, 10))
        instructions.append(mips.SyscallNode())

        return instructions

    @visitor.when(cil.NameNode)
    def visit(self, node):
        instructions = []

        reg = mips.ARG_REGISTERS[0]

        instructions.append(mips.LoadAddressNode(
            reg, mips.TYPENAMES_TABLE_LABEL))

        tp_number = self._types[node.name].index
        instructions.append(
            mips.AddInmediateUnsignedNode(reg, reg, tp_number*4))
        instructions.append(mips.LoadWordNode(
            reg, mips.RegisterRelativeLocation(reg, 0)))

        instructions.append(mips.StoreWordNode(
            reg, self.get_var_location(node.dest)))

        return instructions

    @visitor.when(cil.PlusNode)
    def visit(self, node):
        instructions = []

        reg1, reg2 = None, None
        if type(node.left) == int:
            reg1 = mips.ARG_REGISTERS[0]
            instructions.append(mips.LoadInmediateNode(reg1, node.left))
        else:
            reg1 = mips.ARG_REGISTERS[0]
            instructions.append(mips.LoadWordNode(
                reg1, self.get_var_location(node.left)))

        if type(node.right) == int:
            reg2 = mips.ARG_REGISTERS[1]
            instructions.append(mips.LoadInmediateNode(reg2, node.right))
        else:
            reg2 = mips.ARG_REGISTERS[1]
            instructions.append(mips.LoadWordNode(
                reg2, self.get_var_location(node.right)))


        instructions.append(mips.AddNode(
            mips.ARG_REGISTERS[0], reg1, reg2))
        instructions.append(mips.StoreWordNode(
            mips.ARG_REGISTERS[0], self.get_var_location(node.dest)))
        return instructions

    @visitor.when(cil.MinusNode)
    def visit(self, node):
        instructions = []

        reg1, reg2 = None, None
        if type(node.left) == int:
            reg1 = mips.ARG_REGISTERS[0]
            instructions.append(mips.LoadInmediateNode(reg1, node.left))
        else:
            reg1 = mips.ARG_REGISTERS[0]
            instructions.append(mips.LoadWordNode(
                reg1, self.get_var_location(node.left)))

        if type(node.right) == int:
            instructions.append(mips.LoadInmediateNode(reg2, node.right))
        else:
            reg2 = mips.ARG_REGISTERS[1]
            instructions.append(mips.LoadWordNode(
                reg2, self.get_var_location(node.right)))

        instructions.append(mips.SubNode(
            mips.ARG_REGISTERS[0], reg1, reg2))
        instructions.append(mips.StoreWordNode(
            mips.ARG_REGISTERS[0], self.get_var_location(node.dest)))
        return instructions

    @visitor.when(cil.StarNode)
    def visit(self, node):
        instructions = []

        reg1, reg2 = None, None
        if type(node.left) == int:
            reg1 = mips.ARG_REGISTERS[0]
            instructions.append(mips.LoadInmediateNode(reg1, node.left))
        else:
            reg1 = mips.ARG_REGISTERS[0]
            instructions.append(mips.LoadWordNode(
                reg1, self.get_var_location(node.left)))

        if type(node.right) == int:
            reg2 = mips.ARG_REGISTERS[1]
            instructions.append(mips.LoadInmediateNode(reg2, node.right))
        else:
            reg2 = mips.ARG_REGISTERS[1]
            instructions.append(mips.LoadWordNode(
                reg2, self.get_var_location(node.right)))

        instructions.append(mips.MultiplyNode(
            mips.ARG_REGISTERS[0], reg1, reg2))
        instructions.append(mips.StoreWordNode(
            mips.ARG_REGISTERS[0], self.get_var_location(node.dest)))
        return instructions

    @visitor.when(cil.DivNode)
    def visit(self, node):
        instructions = []

        reg1, reg2 = None, None
        if type(node.left) == int:
            reg1 = mips.ARG_REGISTERS[0]
            instructions.append(mips.LoadInmediateNode(reg1, node.left))
        else:
            reg1 = mips.ARG_REGISTERS[0]
            instructions.append(mips.LoadWordNode(
                reg1, self.get_var_location(node.left)))

        if type(node.right) == int:
            reg2 = mips.ARG_REGISTERS[1]
            instructions.append(mips.LoadInmediateNode(reg2, node.right))
        else:
            reg2 = mips.ARG_REGISTERS[1]
            instructions.append(mips.LoadWordNode(
                reg2, self.get_var_location(node.right)))

        instructions.append(mips.DivideNode(reg1, reg2))
        instructions.append(mips.MoveFromLowNode(mips.ARG_REGISTERS[0]))
        instructions.append(mips.StoreWordNode(
            mips.ARG_REGISTERS[0], self.get_var_location(node.dest)))

        return instructions

    @visitor.when(cil.ComplementNode)
    def visit(self, node):
        instructions = []

        reg1 = None

        if type(node.obj) == int:
            reg1 = mips.ARG_REGISTERS[0]
            instructions.append(mips.LoadInmediateNode(reg1, node.obj))
        else:
            reg1 = mips.ARG_REGISTERS[0]
            instructions.append(mips.LoadWordNode(
                reg1, self.get_var_location(node.obj)))

        reg2 = mips.ARG_REGISTERS[1]
        instructions.append(mips.ComplementNode(reg2, reg1))
        instructions.append(mips.AddInmediateNode(reg2, reg2, 1))
        instructions.append(mips.StoreWordNode(
            reg2, self.get_var_location(node.dest)))

        return instructions

    @visitor.when(cil.LessEqualNode)
    def visit(self, node):
        instructions = []

        if type(node.left) == int:
            instructions.append(mips.LoadInmediateNode(
                mips.ARG_REGISTERS[0], node.left))
        else:
            instructions.append(mips.LoadWordNode(
                mips.ARG_REGISTERS[0], self.get_var_location(node.left)))

        if type(node.right) == int:
            instructions.append(mips.LoadInmediateNode(
                mips.ARG_REGISTERS[1], node.right))
        else:
            instructions.append(mips.LoadWordNode(
                mips.ARG_REGISTERS[1], self.get_var_location(node.right)))

        instructions.append(mips.JumpAndLinkNode('less_equal'))
        instructions.append(mips.StoreWordNode(
            mips.V0_REG, self.get_var_location(node.dest)))
        return instructions

    @visitor.when(cil.LessNode)
    def visit(self, node):
        instructions = []


        if type(node.left) == int:
            instructions.append(mips.LoadInmediateNode(
                mips.ARG_REGISTERS[0], node.left))
        else:
            instructions.append(mips.LoadWordNode(
                mips.ARG_REGISTERS[0], self.get_var_location(node.left)))

        if type(node.right) == int:
            instructions.append(mips.LoadInmediateNode(
                mips.ARG_REGISTERS[1], node.right))
        else:
            instructions.append(mips.LoadWordNode(
                mips.ARG_REGISTERS[1], self.get_var_location(node.right)))
        instructions.append(mips.JumpAndLinkNode('less'))
        instructions.append(mips.StoreWordNode(
            mips.V0_REG, self.get_var_location(node.dest)))


        return instructions

    @visitor.when(cil.ReadStrNode)
    def visit(self, node):
        instructions = []
        instructions.append(mips.JumpAndLinkNode("read_str"))

        instructions.append(mips.StoreWordNode(
            mips.V0_REG, self.get_var_location(node.dest)))
        return instructions

    @visitor.when(cil.LengthNode)
    def visit(self, node):
        instructions = []
        instructions.extend(mips.push_register(mips.ARG_REGISTERS[0]))

        reg = mips.ARG_REGISTERS[0]
        instructions.append(mips.LoadWordNode(
            reg, self.get_var_location(node.source)))

        instructions.append(mips.MoveNode(mips.ARG_REGISTERS[0], reg))
        instructions.append(mips.JumpAndLinkNode("len"))

        instructions.append(mips.StoreWordNode(
            mips.V0_REG, self.get_var_location(node.dest)))

        instructions.extend(mips.pop_register(mips.ARG_REGISTERS[0]))
        return instructions

    @visitor.when(cil.ReadIntNode)
    def visit(self, node):
        instructions = []

        instructions.append(mips.LoadInmediateNode(mips.V0_REG, 5))
        instructions.append(mips.SyscallNode())
        instructions.append(mips.StoreWordNode(
            mips.V0_REG, self.get_var_location(node.dest)))

        return instructions

    @visitor.when(cil.ConcatNode)
    def visit(self, node):
        instructions = []

        instructions.append(mips.LoadWordNode(
            mips.ARG_REGISTERS[0], self.get_var_location(node.prefix)))
        instructions.append(mips.LoadWordNode(
            mips.ARG_REGISTERS[1], self.get_var_location(node.suffix)))
        instructions.append(mips.LoadWordNode(
            mips.ARG_REGISTERS[2], self.get_var_location(node.length)))
        instructions.append(mips.JumpAndLinkNode("concat"))

        instructions.append(mips.StoreWordNode(
            mips.V0_REG, self.get_var_location(node.dest)))
        return instructions

    @visitor.when(cil.SubstringNode)
    def visit(self, node):
        instructions = []

        instructions.append(mips.LoadWordNode(
            mips.ARG_REGISTERS[0], self.get_var_location(node.str_value)))

        if type(node.index) == int:
            instructions.append(mips.LoadInmediateNode(
                mips.ARG_REGISTERS[1], node.index))
        else:
            instructions.append(mips.LoadWordNode(
                mips.ARG_REGISTERS[1], self.get_var_location(node.index)))

        if type(node.length) == int:
            instructions.append(mips.LoadInmediateNode(
                mips.ARG_REGISTERS[2], node.length))
        else:
            instructions.append(mips.LoadWordNode(
                mips.ARG_REGISTERS[2], self.get_var_location(node.length)))
        instructions.append(mips.JumpAndLinkNode("substr"))
        instructions.append(mips.StoreWordNode(
            mips.V0_REG, self.get_var_location(node.dest)))
        return instructions

