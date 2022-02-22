class Node:
    pass


class ProgramNode(Node):
    def __init__(self, location, declarations):
        self.location = location
        self.declarations = declarations


class DeclarationNode(Node):
    pass


class ExpressionNode(Node):
    pass


# Class
class ClassDeclarationNode(DeclarationNode):
    def __init__(self, location, idx, features, parent=None, parent_location=None):
        self.location = location
        self.id, self.id_location = idx
        self.parent = parent
        self.features = features
        self.parent_location = parent_location


# Features
class FuncDeclarationNode(DeclarationNode):
    def __init__(self, location, idx, params, return_type, body):
        self.location = location
        self.id = idx
        self.params = params
        self.type, self.type_location = return_type
        self.expr = body


class AttrDeclarationNode(DeclarationNode):
    def __init__(self, location, idx, typex, expr=None):
        self.location = location
        self.id = idx
        self.type, self.type_location = typex
        self.expr = expr


class VarDeclarationNode(ExpressionNode):
    def __init__(self, location, idx, typex, expr=None):
        self.location = location
        self.id = idx
        self.type, self.type_location = typex
        self.expr = expr


class AssignNode(ExpressionNode):
    def __init__(self, location, symbol_location, idx, expr):
        self.location = location
        self.symbol_location = symbol_location
        self.id = idx
        self.expr = expr
       

class DispatchNode(ExpressionNode):
    def __init__(self, location, obj, idx, args, from_type=None):
        self.location = location
        self.expr = obj
        self.id = idx
        self.arg = args
        self.type = from_type


class BinaryNode(ExpressionNode):
    def __init__(self, location, symbol_location, left, right):
        self.symbol_location = symbol_location
        self.location = location
        self.left = left
        self.right = right


class UnaryNode(ExpressionNode):
    def __init__(self, location, exp):
        self.location = location
        self.expr = exp


class ConditionalNode(ExpressionNode):
    def __init__(self, location, if_exp, then_exp, else_exp):
        self.location = location
        self.predicate = if_exp
        self.then = then_exp
        self.elsex = else_exp


class LoopNode(ExpressionNode):
    def __init__(self, location, while_exp, loop_exp):
        self.location = location
        self.predicate = while_exp
        self.body = loop_exp


class BlockNode(ExpressionNode):
    def __init__(self, location, exp_list):
        self.location = location
        self.expr_lis = exp_list


class LetNode(ExpressionNode):
    def __init__(self,location, var_list, in_exp):
        self.location = location
        self.variables = var_list
        self.expr = in_exp


class CaseNode(ExpressionNode):
    def __init__(self,location, cond, case_list):
        self.location = location
        self.expr = cond
        self.cases = case_list


class CaseAttrNode(ExpressionNode):
    def __init__(self, location, idx, typex, expr):
        self.location = location
        self.id = idx
        self.type, self.type_location = typex
        self.expr = expr


class AtomicNode(ExpressionNode):
    def __init__(self, location, lex):
        self.location = location
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
