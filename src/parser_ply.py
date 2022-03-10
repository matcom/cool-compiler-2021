import ast_cool_hierarchy as ast
import lexer
import ply.yacc as yacc

from utils.utils import find_column, find_last_line

global errors
global input_text


tokens = lexer.tokens


# precedence = (
#     ('right', 'ASSIGN'),
#     ('right', 'NOT'),
#     ('nonassoc', 'LTEQ', 'LT', 'EQ'),
#     ('left', 'PLUS', 'MINUS'),
#     ('left', 'MULT', 'DIV'),
#     ('right', 'ISVOID'),
#     ('right', 'INT_COMP'),
#     ('left', 'AT'),
#     ('left', 'DOT'),
# )


def p_program(p):
    """
    program : class_list
    """
    p[0] = ast.ProgramNode(p.lineno(1), find_column(
        p.lexer.lexdata, p.lexpos(1)), p[1])
    pass


def p_class_list(p):
    """
    class_list : class_def
            | class_def class_list
    """
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[2]


def p_def_class(p):
    """
    class_def : CLASS TYPE_ID LBRACE feature_list RBRACE SEMICOLON
              | CLASS TYPE_ID INHERITS TYPE_ID LBRACE feature_list RBRACE SEMICOLON
    """
    if len(p) == 7:
        p[0] = ast.ClassDeclarationNode(p.lineno(1), find_column(
            p.lexer.lexdata, p.lexpos(2)), p[2], p[4], 'Object')
    else:
        p[0] = ast.ClassDeclarationNode(p.lineno(1), find_column(
            p.lexer.lexdata, p.lexpos(2)), p[2], p[6], p[4])


def p_feature_list(p):
    """
    feature_list : attrs_def SEMICOLON feature_list
                 | meth_def SEMICOLON feature_list
                 | empty
    """
    if len(p) == 4:
        p[0] = [p[1]] + p[3]
    else:
        p[0] = []


def p_attrs_def(p):
    """
    attrs_def : attr_def
              | attr_def COMMA attrs_def
    """
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = [p[1]] + p[3]


def p_attr_def(p):
    """
    attr_def : OBJECT_ID COLON type
             | OBJECT_ID COLON type ASSIGN expr
    """
    if len(p) == 4:
        p[0] = ast.AttrDeclarationNode(p.lineno(1), find_column(
            p.lexer.lexdata, p.lexpos(1)), p[1], p[3])
    else:
        p[0] = ast.AttrDeclarationNode(p.lineno(1), find_column(
            p.lexer.lexdata, p.lexpos(1)), p[1], p[3], p[5])


def p_meth_def(p):
    """
    meth_def : OBJECT_ID LPAREN param_list RPAREN COLON type LBRACE expr RBRACE
    """
    p[0] = ast.FuncDeclarationNode(p.lineno(1), find_column(
        p.lexer.lexdata, p.lexpos(1)), p[1], p[3], p[6], p[8])


def p_param_list(p):
    """
    param_list : param other_param
               | empty
    """
    if len(p) == 3:
        p[0] = [p[1]] + p[2]
    else:
        p[0] = []


def p_param(p):
    """
    param : OBJECT_ID COLON type
    """
    p[0] = (p[1], p[3])


def p_other_param(p):
    """
    other_param : COMMA param other_param
                | empty
    """
    if len(p) == 4:
        p[0] = [p[2]] + p[3]
    else:
        p[0] = []


def p_expr(p):
    """
    expr : comparer LT open_expr_lvl1
         | comparer LTEQ open_expr_lvl1
         | comparer EQ open_expr_lvl1
         | open_expr_lvl1
         | comparer
    """
    operator = p.slice[2].type if len(p) > 2 else None
    if operator == 'LT':
        p[0] = ast.LessNode(p.lineno(2), find_column(
            p.lexer.lexdata, p.lexpos(2)), p[1], p[3])
    elif operator == 'LTEQ':
        p[0] = ast.LessEqualNode(p.lineno(2), find_column(
            p.lexer.lexdata, p.lexpos(2)), p[1], p[3])
    elif operator == 'EQ':
        p[0] = ast.EqualNode(p.lineno(2), find_column(
            p.lexer.lexdata, p.lexpos(2)), p[1], p[3])
    else:
        p[0] = p[1]


def p_open_expr_lvl1(p):
    """
    open_expr_lvl1 : arith PLUS open_expr_lvl2
                   | arith MINUS open_expr_lvl2
                   | open_expr_lvl2
    """
    operator = p.slice[2].type if len(p) > 2 else None
    if operator == 'PLUS':
        p[0] = ast.PlusNode(p.lineno(2), find_column(
            p.lexer.lexdata, p.lexpos(2)), p[1], p[3])
    elif operator == 'MINUS':
        p[0] = ast.MinusNode(p.lineno(2), find_column(
            p.lexer.lexdata, p.lexpos(2)), p[1], p[3])
    else:
        p[0] = p[1]


