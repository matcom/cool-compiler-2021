from run_pipeline import run_pipeline
from src.cool_visitor import FormatVisitor


def test():
    text = """
       class Point {
            x : AUTO_TYPE ;
            y : AUTO_TYPE ;
            init ( n : Int , m : Int ) : SELF_TYPE {
            {
                x <- n ;
                y <- m ;
            } } ;
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
        == "__ProgramNode [<class> ... <class>]__ClassDeclarationNode: class Point  { <feature> ... <feature> }__AttrDeclarationNode: x : AUTO_TYPE <- <exp>__NONE__AttrDeclarationNode: y : AUTO_TYPE <- <exp>__NONE__FuncDeclarationNode: init(n:Int, m:Int) : SELF_TYPE -> <body>__BlockNode: {<exp>; ... <exp>;}__AssignNode: x <- <expr>__ VariableNode: n__AssignNode: y <- <expr>__ VariableNode: m"
    )
