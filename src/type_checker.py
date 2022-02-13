import utils.visitor as visitor
from utils.semantic import Scope, BasicTypes
from utils.semantic import SemanticError
from ast_hierarchy import *


WRONG_SIGNATURE = '(Line %s) Method "%s" already defined in "%s" with a different signature.'
SELF_IS_READONLY = '(Line %s) Variable "self" is read-only.'
LOCAL_ALREADY_DEFINED = '(Line %s) Variable "%s" is already defined in method "%s".'
ATTR_ALREADY_DEFINED = '(Line %s) Attribute "%s" is already defined in ancestor class.'
INCOMPATIBLE_TYPES = '(Line %s) Cannot convert "%s" into "%s".'
VARIABLE_NOT_DEFINED = '(Line %s) Variable "%s" is not defined in "%s".'
INVALID_OPERATION = '(Line %s) Operation is not defined between "%s" and "%s".'
METHOD_ARGS_UNMATCHED = '(Line %s) Method "%s" arguments do not match with definition.'


class TypeChecker:
    def __init__(self, context, errors):
        self.context = context
        self.current_type = None
        self.current_method = None
        self.errors = errors
        self.scope_id = 0
        self.type_scope = {}

    @visitor.on("node")
    def visit(self, node, scope):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node, scope=None, set_type=None):
        scope = Scope(self.scope_id)
        self.scope_id += 1
        for declaration in node.declarations:
            child_scope = scope.create_child(self.scope_id)
            self.scope_id += 1
            self.visit(declaration, child_scope)
        return scope

    @visitor.when(ClassDeclarationNode)
    def visit(self, node, scope, set_type=None):
        # print('class declaration')
        self_type = self.context.get_type(BasicTypes.SELF.value)
        scope.define_variable("self", self_type)
        self.current_type = self.context.get_type(node.id)
        self.type_scope[self.current_type.name] = scope
        if self.current_type.parent.name not in {
            BasicTypes.OBJECT.value,
            BasicTypes.INT.value,
            BasicTypes.BOOL.value,
            BasicTypes.STRING.value,
            BasicTypes.IO.value,
        }:
            try:
                parent_scope = self.type_scope[self.current_type.parent.name]
                scope.parent.children.remove(scope)
                scope.parent = parent_scope
                parent_scope.children.append(scope)
            except KeyError:
                self.errors.append(
                    f'(Line {node.lineno}) Class "{self.current_type.name}" parent not declared before inheritance.'
                )
        for feature in node.features:
            self.visit(feature, scope)

    @visitor.when(AttrDeclarationNode)
    def visit(self, node: AttrDeclarationNode, scope: Scope, set_type=None):
        # print('attr declaration')
        if node.id == "self":
            self.errors.append(
                f'(Line {node.lineno}) "self" is used as attribute name in class "{self.current_type.name}".'
            )
            if node.val is not None:
                self.visit(node.val, scope)
            return
        var, _ = scope.my_find_var(node.id)
        attr_type = self.context.get_type(node.type)
        if var is not None:
            self.errors.append(ATTR_ALREADY_DEFINED % (node.lineno, node.id))
        else:
            scope.define_variable(node.id, attr_type)

        if node.val is not None:
            return_type = self.visit(node.val, scope)
        else:
            return_type = attr_type

        if attr_type.name == BasicTypes.SELF.value:
            attr_type = self.current_type
        if return_type.name == BasicTypes.SELF.value:
            return_type = self.current_type
        if not return_type.conforms_to(attr_type):
            self.errors.append(INCOMPATIBLE_TYPES % (node.lineno, return_type.name, attr_type.name))

    @visitor.when(FuncDeclarationNode)
    def visit(self, node, scope, set_type=None):
        # print('function declaration')
        method, _ = self.current_type.get_method(node.id)
        self.current_method = method

        try:
            ancestor_method, ancestor_type = self.current_type.parent.get_method(node.id)

            old_return_type = ancestor_method.return_type
            current_return_type = method.return_type
            if old_return_type.name != current_return_type.name:
                self.errors.append(WRONG_SIGNATURE % (node.lineno, node.id, ancestor_type.name))
            elif len(ancestor_method.param_types) != len(method.param_types):
                self.errors.append(WRONG_SIGNATURE % (node.lineno, node.id, ancestor_type.name))
            else:
                for i in range(len(method.param_types)):
                    old_param_type = ancestor_method.param_types[i]
                    current_param_type = method.param_types[i]
                    if old_param_type.name != current_param_type.name:
                        self.errors.append(
                            WRONG_SIGNATURE % (node.lineno, node.id, ancestor_type.name)
                        )
                        break
        except SemanticError:
            ancestor_method = None

        child_scope = scope.create_child(self.scope_id)
        self.scope_id += 1
        for i in range(0, len(method.param_names)):
            if method.param_names[i] == "self":
                self.errors.append(
                    f'(Line {node.lineno}) "self" is used as argument name in method: "{method.name}", type: "{self.current_type.name}". '
                )
                continue
            param_type = method.param_types[i]
            child_scope.define_variable(method.param_names[i], param_type)

        return_type = method.return_type
        expr_type = self.visit(node.body, child_scope)

        if expr_type.name == BasicTypes.SELF.value:
            expr_type = self.current_type
        if return_type.name == BasicTypes.SELF.value:
            to_conform = self.current_type
        else:
            to_conform = return_type
        if not expr_type.conforms_to(to_conform):
            self.errors.append(INCOMPATIBLE_TYPES % (node.lineno, expr_type.name, to_conform.name))

    @visitor.when(ConditionalNode)
    def visit(self, node, scope, set_type=None):
        # print('conditional')
        cond_type = self.visit(node.if_expr, scope)
        bool_type = self.context.get_type(BasicTypes.BOOL.value)
        if not cond_type.conforms_to(bool_type):
            self.errors.append(INCOMPATIBLE_TYPES % (node.lineno, cond_type.name, BasicTypes.BOOL.value))

        then_expr_type = self.visit(node.then_expr, scope)
        else_expr_type = self.visit(node.else_expr, scope)

        common_ancestor_type = self.context.find_first_common_ancestor(
            then_expr_type, else_expr_type
        )
        return common_ancestor_type

    @visitor.when(LoopNode)
    def visit(self, node, scope, set_type=None):
        # print('loop')
        cond_type = self.visit(node.condition, scope)
        bool_type = self.context.get_type(BasicTypes.BOOL.value)
        if not cond_type.conforms_to(bool_type):
            self.errors.append(INCOMPATIBLE_TYPES % (cond_type.name, BasicTypes.BOOL.value))

        self.visit(node.body, scope)
        obj_type = self.context.get_type(BasicTypes.OBJECT.value)
        return obj_type

    @visitor.when(BlockNode)
    def visit(self, node: BlockNode, scope, set_type=None):
        # print('block')
        child_scope = scope.create_child(self.scope_id)
        self.scope_id += 1
        error_type = self.context.get_type(BasicTypes.ERROR.value)
        return_type = error_type
        for expr in node.expr_list:
            return_type = self.visit(expr, child_scope)
        return return_type

    @visitor.when(LetNode)
    def visit(self, node, scope, set_type=None):
        # print('let')
        child_scope = scope
        for var, typex, expr in node.var_list:
            child_scope = child_scope.create_child(self.scope_id)
            self.scope_id += 1
            if var == "self":
                self.errors.append(f'(Line {node.lineno}) "self" is used as let variable.')
                self.visit(expr, child_scope)
                continue
            try:
                var_type = self.context.get_type(typex)
            except SemanticError as error:
                self.errors.append(error.text)
                error_type = self.context.get_type(BasicTypes.ERROR.value)
                var_type = error_type

            if expr is not None:
                expr_type = self.visit(expr, child_scope)
            else:
                expr_type = var_type

            if var_type.name == BasicTypes.SELF.value:
                var_type = self.current_type
            if expr_type.name == BasicTypes.SELF.value:
                expr_type = self.current_type
            if not expr_type.conforms_to(var_type):
                self.errors.append(INCOMPATIBLE_TYPES % (node.lineno, expr_type.name, var_type.name))
            child_scope.define_variable(var, var_type)
        return self.visit(node.body, child_scope)

    @visitor.when(CaseNode)
    def visit(self, node, scope, set_type=None):
        # print('case')
        self.visit(node.expr, scope)
        error_type = self.context.get_type(BasicTypes.ERROR.value)
        types_used = set()
        return_type = None
        for var, typex, expr in node.branch_list:
            try:
                var_type = self.context.get_type(typex)
            except SemanticError as error:
                self.errors.append(error.text)
                var_type = error_type

            if var_type.name != BasicTypes.ERROR.value:
                if var_type.name in types_used:
                    self.errors.append(
                        f'(Line {node.lineno}) In method "{self.current_method.name}", type "{self.current_type.name}", more than one '
                        f'branch variable has type "{var_type.name}". '
                    )
                types_used.add(var_type.name)

            self.scope_id += 1
            child_scope = scope.create_child(self.scope_id)
            if var == "self":
                self.errors.append(
                    f'(Line {node.lineno}) In method "{self.current_method.name}", type "{self.current_type.name}", a branch has "self" as '
                    f"variable name. "
                )
            else:
                child_scope.define_variable(var, var_type)

            expr_type = self.visit(expr, child_scope)

            if return_type is None:
                return_type = expr_type
            return_type = self.context.find_first_common_ancestor(
                expr_type, return_type
            )

        return return_type

    @visitor.when(AssignNode)
    def visit(self, node, scope: Scope, set_type=None):
        # print('assign')
        error_type = self.context.get_type(BasicTypes.ERROR.value)
        if node.id == "self":
            self.errors.append(f'(Line {node.lineno}) "self" variable is read-only')
            expr_type = self.visit(node.expr, scope)
            return expr_type
        var, scope_id = scope.my_find_var(node.id)
        if var is None:
            self.errors.append(
                VARIABLE_NOT_DEFINED % (node.lineno, node.id, self.current_method.name)
            )
            var_type = error_type
        else:
            var_type = var.type
        expr_type = self.visit(node.expr, scope)
        if not expr_type.conforms_to(var_type):
            self.errors.append(INCOMPATIBLE_TYPES % (node.lineno, expr_type.name, var_type.name))
        return expr_type

    @visitor.when(CallNode)
    def visit(self, node, scope, set_type=None):
        # print('call')
        error_type = self.context.get_type(BasicTypes.ERROR.value)
        obj_type = self.visit(node.obj, scope)
        if not obj_type:
            obj_type = self.context.get_type(BasicTypes.SELF.value)
        t0 = obj_type
        if t0.name == BasicTypes.SELF.value:
            t0 = self.current_type

        if node.ancestor_type is not None:
            ancestor_type = self.context.get_type(node.ancestor_type)
            if not t0.conforms_to(ancestor_type):
                self.errors.append(
                    f'(Line {node.lineno}) Type "{t0.name}" does not conform to "{ancestor_type.name}".'
                )
            t0 = ancestor_type

        try:
            method, _ = t0.get_method(node.id)
        except SemanticError as error:
            self.errors.append(error.text)
            return error_type

        if not len(method.param_names) == len(node.args):
            self.errors.append(METHOD_ARGS_UNMATCHED % (node.lineno, method.name))
        else:
            for i in range(0, len(node.args)):
                arg_type = self.visit(node.args[i], scope)
                method_param_type = method.param_types[i]
                if not arg_type.conforms_to(method_param_type):
                    self.errors.append(
                        INCOMPATIBLE_TYPES % (node.lineno, arg_type.name, method.param_types[i].name)
                    )
        return_type = method.return_type

        if return_type.name == BasicTypes.SELF.value:
            if self.current_type.conforms_to(obj_type):
                return self.current_type
            else:
                return obj_type
        return return_type

    @visitor.when(ArithBinaryNode)
    def visit(self, node, scope, set_type=None):
        # print('arith binary')
        int_type = self.context.get_type(BasicTypes.INT.value)
        left_type = self.visit(node.left, scope)
        right_type = self.visit(node.right, scope)
        if not left_type.conforms_to(int_type) or not right_type.conforms_to(int_type):
            self.errors.append(INVALID_OPERATION % (node.lineno, left_type.name, right_type.name))
        return int_type

    @visitor.when(BooleanBinaryNode)
    def visit(self, node, scope, set_type=None):
        # print('boolean binary')
        int_type = self.context.get_type(BasicTypes.INT.value)
        bool_type = self.context.get_type(BasicTypes.BOOL.value)
        if isinstance(node, EqualNode):
            left_type = self.visit(node.left, scope)
            right_type = self.visit(node.right, scope)
            if (
                left_type.name in {"Int", "String", "Bool"}
                or right_type.name in {"Int", "String", "Bool"}
            ) and left_type != right_type:
                self.errors.append(INVALID_OPERATION % (node.lineno, left_type.name, right_type.name))
            return bool_type

        left_type = self.visit(node.left, scope)
        right_type = self.visit(node.right, scope)
        if not left_type.conforms_to(int_type) or not right_type.conforms_to(int_type):
            self.errors.append(INVALID_OPERATION % (node.lineno, left_type.name, right_type.name))
        return bool_type

    @visitor.when(ConstantNumNode)
    def visit(self, node, scope, set_type=None):
        # print('constant')
        return self.context.get_type(BasicTypes.INT.value)

    @visitor.when(StringNode)
    def visit(self, node, scope, set_type=None):
        # print('constant')
        return self.context.get_type(BasicTypes.STRING.value)

    @visitor.when(BoolNode)
    def visit(self, node, scope, set_type=None):
        # print('bool')
        return self.context.get_type(BasicTypes.BOOL.value)

    @visitor.when(VariableNode)
    def visit(self, node, scope: Scope, set_type=None):
        # print('variable')
        var, scope_id = scope.my_find_var(node.lex)
        if var is None:
            self.errors.append(
                VARIABLE_NOT_DEFINED % (node.lineno, node.lex, self.current_method.name)
            )
            error_type = self.context.get_type(BasicTypes.ERROR.value)
            return error_type
        else:
            return var.type

    @visitor.when(InstantiateNode)
    def visit(self, node, scope, set_type=None):
        # print('instantiate')
        try:
            instance_type = self.context.get_type(node.lex)
        except SemanticError as error:
            self.errors.append(error.text)
            error_type = self.context.get_type(BasicTypes.ERROR.value)
            instance_type = error_type

        if instance_type.name == BasicTypes.SELF.value:
            instance_type = self.current_type
        return instance_type

    @visitor.when(NotNode)
    def visit(self, node, scope, set_type=None):
        # print('not node')
        bool_type = self.context.get_type(BasicTypes.BOOL.value)
        expr_type = self.visit(node.expr, scope)
        if not expr_type.conforms_to(bool_type):
            self.errors.append(INCOMPATIBLE_TYPES % (node.lineno, expr_type.name, BasicTypes.BOOL.value))
        return bool_type

    @visitor.when(IsVoidNode)
    def visit(self, node, scope, set_type=None):
        # print('is void')
        bool_type = self.context.get_type(BasicTypes.BOOL.value)
        self.visit(node.expr, scope)
        return bool_type

    @visitor.when(IntCompNode)
    def visit(self, node, scope, set_type=None):
        # print('tilde')
        int_type = self.context.get_type(BasicTypes.INT.value)
        expr_type = self.visit(node.expr, scope, set_type)
        if not expr_type.conforms_to(int_type):
            self.errors.append(INCOMPATIBLE_TYPES % (node.lineno, expr_type.name, int_type.name))
        return int_type
