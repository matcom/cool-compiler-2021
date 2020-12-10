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
from src.tset import Tset


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
        # Despues de entregar!!!!!!
        io_type = self.context.get_type("IO")
        self_type = self.context.get_type("SELF_TYPE")
        int_type = self.context.get_type("Int")
        string_type = self.context.get_type("String")

        parent_tset = Tset()
        parent_tset.locals["out_string"] = {"SELF_TYPE"}
        parent_tset.locals["out_int"] = {"SELF_TYPE"}
        parent_tset.locals["in_string"] = {"String"}
        parent_tset.locals["in_int"] = {"Int"}

        method = io_type.define_method("out_string", ["x"], [string_type], self_type)
        method.tset = Tset(parent_tset)
        method.tset.locals["x"] = {"String"}

        method = io_type.define_method("out_int", ["x"], [int_type], self_type)
        method.tset = Tset(parent_tset)
        method.tset.locals["x"] = {"Int"}

        method = io_type.define_method("in_string", [], [], string_type)
        method.tset = Tset(parent_tset)

        method = io_type.define_method("in_int", [], [], int_type)
        method.tset = Tset(parent_tset)

        # ----------------------------------------------------
        for declaration in node.declarations:
            self.visit(declaration)

    @visitor.when(ClassDeclarationNode)
    def visit(self, node):
        self.current_type = self.context.get_type(node.id)

        if node.parent is not None:
            try:
                parent_type = self.get_type(node.parent)
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

        try:
            param_types = [self.get_type(ftype) for fname, ftype in node.params]
            return_type = self.get_type(node.type)
            self.current_type.define_method(
                node.id, param_names, param_types, return_type
            )
        except SemanticError as error:
            self.errors.append(error.text)

    @visitor.when(AttrDeclarationNode)
    def visit(self, node):
        try:
            attr_type = self.get_type(node.type)
            self.current_type.define_attribute(node.id, attr_type)
        except SemanticError as error:
            self.errors.append(error.text)

    def get_type(self, tname):
        try:
            return self.context.get_type(tname)
        except SemanticError as error:
            self.errors.append(error.text)
            return ErrorType()
