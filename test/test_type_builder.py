from run_pipeline import run_pipeline
from src.type_collector import TypeCollector
from src.type_builder import TypeBuilder


def test():
    text = """
       class A { 
           a : String ;
           b : Bool ;
           c : Int <- 0 ;
           d : Object <- while c < 1 loop c = c + 1 pool  ;
       } ;
       class Point {
            step ( p : AUTO_TYPE ) : AUTO_TYPE { p . translate ( 1 , 1 ) } ;
            main ( ) : Object {
                let p : AUTO_TYPE <- new Point in {
                    step ( p ) ; (*Puede lanzar error semantico*)
                } 
            } ;
        } ;
        """

    ast = run_pipeline(text)
    errors = []

    collector = TypeCollector(errors)
    collector.visit(ast)

    context = collector.context

    builder = TypeBuilder(context, errors)
    builder.visit(ast)

    print("Errors:", errors)
    print("Context:")
    print(context)

    assert errors == ["A class Main with a method main most be provided"]
