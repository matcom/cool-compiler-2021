from ...visitors import visitor
from ..cil.cil import *
import core.visitors.mips.mips_ast as mips


def flatten(iterable):
    for item in iterable:
        try:
            yield from flatten(item)
        except TypeError:
            yield item


class FunctionCollectorVisitor:
    def __init__(self):
        self.function_count = 0
        self.functions = {}

    def generate_function_name(self):
        self.function_count += 1
        return f"F_{self.function_count}"

    @visitor.on("node")
    def collect(self, node):
        pass

    @visitor.when(ProgramNode)
    def collect(self, node):
        for func in node.dotcode:
            self.collect(func)

    @visitor.when(FunctionNode)
    def collect(self, node):
        if node.name == "entry":
            self.functions[node.name] = "main"
        else:
            self.functions[node.name] = self.generate_function_name()


class BaseCILToMIPSVisitor:
    def __init__(self):
        self.data = {}
        self.text = {}
        self.types = {}
        self.current_function: mips.FunctionNode = None
        self.pushed_args = 0
        self.label_count = 0
        self.type_count = 0
        self.function_labels = {}
        self.function_collector = FunctionCollectorVisitor()
        self.function_label_count = 0

    def make_data_label(self):
        self.label_count += 1
        return f"data_{self.label_count}"

    def make_function_label(self):
        self.function_label_count += 1
        return f"Label_{self.function_label_count}"

    def make_type_label(self):
        self.type_count += 1
        return f"type_{self.type_count}"

    def make_callee_init_instructions(self, function_node: mips.FunctionNode):
        push_fp = mips.push_to_stack(mips.FP)
        set_fp = mips.AddInmediateNode(mips.FP, mips.SP, 4)
        local_vars_frame_size = len(function_node.localvars) * 4
        set_sp = mips.AddInmediateNode(mips.SP, mips.SP, -local_vars_frame_size)
        return list(flatten([push_fp, set_fp, set_sp]))

    def make_callee_final_instructions(self, function_node: mips.FunctionNode):
        local_vars_frame_size = len(function_node.localvars) * 4
        set_sp = mips.AddInmediateNode(mips.SP, mips.SP, local_vars_frame_size)
        pop_FP = mips.pop_from_stack(mips.FP)
        final = None
        if function_node.label == mips.MAIN_FUNCTION_NAME:
            final = mips.exit_program()
        else:
            final = mips.JumpRegister(mips.RA)

        return list(flatten([set_sp, pop_FP, final]))

    def register_function(self, name, function: FunctionNode):
        self.text[name] = function
        self.current_function = function
        self.function_labels = {}

    def get_param_var_index(self, name):
        index = self.current_function.params.index(name)  # i
        offset = (len(self.current_function.params) - index) * 4
        return mips.RegisterRelativeLocation(mips.FP, offset)

    def get_local_var_index(self, name):
        index = self.current_function.localvars.index(name)
        offset = (index + 1) * -4
        return mips.RegisterRelativeLocation(mips.FP, offset)

    def get_var_location(self, name):
        try:
            return self.get_param_var_index(name)
        except ValueError:
            return self.get_local_var_index(name)

    def get_type_size(self, type_name):
        return len(self.types[type_name].attributes) * 4


