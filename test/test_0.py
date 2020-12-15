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

        init ( hd : Int , tl : String ) : AUTO_TYPE {
                {
                xcar <- hd ;
                xcdr <- tl ;
                self;
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

    if errors != ["A class Main with a method main most be provided"]:
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

    if errors != [
        "A class Main with a method main most be provided",
        "A class Main with a method main most be provided",
    ]:
        print("Errors:", errors)
        print("Context:")
        print(context)
        print(reduced_set)
        print(tree)
        assert False

    final_tree = """__ProgramNode [<class> ... <class>]__ClassDeclarationNode: class Cons  { <feature> ... <feature> }__AttrDeclarationNode: xcar : Int <- <exp>__NONE__AttrDeclarationNode: xcdr : String <- <exp>__NONE__FuncDeclarationNode: isNill() : Bool { <body> }__ BooleanNode: false__FuncDeclarationNode: init(hd:Int, tl:String) : Cons { <body> }__BlockNode: {<exp>; ... <exp>;}__AssignNode: xcar <- <expr>__ VariableNode: hd__AssignNode: xcdr <- <expr>__ VariableNode: tl__ VariableNode: self"""
    tree = tree.replace("\t", "")
    tree = tree.replace("\n", "")
    tree = tree.replace("\\", "")

    print(tree)
    assert tree == final_tree

