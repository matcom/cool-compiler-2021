from os import error
from ..tools import VisitBase, find_type, parent_common
from .. import visitor
from ..__dependency import Type, SemanticError, Object, ErrorType, Int, Bool, Str
from ..v1_create_type import create_type_ast as AST
from . import semantic_checking_ast as ASTR
from .scope import Scope

class CoolSemanticChecking(VisitBase): 
    def __init__(self, errors) -> None:
        super().__init__(errors)
    
    @visitor.on("node")
    def visit(node, scope):
        pass

    @visitor.when(AST.Program)
    @visitor.result(ASTR.Program)
    def visit(self, node : AST.Program, scope = Scope()) : 
        return self.visit_all(node.class_list, scope),
    
    @visitor.when(AST.CoolClass)
    @visitor.result(ASTR.CoolClass)
    def visit(self, node : AST.CoolClass, scope: Scope) : 
        cls_scope : Scope = scope.create_child()
        self.current_type = node.type
        error_handler = self.get_se_handler(node)

        if node.parent_type.conforms_to(node.type):
            error_handler().add_semantic_error(f"class {self.current_type.name} has circular inheritance")        
        
        cls_scope.define_variable('self', self.current_type)
        for name, a_type in node.type.ite_attributes:
            if not cls_scope.is_local(name):
                cls_scope.define_variable(name, a_type)

        feature_list = self.visit_all(node.feature_list, cls_scope)
        return node.type, node.parent_type, feature_list
    
    @visitor.when(AST.AtrDef)
    @visitor.result(ASTR.AtrDef)
    def visit(self, node: AST.AtrDef, scope: Scope) -> ASTR.Node:
        error_handler = self.get_se_handler(node)
        
        try: 
            attr = self.current_type.parent.get_attribute(node.name)
            if not self.type_checking(attr.type, node.type):
                error_handler().add_semantic_error(f"the {node.name} attribute breaks the polymorphism rule")  
        except SemanticError as se:
            pass 

        expr = self.visit(node.expr, scope)
        if expr and not self.type_checking(node.type, expr.static_type):
            error_handler().add_type_error(f"can't save {expr.static_type.name} into {node.type.name}")  

        return node.name, node.type, expr
   
    @visitor.when(AST.FuncDef)
    @visitor.result(ASTR.FuncDef)
    def visit(self, node: AST.FuncDef, scope : Scope) -> ASTR.Node:
        error_handler = self.get_se_handler(node)
        
        try: 
            func = self.current_type.parent.get_method(node.name)

            if len(func.params) != len(node.params): 
                error_handler().add_semantic_error(f"the {node.name} function breaks the polymorphism rule because parmas number")

            for tuple_param_node, tuple_param_func in zip(node.params, func.params):
                name, t_params = tuple_param_node
                _, t_base_params = tuple_param_func
                if not self.type_checking(t_base_params, t_params):
                    error_handler().add_semantic_error(f"the {name} parameters of the {node.name} function breaks the polymorphism rule")  

            if not self.type_checking(func.return_type, node.return_type):
                error_handler().add_semantic_error(f"the {node.name} function breaks the polymorphism rule") 
        except SemanticError as se:
            pass
        
        new_scope : Scope = scope.create_child()
        for param, p_type in node.params:
            new_scope.define_variable(param, p_type)

        expr = self.visit(node.expr, new_scope)
        if not self.type_checking(node.return_type, expr.static_type):
            error_handler().add_type_error(f"Can't return {expr.static_type.name} where method in definition return {node.return_type.name}") 

        return node.name, node.params, node.return_type, expr
    
    @visitor.when(AST.CastingDispatch)
    @visitor.result(ASTR.CastingDispatch)
    def visit(self, node: AST.CastingDispatch, scope: Scope) -> ASTR.Node:
        error_handler = self.get_se_handler(node)
        
        expr = self.visit(node.expr, scope)
        if not  self.type_checking(node.type, expr.static_type):
            error_handler().add_type_error(node.type.name, expr.static_type.name ) 

        params = []
        for p in node.params:
            params.append(self.visit(p,scope))
        
        static_type = ErrorType()
        try:
            func = node.type.get_method(node.id)
            if len(func.params) != len(params):
                error_handler().add_semantic_error(f"The method {node.id} called with wrong number of arguments") 

            for tupl, exp in zip(func.params, params):
                if not self.type_checking(tupl[1], exp.static_type):
                    error_handler().add_type_error(tupl[1].name, exp.static_type.name ) 
            
            static_type = func.return_type
        except SemanticError:
            error_handler().add_attribute_error(node.type.name, node.id ) 

        return expr, node.type, node.id, params, expr.static_type if static_type.is_self_type else static_type

    @visitor.when(AST.Dispatch)
    @visitor.result(ASTR.Dispatch)
    def visit(self, node: AST.Dispatch, scope: Scope) -> ASTR.Node:
        error_handler = self.get_se_handler(node)
        expr = self.visit(node.expr, scope) 

        params = []
        for p in node.params:
            params.append(self.visit(p,scope))
        
        static_type = ErrorType()
        try:
            func = expr.static_type.get_method(node.id)

            if len(func.params) != len(params):
                error_handler().add_semantic_error(f"The method {node.id} called with wrong number of arguments") 
            
            for tupl, exp in zip(func.params, params):
                if not self.type_checking(tupl[1], exp.static_type):
                    error_handler().add_type_error(tupl[1].name, exp.static_type.name ) 
            
            static_type = func.return_type
        except SemanticError:
            error_handler().add_attribute_error(expr.static_type.name, node.id ) 

        return expr, node.id, params, expr.static_type if static_type.is_self_type else static_type
       
    @visitor.when(AST.StaticDispatch)
    @visitor.result(ASTR.StaticDispatch)
    def visit(self, node: AST.StaticDispatch, scope: Scope) -> ASTR.Node:
        error_handler = self.get_se_handler(node)

        params = []
        for p in node.params:
            params.append(self.visit(p,scope))
        
        static_type = ErrorType()
        try:
            func = self.current_type.get_method(node.id)

            if len(func.params) != len(params):
                error_handler().add_semantic_error(f"The method {node.id} called with wrong number of arguments") 

            for tupl, exp in zip(func.params, params):
                if not self.type_checking(tupl[1], exp.static_type):
                    error_handler().add_type_error(tupl[1].name, exp.static_type.name ) 
            
            static_type = func.return_type
        except SemanticError:
            error_handler().add_attribute_error(self.current_type.name, node.id ) 

        return node.id, params, static_type

    @visitor.when(AST.Assing)
    @visitor.result(ASTR.Assing)
    def visit(self, node: AST.Assing, scope: Scope) -> ASTR.Node:
        error_handler = self.get_se_handler(node)
        try: 
            v = scope.find_variable(node.id)
            static_type = v.type
        except SemanticError:
            error_handler().add_name_error(node.id)
            static_type = ErrorType() 
        
        expr = self.visit(node.expr, scope)
        if not self.type_checking(static_type, expr.static_type):
            error_handler().add_type_error(f"Can't  assign {expr.static_type.name} intro {static_type.name}")
       
        return node.id, expr, expr.static_type 
    
    @visitor.when(AST.IfThenElse)
    @visitor.result(ASTR.IfThenElse)
    def visit(self, node: AST.IfThenElse, scope: Scope) -> ASTR.Node:
        error_handler = self.get_se_handler(node)
        cond = self.visit(node.condition, scope)
        if not self.type_checking(Bool(), cond.static_type):
            error_handler().add_type_error("Bool", cond.static_type.name)

        then_expr = self.visit(node.then_expr, scope)
        else_expr = self.visit(node.else_expr, scope)

        return cond, then_expr, else_expr, parent_common(then_expr.static_type, else_expr.static_type)

    @visitor.when(AST.While)
    @visitor.result(ASTR.While)
    def visit(self, node: AST.While, scope: Scope) -> ASTR.Node:
        error_handler = self.get_se_handler(node)
        cond = self.visit(node.condition, scope)
        if not self.type_checking(Bool(), cond.static_type):
            error_handler().add_type_error("Bool", cond.static_type.name)

        return cond, self.visit(node.loop_expr, scope), Object()

    @visitor.when(AST.Block)
    @visitor.result(ASTR.Block)
    def visit(self, node: AST.Block, scope: Scope) -> ASTR.Node:
        block_list= []
        for b in node.expr_list:
            block_list.append(self.visit(b, scope))
        
        return block_list, block_list[-1].static_type

    @visitor.when(AST.LetIn)
    @visitor.result(ASTR.LetIn)
    def visit(self, node: AST.LetIn, scope: Scope) -> ASTR.Node:
        error_handler = self.get_se_handler(node)
        new_scope = scope.create_child()
        
        assing_list = []
        for name, atype, expr in node.assing_list:
            if expr: 
                exp = self.visit(expr, new_scope)
                if not self.type_checking(atype, exp.static_type):
                    error_handler().add_type_error(atype.name, exp.static_type.name)
            else: exp = None    
            
            assing_list.append((name, atype, exp))
            new_scope.define_variable(name,atype)

        expr = self.visit(node.expr, new_scope)
        return assing_list, expr, expr.static_type

    @visitor.when(AST.Case)
    @visitor.result(ASTR.Case)
    def visit(self, node: AST.Case, scope: Scope) -> ASTR.Node:
        expr_cond = self.visit(node.expr, scope)

        static_type = None
        case_list = []
        for name, atype , expr in node.case_list:
            new_scope = scope.create_child()
            new_scope.define_variable(name, atype)
            exp = self.visit(expr, new_scope)

            if static_type is None: static_type = exp.static_type
            else: static_type = parent_common(static_type, exp.static_type)
            case_list.append((name, atype, exp))
        
        return expr_cond, case_list, static_type

    @visitor.when(AST.Sum)
    @visitor.result(ASTR.Sum)
    def visit(self, node: AST.Sum, scope: Scope) -> ASTR.Node:
        error_handler = self.get_se_handler(node)
        left = self.visit(node.left, scope)
        if not self.type_checking(Int(), left.static_type):
            error_handler().add_type_error("Int", left.static_type.name)

        right = self.visit(node.right, scope)
        if not self.type_checking(Int(), right.static_type):
            error_handler().add_type_error("Int", right.static_type.name)
        
        return left, right, Int()

    @visitor.when(AST.Rest)
    @visitor.result(ASTR.Rest)
    def visit(self, node: AST.Rest, scope: Scope) -> ASTR.Node:
        error_handler = self.get_se_handler(node)

        left = self.visit(node.left, scope)
        if not self.type_checking(Int(), left.static_type):
            error_handler().add_type_error("Int", left.static_type.name)

        right = self.visit(node.right, scope)
        if not self.type_checking(Int(), right.static_type):
            error_handler().add_type_error("Int", right.static_type.name)
        
        return left, right, Int()

    @visitor.when(AST.Mult)
    @visitor.result(ASTR.Mult)
    def visit(self, node: AST.Mult, scope: Scope) -> ASTR.Node:
        error_handler = self.get_se_handler(node)

        left = self.visit(node.left, scope)
        if not self.type_checking(Int(), left.static_type):
            error_handler().add_type_error("Int", left.static_type.name)

        right = self.visit(node.right, scope)
        if not self.type_checking(Int(), right.static_type):
            error_handler().add_type_error("Int", right.static_type.name)
        
        return left, right, Int()

    @visitor.when(AST.Div)
    @visitor.result(ASTR.Div)
    def visit(self, node: AST.Div, scope: Scope) -> ASTR.Node:
        error_handler = self.get_se_handler(node)

        left = self.visit(node.left, scope)
        if not self.type_checking(Int(), left.static_type):
            error_handler().add_type_error("Int", left.static_type.name)

        right = self.visit(node.right, scope)
        if not self.type_checking(Int(), right.static_type):
            error_handler().add_type_error("Int", right.static_type.name)
        
        return left, right, Int()

    @visitor.when(AST.Less)
    @visitor.result(ASTR.Less)
    def visit(self, node: AST.Less, scope: Scope) -> ASTR.Node:
        error_handler = self.get_se_handler(node)

        left = self.visit(node.left, scope)
        if not self.type_checking(Int(), left.static_type):
            error_handler().add_type_error("Int", left.static_type.name)

        right = self.visit(node.right, scope)
        if not self.type_checking(Int(), right.static_type):
            error_handler().add_type_error("Int", right.static_type.name)
        
        return left, right, Bool()

    @visitor.when(AST.LessOrEquals)
    @visitor.result(ASTR.LessOrEquals)
    def visit(self, node: AST.LessOrEquals, scope: Scope) -> ASTR.Node:
        error_handler = self.get_se_handler(node)

        left = self.visit(node.left, scope)
        if not self.type_checking(Int(), left.static_type):
            error_handler().add_type_error("Int", left.static_type.name)

        right = self.visit(node.right, scope)
        if not self.type_checking(Int(), right.static_type):
            error_handler().add_type_error("Int", right.static_type.name)
        
        return left, right, Bool()

    @visitor.when(AST.Equals)
    @visitor.result(ASTR.Equals)
    def visit(self, node: AST.Equals, scope: Scope) -> ASTR.Node:
        error_handler = self.get_se_handler(node)
        left = self.visit(node.left, scope)
        right = self.visit(node.right, scope)
        list_type = [ Str, Int, Bool]
  
        if type(left.static_type) in list_type or type(right.static_type) in list_type:
            if not left.static_type == right.static_type:
                error_handler().add_type_error(left.static_type.name, right.static_type.name)
        
        return left, right, Bool()

    @visitor.when(AST.Void)
    @visitor.result(ASTR.Void)
    def visit(self, node: AST.Void, scope: Scope) -> ASTR.Node:
        return self.visit(node.item, scope), Bool()
        
    @visitor.when(AST.New)
    @visitor.result(ASTR.New)
    def visit(self, node: AST.New, scope: Scope) -> ASTR.Node:
        return node.item, node.item

    @visitor.when(AST.Complement)
    @visitor.result(ASTR.Complement)
    def visit(self, node: AST.Complement, scope: Scope) -> ASTR.Node:
        error_handler = self.get_se_handler(node)
        expr = self.visit(node.item, scope)
        if not self.type_checking(Int(), expr.static_type):
            error_handler().add_type_error("Int", expr.static_type.name)
        return expr, Int()

    @visitor.when(AST.Neg)
    @visitor.result(ASTR.Neg)
    def visit(self, node: AST.Neg, scope: Scope) -> ASTR.Node:
        error_handler = self.get_se_handler(node)
        expr = self.visit(node.item, scope)
        if not self.type_checking(Bool(), expr.static_type):
            error_handler().add_type_error("Bool", expr.static_type.name)
        return expr, Bool()

    @visitor.when(AST.Id)
    @visitor.result(ASTR.Id)
    def visit(self, node: AST.Id, scope: Scope) -> ASTR.Node:
        error_handler = self.get_se_handler(node)

        try: 
            v = scope.find_variable(node.item)
            return node.item, v.type
        except AttributeError: pass
        except SemanticError: pass

        error_handler().add_name_error(node.item)
        return node.item, ErrorType()         

    @visitor.when(AST.Int)
    @visitor.result(ASTR.Int)
    def visit(self, node: AST.Int, scope: Scope) -> ASTR.Node:
        return node.item, Int()

    @visitor.when(AST.Bool)
    @visitor.result(ASTR.Bool)
    def visit(self, node: AST.Bool, scope: Scope) -> ASTR.Node:
        return node.item, Bool()

    @visitor.when(AST.Str)
    @visitor.result(ASTR.Str)
    def visit(self, node: AST.Str, scope: Scope) -> ASTR.Node:
        return node.item, Str()