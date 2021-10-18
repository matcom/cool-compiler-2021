from ast import *
import ply.yacc as yacc


class CoolParser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.parser = yacc.yacc(start='program', module=self)

    def parse(self, program):
        pass

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
        '''def_class : CLASS TYPE LPAREN feature_list RPAREN 
                     | CLASS TYPE INHERITS TYPE LPAREN feature_list RPAREN'''
        if len(p) == 8:
            p[0] = ClassDeclarationNode(p[2], p[6], p[4])
        else:
            p[0] = ClassDeclarationNode(p[2], p[4])

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

    def p_def_func(self, p):
        '''def_func : ID LPAREN params RPAREN COLON TYPE LBRACE expr RBRACE'''
        p[0] = FuncDeclarationNode(p[1], p[3], p[6], p[8])

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

    def p_args(self, p):
        '''args : arg_list 
                | arg_list_empty'''
        p[0] = p[1]

    def p_arg_list(self, p):
        '''arg_list : expr
                    | expr COMMA arg_list'''
        p[0] = [p[1]] if len(p) == 2 else [p[1]] + p[3]

    def p_arg_list_empty(p):
        '''arg_list_empty : epsilon'''
        p[0] = []

    def p_atom_int(self, p):
        '''atom : INT'''
        p[0] = IntNode(int(p[1]))

    def p_atom_id(self, p):
        '''atom : ID'''
        p[0] = VarNode(p[1])

    def p_atom_bool(self, p):
        '''atom : BOOL'''
        p[0] = BoolNode(p[1])

    def p_atom_string(self, p):
        '''atom : STRING'''
        p[0] = StringNode(p[1])

    def p_atom_new(self, p):
        '''atom : NEW TYPE'''
        p[0] = NewNode(p[2])
    
    def p_atom_block(self, p):
        '''atom : block'''
        p[0] = p[1]
    
    def p_block(self, p):
        '''block : LBRACE block_list RBRACE'''
        p[0] = p[2]
    
    def p_block_list(self, p):
        ''' block_list : expr SEMICOLON
                       | expr SEMICOLON block_list'''
        p[0] = BlockNode([p[1]]) if len(p) == 3 else BlockNode([p[1]] + p[3].exprs)

    def p_error(self, p):
        pass 

