from lexing.lexing_rules import tokens

from .ast import (AssignNode, AttrDeclarationNode, BlocksNode, BooleanNode,
                  CaseNode, CaseOptionNode, ClassDeclarationNode,
                  ComplementNode, ConditionalNode, DivNode, EqualsNode,
                  InstantiateNode, IntNode, IsVoidNode, LessNode,
                  LessOrEqualNode, LetNode, LoopNode, MethodCallNode, MethodDeclarationNode,
                  MinusNode, NotNode, PlusNode, ProgramNode, StarNode,
                  StringNode, VarDeclarationNode)


def p_program(p):
    """program : class_list"""
    p[0] = ProgramNode(p[1])


def p_class_list(p):
    """class_list : class ';' class_list
                  | class ';'"""
    if len(p) == 4:
        p[0] = [p[1]] + p[3]
    elif len(p) == 3:
        p[0] = [p[1]]


def p_class(p):
    """class : CLASS ID INHERITS ID '{' feature_list '}'
             | CLASS ID '{' feature_list '}'"""
    if len(p) == 8:
        p[0] = ClassDeclarationNode(p[2], p[6], p[4])
    elif len(p) == 6:
        p[0] = ClassDeclarationNode(p[2], p[4])


def p_feature_list(p):
    """feature_list : attribute ';' feature_list
                    | method ';' feature_list
                    | empty"""
    if len(p) == 4:
        p[0] = [p[1]] + p[3]
    elif len(p) == 2:
        p[0] = []


def p_attribute(p):
    """attribute : ID ':' ID ASSIGN expression
                 | ID ':' ID """
    if len(p) == 6:
        p[0] = AttrDeclarationNode(p[1], p[3], p[5])
    else:
        p[0] = AttrDeclarationNode(p[1], p[3])


def p_method(p):
    """method : ID '(' params_list ')' ':' ID '{' expression '}'"""
    p[0] = MethodDeclarationNode(p[1], p[3], p[6], p[8])


def p_params_list(p):
    """params_list : param ',' params_list
                   | param
                   | empty"""
    if len(p) == 4:
        p[0] = [p[1]] + p[3]
    else:
        p[0] = [p[1]]


def p_param(p):
    """param : ID ':' ID"""
    p[0] = VarDeclarationNode(p[1], p[3])


def p_expression_list(p):
    """expression_list : expression ';' expression_list
                       | expression ';' """
    if len(p) == 4:
        p[0] = [p[1]] + p[3]
    elif len(p) ==  3:
        p[0] = [p[1]]


def p_expression_assigment(p):
    """expression : ID ASSIGN expression"""
    p[0] = AssignNode(p[1], p[3])


def p_expression_if_then_else(p):
    """expression : IF expression THEN expression ELSE expression FI"""
    p[0] = ConditionalNode(p[2], p[4], p[6])


def p_expression_while(p):
    """expression : WHILE expression LOOP expression POOL"""
    p[0] = LoopNode(p[2], p[4])


def p_expression_block(p):
    """expression : '{' expression_list '}'"""
    p[0] = BlocksNode(p[2])


def p_expression_let_in(p):
    """expression : LET let_list IN expression"""
    p[0] = LetNode(p[2], p[4])


def p_let_list(p):
    """let_list : let_single ',' let_list
                | let_single"""
    if len(p) == 4:
        p[0] = [p[1]] + p[3]
    else:
        p[0] = [p[1]]


def p_let_single(p):
    """let_single : ID ':' ID ASSIGN expression
                  | ID ':' ID"""
    if len(p) == 6:
        p[0] = VarDeclarationNode(p[1], p[3], p[5])
    else:
        p[0] = VarDeclarationNode(p[1], p[3])


def p_expression_case(p):
    """expression : CASE expression OF case_list ESAC"""
    p[0] = CaseNode(p[2], p[4])


def p_case_list(p):
    """case_list : case_single case_list
                 | case_single"""
    if len(p) == 3:
        p[0] = [p[1]] + p[2]
    else:
        p[0] = [p[1]]


def p_case_single(p):
    """case_single : ID ':' ID RET expression ';'"""
    p[0] = CaseOptionNode(p[1],p[3],p[5])   
    


def p_expression_dispatch(p):
    """expression : expression '@' ID '.' ID '(' args_list ')'
                  | expression '.' ID '(' args_list ')'
                  | ID '(' args_list ')'"""
    if len(p) == 9:
        p[0] = MethodCallNode(p[1],p[3],p[5],p[7])
    elif len(p) == 7:
        p[0] = MethodCallNode(p[1], None, p[3], p[5])
    else:
        p[0]= MethodCallNode(None, None, p[1], p[3])
    

def p_args_list(p):
    """args_list : expression ',' args_list
                 | expression 
                 | empty"""
    if len(p) == 4:
        p[0] = [p[1]] + p[3]
    else:
        p[0] = [p[1]]

def p_expression_instatiate(p):
    """expression : NEW ID"""
    p[0] = InstantiateNode(p[2])


def p_expression_isvoid(p):
    """expression : ISVOID expression"""
    p[0] = IsVoidNode(p[2])


def p_expression_not(p):
    """expression : NOT expression"""
    p[0] = NotNode(p[2])


def p_expression_complement(p):
    """expression : '~' expression"""
    p[0] = ComplementNode(p[2])


def p_expression_plus(p):
    """expression : expression '+' expression"""
    p[0] = PlusNode(p[1],p[3])


def p_expression_minus(p):
    """expression : expression '-' expression"""
    p[0] = MinusNode(p[1],p[3])


def p_expression_div(p):
    """expression : expression '/' expression"""
    p[0] = DivNode(p[1],p[3])


def p_expression_star(p):
    """expression : expression '*' expression"""
    p[0] = StarNode(p[1],p[3])


def p_expression_less(p):
    """expression : expression '<' expression"""
    p[0] = LessNode(p[1],p[3])


def p_expression_lesseq(p):
    """expression : expression LESSEQ expression"""
    p[0] = LessOrEqualNode(p[1],p[3])


def p_expression_equals(p):
    """expression : expression '=' expression"""
    p[0] = EqualsNode(p[1],p[3])


def p_expression_parentheses(p):
    """expression : '(' expression ')'"""
    p[0] = p[2]


def p_expression_string(p):
    """expression : STRING"""
    p[0] = StringNode(p[1])


def p_expression_variable(p):
    """expression : ID"""
    p[0] = InstantiateNode(p[1])


def p_expression_true(p):
    """expression : TRUE"""
    p[0] = BooleanNode(True)


def p_expression_false(p):
    """expression : FALSE"""
    p[0] = BooleanNode(False)


def p_expression_int(p):
    """expression : INT"""
    p[0] = IntNode(p[1])


def p_empty(p):
    """empty : """
    pass


def p_error(p):
    print(f"Syntax error in input! {p} line:{p.lineno} col:{p.col}")



precedence = (
    ('right', 'ASSIGN'),
    ('right', 'NOT'),
    ('nonassoc', 'LESSEQ', '<', '='),
    ('left', '+','-'),
    ('left', '*', '/'),
    ('right', 'ISVOID'),
    ('left', '~'),
    ('left', '@'),
    ('left', '.')
)
