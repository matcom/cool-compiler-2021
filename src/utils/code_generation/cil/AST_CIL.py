class cil_ast:

    class Node:
        pass

    class ProgramNode(Node):
        def __init__(self, dottypes, dotdata, dotcode):
            self.dottypes = dottypes
            self.dotdata = dotdata
            self.dotcode = dotcode

    class TypeNode(Node):
        def __init__(self, idx):
            self.id = idx
            self.attributes = []
            self.methods = []

    class DataNode(Node):
        def __init__(self, vname, value):
            self.name = vname
            self.value = value

    class FunctionNode(Node):
        def __init__(self, idx, params, localvars, instructions):
            self.id = idx
            self.params = params
            self.localvars = localvars
            self.instructions = instructions
            self.ids = dict()
            self.labels_count = 0

    class ParamNode(Node):
        def __init__(self, idx):
            self.id = idx

    class LocalNode(Node):
        def __init__(self, idx):
            self.id = idx

    class InstructionNode(Node):
        def __init__(self):
            self.leader = False

    class AssignNode(InstructionNode):
        def __init__(self, left, right):
            self.left = left
            self.right = right
        
        def __repr__(self):
            return f"{self.left} = {self.right}"

    class ArithmeticNode(InstructionNode):
        def __init__(self, dest, op_l, op_r):
            self.dest = dest
            self.op_l = op_l
            self.op_r = op_r

    class PlusNode(ArithmeticNode):
        pass

    class MinusNode(ArithmeticNode):
        pass

    class StarNode(ArithmeticNode):
        pass

    class DivNode(ArithmeticNode):
        pass

    class LessThanNode(ArithmeticNode):
        pass

    class LessEqualNode(ArithmeticNode):
        pass

    class EqualNode(ArithmeticNode):
        def __repr__(self):
            return f"{self.dest} = {self.op_l} == {self.op_r}"

    # class EqualStrNode(ArithmeticNode):
    #     pass

    class GetAttrNode(InstructionNode):
        def __init__(self, dest, idx, attr, computed_type):
            self.dest = dest
            self.idx = idx
            self.attr = attr
            self.computed_type = computed_type
        
        def __repr__(self):
            return f"{self.dest} = GETATTR {self.idx} {self.attr}"

    class SetAttrNode(InstructionNode):
        def __init__(self, idx, attr, value, computed_type):
            self.idx = idx
            self.attr = attr
            self.value = value
            self.computed_type = computed_type
    
        def __repr__(self):
            return f"SETATTR {self.idx} {self.attr} {self.value}"

    # class GetIndexNode(InstructionNode):
    #     pass

    # class SetIndexNode(InstructionNode):
    #     pass

    class AllocateNode(InstructionNode):
        def __init__(self, dest, typex):
            self.dest = dest
            self.type = typex
        
        def __repr__(self):
            return f"{self.dest} = ALLOCATE {self.type}"

    # class ArrayNode(InstructionNode):
    #     pass

    class TypeOfNode(InstructionNode):
        def __init__(self, idx, dest):
            self.id = idx
            self.dest = dest

        def __repr__(self):
            return f"{self.dest} = TYPEOF {self.id}"

    class StaticCallNode(InstructionNode):
        def __init__(self, function, dest):
            self.function = function
            self.dest = dest
        
        def __repr__(self):
            return f"{self.dest} = CALL {self.function}"

    class DynamicCallNode(InstructionNode):
        def __init__(self, typex, function, dest, computed_type):
            self.type = typex
            self.function = function
            self.dest = dest
            self.computed_type = computed_type
        
        def __repr__(self):
            return f"{self.dest} = VCALL {self.type} {self.function}"

    class ArgNode(InstructionNode):
        def __init__(self, idx):
            self.id = idx

        def __repr__(self):
            return f"ARG {self.id}"
    
    class IfGotoNode(InstructionNode):
        def __init__(self, if_cond, label):
            self.if_cond = if_cond
            self.label = label
        
        def __repr__(self):
            return f"GOTO {self.label} if {self.if_cond}"

    class LabelNode(InstructionNode):
        def __init__(self, label):
            self.label = label
        
        def __repr__(self):
            return f"LABEL {self.label}:"
    
    class GotoNode(InstructionNode):
        def __init__(self, label):
            self.label = label
        
        def __repr__(self):
            return f"GOTO {self.label}"

    class ReturnNode(InstructionNode):
        def __init__(self, idx=None):
            self.id = idx
        
        def __repr__(self):
            return f"RETURN {self.id}"

    class LoadNode(InstructionNode):
        def __init__(self, dest, msg):
            self.dest = dest
            self.msg = msg

        def __repr__(self):
            return f"{self.dest} LOAD {self.msg}"

    class LengthNode(InstructionNode):
        def __init__(self, dest, idx):
            self.dest = dest
            self.id = idx
    
    class ConcatNode(InstructionNode):
        def __init__(self, dest, s1, s2, length):
            self.dest = dest
            self.s1 = s1
            self.s2 = s2
            self.length = length

    class SubstringNode(InstructionNode):
        def __init__(self, dest, s, i, length):
            self.dest = dest
            self.s = s
            self.i = i
            self.length = length

    class ReadStrNode(InstructionNode):
        def __init__(self, dest):
            self.dest = dest

    class PrintStrNode(InstructionNode):
        def __init__(self, value):
            self.value = value
        
        def __repr__(self):
            return f"PRINTSTR {self.value}"