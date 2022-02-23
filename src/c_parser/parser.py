import lexer.lexer as lexer
from lexer.lexer import _tokens
from cool_ast.cool_ast import *
import ply.yacc as yacc
import ply.lex as lt
from utils.errors import _SyntacticError
coolLexer = lexer.CoolLexer()
tokens = _tokens

precedence = (
    ( 'nonassoc', 'assignArrow'),
    ( 'left', 'not'),
    ( 'nonassoc', 'leq', 'lneq', 'equal'),
    ( 'left', 'plus', 'minus'),
    ( 'left', 'star', 'div'),
    ( 'nonassoc', 'isvoid'),
    ( 'nonassoc', 'complement'),
    ( 'nonassoc', 'arroba'),
    ( 'nonassoc', 'dot' )
)
errors = []
class CoolParser:
    # def __init__(self):

    def parse(self, lexer, program):
        self.tokens = _tokens
        self.lexer = lexer
        self.lexer.build()
        ast = self.parser.parse(program)
        self.errors = errors
        return ast
    
    def find_column(input, token):
        line_start = input.rfind('\n', 0, token.lexpos) + 1
        return (token.lexpos - line_start) + 1  
    
    def p_program(p):
        'program : class_list'
        p[0] = ProgramNode(p[1])
        # token_list = []
        # for sl in p.slice:
        #     if type(lt.LexToken()) == type(sl):
        #         token_list.append(sl)
        #         token_list[-1].col = (sl.lexpos - p.lexer.lexdata.rfind('\n', 0, sl.lexpos) + 2)
        # p[0].token_list = token_list
        p[0].token_list = [sl for sl in p.slice if type(lt.LexToken()) == type(sl)]

    def p_class_list(p):
        '''class_list : def_class
                    | def_class class_list
        '''
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = [p[1]] + p[2]

    def p_def_class(p):
        ''' def_class : class type ocur feature_list ccur semi
                    | class type inherits type ocur feature_list ccur semi
        '''
        if len(p) == 7:
            p[0] = ClassDeclarationNode(p[2], p[4])
            # token_list = []
            # for sl in p.slice:
            #     if type(lt.LexToken()) == type(sl):
            #         token_list.append(sl)
            #         token_list[-1].col = (sl.lexpos - p.lexer.lexdata.rfind('\n', 0, sl.lexpos) + 2)
            # p[0].token_list = token_list
            p[0].token_list = [sl for sl in p.slice if type(lt.LexToken()) == type(sl)]
        else:
            p[0] = ClassDeclarationNode(p[2], p[6], p[4])
            # token_list = []
            # for sl in p.slice:
            #     if type(lt.LexToken()) == type(sl):
            #         token_list.append(sl)
            #         token_list[-1].col = (sl.lexpos - p.lexer.lexdata.rfind('\n', 0, sl.lexpos) + 2)
            # p[0].token_list = token_list
            p[0].token_list = [sl for sl in p.slice if type(lt.LexToken()) == type(sl)]

    def p_feature_list_attr(p):
        ''' feature_list : def_attr feature_list
                        | def_func feature_list
                        |  
        '''
        if len(p) == 1:
            p[0] = []
        elif isinstance(p[1], AttrDeclarationNode):
            if len(p) == 3:
                p[0] = [p[1]] + p[2]
            else:
                p[0] = [p[1]]
        elif isinstance(p[1], FuncDeclarationNode):
            if len(p) == 3:
                p[0] = [p[1]] + p[2]
            else:
                p[0] = [p[1]]
            
    # def p_feature_list_func(p):
    #     'feature_list : def_func feature_list'
    #     p[0] = [p[1]] + p[2]

    # def p_feature_list_empty(p):
    #     'feature_list : empty'
    #     p[0] = []

    def p_def_attr(p):
        '''def_attr : id colon type semi
                    | id colon type assignArrow expr semi
        '''
        if len(p) == 5:
            p[0] = AttrDeclarationNode(p[1], p[3])
            # token_list = []
            # for sl in p.slice:
            #     if type(lt.LexToken()) == type(sl):
            #         token_list.append(sl)
            #         token_list[-1].col = (sl.lexpos - p.lexer.lexdata.rfind('\n', 0, sl.lexpos) + 2)
            # p[0].token_list = token_list
            p[0].token_list = [sl for sl in p.slice if type(lt.LexToken()) == type(sl)]
        else:
            p[0] = AttrDeclarationNode(p[1],p[3],p[5])
            # token_list = []
            # for sl in p.slice:
            #     if type(lt.LexToken()) == type(sl):
            #         token_list.append(sl)
            #         token_list[-1].col = (sl.lexpos - p.lexer.lexdata.rfind('\n', 0, sl.lexpos) + 2)
            # p[0].token_list = token_list
            p[0].token_list = [sl for sl in p.slice if type(lt.LexToken()) == type(sl)]
        
    def p_def_func(p):
        'def_func : id opar arg_list cpar colon type ocur expr ccur semi'
        p[0] = FuncDeclarationNode(p[1],p[3],p[6],p[8])
        # token_list = []
        # for sl in p.slice:
        #     if type(lt.LexToken()) == type(sl):
        #         token_list.append(sl)
        #         token_list[-1].col = (sl.lexpos - p.lexer.lexdata.rfind('\n', 0, sl.lexpos) + 2)
        # p[0].token_list = token_list
        p[0].token_list = [sl for sl in p.slice if type(lt.LexToken()) == type(sl)]

    def p_arg_list(p):
        '''arg_list : non_empty_arg_list
                    | 
        '''
        if len(p) == 2: #p[1] == 'non_empty_arg_list':
            p[0] = p[1]
        else:
            p[0] = []

    def p_non_empty_arg_list(p):
        '''non_empty_arg_list   : arg
                                | arg comma non_empty_arg_list
        '''
        if len(p) == 4:
            p[0] = [p[1]] + p[3]
        elif len(p) == 2:
            p[0] = [p[1]]

    def p_arg(p):
        'arg : id colon type'
        p[0] = (p[1], p[3])

    def p_param_list(p):
        '''param_list : expr_list
                    | 
        '''
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = []

    def p_expr_list(p):
        '''expr_list : expr
                    | expr comma expr_list
        '''
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = [p[1]] + p[3]

    def p_chunk(p):
        '''chunk : expr semi
                | expr semi chunk
        '''
        if len(p) == 3:
            p[0] = [p[1]]
        else:
            p[0] = [p[1]] + p[3]

    def p_expr_assign(p):
        'expr : id assignArrow expr'
        p[0] = AssignNode(p[1],p[3])
        # token_list = []
        # for sl in p.slice:
        #     if type(lt.LexToken()) == type(sl):
        #         token_list.append(sl)
        #         token_list[-1].col = (sl.lexpos - p.lexer.lexdata.rfind('\n', 0, sl.lexpos) + 2)
        # p[0].token_list = token_list
        p[0].token_list = [sl for sl in p.slice if type(lt.LexToken()) == type(sl)]

    def p_expr_call(p):
        '''expr : expr dot id opar param_list cpar
                | expr arroba type dot id opar param_list cpar
                | id opar param_list cpar
        '''
        if len(p) == 7:
            p[0] = CallNode(p[3], p[5], p[1])
            # token_list = []
            # for sl in p.slice:
            #     if type(lt.LexToken()) == type(sl):
            #         token_list.append(sl)
            #         token_list[-1].col = (sl.lexpos - p.lexer.lexdata.rfind('\n', 0, sl.lexpos) + 2)
            # p[0].token_list = token_list
            p[0].token_list = [sl for sl in p.slice if type(lt.LexToken()) == type(sl)]
        elif len(p) == 9:
            p[0] = CallNode(p[5], p[7], p[1], p[3])
            # token_list = []
            # for sl in p.slice:
            #     if type(lt.LexToken()) == type(sl):
            #         token_list.append(sl)
            #         token_list[-1].col = (sl.lexpos - p.lexer.lexdata.rfind('\n', 0, sl.lexpos) + 2)
            # p[0].token_list = token_list
            p[0].token_list = [sl for sl in p.slice if type(lt.LexToken()) == type(sl)]
        else:
            p[0] = CallNode(p[1], p[3])
            # token_list = []
            # for sl in p.slice:
            #     if type(lt.LexToken()) == type(sl):
            #         token_list.append(sl)
            #         token_list[-1].col = (sl.lexpos - p.lexer.lexdata.rfind('\n', 0, sl.lexpos) + 2)
            # p[0].token_list = token_list
            p[0].token_list = [sl for sl in p.slice if type(lt.LexToken()) == type(sl)]

    def p_expr_if(p):
        'expr : if expr then expr else expr fi'
        p[0] = ConditionalNode(p[2],p[4],p[6])
        # token_list = []
        # for sl in p.slice:
        #     if type(lt.LexToken()) == type(sl):
        #         token_list.append(sl)
        #         token_list[-1].col = (sl.lexpos - p.lexer.lexdata.rfind('\n', 0, sl.lexpos) + 2)
        # p[0].token_list = token_list
        p[0].token_list = [sl for sl in p.slice if type(lt.LexToken()) == type(sl)]

    def p_expr_while(p):
        'expr : while expr loop expr pool'
        p[0] = WhileNode(p[2], p[4])
        # token_list = []
        # for sl in p.slice:
        #     if type(lt.LexToken()) == type(sl):
        #         token_list.append(sl)
        #         token_list[-1].col = (sl.lexpos - p.lexer.lexdata.rfind('\n', 0, sl.lexpos) + 2)
        # p[0].token_list = token_list
        p[0].token_list = [sl for sl in p.slice if type(lt.LexToken()) == type(sl)]

    def p_expr_chunk(p):
        'expr : ocur chunk ccur'
        p[0] = ChunkNode(p[2])
        # token_list = []
        # for sl in p.slice:
        #     if type(lt.LexToken()) == type(sl):
        #         token_list.append(sl)
        #         token_list[-1].col = (sl.lexpos - p.lexer.lexdata.rfind('\n', 0, sl.lexpos) + 2)
        # p[0].token_list = token_list
        p[0].token_list = [sl for sl in p.slice if type(lt.LexToken()) == type(sl)]

    def p_expr_let(p):
        'expr : let decl_list in expr'
        p[0] = LetInNode(p[2],p[4])
        # token_list = []
        # for sl in p.slice:
        #     if type(lt.LexToken()) == type(sl):
        #         token_list.append(sl)
        #         token_list[-1].col = (sl.lexpos - p.lexer.lexdata.rfind('\n', 0, sl.lexpos) + 2)
        # p[0].token_list = token_list
        p[0].token_list = [sl for sl in p.slice if type(lt.LexToken()) == type(sl)]

    def p_expr_case(p):
        'expr : case expr of case_list esac'
        p[0] = SwitchCaseNode(p[2],p[4])
        a = p[4]
        b = p[2]
        # token_list = []
        # for sl in p.slice:
        #     if type(lt.LexToken()) == type(sl):
        #         token_list.append(sl)
        #         token_list[-1].col = (sl.lexpos - p.lexer.lexdata.rfind('\n', 0, sl.lexpos) + 2)
        # p[0].token_list = token_list
        p[0].token_list = [sl for sl in p.slice if type(lt.LexToken()) == type(sl)]

    def p_expr_instantiate(p):
        'expr : new type'
        p[0] = InstantiateNode(p[2])
        # token_list = []
        # for sl in p.slice:
        #     if type(lt.LexToken()) == type(sl):
        #         token_list.append(sl)
        #         token_list[-1].col = (sl.lexpos - p.lexer.lexdata.rfind('\n', 0, sl.lexpos) + 2)
        # p[0].token_list = token_list
        p[0].token_list = [sl for sl in p.slice if type(lt.LexToken()) == type(sl)]

    def p_expr_isvoid(p):
        'expr : isvoid expr'
        p[0] = IsVoidNode(p[2])
        # token_list = []
        # for sl in p.slice:
        #     if type(lt.LexToken()) == type(sl):
        #         token_list.append(sl)
        #         token_list[-1].col = (sl.lexpos - p.lexer.lexdata.rfind('\n', 0, sl.lexpos) + 2)
        # p[0].token_list = token_list
        p[0].token_list = [sl for sl in p.slice if type(lt.LexToken()) == type(sl)]

    def p_expr_bin1(p):
        '''expr : expr plus expr
                | expr minus expr
        '''
        if p[2] == '+':
            p[0] = PlusNode(p[1], p[3])
            # token_list = []
            # for sl in p.slice:
            #     if type(lt.LexToken()) == type(sl):
            #         token_list.append(sl)
            #         a= p.lexer.lexdata.rfind('\n', 0, sl.lexpos)
            #         b = p.lexer.lexdata
            #         token_list[-1].col = (sl.lexpos - p.lexer.lexdata.rfind('\n', 0, sl.lexpos) + 2)
            # p[0].token_list = token_list
            p[0].token_list = [sl for sl in p.slice if type(lt.LexToken()) == type(sl)]
        else:
            p[0] = MinusNode(p[1], p[3])
            # token_list = []
            # for sl in p.slice:
            #     if type(lt.LexToken()) == type(sl):
            #         token_list.append(sl)
            #         token_list[-1].col = (sl.lexpos - p.lexer.lexdata.rfind('\n', 0, sl.lexpos) + 2)
            # p[0].token_list = token_list
            p[0].token_list = [sl for sl in p.slice if type(lt.LexToken()) == type(sl)]

    def p_expr_bin2(p):
        '''expr : expr star expr
                | expr div expr
        '''
        if p[2] == '*':
            p[0] = StarNode(p[1], p[3])
            # token_list = []
            # for sl in p.slice:
            #     if type(lt.LexToken()) == type(sl):
            #         token_list.append(sl)
            #         token_list[-1].col = (sl.lexpos - p.lexer.lexdata.rfind('\n', 0, sl.lexpos) + 2)
            # p[0].token_list = token_list
            p[0].token_list = [sl for sl in p.slice if type(lt.LexToken()) == type(sl)]
        else:
            p[0] = DivNode(p[1], p[3])
            # token_list = []
            # for sl in p.slice:
            #     if type(lt.LexToken()) == type(sl):
            #         token_list.append(sl)
            #         token_list[-1].col = (sl.lexpos - p.lexer.lexdata.rfind('\n', 0, sl.lexpos) + 2)
            # p[0].token_list = token_list
            p[0].token_list = [sl for sl in p.slice if type(lt.LexToken()) == type(sl)]

    def p_expr_bin3(p):
        '''expr : expr equal expr
                | expr lneq expr
                | expr leq expr
        '''
        if p[2] == '=':
            p[0] = EqualNode(p[1],p[3])
            # token_list = []
            # for sl in p.slice:
            #     if type(lt.LexToken()) == type(sl):
            #         token_list.append(sl)
            #         token_list[-1].col = (sl.lexpos - p.lexer.lexdata.rfind('\n', 0, sl.lexpos) + 2)
            # p[0].token_list = token_list
            p[0].token_list = [sl for sl in p.slice if type(lt.LexToken()) == type(sl)]
        elif p[2] == '<=':
            p[0] = LeqNode(p[1], p[3])
            # token_list = []
            # for sl in p.slice:
            #     if type(lt.LexToken()) == type(sl):
            #         token_list.append(sl)
            #         token_list[-1].col = (sl.lexpos - p.lexer.lexdata.rfind('\n', 0, sl.lexpos) + 2)
            # p[0].token_list = token_list
            p[0].token_list = [sl for sl in p.slice if type(lt.LexToken()) == type(sl)]
        else:
            p[0] = LessNode(p[1], p[3])
            # token_list = []
            # for sl in p.slice:
            #     if type(lt.LexToken()) == type(sl):
            #         token_list.append(sl)
            #         token_list[-1].col = (sl.lexpos - p.lexer.lexdata.rfind('\n', 0, sl.lexpos) + 2)
            # p[0].token_list = token_list
            p[0].token_list = [sl for sl in p.slice if type(lt.LexToken()) == type(sl)]

    def p_expr_unary(p):
        '''expr : complement expr
                | not expr
        '''
        if p[1] == '~':
            p[0] = ComplementNode(p[2])
            # token_list = []
            # for sl in p.slice:
            #     if type(lt.LexToken()) == type(sl):
            #         token_list.append(sl)
            #         token_list[-1].col = (sl.lexpos - p.lexer.lexdata.rfind('\n', 0, sl.lexpos) + 2)
            # p[0].token_list = token_list
            p[0].token_list = [sl for sl in p.slice if type(lt.LexToken()) == type(sl)]
        else:
            p[0] = NotNode(p[2])
            # token_list = []
            # for sl in p.slice:
            #     if type(lt.LexToken()) == type(sl):
            #         token_list.append(sl)
            #         token_list[-1].col = (sl.lexpos - p.lexer.lexdata.rfind('\n', 0, sl.lexpos) + 2)
            # p[0].token_list = token_list
            p[0].token_list = [sl for sl in p.slice if type(lt.LexToken()) == type(sl)]

    def p_expr_par(p):
        'expr : opar expr cpar'
        p[0] = p[2]

    def p_expr_id(p):
        'expr : id'
        p[0] = VariableNode(p[1])
        # token_list = []
        # for sl in p.slice:
        #     if type(lt.LexToken()) == type(sl):
        #         token_list.append(sl)
        #         token_list[-1].col = (sl.lexpos - p.lexer.lexdata.rfind('\n', 0, sl.lexpos) + 2)
        # p[0].token_list = token_list
        p[0].token_list = [sl for sl in p.slice if type(lt.LexToken()) == type(sl)]

    def p_expr_int(p):
        'expr : number'
        p[0] = ConstantNumNode(p[1])
        # token_list = []
        # for sl in p.slice:
        #     if type(lt.LexToken()) == type(sl):
        #         token_list.append(sl)
        #         token_list[-1].col = (sl.lexpos - p.lexer.lexdata.rfind('\n', 0, sl.lexpos) + 2)
        # p[0].token_list = token_list
        p[0].token_list = [sl for sl in p.slice if type(lt.LexToken()) == type(sl)]

    def p_expr_string(p):
        'expr : string'
        p[0] = StringNode(p[1])
        # token_list = []
        # for sl in p.slice:
        #     if type(lt.LexToken()) == type(sl):
        #         token_list.append(sl)
        #         token_list[-1].col = (sl.lexpos - p.lexer.lexdata.rfind('\n', 0, sl.lexpos) + 2)
        # p[0].token_list = token_list
        p[0].token_list = [sl for sl in p.slice if type(lt.LexToken()) == type(sl)]

    def p_expr_boolean(p):
        '''expr : true 
            | false'''
        if p[1] == 'true':
            p[0] =  TrueNode(p[1])
            # token_list = []
            # for sl in p.slice:
            #     if type(lt.LexToken()) == type(sl):
            #         token_list.append(sl)
            #         token_list[-1].col = (sl.lexpos - p.lexer.lexdata.rfind('\n', 0, sl.lexpos) + 2)
            # p[0].token_list = token_list
            p[0].token_list = [sl for sl in p.slice if type(lt.LexToken()) == type(sl)]
        else:
            p[0] = FalseNode(p[1])
            # token_list = []
            # for sl in p.slice:
            #     if type(lt.LexToken()) == type(sl):
            #         token_list.append(sl)
            #         token_list[-1].col = (sl.lexpos - p.lexer.lexdata.rfind('\n', 0, sl.lexpos) + 2)
            # p[0].token_list = token_list
            p[0].token_list = [sl for sl in p.slice if type(lt.LexToken()) == type(sl)]

    def p_decl_list(p):
        '''decl_list : decl 
                | decl comma decl_list'''
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = [p[1]] + p[3]

    def p_decl(p):
        '''decl : id colon type
                | id colon type assignArrow expr
        '''
        if len(p) == 4:
            p[0] = VarDeclarationNode(p[1], p[3])
            # token_list = []
            # for sl in p.slice:
            #     if type(lt.LexToken()) == type(sl):
            #         token_list.append(sl)
            #         token_list[-1].col = (sl.lexpos - p.lexer.lexdata.rfind('\n', 0, sl.lexpos) + 2)
            # p[0].token_list = token_list
            p[0].token_list = [sl for sl in p.slice if type(lt.LexToken()) == type(sl)]
        else:
            p[0] = VarDeclarationNode(p[1], p[3], p[5])
            # token_list = []
            # for sl in p.slice:
            #     if type(lt.LexToken()) == type(sl):
            #         token_list.append(sl)
            #         token_list[-1].col = (sl.lexpos - p.lexer.lexdata.rfind('\n', 0, sl.lexpos) + 2)
            # p[0].token_list = token_list
            p[0].token_list = [sl for sl in p.slice if type(lt.LexToken()) == type(sl)]

    def p_case_list(p):
        '''case_list : id colon type rArrow expr semi
                    | id colon type rArrow expr semi case_list
        '''
        if len(p) == 7:
            p[0] = [(p[1], p[3], p[5], [sl for sl in p.slice if type(lt.LexToken()) == type(sl)])]
        else:
            # p[0] = [(p[1], p[3], p[5], p[7])]
            a = p[3]
            p[0] = [(p[1], p[3], p[5], [sl for sl in p.slice if type(lt.LexToken()) == type(sl)])]+ p[7]
    
    # Compute column.
    #   input is the input text string
    #   token is a token instance
    #parentesis?

    def p_error(p):
        global errors
        def find_column(input, token):
            line_start = input.rfind('\n', 0, token.lexpos) + 1
            return (token.lexpos - line_start) + 1  #parentesis?

        if not p:
            errors.append(_SyntacticError % (0,0,'EOF'))
            return

        token_column = find_column(p.lexer.lexdata, p)
        errors.append(_SyntacticError % (p.lineno, token_column, p.value))
        # print(SyntacticError % (p.lineno, token_column, p.value))
        # print(f'({p.lineno}, {token_column}) - SyntacticError: ERROR at or near "{p.value}"')
        

    parser = yacc.yacc(debug = True)
