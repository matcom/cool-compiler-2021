# AST
import itertools as itt
class Node:
    pass


class ProgramNode(Node):
    def __init__(self, dottypes, dotdata, dotcode):
        self.dottypes = dottypes
        self.dotdata = dotdata
        self.dotcode = dotcode

    @staticmethod
    def visit(node,visitor,mips):
        visitor._data_section["default_str"] = mips.StringConst("default_str", "")
        for tp in node.dottypes:
            visitor.visit(tp)

        for data in node.dotdata:
            visitor.visit(data)

        for func in node.dotcode:
            visitor.visit(func)

        return mips.ProgramNode([data for data in visitor._data_section.values()], [tp for tp in visitor._types.values()], [func for func in visitor._functions.values()])


class TypeNode(Node):
    def __init__(self, name):
        self.name = name
        self.attributes = []
        self.methods = []

    @staticmethod
    def visit(node,visitor,mips):
        visitor._data_section[node.name] = mips.StringConst(node.name, node.name)


        methods = {key: value
                   for key, value in node.methods}
        defaults = []
        if node.name == "String":
            defaults = [('value', 'default_str'), ('length', 'type_Int_shell')]
        new_type = mips.MIPSType(f"type_{node.name}", node.name, node.attributes, methods, len(
             visitor._types), default=defaults)

        visitor._types[node.name] = new_type

class DataNode(Node):
    def __init__(self, vname, value):
        self.name = vname
        self.value = value
    
    @staticmethod
    def visit(node,visitor,mips):
        visitor._data_section[node.name] = mips.StringConst(node.name, node.value)

class FunctionNode(Node):
    def __init__(self, fname, params, localvars, instructions):
        self.name = fname
        self.params = params
        self.localvars = localvars
        self.instructions = instructions
        self.ids = dict()
        self.labels_count = 0

    @staticmethod
    def visit(node,visitor,mips):
        label = "main" if node.name == "entry" else node.name
        params = [param.name for param in node.params]
        localvars = [local.name for local in node.localvars]
        size_for_locals = len(localvars) * mips.ATTR_SIZE

        new_func = mips.FunctionNode(label, params, localvars)
        visitor.register_function(node.name, new_func)
        visitor.init_function(new_func)

        for instruction in node.instructions:
            visitor.collect_labels_in_func(instruction)

        initial_instructions = []
        initial_instructions.extend(mips.push_register(mips.RA_REG))
        initial_instructions.extend(mips.push_register(mips.FP_REG))
        initial_instructions.append(
            mips.AddInmediateNode(mips.FP_REG, mips.SP_REG, 8))
        initial_instructions.append(mips.AddInmediateNode(
            mips.SP_REG, mips.SP_REG, -size_for_locals))

        code_instructions = []

        code_instructions = list(itt.chain.from_iterable(
            [visitor.visit(instruction) for instruction in node.instructions]))

        final_instructions = []

        final_instructions.append(mips.AddInmediateNode(
            mips.SP_REG, mips.SP_REG, size_for_locals))
        final_instructions.append(mips.AddInmediateNode(mips.FP_REG,mips.SP_REG,-8))
        final_instructions.extend(mips.pop_register(mips.FP_REG))
        final_instructions.extend(mips.pop_register(mips.RA_REG))

        if not visitor.in_entry_function():
            final_instructions.append(mips.JumpRegister(mips.RA_REG))
        else:
            final_instructions.extend(mips.exit_program())

        func_instructions = list(
            itt.chain(initial_instructions, code_instructions, final_instructions))
        new_func.add_instructions(func_instructions)

        visitor.finish_functions()



class ParamNode(Node):
    def __init__(self, name):
        self.name = name


class LocalNode(Node):
    def __init__(self, name):
        self.name = name


class InstructionNode(Node):
    def __init__(self):
        self.leader = False


class AssignNode(InstructionNode):
    def __init__(self, dest, source):
        self.dest = dest
        self.source = source

    def __repr__(self):
        return f"{self.dest} = {self.source}"

    @staticmethod
    def visit(node,visitor,mips):
        instructions = []                                             

        reg1 = None
        if type(node.source) == VoidNode:
            reg1 = mips.ZERO_REG
        elif node.source.isnumeric():
            reg1 = mips.ARG_REGISTERS[0]
            instructions.append(mips.LoadInmediateNode(reg1, int(node.source)))
        else:
            reg1 = mips.ARG_REGISTERS[0]
            instructions.append(mips.LoadWordNode(
                reg1, visitor.get_var_location(node.source)))

        instructions.append(mips.StoreWordNode(
            reg1, visitor.get_var_location(node.dest)))
        
        return instructions


