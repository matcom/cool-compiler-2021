

class SemanticAnalyzer:

    def __init__(self, ast):
        self.ast = ast
        self.errors = []
        self.context = None
        self.scope = None
        self.tree = None

    def analyze(self):
        
        return self.ast, self.context, self.scope