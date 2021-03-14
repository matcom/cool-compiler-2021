import coolpyler.utils.meta as meta
import coolpyler.utils.visitor as visitor
import coolpyler.ast.cool.base as base
import coolpyler.ast.cool.type_collected as type_collected
from coolpyler.errors import SemanticError
from coolpyler.semantic import (
    BoolType,
    ErrorType,
    IOType,
    IntType,
    ObjectType,
    StringType,
    Type,
)


class TypeCollectorVisitor(object):
    def __init__(self, errors=None):
        if errors is None:
            errors = []
        self.errors = errors
        self.types = None

    @visitor.on("node")
    def visit(self, node):
        pass

    @visitor.when(base.CoolAstNode)  # noqa: F811
    def visit(self, node: base.CoolAstNode):
        def map_attr(attr):
            if isinstance(attr, base.CoolAstNode):
                return meta.map_to_module(attr, map_attr, type_collected)
            elif isinstance(attr, (tuple, list)):
                return [meta.map_to_module(a, map_attr, type_collected) for a in attr]
            else:
                return attr

        return meta.map_to_module(node, map_attr, type_collected)

    @visitor.when(base.CoolProgramNode)  # noqa: F811
    def visit(self, node: base.CoolProgramNode):
        object_type = ObjectType()

        int_type = IntType()
        int_type.set_parent(object_type)

        bool_type = BoolType()
        bool_type.set_parent(object_type)

        string_type = StringType()
        string_type.set_parent(object_type)

        io_type = IOType()
        io_type.set_parent(object_type)

        self.types = {
            object_type.name: object_type,
            int_type.name: int_type,
            bool_type.name: bool_type,
            string_type.name: string_type,
            io_type.name: io_type,
        }

        classes = [self.visit(c) for c in node.classes]

        return type_collected.CoolProgramNode(
            node.lineno, node.columnno, classes, self.types
        )

    @visitor.when(base.CoolClassNode)  # noqa: F811
    def visit(self, node: base.CoolClassNode):
        if node.id in self.types:
            self.errors.append(
                SemanticError(
                    node.lineno, 0, f"Type with name `{node.id}` already defined."
                )
            )
            type = ErrorType()
        else:
            type = self.types[node.id] = Type(node.id)

        return type_collected.CoolClassNode(
            node.lineno, node.columnno, type, node.features, parent=node.parent
        )
