import ply.yacc as yacc
from .lexer import COOL_Lexer
from .ast import *

class COOL_Parser:

    def __init__(self):
        self.tokens = COOL_Lexer.tokens

    def parse(self, input_string):
        l = COOL_Lexer()
        l.build()
        self.lex = l
        self.errors = []
        self.parser = yacc.yacc(module=self)
        self.input = input_string
        result =  self.parser.parse(input_string, lexer=self.lex.lexer)
        return result, self.errors

    ######################################################################
    #                           Grammar                                  #
    ######################################################################
    
    @staticmethod
    def p_program(p):
        'program : class_list'
        p[0] = ProgramNode(p[1])
    
    @staticmethod
    def p_class_list_single(p):
        'class_list : def_class'
        p[0] = [p[1]]
    
    @staticmethod
    def p_class_list_multi(p):
        'class_list : def_class class_list'
        p[0] = [p[1]] + p[2]

    @staticmethod
    def p_def_class(p):
        'def_class : CLASS TYPEID OCUR feature_list CCUR SEMICOLON'
        p[0] = ClassDeclarationNode(p[2],p[4])

    @staticmethod
    def p_def_class_parent(p):
        'def_class : CLASS TYPEID INHERITS TYPEID OCUR feature_list CCUR SEMICOLON'
        p[0] = ClassDeclarationNode(p[2],p[6],p[4])

    @staticmethod
    def p_feature_list_empty(p):
        'feature_list :'
        p[0] = []
        pass

    @staticmethod
    def p_feature_list_attr(p):
        'feature_list : def_attr feature_list'
        p[0] = [p[1]] + p[2]

    @staticmethod
    def p_feature_list_fun(p):
        'feature_list : def_func feature_list'
        p[0] = [p[1]] + p[2]

    @staticmethod
    def p_attr(p):
        'def_attr : OBJECTID COLON TYPEID SEMICOLON'
        p[0] = AttrDeclarationNode(p[1],p[3])

    @staticmethod
    def p_attr_exp(p):
        'def_attr : OBJECTID COLON TYPEID ASSIGN exp SEMICOLON'
        p[0] = AttrDeclarationNode(p[1],p[3],p[5])

    @staticmethod
    def p_func(p):
        'def_func : OBJECTID OPAR CPAR COLON TYPEID OCUR exp CCUR SEMICOLON'
        p[0] = FuncDeclarationNode(p[1],[],p[5],p[7])

    @staticmethod
    def p_func_param(p):
        'def_func : OBJECTID OPAR param_list CPAR COLON TYPEID OCUR exp CCUR SEMICOLON'
        p[0] = FuncDeclarationNode(p[1],p[3],p[6],p[8])

    @staticmethod
    def p_param_list_single(p):
        'param_list : param'
        p[0] = [p[1]]

    @staticmethod
    def p_param_list_multi(p):
        'param_list : param COMMA param_list'
        p[0] = [p[1]] + p[3]

    @staticmethod
    def p_param(p):
        'param : OBJECTID COLON TYPEID'
        p[0] = VarDeclarationNode(p[1],p[3])

    @staticmethod
    def p_exp_assign(p):
        'exp : OBJECTID ASSIGN exp'
        p[0] = AssignNode(p[1],p[3])

    @staticmethod
    def p_exp_let(p):
        'exp : LET ident_list IN exp'
        p[0] = LetNode(p[2],p[4])
    
    @staticmethod
    def p_ident_list_single(p):
        'ident_list : iden'
        p[0] = [p[1]]

    @staticmethod
    def p_ident_list_multi(p):
        'ident_list : iden COMMA ident_list'
        p[0] = [p[1]] + p[3]

    @staticmethod
    def p_iden(p):
        'iden : OBJECTID COLON TYPEID'
        p[0] = AttrDeclarationNode(p[1],p[3],None)

    @staticmethod
    def p_iden_init(p):
        'iden : OBJECTID COLON TYPEID ASSIGN exp'
        p[0] = AttrDeclarationNode(p[1],p[3],p[5])
        
    @staticmethod
    def p_case_list_single(p):
        'case_list : branch'
        p[0] = [p[1]]

    @staticmethod
    def p_case_list_multi(p):
        'case_list : branch case_list'
        p[0] = [p[1]] + p[2]

    @staticmethod
    def p_branch(p):
        'branch : OBJECTID COLON TYPEID CASSIGN exp SEMICOLON'
        p[0] = CaseAttrNode(p[1],p[3],p[5])

    @staticmethod
    def p_exp_not(p):
        'exp : NOT exp'
        p[0] = NotNode(p[2])

    @staticmethod
    def p_exp_comp(p):
        'exp : comp'
        p[0] = p[1]

    @staticmethod
    def p_comp_arith(p):
        'comp : arith'
        p[0] = p[1]

    @staticmethod
    def p_comp_lower(p):
        'comp : arith LOWER arith'
        p[0] = LessNode(p[1],p[3])

    @staticmethod
    def p_comp_leq(p):
        'comp : arith LEQ arith'
        p[0] = ElessNode(p[1],p[3])

    @staticmethod
    def p_comp_equal(p):
        'comp : arith EQUAL arith'
        p[0] = EqualsNode(p[1],p[3])
    
    # ??????
    @staticmethod
    def p_comp_equal_not(p):
        'comp : arith EQUAL NOT exp'
        p[0] = EqualsNode(p[1],p[4])

    @staticmethod
    def p_arith_term(p):
        'arith : term'
        p[0]= p[1]
    
    @staticmethod
    def p_arith_plus(p):
        'arith : arith PLUS term'
        p[0] = PlusNode(p[1],p[3])

    @staticmethod
    def p_arith_minus(p):
        'arith : arith MINUS term'
        p[0] = MinusNode(p[1],p[3])

    @staticmethod
    def p_term_fac(p):
        'term : factor'
        p[0] = p[1]

    @staticmethod
    def p_term_star(p):
        'term : term STAR factor'
        p[0] = StarNode(p[1],p[3])

    @staticmethod
    def p_term_div(p):
        'term : term DIV factor'
        p[0] = DivNode(p[1],p[3])

    @staticmethod
    def p_factor_atom(p):
        'factor : atom'
        p[0] = p[1]

    @staticmethod
    def p_factor_neg(p):
        'factor : TILDE factor'
        p[0] = PrimeNode(p[2])
    
    @staticmethod
    def p_factor_case(p):
        'factor : CASE exp OF case_list ESAC'
        p[0] = CaseNode(p[2],p[4])
    
    @staticmethod
    def p_factor_while(p):
        'factor : WHILE exp LOOP exp POOL'
        p[0] = LoopNode(p[2],p[4])
    
    @staticmethod
    def p_factor_block(p):
        'factor : OCUR exp_list CCUR'
        p[0] = BlockNode(p[2])

    @staticmethod
    def p_exp_list_single(p):
        'exp_list : exp SEMICOLON'
        p[0] = [p[1]]

    @staticmethod
    def p_exp_list_multi(p):
        'exp_list : exp SEMICOLON exp_list'
        p[0] = [p[1]] + p[3]
    
    @staticmethod
    def p_factor_cond(p):
        'factor : IF exp THEN exp ELSE exp FI'
        p[0] = ConditionalNode(p[2],p[4],p[6])

    @staticmethod
    def p_factor_void(p):
        'factor : ISVOID factor'
        p[0] = IsVoidNode(p[2])

    @staticmethod
    def p_atom_num(p):
        'atom : INT_CONST'
        p[0] = ConstantNumNode(p[1])

    @staticmethod
    def p_atom_string(p):
        'atom : STRING_CONST'
        p[0] = StringNode(p[1])

    @staticmethod
    def p_atom_true(p):
        'atom : TRUE'
        p[0] = TrueNode(p[1])

    @staticmethod
    def p_atom_false(p):
        'atom : FALSE'
        p[0] = FalseNode(p[1])

    @staticmethod
    def p_atom_var(p):
        'atom : OBJECTID'
        p[0] = VariableNode(p[1])

    @staticmethod
    def p_atom_new(p):
        'atom : NEW TYPEID'
        p[0] = InstantiateNode(p[2])

    @staticmethod
    def p_atom_func_call(p):
        'atom : func_call'
        p[0] = p[1]

    @staticmethod
    def p_atom_exp(p):
        'atom : OPAR exp CPAR'
        p[0] = p[2]

    @staticmethod
    def p_func_call_self(p):
        'func_call : OBJECTID OPAR arg_list CPAR'
        p[0] = DispatchNode(VariableNode('self'),p[1],p[3])

    @staticmethod
    def p_func_call(p):
        'func_call : atom DOT OBJECTID OPAR arg_list CPAR'
        p[0] = DispatchNode(p[1],p[3],p[5])

    @staticmethod
    def p_func_call_at(p):
        'func_call : atom AT TYPEID DOT OBJECTID OPAR arg_list CPAR'
        p[0] = DispatchNode(p[1],p[5],p[7],p[3])

    @staticmethod
    def p_arg_list_empty(p):
        'arg_list :'
        p[0] = []
        pass

    @staticmethod
    def p_arg_list_not_empty(p):
        'arg_list : arg_list_not_empty'
        p[0] = p[1]

    @staticmethod
    def p_arg_list_not_empty_single(p):
        'arg_list_not_empty : exp'
        p[0] = [p[1]]

    @staticmethod
    def p_arg_list_not_empty_multi(p):
        'arg_list_not_empty : exp COMMA arg_list_not_empty'
        p[0] = [p[1]] + p[3]

    #Error rule for syntax errors
    def p_error(self, p):
        if not p:
            l = COOL_Lexer()
            l.build()
            for t in l.tokenize(self.input):
                if t.value != 'class': #Error at the beginning
                    p = t
                break
            
            if not p: # Error at the end
                 self.errors.append('(0, 0) - SyntacticError: ERROR at or near EOF')
                 return
        
        col = self.__find_column(p)
        line = p.lineno
        val = p.value
        #(29, 9) - SyntacticError: ERROR at or near "Test1"
        self.errors.append(f'({line}, {col}) - SyntacticError: ERROR at or near "{val}"')
    
    def __find_column(self, token):
        input_s = self.input
        line_start = input_s.rfind('\n', 0, token.lexpos) + 1
        return (token.lexpos - line_start) + 1