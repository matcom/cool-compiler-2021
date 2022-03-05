from typing import List


class CoolAstNode:
    def __init__(self, lineno, columnno):
        self.lineno = lineno
        self.columnno = columnno


class CoolClassNode(CoolAstNode):
    def __init__(self, lineno, columnno, id, features, parent=None):
        super().__init__(lineno, columnno)

        self.id = id
        self.parent = parent
        self.features: List[CoolFeatureNode] = features

    @staticmethod
    def parse(p):
        name, parent, features = p.TYPE_ID0, p.TYPE_ID1, p.feature
        return CoolClassNode(p.lineno, 0, name, features, parent=parent)


class CoolProgramNode(CoolAstNode):
    def __init__(self, lineno, columnno, classes: List[CoolClassNode]):
        super().__init__(lineno, columnno)
        self.classes: List[CoolClassNode] = classes

    @staticmethod
    def parse(p):
        classes = [p.cool_class0] + p.cool_class1
        return CoolProgramNode(p.lineno, 0, classes)


class CoolFeatureNode(CoolAstNode):
    pass


class CoolAttrDeclNode(CoolFeatureNode):
    def __init__(self, lineno, columnno, id, type, body=None):
        super().__init__(lineno, columnno)

        self.id = id
        self.type = type
        self.body = body

    @staticmethod
    def parse(p):
        id, type, expr = p.OBJECT_ID, p.TYPE_ID, p.expr
        return CoolAttrDeclNode(p.lineno, 0, id, type, expr)


class CoolMethodDeclNode(CoolFeatureNode):
    def __init__(self, lineno, columnno, id, param_names, type, body):
        super().__init__(lineno, columnno)

        self.id = id
        self.param_names = param_names
        self.type = type
        self.body = body

    @staticmethod
    def parse(p):
        return CoolMethodDeclNode(p.lineno, 0, p.OBJECT_ID, p.formal_list if p.formal_list is not None else ([], []),  p.TYPE_ID, p.expr)


class CoolExprNode(CoolAstNode):
    pass


class CoolAssignNode(CoolExprNode):
    def __init__(self, lineno, columnno, id, expr):
        super().__init__(lineno, columnno)
        self.id = id
        self.expr = expr

    @staticmethod
    def parse(p):
        return CoolAssignNode(p.lineno, 0, p.OBJECT_ID, p.expr)


class CoolStaticDispatchNode(CoolExprNode):
    def __init__(self, lineno, columnno, expr, static_type, id, args):
        super().__init__(lineno, columnno)

        self.expr = expr
        self.static_type = static_type
        self.id = id
        self.args = args

    @staticmethod
    def parse(p):
        return CoolStaticDispatchNode(p.lineno, 0, p.expr, p.TYPE_ID, p.OBJECT_ID, p.arg_list if p.arg_list is not None else [])


class CoolDispatchNode(CoolExprNode):
    def __init__(self, lineno, columnno, id, args, expr=None):
        super().__init__(lineno, columnno)
        self.expr = expr
        self.id = id
        self.args = args

    @staticmethod
    def parse(p, expr):
        return CoolDispatchNode(p.lineno, 0,  p.OBJECT_ID, p.arg_list if p.arg_list is not None else [], expr)


class CoolIfThenElseNode(CoolExprNode):
    def __init__(self, lineno, columnno, cond, then_expr, else_expr):
        super().__init__(lineno, columnno)
        self.cond = cond
        self.then_expr = then_expr
        self.else_expr = else_expr

    @staticmethod
    def parse(p):
        return CoolIfThenElseNode(p.lineno, 0, p.expr0, p.expr1, p.expr2)


class CoolWhileNode(CoolExprNode):
    def __init__(self, lineno, columnno, cond, body):
        super().__init__(lineno, columnno)
        self.cond = cond
        self.body = body

    @staticmethod
    def parse(p):
        return CoolWhileNode(p.lineno, 0, p.expr0, p.expr1)


class CoolBlockNode(CoolExprNode):
    def __init__(self, lineno, columnno, expr_list):
        super().__init__(lineno, columnno)
        self.expr_list = expr_list

    @staticmethod
    def parse(p):
        return CoolBlockNode(p.lineno, 0, [p.expr0, *p.expr1])


class CoolLetInNode(CoolExprNode):
    def __init__(self, lineno, columnno, decl_list, expr):
        super().__init__(lineno, columnno)
        self.decl_list: List[CoolLetDeclNode] = decl_list
        self.expr = expr

    @staticmethod
    def parse(p):
        return CoolLetInNode(p.lineno, 0, [p.let_decl0, *p.let_decl1], p.expr)


class CoolLetDeclNode(CoolAstNode):
    def __init__(self, lineno, columnno, id, type, expr=None):
        super().__init__(lineno, columnno)
        self.id = id
        self.type = type
        self.expr = expr

    @staticmethod
    def parse(p):
        return CoolLetDeclNode(p.lineno, 0, p.OBJECT_ID,  p.TYPE_ID, expr=p.expr)


