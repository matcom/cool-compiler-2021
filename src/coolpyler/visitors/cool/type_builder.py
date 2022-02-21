import coolpyler.errors as errors
import coolpyler.utils.visitor as visitor
import coolpyler.ast.cool.type_collected as type_collected
import coolpyler.ast.cool.type_built as type_built
import coolpyler.semantic as semantic
from coolpyler.semantic import ErrorType


class TypeBuilderVisitor:
    def __init__(self, errors=None):
        if errors is None:
            errors = []
        self.errors = errors
        self.current_type = None
        self.types = dict()

    def get_type(self, name):
        try:
            return self.types[name]
        except KeyError:
            raise semantic.SemanticError(f"Type `{name}` is not defined.")

    @visitor.on("node")
    def visit(self, node):
        pass

    @visitor.when(type_collected.CoolProgramNode)
    def visit(self, node: type_collected.CoolProgramNode):  # noqa: F811
        self.types = node.types
        classes = [self.visit(c) for c in node.classes]
        return type_built.CoolProgramNode(
            node.lineno, node.columnno, classes, self.types
        )

    @visitor.when(type_collected.CoolClassNode)
    def visit(self, node: type_collected.CoolClassNode):    # noqa: F811
        self.current_type = node.type

        parent_type = self.types["Object"]
        if node.parent is not None:
            try:
                parent_type = self.get_type(node.parent)
            except semantic.SemanticError as e:
                self.errors.append(errors.TypeError(node.lineno, node.columnno, e.text))

        try:
            self.current_type.set_parent(parent_type)
        except semantic.SemanticError as e:
            self.errors.append(errors.SemanticError(node.lineno, node.columnno, e.text))

        features = [self.visit(feat) for feat in node.features]

        return type_built.CoolClassNode(node.lineno, node.columnno,
                                        node.type, features, node.parent)

    @visitor.when(type_collected.CoolAttrDeclNode)
    def visit(self, node: type_collected.CoolAttrDeclNode):  # noqa: F811
        try:
            type = self.get_type(node.type)
        except semantic.SemanticError as e:
            self.errors.append(errors.TypeError(node.lineno, node.columnno, e.text))
            type = ErrorType()

        try:
            attr_info = self.current_type.define_attribute(node.id, type)
        except semantic.SemanticError as e:
            self.errors.append(errors.SemanticError(node.lineno, node.columnno, e.text))
            attr_info = None  # TODO: check

        body = self.visit(node.body) if node.body is not None else None
        return type_built.CoolAttrDeclNode(
            node.lineno, node.columnno, attr_info, body=body
        )

    @visitor.when(type_collected.CoolMethodDeclNode)
    def visit(self, node: type_collected.CoolMethodDeclNode):   # noqa: F811
        param_types = []
        for ptype_name in node.param_types:
            try:
                ptype = self.get_type(ptype_name)
            except semantic.SemanticError as error:
                self.errors.append(
                    errors.TypeError(node.lineno, node.columnno, error.text)
                )
                ptype = ErrorType()
            param_types.append(ptype)

        try:
            return_type = self.get_type(node.type)
        except semantic.SemanticError as error:
            self.errors.append(errors.TypeError(node.lineno, node.columnno, error.text))
            return_type = ErrorType()

        try:
            method_info = self.current_type.define_method(
                node.id,
                node.param_names,
                param_types,
                return_type,
            )
        except semantic.SemanticError as error:
            self.errors.append(
                errors.SemanticError(node.lineno, node.columnno, error.text)
            )
            method_info = None  # TODO: check

        body = self.visit(node.body)

        return type_built.CoolMethodDeclNode(
            node.lineno, node.columnno, method_info, body
        )

    @visitor.when(type_collected.CoolAssignNode)  # noqa: F811
    def visit(self, node: type_collected.CoolAssignNode):    # noqa: F811
        expr = self.visit(node.expr)
        return type_built.CoolAssignNode(
            node.lineno, node.columnno, node.id, expr
        )

    @visitor.when(type_collected.CoolStaticDispatchNode)  # noqa: F811
    def visit(self, node: type_collected.CoolStaticDispatchNode):    # noqa: F811
        expr = self.visit(node.expr)
        args = [self.visit(arg) for arg in node.args]
        return type_built.CoolStaticDispatchNode(
            node.lineno, node.columnno, expr, node.static_type, node.id, args
        )

    @visitor.when(type_collected.CoolDispatchNode)  # noqa: F811
    def visit(self, node: type_collected.CoolDispatchNode):    # noqa: F811
        expr = self.visit(node.expr)
        args = [self.visit(arg) for arg in node.args]
        return type_built.CoolDispatchNode(
            node.lineno, node.columnno, node.id, args, expr
        )

    @visitor.when(type_collected.CoolIfThenElseNode)  # noqa: F811
    def visit(self, node: type_collected.CoolIfThenElseNode):    # noqa: F811
        cond = self.visit(node.cond)
        then_expr = self.visit(node.then_expr)
        else_expr = self.visit(node.else_expr)
        return type_built.CoolIfThenElseNode(
            node.lineno, node.columnno, cond, then_expr, else_expr
        )

    @visitor.when(type_collected.CoolWhileNode)  # noqa: F811
    def visit(self, node: type_collected.CoolWhileNode):    # noqa: F811
        cond = self.visit(node.cond)
        body = self.visit(node.body)
        return type_built.CoolWhileNode(
            node.lineno, node.columnno, cond, body
        )

    @visitor.when(type_collected.CoolBlockNode)  # noqa: F811
    def visit(self, node: type_collected.CoolBlockNode):    # noqa: F811
        expr_list = [self.visit(expr) for expr in node.expr_list]
        return type_built.CoolBlockNode(
            node.lineno, node.columnno, expr_list
        )

    @visitor.when(type_collected.CoolLetInNode)  # noqa: F811
    def visit(self, node: type_collected.CoolLetInNode):    # noqa: F811
        decl_list = [self.visit(decl) for decl in node.decl_list]
        expr = self.visit(node.expr)
        return type_built.CoolLetInNode(
            node.lineno, node.columnno, decl_list, expr
        )

    @visitor.when(type_collected.CoolLetDeclNode)  # noqa: F811
    def visit(self, node: type_collected.CoolLetDeclNode):    # noqa: F811
        expr = self.visit(node.expr)
        return type_built.CoolLetDeclNode(
            node.lineno, node.columnno, node.id, node.type, expr
        )

    @visitor.when(type_collected.CoolCaseNode)  # noqa: F811
    def visit(self, node: type_collected.CoolCaseNode):    # noqa: F811
        case_branches = [self.visit(branch) for branch in node.case_branches]
        expr = self.visit(node.expr)
        return type_built.CoolCaseNode(
            node.lineno, node.columnno, expr, case_branches
        )

    @visitor.when(type_collected.CoolCaseBranchNode)  # noqa: F811
    def visit(self, node: type_collected.CoolCaseBranchNode):    # noqa: F811
        expr = self.visit(node.expr)
        return type_built.CoolCaseBranchNode(
            node.lineno, node.columnno, node.id, node.type, expr
        )

    @visitor.when(type_collected.CoolNewNode)  # noqa: F811
    def visit(self, node: type_collected.CoolNewNode):    # noqa: F811
        return type_built.CoolNewNode(
            node.lineno, node.columnno, node.type
        )

    @visitor.when(type_collected.CoolParenthNode)  # noqa: F811
    def visit(self, node: type_collected.CoolParenthNode):    # noqa: F811
        expr = self.visit(node.expr)
        return type_built.CoolParenthNode(
            node.lineno, node.columnno, expr
        )

    @visitor.when(type_collected.CoolTildeNode)  # noqa: F811
    def visit(self, node: type_collected.CoolTildeNode):    # noqa: F811
        expr = self.visit(node.expr)
        return type_built.CoolTildeNode(
            node.lineno, node.columnno, expr
        )

    @visitor.when(type_collected.CoolNotNode)  # noqa: F811
    def visit(self, node: type_collected.CoolNotNode):    # noqa: F811
        expr = self.visit(node.expr)
        return type_built.CoolNotNode(
            node.lineno, node.columnno, expr
        )

    @visitor.when(type_collected.CoolIsVoidNode)  # noqa: F811
    def visit(self, node: type_collected.CoolIsVoidNode):    # noqa: F811
        expr = self.visit(node.expr)
        return type_built.CoolIsVoidNode(
            node.lineno, node.columnno, expr
        )

    @visitor.when(type_collected.CoolLeqNode)  # noqa: F811
    def visit(self, node: type_collected.CoolLeqNode):    # noqa: F811
        left_expr = self.visit(node.left_expr)
        right_expr = self.visit(node.right_expr)
        return type_built.CoolLeqNode(
            node.lineno, node.columnno, left_expr, right_expr
        )

    @visitor.when(type_collected.CoolEqNode)  # noqa: F811
    def visit(self, node: type_collected.CoolEqNode):    # noqa: F811
        left_expr = self.visit(node.left_expr)
        right_expr = self.visit(node.right_expr)
        return type_built.CoolEqNode(
            node.lineno, node.columnno, left_expr, right_expr
        )

    @visitor.when(type_collected.CoolLeNode)  # noqa: F811
    def visit(self, node: type_collected.CoolLeNode):    # noqa: F811
        left_expr = self.visit(node.left_expr)
        right_expr = self.visit(node.right_expr)
        return type_built.CoolLeNode(
            node.lineno, node.columnno, left_expr, right_expr
        )

    @visitor.when(type_collected.CoolPlusNode)  # noqa: F811
    def visit(self, node: type_collected.CoolPlusNode):    # noqa: F811
        left_expr = self.visit(node.left_expr)
        right_expr = self.visit(node.right_expr)
        return type_built.CoolPlusNode(
            node.lineno, node.columnno, left_expr, right_expr
        )

    @visitor.when(type_collected.CoolMinusNode)  # noqa: F811
    def visit(self, node: type_collected.CoolMinusNode):    # noqa: F811
        left_expr = self.visit(node.left_expr)
        right_expr = self.visit(node.right_expr)
        return type_built.CoolMinusNode(
            node.lineno, node.columnno, left_expr, right_expr
        )

    @visitor.when(type_collected.CoolMultNode)  # noqa: F811
    def visit(self, node: type_collected.CoolMultNode):    # noqa: F811
        left_expr = self.visit(node.left_expr)
        right_expr = self.visit(node.right_expr)
        return type_built.CoolMultNode(
            node.lineno, node.columnno, left_expr, right_expr
        )

    @visitor.when(type_collected.CoolDivNode)  # noqa: F811
    def visit(self, node: type_collected.CoolDivNode):    # noqa: F811
        left_expr = self.visit(node.left_expr)
        right_expr = self.visit(node.right_expr)
        return type_built.CoolDivNode(
            node.lineno, node.columnno, left_expr, right_expr
        )

    @visitor.when(type_collected.CoolIntNode)  # noqa: F811
    def visit(self, node: type_collected.CoolIntNode):    # noqa: F811
        return type_built.CoolIntNode(
            node.lineno, node.columnno, node.value
        )

    @visitor.when(type_collected.CoolBoolNode)  # noqa: F811
    def visit(self, node: type_collected.CoolBoolNode):    # noqa: F811
        return type_built.CoolBoolNode(
            node.lineno, node.columnno, node.value
        )

    @visitor.when(type_collected.CoolStringNode)  # noqa: F811
    def visit(self, node: type_collected.CoolStringNode):    # noqa: F811
        return type_built.CoolStringNode(
            node.lineno, node.columnno, node.value
        )

    @visitor.when(type_collected.CoolVarNode)  # noqa: F811
    def visit(self, node: type_collected.CoolVarNode):    # noqa: F811
        return type_built.CoolVarNode(
            node.lineno, node.columnno, node.value
        )
