from .collector import TypeCollector
from .builder import TypeBuilder
from .consistence import TypeConsistence
from .checker import TypeChecker


def check_semantics(ast) -> list[str]:
    collector = TypeCollector()
    collector.visit(ast)

    builder = TypeBuilder(collector.context, collector.errors)
    builder.visit(ast)

    cons = TypeConsistence(builder.context, builder.errors)
    cons.visit(ast)

    checker = TypeChecker(cons.context, cons.errors)
    checker.visit(ast)

    return checker.errors
