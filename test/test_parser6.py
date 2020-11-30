from run_pipeline import run_pipeline
from src.cool_visitor import FormatVisitor


def test():
    text = """
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

    formatter = FormatVisitor()
    tree = formatter.visit(ast)

    tree = tree.replace("\t", "")
    tree = tree.replace("\n", "")
    tree = tree.replace("\\", "")

    assert (
        tree
        == "__ProgramNode [<class> ... <class>]__ClassDeclarationNode: class Point  { <feature> ... <feature> }__FuncDeclarationNode: step(p:AUTO_TYPE) : AUTO_TYPE -> <body>__CallNode: <obj>.translate(<expr>, ..., <expr>)__ VariableNode: p__ ConstantNumNode: 1__ ConstantNumNode: 1__FuncDeclarationNode: main() : Object -> <body>__LetNode: let <identif-list> in <expr>__VarDeclarationNode: p : AUTO_TYPE <- <expr>__ InstantiateNode: new Point()__BlockNode: {<exp>; ... <exp>;}__CallNode: step(<expr>, ..., <expr>)__ VariableNode: p"
    )