def p_open_expr_lvl2(p):
    """
    open_expr_lvl2 : term MULT open_expr_lvl3
                   | term DIV open_expr_lvl3
                   | open_expr_lvl3
    """
    operator = p.slice[2].type if len(p) > 2 else None
    if operator == 'MULT':
        p[0] = ast.StarNode(p.lineno(2), find_column(
            p.lexer.lexdata, p.lexpos(2)), p[1], p[3])
    elif operator == 'DIV':
        p[0] = ast.DivNode(p.lineno(2), find_column(
            p.lexer.lexdata, p.lexpos(2)), p[1], p[3])
    else:
        p[0] = p[1]


def p_open_expr_lvl3(p):
    """
    open_expr_lvl3 : ISVOID open_expr_lvl3
                   | INT_COMP open_expr_lvl3
                   | open_expr
    """
    first_token = p.slice[1].type if len(p) > 1 else None
    if first_token == 'ISVOID':
        p[0] = ast.IsVoidNode(p.lineno(1), find_column(
            p.lexer.lexdata, p.lexpos(1)), p[2])
    elif first_token == 'INT_COMP':
        p[0] = ast.IntCompNode(p.lineno(1), find_column(
            p.lexer.lexdata, p.lexpos(1)), p[1])
    else:
        p[0] = p[1]


def p_open_expr(p):
    """
    open_expr : LET let_var_list IN expr
              | OBJECT_ID ASSIGN expr
              | NOT expr
    """
    first_token = p.slice[1].type if len(p) > 1 else None
    if first_token == 'LET':
        p[0] = ast.LetNode(p.lineno(1), find_column(
            p.lexer.lexdata, p.lexpos(1)), p[2], p[4])
    elif first_token == 'OBJECT_ID':
        p[0] = ast.AssignNode(p.lineno(1), find_column(
            p.lexer.lexdata, p.lexpos(1)), p[1], p[3])
    elif first_token == 'NOT':
        p[0] = ast.NotNode(p.lineno(1), find_column(
            p.lexer.lexdata, p.lexpos(1)), p[2])


def p_comparer(p):
    """
    comparer : comparer LT arith
             | comparer LTEQ arith
             | comparer EQ arith
             | arith
    """
    operator = p.slice[2].type if len(p) > 2 else None
    if operator == 'LT':
        p[0] = ast.LessNode(p.lineno(2), find_column(
            p.lexer.lexdata, p.lexpos(2)), p[1], p[3])
    elif operator == 'LTEQ':
        p[0] = ast.LessEqualNode(p.lineno(2), find_column(
            p.lexer.lexdata, p.lexpos(2)), p[1], p[3])
    elif operator == 'EQ':
        p[0] = ast.EqualNode(p.lineno(2), find_column(
            p.lexer.lexdata, p.lexpos(2)), p[1], p[3])
    else:
        p[0] = p[1]


def p_arith(p):
    """
    arith : arith PLUS term
          | arith MINUS term
          | term
    """
    operator = p.slice[2].type if len(p) > 2 else None
    if operator is None:
        p[0] = p[1]
    elif operator == 'PLUS':
        p[0] = ast.PlusNode(p.lineno(2), find_column(
            p.lexer.lexdata, p.lexpos(2)), p[1], p[3])
    elif operator == 'MINUS':
        p[0] = ast.MinusNode(p.lineno(2), find_column(
            p.lexer.lexdata, p.lexpos(2)), p[1], p[3])


def p_term(p):
    """
    term : term MULT factor
         | term DIV factor
         | factor
    """
    operator = p.slice[2].type if len(p) > 2 else None
    if operator is None:
        p[0] = p[1]
    elif operator == 'MULT':
        p[0] = ast.StarNode(p.lineno(2), find_column(
            p.lexer.lexdata, p.lexpos(2)), p[1], p[3])
    elif operator == 'DIV':
        p[0] = ast.DivNode(p.lineno(2), find_column(
            p.lexer.lexdata, p.lexpos(2)), p[1], p[3])


def p_factor(p):
    """
    factor : ISVOID factor
           | INT_COMP factor
           | resoluted
    """
    first_token = p.slice[1].type if len(p) > 1 else None
    if first_token == 'ISVOID':
        p[0] = ast.IsVoidNode(p.lineno(1), find_column(
            p.lexer.lexdata, p.lexpos(1)), p[2])
    elif first_token == 'INT_COMP':
        p[0] = ast.IntCompNode(p.lineno(1), find_column(
            p.lexer.lexdata, p.lexpos(1)), p[2])
    else:
        p[0] = p[1]


def p_resoluted(p):
    """
    resoluted : resoluted DOT OBJECT_ID LPAREN arg_list RPAREN
              | resoluted AT TYPE_ID DOT OBJECT_ID LPAREN arg_list RPAREN
              | atom
    """
    if len(p) == 7:
        p[0] = ast.CallNode(p.lineno(1), find_column(
            p.lexer.lexdata, p.lexpos(1)), p[1], p[3], p[5])
    elif len(p) == 9:
        p[0] = ast.CallNode(p.lineno(1), find_column(
            p.lexer.lexdata, p.lexpos(1)), p[1], p[5], p[7], p[3])
    else:
        p[0] = p[1]


