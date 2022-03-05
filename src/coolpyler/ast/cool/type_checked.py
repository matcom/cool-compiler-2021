import coolpyler.utils.meta as meta
import coolpyler.ast.cool.type_built as type_built

meta.from_module(type_built)


class CoolExprNode:
    def __init__(self, lineno, columnno, expr_type):
        super().__init__(lineno, columnno)
        self.expr_type = expr_type


class CoolAssignNode:
    def __init__(self, lineno, columnno, expr_type, id, expr):
        super().__init__(lineno, columnno, expr_type)

        self.id = id
        self.expr = expr


class CoolStaticDispatchNode:
    def __init__(self, lineno, columnno, expr_type, expr, static_type, id, args):
        super().__init__(lineno, columnno, expr_type)

        self.expr = expr
        self.static_type = static_type
        self.id = id
        self.args = args


class CoolDispatchNode:
    def __init__(self, lineno, columnno, expr_type, expr, id, args):
        super().__init__(lineno, columnno, expr_type)

        self.expr = expr
        self.id = id
        self.args = args


class CoolIfThenElseNode:
    def __init__(self, lineno, columnno, expr_type, cond, then_expr, else_expr):
        super().__init__(lineno, columnno, expr_type)

        self.cond = cond
        self.then_expr = then_expr
        self.else_expr = else_expr


class CoolWhileNode:
    def __init__(self, lineno, columnno, expr_type, cond, body):
        super().__init__(lineno, columnno, expr_type)

        self.cond = cond
        self.body = body


class CoolBlockNode:
    def __init__(self, lineno, columnno, expr_type, expr_list):
        super().__init__(lineno, columnno, expr_type)

        self.expr_list = expr_list


class CoolLetInNode:
    def __init__(self, lineno, columnno, expr_type, decl_list, expr):
        super().__init__(lineno, columnno, expr_type)

        self.decl_list = decl_list
        self.expr = expr


class CoolCaseNode:
    def __init__(self, lineno, columnno, expr_type, expr, case_branches):
        super().__init__(lineno, columnno, expr_type)

        self.expr = expr
        self.case_branches = case_branches


class CoolNewNode:
    def __init__(self, lineno, columnno, expr_type, type):
        super().__init__(lineno, columnno, expr_type)

        self.type = type


class CoolParenthNode:
    def __init__(self, lineno, columnno, expr_type, expr):
        super().__init__(lineno, columnno, expr_type)

        self.expr = expr


class CoolUnaryExprNode:
    def __init__(self, lineno, columnno, expr_type, expr):
        super().__init__(lineno, columnno, expr_type)

        self.expr = expr


class CoolBinaryExprNode:
    def __init__(self, lineno, columnno, expr_type, left_expr, right_expr):
        super().__init__(lineno, columnno, expr_type)

        self.left_expr = left_expr
        self.right_expr = right_expr


class CoolAtomNode:
    def __init__(self, lineno, columnno, expr_type, value):
        super().__init__(lineno, columnno, expr_type)

        self.value = value
