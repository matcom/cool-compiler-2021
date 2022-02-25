import compiler.visitors.visitor as visitor
from ..cmp.cil_ast import *
from ..cmp import mips_ast as mips


def flatten(iterable):
    for item in iterable:
        try:
            yield from flatten(item)
        except TypeError:
            yield item


class BaseCILToMIPSVisitor:
    def __init__(self):
        self.data = {}
        self.text = {}
        self.types = {}
        self.current_function: mips.FunctionNode = None
        self.pushed_args = 0
        self.label_count = 0

    def register_type(self, type_name):
        type_node = mips.TypeNode(self.to_type_label_address(type_name))
        self.types[type_name] = type_node
        return type_node

    def register_data(self, data_name, data):
        data_node = mips.DataNode(self.to_data_label_address(data_name), data)
        self.data[data_name] = data_node
        return data_node

    def register_function(self, function_name, params, locals_var):
        function_node = mips.FunctionNode(
            self.to_function_label_address(function_name), params, locals_var
        )
        self.text[function_name] = function_node
        return function_node
    
    def to_label_count_address(self, label_name):
        self.label_count +=1 
        return f'{label_name}_{self.label_count}'

    def to_type_label_address(self, type_name):
        return f"type_{type_name}"

    def to_data_label_address(self, data_name):
        return f"data_{data_name}"

    def to_function_label_address(self, function_name):
        return f"{function_name}"

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
        if function_node.name == mips.MAIN_FUNCTION_NAME:
            final = mips.exit_program()
        else:
            final = mips.JumpRegister(mips.RA)

        return list(flatten([set_sp, pop_FP, final]))

    def get_param_var_index(self, name):
        index = self.current_function.params.index(name)
        offset = ((len(self._params) - 1) - index) * 4
        return mips.RegisterRelativeLocation(mips.FP, offset)

    def get_local_var_index(self, name):
        index = self.current_function.localvars.index(name)
        offset = (index + 2) * - 4
        return mips.RegisterRelativeLocation(mips.FP offset)
    
    def get_var_location(self, name):
        try:
            return self.get_param_var_index()(name)
        except ValueError:
            return self.get_local_var_index()(name)


