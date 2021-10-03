from typing import SupportsComplex
from .ASTs import ast1_create_type_return as AST_init
from .ASTs import ast2_semantic_checking_return as AST_result
from . import visitor
from .scope import Scope
from .__dependency import Type, SemanticError, ErrorType, Int, Bool, Object, Str
from .tools import VisitorBase, type_checking, find_variable, parent_common
from .semantic_checking_funcs import *

class SemanticChecking(VisitorBase):
    def __init__(self, error) -> None:
        super().__init__(error)
        self.casting_error_type = lambda a,b : a if not type(a) is ErrorType else b
    
    @visitor.on("node")
    def visit(self, node, scope) -> AST_result.Node:
        pass

 

    
    @visitor.when(AST_init.AtrDef)
    @visitor.result(AST_result.AtrDef)
    def visit(self, node: AST_init.AtrDef, scope: Scope) -> AST_result.Node:
        error_handler = self.get_se_handler(node)
        
        try: 
            attr = self.current_type.parent.get_attribute(node.name)
            if not self.type_checking(attr.type, node.type):
                error_handler().add_semantic_error(f"the {node.name} attribute breaks the polymorphism rule")  
        except SemanticError as se:
            pass 

        expr = self.visit(node.expr, scope)
        if not self.type_checking(node.type, expr.static_type):
            error_handler().add_semantic_error(f"can't save {expr.static_type.name} into {node.type}")  

        return node.name, node.type, expr

    @visitor.when(AST_init.FuncDef)
    @visitor.result(AST_result.FuncDef)
    def visit(self, node: AST_init.FuncDef, scope : Scope) -> AST_result.Node:
        error_handler = self.get_se_handler(node)
        
        try: 
            func = self.current_type.parent.get_method(node.name)

            for pn, fn in zip(node.params, func.params):
                name, tparams = pn
                _, tbase_params = fn
                if not self.type_checking(tbase_params, tparams):
                    error_handler().add_semantic_error(f"the {name} parameters of the {node.name} function breaks the polymorphism rule")  

            if not self.type_checking(func.return_type, node.return_type):
                error_handler().add_semantic_error(f"the {node.name} function breaks the polymorphism rule") 
        except SemanticError as se:
            pass
        
        new_scope : Scope = scope.create_child()
        for param, ptype in node.params:
            new_scope.define_variable(param, ptype)

        expr = self.visit(node.expr, new_scope)
        
        if not type_checking(node.return_type, expr.static_type):
            self.cool_error(node.lineno, node.index).add_type_error(node.return_type.name, expr.static_type.name ) 

        return node.name, node.params, node.return_type, expr

    @visitor.when(AST_init.CastingDispatch)
    @visitor.result(AST_result.CastingDispatch)
    def visit(self, node: AST_init.CastingDispatch, scope: Scope) -> AST_result.Node:
        
        expr = self.visit(node.expr, scope)
        if not expr.static_type.conforms_to(node.type):
            self.cool_error(node.lineno, node.index).add_type_error(node.type, expr.static_type.name ) 

        params = []
        for p in node.params:
            params.append(self.visit(p,scope))
        
        static_type = ErrorType()
        try:
            func = node.type.get_method(node.id)
            for tupl, exp in zip(func.params, params):
                if not exp.static_type.conforms_to(tupl[1]):
                    self.cool_error(node.lineno, node.index).add_type_error(tupl[1].name, exp.static_type.name ) 
            
            static_type = func.return_type
        except SemanticError:
            self.cool_error(node.lineno, node.index).add_attribute_error(node.type, node.id ) 

        return expr, node.type, node.id, params, static_type

    @visitor.when(AST_init.Dispatch)
    @visitor.result(AST_result.Dispatch)
    def visit(self, node: AST_init.Dispatch, scope: Scope) -> AST_result.Node:
        expr = self.visit(node.expr, scope) 

        params = []
        for p in node.params:
            params.append(self.visit(p,scope))
        
        static_type = ErrorType()
        try:
            func = expr.static_type.get_method(node.id)
            for tupl, exp in zip(func.params, params):
                if not exp.static_type.conforms_to(tupl[1]):
                    self.cool_error(node.lineno, node.index).add_type_error(tupl[1].name, exp.static_type.name ) 
            
            static_type = func.return_type
        except SemanticError:
            self.cool_error(node.lineno, node.index).add_attribute_error(expr.static_type.name, node.id ) 

        return expr, node.id, params, static_type
       
    @visitor.when(AST_init.StaticDispatch)
    @visitor.result(AST_result.StaticDispatch)
    def visit(self, node: AST_init.StaticDispatch, scope: Scope) -> AST_result.Node:
        params = []
        for p in node.params:
            params.append(self.visit(p,scope))
        
        static_type = ErrorType()
        try:
            func = self.current_type.get_method(node.id)
            for tupl, exp in zip(func.params, params):
                if not exp.static_type.conforms_to(tupl[1]):
                    self.cool_error(node.lineno, node.index).add_type_error(tupl[1].name, exp.static_type.name ) 
            
            static_type = func.return_type
        except SemanticError:
            self.cool_error(node.lineno, node.index).add_attribute_error(self.current_type.name, node.id ) 

        return node.id, params, static_type

    @visitor.when(AST_init.Assing)
    @visitor.result(AST_result.Assing)
    def visit(self, node: AST_init.Assing, scope: Scope) -> AST_result.Node:
        try: 
            v = scope.find_variable(node.id)
            static_type = v.type
        except SemanticError:
            self.cool_error(node.lineno, node.index).add_name_error(node.id)
            static_type = ErrorType() 
        
        expr = self.visit(node.expr, scope)
        self.type_checking(static_type, expr.static_type, node)
       
        return node.id, expr, self.casting_error_type(static_type, expr.static_type)      
    
    @visitor.when(AST_init.IfThenElse)
    @visitor.result(AST_result.IfThenElse)
    def visit(self, node: AST_init.IfThenElse, scope: Scope) -> AST_result.Node:
        cond = self.visit(node.condition, scope)
        self.type_checking(Bool(), cond.static_type, node)

        then_expr = self.visit(node.then_expr, scope)
        else_expr = self.visit(node.else_expr, scope)

        return cond, then_expr, else_expr, self.parent_common(then_expr.static_type, else_expr.static_type)

    @visitor.when(AST_init.While)
    @visitor.result(AST_result.While)
    def visit(self, node: AST_init.While, scope: Scope) -> AST_result.Node:
        cond = self.visit(node.condition, scope)
        self.type_checking(Bool(), cond.static_type, node)

        return cond, self.visit(node.loop_expr, scope), Object()

    @visitor.when(AST_init.Block)
    @visitor.result(AST_result.Block)
    def visit(self, node: AST_init.Block, scope: Scope) -> AST_result.Node:
        block_list= []
        for b in node.expr_list:
            block_list.append(self.visit(b, scope))
        
        return block_list, block_list[-1].static_type

    @visitor.when(AST_init.LetIn)
    @visitor.result(AST_result.LetIn)
    def visit(self, node: AST_init.LetIn, scope: Scope) -> AST_result.Node:
        new_scope = scope.create_child()
        
        assing_list = []
        for name, atype, expr in node.assing_list:
            exp = self.visit(expr, new_scope)
            self.type_checking(atype, exp.static_type, node)
            assing_list.append((name, atype, exp))
            new_scope.define_variable(name,atype)

        expr = self.visit(node.expr, new_scope)
        return assing_list, expr, expr.static_type

    @visitor.when(AST_init.Case)
    @visitor.result(AST_result.Case)
    def visit(self, node: AST_init.Case, scope: Scope) -> AST_result.Node:
        expr_cond = self.visit(node.expr, scope)

        static_type = None
        case_list = []
        for name, atype , expr in node.case_list:
            new_scope = scope.create_child()
            new_scope.define_variable(name, atype)
            exp = self.visit(expr, new_scope)

            if static_type is None: static_type = exp.static_type
            else: static_type = self.parent_common(static_type, exp.static_type)
            case_list.append((name, atype, exp))
        
        return expr_cond, case_list, static_type

    @visitor.when(AST_init.Sum)
    @visitor.result(AST_result.Sum)
    def visit(self, node: AST_init.Sum, scope: Scope) -> AST_result.Node:
        left = self.visit(node.left, scope)
        self.type_checking(Int(), left.static_type, node)

        right = self.visit(node.right, scope)
        self.type_checking(Int(), right.static_type, node)
        
        return left, right, Int()

    @visitor.when(AST_init.Rest)
    @visitor.result(AST_result.Rest)
    def visit(self, node: AST_init.Rest, scope: Scope) -> AST_result.Node:
        left = self.visit(node.left, scope)
        self.type_checking(Int(), left.static_type, node)

        right = self.visit(node.right, scope)
        self.type_checking(Int(), right.static_type, node)
        
        return left, right, Int()

    @visitor.when(AST_init.Mult)
    @visitor.result(AST_result.Mult)
    def visit(self, node: AST_init.Mult, scope: Scope) -> AST_result.Node:
        left = self.visit(node.left, scope)
        self.type_checking(Int(), left.static_type, node)

        right = self.visit(node.right, scope)
        self.type_checking(Int(), right.static_type, node)
        
        return left, right, Int()

    @visitor.when(AST_init.Div)
    @visitor.result(AST_result.Div)
    def visit(self, node: AST_init.Div, scope: Scope) -> AST_result.Node:
        left = self.visit(node.left, scope)
        self.type_checking(Int(), left.static_type, node)

        right = self.visit(node.right, scope)
        self.type_checking(Int(), right.static_type, node)
        
        return left, right, Int()

    @visitor.when(AST_init.Less)
    @visitor.result(AST_result.Less)
    def visit(self, node: AST_init.Less, scope: Scope) -> AST_result.Node:
        left = self.visit(node.left, scope)
        self.type_checking(Int(), left.static_type, node)

        right = self.visit(node.right, scope)
        self.type_checking(Int(), right.static_type, node)
        
        return left, right, Bool()

    @visitor.when(AST_init.LessOrEquals)
    @visitor.result(AST_result.LessOrEquals)
    def visit(self, node: AST_init.LessOrEquals, scope: Scope) -> AST_result.Node:
        left = self.visit(node.left, scope)
        self.type_checking(Int(), left.static_type, node)

        right = self.visit(node.right, scope)
        self.type_checking(Int(), right.static_type, node)
        
        return left, right, Bool()

    @visitor.when(AST_init.Equals)
    @visitor.result(AST_result.Equals)
    def visit(self, node: AST_init.Equals, scope: Scope) -> AST_result.Node:
        left = self.visit(node.left, scope)
        right = self.visit(node.right, scope)
        list_type = [ Str, Int, Bool]
        if type(left.static_type) in list_type or type(right.static_type) in list_type:
            if left.static_type == right.static_type:
                self.cool_error(node.lineno, node.index).add_type_error(left.static_type.name, right.static_type.name)
        
        return left, right, Bool()

    @visitor.when(AST_init.Void)
    @visitor.result(AST_result.Void)
    def visit(self, node: AST_init.Void, scope: Scope) -> AST_result.Node:
        return self.visit(node.item, scope), Bool()
        
    @visitor.when(AST_init.New)
    @visitor.result(AST_result.New)
    def visit(self, node: AST_init.New, scope: Scope) -> AST_result.Node:
        return node.item, node.item

    @visitor.when(AST_init.Complement)
    @visitor.result(AST_result.Complement)
    def visit(self, node: AST_init.Complement, scope: Scope) -> AST_result.Node:
        expr = self.visit(node.item, scope)
        self.type_checking(Int(), expr.static_type, node)
        return expr, Int()

    @visitor.when(AST_init.Neg)
    @visitor.result(AST_result.Neg)
    def visit(self, node: AST_init.Neg, scope: Scope) -> AST_result.Node:
        expr = self.visit(node.item, scope)
        self.type_checking(Bool(), expr.static_type)
        return expr, Bool()

    @visitor.when(AST_init.Id)
    @visitor.result(AST_result.Id)
    def visit(self, node: AST_init.Id, scope: Scope) -> AST_result.Node:
        try: 
            v = scope.find_variable(node.item)
            return node.item, v.type
        except SemanticError:
            self.cool_error(node.lineno, node.index).add_name_error(node.item)
            return node.item, ErrorType()         

    @visitor.when(AST_init.Int)
    @visitor.result(AST_result.Int)
    def visit(self, node: AST_init.Int, scope: Scope) -> AST_result.Node:
        return node.item, Int()

    @visitor.when(AST_init.Bool)
    @visitor.result(AST_result.Bool)
    def visit(self, node: AST_init.Bool, scope: Scope) -> AST_result.Node:
        return node.item, Bool()

    @visitor.when(AST_init.Str)
    @visitor.result(AST_result.Str)
    def visit(self, node: AST_init.Str, scope: Scope) -> AST_result.Node:
        return node.item, Str()
