from coolpyler.visitors.cool.type_builder import TypeBuilderVisitor
from coolpyler.visitors.cool.type_checker import TypeCheckerVisitor
from coolpyler.visitors.cool.type_collector import TypeCollectorVisitor


class Visitor:
    def __init__(self, errors=None):
        self.visitors = [TypeCollectorVisitor(errors),
                         TypeBuilderVisitor(errors),
                         TypeCheckerVisitor(errors)]

    def visit(self, ast):
        for visitor in self.visitors:
            ast = visitor.visit(ast)
        return ast
