from typing import List, Tuple


class Node:
    def __init__(self, node) -> None:
        self.line: int = node.line
        self.col: int = node.col
        self.type = None

    def get_position(self) -> Tuple[int, int]:
        return self.line, self.col


class ExpressionNode(Node):
    def __init__(self, node, value: str, locals: List[str] = None) -> None:
        """
        Parameters:
        node <-  Node to set this node positon in the original cool program.
        value <- Name of the local variable where the expresion final value is going to be stored.
        locals <- List of local variables needed to be initialized to execute expression.
        """
        super().__init__(node)
        if locals is None:
            self.locals = []
        self.value = value
        self.locals = locals


class AtomicNode(ExpressionNode):
    pass


class StringNode(AtomicNode):
    pass


class IntNode(AtomicNode):
    pass


class VariableNode(ExpressionNode):
    pass


class VarDeclarationNode(ExpressionNode):
    def __init__(
        self, expr: ExpressionNode, node, value: str, locals: List = None
    ) -> None:
        super().__init__(node, value, locals=locals)
        self.expression = expr


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
        value: str,
        locals: List = None,
    ) -> None:
        super().__init__(node, value, locals=locals)
        self.case_expr = case_expr
        self.options = options


class ConditionalNode(ExpressionNode):
    def __init__(
        self,
        condition: ExpressionNode,
        then_node: ExpressionNode,
        else_node: ExpressionNode,
        node,
        value: str,
        locals: List = None,
    ) -> None:
        super().__init__(node, value, locals=locals)
        self.condition = condition
        self.then_node = then_node
        self.else_node = else_node


class BlocksNode(ExpressionNode):
    def __init__(
        self,
        expression_list: List[ExpressionNode],
        node,
        value: str,
        locals: List = None,
    ) -> None:
        super().__init__(node, value, locals=locals)
        self.expression_list = expression_list


class LetVarDeclarationNode(ExpressionNode):
    def __init__(self, expression: ExpressionNode, node, value: str, locals=None):
        super().__init__(self, node, value, locals=locals)
        self.id = node.id
        self.type = node.type
        self.expression = expression


class DeclarationNode(Node):
    pass


class AttrDeclarationNode(DeclarationNode):
    def __init__(self, expression: ExpressionNode, node) -> None:
        super().__init__(node)
        self.id = node.id
        self.type = node.type
        self.expression = expression


class MethodDeclarationNode(DeclarationNode):
    def __init__(
        self,
        idx: str,
        params: List[ParamNodes],
        body: ExpressionNode,
        return_type: str,
        node,
    ) -> None:
        super().__init__(node)
        self.idx = idx
        self.paramas = params
        self.return_type = return_type
        self.body = body


class ClassDeclarationNode(Node):
    def __init__(self, features: List[DeclarationNode], node) -> None:
        super().__init__(node)
        self.idx = node.id
        self.parent = "?"
        self.features = features


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
