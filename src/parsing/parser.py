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

    def find_line(self, parse):
        line = 0
        for token in self.lexer.list_tokens:
            if token.value == parse.value and token.lexpos == parse.lexpos:
                line = token.lineno
                break
        return line

    # region GRAMMAR RULES

    def p_program(self, parse):
        '''
            program : class_list
        '''
        parse[0] = ProgramNode(parse[1])

    def p_epsilon(self, parse):
        '''
            epsilon :
        '''
        pass

    def p_class_list(self, parse):
        '''
            class_list : def_class class_list 
                       | def_class
        '''
        parse[0] = [parse[1]] if len(parse) == 2 else [parse[1]] + parse[2]

    def p_class_list_error(self, parse):
        '''
            class_list : error class_list
        '''
        parse[0] = [parse[1]] if len(parse) == 2 else [parse[1]] + parse[2]

    def p_def_class(self, parse):
        '''
            def_class : CLASS TYPE OCUR feature_list CCUR SEMICOLON
                      | CLASS TYPE INHERITS TYPE OCUR feature_list CCUR SEMICOLON
        '''
        if len(parse) == 7:
            parse[0] = ClassDeclarationNode(parse.slice[2], parse[4])
        else:
            parse[0] = ClassDeclarationNode(parse.slice[2], parse[6], parse.slice[4])

    def p_def_class_error(self, parse):
        '''
            def_class : CLASS error OCUR feature_list CCUR SEMICOLON 
                      | CLASS TYPE OCUR feature_list CCUR error   
                      | CLASS error INHERITS TYPE OCUR feature_list CCUR SEMICOLON
                      | CLASS error INHERITS error OCUR feature_list CCUR SEMICOLON
                      | CLASS TYPE INHERITS error OCUR feature_list CCUR SEMICOLON
                      | CLASS TYPE INHERITS TYPE OCUR feature_list CCUR error
        '''
        parse[0] = ErrorNode()

    def p_feature_list(self, parse):
        '''
            feature_list : epsilon
                         | def_attr SEMICOLON feature_list
                         | def_func SEMICOLON feature_list
        '''
        parse[0] = [] if len(parse) == 2 else [parse[1]] + parse[3]

    def p_feature_list_error(self, parse):
        '''
            feature_list : error feature_list
        '''
        parse[0] = [parse[1]] + parse[2]

    def p_def_attr(self, parse):
        '''
            def_attr : ID COLON TYPE
                     | ID COLON TYPE LARROW expr
        '''
        if len(parse) == 4:
            parse[0] = AttrDeclarationNode(parse.slice[1], parse.slice[3])
        else:
            parse[0] = AttrDeclarationNode(parse.slice[1], parse.slice[3], parse[5])

    def p_def_attr_error(self, parse):
        '''
            def_attr : error COLON TYPE
                     | ID COLON error
                     | error COLON TYPE LARROW expr
                     | ID COLON error LARROW expr
                     | ID COLON TYPE LARROW error
        '''
        parse[0] = ErrorNode()

    def p_def_func(self, parse):
        '''
            def_func : ID OPAR formals CPAR COLON TYPE OCUR expr CCUR
        '''
        parse[0] = FuncDeclarationNode(parse.slice[1], parse[3], parse.slice[6], parse[8])

    def p_def_func_error(self, parse):
        '''
            def_func : error OPAR formals CPAR COLON TYPE OCUR expr CCUR
                     | ID OPAR error CPAR COLON TYPE OCUR expr CCUR
                     | ID OPAR formals CPAR COLON error OCUR expr CCUR
                     | ID OPAR formals CPAR COLON TYPE OCUR error CCUR
        '''
        parse[0] = ErrorNode()

    def p_formals(self, parse):
        '''
            formals  : param_list
                     | param_list_empty
        '''
        parse[0] = parse[1]

    def p_param_list(self, parse):
        '''
            param_list : param
                       | param COMMA param_list
        '''
        parse[0] = [parse[1]] if len(parse) == 2 else [parse[1]] + parse[3]

    def p_param_list_empty(self, parse):
        '''
            param_list_empty : epsilon
        '''
        parse[0] = []

    def p_param(self, parse):
        '''
            param : ID COLON TYPE
        '''
        parse[0] = (parse.slice[1], parse.slice[3])

    def p_let_list(self, parse):
        '''
            let_list : let_assign
                     | let_assign COMMA let_list
        '''
        parse[0] = [parse[1]] if len(parse) == 2 else [parse[1]] + parse[3]

    def p_let_assign(self, parse):
        '''
            let_assign : param LARROW expr
                       | param
        '''
        if len(parse) == 2:
            parse[0] = VarDeclarationNode(parse[1][0], parse[1][1])
        else:
            parse[0] = VarDeclarationNode(parse[1][0], parse[1][1], parse[3])

    def p_cases_list(self, parse):
        '''
            cases_list : casep SEMICOLON
                       | casep SEMICOLON cases_list
        '''
        parse[0] = [parse[1]] if len(parse) == 3 else [parse[1]] + parse[3]

    def p_cases_list_error(self, parse):
        '''
            cases_list : error cases_list
                       | error SEMICOLON
        '''
        parse[0] = [ErrorNode()]

    def p_case(self, parse):
        '''
            casep : ID COLON TYPE RARROW expr
        '''
        parse[0] = OptionNode(parse.slice[1], parse.slice[3], parse[5])

    def p_expr(self, parse):
        '''
            expr : ID LARROW expr
                 | comp
        '''
        if len(parse) == 4:
            parse[0] = AssignNode(parse.slice[1], parse[3])
        else:
            parse[0] = parse[1]

    def p_comp(self, parse):
        '''
            comp : comp LESS op
                 | comp LESSEQ op
                 | comp EQUAL op
                 | op
        '''
        if len(parse) == 2:
            parse[0] = parse[1]
        elif parse[2] == '<':
            parse[0] = LessNode(parse[1], parse[3])
        elif parse[2] == '<=':
            parse[0] = LessEqNode(parse[1], parse[3])
        elif parse[2] == '=':
            parse[0] = EqualNode(parse[1], parse[3])

    def p_op(self, parse):
        '''
            op : op PLUS term
               | op MINUS term
               | term
        '''
        if len(parse) == 2:
            parse[0] = parse[1]
        elif parse[2] == '+':
            parse[0] = PlusNode(parse[1], parse[3])
        elif parse[2] == '-':
            parse[0] = MinusNode(parse[1], parse[3])
 
    def p_term(self, parse):
        '''
            term : term STAR base_call
                 | term DIV base_call
                 | base_call
        '''
        if len(parse) == 2:
            parse[0] = parse[1]
        elif parse[2] == '*':
            parse[0] = StarNode(parse[1], parse[3])
        elif parse[2] == '/': 
            parse[0] = DivNode(parse[1], parse[3])

    def p_term_error(self, parse):
        '''
            term : term STAR error
                 | term DIV error
        '''
        parse[0] = ErrorNode()
      
    def p_base_call(self, parse):
        '''
            base_call : factor ARROBA TYPE DOT func_call
                      | factor
        '''
        if len(parse) == 2:
            parse[0] = parse[1]
        else:
            parse[0] = BaseCallNode(parse[1], parse.slice[3], *parse[5])

    def p_base_call_error(self, parse):
        '''
            base_call : error ARROBA TYPE DOT func_call
                      | factor ARROBA error DOT func_call
        '''
        parse[0] = ErrorNode()

    def p_factor1(self, parse):
        '''
            factor : atom
                   | OPAR expr CPAR
        ''' 
        parse[0] = parse[1] if len(parse) == 2 else parse[2]
        
    def p_factor2(self, parse):
        '''
            factor : factor DOT func_call
                   | NOT expr
                   | func_call
        '''
        if len(parse) == 2:
            parse[0] = StaticCallNode(*parse[1])
        elif parse[1] == 'not':
            parse[0] = NotNode(parse[2], parse.slice[1])
        else:
            parse[0] = CallNode(parse[1], *parse[3])

    def p_factor3(self, parse):
        '''
            factor : ISVOID base_call
                   | NOX base_call
        '''
        if parse[1] == 'isvoid':
            parse[0] = IsVoidNode(parse[2], parse.slice[1])
        else:
            parse[0] = BinaryNotNode(parse[2], parse.slice[1])
        
    def p_expr_let(self, parse):
        '''
            factor : LET let_list IN expr
        '''
        parse[0] = LetNode(parse[2], parse[4], parse.slice[1])

    def p_expr_case(self, parse):
        '''
            factor : CASE expr OF cases_list ESAC
        '''
        parse[0] = CaseNode(parse[2], parse[4], parse.slice[1])

    def p_expr_if(self, parse):
        '''
            factor : IF expr THEN expr ELSE expr FI
        '''
        parse[0] = ConditionalNode(parse[2], parse[4], parse[6], parse.slice[1])

    def p_expr_while(self, parse):
        '''
            factor : WHILE expr LOOP expr POOL
        '''
        parse[0] = WhileNode(parse[2], parse[4], parse.slice[1])

    def p_atom_num(self, parse):
        '''
            atom : NUM
        '''
        parse[0] = ConstantNumNode(parse.slice[1])
    
    def p_atom_id(self, parse):
        '''
            atom : ID
        '''
        parse[0] = VariableNode(parse.slice[1])

    def p_atom_new(self, parse):
        '''
            atom : NEW TYPE
        '''
        parse[0] = InstantiateNode(parse.slice[2])

    def p_atom_block(self, parse):
        '''
            atom : OCUR block CCUR
        '''
        parse[0] = BlockNode(parse[2], parse.slice[1])

    def p_atom_block_error(self, parse):
        '''
            atom : error block CCUR
                 | OCUR error CCUR
                 | OCUR block error
        '''
        parse[0] = ErrorNode()

    def p_atom_boolean(self, parse):
        '''
            atom : TRUE
                 | FALSE
        '''
        parse[0] = ConstantBoolNode(parse.slice[1])

    def p_atom_string(self, parse):
        '''
            atom : STRING
        '''
        parse[0] = ConstantStrNode(parse.slice[1])

    def p_block(self, parse):
        '''
            block : expr SEMICOLON
                  | expr SEMICOLON block
        '''
        parse[0] = [parse[1]] if len(parse) == 3 else [parse[1]] + parse[3]

    def p_block_error(self, parse):
        '''
            block : error block
                  | error SEMICOLON
        '''
        parse[0] = [ErrorNode()]

    def p_func_call(self, parse):
        '''
            func_call : ID OPAR args CPAR
        '''
        parse[0] = (parse.slice[1], parse[3])

    def p_func_call_error(self, parse):
        '''
            func_call : ID OPAR error CPAR
                      | error OPAR args CPAR
        '''
        parse[0] = (ErrorNode(), ErrorNode())

    def p_args(self, parse):
        '''
            args : arg_list
                 | arg_list_empty
        '''
        parse[0] = parse[1]

    def p_arg_list(self, parse):
        '''
            arg_list : expr  
                     | expr COMMA arg_list
        '''
        if len(parse) == 2:
            parse[0] = [parse[1]]
        else:
            parse[0] = [parse[1]] + parse[3]

    def p_arg_list_error(self, parse):
        '''
            arg_list : error arg_list
        '''
        parse[0] = [ErrorNode()]

    def p_arg_list_empty(self, parse):
        '''
            arg_list_empty : epsilon
        '''
        parse[0] = []

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
    
    # endregion
