import cil_ast as cil
from BaseCoolToCilVisitor import BaseCOOLToCILVisitor
from semantic.semantic import Scope, VariableInfo
from utils import visitor
from utils.ast import *


class COOLToCILVisitor(BaseCOOLToCILVisitor):
    @visitor.on('node')
    def visit(self, node, scope):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node, scope=None):
        scope = Scope()
        self.current_function = self.register_function('main')
        instance = self.define_internal_local(scope=scope, name="instance")
        result = self.define_internal_local(scope=scope, name="result")
        self.register_instruction(cil.AllocateNode(
            'Main', self.context.get_type('Main').tag, instance))
        self.register_instruction(cil.CallNode(
            result, 'Main_init', [cil.ArgNode(instance)], "Main"))
        self.register_instruction(cil.CallNode(result, self.to_function_name(
            'main', 'Main'), [cil.ArgNode(instance)], "Main"))
        self.register_instruction(cil.ReturnNode(None))
        self.current_function = None

        self.register_data('Abort called from class ')
        self.register_data('\n')
        self.dotdata['empty_str'] = ''

        # Add built-in types in .TYPES section
        self.register_builtin_types(scope)

        # Add string equals function
        self.build_string_equals_function(scope)

        for declaration in node.declarations:
            self.visit(declaration, scope.create_child())

        return cil.ProgramNode(self.dottypes, self.dotdata, self.dotcode)

    @visitor.when(ClassDeclarationNode)
    def visit(self, node, scope):
        self.current_type = self.context.get_type(node.id)

        # Handle all the .TYPE section
        cil_type = self.register_type(self.current_type.name)
        cil_type.attributes = [f'{attr.name}' for c,
                               attr in self.current_type.get_all_attributes()]
        cil_type.methods = {f'{m}': f'{c}.{m}' for c,
                            m in self.current_type.get_all_methods()}

        scope.define_cil_local(
            "self", self.current_type.name, self.current_type)

        func_declarations = [
            f for f in node.features if isinstance(f, FuncDeclarationNode)]
        attr_declarations = [
            a for a in node.features if isinstance(a, AttrDeclarationNode)]
        for attr in attr_declarations:
            scope.define_cil_local(attr.id, attr.id, node.id)

        # -------------------------Init---------------------------------
        self.current_function = self.register_function(f'{node.id}_init')
        self.register_param(VariableInfo('self', None))

        # Init parents recursively
        result = self.define_internal_local(scope=scope, name="result")
        self.register_instruction(cil.CallNode(result, f'{node.parent}_init', [
                                  cil.ArgNode('self')], node.parent))
        self.register_instruction(cil.ReturnNode(None))

        for attr in attr_declarations:
            self.visit(attr, scope)
        # ---------------------------------------------------------------
        self.current_function = None

        for func in func_declarations:
            self.visit(func, scope.create_child())

        self.current_type = None

    @visitor.when(FuncDeclarationNode)
    def visit(self, node, scope):
        self.current_method = self.current_type.get_method(node.id)
        self.dottypes[self.current_type.name].methods[
            node.id] = f'{self.current_type.name}.{node.id}'
        cil_method_name = self.to_function_name(
            node.id, self.current_type.name)
        self.current_function = self.register_function(cil_method_name)

        self.register_param(VariableInfo('self', self.current_type))
        for pname, ptype, _, _ in node.params:
            self.register_param(VariableInfo(pname, ptype))

        value = self.visit(node.body, scope)

        self.register_instruction(cil.ReturnNode(value))
        self.current_method = None

    @visitor.when(AttrDeclarationNode)
    def visit(self, node, scope):
        instance = None

        if node.type in ['Int', 'Bool']:
            instance = self.define_internal_local(scope=scope, name="instance")
            self.register_instruction(cil.AllocateNode(
                node.type, self.context.get_type(node.type).tag, instance))
            value = self.define_internal_local(scope=scope, name="value")
            self.register_instruction(cil.LoadIntNode(0, value))
            result_init = self.define_internal_local(
                scope=scope, name="result_init")
            self.register_instruction(cil.CallNode(result_init, f'{node.type}_init', [
                                      cil.ArgNode(value), cil.ArgNode(instance)], node.type))
        elif node.type == 'String':
            instance = self.define_internal_local(scope=scope, name="instance")
            self.register_instruction(cil.AllocateNode(
                node.type, self.context.get_type(node.type).tag, instance))
            value = self.define_internal_local(scope=scope, name="value")
            self.register_instruction(cil.LoadStringNode('empty_str', value))
            result_init = self.define_internal_local(
                scope=scope, name="result_init")
            self.register_instruction(cil.CallNode(result_init, f'{node.type}_init', [
                                      cil.ArgNode(value), cil.ArgNode(instance)], node.type))

        if not node.expr is None:
            expr = self.visit(node.expr, scope)
            self.register_instruction(cil.SetAttrNode(
                'self', node.id, expr, self.current_type.name))
        else:
            self.register_instruction(cil.SetAttrNode(
                'self', node.id, instance, self.current_type.name))

    @visitor.when(AssignNode)
    def visit(self, node, scope):
        expr_local = self.visit(node.expr, scope)
        result_local = self.define_internal_local(scope=scope, name="result")
        cil_node_name = scope.find_cil_local(node.id)

        if self.is_defined_param(node.id):
            self.register_instruction(cil.AssignNode(node.id, expr_local))
        elif self.current_type.has_attr(node.id):
            cil_type_name = 'self'
            self.register_instruction(cil.SetAttrNode(
                cil_type_name, node.id, expr_local, self.current_type.name))
        else:
            self.register_instruction(
                cil.AssignNode(cil_node_name, expr_local))
        return expr_local

    @visitor.when(ArrobaCallNode)
    def visit(self, node, scope):
        result_local = self.define_internal_local(scope=scope, name="result")
        expr_value = self.visit(node.obj, scope)

        call_args = []
        for arg in reversed(node.args):
            param_local = self.visit(arg, scope)
            call_args.append(cil.ArgNode(param_local))
        call_args.append(cil.ArgNode(expr_value))

        static_instance = self.define_internal_local(
            scope=scope, name='static_instance')
        self.register_instruction(cil.AllocateNode(
            node.type, self.context.get_type(node.type).tag, static_instance))

        self.register_instruction(cil.VCallNode(
            result_local, node.id, call_args, node.type, static_instance))
        return result_local

    @visitor.when(DotCallNode)
    def visit(self, node, scope):
        result_local = self.define_internal_local(scope=scope, name="result")
        expr_value = self.visit(node.obj, scope)

        call_args = []
        for arg in reversed(node.args):
            param_local = self.visit(arg, scope)
            call_args.append(cil.ArgNode(param_local))
        call_args.append(cil.ArgNode(expr_value))

        dynamic_type = node.obj.computed_type.name
        self.register_instruction(CIL_AST.VCall(
            result_local, node.method, call_args, dynamic_type, expr_value))

        return result_local

    @visitor.when(MemberCallNode)
    def visit(self, node, scope):
        result_local = self.define_internal_local(scope=scope, name="result")
        expr_value = self.visit(node.instance, scope)

        member_call_args = []
        for arg in node.args:
            param_local = self.visit(arg, scope)
            member_call_args.append(cil.ArgNode(param_local))
        member_call_args.append(cil.ArgNode(expr_value))

        dynamic_type = node.instance.computed_type.name
        self.register_instruction(cil.VCallNode(
            result_local, node.method, member_call_args, dynamic_type, expr_value))

        return result_local

    @visitor.when(IfNode)
    def visit(self, node, scope):
        vcondition = self.define_internal_local()
        value = self.visit(node.condition, scope)

        then_label_node = self.register_label('then_label')
        else_label_node = self.register_label('else_label')
        continue_label_node = self.register_label('continue_label')

        # If condition GOTO then_label
        self.visit(node.condition)
        self.register_instruction(cil.GetAttrNode(
            vcondition, scope.ret_expr, 'value', 'Bool'))
        self.register_instruction(cil.IfGoToNode(
            vcondition, then_label_node.label))
        # GOTO else_label
        self.register_instruction(cil.GoToNode(else_label_node.label))
        # Label then_label
        self.register_instruction(then_label_node)
        self.visit(node.then_expr, scope)
        self.register_instruction(cil.AssignNode(vcondition, scope.ret_expr))
        self.register_instruction(cil.GoToNode(continue_label_node.label))
        # Label else_label
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

        return result, ObjectType()

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
            expr_i = self.visit(
                case, new_scope.create_child(), expr, next_label, typex)
            self.register_instruction(cil.AssignNode(result, expr_i))
            self.register_instruction(cil.GoToNode(end_label.label))
            self.register_instruction(next_label)
        self.register_instruction(end_label)
        return result, typex