class ArithmeticNode(InstructionNode):
    def __init__(self, dest, left, right):
        self.dest = dest
        self.left = left
        self.right = right


class PlusNode(ArithmeticNode):
    pass

    @staticmethod
    def visit(node,visitor,mips):
        instructions = []

        reg1, reg2 = None, None
        if type(node.left) == int:
            reg1 = mips.ARG_REGISTERS[0]
            instructions.append(mips.LoadInmediateNode(reg1, node.left))
        else:
            reg1 = mips.ARG_REGISTERS[0]
            instructions.append(mips.LoadWordNode(
                reg1, visitor.get_var_location(node.left)))

        if type(node.right) == int:
            reg2 = mips.ARG_REGISTERS[1]
            instructions.append(mips.LoadInmediateNode(reg2, node.right))
        else:
            reg2 = mips.ARG_REGISTERS[1]
            instructions.append(mips.LoadWordNode(
                reg2, visitor.get_var_location(node.right)))


        instructions.append(mips.AddNode(
            mips.ARG_REGISTERS[0], reg1, reg2))
        instructions.append(mips.StoreWordNode(
            mips.ARG_REGISTERS[0], visitor.get_var_location(node.dest)))
        return instructions


class MinusNode(ArithmeticNode):
    pass

    @staticmethod
    def visit(node,visitor,mips):
        instructions = []

        reg1, reg2 = None, None
        if type(node.left) == int:
            reg1 = mips.ARG_REGISTERS[0]
            instructions.append(mips.LoadInmediateNode(reg1, node.left))
        else:
            reg1 = mips.ARG_REGISTERS[0]
            instructions.append(mips.LoadWordNode(
                reg1, visitor.get_var_location(node.left)))

        if type(node.right) == int:
            instructions.append(mips.LoadInmediateNode(reg2, node.right))
        else:
            reg2 = mips.ARG_REGISTERS[1]
            instructions.append(mips.LoadWordNode(
                reg2, visitor.get_var_location(node.right)))

        instructions.append(mips.SubNode(
            mips.ARG_REGISTERS[0], reg1, reg2))
        instructions.append(mips.StoreWordNode(
            mips.ARG_REGISTERS[0], visitor.get_var_location(node.dest)))
        return instructions


class StarNode(ArithmeticNode):
    pass

    @staticmethod
    def visit(node,visitor,mips):
        instructions = []

        reg1, reg2 = None, None
        if type(node.left) == int:
            reg1 = mips.ARG_REGISTERS[0]
            instructions.append(mips.LoadInmediateNode(reg1, node.left))
        else:
            reg1 = mips.ARG_REGISTERS[0]
            instructions.append(mips.LoadWordNode(
                reg1, visitor.get_var_location(node.left)))

        if type(node.right) == int:
            reg2 = mips.ARG_REGISTERS[1]
            instructions.append(mips.LoadInmediateNode(reg2, node.right))
        else:
            reg2 = mips.ARG_REGISTERS[1]
            instructions.append(mips.LoadWordNode(
                reg2, visitor.get_var_location(node.right)))

        instructions.append(mips.MultiplyNode(
            mips.ARG_REGISTERS[0], reg1, reg2))
        instructions.append(mips.StoreWordNode(
            mips.ARG_REGISTERS[0], visitor.get_var_location(node.dest)))
        return instructions


class DivNode(ArithmeticNode):
    pass

    @staticmethod
    def visit(node,visitor,mips):
        instructions = []

        reg1, reg2 = None, None
        if type(node.left) == int:
            reg1 = mips.ARG_REGISTERS[0]
            instructions.append(mips.LoadInmediateNode(reg1, node.left))
        else:
            reg1 = mips.ARG_REGISTERS[0]
            instructions.append(mips.LoadWordNode(
                reg1, visitor.get_var_location(node.left)))

        if type(node.right) == int:
            reg2 = mips.ARG_REGISTERS[1]
            instructions.append(mips.LoadInmediateNode(reg2, node.right))
        else:
            reg2 = mips.ARG_REGISTERS[1]
            instructions.append(mips.LoadWordNode(
                reg2, visitor.get_var_location(node.right)))

        instructions.append(mips.DivideNode(reg1, reg2))
        instructions.append(mips.MoveFromLowNode(mips.ARG_REGISTERS[0]))
        instructions.append(mips.StoreWordNode(
            mips.ARG_REGISTERS[0], visitor.get_var_location(node.dest)))

        return instructions


