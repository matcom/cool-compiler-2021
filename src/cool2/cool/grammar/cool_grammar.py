from cmp.pycompiler import Grammar, NonTerminal, Terminal
from cool.ast.ast import *

G = Grammar()

# non-terminals
program = G.NonTerminal('<program>', startSymbol=True)
class_list, def_class = G.NonTerminals('<class-list> <def-class>')
feature_list, def_attr, def_func, feature = G.NonTerminals('<feature-list> <def-attr> <def-func> <feature>')
param_list, param, expr_list = G.NonTerminals('<param-list> <param> <expr-list>')
expr, boolean, compare, arith, term, factor, negate, atom = \
    G.NonTerminals('<expr> <boolean> <compare> <arith> <term> <negate> <factor> <atom>')
func_call, arg_list, dispatch  = G.NonTerminals('<func-call> <arg-list> <dispatch>')
def_var, def_var_list = G.NonTerminals('<def-var> <def-var-list>')
case_check, case_check_list = G.NonTerminals('<case-check> <case-check-list>')

# Terminals

ifx,then,elsex,if_r,whilex,loop,loop_r = G.Terminals('if then else fi while loop pool')
ocur,ccur,colon,semi,comma, dot = G.Terminals('{ } : ; , .')
opar,cpar,plus,minus,div,star,notx,roof = G.Terminals('( ) + - / * not ~')
less,less_eq,greater,greater_eq,equal = G.Terminals('< <= > >= =')
let,inx,case,of,case_r,arrow,assign = G.Terminals('let in case of esac => <-')
true,false,num,string = G.Terminals('true false num string')
classx, inherits, new, isvoid = G.Terminals('class inherits new isvoid')
idx,typex,at = G.Terminals('id type @') # 'at' is @

# productions
program %= class_list, lambda h,s: ProgramNode(s[1],row=0,column=0)

# <class-list>   ???
class_list %= def_class, lambda h,s: [s[1]]
class_list %= def_class + class_list, lambda h,s: [s[1]] + s[2]

# <def-class>    ???
def_class %= classx + typex + ocur + feature_list + ccur + semi, lambda h,s: ClassDeclarationNode(s[2][0],s[4],row=s[1][1] ,column=s[1][2])
def_class %= classx + typex + inherits + typex + ocur + feature_list + ccur + semi, lambda h,s: ClassDeclarationNode(s[2][0],s[6],s[4][0],row=s[1][1] ,column=s[1][2])

def_class %= classx + typex + ocur + ccur + semi, lambda h,s: ClassDeclarationNode(s[2][0],[],row=s[1][1] ,column=s[1][2])
def_class %= classx + typex + inherits + typex + ocur + ccur + semi, lambda h,s: ClassDeclarationNode(s[2][0],[],s[4][0],row=s[1][1] ,column=s[1][2])

# <feature-list> ???
feature_list %= feature + semi, lambda h,s: [s[1]]
feature_list %= feature + semi + feature_list, lambda h,s: [s[1]] + s[3]

# <feature> ???
feature %= def_attr, lambda h,s: s[1]
feature %= def_func, lambda h,s: s[1]

# <def-attr>     ???
def_attr %= idx + colon + typex, lambda h,s: AttrDeclarationNode(s[1][0],s[3][0],row=s[1][1] ,column=s[1][2])
def_attr %= idx + colon + typex + assign + expr, lambda h,s: AttrDeclarationNode(s[1][0],s[3][0],s[5],row=s[1][1] ,column=s[1][2])

# <def-func>     ??? 
def_func %= idx + opar + param_list + cpar + colon + typex + ocur + expr + ccur, lambda h,s: FuncDeclarationNode(s[1][0],s[3],s[6][0],s[8],row=s[1][1] ,column=s[1][2])

param_list %= G.Epsilon, lambda h,s: [ ]
param_list %= param, lambda h,s: [ s[1] ]
param_list %= param + comma + param_list, lambda h,s: [ s[1] ] + s[3]

# <param>        ???
param %= idx + colon + typex, lambda h,s: ParamNode(s[1][0],s[3][0],row=s[1][1],column = s[1][2])

def_var %= idx + colon + typex + assign + expr, lambda h,s: VarDeclarationNode(s[1][0],s[3][0],s[5],row=s[1][1] ,column=s[1][2])
def_var %= idx + colon + typex, lambda h,s: VarDeclarationNode(s[1][0],s[3][0],None,row=s[1][1] ,column=s[1][2])

def_var_list %= def_var, lambda h,s: [ s[1] ]
def_var_list %= def_var + comma + def_var_list, lambda h,s: [ s[1] ] + s[3]

case_check %= idx + colon + typex + arrow + expr + semi, lambda h,s: CheckNode(s[1][0],s[3][0],s[5],row=s[1][1] ,column=s[1][2])

case_check_list %= case_check, lambda h,s: [ s[1] ]
case_check_list %= case_check + case_check_list, lambda h,s: [ s[1] ] + s[2]


