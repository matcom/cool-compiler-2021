from .compiler_component import CompilerComponent
from .lexer import Tokenizer, Lexer
from .ast import *
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
    '''def_class : CLASS type_id LBRACE feature_list RBRACE
                 | CLASS type_id INHERITS type_inherit LBRACE feature_list RBRACE
    '''
    
    line, column = calculate_position(p.lexer.lexdata, p.lexer.lexpos)

    if len(p) == 6:
        p[0] = ClassDeclarationNode(p[2]['value'], p[4], line = line, column = column, type_line = p[2]['line'], type_column = p[2]['column'])
    else:
        p[0] = ClassDeclarationNode(p[2]['value'], p[6], p[4]['value'], line = line, column = column, line_father = p[4]['line'], column_father = p[4]['column'], type_line = p[2]['line'], type_column = p[2]['column'])

def p_type_inherit(p):
    'type_inherit : TYPE_ID'
    line, column = calculate_position(p.lexer.lexdata, p.lexer.lexpos)
    p[0] = {'value':p[1], 'line':line, 'column':column}

def p_type_id(p):
    'type_id : TYPE_ID'
    line, column = calculate_position(p.lexer.lexdata, p.lexer.lexpos)
    p[0] = {'value':p[1], 'line':line, 'column':column}

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
    '''def_attr : ID DOUBLE_DOT TYPE_ID
                | ID DOUBLE_DOT TYPE_ID LEFT_ARROW expr
    '''
    line, column = calculate_position(p.lexer.lexdata, p.lexer.lexpos)
    if len(p) == 4:
        p[0] = AttrDeclarationNode(p[1], p[3], line = line, column = column)
    else:
        p[0] = AttrDeclarationNode(p[1], p[3], p[5], line = line, column = column)

def p_def_func(p):
    '''def_func : ID LPAREN param_list RPAREN DOUBLE_DOT TYPE_ID LBRACE expr RBRACE
    '''
    line, column = calculate_position(p.lexer.lexdata, p.lexer.lexpos)
    p[0] = FuncDeclarationNode(p[1], p[3], p[6], p[8], line = line, column = column)

def p_param_list(p):
    '''param_list : param param_list2
                  | empty
    '''
    if len(p) == 3:
        p[0] = [p[1]] + p[2]
    else:
        p[0] = []

def p_param_list2(p):
    '''param_list2 : COMMA param param_list2
                   | empty
    '''
    if len(p) == 4:
        p[0] = [p[2]] + p[3]
    else:
        p[0] = [] 