class LessEqualNode(ArithmeticNode):
    pass

    @staticmethod
    def visit(node,visitor,mips):
        instructions = []

        if type(node.left) == int:
            instructions.append(mips.LoadInmediateNode(
                mips.ARG_REGISTERS[0], node.left))
        else:
            instructions.append(mips.LoadWordNode(
                mips.ARG_REGISTERS[0], visitor.get_var_location(node.left)))

        if type(node.right) == int:
            instructions.append(mips.LoadInmediateNode(
                mips.ARG_REGISTERS[1], node.right))
        else:
            instructions.append(mips.LoadWordNode(
                mips.ARG_REGISTERS[1], visitor.get_var_location(node.right)))

        instructions.append(mips.JumpAndLinkNode('less_equal'))
        instructions.append(mips.StoreWordNode(
            mips.V0_REG, visitor.get_var_location(node.dest)))
        return instructions


class LessNode(ArithmeticNode):
    pass

    @staticmethod
    def visit(node,visitor,mips):
        instructions = []


        if type(node.left) == int:
            instructions.append(mips.LoadInmediateNode(
                mips.ARG_REGISTERS[0], node.left))
        else:
            instructions.append(mips.LoadWordNode(
                mips.ARG_REGISTERS[0], visitor.get_var_location(node.left)))

        if type(node.right) == int:
            instructions.append(mips.LoadInmediateNode(
                mips.ARG_REGISTERS[1], node.right))
        else:
            instructions.append(mips.LoadWordNode(
                mips.ARG_REGISTERS[1], visitor.get_var_location(node.right)))
        instructions.append(mips.JumpAndLinkNode('less'))
        instructions.append(mips.StoreWordNode(
            mips.V0_REG, visitor.get_var_location(node.dest)))


        return instructions 


class EqualNode(ArithmeticNode):
    def __repr__(self):
        return f"{self.dest} = {self.left} == {self.right}"

    @staticmethod
    def visit(node,visitor,mips):
        instructions = []

        if type(node.left) == int:
            instructions.append(mips.LoadInmediateNode(
                mips.ARG_REGISTERS[0], node.left))
        elif type(node.left) == VoidNode:
            instructions.append(
                mips.LoadInmediateNode(mips.ARG_REGISTERS[0], 0))
        else:
            instructions.append(mips.LoadWordNode(
                mips.ARG_REGISTERS[0], visitor.get_var_location(node.left)))

        if type(node.right) == int:
            instructions.append(mips.LoadInmediateNode(
                mips.ARG_REGISTERS[1], node.right))
        elif type(node.right) == VoidNode:
            instructions.append(
                mips.LoadInmediateNode(mips.ARG_REGISTERS[1], 0))
        else:
            instructions.append(mips.LoadWordNode(
                mips.ARG_REGISTERS[1], visitor.get_var_location(node.right)))

        instructions.append(mips.JumpAndLinkNode("equals"))

        instructions.append(mips.StoreWordNode(
            mips.V0_REG, visitor.get_var_location(node.dest)))
        return instructions

class EqualStrNode(ArithmeticNode):
    pass

    @staticmethod
    def visit(node,visitor,mips):
        instructions = []

        instructions.append(mips.LoadWordNode(
            mips.ARG_REGISTERS[0], visitor.get_var_location(node.left)))
        instructions.append(mips.LoadWordNode(
            mips.ARG_REGISTERS[1], visitor.get_var_location(node.right)))

        instructions.append(mips.JumpAndLinkNode("equal_str"))

        instructions.append(mips.StoreWordNode(
            mips.V0_REG, visitor.get_var_location(node.dest)))

        return instructions


