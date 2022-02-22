from __future__ import annotations

from coolcmp import errors as err
from coolcmp.utils.ast import ProgramNode, ClassDeclarationNode, FuncDeclarationNode, AttrDeclarationNode, \
    IntegerNode, StringNode, BooleanNode, VariableNode
from coolcmp.utils.semantic import SemanticError, Context, ErrorType, Type, VoidType
from coolcmp.utils import visitor


class TypeBuilder:
    """
    Collects attributes, methods and parent in classes.
    In case of a type error set type to ErrorType.
    """
    def __init__(self, context: Context, errors: list[str]):
        self.context = context
        self.current_type: Type | None = None
        self.errors = errors

    @visitor.on('node')
    def visit(self, node):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node: ProgramNode):
        for declaration in node.declarations:
            self.visit(declaration)

        # self.context.get_type('Object').define_attribute('void', VoidType)
        # void_attr = AttrDeclarationNode('void', '<void>', VariableNode('void'))
        # object_class = ClassDeclarationNode('Object', [void_attr])
        # node.declarations.append(object_class)

    @visitor.when(ClassDeclarationNode)
    def visit(self, node: ClassDeclarationNode):
        self.current_type = self.context.get_type(node.id)

        # check parent
        if node.parent is not None:
            if node.parent in ('SELF_TYPE', 'String', 'Int', 'Bool', node.id):
                self.current_type.set_parent(ErrorType())
                self.errors.append(err.CANNOT_INHERIT % (node.parent_pos, node.parent))
            else:
                try:
                    parent_type = self.context.get_type(node.parent)
                except SemanticError:   # the parent type is not defined
                    parent_type = ErrorType()
                    self.errors.append(err.UNDEFINED_TYPE % (node.parent_pos, node.parent))
                try:
                    self.current_type.set_parent(parent_type)
                except SemanticError:   # this node already has a parent
                    self.errors.append(err.CANNOT_INHERIT % (node.pos, node.id, node.parent))
        else:
            try:
                self.current_type.set_parent(self.context.get_type('Object'))
            except SemanticError:
                pass

        # visit features
        for feature in node.features:
            self.visit(feature)

    @visitor.when(FuncDeclarationNode)
    def visit(self, node: FuncDeclarationNode):
        param_names = []
        param_types = []
        for param_node in node.params:
            param_names.append(param_node.id)
            try:
                param_types.append(self.context.get_type(param_node.type))
            except SemanticError:
                param_types.append(ErrorType())
                self.errors.append(err.UNDEFINED_TYPE % (param_node.type_pos, param_node.type))
        try:
            ret_type = self.context.get_type(node.return_type)
        except SemanticError:
            self.errors.append(err.UNDEFINED_TYPE % (node.pos, node.return_type))
            ret_type = ErrorType()

        try:
            self.current_type.define_method(node.id, param_names, param_types, ret_type)
        except SemanticError:
            self.errors.append(err.METHOD_ALREADY_DEFINED % (node.pos, node.id, self.current_type.name))

    @visitor.when(AttrDeclarationNode)
    def visit(self, node: AttrDeclarationNode):
        try:
            attr_type = self.context.get_type(node.type)
        except SemanticError:
            attr_type = ErrorType()
            self.errors.append(err.UNDEFINED_TYPE % (node.pos, node.type))

        # add a default initialization expr to the node if it doesn't have one
        if node.expr is None:
            if attr_type == self.context.get_type('Int'):
                node.expr = IntegerNode('0')
            elif attr_type == self.context.get_type('String'):
                node.expr = StringNode('""')
            elif attr_type == self.context.get_type('Bool'):
                node.expr = BooleanNode('false')
            else:
                node.expr = VariableNode('void')

        try:
            self.current_type.define_attribute(
                node.id, attr_type, node.expr or VariableNode('void'), self.current_type.name)
        except SemanticError:
            self.errors.append(err.ATTRIBUTE_ALREADY_DEFINED % (node.pos, node.id, self.current_type.name))
