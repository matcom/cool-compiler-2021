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
        print('......................')
        print(self.ast.visit())
        tcollector = TypeCollector(self.errors)
        tcollector.visit(self.ast)
        context = tcollector.context
        cycles = context.circular_dependency()
        for cycle in cycles:
            self.errors.append(SemanticError(f"Class {cycle[0][0]},  is involved in an inheritance cycle.",cycle[0][1]))
            return

        tbuilder = TypeBuilder(context,self.errors)
        tbuilder.visit(self.ast)

        tchecking = TypeChecker(context,self.errors)
        scope = Scope()
        tchecking.visit(self.ast, scope)

    def has_errors(self):
        return len(self.errors) > 0

    def print_errors(self):
        for e in self.errors:
            print(e)