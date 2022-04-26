from Semantic.types import cyclic_inheritance
from Semantic.scope import COOL_Scope
from Semantic.errors_types import *
from Semantic import visitor
from Parser import ast
import sys

class COOL_Semantic_Checker:
    
    def __init__(self):
        self.errors = False
    
    @visitor.on('node')
    def visit(self, node, scope):
        pass
    
    
    @visitor.when(ast.Program)
    def visit(self, node : ast.Program, scope_root = None):
        """
        node.classes -> [ Class ... ]
        """
        scope_root = COOL_Scope(None, None)
        
        for _class in node.classes:
            if not scope_root.set_type(_class.name):
                sys.stdout.write(f'({_class.lineno}, {_class.linepos}) - {SEMERROR2 % _class.name}\n')
                self.errors = True
                return None
            COOL_Scope(_class.name, scope_root)
        
        for (_class, _scope) in zip(node.classes, scope_root.children):
            if not _class.parent is None and _scope.get_type(_class.parent) is None:
                sys.stdout.write(f'({_class.lineno}, {_class.linepos}) - {TYPERROR14 % (_class.name, _class.parent)}\n')
                self.errors = True
                return None
            elif _class.parent in _scope.ctype.not_inherits_type:
                sys.stdout.write(f'({_class.lineno}, {_class.linepos}) - {SEMERROR3 % (_class.name, _class.parent)}\n')
                self.errors = True
                return None
            else:
                parent = _scope.ctype.OBJECT if _class.parent is None else _scope.get_type(_class.parent)
                _scope.ctype.defined_types[_class.name].parent = parent
            if cyclic_inheritance(_scope.get_type(_class.name)):
                sys.stdout.write(f'({_class.lineno}, {_class.linepos}) - {SEMERROR6 % (_class.name, _class.name)}\n')
                self.errors = True
                return None
            
        for (_class, _scope) in zip(node.classes, scope_root.children):
            for _method in _class.features:
                if type(_method) is ast.ClassMethod:
                    if _scope.get_var(_class.name, _method.name) == _scope.ctype.SELF:
                        sys.stdout.write(f'({_method.lineno}, {_method.linepos}) - {SEMERROR12 % "a method"}\n')
                        self.errors = True
                        return None
                    
                    return_type = _scope.get_type(_method.return_type)
        
                    if return_type is None:
                        sys.stdout.write(f'({_method.lineno}, {_method.linepos}) - {TYPERROR11 % _method.return_type}\n')
                        self.errors = True
                        return None
                    
                    func = {'formal_params':{}, 'return_type': return_type}
                    for param in _method.formal_params:
                        func['formal_params'][param.name] = _scope.get_type(param.param_type)
                    
                    ret = _scope.get_type(_class.name).add_func(_method.name, func)
                    if ret is None:
                        sys.stdout.write(f'({_method.lineno}, {_method.linepos}) - {SEMERROR8 % _method.name}\n')
                        self.errors = True
                        return None
                    
                    if not ret:
                        sys.stdout.write(f'({_method.lineno}, {_method.linepos}) - {SEMERROR5 % _method.name}\n')
                        self.errors = True
                        return None
                
                else:
                    if _scope.get_var(_class.name, _method.name) == _scope.ctype.SELF:
                        sys.stdout.write(f'({_method.lineno}, {_method.linepos}) - {SEMERROR12 % "an attribute"}\n')
                        self.errors = True
                        return None
            
                    attr_type = _scope.get_type(_method.attr_type)
        
                    if attr_type is None:
                        sys.stdout.write(f'({_method.lineno}, {_method.linepos}) - {TYPERROR11 % _method.attr_type}\n')
                        self.errors = True
                        return None
                    
                    ret = _scope.get_type(_class.name).add_attr(_method.name, attr_type, _method.init_expr)
                    if ret is None:
                        sys.stdout.write(f'({_method.lineno}, {_method.linepos}) - {SEMERROR9 % _method.name}\n')
                        self.errors = True
                        return None
                    
                    if not ret:
                        sys.stdout.write(f'({_method.lineno}, {_method.linepos}) - {SEMERROR4 % _method.name}\n')
                        self.errors = True
                        return None
                             
        for _class1 in node.classes:
            for _class2 in node.classes:
                if _class2.name == _class1.parent:
                    _class1.parent = _class2
                    
        for (_class, _scope) in zip(node.classes, scope_root.children):
            if self.visit(_class, _scope) is None:
                return None
        
        return scope_root
    
    
    @visitor.when(ast.Class)
    def visit(self, node, scope):
        """
        node.name -> str
        node.parent -> Class
        node.features -> [ ClassMethod/ClassAttribute ... ]
        """
        for meth in node.features:
            if self.visit(meth, COOL_Scope(node.name, scope)) is None:
                return None
        return node
    
    
    @visitor.when(ast.ClassMethod)
    def visit(self, node, scope):
        """
        node.name -> str
        node.formal_params -> [ FormalParameter ... ]
        node.return_type -> str
        node.body -> Expr
        """
        return_type = scope.get_type(node.return_type)

        for param in node.formal_params:
            if scope.get_var(scope.classname, param.name) == scope.ctype.SELF:
                sys.stdout.write(f'({param.lineno}, {param.linepos}) - {SEMERROR12 % "a formal parameter"}\n')
                self.errors = True
                return None
            if self.visit(param, scope) is None:
                return None
        
        body_type = scope.get_type(self.visit(node.body, scope))
        
        if body_type is None:
            return None
        
        if body_type == scope.ctype.SELF or return_type == scope.ctype.SELF:
            if body_type != scope.ctype.SELF:
                return_type = scope.get_type(scope.classname)
            elif return_type != scope.ctype.SELF:
                body_type = scope.get_type(scope.classname)
        
        if not (body_type <= return_type):
            sys.stdout.write(f'({node.body.lineno}, {node.body.linepos}) - {TYPERROR13 % (body_type, node.name, return_type)}\n')
            self.errors = True
            return None
        
        node.static_type = return_type
        return return_type
    
    
    @visitor.when(ast.ClassAttribute)
    def visit(self, node, scope):
        """
        node.name -> str
        node.attr_type -> str
        node.init_expr -> Expr
        """
        attr_type = scope.get_type(node.attr_type)
        
        if not node.init_expr is None:
            expr_type = scope.get_type(self.visit(node.init_expr, scope))
            
            if expr_type is None:
                if not self.errors:
                    sys.stdout.write(f'({node.init_expr.lineno}, {node.init_expr.linepos}) - {NAMERROR1 % node.init_expr.name}\n')
                self.errors = True
                return None
            
            if expr_type == scope.ctype.SELF or attr_type == scope.ctype.SELF:
                if expr_type != scope.ctype.SELF:
                    attr_type = scope.get_type(scope.classname)
                elif attr_type != scope.ctype.SELF:
                    expr_type = scope.get_type(scope.classname)
            
            if expr_type == scope.ctype.VOID:
                sys.stdout.write(f'({node.init_expr.lineno}, {node.init_expr.linepos}) - {RNTERROR1}\n')
                self.errors = True
                return None

            if not (expr_type <= attr_type):
                sys.stdout.write(f'({node.init_expr.lineno}, {node.init_expr.linepos}) - {TYPERROR12 % (expr_type, node.name, attr_type)}\n')
                self.errors = True
                return None
        
        node.static_type = attr_type
        return attr_type
    
    
    @visitor.when(ast.FormalParameter)
    def visit(self, node, scope):
        """
        node.name -> str
        node.param_type -> str
        """
        param_type = scope.get_type(node.param_type)
        if param_type is None:
            sys.stdout.write(f'({node.lineno}, {node.linepos}) - {TYPERROR11 % node.param_type}\n')
            self.errors = True
            return None
        
        if not scope.define_new_symbol(node.name, param_type):
            sys.stdout.write(f'({node.lineno}, {node.linepos}) - {SEMERROR4 % node.name}\n')
            self.errors = True
            return None
        
        node.static_type = param_type
        return param_type


    @visitor.when(ast.Formal)
    def visit(self, node, scope):
        """
        node.name -> str
        node.param_type -> str
        node.init_expr -> Expr/None
        """
        param_type = scope.get_type(node.param_type)
        if param_type is None:
            sys.stdout.write(f'({node.lineno}, {node.linepos}) - {TYPERROR11 % node.param_type}\n')
            self.errors = True
            return None
        
        if not scope.define_new_symbol(node.name, param_type, True):
            sys.stdout.write(f'({node.lineno}, {node.linepos}) - {SEMERROR4 % node.name}\n')
            self.errors = True
            return None
        
        if not node.init_expr is None:
            expr_type = scope.get_type(self.visit(node.init_expr, scope))
            
            if expr_type is None:
                if not self.errors:
                    sys.stdout.write(f'({node.init_expr.lineno}, {node.init_expr.linepos}) - {NAMERROR1 % node.init_expr.name}\n')
                self.errors = True
                return None
            
            if expr_type == scope.ctype.VOID:
                sys.stdout.write(f'({node.init_expr.lineno}, {node.init_expr.linepos}) - {RNTERROR1}\n')
                self.errors = True
                return None
            
            if expr_type == scope.ctype.SELF or param_type == scope.ctype.SELF:
                if expr_type != scope.ctype.SELF:
                    param_type = scope.get_type(scope.classname)
                elif param_type != scope.ctype.SELF:
                    expr_type = scope.get_type(scope.classname)

            if not (expr_type <= param_type):
                sys.stdout.write(f'({node.init_expr.lineno}, {node.init_expr.linepos}) - {TYPERROR16 % (expr_type, node.name, param_type)}\n')
                self.errors = True
                return None
        
        node.static_type = param_type
        return param_type
    
    
    @visitor.when(ast.Object)
    def visit(self, node, scope):
        """
        node.name -> str
        """
        obj_type = scope.get_var(scope.classname, node.name)
        
        if obj_type is None:
            return None

        node.static_type = obj_type
        return obj_type
        
    
    @visitor.when(ast.Self)
    def visit(self, node, scope):
        return_type = scope.ctype.SELF
        node.static_type = return_type
        return return_type
    
    
    @visitor.when(ast.Integer)
    def visit(self, node, scope):
        """
        node.content -> int
        """
        return_type = scope.ctype.INT
        node.static_type = return_type
        return return_type


    @visitor.when(ast.String)
    def visit(self, node, scope):
        """
        node.content -> str
        """
        return_type = scope.ctype.STRING
        node.static_type = return_type
        return return_type
    
    
    @visitor.when(ast.Boolean)
    def visit(self, node, scope):
        """
        node.content -> bool
        """
        return_type = scope.ctype.BOOL
        node.static_type = return_type
        return return_type
    
    
    @visitor.when(ast.NewObject)
    def visit(self, node, scope):
        """
        node.type -> int
        """
        new_type = scope.get_type(node.type)
        
        if new_type is None:
            sys.stdout.write(f'({node.lineno}, {node.linepos}) - {TYPERROR10 % node.type}\n')
            self.errors = True
            return None
        
        node.static_type = new_type
        return new_type
    
    
    @visitor.when(ast.IsVoid)
    def visit(self, node, scope):
        """
        node.expr -> Expr
        """
        if self.visit(node.expr, scope) is None:
            if not self.errors:
                sys.stdout.write(f'({node.expr.lineno}, {node.expr.linepos}) - {NAMERROR1 % node.expr.name}\n')
            self.errors = True
            return None
        
        node.static_type = scope.ctype.BOOL
        return node.static_type
    
    
    @visitor.when(ast.Assignment)
    def visit(self, node, scope):
        """
        node.instance -> Object
        node.expr -> Expr
        """
        if scope.get_var(scope.classname, node.instance.name) == scope.ctype.SELF:
            sys.stdout.write(f'({node.lineno}, {node.linepos}) - {SEMERROR10}\n')
            self.errors = True
            return None
        instance_type = scope.get_type(self.visit(node.instance, scope))
        
        expr_type = scope.get_type(self.visit(node.expr, scope))
        if expr_type is None:
            if not self.errors:
                sys.stdout.write(f'({node.expr.lineno}, {node.expr.linepos}) - {NAMERROR1 % node.expr.name}\n')
            self.errors = True
            return None
        
        if expr_type == scope.ctype.SELF or instance_type == scope.ctype.SELF:
            if expr_type != scope.ctype.SELF:
                instance_type = scope.get_type(scope.classname)
            elif instance_type != scope.ctype.SELF:
                expr_type = scope.get_type(scope.classname)
        
        if instance_type is None:
            scope.define_new_symbol(node.instance.name, expr_type)
            instance_type = expr_type
        
        if not (expr_type <= instance_type):
            sys.stdout.write(f'({node.expr.lineno}, {node.expr.linepos}) - {TYPERROR9 % (expr_type, node.instance.name, instance_type)}\n')
            self.errors = True
            return None
    
        node.static_type = expr_type
        return expr_type
    
    
    @visitor.when(ast.Block)
    def visit(self, node, scope):
        """
        node.expr_list -> [ Expr ... ]
        """
        return_type = scope.ctype.VOID
        
        for expr in node.expr_list:
            return_type = scope.get_type(self.visit(expr, scope))
            if return_type is None:
                if not self.errors:
                    sys.stdout.write(f'({node.expr.lineno}, {node.expr.linepos}) - {NAMERROR1 % node.expr.name}\n')
                self.errors = True
                return None
        
        node.static_type = return_type
        return return_type
    
    
    @visitor.when(ast.DynamicDispatch)
    def visit(self, node, scope):
        """
        node.instance -> Expr
        node.method -> str
        node.arguments -> [ Expr ... ]
        """
        instance_type = scope.get_type(self.visit(node.instance, scope))
        if instance_type is None:
            if not self.errors:
                sys.stdout.write(f'({node.instance.lineno}, {node.instance.linepos}) - {NAMERROR1 % node.instance.name}\n')
            self.errors = True
            return None
        
        if instance_type == scope.ctype.VOID:
            sys.stdout.write(f'({node.instance.lineno}, {node.instance.linepos}) - {RNTERROR1}\n')
            self.errors = True
            return None
        
        if instance_type == scope.ctype.SELF:
            instance_type = scope.get_type(scope.classname)
        
        node_args = []
        for arg in node.arguments:
            _type = scope.get_type(self.visit(arg, scope))
            if _type is None:
                if not self.errors:
                    sys.stdout.write(f'({arg.lineno}, {arg.linepos}) - {NAMERROR1 % arg.name}\n')
                self.errors = True
                return None
            
            if _type == scope.ctype.SELF:
                _type = scope.get_type(scope.classname)
            node_args.append(_type)
        
        if scope.get_var(scope.classname, node.method) == scope.ctype.SELF:
            sys.stdout.write(f'({node.lineno}, {node.linepos}) - {SEMERROR12 % "a dispatch call"}\n')
            self.errors = True
            return None
        
        _method = instance_type.get_func(node.method)        
        if _method is None:
            sys.stdout.write(f'({node.lineno}, {node.linepos}) - {ATTRERROR1 % node.method}\n')
            self.errors = True
            return None

        args_types = list(_method['formal_params'].values())
        args_names = list(_method['formal_params'].keys())
        
        if len(args_types) != len(node_args):
            sys.stdout.write(f'({node.lineno}, {node.linepos}) - {SEMERROR1 % node.method}\n')
            self.errors = True
            return None
        
        for i in range(len(args_types)):
            if not (node_args[i] <= args_types[i]):
                sys.stdout.write(f'({node.arguments[i].lineno}, {node.arguments[i].linepos}) - {TYPERROR8 % (node.method, node_args[i], args_names[i], args_types[i])}\n')
                self.errors = True
                return None
        
        return_type = _method['return_type']
        if return_type == scope.ctype.SELF:
            return_type = instance_type
        node.static_type = return_type
        return return_type
    
    
    @visitor.when(ast.StaticDispatch)
    def visit(self, node, scope):
        """
        node.instance -> Expr
        node.dispatch_type -> str
        node.method -> str
        node.arguments -> [ Expr ... ]
        """
        instance_type = scope.get_type(self.visit(node.instance, scope))
        if instance_type is None:
            if not self.errors:
                sys.stdout.write(f'({node.instance.lineno}, {node.instance.linepos}) - {NAMERROR1 % node.instance.name}\n')
            self.errors = True
            return None
        
        if instance_type == scope.ctype.VOID:
            sys.stdout.write(f'({node.instance.lineno}, {node.instance.linepos}) - {RNTERROR1}\n')
            self.errors = True
            return None
        
        if instance_type == scope.ctype.SELF:
            instance_type = scope.get_type(scope.classname)
        
        class_type = scope.get_type(node.dispatch_type)
        if class_type == scope.ctype.SELF:
            class_type = scope.get_type(scope.classname)
        
        if not (instance_type <= class_type):
            sys.stdout.write(f'({node.instance.lineno}, {node.instance.linepos}) - {TYPERROR7 % (instance_type, class_type)}\n')
            self.errors = True
            return None
        
        node_args = []
        for arg in node.arguments:
            _type = scope.get_type(self.visit(arg, scope))
            if _type is None:
                if not self.errors:
                    sys.stdout.write(f'({arg.lineno}, {arg.linepos}) - {NAMERROR1 % arg.name}\n')
                self.errors = True
                return None
            
            if _type == scope.ctype.SELF:
                _type = scope.get_type(scope.classname)
            node_args.append(_type)
        
        if scope.get_var(scope.classname, node.method) == scope.ctype.SELF:
            sys.stdout.write(f'({node.lineno}, {node.linepos}) - {SEMERROR12 % "a dispatch call"}\n')
            self.errors = True
            return None
        
        _method = instance_type.get_func(node.method)
        if _method is None:
            sys.stdout.write(f'({node.lineno}, {node.linepos}) - {ATTRERROR1 % node.method}\n')
            self.errors = True
            return None
        
        args_types = list(_method['formal_params'].values())
        args_names = list(_method['formal_params'].keys())
        
        if len(args_types) != len(node.arguments):
            sys.stdout.write(f'({node.lineno}, {node.linepos}) - {SEMERROR1 % node.method}\n')
            self.errors = True
            return None
        
        for i in range(len(args_types)):
            if not (node_args[i] <= args_types[i]):
                sys.stdout.write(f'({node.arguments[i].lineno}, {node.arguments[i].linepos}) - {TYPERROR8 % (node.method, node_args[i], args_names[i], args_types[i])}\n')
                self.errors = True
                return None
        
        return_type = _method['return_type']
        if return_type == scope.ctype.SELF:
            return_type = class_type
        node.static_type = return_type
        return return_type
        
    
    @visitor.when(ast.Let)
    def visit(self, node, scope):
        """
        node.declarations -> [ Formal ... ]
        node.body -> Expr
        """
        new_scope = COOL_Scope(scope.classname, scope)
        
        for declaration in node.declarations:
            if scope.get_var(scope.classname, declaration.name) == scope.ctype.SELF:
                sys.stdout.write(f'({declaration.lineno}, {declaration.linepos}) - {SEMERROR11 % "let"}\n')
                self.errors = True
                return None
            
            if self.visit(declaration, new_scope) is None:
                return None
            
        body_type = scope.get_type(self.visit(node.body, new_scope))
        
        if body_type is None:
            if not self.errors:
                sys.stdout.write(f'({node.body.lineno}, {node.body.linepos}) - {NAMERROR1 % node.body.name}\n')
            self.errors = True
            return None
        
        node.static_type = body_type
        return body_type
        
    
    @visitor.when(ast.If)
    def visit(self, node, scope):
        """
        node.predicate -> Expr
        node.then_body -> Expr
        node.else_body -> Expr
        """
        pred_type = scope.get_type(self.visit(node.predicate, scope))
        
        if pred_type is None:
            if not self.errors:
                sys.stdout.write(f'({node.predicate.lineno}, {node.predicate.linepos}) - {NAMERROR1 % node.predicate.name}\n')
            self.errors = True
            return None
        
        if pred_type != scope.ctype.BOOL:
            sys.stdout.write(f'({node.predicate.lineno}, {node.predicate.linepos}) - {TYPERROR6}\n')
            self.errors = True
            return None
        
        if_type = scope.get_type(self.visit(node.then_body, scope))
        
        if if_type is None:
            if not self.errors:
                sys.stdout.write(f'({node.then_body.lineno}, {node.then_body.linepos}) - {NAMERROR1 % node.then_body.name}\n')
            self.errors = True
            return None
        
        else_type = scope.get_type(self.visit(node.else_body, scope))
        
        if else_type is None:
            if not self.errors:
                sys.stdout.write(f'({node.else_body.lineno}, {node.else_body.linepos}) - {NAMERROR1 % node.else_body.name}\n')
            self.errors = True
            return None
        
        return_type = if_type
        
        if if_type != scope.ctype.SELF or else_type != scope.ctype.SELF:
            if else_type == scope.ctype.SELF:
                return_type = scope.join(return_type, scope.get_type(scope.classname))
            elif if_type == scope.ctype.SELF:
                return_type = scope.join(else_type, scope.get_type(scope.classname))
            else:
                return_type = scope.join(return_type, else_type)
        
        node.static_type = return_type
        return return_type
    
    
    @visitor.when(ast.WhileLoop)
    def visit(self, node, scope):
        """
        node.predicate -> Expr
        node.body -> Expr
        """
        pred_type = scope.get_type(self.visit(node.predicate, scope))
        
        if pred_type is None:
            if not self.errors:
                sys.stdout.write(f'({node.predicate.lineno}, {node.predicate.linepos}) - {NAMERROR1 % node.predicate.name}\n')
            self.errors = True
            return None
        
        if pred_type != scope.ctype.BOOL:
            sys.stdout.write(f'({node.predicate.lineno}, {node.predicate.linepos}) - {TYPERROR4}\n')
            self.errors = True
            return None
        
        body_type = scope.get_type(self.visit(node.body, scope))
        
        if body_type is None:
            if not self.errors:
                sys.stdout.write(f'({node.body.lineno}, {node.body.linepos}) - {NAMERROR1 % node.body.name}\n')
            self.errors = True
            return None
        
        node.static_type = scope.ctype.OBJECT
        return node.static_type
    
    
    @visitor.when(ast.Case)
    def visit(self, node, scope):
        """
        node.expr -> Expr
        node.actions -> Action
        """
        type_expr = scope.get_type(self.visit(node.expr, scope))
        if type_expr is None:
            if not self.errors:
                sys.stdout.write(f'({node.expr.lineno}, {node.expr.linepos}) - {NAMERROR1 % node.expr.name}\n')
            self.errors = True
            return None
        
        if type_expr == scope.ctype.VOID:
            sys.stdout.write(f'({node.expr.lineno}, {node.expr.linepos}) - {RNTERROR1}\n')
            self.errors = True
            return None
        
        return_type = scope.get_type(self.visit(node.actions[0], scope))
        if return_type is None:
            return None
        
        ids_type = [scope.get_type(node.actions[0].action_type)]
        if ids_type[0] is None:
            sys.stdout.write(f'({node.action[0].lineno}, {node.action[0].linepos}) - {TYPERROR15 % node.action[0].action_type}\n')
            self.errors = True
            return None
        
        for action in node.actions[1:]:
            if scope.get_var(scope.classname, action.name) == scope.ctype.SELF:
                sys.stdout.write(f'({action.lineno}, {action.linepos}) - {SEMERROR11 % "case"}\n')
                self.errors = True
                return None
            
            type_action = scope.get_type(self.visit(action, scope))
            if type_action is None:
                return None
            
            id_type = scope.get_type(action.action_type)
            if id_type is None:
                sys.stdout.write(f'({action.lineno}, {action.linepos}) - {TYPERROR15 % action.action_type}\n')
                self.errors = True
                return None
            
            if id_type in ids_type:
                sys.stdout.write(f'({action.lineno}, {action.linepos}) - {SEMERROR7 % id_type}\n')
                self.errors = True
                return None
            
            ids_type.append(id_type)
            
            if return_type != scope.ctype.SELF or type_action != scope.ctype.SELF:
                if type_action == scope.ctype.SELF:
                    return_type = scope.join(return_type, scope.get_type(scope.classname))
                elif return_type == scope.ctype.SELF:
                    return_type = scope.join(type_action, scope.get_type(scope.classname))
                else:
                    return_type = scope.join(type_action, return_type)
        
        if return_type == scope.ctype.VOID:
            sys.stdout.write(f'({node.lineno}, {node.linepos}) - {RNTERROR2}\n')
            self.errors = True
            return None
        
        node.static_type = return_type
        return return_type
    
    
    @visitor.when(ast.Action)
    def visit(self, node, scope):
        """
        node.name -> str
        node.action_type -> str
        node.body -> Expr
        """
        _type = scope.get_type(node.action_type)
        if _type is None:
            self.errors = True
        
        new_scope = COOL_Scope(scope.classname, scope)
        if not new_scope.define_new_symbol(node.name, _type):
            sys.stdout.write(f'({node.lineno}, {node.linepos}) - {SEMERROR4 % node.name}\n')
            self.errors = True
            return None
        
        return_type = scope.get_type(self.visit(node.body, new_scope))
        
        if return_type is None:
            if not self.errors:
                sys.stdout.write(f'({node.body.lineno}, {node.body.linepos}) - {NAMERROR1 % node.body.name}\n')
            self.errors = True
            return None
        
        node.static_type = return_type
        return return_type
    
    
    @visitor.when(ast.IntegerComplement)
    def visit(self, node, scope):
        """
        node.integer_expr -> Expr
        """
        type_expr = scope.get_type(self.visit(node.integer_expr, scope))
        
        if type_expr is None:
            if not self.errors:
                sys.stdout.write(f'({node.integer_expr.lineno}, {node.integer_expr.linepos}) - {NAMERROR1 % node.integer_expr.name}\n')
            self.errors = True
            return None
        
        if type_expr != scope.ctype.INT:
            sys.stdout.write(f'({node.lineno}, {node.linepos}) - {TYPERROR3 % (node.symbol, type_expr, scope.ctype.INT)}\n')
            self.errors = True
            return None
        
        return_type = scope.ctype.INT
        node.static_type = return_type
        return return_type
    
    
    @visitor.when(ast.BooleanComplement)
    def visit(self, node, scope):
        """
        node.boolean_expr -> Expr
        """
        type_expr = scope.get_type(self.visit(node.boolean_expr, scope))
        
        if type_expr is None:
            if not self.errors:
                sys.stdout.write(f'({node.boolean_expr.lineno}, {node.boolean_expr.linepos}) - {NAMERROR1 % node.boolean_expr.name}\n')
            self.errors = True
            return None
        
        if type_expr != scope.ctype.BOOL:
            sys.stdout.write(f'({node.lineno}, {node.linepos}) - {TYPERROR3 % ("not", type_expr, scope.ctype.BOOL)}\n')
            self.errors = True
            return None
        
        return_type = scope.ctype.BOOL
        node.static_type = return_type
        return return_type
    
    
    @visitor.when(ast.Addition)
    def visit(self, node, scope):
        """
        node.first -> Expr
        node.second -> Expr
        """
        left_type = scope.get_type(self.visit(node.first, scope))
        
        if left_type is None:
            if not self.errors:
                sys.stdout.write(f'({node.first.lineno}, {node.first.linepos}) - {NAMERROR1 % node.first.name}\n')
            self.errors = True
            return None
        
        right_type = scope.get_type(self.visit(node.second, scope))
        
        if right_type is None:
            if not self.errors:
                sys.stdout.write(f'({node.second.lineno}, {node.second.linepos}) - {NAMERROR1 % node.second.name}\n')
            self.errors = True
            return None
        
        if left_type != scope.ctype.INT or right_type != scope.ctype.INT:
            sys.stdout.write(f'({node.lineno}, {node.linepos}) - {TYPERROR2} {left_type} + {right_type}.\n')
            self.errors = True
            return None
        
        return_type = scope.ctype.INT
        node.static_type = return_type
        return return_type
    
    
    @visitor.when(ast.Subtraction)
    def visit(self, node, scope):
        """
        node.first -> Expr
        node.second -> Expr
        """
        left_type = scope.get_type(self.visit(node.first, scope))
        
        if left_type is None:
            if not self.errors:
                sys.stdout.write(f'({node.first.lineno}, {node.first.linepos}) - {NAMERROR1 % node.first.name}\n')
            self.errors = True
            return None
        
        right_type = scope.get_type(self.visit(node.second, scope))
        
        if right_type is None:
            if not self.errors:
                sys.stdout.write(f'({node.second.lineno}, {node.second.linepos}) - {NAMERROR1 % node.second.name}\n')
            self.errors = True
            return None
        
        if left_type != scope.ctype.INT or right_type != scope.ctype.INT:
            sys.stdout.write(f'({node.lineno}, {node.linepos}) - {TYPERROR2} {left_type} - {right_type}.\n')
            self.errors = True
            return None
        
        return_type = scope.ctype.INT
        node.static_type = return_type
        return return_type
        
    
    @visitor.when(ast.Multiplication)
    def visit(self, node, scope):
        """
        node.first -> Expr
        node.second -> Expr
        """
        left_type = scope.get_type(self.visit(node.first, scope))
        
        if left_type is None:
            if not self.errors:
                sys.stdout.write(f'({node.first.lineno}, {node.first.linepos}) - {NAMERROR1 % node.first.name}\n')
            self.errors = True
            return None
        
        right_type = scope.get_type(self.visit(node.second, scope))
        
        if right_type is None:
            if not self.errors:
                sys.stdout.write(f'({node.second.lineno}, {node.second.linepos}) - {NAMERROR1 % node.second.name}\n')
            self.errors = True
            return None
        
        if left_type != scope.ctype.INT or right_type != scope.ctype.INT:
            sys.stdout.write(f'({node.lineno}, {node.linepos}) - {TYPERROR2} {left_type} * {right_type}.\n')
            self.errors = True
            return None
        
        return_type = scope.ctype.INT
        node.static_type = return_type
        return return_type
    
    
    @visitor.when(ast.Division)
    def visit(self, node, scope):
        """
        node.first -> Expr
        node.second -> Expr
        """
        left_type = scope.get_type(self.visit(node.first, scope))
        
        if left_type is None:
            if not self.errors:
                sys.stdout.write(f'({node.first.lineno}, {node.first.linepos}) - {NAMERROR1 % node.first.name}\n')
            self.errors = True
            return None
        
        right_type = scope.get_type(self.visit(node.second, scope))
        
        if right_type is None:
            if not self.errors:
                sys.stdout.write(f'({node.second.lineno}, {node.second.linepos}) - {NAMERROR1 % node.second.name}\n')
            self.errors = True
            return None
        
        if left_type != scope.ctype.INT or right_type != scope.ctype.INT:
            sys.stdout.write(f'({node.lineno}, {node.linepos}) - {TYPERROR2} {left_type} / {right_type}.\n')
            self.errors = True
            return None
        
        return_type = scope.ctype.INT
        node.static_type = return_type
        return return_type
    
    
    @visitor.when(ast.Equal)
    def visit(self, node, scope):
        """
        node.first -> Expr
        node.second -> Expr
        """
        left_type = scope.get_type(self.visit(node.first, scope))
        
        if left_type is None:
            if not self.errors:
                sys.stdout.write(f'({node.first.lineno}, {node.first.linepos}) - {NAMERROR1 % node.first.name}\n')
            self.errors = True
            return None
        
        right_type = scope.get_type(self.visit(node.second, scope))
        
        if right_type is None:
            if not self.errors:
                sys.stdout.write(f'({node.second.lineno}, {node.second.linepos}) - {NAMERROR1 % node.second.name}\n')
            self.errors = True
            return None
        
        if left_type in scope.ctype.not_inherits_type or right_type in scope.ctype.not_inherits_type:
            if left_type == scope.ctype.SELF:
                left_type = scope.get_type(scope.classname)
                
            if right_type == scope.ctype.SELF:
                right_type = scope.get_type(scope.classname)
                
            if left_type != right_type:
                sys.stdout.write(f'({node.lineno}, {node.linepos}) - {TYPERROR1}\n')
                self.errors = True
                return None
        
        return_type = scope.ctype.BOOL
        node.static_type = return_type
        return return_type
        
    
    @visitor.when(ast.LessThan)
    def visit(self, node, scope):
        """
        node.first -> Expr
        node.second -> Expr
        """
        left_type = scope.get_type(self.visit(node.first, scope))
        
        if left_type is None:
            if not self.errors:
                sys.stdout.write(f'({node.first.lineno}, {node.first.linepos}) - {NAMERROR1 % node.first.name}\n')
            self.errors = True
            return None
        
        right_type = scope.get_type(self.visit(node.second, scope))
        
        if right_type is None:
            if not self.errors:
                sys.stdout.write(f'({node.second.lineno}, {node.second.linepos}) - {NAMERROR1 % node.second.name}\n')
            self.errors = True
            return None
        
        if left_type != scope.ctype.INT or right_type != scope.ctype.INT:
            sys.stdout.write(f'({node.lineno}, {node.linepos}) - {TYPERROR1}\n')
            self.errors = True
            return None
        
        return_type = scope.ctype.BOOL
        node.static_type = return_type
        return return_type
    
    
    @visitor.when(ast.LessThanOrEqual)
    def visit(self, node, scope):
        """
        node.first -> Expr
        node.second -> Expr
        """
        left_type = scope.get_type(self.visit(node.first, scope))
        
        if left_type is None:
            if not self.errors:
                sys.stdout.write(f'({node.first.lineno}, {node.first.linepos}) - {NAMERROR1 % node.first.name}\n')
            self.errors = True
            return None
        
        right_type = scope.get_type(self.visit(node.second, scope))
        
        if right_type is None:
            if not self.errors:
                sys.stdout.write(f'({node.second.lineno}, {node.second.linepos}) - {NAMERROR1 % node.second.name}\n')
            self.errors = True
            return None
        
        if left_type != scope.ctype.INT or right_type != scope.ctype.INT:
            sys.stdout.write(f'({node.lineno}, {node.linepos}) - {TYPERROR1}\n')
            self.errors = True
            return None
        
        return_type = scope.ctype.BOOL
        node.static_type = return_type
        return return_type