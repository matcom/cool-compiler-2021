import inspect
from enum import Enum

def factory(cls):
    def call(cls, name_node, *args):
        return cls.__dict_decored[name_node](cls, *args)
    cls.__call__ = call
    return cls

def factory_tester(cls):
    def call(cls, name_node, *args):
        pass
    cls.__call__ = call
    return cls

def decored(string):
    def fn(fn):
        frame = inspect.currentframe().f_back
        try: 
            _dict = frame.f_locals['__dict_decored']
            _dict[string] = fn
        except KeyError:
            frame.f_locals['__dict_decored'] = { string : fn }
        
        return fn
    return fn

class NodesName(Enum):
    Id      = "Id"
    Type    = "Type"
    Program = "Program"
    Class   = "Class" 
    DefAtr  = "DefAtr"
    DefFunc = "DefFunc"
    Assing  = "Assing"
    CastingDispatch = "CastingDispatch"
    Dispatch= "Dispatch"
    StaticDispatch = "StaticDispatch"
    IfThenElse = "IfThenElse"
    While   = "While"
    Block   = "Block"
    LetIn   = "LetIn"
    Case    = "Case"
    New     = "New"
    IsVoid  = "IsVoid"
    Sum     = "Sum"
    Rest    = "Rest"
    Mult    = "Mult"
    Div     = "Div"
    Complement = "Complement"
    Less    = "Less"
    LessOrEquals = "LessOrEquals"
    Equals  = "Equals"
    Neg     = "Neg"
    IdExpr  = "IdExpr"
    Int     = "Int"
    Str     = "Str"
    Bool    = "Bool"
    
@factory_tester
class Tester:
    
    @decored("CLASS")
    def fclass(self, name, parent, feature):
        pass