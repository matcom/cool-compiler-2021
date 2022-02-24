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

    def execute(self):
        self.errors = []
        self.ast = self.parser.ast
        tcollector = TypeCollector(self.errors)
        tcollector.visit(self.ast)
        if(self.has_errors()):
            return
        context = tcollector.context

        tbuilder = TypeBuilder(context,self.errors)
        
        tbuilder.visit(self.ast)
        if self.has_errors():
            return

        tchecking = TypeChecker(context,self.errors)
        scope = Scope()
        
        tchecking.visit(self.ast, scope)

    def has_errors(self):
        return len(self.errors) > 0

    def print_errors(self):
        for e in self.errors:
            print(e)