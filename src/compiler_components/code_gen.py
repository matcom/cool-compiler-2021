from .compiler_component import CompilerComponent
from .semantic_checker import SemanticChecker
from .cool_to_cil import CoolToCil
from .cil_mips_converter import CilToMipsConverter
from . import cil
from .cil_to_mips import CilToMips
from .cil import get_formatter
from . import mips


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

        cool2cil = CoolToCil(self.context)
        f = cil.get_formatter()
        c = cool2cil.visit(self.ast, self.scope)
        # print(f(c))

        cil2mips = CilToMips()
        d = cil2mips.visit(c)
        e = mips.get_formatter()

        self.mips_text = e(d)

    def has_errors(self):
        return False

    def print_errors(self):
        pass
