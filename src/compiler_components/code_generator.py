from compiler_component import CompilerComponent
from semantic_checker import SemanticChecker

class CodeGenerator(CompilerComponent):
    def __init__(self, semantic_checker: SemanticChecker) -> None:
        super().__init__()
        self.semantic_checker = semantic_checker

    def execute():
        pass

    def has_errors():
        pass

    def print_errors():
        pass