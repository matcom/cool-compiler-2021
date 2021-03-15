import coolpyler.errors as errors
import coolpyler.utils.meta as meta
import coolpyler.utils.visitor as visitor
import coolpyler.ast.cool.type_collected as type_collected
import coolpyler.ast.cool.type_built as type_built
import coolpyler.semantic as semantic
from coolpyler.semantic import ErrorType


class TypeBuilderVisitor:
    def __init__(self, errors=None):
        if errors is None:
            errors = []
        self.errors = errors
        self.current_type = None
        self.types = None

    def get_type(self, name):
        try:
            return self.types[name]
        except KeyError:
            raise semantic.SemanticError(f"Type `{name}` is not defined.")

    @visitor.on("node")
    def visit(self, node):
        pass

    @visitor.when(type_collected.CoolAstNode)  # noqa: F811
    def visit(self, node: type_collected.CoolAstNode):
        def map_attr(attr):
            if isinstance(attr, type_collected.CoolAstNode):
                return meta.map_to_module(attr, map_attr, type_built)
            elif isinstance(attr, (tuple, list)):
                return [meta.map_to_module(a, map_attr, type_built) for a in attr]
            else:
                return attr

        return meta.map_to_module(node, map_attr, type_built)

    @visitor.when(type_collected.CoolProgramNode)  # noqa: F811
    def visit(self, node: type_collected.CoolProgramNode):
        self.types = node.types
        classes = [self.visit(c) for c in node.classes]
        return type_built.CoolProgramNode(
            node.lineno, node.columnno, classes, node.types
        )

    @visitor.when(type_collected.CoolClassNode)  # noqa: F811
    def visit(self, node: type_collected.CoolClassNode):
        self.current_type = node.type

        parent_type = self.types["Object"]
        if node.parent is not None:
            try:
                parent_type = self.get_type(node.parent)
            except semantic.SemanticError as e:
                self.errors.append(errors.TypeError(node.lineno, node.columnno, e.text))

        try:
            self.current_type.set_parent(parent_type)
        except semantic.SemanticError as e:
            self.errors.append(errors.SemanticError(node.lineno, node.columnno, e.text))

        features = [self.visit(feat) for feat in node.features]

        return type_built.CoolClassNode(node.lineno, node.columnno, node.type, features)

    @visitor.when(type_collected.CoolAttrDeclNode)  # noqa: F811
    def visit(self, node: type_collected.CoolAttrDeclNode):
        try:
            type = self.get_type(node.type)
        except semantic.SemanticError as e:
            self.errors.append(errors.TypeError(node.lineno, node.columnno, e.text))
            type = ErrorType()

        try:
            attr_info = self.current_type.define_attribute(node.id, type)
        except semantic.SemanticError as e:
            self.errors.append(errors.SemanticError(node.lineno, node.columnno, e.text))
            attr_info = None  # TODO: check

        body = self.visit(node.body) if node.body is not None else None
        return type_built.CoolAttrDeclNode(
            node.lineno, node.columnno, attr_info, body=body
        )

    @visitor.when(type_collected.CoolFuncDeclNode)  # noqa: F811
    def visit(self, node: type_collected.CoolFuncDeclNode):
        param_types = []
        for ptype_name in node.param_types:
            try:
                ptype = self.get_type(ptype_name)
            except semantic.SemanticError as error:
                self.errors.append(
                    errors.TypeError(node.lineno, node.columnno, error.text)
                )
                ptype = ErrorType()
            param_types.append(ptype)

        try:
            return_type = self.get_type(node.type)
        except semantic.SemanticError as error:
            self.errors.append(errors.TypeError(node.lineno, node.columnno, error.text))
            return_type = ErrorType()

        try:
            func_info = self.current_type.define_method(
                node.id,
                node.param_names,
                param_types,
                return_type,
            )
        except semantic.SemanticError as error:
            self.errors.append(
                errors.SemanticError(node.lineno, node.columnno, error.text)
            )
            func_info = None  # TODO: check

        body = self.visit(node.body)

        return type_built.CoolFuncDeclNode(node.lineno, node.columnno, func_info, body)
