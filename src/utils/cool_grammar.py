from fileinput import lineno

import cool_lexer as lex
import ply.yacc as yacc

import utils.ast_nodes as ast

tokens = lex.tokens

errors = []

def p_program(p):
    'program : class_list'
    p[0] = ast.ProgramNode(p[1])


def p_class_list(p):
    '''class_list : class_def class_list
                  | class_def'''
    if len(p) == 2:
        p[0] = [p[1]]
    elif len(p) == 3:
        p[0] = [p[1]] + p[2]

def p_class_def(p):
    '''class_def : CLASS TYPE OBRACE feature_list CBRACE SEMI 
                 | CLASS TYPE INHERITS TYPE OBRACE feature_list CBRACE SEMI'''
    if len(p) == 7:
        p[0] = ast.ClassDecNode(p[2], p[4])
    elif len(p) == 9:
        p[0] = ast.ClassDecNode(p[2], p[6], p[4])

# def p_class_def_error(p):
#     '''class_def : CLASS TYPE OBRACE error CBRACE SEMI
#                  | CLASS TYPE INHERITS TYPE OBRACE error CBRACE SEMI'''
#     if len(p) == 7:
#         errors.append((p.lineno(5), p.lexpos(5), 'EOC not found', 'CBRACE'))
#     else:
#         errors.append((p.lineno(7), p.lexpos(7), 'EOC not found', 'CBRACE'))


def p_feature_list(p):
    '''feature_list : empty
                    | attribute SEMI feature_list
                    | method SEMI feature_list'''
    if len(p) == 2:
        p[0] = []
    elif len(p) == 4:
        p[0] = [p[1]] + p[3]


def p_attribute(p):
    '''attribute : ID COLON TYPE
                 | ID COLON TYPE ASSIGN expr'''
    if len(p) == 4:
        p[0] = ast.AttributeDecNode(p[1], p[3])
    elif len(p) == 6:
        p[0] = ast.AttributeDecNode(p[1], p[3], p[5])


def p_method(p):
    '''method : ID OPAR CPAR COLON TYPE OBRACE expr CBRACE
              | ID OPAR param_list CPAR COLON TYPE OBRACE expr CBRACE'''
    if len(p) == 9:
        p[0] = ast.MethodDecNode(p[1], p[5], p[7], [])
    elif len(p) == 10:
        p[0] = ast.MethodDecNode(p[1], p[6], p[8], p[3])

    


def p_param_list(p):
    '''param_list : ID COLON TYPE
                  | ID COLON TYPE COMA param_list'''
    if len(p) == 4:
        p[0] = [(p[1], p[3])]
    elif len(p) == 6:
        p[0] = [(p[1], p[3])] + p[5]


def p_expr(p):
    '''expr : ID ASSIGN expr
            | OBRACE block CBRACE
            | WHILE expr LOOP expr POOL
            | LET declaration_list IN expr
            | CASE expr OF case_list ESAC
            | notcomp'''
    if len(p) == 2:
        p[0] = p[1]
    elif p[1] == 'while':
        p[0] = ast.WhileNode(p[2], p[4])
    elif p[1] == 'let':
        p[0] = ast.LetNode(p[2], p[4])
    elif p[1] == 'case':
        p[0] = ast.CaseNode(p[2], p[4])
    elif p[2] == '<-':
        p[0] = ast.AssignNode(p[1], p[3])
    elif p[1] == '{':
        p[0] = ast.BlockNode(p[2])

def p_notcomp(p):
    '''notcomp : NOT comp
               | comp'''
    if len(p) == 3:
        p[0] = ast.NegationNode(p[2])
    else:
        p[0] = p[1]


def p_comp(p):
    '''comp : comp LESS notarith
            | comp LESSEQUAL notarith
            | comp EQUAL notarith
            | arith'''

    if len(p) == 4:
        if p[2] == '<':
            p[0] = ast.LessNode(p[1], p[2], p[3])
        elif p[2] == '<=':
            p[0] = ast.LessEqualNode(p[1], p[2], p[3])
        elif p[2] == '=':
            p[0] = ast.EqualNode(p[1], p[2], p[3])
    elif len(p) == 2:
        p[0] = p[1]


def p_notarith(p):
    '''notarith : NOT arith
                | arith'''
    if len(p) == 3:
        p[0] = ast.NegationNode(p[2])
    else:
        p[0] = p[1]

