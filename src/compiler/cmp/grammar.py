from .pycompiler import Grammar
from .ast import *
from .utils import selfToken

# grammar
G = Grammar()


# non-terminals
program = G.NonTerminal("<program>", startSymbol=True)
class_list, def_class = G.NonTerminals("<class-list> <def-class>")
feature_list, def_attr, def_func = G.NonTerminals(
    "<feature-list> <def-attr> <def-func>"
)
param_list, param, expr_list = G.NonTerminals("<param-list> <param> <expr-list>")
expr, comp, arith, term, factor, atom = G.NonTerminals(
    "<expr> <comp> <arith> <term> <factor> <atom>"
)
s_comp, s_arith, s_term, s_factor = G.NonTerminals(
    "<special_comp> <special_arith> <special_term> <special_factor>"
)
func_call, arg_list, args = G.NonTerminals("<func-call> <arg-list> <args>")
case_def, block_def, loop_def, cond_def, let_def, assign_def = G.NonTerminals(
    "<case_def> <block_def> <loop_def> <cond_def> <let_def> <assign_def>"
)
branch_list, branch = G.NonTerminals("<branch_list> <branch>")
iden_list, iden = G.NonTerminals("<iden_list> <iden>")


# terminals
classx, inherits = G.Terminals("class inherits")
let, inx = G.Terminals("let in")
case, of, esac = G.Terminals("case of esac")
whilex, loop, pool = G.Terminals("while loop pool")
ifx, then, elsex, fi = G.Terminals("if then else fi")
isvoid, notx = G.Terminals("isvoid not")
semi, colon, comma, dot, opar, cpar, ocur, ccur, larrow, rarrow, at = G.Terminals(
    "; : , . ( ) { } <- => @"
)
equal, plus, minus, star, div, less, leq, neg = G.Terminals("= + - * / < <= ~")
typeid, objectid, num, stringx, boolx, new = G.Terminals(
    "typeid objectid int string bool new"
)


# productions

program %= class_list, lambda h, s: ProgramNode(s[1])

class_list %= def_class, lambda h, s: [s[1]]
class_list %= def_class + class_list, lambda h, s: [s[1]] + s[2]

def_class %= (
    classx + typeid + ocur + feature_list + ccur + semi,
    lambda h, s: ClassDeclarationNode(s[2], s[4], s[1]),
)
def_class %= (
    classx + typeid + inherits + typeid + ocur + feature_list + ccur + semi,
    lambda h, s: ClassDeclarationNode(s[2], s[6], s[1], s[4]),
)

feature_list %= G.Epsilon, lambda h, s: []
feature_list %= def_attr + feature_list, lambda h, s: [s[1]] + s[2]
feature_list %= def_func + feature_list, lambda h, s: [s[1]] + s[2]

def_attr %= objectid + colon + typeid + semi, lambda h, s: AttrDeclarationNode(
    s[1], s[3]
)
def_attr %= (
    objectid + colon + typeid + larrow + expr + semi,
    lambda h, s: AttrDeclarationNode(s[1], s[3], s[5], s[4]),
)

def_func %= (
    objectid + opar + cpar + colon + typeid + ocur + expr + ccur + semi,
    lambda h, s: FuncDeclarationNode(s[1], [], s[5], s[7]),
)
def_func %= (
    objectid + opar + param_list + cpar + colon + typeid + ocur + expr + ccur + semi,
    lambda h, s: FuncDeclarationNode(s[1], s[3], s[6], s[8]),
)

param_list %= param, lambda h, s: [s[1]]
param_list %= param + comma + param_list, lambda h, s: [s[1]] + s[3]
param %= objectid + colon + typeid, lambda h, s: (s[1], s[3])

expr %= comp, lambda h, s: s[1]
expr %= s_comp, lambda h, s: s[1]

comp %= arith, lambda h, s: s[1]
comp %= arith + leq + arith, lambda h, s: LeqNode(s[1], s[3], s[2])
comp %= arith + less + arith, lambda h, s: LessNode(s[1], s[3], s[2])
comp %= arith + equal + arith, lambda h, s: EqualNode(s[1], s[3], s[2])

arith %= term, lambda h, s: s[1]
arith %= arith + plus + term, lambda h, s: PlusNode(s[1], s[3], s[2])
arith %= arith + minus + term, lambda h, s: MinusNode(s[1], s[3], s[2])

term %= factor, lambda h, s: s[1]
term %= term + star + factor, lambda h, s: StarNode(s[1], s[3], s[2])
term %= term + div + factor, lambda h, s: DivNode(s[1], s[3], s[2])

