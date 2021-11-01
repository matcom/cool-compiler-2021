from ..utils.ast import *
from ..utils import visitor
from .helpers import *
from .types import *


class TypeCollector:
    def __init__(self, errors=[]):
        self.context = None
        self.errors = errors

    @visitor.on('node')
    def visit(self, node):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node: ProgramNode):
        self.context = Context()
        self.context.types['String'] = StringType()
        self.context.types['Int'] = IntType()
        self.context.types['Object'] = ObjectType()
        self.context.types['Bool'] = BoolType()
        self.context.types['SELF_TYPE'] = SelfType()
        self.context.types['IO'] = IOType()

        for d in node.declarations:
            self.visit(d)

    @visitor.when(ClassDeclarationNode)
    def visit(self, node: ClassDeclarationNode):
        try:
            self.context.create_type(node.id, node.pos)
        except SemanticError as e:
            self.errors.append(e)

        if not node.parent:
            node.parent = 'Object'
