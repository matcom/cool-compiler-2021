from ply.yacc import yacc
from asts.parser_ast import (
    AssignNode,
    AttrDeclarationNode,
    BlocksNode,
    BooleanNode,
    CaseNode,
    CaseOptionNode,
    ClassDeclarationNode,
    ComplementNode,
    ConditionalNode,
    DivNode,
    EqualsNode,
    InstantiateNode,
    IntNode,
    IsVoidNode,
    LessNode,
    LessOrEqualNode,
    LetNode,
    LoopNode,
    MethodCallNode,
    MethodDeclarationNode,
    MinusNode,
    NotNode,
    ParamNode,
    PlusNode,
    ProgramNode,
    StarNode,
    StringNode,
    VarDeclarationNode,
    VariableNode,
)
from parsing.errors import SyntacticError


class Parser:
    def __init__(self, lexer) -> None:
        self.errors = []
        self.lexer = lexer
        self.tokens = lexer.tokens

        self.precedence = (
            ("right", "ASSIGN"),
            ("right", "NOT"),
            ("nonassoc", "LESSEQ", "<", "="),
            ("left", "+", "-"),
            ("left", "*", "/"),
            ("right", "ISVOID"),
            ("left", "~"),
            ("left", "@"),
            ("left", "."),
        )
        self._build()

    def _build(self):
        self._parser = yacc(module=self)

    def parse(self, program):
        return self._parser.parse(program)

    def p_program(self, p):
        """program : class_list"""
        p[0] = ProgramNode(p[1])

    def p_class_list(self, p):
        """class_list : class ';' class_list
        | class ';'"""
        if len(p) == 4:
            p[0] = [p[1]] + p[3]
        elif len(p) == 3:
            p[0] = [p[1]]

    def p_class(self, p):
        """class : CLASS TYPE INHERITS TYPE '{' feature_list '}'
        | CLASS TYPE '{' feature_list '}'"""
        if len(p) == 8:
            p[0] = ClassDeclarationNode(p[2], p[6], p[4])
        elif len(p) == 6:
            p[0] = ClassDeclarationNode(p[2], p[4])

        p[0].set_position(p.slice[1].line, p.slice[1].col)

    def p_feature_list(self, p):
        """feature_list : attribute ';' feature_list
        | method ';' feature_list
        | empty"""
        if len(p) == 4:
            p[0] = [p[1]] + p[3]
        elif len(p) == 2:
            p[0] = []

    def p_attribute(self, p):
        """attribute : ID ':' TYPE ASSIGN expression
        | ID ':' TYPE"""
        if len(p) == 6:
            p[0] = AttrDeclarationNode(p[1], p[3], p[5])
        else:
            p[0] = AttrDeclarationNode(p[1], p[3])

        p[0].set_position(p.slice[1].line, p.slice[1].col)

    def p_method(self, p):
        """method : ID '(' params_list ')' ':' TYPE '{' expression '}'
        |  ID '(' empty ')' ':' TYPE '{' expression '}'"""
        p[0] = MethodDeclarationNode(p[1], p[3], p[6], p[8])
        p[0].set_position(p.slice[1].line, p.slice[1].col)

    def p_params_list(self, p):
        """params_list : param ',' params_list
        | param"""
        if len(p) == 4:
            p[0] = [p[1]] + p[3]
        else:
            p[0] = [p[1]]

    # def p_params_list_empty(self,p):
    #     """params_list : empty"""
    #     p[0] = []

    def p_param(self, p):
        """param : ID ':' TYPE"""
        p[0] = ParamNode(p[1], p[3])
        p[0].set_position(p.slice[1].line, p.slice[1].col)

    def p_expression_list(self, p):
        """expression_list : expression ';' expression_list
        | expression ';'"""
        if len(p) == 4:
            p[0] = [p[1]] + p[3]
        elif len(p) == 3:
            p[0] = [p[1]]

    def p_expression_assigment(self, p):
        """expression : ID ASSIGN expression"""
        p[0] = AssignNode(p[1], p[3])
        p[0].set_position(p.slice[1].line, p.slice[1].col)

    def p_expression_if_then_else(self, p):
        """expression : IF expression THEN expression ELSE expression FI"""
        p[0] = ConditionalNode(p[2], p[4], p[6])
        p[0].set_position(p.slice[1].line, p.slice[1].col)

    def p_expression_while(self, p):
        """expression : WHILE expression LOOP expression POOL"""
        p[0] = LoopNode(p[2], p[4])
        p[0].set_position(p.slice[1].line, p.slice[1].col)

    def p_expression_block(self, p):
        """expression : '{' expression_list '}'"""
        p[0] = BlocksNode(p[2])
        p[0].set_position(p.slice[1].line, p.slice[1].col)

    def p_expression_let_in(self, p):
        """expression : LET let_list IN expression"""
        p[0] = LetNode(p[2], p[4])
        p[0].set_position(p.slice[1].line, p.slice[1].col)

    def p_let_list(self, p):
        """let_list : let_single ',' let_list
        | let_single"""
        if len(p) == 4:
            p[0] = [p[1]] + p[3]
        else:
            p[0] = [p[1]]

    def p_let_single(self, p):
        """let_single : ID ':' TYPE ASSIGN expression
        | ID ':' TYPE"""
        if len(p) == 6:
            p[0] = VarDeclarationNode(p[1], p[3], p[5])
        else:
            p[0] = VarDeclarationNode(p[1], p[3])
        p[0].set_position(p.slice[1].line, p.slice[1].col)

    def p_expression_case(self, p):
        """expression : CASE expression OF case_list ESAC"""
        p[0] = CaseNode(p[2], p[4])
        p[0].set_position(p.slice[1].line, p.slice[1].col)

    def p_case_list(self, p):
        """case_list : case_single case_list
        | case_single"""
        if len(p) == 3:
            p[0] = [p[1]] + p[2]
        else:
            p[0] = [p[1]]

    def p_case_single(self, p):
        """case_single : ID ':' TYPE RET expression ';'"""
        p[0] = CaseOptionNode(p[1], p[3], p[5])
        p[0].set_position(p.slice[1].line, p.slice[1].col)

    def p_expression_dispatch(self, p):
        """expression : expression '@' TYPE '.' ID '(' args_list ')'
        | expression '.' ID '(' args_list ')'
        | ID '(' args_list ')'"""
        if len(p) == 9:
            p[0] = MethodCallNode(p[1], p[3], p[5], p[7])
            p[0].set_position(p.slice[2].line, p.slice[2].col)

        elif len(p) == 7:
            p[0] = MethodCallNode(p[1], None, p[3], p[5])
            p[0].set_position(p.slice[2].line, p.slice[2].col)

        else:
            p[0] = MethodCallNode(None, None, p[1], p[3])
            p[0].set_position(p.slice[1].line, p.slice[1].col)

    def p_expression_dispatch_empty(self, p):
        """expression : expression '@' TYPE '.' ID '(' empty ')'
        | expression '.' ID '(' empty ')'
        | ID '(' empty ')'"""
        if len(p) == 9:
            p[0] = MethodCallNode(p[1], p[3], p[5], p[7])
            p[0].set_position(p.slice[2].line, p.slice[2].col)

        elif len(p) == 7:
            p[0] = MethodCallNode(p[1], None, p[3], p[5])
            p[0].set_position(p.slice[2].line, p.slice[2].col)

        else:
            p[0] = MethodCallNode(None, None, p[1], p[3])
            p[0].set_position(p.slice[1].line, p.slice[1].col)

    def p_args_list(self, p):
        """args_list : expression ',' args_list
        | expression"""
        if len(p) == 4:
            p[0] = [p[1]] + p[3]
        else:
            p[0] = [p[1]]

    # def p_args_list_empty(self,p):
    #     """args_list : empty"""
    #     p[0] = []

    def p_expression_instatiate(self, p):
        """expression : NEW TYPE"""
        p[0] = InstantiateNode(p[2])
        p[0].set_position(p.slice[1].line, p.slice[1].col)

    def p_expression_isvoid(self, p):
        """expression : ISVOID expression"""
        p[0] = IsVoidNode(p[2])
        p[0].set_position(p.slice[1].line, p.slice[1].col)

    def p_expression_not(self, p):
        """expression : NOT expression"""
        p[0] = NotNode(p[2])
        p[0].set_position(p.slice[1].line, p.slice[1].col)

    def p_expression_complement(self, p):
        """expression : '~' expression"""
        p[0] = ComplementNode(p[2])
        p[0].set_position(p.slice[1].line, p.slice[1].col)

    def p_expression_plus(self, p):
        """expression : expression '+' expression"""
        p[0] = PlusNode(p[1], p[3])
        p[0].set_position(p.slice[2].line, p.slice[2].col)

    def p_expression_minus(self, p):
        """expression : expression '-' expression"""
        p[0] = MinusNode(p[1], p[3])
        p[0].set_position(p.slice[2].line, p.slice[2].col)

    def p_expression_div(self, p):
        """expression : expression '/' expression"""
        p[0] = DivNode(p[1], p[3])
        p[0].set_position(p.slice[2].line, p.slice[2].col)

    def p_expression_star(self, p):
        """expression : expression '*' expression"""
        p[0] = StarNode(p[1], p[3])
        p[0].set_position(p.slice[2].line, p.slice[2].col)

    def p_expression_less(self, p):
        """expression : expression '<' expression"""
        p[0] = LessNode(p[1], p[3])
        p[0].set_position(p.slice[2].line, p.slice[2].col)

    def p_expression_lesseq(self, p):
        """expression : expression LESSEQ expression"""
        p[0] = LessOrEqualNode(p[1], p[3])
        p[0].set_position(p.slice[2].line, p.slice[2].col)

    def p_expression_equals(self, p):
        """expression : expression '=' expression"""
        p[0] = EqualsNode(p[1], p[3])
        p[0].set_position(p.slice[2].line, p.slice[2].col)

    def p_expression_parentheses(self, p):
        """expression : '(' expression ')'"""
        p[0] = p[2]
        p[0].set_position(p.slice[1].line, p.slice[1].col)

    def p_expression_string(self, p):
        """expression : STRING"""
        p[0] = StringNode(p[1])
        p[0].set_position(p.slice[1].lineno, p.slice[1].col)

    def p_expression_variable(self, p):
        """expression : ID"""
        p[0] = VariableNode(p[1])
        p[0].set_position(p.slice[1].line, p.slice[1].col)

    def p_expression_true(self, p):
        """expression : TRUE"""
        p[0] = BooleanNode(True)
        p[0].set_position(p.slice[1].line, p.slice[1].col)

    def p_expression_false(self, p):
        """expression : FALSE"""
        p[0] = BooleanNode(False)
        p[0].set_position(p.slice[1].line, p.slice[1].col)

    def p_expression_int(self, p):
        """expression : INT"""
        p[0] = IntNode(p[1])
        p[0].set_position(p.slice[1].line, p.slice[1].col)

    def p_empty(self, p):
        """empty :"""
        p[0] = []

    def p_error(self, t):
        if t is None:
            self.errors.append(SyntacticError("EOF", 0, 0))
        else:
            self.errors.append(SyntacticError(t.value, t.line, t.col))
