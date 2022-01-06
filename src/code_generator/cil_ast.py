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




