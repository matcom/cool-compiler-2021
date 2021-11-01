from semantic.tools.error import incompatible_types_, param_wrong_signature, invalid_SELFTYPE, self_name, incorrect_count_params_, read_only_, var_not_defined_, other_branch_declared_, wrong_type_, self_let_, SemanticError, SemanticException
from semantic.tools.type import Error_Type
from semantic.tools.scope import Scope
from nodes import *
from semantic.visitor import visitor


class TypeChecker:
    def __init__(self, context, errors=[]):
        self.context = context
        self.current_type = None
        self.current_method = None
        self.errors = errors

    @visitor.on('node')
    def visit(self, node, scope):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node, scope=None):
        scope = Scope()
        for c in node.classes:
            self.visit(c, scope.create_child())
        return scope

    @visitor.when(ClassNode)
    def visit(self, node, scope):
        self.current_type = self.context.get_type(node.name)
        scope.define_variable('self', self.current_type)

        attributes = self.current_type.get_all_attributes()
        for _, attr in attributes:
            if attr.type.name == 'SELF_TYPE':
                scope.define_variable(attr.name, self.current_type)
            else:
                scope.define_variable(attr.name, attr.type)

        for feature in node.features:
            self.visit(feature, scope)

    @visitor.when(AttrInitNode)
    def visit(self, node, scope):
        try:
            node_type = self.current_type.get_attribute(node.name).type
        except SemanticException as ex:
            node_type = Error_Type()
            error =  SemanticError(ex.text, node.row, node.col, 'AttributeError')
            self.errors.append(error)
         
        self.visit(node.expression, scope)
        expr_type = node.expression.expr_type

        if not expr_type.conforms_to(node_type):
            error = SemanticError(incompatible_types_.replace(
                '%s', expr_type.name, 1).replace('%s', node_type.name, 1), node.row, node.col, 'TypeError')
            self.errors.append(error)

    @visitor.when(AttrDefNode)
    def visit(self, node, scope):
        try:
            self.current_type.get_attribute(node.name)
        except SemanticException as ex:
            error = SemanticError(ex.text, node.row, node.col, 'AttributeError')
            self.errors.append(error)

    @visitor.when(ClassMethodNode)
    def visit(self, node, scope):
        try:
            self.current_method = self.current_type.get_method(node.name)
        except SemanticException as ex:
            error = SemanticError(ex.text, node.row, node.col, 'AttributeError')
            self.errors.append(error)
        
        method_scope = scope.create_child()

        for param in node.params:
            self.visit(param, method_scope)

        self.visit(node.expression, method_scope)

        expr_type = node.expression.expr_type

        return_type = self.current_method.return_type

        if expr_type.name == 'SELF_TYPE':
            if not self.current_type.conforms_to(return_type):
                error = SemanticError(incompatible_types_.replace(
                    '%s', expr_type.name, 1).replace('%s', self.current_type.name, 1), node.row, node.col, 'TypeError')
                self.errors.append(error)
        elif not expr_type.conforms_to(return_type):
            error = SemanticError(incompatible_types_.replace(
                '%s', expr_type.name, 1).replace('%s', return_type.name, 1), node.row, node.col, 'TypeError')
            self.errors.append(error)


    @visitor.when(FormalParamNode)
    def visit(self, node, scope):
        try:
            node_type = self.context.get_type(node.param_type)
            if node_type.name == 'SELF_TYPE':
                node_type = Error_Type()
                error = SemanticError(invalid_SELFTYPE, node.row, node.col)
                self.errors.append(error)
               
        except SemanticException as ex:
            node_type = Error_Type()
            error = SemanticError(ex.text, node.row, node.col, 'TypeError')
            self.errors.append(error)

        if node.name == 'self':
            error = SemanticError(self_name, node.row, node.col)
            self.errors.append(error)            
        elif not scope.is_local(node.name):
            scope.define_variable(node.name, node_type)
        else:
            error = SemanticError(param_wrong_signature.replace(
                '%s', node.name, 1).replace('%s', self.current_method.name, 1), node.row, node.col)
            self.errors.append(error)

    @visitor.when(DynamicCallNode)
    def visit(self, node, scope):
        self.visit(node.obj, scope)
        instance_type = node.obj.expr_type

        if instance_type.name == 'SELF_TYPE':
            instance_type = scope.find_variable('self').type
        try:
            instance_method = instance_type.get_method(node.method)

            if len(node.args) == len(instance_method.param_types):
                for arg, param_type in zip(node.args, instance_method.param_types):
                    self.visit(arg, scope)
                    arg_type = arg.expr_type

                    if not arg_type.conforms_to(param_type):
                        error = SemanticError(incompatible_types_.replace(
                            '%s', arg_type.name, 1).replace('%s', param_type.name, 1), node.row, node.col, 'TypeError')
                        self.errors.append(error)
            else:
                error = SemanticError(incorrect_count_params_.replace("%s", instance_method.name, 1).replace("%s", instance_type.name, 1).replace("%s", str(len(instance_method.param_types)), 1), node.row, node.col)
                self.errors.append(error)

            if instance_method.return_type.name == 'SELF_TYPE':
                node_type = instance_type
            else:
                node_type = instance_method.return_type

        except SemanticException as ex:
            node_type = Error_Type()
            error = SemanticError(ex.text, node.row, node.col, 'AttributeError')
            self.errors.append(error)
            
        node.expr_type = node_type

    @visitor.when(StaticCallNode)
    def visit(self, node, scope):
        self.visit(node.obj, scope)
        instance_type = node.obj.expr_type

        try:
            static_type = self.context.get_type(node.static_type)
        except SemanticException as ex:
            static_type = Error_Type()
            error = SemanticError(ex.text, node.row, node.col, 'TypeError')
            self.errors.append(error)
         
        if not instance_type.conforms_to(static_type):
            error = SemanticError(incompatible_types_.replace(
                '%s', instance_type.name, 1).replace('%s', static_type.name, 1), node.row, node.col, 'TypeError')
            self.errors.append(error)

        try:
            method = static_type.get_method(node.method)

            if len(node.args) == len(method.param_types):
                for arg, param_type in zip(node.args, method.param_types):
                    self.visit(arg, scope)
                    arg_type = arg.expr_type

                    if not arg_type.conforms_to(param_type):
                        error = SemanticError(incompatible_types_.replace(
                            '%s', arg_type.name, 1).replace('%s', param_type.name, 1), node.row, node.col, 'TypeError')
                        self.errors.append(error)
            else:
                error = SemanticError( incorrect_count_params_.replace('%s', method.name, 1).replace('%s', static_type.name, 1).replace('%s', str(len(method.param_types)), 1), node.row, node.col)
                self.errors.append(error)

            if method.return_type.name == 'SELF_TYPE':
                node_type = instance_type
            node_type = method.return_type

        except SemanticException as ex:
            error = SemanticError(ex.text, node.row, node.col, 'AttributeError')
            self.errors.append(error)
            node_type = Error_Type()

        node.expr_type = node_type

    @visitor.when(AssignNode)
    def visit(self, node, scope):
        self.visit(node.expression, scope)
        node_type = node.expression.expr_type

        if scope.is_defined(node.name):
            var = scope.find_variable(node.name)

            if var.name == 'self':
                error = SemanticError(read_only_, node.row, node.col)
                self.errors.append(error)
                node_type = Error_Type()
            elif not node_type.conforms_to(var.type):
                error = SemanticError(incompatible_types_.replace(
                    '%s', node_type.name, 1).replace('%s', var.type.name, 1), node.row, node.col, 'TypeError')
                self.errors.append(error)
                node_type = Error_Type()
        else:
            error = SemanticError(var_not_defined_.replace(
                '%s', node.name, 1), node.row, node.col, 'NameError')
            self.errors.append(error)
            node_type = Error_Type()

        node.expr_type = node_type

    @visitor.when(CaseNode)
    def visit(self, node, scope):
        self.visit(node.expression, scope)
        action_expr_types = []
        var_declared = []

        for action in node.act_list:
            var_type = action.act_type
            if not var_type in var_declared:
                var_declared.append(var_type)
            else:
                error = SemanticError(other_branch_declared_.replace("%s", var_type, 1), action.row, action.col)
                self.errors.append(error)
            self.visit(action, scope.create_child())
            action_expr_types.append(action.expr_type)

        t_0 = action_expr_types.pop(0)
        node_type = t_0.multiple_join(action_expr_types)
       
        node.expr_type = node_type

    @visitor.when(ActionNode)
    def visit(self, node, scope):
        try:
            action_type = self.context.get_type(node.act_type)
        except SemanticException as ex:
            error = SemanticError(ex.text, node.row, node.col , 'TypeError')
            self.errors.append(error)
            action_type = Error_Type()

        scope.define_variable(node.name, action_type)

        self.visit(node.body, scope)
        node.expr_type = node.body.expr_type

    @visitor.when(IfNode)
    def visit(self, node, scope):
        self.visit(node.predicate, scope)
        predicate_type = node.predicate.expr_type

        if predicate_type.name != 'Bool':
            error = SemanticError(wrong_type_.replace('%s', 'Bool', 1), node.row, node.col, 'TypeError')
            self.errors.append(error)

        self.visit(node.then_expr, scope)
        then_type = node.then_expr.expr_type
        self.visit(node.else_expr, scope)
        else_type = node.else_expr.expr_type

        node.expr_type = then_type.join(else_type)
  

    @visitor.when(WhileNode)
    def visit(self, node, scope):
        self.visit(node.predicate, scope)
        predicate_type = node.predicate.expr_type

        if predicate_type.name != 'Bool':
            error = SemanticError(wrong_type_.replace('%s', 'Bool', 1), node.row, node.col, 'TypeError')
            self.errors.append(error)

        self.visit(node.expression, scope)

        node.expr_type = self.context.get_type('Object')

    @visitor.when(BlockNode)
    def visit(self, node, scope):
        for expr in node.expr_list:
            self.visit(expr, scope)

        node.expr_type = node.expr_list[-1].expr_type

    @visitor.when(LetNode)
    def visit(self, node, scope):
        let_scope = scope.create_child()
    
        for var in node.init_list:
            self.visit(var, let_scope)

        self.visit(node.body, let_scope)

        node.expr_type = node.body.expr_type

    @visitor.when(LetInitNode)
    def visit(self, node, scope):
        try:
            node_type = self.context.get_type(node.let_type)
            if node_type.name == 'SELF_TYPE':
                node_type = scope.find_variable('self').type
        except SemanticException as ex:
            error = SemanticError(ex.text, node.row, node.col, 'TypeError')
            self.errors.append(error)
            node_type = ErrorType()

        self.visit(node.expression, scope)
        expr_type = node.expression.expr_type

        if not expr_type.conforms_to(node_type):
            error = SemanticError(incompatible_types_.replace(
                '%s', expr_type.name, 1).replace('%s', node_type.name, 1), node.row, node.col, 'TypeError')
            self.errors.append(error)

        if node.name == 'self':
            error = SemanticError(self_let_, node.row, node.col)
            self.errors.append(error)  
        else:
            if scope.is_local(node.name):
                scope.remove_local(node.name)

            scope.define_variable(node.name, node_type)

    @visitor.when(LetDefNode)
    def visit(self, node, scope):
        try:
            node_type = self.context.get_type(node.let_type)
            if node_type.name == 'SELF_TYPE':
                node_type = scope.find_variable('self').type
        except SemanticException as ex:
            error = SemanticError(ex.text, node.row, node.col, 'TypeError')
            self.errors.append(error)
            node_type = Error_Type()

        if node.name == 'self':
            error = SemanticError(self_let_, node.row, node.col)
            self.errors.append(error)  
        else:
            if scope.is_local(node.name):
                scope.remove_local(node.name)

            scope.define_variable(node.name, node_type)

    @visitor.when(NewNode)
    def visit(self, node, scope):
        try:
            node_type = self.context.get_type(node.new_type)
            if node_type.name == 'SELF_TYPE':
                node_type = scope.find_variable('self').type
        except SemanticException as ex:
            error = SemanticError(ex.text, node.row, node.col, 'TypeError')
            self.errors.append(error)
            node_type = Error_Type()

        node.expr_type = node_type

    @visitor.when(IsVoidNode)
    def visit(self, node, scope):
        self.visit(node.expression, scope)
        node.expr_type = self.context.get_type('Bool')

    @visitor.when(ArithBinOpNode)
    def visit(self, node, scope):
        node_type = self.context.get_type('Int')

        self.visit(node.left, scope)
        left_type = node.left.expr_type

        if left_type.name != 'Int':
            error = SemanticError(wrong_type_.replace('%s', 'Int', 1), node.row, node.col, 'TypeError')
            self.errors.append(error)
            node_type = Error_Type()

        self.visit(node.right, scope)
        right_type = node.right.expr_type

        if right_type.name != 'Int':
            error = SemanticError(wrong_type_.replace('%s', 'Int', 1), node.row, node.col, 'TypeError')
            self.errors.append(error)
            node_type = Error_Type()

        node.expr_type = node_type

    @visitor.when(LogicBinOpNode)
    def visit(self, node, scope):
        node_type = self.context.get_type('Bool')

        self.visit(node.left, scope)
        left_type = node.left.expr_type

        if left_type.name != 'Int':
            error = SemanticError(wrong_type_.replace('%s', 'Int', 1), node.row, node.col, 'TypeError')
            self.errors.append(error)
            node_type = Error_Type()

        self.visit(node.right, scope)
        right_type = node.right.expr_type

        if right_type.name != 'Int':
            error = SemanticError(wrong_type_.replace('%s', 'Int', 1), node.row, node.col, 'TypeError')
            self.errors.append(error)
            node_type = Error_Type()

        node.expr_type = node_type

    @visitor.when(NotNode)
    def visit(self, node, scope):
        node_type = self.context.get_type('Bool')

        self.visit(node.expression, scope)
        expr_type = node.expression.expr_type

        if expr_type.name != 'Bool':      
            error = SemanticError(wrong_type_.replace('%s', 'Bool', 1), node.row, node.col, 'TypeError')      
            self.errors.append(error)
            node_type = Error_Type()

        node.expr_type = node_type

    @visitor.when(LogicNotNode)
    def visit(self, node, scope):
        node_type = self.context.get_type('Int')

        self.visit(node.expression, scope)
        expr_type = node.expression.expr_type

        if expr_type.name != 'Int':
            error = SemanticError(wrong_type_.replace('%s', 'Int', 1), node.row, node.col, 'TypeError')
            self.errors.append(error)
            node_type = Error_Type()

        node.expr_type = node_type

    @visitor.when(EqualsNode)
    def visit(self, node, scope):
        node_type = self.context.get_type('Bool')

        self.visit(node.left, scope)
        left_type = node.left.expr_type

        self.visit(node.right, scope)
        right_type = node.right.expr_type

        if (left_type.name in ['Int', 'Bool', 'String'] or right_type.name in ['Int', 'Bool', 'String']) and left_type.name != right_type.name:
            error = SemanticError(wrong_type_.replace('%s', left_type.name, 1), node.row, node.col, 'TypeError')
            self.errors.append(error)
            node_type = Error_Type()

        node.expr_type = node_type


    @visitor.when(IdNode)
    def visit(self, node, scope):
        if scope.is_defined(node.name):
            node_type = scope.find_variable(node.name).type
        else:
            error = SemanticError(var_not_defined_.replace(
                '%s', node.name, 1), node.row, node.col, 'NameError')
            self.errors.append(error)
            node_type = Error_Type()

        node.expr_type = node_type

    @visitor.when(IntegerNode)
    def visit(self, node, scope):
        node.expr_type = self.context.get_type('Int')

    @visitor.when(StringNode)
    def visit(self, node, scope):
        node.expr_type = self.context.get_type('String')

    @visitor.when(BooleanNode)
    def visit(self, node, scope):
        node.expr_type = self.context.get_type('Bool')
