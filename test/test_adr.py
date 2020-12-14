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

       class Main {
        a : AUTO_TYPE<- "Hola";
        main ( ) : Int { {
            case {let i: AUTO_TYPE <- 12 in {let i: AUTO_TYPE <- "Hola" in {"Hi";
                case 12 of
                    x : Int => x;
                    y : AUTO_TYPE => y;
                    z: String => let i : AUTO_TYPE in {
                       i<- case self of
                            x: Int => 12;
                            x: AUTO_TYPE => if 12<12 then x else "Hola" fi ;
                        esac
                    ;};
                esac
            ;};};} of
                x : Int => 12;
                y : AUTO_TYPE => let i: AUTO_TYPE <- y in y ;
            esac ;
        a.length();} } ;
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

    # print(errors)
    # if errors != []:
    #     print(errors)
    #     assert False

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

    # print("Errors:", errors)
    # print("Context:")
    # print(context)
    # print(reduced_set)
    # print(tree)

    final_tree = """__ProgramNode [<class> ... <class>]__ClassDeclarationNode: class Main  { <feature> ... <feature> }__AttrDeclarationNode: a : String <- <exp>__ StringNode: Hola__FuncDeclarationNode: main() : Int { <body> }__BlockNode: {<exp>; ... <exp>;}__CaseNode: case <expr> of <case_block> esac__BlockNode: {<exp>; ... <exp>;}__LetNode: let <identif-list> in <expr>__VarDeclarationNode: i : Int <- <expr>__ ConstantNumNode: 12__BlockNode: {<exp>; ... <exp>;}__LetNode: let <identif-list> in <expr>__VarDeclarationNode: i : String <- <expr>__ StringNode: Hola__BlockNode: {<exp>; ... <exp>;}__ StringNode: Hi__CaseNode: case <expr> of <case_block> esac__ ConstantNumNode: 12__CaseItemNode: x : Int => <exp>;__ VariableNode: x__CaseItemNode: y : Object => <exp>;__ VariableNode: y__CaseItemNode: z : String => <exp>;__LetNode: let <identif-list> in <expr>__VarDeclarationNode: i : Object <- <expr>__NONE__BlockNode: {<exp>; ... <exp>;}__AssignNode: i <- <expr>__CaseNode: case <expr> of <case_block> esac__ VariableNode: self__CaseItemNode: x : Int => <exp>;__ ConstantNumNode: 12__CaseItemNode: x : Object => <exp>;__IfNode: if <expr> then <expr> else <exp> fi__<expr> LessNode <expr>__ ConstantNumNode: 12__ ConstantNumNode: 12__ VariableNode: x__ StringNode: Hola__CaseItemNode: x : Int => <exp>;__ ConstantNumNode: 12__CaseItemNode: y : Object => <exp>;__LetNode: let <identif-list> in <expr>__VarDeclarationNode: i : Object <- <expr>__ VariableNode: y__ VariableNode: y__CallNode: <obj>.length(<expr>, ..., <expr>)__ VariableNode: a"""

    tree = tree.replace("\t", "")
    tree = tree.replace("\n", "")
    tree = tree.replace("\\", "")

    assert tree == final_tree
    assert errors == []
