from run_pipeline import run_pipeline
from src.cool_visitor import FormatVisitor


def test():
    text = """
       class Main inherits IO {
            main ( ) : AUTO_TYPE {
                let x : AUTO_TYPE <- 3 + 2 in {
                    case x of
                        y : Int => out_string ( " Ok " ) ;
                    esac ;
                }
            } ;
        } ;
        """

    ast = run_pipeline(text)

    formatter = FormatVisitor()
    tree = formatter.visit(ast)

    tree = tree.replace("\t", "")
    tree = tree.replace("\n", "")
    tree = tree.replace("\\", "")

    assert (
        tree
        == "__ProgramNode [<class> ... <class>]__ClassDeclarationNode: class Main inherits IO { <feature> ... <feature> }__FuncDeclarationNode: main() : AUTO_TYPE { <body> }__LetNode: let <identif-list> in <expr>__VarDeclarationNode: x : AUTO_TYPE <- <expr>__<expr> PlusNode <expr>__ ConstantNumNode: 3__ ConstantNumNode: 2__BlockNode: {<exp>; ... <exp>;}__CaseNode: case <expr> of <case_block> esac__ VariableNode: x__CaseItemNode: y : Int => <exp>;__CallNode: out_string(<expr>, ..., <expr>)__ StringNode:  Ok "
    )

