from src.utils.errors import SemanticError
from utils import visitor
from utils.ast import ProgramNode, ClassDeclarationNode
from semantic.semantic import Context, IntType, StringType, BoolType, ObjectType, SelfType, IOType


class TypeCollector(object):
    def __init__(self, errors=[]):
        self.context = None
        self.errors = errors

    @visitor.on('node')
    def visit(self, node):
        pass

    @visitor.when(ProgramNode)
    def visit(self, programNode):
        self.context = Context()
        self.context.types['Int'] = IntType()
        self.context.types['String'] = StringType()
        self.context.types['Bool'] = BoolType()
        self.context.types['Object'] = ObjectType()
        self.context.types['SELF_TYPE'] = SelfType()
        self.context.types['IO'] = IOType()

        for classDeclarationNode in programNode.classes:
            self.visit(self, classDeclarationNode)

    @visitor.when(ClassDeclarationNode)
    def visit(self, classDeclarationNode):
        if classDeclarationNode.name in ['Int', 'String', 'Bool', 'Object', 'SELF_TYPE', 'IO']:
            errorText = f'Redefinition of basic class {classDeclarationNode.name}'
            self.errors.append(SemanticError(errorText, *classDeclarationNode.position))
        try:
            self.context.create_type(classDeclarationNode.name, classDeclarationNode.position)
        except Exception as error:
            self.errors.append(error)
        
        if not classDeclarationNode.parent:
            classDeclarationNode.parent = 'Object'

