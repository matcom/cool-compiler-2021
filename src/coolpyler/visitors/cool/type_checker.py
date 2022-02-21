import coolpyler.errors as errors
import coolpyler.utils.visitor as visitor
import coolpyler.ast.cool.type_checked as type_checked
import coolpyler.ast.cool.type_built as type_built
import coolpyler.semantic as semantic
from coolpyler.semantic import ErrorType


class TypeCheckerVisitor:
    def __init__(self, err=None):
        if err is None:
            err = []
        self.errors = err
        self.current_type = None
        self.types = dict()
        self.current_method = None
        self.scope = semantic.Scope()

    def get_type(self, name):
        try:
            return self.types[name]
        except KeyError:
            raise semantic.SemanticError(f"Type `{name}` is not defined.")

    def lowest_common_ancestor(self, type_1, type_2):
        object_type = self.get_type("Object")
        if type_1 == object_type or type_2 == object_type:
            return object_type

        typex = type_1
        while typex is not None and typex != object_type:
            if type_2.conforms_to(typex):
                return typex
            typex = typex.parent

        typex = type_2
        while typex is not None and typex != object_type:
            if type_1.conforms_to(typex):
                return typex
            typex = typex.parent

        return object_type

    @visitor.on("node")
    def visit(self, node, scope):
        pass

    @visitor.when(type_built.CoolProgramNode)
    def visit(self, node, scope=None):  # noqa: F811
        scope = semantic.Scope()
        self.types = node.types
        classes = [self.visit(c, scope.create_child()) for c in node.classes]

        return type_checked.CoolProgramNode(node.lineno, node.columnno,
                                            classes, self.types, scope)

    @visitor.when(type_built.CoolClassNode)
    def visit(self, node, scope):  # noqa: F811
        self.current_type = self.types[node.id]
        scope.define_variable("self", self.current_type)
        for attr in self.current_type.attributes:
            scope.define_variable(attr.name, attr.type)

        features = [self.visit(feat, scope) for feat in node.features]

        self.current_type = None

        return type_checked.CoolClassNode(node.lineno, node.columnno,
                                          self.types[node.id], features, node.parent)

    @visitor.when(type_built.CoolAttrDeclNode)
    def visit(self, node, scope):  # noqa: F811
        if node.body is not None:
            exp = self.visit(node.body, scope)
            node_type = node.attr_info.type

            if exp.type.name == "SELF_TYPE" and not node_type.conforms_to(
                self.exp_type
            ):
                self.errors.append(
                    errors.IncompatibleTypesError(node.lineno, node.columno,
                                                  node_type.name, self.exp_type.name)
                )

            elif exp.type.name != "SELF_TYPE" and not node_type.conforms_to(exp.type):
                self.errors.append(
                    errors.IncompatibleTypesError(node.lineno, node.columno,
                                                  node_type.name, exp.type.name)
                    )

            return type_built.CoolAttrDeclNode(node.lineno, node.columnno,
                                               node.attr_info, exp)

    @visitor.when(type_built.CoolMethodDeclNode)
    def visit(self, node, scope):  # noqa: F811
        self.current_method = self.current_type.get_method(node.method_info.id)
        method_scope = scope.create_child()

        for pname, ptype in zip(
            self.current_method.param_names, self.current_method.param_types
        ):
            method_scope.define_variable(pname, ptype)

        body = self.visit(node.body, method_scope)

        if (
            self.current_method.return_type.name == "SELF_TYPE"
            and not body.type.conforms_to(self.current_type)
        ):
            self.errors.append(
                errors.IncompatibleTypesError(node.lineno, node.columno,
                                              body.type.name,
                                              self.current_type.name)
            )

        elif (
            self.current_method.return_type.name != "SELF_TYPE"
            and not body.type.conforms_to(self.current_method.return_type)
        ):
            self.errors.append(
                errors.IncompatibleTypesError(node.lineno, node.columno,
                                              body.type.name,
                                              self.current_method.return_type.name)
            )

        if self.current_type.parent is not None:
            try:
                parent_method = self.current_type.parent.get_method(
                    self.current_method.name
                )
                if parent_method != self.current_method:
                    self.errors.append(errors.WrongSignatureError(
                                node.lineno,
                                node.columno,
                                parent_method.name
                            )
                        )
            except errors.SemanticError(node.lineno, node.columno, "error"):
                pass

        self.current_method = None
        return type_checked.CoolMethodDeclNode(node.lineno, node.columnno,
                                               node.method_info, body)

    @visitor.when(type_built.CoolDispatchNode)
    def visit(self, node, scope):  # noqa: F811
        exp = self.visit(node.expr, scope)
        args = [self.visit(arg, scope) for arg in node.args]

        if exp.type.name == "AUTO_TYPE":
            return type_checked.CoolDispatchNode(node.lineno, node.columnno,
                                                 node.id, args,
                                                 exp.type, exp)

        try:
            method = exp.type.get_method(node.id)
        except errors.SemanticError as e:
            self.errors.append(e)
            return type_checked.CoolDispatchNode(node.lineno, node.columnno,
                                                 node.id, args,
                                                 ErrorType(), exp)

        if len(args) != len(method.param_names):
            self.errors.append(
                errors.WrongArgsCountError(node.lineno, node.columnno,
                                           method.name, len(method.param_names),
                                           len(args))
            )

        for arg, ptype in zip(args, method.param_types):
            args.append(arg)
            if not arg.type.conforms_to(ptype):
                self.errors.append(
                    errors.IncompatibleTypesError(node.lineno, node.columnno,
                                                  arg.type.name, ptype.name))

        if method.return_type == "SELF_TYPE":
            return type_checked.CoolDispatchNode(node.lineno, node.columnno,
                                                 node.id, args,
                                                 exp.type, exp)

        return type_checked.CoolDispatchNode(node.lineno, node.columnno,
                                             node.id, args,
                                             method.type, exp)

    @visitor.when(type_built.CoolStaticDispatchNode)
    def visit(self, node, scope):  # noqa: F811
        exp = self.visit(node.expr, scope)
        args = [self.visit(arg, scope) for arg in node.args]
        try:
            method = exp.type.get_method(node.id)
        except errors.SemanticError as e:
            self.errors.append(e)
            return type_checked.CoolStaticDispatchNode(node.lineno, node.columnno,
                                                       exp,
                                                       node.static_type,
                                                       node.id,
                                                       args,
                                                       ErrorType())

        if len(args) != len(method.param_names):
            self.errors.append(
                errors.WrongArgsCountError(node.lineno, node.columnno,
                                           method.name, len(method.param_names),
                                           len(args))
            )

        for arg, ptype in zip(args, method.param_types):
            if not arg.type.conforms_to(ptype):
                self.errors.append(
                    errors.IncompatibleTypesError(node.lineno, node.columnno,
                                                  arg.type.name, ptype.name))

        try:
            specific_type = self.get_type(node.specific_type)
            if not exp.type.conforms_to(specific_type):
                self.errors.append(errors.NotConformsError(node.lineno, node.columnno,
                                                           exp.type, specific_type))
        except errors.SemanticError as e:
            self.errors.append(e)

        return type_checked.CoolStaticDispatchNode(node.lineno, node.columnno,
                                                   exp,
                                                   node.static_type,
                                                   node.id,
                                                   args,
                                                   method.type)

    @visitor.when(type_built.CoolLetInNode)
    def visit(self, node, scope):  # noqa: F811
        let_scope = scope.create_child()

        decl_list = []

        for idx, _type, expx in node.decl_list:
            try:
                typex = self.get_type(_type)
            except errors.SemanticError as e:
                typex = ErrorType()
                self.errors.append(e)

            if expx is None:
                right_type = typex
                decl_list.append(idx, _type, None)
            else:
                right_exp = self.visit(expx, scope)
                right_type = right_exp.type
                decl_list.append(idx, _type, right_exp)

            if typex.name == "SELF_TYPE" and not right_type.conforms_to(
                self.current_type
            ):
                self.errors.append(
                    errors.IncompatibleTypesError(node.lineno, node.columnno,
                                                  right_type.name,
                                                  self.current_type.name))

            elif typex.name != "SELF_TYPE" and not right_type.conforms_to(typex):
                self.errors.append(
                    errors.IncompatibleTypesError(node.lineno, node.columnno,
                                                  right_type.name,
                                                  typex.name))

            let_scope.define_variable(idx, typex)

        exp = self.visit(node.expr, let_scope)

        return type_checked.CoolLetInNode(
            node.lineno, node.columnno,
            decl_list,
            exp,
            exp.type
        )

    @visitor.when(type_built.CoolCaseNode)
    def visit(self, node, scope):  # noqa: F811
        exp = self.visit(node.expr, scope)
        return_type = None
        first = True
        case_branches = []

        for idx, _type, case_exp in node.case_branches:
            try:
                typex = self.context.get_type(_type)
            except errors.SemanticError as e:
                typex = ErrorType()
                self.errors.append(e)

            new_scope = scope.create_child()
            new_scope.define_variable(idx, typex)
            _case_exp = self.visit(case_exp, new_scope)
            case_branches.append(idx, _type, _case_exp)

            static_type = _case_exp.type

            if first:
                return_type = static_type
                first = False
            else:
                return_type = self.lowest_common_ancestor(
                    return_type, static_type
                )

        return type_checked.CoolCaseNode(node.lineno, node.columnno,
                                         exp, case_branches, return_type)

    @visitor.when(type_built.CoolBlockNode)
    def visit(self, node, scope):  # noqa: F811
        expr_list = []
        for exp in node.expr_list:
            exp = self.visit(exp, scope)
            expr_list.append(exp)
        return type_checked.CoolBlockNode(expr_list, exp.type)

    @visitor.when(type_built.CoolAssignNode)
    def visit(self, node, scope):  # noqa: F811
        if node.id == "self":
            self.errors.append(errors.IsReadOnlyError(node.lineno, node.columnno,
                                                      "self"))

        var = scope.find_variable(node.id)
        if var is None:
            self.errors.append(
                errors.VariableNotDefinedError(node.lineno, node.columnno,
                                               node.id)
            )
            var_type = ErrorType()
        else:
            var_type = var.type

        exp = self.visit(node.expr, scope)
        if not exp.type.conforms_to(var_type):
            self.errors.append(errors.IncompatibleTypeError(node.lineno, node.columnno,
                                                            exp.type.name,
                                                            var_type.name))

        return type_checked.CoolAssignNode(node.lineno, node.columnno,
                                           node.id,
                                           exp,
                                           var_type)

    @visitor.when(type_built.CoolNotNode)
    def visit(self, node, scope):  # noqa: F811
        exp = self.visit(node.exp, scope)
        bool_type = self.context.get_type("Bool")
        if exp.type != bool_type:
            self.errors.append(errors.IncompatibleTypesError(node.lineno, node.columnno,
                                                             exp.type.name,
                                                             bool_type.name))

        return type_checked.CoolNotNode(node.lineno, node.columnno, exp, bool_type)

    @visitor.when(type_built.CoolTildeType)
    def visit(self, node, scope):  # noqa: F811
        exp = self.visit(node.exp, scope)
        int_type = self.context.get_type("Int")
        if not exp.type.conforms_to(int_type):
            self.errors.append(errors.IncompatibleTypesError(node.lineno, node.columnno,
                                                             exp.type.name,
                                                             int_type.name))
        return type_checked.CoolTildeNode(node.lineno, node.columnno, exp, int_type)

    @visitor.when(type_built.CoolIsVoidNode)
    def visit(self, node, scope):  # noqa: F811
        exp = self.visit(node.exp, scope)
        return type_checked.CoolIsVoidNode(node.lineno, node.columnno,
                                           exp,
                                           self.context.get_type("Bool"))

    @visitor.when(type_built.CoolParenthExpNode)
    def visit(self, node, scope):  # noqa: F811
        exp = self.visit(node.exp, scope)
        return type_checked.CoolParenthExpNode(node.lineno, node.columnno,
                                               exp,
                                               exp.type)

    @visitor.when(type_built.CoolPlusNode)
    def visit(self, node, scope):  # noqa: F811
        int_type = self.get_type("Int")
        left = self.visit(node.left, scope)
        right = self.visit(node.right, scope)
        if not left.type.conforms_to(int_type) or not right.type.conforms_to(int_type):
            self.errors.append(errors.InvalidOperationError(node.lineno,
                                                            node.columnno,
                                                            left.type.name,
                                                            right.type.name))
        return type_checked.CoolPlusNode(node.lineno, node.columnno,
                                         left,
                                         right,
                                         int_type)

    @visitor.when(type_built.CoolMinusNode)
    def visit(self, node, scope):  # noqa: F811
        int_type = self.get_type("Int")
        left = self.visit(node.left, scope)
        right = self.visit(node.right, scope)
        if not left.type.conforms_to(int_type) or not right.type.conforms_to(int_type):
            self.errors.append(errors.InvalidOperationError(node.lineno,
                                                            node.columnno,
                                                            left.type.name,
                                                            right.type.name))
        return type_checked.CoolMinusNode(node.lineno, node.columnno,
                                          left,
                                          right,
                                          int_type)

    @visitor.when(type_built.CoolDivNode)
    def visit(self, node, scope):  # noqa: F811
        int_type = self.get_type("Int")
        left = self.visit(node.left, scope)
        right = self.visit(node.right, scope)
        if not left.type.conforms_to(int_type) or not right.type.conforms_to(int_type):
            self.errors.append(errors.InvalidOperationError(node.lineno,
                                                            node.columnno,
                                                            left.type.name,
                                                            right.type.name))
        return type_checked.CoolDivNode(node.lineno, node.columnno,
                                        left,
                                        right,
                                        int_type)

    @visitor.when(type_built.CoolMultNode)
    def visit(self, node, scope):  # noqa: F811
        int_type = self.get_type("Int")
        left = self.visit(node.left, scope)
        right = self.visit(node.right, scope)
        if not left.type.conforms_to(int_type) or not right.type.conforms_to(int_type):
            self.errors.append(errors.InvalidOperationError(node.lineno,
                                                            node.columnno,
                                                            left.type.name,
                                                            right.type.name))
        return type_checked.CoolMultNode(node.lineno, node.columnno,
                                         left,
                                         right,
                                         int_type)

    @visitor.when(type_built.CoolLeqNode)
    def visit(self, node, scope):  # noqa: F811
        left = self.visit(node.left, scope)
        right = self.visit(node.right, scope)
        if not left.type.conforms_to(right.type) and not right.type.conforms_to(
            left.type
        ):
            self.errors.append(errors.InvalidComparissonError(node.lineno,
                                                              node.columnno,
                                                              left.type.name,
                                                              right.type.name))
        return type_checked.CoolLeqNode(node.lineno, node.columnno,
                                        left,
                                        right,
                                        self.context.get_type("Bool"))

    @visitor.when(type_built.CoolEqNode)
    def visit(self, node, scope):  # noqa: F811
        left = self.visit(node.left, scope)
        right = self.visit(node.right, scope)
        if not left.type.conforms_to(right.type) and not right.type.conforms_to(
            left.type
        ):
            self.errors.append(errors.InvalidComparissonError(node.lineno,
                                                              node.columnno,
                                                              left.type.name,
                                                              right.type.name))
        return type_checked.CoolEqNode(node.lineno, node.columnno,
                                       left,
                                       right,
                                       self.context.get_type("Bool"))

    @visitor.when(type_built.CoolLeNode)
    def visit(self, node, scope):  # noqa: F811
        left = self.visit(node.left, scope)
        right = self.visit(node.right, scope)
        if not left.type.conforms_to(right.type) and not right.type.conforms_to(
            left.type
        ):
            self.errors.append(errors.InvalidComparissonError(node.lineno,
                                                              node.columnno,
                                                              left.type.name,
                                                              right.type.name))
        return type_checked.CoolLeNode(node.lineno, node.columnno,
                                       left,
                                       right,
                                       self.context.get_type("Bool"))

    @visitor.when(type_built.CoolWhileNode)
    def visit(self, node, scope):  # noqa: F811
        conditional = self.visit(node.cond, scope)
        body = self.visit(node.body, scope)

        if conditional.type != self.context.get_type("Bool"):
            self.errors.append(errors.IncompatibleTypeError(node.lineno, node.columnno,
                                                            conditional.type.name,
                                                            "Bool"))

        return type_checked.CoolWhileNode(node.lineno, node.columnno,
                                          conditional,
                                          body,
                                          self.get_type("Object"))

    @visitor.when(type_built.CoolIfThenElseNode)
    def visit(self, node, scope):  # noqa: F811
        conditional = self.visit(node.cond, scope)
        then_expr = self.visit(node.then_expr, scope)
        else_expr = self.visit(node.else_expr, scope)
        bool_type = self.context.get_type("Bool")

        if not conditional.type.conforms_to(bool_type):
            self.errors.append(errors.IncompatibleTypeError(node.lineno, node.columnno,
                                                            conditional.type.name,
                                                            "Bool"))

        lca = self.lowest_common_ancestor(then_expr.type, else_expr.type, self.context)
        return type_checked.CoolIfThenElseNode(node.lineno, node.columnno,
                                               conditional,
                                               then_expr,
                                               else_expr,
                                               lca)

    @visitor.when(type_built.CoolStringExpNode)
    def visit(self, node, scope):  # noqa: F811
        return type_checked.CoolStringExpNode(node.lineno, node.columnno,
                                              self.context.get_type("String"))

    @visitor.when(type_built.CoolBoolExpNode)
    def visit(self, node, scope):  # noqa: F811
        return type_checked.CoolBoolExpNode(node.lineno, node.columnno,
                                            self.context.get_type("Bool"))

    @visitor.when(type_built.CoolIntExpNode)
    def visit(self, node, scope):  # noqa: F811
        return type_checked.CoolIntExpNode(node.lineno, node.columnno,
                                           self.context.get_type("Int"))

    @visitor.when(type_built.CoolVarNode)
    def visit(self, node, scope):  # noqa: F811
        var = scope.find_variable(node.value)
        if var is None:
            self.errors.append(
                errors.VariableNotDefined(node.lineno, node.columnno, node.value)
            )
            return type_checked.CoolVarNode(node.lineno, node.columnno,
                                            node.value,
                                            ErrorType())

        return type_checked.CoolVarNode(node.lineno, node.columnno,
                                        node.value,
                                        var.type)

    @visitor.when(type_built.CoolNewTypeNode)
    def visit(self, node, scope):  # noqa: F811
        if node.type == "SELF_TYPE":
            type_checked.CoolNewTypeNode(node.lineno, node.columnno,
                                         node.type,
                                         self.current_type)

        return type_checked.CoolNewTypeNode(node.lineno, node.columnno,
                                            node.type,
                                            node.type)
