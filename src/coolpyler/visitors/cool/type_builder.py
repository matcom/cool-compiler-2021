import coolpyler.ast.cool.type_built as type_built
import coolpyler.ast.cool.type_collected as type_collected
import coolpyler.semantic as semantic
import coolpyler.utils.visitor as visitor
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
            raise semantic.TypeError(f"Type `{name}` is not defined.")

    @visitor.on("node")
    def visit(self, node): # type: ignore
        pass

    @visitor.when(type_collected.CoolProgramNode)
    def visit(self, node: type_collected.CoolProgramNode):  # type: ignore
        self.types = node.types

        object_type = self.get_type("Object")
        int_type = self.get_type("Int")
        bool_type = self.get_type("Bool")
        string_type = self.get_type("String")
        io_type = self.get_type("IO")

        object_type.define_method("abort", [], [], object_type)
        object_type.define_method("type_name", [], [], string_type)
        object_type.define_method("copy", [], [], semantic.SelfType(object_type))

        io_type.define_method(
            "out_string", ["x"], [string_type], semantic.SelfType(io_type)
        )
        io_type.define_method("out_int", ["x"], [int_type], semantic.SelfType(io_type))
        io_type.define_method("in_string", [], [], string_type)
        io_type.define_method("in_int", [], [], int_type)

        string_type.define_method("length", [], [], int_type)
        string_type.define_method("concat", ["s"], [string_type], string_type)
        string_type.define_method(
            "substr", ["i", "l"], [int_type, int_type], string_type
        )

        int_type.set_parent(object_type)
        bool_type.set_parent(object_type)
        string_type.set_parent(object_type)
        io_type.set_parent(object_type)

        classes = [self.visit(c) for c in node.classes]

        return type_built.CoolProgramNode(
            node.lineno, node.columnno, classes, self.types
        )

    @visitor.when(type_collected.CoolClassNode)
    def visit(self, node: type_collected.CoolClassNode):  # type: ignore
        self.current_type = node.type

        parent_type = self.types["Object"]
        if node.parent is not None:
            try:
                parent_type = self.get_type(node.parent)
            except semantic.BaseSemanticError as e:
                self.errors.append(e.with_pos(node.lineno, node.columnno))

        try:
            self.current_type.set_parent(parent_type)
        except semantic.BaseSemanticError as e:
            self.errors.append(e.with_pos(node.lineno, node.columnno))

        # attr_info = self.current_type.define_attribute("self", self.current_type)
        # self_attr = type_built.CoolAttrDeclNode(
        #     node.lineno, node.columnno, attr_info, None
        # )
        # features = [self_attr] + [self.visit(feat) for feat in node.features]
        features = [self.visit(feat) for feat in node.features]

        return type_built.CoolClassNode(
            node.lineno, node.columnno, node.type, features, node.parent
        )

    @visitor.when(type_collected.CoolAttrDeclNode)
    def visit(self, node: type_collected.CoolAttrDeclNode):  # type: ignore
        try:
            type = self.get_type(node.type)
        except semantic.BaseSemanticError as e:
            self.errors.append(e.with_pos(node.lineno, node.columnno))
            type = ErrorType()

        try:
            attr_info = self.current_type.define_attribute(node.id, type)
        except semantic.BaseSemanticError as e:
            self.errors.append(e.with_pos(node.lineno, node.columnno))
            attr_info = None  # TODO: check

        body = self.visit(node.body) if node.body is not None else None
        return type_built.CoolAttrDeclNode(
            node.lineno, node.columnno, attr_info, body=body
        )

    @visitor.when(type_collected.CoolMethodDeclNode)
    def visit(self, node: type_collected.CoolMethodDeclNode):  # type: ignore
        # print(node.param_names)
        param_types = []
        for ptype_name in node.param_types:
            try:
                ptype = self.get_type(ptype_name)
            except semantic.BaseSemanticError as e:
                self.errors.append(e.with_pos(node.lineno, node.columnno))
                ptype = ErrorType()
            param_types.append(ptype)

        try:
            return_type = self.get_type(node.type)
        except semantic.BaseSemanticError as e:
            self.errors.append(e.with_pos(node.lineno, node.columnno))
            return_type = ErrorType()

        try:
            method_info = self.current_type.define_method(
                node.id, node.param_names, param_types, return_type,
            )
        except semantic.BaseSemanticError as e:
            self.errors.append(e.with_pos(node.lineno, node.columnno))
            method_info = None  # TODO: check

        body = self.visit(node.body)

        return type_built.CoolMethodDeclNode(
            node.lineno, node.columnno, method_info, body
        )

    @visitor.when(type_collected.CoolAssignNode)
    def visit(self, node: type_collected.CoolAssignNode):  # type: ignore
        expr = self.visit(node.expr)
        return type_built.CoolAssignNode(node.lineno, node.columnno, node.id, expr)

    @visitor.when(type_collected.CoolStaticDispatchNode)
    def visit(self, node: type_collected.CoolStaticDispatchNode):  # type: ignore
        expr = self.visit(node.expr)
        args = [self.visit(arg) for arg in node.args]
        return type_built.CoolStaticDispatchNode(
            node.lineno, node.columnno, expr, node.static_type, node.id, args
        )

    @visitor.when(type_collected.CoolDispatchNode)
    def visit(self, node: type_collected.CoolDispatchNode):  # type: ignore
        expr = self.visit(node.expr)
        args = [self.visit(arg) for arg in node.args]
        return type_built.CoolDispatchNode(
            node.lineno, node.columnno, expr, node.id, args
        )

    @visitor.when(type_collected.CoolIfThenElseNode)
    def visit(self, node: type_collected.CoolIfThenElseNode):  # type: ignore
        cond = self.visit(node.cond)
        then_expr = self.visit(node.then_expr)
        else_expr = self.visit(node.else_expr)
        return type_built.CoolIfThenElseNode(
            node.lineno, node.columnno, cond, then_expr, else_expr
        )

    @visitor.when(type_collected.CoolWhileNode)
    def visit(self, node: type_collected.CoolWhileNode):  # type: ignore
        cond = self.visit(node.cond)
        body = self.visit(node.body)
        return type_built.CoolWhileNode(node.lineno, node.columnno, cond, body)

    @visitor.when(type_collected.CoolBlockNode)
    def visit(self, node: type_collected.CoolBlockNode):  # type: ignore
        expr_list = [self.visit(expr) for expr in node.expr_list]
        return type_built.CoolBlockNode(node.lineno, node.columnno, expr_list)

    @visitor.when(type_collected.CoolLetInNode)
    def visit(self, node: type_collected.CoolLetInNode):  # type: ignore
        decl_list = [self.visit(decl) for decl in node.decl_list]
        expr = self.visit(node.expr)
        return type_built.CoolLetInNode(node.lineno, node.columnno, decl_list, expr)

    @visitor.when(type_collected.CoolLetDeclNode)
    def visit(self, node: type_collected.CoolLetDeclNode):  # type: ignore
        expr = self.visit(node.expr)
        return type_built.CoolLetDeclNode(
            node.lineno, node.columnno, node.id, node.type, expr
        )

    @visitor.when(type_collected.CoolCaseNode)
    def visit(self, node: type_collected.CoolCaseNode):  # type: ignore
        case_branches = [self.visit(branch) for branch in node.case_branches]
        expr = self.visit(node.expr)
        return type_built.CoolCaseNode(node.lineno, node.columnno, expr, case_branches)

    @visitor.when(type_collected.CoolCaseBranchNode)
    def visit(self, node: type_collected.CoolCaseBranchNode):  # type: ignore
        expr = self.visit(node.expr)
        return type_built.CoolCaseBranchNode(
            node.lineno, node.columnno, node.id, node.type, expr
        )

    @visitor.when(type_collected.CoolNewNode)
    def visit(self, node: type_collected.CoolNewNode):  # type: ignore
        return type_built.CoolNewNode(node.lineno, node.columnno, node.type_name)

    @visitor.when(type_collected.CoolParenthNode)
    def visit(self, node: type_collected.CoolParenthNode):  # type: ignore
        expr = self.visit(node.expr)
        return type_built.CoolParenthNode(node.lineno, node.columnno, expr)

    @visitor.when(type_collected.CoolTildeNode)
    def visit(self, node: type_collected.CoolTildeNode):  # type: ignore
        expr = self.visit(node.expr)
        return type_built.CoolTildeNode(node.lineno, node.columnno, expr)

    @visitor.when(type_collected.CoolNotNode)
    def visit(self, node: type_collected.CoolNotNode):  # type: ignore
        expr = self.visit(node.expr)
        return type_built.CoolNotNode(node.lineno, node.columnno, expr)

    @visitor.when(type_collected.CoolIsVoidNode)
    def visit(self, node: type_collected.CoolIsVoidNode):  # type: ignore
        expr = self.visit(node.expr)
        return type_built.CoolIsVoidNode(node.lineno, node.columnno, expr)

    @visitor.when(type_collected.CoolLeqNode)
    def visit(self, node: type_collected.CoolLeqNode):  # type: ignore
        left_expr = self.visit(node.left_expr)
        right_expr = self.visit(node.right_expr)
        return type_built.CoolLeqNode(node.lineno, node.columnno, left_expr, right_expr)

    @visitor.when(type_collected.CoolEqNode)
    def visit(self, node: type_collected.CoolEqNode):  # type: ignore
        left_expr = self.visit(node.left_expr)
        right_expr = self.visit(node.right_expr)
        return type_built.CoolEqNode(node.lineno, node.columnno, left_expr, right_expr)

    @visitor.when(type_collected.CoolLeNode)
    def visit(self, node: type_collected.CoolLeNode):  # type: ignore
        left_expr = self.visit(node.left_expr)
        right_expr = self.visit(node.right_expr)
        return type_built.CoolLeNode(node.lineno, node.columnno, left_expr, right_expr)

    @visitor.when(type_collected.CoolPlusNode)
    def visit(self, node: type_collected.CoolPlusNode):  # type: ignore
        left_expr = self.visit(node.left_expr)
        right_expr = self.visit(node.right_expr)
        return type_built.CoolPlusNode(
            node.lineno, node.columnno, left_expr, right_expr
        )

    @visitor.when(type_collected.CoolMinusNode)
    def visit(self, node: type_collected.CoolMinusNode):  # type: ignore
        left_expr = self.visit(node.left_expr)
        right_expr = self.visit(node.right_expr)
        return type_built.CoolMinusNode(
            node.lineno, node.columnno, left_expr, right_expr
        )

    @visitor.when(type_collected.CoolMultNode)
    def visit(self, node: type_collected.CoolMultNode):  # type: ignore
        left_expr = self.visit(node.left_expr)
        right_expr = self.visit(node.right_expr)
        return type_built.CoolMultNode(
            node.lineno, node.columnno, left_expr, right_expr
        )

    @visitor.when(type_collected.CoolDivNode)
    def visit(self, node: type_collected.CoolDivNode):  # type: ignore
        left_expr = self.visit(node.left_expr)
        right_expr = self.visit(node.right_expr)
        return type_built.CoolDivNode(node.lineno, node.columnno, left_expr, right_expr)

    @visitor.when(type_collected.CoolIntNode)
    def visit(self, node: type_collected.CoolIntNode):  # type: ignore
        return type_built.CoolIntNode(node.lineno, node.columnno, node.value)

    @visitor.when(type_collected.CoolBoolNode)
    def visit(self, node: type_collected.CoolBoolNode):  # type: ignore
        return type_built.CoolBoolNode(node.lineno, node.columnno, node.value)

    @visitor.when(type_collected.CoolStringNode)
    def visit(self, node: type_collected.CoolStringNode):  # type: ignore
        return type_built.CoolStringNode(node.lineno, node.columnno, node.value)

    @visitor.when(type_collected.CoolVarNode)
    def visit(self, node: type_collected.CoolVarNode):  # type: ignore
        return type_built.CoolVarNode(node.lineno, node.columnno, node.value)
