class CILAstNode:
    pass


class ProgramNode(CILAstNode):
    def __init__(self, dottypes, dotdata, dotcode):
        self.dottypes = dottypes
        self.dotdata = dotdata
        self.dotcode = dotcode


class TypeNode(CILAstNode):
    def __init__(self, name, attributes, methods):
        self.name = name
        self.attributes = attributes
        self.methods = methods


class DataNode(CILAstNode):
    def __init__(self, vname, value):
        self.name = vname
        self.value = value


class FunctionNode(CILAstNode):
    def __init__(self, fname, params, localvars, instructions):
        self.name = fname
        self.params = params
        self.localvars = localvars
        self.instructions = instructions


class ParamNode(CILAstNode):
    def __init__(self, name):
        self.name = name


class LocalNode(CILAstNode):
    def __init__(self, name):
        self.name = name


class InstructionNode(CILAstNode):
    pass


class AssignNode(InstructionNode):
    def __init__(self, dest, source):
        self.dest = dest
        self.source = source


class ArithmeticNode(InstructionNode):
    def __init__(self, dest, left, right):
        self.dest = dest
        self.left = left
        self.right = right


class PlusNode(ArithmeticNode):
    pass


class MinusNode(ArithmeticNode):
    pass


class StarNode(ArithmeticNode):
    pass


class DivNode(ArithmeticNode):
    pass


class GetAttrNode(InstructionNode):
    pass


class SetAttrNode(InstructionNode):
    pass


class GetIndexNode(InstructionNode):
    pass


class SetIndexNode(InstructionNode):
    pass


class AllocateNode(InstructionNode):
    def __init__(self, itype, dest):
        self.type = itype
        self.dest = dest


class ArrayNode(InstructionNode):
    pass


class TypeOfNode(InstructionNode):
    def __init__(self, obj, dest):
        self.obj = obj
        self.dest = dest


class LabelNode(InstructionNode):
    pass


class GotoNode(InstructionNode):
    pass


class GotoIfNode(InstructionNode):
    pass


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
    pass


class ConcatNode(InstructionNode):
    pass


class PrefixNode(InstructionNode):
    pass


class SubstringNode(InstructionNode):
    pass


class ToStrNode(InstructionNode):
    def __init__(self, dest, ivalue):
        self.dest = dest
        self.ivalue = ivalue


class ReadNode(InstructionNode):
    def __init__(self, dest):
        self.dest = dest


class PrintNode(InstructionNode):
    def __init__(self, str_addr):
        self.str_addr = str_addr
