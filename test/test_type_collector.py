from run_pipeline import run_pipeline
from src.type_collector import TypeCollector


def test():
    text = """
       class A { } ;
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

    # context = collector.context

    # print("Errors:", errors)
    # print("Context:")
    # print(context)

    assert errors == []
