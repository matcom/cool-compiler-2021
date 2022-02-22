import ply.yacc as yacc
from .lexer import COOL_Lexer
from .ast import *


class COOL_Parser:

    def __init__(self):
        self.tokens = COOL_Lexer.tokens

    def parse(self, input_string):
        #l = COOL_Lexer()
        #l.build()
        self.lex = COOL_Lexer()
        self.errors = []
        self.parser = yacc.yacc(module=self)
        self.input = input_string
        result =  self.parser.parse(input_string, lexer=self.lex)
        return result, self.errors

    ######################################################################
    #                           Grammar                                  #
    ######################################################################
    
    @staticmethod
    def p_program(p):
        'program : class_list'
        p[0] = ProgramNode(None,p[1]) # location of this is 
    
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
        location = (p.lineno(1), p.lexpos(1))
        type_location = (p.lineno(2), p.lexpos(2))
        p[0] = ClassDeclarationNode(location,(p[2], type_location),p[4])

    @staticmethod
    def p_def_class_parent(p):
        'def_class : CLASS TYPEID INHERITS TYPEID OCUR feature_list CCUR SEMICOLON'
        location = (p.lineno(1), p.lexpos(1))
        type_location = (p.lineno(2), p.lexpos(2))
        parent_location = (p.lineno(4), p.lexpos(4))
        p[0] = ClassDeclarationNode(location,(p[2], type_location),p[6],p[4], parent_location)
        

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
        location = (p.lineno(1), p.lexpos(1))
        type_location = (p.lineno(3), p.lexpos(3))
        p[0] = AttrDeclarationNode(location,p[1],(p[3], type_location))


    @staticmethod
    def p_attr_exp(p):
        'def_attr : OBJECTID COLON TYPEID ASSIGN exp SEMICOLON'
        location = (p.lineno(1), p.lexpos(1))
        type_location = (p.lineno(3), p.lexpos(3))
        p[0] = AttrDeclarationNode(location,p[1],(p[3], type_location),p[5])

    @staticmethod
    def p_func(p):
        'def_func : OBJECTID OPAR CPAR COLON TYPEID OCUR exp CCUR SEMICOLON'
        location = (p.lineno(1), p.lexpos(1))
        return_location = (p.lineno(5), p.lexpos(5))
        p[0] = FuncDeclarationNode(location,p[1],[],(p[5], return_location),p[7])

    @staticmethod
    def p_func_param(p):
        'def_func : OBJECTID OPAR param_list CPAR COLON TYPEID OCUR exp CCUR SEMICOLON'
        location = (p.lineno(1), p.lexpos(1))
        return_location = (p.lineno(6), p.lexpos(6))
        p[0] = FuncDeclarationNode(location,p[1],p[3],(p[6], return_location),p[8])

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
        location = (p.lineno(1), p.lexpos(1))
        type_location = (p.lineno(3), p.lexpos(3))
        p[0] = VarDeclarationNode(location,p[1],(p[3], type_location))

    @staticmethod
    def p_exp_assign(p):
        'exp : OBJECTID ASSIGN exp'
        location = (p.lineno(1), p.lexpos(1))
        symbol_location = (p.lineno(2), p.lexpos(2))
        p[0] = AssignNode(location, symbol_location, VariableNode(location,p[1]),p[3])

    @staticmethod
    def p_exp_let(p):
        'exp : LET ident_list IN exp'
        location = (p.lineno(1), p.lexpos(1))
        p[0] = LetNode(location,p[2],p[4])
    
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
        location = (p.lineno(1), p.lexpos(1))
        type_location = (p.lineno(3), p.lexpos(3))
        p[0] = VarDeclarationNode(location,p[1],(p[3], type_location),None)

    @staticmethod
    def p_iden_init(p):
        'iden : OBJECTID COLON TYPEID ASSIGN exp'
        location = (p.lineno(1), p.lexpos(1))
        type_location = (p.lineno(3), p.lexpos(3))
        p[0] = VarDeclarationNode(location,p[1],(p[3], type_location),p[5])
        
        
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
        location = (p.lineno(1), p.lexpos(1))
        type_location = (p.lineno(3), p.lexpos(3))
        p[0] = CaseAttrNode(location,p[1],(p[3], type_location),p[5])

    @staticmethod
    def p_exp_not(p):
        'exp : NOT exp'
        location = (p.lineno(1), p.lexpos(1))
        p[0] = NotNode(location,p[2])

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
        symbol_location = (p.lineno(2), p.lexpos(2))
        p[0] = LessNode(p[1].location, symbol_location, p[1],p[3])

    @staticmethod
    def p_comp_leq(p):
        'comp : arith LEQ arith'
        symbol_location = (p.lineno(2), p.lexpos(2))
        p[0] = ElessNode(p[1].location,symbol_location,p[1],p[3])

    @staticmethod
    def p_comp_equal(p):
        'comp : arith EQUAL arith'
        symbol_location = (p.lineno(2), p.lexpos(2))
        p[0] = EqualsNode(p[1].location,symbol_location,p[1],p[3])
    
    @staticmethod
    def p_comp_equal_not(p):
        'comp : arith EQUAL NOT exp'
        symbol_location = (p.lineno(2), p.lexpos(2))
        p[0] = EqualsNode(p[1].location,symbol_location,p[1],p[4])

    @staticmethod
    def p_arith_term(p):
        'arith : term'
        p[0]= p[1]
    
    @staticmethod
    def p_arith_plus(p):
        'arith : arith PLUS term'
        location = (p.lineno(2), p.lexpos(2))
        symbol_location = (p.lineno(2), p.lexpos(2))
        p[0] = PlusNode(location,symbol_location,p[1],p[3])

    @staticmethod
    def p_arith_minus(p):
        'arith : arith MINUS term'
        symbol_location = (p.lineno(2), p.lexpos(2))
        p[0] = MinusNode(p[1].location,symbol_location,p[1],p[3])

    @staticmethod
    def p_term_fac(p):
        'term : factor'
        p[0] = p[1]

    @staticmethod
    def p_term_star(p):
        'term : term STAR factor'
        symbol_location = (p.lineno(2), p.lexpos(2))
        p[0] = StarNode(p[1].location,symbol_location,p[1],p[3])

    @staticmethod
    def p_term_div(p):
        'term : term DIV factor'
        symbol_location = (p.lineno(2), p.lexpos(2))
        p[0] = DivNode(p[1].location,symbol_location,p[1],p[3])

    @staticmethod
    def p_factor_atom(p):
        'factor : atom'
        p[0] = p[1]

    @staticmethod
    def p_factor_neg(p):
        'factor : TILDE factor'
        location = (p.lineno(1), p.lexpos(1))
        p[0] = PrimeNode(location,p[2])
    
    @staticmethod
    def p_factor_case(p):
        'factor : CASE exp OF case_list ESAC'
        location = (p.lineno(1), p.lexpos(1))
        p[0] = CaseNode(location,p[2],p[4])
    
    @staticmethod
    def p_factor_while(p):
        'factor : WHILE exp LOOP exp POOL'
        location = (p.lineno(1), p.lexpos(1))
        p[0] = LoopNode(location,p[2],p[4])
    
    @staticmethod
    def p_factor_block(p):
        'factor : OCUR exp_list CCUR'
        location = (p.lineno(1), p.lexpos(1))
        p[0] = BlockNode(location,p[2])

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
        location = (p.lineno(1), p.lexpos(1))
        p[0] = ConditionalNode(location,p[2],p[4],p[6])

    @staticmethod
    def p_factor_void(p):
        'factor : ISVOID factor'
        location = (p.lineno(1), p.lexpos(1))
        p[0] = IsVoidNode(location,p[2])

    @staticmethod
    def p_atom_num(p):
        'atom : INT_CONST'
        location = (p.lineno(1), p.lexpos(1))
        p[0] = ConstantNumNode(location,p[1])

    @staticmethod
    def p_atom_string(p):
        'atom : STRING_CONST'
        location = (p.lineno(1), p.lexpos(1))
        p[0] = StringNode(location,p[1])

    @staticmethod
    def p_atom_true(p):
        'atom : TRUE'
        location = (p.lineno(1), p.lexpos(1))
        p[0] = TrueNode(location,p[1])

    @staticmethod
    def p_atom_false(p):
        'atom : FALSE'
        location = (p.lineno(1), p.lexpos(1))
        p[0] = FalseNode(location,p[1])

    @staticmethod
    def p_atom_var(p):
        'atom : OBJECTID'
        location = (p.lineno(1), p.lexpos(1))
        p[0] = VariableNode(location,p[1])

    @staticmethod
    def p_atom_new(p):
        'atom : NEW TYPEID'
        location = (p.lineno(1), p.lexpos(1))
        p[0] = InstantiateNode(location,p[2])

    @staticmethod
    def p_atom_func_call(p):
        'atom : func_call'
        p[0] = p[1]

    @staticmethod
    def p_atom_exp(p):
        'atom : OPAR exp CPAR'
        p[0] = p[2]
        p[0].location = (p.lineno(1), p.lexpos(1))

    @staticmethod
    def p_func_call_self(p):
        'func_call : OBJECTID OPAR arg_list CPAR'
        location = (p.lineno(1), p.lexpos(1))
        p[0] = DispatchNode(location,VariableNode(None,'self'),p[1],p[3])

    @staticmethod
    def p_func_call(p):
        'func_call : atom DOT OBJECTID OPAR arg_list CPAR'
        p[0] = DispatchNode(p[1].location,p[1],p[3],p[5])

    @staticmethod
    def p_func_call_at(p):
        'func_call : atom AT TYPEID DOT OBJECTID OPAR arg_list CPAR'
        p[0] = DispatchNode(p[1].location,p[1],p[5],p[7],p[3])

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
            self.errors.append('(0, 0) - SyntacticError: ERROR at or near EOF')
            return
        
        col = p.lexpos
        line = p.lineno
        val = p.value
        #(29, 9) - SyntacticError: ERROR at or near "Test1"
        self.errors.append(f'({line}, {col}) - SyntacticError: ERROR at or near "{val}"')
    
    def __find_column(self, token):
        input_s = self.input
        line_start = input_s.rfind('\n', 0, token.lexpos) + 1
        return (token.lexpos - line_start) + 1
