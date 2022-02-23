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
        self.register_instruction(cil.VCallNode(
            result_local, node.method, call_args, dynamic_type, expr_value))

        return result_local

    @visitor.when(MemberCallNode)
    def visit(self, node, scope):
        result_local = self.define_internal_local(scope=scope, name="result")

        call_args = []
        for arg in reversed(node.args):
            param_local = self.visit(arg, scope)
            call_args.append(cil.ArgNode(param_local))

        self.register_instruction(cil.VCallNode(
            result_local, node.method, call_args, 'self', 'memberCallGuayaba'))

        return result_local

    @visitor.when(IfThenElseNode)
    def visit(self, node, scope):
        result_local = self.define_internal_local(scope=scope, name="result")

        cond_value = self.visit(node.condition, scope)

        if_then_label = self.get_label()
        self.register_instruction(cil.IfGoToNode(cond_value, if_then_label))

        else_value = self.visit(node.elseBody, scope)
        self.register_instruction(cil.AssignNode(result_local, else_value))

        end_if_label = self.get_label()
        self.register_instruction(cil.GoToNode(end_if_label))

        self.register_instruction(cil.LabelNode(if_then_label))
        then_value = self.visit(node.ifBody, scope)
        self.register_instruction(cil.AssignNode(result_local, then_value))
        self.register_instruction(cil.LabelNode(end_if_label))

        return result_local

    @visitor.when(WhileNode)
    def visit(self, node, scope):
        result_local = self.define_internal_local(scope=scope, name="result")

        loop_init_label = self.get_label()
        loop_body_label = self.get_label()
        loop_end_label = self.get_label()
        self.register_instruction(cil.LabelNode(loop_init_label))
        pred_value = self.visit(node.condition, scope)
        self.register_instruction(cil.IfGoToNode(pred_value, loop_body_label))
        self.register_instruction(cil.GoToNode(loop_end_label))

        self.register_instruction(cil.LabelNode(loop_body_label))
        body_value = self.visit(node.body, scope)
        self.register_instruction(cil.GoToNode(loop_init_label))
        self.register_instruction(cil.LabelNode(loop_end_label))

        self.register_instruction(cil.LoadVoidNode(result_local))
        return result_local

    @visitor.when(BlockNode)
    def visit(self, node, scope):
        for expr in node.exprs:
            result_local = self.visit(expr, scope)
        return result_local

    @visitor.when(LetNode)
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
        expr_value = self.visit(node.expr, scope)
        result_local = self.define_internal_local(
            scope=scope, name="isvoid_result")
        self.register_instruction(cil.IsVoidNode(result_local, expr_value))
        instance = self.define_internal_local(scope=scope, name="instance")
        self.register_instruction(cil.AllocateNode(
            'Bool', self.context.get_type('Bool').tag, instance))
        result_init = self.define_internal_local(
            scope=scope, name="result_init")
        self.register_instruction(cil.CallNode(result_init, 'Bool_init', [
                                  cil.ArgNode(result_local), cil.ArgNode(instance)], "Bool"))
        return instance

    @visitor.when(PlusNode)
    def visit(self, node, scope):
        result_local = self.define_internal_local(scope=scope, name="result")
        op_local = self.define_internal_local(scope=scope, name="op")
        left_local = self.define_internal_local(scope=scope, name="left")
        right_local = self.define_internal_local(scope=scope, name="right")

        left_value = self.visit(node.lvalue, scope)
        right_value = self.visit(node.rvalue, scope)

        self.register_instruction(cil.GetAttrNode(
            left_local, left_value, "value", node.lvalue.computed_type.name))
        self.register_instruction(cil.GetAttrNode(
            right_local, right_value, "value", node.rvalue.computed_type.name))

        self.register_instruction(cil.BinaryOperationNode(
            op_local, left_local, right_local, "+"))

        # Allocate Int result
        self.register_instruction(cil.AllocateNode(
            'Int', self.context.get_type('Int').tag, result_local))
        result_init = self.define_internal_local(
            scope=scope, name="result_init")
        self.register_instruction(cil.CallNode(result_init, 'Int_init', [
                                  cil.ArgNode(op_local), cil.ArgNode(result_local)], "Int"))

        return result_local

    @visitor.when(MinusNode)
    def visit(self, node, scope):
        result_local = self.define_internal_local(scope=scope, name="result")
        op_local = self.define_internal_local(scope=scope, name="op")
        left_local = self.define_internal_local(scope=scope, name="left")
        right_local = self.define_internal_local(scope=scope, name="right")

        left_value = self.visit(node.lvalue, scope)
        right_value = self.visit(node.rvalue, scope)

        self.register_instruction(cil.GetAttrNode(
            left_local, left_value, "value", node.lvalue.computed_type.name))
        self.register_instruction(cil.GetAttrNode(
            right_local, right_value, "value", node.rvalue.computed_type.name))

        self.register_instruction(cil.BinaryOperator(
            op_local, left_local, right_local, "-"))

        # Allocate Int result
        self.register_instruction(cil.AllocateNode(
            'Int', self.context.get_type('Int').tag, result_local))
        result_init = self.define_internal_local(
            scope=scope, name="result_init")
        self.register_instruction(cil.CallNode(result_init, 'Int_init', [
                                  cil.ArgNode(op_local), cil.ArgNode(result_local)], "Int"))

        return result_local

    @visitor.when(StarNode)
    def visit(self, node, scope):
        result_local = self.define_internal_local(scope=scope, name="result")
        op_local = self.define_internal_local(scope=scope, name="op")
        left_local = self.define_internal_local(scope=scope, name="left")
        right_local = self.define_internal_local(scope=scope, name="right")

        left_value = self.visit(node.lvalue, scope)
        right_value = self.visit(node.rvalue, scope)

        self.register_instruction(cil.GetAttrNode(
            left_local, left_value, "value", node.lvalue.computed_type.name))
        self.register_instruction(cil.GetAttrNode(
            right_local, right_value, "value", node.rvalue.computed_type.name))

        self.register_instruction(cil.BinaryOperator(
            op_local, left_local, right_local, "*"))

        # Allocate Int result
        self.register_instruction(cil.AllocateNode(
            'Int', self.context.get_type('Int').tag, result_local))
        result_init = self.define_internal_local(
            scope=scope, name="result_init")
        self.register_instruction(cil.CallNode(result_init, 'Int_init', [
                                  cil.ArgNode(op_local), cil.ArgNode(result_local)], "Int"))

        return result_local

    @visitor.when(DivNode)
    def visit(self, node, scope):
        result_local = self.define_internal_local(scope=scope, name="result")
        op_local = self.define_internal_local(scope=scope, name="op")
        left_local = self.define_internal_local(scope=scope, name="left")
        right_local = self.define_internal_local(scope=scope, name="right")

        left_value = self.visit(node.lvalue, scope)
        right_value = self.visit(node.rvalue, scope)

        self.register_instruction(cil.GetAttrNode(
            left_local, left_value, "value", node.lvalue.computed_type.name))
        self.register_instruction(cil.GetAttrNode(
            right_local, right_value, "value", node.rvalue.computed_type.name))

        self.register_instruction(cil.BinaryOperator(
            op_local, left_local, right_local, "/"))

        # Allocate Int result
        self.register_instruction(cil.AllocateNode(
            'Int', self.context.get_type('Int').tag, result_local))
        result_init = self.define_internal_local(
            scope=scope, name="result_init")
        self.register_instruction(cil.CallNode(result_init, 'Int_init', [
                                  cil.ArgNode(op_local), cil.ArgNode(result_local)], "Int"))

        return result_local

    @visitor.when(LessNode)
    def visit(self, node, scope):
        result_local = self.define_internal_local(scope=scope, name="result")
        op_local = self.define_internal_local(scope=scope, name="op")
        left_local = self.define_internal_local(scope=scope, name="left")
        right_local = self.define_internal_local(scope=scope, name="right")

        left_value = self.visit(node.lvalue, scope)
        right_value = self.visit(node.rvalue, scope)

        self.register_instruction(cil.GetAttrNode(
            left_local, left_value, "value", node.lvalue.computed_type.name))
        self.register_instruction(cil.GetAttrNode(
            right_local, right_value, "value", node.rvalue.computed_type.name))

        self.register_instruction(cil.BinaryOperationNode(
            op_local, left_local, right_local, "<"))

        # Allocate Bool result
        self.register_instruction(cil.AllocateNode(
            'Bool', self.context.get_type('Bool').tag, result_local))
        result_init = self.define_internal_local(
            scope=scope, name="result_init")
        self.register_instruction(cil.CallNode(result_init, 'Bool_init', [
                                  cil.ArgNode(op_local), cil.ArgNode(result_local)], "Bool"))

        return result_local

    @visitor.when(LessEqNode)
    def visit(self, node, scope):
        result_local = self.define_internal_local(scope=scope, name="result")
        op_local = self.define_internal_local(scope=scope, name="op")
        left_local = self.define_internal_local(scope=scope, name="left")
        right_local = self.define_internal_local(scope=scope, name="right")

        left_value = self.visit(node.lvalue, scope)
        right_value = self.visit(node.rvalue, scope)

        self.register_instruction(cil.GetAttrNode(
            left_local, left_value, "value", node.lvalue.computed_type.name))
        self.register_instruction(cil.GetAttrNode(
            right_local, right_value, "value", node.rvalue.computed_type.name))

        self.register_instruction(cil.BinaryOperationNode(
            op_local, left_local, right_local, "<="))

        # Allocate Bool result
        self.register_instruction(cil.AllocateNode(
            'Bool', self.context.get_type('Bool').tag, result_local))
        result_init = self.define_internal_local(
            scope=scope, name="result_init")
        self.register_instruction(cil.CallNode(result_init, 'Bool_init', [
                                  cil.ArgNode(op_local), cil.ArgNode(result_local)], "Bool"))

        return result_local

    @visitor.when(EqualNode)
    def visit(self, node, scope):
        result_local = self.define_internal_local(scope=scope, name="result")
        op_local = self.define_internal_local(scope=scope, name="op")
        left_local = self.define_internal_local(scope=scope, name="left")
        right_local = self.define_internal_local(scope=scope, name="right")

        left_value = self.visit(node.lvalue, scope)
        right_value = self.visit(node.rvalue, scope)

        if node.lvalue.computed_type.name == 'String':
            self.register_instruction(cil.CallNode(op_local, 'String_equals', [
                                      cil.ArgNode(right_value), cil.ArgNode(left_value)], 'String'))

            # Allocate Bool result
            self.register_instruction(cil.AllocateNode(
                'Bool', self.context.get_type('Bool').tag, result_local))
            result_init = self.define_internal_local(
                scope=scope, name="result_init")
            self.register_instruction(cil.CallNode(result_init, 'Bool_init', [
                                      cil.ArgNode(op_local), cil.ArgNode(result_local)], "Bool"))

            return result_local

        elif node.lvalue.computed_type.name in ['Int', 'Bool']:
            self.register_instruction(cil.GetAttrNode(
                left_local, left_value, "value", node.lvalue.computed_type.name))
            self.register_instruction(cil.GetAttrNode(
                right_local, right_value, "value", node.rvalue.computed_type.name))
        else:
            self.register_instruction(cil.AssignNode(left_local, left_value))
            self.register_instruction(cil.AssignNode(right_local, right_value))

        self.register_instruction(cil.BinaryOperationNode(
            op_local, left_local, right_local, "="))

        # Allocate Bool result
        self.register_instruction(cil.AllocateNode(
            'Bool', self.context.get_type('Bool').tag, result_local))
        result_init = self.define_internal_local(
            scope=scope, name="result_init")
        self.register_instruction(cil.CallNode(result_init, 'Bool_init', [
                                  cil.ArgNode(op_local), cil.ArgNode(result_local)], "Bool"))

        return result_local
