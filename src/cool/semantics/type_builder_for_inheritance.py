from typing import List, Optional

import cool.semantics.utils.astnodes as ast
import cool.semantics.utils.errors as err
import cool.visitor as visitor
from cool.semantics.utils.scope import Context, SemanticError, Type, ErrorType


class TypeBuilderForInheritance:
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

        if node.parent is not None:
            if node.parent in ("Int", "String", "Bool", "SELF_TYPE"):
                line, column = node.parent_position
                self.errors.append(
                    err.INVALID_PARENT_TYPE % (line, column, node.id, node.parent)
                )

            try:
                parent_type = self.context.get_type(node.parent)
            except SemanticError:
                parent_type = self.context.get_type("Object")
                line, column = node.parent_position
                self.errors.append(
                    err.PARENT_UNDEFINED % (line, column, node.id, node.parent)
                )

            try:
                self.current_type.set_parent(parent_type)
            except SemanticError:
                self.errors.append(
                    err.PARENT_ALREADY_SET % (node.line, node.column, node.id)
                )

        else:
            try:
                self.current_type.set_parent(self.context.get_type("Object"))
            except SemanticError:
                if node.id not in (
                    "Int",
                    "String",
                    "Bool",
                    "IO",
                    "Object",
                    "SELF_TYPE",
                ):
                    self.errors.append(
                        err.PARENT_ALREADY_SET % (node.line, node.column, node.id)
                    )
