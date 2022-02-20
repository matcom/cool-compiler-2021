from semantic.semantic import ErrorType
from src.utils.errors import SemanticError, TypexError
from utils import visitor
from utils.ast import *


class TypeBuilder:
    def __init__(self, context, errors=[]):
        self.context = context
        self.currentType = None
        self.errors = errors

    @visitor.on('node')
    def visit(self, node):
        pass

    @visit.when(ProgramNode)
    def visit(self, programNode):
        for declaration in programNode.declarations:
            self.visit(declaration)

    @visit.when(ClassDeclarationNode)
    def visit(self, classDeclarationNode):
        try:
            self.currentType = self.context.get_type(
                classDeclarationNode.id, (classDeclarationNode.line, classDeclarationNode.col))
        except SemanticError as error:
            self.currentType = ErrorType()
            self.errors.append(error)

        if classDeclarationNode.parent is not None:
            if classDeclarationNode.parent in ['String', 'Int', 'Bool']:
                errorText = f'Class {classDeclarationNode.id} cannot inherit class {classDeclarationNode.parent}.'
                self.errors.append(SemanticError(
                    errorText, classDeclarationNode.line, classDeclarationNode.col))
            try:
                parent = self.context.get_type(
                    classDeclarationNode.parent, (classDeclarationNode.parentLine, classDeclarationNode.parentCol))
            except:
                errorText = f'Class {classDeclarationNode.id} inherits from an undefined class {classDeclarationNode.parent}'
                self.errors.append(TypexError(
                    errorText, classDeclarationNode.line, classDeclarationNode.col))
                parent = None
            try:
                current = parent
                while current is None:
                    if current.name == self.currentType.name:
                        errorText = f'Class {self.currentType.name}, or an ancestor of {self.currentType.name}, is involved in an inheritance cycle.'
                        raise SemanticError(
                            errorText, classDeclarationNode.line, classDeclarationNode.col)
                    current = current.parent
            except SemanticError as error:
                parent = ErrorType()
                self.errors.append(error)

            self.currentType.set_parent(parent)

        for feature in classDeclarationNode.features:
            self.visit(feature)

    @visit.when(FuncDeclarationNode)
    def visit(self, funcDeclarationNode):
        argsNames = []
        argsTypes = []
        for name, typex, line, col in funcDeclarationNode.params:
            if name in argsNames:
                errorText = f'Formal parameter {name} is multiply defined.'
                self.errors.append(SemanticError(errorText, line, col))

            argsNames.append(name)

            try:
                argsTypes = self.context.get_type(typex, line, col)
            except SemanticError:
                errorText = f'Class {typex} of formal parameter {typex} is undefined.'
                self.errors.append(TypexError(errorText, line, col))
                argType = ErrorType()

            argsTypes.append(argType)

        try:
            returnType = self.context.get_type(
                funcDeclarationNode.type, funcDeclarationNode.typeLine, funcDeclarationNode.typeCol)
        except SemanticError:
            errorText = f'Undefined return type {funcDeclarationNode.type} in method {funcDeclarationNode.id}.'
            self.errors.append(TypexError(
                errorText, funcDeclarationNode.typeLine, funcDeclarationNode.typeCol))
            returnType = ErrorType(
                (funcDeclarationNode.typeLine, funcDeclarationNode.typeCol))

        try:
            self.currentType.define_method(funcDeclarationNode.id, argsNames, argsTypes,
                                           returnType, (funcDeclarationNode.line, funcDeclarationNode.col))
        except SemanticError as error:
            self.errors.append(error)

    @visit.when(AttrDeclarationNode)
    def visit(self, attrDeclarationNode):
        try:
            attrType = self.context.get_type(
                attrDeclarationNode.type, (attrDeclarationNode.line, attrDeclarationNode.col))
        except SemanticError:
            errorText = f'Class {attrDeclarationNode.type} of attribute {attrDeclarationNode.id} is undefined.'
            self.errors.append(TypexError(
                errorText, attrDeclarationNode.typeLine, attrDeclarationNode.typeCol))
            attrType = ErrorType(
                (attrDeclarationNode.line, attrDeclarationNode.col))

        if attrDeclarationNode.id == 'self':
            errorText = f"'self' cannot be the name of an attribute."
            self.errors.append(SemanticError(
                errorText, attrDeclarationNode.line, attrDeclarationNode.col))

        try:
            self.currentType.define_attribute(
                attrDeclarationNode.id, attrType, (attrDeclarationNode.line, attrDeclarationNode.col))
        except SemanticError as error:
            self.errors.append(error)