def p_atom(p):
    """
    atom : INTEGER
         | OBJECT_ID
         | STRING
         | BOOL
         | LPAREN expr RPAREN
         | NEW TYPE_ID
         | IF expr THEN expr ELSE expr FI
         | WHILE expr LOOP expr POOL
         | LBRACE expr_list RBRACE
         | CASE expr OF branch_list ESAC
         | func_call
    """
    first_token = p.slice[1].type if len(p) > 1 else None
    second_token = p.slice[2].type if len(p) > 2 else None
    if first_token == 'INTEGER':
        p[0] = ast.ConstantNumNode(p.lineno(1), find_column(
            p.lexer.lexdata, p.lexpos(1)), p[1])
    elif first_token == 'OBJECT_ID' and second_token is None:
        p[0] = ast.VariableNode(p.lineno(1), find_column(
            p.lexer.lexdata, p.lexpos(1)), p[1])
    elif first_token == 'STRING':
        p[0] = ast.StringNode(p.lineno(1), find_column(
            p.lexer.lexdata, p.lexpos(1)), p[1])
    elif first_token == 'BOOL':
        p[0] = ast.BoolNode(p.lineno(1), find_column(
            p.lexer.lexdata, p.lexpos(1)), p[1])
    elif first_token == 'LPAREN':
        p[0] = p[2]
    elif first_token == 'NEW':
        p[0] = ast.InstantiateNode(p.lineno(1), find_column(
            p.lexer.lexdata, p.lexpos(1)), p[2])
    elif first_token == 'IF':
        p[0] = ast.ConditionalNode(p.lineno(1), find_column(
            p.lexer.lexdata, p.lexpos(1)), p[2], p[4], p[6])
    elif first_token == 'WHILE':
        p[0] = ast.LoopNode(p.lineno(1), find_column(
            p.lexer.lexdata, p.lexpos(1)), p[2], p[4])
    elif first_token == 'LBRACE':
        p[0] = ast.BlockNode(p.lineno(1), find_column(
            p.lexer.lexdata, p.lexpos(1)), p[2])
    elif first_token == 'CASE':
        p[0] = ast.CaseNode(p.lineno(1), find_column(
            p.lexer.lexdata, p.lexpos(1)), p[2], p[4])
    elif first_token == 'func_call':
        p[0] = p[1]


def p_expr_list(p):
    """
    expr_list : expr SEMICOLON
              | expr SEMICOLON expr_list
    """
    if len(p) == 3:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[3]


def p_let_var_list(p):
    """
    let_var_list : let_var
                 | let_var_assign
                 | let_var COMMA let_var_list
                 | let_var_assign COMMA let_var_list
    """
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[3]


def p_let_var(p):
    """
    let_var : OBJECT_ID COLON type
    """
    p[0] = (p[1], p[3], None)


def p_let_var_assign(p):
    """
    let_var_assign : OBJECT_ID COLON type ASSIGN expr
    """
    p[0] = (p[1], p[3], p[5])


def p_branch_list(p):
    """
    branch_list : branch
                | branch branch_list
    """
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[2]


def p_branch(p):
    """
    branch : OBJECT_ID COLON type ACTION expr SEMICOLON
    """
    p[0] = ast.BranchNode(p.lineno(1), find_column(
        p.lexer.lexdata, p.lexpos(1)), p[1], p[3], p[5])


def p_func_call(p):
    """
    func_call : OBJECT_ID LPAREN arg_list RPAREN
    """
    self = ast.VariableNode(p.lineno(1), find_column(
        p.lexer.lexdata, p.lexpos(1)), 'self')
    p[0] = ast.CallNode(p.lineno(1), find_column(
        p.lexer.lexdata, p.lexpos(1)), self, p[1], p[3])


def p_arg_list(p):
    """
    arg_list : expr other_arg
             | empty
    """
    if len(p) == 3:
        p[0] = [p[1]] + p[2]
    else:
        p[0] = []


def p_other_arg(p):
    """
    other_arg : COMMA expr other_arg
              | empty
    """
    if len(p) == 4:
        p[0] = [p[2]] + p[3]
    else:
        p[0] = []


def p_type(p):
    """type : TYPE_ID
            | SELF_TYPE"""
    p[0] = p[1]


def p_empty(p):
    """empty :"""
    p[0] = None


def p_error(p):
    if p is None:
        line_no = find_last_line(input_text)
        errors.append(
            '(%s, 0) - SyntacticError: ERROR at or near EOF' % line_no)
    else:
        col_no = find_column(p.lexer.lexdata, p.lexpos)
        errors.append(('(%s, %s) - SyntacticError: ERROR at or near "%s"'.format(p) %
                       (p.lineno, col_no, p.value)))


def parse(text: str) -> (yacc.LRParser, list):
    global errors
    global input_text

    errors = []
    input_text = text
    lex = lexer.get_a_lexer()
    parser = get_a_parser()
    tree = parser.parse(text, lex, tracking=True)
    return tree, errors


def get_a_parser() -> yacc.LRParser:
    parser = yacc.yacc()
    return parser
