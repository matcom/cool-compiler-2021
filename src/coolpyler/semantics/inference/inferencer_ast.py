from typing import List, Tuple


class Node:
    def __init__(self, node) -> None:
        self.lineno = node.lineno
        self.columnno = node.columnno
        self.inferenced_type = None

    def get_position(self) -> Tuple[int, int]:
        return self.line, self.col


class ProgramNode(Node):
    def __init__(self, declarations, scope, node: Node):
        Node.__init__(self, node)
        self.declarations = declarations
        self.scope = scope


class DeclarationNode(Node):
    pass


class ClassDeclarationNode(DeclarationNode):
    def __init__(self, features, node):
        Node.__init__(self, node)
        self.features = features
        self.id = node.id
        # For debbuging purposses
        self.parent = node.parent


class AttrDeclarationNode(DeclarationNode):
    def __init__(self, node):
        Node.__init__(self, node)
        self.id = node.id
        self.expr = None  # expression is set later if it exists
        # for debbugin purposes
        self.type = node.type


class MethodDeclarationNode(DeclarationNode):
    def __init__(self, params, return_type, body, node):
        Node.__init__(self, node)
        self.id = node.id
        self.params = params
        self.type = return_type
        self.body = body
        # for debbugin purposes
        # self.params = node.params


class ParamNode(DeclarationNode):
    def __init__(self, node, idx: str, typex) -> None:
        super().__init__(node)
        self.id = idx
        self.type = typex


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
    def __init__(self, ret_expr, branch_type, node):
        Node.__init__(self, node)
        self.id = node.id
        self.expr = ret_expr
        self.decl_type = node.type
        self.branch_type = branch_type
        # For debbuging purposes
        self.type = node.type


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
        # For debbugin purposes
        self.type = node.type


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
        self.type = node.static_type
        self.static_type = node.static_type


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
    def __init__(self, node):
        Node.__init__(self, node)
        self.value = node.type
        self.type = node.type
