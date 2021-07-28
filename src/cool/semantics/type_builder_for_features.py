from typing import List, Optional

import cool.semantics.utils.astnodes as ast
import cool.semantics.utils.errors as err
import cool.visitor as visitor
from cool.semantics.utils.scope import Context, SemanticError, Type, ErrorType


class TypeBuilderForFeatures:
    """This visitor collect all the attributes and methods in classes and set the parent to the current class

    Params
    ------
    - syntactic_and_semantic_errors: List[str] is a list of syntactic_and_semantic_errors detected in the ast travel
    - context: Context the context for keeping the classes
    - current_type: Optional[Type] is the current type in the building process"""

    def __init__(self, context: Context, errors: List[str]):
        self.context: Context = context
        self.current_type: Optional[Type] = None
        self.errors: List[str] = errors

    @visitor.on("node")
    def visit(self, node):
        pass

    @visitor.when(ast.ProgramNode)
    def visit(self, node: ast.ProgramNode):
        for declaration in node.declarations:
            self.visit(declaration)

    @visitor.when(ast.ClassDeclarationNode)
    def visit(self, node: ast.ClassDeclarationNode):
        self.current_type = self.context.get_type(node.id)

        for feature in node.features:
            self.visit(feature)

    @visitor.when(ast.AttrDeclarationNode)
    def visit(self, node: ast.AttrDeclarationNode):
        try:
            attr_type = self.context.get_type(node.type)
        except SemanticError:
            attr_type = ErrorType()
            line, column = node.type_position
            self.errors.append(
                err.UNDEFINED_ATTRIBUTE_TYPE
                % (line, column, node.type, node.id, self.current_type.name)
            )

        try:
            self.current_type.define_attribute(node.id, attr_type)
        except SemanticError:
            self.errors.append(
                err.ATTRIBUTE_ALREADY_DEFINED
                % (node.line, node.column, node.id, self.current_type.name)
            )

    @visitor.when(ast.MethodDeclarationNode)
    def visit(self, node: ast.MethodDeclarationNode):
        param_names = []
        param_types = []

        for i, (name, typex) in enumerate(node.params):
            param_names.append(name)
            try:
                param_types.append(self.context.get_type(typex))
            except SemanticError:
                param_types.append(ErrorType())
                line, column = node.param_types_positions[i]
                self.errors.append(
                    err.UNDEFINED_PARAM_TYPE
                    % (line, column, typex, node.id, self.current_type.name)
                )

        try:
            return_type = self.context.get_type(node.return_type)
        except SemanticError:
            return_type = ErrorType()
            line, column = node.return_type_position
            self.errors.append(
                err.UNDEFINED_RETURN_TYPE
                % (line, column, node.return_type, node.id, self.current_type.name)
            )

        try:
            self.current_type.define_method(
                node.id, param_names, param_types, return_type
            )
        except SemanticError:
            self.errors.append(
                err.METHOD_ALREADY_DEFINED
                % (node.line, node.column, node.id, self.current_type.name)
            )
