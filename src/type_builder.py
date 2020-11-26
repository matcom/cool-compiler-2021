from src.cmp.semantic import SemanticError
from src.cmp.semantic import Attribute, Method, Type
from src.cmp.semantic import VoidType, IntType, ErrorType, StringType, BoolType
from src.cmp.semantic import Context
from src.ast_nodes import (
    ProgramNode,
    ClassDeclarationNode,
    AttrDeclarationNode,
    FuncDeclarationNode,
)
import src.cmp.visitor as visitor


class TypeBuilder:
    def __init__(self, context, errors=[]):
        self.context = context
        self.current_type = None
        self.errors = errors

    @visitor.on("node")
    def visit(self, node):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node):
        for declaration in node.declarations:
            self.visit(declaration)

    @visitor.when(ClassDeclarationNode)
    def visit(self, node):
        self.current_type = self.context.get_type(node.id)

        if node.parent is not None:
            parent_type = self.get_type(node.parent)
            try:
                self.current_type.set_parent(parent_type)
            except SemanticError as error:
                self.errors.append(error.text)
        else:
            object_type = self.context.get_type("Object")
            try:
                self.current_type.set_parent(object_type)
            except SemanticError as error:
                self.errors.append(error)

        for feature in node.features:
            self.visit(feature)

    @visitor.when(FuncDeclarationNode)
    def visit(self, node):
        param_names = [fname for fname, ftype in node.params]
        param_types = [self.get_type(ftype) for fname, ftype in node.params]
        return_type = self.get_type(node.type)

        try:
            self.current_type.define_method(
                node.id, param_names, param_types, return_type
            )
        except SemanticError as error:
            self.errors.append(error.text)

    @visitor.when(AttrDeclarationNode)
    def visit(self, node):
        attr_type = self.get_type(node.type)

        try:
            self.current_type.define_attribute(node.id, attr_type)
        except SemanticError as error:
            self.errors.append(error.text)

    def get_type(self, tname):
        try:
            return self.context.get_type(tname)
        except SemanticError as error:
            self.errors.append(error.text)
            return ErrorType()
