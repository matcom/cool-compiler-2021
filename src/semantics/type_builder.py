from utils import visitor
from ast.parser_ast import (
    Node,
    ProgramNode,
    ClassDeclarationNode,
    MethodDeclarationNode,
    AttrDeclarationNode,
)
from semantics.tools.errors import SemanticError
from semantics.tools import SelfType, TypeBag, ErrorType, Context


class TypeBuilder:
    def __init__(self, context: Context):
        self.context = context
        self.current_type = None
        self.errors: list = []

    @visitor.on("node")
    def visit(self, node):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node):
        self.build_default_classes()

        for class_def in node.declarations:
            self.visit(class_def)

        try:
            main = self.context.get_type("Main", unpacked=True).get_method(
                "main", local=True
            )
            if len(main.param_names) > 0:
                raise SemanticError(
                    "Method 'main' in class 'Main' must not have formal parameters"
                )
        except SemanticError as err:
            self.add_error(node, err.text)

    @visitor.when(ClassDeclarationNode)
    def visit(self, node: ClassDeclarationNode):
        self.current_type = self.context.get_type(node.id, unpacked=True)

        if node.parent:
            try:
                parent_type = self.context.get_type(node.parent, unpacked=True)
                self.current_type.set_parent(parent_type)
                for idx, _ in list(parent_type.all_attributes(True)):
                    self.current_type.attributes.append(idx)
            except SemanticError as err:
                self.add_error(node, err.text)

        for feature in node.features:
            self.visit(feature)

    @visitor.when(AttrDeclarationNode)
    def visit(self, node):
        try:
            attr_type = self.context.get_type(node.type)
        except SemanticError as err:
            self.add_error(node, err.text)
            attr_type = ErrorType()

        try:
            self.current_type.define_attribute(node.id, attr_type)
        except SemanticError as err:
            self.add_error(node, err.text)

    @visitor.when(MethodDeclarationNode)
    def visit(self, node):
        try:
            ret_type = self.context.get_type(node.type)
        except SemanticError as err:
            self.add_error(node, err.text)
            ret_type = ErrorType()

        params_type = []
        params_name = []
        for var in node.params:
            p_name = var.id
            p_type = var.type
            try:
                params_type.append(self.context.get_type(p_type, selftype=False))
            except SemanticError as err:
                params_type.append(ErrorType())
                self.add_error(
                    node,
                    err.text
                    + f" While defining parameter {var.id} in method {node.id}.",
                )
            if p_name in params_name:
                self.add_error(
                    node,
                    f"SemanticError: Formal parameter '{p_name}' has been defined multiple times.",
                )
                p_name = f"error({p_name})"
            if p_name == "self":
                self.add_error(
                    node,
                    "SemanticError: Cannot use 'self' as formal parameter identifier.",
                )
                p_name = f"error({p_name})"
            params_name.append(p_name)

        try:
            self.current_type.define_method(node.id, params_name, params_type, ret_type)
        except SemanticError as err:
            self.add_error(node, err.text)

    def build_default_classes(self):
        Object = self.context.get_type("Object", unpacked=True)
        String = self.context.get_type("String", unpacked=True)
        Int = self.context.get_type("Int", unpacked=True)
        Io = self.context.get_type("IO", unpacked=True)
        Bool = self.context.get_type("Bool", unpacked=True)

        String.set_parent(Object)
        Int.set_parent(Object)
        Io.set_parent(Object)
        Bool.set_parent(Object)

        p_Object = self.context.get_type("Object")
        p_String = self.context.get_type("String")
        p_Int = self.context.get_type("Int")
        p_Self = TypeBag({SelfType()})

        Object.define_method("abort", [], [], p_Object)
        Object.define_method("type_name", [], [], p_String)
        Object.define_method("copy", [], [], p_Self)

        String.define_method("length", [], [], p_Int)
        String.define_method("concat", ["s"], [p_String], p_String)
        String.define_method("substr", ["i", "l"], [p_Int, p_Int], p_String)

        Io.define_method("out_string", ["x"], [p_String], p_Self)
        Io.define_method("out_int", ["x"], [p_Int], p_Self)
        Io.define_method("in_string", [], [], p_String)
        Io.define_method("in_int", [], [], p_Int)

    def add_error(self, node: Node, text: str):
        line, col = node.get_position() if node else (0, 0)
        self.errors.append(((line, col), f"({line}, {col}) - " + text))
