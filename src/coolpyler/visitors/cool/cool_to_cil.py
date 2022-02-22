import coolpyler.ast.cil.base as cil
import coolpyler.ast.cool.type_checked as type_checked
import coolpyler.utils.visitor as visitor


class CoolToCilVisitor(object):
    def __init__(self, errors=None):
        if errors is None:
            errors = []
        self.errors = errors

        self.dottypes = []
        self.dotdata = []
        self.dotcode = []

    @visitor.on("node")
    def visit(self, node):  # type: ignore
        pass

    @visitor.when(type_checked.CoolProgramNode)
    def visit(self, node: type_checked.CoolProgramNode):  # type: ignore

        for cool_class in node.classes:
            self.visit(cool_class)

        return cil.ProgramNode(self.dottypes, self.dotdata, self.dotcode)

    @visitor.when(type_checked.CoolClassNode)
    def visit(self, node: type_checked.CoolClassNode):  # type: ignore
        methods = node.type.all_methods()
        attributes = node.type.all_attributes()
        dottype = cil.TypeNode(node.type, attributes, methods)
        self.dottypes.append(dottype)

        for feat in node.features:
            self.visit(feat)

    @visitor.when(type_checked.CoolAttrDeclNode)
    def visit(self, node: type_checked.CoolAttrDeclNode):  # type: ignore
        pass

    @visitor.when(type_checked.CoolMethodDeclNode)
    def visit(self, node: type_checked.CoolMethodDeclNode):  # type: ignore
        pass

    @visitor.when(type_checked.CoolAssignNode)
    def visit(self, node: type_checked.CoolAssignNode):  # type: ignore
        pass

    @visitor.when(type_checked.CoolStaticDispatchNode)
    def visit(self, node: type_checked.CoolStaticDispatchNode):  # type: ignore
        pass

    @visitor.when(type_checked.CoolDispatchNode)
    def visit(self, node: type_checked.CoolDispatchNode):  # type: ignore
        pass

    @visitor.when(type_checked.CoolIfThenElseNode)
    def visit(self, node: type_checked.CoolIfThenElseNode):  # type: ignore
        pass

    @visitor.when(type_checked.CoolWhileNode)
    def visit(self, node: type_checked.CoolWhileNode):  # type: ignore
        pass

    @visitor.when(type_checked.CoolBlockNode)
    def visit(self, node: type_checked.CoolBlockNode):  # type: ignore
        pass

    @visitor.when(type_checked.CoolLetInNode)
    def visit(self, node: type_checked.CoolLetInNode):  # type: ignore
        pass

    @visitor.when(type_checked.CoolLetDeclNode)
    def visit(self, node: type_checked.CoolLetDeclNode):  # type: ignore
        pass

    @visitor.when(type_checked.CoolCaseNode)
    def visit(self, node: type_checked.CoolCaseNode):  # type: ignore
        pass

    @visitor.when(type_checked.CoolCaseBranchNode)
    def visit(self, node: type_checked.CoolCaseBranchNode):  # type: ignore
        pass

    @visitor.when(type_checked.CoolNewNode)
    def visit(self, node: type_checked.CoolNewNode):  # type: ignore
        pass

    @visitor.when(type_checked.CoolParenthNode)
    def visit(self, node: type_checked.CoolParenthNode):  # type: ignore
        pass

    @visitor.when(type_checked.CoolTildeNode)
    def visit(self, node: type_checked.CoolTildeNode):  # type: ignore
        pass

    @visitor.when(type_checked.CoolNotNode)
    def visit(self, node: type_checked.CoolNotNode):  # type: ignore
        pass

    @visitor.when(type_checked.CoolIsVoidNode)
    def visit(self, node: type_checked.CoolIsVoidNode):  # type: ignore
        pass

    @visitor.when(type_checked.CoolLeqNode)
    def visit(self, node: type_checked.CoolLeqNode):  # type: ignore
        pass

    @visitor.when(type_checked.CoolEqNode)
    def visit(self, node: type_checked.CoolEqNode):  # type: ignore
        pass

    @visitor.when(type_checked.CoolLeNode)
    def visit(self, node: type_checked.CoolLeNode):  # type: ignore
        pass

    @visitor.when(type_checked.CoolPlusNode)
    def visit(self, node: type_checked.CoolPlusNode):  # type: ignore
        pass

    @visitor.when(type_checked.CoolMinusNode)
    def visit(self, node: type_checked.CoolMinusNode):  # type: ignore
        pass

    @visitor.when(type_checked.CoolMultNode)
    def visit(self, node: type_checked.CoolMultNode):  # type: ignore
        pass

    @visitor.when(type_checked.CoolDivNode)
    def visit(self, node: type_checked.CoolDivNode):  # type: ignore
        pass

    @visitor.when(type_checked.CoolIntNode)
    def visit(self, node: type_checked.CoolIntNode):  # type: ignore
        pass

    @visitor.when(type_checked.CoolBoolNode)
    def visit(self, node: type_checked.CoolBoolNode):  # type: ignore
        pass

    @visitor.when(type_checked.CoolStringNode)
    def visit(self, node: type_checked.CoolStringNode):  # type: ignore
        pass

    @visitor.when(type_checked.CoolVarNode)
    def visit(self, node: type_checked.CoolVarNode):  # type: ignore
        pass
