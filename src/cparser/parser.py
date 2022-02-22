from ply import yacc
from utils.ast import *
from utils.errors import SyntacticError
from utils.utils import find_column, tokens


class CoolParser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.tokens = tokens
        self.parser = yacc.yacc(start='program', module=self)
        self.errors = []

    # precedence = (
    #     ('left, AT'),
    #     ('left, NOT'),
    #     ('left, ISVOID'),
    #     ('left, EQUAL, LESS, LESSEQ'),
    #     ('left, PLUS, MINUS'),
    #     ('left, STAR, DIV'),
    #     ('left, DOT')
    # )

    precedence = (
        ('right', 'ASSIGN'),
        ('right', 'NOT'),
        ('nonassoc', 'LESSEQ', 'LESS', 'EQUAL'),
        ('left', 'PLUS', 'MINUS'),
        ('left', 'STAR', 'DIV'),
        ('right', 'ISVOID'),
        ('left', 'AT'),
        ('left', 'DOT')
    )

    def parse(self, program):
        return self.parser.parse(program, self.lexer.lexer)

    def p_program(self, p):
        'program : class_list'
        p[0] = ProgramNode(p[1])

    def p_epsilon(self, p):
        'epsilon :'
        pass

    def p_class_list(self, p):
        '''class_list : def_class SEMICOLON class_list
                      | def_class SEMICOLON '''
        p[0] = [p[1]] if len(p) == 3 else [p[1]] + p[3]

    def p_def_class(self, p):
        '''def_class : CLASS TYPE LBRACE feature_list RBRACE
                     | CLASS TYPE INHERITS TYPE LBRACE feature_list RBRACE'''
        if len(p) == 8:
            p[0] = ClassDeclarationNode(p.slice[2], p[6], p.slice[4])
        else:
            p[0] = ClassDeclarationNode(p.slice[2], p[4])

    def p_feature_list(self, p):
        '''feature_list : def_attr SEMICOLON feature_list
                        | def_func SEMICOLON feature_list
                        | epsilon'''
        p[0] = [p[1]] + p[3] if len(p) == 4 else []

    def p_def_attr(self, p):
        '''def_attr : ID COLON TYPE
                    | ID COLON TYPE ASSIGN expr'''
        if len(p) == 4:
            p[0] = AttrDeclarationNode(p.slice[1], p.slice[3])
        else:
            p[0] = AttrDeclarationNode(p.slice[1], p.slice[3], p[5])

    def p_def_func(self, p):
        '''def_func : ID LPAREN params RPAREN COLON TYPE LBRACE expr RBRACE'''
        p[0] = FuncDeclarationNode(p.slice[1], p[3], p.slice[6], p[8])

    def p_params(self, p):
        '''params : param_list
                  | param_list_empty'''
        p[0] = p[1]

    def p_param_list(self, p):
        '''param_list : param
                      | param COMMA param_list'''
        p[0] = [p[1]] if len(p) == 2 else [p[1]] + p[3]

    def p_param_list_empty(self, p):
        '''param_list_empty : epsilon'''
        p[0] = []

    def p_param(self, p):
        '''param : ID COLON TYPE'''
        p[0] = (p.slice[1], p.slice[3])

    def p_expr_flow(self, p):
        '''expr : LET let_attrs IN expr
                | CASE expr OF case_list ESAC
                | IF expr THEN expr ELSE expr FI
                | WHILE expr LOOP expr POOL'''

        if p[1].lower() == 'let':
            p[0] = LetInNode(p[2], p[4], p.slice[1])
        elif p[1].lower() == 'case':
            p[0] = CaseNode(p[2], p[4], p.slice[1])
        elif p[1].lower() == 'if':
            p[0] = IfThenElseNode(p[2], p[4], p[6], p.slice[1])
        elif p[1].lower() == 'while':
            p[0] = WhileNode(p[2], p[4], p.slice[1])

    def p_expr_assign(self, p):
        '''expr : ID ASSIGN expr'''
        p[0] = AssignNode(p.slice[1], p[3])

    def p_expr_func_call(self, p):
        '''expr : expr AT TYPE DOT ID LPAREN args RPAREN
                | expr DOT ID LPAREN args RPAREN
                | ID LPAREN args RPAREN'''
        if len(p) == 9:
            if p[7] is None:
                p[7] = []
            p[0] = ArrobaCallNode(p[1], p.slice[5], p[7], p.slice[3])

        elif len(p) == 7:
            if p[5] is None:
                p[5] = []
            p[0] = DotCallNode(p[1], p.slice[3], p[5])

        else:
            if p[3] is None:
                p[3] = []
            p[0] = MemberCallNode(p.slice[1], p[3])

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
        elif p[2] == '=':
            p[0] = EqualNode(p[1], p[3])

    def p_expr_operators_unary(self, p):
        '''expr : NOT expr
                | ISVOID expr
                | LNOT expr'''
        if p[1] == '~':
            p[0] = NegationNode(p[2], p.slice[1])
        elif p[1].lower() == 'isvoid':
            p[0] = IsVoidNode(p[2], p.slice[1])
        elif p[1].lower() == 'not':
            p[0] = LogicNegationNode(p[2], p.slice[1])

    def p_expr_group(self, p):
        '''expr : LPAREN expr RPAREN'''
        p[0] = p[2]

    def p_expr_atom(self, p):
        '''expr : atom'''
        p[0] = p[1]

    def p_let_attrs(self, p):
        '''let_attrs : def_var
                     | def_var COMMA let_attrs'''
        p[0] = [p[1]] if len(p) == 2 else [p[1]] + p[3]

    def p_def_var(self, p):
        '''def_var : ID COLON TYPE
                   | ID COLON TYPE ASSIGN expr'''
        if len(p) == 4:
            p[0] = VarDeclarationNode(p.slice[1], p.slice[3])
        else:
            p[0] = VarDeclarationNode(p.slice[1], p.slice[3], p[5])

    def p_case_list(self, p):
        '''case_list : case_option SEMICOLON
                     | case_option SEMICOLON case_list'''
        p[0] = [p[1]] if len(p) == 3 else [p[1]] + p[3]

    def p_case_option(self, p):
        '''case_option : ID COLON TYPE ARROW expr'''
        p[0] = CaseOptionNode(p.slice[1], p.slice[3], p[5])

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
        p[0] = IntNode(p.slice[1])

    def p_atom_id(self, p):
        '''atom : ID'''
        p[0] = IdNode(p.slice[1])

    def p_atom_bool(self, p):
        '''atom : TRUE
                | FALSE'''
        p[0] = BoolNode(p.slice[1])

    def p_atom_string(self, p):
        '''atom : STRING'''
        p[0] = StringNode(p.slice[1])

    def p_atom_new(self, p):
        '''atom : NEW TYPE'''
        p[0] = NewNode(p.slice[2])

    def p_atom_block(self, p):
        '''atom : block'''
        p[0] = p[1]

    def p_block(self, p):
        '''block : LBRACE block_list RBRACE'''
        p[0] = p[2]

    def p_block_list(self, p):
        ''' block_list : expr SEMICOLON
                       | expr SEMICOLON block_list'''
        p[0] = BlockNode([p[1]], p.slice[2]) if len(
            p) == 3 else BlockNode([p[1]] + p[3].exprs, p.slice[2])

    def p_error(self, p):
        if p:
            self.add_error(p)
        else:
            self.errors.append(SyntacticError('ERROR at or near EOF', 0, 0))

            # column = find_column(p.lexer.lexdata, p.lexpos)
            # line = self.lexer.lexer.lineno
            # self.errors.append(SyntacticError(
            #     'ERROR at or near EOF', line, column - 1))

    def add_error(self, p):
        self.errors.append(SyntacticError(
            f'ERROR at or near {p.value}', p.lineno, p.column))

    def print_error(self):
        for error in self.errors:
            print(error)
