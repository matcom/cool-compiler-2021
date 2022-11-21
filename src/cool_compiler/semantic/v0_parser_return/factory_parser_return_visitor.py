from ..__dependency import factory, decored, Nodes
from .factory_parser_return_ast import *

@factory
class CoolFactory:
    def __init__(self, errors) -> None:
        self.global_names = []
        self.cool_error = errors

    def get_pos_to_errors(self, lineno, index):
        self.lineno = lineno
        self.index = index
    
    def compose(fn):
        def ffn(*args, **kword):
            node = fn(*args, **kword)
            node.get_pos_to_error(args[0].lineno, args[0].index)
            return node
        return ffn

    @decored(Nodes.Program)
    @compose
    def program(self, class_list):
        return Program(class_list, self.global_names)

    @decored(Nodes.Class)
    @compose
    def cool_class(self, name, parent, features):
        self.global_names.append((name, self.lineno, self.index))
        return CoolClass(name,parent,features)

################################################################
    @decored(Nodes.DefAtr)
    @compose
    def defatr(self, name, atype, expr):
        return AtrDef(name, atype, expr)
    
    @decored(Nodes.DefFunc)
    @compose
    def deffunc(self, name, params, return_type, expr):
        return FuncDef(name, params, return_type, expr)
    
################################################################
    @decored(Nodes.CastingDispatch)
    @compose
    def casting_dispatch(self, expr, atype, idx, params):
        return CastingDispatch(expr, atype, idx, params)
    
    @decored(Nodes.Dispatch)
    @compose
    def dispatch(self, expr, idx, params):
        return Dispatch(expr, idx, params)
    
    @decored(Nodes.StaticDispatch)
    @compose
    def static_dispatch(self, idx, params):
        return StaticDispatch(idx, params)

################################################################
    @decored(Nodes.Assing)
    @compose
    def asssing(self, idx, expr):
        return Assing(idx, expr)
    
    @decored(Nodes.IfThenElse)
    @compose
    def if_then_else(self, cond, then, eelse):
        return IfThenElse(cond, then, eelse)
    
    @decored(Nodes.While)
    @compose
    def wwhile(self, cond, expr):
        return While(cond, expr)
    
    @decored(Nodes.Block)
    @compose
    def block(self, expr_list):
        return Block(expr_list)
    
    @decored(Nodes.LetIn)
    @compose
    def let_in(self, assing_list, expr):
        return LetIn(assing_list, expr)
    
    @decored(Nodes.Case)
    @compose
    def case(self, case_list, expr):
        return Case(case_list, expr)
    
################################################################
    @decored(Nodes.Sum)
    @compose
    def sum(self, left, right):
        return Sum(left,right)
 
    @decored(Nodes.Rest)
    @compose
    def rest(self, left, right):
        return Rest(left,right)
    
    @decored(Nodes.Mult)
    @compose
    def mult(self, left, right):
        return Mult(left,right)
    
    @decored(Nodes.Div)
    @compose
    def div(self, left, right):
        return Div(left,right)
    
    @decored(Nodes.Less)
    @compose
    def less(self, left, right):
        return Less(left,right)    
    
    @decored(Nodes.LessOrEquals)
    @compose
    def less_or_equals(self, left, right):
        return LessOrEquals(left,right)    
    
    @decored(Nodes.Equals)
    @compose
    def equals(self, left, right):
        return Equals(left,right)

###############################################################
    
    @decored(Nodes.IsVoid)
    @compose
    def is_void(self, item):
        return Void(item)
            
    @decored(Nodes.New)
    @compose
    def new(self, item):
        return New(item)
            
    @decored(Nodes.Complement)
    @compose
    def complement(self, item):
        return Complement(item)
            
    @decored(Nodes.Neg)
    @compose
    def neg(self, item):
        return Neg(item)
            
    @decored(Nodes.IdExpr)
    @compose
    def idexpr(self, item):
        return Id(item)
            
    @decored(Nodes.Int)
    @compose
    def intt(self, item):
        return Int(item)
            
    @decored(Nodes.Str)
    @compose
    def string(self, item):
        return Str(item)
            
    @decored(Nodes.Bool)
    @compose
    def boool(self, item):
        return Bool(item)