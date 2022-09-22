from .semantic import Scope

class Token:
    def __init__(self, type, value, line, lexpos):
        self.type = type
        self.value = value
        self.line = line
        self.lexpos = lexpos

class Node:
    line: int
    lexpos: int
    scope: Scope

    def set_line_lexpos(self, line, lexpos):
        self.line = line
        self.lexpos = lexpos
        
    def set_position(self, line, lexpos):
        self.line = line
        self.lexpos = lexpos
        return self

class DeclarationNode(Node):
    pass

class ExprNode(Node):
    pass

class ProgramNode(Node):
    def __init__(self, class_list):
        self.class_list = class_list
        

class ClassDecNode(DeclarationNode):
    def __init__(self, name, data, parent=None):
        self.name = name
        self.parent = parent
        self.data = data

        self.parent_pos = (-1, -1)

class AttributeDecNode(DeclarationNode):
    def __init__(self, name, _type, expr=None):
        self.name = name
        self._type = _type
        self.expr = expr
        self.type_pos = (-1, -1)
        self.expr_pos = (-1, -1)
        
class MethodDecNode(DeclarationNode):
    def __init__(self, name, _type, expr, params=None):
        self.name = name
        self.params = params
        self.type = _type
        self.expr = expr

        self.p_types_pos = []
        self.r_types_pos = (-1, -1)

class ParamNode(ExprNode):
    def __init__(self, name, _type):
        self.name = name
        self.type = _type

class WhileNode(ExprNode):
    def __init__(self, cond, data):
        self.cond = cond
        self.data = data
            
class LetNode(ExprNode):
    def __init__(self, declaration, expr):
        self.declaration = declaration
        self.expr = expr
        self.dec_names_pos = []
        self.dec_types_pos = []


class CaseNode(ExprNode):
    def __init__(self, expr, params):
        self.expr = expr
        self.params = params
        self.cases_positions = []

class AssignNode(ExprNode):
    def __init__(self, idx, expr):
        self.idx = idx
        self.expr = expr

class ParenthesisNode(ExprNode):
    def __init__(self, expr):
        self.expr = expr

class BlockNode(ExprNode):
    def __init__(self, expr):
        self.expr = expr

class MethodCallNode(ExprNode):
    def __init__(self, idx, exprlist, atom=None, typex=None):
        self.idx = idx
        self.exprlist = exprlist
        self.atom = atom
        self.type = typex
        self.id_position = (-1, -1)
        self.type_position = (-1, -1)
        self.exprlist_positions = []

class ConditionalNode(ExprNode):
    def __init__(self, if_expr, then_expr, else_expr):
        self.if_expr = if_expr
        self.then_expr = then_expr
        self.else_expr = else_expr

class IsVoidNode(ExprNode):
    def __init__(self, expr):
        self.expr = expr

class NewNode(ExprNode):
    def __init__(self, type_):
        self.type = type_
        self.type_position = (-1, -1)

class ExprParNode(ExprNode):
    def __init__(self, expr):
        self.expr = expr
        self.expr_pos = (-1, -1)

class AtomicNode(ExprNode):
    def __init__(self, lex):
        self.lex: str = lex

class UnaryNode(ExprNode):
    def __init__(self, expr):
        self.expr: ExprNode = expr
        self.operation_position = (-1, -1)

class BinaryNode(ExprNode):
    def __init__(self, left, operation, right):
        self.left: ExprNode = left
        self.operation: str = operation
        self.right: ExprNode = right           

class PlusNode(BinaryNode):
    pass

class MinusNode(BinaryNode):
    pass

class DivNode(BinaryNode):
    pass

class TimesNode(BinaryNode):
    pass

class LessNode(BinaryNode):
    pass

class LessEqualNode(BinaryNode):
    pass

class EqualNode(BinaryNode):
    pass

class NegationNode(UnaryNode):
    pass

class ComplementNode(UnaryNode):
    pass

class VariableNode(AtomicNode):
    pass

class NumberNode(AtomicNode):
    pass

class StringNode(AtomicNode):
    pass

class BooleanNode(AtomicNode):
    pass
