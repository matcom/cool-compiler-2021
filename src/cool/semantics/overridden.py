from typing import List, Dict, Optional, OrderedDict

import cool.semantics.utils.astnodes as ast
import cool.semantics.utils.errors as err
import cool.visitor as visitor
from cool.semantics.utils.scope import Context, ErrorType, Type, SemanticError


def topological_sorting(
    program_node: ast.ProgramNode, context: Context, errors: List[str]
) -> bool:
    """Set an order in the program node of de ast such that for all class A with parent B, class B is before A in the
    list, if in the process is detected a cycle an error is added to the `error` parameter

    :param program_node: Root of the first AST of the program

    :param context: Context With all collected and building types

    :param errors: The error list

    :return: a new AST where all declared class are in topological order"""

    types = context.types

    contains_dependency_errors = False
    graph: Dict[str, List[str]] = {
        name: [] for name in types if name not in ("SELF_TYPE", "AUTO_TYPE")
    }
    declarations = {d.id: d for d in program_node.declarations}

    for name, typex in types.items():
        if name in ("Object", "SELF_TYPE", "AUTO_TYPE") or typex.parent is None:
            continue
        graph[typex.parent.name].append(name)

    visited = set()
    stack = ["Object"]

    while stack:
        current_name = stack.pop()

        if current_name in visited:
            line, column = declarations[current_name].parent_position
            errors.append(
                err.CYCLIC_DEPENDENCY % (line, column, current_name, current_name)
            )
            contains_dependency_errors = True

        visited.add(current_name)
        stack += graph[current_name]

    if len(visited) != len(graph):
        types_names = set(
            x for x in context.types if x not in ("SELF_TYPE", "AUTO_TYPE")
        )
        exclude_type_names = types_names - visited

        # Select the last declared class that belongs to the cycle
        reference_class = max(exclude_type_names, key=lambda x: declarations[x].line)
        line, column = declarations[reference_class].parent_position
        errors.append(
            err.CYCLIC_DEPENDENCY % (line, column, reference_class, reference_class)
        )

        contains_dependency_errors = True

    return contains_dependency_errors


class OverriddenMethodChecker:
    """This visitor for validate the signature of the overridden methods

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
            if isinstance(feature, ast.MethodDeclarationNode):
                self.visit(feature)

    @visitor.when(ast.AttrDeclarationNode)
    def visit(self, node: ast.AttrDeclarationNode):
        try:
            attribute, owner = self.current_type.parent.get_attribute(node.id)
            self.errors.append(
                err.ATTRIBUTE_OVERRIDE_ERROR % (attribute.name, owner.name)
            )
        except SemanticError:
            pass

    @visitor.when(ast.MethodDeclarationNode)
    def visit(self, node: ast.MethodDeclarationNode):
        # TODO: Change the comparison overriding
        current_method = self.current_type.get_method(node.id)
        try:
            original_method, _ = self.current_type.parent.get_method(
                node.id, get_owner=True
            )

            current_count = len(current_method.param_types)
            original_count = len(original_method.param_types)
            if current_count != original_count:
                line, column = node.line, node.column
                self.errors.append(
                    err.METHOD_OVERRIDE_PARAM_ERROR
                    % (line, column, node.id, original_count, current_count)
                )

            count = min(original_count, current_count)
            for i in range(count):
                current_type = current_method.param_types[i].name
                original_type = original_method.param_types[i].name
                if current_type != original_type:
                    line, column = node.param_types_positions[i]
                    self.errors.append(
                        err.METHOD_OVERRIDE_PARAM_ERROR
                        % (line, column, node.id, current_type, original_method)
                    )

            current_return_type = current_method.return_type.name
            original_return_type = original_method.return_type.name
            if current_return_type != original_return_type:
                line, column = node.return_type_position
                self.errors.append(
                    err.METHOD_OVERRIDE_RETURN_ERROR
                    % (line, column, node.id, current_return_type, original_return_type)
                )
        except SemanticError:
            pass
