import core.cil.CilAst as cil
import core.mips.MipsAst as mips
from ..tools import visitor


class CILToMIPSVisitor:
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

    def get_var_location(self, node):
        if isinstance(node, cil.AttributeNode):
            return mips.RegisterRelativeLocation(mips.SP_REG, 0)
        if isinstance(node, str):
            return self._current_function.get_var_location(node)
        return self._current_function.get_var_location(node.name)

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
            self._function_names[node.name] = node.name

    @visitor.on('node')
    def visit(self, node):
        pass

    @visitor.when(cil.ProgramNode)
    def visit(self, node):
        self.collect_func_names(node)
        self._data_section["default_str"] = mips.StringConst("default_str", "", line=node.line, column=node.column)

        for i in node.dottypes:
            self.visit(i)
        for i in node.dotdata:
            self.visit(i)
        for i in node.dotcode:
            self.visit(i)

        return mips.ProgramNode([i for i in self._data_section.values()],
                                [i for i in self._types_section.values()],
                                [i for i in self._functions_section.values()],
                                line=node.line, column=node.column)

    @visitor.when(cil.TypeNode)
    def visit(self, node):
        name_label = self.generate_data_label()
        self._data_section[node.name] = mips.StringConst(name_label, node.name, line=node.line, column=node.column)

        type_label = self.generate_type_label()
        methods = [self._function_names[key] for key in node.methods.values()]
        defaults = []
        if node.name == "String":
            defaults = [('value', 'default_str'), ('len', 'type_4_proto')]

        type = mips.MIPSType(type_label, name_label, list(node.attributes.keys()), methods,
                             len(self._types_section), defaults)
        self._types_section[node.name] = type

    @visitor.when(cil.DataNode)
    def visit(self, node):
        label = self.generate_data_label()
        self._data_section[node.name] = mips.StringConst(label, node.value, line=node.line, column=node.column)

    @visitor.when(cil.FunctionNode)
    def visit(self, node):
        label = self._function_names[node.name]
        params = [param.name for param in node.params]
        localvars = [local.name for local in node.localvars]
        size_for_locals = len(localvars) * mips.DOUBLE_WORD

        new_func = mips.FunctionNode(label, params, localvars, line=node.line, column=node.column)
        self.enter_function(node.name, new_func)
        self._current_function = new_func
        self._labels = {}

        for instruction in node.instructions:
            if isinstance(instruction, cil.LabelNode):
                mips_label = self.generate_code_label()
                self.register_label(instruction.label, mips_label)

        instructions = []
        instructions.extend(mips.push_register(mips.RA_REG, node.line, node.column))
        instructions.extend(mips.push_register(mips.FP_REG, line=node.line, column=node.column))
        instructions.append(mips.AdditionInmediateNode(mips.FP_REG, mips.SP_REG, 8, line=node.line, column=node.column))
        instructions.append(mips.AdditionInmediateNode(mips.SP_REG, mips.SP_REG, -size_for_locals,
                                                       line=node.line, column=node.column))

        for i in node.instructions:
            instructions.extend(self.visit(i))

        instructions.append(mips.AdditionInmediateNode(mips.SP_REG, mips.SP_REG, size_for_locals,
                                                       line=node.line, column=node.column))
        instructions.extend(mips.pop_register(mips.FP_REG, line=node.line, column=node.column))
        instructions.extend(mips.pop_register(mips.RA_REG, node.line, node.column))

        if self._current_function.label != 'main':
            instructions.append(mips.JumpRegisterNode(mips.RA_REG, line=node.line, column=node.column))
        else:
            instructions.append(mips.LoadInmediateNode(mips.V0_REG, 10, line=node.line, column=node.column))
            instructions.append(mips.SyscallNode())

        new_func.instructions = instructions
        self._current_function = None

    @visitor.when(cil.AssignNode)
    def visit(self, node):
        instructions = []

        if isinstance(node.source, cil.VoidNode):
            reg1 = mips.ZERO_REG
        elif isinstance(node.source, int):
            reg1 = mips.REGISTERS[0]
            instructions.append(mips.LoadInmediateNode(reg1, int(node.source), line=node.line, column=node.column))
        else:
            reg1 = mips.REGISTERS[0]
            instructions.extend(self.visit(node.source))
            instructions.append(mips.LoadWordNode(reg1, self.get_var_location(node.source),
                                                  line=node.line, column=node.column))
            if isinstance(node.source, cil.AttributeNode):
                instructions.append(mips.AdditionInmediateNode(mips.SP_REG, mips.SP_REG, 4,
                                                               node.line, node.column))

        if isinstance(node.dest, cil.AttributeNode):
            self_var = self._current_function.params[0]
            reg2 = mips.REGISTERS[1]
            instructions.append(mips.LoadWordNode(reg2, self.get_var_location(self_var), node.line, node.column))

            index = self._types_section[node.dest.type].attributes.index(node.dest.name) + 3
            instructions.append(mips.AdditionInmediateNode(reg2, reg2, index * 4,
                                                  line=node.line, column=node.column))
            instructions.append(mips.StoreWordNode(reg1, mips.RegisterRelativeLocation(reg2, 0),
                                                   line=node.line, column=node.column))
        else:
            instructions.append(mips.StoreWordNode(reg1, self.get_var_location(node.dest),
                                                   line=node.line, column=node.column))

        return instructions

    @visitor.when(cil.PlusNode)
    def visit(self, node):
        instructions = []

        reg1 = mips.REGISTERS[0]
        if isinstance(node.left, int):
            instructions.append(mips.LoadInmediateNode(reg1, node.left, line=node.line, column=node.column))
        else:
            instructions.extend(self.visit(node.left))
            instructions.append(mips.LoadWordNode(reg1, self.get_var_location(node.left),
                                                  line=node.line, column=node.column))
            if isinstance(node.left, cil.AttributeNode):
                instructions.append(mips.AdditionInmediateNode(mips.SP_REG, mips.SP_REG, 4,
                                                               node.line, node.column))

        reg2 = mips.REGISTERS[1]
        if isinstance(node.right, int):
            instructions.append(mips.LoadInmediateNode(reg2, node.right, line=node.line, column=node.column))
        else:
            instructions.extend(self.visit(node.right))
            instructions.append(mips.LoadWordNode(reg2, self.get_var_location(node.right),
                                                  line=node.line, column=node.column))
            if isinstance(node.right, cil.AttributeNode):
                instructions.append(mips.AdditionInmediateNode(mips.SP_REG, mips.SP_REG, 4,
                                                               node.line, node.column))

        reg3 = mips.REGISTERS[0]
        instructions.append(mips.AdditionNode(reg3, reg1, reg2, line=node.line, column=node.column))
        instructions.extend(self.visit(node.dest))
        instructions.append(mips.StoreWordNode(reg3, self.get_var_location(node.dest),
                                               line=node.line, column=node.column))
        if isinstance(node.dest, cil.AttributeNode):
            instructions.append(mips.AdditionInmediateNode(mips.SP_REG, mips.SP_REG, 4,
                                                           node.line, node.column))

        return instructions

    @visitor.when(cil.MinusNode)
    def visit(self, node):
        instructions = []

        reg1 = mips.REGISTERS[0]
        if isinstance(node.left, int):
            instructions.append(mips.LoadInmediateNode(reg1, node.left, line=node.line, column=node.column))
        else:
            instructions.extend(self.visit(node.left))
            instructions.append(mips.LoadWordNode(reg1, self.get_var_location(node.left),
                                                  line=node.line, column=node.column))
            if isinstance(node.left, cil.AttributeNode):
                instructions.append(mips.AdditionInmediateNode(mips.SP_REG, mips.SP_REG, 4,
                                                               node.line, node.column))

        reg2 = mips.REGISTERS[1]
        if isinstance(node.right, int):
            instructions.append(mips.LoadInmediateNode(reg2, node.right, line=node.line, column=node.column))
        else:
            instructions.extend(self.visit(node.right))
            instructions.append(mips.LoadWordNode(reg2, self.get_var_location(node.right),
                                                  line=node.line, column=node.column))
            if isinstance(node.right, cil.AttributeNode):
                instructions.append(mips.AdditionInmediateNode(mips.SP_REG, mips.SP_REG, 4,
                                                               node.line, node.column))

        reg3 = mips.REGISTERS[0]
        instructions.append(mips.SubstractionNode(reg3, reg1, reg2, line=node.line, column=node.column))
        instructions.extend(self.visit(node.dest))
        instructions.append(mips.StoreWordNode(reg3, self.get_var_location(node.dest),
                                               line=node.line, column=node.column))
        if isinstance(node.dest, cil.AttributeNode):
            instructions.append(mips.AdditionInmediateNode(mips.SP_REG, mips.SP_REG, 4,
                                                           node.line, node.column))

        return instructions

    @visitor.when(cil.StarNode)
    def visit(self, node):
        instructions = []

        reg1 = mips.REGISTERS[0]
        if isinstance(node.left, int):
            instructions.append(mips.LoadInmediateNode(reg1, node.left, line=node.line, column=node.column))
        else:
            instructions.extend(self.visit(node.left))
            instructions.append(mips.LoadWordNode(reg1, self.get_var_location(node.left),
                                                  line=node.line, column=node.column))
            if isinstance(node.left, cil.AttributeNode):
                instructions.append(mips.AdditionInmediateNode(mips.SP_REG, mips.SP_REG, 4,
                                                               node.line, node.column))

        reg2 = mips.REGISTERS[1]
        if isinstance(node.right, int):
            instructions.append(mips.LoadInmediateNode(reg2, node.right, line=node.line, column=node.column))
        else:
            instructions.extend(self.visit(node.right))
            instructions.append(mips.LoadWordNode(reg2, self.get_var_location(node.right),
                                                  line=node.line, column=node.column))
            if isinstance(node.right, cil.AttributeNode):
                instructions.append(mips.AdditionInmediateNode(mips.SP_REG, mips.SP_REG, 4,
                                                               node.line, node.column))

        reg3 = mips.REGISTERS[0]
        instructions.append(mips.MultiplyNode(reg3, reg1, reg2, line=node.line, column=node.column))
        instructions.extend(self.visit(node.dest))
        instructions.append(mips.StoreWordNode(reg3, self.get_var_location(node.dest),
                                               line=node.line, column=node.column))
        if isinstance(node.dest, cil.AttributeNode):
            instructions.append(mips.AdditionInmediateNode(mips.SP_REG, mips.SP_REG, 4,
                                                           node.line, node.column))

        return instructions

    @visitor.when(cil.DivNode)
    def visit(self, node):
        instructions = []

        reg1 = mips.REGISTERS[0]
        if isinstance(node.left, int):
            instructions.append(mips.LoadInmediateNode(reg1, node.left, line=node.line, column=node.column))
        else:
            instructions.extend(self.visit(node.left))
            instructions.append(mips.LoadWordNode(reg1, self.get_var_location(node.left),
                                                  line=node.line, column=node.column))
            if isinstance(node.left, cil.AttributeNode):
                instructions.append(mips.AdditionInmediateNode(mips.SP_REG, mips.SP_REG, 4,
                                                               node.line, node.column))

        reg2 = mips.REGISTERS[1]
        if isinstance(node.right, int):
            instructions.append(mips.LoadInmediateNode(reg2, node.right, line=node.line, column=node.column))
        else:
            instructions.extend(self.visit(node.right))
            instructions.append(mips.LoadWordNode(reg2, self.get_var_location(node.right),
                                                  line=node.line, column=node.column))
            if isinstance(node.right, cil.AttributeNode):
                instructions.append(mips.AdditionInmediateNode(mips.SP_REG, mips.SP_REG, 4,
                                                               node.line, node.column))

        instructions.append(mips.DivideNode(reg1, reg2, line=node.line, column=node.column))
        instructions.append(mips.MoveLowNode(reg1, line=node.line, column=node.column))
        instructions.extend(self.visit(node.dest))
        instructions.append(mips.StoreWordNode(reg1, self.get_var_location(node.dest),
                                               line=node.line, column=node.column))
        if isinstance(node.dest, cil.AttributeNode):
            instructions.append(mips.AdditionInmediateNode(mips.SP_REG, mips.SP_REG, 4,
                                                           node.line, node.column))

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

        instructions.append(mips.LoadInmediateNode(reg1, type, line=node.line, column=node.column))
        instructions.extend(mips.create_object(reg1, reg2, line=node.line, column=node.column))
        instructions.extend(self.visit(node.dest))
        instructions.append(mips.StoreWordNode(mips.V0_REG, self.get_var_location(node.dest),
                                               line=node.line, column=node.column))
        if isinstance(node.dest, cil.AttributeNode):
            instructions.append(mips.AdditionInmediateNode(mips.SP_REG, mips.SP_REG, 4,
                                                           node.line, node.column))

        return instructions

    @visitor.when(cil.TypeOfNode)
    def visit(self, node):
        instructions = []

        reg1 = mips.REGISTERS[0]
        reg2 = mips.REGISTERS[1]

        instructions.extend(self.visit(node.obj))
        instructions.append(mips.LoadWordNode(reg1, self.get_var_location(node.obj),
                                              line=node.line, column=node.column))
        if isinstance(node.obj, cil.AttributeNode):
            instructions.append(mips.AdditionInmediateNode(mips.SP_REG, mips.SP_REG, 4,
                                                           node.line, node.column))
        instructions.append(mips.LoadWordNode(reg2, mips.RegisterRelativeLocation(reg1, 0),
                                              line=node.line, column=node.column))
        instructions.append(mips.ShiftLeftNode(reg2, reg2, 2, node.line, node.column))
        instructions.append(mips.LoadAddressNode(reg1, mips.TYPES_LABEL, node.line, node.column))
        instructions.append(mips.AdditionNode(reg1, reg1, reg2, node.line, node.column))
        instructions.append(mips.LoadWordNode(reg2, mips.RegisterRelativeLocation(reg1, 0),
                                              line=node.line, column=node.column))
        instructions.extend(self.visit(node.dest))
        instructions.append(mips.StoreWordNode(reg2, self.get_var_location(node.dest),
                                               line=node.line, column=node.column))
        if isinstance(node.dest, cil.AttributeNode):
            instructions.append(mips.AdditionInmediateNode(mips.SP_REG, mips.SP_REG, 4,
                                                           node.line, node.column))

        return instructions

    @visitor.when(cil.StaticCallNode)
    def visit(self, node):
        instructions = []
        func_name = self._function_names[node.function]
        instructions.append(mips.JalNode(func_name, line=node.line, column=node.column))

        if self._pushed_args > 0:
            instructions.append(mips.AdditionInmediateNode(mips.SP_REG, mips.SP_REG,
                                                           self._pushed_args * mips.DOUBLE_WORD,
                                                           line=node.line, column=node.column))
            self._pushed_args = 0
        instructions.extend(self.visit(node.dest))
        instructions.append(mips.StoreWordNode(mips.V0_REG, self.get_var_location(node.dest),
                                               line=node.line, column=node.column))
        if isinstance(node.dest, cil.AttributeNode):
            instructions.append(mips.AdditionInmediateNode(mips.SP_REG, mips.SP_REG, 4,
                                                           node.line, node.column))

        return instructions

    @visitor.when(cil.DynamicCallNode)
    def visit(self, node):
        instructions = []

        type = self._types_section[node.type]
        method = type.methods.index(self._function_names[node.method])

        reg1 = mips.REGISTERS[0]
        instructions.append(mips.LoadWordNode(reg1, mips.RegisterRelativeLocation(mips.SP_REG, 0),
                                              line=node.line, column=node.column))
        instructions.append(mips.AdditionInmediateNode(mips.SP_REG, mips.SP_REG, 4, node.line, node.column))
        self._pushed_args -= 1

        instructions.append(mips.LoadWordNode(reg1, mips.RegisterRelativeLocation(reg1, 8),
                                              line=node.line, column=node.column))
        instructions.append(mips.LoadWordNode(reg1, mips.RegisterRelativeLocation(reg1, method * 4),
                                              line=node.line, column=node.column))
        instructions.append(mips.JalrNode(mips.RA_REG, reg1, line=node.line, column=node.column))

        if self._pushed_args > 0:
            instructions.append(mips.AdditionInmediateNode(mips.SP_REG, mips.SP_REG,
                                                           self._pushed_args * mips.DOUBLE_WORD,
                                                           line=node.line, column=node.column))
            self._pushed_args = 0
        instructions.extend(self.visit(node.dest))
        instructions.append(mips.StoreWordNode(mips.V0_REG, self.get_var_location(node.dest),
                                               line=node.line, column=node.column))
        if isinstance(node.dest, cil.AttributeNode):
            instructions.append(mips.AdditionInmediateNode(mips.SP_REG, mips.SP_REG, 4,
                                                           node.line, node.column))

        return instructions

    @visitor.when(cil.ArgNode)
    def visit(self, node):
        self._pushed_args += 1
        instructions = []
        reg = mips.REGISTERS[0]
        if isinstance(node.name, int):
            instructions.append(mips.LoadInmediateNode(reg, node.name,
                                                       line=node.line, column=node.column))
        else:
            instructions.extend(self.visit(node.name))
            instructions.append(mips.LoadWordNode(reg, self.get_var_location(node.name),
                                                  line=node.line, column=node.column))
            if isinstance(node.name, cil.AttributeNode):
                instructions.append(mips.AdditionInmediateNode(mips.SP_REG, mips.SP_REG, 4,
                                                               node.line, node.column))
        instructions.extend(mips.push_register(reg, line=node.line, column=node.column))
        return instructions

    @visitor.when(cil.ReturnNode)
    def visit(self, node):
        instructions = []

        if node.value is None or isinstance(node.value, cil.VoidNode):
            instructions.append(mips.LoadInmediateNode(mips.V0_REG, 0, line=node.value.line, column=node.value.column))
        elif isinstance(node.value, int):
            instructions.append(mips.LoadInmediateNode(mips.V0_REG, node.value,
                                                       line=node.line, column=node.column))
        else:
            instructions.extend(self.visit(node.value))
            instructions.append(mips.LoadWordNode(mips.V0_REG, self.get_var_location(node.value),
                                                  line=node.line, column=node.column))
            if isinstance(node.value, cil.AttributeNode):
                instructions.append(mips.AdditionInmediateNode(mips.SP_REG, mips.SP_REG, 4,
                                                               node.line, node.column))
        return instructions

    @visitor.when(cil.LoadNode)
    def visit(self, node):
        instructions = []

        reg = mips.REGISTERS[0]
        instructions.append(mips.LoadAddressNode(reg, self._data_section[node.msg.name].label, line=node.line, column=node.column))
        instructions.extend(self.visit(node.dest))
        instructions.append(mips.StoreWordNode(reg, self.get_var_location(node.dest)
                                               , line=node.line, column=node.column))
        if isinstance(node.dest, cil.AttributeNode):
            instructions.append(mips.AdditionInmediateNode(mips.SP_REG, mips.SP_REG, 4,
                                                           node.line, node.column))

        return instructions

    @visitor.when(cil.PrintStringNode)
    def visit(self, node: cil.PrintStringNode):
        instructions = []
        instructions.append(mips.LoadInmediateNode(mips.V0_REG, 4, line=node.line, column=node.column))
        instructions.extend(self.visit(node.str_addr))
        instructions.append(mips.LoadWordNode(mips.ARG_REGISTERS[0], self.get_var_location(node.str_addr),
                                              line=node.line, column=node.column))
        if isinstance(node.str_addr, cil.AttributeNode):
            instructions.append(mips.AdditionInmediateNode(mips.SP_REG, mips.SP_REG, 4,
                                                           node.line, node.column))
        instructions.append(mips.SyscallNode())
        return instructions

    @visitor.when(cil.PrintIntNode)
    def visit(self, node: cil.PrintIntNode):
        instructions = []
        instructions.append(mips.LoadInmediateNode(mips.V0_REG, 1, line=node.line, column=node.column))
        instructions.extend(self.visit(node.value))
        instructions.append(mips.LoadWordNode(mips.ARG_REGISTERS[0], self.get_var_location(node.value),
                                              line=node.line, column=node.column))
        if isinstance(node.value, cil.AttributeNode):
            instructions.append(mips.AdditionInmediateNode(mips.SP_REG, mips.SP_REG, 4,
                                                           node.line, node.column))
        instructions.append(mips.SyscallNode())
        return instructions

    @visitor.when(cil.ExitNode)
    def visit(self, node: cil.ExitNode):
        instructions = []
        instructions.append(mips.LoadInmediateNode(mips.V0_REG, 10, line=node.line, column=node.column))
        instructions.append(mips.SyscallNode())
        return instructions

    @visitor.when(cil.CopyNode)
    def visit(self, node):
        instructions = []

        reg = mips.REGISTERS[0]
        instructions.extend(self.visit(node.value))
        instructions.append(mips.LoadWordNode(reg, self.get_var_location(node.value),
                                              line=node.line, column=node.column))
        if isinstance(node.value, cil.AttributeNode):
            instructions.append(mips.AdditionInmediateNode(mips.SP_REG, mips.SP_REG, 4,
                                                           node.line, node.column))
        instructions.append(mips.LoadWordNode(mips.ARG_REGISTERS[0], mips.RegisterRelativeLocation(reg, 4),
                                              line=node.line, column=node.column))
        instructions.append(mips.ShiftLeftNode(mips.ARG_REGISTERS[0], mips.ARG_REGISTERS[0], 2,
                                               line=node.line, column=node.column))
        instructions.append(mips.JalNode("malloc", line=node.line, column=node.column))
        instructions.append(mips.MoveNode(mips.ARG_REGISTERS[2], mips.ARG_REGISTERS[0]
                                          , line=node.line, column=node.column))
        instructions.append(mips.MoveNode(mips.ARG_REGISTERS[0], reg, line=node.line, column=node.column))
        instructions.append(mips.MoveNode(mips.ARG_REGISTERS[1], mips.V0_REG, line=node.line, column=node.column))
        instructions.append(mips.JalNode("copy", line=node.line, column=node.column))
        instructions.extend(self.visit(node.dest))
        instructions.append(mips.StoreWordNode(mips.V0_REG, self.get_var_location(node.dest)
                                               , line=node.line, column=node.column))
        if isinstance(node.dest, cil.AttributeNode):
            instructions.append(mips.AdditionInmediateNode(mips.SP_REG, mips.SP_REG, 4,
                                                           node.line, node.column))

        return instructions

    @visitor.when(cil.GetAttribNode)
    def visit(self, node: cil.GetAttribNode):
        instructions = []

        reg1 = mips.REGISTERS[0]
        reg2 = mips.REGISTERS[1]
        instructions.extend(self.visit(node.obj))
        instructions.append(mips.LoadWordNode(reg1, self.get_var_location(node.obj),
                                              line=node.line, column=node.column))
        if isinstance(node.obj, cil.AttributeNode):
            instructions.append(mips.AdditionInmediateNode(mips.SP_REG, mips.SP_REG, 4,
                                                           node.line, node.column))

        tp = self._types_section[node.computed_type]
        offset = (tp.attributes.index(node.attr) + 3) * mips.DOUBLE_WORD
        instructions.append(mips.LoadWordNode(reg2, mips.RegisterRelativeLocation(reg1, offset),
                                              line=node.line, column=node.column))
        instructions.extend(self.visit(node.dest))
        instructions.append(mips.StoreWordNode(reg2, self.get_var_location(node.dest),
                                               line=node.line, column=node.column))
        if isinstance(node.dest, cil.AttributeNode):
            instructions.append(mips.AdditionInmediateNode(mips.SP_REG, mips.SP_REG, 4,
                                                           node.line, node.column))

        return instructions

    @visitor.when(cil.ErrorNode)
    def visit(self, node: cil.ErrorNode):
        instructions = []

        mips_label = self._data_section[node.data.name].label
        instructions.append(mips.LoadInmediateNode(mips.V0_REG, 4, line=node.line, column=node.column))
        instructions.append(mips.LoadAddressNode(mips.ARG_REGISTERS[0], mips_label, line=node.line, column=node.column))
        instructions.append(mips.SyscallNode())
        instructions.append(mips.LoadInmediateNode(mips.V0_REG, 10, line=node.line, column=node.column))
        instructions.append(mips.SyscallNode())

        return instructions

    @visitor.when(cil.ReadIntNode)
    def visit(self, node: cil.ReadIntNode):
        instructions = []

        instructions.append(mips.LoadInmediateNode(mips.V0_REG, 5, line=node.line, column=node.column))
        instructions.append(mips.SyscallNode())
        instructions.extend(self.visit(node.dest))
        instructions.append(mips.StoreWordNode(mips.V0_REG, self.get_var_location(node.dest),
                                               line=node.line, column=node.column))
        if isinstance(node.dest, cil.AttributeNode):
            instructions.append(mips.AdditionInmediateNode(mips.SP_REG, mips.SP_REG, 4,
                                                           node.line, node.column))

        return instructions

    @visitor.when(cil.ReadStringNode)
    def visit(self, node: cil.ReadStringNode):
        instructions = []

        instructions.append(mips.JalNode('read_string', node.line, node.column))
        instructions.extend(self.visit(node.dest))
        instructions.append(mips.StoreWordNode(mips.V0_REG, self.get_var_location(node.dest), node.line, node.column))
        if isinstance(node.dest, cil.AttributeNode):
            instructions.append(mips.AdditionInmediateNode(mips.SP_REG, mips.SP_REG, 4,
                                                           node.line, node.column))
        return instructions

    @visitor.when(cil.SetAttribNode)
    def visit(self, node: cil.SetAttribNode):
        instructions = []

        tp = self._types_section[node.computed_type]
        offset = (tp.attributes.index(node.attr) + 3) * mips.DOUBLE_WORD

        reg1 = mips.REGISTERS[0]
        instructions.extend(self.visit(node.obj))
        instructions.append(mips.LoadWordNode(reg1, self.get_var_location(node.obj),
                                              line=node.line, column=node.column))
        if isinstance(node.obj, cil.AttributeNode):
            instructions.append(mips.AdditionInmediateNode(mips.SP_REG, mips.SP_REG, 4,
                                                           node.line, node.column))

        reg2 = mips.REGISTERS[1]
        if type(node.value) == int:
            instructions.append(mips.LoadInmediateNode(reg2, node.value,
                                                       line=node.line, column=node.column))
        else:
            instructions.extend(self.visit(node.value))
            instructions.append(mips.LoadWordNode(reg2, self.get_var_location(node.value),
                                                  line=node.line, column=node.column))
            if isinstance(node.value, cil.AttributeNode):
                instructions.append(mips.AdditionInmediateNode(mips.SP_REG, mips.SP_REG, 4,
                                                               node.line, node.column))

        instructions.append(mips.StoreWordNode(reg2, mips.RegisterRelativeLocation(reg1, offset),
                                               line=node.line, column=node.column))
        return instructions

    @visitor.when(cil.LessNode)
    def visit(self, node: cil.LessNode):
        instructions = []

        reg1 = mips.REGISTERS[0]
        instructions.extend(self.visit(node.left))
        instructions.append(mips.LoadWordNode(reg1, self.get_var_location(node.left),
                                              line=node.line, column=node.column))
        if isinstance(node.left, cil.AttributeNode):
            instructions.append(mips.AdditionInmediateNode(mips.SP_REG, mips.SP_REG, 4,
                                                           node.line, node.column))

        reg2 = mips.REGISTERS[1]
        instructions.extend(self.visit(node.right))
        instructions.append(mips.LoadWordNode(reg2, self.get_var_location(node.right),
                                              line=node.line, column=node.column))
        if isinstance(node.right, cil.AttributeNode):
            instructions.append(mips.AdditionInmediateNode(mips.SP_REG, mips.SP_REG, 4,
                                                           node.line, node.column))
        instructions.append(mips.LessNode(reg2, reg1, reg2, line=node.line, column=node.column))
        instructions.extend(self.visit(node.dest))
        instructions.append(mips.StoreWordNode(reg2, self.get_var_location(node.dest),
                                               line=node.line, column=node.column))
        if isinstance(node.dest, cil.AttributeNode):
            instructions.append(mips.AdditionInmediateNode(mips.SP_REG, mips.SP_REG, 4,
                                                           node.line, node.column))

        return instructions

    @visitor.when(cil.GotoIfNode)
    def visit(self, node: cil.GotoIfNode):
        instructions = []
        mips_label = self.get_label(node.label)

        reg1 = mips.REGISTERS[0]
        instructions.extend(self.visit(node.condition))
        instructions.append(mips.LoadWordNode(reg1, self.get_var_location(node.condition),
                                              line=node.line, column=node.column))
        if isinstance(node.condition, cil.AttributeNode):
            instructions.append(mips.AdditionInmediateNode(mips.SP_REG, mips.SP_REG, 4,
                                                           node.line, node.column))
        instructions.append(mips.BranchOnNotEqualNode(reg1, mips.ZERO_REG, mips_label,
                                                      line=node.line, column=node.column))

        return instructions

    @visitor.when(cil.GotoNode)
    def visit(self, node: cil.GotoNode):
        mips_label = self.get_label(node.label)
        return [mips.JumpNode(mips_label, line=node.line, column=node.column)]

    @visitor.when(cil.LabelNode)
    def visit(self, node: cil.LabelNode):
        mips_label = self.get_label(node.label)
        return [mips.LabelNode(mips_label, line=node.line, column=node.column)]

    @visitor.when(cil.SubstringNode)
    def visit(self, node: cil.SubstringNode):
        instructions = []

        reg1 = mips.ARG_REGISTERS[0]
        instructions.extend(self.visit(node.str_value))
        instructions.append(mips.LoadWordNode(reg1, self.get_var_location(node.str_value),
                                              line=node.line, column=node.column))
        if isinstance(node.str_value, cil.AttributeNode):
            instructions.append(mips.AdditionInmediateNode(mips.SP_REG, mips.SP_REG, 4,
                                                           node.line, node.column))

        reg1 = mips.ARG_REGISTERS[1]
        if type(node.index) == int:
            instructions.append(mips.LoadInmediateNode(reg1, node.index, line=node.line, column=node.column))
        else:
            instructions.extend(self.visit(node.index))
            instructions.append(mips.LoadWordNode(reg1, self.get_var_location(node.index),
                                                  line=node.line, column=node.column))
            if isinstance(node.index, cil.AttributeNode):
                instructions.append(mips.AdditionInmediateNode(mips.SP_REG, mips.SP_REG, 4,
                                                               node.line, node.column))

        reg1 = mips.ARG_REGISTERS[2]
        if type(node.index) == int:
            instructions.append(mips.LoadInmediateNode(reg1, node.length, line=node.line, column=node.column))
        else:
            instructions.extend(self.visit(node.length))
            instructions.append(mips.LoadWordNode(reg1, self.get_var_location(node.length),
                                                  line=node.line, column=node.column))
            if isinstance(node.length, cil.AttributeNode):
                instructions.append(mips.AdditionInmediateNode(mips.SP_REG, mips.SP_REG, 4,
                                                               node.line, node.column))

        instructions.append(mips.JalNode("substr", line=node.line, column=node.column))
        instructions.extend(self.visit(node.dest))
        instructions.append(mips.StoreWordNode(mips.V0_REG, self.get_var_location(node.dest),
                                               line=node.line, column=node.column))
        if isinstance(node.dest, cil.AttributeNode):
            instructions.append(mips.AdditionInmediateNode(mips.SP_REG, mips.SP_REG, 4,
                                                           node.line, node.column))
        return instructions

    @visitor.when(cil.ConcatNode)
    def visit(self, node: cil.ConcatNode):
        instructions = []

        reg = mips.ARG_REGISTERS[0]
        instructions.extend(self.visit(node.prefix))
        instructions.append(
            mips.LoadWordNode(reg, self.get_var_location(node.prefix), line=node.line, column=node.column))
        if isinstance(node.prefix, cil.AttributeNode):
            instructions.append(mips.AdditionInmediateNode(mips.SP_REG, mips.SP_REG, 4,
                                                           node.line, node.column))
        reg = mips.ARG_REGISTERS[1]
        instructions.extend(self.visit(node.suffix))
        instructions.append(
            mips.LoadWordNode(reg, self.get_var_location(node.suffix), line=node.line, column=node.column))
        if isinstance(node.suffix, cil.AttributeNode):
            instructions.append(mips.AdditionInmediateNode(mips.SP_REG, mips.SP_REG, 4,
                                                           node.line, node.column))
        reg = mips.ARG_REGISTERS[2]
        instructions.extend(self.visit(node.length))
        instructions.append(
            mips.LoadWordNode(reg, self.get_var_location(node.length), line=node.line, column=node.column))
        if isinstance(node.length, cil.AttributeNode):
            instructions.append(mips.AdditionInmediateNode(mips.SP_REG, mips.SP_REG, 4,
                                                           node.line, node.column))
        instructions.append(mips.JalNode("concat", line=node.line, column=node.column))
        instructions.extend(self.visit(node.dest))
        instructions.append(mips.StoreWordNode(mips.V0_REG, self.get_var_location(node.dest),
                                               line=node.line, column=node.column))
        if isinstance(node.dest, cil.AttributeNode):
            instructions.append(mips.AdditionInmediateNode(mips.SP_REG, mips.SP_REG, 4,
                                                           node.line, node.column))
        return instructions

    @visitor.when(cil.LengthNode)
    def visit(self, node: cil.LengthNode):
        instructions = []

        reg = mips.ARG_REGISTERS[0]
        instructions.extend(self.visit(node.source))
        instructions.append(mips.LoadWordNode(reg, self.get_var_location(node.source),
                                              line=node.line, column=node.column))
        if isinstance(node.source, cil.AttributeNode):
            instructions.append(mips.AdditionInmediateNode(mips.SP_REG, mips.SP_REG, 4,
                                                           node.line, node.column))

        instructions.append(mips.JalNode("length", line=node.line, column=node.column))
        instructions.extend(self.visit(node.dest))
        instructions.append(mips.StoreWordNode(mips.V0_REG, self.get_var_location(node.dest),
                                               line=node.line, column=node.column))
        if isinstance(node.dest, cil.AttributeNode):
            instructions.append(mips.AdditionInmediateNode(mips.SP_REG, mips.SP_REG, 4,
                                                           node.line, node.column))

        return instructions

    @visitor.when(cil.EqualNode)
    def visit(self, node: cil.EqualNode):
        instructions = []

        reg1 = mips.REGISTERS[0]
        if type(node.left) == cil.VoidNode:
            instructions.append(mips.LoadInmediateNode(reg1, 0, line=node.line, column=node.column))
        else:
            instructions.extend(self.visit(node.left))
            instructions.append(mips.LoadWordNode(reg1, self.get_var_location(node.left),
                                                  line=node.line, column=node.column))
            if isinstance(node.left, cil.AttributeNode):
                instructions.append(mips.AdditionInmediateNode(mips.SP_REG, mips.SP_REG, 4,
                                                               node.line, node.column))

        reg2 = mips.REGISTERS[1]
        if type(node.right) == cil.VoidNode:
            instructions.append(mips.LoadInmediateNode(reg2, 0, line=node.line, column=node.column))
        else:
            instructions.extend(self.visit(node.right))
            instructions.append(mips.LoadWordNode(reg2, self.get_var_location(node.right),
                                                  line=node.line, column=node.column))
            if isinstance(node.right, cil.AttributeNode):
                instructions.append(mips.AdditionInmediateNode(mips.SP_REG, mips.SP_REG, 4,
                                                               node.line, node.column))

        instructions.append(mips.EqualNode(reg1, reg1, reg2, line=node.line, column=node.column))
        instructions.extend(self.visit(node.dest))
        instructions.append(mips.StoreWordNode(reg1, self.get_var_location(node.dest),
                                               line=node.line, column=node.column))
        if isinstance(node.dest, cil.AttributeNode):
            instructions.append(mips.AdditionInmediateNode(mips.SP_REG, mips.SP_REG, 4,
                                                           node.line, node.column))
        return instructions

    @visitor.when(cil.NameNode)
    def visit(self, node: cil.NameNode):
        instructions = []

        reg = mips.REGISTERS[0]
        instructions.append(mips.LoadAddressNode(reg, mips.TYPES_LABEL, line=node.line, column=node.column))

        tp_number = self._types_section[node.value].index
        instructions.append(mips.AdditionInmediateNode(reg, reg, tp_number * 4, line=node.line, column=node.column))
        instructions.append(mips.LoadWordNode(reg, mips.RegisterRelativeLocation(reg, 0),
                                              line=node.line, column=node.column))

        instructions.extend(self.visit(node.dest))
        instructions.append(mips.StoreWordNode(reg, self.get_var_location(node.dest),
                                               line=node.line, column=node.column))
        if isinstance(node.dest, cil.AttributeNode):
            instructions.append(mips.AdditionInmediateNode(mips.SP_REG, mips.SP_REG, 4,
                                                           node.line, node.column))
        return instructions

    @visitor.when(cil.EqualStringNode)
    def visit(self, node: cil.EqualStringNode):
        instructions = []

        reg1 = mips.REGISTERS[0]
        instructions.extend(self.visit(node.left))
        instructions.append(mips.LoadWordNode(reg1, self.get_var_location(node.left),
                                              line=node.line, column=node.column))
        if isinstance(node.left, cil.AttributeNode):
            instructions.append(mips.AdditionInmediateNode(mips.SP_REG, mips.SP_REG, 4,
                                                           node.line, node.column))
        instructions.append(mips.MoveNode(mips.ARG_REGISTERS[0], reg1, line=node.line, column=node.column))

        instructions.extend(self.visit(node.right))
        instructions.append(mips.LoadWordNode(reg1, self.get_var_location(node.right),
                                              line=node.line, column=node.column))
        if isinstance(node.right, cil.AttributeNode):
            instructions.append(mips.AdditionInmediateNode(mips.SP_REG, mips.SP_REG, 4,
                                                           node.line, node.column))
        instructions.append(mips.MoveNode(mips.ARG_REGISTERS[1], reg1, line=node.line, column=node.column))

        instructions.append(mips.JalNode("equal_str", line=node.line, column=node.column))
        instructions.extend(self.visit(node.dest))
        instructions.append(mips.StoreWordNode(mips.V0_REG, self.get_var_location(node.dest),
                                               line=node.line, column=node.column))
        if isinstance(node.dest, cil.AttributeNode):
            instructions.append(mips.AdditionInmediateNode(mips.SP_REG, mips.SP_REG, 4,
                                                           node.line, node.column))

        return instructions

    @visitor.when(cil.ComplementNode)
    def visit(self, node: cil.ComplementNode):
        instructions = []

        reg1 = mips.REGISTERS[0]
        instructions.extend(self.visit(node.value))
        instructions.append(mips.LoadWordNode(reg1, self.get_var_location(node.value),
                                              line=node.line, column=node.column))
        if isinstance(node.value, cil.AttributeNode):
            instructions.append(mips.AdditionInmediateNode(mips.SP_REG, mips.SP_REG, 4,
                                                           node.line, node.column))

        instructions.append(mips.ComplementNode(reg1, reg1, line=node.line, column=node.column))
        instructions.append(mips.AdditionInmediateNode(reg1, reg1, 1, line=node.line, column=node.column))
        instructions.extend(self.visit(node.dest))
        instructions.append(mips.StoreWordNode(reg1, self.get_var_location(node.dest),
                                               line=node.line, column=node.column))
        if isinstance(node.dest, cil.AttributeNode):
            instructions.append(mips.AdditionInmediateNode(mips.SP_REG, mips.SP_REG, 4,
                                                           node.line, node.column))

        return instructions

    @visitor.when(cil.LessEqualNode)
    def visit(self, node: cil.LessEqualNode):
        instructions = []

        reg1 = mips.REGISTERS[0]
        instructions.extend(self.visit(node.left))
        instructions.append(mips.LoadWordNode(reg1, self.get_var_location(node.left),
                                              line=node.line, column=node.column))
        if isinstance(node.left, cil.AttributeNode):
            instructions.append(mips.AdditionInmediateNode(mips.SP_REG, mips.SP_REG, 4,
                                                           node.line, node.column))

        reg2 = mips.REGISTERS[1]
        instructions.extend(self.visit(node.right))
        instructions.append(mips.LoadWordNode(reg2, self.get_var_location(node.right),
                                              line=node.line, column=node.column))
        if isinstance(node.right, cil.AttributeNode):
            instructions.append(mips.AdditionInmediateNode(mips.SP_REG, mips.SP_REG, 4,
                                                           node.line, node.column))

        instructions.append(mips.LessEqualNode(reg1, reg1, reg2, line=node.line, column=node.column))
        instructions.extend(self.visit(node.dest))
        instructions.append(mips.StoreWordNode(reg1, self.get_var_location(node.dest),
                                               line=node.line, column=node.column))
        if isinstance(node.dest, cil.AttributeNode):
            instructions.append(mips.AdditionInmediateNode(mips.SP_REG, mips.SP_REG, 4,
                                                           node.line, node.column))
        return instructions

    '''
    @visitor.when(PrefixNode)
    def visit(self, node: PrefixNode):
        return f'PREFFIXNODE'

    @visitor.when(ToStrNode)
    def visit(self, node: ToStrNode):
        return f'{node.dest} = str({node.value})'
    '''

    @visitor.when(cil.NotNode)
    def visit(self, node: cil.NotNode):
        instructions = []

        reg1 = mips.REGISTERS[0]
        instructions.extend(self.visit(node.value))
        instructions.append(mips.LoadWordNode(reg1, self.get_var_location(node.value),
                                              line=node.line, column=node.column))
        if isinstance(node.value, cil.AttributeNode):
            instructions.append(mips.AdditionInmediateNode(mips.SP_REG, mips.SP_REG, 4,
                                                           node.line, node.column))
        instructions.append(mips.NotNode(reg1, reg1, line=node.line, column=node.column))
        instructions.extend(self.visit(node.dest))
        instructions.append(mips.StoreWordNode(reg1, self.get_var_location(node.dest),
                                               line=node.line, column=node.column))
        if isinstance(node.dest, cil.AttributeNode):
            instructions.append(mips.AdditionInmediateNode(mips.SP_REG, mips.SP_REG, 4,
                                                           node.line, node.column))

        return instructions

    @visitor.when(cil.VarNode)
    def visit(self, node: cil.VarNode):
        return []

    @visitor.when(cil.ParamNode)
    def visit(self, node: cil.ParamNode):
        return []

    @visitor.when(cil.AttributeNode)
    def visit(self, node: cil.AttributeNode):
        instructions = []

        self_var = self._current_function.params[0]
        reg1 = mips.REGISTERS[4]
        instructions.append(mips.LoadWordNode(reg1, self.get_var_location(self_var), node.line, node.column))

        index = self._types_section[node.type].attributes.index(node.name) + 3
        instructions.append(mips.LoadWordNode(reg1, mips.RegisterRelativeLocation(reg1, index * 4),
                                              line=node.line, column=node.column))
        instructions.extend(mips.push_register(reg1, node.line, node.column))
        return instructions