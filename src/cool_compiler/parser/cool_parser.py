from sly import Parser
from .__dependency import CoolTokens
from .factory_decored import NodesName

class CoolParser(Parser):
    tokens = CoolTokens.tokens
    start = 'program'
    precedence = (
        ('right', 'ARROW'),
        ('left','NOT'),
        ('nonassoc', '=','<','LESS_OR'),
        ('left', '+', '-'),
        ('left', '*', '/'),
        ('left', "ISVOID"),
        ('left', '~'),
        ('left', '@'),
        ('right', 'IN'),
        ('left', '.'),
  
    )
    def __init__(self, factory, errors):
        self.factory = factory
        self.cool_error = errors
        self.lte = None

    def error(self, token):
        tok = next(self.tokens, None)
        if self.lte is None or not self.lte == token :
            if token is None:
                try: 
                    tok = self.symstack[-1]
                    self.cool_error(tok.lineno, tok.index)
                except AttributeError: 
                    self.cool_error.pos = (0, 0) 
                self.cool_error.add_syntactic(f"ERROR at or near EOF")
                return     
            else: 
                char = token.value
                self.cool_error(token.lineno, token.index)
                self.cool_error.add_syntactic(f"ERROR at or near {char}")
        self.lte = tok
        return tok
        
    @_("")
    def epsilon(self, prod):
        pass
    
    @_('class_list')
    def program(self, prod): 
        return self.factory( NodesName.Program, prod.class_list )
    
    @_("cclass epsilon")
    def class_list(self, prod):
        return [prod.cclass]
    
    @_('cclass class_list')
    def class_list(self, prod):
        return [prod.cclass] + prod.class_list
    
    @_('CLASS TYPE "{" class_feature "}" ";" ')
    def cclass(self, prod):
        self.factory.get_pos_to_errors(prod.lineno, prod.index)
        return self.factory( NodesName.Class, prod.TYPE, None, prod.class_feature )
    
    @_('CLASS TYPE INHERITS TYPE "{" class_feature "}" ";"')
    def cclass(self, prod):
        self.factory.get_pos_to_errors(prod.lineno, prod.index)
        return self.factory( NodesName.Class, prod.TYPE0, prod.TYPE1, prod.class_feature )
    
    @_('def_atr ";" class_feature')
    def class_feature(self, prod):
        return [prod.def_atr] + prod.class_feature
    
    @_('def_func ";" class_feature')
    def class_feature(self, prod):
        return [prod.def_func] + prod.class_feature

    @_('epsilon')
    def class_feature(self, prod):
        return []
    
    @_('ID ":" TYPE')
    def def_atr(self, prod):
        self.factory.get_pos_to_errors(prod.lineno, prod.index)
        return self.factory( NodesName.DefAtr, prod.ID, prod.TYPE, None )
    
    @_('ID ":" TYPE ARROW expr')
    def def_atr(self, prod):
        self.factory.get_pos_to_errors(prod.lineno, prod.index)
        return self.factory( NodesName.DefAtr, prod.ID, prod.TYPE, prod.expr )

    @_('ID "(" param_list ")" ":" TYPE "{" expr "}"')
    def def_func(self, prod):
        self.factory.get_pos_to_errors(prod.lineno, prod.index)
        return self.factory( NodesName.DefFunc, prod.ID, prod.param_list, prod.TYPE, prod.expr )
   
    @_('ID "(" ")" ":" TYPE "{" expr "}"')
    def def_func(self, prod):
        self.factory.get_pos_to_errors(prod.lineno, prod.index)
        return self.factory( NodesName.DefFunc, prod.ID, [], prod.TYPE, prod.expr )
 
    @_('ID ":" TYPE "," param_list')
    def param_list(self, prod):
        return [( prod.ID, prod.TYPE )] + prod.param_list
    
    @_('ID ":" TYPE')
    def param_list(self, prod):
        return [( prod.ID, prod.TYPE )] 

    @_('ID ARROW expr')
    def expr(self, prod):
        self.factory.get_pos_to_errors(prod.lineno, prod.index)
        return self.factory( NodesName.Assing, prod.ID, prod.expr)

    @_('expr "@" TYPE "." ID "(" expr_list ")"', 'expr "@" TYPE "." ID "(" ")"' )
    def expr(self, prod):
        self.factory.get_pos_to_errors(prod.lineno, prod.index)
        try:
            return self.factory( NodesName.CastingDispatch, prod.expr, prod.TYPE, prod.ID, prod.expr_list)
        except AttributeError:
            return self.factory( NodesName.CastingDispatch, prod.expr, prod.TYPE, prod.ID, [])

    @_('expr "." ID "(" expr_list ")"', 'expr "." ID "(" ")"')
    def expr(self, prod):
        self.factory.get_pos_to_errors(prod.lineno, prod.index)
        try: 
            return self.factory( NodesName.Dispatch, prod.expr, prod.ID, prod.expr_list)
        except:
            return self.factory( NodesName.Dispatch, prod.expr, prod.ID, [])

    @_('ID "(" expr_list ")"', 'ID "(" ")"')
    def expr(self, prod):
        self.factory.get_pos_to_errors(prod.lineno, prod.index)
        try:
            return self.factory( NodesName.StaticDispatch, prod.ID, prod.expr_list )
        except AttributeError:
            return self.factory( NodesName.StaticDispatch, prod.ID, [] )
            
    @_('expr "," expr_list')
    def expr_list(self, prod):
        return [prod.expr] + prod.expr_list
    
    @_('expr')
    def expr_list(self, prod):
        return [prod.expr]
    
    @_('IF expr THEN expr ELSE expr FI')
    def expr(self, prod):
        self.factory.get_pos_to_errors(prod.lineno, prod.index)
        return self.factory( NodesName.IfThenElse, prod.expr0, prod.expr1, prod.expr2)
    
    @_('WHILE expr LOOP expr POOL')
    def expr(self, prod):
        self.factory.get_pos_to_errors(prod.lineno, prod.index)
        return self.factory( NodesName.While, prod.expr0, prod.expr1)
    
    @_('"{" block_list "}"')
    def expr(self, prod):
        self.factory.get_pos_to_errors(prod.lineno, prod.index)
        return self.factory( NodesName.Block, prod.block_list)

    @_('expr ";" block_list')
    def block_list(self, prod):
        return [prod.expr] + prod.block_list
    
    @_('expr ";" epsilon')
    def block_list(self, prod):
        return [prod.expr] 

    @_('LET let_list IN expr')
    def expr(self, prod):
        self.factory.get_pos_to_errors(prod.lineno, prod.index)
        return self.factory( NodesName.LetIn, prod.let_list, prod.expr)

    @_('let_assign "," let_list')
    def let_list(self, prod):
        return [prod.let_assign] + prod.let_list
    
    @_('let_assign epsilon')
    def let_list(self, prod):
        return [prod.let_assign]

    @_('ID ":" TYPE ARROW expr')
    def let_assign(self, prod):
        return (prod.ID, prod.TYPE, prod.expr)

    @_('ID ":" TYPE')
    def let_assign(self, prod):
        return (prod.ID, prod.TYPE, None)
    
    @_('CASE expr OF case_list ESAC')
    def expr(self, prod):
        self.factory.get_pos_to_errors(prod.lineno, prod.index)
        return self.factory( NodesName.Case, prod.case_list, prod.expr)

    @_('ID ":" TYPE LOGICAR expr ";" case_list')
    def case_list(self, prod):
        return [( prod.ID, prod.TYPE, prod.expr )] + prod.case_list
    
    @_('ID ":" TYPE LOGICAR expr ";"')
    def case_list(self, prod):
        return [( prod.ID, prod.TYPE, prod.expr )]

    @_('NEW TYPE')
    def expr(self, prod):
        self.factory.get_pos_to_errors(prod.lineno, prod.index)
        return self.factory( NodesName.New, prod.TYPE )
    
    @_('ISVOID expr')
    def expr(self, prod):
        self.factory.get_pos_to_errors(prod.lineno, prod.index)
        return self.factory( NodesName.IsVoid, prod.expr )

    @_('expr "+" expr')
    def expr(self, prod):
        self.factory.get_pos_to_errors(prod.lineno, prod.index)
        return self.factory( NodesName.Sum, prod.expr0, prod.expr1 )
    
    @_('expr "-" expr')
    def expr(self, prod):
        self.factory.get_pos_to_errors(prod.lineno, prod.index)
        return self.factory( NodesName.Rest, prod.expr0, prod.expr1 )
    
    @_('expr "*" expr')
    def expr(self, prod):
        self.factory.get_pos_to_errors(prod.lineno, prod.index)
        return self.factory( NodesName.Mult, prod.expr0, prod.expr1 )
    
    @_('expr "/" expr')
    def expr(self, prod):
        self.factory.get_pos_to_errors(prod.lineno, prod.index)
        return self.factory( NodesName.Div, prod.expr0, prod.expr1 )
    
    @_('"~" expr')
    def expr(self, prod):
        self.factory.get_pos_to_errors(prod.lineno, prod.index)
        return self.factory( NodesName.Complement, prod.expr )

    @_('expr "<" expr')
    def expr(self, prod):
        self.factory.get_pos_to_errors(prod.lineno, prod.index)
        return self.factory( NodesName.Less, prod.expr0, prod.expr1 )
    
    @_('expr LESS_OR expr')
    def expr(self, prod):
        self.factory.get_pos_to_errors(prod.lineno, prod.index)
        return self.factory( NodesName.LessOrEquals, prod.expr0, prod.expr1 )
    
    @_('expr "=" expr')
    def expr(self, prod):
        self.factory.get_pos_to_errors(prod.lineno, prod.index)
        return self.factory( NodesName.Equals, prod.expr0, prod.expr1 )
   
    @_('NOT expr')
    def expr(self, prod):
        self.factory.get_pos_to_errors(prod.lineno, prod.index)
        return self.factory( NodesName.Neg, prod.expr )
    
    @_('"(" expr ")"')
    def expr(self, prod):
        self.factory.get_pos_to_errors(prod.lineno, prod.index)
        return prod.expr
    
    @_("ID")
    def expr(self, prod):
        self.factory.get_pos_to_errors(prod.lineno, prod.index)
        return self.factory( NodesName.IdExpr, prod.ID)
    
    @_("NUMBER")
    def expr(self, prod):
        self.factory.get_pos_to_errors(prod.lineno, prod.index)
        return self.factory( NodesName.Int, prod.NUMBER)
    
    @_("STRING")
    def expr(self, prod):
        self.factory.get_pos_to_errors(prod.lineno, prod.index)
        return self.factory( NodesName.Str, prod.STRING)
    
    @_("TRUE")
    def expr(self, prod):
        self.factory.get_pos_to_errors(prod.lineno, prod.index)
        return self.factory( NodesName.Bool, prod.TRUE)
    
    @_("FALSE")
    def expr(self, prod):
        self.factory.get_pos_to_errors(prod.lineno, prod.index)
        return self.factory( NodesName.Bool, prod.FALSE)