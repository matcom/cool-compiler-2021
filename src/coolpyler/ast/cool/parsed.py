import coolpyler.ast.cool.base as base


class CoolAstNode(base.CoolAstNode):
    pass


class CoolFeatureNode(base.CoolFeatureNode):
    pass


class CoolProgramNode(base.CoolProgramNode):
    def __init__(self, lineno, columnno, classes):
        super().__init__(lineno, columnno)

        self.classes = classes


class CoolClassNode(base.CoolClassNode):
    def __init__(self, lineno, columnno, id, features, parent=None):
        super().__init__(lineno, columnno)

        self.id = id
        self.parent = parent
        self.features = features


class CoolAttrDeclNode(base.CoolAttrDeclNode):
    def __init__(self, lineno, columnno, id, type, body=None):
        super().__init__(lineno, columnno)

        self.id = id
        self.type = type
        self.body = body


class CoolMethodDeclNode(base.CoolMethodDeclNode):
    def __init__(self, lineno, columnno, id, param_names, param_types, type, body):
        super().__init__(lineno, columnno)

        self.id = id
        self.param_names = param_names
        self.param_types = param_types
        self.type = type
        self.body = body


class CoolExprNode(base.CoolExprNode):
    pass


class CoolAssignNode(base.CoolAssignNode):
    def __init__(self, lineno, columnno, id, expr):
        super().__init__(lineno, columnno)

        self.id = id
        self.expr = expr


class CoolStaticDispatchNode(base.CoolStaticDispatchNode):
    def __init__(self, lineno, columnno, expr, static_type, id, args):
        super().__init__(lineno, columnno)

        self.expr = expr
        self.static_type = static_type
        self.id = id
        self.args = args


class CoolDispatchNode(base.CoolDispatchNode):
    def __init__(self, lineno, columnno, id, args, expr=None):
        super().__init__(lineno, columnno)

        self.expr = expr
        self.id = id
        self.args = args


class CoolIfThenElseNode(base.CoolIfThenElseNode):
    def __init__(self, lineno, columnno, cond, then_expr, else_expr):
        super().__init__(lineno, columnno)

        self.cond = cond
        self.then_expr = then_expr
        self.else_expr = else_expr


class CoolWhileNode(base.CoolWhileNode):
    def __init__(self, lineno, columnno, cond, body):
        super().__init__(lineno, columnno)

        self.cond = cond
        self.body = body


class CoolBlockNode(base.CoolBlockNode):
    def __init__(self, lineno, columnno, expr_list):
        super().__init__(lineno, columnno)

        self.expr_list = expr_list


class CoolLetInNode(base.CoolLetInNode):
    def __init__(self, lineno, columnno, decl_list, expr):
        super().__init__(lineno, columnno)

        self.decl_list = decl_list
        self.expr = expr


class CoolLetDeclNode(base.CoolLetDeclNode):
    def __init__(self, lineno, columnno, id, type, expr=None):
        super().__init__(lineno, columnno)

        self.id = id
        self.type = type
        self.expr = expr


class CoolCaseNode(base.CoolCaseNode):
    def __init__(self, lineno, columnno, expr, case_branches):
        super().__init__(lineno, columnno)

        self.expr = expr
        self.case_branches = case_branches


class CoolCaseBranchNode(base.CoolCaseBranchNode):
    def __init__(self, lineno, columnno, id, type, expr):
        super().__init__(lineno, columnno)

        self.id = id
        self.type = type
        self.expr = expr


class CoolNewNode(base.CoolNewNode):
    def __init__(self, lineno, columnno, type):
        super().__init__(lineno, columnno)

        self.type = type


class CoolParenthNode(base.CoolParenthNode):
    def __init__(self, lineno, columnno, expr):
        super().__init__(lineno, columnno)

        self.expr = expr


class CoolUnaryExprNode(base.CoolUnaryExprNode):
    def __init__(self, lineno, columnno, expr):
        super().__init__(lineno, columnno)

        self.expr = expr


class CoolBinaryExprNode(base.CoolBinaryExprNode):
    def __init__(self, lineno, columnno, left_expr, right_expr):
        super().__init__(lineno, columnno)

        self.left_expr = left_expr
        self.right_expr = right_expr


class CoolAtomNode(base.CoolAtomNode):
    def __init__(self, lineno, columnno, value):
        super().__init__(lineno, columnno)

        self.value = value


class CoolComparisonNode(CoolBinaryExprNode):
    pass


class CoolLeqNode(CoolComparisonNode):
    pass


class CoolEqNode(CoolComparisonNode):
    pass


class CoolLeNode(CoolComparisonNode):
    pass


class CoolArithmeticNode(CoolBinaryExprNode):
    pass


class CoolPlusNode(CoolArithmeticNode):
    pass


class CoolMinusNode(CoolArithmeticNode):
    pass


class CoolMultNode(CoolArithmeticNode):
    pass


class CoolDivNode(CoolArithmeticNode):
    pass


class CoolIntNode(CoolAtomNode):
    pass


class CoolStringNode(CoolAtomNode):
    pass


class CoolBoolNode(CoolAtomNode):
    pass


class CoolVarNode(CoolAtomNode):
    pass


class CoolIsVoidNode(CoolUnaryExprNode):
    pass


class CoolNotNode(CoolUnaryExprNode):
    pass


class CoolTildeNode(CoolUnaryExprNode):
    pass
