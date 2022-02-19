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
        def __init__(self, idx, value):
            self.id = idx
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

    class GetAttrNode(InstructionNode):
        def __init__(self, dest, idx, attr, computed_type):
            self.dest = dest
            self.idx = idx
            self.attr = attr
            self.computed_type = computed_type

    class SetAttrNode(InstructionNode):
        def __init__(self, idx, attr, value, computed_type):
            self.idx = idx
            self.attr = attr
            self.value = value
            self.computed_type = computed_type

    class AllocateNode(InstructionNode):
        def __init__(self, dest, typex):
            self.dest = dest
            self.type = typex

    class TypeOfNode(InstructionNode):
        def __init__(self, idx, dest):
            self.id = idx
            self.dest = dest

    class StaticCallNode(InstructionNode):
        def __init__(self, function, dest):
            self.function = function
            self.dest = dest

    class DynamicCallNode(InstructionNode):
        def __init__(self, typex, function, dest, computed_type):
            self.type = typex
            self.function = function
            self.dest = dest
            self.computed_type = computed_type

    class ArgNode(InstructionNode):
        def __init__(self, idx):
            self.id = idx
    
    class IfGotoNode(InstructionNode):
        def __init__(self, if_cond, label):
            self.if_cond = if_cond
            self.label = label

    class LabelNode(InstructionNode):
        def __init__(self, label):
            self.label = label
    
    class GotoNode(InstructionNode):
        def __init__(self, label):
            self.label = label

    class ReturnNode(InstructionNode):
        def __init__(self, idx=None):
            self.id = idx

    class LoadNode(InstructionNode):
        def __init__(self, dest, msg):
            self.dest = dest
            self.msg = msg

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
        
    class ErrorNode(InstructionNode):
        def __init__(self, data_node):
            self.data_node = data_node

    class TypeNameNode(InstructionNode):
        def __init__(self, dest, typex):
            self.dest = dest
            self.type = typex
    
    class NameNode(InstructionNode):
        def __init__(self, dest, idx):
            self.dest = dest
            self.id = idx
    
    class AbortNode(InstructionNode):
        pass

    class CopyNode(InstructionNode):
        def __init__(self, dest, copy):
            self.dest = dest
            self.copy = copy