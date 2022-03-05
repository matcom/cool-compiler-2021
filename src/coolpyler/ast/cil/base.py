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
    def __init__(self, instance, attr, dest) -> None:
        super().__init__()
        self.instance = instance
        self.attr = attr
        self.dest = dest


class SetAttrNode(InstructionNode):
    def __init__(self, instance, attr, source) -> None:
        super().__init__()
        self.instance = instance
        self.attr = attr
        self.source = source


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
    def __init__(self, name) -> None:
        super().__init__()
        self.name = name


class GotoNode(InstructionNode):
    def __init__(self, label) -> None:
        super().__init__()
        self.label = label


class GotoIfGtNode(InstructionNode):
    def __init__(self, cond, label) -> None:
        super().__init__()
        self.cond = cond
        self.label = label


class GotoIfLtNode(InstructionNode):
    def __init__(self, cond, label) -> None:
        super().__init__()
        self.cond = cond
        self.label = label


class GotoIfEqNode(InstructionNode):
    def __init__(self, cond, label) -> None:
        super().__init__()
        self.cond = cond
        self.label = label


class StrEqNode(InstructionNode):
    def __init__(self, dest, str1, str2) -> None:
        super().__init__()
        self.dest = dest
        self.str1 = str1
        self.str2 = str2


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
    def __init__(self, value):
        self.value = value


class ExitNode(InstructionNode):
    def __init__(self, code) -> None:
        self.code = code


class LoadNode(InstructionNode):
    def __init__(self, dest, msg):
        self.dest = dest
        self.msg = msg


class LengthNode(InstructionNode):
    def __init__(self, dest, string):
        self.dest = dest
        self.string = string


class ConcatNode(InstructionNode):
    def __init__(self, dest, string1, string2, dest_lenght):
        self.dest = dest
        self.string1 = string1
        self.string2 = string2
        self.dest_lenght = dest_lenght


class PrefixNode(InstructionNode):
    def __init__(self, dest, string, n):
        self.dest = dest
        self.string = string
        self.n = n


class SubstringNode(InstructionNode):
    def __init__(self, dest, string, n, index):
        self.dest = dest
        self.string = string
        self.n = n
        self.index = index


class ToStrNode(InstructionNode):
    def __init__(self, dest, ivalue):
        self.dest = dest
        self.ivalue = ivalue


class ReadNode(InstructionNode):
    def __init__(self, dest, is_string):
        self.is_string = is_string
        self.dest = dest


class PrintNode(InstructionNode):
    def __init__(self, str_addr, is_string):
        self.is_string = is_string
        self.str_addr = str_addr


class ComplementNode(InstructionNode):
    def __init__(self, dest, source):
        self.source = source
        self.dest = dest
