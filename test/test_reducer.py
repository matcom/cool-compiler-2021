from run_pipeline import run_pipeline
from src.type_collector import TypeCollector
from src.type_builder import TypeBuilder
from src.type_checker import TypeChecker
from src.tset_builder import TSetBuilder
from src.tsets_reducer import TSetReducer


def test():
    text = """
       class A { 
           a : String ;
           b : AUTO_TYPE ;
           c : Int <- 0 ;
           d : Object <- while c < 1 loop c + 1 pool  ;
           j : AUTO_TYPE ;
           l : AUTO_TYPE ;
           step ( p : AUTO_TYPE ) : AUTO_TYPE {
               b <-
                {
                    p + 5 ;
                    p <- false ;
                    j <- p ;
                    isvoid d ;
                } 
            } ;
       } ;
         
        class Point inherits A {
            h : AUTO_TYPE <- "debe ser tipo string" ;
            k : AUTO_TYPE ;
            step ( p : AUTO_TYPE ) : AUTO_TYPE { k <- if p then new Point else new A fi } ;
            main ( ) : Object {
                let i : AUTO_TYPE <- new A in {
                    isvoid i ; *Puede lanzar error semantico*
                }
            } ;
        } ;
        """
    # l <- ~ c ;

    ast = run_pipeline(text)
    errors = []

    collector = TypeCollector(errors)
    collector.visit(ast)

    context = collector.context

    builder = TypeBuilder(context, errors)
    builder.visit(ast)

    checker = TypeChecker(context, errors)
    __ = checker.visit(ast, None)

    tset_builder = TSetBuilder(context, errors)
    tset = tset_builder.visit(ast, None)

    tset_reducer = TSetReducer(context, errors)
    reduced_set = tset_reducer.visit(ast, tset)

    print("Errors:", errors)
    print("Context:")
    print(context)
    print(reduced_set)

    assert False
