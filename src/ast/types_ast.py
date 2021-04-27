from typing import List, Tuple


class Node:
    def __init__(self, node) -> None:
        self.line = node.line
        self.col = node.col
        self.type = None

    def get_position(self) -> Tuple[int, int]:
        return self.line, self.col


class ProgramNode(Node):
    def __init__(self, declarations, node: Node):
        Node.__init__(self, node)
        self.declarations = declarations


class DeclarationNode(Node):
    pass


class ClassDeclarationNode(DeclarationNode):
    def __init__(self, features, node):
        Node.__init__(self, node)
        self.features = features
        self.id = node.id


class AttrDeclarationNode(DeclarationNode):
    def __init__(self, node):
        Node.__init__(self, node)
        self.id = node.id
        self.expr = None


class MethodDeclarationNode(DeclarationNode):
    def __init__(self, params, return_type, body, node):
        Node.__init__(self, node)
        self.id = node.id
        self.params: List[VarDeclarationNode] = params
        self.type = return_type
        self.body = body


class ExpressionNode(Node):
    pass


class BlocksNode(ExpressionNode):
    def __init__(self, expr_list, node):
        Node.__init__(self, node)
        self.expr_list = expr_list


class ConditionalNode(ExpressionNode):
    def __init__(self, condition, then_node, else_node, node):
        Node.__init__(self, node)
        self.condition = condition
        self.then_body = then_node
        self.else_body = else_node


class CaseNode(ExpressionNode):
    def __init__(self, case_expr, options, node):
        Node.__init__(self, node)
        self.case_expr = case_expr
        self.options: List[CaseOptionNode] = options


class CaseOptionNode(ExpressionNode):
    def __init__(self, ret_expr, node):
        Node.__init__(self, node)
        self.id = node.id
        self.decl_type = node.decl_type
        self.expr = ret_expr


class LoopNode(ExpressionNode):
    def __init__(self, condition, body, node):
        Node.__init__(self, node)
        self.condition = condition
        self.body = body


class LetNode(ExpressionNode):
    def __init__(self, var_decl_list, in_expr, node):
        Node.__init__(self, node)
        self.var_decl_list = var_decl_list
        self.in_expr = in_expr


class VarDeclarationNode(ExpressionNode):
    def __init__(self, node):
        Node.__init__(self, node)
        self.id = node.id
        self.expr = None  # Expression is set later if it exists
        self.index = None


class AssignNode(ExpressionNode):
    def __init__(self, expr, node):
        Node.__init__(self, node)
        self.id = node.id
        self.expr = expr
        self.defined = False


class MethodCallNode(ExpressionNode):
    def __init__(self, caller_type, expr, args, node):
        Node.__init__(self, node)
        self.caller_type = caller_type
        self.expr = expr
        self.args = args
        self.id = node.id
        self.at_type = node.at_type


class UnaryNode(ExpressionNode):
    def __init__(self, expr, node):
        Node.__init__(self, node)
        self.expr = expr


class IsVoidNode(UnaryNode):
    pass


class NotNode(UnaryNode):
    pass


class ComplementNode(UnaryNode):
    pass


class BinaryNode(ExpressionNode):
    def __init__(self, left, right, node):
        Node.__init__(self, node)
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
    def __init__(self, node):
        Node.__init__(self, node)
        self.value = node.value


class BooleanNode(AtomicNode):
    pass


class IntNode(AtomicNode):
    pass


class StringNode(AtomicNode):
    pass


class VariableNode(AtomicNode):
    def __init__(self, node):
        super().__init__(node)
        self.defined = False


class InstantiateNode(AtomicNode):
    pass
