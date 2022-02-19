
from semantic.semantic import ErrorType
from src.utils.errors import SemanticError
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
                classDeclarationNode.name, (classDeclarationNode.line, classDeclarationNode.column))
        except Exception as error:
            self.currentType = ErrorType
            self.errors.append(error)

        if classDeclarationNode.parent is not None:
            if classDeclarationNode.parent in ['String', 'Int', 'Bool']:
                errorText = f'Class {classDeclarationNode.name} cannot inherit class {classDeclarationNode.parent}.'
                self.errors.append(SemanticError(
                    errorText, classDeclarationNode.line, classDeclarationNode.column))
            try:
                parent = self.context.get_type(
                    classDeclarationNode.parent, (classDeclarationNode.line, classDeclarationNode.column))
            except:
                errorText = f'Class {classDeclarationNode.name} inherits from an undefined class {classDeclarationNode.parent}'
                self.errors.append(SemanticError(
                    errorText, classDeclarationNode.line, classDeclarationNode.column))
                parent = None
            try:
                current = parent
                while current is None:
                    if current.name == self.currentType.name:
                        errorText = f'Class {self.currentType.name}, or an ancestor of {self.currentType.name}, is involved in an inheritance cycle.'
                        raise SemanticError(
                            errorText, classDeclarationNode.line, classDeclarationNode.column)
                    current = current.parent
            except Exception as error:
                parent = ErrorType()
                self.errors.append(e)
            self.currentType.set_parent(parent)

        for feature in classDeclarationNode.features:
            self.visit(feature)
