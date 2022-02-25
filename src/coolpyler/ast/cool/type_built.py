import coolpyler.ast.cool.base as base
import coolpyler.ast.cool.type_collected as type_collected


class CoolAstNode(type_collected.CoolAstNode):
    pass


# class CoolProgramNode(base.CoolProgramNode):
#     def __init__(self, lineno, columnno, classes):
#         super().__init__(lineno, columnno)
#         self.classes = classes


# class CoolClassNode(base.CoolClassNode):
#     def __init__(self, lineno, columnno, type, features):
#         super().__init__(lineno, columnno)

#         self.type = type
#         self.features = features


class CoolProgramNode(type_collected.CoolProgramNode):
    pass


class CoolClassNode(type_collected.CoolClassNode):
    pass


class CoolFeatureNode(type_collected.CoolFeatureNode):
    pass


class CoolAttrDeclNode(base.CoolAttrDeclNode):
    def __init__(self, lineno, columnno, attr_info, body=None):
        super().__init__(lineno, columnno)

        self.attr_info = attr_info
        self.body = body


class CoolMethodDeclNode(base.CoolMethodDeclNode):
    def __init__(self, lineno, columnno, method_info, body):
        super().__init__(lineno, columnno)

        self.method_info = method_info
        self.body = body


class CoolExprNode(type_collected.CoolExprNode):
    pass


class CoolAssignNode(type_collected.CoolAssignNode):
    pass


class CoolStaticDispatchNode(type_collected.CoolStaticDispatchNode):
    pass


class CoolDispatchNode(type_collected.CoolDispatchNode):
    pass


class CoolIfThenElseNode(type_collected.CoolIfThenElseNode):
    pass


class CoolWhileNode(type_collected.CoolWhileNode):
    pass


class CoolBlockNode(type_collected.CoolBlockNode):
    pass


class CoolLetInNode(type_collected.CoolLetInNode):
    pass


class CoolLetDeclNode(type_collected.CoolLetDeclNode):
    pass


class CoolCaseNode(type_collected.CoolCaseNode):
    pass


class CoolCaseBranchNode(type_collected.CoolCaseBranchNode):
    pass


class CoolNewNode(type_collected.CoolNewNode):
    pass


class CoolParenthNode(type_collected.CoolParenthNode):
    pass


class CoolUnaryExprNode(type_collected.CoolUnaryExprNode):
    pass


class CoolIsVoidNode(type_collected.CoolIsVoidNode):
    pass


class CoolNotNode(type_collected.CoolNotNode):
    pass


class CoolTildeNode(type_collected.CoolTildeNode):
    pass


class CoolBinaryExprNode(type_collected.CoolBinaryExprNode):
    pass


class CoolComparisonNode(type_collected.CoolComparisonNode):
    pass


class CoolLeqNode(type_collected.CoolLeqNode):
    pass


class CoolEqNode(type_collected.CoolEqNode):
    pass


class CoolLeNode(type_collected.CoolLeNode):
    pass


class CoolArithmeticNode(type_collected.CoolArithmeticNode):
    pass


class CoolPlusNode(type_collected.CoolPlusNode):
    pass


class CoolMinusNode(type_collected.CoolMinusNode):
    pass


class CoolMultNode(type_collected.CoolMultNode):
    pass


class CoolDivNode(type_collected.CoolDivNode):
    pass


class CoolAtomNode(type_collected.CoolAtomNode):
    pass


class CoolIntNode(type_collected.CoolIntNode):
    pass


class CoolStringNode(type_collected.CoolStringNode):
    pass


class CoolBoolNode(type_collected.CoolBoolNode):
    pass


class CoolVarNode(type_collected.CoolVarNode):
    pass
