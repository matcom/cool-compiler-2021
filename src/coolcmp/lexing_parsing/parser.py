import ply.yacc as yacc

from coolcmp.utils import ast
from coolcmp import errors as err
from coolcmp.lexing_parsing import lexer
from coolcmp.utils import find_column


tokens = lexer.tokens

precedence = (
    ('right', 'ASSIGN'),
    ('right', 'NOT'),
    ('nonassoc', 'LEQ', 'LESS', 'EQ'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'STAR', 'DIV'),
    ('right', 'ISVOID'),
    ('right', 'COMP'),
    ('left', 'AT'),
    ('left', 'DOT')
)


def p_program(p):
    """
    program : class_list
    """
    p[0] = ast.ProgramNode(p[1])


def p_class_list(p):
    """
    class_list : class_def SEMI class_list
               | class_def SEMI
    """
    if len(p) == 4:
        p[0] = [p[1]] + p[3]
    else:
        p[0] = [p[1]]


def p_class_def(p):
    """
    class_def : CLASS TYPE INHERITS TYPE OCUR feature_list CCUR
              | CLASS TYPE OCUR feature_list CCUR
    """
    if len(p) == 8:
        p[0] = ast.ClassDeclarationNode(p[2], p[6], p[4])
        p[0].parent_pos = (p.lineno(4), find_column(p.lexer.lexdata, p.lexpos(4)))
    else:
        p[0] = ast.ClassDeclarationNode(p[2], p[4])
    p[0].set_pos(p.lineno(2), find_column(p.lexer.lexdata, p.lexpos(2)))


def p_feature_list(p):
    """
    feature_list : attr_def SEMI feature_list
                 | func_def SEMI feature_list
                 | empty
    """
    if len(p) == 4:
        p[0] = [p[1]] + p[3]
    else:
        p[0] = []


def p_attr_def(p):
    """
    attr_def : ID COLON TYPE ASSIGN expr
             | ID COLON TYPE
    """
    if len(p) == 6:
        p[0] = ast.AttrDeclarationNode(p[1], p[3], p[5])
        p[0].expr_pos = p[5].pos
    else:
        p[0] = ast.AttrDeclarationNode(p[1], p[3])

    p[0].set_pos(p.lineno(1), find_column(p.lexer.lexdata, p.lexpos(1)))
    p[0].type_pos = (p.lineno(3), find_column(p.lexer.lexdata, p.lexpos(3)))


def p_func_def(p):
    """
    func_def : ID OPAR param_list CPAR COLON TYPE OCUR expr CCUR
             | ID OPAR CPAR COLON TYPE OCUR expr CCUR
    """
    if len(p) == 10:
        p[0] = ast.FuncDeclarationNode(p[1], p[3], p[6], p[8])
        p[0].set_pos(p.lineno(1), find_column(p.lexer.lexdata, p.lexpos(1)))
        p[0].type_pos = (p.lineno(6), find_column(p.lexer.lexdata, p.lexpos(6)))
    else:
        p[0] = ast.FuncDeclarationNode(p[1], [], p[5], p[7])
        p[0].set_pos(p.lineno(1), find_column(p.lexer.lexdata, p.lexpos(1)))
        p[0].type_pos = (p.lineno(5), find_column(p.lexer.lexdata, p.lexpos(5)))


def p_param_list(p):
    """
    param_list : ID COLON TYPE COMMA param_list
               | ID COLON TYPE
    """
    param = ast.ParamNode(p[1], p[3])
    param.set_pos(p.lineno(1), find_column(p.lexer.lexdata, p.lexpos(1)))
    param.type_pos = (p.lineno(3), find_column(p.lexer.lexdata, p.lexpos(3)))
    if len(p) == 6:
        p[0] = [param] + p[5]
    elif len(p) == 4:
        p[0] = [param]


# expr productions

def p_expr_assign(p):
    """
    expr : ID ASSIGN expr
    """
    p[0] = ast.AssignNode(p[1], p[3])

    p[0].set_pos(p.lineno(2), find_column(p.lexer.lexdata, p.lexpos(2)))


def p_expr_list(p):
    """
    expr_list : expr COMMA expr_list_not_empty
              | expr
    """
    if len(p) == 4:
        p[0] = [p[1]] + p[3]
    else:
        p[0] = [p[1]]