def p_param(p):
    '''param : ID DOUBLE_DOT TYPE_ID
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
    'expr : bool'
    p[0] = p[1]

def p_bool(p):
    '''bool : NOT bool
            | arith MINOR arith
            | arith MINOR_EQUALS arith
            | arith EQUALS arith
            | arith
    '''
    line, column = calculate_position(p.lexer.lexdata, p.lexer.lexpos)
    if len(p) == 3:
        p[0] = NotNode(p[2], line = line, column = column)

    elif len(p) == 2:
        p[0] = p[1]
    else:
        if p[2] == '<':
            p[0] = MinorNode(p[1], p[3], line = line, column = column)
        elif p[2] == '<=':
            p[0] = MinorEqualsNode(p[1], p[3], line = line, column = column)
        else:
            p[0] = EqualsNode(p[1], p[3], line = line, column = column)

def p_expr2(p):
    'expr : ID LEFT_ARROW expr'
    line, column = calculate_position(p.lexer.lexdata, p.lexer.lexpos)
    p[0] = AssignNode(p[1], p[3], line = line, column = column)

def p_arith(p):
    '''arith : term
             | NOT bool   
             | arith PLUS term
             | arith MINUS term
    '''
    line, column = calculate_position(p.lexer.lexdata, p.lexer.lexpos)
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 3:
        p[0] = NotNode(p[2], line = line, column = column)
    else:
        if p[2] == '+':
            p[0] = PlusNode(p[1], p[3], line = line, column = column)
        else:
            p[0] = MinusNode(p[1], p[3], line = line, column = column)

def p_term(p):
    '''term : factor
             | term TIMES factor
             | term DIVIDE factor
    '''
    line, column = calculate_position(p.lexer.lexdata, p.lexer.lexpos)
    if len(p) == 2:
        p[0] = p[1]
    else:
        if p[2] == '*':
            p[0] = StarNode(p[1], p[3], line = line, column = column)
        else:
            p[0] = DivNode(p[1], p[3], line = line, column = column)

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
    line, column = calculate_position(p.lexer.lexdata, p.lexer.lexpos)
    p[0] = VariableNode(p[1], line = line, column = column)

def p_atom2(p):
    'atom : NUMBER'
    line, column = calculate_position(p.lexer.lexdata, p.lexer.lexpos)
    p[0] = ConstantNumNode(p[1], line = line, column = column)

def p_atom3(p):
    'atom : func_call'
    p[0] = p[1]

def p_atom4(p):
    '''atom : NEW TYPE_ID 
    '''
    line, column = calculate_position(p.lexer.lexdata, p.lexer.lexpos)
    p[0] = InstantiateNode(p[2], line = line, column = column)

def p_atomString(p):
    'atom : STRING'
    line, column = calculate_position(p.lexer.lexdata, p.lexer.lexpos)
    p[0] = ConstantStringNode(p[1][1:len(p[1]) -1 ], line = line, column = column)

def p_atomBool(p):
    '''atom : TRUE
            | FALSE
    '''
    line, column = calculate_position(p.lexer.lexdata, p.lexer.lexpos)
    if p[1].lower() == "true":
        p[0] = ConstantBooleanNode(True, line = line, column = column)
    else:
        p[0] = ConstantBooleanNode(False, line = line, column = column)

#def p_atomSelf(p):
    #'atom : SELF'
    #p[0] = SelfNode(None)

def p_atomIF(p):
    'atom : IF expr THEN expr ELSE expr FI'
    line, column = calculate_position(p.lexer.lexdata, p.lexer.lexpos)
    p[0] = IfNode(p[2], p[4], p[6], line = line, column = column)

def p_atomCicle(p):
    'atom : WHILE expr LOOP expr POOL'
    line, column = calculate_position(p.lexer.lexdata, p.lexer.lexpos)
    p[0] = WhileNode(p[2], p[4], line = line, column = column)

def p_atomBlock(p):
    'atom : LBRACE expr_list RBRACE'
    line, column = calculate_position(p.lexer.lexdata, p.lexer.lexpos)
    p[0] = BlockNode(p[2], line = line, column = column)

def p_atomLet(p):
    'atom : LET atr_decl_list IN expr'
    line, column = calculate_position(p.lexer.lexdata, p.lexer.lexpos)
    p[0] = LetNode(p[2], p[4], line = line, column = column)

def p_atr_decl_list(p):
    '''atr_decl_list : def_attr
                     | def_attr COMMA atr_decl_list    
    
    '''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[3]

def p_atomCase(p):
    'atom : CASE expr OF case_list ESAC'
    line, column = calculate_position(p.lexer.lexdata, p.lexer.lexpos)
    p[0] = CaseNode(p[2], p[4], line = line, column = column)

def p_caseList(p):
    '''case_list : ID DOUBLE_DOT TYPE_ID RIGHT_ARROW expr SEMICOLON
                 | ID DOUBLE_DOT TYPE_ID RIGHT_ARROW expr SEMICOLON case_list
    '''
    line, column = calculate_position(p.lexer.lexdata, p.lexer.lexpos)
    if len(p) == 7:
        p[0] = [AttrDeclarationNode(p[1], p[3], p[5], line = line, column = column)]
    else:
        p[0] = [AttrDeclarationNode(p[1], p[3], p[5], line = line, column = column)] + p[7]

def p_atomIsVoid(p):
    'atom : ISVOID factor'
    line, column = calculate_position(p.lexer.lexdata, p.lexer.lexpos)
    p[0] = IsVoidNode(p[2], line = line, column = column)

'''
def p_atomNot(p):
    'atom : NOT factor'
    p[0] = NotNode(p[2])
'''

def p_atomNhanhara(p):
    'atom : NHANHARA factor'
    line, column = calculate_position(p.lexer.lexdata, p.lexer.lexpos)
    p[0] = NhanharaNode(p[2], line = line, column = column)

def p_func_call(p):
    '''func_call : factor DOT ID LPAREN arg_list RPAREN
    '''
    line, column = calculate_position(p.lexer.lexdata, p.lexer.lexpos)
    p[0] = DispatchNode(p[1], p[3], p[5], line = line, column = column)

def p_func_call2(p):
    'func_call : ID LPAREN arg_list RPAREN'
    line, column = calculate_position(p.lexer.lexdata, p.lexer.lexpos)
    p[0] = CallNode(None, p[1], p[3], line = line, column = column)

def p_func_call3(p):
    'func_call : factor ARROBA TYPE_ID DOT ID LPAREN arg_list RPAREN'
    line, column = calculate_position(p.lexer.lexdata, p.lexer.lexpos)
    p[0] = DispatchNode(p[1], p[5], params = p[7], typex = p[3], line = line, column = column)



def p_arg_list(p):
    '''arg_list : expr arg_list2
                | empty
    '''
    if len(p) == 3:
        p[0] = [p[1]] + p[2]
    else:
        p[0] = []

def p_arg_list2(p):
    '''arg_list2 : COMMA expr arg_list2
                 | empty
    '''
    if len(p) == 4:
        p[0] = [p[2]] + p[3]
    else:
        p[0] = []


def p_error(p):
    if p:
        line, column = calculate_position(p.lexer.lexdata, p.lexpos)
        errors.append(f'({line},{column}) - SyntacticError: ERROR at or near "{p.value}"')
        
    else:
        errors.append(f'(0, 0) - SyntacticError: ERROR at or near EOF)')

############## End Grammar ############################

def calculate_position(data, pos):
    data_array = data.split('\n')
    count = 0
    number_line = 0
    for line in data_array:
        number_line += 1
        if count + len(line) >= pos:
            return (number_line, pos - count + 1)
        count += len(line) + 1


class Parser(CompilerComponent):

    def __init__(self, lexer: Lexer) -> None:
        super().__init__()
        self.lexer = lexer

    def execute(self):
       parser = yacc.yacc()
       errors = []
       self.ast = parser.parse(self.lexer.cool_program)

    def has_errors(self):
        return len(errors) > 0

    def print_errors(self):
        for e in errors:
            print(e)