class CoolCaseNode(CoolExprNode):
    def __init__(self, lineno, columnno, expr, case_branches):
        super().__init__(lineno, columnno)
        self.expr = expr
        self.case_branches = case_branches

    @staticmethod
    def parse(p):
        return CoolCaseNode(p.lineno, 0, p.expr, [p.case0, * p.case1])


class CoolCaseBranchNode(CoolAstNode):
    def __init__(self, lineno, columnno, id, type, expr):
        super().__init__(lineno, columnno)

        self.id = id
        self.type = type
        self.expr = expr

    @staticmethod
    def parse(p):
        id, type, expr = p.OBJECT_ID, p.TYPE_ID, p.expr
        return CoolCaseBranchNode(p.lineno, 0, id, type, expr)


class CoolNewNode(CoolExprNode):
    def __init__(self, lineno, columnno, type):
        super().__init__(lineno, columnno)
        # self.lineno = lineno
        # self.columnno = columnno

        self.type = type

    @staticmethod
    def parse(p):
        type = p.TYPE_ID
        return CoolNewNode(p.lineno, 0, type)


class CoolParenthNode(CoolExprNode):
    def __init__(self, lineno, columnno, expr):
        super().__init__(lineno, columnno)
        # self.lineno = lineno
        # self.columnno = columnno

        self.expr = expr

    @staticmethod
    def parse(p):
        expr = p.expr
        return CoolParenthNode(p.lineno, 0, expr)


class CoolUnaryExprNode(CoolExprNode):
    def __init__(self, lineno, columnno, expr):
        super().__init__(lineno, columnno)
        # self.lineno = lineno
        # self.columnno = columnno

        self.expr = expr


class CoolIsVoidNode(CoolUnaryExprNode):
    @staticmethod
    def parse(p):
        expr = p.expr
        return CoolIsVoidNode(p.lineno, 0, expr)


class CoolNotNode(CoolUnaryExprNode):
    @staticmethod
    def parse(p):
        expr = p.expr
        return CoolNotNode(p.lineno, 0, expr)


class CoolTildeNode(CoolUnaryExprNode):
    @staticmethod
    def parse(p):
        expr = p.expr
        return CoolTildeNode(p.lineno, 0, expr)


class CoolBinaryExprNode(CoolExprNode):
    def __init__(self, lineno, columnno, left_expr, right_expr):
        super().__init__(lineno, columnno)

        self.left_expr = left_expr
        self.right_expr = right_expr


class CoolComparisonNode(CoolBinaryExprNode):
    pass


class CoolLeqNode(CoolComparisonNode):
    @staticmethod
    def parse(p):
        # print(p._slice[0])
        left_expr, right_expr = p.expr0, p.expr1
        return CoolLeqNode(p.lineno, p[0].columnno, left_expr, right_expr)


class CoolEqNode(CoolComparisonNode):
    @staticmethod
    def parse(p):
        # print(p._slice[0])
        left_expr, right_expr = p.expr0, p.expr1
        return CoolEqNode(p.lineno, p[0].columnno, left_expr, right_expr)


class CoolLeNode(CoolComparisonNode):
    @staticmethod
    def parse(p):
        # print(p._slice[0])
        left_expr, right_expr = p.expr0, p.expr1
        return CoolLeNode(p.lineno, p[0].columnno, left_expr, right_expr)


class CoolArithmeticNode(CoolBinaryExprNode):
    pass


class CoolPlusNode(CoolArithmeticNode):
    @staticmethod
    def parse(p):
        left_expr, right_expr = p.expr0, p.expr1
        return CoolPlusNode(p.lineno, p[0].columnno, left_expr, right_expr)


class CoolMinusNode(CoolArithmeticNode):
    @staticmethod
    def parse(p):
        # print(p._slice[0])
        left_expr, right_expr = p.expr0, p.expr1
        return CoolMinusNode(p.lineno, p[0].columnno, left_expr, right_expr)


class CoolMultNode(CoolArithmeticNode):
    @staticmethod
    def parse(p):
        # print(p._slice[0])
        left_expr, right_expr = p.expr0, p.expr1
        return CoolMinusNode(p.lineno, p[0].columnno, left_expr, right_expr)


class CoolDivNode(CoolArithmeticNode):
    @staticmethod
    def parse(p):
        # print(p._slice[0])
        left_expr, right_expr = p.expr0, p.expr1
        return CoolMinusNode(p.lineno, p[0].columnno, left_expr, right_expr)


class CoolAtomNode(CoolExprNode):
    def __init__(self, lineno, columnno, value):
        super().__init__(lineno, columnno)

        self.value = value


class CoolIntNode(CoolAtomNode):
    @staticmethod
    def parse(p):
        value = p.INT
        return CoolIntNode(p.lineno, p._slice[0].columnno, value)


class CoolStringNode(CoolAtomNode):
    @staticmethod
    def parse(p):
        value = p.QUOTE
        return CoolStringNode(p.lineno, p._slice[0].columnno, value)


class CoolBoolNode(CoolAtomNode):
    @staticmethod
    def parse(p, value):
        return CoolBoolNode(p.lineno, p._slice[0].columnno, value)


class CoolVarNode(CoolAtomNode):
    @staticmethod
    def parse(p):
        return CoolVarNode(p.lineno, p._slice[0].columnno, p.OBJECT_ID)
