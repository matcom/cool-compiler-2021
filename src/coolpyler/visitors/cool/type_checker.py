import coolpyler.ast.cool.type_built as type_built
import coolpyler.ast.cool.type_checked as type_checked
import coolpyler.errors as errors
import coolpyler.semantic as semantic
import coolpyler.utils.visitor as visitor
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
            raise semantic.TypeError(f"Type `{name}` is not defined.")

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

        return type_checked.CoolProgramNode(
            node.lineno, node.columnno, classes, self.types, scope
        )

    @visitor.when(type_built.CoolClassNode)
    def visit(self, node, scope):  # noqa: F811
        self.current_type = node.type
        scope.define_variable("self", self.current_type, first_self=True)
        for attr in self.current_type.attributes:
            try:
                scope.define_variable(attr.name, attr.type)
            except semantic.BaseSemanticError as e:

                self.errors.append(e.with_pos(node.lineno, node.columnno))

        features = [self.visit(feat, scope) for feat in node.features]

        self.current_type = None

        return type_checked.CoolClassNode(
            node.lineno,
            node.columnno,
            self.types[node.type.name],
            features,
            node.parent,
        )

    @visitor.when(type_built.CoolAttrDeclNode)
    def visit(self, node, scope):  # noqa: F811
        if node.body != [] and node.attr_info is not None:
            exp = self.visit(node.body, scope)
            node_type = node.attr_info.type

            if exp.type.name == "SELF_TYPE" and not self.exp_type.conforms_to(
                node_type
            ):
                self.errors.append(
                    errors.IncompatibleTypesError(
                        node.lineno, node.columnno, node_type.name, self.exp_type.name
                    )
                )

            elif exp.type.name != "SELF_TYPE" and not exp.type.conforms_to(node_type):
                self.errors.append(
                    errors.IncompatibleTypesError(
                        node.lineno, node.columnno, node_type.name, exp.type.name
                    )
                )

            return type_built.CoolAttrDeclNode(
                node.lineno, node.columnno, node.attr_info, exp
            )

    @visitor.when(type_built.CoolMethodDeclNode)
    def visit(self, node, scope):  # noqa: F811
        if node.method_info is not None:
            self.current_method = self.current_type.get_method(node.method_info.name)
            method_scope = scope.create_child()

            for pname, ptype in zip(
                self.current_method.param_names, self.current_method.param_types
            ):
                try:
                    method_scope.define_variable(pname, ptype)
                except semantic.BaseSemanticError as e:
                    self.errors.append(e.with_pos(node.lineno, node.columnno))

            body = self.visit(node.body, method_scope)

            if (
                self.current_method.return_type.name == "SELF_TYPE"
                and not body.type.conforms_to(self.current_type)
            ):
                self.errors.append(
                    errors.IncompatibleTypesError(
                        node.lineno,
                        node.columnno,
                        body.type.name,
                        self.current_type.name,
                    )
                )

            elif (
                self.current_method.return_type.name != "SELF_TYPE"
                and not body.type.conforms_to(self.current_method.return_type)
            ):
                self.errors.append(
                    errors.IncompatibleTypesError(
                        node.lineno,
                        node.columnno,
                        body.type.name,
                        self.current_method.return_type.name,
                    )
                )

            if self.current_type.parent is not None:
                try:
                    parent_method = self.current_type.parent.get_method(
                        self.current_method.name
                    )
                except semantic.BaseSemanticError as e:
                    parent_method = None

                if parent_method is not None and parent_method != self.current_method:
                    self.errors.append(
                        errors.WrongSignatureError(
                            node.lineno, node.columnno, self.current_method.name
                        )
                    )

            self.current_method = None
            return type_checked.CoolMethodDeclNode(
                node.lineno, node.columnno, node.method_info, body
            )

    @visitor.when(type_built.CoolDispatchNode)
    def visit(self, node, scope):  # noqa: F811

        exp = self.visit(node.expr, scope)

        args = [self.visit(arg, scope) for arg in node.args]

        if exp.type.name == "AUTO_TYPE":
            return type_checked.CoolDispatchNode(
                node.lineno, node.columnno, exp, node.id, args, exp.type
            )

        try:
            method = exp.type.get_method(node.id)
        except semantic.BaseSemanticError as e:
            self.errors.append(e.with_pos(node.lineno, node.columnno))
            return type_checked.CoolDispatchNode(
                node.lineno, node.columnno, exp, node.id, args, ErrorType()
            )

        if len(args) != len(method.param_names):
            self.errors.append(
                errors.WrongArgsCountError(
                    node.lineno,
                    node.columnno,
                    method.name,
                    len(method.param_names),
                    len(args),
                )
            )

        for arg, ptype in zip(args, method.param_types):
            args.append(arg)
            if not arg.type.conforms_to(ptype):
                self.errors.append(
                    errors.IncompatibleTypesError(
                        node.lineno, node.columnno, arg.type.name, ptype.name
                    )
                )

        if method.return_type.name == "SELF_TYPE":
            return type_checked.CoolDispatchNode(
                node.lineno, node.columnno, exp, node.id, args, exp.type
            )

        return type_checked.CoolDispatchNode(
            node.lineno, node.columnno, exp, node.id, args, method.return_type
        )

    @visitor.when(type_built.CoolStaticDispatchNode)
    def visit(self, node, scope):  # noqa: F811
        exp = self.visit(node.expr, scope)
        args = [self.visit(arg, scope) for arg in node.args]
        try:
            static_type = self.get_type(node.static_type)
            method = static_type.get_method(node.id)
            if not exp.type.conforms_to(static_type):
                raise semantic.TypeError(
                    f"Expression type {exp.type.name} does not conform to declared static dispatch type {static_type.name}."
                )
        except semantic.BaseSemanticError as e:
            self.errors.append(e.with_pos(node.lineno, node.columnno))
            return type_checked.CoolStaticDispatchNode(
                node.lineno,
                node.columnno,
                exp,
                ErrorType(),
                node.id,
                args,
                ErrorType(),
            )

        if len(args) != len(method.param_names):
            self.errors.append(
                errors.WrongArgsCountError(
                    node.lineno,
                    node.columnno,
                    method.name,
                    len(method.param_names),
                    len(args),
                )
            )

        for arg, ptype in zip(args, method.param_types):
            if not arg.type.conforms_to(ptype):
                self.errors.append(
                    errors.IncompatibleTypesError(
                        node.lineno, node.columnno, arg.type.name, ptype.name
                    )
                )

        # try:
        #     static_type = self.get_type(node.static_type)
        #     if not exp.type.conforms_to(static_type):
        #         self.errors.append(
        #             errors.NotConformsError(
        #                 node.lineno, node.columnno, exp.type, static_type
        #             )
        #         )
        # except semantic.BaseSemanticError as e:
        #     self.errors.append(e.with_pos(node.lineno, node.columnno))

        return type_checked.CoolStaticDispatchNode(
            node.lineno,
            node.columnno,
            exp,
            static_type,
            node.id,
            args,
            method.return_type,
        )

    @visitor.when(type_built.CoolLetInNode)
    def visit(self, node, scope):  # noqa: F811
        let_scope = scope.create_child()

        decl_list = [self.visit(decl, let_scope) for decl in node.decl_list]

        # for idx, _type, expx in node.decl_list:

        exp = self.visit(node.expr, let_scope)

        return type_checked.CoolLetInNode(
            node.lineno, node.columnno, decl_list, exp, exp.type
        )

    @visitor.when(type_built.CoolLetDeclNode)
    def visit(self, node, scope):  # noqa: F811
        try:
            typex = self.get_type(node.type)
        except semantic.BaseSemanticError as e:
            typex = ErrorType()
            self.errors.append(e.with_pos(node.lineno, node.columnno))

        if node.expr == []:
            right_type = typex
            right_exp = None
            # decl_list.append(idx, _type, None)
        else:
            right_exp = self.visit(node.expr, scope)
            right_type = right_exp.type
            # decl_list.append(idx, _type, right_exp)

        if typex.name == "SELF_TYPE" and not right_type.conforms_to(self.current_type):
            self.errors.append(
                errors.IncompatibleTypesError(
                    node.lineno, node.columnno, right_type.name, self.current_type.name,
                )
            )

        elif typex.name != "SELF_TYPE" and not right_type.conforms_to(typex):
            self.errors.append(
                errors.IncompatibleTypesError(
                    node.lineno, node.columnno, right_type.name, typex.name
                )
            )

        try:
            scope.define_variable(node.id, typex, force=True)
        except semantic.BaseSemanticError as e:
            self.errors.append(e.with_pos(node.lineno, node.columnno))

        return type_checked.CoolLetDeclNode(
            node.lineno, node.columnno, node.id, right_type, right_exp
        )

    @visitor.when(type_built.CoolCaseNode)
    def visit(self, node, scope):  # noqa: F811
        exp = self.visit(node.expr, scope)
        return_type = None
        first = True
        case_branches = [self.visit(branch, scope) for branch in node.case_branches]

        for branch in case_branches:
            static_type = branch.type

            if first:
                return_type = static_type
                first = False
            else:
                return_type = self.lowest_common_ancestor(return_type, static_type)

        return type_checked.CoolCaseNode(
            node.lineno, node.columnno, exp, case_branches, return_type
        )

    @visitor.when(type_built.CoolCaseBranchNode)
    def visit(self, node, scope):  # noqa: F811
        try:
            typex = self.get_type(node.type)
        except semantic.BaseSemanticError as e:
            typex = ErrorType()
            self.errors.append(e.with_pos(node.lineno, node.columnno))

        new_scope = scope.create_child()
        try:
            new_scope.define_variable(node.id, typex)
        except semantic.BaseSemanticError as e:
            self.errors.append(e.with_pos(node.lineno, node.columnno))

        _case_exp = self.visit(node.expr, new_scope)
        return type_checked.CoolCaseBranchNode(
            node.lineno, node.columnno, node.id, typex, _case_exp
        )

    @visitor.when(type_built.CoolBlockNode)
    def visit(self, node, scope):  # noqa: F811
        exp = None
        expr_list = []
        for exp in node.expr_list:
            exp = self.visit(exp, scope)
            expr_list.append(exp)
        return type_checked.CoolBlockNode(
            node.lineno,
            node.columnno,
            expr_list,
            exp.type if exp is not None else ErrorType(),
        )

    @visitor.when(type_built.CoolAssignNode)
    def visit(self, node, scope):  # noqa: F811
        if node.id == "self":
            self.errors.append(
                errors.IsReadOnlyError(node.lineno, node.columnno, "self")
            )

        try:
            var = scope.find_variable(node.id)
            var_type = var.type
        except semantic.BaseSemanticError as e:
            self.errors.append(e.with_pos(node.lineno, node.columnno))
            var_type = ErrorType()

        exp = self.visit(node.expr, scope)
        if not exp.type.conforms_to(var_type):
            self.errors.append(
                errors.IncompatibleTypesError(
                    node.lineno, node.columnno, exp.type.name, var_type.name
                )
            )

        return type_checked.CoolAssignNode(
            node.lineno, node.columnno, node.id, exp, exp.type
        )

    @visitor.when(type_built.CoolNotNode)
    def visit(self, node, scope):  # noqa: F811
        exp = self.visit(node.expr, scope)
        bool_type = self.get_type("Bool")
        if exp.type != bool_type:
            self.errors.append(
                errors.IncompatibleTypesError(
                    node.lineno, node.columnno, exp.type.name, bool_type.name
                )
            )

        return type_checked.CoolNotNode(node.lineno, node.columnno, exp, bool_type)

    @visitor.when(type_built.CoolTildeNode)
    def visit(self, node, scope):  # noqa: F811
        exp = self.visit(node.expr, scope)
        int_type = self.get_type("Int")
        if not exp.type.conforms_to(int_type):
            self.errors.append(
                errors.IncompatibleTypesError(
                    node.lineno, node.columnno, exp.type.name, int_type.name
                )
            )
        return type_checked.CoolTildeNode(node.lineno, node.columnno, exp, int_type)

    @visitor.when(type_built.CoolIsVoidNode)
    def visit(self, node, scope):  # noqa: F811
        exp = self.visit(node.expr, scope)
        return type_checked.CoolIsVoidNode(
            node.lineno, node.columnno, exp, self.get_type("Bool")
        )

    @visitor.when(type_built.CoolParenthNode)
    def visit(self, node, scope):  # noqa: F811
        exp = self.visit(node.expr, scope)
        return type_checked.CoolParenthNode(node.lineno, node.columnno, exp, exp.type)

    @visitor.when(type_built.CoolPlusNode)
    def visit(self, node, scope):  # noqa: F811
        int_type = self.get_type("Int")
        left = self.visit(node.left_expr, scope)
        right = self.visit(node.right_expr, scope)
        if not left.type.conforms_to(int_type) or not right.type.conforms_to(int_type):
            self.errors.append(
                errors.InvalidOperationError(
                    node.lineno, node.columnno, left.type.name, right.type.name
                )
            )
        return type_checked.CoolPlusNode(
            node.lineno, node.columnno, left, right, int_type
        )

    @visitor.when(type_built.CoolMinusNode)
    def visit(self, node, scope):  # noqa: F811
        int_type = self.get_type("Int")
        left = self.visit(node.left_expr, scope)
        right = self.visit(node.right_expr, scope)
        if not left.type.conforms_to(int_type) or not right.type.conforms_to(int_type):
            self.errors.append(
                errors.InvalidOperationError(
                    node.lineno, node.columnno, left.type.name, right.type.name
                )
            )
        return type_checked.CoolMinusNode(
            node.lineno, node.columnno, left, right, int_type
        )

    @visitor.when(type_built.CoolDivNode)
    def visit(self, node, scope):  # noqa: F811
        int_type = self.get_type("Int")
        left = self.visit(node.left_expr, scope)
        right = self.visit(node.right_expr, scope)
        if not left.type.conforms_to(int_type) or not right.type.conforms_to(int_type):
            self.errors.append(
                errors.InvalidOperationError(
                    node.lineno, node.columnno, left.type.name, right.type.name
                )
            )
        return type_checked.CoolDivNode(
            node.lineno, node.columnno, left, right, int_type
        )

    @visitor.when(type_built.CoolMultNode)
    def visit(self, node, scope):  # noqa: F811
        int_type = self.get_type("Int")
        left = self.visit(node.left_expr, scope)
        right = self.visit(node.right_expr, scope)
        if not left.type.conforms_to(int_type) or not right.type.conforms_to(int_type):
            self.errors.append(
                errors.InvalidOperationError(
                    node.lineno, node.columnno, left.type.name, right.type.name
                )
            )
        return type_checked.CoolMultNode(
            node.lineno, node.columnno, left, right, int_type
        )

    @visitor.when(type_built.CoolLeqNode)
    def visit(self, node, scope):  # noqa: F811
        left = self.visit(node.left_expr, scope)
        right = self.visit(node.right_expr, scope)
        if not left.type.conforms_to(right.type) and not right.type.conforms_to(
            left.type
        ):
            self.errors.append(
                errors.InvalidComparissonError(
                    node.lineno, node.columnno, left.type.name, right.type.name
                )
            )
        return type_checked.CoolLeqNode(
            node.lineno, node.columnno, left, right, self.get_type("Bool")
        )

    @visitor.when(type_built.CoolEqNode)
    def visit(self, node, scope):  # noqa: F811
        left = self.visit(node.left_expr, scope)
        right = self.visit(node.right_expr, scope)
        if not left.type.conforms_to(right.type) and not right.type.conforms_to(
            left.type
        ):
            self.errors.append(
                errors.InvalidComparissonError(
                    node.lineno, node.columnno, left.type.name, right.type.name
                )
            )
        return type_checked.CoolEqNode(
            node.lineno, node.columnno, left, right, self.get_type("Bool")
        )

    @visitor.when(type_built.CoolLeNode)
    def visit(self, node, scope):  # noqa: F811
        left = self.visit(node.left_expr, scope)
        right = self.visit(node.right_expr, scope)
        if not left.type.conforms_to(right.type) and not right.type.conforms_to(
            left.type
        ):
            self.errors.append(
                errors.InvalidComparissonError(
                    node.lineno, node.columnno, left.type.name, right.type.name
                )
            )
        return type_checked.CoolLeNode(
            node.lineno, node.columnno, left, right, self.get_type("Bool")
        )

    @visitor.when(type_built.CoolWhileNode)
    def visit(self, node, scope):  # noqa: F811
        conditional = self.visit(node.cond, scope)
        body = self.visit(node.body, scope)

        if conditional.type != self.get_type("Bool"):
            self.errors.append(
                errors.IncompatibleTypesError(
                    node.lineno, node.columnno, conditional.type.name, "Bool"
                )
            )

        return type_checked.CoolWhileNode(
            node.lineno, node.columnno, conditional, body, self.get_type("Object")
        )

    @visitor.when(type_built.CoolIfThenElseNode)
    def visit(self, node, scope):  # noqa: F811
        conditional = self.visit(node.cond, scope)
        then_expr = self.visit(node.then_expr, scope)
        else_expr = self.visit(node.else_expr, scope)
        bool_type = self.get_type("Bool")

        if not conditional.type.conforms_to(bool_type):
            self.errors.append(
                errors.IncompatibleTypesError(
                    node.lineno, node.columnno, conditional.type.name, "Bool"
                )
            )

        lca = self.lowest_common_ancestor(then_expr.type, else_expr.type)
        return type_checked.CoolIfThenElseNode(
            node.lineno, node.columnno, conditional, then_expr, else_expr, lca
        )

    @visitor.when(type_built.CoolStringNode)
    def visit(self, node, scope):  # noqa: F811
        return type_checked.CoolStringNode(
            node.lineno, node.columnno, node.value, self.get_type("String")
        )

    @visitor.when(type_built.CoolBoolNode)
    def visit(self, node, scope):  # noqa: F811
        return type_checked.CoolBoolNode(
            node.lineno, node.columnno, node.value, self.get_type("Bool")
        )

    @visitor.when(type_built.CoolIntNode)
    def visit(self, node, scope):  # noqa: F811
        return type_checked.CoolIntNode(
            node.lineno, node.columnno, node.value, self.get_type("Int")
        )

    @visitor.when(type_built.CoolVarNode)
    def visit(self, node, scope):  # noqa: F811
        try:
            var = scope.find_variable(node.value)
        except semantic.BaseSemanticError as e:
            self.errors.append(e.with_pos(node.lineno, node.columnno))
            return type_checked.CoolVarNode(
                node.lineno, node.columnno, node.value, ErrorType()
            )

        return type_checked.CoolVarNode(
            node.lineno, node.columnno, node.value, var.type
        )

    @visitor.when(type_built.CoolNewNode)
    def visit(self, node, scope):  # noqa: F811
        if node.type_name == "SELF_TYPE":
            type_checked.CoolNewNode(node.lineno, node.columnno, self.current_type)

        try:
            type = self.get_type(node.type_name)
        except semantic.BaseSemanticError as e:
            self.errors.append(e.with_pos(node.lineno, node.columnno))
            return type_checked.CoolNewNode(node.lineno, node.columnno, ErrorType())

        return type_checked.CoolNewNode(node.lineno, node.columnno, type)

