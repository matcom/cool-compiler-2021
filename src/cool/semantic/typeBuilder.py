from ..utils.ast import *
from ..utils import visitor
from .helpers import *
from .types import *
from typing import List


class TypeBuilder:
    def __init__(self, context: Context, errors=[]):
        self.context: Context = context
        self.errors: List = errors
        self.current_type: Type = None

    @visitor.on('node')
    def visit(self, node):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node: ProgramNode):
        for d in node.declarations:
            self.visit(d)

    @visitor.when(ClassDeclarationNode)
    def visit(self, node: ClassDeclarationNode):
        try:
            self.current_type = self.context.get_type(node.id, node.pos)
        except SemanticError as e:
            self.current_type = ErrorType()
            self.errors.append(e)

        if node.parent is not None:
            if node.parent in ['Int', 'Bool', 'String']:
                error_text = SemanticError.INHERIT_ERROR % (node.id, node.parent)
                self.errors.append(SemanticError(error_text, *node.parent_pos))

            try:
                parent = self.context.get_type(node.parent, node.parent_pos)
            except SemanticError:
                error_text = TypesError.INHERIT_UNDEFINED % (node.id, node.parent)
                self.errors.append(TypesError(error_text, *node.parent_pos))
                parent = None

            try:
                current = parent
                while current is not None:
                    if current.name == self.current_type.name:
                        error_text = SemanticError.CIRCULAR_DEPENDENCY % (
                            self.current_type.name, self.current_type.name)

                        raise SemanticError(error_text, *node.pos)
                    current = current.parent
            except SemanticError as e:
                parent = ErrorType()
                self.errors.append(e)

            self.current_type.set_parent(parent)

        for f in node.features:
            self.visit(f)

    @visitor.when(FuncDeclarationNode)
    def visit(self, node: FuncDeclarationNode):
        args_names = []
        args_types = []
        for name, type_ in node.params:
            if name in args_names:
                error_text = SemanticError.PARAMETER_MULTY_DEFINED % name
                self.errors.append(SemanticError(error_text, *type_.pos))
            args_names.append(name)

            try:
                arg_type = self.context.get_type(type_.value, type_.pos)
            except SemanticError:
                error_text = TypesError.PARAMETER_UNDEFINED % (type_.value, type_.value)
                self.errors.append(TypesError(error_text, *type_.pos))
                arg_type = ErrorType()
            args_types.append(arg_type)

        try:
            return_type = self.context.get_type(node.type, node.type_pos)
        except SemanticError as e:
            error_text = TypesError.RETURN_TYPE_UNDEFINED % (node.type, node.id)
            self.errors.append(TypesError(error_text, *node.type_pos))
            return_type = ErrorType(node.type_pos)

        try:
            self.current_type.define_method(node.id, args_names, args_types, return_type, node.pos)
        except SemanticError as e:
            self.errors.append(e)
