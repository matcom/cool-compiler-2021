import core.cil.CILAst as cil
import core.mips.MipsAst as mips
from ..tools import visitor
from ..cil.CILAst import *

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

    @visitor.when(MinusNode)
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

    @visitor.when(StarNode)
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

    @visitor.when(DivNode)
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

    @visitor.when(AllocateNode)
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
        instructions.append(mips.AdditionUnsignedNode(reg2, reg2, reg1))
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






    @visitor.when(TypeOfNode)
    def visit(self, node):
        return f'{node.dest} = TYPEOF {node.obj}'

    @visitor.when(StaticCallNode)
    def visit(self, node):
        return f'{node.dest} = CALL {node.function}'

    @visitor.when(DynamicCallNode)
    def visit(self, node):
        return f'{node.dest} = VCALL {node.type} {node.method.lex}'

    @visitor.when(ArgNode)
    def visit(self, node):
        return f'ARG {node.name}'

    @visitor.when(ReturnNode)
    def visit(self, node):
        return f'RETURN {node.value if node.value is not None else ""}'

    @visitor.when(LoadNode)
    def visit(self, node):
        return f'{node.dest} = LOAD {self.visit(node.msg)}'

    @visitor.when(PrintStringNode)
    def visit(self, node: PrintStringNode):
        return f'PRINTSTRING {node.str_addr}'

    @visitor.when(PrintIntNode)
    def visit(self, node: PrintIntNode):
        return f'PRINTINT {node.value}'

    @visitor.when(ExitNode)
    def visit(self, node: ExitNode):
        return f'EXIT'

    @visitor.when(CopyNode)
    def visit(self, node):
        return f'{node.dest} = COPY {node.value}'

    @visitor.when(GetAttribNode)
    def visit(self, node: GetAttribNode):
        return f'{node.dest} = GETATTRIB {node.obj}.{node.attr} {node.computed_type}'

    @visitor.when(ErrorNode)
    def visit(self, node: ErrorNode):
        return f'ERROR {self.visit(node.data)}'

    @visitor.when(ReadNode)
    def visit(self, node: ReadNode):
        return f'{node.dest} = READ'

    @visitor.when(SetAttribNode)
    def visit(self, node: SetAttribNode):
        return f'SETATTR {node.obj}.{node.attr}: {node.computed_type} = {node.value}'

    @visitor.when(LessNode)
    def visit(self, node: LessNode):
        return f'{node.dest} = {node.left} < {node.right}'

    @visitor.when(GotoIfNode)
    def visit(self, node: GotoIfNode):
        return f'GOTOIF {node.condition} {node.label}'

    @visitor.when(GotoNode)
    def visit(self, node: GotoNode):
        return f'GOTO {node.label}'

    @visitor.when(LabelNode)
    def visit(self, node: LabelNode):
        return f'LABEL {node.label}'

    @visitor.when(SubstringNode)
    def visit(self, node: SubstringNode):
        return f'{node.dest} = SUBSTRING {node.str_value}[{node.index}:{node.index + node.length}]'

    @visitor.when(ConcatNode)
    def visit(self, node: ConcatNode):
        return f'{node.dest} = CONCAT {node.prefix} + {node.suffix}'

    @visitor.when(LengthNode)
    def visit(self, node: LengthNode):
        return f'{node.dest} = LENGTH {node.source}'

    @visitor.when(EqualNode)
    def visit(self, node: EqualNode):
        return f'{node.dest} = {node.left} == {node.right}'

    @visitor.when(NameNode)
    def visit(self, node: NameNode):
        return f'{node.dest} = NAME {node.value}'

    @visitor.when(EqualStringNode)
    def visit(self, node: EqualStringNode):
        return f'{node.dest} = {node.left} == {node.right}'

    @visitor.when(ComplementNode)
    def visit(self, node: ComplementNode):
        return f'{node.dest} = ~{node.value}'

    @visitor.when(LessEqualNode)
    def visit(self, node: LessEqualNode):
        return f'{node.dest} = {node.left} <= {node.right}'

    @visitor.when(GetIndexNode)
    def visit(self, node: GetIndexNode):
        return f'GETINDEXNODE'

    @visitor.when(SetIndexNode)
    def visit(self, node: SetIndexNode):
        return f'SETINDEXNODE'

    @visitor.when(PrefixNode)
    def visit(self, node: PrefixNode):
        return f'PREFFIXNODE'

    @visitor.when(ToStrNode)
    def visit(self, node: ToStrNode):
        return f'{node.dest} = str({node.value})'

    @visitor.when(VoidNode)
    def visit(self, node: VoidNode):
        return 'VOID'

    @visitor.when(NotNode)
    def visit(self, node: NotNode):
        return f'{node.dest} = NOT {node.value}'


