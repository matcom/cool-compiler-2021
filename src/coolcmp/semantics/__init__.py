from .collector import TypeCollector
from .builder import TypeBuilder
from .consistence import TypeConsistence
from .checker import TypeChecker
from coolcmp.utils.semantic import Context, Scope


def check_semantics(ast) -> tuple[list[str], Context, Scope]:
    collector = TypeCollector()
    collector.visit(ast)

    builder = TypeBuilder(collector.context, collector.errors)
    builder.visit(ast)

    cons = TypeConsistence(builder.context, builder.errors)
    cons.visit(ast)

    checker = TypeChecker(cons.context, cons.errors)
    scope = checker.visit(ast)

    return checker.errors, checker.context, scope
