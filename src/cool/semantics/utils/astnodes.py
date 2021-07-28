from typing import List, Union, Tuple, Optional

Feature = Union["MethodDeclarationNode", "AttrDeclarationNode"]


class Node:
    line: int
    column: int

    def set_main_position(self, line: int, col: int) -> "Node":
        self.line = line
        self.column = col
        return self


class ProgramNode(Node):
    def __init__(self, declarations: List["ClassDeclarationNode"]):
        self.declarations: List[ClassDeclarationNode] = declarations


class DeclarationNode(Node):
    pass


class ClassDeclarationNode(DeclarationNode):
    def __init__(self, idx: str, features: List[Feature], parent: Optional[str] = None):
        self.id: str = idx
        self.parent: str = parent
        self.features: List[Feature] = features

        self.parent_position: Tuple[int, int] = -1, -1


class MethodDeclarationNode(DeclarationNode):
    def __init__(
        self,
        idx: str,
        params: List[Tuple[str, str]],
        return_type: str,
        body: "ExprNode",
    ):
        self.id: str = idx
        self.params: List[Tuple[str, str]] = params
        self.return_type: str = return_type
        self.body: ExprNode = body

        self.param_types_positions: List[Tuple[int, int]] = []
        self.return_type_position: Tuple[int, int] = -1, -1


class AttrDeclarationNode(DeclarationNode):
    def __init__(self, idx: str, typex: str, expr: "ExprNode" = None):
        self.id: str = idx
        self.type: str = typex
        self.expr: ExprNode = expr

        self.type_position: Tuple[int, int] = -1, -1
        self.expr_position: Tuple[int, int] = -1, -1


class ExprNode(Node):
    pass


class ParenthesisExpr(ExprNode):
    def __init__(self, expr: "ExprNode"):
        self.expr: "ExprNode" = expr


class BlockNode(ExprNode):
    def __init__(self, expressions):
        self.expressions: List[ExprNode] = expressions


class LetNode(ExprNode):
    def __init__(self, declarations, expr):
        self.declarations: List[Tuple[str, str, Optional[ExprNode]]] = declarations
        self.expr: ExprNode = expr

        self.declaration_names_positions: List[Tuple[int, int]] = []
        self.declaration_types_positions: List[Tuple[int, int]] = []


class SwitchCaseNode(ExprNode):
    def __init__(self, expr, cases):
        self.expr: ExprNode = expr
        self.cases: List[Tuple[str, str, ExprNode]] = cases

        self.cases_positions: List[Tuple[int, int]] = []


class AssignNode(ExprNode):
    def __init__(self, idx, expr):
        self.id: str = idx
        self.expr: ExprNode = expr


class ConditionalNode(ExprNode):
    def __init__(self, ifx, then, elsex):
        self.if_expr: ExprNode = ifx
        self.then_expr: ExprNode = then
        self.else_expr: ExprNode = elsex


class WhileNode(ExprNode):
    def __init__(self, condition, body):
        self.condition: ExprNode = condition
        self.body: ExprNode = body


class MethodCallNode(ExprNode):
    def __init__(self, idx, args, obj=None, typex=None):
        self.obj: ExprNode = obj
        self.id: str = idx
        self.args: List[ExprNode] = args
        self.type: str = typex

        self.id_position: Tuple[int, int] = -1, -1
        self.type_position: Tuple[int, int] = -1, -1
        self.args_positions: List[Tuple[int, int]] = []


class AtomicNode(ExprNode):
    def __init__(self, lex):
        self.lex: str = lex


class UnaryNode(ExprNode):
    def __init__(self, expr):
        self.expr: ExprNode = expr

        self.operation_position: Tuple[int, int] = -1, -1


class BinaryNode(ExprNode):
    def __init__(self, left, operation, right):
        self.left: ExprNode = left
        self.operation: str = operation
        self.right: ExprNode = right


class VariableNode(AtomicNode):
    pass


class InstantiateNode(AtomicNode):
    def __init__(self, lex):
        super().__init__(lex)

        self.type_position: Tuple[int, int] = -1, -1


class IntegerNode(AtomicNode):
    pass


class StringNode(AtomicNode):
    pass


class BooleanNode(AtomicNode):
    pass


class NegationNode(UnaryNode):
    pass


class ComplementNode(UnaryNode):
    pass


class IsVoidNode(UnaryNode):
    pass


class PlusNode(BinaryNode):
    pass


class MinusNode(BinaryNode):
    pass


class StarNode(BinaryNode):
    pass


class DivNode(BinaryNode):
    pass


class LessThanNode(BinaryNode):
    pass


class LessEqualNode(BinaryNode):
    pass


class EqualNode(BinaryNode):
    pass
