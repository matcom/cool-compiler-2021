import imp
from src.utils import visitor
from src.utils.ast import ArrobaCallNode, AssignNode, AttrDeclarationNode, BlockNode, CaseNode, ClassDeclarationNode, DotCallNode, FuncDeclarationNode, IdNode, IfThenElseNode, IntNode, IsVoidNode, LetInNode, MemberCallNode, ProgramNode, VarDeclarationNode, WhileNode
from src.semantic.semantic import ErrorType, IntType, Scope, define_default_value
from src.utils.errors import NamexError, SemanticError, TypexError


class VarCollector:
    def __init__(self, context, errors):
        self.context = context
        self.errors = errors
        self.currentType = None
        self.currentMethod = None
        self.currentIndex = None

    @visitor.on('node')
    def visit(self, node, scope):
        pass

    @visitor.when(ProgramNode)
    def visit(self, programNode, scope):
        scope = Scope()
        for declaration in programNode.declarations:
            self.visit(declaration, scope.create_child())
        return scope

    @visitor.when(ClassDeclarationNode)
    def visit(self, classDeclarationNode, scope):
        self.currentType = self._get_type(
            classDeclarationNode.id, (classDeclarationNode.line, classDeclarationNode.col))
        scope.define_variable('self', self.currentType)

        for feature in classDeclarationNode.features:
            if isinstance(feature, AttrDeclarationNode):
                self.visit(feature, scope)

        for attr, _ in self.currentType.all_attributes():
            if scope.find_attribute(attr.name) is None:
                scope.define_attribute(attr)

        for feature in classDeclarationNode.features:
            if isinstance(feature, FuncDeclarationNode):
                self.visit(feature, scope)

    @visitor.when(AttrDeclarationNode)
    def visit(self, attrDeclarationNode, scope):
        attr = self.currentType.get_attribute(
            attrDeclarationNode.id, (attrDeclarationNode.line, attrDeclarationNode.col))
        if attrDeclarationNode.expr is None:
            define_default_value(attr.type, attrDeclarationNode)
        else:
            self.visit(attrDeclarationNode.expr, scope)
        attr.expr = attrDeclarationNode.expr
        scope.define_attribute(attr)

    @visitor.when(FuncDeclarationNode)
    def visit(self, funcDeclarationNode, scope):
        parent = self.currentType.parent
        pnames = [param[0] for param in funcDeclarationNode.params]
        ptypes = [param[1] for param in funcDeclarationNode.params]

        self.currentMethod = self.currentType.get_method(
            funcDeclarationNode.id, (funcDeclarationNode.line, funcDeclarationNode.col))

        newScope = scope.create_child()
        scope.functions[funcDeclarationNode.id] = newScope

        for pname, ptype, pline, pcol in funcDeclarationNode.params:
            if pname == 'self':
                errorText = "'self' cannot be the name of a formal parameter."
                self.errors.append(SemanticError(errorText, pline, pcol))
            newScope.define_variable(
                pname, self._get_type(ptype, (pline, pcol)))

        self.visit(funcDeclarationNode.body, newScope)

    def _get_type(self, ntype, pos):
        try:
            return self.context.get_type(ntype, pos)
        except SemanticError as e:
            self.errors.append(e)
            return ErrorType()

    @visitor.when(VarDeclarationNode)
    def visit(self, varDeclarationNode, scope):
        if varDeclarationNode.id == 'self':
            errorText = '\'self\' cannot be bound in a \'let\' expression.'
            self.errors.append(SemanticError(
                errorText, varDeclarationNode.line, varDeclarationNode.col))
            return

        try:
            vType = self.context.get_type(
                varDeclarationNode.type, varDeclarationNode.line, varDeclarationNode.col)
        except:
            errorText = f'Class {varDeclarationNode.type} of let-bound identifier {varDeclarationNode.id} is undefined.'
            self.errors.append(TypexError(
                errorText, varDeclarationNode.typeLine, varDeclarationNode.typeCol))
            vType = ErrorType()

        vType = self._get_type(
            varDeclarationNode.type, (varDeclarationNode.typeLine, varDeclarationNode.typeCol))
        varInfo = scope.define_variable(varDeclarationNode.id, vType)

        if varDeclarationNode.expr is not None:
            self.visit(varDeclarationNode.expr, scope)
        else:
            define_default_value(vType, varDeclarationNode)

    @visitor.when(AssignNode)
    def visit(self, assignNode, scope):
        if assignNode.id == 'self':
            errorText = 'Cannot assign to \'self\'.'
            self.errors.append(SemanticError(
                errorText, assignNode.line, assignNode.col))
            return

        vInfo = scope.find_variable(assignNode.id)
        if vInfo is None:
            varInfo = scope.find_attribute(assignNode.id)
            if varInfo is None:
                errorText = f'Undeclared identifier {assignNode.id}.'
                self.errors.append(NamexError(
                    errorText, assignNode.line, assignNode.col))
                vType = ErrorType()
                scope.define_variable(assignNode.id, vType)

        self.visit(assignNode.expr, scope)

    @visitor.when(BlockNode)
    def visit(self, blockNode, scope):
        for expr in blockNode.exprs:
            self.visit(expr, scope)

    @visitor.when(LetInNode)
    def visit(self, letInNode, scope):
        newScope = scope.create_child()
        scope.expr_dict[letInNode] = newScope
        for letDeclaration in letInNode.letBody:
            self.visit(letDeclaration, newScope)

        self.visit(letInNode.inBody, newScope)

    @visitor.when(IdNode)
    def visit(self, idNode, scope):
        try:
            return self.currentType.get_attribute(idNode.id, (idNode.line, idNode.col)).type
        except:
            if not scope.is_defined(idNode.id):
                errorText = f'Undeclared identifier {idNode.id}.'
                self.errors.append(NamexError(
                    errorText, idNode.line, idNode.col))
                vInfo = scope.define_variable(
                    idNode.id, ErrorType((idNode.line, idNode.col)))
            else:
                vInfo = scope.find_variable(idNode.id)

            return vInfo.type

    @visitor.when(WhileNode)
    def visit(self, whileNode, scope):
        self.visit(whileNode.condition, scope)
        self.visit(whileNode.body, scope)

    @visitor.when(IfThenElseNode)
    def visit(self, ifThenElseNode, scope):
        self.visit(ifThenElseNode.condition, scope)
        self.visit(ifThenElseNode.ifBody, scope)
        self.visit(ifThenElseNode.elseBody, scope)

    @visitor.when(IsVoidNode)
    def visit(self, isVoidNode, scope):
        self.visit(isVoidNode.expr, scope)

    @visitor.when(ArrobaCallNode)
    def visit(self, arrobaCallNode, scope):
        self.visit(arrobaCallNode.obj, scope)
        for arg in arrobaCallNode.args:
            self.visit(arg)

    @visitor.when(DotCallNode)
    def visit(self, dotCallNode, scope):
        self.visit(dotCallNode.obj, scope)
        for arg in dotCallNode.args:
            self.visit(arg)

    @visitor.when(MemberCallNode)
    def visit(self, memberCallNode, scope):
        for arg in memberCallNode.args:
            self.visit(arg)


    @visitor.when(CaseNode)
    def visit(self, caseNode, scope):
        self.visit(caseNode.expr, scope)
        newScope = scope.create_child()
        scope.expr_dict[caseNode] = newScope

        for 

