from cool.lexer.lexer import Lexer
from cool.utils.LexerTokens.Tokens import tokens
import ply.yacc as yacc
from cool.Parser.AstNodes import *
from cool.utils.Errors.parser_errors import *

class Parser():
    def __init__(self, lexer:Lexer = None) -> None:
            self.lexer = Lexer() if not lexer else lexer

            self.tokens = tokens
            self.errors = []
            self.parser = yacc.yacc(start='program',
                                module=self,
                                optimize=1,
                                debug=False,
                                write_tables=True,
                                debuglog=None,
                                errorlog=None, )

    def parse(self, program, debug=False):
        self.found_error = False
        return self.parser.parse(program, self.lexer.lexer)

    def p_empty(self,p):
        'empty :'
        pass

    def p_program(self,p):
        'program : class_list'
        p[0]=ProgramNode(p[1])

    def p_class_list(self,p):
        '''class_list : def_class SEMI class_list
                      | def_class SEMI'''
        p[0]= [p[1]]+p[3] if len(p)==4 else [p[1]]

    def p_def_class(self,p):
        '''def_class : class TYPE OCUR feature_list CCUR
                     | class TYPE inherits TYPE OCUR feature_list CCUR'''
        col = p.slice[2].column
        line = p.lineno(1)
        if len(p) == 6:
            p[0] = ClassDeclarationNode(p[2], p[4],'Object', line, col)
        else: 
            col = p.slice[4].column
            p[0] = ClassDeclarationNode(p[2], p[6], p[4], line, col)


    def p_feature_list(self,p):
        '''feature_list : def_attr SEMI feature_list
                        | def_func SEMI feature_list
                        | empty'''
        p[0] = [p[1]] + p[3] if len(p) == 4 else []


    def p_def_attr(self,p):
        '''def_attr : ID COLON TYPE
                    | ID COLON TYPE LARROW expr'''
        col = p.slice[3].column
        line = p.lineno(1)
        p[0] = AttrDeclarationNode(p[1], p[3], None, line, col) if len(p)==4\
                else AttrDeclarationNode(p[1],p[3],p[5], line, col)


    def p_def_func(self,p):
        '''def_func : ID OPAR param_list_call CPAR COLON TYPE OCUR expr CCUR'''
        line = p.lineno(1)
        col = p.slice[1].column
        p[0] = FuncDeclarationNode(p[1], p[3], p[6], p[8], line, col) 

    def p_param_list_call(self,p):
        '''param_list_call : param_list
                           | param_list_empty'''
        p[0] = p[1]

    def p_param_list(self,p):
        '''param_list : param
                      | param COMMA param_list'''
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = [p[1]] + p[3]

    def p_param_list_empty(self,p):
        '''param_list_empty : empty'''
        p[0] = []
            

    def p_param(self,p):
        '''param : ID COLON TYPE'''
        col = p.slice[1].column
        line = p.lineno(1)
        p[0] = ParamDeclarationNode(p[1],p[3],line,col) 

    def p_expr_list(self,p):
        '''expr_list : expr SEMI expr_list
                     | expr SEMI'''
        p[0] = [p[1]] + p[3] if len(p) == 4\
                else [p[1]]

    def p_declar_list(self,p):
        '''declar_list : declar
                       | declar COMMA declar_list'''
        p[0] = [p[1]] if len(p) == 2 else [p[1]]+p[3]

    def p_declar(self,p):
        '''declar : ID COLON TYPE
                  | ID COLON TYPE LARROW expr'''
        col = p.slice[3].column
        line = p.lineno(1)
        p[0] = LetDeclarationNode(p[1], p[3], None, line, col) if len(p) == 4\
                else LetDeclarationNode(p[1],p[3],p[5], line, col)

    def p_assign_list(self,p):
        '''assign_list : case_assign
                       | case_assign assign_list'''
        p[0] = [p[1]] if len(p) == 2 else [p[1]]+p[2]


    def p_case_assign(self,p):
        '''case_assign : ID COLON TYPE RARROW expr SEMI'''
        col = p.slice[3].column
        line = p.lineno(1)
        p[0] = VarDeclarationNode(p[1],p[3],p[5], line, col)

    def p_expr_boolean(self,p):
        '''expr : boolean'''
        p[0] = p[1]
    
    def p_boolean(self,p):
        '''boolean : not comparison
                   | comparison'''
        line = p.lineno(1)
        p[0] = NotNode(p[2], line, p.slice[1].column) if len(p) == 3 else p[1]

    def p_comparison(self,p):
        '''comparison : comparison EQUAL boolean
                      | comparison LESS boolean
                      | comparison LESSEQ boolean 
                      | arith'''
        if len(p) ==4 and p[2] == '=':
            p[0] = EqualNode(p.slice[2], p[1],p[3], p.lineno(2), p.slice[2].column)
        elif len(p) ==4 and p[2] == '<':
            p[0] = LessNode(p.slice[2], p[1],p[3], p.lineno(2), p.slice[2].column)
        elif len(p) ==4 and p[2] == '<=':
            p[0] = LessEqual(p.slice[2], p[1],p[3], p.lineno(2), p.slice[2].column)
        else: p[0] = p[1]

    def p_arith(self,p):
        '''arith : arith PLUS term
                 | arith MINUS term
                 | term'''
        if len(p) ==4 and p[2] == '+':
            p[0] = PlusNode(p.slice[2], p[1], p[3], p.lineno(2), p.slice[2].column)
        elif len(p) ==4 and p[2] == '-':
            p[0] = MinusNode(p.slice[2], p[1], p[3], p.lineno(2), p.slice[2].column)
        else: p[0] = p[1]

    def p_term(self,p):
        '''term : term STAR unary
                | term DIV unary
                | unary'''
        if len(p) == 4 and p[2] == '*':
            p[0] = StarNode(p.slice[2], p[1], p[3], p.lineno(2), p.slice[2].column)
        elif len(p) == 4 and p[2] == '/':
            p[0] = DivNode(p.slice[2], p[1], p[3], p.lineno(2), p.slice[2].column)
        else: p[0] = p[1]
    
    def p_unary_factor(self,p):
        '''unary : factor'''
        p[0] = p[1]
    
    def p_unary_negate(self,p):
        '''unary : NOX unary'''
        col = p.slice[1].column
        line = p.lineno(1)
        p[0] = NegateNode(p[2], line, col)
    
    def p_unary_isvoid(self,p):
        '''unary : isvoid expr'''
        col = p.slice[1].column
        line = p.lineno(1)
        p[0] = IsVoidNode(p[2], line, col)

    def p_expr_let(self,p):
        '''atom : let declar_list in expr'''
        col = p.slice[1].column
        line = p.lineno(1)
        p[0] = LetNode(p[2],p[4], line, col)

    def p_expr_while(self,p):
        '''atom : while expr loop expr pool'''
        col = p.slice[1].column
        line = p.lineno(1)
        p[0] = WhileNode(p[2], p[4], line, col)

    def p_expr_if(self,p):
        '''atom : if expr then expr else expr fi'''
        col = p.slice[1].column
        line = p.lineno(1)
        p[0] =  IfNode(p[2],p[4],p[6], line, col)

    def p_expr_case(self,p):
        '''atom : case expr of assign_list esac'''
        col = p.slice[1].column
        line = p.lineno(1)
        p[0] = CaseNode(p[2], p[4], line, col)
    
    def p_expr_group(self,p):
        '''atom : OCUR expr_list CCUR'''
        col = p.slice[1].column
        line = p.lineno(1)
        p[0] = ExpressionGroupNode(p[2], line, col)

    def p_expr_assign(self,p):
        '''atom : ID LARROW expr'''
        col = p.slice[1].column
        line = p.lineno(1)
        p[0] = AssignNode(p[1],p[3], line, col)
    
    def p_factor_atom(self,p):
        '''factor : atom'''
        p[0] = p[1]

    def p_factor_expr(self,p):
        '''factor : OPAR expr CPAR'''
        p[0] = p[2]

    def p_factor_call(self,p):
        '''factor : factor DOT ID OPAR arg_list_call CPAR
                  | ID OPAR arg_list_call CPAR
                  | factor ARROBA TYPE DOT ID OPAR arg_list_call CPAR'''
        if p[2] == '.':
            p[0] = CallNode(p[1], p[3], p[5], None,1, p.lineno(2), p.slice[2].column)
        elif p[2] == '(':
            p[0] = CallNode(None, p[1], p[3], None,2, p.lineno(1), p.slice[1].column)
        elif p[2] == '@': 
            p[0] = CallNode(p[1], p[5], p[7], p[3],3, p.lineno(3), p.slice[3].column)

    def p_arg_list_call(self,p):
        '''arg_list_call : arg_list
                         | arg_list_empty'''
        p[0] = p[1]
    
    def p_atom_num(self,p):
        '''atom : NUMBER'''
        col = p.slice[1].column
        line = p.lineno(1)
        p[0] = ConstantNumNode(p[1], line, col)
    
    def p_atom_boolean(self, p):
        '''atom : true
                | false'''
        col = p.slice[1].column
        line = p.lineno(1)
        p[0] = BooleanNode(p[1], line, col)

    def p_atom_id(self,p):
        '''atom : ID'''
        col = p.slice[1].column
        line = p.lineno(1)
        p[0] = VariableNode(p[1], line, col)

    def p_atom_instantiate(self,p):
        '''atom : new TYPE'''
        col = p.slice[1].column
        line = p.lineno(2)
        p[0] = InstantiateNode(p[2], line, col)
    
    def p_atom_string(self,p):
        '''atom : STRING'''
        col = p.slice[1].column
        line = p.lineno(1)
        p[0] = StringNode(p[1], line, col)
    
    def p_arg_list(self,p):
        '''arg_list : expr
                    | expr COMMA arg_list'''
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = [p[1]] + p[3]
        
    def p_arg_list_empty(self,p):
        '''arg_list_empty : empty'''
        p[0] = []

    def p_error(self,p):
        self.found_error = True
        if not p:
            error = ParserError(0,0,"EOF")
            self.errors.append(error)
            return
        msg = f'ERROR at or near "{p.value}"'
        error = ParserError(p.column,p.lineno,msg)
        self.errors.append(error)
        self.parser.errok()
