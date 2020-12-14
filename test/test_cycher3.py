from run_pipeline import run_pipeline
from src.type_collector import TypeCollector
from src.type_builder import TypeBuilder
from src.type_checker import TypeChecker
from src.tset_builder import TSetBuilder
from src.tsets_reducer import TSetReducer
from src.tset_merger import TSetMerger
from src.cool_visitor import FormatVisitor


def test():
    text = """
            class C inherits J { } ;
            class A inherits B { } ;
            class B inherits A { } ;
            class C { } ;
            class D inherits E { } ;
            class E inherits F { } ;
            class F inherits D { } ;
            class G inherits F { } ;
           """

    ast = run_pipeline(text)
    errors = []

    collector = TypeCollector(errors)
    collector.visit(ast)

    context = collector.context

    builder = TypeBuilder(context, errors)
    builder.visit(ast)

    err = [
        "Type with the same name (C) already in context.",
        'Type "J" is not defined.',
        "Parent type is already set for C.",
        "A is involved in a cyclic heritage",
        "D is involved in a cyclic heritage",
        "A class Main with a method main most be provided",
    ]

    checker = TypeChecker(context, errors)
    checker.visit(ast, None)

    if errors != err:
        print(errors)
        assert False

    assert True


test()
