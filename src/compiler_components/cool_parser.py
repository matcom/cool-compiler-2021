from compiler_component import CompilerComponent
from lexer import Tokenizer, Lexer
from ast import *
import ply.yacc as yacc
import ply.lex as lex

t = Tokenizer()
tokens = t.tokens
lexer = lex.lex(t)

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
                 | CLASS ID DOUBLE_DOT ID LBRACE feature_list RBRACE
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
    '''def_attr : ID DOUBLE_DOT ID SEMICOLON
    '''
    p[0] = AttrDeclarationNode(p[1], p[3])

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
    '''expr : LET ID DOUBLE_DOT ID EQUALS expr
            | LET ID EQUALS expr
    '''
    if len(p) > 5:
        p[0] = VarDeclarationNode(p[2], p[4], p[6])
    else:
        p[0] = AssignNode(p[2], p[4])

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

def p_func_call(p):
    '''func_call : factor DOT ID LPAREN arg_list RPAREN
    '''
    p[0] = CallNode(p[1], p[3], p[5])

def p_arg_list(p):
    '''arg_list : expr
                | expr COMMA arg_list
    '''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[3]

def p_error(p):
    print(p)

############## End Grammar ############################


class Parser(CompilerComponent):

    def __init__(self, lexer: Lexer) -> None:
        super().__init__()
        self.lexer = lexer

    def execute(self):
       pass

    def has_errors(self):
        pass

    def print_errors(self):
        pass

data = '''class A { 
    f(a:int,b:bool,c:hijo):hello{1};

    };'''  
parser = yacc.yacc()
result = parser.parse(data, debug=True)
print(result.visit())