class Node:
    pass

class ProgramNode(Node):
    def __init__(self, declarations):
        self.declarations = declarations

class DeclarationNode(Node):
    pass

class ExpressionNode(Node):
    pass

# Class
class ClassDeclarationNode(DeclarationNode):
    def __init__(self, idx, features, parent=None):
        self.id = idx
        self.parent = parent
        self.features = features

# Features
class FuncDeclarationNode(DeclarationNode):
    def __init__(self, idx, params, return_type, body):
        self.id = idx
        self.params = params
        self.type = return_type
        self.expr = body

class AttrDeclarationNode(DeclarationNode):
    def __init__(self, idx, typex, expr=None):
        self.id = idx
        self.type = typex
        self.expr = expr

class VarDeclarationNode(ExpressionNode):
    def __init__(self, idx, typex, expr=None):
        self.id = idx
        self.type = typex
        self.expr = expr

class AssignNode(ExpressionNode):
    def __init__(self, idx, expr):
        self.id = idx
        self.expr = expr

class DispatchNode(ExpressionNode):
    def __init__(self, obj, idx, args, from_type=None):
        self.expr = obj
        self.id = idx
        self.arg = args
        self.type = from_type

class BinaryNode(ExpressionNode):
    def __init__(self, left, right):
        self.left = left
        self.right = right

class UnaryNode(ExpressionNode):
    def __init__(self, exp):
        self.expr = exp

class ConditionalNode(ExpressionNode):
    def __init__(self, if_exp, then_exp, else_exp):
        self.predicate = if_exp
        self.then = then_exp
        self.elsex = else_exp

class LoopNode(ExpressionNode):
    def __init__(self, while_exp, loop_exp):
        self.predicate = while_exp
        self.body = loop_exp

class BlockNode(ExpressionNode):
    def __init__(self, exp_list):
        self.expr_lis = exp_list

class LetNode(ExpressionNode):
    def __init__(self, var_list, in_exp):
        self.variables = var_list
        self.expr = in_exp

class CaseNode(ExpressionNode):
    def __init__(self, cond, case_list):
        self.expr = cond
        self.cases = case_list

class CaseAttrNode(ExpressionNode):
    def __init__(self, idx, typex, expr):
        self.id = idx
        self.type = typex
        self.expr = expr

class AtomicNode(ExpressionNode):
    def __init__(self, lex):
        self.lex = lex

# Atomic Expressions
class ConstantNumNode(AtomicNode):
    pass

class StringNode(AtomicNode):
    pass

class TrueNode(AtomicNode):
    pass

class FalseNode(AtomicNode):
    pass       

class VariableNode(AtomicNode):
    pass  

class InstantiateNode(AtomicNode):
    pass

# Arithmetic Operations
class PlusNode(BinaryNode):
    pass

class MinusNode(BinaryNode):
    pass

class StarNode(BinaryNode):
    pass

class DivNode(BinaryNode):
    pass

# Comparison Operations
class LessNode(BinaryNode):
    pass

class ElessNode(BinaryNode):
    pass  

class EqualsNode(BinaryNode):
    pass

# Unary Operations
class NotNode(UnaryNode):
    pass

class PrimeNode(UnaryNode):
    pass  

class IsVoidNode(UnaryNode): 
    pass




