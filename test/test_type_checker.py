from run_pipeline import run_pipeline
from src.type_collector import TypeCollector
from src.type_builder import TypeBuilder
from src.type_checker import TypeChecker


def test():
    text = """
       class A { 
           a : String ;
           b : Bool ;
           c : Int <- 0 ;
           d : Object <- while c < 1 loop c = c + 1 pool  ;
           step ( p : AUTO_TYPE ) : AUTO_TYPE { p . translate ( 1 , 1 ) } ;
       } ;
         
        class Point {
            step ( p : AUTO_TYPE ) : AUTO_TYPE { p . translate ( 1 , 1 ) } ;
            main ( ) : Object {
                let p : AUTO_TYPE <- new Point in {
                    step ( p ) ; (*Puede lanzar error semantico*)
                }
            } ;
        } ;
        class B inherits A {
            e : Bool ;
            step ( p : AUTO_TYPE ) : AUTO_TYPE { p } ;
            test ( e : Int ) : Bool {
                 {
                      let x : Int <- 4 in e + ~ x ;

                      case 5 + 4 of
                        f : Bool => f ;
                        g : Bool => not g ;
                      esac ;
                      self . step ( e ) ;
                 }
            } ;
        } ;

        class C {
            a : B ;
            b : Int <- 8 ;
            c : Bool <- false ;

            m ( ) : Bool { 
                {
                    a @ A . step ( b ) ;
                    if not c then true else false fi ;
                    a . step ( b ) ;
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

    checker = TypeChecker(context, errors)
    scope = checker.visit(ast, None)

    print("Errors:", errors)
    print("Context:")
    print(context)
    print(scope)

    assert errors == ["A class Main with a method main most be provided"]
