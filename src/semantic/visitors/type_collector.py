from utils.ast import *
from utils import visitor
from semantic.types import *
from semantic.tools import Context
from utils.errors import SemanticError

class TypeCollector(object):
    def __init__(self, errors=[]):
        self.context = None
        self.errors = errors
    
    @visitor.on('node')
    def visit(self, node):
        pass 
    
    @visitor.when(ProgramNode)
    def visit(self, node:ProgramNode):
        self.context = Context()
        self.context.types['String'] = StringType()
        self.context.types['Int'] = IntType()
        self.context.types['Object'] = ObjectType()
        self.context.types['Bool'] = BoolType()
        self.context.types['SELF_TYPE'] = SelfType()
        self.context.types['IO'] = IOType()

        for dec in node.declarations:
            self.visit(dec)

    @visitor.when(ClassDeclarationNode)
    def visit(self, node:ClassDeclarationNode):
        if node.id in ['String', 'Int', 'Object', 'Bool', 'SELF_TYPE', 'IO']:
            error_text = SemanticError.REDEFINITION_ERROR % node.id
            self.errors.append(SemanticError(*node.pos, error_text))

        try:
            self.context.create_type(node.id, node.pos)
        except SemanticError as exception:
            self.errors.append(exception)

        if not node.parent:
            node.parent = 'Object'