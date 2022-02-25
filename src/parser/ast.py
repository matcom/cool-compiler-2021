from lexer.lexer import *
from ply.lex import LexToken

class Node:
    def __init__(self):
        self.lineno = 0
        self.colno = 0


class ProgramNode(Node):
    def __init__(self, p, classes):
        super().__init__()
        self.classes = p[classes]


class ClassDeclarationNode(Node):
    def __init__(self, p, pos, type, features, parent_type=None):
        super().__init__()
        self.type = p[type]
        self.feature_nodes = p[features]
        self.parent_type = p[parent_type] if parent_type else parent_type
        self.lineno = p.lineno(pos)
        self.colno = find_column1(p, pos)


class BlockNode(Node):
    def __init__(self, p):
        super().__init__()
        self.returned_type = None
        self.expressions = [p[1]] + p[3].expressions if len(p) == 4 else [p[1]]


class DataNode(Node):
    def __init__(self, p, pos, id):
        super().__init__()
        self.id = p[id]
        self.lineno = p.lineno(pos)
        self.colno = find_column1(p, pos)


class AttrDeclarationNode(DataNode):
    def __init__(self, p, pos, id, type, expr=None):
        super().__init__(p, pos, id)
        self.type = p[type]
        self.expr = p[expr] if expr else expr
    

class FuncDeclarationNode(DataNode):
    def __init__(self, p, pos, id, params, return_type, expressions):
        super().__init__(p, pos, id)
        self.params = p[params]
        self.return_type = p[return_type]
        self.expressions = p[expressions]


class ExpressionNode(Node):
    def __init__(self, p, pos):
        super().__init__()
        self.returned_type = None
        if p or pos:
            self.lineno = p.lineno(pos)
            self.colno = find_column1(p, pos)


class LetNode(ExpressionNode):
    def __init__(self, p, pos, let_attrs, expr):
        super().__init__(p, pos)
        self.let_attrs = p[let_attrs]
        self.expr = p[expr]


class CaseNode(ExpressionNode):
    def __init__(self, p, pos, expr, case_list):
        super().__init__(p, pos)
        self.expr = p[expr]
        self.case_list = p[case_list]


class IfNode(ExpressionNode):
    def __init__(self, p, pos, if_expr, then_expr, else_expr):
        super().__init__(p, pos)
        self.if_expr = p[if_expr]
        self.then_expr = p[then_expr]
        self.else_expr = p[else_expr]


class WhileNode(ExpressionNode):
    def __init__(self, p, pos, cond, body):
        super().__init__(p, pos)
        self.cond = p[cond]
        self.body = p[body]


class AssignNode(ExpressionNode):
    def __init__(self, p, pos, id, expr):
        super().__init__(p, pos)
        self.id = p[id]
        self.expr = p[expr]


class FuncCallNode(ExpressionNode):
    def __init__(self, p, pos, id, args, object=None, type=None):
        super().__init__(p, pos)
        self.object = p[object] if object else None
        self.type = p[type] if type else None
        self.id = p[id]
        self.args = p[args]
        self.self_type = None


class BinaryNode(ExpressionNode):
    def __init__(self, p, pos, lvalue, rvalue):
        super().__init__(p, pos)
        self.lvalue = p[lvalue]
        self.rvalue = p[rvalue]


class UnaryNode(ExpressionNode):
    def __init__(self, p, pos, val):
        super().__init__(p, pos)
        self.val = p[val]


class CaseElemNode(ExpressionNode):
    def __init__(self, p, pos, expr, id, type):
        super().__init__(p, pos)
        self.expr = p[expr]
        self.id = p[id]
        self.type = p[type]


class VarNode(ExpressionNode):
    def __init__(self, p, pos, id):
        super().__init__(p, pos)
        self.id = p[id]


class NewNode(ExpressionNode):
    def __init__(self, p, pos, type):
        super().__init__(p, pos)
        self.type = p[type] if p else type


class ConstantNode(ExpressionNode):
    def __init__(self, p, pos, isInt, value):
        super().__init__(p, pos)
        self.value = int(p[value]) if isInt else p[value]


class PlusNode(BinaryNode):
    pass


class MinusNode(BinaryNode):
    pass


class MultNode(BinaryNode):
    pass


class DivNode(BinaryNode):
    pass


class LessThanNode(BinaryNode):
    pass


class LessEqualNode(BinaryNode):
    pass


class EqualNode(BinaryNode):
    pass


class IntCompNode(UnaryNode):
    pass


class NotNode(UnaryNode):
    pass


class AtomNode(UnaryNode):
    pass


class IsVoidNode(UnaryNode):
    pass


class IntNode(ConstantNode):
    pass


class BoolNode(ConstantNode):
    pass


class StringNode(ConstantNode):
    pass

