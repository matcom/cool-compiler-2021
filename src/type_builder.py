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
        self.check_cycles(node.declarations)

        parent_child_dict = {}
        queue = deque()
        visited = {}
        not_visited = []  # ++
        for class_declaration in node.declarations:
            not_visited.append(class_declaration)  
            try:
                parent_type = class_declaration.parent.lex
                self.context.get_type(parent_type)
                try:
                    parent_child_dict[parent_type].append(class_declaration)
                except:  # KeyError
                    parent_child_dict[parent_type] = [class_declaration]
            except Exception:  # parent is None or not definition provided
                queue.append(class_declaration)

        while not_visited:  # ++
            while queue:
                class_declaration = queue.popleft()
                try: # avoid redefining classes involved in a ciclyc heritage
                    class_visited = visited[class_declaration]  # .id
                except:
                    not_visited.remove(class_declaration)
                    try:
                        children = parent_child_dict[class_declaration.id]
                        for declaration in children:
                            queue.append(declaration)
                    except:  # no one inherits from this class
                        pass

                    self.visit(class_declaration)
                    visited[class_declaration] = True  # .id

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
            self.errors.append(SemanticError(0, 0 ,"A class Main with a method main most be provided"))

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
        self.current_type = self.context.get_type(node.id)

        if node.parent is not None:
            try:
                parent_type = self.get_type(node.parent, f"declared as {node.id}'s parent")
                self.current_type.set_parent(parent_type)
            except SError as error:
                node_row, node_col = node.parent.location
                self.errors.append(SemanticError(node_row, node_col, error.text))
        else:
            object_type = self.context.get_type("Object")
            try:
                self.current_type.set_parent(object_type)
            except SError as error: # this is actually an intern error, a class parent most not be setted twice (is valid to note that the intention to inherit from a prohibited class is considered a semantic error)
                node_row, node_col = node.token.location
                self.errors.append(SemanticError(node_row, node_col, error.text))

        for feature in node.features:
            self.visit(feature)

    @visitor.when(FuncDeclarationNode)
    def visit(self, node):
        param_names = [fname.lex for fname, ftype in node.params]

        try:
            param_types = [self.get_type(ftype, f"of formal parameter {fname.lex}") for fname, ftype in node.params]
            return_type = self.get_type(node.type, f"marked in '{node.id.lex}' as return type")
            self.current_type.define_method(
                node.id.lex, param_names, param_types, return_type
            )
        except SError as error:
            node_row, node_col = node.id.location
            # print("--------aqui se esta reportando el error del metodo doble---------")
            self.errors.append(SemanticError(node_row, node_col,error.text))

    @visitor.when(AttrDeclarationNode)
    def visit(self, node):
        if node.id.lex == "self":
            node_row, node_col = node.id.location
            self.errors.append(SemanticError(node_row, node_col,"'self' cannot be the name of an attribute."))
            return
        try:
            attr_type = self.get_type(node.type, f"of attribute {node.id.lex}")
            self.current_type.define_attribute(node.id.lex, attr_type)
        except SError as error:
            node_row, node_col = node.id.location
            self.errors.append(SemanticError(node_row, node_col,error.text))

    def get_type(self, ntype, comp_error_mesg):
        try:
            return self.context.get_type(ntype.lex)
        except SError as error:
            node_row, node_col = ntype.location
            self.errors.append(TypeError(node_row, node_col, f"Type {ntype.lex} " + comp_error_mesg + " is not defined."))
            return ErrorType()

    def check_cycles(self, class_declarations):
        # checking for cycles
        paths = []
        modified_paths = paths

        for class_declaration in class_declarations:
            if not (class_declaration.parent is None):
                d = class_declaration.id
                p = class_declaration.parent.lex

                modified_paths = paths

                already_in_some_path = False
                for i in range(0,len(paths)):
                    path = paths[i]
                    if path[-1] == d:
                        if not (p in path):
                            modified_paths[i] = path + [p]
                            # add parent to last pos
                        else:
                            # error
                            node_row, node_col = class_declaration.parent.location
                            self.errors.append(
                                SemanticError(node_row, node_col, f"Class {class_declaration.id}, or an ancestor of {class_declaration.id}, is involved in an inheritance cycle.")
                            )
                        already_in_some_path = True

                    elif path[0] == p:
                        if not (d in path):
                            # add himself to first pos
                            modified_paths[i] = [d] + path
                        else:
                            # error
                            node_row, node_col = class_declaration.parent.location
                            self.errors.append(
                                SemanticError(node_row, node_col, f"Class {class_declaration.id}, or an ancestor of {class_declaration.id}, is involved in an inheritance cycle.")
                            )
                        already_in_some_path = True
                        
                    elif p in path:
                        # duplicate list
                        indx = path.index(p)
                        modified_paths = modified_paths + [[d] + path[indx:len(path)]] 
                        already_in_some_path = True

                if not already_in_some_path: 
                    if d != p:
                        modified_paths = paths + [[d, p]]
                    else: # class inherits from itself
                        node_row, node_col = class_declaration.parent.location
                        self.errors.append(
                            SemanticError(node_row, node_col, f"Class {class_declaration.id}, or an ancestor of {class_declaration.id}, is involved in an inheritance cycle.")
                        )
                paths = modified_paths