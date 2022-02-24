import code_generator.cil_ast as cil
from code_generator.BaseCoolToCilVisitor import BaseCOOLToCILVisitor
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
        self.define_built_in(scope)

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
            result_local, node.id, call_args, dynamic_type, expr_value))

        return result_local

    @visitor.when(MemberCallNode)
    def visit(self, node, scope):
        result_local = self.define_internal_local(scope=scope, name="result")

        call_args = []
        for arg in reversed(node.args):
            param_local = self.visit(arg, scope)
            call_args.append(cil.ArgNode(param_local))
        call_args.append(cil.ArgNode("self"))

        self.register_instruction(cil.VCallNode(
            result_local, node.id, call_args, node.static_type.name, "self"))

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

    @visitor.when(LetInNode)
    def visit(self, node, scope):
        let_scope = scope.create_child()
        for var in node.letBody:
            self.visit(var, let_scope)

        body_value = self.visit(node.inBody, let_scope)
        result_local = self.define_internal_local(
            scope=scope, name="let_result")
        self.register_instruction(cil.AssignNode(result_local, body_value))
        return result_local

    @visitor.when(VarDeclarationNode)
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
            expr_value = self.visit(node.expr, scope)
            let_var = self.define_internal_local(
                scope=scope, name=node.id, cool_var=node.id)
            self.register_instruction(cil.AssignNode(let_var, expr_value))
        else:
            let_var = self.define_internal_local(
                scope=scope, name=node.id, cool_var=node.id)
            self.register_instruction(cil.AssignNode(let_var, instance))

        return let_var

    @visitor.when(CaseNode)
    def visit(self, node, scope):
        result_local = self.define_internal_local(scope=scope, name="result")
        case_expr = self.visit(node.expr, scope)

        exit_label = self.get_label()
        label = self.get_label()

        self.register_instruction(cil.CaseNode(case_expr, label))

        tag_lst = []
        option_dict = {}
        for option in node.optionList:
            tag = self.context.get_type(option.type).tag
            tag_lst.append(tag)
            option_dict[tag] = option
        tag_lst.sort()

        for t in reversed(tag_lst):
            option = option_dict[t]
            self.register_instruction(cil.LabelNode(label))
            label = self.get_label()

            option_type = self.context.get_type(option.type)
            self.register_instruction(cil.CaseOptionNode(
                case_expr, option_type.tag, option_type.max_tag, label))

            option_scope = scope.create_child()
            option_id = self.define_internal_local(
                scope=option_scope, name=option.id, cool_var=option.id)
            self.register_instruction(cil.AssignNode(option_id, case_expr))
            expr_result = self.visit(option.expr, option_scope)

            self.register_instruction(
                cil.AssignNode(result_local, expr_result))
            self.register_instruction(cil.GoToNode(exit_label))

        self.register_instruction(cil.LabelNode(label))
        self.register_instruction(cil.GoToNode('case_no_match_error'))
        self.register_instruction(cil.LabelNode(exit_label))
        return result_local

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

        self.register_instruction(cil.BinaryOperationNode(
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

        self.register_instruction(cil.BinaryOperationNode(
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

        self.register_instruction(cil.BinaryOperationNode(
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

    @visitor.when(NegationNode)
    def visit(self, node, scope):
        result_local = self.define_internal_local(scope=scope, name="result")
        op_local = self.define_internal_local(scope=scope, name="op")
        expr_local = self.define_internal_local(scope=scope)

        expr_value = self.visit(node.expr, scope)

        self.register_instruction(cil.GetAttrNode(
            expr_local, expr_value, "value", node.expr.computed_type.name))
        self.register_instruction(
            cil.UnaryOperationNode(op_local, expr_local, "~"))

        # Allocate Int result
        self.register_instruction(cil.AllocateNode(
            'Int', self.context.get_type('Int').tag, result_local))
        result_init = self.define_internal_local(
            scope=scope, name="result_init")
        self.register_instruction(cil.CallNode(result_init, 'Int_init', [
                                  cil.ArgNode(op_local), cil.ArgNode(result_local)], "Int"))

        return result_local

    @visitor.when(LogicNegationNode)
    def visit(self, node, scope):
        result_local = self.define_internal_local(scope=scope, name="result")
        op_local = self.define_internal_local(scope=scope, name="op")
        expr_local = self.define_internal_local(scope=scope)

        expr_value = self.visit(node.expr, scope)

        self.register_instruction(cil.GetAttrNode(
            expr_local, expr_value, "value", node.expr.computed_type.name))
        self.register_instruction(
            cil.UnaryOperationNode(op_local, expr_local, "not"))

        # Allocate Bool result
        self.register_instruction(cil.AllocateNode(
            'Bool', self.context.get_type('Bool').tag, result_local))
        result_init = self.define_internal_local(
            scope=scope, name="result_init")
        self.register_instruction(cil.CallNode(result_init, 'Bool_init', [
                                  cil.ArgNode(op_local), cil.ArgNode(result_local)], "Bool"))

        return result_local

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

    @visitor.when(IdNode)
    def visit(self, node, scope):
        if self.is_defined_param(node.id):
            return node.id
        elif self.current_type.has_attr(node.id):
            result_local = self.define_internal_local(
                scope=scope, name=node.id, class_type=self.current_type.name)
            self.register_instruction(cil.GetAttrNode(
                result_local, 'self', node.id, self.current_type.name))
            return result_local
        else:
            return scope.find_cil_local(node.id)

    @visitor.when(NewNode)
    def visit(self, node, scope):
        result_local = self.define_internal_local(scope=scope, name="result")
        result_init = self.define_internal_local(scope=scope, name="init")

        if node.id == "SELF_TYPE":
            self.register_instruction(cil.AllocateNode(
                self.current_type.name, self.current_type.tag, result_local))
            self.register_instruction(cil.CallNode(result_init, f'{self.current_type.name}_init', [
                                      result_local], self.current_type.name))
        else:
            self.register_instruction(cil.AllocateNode(
                node.id, self.context.get_type(node.id).tag, result_local))
            self.register_instruction(cil.CallNode(result_init, f'{node.id}_init', [
                                      cil.ArgNode(result_local)], self.current_type.name))

        return result_local

    @visitor.when(IntNode)
    def visit(self, node, scope):
        instance = self.define_internal_local(scope=scope, name="instance")
        self.register_instruction(cil.AllocateNode(
            'Int', self.context.get_type('Int').tag, instance))
        value = self.define_internal_local(scope=scope, name="value")
        self.register_instruction(cil.LoadIntNode(node.id, value))
        result_init = self.define_internal_local(
            scope=scope, name="result_init")
        self.register_instruction(cil.CallNode(result_init, 'Int_init', [
                                  cil.ArgNode(value), cil.ArgNode(instance)], "Int"))
        return instance

    @visitor.when(StringNode)
    def visit(self, node, scope):
        str_name = ""
        for s in self.dotdata.keys():
            if self.dotdata[s] == node.id:
                str_name = s
                break
        if str_name == "":
            str_name = self.register_data(node.id)

        result_local = self.define_internal_local(scope=scope)
        self.register_instruction(cil.LoadStringNode(str_name, result_local))
        instance = self.define_internal_local(scope=scope, name="instance")
        self.register_instruction(cil.AllocateNode(
            'String', self.context.get_type('String').tag, instance))
        result_init = self.define_internal_local(
            scope=scope, name="result_init")
        self.register_instruction(cil.CallNode(result_init, 'String_init', [
                                  cil.ArgNode(result_local), cil.ArgNode(instance)], "String"))
        return instance

    @visitor.when(BoolNode)
    def visit(self, node, scope):
        boolean = 0
        if str(node.id) == "true":
            boolean = 1
        instance = self.define_internal_local(scope=scope, name="instance")
        self.register_instruction(cil.AllocateNode(
            'Bool', self.context.get_type('Bool').tag, instance))
        value = self.define_internal_local(scope=scope, name="value")
        self.register_instruction(cil.LoadIntNode(boolean, value))
        result_init = self.define_internal_local(
            scope=scope, name="result_init")
        self.register_instruction(cil.CallNode(result_init, 'Bool_init', [
                                  cil.ArgNode(value), cil.ArgNode(instance)], "Bool"))
        return instance

    @visitor.when(VoidNode)
    def visit(self, node, scope):
        result_local = self.define_internal_local(scope=scope)
        self.register_instruction(cil.LoadStringNode(node.id, result_local))
        instance = self.define_internal_local(scope=scope, name="instance")
        self.register_instruction(cil.AllocateNode(
            'String', self.context.get_type('String').tag, instance))
        result_init = self.define_internal_local(
            scope=scope, name="result_init")
        self.register_instruction(cil.CallNode(result_init, 'Void_init', [
                                  cil.ArgNode(result_local), cil.ArgNode(instance)], "String"))
        return instance
