import coolpyler.ast.cool.base as base
import coolpyler.ast.cool.parsed as parsed


class CoolAstNode(parsed.CoolAstNode):
    pass


class CoolProgramNode(base.CoolProgramNode):
    def __init__(self, lineno, columnno, classes, types):
        super().__init__(lineno, columnno)

        self.classes = classes
        self.types = types


class CoolClassNode(base.CoolClassNode):
    def __init__(self, lineno, columnno, _type, features, parent=None):
        super().__init__(lineno, columnno)

        self.type = _type
        self.parent = parent
        self.features = features


class CoolExprNode(parsed.CoolExprNode):
    pass


class CoolFeatureNode(parsed.CoolFeatureNode):
    pass


class CoolAttrDeclNode(parsed.CoolAttrDeclNode):
    pass


class CoolMethodDeclNode(parsed.CoolMethodDeclNode):
    pass


class CoolAssignNode(parsed.CoolAssignNode):
    pass


class CoolStaticDispatchNode(parsed.CoolStaticDispatchNode):
    pass


class CoolDispatchNode(parsed.CoolDispatchNode):
    pass


class CoolIfThenElseNode(parsed.CoolIfThenElseNode):
    pass


class CoolWhileNode(parsed.CoolWhileNode):
    pass


class CoolBlockNode(parsed.CoolBlockNode):
    pass


class CoolLetInNode(parsed.CoolLetInNode):
    pass


class CoolLetDeclNode(parsed.CoolLetDeclNode):
    pass


class CoolCaseNode(parsed.CoolCaseNode):
    pass


class CoolCaseBranchNode(parsed.CoolCaseBranchNode):
    pass


class CoolNewNode(parsed.CoolNewNode):
    pass


class CoolParenthNode(parsed.CoolParenthNode):
    pass


class CoolUnaryExprNode(parsed.CoolUnaryExprNode):
    pass


class CoolIsVoidNode(parsed.CoolIsVoidNode):
    pass


class CoolNotNode(parsed.CoolNotNode):
    pass


class CoolTildeNode(parsed.CoolTildeNode):
    pass


class CoolBinaryExprNode(parsed.CoolBinaryExprNode):
    pass


class CoolComparisonNode(parsed.CoolComparisonNode):
    pass


class CoolLeqNode(parsed.CoolLeqNode):
    pass


class CoolEqNode(parsed.CoolEqNode):
    pass


class CoolLeNode(parsed.CoolLeNode):
    pass


class CoolArithmeticNode(parsed.CoolArithmeticNode):
    pass


class CoolPlusNode(parsed.CoolPlusNode):
    pass


class CoolMinusNode(parsed.CoolMinusNode):
    pass


class CoolMultNode(parsed.CoolMultNode):
    pass


class CoolDivNode(parsed.CoolDivNode):
    pass


class CoolAtomNode(parsed.CoolAtomNode):
    pass


class CoolIntNode(parsed.CoolIntNode):
    pass


class CoolStringNode(parsed.CoolStringNode):
    pass


class CoolBoolNode(parsed.CoolBoolNode):
    pass


class CoolVarNode(parsed.CoolVarNode):
    pass


