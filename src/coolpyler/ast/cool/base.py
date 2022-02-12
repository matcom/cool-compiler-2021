class CoolAstNode:
    def __init__(self, lineno, columnno):
        self.lineno = lineno
        self.columnno = columnno


class CoolProgramNode(CoolAstNode):
    pass


class CoolClassNode(CoolAstNode):
    pass


class CoolFeatureNode(CoolAstNode):
    pass


class CoolAttrDeclNode(CoolFeatureNode):
    pass


class CoolMethodDeclNode(CoolFeatureNode):
    pass


class CoolExprNode(CoolAstNode):
    pass


class CoolAssignNode(CoolExprNode):
    pass


class CoolStaticDispatchNode(CoolExprNode):
    pass


class CoolDispatchNode(CoolExprNode):
    pass


class CoolIfThenElseNode(CoolExprNode):
    pass


class CoolWhileNode(CoolExprNode):
    pass


class CoolBlockNode(CoolExprNode):
    pass


class CoolLetInNode(CoolExprNode):
    pass


class CoolLetDeclNode(CoolAstNode):
    pass

class CoolCaseNode(CoolExprNode):
    pass


class CoolCaseBranchNode(CoolAstNode):
    pass


class CoolNewNode(CoolExprNode):
    pass


class CoolParenthNode(CoolExprNode):
    pass


class CoolUnaryExprNode(CoolExprNode):
    pass


class CoolIsVoidNode(CoolUnaryExprNode):
    pass


class CoolNotNode(CoolUnaryExprNode):
    pass


class CoolTildeNode(CoolUnaryExprNode):
    pass


class CoolBinaryExprNode(CoolExprNode):
    pass


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
    pass


class CoolIntNode(CoolAtomNode):
    pass


class CoolStringNode(CoolAtomNode):
    pass


class CoolBoolNode(CoolAtomNode):
    pass


class CoolVarNode(CoolAtomNode):
    pass
