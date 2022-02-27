import app.semantics.ast as inf_ast


class Node:
    def __init__(self, node) -> None:
        self.lineno = node.lineno
        self.columnno = node.columnno
        self.inferenced_type = None
        self._exec_inferred_type = None

    @property
    def exec_inferred_type(self):
        if self._exec_inferred_type is None:
            return self.inferenced_type
        else:
            return self._exec_inferred_type

    @exec_inferred_type.setter
    def exec_inferred_type(self, value):
        self._exec_inferred_type = value


class ProgramNode(Node):
    def __init__(self, declarations, scope, node: Node):
        super().__init__(node)
        self.declarations = declarations
        self.scope = scope

    def shallow_infer(node, scope, shallow_inferrer):
        new_classes = []
        for declaration in node.classes:
            new_classes.append(shallow_inferrer.visit(
                declaration, scope.create_child()))

        program = inf_ast.ProgramNode(new_classes, scope, node)
        return program

    @staticmethod
    def deep_infer(node, hard_inferrer):
        scope = node.scope
        new_declaration = []
        for declaration in node.declarations:
            new_declaration.append(hard_inferrer.visit(
                declaration, scope.next_child()))

        scope.reset()
        program = ProgramNode(new_declaration, scope, node)
        return program


class DeclarationNode(Node):
    pass


class ExpressionNode(Node):
    pass


class UnaryNode(ExpressionNode):
    def __init__(self, expr, node):
        super().__init__(node)
        self.expr = expr


class BinaryNode(ExpressionNode):
    def __init__(self, left, right, node):
        super().__init__(node)
        self.left = left
        self.right = right
