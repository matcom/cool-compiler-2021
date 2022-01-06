class ASTNode:
    def __init__(self):
        pass
    def __repr__(self):
        return str(self)

class ProgramNode(ASTNode):
    def __init__(self, dottypes, dotdata, dotcode):
        self.dottypes = dottypes
        self.dotdata = dotdata
        self.dotcode = dotcode

#.TYPE
class TypeNode(ASTNode):
    def __init__(self, name):
        self.name = name
        self.attributes = []
        self.methods = {}

#.DATA
class DataNode(ASTNode):
    def __init__(self, vname, value):
        self.name = vname
        self.value = value
        
#.CODE
class FunctionNode(ASTNode):
    def __init__(self, name, params=[], localvars=[], instructions =[]):
        self.name = name
        self.params = params
        self.localvars = localvars
        self.instructions = instructions

class ExpressionNode(ASTNode):
    def __init__(self):
        pass

#sin type expression
class ParamNode(ExpressionNode):
    def __init__(self, name):
        self.name = name

class LocalNode(ExpressionNode):
    def __init__(self, name):
        self.name = name

class AssignNode(ExpressionNode):
    def __init__(self, dest, expr):
        self.dest = dest
        self.expr = expr

class ArithExpressionNode(ExpressionNode):
    def __init__(self, dest, left, right):
        self.dest = dest
        self.left = left
        self.right = right

#Arith
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

#Attr
class GetAttrNode(ExpressionNode):
    def __init__(self, dest, instance, attr, static_type):
        self.local_dest = dest
        self.instance = instance
        self.attr = attr
        self.static_type = static_type
        
class SetAttrNode(ExpressionNode):
    def __init__(self, instance, attr, value, static_type):
        self.instance = instance
        self.attr = attr
        self.value = value
        self.static_type = static_type


#Arrays and Strings
class GetIndexNode(ExpressionNode):
    pass
class SetIndexNode(ExpressionNode):
    pass

#Memory
class AllocateNode(ExpressionNode):
    def __init__(self, t, dest):
        self.type = t
        self.local_dest = dest
        
class ArrayNode(ExpressionNode):
    pass

class TypeOfNode(ExpressionNode):
    def __init__(self, t, dest):
        self.var = t
        self.local_dest = dest

#Jumps
class LabelNode(ExpressionNode):
    def __init__(self, label):
        self.label = label

class GoToNode(ExpressionNode):
    def __init__(self, label):
        self.label = label

class IfGoTo(ExpressionNode):
    def __init__(self, condition, label):
        self.condition = condition
        self.label = label

#Static Invocation
class CallNode(ExpressionNode):
    def __init__(self, dest, func, args, static_type, ret_type):
        self.local_dest = dest
        self.function = func
        self.args = args
        self.static_type = static_type
        self.ret_type = ret_type

#Dynamic Invocation
class VCallNode(ExpressionNode):
    def __init__(self, instance, dest, func, args, dynamic_type, ret_type):
        self.instance = instance
        self.local_dest = dest
        self.function = func
        self.args = args
        self.dynamic_type = dynamic_type
        self.ret_type = ret_type


#Args
class ArgNode(ExpressionNode):
    def __init__(self, name):
        self.name = name


#Return
class ReturnNode(ExpressionNode):
    def __init__(self, value):
        self.value = value

#IO
class LoadNode(ExpressionNode):
    def __init__(self, dest, msg):
        self.local_dest = dest
        self.msg = msg

class LengthNode(ExpressionNode):
    def __init__(self, dest, arg):
        self.local_dest = dest
        self.arg = arg
        
class ConcatNode(ExpressionNode):
    def __init__(self, dest, head, tail):
        self.local_dest = dest
        self.head = head
        self.tail = tail

class PrefixNode(ExpressionNode):
    def __init__(self, dest, string, n):
        self.local_dest = dest
        self.string = string
        self.n = n

class SubstringNode(ExpressionNode):
    def __init__(self, dest, string, begin, final):
        self.local_dest = dest
        self.begin = begin
        self.string = string
        self.final = final

class StrNode(ExpressionNode):
    def __init__(self, dest, value):
        self.local_dest = dest
        self.value = value

class ReadNode(ExpressionNode):
    def __init__(self, dest):
        self.local_dest = dest

class PrintNode(ExpressionNode):
    def __init__(self, value):
        self.value = value