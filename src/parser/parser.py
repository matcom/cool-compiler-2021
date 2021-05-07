import ply.yacc as yacc
from nodes import *
from lexer import MyLexer
from .syntactic_error import SyntaxError
import sys

class MyParser():
    def __init__(self, build_parser=True, debug=False, write_tables=True, optimize=True, outputdir="", yacctab="pycoolc.yacctab", debuglog=None, errorlog=None, tracking =True):
        
        self.build(debug=debug, write_tables=write_tables, optimize=optimize, outputdir=outputdir,
                    yacctab=yacctab, debuglog=debuglog, errorlog=errorlog)

    # Build the parser
    def build(self, **kwargs):

        debug = kwargs.get("debug")
        write_tables = kwargs.get("write_tables")
        optimize = kwargs.get("optimize")
        outputdir = kwargs.get("outputdir")
        yacctab = kwargs.get("yacctab")
        debuglog = kwargs.get("debuglog")

        self.lexer = MyLexer()
        self.tokens = self.lexer.tokens
        self.errors = []
        self.parser = yacc.yacc(module=self, write_tables=write_tables, debug=debug, optimize=optimize,
                                outputdir=outputdir, tabmodule=yacctab, debuglog=debuglog, errorlog=yacc.NullLogger())

    def parse(self, _cool_program):
        return self.parser.parse(_cool_program)
    
    def find_col(self, input, lexpos):
        _start = input.rfind('\n', 0, lexpos) + 1
        return (lexpos - _start) + 1
    
    # Precedence rules
    precedence = (
        ('right', 'ASSIGN'),
        ('right', 'NOT'),
        ('nonassoc', 'LESS', 'LESSEQ', 'EQUAL'),
        ('left', 'PLUS', 'MINUS'),
        ('left', 'MULTIPLY', 'DIVIDE'),
        ('right', 'ISVOID'),
        ('right', 'NOX'),
        ('right', 'ARROBA'),
        ('right', 'DOT')
    )

    # Grammar rules declarations
    def p_program(self, p):
        '''
        program : class_list
        '''
        p[0] = ProgramNode(classes=p[1])

    def p_class_list(self, p):
        '''
        class_list : class_list class SEMIC
                   | class SEMIC
        '''
        p[0] = (p[1],) if len(p) == 3 else p[1] + (p[2],)
        
    def p_def_class(self, p):
        '''
        class : CLASS TYPE LBRACE feature_opt RBRACE
        '''
        p[0] = ClassNode(
            name=p[2], parent='Object', features=p[4], row=p.lineno(2), col=self.find_col(p.lexer.lexdata, p.lexpos(2)))
       
    def p_def_class_inherits(self, p):
        '''
        class : CLASS TYPE INHERITS TYPE LBRACE feature_opt RBRACE
        '''
        p[0] = ClassNode(
            name=p[2], parent=p[4], features=p[6], row=p.lineno(2), col=self.find_col(p.lexer.lexdata, p.lexpos(4)))

    def p_feature_list(self, p):
        '''
        feature_list : feature_list feature SEMIC
                     | feature SEMIC
        '''
        p[0] = (p[1],) if len(p) == 3 else p[1] + (p[2],)
    
    def p_feature_opt(self, p):
        '''
        feature_opt : feature_list
                    | empty
        '''
        p[0] = tuple() if p.slice[1].type == "empty" else p[1]

    def p_feature_f_class_method(self, p):
        '''
        feature : ID LPAREN formal_param_list RPAREN COLON TYPE LBRACE expr RBRACE
        '''
        p[0] = ClassMethodNode(
            name=p[1], params=p[3], expression=p[8], return_type=p[6], row=p.lineno(1), col=self.find_col(p.lexer.lexdata, p.lexpos(1)))

    def p_feature_class_method(self, p):
        '''
        feature : ID LPAREN RPAREN COLON TYPE LBRACE expr RBRACE
        '''
        p[0] = ClassMethodNode(
            name=p[1], params=tuple(), expression=p[7], return_type=p[5], row=p.lineno(1), col=self.find_col(p.lexer.lexdata, p.lexpos(1)))

    def p_feature_attr(self, p):
        '''
        feature : attr_init
        '''
        p[0] = p[1]

    def p_attr_init(self, p):
        '''
        attr_init : ID COLON TYPE ASSIGN expr 
                  | attr_def
        '''
        p[0] = p[1] if len(p) == 2 else AttrInitNode(
            name=p[1], attr_type=p[3], expression=p[5], row=p.lineno(1), col=self.find_col(p.lexer.lexdata, p.lexpos(1)))

    def p_attr_def(self, p):
        '''
        attr_def : ID COLON TYPE
        '''
        p[0] = AttrDefNode(
            name=p[1], attr_type=p[3], row=p.lineno(1), col=self.find_col(p.lexer.lexdata, p.lexpos(1)))

    def p_action_list(self, p):
        '''
        action_list : action_list action
                    | action
        '''
        p[0] = (p[1],) if len(p) == 2 else tuple(p[1]) + (p[2],)

    def p_action(self, p):
        '''
        action : ID COLON TYPE ARROW expr SEMIC
        '''
        p[0] = ActionNode(
            name=p[1], act_type=p[3], body=p[5], row=p.lineno(1), col=self.find_col(p.lexer.lexdata, p.lexpos(1)))

    def p_let_var(self, p):
        '''
        let_var  : let_init
                 | let_var COMMA let_init
        '''
        p[0] = (p[1],) if len(p) == 2 else p[1] + (p[3],)

    def p_let_init(self, p):
        '''
        let_init : ID COLON TYPE ASSIGN expr 
                 | let_def
        '''
        p[0] = p[1] if len(p) == 2 else LetInitNode(
            name=p[1], let_type=p[3], expression=p[5], row=p.lineno(2), col=self.find_col(p.lexer.lexdata, p.lexpos(2)))            

    def p_let_def(self, p):
        '''
        let_def : ID COLON TYPE
        '''
        p[0] = LetDefNode(
            name=p[1], let_type=p[3], row=p.lineno(1), col=self.find_col(p.lexer.lexdata, p.lexpos(1)))

    def p_formal_param_list(self, p):
        '''
        formal_param_list  : formal_param_list COMMA formal_param
                           | formal_param
        '''
        p[0] = (p[1],) if len(p) == 2 else p[1] + (p[3],)

    def p_formal_param(self, p):
        '''
        formal_param : ID COLON TYPE
        '''
        p[0] = FormalParamNode(
            name=p[1], param_type=p[3], row=p.lineno(1), col=self.find_col(p.lexer.lexdata, p.lexpos(1)))

    def p_args_list(self, p):
        '''
        args_list : args_list COMMA expr
                  | expr
        '''
        p[0] = (p[1],) if len(p) == 2 else p[1] + (p[3],)

    def p_args_list_opt(self, p):
        '''
        args_list_opt : args_list
                      | empty
        '''
        p[0] = tuple() if p.slice[1].type == "empty" else p[1]

    def p_expr_dynamic_call(self, p):
        '''
        expr : expr DOT ID LPAREN args_list_opt RPAREN
        '''
        p[0] = DynamicCallNode(
            obj=p[1], method=p[3], args=p[5], row=p.lineno(3), col=self.find_col(p.lexer.lexdata, p.lexpos(3)))

    def p_expr_static_call(self, p):
        '''
        expr : expr ARROBA TYPE DOT ID LPAREN args_list_opt RPAREN
        '''
        p[0] = StaticCallNode(
            obj=p[1], static_type=p[3], method=p[5], args=p[7], row=p.lineno(5), col=self.find_col(p.lexer.lexdata, p.lexpos(5)))

    def p_expr_self_call(self, p):
        '''
        expr : ID LPAREN args_list_opt RPAREN
        '''
        p[0] = DynamicCallNode(
            obj=IdNode('self', row=p.lineno(1), col=self.find_col(p.lexer.lexdata, p.lexpos(1))), method=p[1], args=p[3], row=p.lineno(1), col=self.find_col(p.lexer.lexdata, p.lexpos(1)))

    def p_expr_assign(self, p):
        '''
        expr : ID ASSIGN expr
        '''
        p[0] = AssignNode(
            name=p[1], expression=p[3], row=p.lineno(1), col=self.find_col(p.lexer.lexdata, p.lexpos(1)))

    def p_expr_if(self, p):
        '''
        expr : IF expr THEN expr ELSE expr FI
        '''
        p[0] = IfNode(
            predicate=p[2], then_expr=p[4], else_expr=p[6], row=p.lineno(1), col=self.find_col(p.lexer.lexdata, p.lexpos(1)))

    def p_expr_while(self, p):
        '''
        expr : WHILE expr LOOP expr POOL
        '''
        p[0] = WhileNode(
            predicate=p[2], expression=p[4], row=p.lineno(1), col=self.find_col(p.lexer.lexdata, p.lexpos(1)))

    def p_block_list(self, p):
        '''
        block_list : block_list expr SEMIC
                   | expr SEMIC
        '''
        p[0] = (p[1],) if len(p) == 3 else p[1] + (p[2],)
    
    def p_expr_block(self, p):
        '''
        expr : LBRACE block_list RBRACE
        '''
        p[0] = BlockNode(
            expr_list=p[2], row=p.lineno(1), col=self.find_col(p.lexer.lexdata, p.lexpos(1)))

    def p_expr_simple_let(self, p):
        '''
         expr : let_expr
        '''
        p[0] = p[1]

    def p_expr_let(self, p):
        '''
        let_expr : LET let_var IN expr
        '''
        p[0] = LetNode(
            init_list=p[2], body=p[4], row=p.lineno(2), col=self.find_col(p.lexer.lexdata, p.lexpos(2)))

    def p_expr_case(self, p):
        '''
        expr : CASE expr OF action_list ESAC
        '''
        p[0] = CaseNode(
            expression=p[2], act_list=p[4], row=p.lineno(1), col=self.find_col(p.lexer.lexdata, p.lexpos(1)))

    def p_expr_new(self, p):
        '''
        expr : NEW TYPE
        '''
        p[0] = NewNode(
            new_type=p[2], row=p.lineno(2), col=self.find_col(p.lexer.lexdata, p.lexpos(2)))

    def p_expr_isvoid(self, p):
        '''
        expr : ISVOID expr
        '''
        p[0] = IsVoidNode(
            expression=p[2], row=p.lineno(2), col=self.find_col(p.lexer.lexdata, p.lexpos(2)))

    def p_expr_id(self, p):
        '''
        expr : ID
        '''
        p[0] = IdNode(
            name=p[1], row=p.lineno(1), col=self.find_col(p.lexer.lexdata, p.lexpos(1)))

    def p_expr_int(self, p):
        '''
        expr : INTEGER
        '''
        p[0] = IntegerNode(
            value=p[1], row=p.lineno(1), col=self.find_col(p.lexer.lexdata, p.lexpos(1)))

    def p_expr_str(self, p):
        '''
        expr : STRING
        '''
        p[0] = StringNode(
            value=p[1], row=p.lineno(1), col=self.find_col(p.lexer.lexdata, p.lexpos(1)))

    def p_expr_bool(self, p):
        '''
        expr : TRUE 
             | FALSE
        '''
        p[0] = BooleanNode(
            value=p[1], row=p.lineno(1), col=self.find_col(p.lexer.lexdata, p.lexpos(1)))

    def p_expr_binary_op(self, p):
        '''
        expr : expr PLUS expr
             | expr MINUS expr
             | expr MULTIPLY expr
             | expr DIVIDE expr
             | expr LESS expr
             | expr LESSEQ expr
             | expr EQUAL expr
        '''
        if p[2] == '+':
            p[0] = SumNode(
                left=p[1], right=p[3], row=p.lineno(2), col=self.find_col(p.lexer.lexdata, p.lexpos(2)))
        elif p[2] == '-':
            p[0] = SubNode(
                left=p[1], right=p[3], row=p.lineno(2), col=self.find_col(p.lexer.lexdata, p.lexpos(2)))
        elif p[2] == '*':
            p[0] = MultNode(
                left=p[1], right=p[3], row=p.lineno(2), col=self.find_col(p.lexer.lexdata, p.lexpos(2)))
        elif p[2] == '/':
            p[0] = DivNode(
                left=p[1], right=p[3], row=p.lineno(2), col=self.find_col(p.lexer.lexdata, p.lexpos(2)))
        elif p[2] == '<':
            p[0] = LessNode(
                left=p[1], right=p[3], row=p.lineno(2), col=self.find_col(p.lexer.lexdata, p.lexpos(2)))
        elif p[2] == '<=':
            p[0] = LessEqualNode(
                left=p[1], right=p[3], row=p.lineno(2), col=self.find_col(p.lexer.lexdata, p.lexpos(2)))
        elif p[2] == '=':
            p[0] = EqualsNode(
                left=p[1], right=p[3], row=p.lineno(2), col=self.find_col(p.lexer.lexdata, p.lexpos(2)))

    def p_expr_unary_op(self, p):
        '''
        expr : NOX expr
             | NOT expr
        '''
        if p[1] == '~':
            p[0] = LogicNotNode(
                expression=p[2], row=p.lineno(1), col=self.find_col(p.lexer.lexdata, p.lexpos(1)))
        elif p[1].lower() == 'not':
            p[0] = NotNode(
                expression=p[2], row=p.lineno(1), col=self.find_col(p.lexer.lexdata, p.lexpos(1)))

    def p_expr_parenthesis(self, p):
        '''
        expr : LPAREN expr RPAREN
        '''
        p[0] = p[2]

    def p_empty(self, p):
        '''
        empty :
        '''
        p[0] = None

    # Error rule for Syntax Errors handling
    def p_error(self, p):
        if p:
            self.errors.append(SyntaxError(f'"ERROR at or near {p.value}"', p.lineno, self.find_col(p.lexer.lexdata, p.lexpos)))
            self.parser.errok()
        else:
            self.errors.append(SyntaxError('"ERROR at or near EOF"',0,0))
            return

    