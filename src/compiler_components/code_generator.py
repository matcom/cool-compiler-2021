from .compiler_component import CompilerComponent
from .semantic_checker import SemanticChecker

class CodeGenerator(CompilerComponent):
    def __init__(self, semantic_checker: SemanticChecker) -> None:
        super().__init__()
        self.semantic_checker = semantic_checker

    def execute(self):
        return

    def has_errors(self):
        return False

    def print_errors():
        print("errors at code generator")