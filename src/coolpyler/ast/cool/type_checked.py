import coolpyler.ast.cool.base as base
import coolpyler.ast.cool.type_built as type_built


class CoolAstNode(type_built.CoolAstNode):
    pass


class CoolProgramNode(base.CoolProgramNode):
    def __init__(self, lineno, columnno, classes, types, scope):
        super().__init__(lineno, columnno)

        self.classes = classes
        self.types = types
        self.scope = scope


class CoolClassNode(type_built.CoolClassNode):
    pass


class CoolFeatureNode(type_built.CoolFeatureNode):
    pass


class CoolAttrDeclNode(type_built.CoolAttrDeclNode):
    pass


class CoolMethodDeclNode(type_built.CoolMethodDeclNode):
    pass


class CoolLetDeclNode(base.CoolLetDeclNode):
    pass


class CoolCaseBranchNode(base.CoolCaseBranchNode):
    pass


class CoolExprNode(base.CoolExprNode):
    def __init__(self, lineno, columnno, type):
        super().__init__(lineno, columnno)
        self.type = type


class CoolAssignNode(CoolExprNode):
    def __init__(self, lineno, columnno, id, expr, type):
        super().__init__(lineno, columnno, type)

        self.id = id
        self.expr = expr


class CoolStaticDispatchNode(CoolExprNode):
    def __init__(self, lineno, columnno, expr, static_type, id, args, type):
        super().__init__(lineno, columnno, type)

        self.expr = expr
        self.static_type = static_type
        self.id = id
        self.args = args


class CoolDispatchNode(CoolExprNode):
    def __init__(self, lineno, columnno, id, args, type, expr=None):
        super().__init__(lineno, columnno, type)

        self.expr = expr
        self.id = id
        self.args = args


class CoolIfThenElseNode(CoolExprNode):
    def __init__(self, lineno, columnno, cond, then_expr, else_expr, type):
        super().__init__(lineno, columnno, type)

        self.cond = cond
        self.then_expr = then_expr
        self.else_expr = else_expr


class CoolWhileNode(CoolExprNode):
    def __init__(self, lineno, columnno, cond, body, type):
        super().__init__(lineno, columnno, type)

        self.cond = cond
        self.body = body


class CoolBlockNode(CoolExprNode):
    def __init__(self, lineno, columnno, expr_list, type):
        super().__init__(lineno, columnno, type)

        self.expr_list = expr_list


class CoolLetInNode(CoolExprNode):
    def __init__(self, lineno, columnno, decl_list, expr, type):
        super().__init__(lineno, columnno, type)

        self.decl_list = decl_list
        self.expr = expr


class CoolCaseNode(CoolExprNode):
    def __init__(self, lineno, columnno, expr, case_branches, type):
        super().__init__(lineno, columnno, type)

        self.expr = expr
        self.case_branches = case_branches


class CoolNewNode(CoolExprNode):
    def __init__(self, lineno, columnno, _type, type):
        super().__init__(lineno, columnno, type)

        self.type = _type


class CoolParenthNode(CoolExprNode):
    def __init__(self, lineno, columnno, expr, type):
        super().__init__(lineno, columnno, type)

        self.expr = expr


class CoolUnaryExprNode(CoolExprNode):
    def __init__(self, lineno, columnno, expr, type):
        super().__init__(lineno, columnno, type)

        self.expr = expr


class CoolBinaryExprNode(CoolExprNode):
    def __init__(self, lineno, columnno, left_expr, right_expr, type):
        super().__init__(lineno, columnno, type)

        self.left_expr = left_expr
        self.right_expr = right_expr


class CoolAtomNode(CoolExprNode):
    def __init__(self, lineno, columnno, value, type):
        super().__init__(lineno, columnno, type)

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
