import coolpyler.ast.cool.parsed as parsed
import coolpyler.ast.cool.type_collected as type_collected
import coolpyler.utils.visitor as visitor
from coolpyler.errors import SemanticError
from coolpyler.semantic import BoolType, IntType, IOType, ObjectType, StringType, Type


class TypeCollectorVisitor(object):
    def __init__(self, errors=None):
        if errors is None:
            errors = []
        self.errors = errors
        self.types = None

    @visitor.on("node")
    def visit(self, node):
        pass

    @visitor.when(parsed.CoolProgramNode)
    def visit(self, node: parsed.CoolProgramNode):
        object_type = ObjectType()
        int_type = IntType()
        bool_type = BoolType()
        string_type = StringType()
        io_type = IOType()

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

    @visitor.when(parsed.CoolClassNode)
    def visit(self, node: parsed.CoolClassNode):
        try:
            type = self.types[node.id]
            self.errors.append(
                SemanticError(
                    node.lineno, 0, f"Type with name `{node.id}` already defined."
                )
            )
            return None
        except KeyError:
            type = self.types[node.id] = Type(node.id)

        features = [self.visit(feat) for feat in node.features]

        return type_collected.CoolClassNode(
            node.lineno, node.columnno, type, features, parent=node.parent
        )

    @visitor.when(parsed.CoolAttrDeclNode)
    def visit(self, node: parsed.CoolAttrDeclNode):
        body = self.visit(node.body)
        return type_collected.CoolAttrDeclNode(
            node.lineno, node.columnno, node.id, node.type, body
        )

    @visitor.when(parsed.CoolMethodDeclNode)
    def visit(self, node: parsed.CoolMethodDeclNode):
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

    @visitor.when(parsed.CoolAssignNode)
    def visit(self, node: parsed.CoolAssignNode):
        expr = self.visit(node.expr)
        return type_collected.CoolAssignNode(node.lineno, node.columnno, node.id, expr)

    @visitor.when(parsed.CoolStaticDispatchNode)
    def visit(self, node: parsed.CoolStaticDispatchNode):
        expr = self.visit(node.expr)
        args = [self.visit(arg) for arg in node.args]
        return type_collected.CoolStaticDispatchNode(
            node.lineno, node.columnno, expr, node.static_type, node.id, args
        )

    @visitor.when(parsed.CoolDispatchNode)
    def visit(self, node: parsed.CoolDispatchNode):
        expr = self.visit(node.expr)
        args = [self.visit(arg) for arg in node.args]
        return type_collected.CoolDispatchNode(
            node.lineno, node.columnno, expr, node.id, args
        )

    @visitor.when(parsed.CoolIfThenElseNode)
    def visit(self, node: parsed.CoolIfThenElseNode):
        cond = self.visit(node.cond)
        then_expr = self.visit(node.then_expr)
        else_expr = self.visit(node.else_expr)
        return type_collected.CoolIfThenElseNode(
            node.lineno, node.columnno, cond, then_expr, else_expr
        )

    @visitor.when(parsed.CoolWhileNode)
    def visit(self, node: parsed.CoolWhileNode):
        cond = self.visit(node.cond)
        body = self.visit(node.body)
        return type_collected.CoolWhileNode(node.lineno, node.columnno, cond, body)

    @visitor.when(parsed.CoolBlockNode)
    def visit(self, node: parsed.CoolBlockNode):
        expr_list = [self.visit(expr) for expr in node.expr_list]
        return type_collected.CoolBlockNode(node.lineno, node.columnno, expr_list)

    @visitor.when(parsed.CoolLetInNode)
    def visit(self, node: parsed.CoolLetInNode):
        decl_list = [self.visit(decl) for decl in node.decl_list]
        expr = self.visit(node.expr)
        return type_collected.CoolLetInNode(node.lineno, node.columnno, decl_list, expr)

    @visitor.when(parsed.CoolLetDeclNode)
    def visit(self, node: parsed.CoolLetDeclNode):
        expr = self.visit(node.expr)
        return type_collected.CoolLetDeclNode(
            node.lineno, node.columnno, node.id, node.type, expr
        )

    @visitor.when(parsed.CoolCaseNode)
    def visit(self, node: parsed.CoolCaseNode):
        case_branches = [self.visit(branch) for branch in node.case_branches]
        expr = self.visit(node.expr)
        return type_collected.CoolCaseNode(
            node.lineno, node.columnno, expr, case_branches
        )

    @visitor.when(parsed.CoolCaseBranchNode)
    def visit(self, node: parsed.CoolCaseBranchNode):
        expr = self.visit(node.expr)
        return type_collected.CoolCaseBranchNode(
            node.lineno, node.columnno, node.id, node.type, expr
        )

    @visitor.when(parsed.CoolNewNode)
    def visit(self, node: parsed.CoolNewNode):
        return type_collected.CoolNewNode(node.lineno, node.columnno, node.type_name)

    @visitor.when(parsed.CoolParenthNode)
    def visit(self, node: parsed.CoolParenthNode):
        expr = self.visit(node.expr)
        return type_collected.CoolParenthNode(node.lineno, node.columnno, expr)

    @visitor.when(parsed.CoolTildeNode)
    def visit(self, node: parsed.CoolTildeNode):
        expr = self.visit(node.expr)
        return type_collected.CoolTildeNode(node.lineno, node.columnno, expr)

    @visitor.when(parsed.CoolNotNode)
    def visit(self, node: parsed.CoolNotNode):
        expr = self.visit(node.expr)
        return type_collected.CoolNotNode(node.lineno, node.columnno, expr)

    @visitor.when(parsed.CoolIsVoidNode)
    def visit(self, node: parsed.CoolIsVoidNode):
        expr = self.visit(node.expr)
        return type_collected.CoolIsVoidNode(node.lineno, node.columnno, expr)

    @visitor.when(parsed.CoolLeqNode)
    def visit(self, node: parsed.CoolLeqNode):
        left_expr = self.visit(node.left_expr)
        right_expr = self.visit(node.right_expr)
        return type_collected.CoolLeqNode(
            node.lineno, node.columnno, left_expr, right_expr
        )

    @visitor.when(parsed.CoolEqNode)
    def visit(self, node: parsed.CoolEqNode):
        left_expr = self.visit(node.left_expr)
        right_expr = self.visit(node.right_expr)
        return type_collected.CoolEqNode(
            node.lineno, node.columnno, left_expr, right_expr
        )

    @visitor.when(parsed.CoolLeNode)
    def visit(self, node: parsed.CoolLeNode):
        left_expr = self.visit(node.left_expr)
        right_expr = self.visit(node.right_expr)
        return type_collected.CoolLeNode(
            node.lineno, node.columnno, left_expr, right_expr
        )

    @visitor.when(parsed.CoolPlusNode)
    def visit(self, node: parsed.CoolPlusNode):
        left_expr = self.visit(node.left_expr)
        right_expr = self.visit(node.right_expr)
        return type_collected.CoolPlusNode(
            node.lineno, node.columnno, left_expr, right_expr
        )

    @visitor.when(parsed.CoolMinusNode)
    def visit(self, node: parsed.CoolMinusNode):
        left_expr = self.visit(node.left_expr)
        right_expr = self.visit(node.right_expr)
        return type_collected.CoolMinusNode(
            node.lineno, node.columnno, left_expr, right_expr
        )

    @visitor.when(parsed.CoolMultNode)
    def visit(self, node: parsed.CoolMultNode):
        left_expr = self.visit(node.left_expr)
        right_expr = self.visit(node.right_expr)
        return type_collected.CoolMultNode(
            node.lineno, node.columnno, left_expr, right_expr
        )

    @visitor.when(parsed.CoolDivNode)
    def visit(self, node: parsed.CoolDivNode):
        left_expr = self.visit(node.left_expr)
        right_expr = self.visit(node.right_expr)
        return type_collected.CoolDivNode(
            node.lineno, node.columnno, left_expr, right_expr
        )

    @visitor.when(parsed.CoolIntNode)
    def visit(self, node: parsed.CoolIntNode):
        return type_collected.CoolIntNode(node.lineno, node.columnno, node.value)

    @visitor.when(parsed.CoolBoolNode)
    def visit(self, node: parsed.CoolBoolNode):
        return type_collected.CoolBoolNode(node.lineno, node.columnno, node.value)

    @visitor.when(parsed.CoolStringNode)
    def visit(self, node: parsed.CoolStringNode):
        return type_collected.CoolStringNode(node.lineno, node.columnno, node.value)

    @visitor.when(parsed.CoolVarNode)
    def visit(self, node: parsed.CoolVarNode):
        return type_collected.CoolVarNode(node.lineno, node.columnno, node.value)
