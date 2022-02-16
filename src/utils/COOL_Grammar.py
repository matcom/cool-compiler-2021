from cmp.pycompiler import Grammar
from utils.ast.AST_Nodes import ast_nodes as node

def build_COOL_Grammar():
    # gramatica
    G = Grammar()
    
    # no terminales
    program = G.NonTerminal('<program>', startSymbol=True)
    class_list, def_class, param_list, param = G.NonTerminals('<class-list> <def-class> <param-list> <param>')
    feature_list, def_attr, def_meth, arg_list = G.NonTerminals('<feature-list> <def-attr> <def-meth> <arg-list>')
    expr, expr_list, id_list, case_list, comp = G.NonTerminals('<expr> <expr-list> <id-list> <case-list> <comp>')
    expr, arith, term, factor, atom, dispatch = G.NonTerminals('<expr> <arith> <term> <factor> <atom> <dispatch>')
    boolean = G.NonTerminal('<boolean>')

    #terminales
    classx, let, inx = G.Terminals('class let in')
    semi, colon, arrow, comma, dot, opar, cpar, ocur, ccur, darrow = G.Terminals('; : <- , . ( ) { } =>')
    equal, plus, minus, star, div, less, lesse, tilde, at = G.Terminals('= + - * / < <= ~ @')
    typex, inherits, idx, whilex, loop, pool, num, new = G.Terminals('type inherits id while loop pool int new')
    ifx, then, elsex, fi, case, esac, of, notx, isvoid = G.Terminals('if then else fi case esac of not isvoid')
    true, false, string = G.Terminals('true false string')


    #produciones
    program %= class_list, lambda h,s: node.ProgramNode(s[1])

    class_list %= def_class + semi, lambda h,s: [s[1]]
    class_list %= def_class + semi + class_list, lambda h,s: [s[1]] + s[3]

    def_class %= classx + typex + ocur + feature_list + ccur, lambda h,s: node.ClassDeclarationNode(s[2],s[4],s[1])
    def_class %= classx + typex + inherits + typex + ocur + feature_list + ccur, lambda h,s: node.ClassDeclarationNode(s[2],s[6],s[1],s[4])

    feature_list %= def_attr + semi + feature_list, lambda h,s: [s[1]] + s[3]
    feature_list %= def_meth + semi + feature_list, lambda h,s: [s[1]] + s[3]
    feature_list %= G.Epsilon, lambda h,s: []

    def_attr %= idx + colon + typex, lambda h,s: node.AttrDeclarationNode(s[1],s[3])
    def_attr %= idx + colon + typex + arrow + expr, lambda h,s: node.AttrDeclarationNode(s[1],s[3],s[4],s[5])

    def_meth %= idx + opar + param_list + cpar + colon + typex + ocur + expr + ccur, lambda h,s: node.MethDeclarationNode(s[1],s[3],s[6],s[8],s[7])

    param_list %= param, lambda h,s: [s[1]]
    param_list %= param + comma + param_list, lambda h,s: [s[1]] + s[3]
    param_list %= G.Epsilon, lambda h,s: []

    param %= idx + colon + typex, lambda h,s: [s[1],s[3]]

    expr %= idx + arrow + expr, lambda h,s: node.AssignNode(s[1],s[3],s[2])
    expr %= ifx + expr + then + expr + elsex + expr + fi, lambda h,s: node.IfThenElseNode(s[2],s[4],s[6],s[1])
    expr %= whilex + expr + loop + expr + pool, lambda h,s: node.WhileNode(s[2],s[4],s[1])
    

    expr %= ocur + expr_list + ccur, lambda h,s: node.BlockNode(s[2],s[1])

    expr_list %= expr + semi, lambda h,s: [s[1]]
    expr_list %= expr + semi + expr_list, lambda h,s: [s[1]] + s[3]
    
    expr %= let + id_list + inx + expr, lambda h,s: node.LetNode(s[2],s[4],s[1])

    id_list %= idx + colon + typex, lambda h,s: [(s[1],s[3],None)]
    id_list %= idx + colon + typex + arrow + expr, lambda h,s: [(s[1],s[3],s[5])]
    id_list %= idx + colon + typex + comma + id_list, lambda h,s: [(s[1],s[3],None)] + s[5]
    id_list %= idx + colon + typex + arrow + expr + comma + id_list, lambda h,s: [(s[1],s[3],s[5])] + s[7]

    expr %= case + expr + of + case_list + esac, lambda h,s: node.CaseNode(s[2],s[4],s[1])

    case_list %= idx + colon + typex + darrow + expr + semi, lambda h,s: [(s[1],s[3],s[5])]
    case_list %= idx + colon + typex + darrow + expr + semi + case_list, lambda h,s: [(s[1],s[3],s[5])] + s[7]

    expr %= boolean, lambda h,s: s[1]

    boolean %= comp, lambda h,s: s[1]
    boolean %= notx + comp, lambda h,s: node.NotNode(s[2], s[1])

    comp %= comp + less + arith, lambda h,s: node.LessThanNode(s[1],s[3],s[2])
    comp %= comp + lesse + arith, lambda h,s: node.LessEqualNode(s[1],s[3],s[2])
    comp %= comp + equal + arith, lambda h,s: node.EqualNode(s[1],s[3],s[2])
    comp %= arith, lambda h,s: s[1]

    arith %= arith + plus + term, lambda h,s: node.PlusNode(s[1],s[3],s[2])
    arith %= arith + minus + term, lambda h,s: node.MinusNode(s[1],s[3],s[2])
    arith %= term, lambda h,s:s[1]

    term %= term + star + factor, lambda h,s: node.StarNode(s[1],s[3],s[2])
    term %= term + div + factor, lambda h,s: node.DivNode(s[1],s[3],s[2])
    term %= factor, lambda h,s: s[1]

    factor %= isvoid + factor, lambda h,s: node.IsVoidNode(s[2])
    factor %= tilde + factor, lambda h,s: node.ComplementNode(s[2], s[1])
    factor %= atom, lambda h,s: s[1]

    atom %= true, lambda h,s: node.ConstantBoolNode(s[1])
    atom %= false, lambda h,s: node.ConstantBoolNode(s[1])
    atom %= string, lambda h,s: node.ConstantStringNode(s[1])
    atom %= num, lambda h,s: node.ConstantNumNode(s[1])
    atom %= idx, lambda h,s: node.VariableNode(s[1])
    atom %= new + typex, lambda h,s: node.InstantiateNode(s[2],s[1])
    atom %= opar + expr + cpar, lambda h,s: s[2]
    atom %= dispatch, lambda h,s: s[1]

    dispatch %= atom + dot + idx + opar + arg_list + cpar, lambda h,s: node.CallNode(s[3],s[5],s[1])
    dispatch %= idx + opar + arg_list + cpar, lambda h,s: node.CallNode(s[1],s[3])
    dispatch %= atom + at + typex + dot + idx + opar + arg_list + cpar, lambda h,s: node.CallNode(s[5],s[7],s[1],s[3])

    arg_list %= expr, lambda h,s: [s[1]]
    arg_list %= expr + comma + arg_list, lambda h,s: [s[1]] + s[3]
    arg_list %= G.Epsilon, lambda h,s: []

    return G