class CILToMIPSVisitor(BaseCILToMIPSVisitor):
    @visitor.on("node")
    def visit(self, node):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node: ProgramNode) -> mips.ProgramNode:

        self.function_collector.collect(node)
        self.data["default_str"] = mips.StringConst("default_str", "")

        for dd in node.dotdata:
            self.visit(dd)

        for dt in node.dottypes:
            self.visit(dt)

        for dc in node.dotcode:
            self.visit(dc)

        return mips.ProgramNode(
            [t for t in self.types.values()],
            [d for d in self.data.values()],
            [f for f in self.text.values()],
        )

    @visitor.when(TypeNode)
    def visit(self, node: TypeNode):
        data_label = self.make_data_label()
        self.data[data_label] = mips.StringConst(data_label, node.name)

        type_label = self.make_type_label()
        methods = {
            type_function: self.function_collector.functions[implemented_function]
            for type_function, implemented_function in node.methods
        }
        defaults = {}
        if node.name == "String":
            defaults = {"value": "default_str", "length": "type_4_proto"}
        else:
            defaults = {att: "0" for att in node.attributes}

        self.types[node.name] = mips.TypeNode(
            data_label, type_label, node.attributes, methods, self.type_count, defaults
        )

    @visitor.when(DataNode)
    def visit(self, node: DataNode):
        data_label = self.make_data_label()
        self.data[node.name] = mips.StringConst(data_label, node.value)

    @visitor.when(FunctionNode)
    def visit(self, node: FunctionNode):
        # Init function
        params = [p.name for p in node.params]
        local_vars = [lv.name for lv in node.localvars]
        function_name = self.function_collector.functions[node.name]
        function_node = mips.FunctionNode(function_name, params, local_vars)
        self.register_function(function_name, function_node)
        for inst in node.instructions:
            if isinstance(inst, LabelNode):
                new_label = self.make_function_label()
                self.function_labels[inst.label] = new_label

        # Conventions of Init intructions of the calle function
        init_callee = self.make_callee_init_instructions(function_node)

        # Body instructions
        self.current_function = function_node
        body = [self.visit(instruction) for instruction in node.instructions]

        # Conventions of Final calle instrucctions
        final_callee = self.make_callee_final_instructions(function_node)

        total_instructions = list(flatten(init_callee + body + final_callee))
        function_node.instructions = total_instructions
        self.current_function = None

    @visitor.when(AssignNode)
    def visit(self, node: AssignNode):
        instructions = []

        if type(node.source) == VoidNode:
            instructions.append(
                mips.StoreWordNode(mips.ZERO, self.get_var_location(node.dest))
            )
            return instructions

        if node.source.isnumeric():
            instructions.append(mips.LoadInmediateNode(mips.A0, int(node.source)))
        else:
            instructions.append(
                mips.LoadWordNode(mips.A0, self.get_var_location(node.source))
            )

        instructions.append(
            mips.StoreWordNode(mips.A0, self.get_var_location(node.dest))
        )

        return instructions

    @visitor.when(PlusNode)
    def visit(self, node):
        instructions = []

        if type(node.left) == int:
            instructions.append(mips.LoadInmediateNode(mips.T0, node.left))
        else:
            instructions.append(
                mips.LoadWordNode(mips.T0, self.get_var_location(node.left))
            )

        if type(node.right) == int:
            instructions.append(mips.LoadInmediateNode(mips.T1, node.right))
        else:
            instructions.append(
                mips.LoadWordNode(mips.T1, self.get_var_location(node.right))
            )

        instructions.append(mips.AddNode(mips.T2, mips.T0, mips.T1))
        instructions.append(
            mips.StoreWordNode(mips.T2, self.get_var_location(node.dest))
        )

        return instructions

    @visitor.when(MinusNode)
    def visit(self, node):
        instructions = []

        if type(node.left) == int:
            instructions.append(mips.LoadInmediateNode(mips.T0, node.left))
        else:
            instructions.append(
                mips.LoadWordNode(mips.T0, self.get_var_location(node.left))
            )

        if type(node.right) == int:
            instructions.append(mips.LoadInmediateNode(mips.T1, node.right))
        else:
            instructions.append(
                mips.LoadWordNode(mips.T1, self.get_var_location(node.right))
            )

        instructions.append(mips.SubNode(mips.T2, mips.T0, mips.T1))
        instructions.append(
            mips.StoreWordNode(mips.T2, self.get_var_location(node.dest))
        )

        return instructions

    @visitor.when(StarNode)
    def visit(self, node):
        instructions = []

        if type(node.left) == int:
            instructions.append(mips.LoadInmediateNode(mips.T0, node.left))
        else:
            instructions.append(
                mips.LoadWordNode(mips.T0, self.get_var_location(node.left))
            )

        if type(node.right) == int:
            instructions.append(mips.LoadInmediateNode(mips.T1, node.right))
        else:
            instructions.append(
                mips.LoadWordNode(mips.T1, self.get_var_location(node.right))
            )

        instructions.append(mips.MultiplyNode(mips.T2, mips.T0, mips.T1))
        instructions.append(
            mips.StoreWordNode(mips.T2, self.get_var_location(node.dest))
        )

        return instructions

    @visitor.when(DivNode)
    def visit(self, node):
        instructions = []

        if type(node.left) == int:
            instructions.append(mips.LoadInmediateNode(mips.T0, node.left))
        else:
            instructions.append(
                mips.LoadWordNode(mips.T0, self.get_var_location(node.left))
            )

        if type(node.right) == int:
            instructions.append(mips.LoadInmediateNode(mips.T1, node.right))
        else:
            instructions.append(
                mips.LoadWordNode(mips.T1, self.get_var_location(node.right))
            )

        instructions.append(mips.DivideNode(mips.T0, mips.T1))
        instructions.append(mips.MoveFromLowNode(mips.MoveFromLowNode(mips.T2)))
        instructions.append(
            mips.StoreWordNode(mips.T2, self.get_var_location(node.dest))
        )

        return instructions

    # @visitor.when(LeqNode)
    # def visit(self, node):
    #     instructions = []

    #     if type(node.left) == int:
    #         instructions.append(mips.LoadInmediateNode(mips.A0, node.left))
    #     else:
    #         instructions.append(
    #             mips.LoadWordNode(mips.A0, self.get_var_location(node.left))
    #         )

    #     if type(node.right) == int:
    #         instructions.append(mips.LoadInmediateNode(mips.A1, node.right))
    #     else:
    #         instructions.append(
    #             mips.LoadWordNode(mips.A1, self.get_var_location(node.right))
    #         )

    #     instructions.append(mips.JumpAndLinkNode("less_equal"))
    #     instructions.append(
    #         mips.StoreWordNode(mips.V0, self.get_var_location(node.dest))
    #     )

    #     return instructions

    @visitor.when(LessEqualNode)
    def visit(self, node):
        instructions = []

        if type(node.left) == int:
            instructions.append(mips.LoadInmediateNode(mips.A0, node.left))
        else:
            instructions.append(
                mips.LoadWordNode(mips.A0, self.get_var_location(node.left))
            )

        if type(node.right) == int:
            instructions.append(mips.LoadInmediateNode(mips.A1, node.right))
        else:
            instructions.append(
                mips.LoadWordNode(mips.A1, self.get_var_location(node.right))
            )

        instructions.append(mips.JumpAndLinkNode("less_equal"))
        instructions.append(
            mips.StoreWordNode(mips.V0, self.get_var_location(node.dest))
        )

        return instructions

    @visitor.when(LessNode)
    def visit(self, node):
        instructions = []

        if type(node.left) == int:
            instructions.append(mips.LoadInmediateNode(mips.A0, node.left))
        else:
            instructions.append(
                mips.LoadWordNode(mips.A0, self.get_var_location(node.left))
            )

        if type(node.right) == int:
            instructions.append(mips.LoadInmediateNode(mips.A1, node.rigth))
        else:
            instructions.append(
                mips.LoadWordNode(mips.A1, self.get_var_location(node.right))
            )

        instructions.append(mips.JumpAndLinkNode("less"))
        instructions.append(
            mips.StoreWordNode(mips.V0, self.get_var_location(node.dest))
        )

        return instructions

    @visitor.when(EqualNode)
    def visit(self, node):
        instructions = []

        if type(node.left) == int:
            instructions.append(mips.LoadInmediateNode(mips.A0, node.left))
        elif type(node.left) == VoidNode:
            instructions.append(mips.LoadInmediateNode(mips.A0, 0))
        else:
            instructions.append(
                mips.LoadWordNode(mips.A0, self.get_var_location(node.left))
            )

        if type(node.right) == int:
            instructions.append(mips.LoadInmediateNode(mips.A1, node.right))
        elif type(node.right) == VoidNode:
            instructions.append(mips.LoadInmediateNode(mips.A1, 0))
        else:
            instructions.append(
                mips.LoadWordNode(mips.A1, self.get_var_location(node.right))
            )

        instructions.append(mips.JumpAndLinkNode("equals"))

        instructions.append(
            mips.StoreWordNode(mips.V0, self.get_var_location(node.dest))
        )

        return instructions

    @visitor.when(EqualStrNode)
    def visit(self, node):
        instructions = []

        instructions.append(
            mips.LoadWordNode(mips.A0, self.get_var_location(node.left))
        )
        instructions.append(
            mips.LoadWordNode(mips.A1, self.get_var_location(node.right))
        )
        instructions.append(mips.JumpAndLinkNode("equal_str"))
        instructions.append(
            mips.StoreWordNode(mips.V0, self.get_var_location(node.dest))
        )
        return instructions

    @visitor.when(ComplementNode)
    def visit(self, node):
        instructions = []

        if type(node.obj) == int:
            instructions.append(mips.LoadInmediateNode(mips.T0, node.obj))
        else:
            instructions.append(
                mips.LoadWordNode(mips.T0, self.get_var_location(node.obj))
            )

        instructions.append(mips.ComplementNode(mips.T1, mips.T0))
        instructions.append(mips.AddInmediateNode(mips.T1, mips.T1, 1))
        instructions.append(
            mips.StoreWordNode(mips.T1, self.get_var_location(node.dest))
        )

        return instructions

    @visitor.when(AllocateNode)
    def visit(self, node: AllocateNode):
        instructions = []

        tp = 0
        if node.type.isnumeric():
            tp = node.type
        else:
            tp = self.types[node.type].pos

        # reg1 = t0 reg2 = t1
        instructions.extend(mips.push_to_stack(mips.T0))
        instructions.extend(mips.push_to_stack(mips.T1))
        instructions.append(mips.LoadInmediateNode(mips.T0, tp))

        instructions.append(mips.ShiftLeftLogicalNode(mips.T0, mips.T0, 2))
        instructions.append(mips.LoadAddressNode(mips.T1, mips.VIRTUAL_TABLE))
        instructions.append(mips.AddUnsignedNode(mips.T1, mips.T1, mips.T0))
        instructions.append(
            mips.LoadWordNode(mips.T1, mips.RegisterRelativeLocation(mips.T1, 0))
        )
        instructions.append(
            mips.LoadWordNode(mips.A0, mips.RegisterRelativeLocation(mips.T1, 4))
        )
        instructions.append(mips.ShiftLeftLogicalNode(mips.A0, mips.A0, 2))
        instructions.append(mips.JumpAndLinkNode("malloc"))
        instructions.append(mips.MoveNode(mips.A1, mips.A0))
        instructions.append(mips.MoveNode(mips.A0, mips.T1))
        instructions.append(mips.MoveNode(mips.A1, mips.V0))
        instructions.append(mips.JumpAndLinkNode("copy"))

        instructions.extend(mips.pop_from_stack(mips.T1))
        instructions.extend(mips.pop_from_stack(mips.T0))

        instructions.append(
            mips.StoreWordNode(mips.V0, self.get_var_location(node.dest))
        )

        return instructions

    # @visitor.when(AllocateNode)
    # def visit(self, node: AllocateNode):
    #     instructions = []
    #     instructions.append(mips.LoadInmediateNode(mips.V0, 9))
    #     instructions.append(
    #         mips.LoadInmediateNode(mips.A0, self.get_type_size(node.type))
    #     )
    #     instructions.append(mips.SyscallNode())
    #     return instructions

    @visitor.when(TypeOfNode)
    def visit(self, node: TypeOfNode):
        instructions = []
        instructions.append(mips.LoadWordNode(mips.A0, self.get_var_location(node.obj)))

        instructions.append(
            mips.LoadWordNode(mips.A1, mips.RegisterRelativeLocation(mips.A0, 0))
        )
        instructions.append(
            mips.StoreWordNode(mips.A1, self.get_var_location(node.dest))
        )

        return instructions

    @visitor.when(NameNode)
    def visit(self, node):
        instructions = []

        instructions.append(mips.LoadAddressNode(mips.A0, mips.TYPE_LIST))

        tp_number = self.types[node.name].index
        instructions.append(
            mips.AddInmediateUnsignedNode(mips.a0, mips.a0, tp_number * 4)
        )
        instructions.append(
            mips.LoadWordNode(mips.a0, mips.RegisterRelativeLocation(mips.a0, 0))
        )

        instructions.append(
            mips.StoreWordNode(mips.a0, self.get_var_location(node.dest))
        )

        return instructions

    @visitor.when(LabelNode)
    def visit(self, node: LabelNode):
        return [mips.LabelNode(self.function_labels[node.label])]

    @visitor.when(StaticCallNode)
    def visit(self, node: StaticCallNode):
        instructions = []
        function_to_call = self.function_collector.functions[node.function]
        instructions.append(mips.JumpAndLinkNode(function_to_call))
        instructions.append(
            mips.StoreWordNode(mips.V0, self.get_var_location(node.dest))
        )
        if self.pushed_args > 0:
            instructions.append(
                mips.AddInmediateNode(mips.SP, mips.SP, self.pushed_args * 4)
            )
        self.pushed_args = 0
        return instructions

    @visitor.when(DynamicCallNode)
    def visit(self, node: DynamicCallNode):
        instructions = []
        caller_type = self.types[node.computed_type]
        print(caller_type.methods)
        index = [m for m, m_label in caller_type.methods.items()].index(node.method)
        instructions.append(
            mips.LoadWordNode(mips.A0, self.get_var_location(node.type))
        )

        instructions.append(mips.LoadAddressNode(mips.A1, mips.VIRTUAL_TABLE))
        instructions.append(mips.ShiftLeftLogicalNode(mips.A2, mips.A1, 2))
        instructions.append(mips.AddUnsignedNode(mips.A1, mips.A1, mips.A2))
        instructions.append(
            mips.LoadWordNode(mips.A1, mips.RegisterRelativeLocation(mips.A1, 0))
        )
        instructions.append(
            mips.LoadWordNode(mips.A1, mips.RegisterRelativeLocation(mips.A1, 8))
        )
        instructions.append(mips.AddInmediateUnsignedNode(mips.A1, mips.A1, index * 4))
        instructions.append(
            mips.LoadWordNode(mips.A1, mips.RegisterRelativeLocation(mips.A1, 0))
        )
        instructions.append(mips.JumpRegisterAndLinkNode(mips.A1))

        instructions.append(
            mips.StoreWordNode(mips.V0, self.get_var_location(node.dest))
        )

        if self.pushed_args > 0:
            instructions.append(
                mips.AddInmediateNode(mips.SP, mips.SP, self.pushed_args * 4)
            )
            self.pushed_args = 0

        return instructions

    @visitor.when(ArgNode)
    def visit(self, node: ArgNode):
        self.pushed_args += 1
        instructions = []
        if type(node.name) == int:
            instructions.append(mips.LoadInmediateNode(mips.A0, node.name))
            instructions.extend(mips.push_to_stack(mips.A0))
        else:
            instructions.append(
                mips.LoadWordNode(mips.A0, self.get_var_location(node.name))
            )
            instructions.extend(mips.push_to_stack(mips.A0))

        return instructions

    @visitor.when(ReturnNode)
    def visit(self, node):
        instructions = []
        if node.value is None:
            instructions.append(mips.LoadInmediateNode(mips.V0, 0))
        elif isinstance(node.value, int):
            instructions.append(mips.LoadInmediateNode(mips.V0, node.value))
        elif isinstance(node.value, VoidNode):
            instructions.append(mips.LoadInmediateNode(mips.V0, 0))
        else:
            instructions.append(
                mips.LoadWordNode(mips.V0, self.get_var_location(node.value))
            )

        return instructions

    @visitor.when(LoadNode)
    def visit(self, node: LoadNode):
        instructions = []

        location = mips.LabelRelativeLocation(self.data[node.msg.name].label, 0)
        instructions.append(mips.LoadAddressNode(mips.A0, location))
        instructions.append(
            mips.StoreWordNode(mips.A0, self.get_var_location(node.dest))
        )

        return instructions

    @visitor.when(LengthNode)
    def visit(self, node):
        instructions = []

        instructions.append(
            mips.LoadWordNode(mips.A0, self.get_var_location(node.source))
        )

        instructions.append(mips.JumpAndLinkNode("len"))

        instructions.append(
            mips.StoreWordNode(mips.V0, self.get_var_location(node.dest))
        )

        return instructions

    @visitor.when(ConcatNode)
    def visit(self, node):
        instructions = []

        instructions.append(
            mips.LoadWordNode(mips.A0, self.get_var_location(node.prefix))
        )

        instructions.append(
            mips.LoadWordNode(mips.A1, self.get_var_location(node.suffix))
        )

        instructions.append(
            mips.LoadWordNode(mips.A2, self.get_var_location(node.length))
        )

        instructions.append(mips.JumpAndLinkNode("concat"))

        instructions.append(
            mips.StoreWordNode(mips.V0, self.get_var_location(node.dest))
        )

        return instructions

    @visitor.when(SubstringNode)
    def visit(self, node):
        instructions = []

        instructions.append(
            mips.LoadWordNode(mips.A0, self.get_var_location(node.str_value))
        )

        if type(node.index) == int:
            instructions.append(mips.LoadInmediateNode(mips.A1, node.index))
        else:
            instructions.append(
                mips.LoadWordNode(mips.A1, self.get_var_location(node.index))
            )

        if type(node.length) == int:
            instructions.append(mips.LoadInmediateNode(mips.A2, node.length))
        else:
            instructions.append(
                mips.LoadWordNode(mips.A2, self.get_var_location(node.length))
            )

        instructions.append(mips.JumpAndLinkNode("substr"))
        instructions.append(
            mips.StoreWordNode(mips.V0, self.get_var_location(node.dest))
        )
        return instructions

    @visitor.when(ReadStrNode)
    def visit(self, node):
        instructions = []
        instructions.append(mips.JumpAndLinkNode("read_str"))

        instructions.append(
            mips.StoreWordNode(mips.V0, self.get_var_location(node.dest))
        )

        return instructions

    @visitor.when(PrintIntNode)
    def visit(self, node):
        instructions = []
        instructions.append(mips.LoadInmediateNode(mips.V0, 1))
        instructions.append(
            mips.LoadWordNode(mips.A0, self.get_var_location(node.value))
        )
        instructions.append(mips.SyscallNode())

        return instructions

    @visitor.when(PrintStrNode)
    def visit(self, node):
        instructions = []
        instructions.append(mips.LoadInmediateNode(mips.V0, 4))
        instructions.append(
            mips.LoadWordNode(mips.A0, self.get_var_location(node.value))
        )
        instructions.append(mips.SyscallNode())
        return instructions

    @visitor.when(ErrorNode)
    def visit(self, node):
        instructions = []

        mips_label = self.data[node.data_node.name].label

        instructions.append(mips.LoadInmediateNode(mips.V0, 4))
        instructions.append(mips.LoadAddressNode(mips.A0, mips_label))
        instructions.append(mips.SyscallNode())
        instructions.append(mips.LoadInmediateNode(mips.V0, 10))
        instructions.append(mips.SyscallNode())

        return instructions

    @visitor.when(TypeNameNode)
    def visit(self, node: TypeNameNode):
        instructions = []

        instructions.append(
            mips.LoadWordNode(mips.A0, self.get_var_location(node.source))
        )
        instructions.append(
            mips.LoadWordNode(mips.A0, mips.RegisterRelativeLocation(mips.A0, 0))
        )

        instructions.append(mips.ShiftLeftLogicalNode(mips.A0, mips.A0, 2))
        instructions.append(mips.LoadAddressNode(mips.A1, mips.TYPE_LIST))
        instructions.append(mips.AddUnsignedNode(mips.A0, mips.A0, mips.A1))
        instructions.append(
            mips.LoadWordNode(mips.A0, mips.RegisterRelativeLocation(mips.A0, 0))
        )

        instructions.append(
            mips.StoreWordNode(mips.A0, self.get_var_location(node.dest))
        )

        return instructions

    @visitor.when(ExitNode)
    def visit(self, node):
        instructions = []
        instructions.append(mips.LoadInmediateNode(mips.V0, 10))
        instructions.append(mips.SyscallNode())

        return instructions

    @visitor.when(GetAttribNode)
    def visit(self, node: GetAttribNode):

        instructions = []

        dest = node.dest if type(node.dest) == str else node.dest.name
        obj = node.obj if type(node.obj) == str else node.obj.name
        comp_type = (
            node.computed_type
            if type(node.computed_type) == str
            else node.computed_type.name
        )

        instructions.append(mips.LoadWordNode(mips.A0, self.get_var_location(obj)))

        tp = self.types[comp_type]
        offset = 12 + tp.attributes.index(node.attr) * 4
        instructions.append(
            mips.LoadWordNode(mips.A1, mips.RegisterRelativeLocation(mips.A0, offset))
        )

        instructions.append(mips.StoreWordNode(mips.A1, self.get_var_location(dest)))

        return instructions

    @visitor.when(SetAttribNode)
    def visit(self, node: SetAttribNode):

        instructions = []

        obj = node.obj if type(node.obj) == str else node.obj.name
        comp_type = (
            node.computed_type
            if type(node.computed_type) == str
            else node.computed_type.name
        )

        tp = self.types[comp_type]
        offset = 12 + tp.attributes.index(node.attr) * 4

        instructions.append(mips.LoadWordNode(mips.A0, self.get_var_location(obj)))

        if type(node.value) == int:
            instructions.append(mips.LoadInmediateNode(mips.A1, node.value))
        else:
            instructions.append(
                mips.LoadWordNode(mips.A1, self.get_var_location(node.value))
            )

        instructions.append(
            mips.StoreWordNode(mips.A1, mips.RegisterRelativeLocation(mips.A0, offset))
        )

        return instructions

    @visitor.when(CopyNode)
    def visit(self, node):
        instructions = []
        # reg1 T0 reg2 A3
        instructions.extend(mips.push_to_stack(mips.T0))

        instructions.append(
            mips.LoadWordNode(mips.T0, self.get_var_location(node.source))
        )

        instructions.append(
            mips.LoadWordNode(mips.A0, mips.RegisterRelativeLocation(mips.T0, 4))
        )
        instructions.append(mips.ShiftLeftLogicalNode(mips.A0, mips.A0, 2))
        instructions.append(mips.JumpAndLinkNode("malloc"))
        instructions.append(mips.MoveNode(mips.A2, mips.A0))
        instructions.append(mips.MoveNode(mips.A0, mips.T0))
        instructions.append(mips.MoveNode(mips.A1, mips.V0))
        instructions.append(mips.JumpAndLinkNode("copy"))

        instructions.extend(mips.pop_from_stack(mips.T0))

        instructions.append(
            mips.StoreWordNode(mips.V0, self.get_var_location(node.dest))
        )
        return instructions

    @visitor.when(GotoIfNode)
    def visit(self, node):
        instructions = []

        local_label = self.function_labels[node.label]

        instructions.append(
            mips.LoadWordNode(mips.A0, self.get_var_location(node.condition))
        )

        instructions.append(mips.BranchOnNotEqualNode(mips.A0, mips.ZERO, local_label))

        return instructions

    @visitor.when(GotoNode)
    def visit(self, node):
        local_label = self.function_labels[node.label]
        return [mips.JumpNode(local_label)]

    @visitor.when(ReadIntNode)
    def visit(self, node):
        instructions = []

        instructions.append(mips.LoadInmediateNode(mips.V0, 5))
        instructions.append(mips.SyscallNode())
        instructions.append(
            mips.StoreWordNode(mips.V0, self.get_var_location(node.dest))
        )

        return instructions

    # @visitor.when(NotNode)
    # def visit(self, node):
    #     pass

    # @visitor.when(GetIndexNode)
    # def visit(self, node):
    #     pass

    # @visitor.when(SetIndexNode)
    # def visit(self, node):
    #     pass

    # @visitor.when(ArrayNode)
    # def visit(self, node):
    #     pass

    # @visitor.when(PrefixNode)
    # def visit(self, node):
    #     pass