class GetAttribNode(InstructionNode):
    def __init__(self, dest, obj, attr, computed_type):
        self.dest = dest
        self.obj = obj
        self.attr = attr
        self.computed_type = computed_type

    def __repr__(self):
        return f"{self.dest} = GETATTR {self.obj} {self.attr}"

    @staticmethod
    def visit(node,visitor,mips):
        instructions = []

        dest = node.dest if type(node.dest) == str else node.dest.name
        obj = node.obj if type(node.obj) == str else node.obj.name
        comp_type = node.computed_type if type(
            node.computed_type) == str else node.computed_type.name

        reg = mips.ARG_REGISTERS[0]

        instructions.append(mips.LoadWordNode(
            reg, visitor.get_var_location(obj)))

        tp = visitor._types[comp_type]
        offset = (tp.attributes.index(node.attr) + 3) * mips.ATTR_SIZE
        instructions.append(mips.LoadWordNode(
            mips.ARG_REGISTERS[1], mips.RegisterRelativeLocation(reg, offset)))

        instructions.append(mips.StoreWordNode(
            mips.ARG_REGISTERS[1], visitor.get_var_location(dest)))
        return instructions


class SetAttribNode(InstructionNode):
    def __init__(self, obj, attr, value, computed_type):
        self.obj = obj
        self.attr = attr
        self.value = value
        self.computed_type = computed_type

    @staticmethod
    def visit(node,visitor,mips):
        instructions = []

        obj = node.obj if type(node.obj) == str else node.obj.name
        comp_type = node.computed_type if type(
            node.computed_type) == str else node.computed_type.name

        tp = visitor._types[comp_type]
        offset = (tp.attributes.index(node.attr) + 3) * mips.ATTR_SIZE

        reg1 = mips.ARG_REGISTERS[0]
        instructions.append(mips.LoadWordNode(
            mips.ARG_REGISTERS[0], visitor.get_var_location(obj)))

        reg2 = None
        if type(node.value) == int:
            reg2 = instructions.append(mips.LoadInmediateNode(
                mips.ARG_REGISTERS[1], node.value))
        else:
            word_to_load = visitor.get_var_location(node.value) if type(node.value).__name__ =='str' else 0
            reg2 = mips.ARG_REGISTERS[1]
            instructions.append(mips.LoadWordNode(
                reg2, word_to_load))

        instructions.append(mips.StoreWordNode(
            reg2, mips.RegisterRelativeLocation(reg1, offset)))

        return instructions
class GetIndexNode(InstructionNode):
    pass


class SetIndexNode(InstructionNode):
    pass


class AllocateNode(InstructionNode):
    def __init__(self, itype, dest):
        self.type = itype
        self.dest = dest

    @staticmethod
    def visit(node,visitor,mips):
        instructions = []

        tp = 0
        if node.type.isnumeric():
            tp = node.type
        else:
            tp = visitor._types[node.type].index


        instructions.append(mips.LoadInmediateNode(mips.ARG_REGISTERS[0], tp))

        instructions.extend(mips.create_object(mips.ARG_REGISTERS[0], mips.ARG_REGISTERS[1] ))

        instructions.append(mips.StoreWordNode(
            mips.V0_REG, visitor.get_var_location(node.dest)))
        
        return instructions

class ArrayNode(InstructionNode):
    pass


class TypeOfNode(InstructionNode):
    def __init__(self, obj, dest):
        self.obj = obj
        self.dest = dest

    def __repr__(self):
        return f"{self.dest} = TYPEOF {self.obj}"

    @staticmethod
    def visit(node,visitor,mips):
        instructions = []

        reg1 = mips.ARG_REGISTERS[0]
        instructions.append(mips.LoadWordNode(
            reg1, visitor.get_var_location(node.obj)))

        instructions.append(mips.LoadWordNode(
            mips.ARG_REGISTERS[1], mips.RegisterRelativeLocation(reg1, 0)))
        instructions.append(mips.StoreWordNode(
            mips.ARG_REGISTERS[1], visitor.get_var_location(node.dest)))
        return instructions

class LabelNode(InstructionNode):
    def __init__(self, label):
        self.label = label

    def __repr__(self):
        return f"LABEL {self.label}:"

    @staticmethod
    def visit(node,visitor,mips):
        return [mips.LabelNode(visitor.get_mips_label(node.label))]