factor %= atom, lambda h, s: s[1]
factor %= opar + expr + cpar, lambda h, s: s[2]
factor %= isvoid + factor, lambda h, s: VoidNode(s[2], s[1])
factor %= neg + factor, lambda h, s: NegNode(s[2], s[1])
factor %= func_call, lambda h, s: s[1]
factor %= case_def, lambda h, s: s[1]
factor %= block_def, lambda h, s: s[1]
factor %= loop_def, lambda h, s: s[1]
factor %= cond_def, lambda h, s: s[1]

atom %= num, lambda h, s: ConstantNumNode(s[1])
atom %= stringx, lambda h, s: ConstantStringNode(s[1])
atom %= boolx, lambda h, s: ConstantBoolNode(s[1])
atom %= objectid, lambda h, s: VariableNode(s[1])
atom %= new + typeid, lambda h, s: InstantiateNode(s[2])

func_call %= objectid + opar + arg_list + cpar, lambda h, s: CallNode(
    VariableNode(selfToken), s[1], s[3]
)
func_call %= factor + dot + objectid + opar + arg_list + cpar, lambda h, s: CallNode(
    s[1], s[3], s[5]
)
func_call %= (
    factor + at + typeid + dot + objectid + opar + arg_list + cpar,
    lambda h, s: CallNode(s[1], s[5], s[7], s[3]),
)

arg_list %= G.Epsilon, lambda h, s: []
arg_list %= args, lambda h, s: s[1]
args %= expr, lambda h, s: [s[1]]
args %= expr + comma + args, lambda h, s: [s[1]] + s[3]

case_def %= case + expr + of + branch_list + esac, lambda h, s: CaseNode(
    s[2], s[4], s[1]
)
branch_list %= branch, lambda h, s: [s[1]]
branch_list %= branch + branch_list, lambda h, s: [s[1]] + s[2]
branch %= objectid + colon + typeid + rarrow + expr + semi, lambda h, s: CaseBranchNode(
    s[4], s[1], s[3], s[5]
)

block_def %= ocur + expr_list + ccur, lambda h, s: BlockNode(s[2], s[1])
expr_list %= expr + semi, lambda h, s: [s[1]]
expr_list %= expr + semi + expr_list, lambda h, s: [s[1]] + s[3]

loop_def %= whilex + expr + loop + expr + pool, lambda h, s: LoopNode(s[2], s[4], s[1])

cond_def %= ifx + expr + then + expr + elsex + expr + fi, lambda h, s: ConditionalNode(
    s[2], s[4], s[6], s[1]
)

s_comp %= s_arith, lambda h, s: s[1]
s_comp %= arith + leq + s_arith, lambda h, s: LeqNode(s[1], s[3], s[2])
s_comp %= arith + less + s_arith, lambda h, s: LessNode(s[1], s[3], s[2])
s_comp %= arith + equal + s_arith, lambda h, s: EqualNode(s[1], s[3], s[2])

s_arith %= s_term, lambda h, s: s[1]
s_arith %= arith + plus + s_term, lambda h, s: PlusNode(s[1], s[3], s[2])
s_arith %= arith + minus + s_term, lambda h, s: MinusNode(s[1], s[3], s[2])

s_term %= s_factor, lambda h, s: s[1]
s_term %= term + star + s_factor, lambda h, s: StarNode(s[1], s[3], s[2])
s_term %= term + div + s_factor, lambda h, s: DivNode(s[1], s[3], s[2])

s_factor %= notx + expr, lambda h, s: NotNode(s[2], s[1])
s_factor %= let_def, lambda h, s: s[1]
s_factor %= assign_def, lambda h, s: s[1]
s_factor %= isvoid + s_factor, lambda h, s: VoidNode(s[2], s[1])
s_factor %= neg + s_factor, lambda h, s: NegNode(s[2], s[1])

let_def %= let + iden_list + inx + expr, lambda h, s: LetNode(s[2], s[4], s[1])
iden_list %= iden, lambda h, s: [s[1]]
iden_list %= iden + comma + iden_list, lambda h, s: [s[1]] + s[3]
iden %= objectid + colon + typeid, lambda h, s: LetVarNode(s[1], s[3])
iden %= objectid + colon + typeid + larrow + expr, lambda h, s: LetVarNode(
    s[1], s[3], s[5], s[4]
)

assign_def %= objectid + larrow + expr, lambda h, s: AssignNode(s[1], s[3], s[2])
