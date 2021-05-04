import ply.yacc as yacc

from cmp.lexer import Lexer
from cmp.ast import *
from cmp.errors import SyntacticError

class Parser(object):

    def __init__(self, tokens, errors=[]):
        object.__init__(self)
        self.tokens = tokens
        self.errors = errors
        self.build()
    
    @property
    def precedence(self): 
        return (
            ('right', 'LDASH', 'IN'),
            ('left', 'NOT'),
            ('left', 'LEQUAL', 'LESS', 'EQUAL'),
            ('left', 'PLUS', 'MINUS'),
            ('left', 'STAR', 'DIVIDE'),
            ('left', 'ISVOID'),
            ('left', 'TILDE'),
            ('left', 'AT'),
            ('left', 'DOT'),
        )
    
    def p_programm(self, p):
        '''program : classlist'''
        p[0] = ProgramNode(p[1])

    def p_classlist(self, p):
        '''classlist : defclass SEMICOLON
                     | defclass SEMICOLON classlist'''
        try:
            p[0] = [p[1]] + p[3]
        except IndexError:
            p[0] = [p[1]]
    
    def p_defclass(self, p):
        '''defclass : CLASS TYPE LCURLY featurelist RCURLY
                    | CLASS TYPE INHERITS TYPE LCURLY featurelist RCURLY'''
        try:
            p[0] = ClassNode(p[2], p[6], p[4])
        except IndexError:
            p[0] = ClassNode(p[2], p[4])

    def p_featurelist(self, p):
        '''featurelist : defmethods SEMICOLON featurelist
                       | defattributes SEMICOLON featurelist
                       | '''
        try:
            p[0] = [p[1]] + p[3]
        except IndexError:
            p[0] = []

    def p_defattributes(self, p):
        '''defattributes : ID COLON TYPE 
                         | ID COLON TYPE LDASH expression'''
        try:
            p[0] = AttributeNode(p[1], p[3], p[5])
        except IndexError:
            p[0] = AttributeNode(p[1], p[3])

    def p_defmethods(self, p):
        '''defmethods : ID LPAREN parameterslist RPAREN COLON TYPE LCURLY expression RCURLY'''
        p[0] = MethodNode(p[1], p[3], p[6], p[8])

    def p_parameterslist(self, p):
        '''parameterslist : parameters
                          | '''
        try:
            p[0] = p[1]
        except IndexError:
            p[0] = None

    def p_parameters(self, p):
        '''parameters : ID COLON TYPE
                      | ID COLON TYPE COMMA parameters'''
        try:
            p[0] = [(p[1], p[3])] + p[5]
        except IndexError:
            p[0] = [(p[1], p[3])]
   
    def p_expression_assignment(self, p):
        ''' expression : ID LDASH expression'''
        p[0] = AssignmentNode(p[1], p[3])
    
    def p_expression_dispatch(self, p):
        '''expression : ID LPAREN argumentslist RPAREN
                      | expression DOT ID LPAREN argumentslist RPAREN
                      | expression AT TYPE DOT ID LPAREN argumentslist RPAREN'''
        try:
            p[0] = DispatchNode(p[5], p[7], p[1], p[3])
        except IndexError:
            try:
                p[0] = DispatchNode(p[3], p[5], p[1])
            except IndexError:
                p[0] = DispatchNode(p[1], p[3])

    def p_argumentslist(self, p):
        '''argumentslist : argument
                         | '''
        try:
            p[0] = p[1]
        except IndexError:
            p[0] = None

    def p_argument(self, p):
        '''argument : expression
                    | expression COMMA argument'''
        try:
            p[0] = [p[1]] + p[3]
        except IndexError:
            p[0] = [p[1]]

    def p_expression_conditionals(self, p):
        '''expression : IF expression THEN expression ELSE expression FI'''
        p[0] = ConditionalNode(p[2], p[4], p[6])

    def p_expression_loops(self, p):
        '''expression : WHILE expression LOOP expression POOL'''
        p[0] = LoopsNode(p[2], p[4])

    def p_expression_blocks(self, p):
        '''expression : LCURLY expressionlist RCURLY'''
        p[0] = BlockNode(p[2])

    def p_expressionlist(self, p):
        '''expressionlist : expression SEMICOLON
                          | expression SEMICOLON expressionlist'''
        try:
            p[0] = [p[1]] + p[3]
        except IndexError:
            p[0] = [p[1]]

    def p_expression_let(self, p):
        '''expression : LET variableslist IN expression'''
        p[0] = LetNode(p[2], p[4])

    def p_variableslist(self, p):
        '''variableslist : variable
                         | variable COMMA variableslist'''
        try:
            p[0] = [p[1]] + p[3]
        except IndexError:
            p[0] = [p[1]]

    def p_variable(self, p):
        '''variable : ID COLON TYPE
                    | ID COLON TYPE LDASH expression'''
        try:
            p[0] = [(p[1], p[3], p[5])]
        except IndexError:
            p[0] = [(p[1], p[3], None)]

    def p_expression_case(self, p):
        '''expression : CASE expression OF typetestlist ESAC'''
        p[0] = CaseNode(p[2], p[4])

    def p_typetestlist(self, p):
        '''typetestlist : ID COLON TYPE GEQUAL expression SEMICOLON
                        | ID COLON TYPE GEQUAL expression SEMICOLON typetestlist'''
        try:
            p[0] = [(p[1], p[3], p[5])] + p[7]
        except IndexError:
            p[0] = [(p[1], p[3], p[5])]

    def p_expression_new(self, p):
        '''expression : NEW TYPE'''
        p[0] = NewNode(p[2])

    def p_expression_isvoid(self, p):
        '''expression : ISVOID expression'''
        p[0] = IsvoidNode(p[2])

    def p_expression_plus(self, p):
        '''expression : expression PLUS expression'''
        p[0] = PlusNode(p[1], p[3])

    def p_expression_minus(self, p):
        '''expression : expression MINUS expression'''
        p[0] = MinusNode(p[1], p[3])
    
    def p_expression_star(self, p):
        '''expression : expression STAR expression'''
        p[0] = StarNode(p[1], p[3])

    def p_expression_divide(self, p):
        '''expression : expression DIVIDE expression'''
        p[0] = DivideNode(p[1], p[3])

    def p_expression_less(self, p):
        '''expression : expression LESS expression'''
        p[0] = LessNode(p[1], p[3])

    def p_expression_lequal(self, p):
        '''expression : expression LEQUAL expression'''
        p[0] = LequalNode(p[1], p[3])

    def p_expression_equal(self, p):
        '''expression : expression EQUAL expression'''
        p[0] = EqualNode(p[1], p[3])

    def p_expression_complement(self, p):
        '''expression : TILDE expression'''
        p[0] = ComplementNode(p[2])

    def p_expression_not(self, p):
        '''expression : NOT expression'''
        p[0] = NegationNode(p[2])

    def p_expression_paren(self, p):
        '''expression : LPAREN expression RPAREN'''
        p[0] = p[2]

    def p_expression_atomic_id(self, p):
        '''expression : ID'''
        
        p[0] = IdentifierNode(p[1])
    
    def p_expression_atomic_int(self, p):
        '''expression : INT'''
        
        p[0] = IntegerNode(p[1])
    
    def p_expression_atomic_string(self, p):
        '''expression : STRING'''
        
        p[0] = StringNode(p[1])
    
    def p_expression_atomic_bool(self, p):
        '''expression : BOOL'''
        
        p[0] = BoolNode(p[1])
    
    def p_error(self, p):
        if not p:
            self.errors.append(SyntacticError.text_eof())
        else:
            p = p.value

            self.errors.append(SyntacticError.text(p.line, p.column, p.value))         

    def build(self, **kwargs):
        self.parser = yacc.yacc(module=self, **kwargs)

    def __call__(self, data, lexer):
        return self.parser.parse(input=data, lexer=Lexer().lexer)