# <expr>         ???
expr %= idx + assign + expr, lambda h,s: AssignNode(s[1][0],s[3],row=s[1][1] ,column=s[1][2])
expr %= idx + colon + typex + assign + expr, lambda h,s: VarDeclarationNode(s[1][0],s[3][0],s[5],row=s[1][1] ,column=s[1][2])
expr %= boolean, lambda h,s: s[1]
expr %= ocur + expr_list + ccur, lambda h,s: BlockNode(s[2],row=s[1][1] ,column=s[1][2])
expr %= ifx + expr + then + expr + elsex + expr + if_r, lambda h,s: ConditionalNode(s[2],s[4],s[6],row=s[1][1] ,column=s[1][2])
expr %= let + def_var_list + inx + expr, lambda h,s: LetNode(s[2],s[4],row=s[1][1] ,column=s[1][2])
expr %= case + expr + of + case_check_list + case_r, lambda h,s: CaseNode(s[2],s[4],row=s[1][1] ,column=s[1][2])
expr %= whilex + expr + loop + expr + loop_r, lambda h,s: WhileNode(s[2],s[4],row=s[1][1] ,column=s[1][2])

# <expr-list>    ???
expr_list %= expr + semi, lambda h,s: [ s[1] ]
expr_list %= expr + semi + expr_list, lambda h,s: [ s[1] ] + s[3]

# <boolean>         ???
boolean %= notx + boolean, lambda h,s: NotNode(s[2],s[1][1],s[1][2])
boolean %= compare, lambda h,s: s[1]

# <compare>         ???
compare %= arith + equal + arith     , lambda h,s: EqualNode(s[1],s[3],s[2][1],s[2][2])
compare %= arith + less + arith      , lambda h,s: LesserNode(s[1],s[3],s[2][1],s[2][2])
compare %= arith + less_eq + arith   , lambda h,s: LesserEqualNode(s[1],s[3],s[2][1],s[2][2])
compare %= arith + greater + arith   , lambda h,s: GreaterNode(s[1],s[3],s[2][1],s[2][2])
compare %= arith + greater_eq + arith, lambda h,s: GreaterEqualNode(s[1],s[3],s[2][1],s[2][2])
compare %= arith, lambda h,s: s[1]

# <arith>        ???
arith %= arith + plus + term, lambda h,s: PlusNode(s[1],s[3],row=s[2][1] ,column=s[2][2])
arith %= arith + minus + term, lambda h,s: MinusNode(s[1],s[3],row=s[2][1] ,column=s[2][2])
arith %= term, lambda h,s: s[1]

# <term>         ???
term %= term + star + factor, lambda h,s: StarNode(s[1],s[3],row=s[2][1] ,column=s[2][2])
term %= term + div + factor,  lambda h,s: DivNode(s[1],s[3],row=s[2][1] ,column=s[2][2])
term %= factor,  lambda h,s: s[1]

# <factor>       ???
factor %= isvoid + factor, lambda h,s: IsVoidNode(s[2],row=s[1][1] ,column=s[1][2])
factor %= negate, lambda h,s: s[1]

# <negate>
negate %= roof + negate, lambda h,s: RoofNode(s[2],row=s[1][1] ,column=s[1][2])
negate %= dispatch, lambda h,s: s[1]

# <dispatch> 
dispatch %= dispatch + at + typex + dot + func_call, lambda h,s: CallNode(s[1],s[5][1],s[5][2],s[3][0],row=s[5][3] ,column=s[5][4])
dispatch %= dispatch + dot + func_call, lambda h,s: CallNode(s[1],s[3][1],s[3][2],None,row=s[3][3] ,column=s[3][4])
dispatch %= atom, lambda h,s: s[1]

# <atom>         ???
atom %= num, lambda h,s: ConstantNumNode(s[1][0],row=s[1][1] ,column=s[1][2])
atom %= string, lambda h,s: StringNode(s[1][0],row=s[1][1] ,column=s[1][2])
atom %= true, lambda h,s: BoolNode(s[1][0],row=s[1][1] ,column=s[1][2])
atom %= false, lambda h,s: BoolNode(s[1][0],row=s[1][1] ,column=s[1][2])
atom %= idx, lambda h,s: VariableNode(s[1][0],row=s[1][1] ,column=s[1][2])
atom %= new + typex, lambda h,s: InstantiateNode(s[2][0],row=s[1][1] ,column=s[1][2])
atom %= func_call, lambda h,s: CallNode(s[1][0],s[1][1],s[1][2],None,row=s[1][3] ,column=s[1][4])
atom %= at + typex + dot + func_call, lambda h,s: CallNode(s[4][0],s[4][1],s[4][2],s[2][0],row=s[4][3] ,column=s[4][4])
atom %= opar + expr + cpar, lambda h,s: s[2]

# <func-call>    ???
func_call %= idx + opar + arg_list + cpar, lambda h,s: (VariableNode('self',s[1][1],s[1][2]),s[1][0],s[3],s[1][1],s[1][2])

arg_list %= G.Epsilon, lambda h,s: [ ]
arg_list %= expr, lambda h,s: [ s[1] ]
arg_list %= expr + comma + arg_list, lambda h,s: [ s[1] ] + s[3]
