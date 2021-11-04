import ply.yacc as yacc
import lexer
import ast as ast


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
    p[0] = ast.ProgramNode(p[1])


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
        p[0] = ast.ClassDeclarationNode(p[2], p[4])
    else:
        p[0] = ast.ClassDeclarationNode(p[2], p[6], p[4])


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
        p[0] = ast.AttrDeclarationNode(p[1], p[3])
    else:
        p[0] = ast.AttrDeclarationNode(p[1], p[3], p[5])


def p_meth_def(p):
    """
    meth_def : OBJECT_ID LPAREN param_list RPAREN COLON type LBRACE expr RBRACE
    """
    p[0] = ast.FuncDeclarationNode(p[1], p[3], p[6], p[8])


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
    expr : comparer
    """
    p[0] = p[1]


def p_comparer(p):
    """
    comparer : comparer LT arith
             | comparer LTEQ arith
             | comparer EQ arith
             | arith
    """
    operator = p.slice[2].type if len(p) > 2 else None
    if operator is None:
        p[0] = p[1]
    elif operator == 'LT':
        p[0] = ast.LessNode(p[1], p[3])
    elif operator == 'LTEQ':
        p[0] = ast.LessEqualNode(p[1], p[3])
    elif operator == 'EQ':
        p[0] = ast.EqualNode(p[1], p[3])


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
        p[0] = ast.PlusNode(p[1], p[3])
    elif operator == 'MINUS':
        p[0] = ast.MinusNode(p[1], p[3])


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
        p[0] = ast.StarNode(p[1], p[3])
    elif operator == 'DIV':
        p[0] = ast.DivNode(p[1], p[3])


def p_factor(p):
    """
    factor : atom
    """
    p[0] = p[1]


def p_atom(p):
    """
    atom : INTEGER
         | OBJECT_ID
         | STRING
         | BOOL
         | LPAREN expr RPAREN
         | OBJECT_ID ASSIGN atom
         | NEW TYPE_ID
         | IF expr THEN expr ELSE expr FI
         | WHILE expr LOOP expr POOL
         | LBRACE expr_list RBRACE
         | LET let_var_list IN atom
         | CASE expr OF branch_list ESAC
         | NOT atom
         | ISVOID atom
         | INT_COMP atom
         | func_call
    """
    first_token = p.slice[1].type if len(p) > 1 else None
    second_token = p.slice[2].type if len(p) > 2 else None
    if first_token == 'INTEGER':
        p[0] = ast.ConstantNumNode(p[1])
    elif first_token == 'OBJECT_ID' and second_token is None:
        p[0] = ast.VariableNode(p[1])
    elif first_token == 'STRING':
        p[0] = ast.StringNode(p[1])
    elif first_token == 'BOOL':
        p[0] = ast.BoolNode(p[1])
    elif first_token == 'LPAREN':
        p[0] = p[2]
    elif first_token == 'OBJECT_ID' and second_token == 'ASSIGN':
        p[0] = ast.AssignNode(p[1], p[3])
    elif first_token == 'NEW':
        p[0] = ast.InstantiateNode(p[2])
    elif first_token == 'IF':
        p[0] = ast.ConditionalNode(p[2], p[4], p[6])
    elif first_token == 'WHILE':
        p[0] = ast.LoopNode(p[2], p[4])
    elif first_token == 'LBRACE':
        p[0] = ast.BlockNode(p[2])
    elif first_token == 'LET':
        p[0] = ast.LetNode(p[2], p[4])
    elif first_token == 'CASE':
        p[0] = ast.CaseNode(p[2], p[4])
    elif first_token == 'NOT':
        p[0] = ast.NotNode(p[2])
    elif first_token == 'ISVOID':
        p[0] = ast.IsVoidNode(p[2])
    elif first_token == 'INT_COMP':
        p[0] = ast.IntCompNode(p[2])
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
    let_var_list : OBJECT_ID COLON type
                 | OBJECT_ID COLON type ASSIGN expr
                 | OBJECT_ID COLON type COMMA let_var_list
                 | OBJECT_ID COLON type ASSIGN expr COMMA let_var_list
    """
    fourth_token = p.slice[4].type if len(p) > 1 else None
    if len(p) == 4:
        p[0] = [(p[1], p[3], None)]
    elif len(p) == 8:
        p[0] = [(p[1], p[3], p[5])] + p[7]
    elif fourth_token == 'ASSIGN':
        p[0] = [(p[1], p[3], p[5])]
    elif fourth_token == 'COMMA':
        p[0] = [(p[1], p[3], None)] + p[5]


def p_branch_list(p):
    """
    branch_list : OBJECT_ID COLON type ACTION expr SEMICOLON
                | OBJECT_ID COLON type ACTION expr SEMICOLON branch_list
    """
    if len(p) == 7:
        p[0] = (p[1], p[3], p[5])
    else:
        p[0] = [(p[1], p[3], p[5])] + p[7]


def p_func_call(p):
    """
    func_call : obj DOT OBJECT_ID LPAREN arg_list RPAREN
              | OBJECT_ID LPAREN arg_list RPAREN
              | obj AT TYPE_ID DOT OBJECT_ID LPAREN arg_list RPAREN
    """
    if len(p) == 6:
        p[0] = ast.CallNode(p[1], p[3], p[5])
    elif len(p) == 4:
        p[0] = ast.CallNode(None, p[1], p[3])
    elif len(p) == 8:
        p[0] = ast.CallNode(p[1], p[5], p[7], p[3])


def p_obj(p):
    """
    obj : INTEGER
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
        p[0] = ast.ConstantNumNode(p[1])
    elif first_token == 'OBJECT_ID' and second_token is None:
        p[0] = ast.VariableNode(p[1])
    elif first_token == 'STRING':
        p[0] = ast.StringNode(p[1])
    elif first_token == 'BOOL':
        p[0] = ast.BoolNode(p[1])
    elif first_token == 'LPAREN':
        p[0] = p[2]
    elif first_token == 'NEW':
        p[0] = ast.InstantiateNode(p[2])
    elif first_token == 'IF':
        p[0] = ast.ConditionalNode(p[2], p[4], p[6])
    elif first_token == 'WHILE':
        p[0] = ast.LoopNode(p[2], p[4])
    elif first_token == 'LBRACE':
        p[0] = ast.BlockNode(p[2])
    elif first_token == 'CASE':
        p[0] = ast.CaseNode(p[2], p[4])
    elif first_token == 'func_call':
        p[0] = p[1]


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
    errors.append(('Syntax error in input at {!r}'.format(p)))


def parse(text: str) -> (yacc.LRParser, list):
    global errors
    errors = []
    lex = lexer.get_a_lexer()
    parser = get_a_parser()
    tree = parser.parse(text, lex)
    return tree, errors


def get_a_parser() -> yacc.LRParser:
    parser = yacc.yacc()
    return parser
