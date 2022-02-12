import coolpyler.ast.cool.base as base


class CoolExprNode(base.CoolExprNode):
    def __init__(self, lineno, columnno, expr_type):
        super().__init__(lineno, columnno)
        self.expr_type = expr_type


class CoolAssignNode(CoolExprNode):
    def __init__(self, lineno, columnno, expr_type, id, expr):
        super().__init__(lineno, columnno, expr_type)

        self.id = id
        self.expr = expr


class CoolStaticDispatchNode(CoolExprNode):
    def __init__(self, lineno, columnno, expr_type, expr, static_type, id, args):
        super().__init__(lineno, columnno, expr_type)

        self.expr = expr
        self.static_type = static_type
        self.id = id
        self.args = args


class CoolDispatchNode(CoolExprNode):
    def __init__(self, lineno, columnno, expr_type, expr, id, args):
        super().__init__(lineno, columnno, expr_type)

        self.expr = expr
        self.id = id
        self.args = args


class CoolIfThenElseNode(CoolExprNode):
    def __init__(self, lineno, columnno, expr_type, cond, then_expr, else_expr):
        super().__init__(lineno, columnno, expr_type)

        self.cond = cond
        self.then_expr = then_expr
        self.else_expr = else_expr


class CoolWhileNode(CoolExprNode):
    def __init__(self, lineno, columnno, expr_type, cond, body):
        super().__init__(lineno, columnno, expr_type)

        self.cond = cond
        self.body = body


class CoolBlockNode(CoolExprNode):
    def __init__(self, lineno, columnno, expr_type, expr_list):
        super().__init__(lineno, columnno, expr_type)

        self.expr_list = expr_list


class CoolLetInNode(CoolExprNode):
    def __init__(self, lineno, columnno, expr_type, decl_list, expr):
        super().__init__(lineno, columnno, expr_type)

        self.decl_list = decl_list
        self.expr = expr


class CoolCaseNode(CoolExprNode):
    def __init__(self, lineno, columnno, expr_type, expr, case_branches):
        super().__init__(lineno, columnno, expr_type)

        self.expr = expr
        self.case_branches = case_branches


class CoolNewNode(CoolExprNode):
    def __init__(self, lineno, columnno, expr_type, type):
        super().__init__(lineno, columnno, expr_type)

        self.type = type


class CoolParenthNode(CoolExprNode):
    def __init__(self, lineno, columnno, expr_type, expr):
        super().__init__(lineno, columnno, expr_type)

        self.expr = expr


class CoolUnaryExprNode(CoolExprNode):
    def __init__(self, lineno, columnno, expr_type, expr):
        super().__init__(lineno, columnno, expr_type)

        self.expr = expr


class CoolBinaryExprNode(CoolExprNode):
    def __init__(self, lineno, columnno, expr_type, left_expr, right_expr):
        super().__init__(lineno, columnno, expr_type)

        self.left_expr = left_expr
        self.right_expr = right_expr


class CoolAtomNode(CoolExprNode):
    def __init__(self, lineno, columnno, expr_type, value):
        super().__init__(lineno, columnno, expr_type)

        self.value = value
