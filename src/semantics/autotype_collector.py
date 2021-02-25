import semantics.visitor as visitor
from semantics.tools import Context, Scope
from parsing.ast import AttrDeclarationNode, ClassDeclarationNode, ProgramNode

class AutotypeCollector:
    def __init__(self, context:Context):
        self.context = context
        self.current_type = None
        self.current_method = None
        self.current_attrb = None
        self.inference_graph = dict()
        self.errors = []
    
    @visitor.on('node')
    def visit(self, node, scope):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node:ProgramNode) -> Scope:
        scope = Scope()
        for declaration in node.declarations:
            self.visit(declaration, scope.create_child())
        
        return scope

    @visitor.when(ClassDeclarationNode)
    def visit(self, node, scope):
        self.current_type = self.context.get_type(node.id)
        scope.define_variable("self", self.current_type)
        for attr in self.current_type.attributes:
            scope.define_variable(attr.name, attr.type)
        
        for feature in node.features:
            self.visit(feature, scope)
    
    @visitor.when(AttrDeclarationNode)
    def visit(self, node, scope):
        self.current_attrb = self.current_type.get_attribute(node.id)
        node_type = self.update_type(self.current_attrb.type)

        if not node.expr:
            self.current_attrb = None
            node.inferenced_type = node_type
            return


# todo: Revisar los auto types que me hace falta y que no
# todo: completar de manera acorde el autotype collector