from ply.lex import LexToken


class Node():
    pass


class ProgramNode(Node):
    def __init__(self, declarations):
        self.declarations = declarations


class DeclarationNode(Node):
    pass


class ClassDeclarationNode(DeclarationNode):
    def __init__(self, idx, features, parent=None):
        self.id = idx.value
        self.token = idx
        self.features = features
        self.position = (idx.lineno, idx.column)
        if parent:
            self.parent = parent.value
            self.parentPos = (parent.lineno, parent.column)
        else:
            self.parent = None
            self.parentPos = (0, 0)


class AttrDeclarationNode(DeclarationNode):
    def __init__(self, idx, typex, expr=None):
        self.id = idx.value
        self.position = (idx.lineno, idx.column)
        self.type = typex
        self.typePos = (typex.lineno, typex.column)
        self.expr = expr


class FuncDeclarationNode(DeclarationNode):
    def __init__(self, idx, params, returnType, body):
        self.id = idx.value
        self.position = (idx.lineno, idx.column)
        self.params = params
        self.type = returnType.value
        self.typePos = (returnType.lineno, returnType.column)
        self.body = body


class ExpressionNode(Node):
    pass


class AssignNode(ExpressionNode):
    def __init__(self, idx, expr):
        self.id = idx.value
        self.position = (idx.lineno, idx.column)
        self.expr = expr


class FuncCallNode(ExpressionNode):
    def __init__(self, obj, idx, args, typex):
        self.obj = obj
        self.id = idx.value
        self.position = (idx.lineno, idx.column)
        self.args = args
        self.type = typex.value
        self.typePos = (typex.lineno, typex.column)


class MemberCallNode(ExpressionNode):
    def __init__(self, obj, idx, args):
        self.obj = obj
        self.id = idx.value
        self.position = (idx.lineno, idx.column)
        self.args = args


class ConditionalNode(ExpressionNode):
    def __init__(self, condition, then_expr, else_expr, token):
        self.condition = condition
        self.then_expr = then_expr
        self.else_expr = else_expr
        self.position = (token.lineno, token.column)


class WhileNode(ExpressionNode):
    def __init__(self, condition, body, token):
        self.condition = condition
        self.body = body
        self.position = (token.lineno, token.column)


class BlockNode(ExpressionNode):
    def __init__(self, exprs, token):
        self.exprs = exprs
        self.position = (token.lineno, token.column)


class LetNode(ExpressionNode):
    def __init__(self, let_attrs, expr, token):
        self.let_attrs = let_attrs
        self.expr = expr
        self.position = (token.lineno, token.column)


class CaseNode(ExpressionNode):
    def __init__(self, expr, case_list, token):
        self.expr = expr
        self.case_list = case_list
        self.position = (token.lineno, token.column)


class CaseOptionNode(ExpressionNode):
    def __init__(self, idx, typex, expr):
        self.id = idx.value
        self.position = (idx.lineno, idx.column)
        self.type = typex
        self.typePos = (typex.lineno, typex.column)
        self.expr = expr


class VarDeclarationNode(ExpressionNode):
    def __init__(self, idx, typex, expr=None):
        self.id = idx.value
        self.position = (idx.lineno, idx.column)
        self.type = typex
        self.typePos = (typex.lineno, typex.column)
        self.expr = expr


class NewNode(ExpressionNode):
    def __init__(self, typex):
        self.type = typex
        self.typePos = (typex.lineno, typex.column)



# ---------------- Binary Nodes ------------------

class BinaryNode(ExpressionNode):
    def __init__(self, lvalue, rvalue):
        self.lvalue = lvalue
        self.rvalue = rvalue
        self.position = lvalue.position


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


class LessEqNode(BinaryNode):
    pass


class EqualNode(BinaryNode):
    pass


# ---------------- Unary Nodes ------------------

class UnaryNode(ExpressionNode):
    def __init__(self, expr, token):
        self.expr = expr
        self.position = (token.lineno, token.column)


class NegationNode(UnaryNode):
    pass


class LogicNegationNode(UnaryNode):
    pass


class IsVoidNode(UnaryNode):
    pass


# ---------------- Atomic Nodes ------------------

class AtomicNode(ExpressionNode):
    def __init__(self, lex):
        try:
            self.lex = lex.value
            self.position = (lex.lineno, lex.column)
        except:
            self.lex = lex
            self.position = (0, 0)

class IntNode(AtomicNode):
    pass


class BoolNode(AtomicNode):
    pass


class StringNode(AtomicNode):
    pass
