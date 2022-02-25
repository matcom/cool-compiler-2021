

import ply.yacc as yacc

from .ast import *
from lexer.lexer import *

precedence = (
    ('left', 'AT'),
    ('left', 'INT_COMPLEMENT'),
    ('left', 'ISVOID'),
    ('left', 'NOT'),
    ('left', 'LESSEQUAL', 'LESS', 'EQUAL'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'MULT', 'DIV'),
    ('left', 'DOT'),
)


def p_program(p):
    'program : class_list'
    p[0] = ProgramNode(p, 1)


def p_epsilon(p):
    'epsilon :'
    pass


def p_class_list(p):
    '''class_list : def_class SEMICOLON class_list
                  | def_class SEMICOLON'''

    try:
        p[0] = [p[1]] + p[3]
    except IndexError:
        p[0] = [p[1]]


def p_def_class(p):
    '''def_class : CLASS TYPE OBRACE feature_list CBRACE
                 | CLASS TYPE INHERITS TYPE OBRACE feature_list CBRACE'''
    if len(p) == 8:
        p[0] = ClassDeclarationNode(p, 2, 2, 6, 4)
    else:
        p[0] = ClassDeclarationNode(p, 2, 2, 4)



def p_feature_list(p):
    '''feature_list : def_attr SEMICOLON feature_list
                    | def_func SEMICOLON feature_list
                    | epsilon'''
    if len(p) == 4:
        p[0] = [p[1]] + p[3]
    else:
        p[0] = []


def p_block_list(p):
    '''block_list : expr SEMICOLON block_list
                  | expr SEMICOLON'''
    p[0] = BlockNode(p)


def p_def_attr_declaration(p):
    '''def_attr : ID COLON TYPE ASSIGN expr
                | ID COLON TYPE'''
    try:
        p[0] = AttrDeclarationNode(p, 0, 1, 3, 5)
    except IndexError:
        p[0] = AttrDeclarationNode(p, 0, 1, 3)


def p_def_func(p):
    '''def_func : ID OPAR params CPAR COLON TYPE OBRACE expr CBRACE'''
    p[0] = FuncDeclarationNode(p, 6, 1, 3, 6, 8)


def p_params_ne(p):
    '''params : param_list'''
    p[0] = p[1]


def p_params_e(p):
    '''params : epsilon'''
    p[0] = []


def p_param_list(p):
    '''param_list : param COMMA param_list
                  | param epsilon'''
    try:
        p[0] = [p[1]] + p[3]
    except IndexError:
        p[0] = [p[1]]


def p_param(p):
    # noinspection PySingleQuotedDocstring
    '''param : ID COLON TYPE'''
    p[0] = (p[1], p[3])


def p_expr_flow(p):
    '''expr : LET let_attrs IN expr
            | CASE expr OF case_list ESAC
            | IF expr THEN expr ELSE expr FI
            | WHILE expr LOOP expr POOL'''

    if p[1].lower() == 'let':
        p[0] = LetNode(p, 2, 2, 4)
    elif p[1].lower() == 'case':
        p[0] = CaseNode(p, 2, 2, 4)
    elif p[1].lower() == 'if':
        p[0] = IfNode(p, 2, 2, 4, 6)
    elif p[1].lower() == 'while':
        p[0] = WhileNode(p, 2, 2, 4)



def p_expr_assign(p):
    '''expr : ID ASSIGN expr'''
    p[0] = AssignNode(p, 1, 1, 3)


def p_expr_func_all(p):
    '''expr : expr AT TYPE DOT ID OPAR arg_list CPAR
            | expr DOT ID OPAR arg_list CPAR
            | ID OPAR arg_list CPAR'''
    if len(p) == 9:
        if p[7] is None:
            p[7] = []
        p[0] = FuncCallNode(p, 5, 5, 7, 1, 3)
    elif len(p) == 7:
        if p[5] is None:
            p[5] = []
        p[0] = FuncCallNode(p, 3, 3, 5, 1)
    else:
        if p[3] is None:
            p[3] = []
        p[0] = FuncCallNode(p, 1, 1, 3)
    
    p[0].lineno = p.lineno(0)


