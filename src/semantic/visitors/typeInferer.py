import imp
from src.utils import visitor
from src.utils.ast import AttrDeclarationNode, ClassDeclarationNode, FuncDeclarationNode, IntNode, ProgramNode
from src.semantic.semantic import IntType, Scope, define_default_value
from src.utils.errors import SemanticError


class TypeInferer:
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

        self.currentMethod = self.currentType.get_method(funcDeclarationNode.id, (funcDeclarationNode.line, funcDeclarationNode.col))

        newScope = scope.create_child()
        scope.functions[funcDeclarationNode.id] = newScope

        for pname, ptype, pline, pcol in funcDeclarationNode.params:
            if pname == 'self':
                errorText = "'self' cannot be the name of a formal parameter."
                self.errors.append(SemanticError(errorText, pline, pcol))
            newScope.define_variable(pname, self._get_type(ptype, (pline,pcol)))
        
        self.visit(funcDeclarationNode.body, newScope)

