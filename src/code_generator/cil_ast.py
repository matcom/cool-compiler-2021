class Node:
    pass


class ProgramNode(Node):
    def __init__(self, dottypes, dotdata, dotcode):
        self.dottypes = dottypes
        self.dotdata = dotdata
        self.dotcode = dotcode

# .TYPE


class TypeNode(Node):
    def __init__(self, name):
        self.name = name
        self.attributes = []
        self.methods = {}

# .DATA


class DataNode(Node):
    def __init__(self, vname, value):
        self.name = vname
        self.value = value

# .CODE


class FunctionNode(Node):
    def __init__(self, name, params=[], localvars=[], instructions=[]):
        self.name = name
        self.params = params
        self.localvars = localvars
        self.instructions = instructions


class InstructionNode(Node):
    def __init__(self):
        pass


class ParamNode(InstructionNode):
    def __init__(self, name):
        self.name = name


class LocalNode(InstructionNode):
    def __init__(self, name):
        self.name = name


class AssignNode(InstructionNode):
    def __init__(self, local_dest, expr):
        self.local_dest = local_dest
        self.expr = expr


class BinaryOperationNode(InstructionNode):
    def __init__(self, local_dest, lvalue, rvalue, op):
        self.local_dest = local_dest
        self.lvalue = lvalue
        self.rvalue = rvalue
        self.operator = op


class ArithExpressionNode(InstructionNode):
    def __init__(self, dest, left, right):
        self.dest = dest
        self.left = left
        self.right = right

# Arith


class PlusNode(ArithExpressionNode):
    pass


class MinusNode(ArithExpressionNode):
    pass


class StarNode(ArithExpressionNode):
    pass


class DivNode(ArithExpressionNode):
    pass


class LessNode(ArithExpressionNode):
    pass


class LessEqualNode(ArithExpressionNode):
    pass


class EqualNode(ArithExpressionNode):
    pass


class NotNode(Node):
    def __init__(self, dest, expr):
        self.dest = dest
        self.expr = expr


class LogicNotNode(Node):
    def __init__(self, dest, expr):
        self.dest = dest
        self.expr = expr

# Attr


class GetAttrNode(InstructionNode):
    def __init__(self, dest, instance, attr, static_type):
        self.local_dest = dest
        self.instance = instance
        self.attr = attr
        self.static_type = static_type


class SetAttrNode(InstructionNode):
    def __init__(self, instance, attr, value, static_type):
        self.instance = instance
        self.attr = attr
        self.value = value
        self.static_type = static_type


#Arrays and Strings
class GetIndexNode(InstructionNode):
    pass


class SetIndexNode(InstructionNode):
    pass

# Memory


class AllocateNode(InstructionNode):
    def __init__(self, typex, tag, dest):
        self.type = typex
        self.tag = tag
        self.local_dest = dest


class ArrayNode(InstructionNode):
    pass


class TypeOfNode(InstructionNode):
    def __init__(self, instance, dest):
        self.instance = instance
        self.local_dest = dest

# Jumps


class LabelNode(InstructionNode):
    def __init__(self, label):
        self.label = label


class GoToNode(InstructionNode):
    def __init__(self, label):
        self.label = label


class IfGoToNode(InstructionNode):
    def __init__(self, condition, label):
        self.condition = condition
        self.label = label


# Dynamic Invocation
class CallNode(InstructionNode):
    def __init__(self, local_dest, function, params, static_type):
        self.function = function
        self.params = params
        self.static_type = static_type
        self.local_dest = local_dest


# Static Invocation
class VCallNode(InstructionNode):
    def __init__(self, local_dest, function, params, dynamic_type, instance):
        self.function = function
        self.params = params
        self.dynamic_type = dynamic_type
        self.local_dest = local_dest
        self.instance = instance


# Args
class ArgNode(InstructionNode):
    def __init__(self, name):
        self.name = name


# Return
class ReturnNode(InstructionNode):
    def __init__(self, value):
        self.value = value


# IO
class LoadIntNode(InstructionNode):
    def __init__(self, value, dest):
        self.value = value
        self.local_dest = dest


class LoadStringNode(InstructionNode):
    def __init__(self, msg, dest):
        self.msg = msg
        self.local_dest = dest


class LoadVoidNode(InstructionNode):
    def __init__(self, dest):
        self.local_dest = dest


class LengthNode(InstructionNode):
    def __init__(self, variable, result):
        self.variable = variable
        self.result = result


class ConcatNode(InstructionNode):
    def __init__(self, str1, len1, str2, len2, result):
        self.str1 = str1
        self.len1 = len1
        self.str2 = str2
        self.len2 = len2
        self.result = result


class PrefixNode(InstructionNode):
    def __init__(self, dest, string, n):
        self.local_dest = dest
        self.string = string
        self.n = n


class SubstringNode(InstructionNode):
    def __init__(self, dest, string, begin, final):
        self.local_dest = dest
        self.begin = begin
        self.string = string
        self.final = final


class StrNode(InstructionNode):
    def __init__(self, dest, value):
        self.local_dest = dest
        self.value = value


class ReadStringNode(InstructionNode):
    def __init__(self, dest):
        self.local_dest = dest


class ReadIntNode(InstructionNode):
    def __init__(self, dest):
        self.local_dest = dest


class PrintStringNode(InstructionNode):
    def __init__(self, value):
        self.value = value


class PrintIntNode(InstructionNode):
    def __init__(self, value):
        self.value = value


class IsVoidNode(InstructionNode):
    def __init__(self, result_local, expr):
        self.result_local = result_local
        self.expr = expr


class HaltNode(InstructionNode):
    def __init__(self):
        pass


class CopyNode(InstructionNode):
    def __init__(self, typex, local_dest):
        self.type = typex
        self.local_dest = local_dest


class StringEqualsNode(InstructionNode):
    def __init__(self, s1, s2, result):
        self.s1 = s1
        self.s2 = s2
        self.result = result
