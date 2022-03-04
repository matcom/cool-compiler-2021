from cmp.semantic import Context
from cmp.utils import Token 

class Node:
    def __init__(self, token):
        self.token = token


class ProgramNode(Node):
    def __init__(self,  declarations, context=None):
        super().__init__(Token("", "", (0,0))) # symbolic initial token
        self.declarations = declarations
        self.context = context


class ExpressionNode(Node):
    pass


class ClassDeclarationNode:
    def __init__(self, idx, features, token, parent=None):
        self.id = idx
        self.parent = parent
        self.features = features
        self.token = token


class FuncDeclarationNode:
    def __init__(self, idx, params, return_type, body, token):
        self.id = idx
        self.params = params
        self.type = return_type
        self.body = body
        self.token = token


class AttrDeclarationNode:
    def __init__(self, idx, typex, init_exp=None, token = Token("", "", (0,0))):
        self.id = idx
        self.type = typex
        self.init_exp = init_exp
        self.token = token


class AssignNode(ExpressionNode):
    def __init__(self, idx, expr, token):
        self.id = idx
        self.expr = expr
        self.token = token


class LetNode(ExpressionNode):
    def __init__(self, identifiers, body, token):
        self.identifiers = identifiers
        self.body = body
        self.token = token


#No tiene uno asi
class VarDeclarationNode:
    def __init__(self, token, typex, expr=None):
        self.id = token.lex
        self.type = typex
        self.expr = expr
        self.token = token


class IfNode(ExpressionNode):
    def __init__(self, if_exp, then_exp, else_exp, token):
        self.if_expr = if_exp
        self.then_expr = then_exp
        self.else_expr = else_exp
        self.token = token


class WhileNode(ExpressionNode):
    def __init__(self, condition, body, token):
        self.condition = condition
        self.body = body
        self.token = token


class CaseNode(ExpressionNode):
    def __init__(self, exp, case_items, token):
        self.expr = exp
        self.case_items = case_items
        self.token = token

#este no existe en la otra jerarquia
class CaseItemNode(ExpressionNode):
    def __init__(self, idx, typex, exp, token):
        self.id = idx
        self.type = typex
        self.expr = exp
        self.token = token


class CallNode(ExpressionNode):
    def __init__(self, idx, args, obj=None, at_type=None, token = Token("", "", (-1,-1))):
        self.obj = obj
        self.id = idx
        self.args = args
        self.at_type = at_type
        if token.location[0] == -1:
            self.token = idx
        else:
            self.token = token


class BlockNode(ExpressionNode):
    def __init__(self, expression_list, token):
        self.expression_list = expression_list
        self.token = token
 

class AtomicNode(ExpressionNode):
    def __init__(self, token):
        self.lex = token.lex
        self.token = token


#aqui y abajo se llama symbol
class UnaryNode(ExpressionNode):
    def __init__(self, expr, token):
        self.expr = expr
        self.token = token


class BinaryNode(ExpressionNode):
    def __init__(self, left, right, token):
        self.left = left
        self.right = right
        self.token = token


class ArithmeticOperation(BinaryNode):
    pass


class ComparisonOperation(BinaryNode):
    pass


class ConstantNumNode(AtomicNode):
    pass


class VariableNode(AtomicNode):
    pass


class StringNode(AtomicNode):
    pass


class BooleanNode(AtomicNode):
    pass


class InstantiateNode(AtomicNode):
    def __init__(self, lex, token):
        self.lex = lex
        self.token = token


class NotNode(UnaryNode):
    pass


class IsvoidNode(UnaryNode):
    pass


class NegNode(UnaryNode):
    pass


class PlusNode(ArithmeticOperation):
    pass


class MinusNode(ArithmeticOperation):
    pass


class StarNode(ArithmeticOperation):
    pass


class DivNode(ArithmeticOperation):
    pass


class LessNode(ComparisonOperation):
    pass


class LessEqualNode(ComparisonOperation):
    pass


class EqualNode(ComparisonOperation):
    pass
