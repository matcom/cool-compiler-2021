from cmp.pycompiler import Grammar
from AST import *

# Grammar
G = Grammar()

# Non-terminals
program = G.NonTerminal('<program>', startSymbol=True)
class_list, def_class = G.NonTerminals('<class-list> <def-class>')
feature_list, def_attr, def_func = G.NonTerminals('<feature-list> <def-attr> <def-func>')
param_list, param = G.NonTerminals('<param-list> <param>')
expr, expr_list, arg_list = G.NonTerminals('<expr> <expr-list> <arg-list>')
case_attr, case_attr_list, let_list, attr_let = G.NonTerminals('<case-attr> <case-attr-list> <let-list> <attr-let>')
compare, arith, term, factor, atom = G.NonTerminals('<compare> <arith> <term> <factor> <atom>')

# Terminals
classx, inherits = G.Terminals('class inherits') 
let, inx = G.Terminals('let in')
ifx, then, elsex, fi = G.Terminals('if then else fi')
whilex, loop, pool = G.Terminals('while loop pool')
case, of, esac = G.Terminals('case of esac')
semi, colon, comma, dot, opar, cpar, ocur, ccur, arrow, imp, at, less, eless, prime = G.Terminals('; : , . ( ) { } assig case_assig @ < eless ~')
equal, plus, minus, star, div = G.Terminals('= + - * /')
idx, num, new, isvoid, notx, string, true, false = G.Terminals('id int new isvoid not string true false')

# Productions
program %= class_list, lambda h,s: ProgramNode(s[1])

# <class-list>
class_list %= def_class + semi + class_list, lambda h,s: [s[1]] + s[3]
class_list %= def_class + semi, lambda h,s: [s[1]]

# <def-class>
def_class %= classx + idx + ocur + feature_list + ccur, lambda h,s: ClassDeclarationNode(s[2],s[4])
def_class %= classx + idx + inherits + idx + ocur + feature_list + ccur, lambda h,s: ClassDeclarationNode(s[2],s[6],s[4])

# <feature-list>
feature_list %= def_attr + semi + feature_list, lambda h,s: [s[1]] + s[3]
feature_list %= def_func + semi + feature_list, lambda h,s: [s[1]] + s[3]
feature_list %= G.Epsilon, lambda h,s: []

# <def-attr>
def_attr %= idx + colon + idx, lambda h,s: AttrDeclarationNode(s[1],s[3]) 
def_attr %= idx + colon + idx + arrow + expr, lambda h,s: AttrDeclarationNode(s[1],s[3],s[5]) 

# <def-func>
def_func %= idx + opar + param_list + cpar + colon + idx + ocur + expr + ccur, lambda h,s: FuncDeclarationNode(s[1],s[6],s[8],s[3])

# <param-list>
param_list %= param + comma + param_list, lambda h,s: [s[1]] + s[3]
param_list %= param, lambda h,s: [s[1]]
param_list %= G.Epsilon, lambda h,s: []

# <param>
param %= idx + colon + idx, lambda h,s: VarDeclarationNode(s[1],s[3])

# <expr-list>
expr_list %= expr + semi, lambda h,s: [s[1]] 
expr_list %= expr + semi + expr_list, lambda h,s: [s[1]] + s[3]

# <expr>
# assigment
expr %= idx + arrow + expr, lambda h,s: AssignNode(VariableNode(s[1]),s[3])
# loop
expr %= whilex + expr + loop + expr + pool, lambda h,s: LoopNode(s[2],s[4])
# block 
expr %= ocur + expr_list + ccur, lambda h,s: BlockNode(s[2])
# let
expr %= let + let_list + inx + expr, lambda h,s: LetNode(s[2],s[4])
# case
expr %= case + expr + of + case_attr_list + esac, lambda h,s: CaseNode(s[2],s[4])
# is_void
expr %= isvoid + expr, lambda h,s: IsVoidNode(s[2])  
# not 
expr %= notx + expr, lambda h,s: NotNode(s[2])
# compare
expr %= compare, lambda h,s: s[1]

# <compare>
compare %= compare + less + arith, lambda h,s: LessNode(s[1],s[3])
compare %= compare + eless + arith, lambda h,s: ElessNode(s[1],s[3])
compare %= compare + equal + arith, lambda h,s: EqualsNode(s[1],s[3])
compare %= arith, lambda h,s: s[1]

# <arith>
arith %= prime + arith, lambda h,s: PrimeNode(s[2]) 
arith %= arith + plus + term, lambda h,s: PlusNode(s[1],s[3])
arith %= arith + minus + term, lambda h,s: MinusNode(s[1],s[3]) 
arith %= term, lambda h,s: s[1]

# <term>
term %= term + star + factor, lambda h,s: StarNode(s[1],s[3])
term %= term + div + factor, lambda h,s: DivNode(s[1],s[3])
term %= factor, lambda h,s: s[1]

# <factor>
factor %= atom, lambda h,s: s[1]
factor %= opar + expr + cpar, lambda h,s: s[2]
factor %= new + idx,  lambda h,s: InstantiateNode(s[2])

# <atom>
atom %= false, lambda h,s: FalseNode(s[1])
atom %= true, lambda h,s: TrueNode(s[1])
atom %= num, lambda h,s: ConstantNumNode(s[1])
atom %= string, lambda h,s: StringNode(s[1])
atom %= idx, lambda h,s: VariableNode(s[1])
atom %= factor + at + idx + dot + idx + opar + arg_list + cpar, lambda h,s: DispatchNode(s[5],s[3],s[7],s[1])
atom %= factor + dot + idx + opar + arg_list + cpar, lambda h,s: DispatchNode(s[3],None,s[5],s[1])
atom %= idx + opar + arg_list + cpar, lambda h,s: DispatchNode(s[1],None,s[3])
atom %= ifx + expr + then + expr + elsex + expr + fi, lambda h,s: ConditionalNode(s[2],s[4],s[6])

# <arg-list>
arg_list %= expr, lambda h,s: [s[1]]
arg_list %= expr + comma + arg_list, lambda h,s: [s[1]] + s[3]
arg_list %= G.Epsilon, lambda h,s: []

# <let-list>
let_list %= attr_let + comma + let_list, lambda h,s: [s[1]] + s[3]
let_list %= attr_let, lambda h,s: [s[1]] 

# <attr-let>
attr_let %= idx + colon + idx, lambda h,s: VarDeclarationNode(s[1],s[3])
attr_let %= idx + colon + idx + arrow + expr, lambda h,s: VarDeclarationNode(s[1],s[3],s[5])

# <case-attr-list>
case_attr_list %= case_attr + semi + case_attr_list, lambda h,s: [s[1]] + s[3]
case_attr_list %= case_attr + semi, lambda h,s: [s[1]]

# <attr-case>
case_attr %= idx + colon + idx + imp + expr, lambda h,s: CaseAttrNode(s[1],s[3],s[5])


# Print tokens
def pprint_tokens(tokens):
    indent = 0
    pending = []
    for token in tokens:
        pending.append(token)
        if token.token_type in { ocur, ccur, semi }:
            if token.token_type == ccur:
                indent -= 1
            print('    '*indent + ' '.join(str(t.token_type) for t in pending))
            pending.clear()
            if token.token_type == ocur:
                indent += 1
    print(' '.join([str(t.token_type) for t in pending]))