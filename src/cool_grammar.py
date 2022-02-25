from cmp.pycompiler import Grammar
from ast_nodes import (
    ProgramNode,
    ClassDeclarationNode,
    FuncDeclarationNode,
    AttrDeclarationNode,
    IfNode,
    WhileNode,
    LetNode,
    CaseNode,
    IsvoidNode,
    AssignNode,
    VarDeclarationNode,
    CaseItemNode,
    NotNode,
    LessNode,
    LessEqualNode,
    EqualNode,
    PlusNode,
    MinusNode,
    StarNode,
    DivNode,
    NegNode,
    InstantiateNode,
    BlockNode,
    CallNode,
    ConstantNumNode,
    VariableNode,
    BooleanNode,
    StringNode,
)


def define_cool_grammar(print_grammar=False):
    # grammar
    G = Grammar()

    # non-terminals
    program = G.NonTerminal("<program>", startSymbol=True)
    class_list, def_class = G.NonTerminals("<class-list> <def-class>")
    feature_list, def_attr, def_func = G.NonTerminals(
        "<feature-list> <def-attr> <def-func>"
    )
    param_list, param_list_rest, param = G.NonTerminals("<param-list> <param-list-rest> <param>")
    expr, comp, arith, term, factor, element, atom = G.NonTerminals(
        "<expr> <comp> <arith> <term> <factor> <element> <atom>"
    )
    identifiers_list, identifier_init = G.NonTerminals("<ident-list> <ident-init>")
    block, case_block, case_item = G.NonTerminals("<block> <case-block> <case-item>")
    func_call, arg_list, arg_list_rest = G.NonTerminals("<func-call> <arg-list> <arg-list-rest>")

    # terminals
    classx, inherits, notx, isvoid = G.Terminals("class inherits not isvoid")
    let, inx = G.Terminals("let in")
    ifx, then, elsex, fi = G.Terminals("if then else fi")
    whilex, loop, pool = G.Terminals("while loop pool")
    case, of, esac = G.Terminals("case of esac")
    semi, colon, comma, dot, opar, cpar, ocur, ccur, at, larrow, rarrow = G.Terminals(
        "; : , . ( ) { } @ <- =>"
    )
    equal, plus, minus, star, div, less, equal, lesseq, neg = G.Terminals(
        "= + - * / < = <= ~"
    )
    idx, type_id, num, new, string, true, false = G.Terminals("id type_id int new string true false")

    # productions
    program %= class_list, lambda h, s: ProgramNode(s[1])

    class_list %= def_class + class_list, lambda h, s: [s[1]] + s[2]
    class_list %= def_class, lambda h, s: [s[1]]

    def_class %= (
        classx + type_id + ocur + feature_list + ccur + semi,
        lambda h, s: ClassDeclarationNode(s[2].lex, s[4], s[1]),
    )
    def_class %= (
        classx + type_id + inherits + type_id + ocur + feature_list + ccur + semi,
        lambda h, s: ClassDeclarationNode(s[2].lex, s[6], s[1], s[4]), # aqui hay que buscar otra alternativa a simplemente pasar el lexema pues a la hora de dar errores estaria bien decir que el tipo que se refencia noe sta definido
    )

    feature_list %= def_attr + semi + feature_list, lambda h, s: [s[1]] + s[3]
    feature_list %= def_func + semi + feature_list, lambda h, s: [s[1]] + s[3]
    feature_list %= G.Epsilon, lambda h, s: []

    def_attr %= (
        idx + colon + type_id + larrow + expr, # el token podria ser el del id en estos 3
        lambda h, s: AttrDeclarationNode(s[1], s[3], s[5], s[4]),
    )
    def_attr %= idx + colon + type_id, lambda h, s: AttrDeclarationNode(s[1], s[3], token = s[2])

    def_func %= (#verificar el token que se manda
        idx + opar + param_list + cpar + colon + type_id + ocur + expr + ccur,
        lambda h, s: FuncDeclarationNode(s[1], s[3], s[6], s[8], s[2]),
    )

    param_list %= param + param_list_rest, lambda h, s: [s[1]] + s[2]
    param_list %= param, lambda h, s: [s[1]]
    param_list %= G.Epsilon, lambda h, s: []

    param_list_rest %= comma + param + param_list_rest, lambda h, s: [s[2]] + s[3]
    param_list_rest %= comma + param, lambda h, s: [s[2]]
    #aqui podria ser conveniente annadir un token para registrar la pos ante un error
    param %= idx + colon + type_id, lambda h, s: (s[1], s[3])

    expr %= idx + larrow + expr, lambda h, s: AssignNode(s[1], s[3], s[2])
    expr %= let + identifiers_list + inx + expr, lambda h, s: LetNode(s[2], s[4], s[1])
    expr %= comp, lambda h, s: s[1]

    # igual, deberia considerarse registrar estos tokens
    identifiers_list %= (
        identifier_init + comma + identifiers_list,
        lambda h, s: [s[1]] + s[3],
    )
    identifiers_list %= identifier_init, lambda h, s: [s[1]]

    identifier_init %= (
        idx + colon + type_id + larrow + expr,
        lambda h, s: VarDeclarationNode(s[1], s[3], s[5]),
    )
    identifier_init %= idx + colon + type_id, lambda h, s: VarDeclarationNode(s[1], s[3])

    comp %= comp + less + arith, lambda h, s: LessNode(s[1], s[3], s[2])
    comp %= comp + equal + arith, lambda h, s: EqualNode(s[1], s[3], s[2])
    comp %= comp + lesseq + arith, lambda h, s: LessEqualNode(s[1], s[3], s[2])
    comp %= arith, lambda h, s: s[1]

    arith %= notx + term, lambda h, s: NotNode(s[2], s[1]) 
    arith %= arith + plus + term, lambda h, s: PlusNode(s[1], s[3], s[2])
    arith %= arith + minus + term, lambda h, s: MinusNode(s[1], s[3], s[2])
    arith %= term, lambda h, s: s[1]

    term %= term + star + factor, lambda h, s: StarNode(s[1], s[3], s[2])
    term %= term + div + factor, lambda h, s: DivNode(s[1], s[3], s[2])
    term %= factor, lambda h, s: s[1]

    factor %= isvoid + element, lambda h, s: IsvoidNode(s[2], s[1])
    factor %= neg + element, lambda h, s: NegNode(s[2], s[1])
    factor %= element, lambda h, s: s[1]

    element %= (
        ifx + expr + then + expr + elsex + expr + fi,
        lambda h, s: IfNode(s[2], s[4], s[6], s[1]),
    )
    element %= whilex + expr + loop + expr + pool, lambda h, s: WhileNode(s[2], s[4], s[1])
    element %= case + expr + of + case_block + esac, lambda h, s: CaseNode(s[2], s[4], s[1])
    element %= new + type_id, lambda h, s: InstantiateNode(s[2], s[1])
    element %= opar + expr + cpar, lambda h, s: s[2]
    element %= ocur + block + ccur, lambda h, s: BlockNode(s[2])
    element %= (element + dot + func_call, lambda h, s: CallNode(*s[3], obj=s[1], token = s[2]))#arreglar
    element %= (
        element + at + type_id + dot + func_call,
        lambda h, s: CallNode(*s[5], obj=s[1], at_type=s[3], token = s[2]),
    )
    element %= func_call, lambda h, s: CallNode(*s[1],)
    element %= atom, lambda h, s: s[1]

    case_block %= case_item + case_block, lambda h, s: [s[1]] + s[2]
    case_block %= case_item, lambda h, s: [s[1]]
    case_item %= (
        idx + colon + type_id + rarrow + expr + semi,
        lambda h, s: CaseItemNode(s[1], s[3], s[5]),
    )

    atom %= num, lambda h, s: ConstantNumNode(s[1])
    atom %= idx, lambda h, s: VariableNode(s[1])
    atom %= (
        true,
        lambda h, s: BooleanNode(s[1]),
    )
    atom %= false, lambda h, s: BooleanNode(s[1])
    atom %= string, lambda h, s: StringNode(s[1])

    block %= expr + semi, lambda h, s: [s[1]]
    block %= expr + semi + block, lambda h, s: [s[1]] + s[3]

    func_call %= idx + opar + arg_list + cpar, lambda h, s: (s[1], s[3])

    arg_list %= expr + arg_list_rest, lambda h, s: [s[1]] + s[2]
    arg_list %= expr, lambda h, s: [s[1]]
    arg_list %= G.Epsilon, lambda h, s: []

    arg_list_rest %= comma + expr + arg_list_rest, lambda h, s: [s[2]] + s[3]
    arg_list_rest %= comma + expr, lambda h, s: [s[2]]

    if print_grammar:
        print(G)
    return (G, idx, type_id, string, num)
