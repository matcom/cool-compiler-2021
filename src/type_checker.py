import utils.visitor as visitor
from utils.semantic import Scope, StrType, BasicTypes
from utils.semantic import SemanticError
from utils.semantic import SelfType, AutoType
from utils.semantic import ErrorType, IntType, BoolType, ObjType
from ast_hierarchy import *


WRONG_SIGNATURE = 'Method "%s" already defined in "%s" with a different signature.'
SELF_IS_READONLY = 'Variable "self" is read-only.'
LOCAL_ALREADY_DEFINED = 'Variable "%s" is already defined in method "%s".'
ATTR_ALREADY_DEFINED = 'Attribute "%s" is already defined in ancestor class.'
INCOMPATIBLE_TYPES = 'Cannot convert "%s" into "%s".'
VARIABLE_NOT_DEFINED = 'Variable "%s" is not defined in "%s".'
INVALID_OPERATION = 'Operation is not defined between "%s" and "%s".'
METHOD_ARGS_UNMATCHED = 'Method "%s" arguments do not match with definition.'


class TypeChecker:
    def __init__(self, context, errors, inferred_types):
        self.context = context
        self.current_type = None
        self.current_method = None
        self.errors = errors
        self.scope_id = 0
        self.auto_types = []
        self.inferred_types = inferred_types
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
        return scope, self.inferred_types, self.auto_types

    @visitor.when(ClassDeclarationNode)
    def visit(self, node, scope, set_type=None):
        # print('class declaration')
        scope.define_variable("self", SelfType())
        self.current_type = self.context.get_type(node.id)
        self.type_scope[self.current_type.name] = scope
        if self.current_type.parent.name not in {
            ObjType().name,
            IntType().name,
            BoolType().name,
            StrType().name,
            "IO",
        }:
            try:
                parent_scope = self.type_scope[self.current_type.parent.name]
                scope.parent.children.remove(scope)
                scope.parent = parent_scope
                parent_scope.children.append(scope)
            except KeyError:
                self.errors.append(
                    f'Class "{self.current_type.name}" parent not declared before inheritance.'
                )
        for feature in node.features:
            self.visit(feature, scope)

    @visitor.when(AttrDeclarationNode)
    def visit(self, node: AttrDeclarationNode, scope: Scope, set_type=None):
        # print('attr declaration')
        if node.id == "self":
            self.errors.append(
                f'"self" is used as attribute name in class "{self.current_type.name}".'
            )
            if node.val is not None:
                self.visit(node.val, scope)
            return
        var, _ = scope.my_find_var(node.id)
        attr_type = self.context.get_type(node.type)
        if var is not None:
            self.errors.append(ATTR_ALREADY_DEFINED % node.id)
        else:
            scope.define_variable(node.id, attr_type)

        if isinstance(attr_type, AutoType):
            try:
                var_type = self.inferred_types[(node.id, scope.id)]
                var, _ = scope.my_find_var(node.id)
                var.type = var_type
                attr_type = var_type
            except KeyError:
                self.auto_types.append((node.id, scope.id))

        if node.val is not None:
            return_type = self.visit(node.val, scope)
            if (
                isinstance(attr_type, AutoType)
                and not isinstance(return_type, AutoType)
                and (node.id, scope.id) in self.auto_types
            ):
                try:
                    self.auto_types.remove((node.id, scope.id))
                except ValueError:
                    pass
                self.inferred_types[(node.id, scope.id)] = return_type
                attr_type = return_type
        else:
            return_type = attr_type

        if isinstance(attr_type, SelfType):
            attr_type = self.current_type
        if isinstance(return_type, SelfType):
            return_type = self.current_type
        if not return_type.conforms_to(attr_type):
            self.errors.append(INCOMPATIBLE_TYPES % (return_type.name, attr_type.name))

    @visitor.when(FuncDeclarationNode)
    def visit(self, node, scope, set_type=None):
        # print('function declaration')
        method, _ = self.current_type.get_method(node.id)
        self.current_method = method

        if self.current_type.parent is not None:
            try:
                ancestor_method, ancestor_type = self.current_type.parent.get_method(
                    node.id
                )

                try:
                    old_return_type = self.inferred_types[
                        (ancestor_method.name, ancestor_type.name)
                    ]
                except KeyError:
                    old_return_type = ancestor_method.return_type
                try:
                    current_return_type = self.inferred_types[
                        (method.name, self.current_type.name)
                    ]
                except KeyError:
                    current_return_type = method.return_type
                if isinstance(old_return_type, AutoType) and not isinstance(
                    current_return_type, AutoType
                ):
                    try:
                        self.auto_types.remove(
                            (ancestor_method.name, ancestor_type.name)
                        )
                    except ValueError:
                        pass
                    self.inferred_types[
                        (ancestor_method.name, ancestor_type.name)
                    ] = current_return_type
                if isinstance(current_return_type, AutoType) and not isinstance(
                    old_return_type, AutoType
                ):
                    try:
                        self.auto_types.remove((method.name, self.current_type.name))
                    except ValueError:
                        pass
                    self.inferred_types[
                        (method.name, self.current_type.name)
                    ] = old_return_type

                if old_return_type.name != current_return_type.name:
                    self.errors.append(WRONG_SIGNATURE % (node.id, ancestor_type.name))
                elif len(ancestor_method.param_types) != len(method.param_types):
                    self.errors.append(WRONG_SIGNATURE % (node.id, ancestor_type.name))
                else:
                    for i in range(len(method.param_types)):
                        try:
                            old_param_type = self.inferred_types[
                                (ancestor_method.name, ancestor_type.name, i)
                            ]
                        except KeyError:
                            old_param_type = ancestor_method.param_types[i]
                        try:
                            current_param_type = self.inferred_types[
                                (method.name, self.current_type.name, i)
                            ]
                        except KeyError:
                            current_param_type = method.param_types[i]
                        if isinstance(old_param_type, AutoType) and not isinstance(
                            current_param_type, AutoType
                        ):
                            try:
                                self.auto_types.remove(
                                    (ancestor_method.name, ancestor_type.name, i)
                                )
                            except ValueError:
                                pass
                            self.inferred_types[
                                (ancestor_method.name, ancestor_type.name, i)
                            ] = current_param_type
                        if isinstance(current_param_type, AutoType) and not isinstance(
                            old_param_type, AutoType
                        ):
                            try:
                                self.auto_types.remove(
                                    (method.name, self.current_type.name, i)
                                )
                            except ValueError:
                                pass
                            self.inferred_types[
                                (method.name, self.current_type.name, i)
                            ] = old_param_type

                        if old_param_type.name != current_param_type.name:
                            self.errors.append(
                                WRONG_SIGNATURE % (node.id, ancestor_type.name)
                            )
                            break

            except SemanticError:
                ancestor_method = None

        child_scope = scope.create_child(self.scope_id)
        self.scope_id += 1
        for i in range(0, len(method.param_names)):
            if method.param_names[i] == "self":
                self.errors.append(
                    f'"self" is used as argument name in method: "{method.name}", type: "{self.current_type.name}".'
                )
                continue
            try:
                param_type = self.inferred_types[
                    (method.name, self.current_type.name, i)
                ]
            except KeyError:
                if isinstance(method.param_types[i], AutoType):
                    self.auto_types.append((method.param_names[i], child_scope.id))
                    self.auto_types.append((method.name, self.current_type.name, i))
                param_type = method.param_types[i]
            child_scope.define_variable(method.param_names[i], param_type)

        try:
            return_type = self.inferred_types[(method.name, self.current_type.name)]
        except KeyError:
            if isinstance(method.return_type, AutoType):
                self.auto_types.append((method.name, self.current_type.name))
            return_type = method.return_type

        if isinstance(return_type, AutoType):
            expr_type = self.visit(node.body, child_scope)
        else:
            expr_type = self.visit(node.body, child_scope, return_type)

        for i in range(len(method.param_names)):
            try:
                type = self.inferred_types[(method.param_names[i], child_scope.id)]
                try:
                    self.auto_types.remove((method.name, self.current_type.name, i))
                except ValueError:
                    pass
                self.inferred_types[(method.name, self.current_type.name, i)] = type
            except KeyError:
                continue
        try:
            return_type = self.inferred_types[(method.name, self.current_type.name)]
        except KeyError:
            pass

        if isinstance(expr_type, SelfType):
            expr_type = self.current_type
        if isinstance(return_type, SelfType):
            to_conform = self.current_type
        else:
            if isinstance(return_type, AutoType) and not isinstance(
                expr_type, AutoType
            ):
                try:
                    self.auto_types.remove((method.name, self.current_type.name))
                except ValueError:
                    pass
                self.inferred_types[(method.name, self.current_type.name)] = expr_type
                return_type = expr_type
            to_conform = return_type
        if not expr_type.conforms_to(to_conform):
            self.errors.append(INCOMPATIBLE_TYPES % (expr_type.name, to_conform.name))

    @visitor.when(ConditionalNode)
    def visit(self, node, scope, set_type=None):
        # print('conditional')
        cond_type = self.visit(node.if_expr, scope)
        if not cond_type.conforms_to(BoolType()):
            self.errors.append(INCOMPATIBLE_TYPES % (cond_type.name, BoolType().name))

        then_expr_type = self.visit(node.then_expr, scope, set_type)
        else_expr_type = self.visit(node.else_expr, scope, set_type)

        common_ancestor_type = self.context.find_first_common_ancestor(
            then_expr_type, else_expr_type
        )

        return common_ancestor_type

    @visitor.when(LoopNode)
    def visit(self, node, scope, set_type=None):
        # print('loop')
        cond_type = self.visit(node.condition, scope)
        if not cond_type.conforms_to(BoolType()):
            self.errors.append(INCOMPATIBLE_TYPES % (cond_type.name, BoolType().name))

        self.visit(node.body, scope)

        return ObjType()

    @visitor.when(BlockNode)
    def visit(self, node: BlockNode, scope, set_type=None):
        # print('block')
        child_scope = scope.create_child(self.scope_id)
        self.scope_id += 1
        return_type = ErrorType()
        for expr in node.expr_list:
            if expr == node.expr_list[-1]:
                return_type = self.visit(expr, child_scope, set_type)
            else:
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
                self.errors.append('"self" is used as let variable.')
                self.visit(expr, child_scope)
                continue
            try:
                var_type = self.context.get_type(typex)
            except SemanticError as error:
                self.errors.append(error.text)
                var_type = ErrorType()
            try:
                var_type = self.inferred_types[(var, child_scope.id)]
            except KeyError:
                pass
            if isinstance(var_type, AutoType):
                self.auto_types.append((var, child_scope.id))

            if expr is not None:
                expr_type = self.visit(expr, child_scope)
            else:
                expr_type = var_type

            if isinstance(var_type, SelfType):
                var_type = self.current_type
            if isinstance(expr_type, SelfType):
                expr_type = self.current_type
            if isinstance(var_type, AutoType) and not isinstance(expr_type, AutoType):
                try:
                    self.auto_types.remove((var, child_scope.id))
                except ValueError:
                    pass
                self.inferred_types[(var, child_scope.id)] = expr_type
            if not expr_type.conforms_to(var_type):
                self.errors.append(INCOMPATIBLE_TYPES % (expr_type.name, var_type.name))

            child_scope.define_variable(var, var_type)

        return self.visit(node.body, child_scope, set_type)

    @visitor.when(CaseNode)
    def visit(self, node, scope, set_type=None):
        # print('case')
        self.visit(node.expr, scope)

        types_used = set()
        return_type = None
        for var, typex, expr in node.branch_list:
            try:
                var_type = self.context.get_type(typex)
            except SemanticError as error:
                self.errors.append(error.text)
                var_type = ErrorType()

            if not isinstance(var_type, ErrorType):
                if var_type.name in types_used:
                    self.errors.append(
                        f'In method "{self.current_method.name}", type "{self.current_type.name}", more than one '
                        f'branch variable has type "{var_type.name}". '
                    )
                types_used.add(var_type.name)

            self.scope_id += 1
            child_scope = scope.create_child(self.scope_id)
            if var == "self":
                self.errors.append(
                    f'In method "{self.current_method.name}", type "{self.current_type.name}", a branch has "self" as '
                    f"variable name. "
                )
            else:
                child_scope.define_variable(var, var_type)

            expr_type = self.visit(expr, child_scope, set_type)

            if return_type is None:
                return_type = expr_type
            return_type = self.context.find_first_common_ancestor(
                expr_type, return_type
            )

        return return_type

    @visitor.when(AssignNode)
    def visit(self, node, scope: Scope, set_type=None):
        # print('assign')
        if node.id == "self":
            self.errors.append(f'"self" variable is read-only')
            expr_type = self.visit(node.expr, scope, set_type)
            return expr_type
        var, scope_id = scope.my_find_var(node.id)
        if var is None:
            self.errors.append(
                VARIABLE_NOT_DEFINED % (node.id, self.current_method.name)
            )
            var_type = ErrorType()
        else:
            try:
                var_type = self.inferred_types[(var.name, scope_id)]
            except:
                var_type = var.type

        if not isinstance(var_type, AutoType):
            expr_type = self.visit(node.expr, scope, var_type)
        else:
            expr_type = self.visit(node.expr, scope, set_type)

        if isinstance(var_type, AutoType) and not isinstance(expr_type, AutoType):
            try:
                self.auto_types.remove((var.name, scope_id))
            except ValueError:
                pass
            self.inferred_types[(var.name, scope_id)] = expr_type
            var_type = expr_type

        if not expr_type.conforms_to(var_type):
            self.errors.append(INCOMPATIBLE_TYPES % (expr_type.name, var_type.name))

        return expr_type

    @visitor.when(CallNode)
    def visit(self, node, scope, set_type=None):
        # print('call')
        obj_type = self.visit(node.obj, scope)
        if not obj_type:
            obj_type = self.context.get_type(BasicTypes.SELF.value)
        t0 = obj_type
        if isinstance(t0, SelfType):
            t0 = self.current_type
        if isinstance(t0, AutoType):
            return AutoType()

        if node.ancestor_type is not None:
            ancestor_type = self.context.get_type(node.ancestor_type)
            if not t0.conforms_to(ancestor_type):
                self.errors.append(
                    f'Type "{t0.name}" does not conform to "{ancestor_type.name}".'
                )
            t0 = ancestor_type

        try:
            method, _ = t0.get_method(node.id)
        except SemanticError as error:
            self.errors.append(error.text)
            return ErrorType()

        if not len(method.param_names) == len(node.args):
            self.errors.append(METHOD_ARGS_UNMATCHED % method.name)
        else:
            for i in range(0, len(node.args)):
                arg_type = self.visit(node.args[i], scope)
                try:
                    method_param_type = self.inferred_types[(node.id, t0.name, i)]
                except KeyError:
                    method_param_type = method.param_types[i]
                if isinstance(method_param_type, AutoType) and not isinstance(
                    arg_type, AutoType
                ):
                    try:
                        self.auto_types.remove((node.id, t0.name, i))
                    except ValueError:
                        pass
                    self.inferred_types[(node.id, t0.name, i)] = arg_type
                if not arg_type.conforms_to(method_param_type):
                    self.errors.append(
                        INCOMPATIBLE_TYPES % (arg_type.name, method.param_types[i].name)
                    )

        try:
            return_type = self.inferred_types[(node.id, t0.name)]
        except KeyError:
            return_type = method.return_type

        if isinstance(return_type, SelfType):
            return obj_type
        if isinstance(return_type, AutoType) and set_type is not None:
            try:
                self.auto_types.remove((node.id, t0.name))
            except ValueError:
                pass
            self.inferred_types[(node.id, t0.name)] = set_type
            return_type = set_type
        return return_type

    @visitor.when(ArithBinaryNode)
    def visit(self, node, scope, set_type=None):
        # print('arith binary')
        int_type = self.context.get_type(IntType().name)
        left_type = self.visit(node.left, scope, int_type)
        right_type = self.visit(node.right, scope, int_type)
        if not left_type.conforms_to(int_type) or not right_type.conforms_to(int_type):
            self.errors.append(INVALID_OPERATION % (left_type.name, right_type.name))
        return int_type

    @visitor.when(BooleanBinaryNode)
    def visit(self, node, scope, set_type=None):
        # print('boolean binary')

        if isinstance(node, EqualNode):
            left_type = self.visit(node.left, scope)
            right_type = self.visit(node.right, scope)
            if (
                left_type.name in {"Int", "String", "Bool"}
                or right_type.name in {"Int", "String", "Bool"}
            ) and left_type != right_type:
                if not isinstance(left_type, AutoType) and not isinstance(
                    right_type, AutoType
                ):
                    self.errors.append(
                        INVALID_OPERATION % (left_type.name, right_type.name)
                    )
            return BoolType()

        int_type = self.context.get_type(IntType().name)
        left_type = self.visit(node.left, scope, int_type)
        right_type = self.visit(node.right, scope, int_type)
        if not left_type.conforms_to(int_type) or not right_type.conforms_to(int_type):
            self.errors.append(INVALID_OPERATION % (left_type.name, right_type.name))
        return BoolType()

    @visitor.when(ConstantNumNode)
    def visit(self, node, scope, set_type=None):
        # print('constant')
        return self.context.get_type(IntType().name)

    @visitor.when(StringNode)
    def visit(self, node, scope, set_type=None):
        # print('constant')
        return self.context.get_type(StrType().name)

    @visitor.when(BoolNode)
    def visit(self, node, scope, set_type=None):
        # print('bool')
        return self.context.get_type(BoolType().name)

    @visitor.when(VariableNode)
    def visit(self, node, scope: Scope, set_type=None):
        # print('variable')
        var, scope_id = scope.my_find_var(node.lex)
        if var is None:
            self.errors.append(
                VARIABLE_NOT_DEFINED % (node.lex, self.current_method.name)
            )
            return ErrorType()
        else:
            try:
                var_type = self.inferred_types[(node.lex, scope_id)]
            except KeyError:
                var_type = var.type
                if (set_type is not None) and isinstance(var_type, AutoType):
                    try:
                        self.auto_types.remove((var.name, scope_id))
                    except ValueError:
                        pass
                    self.inferred_types[(var.name, scope_id)] = set_type
                    var_type = set_type
            return var_type

    @visitor.when(InstantiateNode)
    def visit(self, node, scope, set_type=None):
        # print('instantiate')
        try:
            instance_type = self.context.get_type(node.lex)
        except SemanticError as error:
            self.errors.append(error.text)
            instance_type = ErrorType()

        if isinstance(instance_type, SelfType):
            instance_type = self.current_type
        return instance_type

    @visitor.when(NotNode)
    def visit(self, node, scope, set_type=None):
        # print('not node')
        set_type = self.context.get_type(BoolType().name)
        expr_type = self.visit(node.expr, scope, set_type)
        if not expr_type.conforms_to(BoolType()):
            self.errors.append(INCOMPATIBLE_TYPES % (expr_type.name, BoolType().name))
        return BoolType()

    @visitor.when(IsVoidNode)
    def visit(self, node, scope, set_type=None):
        # print('is void')
        self.visit(node.expr, scope)
        return BoolType()

    @visitor.when(IntCompNode)
    def visit(self, node, scope, set_type=None):
        # print('tilde')
        int_type = self.context.get_type(IntType().name)
        set_type = int_type
        expr_type = self.visit(node.expr, scope, set_type)
        if not expr_type.conforms_to(int_type):
            self.errors.append(INCOMPATIBLE_TYPES % (expr_type.name, int_type.name))
        return int_type
