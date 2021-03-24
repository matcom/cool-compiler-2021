from semantic.visitors.type_builder import TypeBuilder
from semantic.visitors.type_collector import TypeCollector

class SemanticAnalyzer:

    def __init__(self, ast):
        self.ast = ast
        self.errors = []
        self.context = None
        self.scope = None
        self.tree = None

    def analyze(self):
        
        collector = TypeCollector(self.errors)
        collector.visit(self.ast)
        self.context = collector.context
        print(self.context)

        builder = TypeBuilder(self.context, self.errors)
        builder.visit(self.ast)



        return self.ast, self.context, self.scope