from cmath import exp
from select import select


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
        self.line = idx.lineno
        self.col = idx.column
        self.features = features
        if parent:
            self.parent = parent.value
            self.parentLine = parent.lineno
            self.parentCol = parent.column
        else:
            self.parent = None
            self.parentLine = 0
            self.parentCol = 0


class FuncDeclarationNode(DeclarationNode):
    def __init__(self, idx, params, return_type, body):
        self.id = idx.value
        self.line = idx.lineno
        self.col = idx.column
        self.params = [(pname.value, ptype.value, ptype.lineno,
                        ptype.column) for pname, ptype in params]
        self.type = return_type.value
        self.typeLine = return_type.lineno
        self.typeCol = return_type.column
        self.body = body


class AttrDeclarationNode(DeclarationNode):
    def __init__(self, idx, typex, expr=None):
        self.id = idx.value
        self.line = idx.lineno
        self.col = idx.column
        self.type = typex.value
        self.typeLine = typex.lineno
        self.typeCol = typex.column
        self.expr = expr


class ExpressionNode(Node):
    pass


class AssignNode(ExpressionNode):
    def __init__(self, idx, expr):
        self.id = idx.value
        self.line = idx.lineno
        self.col = idx.column
        self.expr = expr


class ArrobaCallNode(ExpressionNode):
    def __init__(self, obj, idx, args, typex):
        self.obj = obj
        self.id = idx.value
        self.line = idx.lineno
        self.col = idx.column
        self.args = args
        self.type = typex.value
        self.typeLine = typex.lineno
        self.typeCol = typex.column


class DotCallNode(ExpressionNode):
    def __init__(self, obj, idx, args):
        self.obj = obj
        self.id = idx.value
        self.line = idx.lineno
        self.col = idx.column
        self.args = args


class MemberCallNode(ExpressionNode):
    def __init__(self, idx, args):
        self.id = idx.value
        self.line = idx.lineno
        self.col = idx.column
        self.args = args


class IfThenElseNode(ExpressionNode):
    def __init__(self, condition, ifBody, elseBody, token):
        self.condition = condition
        self.ifBody = ifBody
        self.elseBody = elseBody
        self.line = token.lineno
        self.col = token.column


class WhileNode(ExpressionNode):
    def __init__(self, condition, body, token):
        self.condition = condition
        self.body = body
        self.line = token.lineno
        self.col = token.column


class BlockNode(ExpressionNode):
    def __init__(self, exprs, token):
        self.exprs = exprs
        self.line = token.lineno
        self.col = token.column


class LetInNode(ExpressionNode):
    def __init__(self, letBody, inBody, token):
        self.letBody = letBody
        self.inBody = inBody
        self.line = token.lineno
        self.col = token.column


class CaseNode(ExpressionNode):
    def __init__(self, expr, caseList, token):
        self.expr = expr
        self.caseList = caseList
        self.line = token.lineno
        self.col = token.column


class CaseOptionNode(ExpressionNode):
    def __init__(self, idx, typex, expr):
        self.id = idx.value
        self.line = idx.lineno
        self.col = idx.column
        self.type = typex.value
        self.typeLine = typex.lineno
        self.typeCol = typex.column

        # ---------------- Binary Nodes ------------------


class BinaryNode(ExpressionNode):
    def __init__(self, lvalue, rvalue):
        self.lvalue = lvalue
        self.rvalue = rvalue
        self.line = lvalue.line
        self.col = lvalue.col


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
        self.line = token.lineno
        self.column = token.column


class NegationNode(UnaryNode):
    pass


class LogicNegationNode(UnaryNode):
    pass


class IsVoidNode(UnaryNode):
    pass


# ---------------- Atomic Nodes ------------------

class AtomicNode(ExpressionNode):
    def __init__(self, token):
        try:
            self.id = token.value
            self.line = token.lineno
            self.col = token.column
        except:
            self.id = token
            self.line = 0
            self.col = 0


class NewNode(AtomicNode):
    pass


class IdNode(AtomicNode):
    pass


class IntNode(AtomicNode):
    pass


class BoolNode(AtomicNode):
    pass


class StringNode(AtomicNode):
    pass
