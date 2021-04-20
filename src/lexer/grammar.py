from cmp.pycompiler import Grammar


def CoolGrammar():
    G = Grammar()

    program = G.NonTerminal('<program>', startSymbol=True)
    
    class_list, feature_list, block_list = G.NonTerminals('<class-list> <feature-list> <block-list>')
    param_list, expr_list, expr_add_list = G.NonTerminal('<param-list> <expr-list> <expr-add-list>')
    init_list, branch_list = G.NonTerminals('<init-list> <branch-list>')
    
    def_class, def_attr, def_meth = G.NonTerminals('<def-class> <def-attr> <def-meth>')
    
    disp_add, let_add = G.NonTerminals('<disp_add> <let_add>')
    
    expression, parameter = G.NonTerminals('<expr> <param>')

    less, leq, eq = G.Terminals('< <= =')
    plus, minus, star, div = G.Terminals('+ - * /')
    opar, cpar, ocur, ccur = G.Terminals('( ) { }')
    tash, dot, colon, semi, comma = G.Terminals('~ . : ; ,')
    assi, strudle, impl = G.Terminal('<- @ =>')

    _class, _type, _id, _int, _string = G.Terminals('class type int string')
    _if, _else, _while, _in = G.Terminals('if else while in')
    
    inherits, true, false = G.Terminal('inherits true false')
    then, fi, loop, pool = G.Terminals('then fi loop pool')
    let, case, of, esac = G.Terminals('let case of esac')
    new, isvoid = G.Terminals('new isvoid')

    program %= class_list

    class_list %= def_class + semi + class_list
    class_list %=  G.Epsilon

    def_class %= _class + _type + ocur + feature_list + ccur
    def_class %= _class + _type + inherits + _type + ocur + feature_list + ccur

    feature_list %= def_attr + semi + feature_list
    feature_list %= def_meth + semi + feature_list
    feature_list %= G.Epsilon

    def_attr %= _id + colon + _type
    def_attr %= _id + colon + _type + assi + expression

    def_meth %= _id + opar + param_list + cpar + colon + _type + ocur + expression + ccur
    
    #Expressions:
    
    #Assignment 
    expression %= _id + assi + expression
    
    #Dispatch
    expression %= expression + disp_add + dot + _id + opar + expr_list + cpar
    disp_add %= strudle + _type
    disp_add %= G.Epsilon
    expr_list %= expr_add_list
    expr_list %= G.Epsilon
    expr_add_list %= expression
    expr_add_list %= expression + comma + expr_add_list
    
    #Conditionals
    expression %= _if + expression + then + expression + _else + expression + fi
        
    #Loops
    expression %= _while + expression + loop + expression + pool
        
    #Blocks
    expression %= ocur + block_list  + ccur
    block_list %= expression + semi
    block_list %= expression + semi + block_list
        
    #Let
    expression %= let + init_list + colon + _type + let_add + _in + expression
    init_list %= _id + colon + _type + let_add
    init_list %= _id + colon + _type + let_add + comma + init_list
    let_add %= assi + expression
    let_add %= G.Epsilon
        
    #Case
    expression %= case + expression + of + branch_list + esac
    branch_list %= _id + colo + _type + impl + expression + semi
    branch_list %= _id + colo + _type + impl + expression + semi + branch_list
        
    #New
    expression %= new + _type
    
    #Isvoid
    expression %= isvoid + expression
    
    #Arithmetics
    expression %= expression + plus + expression
    expression %= expression + minus + expression
    expression %= expression + star + expression
    expression %= expression + div + expression
    
    #Other
    expression %= tash + expression
    
    expression %= expression + less + expression
    expression %= expression + leq + expression
    expression %= expression + eq + expression

    expression %= _not + expression

    expression %= opar + expression + cpar

    #Identifiers
    expression %= _id

    #Constants
    expression %= _int
    expression %= _string
    expression %= false
    expression %= true  

    return G