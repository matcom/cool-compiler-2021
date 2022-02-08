import utils.visitor as visitor
from ast_hierarchy import *
from utils.semantic import SemanticError, Context
from utils.semantic import ObjType, IntType, StrType, SelfType, AutoType, BoolType, ErrorType, Type


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

        self.context.types["Bool"] = bool_type
        self.context.types["Int"] = int_type
        self.context.types["String"] = str_type
        self.context.types["SELF_TYPE"] = self_type
        self.context.types["Object"] = obj_type
        self.context.types["IO"] = io_type
        self.context.types["AUTO_TYPE"] = auto_type
        self.context.types["<error>"] = error_type

        for class_dec_node in node.declarations:
            self.visit(class_dec_node)

    @visitor.when(ClassDeclarationNode)
    def visit(self, node):
        try:
            typex = self.context.create_type(node.id)
            typex.set_parent(self.context.types["Object"])
        except SemanticError as error:
            self.errors.append(error.text)


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
    io_type = Type("IO")
    io_type.define_method("out_string", ["x"], [str_type], self_type)
    io_type.define_method("out_int", ["x"], [int_type], self_type)
    io_type.define_method("in_string", [], [], str_type)
    io_type.define_method("in_int", [], [], int_type)
    return io_type
