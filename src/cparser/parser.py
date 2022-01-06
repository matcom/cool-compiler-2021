from ply import yacc
from utils.ast import *
from utils.errors import SyntacticError
from utils.utils import find_column


class CoolParser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.parser = yacc.yacc(start='program', module=self)
        self.errors = []

    procedence = (
        ('left, AT'),
        ('left, NOT'),
        ('left, ISVOID'),
        ('left, EQUAL, LESS, LESSEQ'),
        ('left, PLUS, MINUS'),
        ('left, STAR, DIV'),
        ('left, DOT')
    )

    def parse(self, program):
        return self.parser.parse(program, self.lexer.lexer)

    def p_program(self, p):
        'program : class_list'
        p[0] = ProgramNode(p[1])

    def p_epsilon(self, p):
        'epsilon :'

    def p_class_list(self, p):
        '''class_list : def_class SEMICOLON class_list
                      | def_class SEMICOLON '''
        p[0] = [p[1]] if len(p) == 3 else [p[1]] + p[3]

    def p_def_class(self, p):
        '''def_class : CLASS TYPE LPAREN feature_list RPAREN
                     | CLASS TYPE INHERITS TYPE LPAREN feature_list RPAREN'''
        if len(p) == 8:
            p[0] = ClassDeclarationNode(p[2], p[6], p[4])
        else:
            p[0] = ClassDeclarationNode(p[2], p[4])

        p[0].add_line_column(p.lineno(2), find_column(
            p.lexer.lexdata, p.lexpos(2)))

    def p_feature_list(self, p):
        '''feature_list : def_attr SEMICOLON feature_list
                        | def_func SEMICOLON feature_list
                        | epsilon'''
        p[0] = [p[1]] + p[3] if len(p) == 4 else []

    def p_def_attr(self, p):
        '''def_attr : ID COLON TYPE
                    | ID COLON TYPE ASSIGN expr'''
        if len(p) == 4:
            p[0] = AttrDeclarationNode(p[1], p[3])
        else:
            p[0] = AttrDeclarationNode(p[1], p[3], p[5])

        p[0].add_line_column(p.lineno(3), find_column(
            p.lexer.lexdata, p.lexpos(3)))

    def p_def_func(self, p):
        '''def_func : ID LPAREN params RPAREN COLON TYPE LBRACE expr RBRACE'''
        p[0] = FuncDeclarationNode(p[1], p[3], p[6], p[8])
        p[0].add_line_column(p.lineno(6), find_column(
            p.lexer.lexdata, p.lexpos(6)))

    def p_params(self, p):
        '''params : param_list
                  | param_list_empty'''
        p[0] = p[1]

    def p_param_list(self, p):
        '''param_list : param
                      | param COMMA param_list'''
        p[0] = [p[1]] if len(p) == 2 else [p[1]] + p[3]

    def p_param_list_empty(self, p):
        '''para,_list_empty : epsilon'''
        p[0] = []

    def p_param(self, p):
        '''param : ID COLON TYPE'''
        p[0] = (p[1], p[3])

    def p_expr_flow(self, p):
        '''expr : LET let_attrs IN expr
                | CASE expr OF case_list ESAC
                | IF expr THEN expr ELSE expr FI
                | WHILE expr LOOP expr POOL'''

        if p[1].lower() == 'let':
            p[0] = LetNode(p[2], p[4])
        elif p[1].lower() == 'case':
            p[0] = CaseNode(p[2], p[4])
        elif p[1].lower() == 'if':
            p[0] = IfNode(p[2], p[4], p[6])
        elif p[1].lower() == 'while':
            p[0] = WhileNode(p[2], p[4])

        p[0].add_line_column(p.lineno(2), find_column(
            p.lexer.lexdata, p.lexpos(2)))

    def p_expr_assign(self, p):
        '''expr : ID ASSIGN expr'''
        p[0] = AssignNode(p[1], p[3])
        p[0].add_line_column(p.lineno(1), find_column(
            p.lexer.lexdata, p.lexpos(1)))

    def p_expr_func_call(self, p):
        '''expr : expr AT TYPE DOT ID LPAREN args RPAREN
                | expr DOT ID LPAREN args RPAREN
                | ID LPAREN args RPAREN'''
        if len(p) == 9:
            if p[7] is None:
                p[7] = []
            p[0] = FuncCallNode(p[5], p[7], p[1], p[3])
            p[0].add_line_column(p.lineno(5), find_column(
                p.lexer.lexdata, p.lexpos(5)))
        elif len(p) == 7:
            if p[5] is None:
                p[5] = []
            p[0] = FuncCallNode(p[3], p[5], p[1])
            p[0].add_line_column(p.lineno(3), find_column(
                p.lexer.lexdata, p.lexpos(3)))
        else:
            if p[3] is None:
                p[3] = []
            p[0] = FuncCallNode(p[1], p[3])
            p[0].add_line_column(p.lineno(1), find_column(
                p.lexer.lexdata, p.lexpos(1)))

        p[0].lineno = p.lineno(0)

    def p_expr_operators_binary(self, p):
        '''expr : expr PLUS expr
                | expr MINUS expr
                | expr STAR expr
                | expr DIV expr
                | expr LESS expr
                | expr LESSEQ expr
                | expr EQUAL expr'''
        if p[2] == '+':
            p[0] = PlusNode(p[1], p[3])
        elif p[2] == '-':
            p[0] = MinusNode(p[1], p[3])
        elif p[2] == '*':
            p[0] = StarNode(p[1], p[3])
        elif p[2] == '/':
            p[0] = DivNode(p[1], p[3])
        elif p[2] == '<':
            p[0] = LessNode(p[1], p[3])
        elif p[2] == '<=':
            p[0] = LessEqNode(p[1], p[3])
        elif p[2] == '<=':
            p[0] = EqualNode(p[1], p[3])

        p[0].add_line_column(p.lineno(0), find_column(
            p.lexer.lexdata, p.lexpos(0)))

    def p_expr_operators_unary(self, p):
        '''expr : NOT expr
                | ISVOID expr'''
        if p[1] == '~':
            p[0] = NotNode(p[2])
        elif p[1].lower() == 'isvoid':
            p[0] = IsVoidNode(p[2])

        p[0].add_line_column(p.lineno(2), find_column(
            p.lexer.lexdata, p.lexpos(2)))

    def p_expr_group(self, p):
        '''expr : LPAREN expr RPAREN'''
        p[0] = p[2]

    def p_expr_atom(self, p):
        '''expr : atom'''
        p[0] = p[1]

    def p_let_attrs(self, p):
        '''let_attrs : def_attr
                     | def_attr COMMA let_attrs'''
        p[0] = [p[1]] if len(p) == 2 else [p[1]] + p[3]

    def p_case_list(self, p):
        '''case_list : case_option SEMICOLON
                     | case_option SEMICOLON case_list'''
        p[0] = [p[1]] if len(p) == 3 else [p[1]] + p[3]

    def p_case_option(self, p):
        '''case_option : ID COLON TYPE ARROW expr'''
        p[0] = CaseOptionNode(p[1], p[3], p[5])
        p[0].add_line_column(p.lineno(3), find_column(
            p.lexer.lexdata, p.lexpos(3)))

    def p_args(self, p):
        '''args : arg_list
                | arg_list_empty'''
        p[0] = p[1]

    def p_arg_list(self, p):
        '''arg_list : expr
                    | expr COMMA arg_list'''
        p[0] = [p[1]] if len(p) == 2 else [p[1]] + p[3]

    def p_arg_list_empty(self, p):
        '''arg_list_empty : epsilon'''
        p[0] = []

    def p_atom_int(self, p):
        '''atom : INT'''
        p[0] = IntNode(int(p[1]))
        p[0].add_line_column(p.lineno(1), find_column(
            p.lexer.lexdata, p.lexpos(1)))

    def p_atom_id(self, p):
        '''atom : ID'''
        p[0] = VarNode(p[1])
        p[0].add_line_column(p.lineno(1), find_column(
            p.lexer.lexdata, p.lexpos(1)))

    def p_atom_bool(self, p):
        '''atom : BOOL'''
        p[0] = BoolNode(p[1])
        p[0].add_line_column(p.lineno(1), find_column(
            p.lexer.lexdata, p.lexpos(1)))

    def p_atom_string(self, p):
        '''atom : STRING'''
        p[0] = StringNode(p[1])
        p[0].add_line_column(p.lineno(1), find_column(
            p.lexer.lexdata, p.lexpos(1)))

    def p_atom_new(self, p):
        '''atom : NEW TYPE'''
        p[0] = NewNode(p[2])
        p[0].add_line_column(p.lineno(2), find_column(
            p.lexer.lexdata, p.lexpos(2)))

    def p_atom_block(self, p):
        '''atom : block'''
        p[0] = p[1]

    def p_block(self, p):
        '''block : LBRACE block_list RBRACE'''
        p[0] = p[2]

    def p_block_list(self, p):
        ''' block_list : expr SEMICOLON
                       | expr SEMICOLON block_list'''
        p[0] = BlockNode([p[1]]) if len(
            p) == 3 else BlockNode([p[1]] + p[3].exprs)

    def p_error(self, p):
        if p:
            self.lexer.add_line_column(p)
            self.errors.append(SyntacticError(
                f'ERROR at or near {p.value}', p.line, p.column))
        else:
            self.errors.append(SyntacticError('ERROR at or near EOF', 0, 0))
