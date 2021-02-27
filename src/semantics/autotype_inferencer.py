import semantics.visitor as visitor
from parsing.ast import AttrDeclarationNode, ClassDeclarationNode, ProgramNode
from semantics.tools import Context, Scope

class AutotypeInferencer:
    def __init__(self, context:Context) -> None:
        self.context = context
        self.current_type = None
        self.errors = []

    @visitor.when(ProgramNode)
    def visit(self, node:ProgramNode, scope:Scope):
        for declaration in node.declarations:
            self.visit(declaration, scope.next_child())
        
        scope.reset()

    @visitor.when(ClassDeclarationNode)
    def visit(self, node, scope):
        self.current_type = self.context.get_type(node.id, unpacked=True)
        for feature in node.features:
            self.visit(feature, scope)
    
    @visitor.when(AttrDeclarationNode)
    def visit(self, node, scope):

        self.visit(node.expr, scope)
        node_expr = node.expr.inferenced_type