def p_expr_list_empty(p):
    """
    expr_list : empty
    """
    p[0] = []


def p_expr_list_not_empty(p):
    """
    expr_list_not_empty : expr COMMA expr_list_not_empty
                        | expr
    """
    if len(p) == 4:
        p[0] = [p[1]] + p[3]
    else:
        p[0] = [p[1]]


def p_expr_func_call(p):
    """
    expr : ID OPAR expr_list CPAR
         | expr DOT ID OPAR expr_list CPAR
         | expr AT TYPE DOT ID OPAR expr_list CPAR
    """
    if len(p) == 5:
        p[0] = ast.CallNode(p[1], p[3])
        p[0].set_pos(p.lineno(1), find_column(p.lexer.lexdata, p.lexpos(1)))
    elif len(p) == 7:
        p[0] = ast.CallNode(p[3], p[5], p[1])
        p[0].set_pos(p.lineno(3), find_column(p.lexer.lexdata, p.lexpos(3)))
    else:
        p[0] = ast.CallNode(p[5], p[7], p[1], p[3])
        p[0].set_pos(p.lineno(5), find_column(p.lexer.lexdata, p.lexpos(5)))
        p[0].parent_pos = (p.lineno(3), find_column(p.lexer.lexdata, p.lexpos(3)))


def p_expr_if(p):
    """
    expr : IF expr THEN expr ELSE expr FI
    """
    p[0] = ast.ConditionalNode(p[2], p[4], p[6])

    p[0].set_pos(p.lineno(1), find_column(p.lexer.lexdata, p.lexpos(1)))


def p_expr_while(p):
    """
    expr : WHILE expr LOOP expr POOL
    """
    p[0] = ast.WhileNode(p[2], p[4])

    p[0].set_pos(p.lineno(1), find_column(p.lexer.lexdata, p.lexpos(1)))


def p_block(p):
    """
    block : expr SEMI block
          | expr SEMI
    """
    if len(p) == 4:
        p[0] = [p[1]] + p[3]
    else:
        p[0] = [p[1]]


def p_expr_block(p):
    """
    expr : OCUR block CCUR
    """
    p[0] = ast.BlockNode(p[2])

    p[0].set_pos(p.lineno(1), find_column(p.lexer.lexdata, p.lexpos(1)))


def p_decl_list(p):
    """
    decl_list : ID COLON TYPE ASSIGN expr COMMA decl_list
              | ID COLON TYPE COMMA decl_list
              | ID COLON TYPE ASSIGN expr
              | ID COLON TYPE
    """
    if len(p) > 4 and p[4] == '<-':
        declaration = ast.LetDeclarationNode(p[1], p[3], p[5])
        declaration.type_pos = (p.lineno(3), find_column(p.lexer.lexdata, p.lexpos(3)))
        declaration.expr_pos = p[5].pos
        declaration.set_pos(p.lineno(1), find_column(p.lexer.lexdata, p.lexpos(1)))
        if len(p) == 8:
            p[0] = [declaration] + p[7]
        else:
            p[0] = [declaration]
    else:
        declaration = ast.LetDeclarationNode(p[1], p[3])
        declaration.type_pos = (p.lineno(3), find_column(p.lexer.lexdata, p.lexpos(3)))
        declaration.set_pos(p.lineno(1), find_column(p.lexer.lexdata, p.lexpos(1)))
        if len(p) == 6:
            p[0] = [declaration] + p[5]
        else:
            p[0] = [declaration]

    # if len(p) == 8:
    #     p[0] = [ast.LetDeclarationNode(p[1], p[3], p[5])] + p[7]
    # elif len(p) == 6:
    #     if p[4] == ',':
    #         p[0] = [ast.LetDeclarationNode(p[1], p[3])] + p[5]
    #     else:
    #         p[0] = [ast.LetDeclarationNode(p[1], p[3], p[5])]
    # else:
    #     p[0] = [ast.LetDeclarationNode(p[1], p[3])]


def p_expr_let(p):
    """
    expr : LET decl_list IN expr
    """
    p[0] = ast.LetNode(p[2], p[4])

    p[0].set_pos(p.lineno(1), find_column(p.lexer.lexdata, p.lexpos(1)))


