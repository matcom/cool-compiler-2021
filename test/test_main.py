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
            class Main inherits Point {
                x : String ;
                init ( n : String , m : Int) : Int {
                {
                    n <- "Testing main" ;
                    m <- 1 + 2 ;
                } } ;
            } ;
        class Point {
                x : AUTO_TYPE ;
                y : AUTO_TYPE ;
                init ( n : String , m : Int ) : Int {
                {
                    x <- n ;
                    y <- m ;
                } } ;
                main ( n : String , m : Int ) : Int {
                {
                    x <- n ;
                    y <- m ;
                } } ;
            } ;
            """

    ast = run_pipeline(text)
    errors = []

    collector = TypeCollector(errors)
    collector.visit(ast)

    context = collector.context

    builder = TypeBuilder(context, errors)
    builder.visit(ast)

    checker = TypeChecker(context, errors)
    checker.visit(ast, None)

    assert errors == [
        'Attribute "x" is already defined in Main.',
        "A class Main with a method main most be provided",
    ]

