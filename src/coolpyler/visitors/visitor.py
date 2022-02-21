from coolpyler.visitors.cool.type_builder import TypeBuilderVisitor
from coolpyler.visitors.cool.type_collector import TypeCollectorVisitor
from coolpyler.visitors.cool.type_checked import TypeCheckedVisitor


class Visitor:
    def __init__(self, errors=None):
        self.visitors = [TypeCollectorVisitor(errors),
                         TypeBuilderVisitor(errors),
                         TypeCheckedVisitor(errors)]

    def visit(self, ast):
        for visitor in self.visitors:
            ast = visitor.visit(ast)
        return ast
