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
