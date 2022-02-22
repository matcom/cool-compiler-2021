from typing import List, Tuple

from code_gen.tools import LocalVar


class Node:
    def __init__(self, node) -> None:
        self.line: int = node.line
        self.col: int = node.col
        self.type = None

    def get_position(self) -> Tuple[int, int]:
        return self.line, self.col


class ExpressionNode(Node):
    def __init__(self, node, locals: List[LocalVar] = None) -> None:
        """
        Parameters:
        node <-  Node to set this node positon in the original cool program.
        locals <- List of local variables needed to be initialized to execute expression.
        value <- Name of the local variable where the expresion final value is going to be stored.
        """
        super().__init__(node)
        if locals is None:
            locals = []

        self.locals = locals

    @property
    def value(self):
        return self.locals[-1]


class FuncCallNode(Node):
    def __init__(self, node, idx: str, arg_list: List) -> None:
        super().__init__(node)
        self.id = idx
        self.arg_list = arg_list


class VirtualFuncCallNode(FuncCallNode):
    def __init__(self, node, idx: str, class_idx: str, arg_list: List) -> None:
        super().__init__(node, idx, arg_list)
        self.class_idx = class_idx


class ReturnOpNode(Node):
    def __init__(self, node) -> None:
        super().__init__(node)


class FlowControlNode(Node):
    def __init__(self, node, target) -> None:
        super().__init__(node)

        self.target = target


class ConditionalFlowControlNode(FlowControlNode):
    def __init__(self, node, target, value) -> None:
        super().__init__(node, target)

        self.value = value


class AtomicNode(ExpressionNode):
    pass


class StringNode(AtomicNode):
    pass


class IntNode(AtomicNode):
    pass


class VariableNode(ExpressionNode):
    pass


class VarDeclarationNode(ExpressionNode):
    def __init__(self, expr: ExpressionNode, node, locals: List = None) -> None:
        super().__init__(node, locals=locals)
        self.expression = expr


class GoToNode(FlowControlNode):
    pass


class LabelNode(FlowControlNode):
    pass


class IfGoToNode(ConditionalFlowControlNode):
    pass


class IfFalseGoToNode(ConditionalFlowControlNode):
    pass


class LetNode(ExpressionNode):
    pass


class LoopNode(ExpressionNode):
    pass


class CaseOptionNode(ExpressionNode):
    pass


class CaseNode(ExpressionNode):
    def __init__(
        self,
        case_expr: ExpressionNode,
        options: List[CaseOptionNode],
        node,
        locals: List = None,
    ) -> None:
        super().__init__(node, locals=locals)
        self.case_expr = case_expr
        self.options = options


class ConditionalNode(ExpressionNode):
    def __init__(
        self,
        condition: ExpressionNode,
        then_node: ExpressionNode,
        else_node: ExpressionNode,
        node,
        locals: List = None,
    ) -> None:
        super().__init__(node, locals=locals)
        self.condition = condition
        self.then_node = then_node
        self.else_node = else_node


class BlocksNode(ExpressionNode):
    def __init__(
        self,
        expression_list: List[ExpressionNode],
        node,
        locals: List = None,
    ) -> None:
        super().__init__(node, locals=locals)
        self.expression_list = expression_list


class LetVarDeclarationNode(ExpressionNode):
    def __init__(self, expression: ExpressionNode, node, locals=None):
        super().__init__(node, locals=locals)
        self.id = node.id
        self.type = node.type
        self.expression = expression


class DeclarationNode(Node):
    pass


class AttrDeclarationNode(DeclarationNode):
    def __init__(self, expression: ExpressionNode | None, node) -> None:
        super().__init__(node)
        self.id = node.id
        self.type = node.type
        self.expression = expression
        self.value = expression.value if expression is not None else None


class MethodDeclarationNode(DeclarationNode):
    def __init__(
        self,
        idx: str,
        params: List[VarDeclarationNode],
        body: ExpressionNode,
        node,
    ) -> None:
        super().__init__(node)
        self.idx: str = idx
        self.params: List[VarDeclarationNode] = params
        self.body: ExpressionNode = body
        self.value = body.value


class ClassDeclarationNode(Node):
    def __init__(
        self,
        attributes: List[AttrDeclarationNode],
        methods: List[MethodDeclarationNode],
        feature_info: List,
        node,
    ) -> None:
        super().__init__(node)
        self.idx: str = node.id
        self.parent: str = node.parent
        self.attributes: List[AttrDeclarationNode] = attributes
        self.methods: List[MethodDeclarationNode] = methods
        self.feature_info: List = feature_info


class ProgramNode(Node):
    def __init__(
        self,
        types: List[ClassDeclarationNode],
        data: List[str],
        node,
    ) -> None:
        super().__init__(node)
        self.types = types
        self.data = data
