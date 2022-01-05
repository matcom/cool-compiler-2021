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