class GotoNode(InstructionNode):
    def __init__(self, label):
        self.label = label

    def __repr__(self):
        return f"GOTO {self.label}"

    @staticmethod
    def visit(node,visitor,mips):
        mips_label = visitor.get_mips_label(node.label)
        return [mips.JumpNode(mips_label)]

class GotoIfNode(InstructionNode):
    def __init__(self, condition, label):
        self.condition = condition
        self.label = label

    def __repr__(self):
        return f"GOTO {self.label} if {self.condition}"

    @staticmethod
    def visit(node,visitor,mips):
        instructions = []

        mips_label = visitor.get_mips_label(node.label)

        reg = mips.ARG_REGISTERS[0]
        instructions.append(mips.LoadWordNode(
            mips.ARG_REGISTERS[0], visitor.get_var_location(node.condition)))

        instructions.append(mips.BranchOnNotEqualNode(
            reg, mips.ZERO_REG, mips_label))

        

        return instructions

class StaticCallNode(InstructionNode):
    def __init__(self, function, dest):
        self.function = function
        self.dest = dest

    def __repr__(self):
        return f"{self.dest} = CALL {self.function}"

    @staticmethod
    def visit(node,visitor,mips):
        instructions = []
        label = node.function
        instructions.append(mips.JumpAndLinkNode(label))

        instructions.append(mips.StoreWordNode(
            mips.V0_REG, visitor.get_var_location(node.dest)))

        if visitor._pushed_args > 0:
            instructions.append(mips.AddInmediateNode(
                mips.SP_REG, mips.SP_REG, visitor._pushed_args * mips.ATTR_SIZE))
            visitor.clean_pushed_args()
        return instructions

class DynamicCallNode(InstructionNode):
    def __init__(self, xtype, method, dest, computed_type):
        self.type = xtype
        self.method = method
        self.dest = dest
        self.computed_type = computed_type

    def __repr__(self):
        return f"{self.dest} = VCALL {self.type} {self.method}"

    @staticmethod
    def visit(node,visitor,mips):
        instructions = []

        comp_tp = visitor._types[node.computed_type]
        method_index = list(comp_tp.methods).index(node.method)
        reg = mips.ARG_REGISTERS[0]
        instructions.append(mips.LoadWordNode(
            reg, visitor.get_var_location(node.type)))

        instructions.append(mips.LoadAddressNode(
            mips.ARG_REGISTERS[1], mips.SHELLS_TABLE_LABEL))
        
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
            mips.V0_REG, visitor.get_var_location(node.dest)))
        if visitor._pushed_args > 0:
            instructions.append(mips.AddInmediateNode(
                mips.SP_REG, mips.SP_REG, visitor._pushed_args * mips.ATTR_SIZE))
            visitor.clean_pushed_args()

        return instructions


class ArgNode(InstructionNode):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"ARG {self.name}"

    @staticmethod
    def visit(node,visitor,mips):
        visitor.push_arg()
        instructions = []
        if type(node.name) == int:
            instructions.append(mips.LoadInmediateNode(
                mips.ARG_REGISTERS[0], node.name))
            instructions.extend(mips.push_register(mips.ARG_REGISTERS[0]))
        else:
            reg = mips.ARG_REGISTERS[0]
            instructions.append(mips.LoadWordNode(
                reg, visitor.get_var_location(node.name)))
            instructions.extend(mips.push_register(reg))
        return instructions


class ReturnNode(InstructionNode):
    def __init__(self, value=None):
        self.value = value

    def __repr__(self):
        return f"RETURN {self.value}"

    @staticmethod
    def visit(node,visitor,mips):
        instructions = []

        if node.value is None:
            instructions.append(mips.LoadInmediateNode(mips.V0_REG, 0))
        elif isinstance(node.value, int):
            instructions.append(
                mips.LoadInmediateNode(mips.V0_REG, node.value))
        elif isinstance(node.value, VoidNode):
            instructions.append(mips.LoadInmediateNode(mips.V0_REG, 0))
        else:
            instructions.append(mips.LoadWordNode(
                mips.V0_REG, visitor.get_var_location(node.value)))
        return instructions