class BaseCILToMIPSVisitor(BaseCILToMIPSVisitor):
    @visitor.on(Node)
    def visit(self, node):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node: ProgramNode) -> mips.ProgramNode:
        for dd in node.dotdata:
            self.visit(dd)

        for dt in node.dottypes:
            self.visit(dt)

        for dc in node.dotcode:
            self.visit(dc)

        return mips.ProgramNode(self.data, self.text)

    @visitor.when(TypeNode)
    def visit(self, node: TypeNode):
        type_node = self.register_type(node.name)
        type_node.methods = [method[1] for method in node.methods]

    @visitor.when(DataNode)
    def visit(self, node: DataNode):
        self.register_data(node.name, node.value)

    @visitor.when(FunctionNode)
    def visit(self, node: FunctionNode):
        params = [p.name for p in node.params]
        local_vars = [lv.name for lv in node.localvars]
        function_node = self.register_function(node.name, params, local_vars)

        init_callee = self.make_callee_init_instructions(function_node)
        self.current_function = function_node
        body = [self.visit(instruction) for instruction in node.instructions]
        final_callee = self.make_callee_final_instructions(function_node)

        total_instructions = list(flatten(init_callee + body + final_callee))
        function_node.instrucctions = total_instructions
        self.current_function = None

    # @visitor.when(ParamNode)
    # def visit(self, node):
    #     pass

    # @visitor.when(LocalNode)
    # def visit(self, node):
    #     pass

    @visitor.when(AssignNode)
    def visit(self, node):
        instructions = []

        if type(node.source) == VoidNode:
            instructions.append(mips.StoreWordNode(mips.ZERO, self.get_var_location(node.dest)))
            return instructions
            
        if node.source.isnumeric():
            instructions.append(mips.LoadInmediateNode(mips.A0, int(node.source)))
        else:
            instructions.append(mips.LoadWordNode(mips.A0, self.get_var_location(node.source)))

        instructions.append(mips.StoreWordNode(mips.A0, self.get_var_location(node.dest)))

        return instructions

    # @visitor.when(ArithmeticNode)
    # def visit(self, node):
    #     pass

    @visitor.when(PlusNode)
    def visit(self, node):
        instructions = []

        if type(node.left) == int:
            instructions.append(mips.LoadInmediateNode(mips.T0, node.left))
        else:
            instructions.append(mips.LoadWordNode(mips.T0, self.get_var_location(node.left)))

        if type(node.right) == int:
            instructions.append(mips.LoadInmediateNode(mips.T1, node.right))
        else:
            instructions.append(mips.LoadWordNode(mips.T1, self.get_var_location(node.right)))

        instructions.append(mips.AddNode(mips.T2, mips.T0, mips.T1))
        instructions.append(mips.StoreWordNode(mips.T2, self.get_var_location(node.dest)))

        return instructions

    @visitor.when(MinusNode)
    def visit(self, node):
        instructions = []

        if type(node.left) == int:
            instructions.append(mips.LoadInmediateNode(mips.T0, node.left))
        else:
            instructions.append(mips.LoadWordNode(mips.T0, self.get_var_location(node.left)))

        if type(node.right) == int:
            instructions.append(mips.LoadInmediateNode(mips.T1, node.right))
        else:
            instructions.append(mips.LoadWordNode(mips.T1, self.get_var_location(node.right)))

        instructions.append(mips.SubNode(mips.T2, mips.T0, mips.T1))
        instructions.append(mips.StoreWordNode(mips.T2, self.get_var_location(node.dest)))

        return instructions

    @visitor.when(StarNode)
    def visit(self, node):
        instructions = []

        if type(node.left) == int:
            instructions.append(mips.LoadInmediateNode(mips.T0, node.left))
        else:
            instructions.append(mips.LoadWordNode(mips.T0, self.get_var_location(node.left)))

        if type(node.right) == int:
            instructions.append(mips.LoadInmediateNode(mips.T1, node.right))
        else:
            instructions.append(mips.LoadWordNode(mips.T1, self.get_var_location(node.right)))

        instructions.append(mips.MultiplyNode(mips.T2, mips.T0, mips.T1))
        instructions.append(mips.StoreWordNode(mips.T2, self.get_var_location(node.dest)))

        return instructions

    @visitor.when(DivNode)
    def visit(self, node):
        instructions = []

        if type(node.left) == int:
            instructions.append(mips.LoadInmediateNode(mips.T0, node.left))
        else:
            instructions.append(mips.LoadWordNode(mips.T0, self.get_var_location(node.left)))

        if type(node.right) == int:
            instructions.append(mips.LoadInmediateNode(mips.T1, node.right))
        else:
            instructions.append(mips.LoadWordNode(mips.T1, self.get_var_location(node.right)))

        instructions.append(mips.DivideNode(mips.T0,mips.T1))
        instructions.append(mips.MoveFromLowNode(mips.MoveFromLowNode(mips.T2)))
        instructions.append(mips.StoreWordNode(mips.T2, self.get_var_location(node.dest)))

        return instructions

    @visitor.when(LeqNode)
    def visit(self, node):
        instructions = []

        if type(node.left) == int:
            instructions.append(mips.LoadInmediateNode(mips.A0, node.left))
        else:
            instructions.append(mips.LoadWordNode(mips.A0, self.get_var_location(node.left)))
        
        if type(node.right) == int:
            instructions.append(mips.LoadInmediateNode(mips.A1, node.right))
        else:
            instructions.append(mips.LoadWordNode(mips.A1, self.get_var_location(node.right)))

        instructions.append(mips.JumpAndLinkNode(self.to_function_label_address("less_equal")))
        instructions.append(mips.StoreWordNode(mips.V0, self.get_var_location(node.dest)))

        return instructions

    @visitor.when(LessNode)
    def visit(self, node):
        instructions = []

        if type(node.left) == int:
            instructions.append(mips.LoadInmediateNode(mips.A0, node.left))
        else:
            instructions.append(mips.LoadWordNode(mips.A0, self.get_var_location(node.left)))
        
        if type(node.right) == int:
            instructions.append(mips.LoadInmediateNode(mips.A1, node.right))
        else:
            instructions.append(mips.LoadWordNode(mips.A1, self.get_var_location(node.right)))
        
        instructions.append(mips.JumpAndLinkNode(self.to_function_label_address("less")))
        instructions.append(mips.StoreWordNode(mips.V0, self.get_var_location(node.dest)))

        return instructions

    @visitor.when(EqualNode)
    def visit(self, node):
        instructions = []

        if type(node.left) == int:
            instructions.append(mips.LoadInmediateNode(mips.A0, node.left))
        elif type(node.left) == VoidNode:
            instructions.append(mips.LoadInmediateNode(mips.A0, 0))
        else:
            instructions.append(mips.LoadWordNode(mips.A0, self.get_var_location(node.left)))
        
        if type(node.right) == int:
            instructions.append(mips.LoadInmediateNode(mips.A1, node.right))
        elif type(node.right) == VoidNode:
            instructions.append(mips.LoadInmediateNode(mips.A1, 0))
        else:
            instructions.append(mips.LoadWordNode(mips.A1, self.get_var_location(node.right)))

        instructions.append(mips.JumpAndLinkNode(self.to_function_label_address("equals")))

        instructions.append(mips.StoreWordNode(mips.V0, self.get_var_location(node.dest)))
        
        return instructions

    @visitor.when(EqualStrNode)
    def visit(self, node):
        instructions = []

        instructions.append(mips.LoadWordNode(mips.A0, self.get_var_location(node.left)))
        instructions.append(mips.LoadWordNode(mips.A1, self.get_var_location(node.right)))
        instructions.append(mips.JumpAndLinkNode(self.to_function_label_address("equal_str")))
        instructions.append(mips.StoreWordNode(mips.V0, self.get_var_location(node.dest)))
        return  instructions

    # @visitor.when(VoidNode)
    # def visit(self, node):
    #     pass

    @visitor.when(NotNode)
    def visit(self, node):
        pass

    @visitor.when(ComplementNode)
    def visit(self, node):
        instructions = []

        if type(node.obj) == int:
            instructions.append(mips.LoadInmediateNode(mips.T0, node.obj))
        else:
            instructions.append(mips.LoadWordNode(mips.T0, self.get_var_location(node.obj)))

        instructions.append(mips.ComplementNode(mips.T1, mips.T0))
        instructions.append(mips.AddInmediateNode(mips.T1, mips.T1, 1))
        instructions.append(mips.StoreWordNode(mips.T1, self.get_var_location(node.dest)))

        return instructions

    @visitor.when(GetAttribNode)
    def visit(self, node):
        pass

    @visitor.when(SetAttribNode)
    def visit(self, node):
        pass

    @visitor.when(GetIndexNode)
    def visit(self, node):
        pass

    @visitor.when(SetIndexNode)
    def visit(self, node):
        pass

    @visitor.when(AllocateNode)
    def visit(self, node):
        pass

    @visitor.when(ArrayNode)
    def visit(self, node):
        pass

    @visitor.when(TypeOfNode)
    def visit(self, node):
        pass

    @visitor.when(NameNode)
    def visit(self, node):
        pass

    @visitor.when(LabelNode)
    def visit(self, node:LabelNode):
        pass

    @visitor.when(GotoNode)
    def visit(self, node):
        pass

    @visitor.when(GotoIfNode)
    def visit(self, node):
        pass

    @visitor.when(StaticCallNode)
    def visit(self, node:StaticCallNode):
        instructions = []
        instructions.append(mips.JumpAndLinkNode(self.to_function_label_address(node.function)))
        instructions.append(mips.StoreWordNode(mips.V0, self.get_var_location(node.dest)))
        if self.pushed_args > 0:
            instructions.append(mips.AddInmediateNode(mips.SP, mips.SP, self.pushed_args * 4))
        self.pushed_args = 0
        return instructions

    @visitor.when(DynamicCallNode)
    def visit(self, node):
        pass

    @visitor.when(ArgNode)
    def visit(self, node):
        self.pushed_args +=1
        instructions = []
        if type(node.name) == int:
            instructions.append(mips.LoadInmediateNode(mips.A0, node.name))
            instructions.extend(mips.push_to_stack(mips.A0))
        else: 
            instructions.append(mips.LoadWordNode(mips.A0, self.get_var_location(node.name)))
            instructions.extend(mips.push_to_stack(mips.A0))

        return instructions

    @visitor.when(ReturnNode)
    def visit(self, node):
        pass

    @visitor.when(LoadNode)
    def visit(self, node):
        pass

    @visitor.when(LengthNode)
    def visit(self, node):
        pass

    @visitor.when(ConcatNode)
    def visit(self, node):
        pass

    @visitor.when(PrefixNode)
    def visit(self, node):
        pass

    @visitor.when(SubstringNode)
    def visit(self, node):
        pass

    @visitor.when(ToStrNode)
    def visit(self, node):
        pass

    @visitor.when(ReadNode)
    def visit(self, node):
        pass

    @visitor.when(PrintNode)
    def visit(self, node):
        pass

    @visitor.when(ErrorNode)
    def visit(self, node):
        pass
