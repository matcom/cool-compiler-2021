from cmp.semantic import SemanticError as SError
from cmp.semantic import Attribute, Method, Type
from cmp.semantic import (
    VoidType,
    IntType,
    ErrorType,
    StringType,
    BoolType,
    AutoType,
    ObjectType,
    SelfType,
    IOType,
)
from cmp.semantic import Context
from semantic.ast_nodes import ProgramNode, ClassDeclarationNode
import cmp.visitor as visitor
from semantic.cool_visitor import CopyVisitor
from cmp.errors import SemanticError

class TypeCollector(object):
    def __init__(self, errors=[]):
        self.context = None
        self.errors = errors

    @visitor.on("node")
    def visit(self, node):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node):
        self.context = Context()
        self.context.types["Object"] = ObjectType()
        self.context.types["Int"] = IntType()
        self.context.types["String"] = StringType()
        self.context.types["Bool"] = BoolType()
        self.context.types["AUTO_TYPE"] = AutoType()
        self.context.types["SELF_TYPE"] = SelfType()
        self.context.types["IO"] = IOType()

        object_type = self.context.get_type("Object")
        for typex in self.context.types.values():
            if typex == object_type:
                continue
            typex.set_parent(object_type)

        for declaration in node.declarations:
            self.visit(declaration)

        copy_visitor = CopyVisitor()
        newAst = copy_visitor.visit(node)
        newAst.context = self.context

        # Reset state
        self.context = None
        self.errors = None

        return newAst

    @visitor.when(ClassDeclarationNode)
    def visit(self, node):
        try:
            self.context.create_type(node.id.lex)
        except SError as error: # class alerady defined
            node_row, node_col = node.id.location
            self.errors.append(SemanticError(node_row, node_col, error.text))
