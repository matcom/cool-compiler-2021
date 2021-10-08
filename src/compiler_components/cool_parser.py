from compiler_component import CompilerComponent
from lexer import Tokenizer, Lexer
from ast import *
import ply.yacc as yacc
import ply.lex as lex

t = Tokenizer()
tokens = t.tokens
lexer = lex.lex(t)
errors = []

##### Grammar ####################
def p_program(p):
    'program : class_list'
    p[0] = ProgramNode(p[1])

def p_class_list(p):
    '''class_list : def_class SEMICOLON
                  | def_class SEMICOLON class_list
       '''
    if len(p) == 3:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[3]  

def p_def_class(p):
    '''def_class : CLASS ID LBRACE feature_list RBRACE
                 | CLASS ID INHERITS ID LBRACE feature_list RBRACE
    '''
    if len(p) == 6:
        p[0] = ClassDeclarationNode(p[2], p[4])
    else:
        p[0] = ClassDeclarationNode(p[2], p[6], p[4])

def p_empty(p):
    'empty :'
    pass

def p_feature_list(p):
    '''feature_list : def_attr SEMICOLON feature_list
                    | def_func SEMICOLON feature_list
                    | empty
    '''
    if len(p) == 2:
        p[0] = []
    else:
        p[0] = [p[1]] + p[3]

def p_def_attr(p):
    '''def_attr : ID DOUBLE_DOT ID
                | ID DOUBLE_DOT ID LEFT_ARROW expr
    '''
    if len(p) == 4:
        p[0] = AttrDeclarationNode(p[1], p[3])
    else:
        p[0] = AttrDeclarationNode(p[1], p[3], p[5])

def p_def_func(p):
    '''def_func : ID LPAREN param_list RPAREN DOUBLE_DOT ID LBRACE expr RBRACE
    '''
    p[0] = FuncDeclarationNode(p[1], p[3], p[6], p[8])

def p_param_list(p):
    '''param_list : param
                  | param COMMA param_list
    '''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[3]

def p_param(p):
    '''param : ID DOUBLE_DOT ID
    '''
    p[0] = [p[1], p[3]]

def p_expr_list(p):
    '''expr_list : expr SEMICOLON
                 | expr SEMICOLON expr_list
    '''
    if len(p) == 3:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[3]

def p_expr(p):
    'expr : arith'
    p[0] = p[1]

def p_expr2(p):
    'expr : ID LEFT_ARROW expr'
    p[0] = AssignNode(p[1], p[3])

def p_arith(p):
    '''arith : term
             | arith PLUS term
             | arith MINUS term
    '''
    if len(p) == 2:
        p[0] = p[1]
    else:
        if p[2] == '+':
            p[0] = PlusNode(p[1], p[3])
        else:
            p[0] = MinusNode(p[1], p[3])

def p_term(p):
    '''term : factor
             | term TIMES factor
             | term DIVIDE factor
    '''
    if len(p) == 2:
        p[0] = p[1]
    else:
        if p[2] == '*':
            p[0] = StarNode(p[1], p[3])
        else:
            p[0] = DivNode(p[1], p[3])

def p_factor(p):
    '''factor : atom
              | LPAREN expr RPAREN
    '''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[2]

#4 (por ahora) metodos para el no-terminal 'atom' 
def p_atom1(p):
    'atom : ID'
    p[0] = VariableNode(p[1])

def p_atom2(p):
    'atom : NUMBER'
    p[0] = ConstantNumNode(p[1])

def p_atom3(p):
    'atom : func_call'
    p[0] = p[1]

def p_atom4(p):
    '''atom : NEW ID LPAREN RPAREN 
    '''
    p[0] = InstantiateNode(p[2])

def p_atomString(p):
    'atom : STRING'
    print(p[1][1:len(p[1]) -1 ])
    p[0] = ConstantStringNode(p[1][1:len(p[1]) -1 ])

def p_atomBool(p):
    '''atom : TRUE
            | FALSE
    '''
    if p[1].lower() == "true":
        p[0] = ConstantBooleanNode(True)
    else:
        p[0] = ConstantBooleanNode(False)

def p_atomSelf(p):
    'atom : SELF'
    p[0] = SelfNode(None)

def p_func_call(p):
    '''func_call : factor DOT ID LPAREN arg_list RPAREN
    '''
    if not p[5][0] is None:
        p[0] = CallNode(p[1], p[3], p[5])
    else:
        p[0] = CallNode(p[1], p[3])


def p_arg_list(p):
    '''arg_list : expr
                | expr COMMA arg_list
                | empty
    '''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[3]


def p_error(p):
    if p:
        errors.append("sintax error at line " + str(p.lineno) + " --> token: '" + p.value + "'")
    else:
        errors.append("sintanx error at end of file")

############## End Grammar ############################


class Parser(CompilerComponent):

    def __init__(self, lexer: Lexer) -> None:
        super().__init__()
        self.lexer = lexer

    def execute(self):
       parser = yacc.yacc()
       errors = []
       self.ast = parser.parse(self.lexer.cool_program)

    def has_errors(self):
        return len(errors) == 0

    def print_errors(self):
        for e in errors:
            print(e)
        print()


################ TEsting zone ###########################
data = '''class A inheritS B{ 
    a:int ;
    f(a:int,b:bool,c:hijo):hello{hola <- f()};

    };'''  
parser = yacc.yacc()
result = parser.parse(data)
if len(errors) == 0:
    print(result.visit())
else:
    print(errors)

########################################################