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
    def __init__(self, idx, features, parent=None):
        self.id = idx
        self.parent = parent
        self.features = features

class FuncDeclarationNode(DeclarationNode):
    def __init__(self, idx, params, return_type, body):
        self.id = idx
        self.params = params
        self.return_type = return_type
        self.body = body

class AttrDeclarationNode(DeclarationNode):
    def __init__(self, idx, typex, expr = None):
        self.id = idx
        self.type = typex
        self.expr = expr

class VarDeclarationNode(ExpressionNode):
    def __init__(self, idx, typex, expr):
        self.id = idx
        self.type = typex
        self.expr = expr

class AssignNode(ExpressionNode):
    def __init__(self, idx, expr):
        self.id = idx
        self.expr = expr

class CallNode(ExpressionNode):
    def __init__(self, obj, idx, args, from_type= None):
        self.obj = obj
        self.id = idx
        self.args = args
        self.from_type = from_type


class BinaryNode(ExpressionNode):
    def __init__(self, left, right):
        self.left = left
        self.right = right

class UnaryNode(ExpressionNode):
    def __init__(self, exp):
        self.exp = exp


class ConditionalNode(ExpressionNode):
    def __init__(self,if_exp,then_exp,else_exp):
        self.if_exp = if_exp
        self.then_exp = then_exp
        self.else_exp = else_exp

class LoopNode(ExpressionNode):
    def __init__(self,while_exp, loop_exp):
        self.while_exp = while_exp
        self.loop_exp = loop_exp

class BlockNode(ExpressionNode):
    def __init__(self,exp_list):
        self.exp_list = exp_list

class LetNode(ExpressionNode):
    def __init__(self, var_list, in_exp):
        self.var_list = var_list
        self.in_exp = in_exp

class CaseNode(ExpressionNode):
    def __init__(self,cond, case_list):
        self.cond = cond
        self.case_list = case_list


class AtomicNode(ExpressionNode):
    def __init__(self, lex):
        self.lex = lex


class ConstantNumNode(AtomicNode):
    pass

class ConstantStringNode(AtomicNode):
    pass

class ConstantBoolNode(AtomicNode):
    pass

class VariableNode(AtomicNode):
    pass

class InstantiateNode(AtomicNode):
    pass

class IsVoidNode(UnaryNode):
    pass

class NotNode(UnaryNode):
    pass

class NegNode(UnaryNode):
    pass


class PlusNode(BinaryNode):
    pass

class MinusNode(BinaryNode):
    pass

class StarNode(BinaryNode):
    pass

class DivNode(BinaryNode):
    pass

class LessNode(BinaryNode):
    pass

class LessEqualNode(BinaryNode):
    pass

class EqualNode(BinaryNode):
    pass

