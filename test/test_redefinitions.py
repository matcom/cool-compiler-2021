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
   
     class B inherits Point {
                x : String ;
                init ( n : String , z : Int , z : Int) : Bool {
                {
                    n <- "ok" ;
                    z <- 1 + 3 ;
                } } ;
            } ;
        class Point {
                x : AUTO_TYPE ;
                y : AUTO_TYPE ;
                init ( n : Int , m : Int ) : Int {
                {
                    x <- n ;
                    y <- m ;
                } } ;
            } ;
       
            """

    print("corriendo")
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
        'Attribute "x" is already defined in B.',
        "A class Main with a method main most be provided",
        "More tan one param in method init has the name z",
        'Cannot convert "Int" into "Bool".',
        'Method "init" already defined in "an ancestor of B" with a different signature.',
    ]

