import ply.yacc as yacc
from utils.ast import *
from lexing.lexer import Lexer
from utils.errors import SyntacticError

class Parser:
    def __init__(self, lexer=None):
        self.lexer = lexer if lexer else Lexer()
        self.tokens = None
        self.parser = None
        self.errors = []
        self.build()

    def build(self):
        self.tokens = self.lexer.tokens
        self.parser = yacc.yacc(module=self)
        
    def __call__(self, code):
        return self.parser.parse(code)

############################## GRAMMAR RULES ##############################

    def p_program(self, p):
        '''
            program : class_list
        '''
        p[0] = ProgramNode(p[1])

    def p_epsilon(self, p):
        '''
            epsilon :
        '''
        pass

    def p_class_list(self, p):
        '''
            class_list : def_class class_list 
                       | def_class
        '''
        p[0] = [p[1]] if len(p) == 2 else [p[1]] + p[2]

    def p_class_list_error(self, p):
        '''
            class_list : error class_list
        '''
        p[0] = [p[1]] if len(p) == 2 else [p[1]] + p[2]

    def p_def_class(self, p):
        '''
            def_class : CLASS TYPE OCUR feature_list CCUR SEMICOLON
                      | CLASS TYPE INHERITS TYPE OCUR feature_list CCUR SEMICOLON
        '''
        if len(p) == 7:
            p[0] = ClassDeclarationNode(p.slice[2], p[4])
        else:
            p[0] = ClassDeclarationNode(p.slice[2], p[6], p.slice[4])

    def p_def_class_error(self, p):
        '''
            def_class : CLASS error OCUR feature_list CCUR SEMICOLON 
                      | CLASS TYPE OCUR feature_list CCUR error   
                      | CLASS error INHERITS TYPE OCUR feature_list CCUR SEMICOLON
                      | CLASS error INHERITS error OCUR feature_list CCUR SEMICOLON
                      | CLASS TYPE INHERITS error OCUR feature_list CCUR SEMICOLON
                      | CLASS TYPE INHERITS TYPE OCUR feature_list CCUR error
        '''
        p[0] = ErrorNode()

    def p_feature_list(self, p):
        '''
            feature_list : epsilon
                         | def_attr SEMICOLON feature_list
                         | def_func SEMICOLON feature_list
        '''
        p[0] = [] if len(p) == 2 else [p[1]] + p[3]

    def p_feature_list_error(self, p):
        '''
            feature_list : error feature_list
        '''
        p[0] = [p[1]] + p[2]

    def p_def_attr(self, p):
        '''
            def_attr : ID COLON TYPE
                     | ID COLON TYPE LARROW expr
        '''
        if len(p) == 4:
            p[0] = AttrDeclarationNode(p.slice[1], p.slice[3])
        else:
            p[0] = AttrDeclarationNode(p.slice[1], p.slice[3], p[5])

    def p_def_attr_error(self, p):
        '''
            def_attr : error COLON TYPE
                     | ID COLON error
                     | error COLON TYPE LARROW expr
                     | ID COLON error LARROW expr
                     | ID COLON TYPE LARROW error
        '''
        p[0] = ErrorNode()

    def p_def_func(self, p):
        '''
            def_func : ID OPAR formals CPAR COLON TYPE OCUR expr CCUR
        '''
        p[0] = FuncDeclarationNode(p.slice[1], p[3], p.slice[6], p[8])

    def p_def_func_error(self, p):
        '''
            def_func : error OPAR formals CPAR COLON TYPE OCUR expr CCUR
                     | ID OPAR error CPAR COLON TYPE OCUR expr CCUR
                     | ID OPAR formals CPAR COLON error OCUR expr CCUR
                     | ID OPAR formals CPAR COLON TYPE OCUR error CCUR
        '''
        p[0] = ErrorNode()

    def p_formals(self, p):
        '''
            formals  : param_list
                     | param_list_empty
        '''
        p[0] = p[1]

    def p_param_list(self, p):
        '''
            param_list : param
                       | param COMMA param_list
        '''
        p[0] = [p[1]] if len(p) == 2 else [p[1]] + p[3]

    def p_param_list_empty(self, p):
        '''
            param_list_empty : epsilon
        '''
        p[0] = []

    def p_param(self, p):
        '''
            param : ID COLON TYPE
        '''
        p[0] = (p.slice[1], p.slice[3])

    def p_let_list(self, p):
        '''
            let_list : let_assign
                     | let_assign COMMA let_list
        '''
        p[0] = [p[1]] if len(p) == 2 else [p[1]] + p[3]

    def p_let_assign(self, p):
        '''
            let_assign : param LARROW expr
                       | param
        '''
        if len(p) == 2:
            p[0] = VarDeclarationNode(p[1][0], p[1][1])
        else:
            p[0] = VarDeclarationNode(p[1][0], p[1][1], p[3])

    def p_cases_list(self, p):
        '''
            cases_list : casep SEMICOLON
                       | casep SEMICOLON cases_list
        '''
        p[0] = [p[1]] if len(p) == 3 else [p[1]] + p[3]

    def p_cases_list_error(self, p):
        '''
            cases_list : error cases_list
                       | error SEMICOLON
        '''
        p[0] = [ErrorNode()]

    def p_case(self, p):
        '''
            casep : ID COLON TYPE RARROW expr
        '''
        p[0] = OptionNode(p.slice[1], p.slice[3], p[5])

    def p_expr(self, p):
        '''
            expr : ID LARROW expr
                 | comp
        '''
        if len(p) == 4:
            p[0] = AssignNode(p.slice[1], p[3])
        else:
            p[0] = p[1]

    def p_comp(self, p):
        '''
            comp : comp LESS op
                 | comp LESSEQ op
                 | comp EQUAL op
                 | op
        '''
        if len(p) == 2:
            p[0] = p[1]
        elif p[2] == '<':
            p[0] = LessNode(p[1], p[3])
        elif p[2] == '<=':
            p[0] = LessEqNode(p[1], p[3])
        elif p[2] == '=':
            p[0] = EqualNode(p[1], p[3])

    def p_op(self, p):
        '''
            op : op PLUS term
               | op MINUS term
               | term
        '''
        if len(p) == 2:
            p[0] = p[1]
        elif p[2] == '+':
            p[0] = PlusNode(p[1], p[3])
        elif p[2] == '-':
            p[0] = MinusNode(p[1], p[3])
 
    def p_term(self, p):
        '''
            term : term STAR base_call
                 | term DIV base_call
                 | base_call
        '''
        if len(p) == 2:
            p[0] = p[1]
        elif p[2] == '*':
            p[0] = StarNode(p[1], p[3])
        elif p[2] == '/': 
            p[0] = DivNode(p[1], p[3])

    def p_term_error(self, p):
        '''
            term : term STAR error
                 | term DIV error
        '''
        p[0] = ErrorNode()
      
    def p_base_call(self, p):
        '''
            base_call : factor ARROBA TYPE DOT func_call
                      | factor
        '''
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = BaseCallNode(p[1], p.slice[3], *p[5])

    def p_base_call_error(self, p):
        '''
            base_call : error ARROBA TYPE DOT func_call
                      | factor ARROBA error DOT func_call
        '''
        p[0] = ErrorNode()

    def p_factor1(self, p):
        '''
            factor : atom
                   | OPAR expr CPAR
        ''' 
        p[0] = p[1] if len(p) == 2 else p[2]
        
    def p_factor2(self, p):
        '''
            factor : factor DOT func_call
                   | NOT expr
                   | func_call
        '''
        if len(p) == 2:
            p[0] = StaticCallNode(*p[1])
        elif p[1] == 'not':
            p[0] = NotNode(p[2], p.slice[1])
        else:
            p[0] = CallNode(p[1], *p[3])

    def p_factor3(self, p):
        '''
            factor : ISVOID base_call
                   | NOX base_call
        '''
        if p[1] == 'isvoid':
            p[0] = IsVoidNode(p[2], p.slice[1])
        else:
            p[0] = BinaryNotNode(p[2], p.slice[1])
        
    def p_expr_let(self, p):
        '''
            factor : LET let_list IN expr
        '''
        p[0] = LetNode(p[2], p[4], p.slice[1])

    def p_expr_case(self, p):
        '''
            factor : CASE expr OF cases_list ESAC
        '''
        p[0] = CaseNode(p[2], p[4], p.slice[1])

    def p_expr_if(self, p):
        '''
            factor : IF expr THEN expr ELSE expr FI
        '''
        p[0] = ConditionalNode(p[2], p[4], p[6], p.slice[1])

    def p_expr_while(self, p):
        '''
            factor : WHILE expr LOOP expr POOL
        '''
        p[0] = WhileNode(p[2], p[4], p.slice[1])

    def p_atom_num(self, p):
        '''
            atom : NUM
        '''
        p[0] = ConstantNumNode(p.slice[1])
    
    def p_atom_id(self, p):
        '''
            atom : ID
        '''
        p[0] = VariableNode(p.slice[1])

    def p_atom_new(self, p):
        '''
            atom : NEW TYPE
        '''
        p[0] = InstantiateNode(p.slice[2])

    def p_atom_block(self, p):
        '''
            atom : OCUR block CCUR
        '''
        p[0] = BlockNode(p[2], p.slice[1])

    def p_atom_block_error(self, p):
        '''
            atom : error block CCUR
                 | OCUR error CCUR
                 | OCUR block error
        '''
        p[0] = ErrorNode()

    def p_atom_boolean(self, p):
        '''
            atom : TRUE
                 | FALSE
        '''
        p[0] = ConstantBoolNode(p.slice[1])

    def p_atom_string(self, p):
        '''
            atom : STRING
        '''
        p[0] = ConstantStrNode(p.slice[1])

    def p_block(self, p):
        '''
            block : expr SEMICOLON
                  | expr SEMICOLON block
        '''
        p[0] = [p[1]] if len(p) == 3 else [p[1]] + p[3]

    def p_block_error(self, p):
        '''
            block : error block
                  | error SEMICOLON
        '''
        p[0] = [ErrorNode()]

    def p_func_call(self, p):
        '''
            func_call : ID OPAR args CPAR
        '''
        p[0] = (p.slice[1], p[3])

    def p_func_call_error(self, p):
        '''
            func_call : ID OPAR error CPAR
                      | error OPAR args CPAR
        '''
        p[0] = (ErrorNode(), ErrorNode())

    def p_args(self, p):
        '''
            args : arg_list
                 | arg_list_empty
        '''
        p[0] = p[1]

    def p_arg_list(self, p):
        '''
            arg_list : expr  
                     | expr COMMA arg_list
        '''
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = [p[1]] + p[3]

    def p_arg_list_error(self, p):
        '''
            arg_list : error arg_list
        '''
        p[0] = [ErrorNode()]

    def p_arg_list_empty(self, p):
        '''
            arg_list_empty : epsilon
        '''
        p[0] = []

    def p_error(self, parse):
        if parse:
            error_text = SyntacticError.ERROR % parse.value
            line = self.find_line(parse)
            column = self.lexer.find_column(parse.lexer, parse)
            self.errors.append(SyntacticError(line, column, error_text))
            print(self.errors[0])
            exit(1)
        else:
            error_text = SyntacticError.ERROR % 'EOF'
            line = self.find_line(parse)
            column = self.lexer.find_column(self.lexer.lexer, self.lexer.lexer)
            self.errors.append(SyntacticError(line, column - 1, error_text))
    
    def find_line(self, parse):
        line = 0
        for token in self.lexer.list_tokens:
            if token.value == parse.value and token.lexpos == parse.lexpos:
                line = token.lineno
                break
        return line