class LoadNode(InstructionNode):
    def __init__(self, dest, msg):
        self.dest = dest
        self.msg = msg

    def __repr__(self):
        return f"{self.dest} LOAD {self.msg}"

    @staticmethod
    def visit(node,visitor,mips):
        instructions = []

        string_location = mips.LabelRelativeLocation(
            node.msg.name, 0)
        instructions.append(mips.LoadAddressNode(
            mips.ARG_REGISTERS[0], string_location))
        instructions.append(mips.StoreWordNode(
            mips.ARG_REGISTERS[0], visitor.get_var_location(node.dest)))
        
        return instructions


class ExitNode(InstructionNode):
    pass

    @staticmethod
    def visit(node,visitor,mips):
        instructions = []
        instructions.append(mips.LoadInmediateNode(mips.V0_REG, 10))
        instructions.append(mips.SyscallNode())

        return instructions


class TypeNameNode(InstructionNode):
    def __init__(self, dest, source):
        self.dest = dest
        self.source = source

    def __repr__(self):
        return f"{self.dest} = TYPENAME {self.source}"

    @staticmethod
    def visit(node,visitor,mips):
        instructions = []

        reg1 = mips.REGISTERS[0]
        instructions.append(mips.LoadWordNode(
            reg1, visitor.get_var_location(node.source)))
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
            mips.ARG_REGISTERS[0], visitor.get_var_location(node.dest)))

        return instructions


class NameNode(InstructionNode):
    def __init__(self, dest, name):
        self.dest = dest
        self.name = name

    def __repr__(self):
        return f"{self.dest} = NAME {self.name}"

    @staticmethod
    def visit(node,visitor,mips):
        instructions = []

        reg = mips.ARG_REGISTERS[0]

        instructions.append(mips.LoadAddressNode(
            reg, mips.TYPENAMES_TABLE_LABEL))

        tp_number = visitor._types[node.name].index
        instructions.append(
            mips.AddInmediateUnsignedNode(reg, reg, tp_number*4))
        instructions.append(mips.LoadWordNode(
            reg, mips.RegisterRelativeLocation(reg, 0)))

        instructions.append(mips.StoreWordNode(
            reg, visitor.get_var_location(node.dest)))

        return instructions


class CopyNode(InstructionNode):
    def __init__(self, dest, source):
        self.dest = dest
        self.source = source
    
    @staticmethod
    def visit(node,visitor,mips):
        instructions = []

        reg = mips.ARG_REGISTERS[0]
        instructions.append(mips.LoadWordNode(
            reg, visitor.get_var_location(node.source)))

        instructions.extend(mips.copy_object(reg, mips.ARG_REGISTERS[3]))

        instructions.append(mips.StoreWordNode(
            mips.V0_REG, visitor.get_var_location(node.dest)))
        return instructions

class LengthNode(InstructionNode):
    def __init__(self, dest, source):
        self.dest = dest
        self.source = source

    @staticmethod
    def visit(node,visitor,mips):
        instructions = []
        instructions.extend(mips.push_register(mips.ARG_REGISTERS[0]))

        reg = mips.ARG_REGISTERS[0]
        instructions.append(mips.LoadWordNode(
            reg, visitor.get_var_location(node.source)))

        instructions.append(mips.MoveNode(mips.ARG_REGISTERS[0], reg))
        instructions.append(mips.JumpAndLinkNode("len"))

        instructions.append(mips.StoreWordNode(
            mips.V0_REG, visitor.get_var_location(node.dest)))

        instructions.extend(mips.pop_register(mips.ARG_REGISTERS[0]))
        return instructions


class ConcatNode(InstructionNode):
    def __init__(self, dest, prefix, suffix, length):
        self.dest = dest
        self.prefix = prefix
        self.suffix = suffix
        self.length = length
    
    @staticmethod
    def visit(node,visitor,mips):
        instructions = []

        instructions.append(mips.LoadWordNode(
            mips.ARG_REGISTERS[0], visitor.get_var_location(node.prefix)))
        instructions.append(mips.LoadWordNode(
            mips.ARG_REGISTERS[1], visitor.get_var_location(node.suffix)))
        instructions.append(mips.LoadWordNode(
            mips.ARG_REGISTERS[2], visitor.get_var_location(node.length)))
        instructions.append(mips.JumpAndLinkNode("concat"))

        instructions.append(mips.StoreWordNode(
            mips.V0_REG, visitor.get_var_location(node.dest)))
        return instructions


