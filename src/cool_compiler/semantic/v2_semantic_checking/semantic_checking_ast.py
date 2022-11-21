class Node:
    def __init__(self, static_type = None) -> None:
        self.static_type = static_type

    def get_pos_to_error(self, lineno, index):
        self.lineno = lineno
        self.index = index

####################################################################
class Program(Node):
    def __init__(self, class_list) -> None:
        self.class_list = class_list
        
class CoolClass(Node):
    def __init__(self, typee, parent_typee, feature_list) -> None:
        self.type = typee
        self.parent_type = parent_typee
        self.feature_list = feature_list

######################################################################
class Feature(Node):
    pass

class AtrDef(Feature):
    def __init__(self, name, atype, expr) -> None:
        self.name = name
        self.type = atype
        self.expr = expr

class FuncDef(Feature):
    def __init__(self, name, param_list, return_type, expr) -> None:
        self.name = name
        self.params = param_list
        self.return_type = return_type
        self.expr = expr

########################################################################
class Expresion(Node):
    pass

class CastingDispatch(Expresion):
        
    def __init__(self, expr, atype, idf, params, static_type) -> None:
        super().__init__(static_type)
        self.expr = expr
        self.type = atype
        self.id = idf
        self.params = params

class Dispatch(Expresion):
    def __init__(self, expr, idf, params, static_type) -> None:
        super().__init__(static_type)
        self.expr = expr
        self.id = idf
        self.params = params

class StaticDispatch(Expresion):
    def __init__(self, idf, params, static_type) -> None:
        super().__init__(static_type)
        self.id = idf
        self.params = params

#######################################################################
class Statement(Expresion):
    pass

class Assing(Statement):
    def __init__(self, name, expr, static_type) -> None:
        super().__init__(static_type)
        self.id = name
        self.expr = expr

class IfThenElse(Statement):
    def __init__(self, condition, then_expr, else_expr, static_type) -> None:
        super().__init__(static_type)
        self.condition = condition
        self.then_expr = then_expr
        self.else_expr = else_expr

class While(Statement):
    def __init__(self, condition, loop_expr, static_type) -> None:
        super().__init__(static_type)
        self.condition = condition
        self.loop_expr = loop_expr

class Block(Statement):
    def __init__(self, expr_list, static_type) -> None:
        super().__init__(static_type)
        self.expr_list = expr_list

class LetIn(Statement):
    def __init__(self, assing_list, expr, static_type) -> None:
        super().__init__(static_type)
        self.assing_list = assing_list
        self.expr = expr

class Case(Statement):
    def __init__(self, expr, case_list, static_type) -> None:
        super().__init__(static_type)
        self.case_list = case_list
        self.expr = expr

##################################################################
class Binary(Expresion):
    def __init__(self, left, right, static_type) -> None:
        super().__init__(static_type)
        self.left = left
        self.right = right

class Sum(Binary):
    pass

class Rest(Binary):
    pass

class Mult(Binary):
    pass

class Div(Binary):
    pass

class Less(Binary):
    pass

class LessOrEquals(Binary):
    pass

class Equals(Binary):
    pass

###########################################################
class Atomic(Expresion):
    def __init__(self, item, static_type) -> None:
        super().__init__(static_type)
        self.item = item
    
class Void(Atomic):
    pass
    
class New(Atomic):
    pass
    
class Complement(Atomic):
    pass
    
class Neg(Atomic):
    pass
    
class Id(Atomic):
    pass
    
class Int(Atomic):
    pass
    
class Str(Atomic):
    pass

class Bool(Atomic):
    pass