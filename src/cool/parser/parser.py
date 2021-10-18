import ply.yacc as yacc

from ..lexer.lexer import CoolLexer
from ..utils.ast import *
from ..utils.errors import SyntacticError
from ..utils.helpers import find_column
from ..utils.tokens import tokens
from ..utils.logger import log


class Parser:
    def __init__(self, lexer=None):
        self.lexer = lexer if lexer else CoolLexer()
        self.outputdir = 'parser/output'
        self.tokens = tokens
        self.errors = False
        self.parser = yacc.yacc(start='program',
                                module=self,
                                outputdir=self.outputdir,
                                optimize=1,
                                debuglog=log,
                                errorlog=log)

    def parse(self, program, debug=False):
        self.errors = False
        return self.parser.parse(program, self.lexer.lexer, debug=log)


class CoolParser(Parser):
    def p_program(self, p):
        'program : class_list'

        p[0] = ProgramNode(p[1])

    def p_class_list(self, p):
        '''class_list : def_class class_list
                      | def_class'''

        p[0] = [p[1]] if len(p) == 2 else [p[1]] + p[2]

    def p_class_list_error(self, p):
        'class_list : error class_list'

        p[0] = [p[1]] if len(p) == 2 else [p[1]] + p[2]

    def p_epsilon(self, p):
        'epsilon :'
        pass

    def p_def_class(self, p):
        '''def_class : class type ocur feature_list ccur semi 
                     | class type inherits type ocur feature_list ccur semi'''

        p[0] = ClassDeclarationNode(p.slice[2], p[4]) if len(p) == 7 else \
            ClassDeclarationNode(p.slice[2], p[6], p.slice[4])

    def p_def_class_error(self, p):
        '''def_class : class error ocur feature_list ccur semi 
                     | class type ocur feature_list ccur error   
                     | class error inherits type ocur feature_list ccur semi
                     | class error inherits error ocur feature_list ccur semi
                     | class type inherits error ocur feature_list ccur semi
                     | class type inherits type ocur feature_list ccur error'''

        p[0] = ErrorNode()

    def p_feature_list(self, p):
        '''feature_list : epsilon
                        | def_attr semi feature_list
                        | def_func semi feature_list'''

        p[0] = [] if len(p) == 2 else [p[1]] + p[3]

    def p_feature_list_error(self, p):
        'feature_list : error feature_list'

        p[0] = [p[1]] + p[2]

    def p_def_attr(self, p):
        '''def_attr : id colon type
                    | id colon type larrow expr'''

        p[0] = AttrDeclarationNode(p.slice[1], p.slice[3]) if len(p) == 4 else \
            AttrDeclarationNode(p.slice[1], p.slice[3], p[5])

    def p_def_attr_error(self, p):
        '''def_attr : error colon type
                    | id colon error
                    | error colon type larrow expr
                    | id colon error larrow expr
                    | id colon type larrow error'''

        p[0] = ErrorNode()

    def p_def_func(self, p):
        'def_func : id opar formals cpar colon type ocur expr ccur'

        p[0] = FuncDeclarationNode(p.slice[1], p[3], p.slice[6], p[8])

    def p_def_func_error(self, p):
        '''def_func : error opar formals cpar colon type ocur expr ccur
                    | id opar error cpar colon type ocur expr ccur
                    | id opar formals cpar colon error ocur expr ccur
                    | id opar formals cpar colon type ocur error ccur'''

        p[0] = ErrorNode()

    def p_formals(self, p):
        '''formals : param_list
                   | param_list_empty'''

        p[0] = p[1]

    def p_param_list(self, p):
        '''param_list : param
                      | param comma param_list'''

        p[0] = [p[1]] if len(p) == 2 else [p[1]] + p[3]

    def p_param_list_empty(self, p):
        'param_list_empty : epsilon'

        p[0] = []

    def p_param(self, p):
        'param : id colon type'

        p[0] = (p.slice[1], p.slice[3])

    def p_let_list(self, p):
        '''let_list : let_assign
                    | let_assign comma let_list'''

        p[0] = [p[1]] if len(p) == 2 else [p[1]] + p[3]

    def p_let_assign(self, p):
        '''let_assign : param larrow expr
                      | param'''

        p[0] = VarDeclarationNode(p[1][0], p[1][1]) if len(p) == 2 else \
            VarDeclarationNode(p[1][0], p[1][1], p[3])

    def p_cases_list(self, p):
        '''cases_list : casep semi
                      | casep semi cases_list'''

        p[0] = [p[1]] if len(p) == 3 else [p[1]] + p[3]

    def p_cases_list_error(self, p):
        '''cases_list : error cases_list
                      | error semi'''

        p[0] = [ErrorNode()]

    def p_case(self, p):
        'casep : id colon type rarrow expr'

        p[0] = OptionNode(p.slice[1], p.slice[3], p[5])

    def p_expr(self, p):
        '''expr : id larrow expr
                | comp'''

        p[0] = AssignNode(p.slice[1], p[3]) if len(p) == 4 else p[1]

    def p_comp(self, p):
        '''comp : comp less op
                | comp lesseq op
                | comp equal op
                | op'''

        if len(p) == 2:
            p[0] = p[1]
        elif p[2] == '<':
            p[0] = LessNode(p[1], p[3])
        elif p[2] == '<=':
            p[0] = LessEqNode(p[1], p[3])
        elif p[2] == '=':
            p[0] = EqualNode(p[1], p[3])

    def p_op(self, p):
        '''op : op plus term
              | op minus term
              | term'''

        if len(p) == 2:
            p[0] = p[1]
        elif p[2] == '+':
            p[0] = PlusNode(p[1], p[3])
        elif p[2] == '-':
            p[0] = MinusNode(p[1], p[3])

    def p_term(self, p):
        '''term : term star base_call
                | term div base_call
                | base_call'''

        if len(p) == 2:
            p[0] = p[1]
        elif p[2] == '*':
            p[0] = StarNode(p[1], p[3])
        elif p[2] == '/':
            p[0] = DivNode(p[1], p[3])

    def p_term_error(self, p):
        '''term : term star error
                | term div error'''

        p[0] = ErrorNode()

    def p_base_call(self, p):
        '''base_call : factor arroba type dot func_call
                     | factor'''

        p[0] = p[1] if len(p) == 2 else BaseCallNode(p[1], p.slice[3], *p[5])

    def p_base_call_error(self, p):
        '''base_call : error arroba type dot func_call
                     | factor arroba error dot func_call'''

        p[0] = ErrorNode()

    def p_factor1(self, p):
        '''factor : atom
                  | opar expr cpar'''

        p[0] = p[1] if len(p) == 2 else p[2]

    def p_factor2(self, p):
        '''factor : factor dot func_call
                  | not expr
                  | func_call'''

        if len(p) == 2:
            p[0] = StaticCallNode(*p[1])
        elif p[1] == 'not':
            p[0] = NotNode(p[2], p.slice[1])
        else:
            p[0] = CallNode(p[1], *p[3])

    def p_factor3(self, p):
        '''factor : isvoid base_call
                  | nox base_call'''

        p[0] = IsVoidNode(p[2], p.slice[1]) if p[1] == 'isvoid' else BinaryNotNode(p[2], p.slice[1])

    def p_expr_let(self, p):
        'factor : let let_list in expr'

        p[0] = LetNode(p[2], p[4], p.slice[1])

    def p_expr_case(self, p):
        'factor : case expr of cases_list esac'

        p[0] = CaseNode(p[2], p[4], p.slice[1])

    def p_expr_if(self, p):
        'factor : if expr then expr else expr fi'

        p[0] = ConditionalNode(p[2], p[4], p[6], p.slice[1])

    def p_expr_while(self, p):
        'factor : while expr loop expr pool'

        p[0] = WhileNode(p[2], p[4], p.slice[1])

    def p_atom_num(self, p):
        'atom : num'

        p[0] = ConstantNumNode(p.slice[1])

    def p_atom_id(self, p):
        'atom : id'

        p[0] = VariableNode(p.slice[1])

    def p_atom_new(self, p):
        'atom : new type'

        p[0] = InstantiateNode(p.slice[2])

    def p_atom_block(self, p):
        'atom : ocur block ccur'

        p[0] = BlockNode(p[2], p.slice[1])

    def p_atom_block_error(self, p):
        '''atom : error block ccur
                | ocur error ccur
                | ocur block error'''

        p[0] = ErrorNode()

    def p_atom_boolean(self, p):
        '''atom : true
                | false'''

        p[0] = ConstantBoolNode(p.slice[1])

    def p_atom_string(self, p):
        'atom : string'

        p[0] = ConstantStrNode(p.slice[1])

    def p_block(self, p):
        '''block : expr semi
                 | expr semi block'''

        p[0] = [p[1]] if len(p) == 3 else [p[1]] + p[3]

    def p_block_error(self, p):
        '''block : error block
                 | error semi'''

        p[0] = [ErrorNode()]

    def p_func_call(self, p):
        'func_call : id opar args cpar'

        p[0] = (p.slice[1], p[3])

    def p_func_call_error(self, p):
        '''func_call : id opar error cpar
                     | error opar args cpar'''

        p[0] = (ErrorNode(), ErrorNode())

    def p_args(self, p):
        '''args : arg_list
                | arg_list_empty'''

        p[0] = p[1]

    def p_arg_list(self, p):
        '''arg_list : expr  
                    | expr comma arg_list'''

        p[0] = [p[1]] if len(p) == 2 else \
            [p[1]] + p[3]

    def p_arg_list_error(self, p):
        'arg_list : error arg_list'

        p[0] = [ErrorNode()]

    def p_arg_list_empty(self, p):
        'arg_list_empty : epsilon'

        p[0] = []

    def p_error(self, p):
        self.errors = True
        if p:
            self.print_error(p)
        else:
            error_text = SyntacticError.ERROR % 'EOF'
            column = find_column(self.lexer.lexer, self.lexer.lexer)
            line = self.lexer.lexer.lineno
            print(SyntacticError(error_text, line, column - 1))

        raise Exception()

    def print_error(self, tok):
        error_text = SyntacticError.ERROR % tok.value
        line, column = tok.lineno, tok.column
        print(SyntacticError(error_text, line, column))