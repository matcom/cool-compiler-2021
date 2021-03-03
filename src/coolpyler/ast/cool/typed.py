class CoolAstNode:
    pass


class CoolProgramNode(CoolAstNode):
    def __init__(self, classes):
        self.classes = classes


class CoolClassNode(CoolAstNode):
    def __init__(self, type, parent_type, features):
        self.type = type
        self.parent_type = parent_type
        self.features = features


class CoolFeatureNode(CoolAstNode):
    pass


class CoolAttrDeclNode(CoolFeatureNode):
    def __init__(self, id, type, body=None):
        self.id = id
        self.type = type
        self.body = body


class CoolFuncDeclNode(CoolFeatureNode):
    def __init__(self, id, params, type, body):
        self.id = id
        self.params = params
        self.type = type
        self.body = body


class CoolFormalNode(CoolAstNode):
    def __init__(self, id, type):
        self.id = id
        self.type = type


class CoolExprNode(CoolAstNode):
    pass


class CoolAssignNode(CoolExprNode):
    def __init__(self, id, expr):
        self.id = id
        self.expr = expr


class CoolStaticDispatchNode(CoolExprNode):
    def __init__(self, expr, type, id, args):
        self.expr = expr
        self.type = type
        self.id = id
        self.args = args


class CoolDispatchNode(CoolExprNode):
    def __init__(self, id, args, expr=None):
        self.id = id
        self.args = args
        if expr is None:
            expr = CoolVarNode("self")
        self.expr = expr


class CoolIfThenElseNode(CoolExprNode):
    def __init__(self, cond, then_expr, else_expr):
        self.cond = cond
        self.then_expr = then_expr
        self.else_expr = else_expr


class CoolWhileNode(CoolExprNode):
    def __init__(self, cond, body):
        self.cond = cond
        self.body = body


class CoolBlockNode(CoolExprNode):
    def __init__(self, expr_list):
        self.expr_list = expr_list


class CoolLetInNode(CoolExprNode):
    def __init__(self, decl_list, expr):
        self.decl_list = decl_list
        self.expr = expr


class CoolLetDeclNode(CoolAstNode):
    def __init__(self, id, type, expr=None):
        self.id = id
        self.type = type
        self.expr = expr


class CoolCaseOfNode(CoolExprNode):
    def __init__(self, expr, case_list):
        self.expr = expr
        self.case_list = case_list


class CoolCaseNode(CoolAstNode):
    def __init__(self, id, type, expr):
        self.id = id
        self.type = type
        self.expr = expr


class CoolNewNode(CoolExprNode):
    def __init__(self, type):
        self.type = type


class CoolParenthNode(CoolExprNode):
    def __init__(self, expr):
        self.expr = expr


class CoolUnaryExprNode(CoolExprNode):
    def __init__(self, expr):
        self.expr = expr


class CoolIsVoidNode(CoolUnaryExprNode):
    pass


class CoolNotNode(CoolUnaryExprNode):
    pass


class CoolTildeNode(CoolUnaryExprNode):
    pass


class CoolBinaryExprNode(CoolExprNode):
    def __init__(self, left_expr, right_expr):
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
    def __init__(self, value):
        self.value = value


class CoolIntNode(CoolAtomNode):
    pass


class CoolStringNode(CoolAtomNode):
    pass


class CoolBoolNode(CoolAtomNode):
    pass


class CoolVarNode(CoolAtomNode):
    pass
