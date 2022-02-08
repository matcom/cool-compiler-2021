import cil_ast as cil
from BaseCOOLToCILVisitor import *
from utils import visitor
from utils.ast import *

class COOLToCILVisitor(BaseCOOLToCILVisitor):
    @visitor.on('node')
    def visit(self, node):
        pass
    
    @visitor.when(ProgramNode)
    def visit(self, node, scope):
        self.current_function = self.register_function('entry')
        instance = self.define_internal_local()
        result = self.define_internal_local()
        self.register_instruction(cil.AllocateNode('Main', instance))
        self.register_instruction(cil.ArgNode(instance))

        #self.register_instruction(cil.CallNode(self.to_function_name('main', 'Main'), result))
        self.register_instruction(cil.CallNode(result, self.to_function_name('main', 'Main'), [cil.ArgNode(instance)], 'Main'))

        self.register_instruction(cil.ReturnNode(0))
        self.current_function = None

       # self.create_built_in()

        for declaration, child_scope in zip(node.declarations, scope.children):
            self.visit(declaration, child_scope)

        return cil.ProgramNode(self.dottypes, self.dotdata, self.dotcode)

    @visitor.when(ClassDeclarationNode)
    def visit(self, node, scope):
        self.current_type = self.context.get_type(node.id)

        cil_type_node = self.register_type(self.current_type)
        cil_type_node.attributes = self.current_type.get_all_attributes()
        
        if len(cil_type_node.attributes) != 0:
            constructor = FuncDeclarationNode(node.token, [], node.token, BlockNode([], node.token))
            func_declarations = [constructor]
            self.constructors.append(node.id)
            self.current_type.define_method(self.current_type.name, [], [], self.current_type, node.pos)
            scopes = [scope] + list(scope.functions.values())
        else:
            func_declarations = []
            scopes = list(scope.functions.values())

        for attr, a_type in cil_type_node.attributes:
            cil_type_node.attributes.append((attr.name, self.to_attribute_name(attr.name, a_type.name)))
            self.initialize_attr(constructor, attr, scope)
        if cil_type_node.attributes:
            constructor.body.expr_list.append(SelfNode())

        for method, mtype in self.current_type.all_methods():
            cil_type_node.methods.append((method.name, self.to_function_name(method.name, mtype.name)))

        func_declarations += [f for f in node.features if isinstance(f, FuncDeclarationNode)] 
        for feature, child_scope in zip(func_declarations, scopes):
            self.visit(feature, child_scope)

        self.current_type = None

    @visitor.when(FuncDeclarationNode)
    def visit(self, node, scope):        
        self.current_method = self.current_type.get_method(node.id)
        cil_name = self.to_function_name(node.id, self.current_type.name)
        self.current_function = self.register_function(cil_name)

        self.register_param('self', self.current_type.name)
        for param_name, param_type in node.params:
            self.register_param(param_name, param_type.value)
        
        ret_value = self.visit(node.body, scope)
        if not isinstance(ret_value, str):
            result = self.define_internal_local()
            self.register_instruction(cil.AssignNode(result, ret_value))
            self.register_instruction(cil.ReturnNode(result))
        else:
            self.register_instruction(cil.ReturnNode(ret_value))   

        self.current_method = None

    @visitor.when(AttrDeclarationNode)
    def visit(self, node, scope):
        if node.expr:
            self.visit(node.expr, scope)
            self.register_instruction(cil.SetAttrNode(self.vself.name, node.id, scope.ret_expr, self.current_type))
        elif node.type in self.value_types:
            local_value = self.define_internal_local()
            self.register_instruction(cil.AllocateNode(node.type, local_value))
            self.register_instruction(cil.SetAttrNode(self.vself.name, node.id, local_value, self.current_type))

    @visitor.when(AssignNode)
    def visit(self, node, scope):
        var_info = scope.find_local(node.id)
        value, typex = self.visit(node.expr, scope)
        if var_info is None:
            var_info = scope.find_attribute(node.id)
            attributes_names = [attr.name for attr, attr_type in self.current_type.get_all_attributes()]
            self.register_instruction(cil.SetAttrNode('self', var_info.name, self.current_type.name, value))
        else:
            local_name = self.to_variable_name(var_info.name)
            self.register_instruction(cil.AssignNode(local_name, value))
        return value, typex

    @visitor.when(FuncCallNode)
    def visit(self, node, scope):
        obj, otype = self.visit(node.obj, scope)
        
        meth = otype.get_method(node.id)
        args_node = [cil.ArgNode(obj)] + self.handle_arguments(node.args, scope, meth.param_types)

        rtype = meth.return_type
        result = None if isinstance(rtype, VoidType) else self.define_internal_local()

        continue_label = cil.LabelNode(f'continue__{self.index}') 
        isvoid = self.check_void(obj)
        self.register_instruction(cil.IfGoToNode(isvoid, continue_label.label))
        self.register_instruction(cil.ErrorNode('dispatch_error'))
        self.register_instruction(continue_label)

        #desambiguar segun sea el llamado, dinamico o estatico
        # self.register_instruction(cil.StaticCallNode(node.type, node.id, result, args_node, rtype.name))
        # return result, self._return_type(otype, node)

        # self.register_instruction(cil.DynamicCallNode(self.current_type.name, 'self', node.id, result, args_node, rtype.name))
        # return result, self._return_type(self.current_type, node)

        # if otype in [StringType(), IntType(), BoolType()]:
        #     self.register_instruction(cil.StaticCallNode(otype.name, node.id, result, args_node, rtype.name))
        # else:
        #     self.register_instruction(cil.DynamicCallNode(otype.name, obj, node.id, result, args_node, rtype.name))
        # return result, self._return_type(otype, node)

        return

    @visitor.when(IfNode)
    def visit(self, node, scope):
        vcondition = self.define_internal_local()
        value = self.visit(node.condition, scope)

        then_label_node = self.register_label('then_label')
        else_label_node = self.register_label('else_label')
        continue_label_node = self.register_label('continue_label')

        #If condition GOTO then_label
        self.visit(node.condition)
        self.register_instruction(cil.GetAttrNode(vcondition, scope.ret_expr, 'value', 'Bool'))
        self.register_instruction(cil.IfGoToNode(vcondition, then_label_node.label))
        #GOTO else_label
        self.register_instruction(cil.GoToNode(else_label_node.label))
        #Label then_label
        self.register_instruction(then_label_node)
        self.visit(node.then_expr, scope)
        self.register_instruction(cil.AssignNode(vcondition, scope.ret_expr))
        self.register_instruction(cil.GoToNode(continue_label_node.label))
        #Label else_label
        self.register_instruction(else_label_node)
        self.visit(node.else_expr, scope)
        self.register_instruction(cil.AssignNode(vcondition, scope.ret_expr))

        self.register_instruction(continue_label_node)
        scope.ret_expr = vcondition

    @visitor.when(WhileNode)
    def visit(self, node, scope):
        start_label = cil.LabelNode(f'start__{self.idx}')
        end_label = cil.LabelNode(f'end__{self.idx}')
        
        result = self.define_internal_local()
        self.register_instruction(cil.VoidConstantNode(result))
        self.register_instruction(start_label)

        cond, _ = self.visit(node.cond, scope)
        self.register_instruction(cil.IfGoToNode(cond, end_label.label))
        expr, typex = self.visit(node.expr, scope)
        self.register_instruction(cil.AssignNode(result, expr))
        self.register_instruction(cil.GoToNode(start_label.label))
        self.register_instruction(end_label)
        
    @visitor.when(BlockNode)
    def visit(self, node, scope):
        for expr in node.exprs:
            value, typex = self.visit(expr, scope)
        result = self.define_internal_local()
        self.register_instruction(cil.AssignNode(result, value))
        return result, typex

    visitor.when(LetNode)
    def visit(self, node, scope):
        child_scope = scope.expr_dict[node]
        for init in node.let_attrs:
            self.visit(init, child_scope)
        
        expr, typex = self.visit(node.expr, child_scope)
        return expr, typex

    visitor.when(CaseNode)
    def visit(self, node, scope):
        expr, typex = self.visit(node.expr, scope)
        
        result = self.define_internal_local()
        end_label = cil.LabelNode(f'end__{self.idx}')
        error_label = cil.LabelNode(f'error__{self.idx}')
     
        isvoid = self.check_void(expr)
        self.register_instruction(cil.IfGoToNode(isvoid, error_label.label))
        try:
            new_scope = scope.expr_dict[node]
        except:
            new_scope = scope
        sorted_case_list = self.sort_option_nodes_by_type(node.case_list)
        for i, case in enumerate(sorted_case_list):
            next_label = cil.LabelNode(f'next__{self.idx}_{i}')
            expr_i = self.visit(case, new_scope.create_child(), expr, next_label, typex)
            self.register_instruction(cil.AssignNode(result, expr_i))
            self.register_instruction(cil.GoToNode(end_label.label))
            self.register_instruction(next_label)
        self.register_instruction(end_label)
        return result, typex

    visitor.when(VarNode)
    def visit(self, node, scope):
        try:
            typex = scope.find_local(node.lex).type
            name = self.to_var_name(node.lex)
            return name, get_type(typex, self.current_type)
        except:
            var_info = scope.find_attribute(node.lex)
            local_var = self.register_local(var_info.name)
            self.register_instruction(cil.GetAttrNode('self', var_info.name, self.current_type.name, local_var, var_info.type.name))
            return local_var, get_type(var_info.type, self.current_type)

    visitor.when(NewNode)
    def visit(self, node, scope):
        instance = self.define_internal_local()
        typex = self.context.get_type(node.lex)
        typex = get_type(typex, self.current_type)
        self.register_instruction(cil.AllocateNode(typex.name, instance))
        
        if typex.get_all_attributes():
            self.register_instruction(cil.CallNode(typex.name, typex.name, instance, [cil.ArgNode(instance)], typex.name))
        
        return instance, typex

    @visitor.when(PlusNode)
    def visit(self, node, scope):
        return self._define_binary_node(node, scope, cil.PlusNode)

    @visitor.when(MinusNode)
    def visit(self, node, scope):
        return self._define_binary_node(node, scope, cil.MinusNode)

    @visitor.when(StarNode)
    def visit(self, node, scope):
        return self._define_binary_node(node, scope, cil.StarNode)

    @visitor.when(DivNode)
    def visit(self, node, scope):
        return self._define_binary_node(node, scope, cil.DivNode)

    @visitor.when(LessNode)
    def visit(self, node, scope):
        return self._define_binary_node(node, scope, cil.LessNode)
        
    @visitor.when(LessEqNode)
    def visit(self, node, scope):
        return self._define_binary_node(node, scope, cil.LessEqualNode)

    @visitor.when(EqualNode)
    def visit(self, node, scope):
        return self._define_binary_node(node, scope, cil.EqualNode)

#nuevo cambio