def p_expr_operators_binary(p):
    '''expr : expr PLUS expr
            | expr MINUS expr
            | expr MULT expr
            | expr DIV expr
            | expr LESS expr
            | expr LESSEQUAL expr
            | expr EQUAL expr'''
    if p[2] == '+':
        p[0] = PlusNode(p, 0, 1, 3)
    elif p[2] == '-':
        p[0] = MinusNode(p, 0, 1, 3)
    elif p[2] == '*':
        p[0] = MultNode(p, 0, 1, 3)
    elif p[2] == '/':
        p[0] = DivNode(p, 0, 1, 3)
    elif p[2] == '<':
        p[0] = LessThanNode(p, 0, 1, 3)
    elif p[2] == '<=':
        p[0] = LessEqualNode(p, 0, 1, 3)
    elif p[2] == '=':
        p[0] = EqualNode(p, 0, 1, 3)



def p_expr_operators_unary(p):
    '''expr : INT_COMPLEMENT expr
            | ISVOID expr
            | NOT expr'''
    if p[1] == '~':
        p[0] = IntCompNode(p, 2, 2)
    elif p[1].lower() == 'isvoid':
        p[0] = IsVoidNode(p, 2, 2)
    elif p[1].lower() == 'not':
        p[0] = NotNode(p, 2, 2)



def p_expr_group(p):
    '''expr : OPAR expr CPAR'''
    p[0] = p[2]


def p_expr_atom(p):
    '''expr : atom'''
    p[0] = p[1]


def p_let_attrs(p):
    '''let_attrs : def_attr COMMA let_attrs
                | def_attr'''
    try:
        p[0] = [p[1]] + p[3]
    except IndexError:
        p[0] = [p[1]]


def p_case_list(p):
    '''case_list : case_elem SEMICOLON case_list
                 | case_elem SEMICOLON'''
    try:
        p[0] = [p[1]] + p[3]
    except IndexError:
        p[0] = [p[1]]


def p_case_elem(p):
    '''case_elem : ID COLON TYPE ACTION expr'''
    p[0] = CaseElemNode(p, 3, 5, 1, 3)


def p_arg_list(p):
    '''arg_list : arg_list_ne
                | epsilon'''
    p[0] = p[1]


def p_arg_list_ne(p):
    '''arg_list_ne : expr COMMA arg_list_ne
                   | expr '''
    if len(p) == 4:
        p[0] = [p[1]] + p[3]
    else:
        p[0] = [p[1]]


def p_atom_id(p):
    '''atom : ID'''
    p[0] = VarNode(p, 1, 1)


def p_atom_new(p):
    '''atom : NEW TYPE'''
    p[0] = NewNode(p, 2, 2)


def p_atom_block(p):
    '''atom : block'''
    p[0] = p[1]


def p_atom_int(p):
    '''atom : INTEGER'''
    p[0] = IntNode(p, 1, True, 1)


def p_atom_bool(p):
    '''atom :  BOOL'''
    p[0] = BoolNode(p, 1, False, 1)


def p_atom_atring(p):
    '''atom : STRING'''
    p[0] = StringNode(p, 1, False, 1)
    

def p_block(p):
    '''block : OBRACE block_list CBRACE'''
    p[0] = p[2]


def p_error(p):
    if p:
        append_errors_parsing(p.lineno, find_column(
            p.lexer.lexdata, p.lexpos), f'ERROR at or near \'{p.value}\'')
    else:
        append_errors_parsing(0, 0, "ERROR at or near EOF")

errors_parsing = []

def append_errors_parsing(line, column, message):
    errors_parsing.append(f'({line}, {column}) - SyntacticError: {message}')

parser = yacc.yacc()
