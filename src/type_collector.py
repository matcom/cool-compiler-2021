from src.cmp.semantic import SemanticError
from src.cmp.semantic import Attribute, Method, Type
from src.cmp.semantic import (
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
from src.cmp.semantic import Context
from src.ast_nodes import ProgramNode, ClassDeclarationNode
import src.cmp.visitor as visitor
from cool_visitor import CopyVisitor


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
        # TODO: Es necesario crear estos tipos especificos?
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

        newAst.context = self.context.copy()
        self.context = None
        # TODO: self.errors tambien deberia volver a su estado inicial
        # devolver (newAst,errors) ???
        return newAst

    @visitor.when(ClassDeclarationNode)
    def visit(self, node):
        try:
            self.context.create_type(node.id)
        except SemanticError as error:
            self.errors.append(error.text)
