from coolpyler.visitors.cool.cool_to_cil import CoolToCilVisitor
from coolpyler.visitors.cool.type_builder import TypeBuilderVisitor
from coolpyler.visitors.cool.type_checker import TypeCheckerVisitor
from coolpyler.visitors.cool.type_collector import TypeCollectorVisitor
from coolpyler.visitors.mips.cil_to_mips import CilToMIPS
from coolpyler.visitors.mips.mips_to_text import MIPSGenerator


class Visitor:
    def __init__(self, errors:list):
        self.visitors_up = [
            TypeCollectorVisitor(errors),
            TypeBuilderVisitor(errors),
            TypeCheckerVisitor(errors),
            CoolToCilVisitor(),
        ]
        self.visitors_down = [CilToMIPS(), MIPSGenerator()]

    def visit_up(self, ast):
        for visitor in self.visitors_up:
            ast = visitor.visit(ast)
        return ast

    def visit_down(self, ast):
        for visitor in self.visitors_down:
            ast = visitor.visit(ast)
        return ast