def p_arith(p):
    '''arith : arith PLUS term
             | arith MINUS term
             | term'''
    if len(p) == 4:
        if p[2] == '+':
            p[0] = ast.PlusNode(p[1], p[2], p[3])
        elif p[2] == '-':
            p[0] = ast.MinusNode(p[1], p[2], p[3])
    elif len(p) == 2:
        p[0] = p[1]


def p_term(p):
    '''term : term TIMES factor
            | term DIV factor
            | factor'''

    if len(p) == 4:
        if p[2] == '*':
            p[0] = ast.TimesNode(p[1], p[2], p[3])
        elif p[2] == '/':
            p[0] = ast.DivNode(p[1], p[2], p[3])
    elif len(p) == 2:
        p[0] = p[1]


def p_factor(p):
    '''factor : ISVOID factor
              | COMPLEMENT factor
              | atom'''

    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 3:
        if p[1] == '~':
            p[0] = ast.ComplementNode(p[2])
        elif p[1] == 'isvoid':
            p[0] = ast.IsVoidNode(p[2])


def p_atom(p):
    '''atom : ID
            | NEW TYPE
            | OPAR expr CPAR
            | IF expr THEN expr ELSE expr FI'''

    if len(p) == 4:
        # p[0] = ast.ExprParNode(p[2])
        p[0] = p[2]
    elif len(p) == 3:
        p[0] = ast.NewNode(p[2])
    elif len(p) == 2:
        p[0] = ast.VariableNode(p[1])
    elif len(p) == 8:
        p[0] = ast.ConditionalNode(p[2], p[4], p[6])


def p_atom_funccall(p):
    'atom : function_call'

    p[0] = p[1]


def p_atom_string(p):
    # 'atom : QUOTATION STRING QUOTATION'
    'atom : STRING'

    p[0] = ast.StringNode(p[1])


def p_atom_true(p):
    '''atom : TRUE
            | FALSE'''

    p[0] = ast.BooleanNode(p[1])


def p_atom_number(p):
    'atom : NUMBER'

    p[0] = ast.NumberNode(p[1])


def p_block(p):
    '''block : expr SEMI
             | expr SEMI block'''
    if len(p) == 3:
        p[0] = [p[1]]
    elif len(p) == 4:
        p[0] = [p[1]] + p[3]


def p_declaration_list(p):
    '''declaration_list : ID COLON TYPE
                        | ID COLON TYPE ASSIGN expr
                        | ID COLON TYPE COMA declaration_list
                        | ID COLON TYPE ASSIGN expr COMA declaration_list'''
    if len(p) == 4:
        p[0] = [(p[1], p[3], None)]
    elif len(p) == 6:
        if p[4] == '<-':
            p[0] = [(p[1], p[3], p[5])]
        elif p[4] == ',':
            p[0] = [(p[1], p[3], None)] + p[5]
    elif len(p) == 8:
        p[0] = [(p[1], p[3], p[5])] + p[7]


def p_case_list(p):
    '''case_list : ID COLON TYPE ARROW expr SEMI
                 | ID COLON TYPE ARROW expr SEMI case_list'''
    if len(p) == 7:
        p[0] = [(p[1], p[3], p[5])]
    elif len(p) == 8:
        p[0] = [(p[1], p[3], p[5])] + p[7]


def p_function_call(p):
    '''function_call : ID OPAR expr_list CPAR
                     | atom DOT ID OPAR expr_list CPAR
                     | atom ARROBA TYPE DOT ID OPAR expr_list CPAR'''
    if len(p) == 5:
        p[0] = ast.MethodCallNode(p[1], p[3])
    elif len(p) == 7:
        p[0] = ast.MethodCallNode(p[3], p[5], p[1])
    elif len(p) == 9:
        p[0] = ast.MethodCallNode(p[5], p[7], p[1], p[3])


def p_expr_list(p):
    '''expr_list : empty
                 | list_not_empty'''
    if p[1]:
        p[0] = p[1]
    else:
        p[0] = []


def p_list_not_empty(p):
    '''list_not_empty : expr
                      | expr COMA list_not_empty'''
    if len(p) == 2:
        p[0] = [p[1]]
    elif len(p) == 4:
        p[0] = [p[1]] + p[3]


def p_empty(p):
    'empty :'
    pass


def p_error(p):
    if p:
        errors.append((p.lineno, p.lexpos, p.value, p.type))


parser = yacc.yacc()