def p_case_list(p):
    """
    case_list : ID COLON TYPE ARROW expr SEMI case_list
              | ID COLON TYPE ARROW expr SEMI
    """
    branch = ast.CaseBranchNode(p[1], p[3], p[5])
    branch.set_pos(p.lineno(1), find_column(p.lexer.lexdata, p.lexpos(1)))
    branch.type_pos = (p.lineno(3), find_column(p.lexer.lexdata, p.lexpos(3)))

    if len(p) == 8:
        p[0] = [branch] + p[7]
    else:
        p[0] = [branch]


def p_expr_case(p):
    """
    expr : CASE expr OF case_list ESAC
    """
    p[0] = ast.CaseNode(p[2], p[4])

    p[0].set_pos(p.lineno(1), find_column(p.lexer.lexdata, p.lexpos(1)))


def p_expr_new(p):
    """
    expr : NEW TYPE
    """
    p[0] = ast.InstantiateNode(p[2])

    p[0].set_pos(p.lineno(1), find_column(p.lexer.lexdata, p.lexpos(1)))


def p_expr_isvoid(p):
    """
    expr : ISVOID expr
    """
    p[0] = ast.IsVoidNode(p[2])

    p[0].set_pos(p.lineno(1), find_column(p.lexer.lexdata, p.lexpos(1)))


def p_expr_binary_op(p):
    """
    expr : expr PLUS expr
         | expr MINUS expr
         | expr STAR expr
         | expr DIV expr
         | expr LESS expr
         | expr LEQ expr
         | expr EQ expr
    """
    if p[2] == '+':
        p[0] = ast.PlusNode(p[1], p[2], p[3])
    elif p[2] == '-':
        p[0] = ast.MinusNode(p[1], p[2], p[3])
    elif p[2] == '/':
        p[0] = ast.DivNode(p[1], p[2], p[3])
    elif p[2] == '*':
        p[0] = ast.StarNode(p[1], p[2], p[3])
    elif p[2] == '<':
        p[0] = ast.LessThanNode(p[1], p[2], p[3])
    elif p[2] == '<=':
        p[0] = ast.LessEqualNode(p[1], p[2], p[3])
    else:
        p[0] = ast.EqualNode(p[1], p[2], p[3])

    p[0].set_pos(p.lineno(2), find_column(p.lexer.lexdata, p.lexpos(2)))


def p_expr_comp(p):
    """
    expr : COMP expr
    """
    p[0] = ast.ComplementNode(p[2])

    p[0].set_pos(p.lineno(1), find_column(p.lexer.lexdata, p.lexpos(1)))


def p_expr_not(p):
    """
    expr : NOT expr
    """
    p[0] = ast.NegationNode(p[2])

    p[0].set_pos(p.lineno(1), find_column(p.lexer.lexdata, p.lexpos(1)))


def p_expr_pars(p):
    """
    expr : OPAR expr CPAR
    """
    p[0] = p[2]


def p_expr_id(p):
    """
    expr : ID
    """
    p[0] = ast.VariableNode(p[1])

    p[0].set_pos(p.lineno(1), find_column(p.lexer.lexdata, p.lexpos(1)))


def p_expr_int(p):
    """
    expr : INT
    """
    p[0] = ast.IntegerNode(p[1])

    p[0].set_pos(p.lineno(1), find_column(p.lexer.lexdata, p.lexpos(1)))


def p_expr_string(p):
    """
    expr : STRING
    """
    p[0] = ast.StringNode(p[1])

    p[0].set_pos(p.lineno(1), find_column(p.lexer.lexdata, p.lexpos(1)))


def p_expr_bool(p):
    """
    expr : BOOL
    """
    p[0] = ast.BooleanNode(p[1])

    p[0].set_pos(p.lineno(1), find_column(p.lexer.lexdata, p.lexpos(1)))


# empty productions

def p_empty(p):
    """
    empty :
    """
    pass


# error handling

def p_error(p):
    if p:
        line, col = p.lineno, find_column(p.lexer.lexdata, p.lexpos)
        errors.append(err.SYN_ERROR % (line, col, p.value))
    else:
        errors.append(err.SYN_EOF)


errors = []
parser = yacc.yacc()
