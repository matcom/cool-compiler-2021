from utils.utils import Utils
from semantic.visitors.type_builder import TypeBuilder
from semantic.visitors.type_checker import TypeChecker
from semantic.visitors.var_collector import VarCollector
from semantic.visitors.type_collector import TypeCollector

class SemanticAnalyzer:

    def __init__(self, ast, debug_path, debug):
        self.ast = ast
        self.debug_path = debug_path
        self.debug = debug
        self.errors = []
        self.context = None
        self.scope = None

    def analyze(self):
        
        collector = TypeCollector(self.errors)
        collector.visit(self.ast)
        self.context = collector.context
        Utils.Write(self.debug_path, '.context', str(self.context)) if self.debug else None

        builder = TypeBuilder(self.context, self.errors)
        builder.visit(self.ast)

        checker = VarCollector(self.context, self.errors)
        self.scope = checker.visit(self.ast)
        Utils.Write(self.debug_path, '.scope', str(self.scope)) if self.debug else None

        checker = TypeChecker(self.context, self.errors)
        checker.visit(self.ast, self.scope)

        return self.ast, self.context, self.scope
