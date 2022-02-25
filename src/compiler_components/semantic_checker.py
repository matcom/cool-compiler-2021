import sys
sys.path.append('./semantic')
from .semantic.type_collector import *
from .semantic.type_builder import *
from .semantic.type_checker import *
from .semantic.structures import *
from .compiler_component import CompilerComponent
from .cool_parser import Parser


class SemanticChecker(CompilerComponent):
    def __init__(self, parser: Parser) -> None:
        super().__init__()
        self.parser = parser
        self.context = None
        self.scope = None
        self.ast = None

    def execute(self):
        self.errors = []
        self.ast = self.parser.ast
        tcollector = TypeCollector(self.errors)
        tcollector.visit(self.ast)
        if(self.has_errors()):
            return
        self.context = tcollector.context

        tbuilder = TypeBuilder(self.context, self.errors)
        
        tbuilder.visit(self.ast)
        if self.has_errors():
            return

        tchecking = TypeChecker(self.context,self.errors)
        self.scope = Scope()
        
        tchecking.visit(self.ast, self.scope)

    def has_errors(self):
        return len(self.errors) > 0

    def print_errors(self):
        for e in self.errors:
            print(e)