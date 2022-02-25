from .compiler_component import CompilerComponent
from .semantic_checker import SemanticChecker
from .cool_cil_converter import CoolToCilConverter
from .cil_mips_converter import CilToMipsConverter
from .code_generator.mips_formatter import get_formatter


class CodeGenerator(CompilerComponent):
    def __init__(self, semantic_checker: SemanticChecker) -> None:
        super().__init__()
        self.semantic_checker = semantic_checker
        self.context = None
        self.scope = None
        self.ast = None
        self.mips_text = None

    def execute(self):
        self.context = self.semantic_checker.context
        self.scope = self.semantic_checker.scope
        self.ast = self.semantic_checker.ast

        cool_cil_converter = CoolToCilConverter(self.context)
        cil_tree = cool_cil_converter.visit(self.ast, self.scope)

        cil_mips_converter = CilToMipsConverter()
        mips_tree = cil_mips_converter.visit(cil_tree)
        mips_formatter = get_formatter()

        self.mips_text = mips_formatter(mips_tree)

    def has_errors(self):
        return False

    def print_errors(self):
        pass
