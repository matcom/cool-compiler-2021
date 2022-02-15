from core.tools.pycompiler import Grammar
from core.tools.Parser_LR1 import LR1Parser
from core.tools.COOLAst import *


# Representacion de la gramatica de COOL utilizando la clase grammar
CoolGrammar = Grammar()

# noterminales
program = CoolGrammar.NonTerminal('<program>', startSymbol=True)
class_list, def_class = CoolGrammar.NonTerminals('<class-list> <def-class>')
feature_list, feature = CoolGrammar.NonTerminals('<feature-list> <feature>')
param_list, param = CoolGrammar.NonTerminals('<param-list> <param>')
expr_1, expr_2, member_call, expr_list, let_list, case_list = CoolGrammar.NonTerminals(
    '<expr_1> <expr_2> <member-call> <expr-list> <let-list> <case-list>')
comp_expr, arith, arith_2, term, factor, factor_2 = CoolGrammar.NonTerminals(
    '<comp-expr> <arith> <arith-2> <term> <factor> <factor-2>')
atom, func_call, arg_list = CoolGrammar.NonTerminals('<atom> <func-call> <arg-list>')

# terminales
classx, inherits, function = CoolGrammar.Terminals('class inherits function')
ifx, then, elsex, fi = CoolGrammar.Terminals('if then else fi')
whilex, loop, pool = CoolGrammar.Terminals('while loop pool')
let, inx = CoolGrammar.Terminals('let in')
case, of, esac = CoolGrammar.Terminals('case of esac')
semi, colon, comma, dot, at, opar, cpar, ocur, ccur, larrow, rarrow = CoolGrammar.Terminals(
    '; : , . @ ( ) { } <- =>')
plus, minus, star, div, isvoid, compl = CoolGrammar.Terminals('+ - * / isvoid ~')
notx, less, leq, equal = CoolGrammar.Terminals('not < <= =')
new, idx, typex, integer, string, boolx = CoolGrammar.Terminals('new id type integer string bool')

# Producciones
program %= class_list, lambda h, s: ProgramNode(s[1])

# Lista de clases
class_list %= def_class + class_list, lambda h, s: [s[1]] + s[2]
class_list %= def_class, lambda h, s: [s[1]]

# Defincicion de la clase
def_class %= classx + typex + ocur + feature_list + ccur + semi, lambda h, s: ClassDeclarationNode(s[1], s[2], s[4])
def_class %= classx + typex + inherits + typex + ocur + feature_list + ccur + semi, lambda h, s: ClassDeclarationNode(
    s[1], s[2], s[6], s[4])

# Lista de propiedades de la clase
feature_list %= feature + feature_list, lambda h, s: [s[1]] + s[2]
feature_list %= CoolGrammar.Epsilon, lambda h, s: []

# Atributos de la clase
feature %= idx + colon + typex + semi, lambda h, s: AttrDeclarationNode(s[1], s[3])
feature %= idx + colon + typex + larrow + expr_1 + semi, lambda h, s: AttrDeclarationNode(s[1], s[3], s[5])

# Metodos constructores de la clase
feature %= idx + opar + param_list + cpar + colon + typex + ocur + expr_1 + ccur + semi, lambda h, s: FuncDeclarationNode(
    s[1], s[3], s[6], s[8])
feature %= idx + opar + cpar + colon + typex + ocur + expr_1 + ccur + semi, lambda h, s: FuncDeclarationNode(s[1], [],
                                                                                                           s[5], s[7])
# Metodos de la clase
feature %= function + idx + opar + param_list + cpar + colon + typex + ocur + expr_1 + ccur + semi, lambda h, s: FuncDeclarationNode(
    s[2], s[4], s[7], s[9])
feature %= function + idx + opar + cpar + colon + typex + ocur + expr_1 + ccur + semi, lambda h, s: FuncDeclarationNode(s[2], [],
                                                                                                           s[6], s[8])
# Lista de parametros de funcion
param_list %= param, lambda h, s: [s[1]]
param_list %= param + comma + param_list, lambda h, s: [s[1]] + s[3]

# parametro de funcion
param %= idx + colon + typex, lambda h, s: (s[1], s[3])

