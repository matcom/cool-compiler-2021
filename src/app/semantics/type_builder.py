from app.semantics.tools.type import Type
import app.utils.visitor as visitor
from app.parser.ast import (
    AstNode,
    MethodDeclNode,
    ProgramNode,
    ClassNode,
    MethodDeclNode,
    AttrDeclNode,
)
from app.semantics.tools.errors import SemanticError
from app.semantics.tools import TypeBag, Context


class TypeBuilder:
    def __init__(self, context: Context):
        self.context = context
        self.current_type: Type
        self.errors: list = []

    @visitor.on("node")
    def visit(self, node):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node: ProgramNode):
        self.build_default_classes()

        for class_def in node.classes:
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

    @visitor.when(ClassNode)
    def visit(self, node: ClassNode):
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

    @visitor.when(AttrDeclNode)
    def visit(self, node: AttrDeclNode):
        try:
            attr_type = self.context.get_type(node.type)
        except SemanticError as err:
            self.add_error(node, err.text)
            attr_type = TypeBag(set())

        try:
            self.current_type.define_attribute(node.id, attr_type)
        except SemanticError as err:
            self.add_error(node, err.text)

    @visitor.when(MethodDeclNode)
    def visit(self, node: MethodDeclNode):
        try:
            ret_type = self.context.get_type(node.type)
        except SemanticError as err:
            self.add_error(node, err.text)
            ret_type = TypeBag(set())

        params_type = []
        params_name = []
        # print(node.id, node.param_names)
        for var in zip(node.param_names[0], node.param_names[1]):
            p_name, p_type = var
            try:
                params_type.append(
                    self.context.get_type(p_type, selftype=False))
            except SemanticError as err:
                params_type.append(TypeBag(set()))
                self.add_error(
                    node,
                    err.text
                    + f" While defining parameter {p_name} in method {node.id}.",
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
            self.current_type.define_method(
                node.id, params_name, params_type, ret_type)
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
        p_Self = self.context.get_type("SELF_TYPE")  # TypeBag({SelfType()})

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

    def add_error(self, node: AstNode, text: str):
        line, col = node.lineno, node.columnno if node else (0, 0)
        self.errors.append(f"({line}, {col}) - " + text)
