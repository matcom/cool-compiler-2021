class Node:
    pass

class ProgramNode(Node):
    def __init__(self, dottypes, dotdata, dotcode):
        self.dottypes = dottypes
        self.dotdata = dotdata
        self.dotcode = dotcode

class TypeNode(Node):
    def __init__(self, name):
        self.name = name
        self.attrs = {}
        self.methods = []
    
    @property
    def attributes(self):
        return self.attrs.keys()

class DataNode(Node):
    def __init__(self, vname, value):
        self.name = vname
        self.value = value

class FunctionNode(Node):
    def __init__(self, fname, params, localvars, instructions, ctor= False):
        self.name = fname
        self.params = params
        self.localvars = localvars
        self.instructions = instructions
        self.ctor = ctor

class ParamNode(Node):
    def __init__(self, name):
        self.name = name

class LocalNode(Node):
    def __init__(self, name):
        self.name = name

class InstructionNode(Node):
    def __init__(self, dest, op, second_op):
        self.dest = dest
        self.op = op
        self.second_op = second_op


class AssignNode(InstructionNode):
    def __init__(self, dest, source):
        self.dest = dest
        self.source = source

class BinaryOperatorNode(InstructionNode):
    def __init__(self, dest, left, right):
        self.dest = dest
        self.left = left
        self.right = right

class PlusNode(BinaryOperatorNode):
    def __init__(self, dest, left, right):
        super().__init__(dest, left, right)

class MinusNode(BinaryOperatorNode):
    def __init__(self, dest, left, right):
        super().__init__(dest, left, right)

class StarNode(BinaryOperatorNode):
    def __init__(self, dest, left, right):
        super().__init__(dest, left, right)

class DivNode(BinaryOperatorNode):
    def __init__(self, dest, left, right):
        super().__init__(dest, left, right)

class EqualNode(BinaryOperatorNode):
    def __init__(self, dest, left, right):
        super().__init__(dest, left, right)

class LessNode(BinaryOperatorNode):
    def __init__(self, dest, left, right):
        super().__init__(dest, left, right)

class LeqNode(BinaryOperatorNode):
    def __init__(self, dest, left, right):
        super().__init__(dest, left, right)

class GetAttribNode(InstructionNode):
    def __init__(self, dest, inst, attr):
        self. dest = dest
        self.inst = inst
        self.attr = attr

class SetAttribNode(InstructionNode):
    def __init__(self, inst, attr, source):
        self.inst = inst
        self.attr = attr
        self.source = source

class GetIndexNode(InstructionNode):
    def __init__(self, dest, array, index):
        self.dest = dest
        self.array = array
        self.index = index

class SetIndexNode(InstructionNode):
    def __init__(self, array, index, source):
        self.array = array
        self.index = index
        self.source = source

class AllocateNode(InstructionNode):
    def __init__(self, itype, dest):
        self.type = itype
        self.dest = dest

class ArrayNode(InstructionNode):
    def __init__(self, dest, length):
        self.dest = dest
        self.length = length

class TypeOfNode(InstructionNode):
    def __init__(self, obj, dest):
        self.obj = obj
        self.dest = dest

class IsTypeNode(InstructionNode):
    def __init(self, dest, type_obj, type_name):
        self.dest = dest
        self.type_obj = type_obj
        self.type_name = type_name

class ParentTypeNode(InstructionNode):
    def __init__(self, dest, type_obj):
        self.dest = dest
        self.type_obj = type_obj

class LabelNode(InstructionNode):
    def __init__(self, name):
        self.name = name

class GotoNode(InstructionNode):
    def __init__(self, label):
        self.label = label

class GotoIfNode(InstructionNode):
    def __init__(self, label, condition):
        self.label = label
        self.condition = condition

class StaticCallNode(InstructionNode):
    def __init__(self, function, dest):
        self.function = function
        self.dest = dest

class DynamicCallNode(InstructionNode):
    def __init__(self, xtype, method, dest):
        self.type = xtype
        self.method = method
        self.dest = dest

class ArgNode(InstructionNode):
    def __init__(self, name):
        self.name = name

class ReturnNode(InstructionNode):
    def __init__(self, value=None):
        self.value = value

class LoadNode(InstructionNode):
    def __init__(self, dest, msg):
        self.dest = dest
        self.msg = msg

class LengthNode(InstructionNode):
    def __init__(self, dest, string):
        self.dest = dest
        self.string = string

class ConcatNode(InstructionNode):
    def __init__(self, dest, prefix, sufix):
        self.dest = dest
        self.prefix = prefix
        self.sufix = sufix

class PrefixNode(InstructionNode):
    def __init__(self, dest, string, n):
        self.dest = dest
        self.string = string
        self.n = n

class SubstringNode(InstructionNode):
    def __init__(self, dest, string, i, n):
        self.dest = dest
        self.string = string
        self.i = i
        self.n = n

class ToStrNode(InstructionNode):
    def __init__(self, dest, ivalue):
        self.dest = dest
        self.ivalue = ivalue