from .. import visitor
from ..__dependency import Type, SemanticError, Object, ErrorType, Int, Bool, Str
from ..v0_parser_return import factory_return_ast as AST
from . import create_type_ast as ASTR
from ..tools import VisitBase, find_type

class CoolCreateType(VisitBase):
    def __init__(self, errors) -> None:
        self.cool_error = errors
        self.current_type : Type = None
        self.global_types = {}

    def get_parent_type(self, node, error_handler):
        if node.parent is None: return Object()
            
        find_result = find_type(node.parent, self.global_types)
        parent_type = find_result.get_value( if_fail_do= error_handler().add_semantic_error )
            
        if parent_type.is_shield or parent_type.name == self.current_type.name: 
            error_handler().add_semantic_error( f"class {self.current_type.name} can't be inherited from {parent_type.name}" )
            return ErrorType()

        return parent_type 


    @visitor.on("node")
    def visit(node):
        pass
    
    @visitor.when(AST.Program)
    @visitor.result(ASTR.Program)
    def visit(self, node : AST.Program) : 
        for name, lineno, index in node.names_list:
            if name in self.global_types:
                self.cool_error(lineno, index)
                self.cool_error.add_semantic_error(f"{name} is already defined")
            else: self.global_types[name] = Type(name)

        class_list = self.visit_all(node.class_list)
        return class_list,

    @visitor.when(AST.CoolClass)
    @visitor.result(ASTR.CoolClass)
    def visit(self, node : AST.CoolClass) : 
        self.current_type = self.global_types[node.name]
        error_handler = self.get_se_handler(node)
        
        parent_type = self.get_parent_type(node, error_handler)
        try: self.current_type.set_parent(parent_type)
        except SemanticError: pass

        feature_list = self.visit_all(node.feature_list)
        
        return self.current_type, parent_type, feature_list

    @visitor.when(AST.AtrDef)
    @visitor.result(ASTR.AtrDef)
    def visit(self, node : AST.AtrDef) : 
        error_handler = self.get_se_handler(node)
        
        atype = self.get_type(node.type, error_handler)
        self.current_type.define_attribute(node.name, atype)

        expr = self.visit(node.expr)
        return node.name, atype, expr
    
    @visitor.when(AST.FuncDef)
    @visitor.result(ASTR.FuncDef)
    def visit(self, node : AST.FuncDef) : 
        error_handler = self.get_se_handler(node)
        
        return_type = self.get_type(node.return_type, error_handler)

        params = []
        for name, ptype in node.params:
            param_type = self.get_type(ptype, error_handler)
            params.append((name, param_type))

        self.current_type.define_method(node.name, params, return_type)
        expr = self.visit(node.expr)
        return node.name, params, return_type, expr  

    @visitor.when(AST.CastingDispatch)
    @visitor.result(ASTR.CastingDispatch)
    def visit(self, node: AST.CastingDispatch):
        error = self.get_se_handler(node)
        return tuple([
            self.visit(node.expr),
            self.get_type(node, error),
            node.id,
            self.visit_all(node.params)
        ])

    @visitor.when(AST.Dispatch)
    @visitor.result(ASTR.Dispatch)
    def visit(self, node: AST.Dispatch):
        return tuple([
            self.visit(node.expr),
            node.id,
            self.visit_all(node.params)
        ])

    @visitor.when(AST.StaticDispatch)
    @visitor.result(ASTR.StaticDispatch)
    def visit(self, node: AST.StaticDispatch):
        return tuple([
            node.id,
            self.visit_all(node.params)
        ])

    @visitor.when(AST.Assing)
    @visitor.result(ASTR.Assing)
    def visit(self, node: AST.Assing):
        return tuple([
            node.id,
            self.visit(node.expr)
        ])
    
    @visitor.when(AST.IfThenElse)
    @visitor.result(ASTR.IfThenElse)
    def visit(self, node: AST.IfThenElse):
        return tuple([
            self.visit(node.condition),
            self.visit(node.then_expr),
            self.visit(node.else_expr),
        ])

    @visitor.when(AST.While)
    @visitor.result(ASTR.While)
    def visit(self, node: AST.While):
        return tuple([
            self.visit(node.condition),
            self.visit(node.loop_expr),
        ])

    @visitor.when(AST.While)
    @visitor.result(ASTR.While)
    def visit(self, node: AST.While):
        return tuple([
            self.visit(node.condition),
            self.visit(node.loop_expr),
        ])


    @visitor.when(AST.Block)
    @visitor.result(ASTR.Block)
    def visit(self, node: AST.Block):
        return tuple([
            self.visit_all(node.expr_list),
        ])
    
    @visitor.when(AST.LetIn)
    @visitor.result(ASTR.LetIn)
    def visit(self, node : AST.LetIn) : 
        error_handler = self.get_se_handler(node)

        assing_list = []
        for name, atype, expr in node.assing_list:
            rtype = self.get_type(atype, error_handler) 
            assing_list.append((name, rtype, self.visit(expr)))
 
        return assing_list, self.visit(node.expr)

    @visitor.when(AST.Case)
    @visitor.result(ASTR.Case)
    def visit(self, node : AST.Case) : 
        error_handler = self.get_se_handler(node)

        case_list = []
        for name, atype, expr in node.case_list:
            rtype = self.get_type(atype, error_handler) 
            case_list.append((name, rtype, self.visit(expr)))
 
        return self.visit(node.expr), case_list

    @visitor.when(AST.Sum)
    @visitor.result(ASTR.Sum)
    def visit(self, node: AST.Sum):
        return tuple([
            self.visit(node.left),
            self.visit(node.right),
        ])

    @visitor.when(AST.Rest)
    @visitor.result(ASTR.Rest)
    def visit(self, node: AST.Rest):
        return tuple([
            self.visit(node.left),
            self.visit(node.right),
        ])

    @visitor.when(AST.Mult)
    @visitor.result(ASTR.Mult)
    def visit(self, node: AST.Mult):
        return tuple([
            self.visit(node.left),
            self.visit(node.right),
        ])

    @visitor.when(AST.Div)
    @visitor.result(ASTR.Div)
    def visit(self, node: AST.Div):
        return tuple([
            self.visit(node.left),
            self.visit(node.right),
        ])

    @visitor.when(AST.Less)
    @visitor.result(ASTR.Less)
    def visit(self, node: AST.Less):
        return tuple([
            self.visit(node.left),
            self.visit(node.right),
        ])

    @visitor.when(AST.LessOrEquals)
    @visitor.result(ASTR.LessOrEquals)
    def visit(self, node: AST.LessOrEquals):
        return tuple([
            self.visit(node.left),
            self.visit(node.right),
        ])

    @visitor.when(AST.Equals)
    @visitor.result(ASTR.Equals)
    def visit(self, node: AST.Equals):
        return tuple([
            self.visit(node.left),
            self.visit(node.right),
        ])

    @visitor.when(AST.Void)
    @visitor.result(ASTR.Void)
    def visit(self, node: AST.Void):
        return tuple([
            self.visit(node.item),
        ])

    @visitor.when(AST.New)
    @visitor.result(ASTR.New)
    def visit(self, node: AST.New):
        error =  self.get_se_handler(node)
        return tuple([
            self.get_type(node.item, error),
        ])

    @visitor.when(AST.Complement)
    @visitor.result(ASTR.Complement)
    def visit(self, node: AST.Complement):
        return tuple([
            self.visit(node.item),
        ])

    @visitor.when(AST.Neg)
    @visitor.result(ASTR.Neg)
    def visit(self, node: AST.Neg):
        return tuple([
            self.visit(node.item),
        ])

    @visitor.when(AST.Id)
    @visitor.result(ASTR.Id)
    def visit(self, node: AST.Id):
        return tuple([
            node.item,
        ])

    @visitor.when(AST.Int)
    @visitor.result(ASTR.Int)
    def visit(self, node: AST.Int):
        return Int(),

    @visitor.when(AST.Bool)
    @visitor.result(ASTR.Bool)
    def visit(self, node: AST.Bool):
        return Bool(), 

    @visitor.when(AST.Str)
    @visitor.result(ASTR.Str)
    def visit(self, node: AST.Str):
        return Str(), 