class SubstringNode(InstructionNode):
    def __init__(self, dest, str_value, index, length):
        self.dest = dest
        self.str_value = str_value
        self.index = index
        self.length = length

    @staticmethod
    def visit(node,visitor,mips):
        instructions = []

        instructions.append(mips.LoadWordNode(
            mips.ARG_REGISTERS[0], visitor.get_var_location(node.str_value)))

        if type(node.index) == int:
            instructions.append(mips.LoadInmediateNode(
                mips.ARG_REGISTERS[1], node.index))
        else:
            instructions.append(mips.LoadWordNode(
                mips.ARG_REGISTERS[1], visitor.get_var_location(node.index)))

        if type(node.length) == int:
            instructions.append(mips.LoadInmediateNode(
                mips.ARG_REGISTERS[2], node.length))
        else:
            instructions.append(mips.LoadWordNode(
                mips.ARG_REGISTERS[2], visitor.get_var_location(node.length)))
        instructions.append(mips.JumpAndLinkNode("substr"))
        instructions.append(mips.StoreWordNode(
            mips.V0_REG, visitor.get_var_location(node.dest)))
        return instructions


class ReadStrNode(InstructionNode):
    def __init__(self, dest):
        self.dest = dest

    @staticmethod
    def visit(node,visitor,mips):
        instructions = []
        instructions.append(mips.JumpAndLinkNode("read_str"))

        instructions.append(mips.StoreWordNode(
            mips.V0_REG, visitor.get_var_location(node.dest)))
        return instructions


class ReadIntNode(InstructionNode):
    def __init__(self, dest):
        self.dest = dest

    @staticmethod
    def visit(node,visitor,mips):
        instructions = []

        instructions.append(mips.LoadInmediateNode(mips.V0_REG, 5))
        instructions.append(mips.SyscallNode())
        instructions.append(mips.StoreWordNode(
            mips.V0_REG, visitor.get_var_location(node.dest)))

        return instructions

class PrintStrNode(InstructionNode):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"PRINTSTR {self.value}"

    @staticmethod
    def visit(node,visitor,mips):
        instructions = []
        instructions.append(mips.LoadInmediateNode(mips.V0_REG, 4))

        instructions.append(mips.LoadWordNode(
            mips.ARG_REGISTERS[0], visitor.get_var_location(node.value)))
        instructions.append(mips.SyscallNode())

        return instructions

class PrintIntNode(InstructionNode):
    def __init__(self, value):
        self.value = value

    @staticmethod
    def visit(node,visitor,mips):
        instructions = []
        instructions.append(mips.LoadInmediateNode(mips.V0_REG, 1))

        instructions.append(mips.LoadWordNode(
            mips.ARG_REGISTERS[0], visitor.get_var_location(node.value)))
        
        instructions.append(mips.SyscallNode())

        return instructions
class ComplementNode(InstructionNode):
    def __init__(self, dest, obj):
        self.dest = dest
        self.obj = obj

    @staticmethod
    def visit(node,visitor,mips):
        instructions = []

        reg1 = None

        if type(node.obj) == int:
            reg1 = mips.ARG_REGISTERS[0]
            instructions.append(mips.LoadInmediateNode(reg1, node.obj))
        else:
            reg1 = mips.ARG_REGISTERS[0]
            instructions.append(mips.LoadWordNode(
                reg1, visitor.get_var_location(node.obj)))

        reg2 = mips.ARG_REGISTERS[1]
        instructions.append(mips.ComplementNode(reg2, reg1))
        instructions.append(mips.AddInmediateNode(reg2, reg2, 1))
        instructions.append(mips.StoreWordNode(
            reg2, visitor.get_var_location(node.dest)))

        return instructions


class VoidNode(InstructionNode):
    pass


class ErrorNode(InstructionNode):
    def __init__(self, data_node):
        self.data_node = data_node

    def __repr__(self):
        return f"ERROR {self.data_node}"

    @staticmethod
    def visit(node,visitor,mips):
        instructions = []

        mips_label = visitor._data_section[node.data_node.name].label

        instructions.append(mips.LoadInmediateNode(mips.V0_REG, 4))
        instructions.append(mips.LoadAddressNode(
            mips.ARG_REGISTERS[0], mips_label))
        instructions.append(mips.SyscallNode())
        instructions.append(mips.LoadInmediateNode(mips.V0_REG, 10))
        instructions.append(mips.SyscallNode())

        return instructions