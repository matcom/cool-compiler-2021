from __future__ import annotations

from coolcmp import visitor, errors as err
from coolcmp.ast import ProgramNode, ClassDeclarationNode
from coolcmp.semantic import Context, ErrorType, SemanticError


class TypeConsistence:
    """
    Checks for cyclic inheritance.
    """

    def __init__(self, context: Context, errors: list[str]):
        self.context = context
        self.errors = errors

    @visitor.on('node')
    def visit(self, node):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node: ProgramNode):
        for declaration in reversed(node.declarations):     # TODO: reversed to match tests
            self.visit(declaration)

    @visitor.when(ClassDeclarationNode)
    def visit(self, node: ClassDeclarationNode):
        type_ = self.context.get_type(node.id)
        try:
            type_.get_ancestors(node.id)
        except SemanticError:
            self.errors.append(err.CYCLIC_INHERITANCE % (node.parent_pos, node.parent))
            type_.parent = None
            type_.set_parent(ErrorType())
