from typing import List


class Node:
    def __init__(self) -> None:
        pass

    def __str__(self) -> str:
        raise NotImplementedError()


class ExpressionNode(Node):
    def __init__(self, locals: List = []) -> None:
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
        locals: List = [],
    ) -> None:
        super().__init__(locals=locals)
        self.case_expr = case_expr
        self.options = options


class ConditionalNode(ExpressionNode):
    def __init__(
        self,
        condition: ExpressionNode,
        then_node: ExpressionNode,
        else_node: ExpressionNode,
        locals: List = [],
    ) -> None:
        super().__init__(locals=locals)
        self.condition = condition
        self.then_node = then_node
        self.else_node = else_node

    def __str__(self):
        # ToDo
        pass


class BlocksNode(ExpressionNode):
    def __init__(self, expression_list: List[ExpressionNode]) -> None:
        super().__init__()
        self.expression_list = expression_list

    def __str__(self):
        block_str = "{\n"
        block_str += ";\n".join(expression for expression in self.expression_list)
        block_str += ";\n}\n"
        return block_str


class LetVarDeclarationNode(ExpressionNode):
    def __init__(self, idx: str, typex: str, expression=None, locals=[]):
        super().__init__(self, locals=locals)
        self.idx = idx
        self.type = typex
        self.expression = expression


class DeclarationNode(Node):
    def info(self):
        raise NotImplementedError()


class AttrDeclarationNode(DeclarationNode):
    def __init__(
        self,
        idx: str,
        typex: str,
        expression: ExpressionNode = None,
    ) -> None:
        super().__init__()
        self.id = idx
        self.type = typex
        self.expression = expression

    def __str__(self) -> str:
        return f"attribute {self.id}"

    def info(self):
        pass


class MethodDeclarationNode(DeclarationNode):
    def __init__(
        self,
        idx: str,
        params: List[ParamNodes],
        body: ExpressionNode,
        return_type: str,
    ) -> None:
        super().__init__()
        self.idx = idx
        self.paramas = params
        self.return_type = return_type
        self.body = body

    def __str__(self):
        # Return func name and address
        pass

    def info(self):
        # Return all the code of the function
        pass


class ClassDeclarationNode(Node):
    def __init__(self, idx: str, parent: str, features: List[DeclarationNode]) -> None:
        super().__init__()
        self.idx = idx
        self.parent = parent
        self.features = features

    def __str__(self) -> str:
        type_str = (
            "type "
            + self.idx
            + (f" : {self.parent}" if self.parent != "" else "")
            + " {\n"
        )
        type_str += " ;\n".join(str(feature) for feature in self.features)
        type_str += ";\n}\n"


class ProgramNode(Node):
    def __init__(
        self,
        types: List[ClassDeclarationNode],
        data: List[StringNode],
        code: List[MethodDeclarationNode],
    ) -> None:
        super().__init__()
        self.types = types
        self.data = data
        self.code = code

    def __str__(self) -> str:
        types = ".TYPE\n"
        types += "\n".join(str(typex) for typex in self.types)

        data = ".DATA\n"
        data = "\n".join(str(string_node) for string_node in self.data)

        code = ".CODE\n"
        code += "\n".join(func_node.info() for func_node in self.code)

        return f"{types}\n{data}\n{code}"
