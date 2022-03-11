from CodeGen.Intermediate.base_generator import BaseCOOLToCILVisitor
from CodeGen.Intermediate import cil
from Semantic import visitor
from Semantic.scope import *
from Parser import ast

class COOLToCILVisitor(BaseCOOLToCILVisitor):
    
    def __init__(self, context):
        super(COOLToCILVisitor, self).__init__()
        self.context = context
        self.program_node = None
    
    ##################################################################################################################
    # VISITOR
    ##################################################################################################################
    
    @visitor.on('node')
    def visit(self, node, scope, cil_scope):
        pass
    
    @visitor.when(ast.Program)
    def visit(self, node, scope, cil_scope = None):
        """
        node.classes -> [ Class ... ]
        """
        self.program_node = node
        cil_scope = cil.Scope()
        self.define_entry_function()
        self.predefined_types()
        
        for _class in node.classes:
            data = self.register_data(_class.name)
            self.types_names[_class.name] = data
            cil_scope.create_child()
        
        for _class, child_scope, ch_cil_scope in zip(node.classes, scope.children, cil_scope.children):
            self.visit(_class, child_scope, ch_cil_scope)
        
        self.fill_cil_types(self.context)

        return cil.ProgramNode(self.dottypes, self.dotdata, self.dotcode)
    
    
    @visitor.when(ast.Class)
    def visit(self, node, scope, cil_scope):
        """
        node.name -> str
        node.parent -> Class
        node.features -> [ ClassMethod/ClassAttribute ... ]
        """        
        self.current_type = scope.ctype.defined_types[node.name]
        
        parent = node.parent if type(node.parent) is str else node.parent.name
        cil_type = self.register_type(node.name, parent)
        cil_type.attributes = [a for a in self.current_type.get_all_attr()]
        
        for feature, num in zip(node.features, range(len(node.features))):
            child_scope = scope.next_child()
            if isinstance(feature, ast.ClassMethod):
                self.visit(feature, child_scope, cil_scope.create_child())
        
        function_init_attr = self.define_init_attr_function()
        self.init_attr_functions[function_init_attr.name] = self.current_type
        self.dottypes[-1].methods.append((function_init_attr.name, function_init_attr.name))
        
        current = node
        current_list = []
        while isinstance(current, ast.Class):
            current_list.append(current)
            current = current.parent
        current_list = current_list[::-1]
        
        num = 0
        for current in current_list:
            indx = self.program_node.classes.index(current)
            current_scope = scope.parent.children[indx]
            current_scope.child_index = 0
            current_child_scope = cil_scope.parent.children[indx]
            
            for feature in current.features:
                child_scope = current_scope.next_child()
                if isinstance(feature, ast.ClassAttribute):
                    self.current_function = function_init_attr
                    if feature.init_expr is None:
                        value = self.define_internal_local()
                        self.register_instruction(cil.AllocateNode(f'type_{feature.static_type.name}', value))
                    else:
                        value = self.visit(feature.init_expr, child_scope, current_child_scope.create_child())
                    self.register_instruction(cil.SetAttribNode('self', num, value))
                    self.current_function = None
                    num += 1
                
        self.current_function = function_init_attr
        self.register_instruction(cil.ReturnNode('self'))
        self.current_function = None
        self.current_type = None

                
    @visitor.when(ast.ClassMethod)
    def visit(self, node, scope,cil_scope):
        """
        node.name -> str
        node.formal_params -> [ FormalParameter ... ]
        node.return_type -> str
        node.body -> Expr
        """
        function_name = self.to_function_name(node.name, self.current_type.name)
        self.dottypes[-1].methods.append((node.name, function_name))
        self.current_function = self.register_function(function_name)
        self.current_function.params = [cil.ParamNode('self')]
        
        for param in node.formal_params:
            self.current_function.params.append(cil.ParamNode(param.name))
            cil_scope.define_variable(param.name, param.name, param.static_type)

        value = self.visit(node.body, scope, cil_scope)

        self.register_instruction(cil.ReturnNode(value))
        self.current_function = None
    

    @visitor.when(ast.Formal)
    def visit(self, node, scope, cil_scope):
        """
        node.name -> str
        node.param_type -> str
        node.init_expr -> Expr/None
        """
        vname = self.register_local(VariableInfo(node.name, node.static_type))
        cil_scope.define_variable(node.name, vname, node.static_type)
        
        if not node.init_expr is None:
            value = self.visit(node.init_expr, scope, cil_scope)
            self.register_instruction(cil.AssignNode(vname, value))
        
        else:
            self.register_instruction(cil.AllocateNode(f'type_{node.static_type.name}', vname))


    @visitor.when(ast.Object)
    def visit(self, node, scope, cil_scope):
        """
        node.name -> str
        """
        if node.name == 'self':
            return node.name
        
        current_cil_scope = cil_scope
        while not current_cil_scope is None:
            if not current_cil_scope.local_by_name.get(node.name) is None:
                return current_cil_scope.local_by_name[node.name].name
            current_cil_scope = current_cil_scope.parent
        
        current_type = self.current_type
        while not current_type is None:
            if node.name in list(current_type.attr.keys()):
                vname = self.define_internal_local()
                self.register_instruction(cil.GetAttribNode(vname, 'self', current_type.get_all_attr().index(node.name)))
                return vname
            current_type = current_type.parent
        
        vname = self.register_local(VariableInfo(node.name, node.static_type))
        cil_scope.define_variable(node.name, vname, node.static_type)
        return vname
    
    
    @visitor.when(ast.Self)
    def visit(self, node, scope, cil_scope):
        return 'self'
    
    
    @visitor.when(ast.Integer)
    def visit(self, node, scope, cil_scope):
        """
        node.content -> int
        """
        instance = self.define_internal_local()
        self.register_instruction(cil.AllocateNode(f'type_{scope.ctype.INT}', instance, node.content))
        return instance
    
    
    @visitor.when(ast.String)
    def visit(self, node, scope, cil_scope):
        """
        node.content -> str
        """
        data_node = self.register_data(node.content)
        
        instance = self.define_internal_local()
        self.register_instruction(cil.AllocateNode(f'type_{scope.ctype.STRING}', instance, data_node.name))
        return instance
    
    
    @visitor.when(ast.Boolean)
    def visit(self, node, scope, cil_scope):
        """
        node.content -> bool
        """
        false = self.define_internal_local()
        self.register_instruction(cil.AllocateNode(f'type_{scope.ctype.BOOL}', false, 0))
        
        if node.content:
            true = self.define_internal_local()
            self.register_instruction(cil.BoolComplementNode(true, false))
            return true
        
        return false
    
    
    @visitor.when(ast.NewObject)
    def visit(self, node, scope, cil_scope):
        """
        node.type -> int
        """
        instance = self.define_internal_local()
        self.register_instruction(cil.AllocateNode(f'type_{node.static_type}', instance))
        self.register_instruction(cil.ArgNode(instance))
        self.register_instruction(cil.StaticCallNode(f'function_initialize_{node.static_type.name}_attributes', instance))
        return instance
    
    
    @visitor.when(ast.IsVoid)
    def visit(self, node, scope, cil_scope):
        """
        node.expr -> Expr
        """
        value = self.visit(node.expr, scope, cil_scope)
        
        true = self.define_internal_local()
        false = self.define_internal_local()
        _type1 = self.define_internal_local()
        _type2 = self.define_internal_local()
        result = self.define_internal_local()
        
        void = self.register_data(scope.ctype.VOID)
        
        then_label = cil.LabelNode(self.define_label())
        out_label = cil.LabelNode(self.define_label())
        
        self.register_instruction(cil.AllocateNode(f'type_{scope.ctype.BOOL}', false, 0))
        self.register_instruction(cil.BoolComplementNode(true, false))
        
        self.register_instruction(cil.TypeOfNode(value, _type1))
        self.register_instruction(cil.LoadNode(_type2, void.name))
        self.register_instruction(cil.BranchEqualNode(_type1, _type2, then_label.name))
        
        self.register_instruction(cil.AssignNode(result, false))
        self.register_instruction(cil.GotoNode(out_label.name))
        
        self.register_instruction(then_label)
        self.register_instruction(cil.AssignNode(result, true))
        self.register_instruction(out_label)
        
        return result
    
    
    @visitor.when(ast.Assignment)
    def visit(self, node, scope, cil_scope):
        """
        node.instance -> Object
        node.expr -> Expr
        """
        value = self.visit(node.expr, scope, cil_scope)
        
        current_type = self.current_type
        while not current_type is None:
            if node.instance.name in list(current_type.attr.keys()):
                instr = cil.SetAttribNode('self', current_type.get_all_attr().index(node.instance.name), value)
                self.register_instruction(instr)
                return value
            current_type = current_type.parent
            
        vname = self.visit(node.instance, scope, cil_scope)
        self.register_instruction(cil.AssignNode(vname, value))
        return value
    
    
    @visitor.when(ast.Block)
    def visit(self, node, scope, cil_scope):
        """
        node.expr_list -> [ Expr ... ]
        """
        value = self.visit(node.expr_list[0], scope, cil_scope)
        for expr in node.expr_list[1:]:
            value = self.visit(expr, scope, cil_scope)
        return value
    
    
    @visitor.when(ast.DynamicDispatch)
    def visit(self, node, scope, cil_scope):
        """
        node.instance -> Expr
        node.method -> str
        node.arguments -> [ Expr ... ]
        """
        args = list()
        instance = self.visit(node.instance, scope, cil_scope)
        dest = self.define_internal_local()
        
        _type = self.define_internal_local()
        self.register_instruction(cil.TypeOfNode(instance, _type))
        
        for arg in node.arguments:
            args.append(self.visit(arg, scope, cil_scope))
        
        labels = list()
        for t in list(scope.ctype.defined_types.keys()):
            current_type = scope.get_type(t).get_func_context(node.method)
            if not current_type is None:
                ldata = self.define_internal_local()
                label = cil.LabelNode(self.define_label())
                self.register_instruction(cil.LoadNode(ldata, self.types_names[t].name))
                self.register_instruction(cil.BranchEqualNode(_type, ldata, label.name))
                labels.append((label, self.to_function_name(node.method, current_type.name)))
        
        end_label = cil.LabelNode(self.define_label())
        self.register_instruction(cil.GotoNode(end_label.name))
        
        for label, func_name in labels:
            self.register_instruction(label)
            self.register_instruction(cil.ArgNode(instance))
            for arg in args:
                self.register_instruction(cil.ArgNode(arg))
            self.register_instruction(cil.StaticCallNode(func_name, dest))
            self.register_instruction(cil.GotoNode(end_label.name))
            
        self.register_instruction(end_label)
        return dest
    
    
    @visitor.when(ast.StaticDispatch)
    def visit(self, node, scope, cil_scope):
        """
        node.instance -> Expr
        node.dispatch_type -> str
        node.method -> str
        node.arguments -> [ Expr ... ]
        """
        instance = self.visit(node.instance, scope, cil_scope)
        args = list()
        dest = self.define_internal_local()
        
        if node.dispatch_type == scope.ctype.SELF:
            _type = self.current_type
        else:
            _type = scope.get_type(node.dispatch_type)
        
        for arg in node.arguments:
            args.append(self.visit(arg, scope, cil_scope))
        
        self.register_instruction(cil.ArgNode(instance))
        
        for arg in args:
            self.register_instruction(cil.ArgNode(arg))
        
        func_name = self.to_function_name(node.method, _type.get_func_context(node.method).name)
        self.register_instruction(cil.StaticCallNode(func_name, dest))
        return dest
    
    
    @visitor.when(ast.Let)
    def visit(self, node, scope, cil_scope):
        """
        node.declarations -> [ Formal ... ]
        node.body -> Expr
        """
        new_cil_scope = cil_scope.create_child()
        child = scope.next_child()
        
        for declaration in node.declarations:
            self.visit(declaration, child, new_cil_scope)
        
        return self.visit(node.body, child, new_cil_scope)
    
    
    @visitor.when(ast.If)
    def visit(self, node, scope, cil_scope):
        """
        node.predicate -> Expr
        node.then_body -> Expr
        node.else_body -> Expr
        """
        predicate = self.visit(node.predicate, scope, cil_scope)
        
        then_label = cil.LabelNode(self.define_label())
        else_label = cil.LabelNode(self.define_label())
        end_label = cil.LabelNode(self.define_label())
        
        then_goto = cil.GotoNode(then_label.name)
        else_goto = cil.GotoNode(else_label.name)
        end_goto = cil.GotoNode(end_label.name)
        
        self.register_instruction(cil.GotoIfNode(predicate, then_goto.label))
        self.register_instruction(else_goto)
        self.register_instruction(then_label)
        
        vname = self.define_internal_local()
        self.register_instruction(cil.AssignNode(vname, self.visit(node.then_body, scope, cil_scope)))
        self.register_instruction(end_goto)
        
        self.register_instruction(else_label)
        self.register_instruction(cil.AssignNode(vname, self.visit(node.else_body, scope, cil_scope)))
        self.register_instruction(end_label)
        return vname
    
    
    @visitor.when(ast.WhileLoop)
    def visit(self, node, scope, cil_scope):
        """
        node.predicate -> Expr
        node.body -> Expr
        """
        var_return = self.define_internal_local()
        var_void = self.define_internal_local()
        
        self.register_instruction(cil.AllocateNode(f'type_{scope.ctype.OBJECT}', var_return))
        self.register_instruction(cil.AllocateNode(f'type_{scope.ctype.VOID}', var_void))
        
        bucle_label = cil.LabelNode(self.define_label())
        self.register_instruction(bucle_label)
        continue_bucle_label = cil.LabelNode(self.define_label())
        end_bucle_label = cil.LabelNode(self.define_label())
        
        predicate = self.visit(node.predicate, scope, cil_scope)
        self.register_instruction(cil.GotoIfNode(predicate, continue_bucle_label.name))
        self.register_instruction(cil.GotoNode(end_bucle_label.name))
        self.register_instruction(continue_bucle_label)
        self.register_instruction(cil.AssignNode(var_return, var_void))
        self.visit(node.body, scope, cil_scope)
        
        self.register_instruction(cil.GotoNode(bucle_label.name))
        self.register_instruction(end_bucle_label)
        return var_return

    
    @visitor.when(ast.Case)
    def visit(self, node, scope, cil_scope):
        """
        node.expr -> Expr
        node.actions -> Action
        """
        value = self.visit(node.expr, scope, cil_scope)
        value_type = self.define_internal_local()
        self.register_instruction(cil.TypeOfNode(value, value_type))
        data = self.types_names[scope.ctype.VOID.name].name
        void_type = self.define_internal_local()
        self.register_instruction(cil.LoadNode(void_type, data))
        
        _continue = cil.LabelNode(self.define_label())
        _error = cil.LabelNode(self.define_label())
        self.register_instruction(cil.BranchEqualNode(value_type, void_type, _error.name))
        self.register_instruction(cil.GotoNode(_continue.name))
        self.register_instruction(_error)
        error = self.register_data(f'({node.expr.lineno}, {node.expr.linepos}) - RuntimeError: Expression cant\'t be Void type.\\n')
        self.register_instruction(cil.RunTimeNode(error.name))
        self.register_instruction(_continue)
        
        _types = list()
        for action in node.actions:
            _types.append(scope.get_type(action.action_type))
        
        count = self.define_internal_local()
        self.register_instruction(cil.AllocateNode(f'type_Int', count, len(_types)))
        self.register_instruction(cil.ArgNode(value))
        self.register_instruction(cil.ArgNode(count))
        for _type in _types:
            data_node = self.register_data(_type.name)
            vdata = self.define_internal_local()
            self.register_instruction(cil.LoadNode(vdata, data_node.name))
            self.register_instruction(cil.ArgNode(vdata))
        number = self.define_internal_local()
        self.register_instruction(cil.StaticCallNode('get_number_action', number))
        
        branchs = list()
        for i in range(len(_types)):
            opt = self.define_internal_local()
            label = cil.LabelNode(self.define_label())
            self.register_instruction(cil.AllocateNode(f'type_Int', opt, i))
            self.register_instruction(cil.BranchEqualNode(number, opt, label.name))
            branchs.append(label)
        
        end_label = cil.LabelNode(self.define_label())
        data = self.register_data(f'({node.expr.lineno}, {node.expr.linepos}) - RuntimeError: None branch selected\\n')
        self.register_instruction(cil.RunTimeNode(data.name))
        vname = self.define_internal_local()
        
        for i in range(len(_types)):
            self.register_instruction(branchs[i])
            new_cil_scope = cil_scope.create_child()
            action_type = scope.get_type(node.actions[i].action_type)
            id = self.register_local(VariableInfo(node.actions[i].name, action_type))
            new_cil_scope.define_variable(node.actions[i].name, id, action_type)
            self.register_instruction(cil.AssignNode(id, value))
            action_value = self.visit(node.actions[i].body, scope.next_child(), new_cil_scope)
            self.register_instruction(cil.AssignNode(vname, action_value))
            self.register_instruction(cil.GotoNode(end_label.name))
        
        self.register_instruction(end_label)
        return vname
    
    
    @visitor.when(ast.IntegerComplement)
    def visit(self, node, scope, cil_scope):
        """
        node.integer_expr -> Expr
        """
        value = self.visit(node.integer_expr, scope, cil_scope)
        vname = self.define_internal_local()
        self.register_instruction(cil.IntComplementNode(vname, value))
        return vname
    
    
    @visitor.when(ast.BooleanComplement)
    def visit(self, node, scope, cil_scope):
        """
        node.boolean_expr -> Expr
        """
        value = self.visit(node.boolean_expr, scope, cil_scope)
        vname = self.define_internal_local()
        self.register_instruction(cil.BoolComplementNode(vname, value))
        return vname
    
    
    @visitor.when(ast.Addition)
    def visit(self, node, scope, cil_scope):
        """
        node.first -> Expr
        node.second -> Expr
        """
        value1 = self.visit(node.first, scope, cil_scope)
        value2 = self.visit(node.second, scope, cil_scope)
        vname = self.define_internal_local()
        self.register_instruction(cil.PlusNode(vname, value1, value2))
        return vname
    
    
    @visitor.when(ast.Subtraction)
    def visit(self, node, scope, cil_scope):
        """
        node.first -> Expr
        node.second -> Expr
        """
        value1 = self.visit(node.first, scope, cil_scope)
        value2 = self.visit(node.second, scope, cil_scope)
        vname = self.define_internal_local()
        self.register_instruction(cil.MinusNode(vname, value1, value2))
        return vname
    
    @visitor.when(ast.Multiplication)
    def visit(self, node, scope, cil_scope):
        """
        node.first -> Expr
        node.second -> Expr
        """
        value1 = self.visit(node.first, scope, cil_scope)
        value2 = self.visit(node.second, scope, cil_scope)
        vname = self.define_internal_local()
        self.register_instruction(cil.StarNode(vname, value1, value2))
        return vname
    
    
    @visitor.when(ast.Division)
    def visit(self, node, scope, cil_scope):
        """
        node.first -> Expr
        node.second -> Expr
        """
        value1 = self.visit(node.first, scope, cil_scope)
        value2 = self.visit(node.second, scope, cil_scope)
        vname = self.define_internal_local()
        self.register_instruction(cil.DivNode(vname, value1, value2))
        return vname
    
    
    @visitor.when(ast.Equal)
    def visit(self, node, scope, cil_scope):
        """
        node.first -> Expr
        node.second -> Expr
        """
        first = self.visit(node.first, scope, cil_scope)
        second = self.visit(node.second, scope, cil_scope)
        
        then_label = cil.LabelNode(self.define_label())
        out_label = cil.LabelNode(self.define_label())
        self.register_instruction(cil.BranchEqualNode(first, second, then_label.name))
        
        vname = self.define_internal_local()
        self.register_instruction(cil.AllocateNode(f'type_{scope.ctype.BOOL}', vname, 0))
        self.register_instruction(cil.GotoNode(out_label.name))
        
        self.register_instruction(then_label)
        self.register_instruction(cil.AllocateNode(f'type_{scope.ctype.BOOL}', vname, 1))
        self.register_instruction(out_label)
        return vname
    
    
    @visitor.when(ast.LessThan)
    def visit(self, node, scope, cil_scope):
        """
        node.first -> Expr
        node.second -> Expr
        """
        first = self.visit(node.first, scope, cil_scope)
        second = self.visit(node.second, scope, cil_scope)
        
        then_label = cil.LabelNode(self.define_label())
        out_label = cil.LabelNode(self.define_label())
        self.register_instruction(cil.BranchLTNode(first, second, then_label.name))
        
        vname = self.define_internal_local()
        self.register_instruction(cil.AllocateNode(f'type_{scope.ctype.BOOL}', vname, 0))
        self.register_instruction(cil.GotoNode(out_label.name))
        
        self.register_instruction(then_label)
        self.register_instruction(cil.AllocateNode(f'type_{scope.ctype.BOOL}', vname, 1))
        self.register_instruction(out_label)
        return vname
    
    
    @visitor.when(ast.LessThanOrEqual)
    def visit(self, node, scope, cil_scope):
        """
        node.first -> Expr
        node.second -> Expr
        """
        first = self.visit(node.first, scope, cil_scope)
        second = self.visit(node.second, scope, cil_scope)
        
        then_label = cil.LabelNode(self.define_label())
        out_label = cil.LabelNode(self.define_label())
        self.register_instruction(cil.BranchLENode(first, second, then_label.name))
        
        vname = self.define_internal_local()
        self.register_instruction(cil.AllocateNode(f'type_{scope.ctype.BOOL}', vname, 0))
        self.register_instruction(cil.GotoNode(out_label.name))
        
        self.register_instruction(then_label)
        self.register_instruction(cil.AllocateNode(f'type_{scope.ctype.BOOL}', vname, 1))
        self.register_instruction(out_label)
        return vname