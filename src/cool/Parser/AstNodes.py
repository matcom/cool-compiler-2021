class Node:
    pass

class ProgramNode(Node):
    def __init__(self, declarations):
        self.declarations = declarations
class DeclarationNode(Node):
    pass
class ExpressionNode(Node):
    pass

class ClassDeclarationNode(DeclarationNode):
    def __init__(self, idx, features, parent, row , column):
        self.id = idx
        self.parent = parent
        self.features = features
        self.place_holder = None
        self.row = row
        self.column = column


class FuncDeclarationNode(DeclarationNode):
    def __init__(self, idx, params, return_type, body, row, column):
        self.id = idx
        self.params = params
        self.type = return_type
        self.body = body
        self.place_holder = None
        self.row = row
        self.column = column

class IfNode(ExpressionNode):
    def __init__(self,ifexp, thenexp,elseexp, row, column):
        self.ifexp = ifexp
        self.thenexp = thenexp
        self.elseexp = elseexp
        self.place_holder = None
        self.row = row
        self.column = column

class WhileNode(ExpressionNode):
    def __init__(self, condition, body, row, column):
        self.condition = condition
        self.body = body
        self.place_holder = None
        self.row = row
        self.column = column

class CaseNode(ExpressionNode):
    def __init__(self,case,body, row, column):
        self.case = case
        self.body = body
        self.place_holder = None
        self.row = row
        self.column = column

class LetNode(ExpressionNode):
    def __init__(self, params, body, row, column):
        self.params = params
        self.body = body
        self.place_holder = None
        self.row = row
        self.column = column

class ExpressionGroupNode(ExpressionNode):
    def __init__(self, body, row, column):
        self.body = body
        self.place_holder = None
        self.row = row
        self.column = column

class AttrDeclarationNode(DeclarationNode):
    def __init__(self, idx, typex, expr, row = 0, column = 0):
        self.id = idx
        self.type = typex
        self.expr = expr
        self.place_holder = None
        self.row = row
        self.column = column

class ParamDeclarationNode(DeclarationNode):
    def __init__(self, idx, typex, row = 0, column = 0):
        self.id = idx
        self.type = typex
        self.row = row
        self.column = column

class VarDeclarationNode(ExpressionNode): #Case expr
    def __init__(self, idx, typex, expr, row = 0, column = 0):
        self.id = idx
        self.type = typex
        self.expr = expr
        self.place_holder = None
        self.row = row
        self.column = column
        
class LetDeclarationNode(ExpressionNode): #Let expr
    def __init__(self, idx, typex, expr, row = 0, column = 0):
        self.id = idx
        self.type = typex
        self.expr = expr
        self.place_holder = None
        self.row = row
        self.column = column

class AssignNode(ExpressionNode):
    def __init__(self, idx, expr, row, column):
        self.id = idx
        self.expr = expr
        self.place_holder = None
        self.row = row
        self.column = column

class CallNode(ExpressionNode):
    def __init__(self, obj, idx, args, parent,call_type, row = 0, column = 0):
        self.obj = obj
        self.id = idx
        self.args = args
        self.parent = parent
        self.place_holder = None
        self.call_type = call_type
        self.row = row
        self.column = column

class ExpressionGroupNode(ExpressionNode):
    def __init__(self, body, row, column):
        self.body = body
        self.place_holder = None
        self.row = row
        self.column = column

class AtomicNode(ExpressionNode):
    def __init__(self, lex, row, column):
        self.lex = lex
        self.place_holder = None
        self.row = row
        self.column = column

class BinaryNode(ExpressionNode):
    def __init__(self, tok, left, right, row, column):
        self.left = left
        self.right = right
        self.lex = tok.value
        self.row = row
        self.column = column
        
class BinaryIntNode(BinaryNode):
    pass
class BinaryBoolNode(BinaryNode):
    pass

class UnaryNode(ExpressionNode):
    def __init__(self,right, row, column):
        self.right = right
        self.place_holder = None
        self.row = row
        self.column = column

class StringNode(AtomicNode):
    pass
class ConstantNumNode(AtomicNode):
    pass
class VariableNode(AtomicNode):
    pass
class InstantiateNode(AtomicNode):
    pass
class BooleanNode(AtomicNode):
    pass
class SelfNode(AtomicNode):
    pass
class PlusNode(BinaryIntNode):
    pass
class MinusNode(BinaryIntNode):
    pass
class StarNode(BinaryIntNode):
    pass
class DivNode(BinaryIntNode):
    pass
class EqualNode(BinaryNode):
    pass
class LessEqual(BinaryBoolNode):
    pass
class LessNode(BinaryBoolNode):
    pass
class IsVoidNode(UnaryNode):
    pass
class NotNode(UnaryNode):
    pass
class NegateNode(UnaryNode):
    pass