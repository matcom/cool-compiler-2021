class CoolAstNode:
    def __init__(self, lineno, columnno):
        self.lineno = lineno
        self.columnno = columnno


class CoolProgramNode(CoolAstNode):
    def __init__(self, lineno, columnno, classes):
        super().__init__(lineno, columnno)
        # self.lineno = lineno
        # self.columnno = columnno

        self.classes = classes


class CoolClassNode(CoolAstNode):
    def __init__(self, lineno, columnno, id, features, parent=None):
        super().__init__(lineno, columnno)
        # self.lineno = lineno
        # self.columnno = columnno

        self.id = id
        self.parent = parent
        self.features = features


class CoolFeatureNode(CoolAstNode):
    pass


class CoolAttrDeclNode(CoolFeatureNode):
    def __init__(self, lineno, columnno, id, type, body=None):
        super().__init__(lineno, columnno)
        # self.lineno = lineno
        # self.columnno = columnno

        self.id = id
        self.type = type
        self.body = body


class CoolMethodDeclNode(CoolFeatureNode):
    def __init__(self, lineno, columnno, id, param_names, param_types, type, body):
        super().__init__(lineno, columnno)
        # self.lineno = lineno
        # self.columnno = columnno

        self.id = id
        self.param_names = param_names
        self.param_types = param_types
        self.type = type
        self.body = body


class CoolExprNode(CoolAstNode):
    pass


class CoolAssignNode(CoolExprNode):
    def __init__(self, lineno, columnno, id, expr):
        super().__init__(lineno, columnno)
        # self.lineno = lineno
        # self.columnno = columnno

        self.id = id
        self.expr = expr


class CoolStaticDispatchNode(CoolExprNode):
    def __init__(self, lineno, columnno, expr, static_type, id, args):
        super().__init__(lineno, columnno)
        # self.lineno = lineno
        # self.columnno = columnno

        self.expr = expr
        self.static_type = static_type
        self.id = id
        self.args = args


class CoolDispatchNode(CoolExprNode):
    def __init__(self, lineno, columnno, id, args, expr=None):
        super().__init__(lineno, columnno)
        # self.lineno = lineno
        # self.columnno = columnno

        self.expr = expr
        self.id = id
        self.args = args


class CoolIfThenElseNode(CoolExprNode):
    def __init__(self, lineno, columnno, cond, then_expr, else_expr):
        super().__init__(lineno, columnno)
        # self.lineno = lineno
        # self.columnno = columnno

        self.cond = cond
        self.then_expr = then_expr
        self.else_expr = else_expr


class CoolWhileNode(CoolExprNode):
    def __init__(self, lineno, columnno, cond, body):
        super().__init__(lineno, columnno)
        # self.lineno = lineno
        # self.columnno = columnno

        self.cond = cond
        self.body = body


class CoolBlockNode(CoolExprNode):
    def __init__(self, lineno, columnno, expr_list):
        super().__init__(lineno, columnno)
        # self.lineno = lineno
        # self.columnno = columnno

        self.expr_list = expr_list


class CoolLetInNode(CoolExprNode):
    def __init__(self, lineno, columnno, decl_list, expr):
        super().__init__(lineno, columnno)
        # self.lineno = lineno
        # self.columnno = columnno

        self.decl_list = decl_list
        self.expr = expr


class CoolLetDeclNode(CoolAstNode):
    def __init__(self, lineno, columnno, id, type, expr=None):
        super().__init__(lineno, columnno)
        # self.lineno = lineno
        # self.columnno = columnno

        self.id = id
        self.type = type
        self.expr = expr


class CoolCaseNode(CoolExprNode):
    def __init__(self, lineno, columnno, expr, case_branches):
        super().__init__(lineno, columnno)
        # self.lineno = lineno
        # self.columnno = columnno

        self.expr = expr
        self.case_branches = case_branches


class CoolCaseBranchNode(CoolAstNode):
    def __init__(self, lineno, columnno, id, type, expr):
        super().__init__(lineno, columnno)
        # self.lineno = lineno
        # self.columnno = columnno

        self.id = id
        self.type = type
        self.expr = expr


class CoolNewNode(CoolExprNode):
    def __init__(self, lineno, columnno, type):
        super().__init__(lineno, columnno)
        # self.lineno = lineno
        # self.columnno = columnno

        self.type = type


class CoolParenthNode(CoolExprNode):
    def __init__(self, lineno, columnno, expr):
        super().__init__(lineno, columnno)
        # self.lineno = lineno
        # self.columnno = columnno

        self.expr = expr


class CoolUnaryExprNode(CoolExprNode):
    def __init__(self, lineno, columnno, expr):
        super().__init__(lineno, columnno)
        # self.lineno = lineno
        # self.columnno = columnno

        self.expr = expr


class CoolIsVoidNode(CoolUnaryExprNode):
    pass


class CoolNotNode(CoolUnaryExprNode):
    pass


class CoolTildeNode(CoolUnaryExprNode):
    pass


class CoolBinaryExprNode(CoolExprNode):
    def __init__(self, lineno, columnno, left_expr, right_expr):
        super().__init__(lineno, columnno)
        # self.lineno = lineno
        # self.columnno = columnno

        self.left_expr = left_expr
        self.right_expr = right_expr


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


class CoolAtomNode(CoolExprNode):
    def __init__(self, lineno, columnno, value):
        super().__init__(lineno, columnno)
        # self.lineno = lineno
        # self.columnno = columnno

        self.value = value


class CoolIntNode(CoolAtomNode):
    pass


class CoolStringNode(CoolAtomNode):
    pass


class CoolBoolNode(CoolAtomNode):
    pass


class CoolVarNode(CoolAtomNode):
    pass
