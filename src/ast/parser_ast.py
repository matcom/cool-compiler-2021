from typing import List, Tuple


class Node:
    def __init__(self) -> None:
        self.line = 0
        self.col = 0

    def get_position(self) -> Tuple[int, int]:
        return self.line, self.col

    def set_position(self, line: int, col: int) -> None:
        self.line = line
        self.col = col


class ProgramNode(Node):
    def __init__(self, declarations):
        Node.__init__(self)
        self.declarations = declarations


class DeclarationNode(Node):
    pass


class ClassDeclarationNode(DeclarationNode):
    def __init__(self, idx, features, parent=None):
        Node.__init__(self)
        self.id = idx
        self.parent = parent
        self.features = features


class AttrDeclarationNode(DeclarationNode):
    def __init__(self, idx, typex, expression=None):
        Node.__init__(self)
        self.id = idx
        self.type = typex
        self.expr = expression


class MethodDeclarationNode(DeclarationNode):
    def __init__(self, idx, params, return_type, body):
        Node.__init__(self)
        self.id = idx
        self.params: List[VarDeclarationNode] = params
        self.type = return_type
        self.body = body


class ExpressionNode(Node):
    pass


class VarDeclarationNode(ExpressionNode):
    def __init__(self, idx, typex, expression=None):
        Node.__init__(self)
        self.id = idx
        self.type = typex
        self.expr = expression

class ParamNode(ExpressionNode):
     def __init__(self, idx, typex):
        Node.__init__(self)
        self.id = idx
        self.type = typex


class AssignNode(ExpressionNode):
    def __init__(self, idx, expr):
        Node.__init__(self)
        self.id = idx
        self.expr = expr


class MethodCallNode(ExpressionNode):
    def __init__(self, expr=None, typex=None, idx=None, args=None):
        Node.__init__(self)
        self.expr = expr
        self.type = typex
        self.id = idx
        self.args = args


class ConditionalNode(ExpressionNode):
    def __init__(
        self,
        condition: ExpressionNode,
        then_body: ExpressionNode,
        else_body: ExpressionNode,
    ):
        Node.__init__(self)
        self.condition = condition
        self.then_body = then_body
        self.else_body = else_body


class LoopNode(ExpressionNode):
    def __init__(self, condition: ExpressionNode, body: ExpressionNode):
        Node.__init__(self)
        self.condition = condition
        self.body = body


class LetNode(ExpressionNode):
    def __init__(
        self, var_decl_list: List[VarDeclarationNode], in_expr: ExpressionNode
    ):
        Node.__init__(self)
        self.var_decl_list = var_decl_list
        self.in_expr = in_expr


class CaseNode(ExpressionNode):
    def __init__(self, case_expr, options):
        Node.__init__(self)
        self.case_expr = case_expr
        self.options: List[CaseOptionNode] = options


class CaseOptionNode(ExpressionNode):
    def __init__(self, idx, typex, ret_expr):
        Node.__init__(self)
        self.id = idx
        self.type = typex
        self.expr = ret_expr


class BlocksNode(ExpressionNode):
    def __init__(self, expr_list):
        Node.__init__(self)
        self.expr_list = expr_list


class UnaryNode(ExpressionNode):
    def __init__(self, expr):
        Node.__init__(self)
        self.expr = expr


class IsVoidNode(UnaryNode):
    pass


class NotNode(UnaryNode):
    pass


class ComplementNode(UnaryNode):
    pass


class BinaryNode(ExpressionNode):
    def __init__(self, left, right):
        Node.__init__(self)
        self.left = left
        self.right = right


class ComparerNode(BinaryNode):
    pass


class LessNode(ComparerNode):
    pass


class LessOrEqualNode(ComparerNode):
    pass


class EqualsNode(ComparerNode):
    pass


class ArithmeticNode(BinaryNode):
    pass


class PlusNode(ArithmeticNode):
    pass


class MinusNode(ArithmeticNode):
    pass


class StarNode(ArithmeticNode):
    pass


class DivNode(ArithmeticNode):
    pass


class AtomicNode(ExpressionNode):
    def __init__(self, value):
        Node.__init__(self)
        self.value = value


class BooleanNode(AtomicNode):
    pass


class IntNode(AtomicNode):
    pass


class StringNode(AtomicNode):
    pass


class VariableNode(AtomicNode):
    pass


class InstantiateNode(AtomicNode):
    pass