### Expresiones ###
# Expresion Let-in
expr_1 %= let + let_list + inx + expr_1, lambda h, s: LetInNode(s[1], s[2], s[4])
let_list %= idx + colon + typex, lambda h, s: [(s[1], s[3], None)]
let_list %= idx + colon + typex + larrow + expr_1, lambda h, s: [(s[1], s[3], s[5])]
let_list %= idx + colon + typex + comma + let_list, lambda h, s: [(s[1], s[3], None)] + s[5]
let_list %= idx + colon + typex + larrow + expr_1 + comma + let_list, lambda h, s: [(s[1], s[3], s[5])] + s[7]

expr_1 %= idx + larrow + expr_1, lambda h, s: AssignNode(s[1], s[3])
expr_1 %= notx + expr_1, lambda h, s: NotNode(s[1], s[2])
expr_1 %= expr_2 + equal + expr_1, lambda h, s: EqualNode(s[1], s[2], s[3])
expr_1 %= expr_2, lambda h, s: s[1]

expr_2 %= arith + less + arith, lambda h, s: LessNode(s[1], s[2], s[3])
expr_2 %= arith + leq + arith, lambda h, s: LessEqualNode(s[1], s[2], s[3])
expr_2 %= arith, lambda h, s: s[1]

#Expresiones aritmeticas
arith %= arith + plus + factor, lambda h, s: PlusNode(s[1], s[2], s[3])
arith %= arith + minus + factor, lambda h, s: MinusNode(s[1], s[2], s[3])
arith %= factor, lambda h, s: s[1]

factor %= factor + star + term, lambda h, s: StarNode(s[1], s[2], s[3])
factor %= factor + div + term, lambda h, s: DivNode(s[1], s[2], s[3])
factor %= term, lambda h, s: s[1]

term %= compl + term, lambda h, s: ComplementNode(s[1], s[2])
term %= isvoid + term, lambda h, s: IsVoidNode(s[1], s[2])
term %= atom, lambda h, s: s[1]

# Encapsulaciones atomicas
atom %= opar + expr_1 + cpar, lambda h, s: s[2]
atom %= integer, lambda h, s: IntegerNode(s[1])
atom %= string, lambda h, s: StringNode(s[1])
atom %= boolx, lambda h, s: BoolNode(s[1])
atom %= idx, lambda h, s: IdNode(s[1])
atom %= ifx + expr_1 + then + expr_1 + elsex + expr_1 + fi, lambda h, s: IfThenElseNode(s[1], s[2], s[4], s[6])
atom %= whilex + expr_1 + loop + expr_1 + pool, lambda h, s: WhileLoopNode(s[1], s[2], s[4])

# Expresion new
atom %= new + typex, lambda h, s: NewNode(s[1], s[2])

# Encapsulamiento entre corchetes
atom %= ocur + expr_list + ccur, lambda h, s: BlockNode(s[1], s[2])
expr_list %= expr_1 + semi, lambda h, s: [s[1]]
expr_list %= expr_1 + semi + expr_list, lambda h, s: [s[1]] + s[3]

# Expresion Case of
atom %= case + expr_1 + of + case_list + esac, lambda h, s: CaseOfNode(s[1], s[2], s[4])
case_list %= idx + colon + typex + rarrow + expr_1 + semi, lambda h, s: [(s[1], s[3], s[5])]
case_list %= idx + colon + typex + rarrow + expr_1 + semi + case_list, lambda h, s: [(s[1], s[3], s[5])] + s[7]

atom %= func_call, lambda h, s: s[1]

# Llamado a funcion
func_call %= atom + at + typex + dot + idx + opar + arg_list + cpar, lambda h, s: FunctionCallNode(s[1], s[5], s[7], s[3])
func_call %= atom + at + typex + dot + idx + opar + cpar, lambda h, s: FunctionCallNode(s[1], s[5], [], s[3])
func_call %= atom + dot + idx + opar + arg_list + cpar, lambda h, s: FunctionCallNode(s[1], s[3], s[5])
func_call %= atom + dot + idx + opar + cpar, lambda h, s: FunctionCallNode(s[1], s[3], [])

# Llamado a miembro de clase
func_call %= idx + opar + arg_list + cpar, lambda h, s: MemberCallNode(s[1], s[3])
func_call %= idx + opar + cpar, lambda h, s: MemberCallNode(s[1], [])

# Lista de argumentos
arg_list %= expr_1, lambda h, s: [s[1]]
arg_list %= expr_1 + comma + arg_list, lambda h, s: [s[1]] + s[3]

# parser
CoolParser = LR1Parser(CoolGrammar)
