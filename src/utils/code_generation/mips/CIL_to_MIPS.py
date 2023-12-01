import itertools as itt
import cmp.visitor as visitor
from utils.code_generation.cil.AST_CIL import cil_ast as cil
from utils.code_generation.mips.AST_MIPS import mips_ast as mips
from utils.code_generation.mips.AST_MIPS import *
from utils.code_generation.mips.utils_mips import *


class CILToMIPS:
    def __init__(self, label_generator=LabelGenerator()):
        self._label_generator = label_generator
        self.memory_manager = None
        self._types = {}
        self._data_section = {}
        self._functions = {}
        self._actual_function = None
        self._name_func_map = {}
        self._pushed_args = 0
        self._labels_map = {}

    def generate_type_label(self):
        return self._label_generator.generate_type_label()

    def generate_data_label(self):
        return self._label_generator.generate_data_label()

    def generate_code_label(self):
        return self._label_generator.generate_code_label()

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
    def collect_func_names(self, node):
        pass

    @visitor.when(cil.ProgramNode)
    def collect_func_names(self, node):
        for func in node.dotcode:
            self.collect_func_names(func)

    @visitor.when(cil.FunctionNode)
    def collect_func_names(self, node):
        if node.id == "entry":
            self._name_func_map[node.id] = 'main'
        else:
            self._name_func_map[node.id] = self.generate_code_label()

    @visitor.on('node')
    def collect_labels_in_func(self, node):
        pass

    @visitor.when(cil.LabelNode)
    def collect_labels_in_func(self, node):
        mips_label = self.generate_code_label()
        self.register_label(node.label, mips_label)

    @visitor.on('node')
    def visit(self, node):
        pass

    @visitor.when(cil.ProgramNode)
    def visit(self, node):

        self.collect_func_names(node)

        self._data_section["default_str"] = mips.StringConst("default_str", "")
        for tp in node.dottypes:
            self.visit(tp)

        for data in node.dotdata:
            self.visit(data)

        for func in node.dotcode:
            self.visit(func)

        return mips.ProgramNode([data for data in self._data_section.values()], [tp for tp in self._types.values()], [func for func in self._functions.values()])

    @visitor.when(cil.TypeNode)
    def visit(self, node):
        name_label = self.generate_data_label()
        self._data_section[node.id] = mips.StringConst(name_label, node.id)

        type_label = self.generate_type_label()
        methods = {key: self._name_func_map[value]
                   for key, value in node.methods}
        defaults = []
        if node.id == "String":
            defaults = [('value', 'default_str'), ('length', 'type_4_proto')]
        new_type = MIPSType(type_label, name_label, node.attributes, methods, len(
            self._types), default=defaults)

        self._types[node.id] = new_type

    @visitor.when(cil.DataNode)
    def visit(self, node):
        label = self.generate_data_label()
        self._data_section[node.id] = mips.StringConst(label, node.value)

    @visitor.when(cil.FunctionNode)
    def visit(self, node):
        used_regs_finder = UsedRegisterFinder()

        label = self._name_func_map[node.id]
        params = [param.id for param in node.params]
        localvars = [local.id for local in node.localvars]
        size_for_locals = len(localvars) * 4

        new_func = mips.FunctionNode(label, params, localvars)
        self.register_function(node.id, new_func)
        self.init_function(new_func)

        ra = RegistersAllocator()

        if len(node.instructions):
            reg_for_var = ra.get_registers_for_variables(
                node.instructions, node.params, 10)
            self.memory_manager = MemoryManager(
                [Register(name) for name in ['t0', 't1', 't2',
                                             't3', 't4', 't5', 't6', 't7', 't8', 't9']], lambda x: reg_for_var[x])

        for instruction in node.instructions:
            self.collect_labels_in_func(instruction)

        initial_instructions = []
        if self.in_entry_function():
            initial_instructions.append(
                mips.JumpAndLinkNode("mem_manager_init"))

        initial_instructions.extend(push_register(Register('fp')))
        initial_instructions.append(
            mips.AddInmediateNode(Register('fp'), SP_REG, 4))
        initial_instructions.append(mips.AddInmediateNode(
            SP_REG, SP_REG, -size_for_locals))

        code_instructions = []

        code_instructions = list(itt.chain.from_iterable(
            [self.visit(instruction) for instruction in node.instructions]))

        final_instructions = []

        for param in params:
            reg = self.memory_manager.get_reg_for_var(param)
            if reg is not None:
                code_instructions.insert(0, mips.LoadWordNode(
                    reg, self.get_var_location(param)))

        if not self.in_entry_function():
            used_regs = used_regs_finder.get_used_registers(code_instructions)
            for reg in used_regs:
                initial_instructions.extend(push_register(reg))

            for reg in used_regs[::-1]:
                final_instructions.extend(pop_register(reg))

        final_instructions.append(mips.AddInmediateNode(
            SP_REG, SP_REG, size_for_locals))
        final_instructions.extend(pop_register(Register('fp')))

        if not self.in_entry_function():
            final_instructions.append(mips.JumpRegisterNode(RA_REG))
        else:
            final_instructions.extend(exit_program())

        func_instructions = list(
            itt.chain(initial_instructions, code_instructions, final_instructions))
        new_func.add_instructions(func_instructions)

        self.finish_functions()

    @visitor.when(cil.InstructionNode)
    def visit(self, node):
        print(type(node))

    @visitor.when(cil.AssignNode)
    def visit(self, node):
        instructions = []

        reg1 = None
        if type(node.right) == cil.VoidNode:
            reg1 = ZERO_REG
        elif node.right.isnumeric():
            reg1 = ARG_REGISTERS[0]
            instructions.append(mips.LoadInmediateNode(reg1, int(node.right)))
        else:
            reg1 = self.memory_manager.get_reg_for_var(node.right)
            if reg1 is None:
                reg1 = ARG_REGISTERS[0]
                instructions.append(mips.LoadWordNode(
                    reg1, self.get_var_location(node.right)))

        reg2 = self.memory_manager.get_reg_for_var(node.left)
        if reg2 is None:
            instructions.append(mips.StoreWordNode(
                reg1, self.get_var_location(node.left)))
        else:
            instructions.append(mips.MoveNode(reg2, reg1))

        return instructions

    @visitor.when(cil.PlusNode)
    def visit(self, node):
        instructions = []

        reg1, reg2 = None, None
        if type(node.op_l) == int:
            reg1 = ARG_REGISTERS[0]
            instructions.append(mips.LoadInmediateNode(reg1, node.op_l))
        else:
            reg1 = self.memory_manager.get_reg_for_var(node.op_l)
            if reg1 is None:
                reg1 = ARG_REGISTERS[0]
                instructions.append(mips.LoadWordNode(
                    reg1, self.get_var_location(node.op_l)))

        if type(node.op_r) == int:
            reg2 = ARG_REGISTERS[1]
            instructions.append(mips.LoadInmediateNode(reg2, node.op_r))
        else:
            reg2 = self.memory_manager.get_reg_for_var(node.op_r)
            if reg2 is None:
                reg2 = ARG_REGISTERS[1]
                instructions.append(mips.LoadWordNode(
                    reg2, self.get_var_location(node.op_r)))

        reg3 = self.memory_manager.get_reg_for_var(node.dest)
        if reg3 is None:
            instructions.append(mips.AddNode(
                ARG_REGISTERS[0], reg1, reg2))
            instructions.append(mips.StoreWordNode(
                ARG_REGISTERS[0], self.get_var_location(node.dest)))
        else:
            instructions.append(mips.AddNode(reg3, reg1, reg2))

        return instructions

    @visitor.when(cil.MinusNode)
    def visit(self, node):
        instructions = []

        reg1, reg2 = None, None
        if type(node.op_l) == int:
            reg1 = ARG_REGISTERS[0]
            instructions.append(mips.LoadInmediateNode(reg1, node.op_l))
        else:
            reg1 = self.memory_manager.get_reg_for_var(node.op_l)
            if reg1 is None:
                reg1 = ARG_REGISTERS[0]
                instructions.append(mips.LoadWordNode(
                    reg1, self.get_var_location(node.op_l)))

        if type(node.op_r) == int:
            instructions.append(mips.LoadInmediateNode(reg2, node.op_r))
        else:
            reg2 = self.memory_manager.get_reg_for_var(node.op_r)
            if reg2 is None:
                reg2 = ARG_REGISTERS[1]
                instructions.append(mips.LoadWordNode(
                    reg2, self.get_var_location(node.op_r)))

        reg3 = self.memory_manager.get_reg_for_var(node.dest)
        if reg3 is None:
            instructions.append(mips.SubNode(
                ARG_REGISTERS[0], reg1, reg2))
            instructions.append(mips.StoreWordNode(
                ARG_REGISTERS[0], self.get_var_location(node.dest)))
        else:
            instructions.append(mips.SubNode(reg3, reg1, reg2))

        return instructions

    @visitor.when(cil.StarNode)
    def visit(self, node):
        instructions = []

        reg1, reg2 = None, None
        if type(node.op_l) == int:
            reg1 = ARG_REGISTERS[0]
            instructions.append(mips.LoadInmediateNode(reg1, node.op_l))
        else:
            reg1 = self.memory_manager.get_reg_for_var(node.op_l)
            if reg1 is None:
                reg1 = ARG_REGISTERS[0]
                instructions.append(mips.LoadWordNode(
                    reg1, self.get_var_location(node.op_l)))

        if type(node.op_r) == int:
            reg2 = ARG_REGISTERS[1]
            instructions.append(mips.LoadInmediateNode(reg2, node.op_r))
        else:
            reg2 = self.memory_manager.get_reg_for_var(node.op_r)
            if reg2 is None:
                reg2 = ARG_REGISTERS[1]
                instructions.append(mips.LoadWordNode(
                    reg2, self.get_var_location(node.op_r)))

        reg3 = self.memory_manager.get_reg_for_var(node.dest)
        if reg3 is None:
            instructions.append(mips.MultiplyNode(
                ARG_REGISTERS[0], reg1, reg2))
            instructions.append(mips.StoreWordNode(
                ARG_REGISTERS[0], self.get_var_location(node.dest)))
        else:
            instructions.append(mips.MultiplyNode(reg3, reg1, reg2))

        return instructions

    @visitor.when(cil.DivNode)
    def visit(self, node):
        instructions = []

        reg1, reg2 = None, None
        if type(node.op_l) == int:
            reg1 = ARG_REGISTERS[0]
            instructions.append(mips.LoadInmediateNode(reg1, node.op_l))
        else:
            reg1 = self.memory_manager.get_reg_for_var(node.op_l)
            if reg1 is None:
                reg1 = ARG_REGISTERS[0]
                instructions.append(mips.LoadWordNode(
                    reg1, self.get_var_location(node.op_l)))

        if type(node.op_r) == int:
            reg2 = ARG_REGISTERS[1]
            instructions.append(mips.LoadInmediateNode(reg2, node.op_r))
        else:
            reg2 = self.memory_manager.get_reg_for_var(node.op_r)
            if reg2 is None:
                reg2 = ARG_REGISTERS[1]
                instructions.append(mips.LoadWordNode(
                    reg2, self.get_var_location(node.op_r)))

        instructions.append(mips.DivideNode(reg1, reg2))
        reg3 = self.memory_manager.get_reg_for_var(node.dest)
        if reg3 is None:
            instructions.append(mips.MoveFromLowNode(ARG_REGISTERS[0]))
            instructions.append(mips.StoreWordNode(
                ARG_REGISTERS[0], self.get_var_location(node.dest)))
        else:
            instructions.append(mips.MoveFromLowNode(reg3))

        return instructions

    @visitor.when(cil.LessThanNode)
    def visit(self, node):
        instructions = []

        if type(node.op_l) == int:
            instructions.append(mips.LoadInmediateNode(
                ARG_REGISTERS[0], node.op_l))
        else:
            reg = self.memory_manager.get_reg_for_var(node.op_l)
            if reg is None:
                instructions.append(mips.LoadWordNode(
                    ARG_REGISTERS[0], self.get_var_location(node.op_l)))
            else:
                instructions.append(mips.MoveNode(ARG_REGISTERS[0], reg))

        if type(node.op_r) == int:
            instructions.append(mips.LoadInmediateNode(
                ARG_REGISTERS[1], node.op_r))
        else:
            reg = self.memory_manager.get_reg_for_var(node.op_r)
            if reg is None:
                instructions.append(mips.LoadWordNode(
                    ARG_REGISTERS[1], self.get_var_location(node.op_r)))
            else:
                instructions.append(mips.MoveNode(ARG_REGISTERS[1], reg))

        instructions.append(mips.JumpAndLinkNode('less'))
        reg = self.memory_manager.get_reg_for_var(node.dest)
        if reg is None:
            instructions.append(mips.StoreWordNode(
                V0_REG, self.get_var_location(node.dest)))
        else:
            instructions.append(mips.MoveNode(reg, V0_REG))

        return instructions

    @visitor.when(cil.LessEqualNode)
    def visit(self, node):
        instructions = []

        if type(node.op_l) == int:
            instructions.append(mips.LoadInmediateNode(
                ARG_REGISTERS[0], node.op_l))
        else:
            reg = self.memory_manager.get_reg_for_var(node.op_l)
            if reg is None:
                instructions.append(mips.LoadWordNode(
                    ARG_REGISTERS[0], self.get_var_location(node.op_l)))
            else:
                instructions.append(mips.MoveNode(ARG_REGISTERS[0], reg))

        if type(node.op_r) == int:
            instructions.append(mips.LoadInmediateNode(
                ARG_REGISTERS[1], node.op_r))
        else:
            reg = self.memory_manager.get_reg_for_var(node.op_r)
            if reg is None:
                instructions.append(mips.LoadWordNode(
                    ARG_REGISTERS[1], self.get_var_location(node.op_r)))
            else:
                instructions.append(mips.MoveNode(ARG_REGISTERS[1], reg))

        instructions.append(mips.JumpAndLinkNode('less_eq'))
        reg = self.memory_manager.get_reg_for_var(node.dest)
        if reg is None:
            instructions.append(mips.StoreWordNode(
                V0_REG, self.get_var_location(node.dest)))
        else:
            instructions.append(mips.MoveNode(reg, V0_REG))

        return instructions

    @visitor.when(cil.EqualNode)
    def visit(self, node):
        instructions = []

        if type(node.op_l) == int:
            instructions.append(mips.LoadInmediateNode(
                ARG_REGISTERS[0], node.op_l))
        elif type(node.op_l) == cil.VoidNode:
            instructions.append(
                mips.LoadInmediateNode(ARG_REGISTERS[0], 0))
        else:
            reg = self.memory_manager.get_reg_for_var(node.op_l)
            if reg is None:
                instructions.append(mips.LoadWordNode(
                    ARG_REGISTERS[0], self.get_var_location(node.op_l)))
            else:
                instructions.append(mips.MoveNode(ARG_REGISTERS[0], reg))

        if type(node.op_r) == int:
            instructions.append(mips.LoadInmediateNode(
                ARG_REGISTERS[1], node.op_r))
        elif type(node.op_r) == cil.VoidNode:
            instructions.append(
                mips.LoadInmediateNode(ARG_REGISTERS[1], 0))
        else:
            reg = self.memory_manager.get_reg_for_var(node.op_r)
            if reg is None:
                instructions.append(mips.LoadWordNode(
                    ARG_REGISTERS[1], self.get_var_location(node.op_r)))
            else:
                instructions.append(mips.MoveNode(ARG_REGISTERS[1], reg))

        instructions.append(mips.JumpAndLinkNode("eqs"))

        reg = self.memory_manager.get_reg_for_var(node.dest)
        if reg is None:
            instructions.append(mips.StoreWordNode(
                V0_REG, self.get_var_location(node.dest)))
        else:
            instructions.append(mips.MoveNode(reg, V0_REG))

        return instructions

    @visitor.when(cil.EqualStrNode)
    def visit(self, node):
        instructions = []

        reg = self.memory_manager.get_reg_for_var(node.op_l)
        if reg is None:
            instructions.append(mips.LoadWordNode(
                ARG_REGISTERS[0], self.get_var_location(node.op_l)))
        else:
            instructions.append(mips.MoveNode(ARG_REGISTERS[0], reg))

        reg = self.memory_manager.get_reg_for_var(node.op_r)
        if reg is None:
            instructions.append(mips.LoadWordNode(
                ARG_REGISTERS[1], self.get_var_location(node.op_r)))
        else:
            instructions.append(mips.MoveNode(ARG_REGISTERS[1], reg))

        instructions.append(mips.JumpAndLinkNode("eq_string"))

        reg = self.memory_manager.get_reg_for_var(node.dest)
        if reg is None:
            instructions.append(mips.StoreWordNode(
                V0_REG, self.get_var_location(node.dest)))
        else:
            instructions.append(mips.MoveNode(reg, V0_REG))

        return instructions

    @visitor.when(cil.GetAttrNode)
    def visit(self, node):
        instructions = []

        dest = node.dest if type(node.dest) == str else node.dest.id
        idx = node.id if type(node.id) == str else node.id.id
        comp_type = node.computed_type if type(
            node.computed_type) == str else node.computed_type.id

        reg = self.memory_manager.get_reg_for_var(idx)
        if reg is None:
            reg = ARG_REGISTERS[0]
            instructions.append(mips.LoadWordNode(
                reg, self.get_var_location(idx)))

        tp = self._types[comp_type]
        offset = (tp.attributes.index(node.attr) + 3) * 4
        instructions.append(mips.LoadWordNode(
            ARG_REGISTERS[1], RegisterRelativeLocation(reg, offset)))

        reg = self.memory_manager.get_reg_for_var(dest)
        if reg is None:
            instructions.append(mips.StoreWordNode(
                ARG_REGISTERS[1], self.get_var_location(dest)))
        else:
            instructions.append(mips.MoveNode(reg, ARG_REGISTERS[1]))

        return instructions

    @visitor.when(cil.SetAttrNode)
    def visit(self, node):
        instructions = []

        idx = node.id if type(node.id) == str else node.id.id
        comp_type = node.computed_type if type(
            node.computed_type) == str else node.computed_type.name

        tp = self._types[comp_type]
        offset = (tp.attributes.index(node.attr) + 3) * 4

        reg1 = self.memory_manager.get_reg_for_var(idx)
        if reg1 is None:
            reg1 = ARG_REGISTERS[0]
            instructions.append(mips.LoadWordNode(
                ARG_REGISTERS[0], self.get_var_location(idx)))

        reg2 = None
        if type(node.value) == int:
            reg2 = instructions.append(mips.LoadInmediateNode(
                ARG_REGISTERS[1], node.value))
        else:
            reg2 = self.memory_manager.get_reg_for_var(node.value)
            if reg2 is None:
                reg2 = ARG_REGISTERS[1]
                instructions.append(mips.LoadWordNode(
                    reg2, self.get_var_location(node.value)))

        instructions.append(mips.StoreWordNode(
            reg2, RegisterRelativeLocation(reg1, offset)))

        return instructions

    @visitor.when(cil.AllocateNode)
    def visit(self, node):
        instructions = []

        tp = 0
        if node.type.isnumeric():
            tp = node.type
        else:
            tp = self._types[node.type].index

        reg1 = self.memory_manager.get_reg_unusued()
        reg2 = self.memory_manager.get_reg_unusued([reg1])
        instructions.extend(push_register(reg1))
        instructions.extend(push_register(reg2))

        instructions.append(mips.LoadInmediateNode(reg1, tp))

        instructions.extend(create_object(reg1, reg2))

        instructions.extend(pop_register(reg2))
        instructions.extend(pop_register(reg1))

        reg3 = self.memory_manager.get_reg_for_var(node.dest)
        if reg3 is None:
            instructions.append(mips.StoreWordNode(
                V0_REG, self.get_var_location(node.dest)))
        else:
            instructions.append(mips.MoveNode(reg3, V0_REG))

        return instructions

    @visitor.when(cil.TypeOfNode)
    def visit(self, node):
        instructions = []

        reg1 = self.memory_manager.get_reg_for_var(node.id)
        if reg1 is None:
            reg1 = ARG_REGISTERS[0]
            instructions.append(mips.LoadWordNode(
                reg1, self.get_var_location(node.id)))

        reg2 = self.memory_manager.get_reg_for_var(node.dest)
        if reg2 is None:
            instructions.append(mips.LoadWordNode(
                ARG_REGISTERS[1], RegisterRelativeLocation(reg1, 0)))
            instructions.append(mips.StoreWordNode(
                ARG_REGISTERS[1], self.get_var_location(node.dest)))
        else:
            instructions.append(mips.LoadWordNode(
                reg2, RegisterRelativeLocation(reg1, 0)))

        return instructions

    @visitor.when(cil.StaticCallNode)
    def visit(self, node):
        instructions = []
        label = self._name_func_map[node.function]
        instructions.append(mips.JumpAndLinkNode(label))

        reg = self.memory_manager.get_reg_for_var(node.dest)
        if reg is None:
            instructions.append(mips.StoreWordNode(
                V0_REG, self.get_var_location(node.dest)))
        else:
            instructions.append(mips.MoveNode(reg, V0_REG))

        if self._pushed_args > 0:
            instructions.append(mips.AddInmediateNode(
                SP_REG, SP_REG, self._pushed_args * 4))
            self.clean_pushed_args()
        return instructions

    @visitor.when(cil.DynamicCallNode)
    def visit(self, node):
        instructions = []

        comp_tp = self._types[node.computed_type]
        method_index = list(comp_tp.methods).index(node.function)
        reg = self.memory_manager.get_reg_for_var(node.type)
        if reg is None:
            reg = ARG_REGISTERS[0]
            instructions.append(mips.LoadWordNode(
                reg, self.get_var_location(node.type)))

        instructions.append(mips.LoadAddressNode(
            ARG_REGISTERS[1], "proto_table"))
        instructions.append(mips.ShiftLeftLogicalNode(
            ARG_REGISTERS[2], reg, 2))
        instructions.append(mips.AddUnsignedNode(
            ARG_REGISTERS[1], ARG_REGISTERS[1], ARG_REGISTERS[2]))
        instructions.append(mips.LoadWordNode(
            ARG_REGISTERS[1], RegisterRelativeLocation(ARG_REGISTERS[1], 0)))
        instructions.append(mips.LoadWordNode(
            ARG_REGISTERS[1], RegisterRelativeLocation(ARG_REGISTERS[1], 8)))
        instructions.append(mips.AddInmediateUnsignedNode(
            ARG_REGISTERS[1], ARG_REGISTERS[1], method_index * 4))
        instructions.append(mips.LoadWordNode(
            ARG_REGISTERS[1], RegisterRelativeLocation(ARG_REGISTERS[1], 0)))
        instructions.append(
            mips.JumpRegisterAndLinkNode(ARG_REGISTERS[1]))

        reg = self.memory_manager.get_reg_for_var(node.dest)
        if reg is None:
            instructions.append(mips.StoreWordNode(
                V0_REG, self.get_var_location(node.dest)))
        else:
            instructions.append(mips.MoveNode(reg, V0_REG))

        if self._pushed_args > 0:
            instructions.append(mips.AddInmediateNode(
                SP_REG, SP_REG, self._pushed_args * 4))
            self.clean_pushed_args()

        return instructions

    @visitor.when(cil.ArgNode)
    def visit(self, node):
        self.push_arg()
        instructions = []
        if type(node.id) == int:
            instructions.append(mips.LoadInmediateNode(
                ARG_REGISTERS[0], node.id))
            instructions.extend(push_register(ARG_REGISTERS[0]))
        else:
            reg = self.memory_manager.get_reg_for_var(node.id)
            if reg is None:
                reg = ARG_REGISTERS[0]
                instructions.append(mips.LoadWordNode(
                    reg, self.get_var_location(node.id)))
            instructions.extend(push_register(reg))
        return instructions

    @visitor.when(cil.IfGotoNode)
    def visit(self, node):
        instructions = []

        mips_label = self.get_mips_label(node.label)

        reg = self.memory_manager.get_reg_for_var(node.if_cond)
        if reg is None:
            reg = ARG_REGISTERS[0]
            instructions.append(mips.LoadWordNode(
                ARG_REGISTERS[0], self.get_var_location(node.if_cond)))

        instructions.append(mips.BranchOnNotEqualNode(
            reg, ZERO_REG, mips_label))

        return instructions

    @visitor.when(cil.LabelNode)
    def visit(self, node):
        return [mips.LabelNode(self.get_mips_label(node.label))]

    @visitor.when(cil.GotoNode)
    def visit(self, node):
        mips_label = self.get_mips_label(node.label)
        return [mips.JumpNode(mips_label)]

    @visitor.when(cil.ReturnNode)
    def visit(self, node):
        instructions = []

        if node.id is None:
            instructions.append(mips.LoadInmediateNode(V0_REG, 0))
        elif isinstance(node.id, int):
            instructions.append(
                mips.LoadInmediateNode(V0_REG, node.id))
        elif isinstance(node.id, cil.VoidNode):
            instructions.append(mips.LoadInmediateNode(V0_REG, 0))
        else:
            reg = self.memory_manager.get_reg_for_var(node.id)
            if reg is None:
                instructions.append(mips.LoadWordNode(
                    V0_REG, self.get_var_location(node.id)))
            else:
                instructions.append(mips.MoveNode(V0_REG, reg))
        return instructions

    @visitor.when(cil.LoadNode)
    def visit(self, node):
        instructions = []

        string_location = LabelRelativeLocation(
            self._data_section[node.msg.id].label, 0)
        reg = self.memory_manager.get_reg_for_var(node.dest)
        if reg is None:
            instructions.append(mips.LoadAddressNode(
                ARG_REGISTERS[0], string_location))
            instructions.append(mips.StoreWordNode(
                ARG_REGISTERS[0], self.get_var_location(node.dest)))
        else:
            instructions.append(mips.LoadAddressNode(reg, string_location))

        return instructions

    @visitor.when(cil.LengthNode)
    def visit(self, node):
        instructions = []

        reg = self.memory_manager.get_reg_for_var(node.id)
        if reg is None:
            reg = ARG_REGISTERS[0]
            instructions.append(mips.LoadWordNode(
                reg, self.get_var_location(node.id)))

        instructions.append(mips.MoveNode(ARG_REGISTERS[0], reg))
        instructions.append(mips.JumpAndLinkNode("len"))

        reg = self.memory_manager.get_reg_for_var(node.dest)
        if reg is None:
            instructions.append(mips.StoreWordNode(
                V0_REG, self.get_var_location(node.dest)))
        else:
            instructions.append(mips.MoveNode(reg, V0_REG))

        return instructions

    @visitor.when(cil.ConcatNode)
    def visit(self, node):
        instructions = []

        reg = self.memory_manager.get_reg_for_var(node.s1)
        if reg is None:
            instructions.append(mips.LoadWordNode(
                ARG_REGISTERS[0], self.get_var_location(node.s1)))
        else:
            instructions.append(mips.MoveNode(ARG_REGISTERS[0], reg))

        reg = self.memory_manager.get_reg_for_var(node.s2)
        if reg is None:
            instructions.append(mips.LoadWordNode(
                ARG_REGISTERS[1], self.get_var_location(node.s2)))
        else:
            instructions.append(mips.MoveNode(ARG_REGISTERS[1], reg))

        reg = self.memory_manager.get_reg_for_var(node.length)
        if reg is None:
            instructions.append(mips.LoadWordNode(
                ARG_REGISTERS[2], self.get_var_location(node.lenght)))
        else:
            instructions.append(mips.MoveNode(ARG_REGISTERS[2], reg))

        instructions.append(mips.JumpAndLinkNode("concat"))

        reg = self.memory_manager.get_reg_for_var(node.dest)
        if reg is None:
            instructions.append(mips.StoreWordNode(
                V0_REG, self.get_var_location(node.dest)))
        else:
            instructions.append(mips.MoveNode(reg, V0_REG))

        return instructions

    @visitor.when(cil.SubstringNode)
    def visit(self, node):
        instructions = []

        reg = self.memory_manager.get_reg_for_var(node.s)
        if reg is None:
            instructions.append(mips.LoadWordNode(
                ARG_REGISTERS[0], self.get_var_location(node.s)))
        else:
            instructions.append(mips.MoveNode(ARG_REGISTERS[0], reg))

        if type(node.i) == int:
            instructions.append(mips.LoadInmediateNode(
                ARG_REGISTERS[1], node.i))
        else:
            reg = self.memory_manager.get_reg_for_var(node.i)
            if reg is None:
                instructions.append(mips.LoadWordNode(
                    ARG_REGISTERS[1], self.get_var_location(node.i)))
            else:
                instructions.append(mips.MoveNode(ARG_REGISTERS[1], reg))

        if type(node.length) == int:
            instructions.append(mips.LoadInmediateNode(
                ARG_REGISTERS[2], node.length))
        else:
            reg = self.memory_manager.get_reg_for_var(node.length)
            if reg is None:
                instructions.append(mips.LoadWordNode(
                    ARG_REGISTERS[2], self.get_var_location(node.length)))
            else:
                instructions.append(mips.MoveNode(ARG_REGISTERS[2], reg))

        instructions.append(mips.JumpAndLinkNode("sub_string"))
        reg = self.memory_manager.get_reg_for_var(node.dest)
        if reg is None:
            instructions.append(mips.StoreWordNode(
                V0_REG, self.get_var_location(node.dest)))
        else:
            instructions.append(mips.MoveNode(reg, V0_REG))
        return instructions

    @visitor.when(cil.ReadStrNode)
    def visit(self, node):
        instructions = []
        instructions.append(mips.JumpAndLinkNode("get_string"))

        reg = self.memory_manager.get_reg_for_var(node.dest)
        if reg is None:
            instructions.append(mips.StoreWordNode(
                V0_REG, self.get_var_location(node.dest)))
        else:
            instructions.append(mips.MoveNode(reg, V0_REG))

        return instructions

    @visitor.when(cil.PrintStrNode)
    def visit(self, node):
        instructions = []
        instructions.append(mips.LoadInmediateNode(V0_REG, 4))

        reg = self.memory_manager.get_reg_for_var(node.value)
        if reg is None:
            instructions.append(mips.LoadWordNode(
                ARG_REGISTERS[0]. self.get_var_location(node.value)))
        else:
            instructions.append(mips.MoveNode(ARG_REGISTERS[0], reg))
        instructions.append(mips.SyscallNode())

        return instructions

    @visitor.when(cil.ErrorNode)
    def visit(self, node):
        instructions = []

        mips_label = self._data_section[node.data_node.id].label

        instructions.append(mips.LoadInmediateNode(V0_REG, 4))
        instructions.append(mips.LoadAddressNode(
            ARG_REGISTERS[0], mips_label))
        instructions.append(mips.SyscallNode())
        instructions.append(mips.LoadInmediateNode(V0_REG, 10))
        instructions.append(mips.SyscallNode())

        return instructions

    @visitor.when(cil.TypeNameNode)
    def visit(self, node):
        instructions = []

        reg1 = self.memory_manager.get_reg_for_var(node.type)
        pushed = False
        if reg1 is None:
            reg1 = self.memory_manager.get_reg_unusued()
            instructions.extend(push_register(reg1))
            instructions.append(mips.LoadWordNode(
                reg1, self.get_var_location(node.type)))
            pushed = True

        instructions.append(mips.LoadWordNode(
            ARG_REGISTERS[0], RegisterRelativeLocation(reg1, 0)))

        if pushed:
            instructions.extend(pop_register(reg1))

        instructions.append(mips.ShiftLeftLogicalNode(
            ARG_REGISTERS[0], ARG_REGISTERS[0], 2))
        instructions.append(mips.LoadAddressNode(
            ARG_REGISTERS[1], "type_name_table"))
        instructions.append(mips.AddUnsignedNode(
            ARG_REGISTERS[0], ARG_REGISTERS[0], ARG_REGISTERS[1]))
        instructions.append(mips.LoadWordNode(
            ARG_REGISTERS[0], RegisterRelativeLocation(ARG_REGISTERS[0], 0)))

        reg2 = self.memory_manager.get_reg_for_var(node.dest)
        if reg2 is None:
            instructions.append(mips.StoreWordNode(
                ARG_REGISTERS[0], self.get_var_location(node.dest)))
        else:
            instructions.append(mips.MoveNode(reg2, ARG_REGISTERS[0]))

        return instructions

    @visitor.when(cil.NameNode)
    def visit(self, node):
        instructions = []

        save = False
        reg = self.memory_manager.get_reg_for_var(node.dest)
        if reg is None:
            reg = ARG_REGISTERS[0]
            save = True

        instructions.append(mips.LoadAddressNode(
            reg, "type_name_table"))

        tp_number = self._types[node.id].index
        instructions.append(
            mips.AddInmediateUnsignedNode(reg, reg, tp_number*4))
        instructions.append(mips.LoadWordNode(
            reg, RegisterRelativeLocation(reg, 0)))

        if save:
            instructions.append(mips.StoreWordNode(
                reg, self.get_var_location(node.dest)))

        return instructions

    @visitor.when(cil.AbortNode)
    def visit(self, node):
        instructions = []
        instructions.append(mips.LoadInmediateNode(V0_REG, 10))
        instructions.append(mips.SyscallNode())

        return instructions

    @visitor.when(cil.CopyNode)
    def visit(self, node):
        instructions = []

        pushed = False
        reg = self.memory_manager.get_reg_for_var(node.copy)
        if reg is None:
            reg = self.memory_manager.get_reg_unusued()
            instructions.extend(push_register(reg))
            instructions.append(mips.LoadWordNode(
                reg, self.get_var_location(node.copy)))
            pushed = True

        instructions.extend(copy_object(reg, ARG_REGISTERS[3]))

        if pushed:
            instructions.extend(pop_register(reg))

        reg = self.memory_manager.get_reg_for_var(node.dest)
        if reg is None:
            instructions.append(mips.StoreWordNode(
                V0_REG, self.get_var_location(node.dest)))
        else:
            instructions.append(mips.MoveNode(reg, V0_REG))

        return instructions

    @visitor.when(cil.ReadIntNode)
    def visit(self, node):
        instructions = []

        instructions.append(mips.LoadInmediateNode(V0_REG, 5))
        instructions.append(mips.SyscallNode())
        reg = self.memory_manager.get_reg_for_var(node.dest)
        if reg is None:
            instructions.append(mips.StoreWordNode(
                V0_REG, self.get_var_location(node.dest)))
        else:
            instructions.append(mips.MoveNode(reg, V0_REG))

        return instructions

    @visitor.when(cil.PrintIntNode)
    def visit(self, node):
        instructions = []
        instructions.append(mips.LoadInmediateNode(V0_REG, 1))

        reg = self.memory_manager.get_reg_for_var(node.value)
        if reg is None:
            instructions.append(mips.LoadWordNode(
                ARG_REGISTERS[0], self.get_var_location(node.value)))
        else:
            instructions.append(mips.MoveNode(ARG_REGISTERS[0], reg))

        instructions.append(mips.SyscallNode())

        return instructions

    @visitor.when(cil.ComplementNode)
    def visit(self, node):
        instructions = []

        reg1 = None

        if type(node.id) == int:
            reg1 = ARG_REGISTERS[0]
            instructions.append(mips.LoadInmediateNode(reg1, node.id))
        else:
            reg1 = self.memory_manager.get_reg_for_var(node.id)
            if reg1 is None:
                reg1 = ARG_REGISTERS[0]
                instructions.append(mips.LoadWordNode(
                    reg1, self.get_var_location(node.id)))

        reg2 = self.memory_manager.get_reg_for_var(node.dest)
        if reg2 is None:
            reg2 = ARG_REGISTERS[1]
            instructions.append(mips.ComplementNode(reg2, reg1))
            instructions.append(mips.AddInmediateNode(reg2, reg2, 1))
            instructions.append(mips.StoreWordNode(
                reg2, self.get_var_location(node.dest)))
        else:
            instructions.append(mips.ComplementNode(reg2, reg1))
            instructions.append(mips.AddInmediateNode(reg2, reg2, 1))

        return instructions
