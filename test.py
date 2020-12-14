from run_pipeline import run_pipeline
from src.type_collector import TypeCollector
from src.type_builder import TypeBuilder
from src.type_checker import TypeChecker
from src.tset_builder import TSetBuilder
from src.tsets_reducer import TSetReducer
from src.tset_merger import TSetMerger
from src.cool_visitor import FormatVisitor


def test():
    # text = """
    #         class A {
    #             f ( a : Int , d : Int ) : Int {
    #                 d <- False
    #             };
    #         };
    #         class B inherits A {
    #             f ( a : A , d : Int ) : A {
    #                 d <- True
    #             };
    #         };
    #         """

    text = """
        class Cons {
        xcar : Int ;
        xcdr : String ;

        isNill ( ) : Bool {
                false
        } ;

        init ( hd : Int , tl : String ) : String {
                {
                xcar <- hd ;
                xcdr <- tl ;
                }
        } ;
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

    if errors != []:
        print(errors)
        assert False

    tset_builder = TSetBuilder(context, errors)
    tset = tset_builder.visit(ast, None)

    tset_reducer = TSetReducer(context, errors)
    reduced_set = tset_reducer.visit(ast, tset)

    tset_merger = TSetMerger(context, errors)
    tset_merger.visit(ast, reduced_set)

    collector = TypeCollector(errors)
    collector.visit(ast)

    context = collector.context

    builder = TypeBuilder(context, errors)
    builder.visit(ast)

    checker = TypeChecker(context, errors)
    checker.visit(ast, None)

    formatter = FormatVisitor()
    tree = formatter.visit(ast)

    if errors != []:
        print("Errors:", errors)
        print("Context:")
        print(context)
        print(reduced_set)
        print(tree)
        assert False

    final_tree = """__ProgramNode [<class> ... <class>]__ClassDeclarationNode: class C inherits J { <feature> ... <feature> }__ClassDeclarationNode: class A inherits B { <feature> ... <feature> }__ClassDeclarationNode: class B inherits A { <feature> ... <feature> }__ClassDeclarationNode: class C  { <feature> ... <feature> }__ClassDeclarationNode: class D inherits E { <feature> ... <feature> }__ClassDeclarationNode: class E inherits F { <feature> ... <feature> }__ClassDeclarationNode: class F inherits D { <feature> ... <feature> }__ClassDeclarationNode: class G inherits F { <feature> ... <feature> }"""

    tree = tree.replace("\t", "")
    tree = tree.replace("\n", "")
    tree = tree.replace("\\", "")

    assert tree == final_tree


test()
