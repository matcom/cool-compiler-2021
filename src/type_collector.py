import utils.visitor as visitor
from ast_cool_hierarchy import *
from utils.semantic import SemanticError, Context, BasicTypes
from utils.semantic import (
    ObjType,
    IntType,
    StrType,
    SelfType,
    AutoType,
    BoolType,
    ErrorType,
    Type,
)

TYPE_ERROR = "(%s, %s) - TypeError: %s"
SEMANTIC_ERROR = "(%s, %s) - SemanticError: %s"


class TypeCollector(object):
    def __init__(self, errors=None):
        if errors is None:
            errors = []
        self.context = None
        self.errors = errors

    @visitor.on("node")
    def visit(self, node):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node):
        self.context = Context()

        bool_type = BoolType()
        int_type = IntType()
        str_type = _create_string_type(int_type)
        self_type = SelfType()
        obj_type = _create_object_type(str_type, self_type)
        io_type = _create_io_type(str_type, self_type, int_type)
        auto_type = AutoType()
        error_type = ErrorType()

        bool_type.set_parent(obj_type)
        int_type.set_parent(obj_type)
        str_type.set_parent(obj_type)
        self_type.set_parent(obj_type)
        io_type.set_parent(obj_type)
        auto_type.set_parent(obj_type)
        error_type.set_parent(obj_type)

        self.context.types[BasicTypes.BOOL.value] = bool_type
        self.context.types[BasicTypes.INT.value] = int_type
        self.context.types[BasicTypes.STRING.value] = str_type
        self.context.types[BasicTypes.SELF.value] = self_type
        self.context.types[BasicTypes.OBJECT.value] = obj_type
        self.context.types[BasicTypes.IO.value] = io_type
        self.context.types[BasicTypes.AUTO.value] = auto_type
        self.context.types[BasicTypes.ERROR.value] = error_type

        for class_dec_node in node.declarations:
            self.visit(class_dec_node)

    @visitor.when(ClassDeclarationNode)
    def visit(self, node):
        try:
            typex = self.context.create_type(node)
            typex.set_parent(self.context.types[BasicTypes.OBJECT.value])
        except SemanticError as error:
            self.errors.append(SEMANTIC_ERROR % (node.line_no, node.col_no, error.text))
            node.id = BasicTypes.ERROR.value


def _create_string_type(int_type):
    str_type = StrType()
    str_type.define_method("length", [], [], int_type)
    str_type.define_method("concat", ["s"], [str_type], str_type)
    str_type.define_method("substr", ["i", "l"], [int_type, int_type], str_type)
    return str_type


def _create_object_type(str_type, self_type):
    obj_type = ObjType()
    obj_type.define_method("abort", [], [], obj_type)
    obj_type.define_method("type_name", [], [], str_type)
    obj_type.define_method("copy", [], [], self_type)
    return obj_type


def _create_io_type(str_type, self_type, int_type):
    io_type = Type(BasicTypes.IO.value)
    io_type.define_method("out_string", ["x"], [str_type], self_type)
    io_type.define_method("out_int", ["x"], [int_type], self_type)
    io_type.define_method("in_string", [], [], str_type)
    io_type.define_method("in_int", [], [], int_type)
    return io_type
