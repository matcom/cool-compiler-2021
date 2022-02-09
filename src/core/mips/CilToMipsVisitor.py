import core.cil.CILAst as cil
import core.mips.MipsAst as mips
from ..tools import visitor

class CILtoMIPSvisitor:
    def __init__(self):
        self.type_label_count = 0
        self.data_label_count = 0
        self.code_label_count = 0

        self._types_section = {}
        self._data_section = {}
        self._functions_section = {}

        self._current_function = None
        self._function_names = {}
        self._pushed_args = 0
        self._labels = {}

        self.registers = mips.REGISTERS

    def generate_type_label(self):
        self.type_label_count += 1
        return f'type_{self.type_label_count}'

    def generate_data_label(self):
        self.data_label_count += 1
        return f'data_{self.data_label_count}'

    def generate_code_label(self):
        self.code_label_count += 1
        return f'label_{self.code_label_count}'

    def enter_function(self, name, function):
        self._functions_section[name] = function
        self._current_function = function
        self._labels = {}

    def exit_function(self):
        self._current_function = None

    def get_free_register(self):
        r, rest = self.registers
        self.registers = rest
        return r

    def free_register(self, reg):
        self.registers.append(reg)

    def register_label(self, old_label, new_label):
        self._labels[old_label] = new_label

    def get_label(self, label):
        return self._labels[label]

    def get_var_location(self, name):
        return self._current_function.get_var_location(name)

    @visitor.on('node')
    def collect_func_names(self, node):
        pass

    @visitor.when(cil.ProgramNode)
    def collect_func_names(self, node):
        for f in node.dotcode:
            self.collect_func_names(f)

    @visitor.when(cil.FunctionNode)
    def collect_func_names(self, node):
        if node.name == "entry":
            self._function_names[node.name] = 'main'
        else:
            self._function_names[node.name] = self.generate_code_label()


    @visitor.on('node')
    def visit(self, node):
        pass

    @visitor.when(cil.ProgramNode)
    def visit(self, node):
        self.collect_func_names(node)
        self._data_section["default_str"] = mips.StringConst("default_str", "")

        for i in node.dottypes:
            self.visit(i)
        for i in node.dotdata:
            self.visit(i)
        for i in node.dotcode:
            self.visit(i)

        return mips.ProgramNode([i for i in self._data_section.values()],
                                [i for i in self._types_section.values()],
                                [i for i in self._functions_section.values()])

    @visitor.when(cil.TypeNode)
    def visit(self, node):
        name_label = self.generate_data_label()
        self._data_section[node.name] = mips.StringConst(name_label, node.name)

        type_label = self.generate_type_label()
        methods = {key: self._function_names[value] for key, value in node.methods}
        defaults = []
        if node.name == "String":
            defaults = [('value', 'default_str'), ('len', 'type_4_proto')]

        type = mips.MIPSType(type_label, name_label, node.attributes, methods,
                             len(self._types_section), defaults)
        self._types_section[node.name] = type

    @visitor.when(cil.DataNode)
    def visit(self, node):
        label = self.generate_data_label()
        self._data_section[node.name] = mips.StringConst(label, node.value)

    @visitor.when(cil.FunctionNode)
    def visit(self, node):
        raise NotImplementedError()

    @visitor.when(cil.ParamNode)
    def visit(self, node):
        raise NotImplementedError()

    @visitor.when(cil.LocalNode)
    def visit(self, node):
        raise NotImplementedError()

    @visitor.when(cil.AssignNode)
    def visit(self, node):
        instructions = []

        if isinstance(node.source, cil.VoidNode):
            reg1 = mips.ZERO_REG
        elif node.source.isnumeric():
            reg1 = mips.REGISTERS[0]
            instructions.append(mips.LoadInmediateNode(reg1, int(node.source)))
        else:
            reg1 = mips.REGISTERS[0]
            instructions.append(mips.LoadWordNode(reg1, self.get_var_location(node.source)))

        instructions.append(mips.StoreWordNode(reg1, self.get_var_location(node.dest)))
        return instructions

    @visitor.when(cil.PlusNode)
    def visit(self, node):
        instructions = []

        reg1 = mips.REGISTERS[0]
        if isinstance(node.left, int):
            instructions.append(mips.LoadInmediateNode(reg1,node.left))
        else:
            instructions.append(mips.LoadWordNode(reg1,self.get_var_location(node.left)))

        reg2 = mips.REGISTERS[1]
        if isinstance(node.right, int):
            instructions.append(mips.LoadInmediateNode(reg2, node.right))
        else:
            instructions.append(mips.LoadWordNode(reg2, self.get_var_location(node.right)))

        reg3 = mips.REGISTERS[0]
        instructions.append(mips.AdditionNode(reg3, reg1, reg2))
        instructions.append(mips.StoreWordNode(reg3, self.get_var_location(node.dest)))

        return instructions

    @visitor.when(cil.MinusNode)
    def visit(self, node):
        instructions = []

        reg1 = mips.REGISTERS[0]
        if isinstance(node.left, int):
            instructions.append(mips.LoadInmediateNode(reg1, node.left))
        else:
            instructions.append(mips.LoadWordNode(reg1, self.get_var_location(node.left)))

        reg2 = mips.REGISTERS[1]
        if isinstance(node.right, int):
            instructions.append(mips.LoadInmediateNode(reg2, node.right))
        else:
            instructions.append(mips.LoadWordNode(reg2, self.get_var_location(node.right)))

        reg3 = mips.REGISTERS[0]
        instructions.append(mips.SubstractionNode(reg3, reg1, reg2))
        instructions.append(mips.StoreWordNode(reg3, self.get_var_location(node.dest)))

        return instructions

    @visitor.when(cil.StarNode)
    def visit(self, node):
        instructions = []

        reg1 = mips.REGISTERS[0]
        if isinstance(node.left, int):
            instructions.append(mips.LoadInmediateNode(reg1, node.left))
        else:
            instructions.append(mips.LoadWordNode(reg1, self.get_var_location(node.left)))

        reg2 = mips.REGISTERS[1]
        if isinstance(node.right, int):
            instructions.append(mips.LoadInmediateNode(reg2, node.right))
        else:
            instructions.append(mips.LoadWordNode(reg2, self.get_var_location(node.right)))

        reg3 = mips.REGISTERS[0]
        instructions.append(mips.MultiplyNode(reg3, reg1, reg2))
        instructions.append(mips.StoreWordNode(reg3, self.get_var_location(node.dest)))

        return instructions

    @visitor.when(cil.DivNode)
    def visit(self, node):
        instructions = []

        reg1 = mips.REGISTERS[0]
        if isinstance(node.left, int):
            instructions.append(mips.LoadInmediateNode(reg1, node.left))
        else:
            instructions.append(mips.LoadWordNode(reg1, self.get_var_location(node.left)))

        reg2 = mips.REGISTERS[1]
        if isinstance(node.right, int):
            instructions.append(mips.LoadInmediateNode(reg2, node.right))
        else:
            instructions.append(mips.LoadWordNode(reg2, self.get_var_location(node.right)))

        reg3 = mips.LOW_REG
        instructions.append(mips.DivideNode(reg1, reg2))
        instructions.append(mips.StoreWordNode(reg3, self.get_var_location(node.dest)))

        return instructions

    @visitor.when(cil.AllocateNode)
    def visit(self, node):
        instructions = []

        if isinstance(node.type, int):
            type = node.type
        else:
            type = self._types_section[node.type].index

        reg1 = mips.REGISTERS[0]
        reg2 = mips.REGISTERS[1]

        instructions.append(mips.LoadInmediateNode(reg1, type))
        instructions.append(mips.ShiftLeftLogicalNode(reg1, reg2, 2))
        instructions.append(mips.LoadAddressNode(reg2, mips.PROTO_TABLE_LABEL))
        instructions.append(mips.AdditionNode(reg2, reg2, reg1))
        instructions.append(mips.LoadWordNode(reg2, mips.RegisterRelativeLocation(reg2, 0)))
        reg3 = mips.ARG_REGISTERS[0]
        instructions.append(mips.LoadWordNode(reg3, mips.RegisterRelativeLocation(reg2, 4)))
        instructions.append(mips.ShiftLeftLogicalNode(reg3, reg3, 2))
        instructions.append(mips.JalNode('malloc'))
        instructions.append(mips.MoveNode(mips.ARG_REGISTERS[2], reg3))
        instructions.append(mips.MoveNode(reg3, reg2))
        instructions.append(mips.MoveNode(mips.ARG_REGISTERS[1], mips.V0_REG))
        instructions.append(mips.JalNode('copy'))

        instructions.append(mips.StoreWordNode(mips.V0_REG, self.get_var_location(node.dest)))

        return instructions

    @visitor.when(cil.TypeOfNode)
    def visit(self, node):
        instructions = []

        reg1 = mips.REGISTERS[0]
        reg2 = mips.REGISTERS[1]

        instructions.append(mips.LoadWordNode(reg1, self.get_var_location(node.obj)))
        instructions.append(mips.LoadWordNode(reg2, mips.RegisterRelativeLocation(reg1, 0)))
        instructions.append(mips.StoreWordNode(reg2, self.get_var_location(node.dest)))

        return instructions

    @visitor.when(cil.StaticCallNode)
    def visit(self, node):
        instructions = []
        func_name = self._function_names[node.function]
        instructions.append(mips.JalNode(func_name))

        instructions.append(mips.StoreWordNode(mips.V0_REG, self.get_var_location(node.dest)))
        if self._pushed_args > 0:
            instructions.append(mips.AdditionInmediateNode(mips.SP_REG, mips.SP_REG, self._pushed_args * mips.DOUBLE_WORD))
            self._pushed_args = 0

        return instructions
    '''
    @visitor.when(cil.DynamicCallNode)
    def visit(self, node):
        instructions = []

        type = self._types_section[node.type]
        method = type.methods.index(node.method)

        reg = mips.REGISTERS[0]
        instructions.append(mips.LoadWordNode(reg, self.get_var_location(node.type)))
        instructions.append(mips.LoadAddressNode(mips.ARG_REGISTERS[1], mips.PROTO_TABLE_LABEL))
        instructions.append(mips.ShiftLeftLogicalNode(mips.ARG_REGISTERS[2], reg, 2))
        instructions.append(mips.AddUnsignedNode(mips.ARG_REGISTERS[1], mips.ARG_REGISTERS[1], mips.ARG_REGISTERS[2]))
        instructions.append(
            mips.LoadWordNode(mips.ARG_REGISTERS[1], mips.RegisterRelativeLocation(mips.ARG_REGISTERS[1], 0)))
        instructions.append(
            mips.LoadWordNode(mips.ARG_REGISTERS[1], mips.RegisterRelativeLocation(mips.ARG_REGISTERS[1], 8)))
        instructions.append(
            mips.AddInmediateUnsignedNode(mips.ARG_REGISTERS[1], mips.ARG_REGISTERS[1], method_index * 4))
        instructions.append(
            mips.LoadWordNode(mips.ARG_REGISTERS[1], mips.RegisterRelativeLocation(mips.ARG_REGISTERS[1], 0)))
        instructions.append(mips.JumpRegisterAndLinkNode(mips.ARG_REGISTERS[1]))
    '''

    @visitor.when(cil.ArgNode)
    def visit(self, node):
        self._pushed_args += 1
        instructions = []
        reg = mips.REGISTERS[0]
        if isinstance(node.name, int):
            instructions.append(mips.LoadInmediateNode(mips.ARG_REGISTERS[0], node.name))
        else:
            instructions.append(mips.LoadWordNode(reg, self.get_var_location(node.name)))
        instructions.extend(mips.push_register(reg))
        return instructions

    @visitor.when(cil.ReturnNode)
    def visit(self, node):
        instructions = []

        if node.value is None or isinstance(node.value, cil.VoidNode):
            instructions.append(mips.LoadInmediateNode(mips.V0_REG, 0))
        elif isinstance(node.value, int):
            instructions.append(mips.LoadInmediateNode(mips.V0_REG, node.value))
        else:
            instructions.append(mips.LoadWordNode(mips.V0_REG, self.get_var_location(node.value)))
        return instructions

    @visitor.when(cil.LoadNode)
    def visit(self, node):
        instructions = []

        string = mips.LabelRelativeLocation(self._data_section[node.msg.name].label, 0)
        reg = mips.REGISTERS[0]

        instructions.append(mips.LoadAddressNode(reg, string))

        return instructions

    '''
    @visitor.when(cil.PrintStringNode)
    def visit(self, node: cil.PrintStringNode):
        instructions = []
        reg = mips.REGISTERS[0]
        instructions.append(mips.MoveNode(reg, self.get_var_location(node.str_addr)))
        instructions.append(mips.SyscallNode())

        return instructions
    '''

    '''
    @visitor.when(PrintIntNode)
    def visit(self, node: PrintIntNode):
        instructions = []
        instructions.append(mips.LoadInmediateNode(mips.V0_REG, 1))

        reg = self.memory_manager.get_reg_for_var(node.value)
        if reg is None:
            instructions.append(mips.LoadWordNode(mips.ARG_REGISTERS[0], self.get_var_location(node.value)))
        else:
            instructions.append(mips.MoveNode(mips.ARG_REGISTERS[0], reg))

        instructions.append(mips.SyscallNode())

        return instructions
    '''

    @visitor.when(cil.ExitNode)
    def visit(self, node: cil.ExitNode):
        instructions = []
        instructions.append(mips.ExitNode())
        return instructions

    '''
    @visitor.when(cil.CopyNode)
    def visit(self, node):
        instructions = []

        reg = mips.REGISTERS[0]
        instructions.append(mips.LoadWordNode(reg, self.get_var_location(node.source)))
        instructions.append(mips.LoadWordNode(mips.ARG_REGISTERS[0], mips.RegisterRelativeLocation(reg, 4)))
        instructions.append(mips.ShiftLeftLogicalNode(mips.ARG_REGISTERS[0], mips.ARG_REGISTERS[0], 2))
        instructions.append(mips.JalNode("malloc"))
        instructions.append(mips.MoveNode(mips.ARG_REGISTERS[2], mips.ARG_REGISTERS[0]))
        instructions.append(mips.MoveNode(mips.ARG_REGISTERS[0], reg))
        instructions.append(mips.MoveNode(mips.ARG_REGISTERS[1], mips.V0_REG))
        instructions.append(mips.JalNode("copy"))

        if pushed:
            instructions.extend(mips.pop_register(reg))

        reg = self.memory_manager.get_reg_for_var(node.dest)
        if reg is None:
            instructions.append(mips.StoreWordNode(mips.V0_REG, self.get_var_location(node.dest)))
        else:
            instructions.append(mips.MoveNode(reg, mips.V0_REG))

        return instructions
    '''

    @visitor.when(cil.GetAttribNode)
    def visit(self, node: cil.GetAttribNode):
        instructions = []

        reg1 = mips.REGISTERS[0]
        reg2 = mips.REGISTERS[1]
        instructions.append(mips.LoadWordNode(reg1, self.get_var_location(node.obj)))

        tp = self._types_section[node.computed_type]
        offset = (tp.attributes.index(node.attr) + 3) * mips.DOUBLE_WORD
        instructions.append(mips.LoadWordNode(reg2, mips.RegisterRelativeLocation(reg1, offset)))
        instructions.append(mips.StoreWordNode(reg2, self.get_var_location(node.dest)))

        return instructions

    '''
    @visitor.when(cil.ErrorNode)
    def visit(self, node: cil.ErrorNode):
        instructions = []

        mips_label = self._data_section[node.data.name].label

        instructions.append(mips.LoadInmediateNode(mips.V0_REG, 4))
        instructions.append(mips.LoadAddressNode(mips.ARG_REGISTERS[0], mips_label))
        instructions.append(mips.SyscallNode())
        instructions.append(mips.LoadInmediateNode(mips.V0_REG, 10))
        instructions.append(mips.SyscallNode())

        return instructions
    '''

    '''
    @visitor.when(cil.ReadNode)
    def visit(self, node: cil.ReadNode):
        instructions = []

        instructions.append(mips.LoadInmediateNode(mips.V0_REG, 5))
        instructions.append(mips.SyscallNode())
        reg = self.memory_manager.get_reg_for_var(node.dest)
        if reg is None:
            instructions.append(mips.StoreWordNode(mips.V0_REG, self.get_var_location(node.dest)))
        else:
            instructions.append(mips.MoveNode(reg, mips.V0_REG))

        return instructions
    '''

    @visitor.when(cil.SetAttribNode)
    def visit(self, node: cil.SetAttribNode):
        instructions = []

        tp = self._types_section[node.computed_type]
        offset = (tp.attributes.index(node.attr) + 3) * mips.DOUBLE_WORD

        reg1 = mips.REGISTERS[0]
        instructions.append(mips.LoadWordNode(reg1, self.get_var_location(node.obj)))

        reg2 = mips.REGISTERS[1]
        if type(node.value) == int:
            instructions.append(mips.LoadInmediateNode(reg2, node.value))
        else:
            instructions.append(mips.LoadWordNode(reg2, self.get_var_location(node.value)))

        instructions.append(mips.StoreWordNode(reg2, mips.RegisterRelativeLocation(reg1, offset)))
        return instructions

    @visitor.when(cil.LessNode)
    def visit(self, node: cil.LessNode):
        instructions = []

        reg1 = mips.REGISTERS[0]
        instructions.append(mips.LoadWordNode(reg1, self.get_var_location(node.left)))

        reg2 = mips.REGISTERS[1]
        instructions.append(mips.LoadWordNode(reg2, self.get_var_location(node.right)))
        instructions.append(mips.LessNode(reg2, reg1, reg2))
        instructions.append(mips.StoreWordNode(reg2, self.get_var_location(node.dest)))

        return instructions

    @visitor.when(cil.GotoIfNode)
    def visit(self, node: cil.GotoIfNode):
        instructions = []
        mips_label = self.get_label(node.label)

        reg1 = mips.REGISTERS[0]
        instructions.append(mips.LoadWordNode(reg1, self.get_var_location(node.condition)))
        instructions.append(mips.BranchOnNotEqualNode(reg1, mips.ZERO_REG, mips_label))

        return instructions

    @visitor.when(cil.GotoNode)
    def visit(self, node: cil.GotoNode):
        mips_label = self.get_label(node.label)
        return [mips.JumpNode(mips_label)]

    @visitor.when(cil.LabelNode)
    def visit(self, node: cil.LabelNode):
        return [mips.LabelNode(self.get_label(node.label))]

    @visitor.when(cil.SubstringNode)
    def visit(self, node: cil.SubstringNode):
        instructions = []

        reg1 = mips.REGISTERS[0]
        instructions.append(mips.LoadWordNode(reg1, self.get_var_location(node.str_value)))
        instructions.extend(mips.push_register(reg1))

        if type(node.index) == int:
            instructions.append(mips.LoadInmediateNode(reg1, node.index))
        else:
            instructions.append(mips.LoadWordNode(reg1, self.get_var_location(node.index)))
        instructions.extend(mips.push_register(reg1))

        if type(node.index) == int:
            instructions.append(mips.LoadInmediateNode(reg1, node.length))
        else:
            instructions.append(mips.LoadWordNode(reg1, self.get_var_location(node.length)))
        instructions.extend(mips.push_register(reg1))

        instructions.append(mips.JalNode("substr"))
        instructions.append(mips.StoreWordNode(mips.V0_REG, self.get_var_location(node.dest)))
        return instructions

    @visitor.when(cil.ConcatNode)
    def visit(self, node: cil.ConcatNode):
        instructions = []

        reg = mips.REGISTERS[0]
        instructions.append(mips.LoadWordNode(reg, self.get_var_location(node.prefix)))
        instructions.extend(mips.push_register(reg))

        instructions.append(mips.LoadWordNode(reg, self.get_var_location(node.suffix)))
        instructions.extend(mips.push_register(reg))

        instructions.append(mips.LoadWordNode(reg, self.get_var_location(node.suffix)))
        instructions.extend(mips.push_register(reg))

        instructions.append(mips.JalNode("concat"))
        instructions.append(mips.StoreWordNode(mips.V0_REG, self.get_var_location(node.dest)))
        return instructions

    @visitor.when(cil.LengthNode)
    def visit(self, node: cil.LengthNode):
        instructions = []

        reg = mips.REGISTERS[0]
        instructions.append(mips.LoadWordNode(reg, self.get_var_location(node.source)))
        instructions.append(mips.push_register(reg))

        instructions.append(mips.JalNode("len"))
        instructions.append(mips.StoreWordNode(mips.V0_REG, self.get_var_location(node.dest)))

        return instructions

    @visitor.when(cil.EqualNode)
    def visit(self, node: cil.EqualNode):
        instructions = []

        reg1 = mips.REGISTERS[0]
        if type(node.left) == cil.VoidNode:
            instructions.append(mips.LoadInmediateNode(reg1, 0))
        else:
            instructions.append(mips.LoadWordNode(reg1, self.get_var_location(node.left)))

        reg2 = mips.REGISTERS[0]
        if type(node.left) == cil.VoidNode:
            instructions.append(mips.LoadInmediateNode(reg2, 0))
        else:
            instructions.append(mips.LoadWordNode(reg2, self.get_var_location(node.left)))

        instructions.append(mips.EqualNode(reg1, reg1, reg2))
        instructions.append(mips.StoreWordNode(reg1, self.get_var_location(node.dest)))
        return instructions

    @visitor.when(cil.NameNode)
    def visit(self, node: cil.NameNode):
        instructions = []

        reg = mips.REGISTERS[0]
        instructions.append(mips.LoadAddressNode(reg, mips.TYPENAMES_TABLE_LABEL))

        tp_number = self._types_section[node.value].index
        instructions.append(mips.AdditionInmediateNode(reg, reg, tp_number * 4))
        instructions.append(mips.LoadWordNode(reg, mips.RegisterRelativeLocation(reg, 0)))

        instructions.append(mips.StoreWordNode(reg, self.get_var_location(node.dest)))
        return instructions

    @visitor.when(cil.EqualStringNode)
    def visit(self, node: cil.EqualStringNode):
        instructions = []

        reg1 = mips.REGISTERS[0]
        instructions.append(mips.LoadWordNode(reg1, self.get_var_location(node.left)))
        instructions.extend(mips.push_register(reg1))

        instructions.append(mips.LoadWordNode(reg1, self.get_var_location(node.right)))
        instructions.extend(mips.push_register(reg1))

        instructions.append(mips.JalNode("equal_str"))
        instructions.append(mips.StoreWordNode(mips.V0_REG, self.get_var_location(node.dest)))

        return instructions

    @visitor.when(cil.ComplementNode)
    def visit(self, node: cil.ComplementNode):
        instructions = []

        reg1 = mips.REGISTERS[0]
        instructions.append(mips.LoadWordNode(reg1, self.get_var_location(node.value)))

        instructions.append(mips.NotNode(reg1, reg1))
        instructions.append(mips.AdditionInmediateNode(reg1, reg1, 1))
        instructions.append(mips.StoreWordNode(reg1, self.get_var_location(node.dest)))

        return instructions

    @visitor.when(cil.LessEqualNode)
    def visit(self, node: cil.LessEqualNode):
        instructions = []

        reg1 = mips.REGISTERS[0]
        instructions.append(mips.LoadWordNode(reg1, self.get_var_location(node.left)))

        reg2 = mips.REGISTERS[0]
        instructions.append(mips.LoadWordNode(reg2, self.get_var_location(node.right)))

        instructions.append(mips.LessEqualNode(reg1, reg1, reg2))
        instructions.append(mips.StoreWordNode(reg1, self.get_var_location(node.dest)))
        return instructions

    '''
    @visitor.when(PrefixNode)
    def visit(self, node: PrefixNode):
        return f'PREFFIXNODE'

    @visitor.when(ToStrNode)
    def visit(self, node: ToStrNode):
        return f'{node.dest} = str({node.value})'

    @visitor.when(VoidNode)
    def visit(self, node: VoidNode):
        return 'VOID'
    '''

    @visitor.when(cil.NotNode)
    def visit(self, node: cil.NotNode):
        instructions = []

        reg1 = mips.REGISTERS[0]
        instructions.append(mips.LoadWordNode(reg1, self.get_var_location(node.value)))
        instructions.append(mips.NotNode(reg1, reg1))
        instructions.append(mips.StoreWordNode(reg1, self.get_var_location(node.dest)))

        return instructions



