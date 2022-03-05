import copy
from cmp.semantic import SemanticError as SError
from cmp.semantic import Attribute, Method, Type
from cmp.semantic import VoidType, IntType, ErrorType, StringType, BoolType
from cmp.semantic import Context
from ast_nodes import (
    ProgramNode,
    ClassDeclarationNode,
    AttrDeclarationNode,
    FuncDeclarationNode,
)
import cmp.visitor as visitor
from tset import Tset
from collections import deque
from cool_visitor import CopyVisitor
from errors import SemanticError, TypeError

class TypeBuilder:
    def __init__(self, errors=[]):
        self.context = None
        self.current_type = None
        self.errors = errors

    @visitor.on("node")
    def visit(self, node):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node):
        self.context = copy.copy(node.context)

        io_type = self.context.get_type("IO")
        self_type = self.context.get_type("SELF_TYPE")
        int_type = self.context.get_type("Int")
        string_type = self.context.get_type("String")
        object_type = self.context.get_type("Object")

        # IO
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

        # String
        parent_tset = Tset()
        parent_tset.locals["concat"] = {"String"}
        parent_tset.locals["substr"] = {"String"}
        parent_tset.locals["length"] = {"Int"}

        method = string_type.define_method("concat", ["s"], [string_type], string_type)
        method.tset = Tset(parent_tset)
        method.tset.locals["s"] = {"String"}

        method = string_type.define_method(
            "substr", ["i", "l"], [int_type, int_type], string_type
        )
        method.tset = Tset(parent_tset)
        method.tset.locals["i"] = {"Int"}
        method.tset.locals["l"] = {"Int"}

        method = string_type.define_method("length", [], [], int_type)
        method.tset = Tset(parent_tset)

        # Object
        parent_tset = Tset()
        parent_tset.locals["abort"] = {"Object"}
        parent_tset.locals["type_name"] = {"String"}
        parent_tset.locals["copy"] = {"SELF_TYPE"}

        method = object_type.define_method("abort", [], [], object_type)
        method.tset = Tset(parent_tset)

        method = object_type.define_method("type_name", [], [], string_type)
        method.tset = Tset(parent_tset)

        method = object_type.define_method("copy", [], [], self_type)
        method.tset = Tset(parent_tset)

        # ------checking for in order definitions and cyclic heritage
        parent_child_dict = {}
        queue = deque()
        visited = {}
        not_visited = []  # ++

        for class_declaration in node.declarations:
            not_visited.append(class_declaration)  # ++
            if not (class_declaration.parent is None):
                parent_type = class_declaration.parent.lex
            else:
                parent_type = None
            try:
                self.context.get_type(parent_type)
                try:
                    parent_child_dict[parent_type].append(class_declaration)
                except:  # KeyError
                    parent_child_dict[parent_type] = [class_declaration]
            except SError:  # parent is None or not definition provided
                queue.append(class_declaration)

        main_round = 0
        while not_visited:  # ++
            main_round += 1
            while queue:
                class_declaration = queue.popleft()
                try:
                    class_visited, roundn = visited[class_declaration]  # .id

                    if roundn == main_round:
                        self.errors.append(
                            f"{class_declaration.id} is involved in a cyclic heritage"
                        )

                except:
                    not_visited.remove(class_declaration)
                    try:
                        children = parent_child_dict[class_declaration.id]
                        for declaration in children:
                            queue.append(declaration)
                    except:  # no es padre de nadie
                        pass

                    self.visit(class_declaration)
                    visited[class_declaration] = (True, main_round)  # .id

            if not_visited:
                queue.append(not_visited[0])

        try:
            main_meth = self.context.get_type("Main").get_method("main", non_rec=True)
            if len(main_meth.param_names) > 0:
                self.errors.append(
                    '"main" method in class Main does not receive any parameters'
                )
            # modify in semantic get_method in order to get some ancestor where the method is already defined
        except SError:
            self.errors.append("A class Main with a method main most be provided")

        # ----------------------------------------------------
        # for declaration in node.declarations:
        #     self.visit(declaration)

        copy_visitor = CopyVisitor()
        newAst = copy_visitor.visit(node)
        newAst.context = self.context

        # Reset state
        self.context = None
        self.current_type = None
        self.errors = None

        return newAst

    @visitor.when(ClassDeclarationNode)
    def visit(self, node):
        # print(f"------------visiting class {node.id}------------")
        self.current_type = self.context.get_type(node.id)

        if node.parent is not None:
            try:
                parent_type = self.get_type(node.parent)
                self.current_type.set_parent(parent_type)
            except SError as error:
                node_row, node_col = node.parent.location
                self.errors.append(SemanticError(node_row, node_col, error.text))
        else:
            object_type = self.context.get_type("Object")
            try:
                self.current_type.set_parent(object_type)
            except SError as error:
                self.errors.append(error.text)

        for feature in node.features:
            self.visit(feature)

    @visitor.when(FuncDeclarationNode)
    def visit(self, node):
        param_names = [fname.lex for fname, ftype in node.params]

        try:
            param_types = [self.get_type(ftype) for fname, ftype in node.params]
            return_type = self.get_type(node.type)
            self.current_type.define_method(
                node.id.lex, param_names, param_types, return_type
            )
        except SError as error:
            node_row, node_col = node.id.location
            # print("--------aqui se esta reportando el error del metodo doble---------")
            self.errors.append(SemanticError(node_row, node_col,error.text))

    @visitor.when(AttrDeclarationNode)
    def visit(self, node):
        try:
            attr_type = self.get_type(node.type)
            self.current_type.define_attribute(node.id.lex, attr_type)
        except SError as error:
            node_row, node_col = node.id.location
            self.errors.append(SemanticError(node_row, node_col,error.text))

    def get_type(self, ntype):
        try:
            return self.context.get_type(ntype.lex)
        except SError as error:
            node_row, node_col = ntype.location
            self.errors.append(TypeError(node_row, node_col,error.text))
            return ErrorType()
