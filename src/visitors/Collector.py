from cool_ast.cool_ast import ProgramNode, ClassDeclarationNode
import visitors.visitor as visitor
from utils.semantic import Context, SemanticError


class TypeCollector:
    def __init__(self, context = Context(), errors = []):
        self.errors = errors
        self.context = context

    @visitor.on('node')
    def visit(self, node):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node):
        self.context.create_type('Object')
        self.context.create_type('Int')
        self.context.create_type('Bool')
        self.context.create_type('String')
        self.context.create_type('IO')
        self.context.create_type('SELF_TYPE')
        self.context.create_type('AUTO_TYPE')
        
        for declaration in node.declarations:
            self.visit(declaration)

    @visitor.when(ClassDeclarationNode)
    def visit(self, node):
        try:
            self.context.create_type(node.id)
        except SemanticError as e:
            self.errors.append(e.text)