import coolpyler.ast.cool.parsed as parsed
import coolpyler.ast.cool.type_collected as type_collected
import coolpyler.utils.visitor as visitor
from coolpyler.errors import SemanticError
from coolpyler.semantic import (
    BoolType,
    ErrorType,
    IntType,
    IOType,
    ObjectType,
    SelfType,
    StringType,
    Type,
)


class TypeCollectorVisitor(object):
    def __init__(self, errors=None):
        if errors is None:
            errors = []
        self.errors = errors
        self.types = None

    @visitor.on("node")
    def visit(self, node):
        pass

    @visitor.when(parsed.CoolProgramNode)  # noqa: F811
    def visit(self, node: parsed.CoolProgramNode):  # noqa: F811
        object_type = ObjectType()

        int_type = IntType()
        int_type.set_parent(object_type)

        bool_type = BoolType()
        bool_type.set_parent(object_type)

        string_type = StringType()
        string_type.set_parent(object_type)

        io_type = IOType()
        io_type.set_parent(object_type)

        # self_type = SelfType()
        # self_type.set_parent(object_type)

        self.types = {
            object_type.name: object_type,
            int_type.name: int_type,
            bool_type.name: bool_type,
            string_type.name: string_type,
            io_type.name: io_type,
        }

        classes = [self.visit(c) for c in node.classes]

        return type_collected.CoolProgramNode(
            node.lineno, node.columnno, classes, self.types
        )

    @visitor.when(parsed.CoolClassNode)  # noqa: F811
    def visit(self, node: parsed.CoolClassNode):  # noqa: F811
        if node.id in self.types:
            self.errors.append(
                SemanticError(
                    node.lineno, 0, f"Type with name `{node.id}` already defined."
                )
            )
            type = ErrorType()
        else:
            type = self.types[node.id] = Type(node.id)

        features = [self.visit(feat) for feat in node.features]

        return type_collected.CoolClassNode(
            node.lineno, node.columnno, type, features, parent=node.parent
        )

    @visitor.when(parsed.CoolAttrDeclNode)  # noqa: F811
    def visit(self, node: parsed.CoolAttrDeclNode):  # noqa: F811
        body = self.visit(node.body)
        return type_collected.CoolAttrDeclNode(
            node.lineno, node.columnno, node.id, node.type, body
        )

    @visitor.when(parsed.CoolMethodDeclNode)  # noqa: F811
    def visit(self, node: parsed.CoolMethodDeclNode):  # noqa: F811
        body = self.visit(node.body)
        return type_collected.CoolMethodDeclNode(
            node.lineno,
            node.columnno,
            node.id,
            node.param_names,
            node.param_types,
            node.type,
            body,
        )

    @visitor.when(parsed.CoolAssignNode)  # noqa: F811
    def visit(self, node: parsed.CoolAssignNode):  # noqa: F811
        expr = self.visit(node.expr)
        return type_collected.CoolAssignNode(node.lineno, node.columnno, node.id, expr)

    @visitor.when(parsed.CoolStaticDispatchNode)  # noqa: F811
    def visit(self, node: parsed.CoolStaticDispatchNode):  # noqa: F811
        expr = self.visit(node.expr)
        args = [self.visit(arg) for arg in node.args]
        return type_collected.CoolStaticDispatchNode(
            node.lineno, node.columnno, expr, node.static_type, node.id, args
        )

    @visitor.when(parsed.CoolDispatchNode)  # noqa: F811
    def visit(self, node: parsed.CoolDispatchNode):  # noqa: F811
        expr = self.visit(node.expr)
        args = [self.visit(arg) for arg in node.args]
        return type_collected.CoolDispatchNode(
            node.lineno, node.columnno, node.id, args, expr
        )

    @visitor.when(parsed.CoolIfThenElseNode)  # noqa: F811
    def visit(self, node: parsed.CoolIfThenElseNode):  # noqa: F811
        cond = self.visit(node.cond)
        then_expr = self.visit(node.then_expr)
        else_expr = self.visit(node.else_expr)
        return type_collected.CoolIfThenElseNode(
            node.lineno, node.columnno, cond, then_expr, else_expr
        )

    @visitor.when(parsed.CoolWhileNode)  # noqa: F811
    def visit(self, node: parsed.CoolWhileNode):  # noqa: F811
        cond = self.visit(node.cond)
        body = self.visit(node.body)
        return type_collected.CoolWhileNode(node.lineno, node.columnno, cond, body)

    @visitor.when(parsed.CoolBlockNode)  # noqa: F811
    def visit(self, node: parsed.CoolBlockNode):  # noqa: F811
        expr_list = [self.visit(expr) for expr in node.expr_list]
        return type_collected.CoolBlockNode(node.lineno, node.columnno, expr_list)

    @visitor.when(parsed.CoolLetInNode)  # noqa: F811
    def visit(self, node: parsed.CoolLetInNode):  # noqa: F811
        decl_list = [self.visit(decl) for decl in node.decl_list]
        expr = self.visit(node.expr)
        return type_collected.CoolLetInNode(node.lineno, node.columnno, decl_list, expr)

    @visitor.when(parsed.CoolLetDeclNode)  # noqa: F811
    def visit(self, node: parsed.CoolLetDeclNode):  # noqa: F811
        expr = self.visit(node.expr)
        return type_collected.CoolLetDeclNode(
            node.lineno, node.columnno, node.id, node.type, expr
        )

    @visitor.when(parsed.CoolCaseNode)  # noqa: F811
    def visit(self, node: parsed.CoolCaseNode):  # noqa: F811
        case_branches = [self.visit(branch) for branch in node.case_branches]
        expr = self.visit(node.expr)
        return type_collected.CoolCaseNode(
            node.lineno, node.columnno, expr, case_branches
        )

    @visitor.when(parsed.CoolCaseBranchNode)  # noqa: F811
    def visit(self, node: parsed.CoolCaseBranchNode):  # noqa: F811
        expr = self.visit(node.expr)
        return type_collected.CoolCaseBranchNode(
            node.lineno, node.columnno, node.id, node.type, expr
        )

    @visitor.when(parsed.CoolNewNode)  # noqa: F811
    def visit(self, node: parsed.CoolNewNode):  # noqa: F811
        return type_collected.CoolNewNode(node.lineno, node.columnno, node.type)

    @visitor.when(parsed.CoolParenthNode)  # noqa: F811
    def visit(self, node: parsed.CoolParenthNode):  # noqa: F811
        expr = self.visit(node.expr)
        return type_collected.CoolParenthNode(node.lineno, node.columnno, expr)

    @visitor.when(parsed.CoolTildeNode)  # noqa: F811
    def visit(self, node: parsed.CoolTildeNode):  # noqa: F811
        expr = self.visit(node.expr)
        return type_collected.CoolTildeNode(node.lineno, node.columnno, expr)

    @visitor.when(parsed.CoolNotNode)  # noqa: F811
    def visit(self, node: parsed.CoolNotNode):  # noqa: F811
        expr = self.visit(node.expr)
        return type_collected.CoolNotNode(node.lineno, node.columnno, expr)

    @visitor.when(parsed.CoolIsVoidNode)  # noqa: F811
    def visit(self, node: parsed.CoolIsVoidNode):  # noqa: F811
        expr = self.visit(node.expr)
        return type_collected.CoolIsVoidNode(node.lineno, node.columnno, expr)

    @visitor.when(parsed.CoolLeqNode)  # noqa: F811
    def visit(self, node: parsed.CoolLeqNode):  # noqa: F811
        left_expr = self.visit(node.left_expr)
        right_expr = self.visit(node.right_expr)
        return type_collected.CoolLeqNode(
            node.lineno, node.columnno, left_expr, right_expr
        )

    @visitor.when(parsed.CoolEqNode)  # noqa: F811
    def visit(self, node: parsed.CoolEqNode):  # noqa: F811
        left_expr = self.visit(node.left_expr)
        right_expr = self.visit(node.right_expr)
        return type_collected.CoolEqNode(
            node.lineno, node.columnno, left_expr, right_expr
        )

    @visitor.when(parsed.CoolLeNode)  # noqa: F811
    def visit(self, node: parsed.CoolLeNode):  # noqa: F811
        left_expr = self.visit(node.left_expr)
        right_expr = self.visit(node.right_expr)
        return type_collected.CoolLeNode(
            node.lineno, node.columnno, left_expr, right_expr
        )

    @visitor.when(parsed.CoolPlusNode)  # noqa: F811
    def visit(self, node: parsed.CoolPlusNode):  # noqa: F811
        left_expr = self.visit(node.left_expr)
        right_expr = self.visit(node.right_expr)
        return type_collected.CoolPlusNode(
            node.lineno, node.columnno, left_expr, right_expr
        )

    @visitor.when(parsed.CoolMinusNode)  # noqa: F811
    def visit(self, node: parsed.CoolMinusNode):  # noqa: F811
        left_expr = self.visit(node.left_expr)
        right_expr = self.visit(node.right_expr)
        return type_collected.CoolMinusNode(
            node.lineno, node.columnno, left_expr, right_expr
        )

    @visitor.when(parsed.CoolMultNode)  # noqa: F811
    def visit(self, node: parsed.CoolMultNode):  # noqa: F811
        left_expr = self.visit(node.left_expr)
        right_expr = self.visit(node.right_expr)
        return type_collected.CoolMultNode(
            node.lineno, node.columnno, left_expr, right_expr
        )

    @visitor.when(parsed.CoolDivNode)  # noqa: F811
    def visit(self, node: parsed.CoolDivNode):  # noqa: F811
        left_expr = self.visit(node.left_expr)
        right_expr = self.visit(node.right_expr)
        return type_collected.CoolDivNode(
            node.lineno, node.columnno, left_expr, right_expr
        )

    @visitor.when(parsed.CoolIntNode)  # noqa: F811
    def visit(self, node: parsed.CoolIntNode):  # noqa: F811
        return type_collected.CoolIntNode(node.lineno, node.columnno, node.value)

    @visitor.when(parsed.CoolBoolNode)  # noqa: F811
    def visit(self, node: parsed.CoolBoolNode):  # noqa: F811
        return type_collected.CoolBoolNode(node.lineno, node.columnno, node.value)

    @visitor.when(parsed.CoolStringNode)  # noqa: F811
    def visit(self, node: parsed.CoolStringNode):  # noqa: F811
        return type_collected.CoolStringNode(node.lineno, node.columnno, node.value)

    @visitor.when(parsed.CoolVarNode)  # noqa: F811
    def visit(self, node: parsed.CoolVarNode):  # noqa: F811
        return type_collected.CoolVarNode(node.lineno, node.columnno, node.value)

