from run_pipeline import run_pipeline
from src.cool_visitor import FormatVisitor


def test():
    text = """
       class Point {
           succ ( n : Int ) : AUTO_TYPE { n + 1 } ;
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
        == "__ProgramNode [<class> ... <class>]__ClassDeclarationNode: class Point  { <feature> ... <feature> }__FuncDeclarationNode: succ(n:Int) : AUTO_TYPE -> <body>__<expr> PlusNode <expr>__ VariableNode: n__ ConstantNumNode: 1"
    )