# this find_local, find_attribute is from scope, this get_type is separate, need to do it well
    visitor.when(VarNode)

    def visit(self, node, scope):
        try:
            typex = scope.find_local(node.lex).type
            name = self.to_variable_name(node.lex)
            return name, get_type(typex, self.current_type)
        except:
            var_info = scope.find_attribute(node.lex)
            local_var = self.register_local(var_info.name)
            self.register_instruction(cil.GetAttrNode(
                'self', var_info.name, self.current_type.name, local_var, var_info.type.name))
            return local_var, get_type(var_info.type, self.current_type)

    visitor.when(NewNode)

    def visit(self, node, scope):
        instance = self.define_internal_local()
        typex = self.context.get_type(node.lex)
        typex = get_type(typex, self.current_type)
        self.register_instruction(cil.AllocateNode(typex.name, instance))

        if typex.get_all_attributes():
            self.register_instruction(cil.CallNode(typex.name, typex.name, instance, [
                                      cil.ArgNode(instance)], typex.name))

        return instance, typex

    @visitor.when(NegationNode)
    def visit(self, node, scope):
        return self._define_unary_node(node, scope, cil.NotNode)

    @visitor.when(IsVoidNode)
    def visit(self, node, scope):
        expr, _ = self.visit(node.expr, scope)
        result = self.check_void(expr)
        return result, BoolType()

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
