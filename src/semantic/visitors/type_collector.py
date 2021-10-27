from utils import visitor





class TypeCollector(object):
    def __init__(self, errors = []):
        self.context = None
        self.errors = errors
    
    @visitor.on('node')
    def visit(self, node):
        pass

    
    @visitor.when(ProgramNode)
    def visit(self, node):
        pass

    @visitor.when(ClassDeclarationNode)
    def visit(self, node):
        pass
