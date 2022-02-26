from app.semantics.tools.type import Type
import app.shared.visitor as visitor
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
from .constants import *
from app.shared.cascade import chained


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
                [self.current_type.attributes.append(idx) for idx, _ in list(
                    parent_type.all_attributes(True))]
            except SemanticError as err:
                self.add_error(node, err.text)

        [self.visit(feature) for feature in node.features]

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
        [self._analyze_param(node, params_name, params_type, p_name, p_type)
         for p_name, p_type in zip(node.param_names[0], node.param_names[1])]

        try:
            self.current_type.define_method(
                node.id, params_name, params_type, ret_type)
        except SemanticError as err:
            self.add_error(node, err.text)

    def _analyze_param(self, node, params_name, params_type, p_name, p_type):
        try:
            typex = self.context.get_type(p_type, selftype=False)
        except SemanticError as err:
            typex = TypeBag(set())
            self.add_error(
                node,
                err.text
                + f" While defining parameter {p_name} in method {node.id}.",
            )
        params_type.append(typex)
        if p_name == "self":
            self.add_error(
                node,
                "SemanticError: Cannot use 'self' as formal parameter identifier.",
            )
            p_name = f"error({p_name})"
        if p_name in params_name:
            self.add_error(
                node,
                f"SemanticError: Formal parameter '{p_name}' has been defined multiple times.",
            )
            p_name = f"error({p_name})"

        params_name.append(p_name)

    def build_default_classes(self):
        Object = self.context.get_type(OBJECT_TYPE, unpacked=True)
        String = self.context.get_type(STRING_TYPE, unpacked=True)
        Int = self.context.get_type(INT_TYPE, unpacked=True)
        Io = self.context.get_type(IO_TYPE, unpacked=True)
        Bool = self.context.get_type(BOOL_TYPE, unpacked=True)

        String.set_parent(Object)
        Int.set_parent(Object)
        Io.set_parent(Object)
        Bool.set_parent(Object)

        p_Object = self.context.get_type(OBJECT_TYPE)
        p_String = self.context.get_type(STRING_TYPE)
        p_Int = self.context.get_type(INT_TYPE)
        p_Self = self.context.get_type(SELF_TYPE)

        chained(Object)\
            .define_method(ABORT_METHOD_NAME, [], [], p_Object)\
            .define_method(TYPE_NAME_METHOD_NAME, [], [], p_String)\
            .define_method(COPY_METHOD_NAME, [], [], p_Self)

        chained(Io)\
            .define_method(OUT_STRING_METHOD_NAME, ["x"], [p_String], p_Self)\
            .define_method(OUT_INT_METHOD_NAME, ["x"], [p_Int], p_Self)\
            .define_method(IN_STRING_METHOD_NAME, [], [], p_String)\
            .define_method(IN_INT_METHOD_NAME, [], [], p_Int)

        chained(String)\
            .define_method(LENGTH_METHOD_NAME, [], [], p_Int)\
            .define_method(CONCAT_METHOD_NAME, ["s"], [p_String], p_String)\
            .define_method(SUBSTR_METHOD_NAME, ["i", "l"], [
                p_Int, p_Int], p_String)

    def add_error(self, node: AstNode, text: str):
        line, col = node.lineno, node.columnno if node else (0, 0)
        self.errors.append(f"({line}, {col}) - " + text)
