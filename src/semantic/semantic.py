from utils.utils import Utils
from semantic.visitors.type_builder import TypeBuilder
from semantic.visitors.var_collector import VarCollector
from semantic.visitors.type_collector import TypeCollector

class SemanticAnalyzer:

    def __init__(self, ast, debug_path, debug=True):
        self.ast = ast
        self.debug_path = debug_path
        self.debug = debug
        self.errors = []
        self.context = None
        self.scope = None
        self.tree = None

    def analyze(self):
        
        collector = TypeCollector(self.errors)
        collector.visit(self.ast)
        self.context = collector.context
        print(self.context)
        Utils.Write(self.debug_path, '.context', str(self.context)) if self.debug else None

        builder = TypeBuilder(self.context, self.errors)
        builder.visit(self.ast)

        checker = VarCollector(self.context, self.errors)
        self.scope = checker.visit(self.ast)
        print(self.scope)
        


        return self.ast, self.context, self.scope