import ply.yacc as yacc
import Parser.ast as AST
from Parser.errors_types import *

class COOL_Parser:
    '''
    CoolParser class.
    '''
    def __init__(self, cool_lexer):
        self.cool_lexer = cool_lexer
        self.tokens = self.cool_lexer.tokens
        self.parser = None
        self.error_list = []
        self.errors = False
    
    def run(self, code):
        self.parser = yacc.yacc(module = self)
        ast = self.parser.parse(input = code, lexer = self.cool_lexer.lexer)
        self.errors = self.errors or self.cool_lexer.errors
        return ast

    # ################################ PRECEDENCE RULES ################################

    precedence = (
        ('right', 'ASSIGN'),
        ('right', 'NOT'),
        ('nonassoc', 'LTEQ', 'LT', 'EQ'),
        ('left', 'PLUS', 'MINUS'),
        ('left', 'MULTIPLY', 'DIVIDE'),
        ('right', 'ISVOID'),
        ('right', 'INT_COMP'),
        ('left', 'AT'),
        ('left', 'DOT')
    )

    # ################### START OF FORMAL GRAMMAR RULES DECLARATION ####################

    def p_program(self, parse):
        'program : class_list'
        parse[0] = AST.Program(classes=parse[1])

    def p_class_list(self, parse):
        '''class_list : class SEMICOLON class_list
                      | class SEMICOLON'''
        if len(parse) == 4:
            parse[0] = [parse[1]] + parse[3]
        else:
            parse[0] = [parse[1]]

    def p_class(self, parse):
        'class : CLASS TYPE LBRACE features_list_opt RBRACE'
        parse[0] = AST.Class(name=parse[2], parent="Object", features=parse[4])
        _l = parse.lineno(2)
        _p = parse.lexpos(2) - self.cool_lexer.linelastpos[_l-1]
        parse[0].pos(_l, _p)

    def p_class_inherits(self, parse):
        'class : CLASS TYPE INHERITS TYPE LBRACE features_list_opt RBRACE'
        parse[0] = AST.Class(name=parse[2], parent=parse[4], features=parse[6])
        _l = parse.lineno(2)
        _p = parse.lexpos(2) - self.cool_lexer.linelastpos[_l-1]
        parse[0].pos(_l, _p)

    def p_feature_list_opt(self, parse):
        '''features_list_opt : features_list
                             | empty'''
        parse[0] = list() if parse.slice[1].type == "empty" else parse[1]

    def p_feature_list(self, parse):
        '''features_list : feature SEMICOLON features_list
                         | empty'''
        parse[0] = list() if parse.slice[1].type == "empty" else [parse[1]] + parse[3]

    def p_feature_method(self, parse):
        'feature : ID LPAREN formal_params_list RPAREN COLON TYPE LBRACE expression RBRACE'
        parse[0] = AST.ClassMethod(name=parse[1], formal_params=parse[3], return_type=parse[6], body=parse[8])
        _l = parse.lineno(1)
        _p = parse.lexpos(1) - self.cool_lexer.linelastpos[_l-1]
        parse[0].pos(_l, _p)

    def p_feature_method_no_formals(self, parse):
        'feature : ID LPAREN RPAREN COLON TYPE LBRACE expression RBRACE'
        parse[0] = AST.ClassMethod(name=parse[1], formal_params=tuple(), return_type=parse[5], body=parse[7])
        _l = parse.lineno(1)
        _p = parse.lexpos(1) - self.cool_lexer.linelastpos[_l-1]
        parse[0].pos(_l, _p)

    def p_feature_attr_initialized(self, parse):
        'feature : ID COLON TYPE ASSIGN expression'
        parse[0] = AST.ClassAttribute(name=parse[1], attr_type=parse[3], init_expr=parse[5])
        _l = parse.lineno(1)
        _p = parse.lexpos(1) - self.cool_lexer.linelastpos[_l-1]
        parse[0].pos(_l, _p)

    def p_feature_attr(self, parse):
        'feature : ID COLON TYPE'
        parse[0] = AST.ClassAttribute(name=parse[1], attr_type=parse[3], init_expr=None)
        _l = parse.lineno(1)
        _p = parse.lexpos(1) - self.cool_lexer.linelastpos[_l-1]
        parse[0].pos(_l, _p)

    def p_formal_list_many(self, parse):
        '''formal_params_list  : formal_param COMMA formal_params_list
                               | formal_param'''
        if len(parse) == 4:
            parse[0] = [parse[1]] + parse[3]
        else:
            parse[0] = [parse[1]]

    def p_formal(self, parse):
        'formal_param : ID COLON TYPE'
        parse[0] = AST.FormalParameter(name=parse[1], param_type=parse[3])
        _l = parse.lineno(1)
        _p = parse.lexpos(1) - self.cool_lexer.linelastpos[_l-1]
        parse[0].pos(_l, _p)

    def p_expression_object_identifier(self, parse):
        'expression : ID'
        parse[0] = AST.Object(name=parse[1])
        _l = parse.lineno(1)
        _p = parse.lexpos(1) - self.cool_lexer.linelastpos[_l-1]
        parse[0].pos(_l, _p)

    def p_expression_integer_constant(self, parse):
        'expression : INTEGER'
        parse[0] = AST.Integer(content=parse[1])
        _l = parse.lineno(1)
        _p = parse.lexpos(1) - self.cool_lexer.linelastpos[_l-1]
        parse[0].pos(_l, _p)

    def p_expression_boolean_constant(self, parse):
        'expression : BOOLEAN'
        parse[0] = AST.Boolean(content=parse[1])
        _l = parse.lineno(1)
        _p = parse.lexpos(1) - self.cool_lexer.linelastpos[_l-1]
        parse[0].pos(_l, _p)

    def p_expression_string_constant(self, parse):
        'expression : STRING'
        parse[0] = AST.String(content=parse[1])
        _l = parse.lineno(1)
        _p = parse.lexpos(1) - self.cool_lexer.linelastpos[_l-1] - len(parse[0].content) - 1
        parse[0].pos(_l, _p)

    def p_expression_block(self, parse):
        'expression : LBRACE block_list RBRACE'
        parse[0] = AST.Block(expr_list=parse[2])
        _l = parse.lineno(1)
        _p = parse.lexpos(1) - self.cool_lexer.linelastpos[_l-1]
        parse[0].pos(_l, _p)

    def p_block_list(self, parse):
        '''block_list : expression SEMICOLON block_list
                      | expression SEMICOLON'''
        if len(parse) == 4:
            parse[0] = [parse[1]] + parse[3]
        else:
            parse[0] = [parse[1]]

    def p_expression_assignment(self, parse):
        'expression : ID ASSIGN expression'
        parse[0] = AST.Assignment(AST.Object(name=parse[1]), expr=parse[3])
        _l = parse.lineno(2)
        _p = parse.lexpos(2) - self.cool_lexer.linelastpos[_l-1]
        parse[0].pos(_l, _p)

    # ######################### METHODS DISPATCH ######################################

    def p_expression_dispatch(self, parse):
        'expression : expression DOT ID LPAREN arguments_list_opt RPAREN'
        parse[0] = AST.DynamicDispatch(instance=parse[1], method=parse[3], arguments=parse[5])
        _l = parse.lineno(3)
        _p = parse.lexpos(3) - self.cool_lexer.linelastpos[_l-1]
        parse[0].pos(_l, _p)

    def p_arguments_list_opt(self, parse):
        '''arguments_list_opt : arguments_list
                              | empty'''
        parse[0] = list() if parse.slice[1].type == "empty" else parse[1]

    def p_arguments_list(self, parse):
        '''arguments_list : expression COMMA arguments_list
                          | expression'''
        if len(parse) == 4:
            parse[0] = [parse[1]] + parse[3]
        else:
            parse[0] = [parse[1]]

    def p_expression_static_dispatch(self, parse):
        'expression : expression AT TYPE DOT ID LPAREN arguments_list_opt RPAREN'
        parse[0] = AST.StaticDispatch(instance=parse[1], dispatch_type=parse[3], method=parse[5], arguments=parse[7])
        _l = parse.lineno(5)
        _p = parse.lexpos(5) - self.cool_lexer.linelastpos[_l-1]
        parse[0].pos(_l, _p)

    def p_expression_self_dispatch(self, parse):
        'expression : ID LPAREN arguments_list_opt RPAREN'
        parse[0] = AST.DynamicDispatch(instance=AST.Self(), method=parse[1], arguments=parse[3])
        _l = parse.lineno(1)
        _p = parse.lexpos(1) - self.cool_lexer.linelastpos[_l-1]
        parse[0].pos(_l, _p)

    # ######################### PARENTHESIZED, MATH & COMPARISONS #####################

    def p_expression_math_operations(self, parse):
        '''expression : expression PLUS expression
                      | expression MINUS expression
                      | expression MULTIPLY expression
                      | expression DIVIDE expression'''
        if parse[2] == '+':
            parse[0] = AST.Addition(first=parse[1], second=parse[3])
        elif parse[2] == '-':
            parse[0] = AST.Subtraction(first=parse[1], second=parse[3])
        elif parse[2] == '*':
            parse[0] = AST.Multiplication(first=parse[1], second=parse[3])
        elif parse[2] == '/':
            parse[0] = AST.Division(first=parse[1], second=parse[3])
        _l = parse.lineno(2)
        _p = parse.lexpos(2) - self.cool_lexer.linelastpos[_l-1]
        parse[0].pos(_l, _p)

    def p_expression_math_comparisons(self, parse):
        '''expression : expression LT expression
                      | expression LTEQ expression
                      | expression EQ expression'''
        if parse[2] == '<':
            parse[0] = AST.LessThan(first=parse[1], second=parse[3])
        elif parse[2] == '<=':
            parse[0] = AST.LessThanOrEqual(first=parse[1], second=parse[3])
        elif parse[2] == '=':
            parse[0] = AST.Equal(first=parse[1], second=parse[3])
        _l = parse.lineno(2)
        _p = parse.lexpos(2) - self.cool_lexer.linelastpos[_l-1]
        parse[0].pos(_l, _p)

    def p_expression_with_parenthesis(self, parse):
        'expression : LPAREN expression RPAREN'
        parse[0] = parse[2]

    # ######################### CONTROL FLOW EXPRESSIONS ##############################

    def p_expression_if_conditional(self, parse):
        'expression : IF expression THEN expression ELSE expression FI'
        parse[0] = AST.If(predicate=parse[2], then_body=parse[4], else_body=parse[6])
        _l = parse.lineno(1)
        _p = parse.lexpos(1) - self.cool_lexer.linelastpos[_l-1]
        parse[0].pos(_l, _p)

    def p_expression_while_loop(self, parse):
        'expression : WHILE expression LOOP expression POOL'
        parse[0] = AST.WhileLoop(predicate=parse[2], body=parse[4])
        _l = parse.lineno(1)
        _p = parse.lexpos(1) - self.cool_lexer.linelastpos[_l-1]
        parse[0].pos(_l, _p)

    # ######################### LET EXPRESSIONS ########################################

    def p_expression_let(self, parse):
        'expression : let_expression'
        parse[0] = parse[1]

    def p_expression_let_list(self, parse):
        'let_expression : LET formal_list IN expression'
        parse[0] = AST.Let(declarations=parse[2], body=parse[4])
        _l = parse.lineno(1)
        _p = parse.lexpos(1) - self.cool_lexer.linelastpos[_l-1]
        parse[0].pos(_l, _p)

    def p_formal_list(self, parse):
        '''formal_list : formal_list COMMA formal
                       | formal'''
        if len(parse) == 4:
            parse[0] = parse[1] + [parse[3]]
        else:
            parse[0] = [parse[1]]

    def p_formal_let_simpleparam(self, parse):
        'formal : ID COLON TYPE'
        parse[0] = AST.Formal(name=parse[1], param_type=parse[3], init_expr=None)
        _l = parse.lineno(1)
        _p = parse.lexpos(1) - self.cool_lexer.linelastpos[_l-1]
        parse[0].pos(_l, _p)

    def p_formal_let_param(self, parse):
        'formal : ID COLON TYPE ASSIGN expression'
        parse[0] = AST.Formal(name=parse[1], param_type=parse[3], init_expr=parse[5])
        _l = parse.lineno(1)
        _p = parse.lexpos(1) - self.cool_lexer.linelastpos[_l-1]
        parse[0].pos(_l, _p)

    # ######################### CASE EXPRESSION ########################################

    def p_expression_case(self, parse):
        'expression : CASE expression OF actions_list ESAC'
        parse[0] = AST.Case(expr=parse[2], actions=parse[4])
        _l = parse.lineno(1)
        _p = parse.lexpos(1) - self.cool_lexer.linelastpos[_l-1]
        parse[0].pos(_l, _p)

    def p_actions_list(self, parse):
        '''actions_list : action actions_list
                        | action'''
        if len(parse) == 3:
            parse[0] = [parse[1]] + parse[2]
        else:
            parse[0] = [parse[1]]

    def p_action_expr(self, parse):
        'action : ID COLON TYPE ARROW expression SEMICOLON'
        parse[0] = AST.Action(parse[1], parse[3], parse[5])
        _l = parse.lineno(3)
        _p = parse.lexpos(3) - self.cool_lexer.linelastpos[_l-1]
        parse[0].pos(_l, _p)

    # ######################### UNARY OPERATIONS #######################################

    def p_expression_new(self, parse):
        'expression : NEW TYPE'
        parse[0] = AST.NewObject(parse[2])
        _l = parse.lineno(2)
        _p = parse.lexpos(2) - self.cool_lexer.linelastpos[_l-1]
        parse[0].pos(_l, _p)

    def p_expression_isvoid(self, parse):
        'expression : ISVOID expression'
        parse[0] = AST.IsVoid(parse[2])
        _l = parse.lineno(1)
        _p = parse.lexpos(1) - self.cool_lexer.linelastpos[_l-1]
        parse[0].pos(_l, _p)

    def p_expression_integer_complement(self, parse):
        'expression : INT_COMP expression'
        parse[0] = AST.IntegerComplement(parse[2])
        _l = parse.lineno(1)
        _p = parse.lexpos(1) - self.cool_lexer.linelastpos[_l-1]
        parse[0].pos(_l, _p)

    def p_expression_boolean_complement(self, parse):
        'expression : NOT expression'
        parse[0] = AST.BooleanComplement(parse[2])
        _l = parse.lineno(1)
        _p = parse.lexpos(1) - self.cool_lexer.linelastpos[_l-1]
        parse[0].pos(_l, _p)

    # ######################### THE EMPTY PRODUCTION ###################################

    def p_empty(self, parse):
        'empty :'
        parse[0] = None

    # ######################### PARSE ERROR HANDLER ####################################

    def p_error(self, parse):
        """
        Error rule for Syntax Errors handling and reporting.
        """
        if parse is None:
            self.error_list.append(f'(0,0) - {PREOF}')
        else:
            self.error_list.append(f'({parse.lineno}, {parse.lexpos - self.cool_lexer.linelastpos[parse.lineno-1]}) - {PRSTX1} "{parse.value}"')
            self.parser.errok()
        self.errors = True