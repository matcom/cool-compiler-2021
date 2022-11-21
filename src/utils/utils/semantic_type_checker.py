from inspect import Attribute
from typing import Dict, List, Optional, Set, Tuple, Deque
from collections import OrderedDict, deque
from abc import ABC

import utils.ast_nodes as cool
import utils.errors as err
import utils.visitor as visitor
from utils.semantic import Context, ErrorType, Method, Scope, SemanticError, Type, VariableInfo


#### Colector de tipos inicial ####

class TypeCollector:
    def __init__(self, context: Context = Context(), errors: List[str] = []):
        self.errors: List[str] = errors
        self.context: Context = context

    @visitor.on("node")
    def visit(self, node):
        pass

    @visitor.when(cool.ProgramNode)
    def visit(self, node: cool.ProgramNode):
        self.context.create_type("AUTO_TYPE")
        self_type = self.context.create_type("SELF_TYPE")
        object_type = self.context.create_type("Object")
        io_type = self.context.create_type("IO")
        string_type = self.context.create_type("String")
        int_type = self.context.create_type("Int")
        bool_type = self.context.create_type("Bool")

        io_type.set_parent(object_type)
        string_type.set_parent(object_type)
        int_type.set_parent(object_type)
        bool_type.set_parent(object_type)

        object_type.define_method("abort", [], [], object_type)
        object_type.define_method("type_name", [], [], string_type)
        object_type.define_method("copy", [], [], self_type)

        io_type.define_method("out_string", ["x"], [string_type], self_type)
        io_type.define_method("out_int", ["x"], [int_type], self_type)
        io_type.define_method("in_string", [], [], string_type)
        io_type.define_method("in_int", [], [], int_type)

        string_type.define_method("length", [], [], int_type)
        string_type.define_method("concat", ["s"], [string_type], string_type)
        string_type.define_method(
            "substr", ["i", "l"], [int_type, int_type], string_type
        )

        for declaration in node.class_list:
            self.visit(declaration)

    @visitor.when(cool.ClassDecNode)
    def visit(self, node: cool.ClassDecNode):
        try:
            self.context.create_type(node.name)
        except SemanticError:
            self.errors.append(
                err.INVALID_REDEFINITION_CLASS % (node.line, node.lexpos, node.name)
            )


#### colector de tipos para la herencia ####

class TypeBuilderForInheritance:
    def __init__(self, context: Context, errors: List[str]):
        self.context: Context = context
        self.current_type: Optional[Type] = None
        self.errors: List[str] = errors

    @visitor.on("node")
    def visit(self, node):
        pass

    @visitor.when(cool.ProgramNode)
    def visit(self, node: cool.ProgramNode):
        for declaration in node.class_list:
            self.visit(declaration)

    @visitor.when(cool.ClassDecNode)
    def visit(self, node: cool.ClassDecNode):
        self.current_type = self.context.get_type(node.name)

        if node.parent is not None:
            if node.parent in ("Int", "String", "Bool", "SELF_TYPE"):
                line, column = node.parent_position
                self.errors.append(err.INVALID_PARENT_TYPE % (line, column, node.name, node.parent))

            try:
                parent_type = self.context.get_type(node.parent)
            except SemanticError:
                parent_type = self.context.get_type("Object")
                line, column = node.parent_position
                self.errors.append(err.PARENT_UNDEFINED % (line, column, node.name, node.parent))

            try:
                self.current_type.set_parent(parent_type)
            except SemanticError:
                self.errors.append(err.PARENT_ALREADY_SET % (node.line, node.lexpos, node.name))

        else:
            try:
                self.current_type.set_parent(self.context.get_type("Object"))
            except SemanticError:
                if node.name not in ("Int", "String", "Bool", "IO", "Object", "SELF_TYPE",):
                    self.errors.append(err.PARENT_ALREADY_SET % (node.line, node.lexpos, node.name))


#### chequeo de tipos para los features ####

class TypeBuilderForFeatures:
    def __init__(self, context: Context, errors: List[str]):
        self.context: Context = context
        self.current_type: Optional[Type] = None
        self.errors: List[str] = errors

    @visitor.on("node")
    def visit(self, node):
        pass

    @visitor.when(cool.ProgramNode)
    def visit(self, node: cool.ProgramNode):
        for declaration in node.class_list:
            self.visit(declaration)

    @visitor.when(cool.ClassDecNode)
    def visit(self, node: cool.ClassDecNode):
        self.current_type = self.context.get_type(node.name)

        for feature in node.data:
            self.visit(feature)

    @visitor.when(cool.AttributeDecNode)
    def visit(self, node: cool.AttributeDecNode):
        try:
            attr_type = self.context.get_type(node._type)
        except SemanticError:
            attr_type = ErrorType()
            line, column = node.type_position
            self.errors.append(
                err.UNDEFINED_ATTRIBUTE_TYPE
                % (line, column, node._type, node.name, self.current_type.name)
            )

        try:
            self.current_type.define_attribute(node.name, attr_type)
        except SemanticError:
            self.errors.append(err.ATTRIBUTE_ALREADY_DEFINED % (node.line, node.lexpos, node.name, self.current_type.name))

    @visitor.when(cool.MethodDecNode)
    def visit(self, node: cool.MethodDecNode):
        param_names = []
        param_types = []

        for i, (name, _type) in enumerate(node.params):
            name, typex = name, _type
            param_names.append(name)
            try:
                param_types.append(self.context.get_type(typex))
            except SemanticError:
                param_types.append(ErrorType())
                line, column = node.p_types_pos[i]
                self.errors.append(
                    err.UNDEFINED_PARAM_TYPE
                    % (line, column, typex, node.name, self.current_type.name)
                )

        try:
            return_type = self.context.get_type(node.type)
        except SemanticError:
            return_type = ErrorType()
            line, column = node.r_types_pos
            self.errors.append(
                err.UNDEFINED_RETURN_TYPE
                % (line, column, node.type, node.name, self.current_type.name)
            )

        try:
            self.current_type.define_method(
                node.name, param_names, param_types, return_type
            )
        except SemanticError:
            self.errors.append(
                err.METHOD_ALREADY_DEFINED
                % (node.line, node.lexpos, node.name, self.current_type.name)
            )


#### override zone  y orden topologico #####

def topological_sorting(program_node: cool.ProgramNode, context: Context, errors: List[str]) :
    types = context.types

    contains_dependency_errors = False
    graph: Dict[str, List[str]] = {
        name: [] for name in types if name not in ("SELF_TYPE", "AUTO_TYPE")
    }
    declarations = {d.name: d for d in program_node.class_list}

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
    def __init__(self, context: Context, errors: List[str]):
        self.context: Context = context
        self.current_type: Optional[Type] = None
        self.errors: List[str] = errors

    @visitor.on("node")
    def visit(self, node):
        pass

    @visitor.when(cool.ProgramNode)
    def visit(self, node: cool.ProgramNode):
        for declaration in node.class_list:
            self.visit(declaration)

    @visitor.when(cool.ClassDecNode)
    def visit(self, node: cool.ClassDecNode):
        self.current_type = self.context.get_type(node.name)

        for feature in node.data:
            if isinstance(feature, cool.MethodDecNode):
                self.visit(feature)

    @visitor.when(cool.AttributeDecNode)
    def visit(self, node: cool.AttributeDecNode):
        try:
            attribute, owner = self.current_type.parent.get_attribute(node.name)
            self.errors.append(
                err.ATTRIBUTE_OVERRIDE_ERROR % (attribute.name, owner.name)
            )
        except SemanticError:
            pass

    @visitor.when(cool.MethodDecNode)
    def visit(self, node: cool.MethodDecNode):
        # TODO: Change the comparison overriding
        current_method = self.current_type.get_method(node.name)
        try:
            original_method, _ = self.current_type.parent.get_method(
                node.name, owner=True
            )

            current_count = len(current_method.param_types)
            original_count = len(original_method.param_types)
            if current_count != original_count:
                line, column = node.line, node.lexpos
                self.errors.append(
                    err.METHOD_OVERRIDE_PARAM_ERROR
                    % (line, column, node.name, original_count, current_count)
                )

            count = min(original_count, current_count)
            for i in range(count):
                current_type = current_method.param_types[i].name
                original_type = original_method.param_types[i].name
                if current_type != original_type:
                    line, column = node.p_types_pos[i]
                    self.errors.append(
                        err.METHOD_OVERRIDE_PARAM_ERROR
                        % (line, column, node.name, current_type, original_method)
                    )

            current_return_type = current_method.return_type.name
            original_return_type = original_method.return_type.name
            if current_return_type != original_return_type:
                line, column = node.r_types_pos
                self.errors.append(
                    err.METHOD_OVERRIDE_RETURN_ERROR
                    % (line, column, node.name, current_return_type, original_return_type)
                )
        except SemanticError:
            pass


#### grafo de dependencias e inferencia de tipos ####

class DependencyNode:
    type: Type

    def update(self, _type: Type) -> None:
        raise NotImplementedError()

    def __repr__(self):
        return str(self)

    @property
    def is_ready(self):
        return True


class AtomNode(DependencyNode):
    def __init__(self, atom_type: Type):
        self.type: Type = atom_type

    def update(self, _type: Type) -> None:
        pass

    def __str__(self):
        return f"Atom({self.type.name})"


class VariableInfoNode(DependencyNode):
    def __init__(self, var_type: Type, variable_info: VariableInfo):
        self.type: Type = var_type
        self.variable_info: VariableInfo = variable_info

    def update(self, _type):
        self.type = self.variable_info.type = _type

    def __str__(self):
        return f"VarInfo({self.variable_info.name}, {self.type.name})"


class AttributeNode(DependencyNode):
    def __init__(self, attr_type: Type, attribute: Attribute):
        self.type: Type = attr_type
        self.attribute: Attribute = attribute

    def update(self, _type: Type) -> None:
        self.type = self.attribute.type = _type

    def __str__(self):
        return f"Attr({self.attribute.name}, {self.type.name})"


class ParameterNode(DependencyNode):
    def __init__(self, param_type: Type, method: Method, index: int):
        self.type: Type = param_type
        self.method: Method = method
        self.index: int = index

    def update(self, _type):
        self.type = self.method.param_types[self.index] = _type

    def __str__(self):
        return f"Param({self.method.name}, {self.index}, {self.type.name})"


class ReturnTypeNode(DependencyNode):
    def __init__(self, ret_type: Type, method: Method):
        self.type: Type = ret_type
        self.method: Method = method

    def update(self, _type):
        self.type = self.method.return_type = _type

    def __str__(self):
        return f"Return({self.method.name}, {self.type.name})"


class BranchedNode(DependencyNode, ABC):
    branches: List[DependencyNode] = []

    @property
    def is_ready(self) :
        return all(x.type.name != "AUTO_TYPE" for x in self.branches)


class ConditionalNode(BranchedNode):
    def __init__(self, conditional_type, then_branch, else_branch):
        self.type = conditional_type
        self.branches = [then_branch, else_branch]

    def update(self, _type: Type) :
        self.type = _type

    def __str__(self):
        return f"ConditionalNode({self.type.name})"


class CaseOfNode(BranchedNode):
    def __init__(self, _type, branches):
        self.type = _type
        self.branches = branches

    def update(self, _type: Type) :
        self.type = _type

    def __str__(self):
        return f"CaseOfNode({self.type.name})"


class DependencyGraph:
    def __init__(self):
        self.dependencies: Dict[DependencyNode, List[DependencyNode]] = OrderedDict()

    def add_node(self, node: DependencyNode):
        if node not in self.dependencies:
            self.dependencies[node] = []

    def add_edge(self, node: DependencyNode, other: DependencyNode):
        try:
            self.dependencies[node].append(other)
        except KeyError:
            self.dependencies[node] = [other]
        self.add_node(other)

    def update_dependencies(self, default_type: Type = None):
        queue: Deque[DependencyNode] = deque(
            node for node in self.dependencies if isinstance(node, AtomNode)
        )
        visited: Set[DependencyNode] = set(queue)

        while queue:
            node = queue.popleft()

            if not node.is_ready:
                continue

            for adj in self.dependencies[node]:
                if adj not in visited:
                    adj.update(node.type)
                    visited.add(adj)
                    if not isinstance(adj, BranchedNode):
                        queue.append(adj)

        for node in self.dependencies:
            if isinstance(node, BranchedNode) and node.is_ready:
                node.update(Type.multi_join([x.type for x in node.branches]))

        queue = deque(
            node
            for node in self.dependencies
            if isinstance(node, BranchedNode) and node.type.name != "AUTO_TYPE"
        )
        visited.update(queue)
        while queue:
            node = queue.popleft()
            for adj in self.dependencies[node]:
                if adj not in visited:
                    adj.update(node.type)
                    visited.add(adj)
                    queue.append(adj)

        if default_type is not None:
            for node in self.dependencies:
                if node not in visited:
                    node.update(default_type)

    def __str__(self):
        return (
            "{\n\t"
            + "\n\t".join(f"{key}: {value}" for key, value in self.dependencies.items())
            + "\n}"
        )


class InferenceChecker:
    def __init__(self, context, errors):
        self.context: Context = context
        self.errors: List[str] = errors
        self.current_type: Optional[Type] = None
        self.current_method: Optional[Method] = None

        self.variables: Dict[VariableInfo, VariableInfoNode] = {}
        self.attributes = self.build_attributes_reference(context)
        self.methods = self.build_methods_reference(context)
        self.graph = DependencyGraph()

    @staticmethod
    def build_attributes_reference(
        context: Context,
    ) -> Dict[Tuple[str, str], AttributeNode]:
        attributes = {}

        for typex in context:
            for attr in typex.attributes:
                attributes[typex.name, attr.name] = AttributeNode(attr.type, attr)

        return attributes

    @staticmethod
    def build_methods_reference(
        context: Context,
    ) -> Dict[Tuple[str, str], Tuple[List[ParameterNode], ReturnTypeNode]]:
        methods = {}

        for typex in context:
            for method in typex.methods:
                methods[typex.name, method.name] = (
                    [
                        ParameterNode(t, method, i)
                        for i, t in enumerate(method.param_types)
                    ],
                    ReturnTypeNode(method.return_type, method),
                )

        return methods

    @visitor.on("node")
    def visit(self, node, scope):
        pass

    @visitor.when(cool.ProgramNode)
    def visit(self, node: cool.ProgramNode, scope: Scope = None):
        if scope is None:
            scope = Scope()

        node.scope = scope

        for item in node.class_list:
            self.visit(item, scope.create_child())

        # print(self.graph, '\n')
        self.graph.update_dependencies(default_type=self.context.get_type("Object"))
        # print(self.graph, '\n')
        InferenceTypeSubstitute(self.context, self.errors).visit(node, scope)

    @visitor.when(cool.ClassDecNode)
    def visit(self, node: cool.ClassDecNode, scope: Scope):
        node.scope = scope
        self.current_type = self.context.get_type(node.name)

        attrs = [
            feature
            for feature in node.data
            if isinstance(feature, cool.AttributeDecNode)
        ]
        methods = [
            feature
            for feature in node.data
            if isinstance(feature, cool.MethodDecNode)
        ]

        for attr, attr_owner in self.current_type.all_attributes():
            if attr_owner != self.current_type:
                scope.define_variable(attr.name, attr.type)

        for attr in attrs:
            self.visit(attr, scope)

        for method in methods:
            self.visit(method, scope.create_child())

    @visitor.when(cool.AttributeDecNode)
    def visit(self, node: cool.AttributeDecNode, scope: Scope):
        node.scope = scope
        if node.name == "self":
            if node.expr is not None:
                scope.create_child()
            return

        scope.define_variable("self", self.current_type)

        # Solve the expression of the attribute
        expr_node = (self.visit(node.expr, scope.create_child()) if node.expr is not None else None)

        try:
            # Define attribute in the scope
            var_info = scope.define_variable(node.name, self.context.get_type(node._type))

            # Set and get the reference to the variable info node
            var_info_node = self.variables[var_info] = VariableInfoNode(
                self.context.get_type(node._type), var_info
            )

            if node._type == "AUTO_TYPE":
                # Get the reference to the attribute node
                attr_node = self.attributes[self.current_type.name, node.name]

                # If the expression node is not None then two edges are creates in the graph
                if expr_node is not None:
                    self.graph.add_edge(expr_node, var_info_node)
                    self.graph.add_edge(expr_node, attr_node)

                # Finally a cycle of two nodes is created between var_info_node and attr_node
                self.graph.add_edge(var_info_node, attr_node)
                self.graph.add_edge(attr_node, var_info_node)
        except SemanticError:
            pass

    @visitor.when(cool.MethodDecNode)
    def visit(self, node: cool.MethodDecNode, scope: Scope):
        node.scope = scope
        self.current_method = self.current_type.get_method(node.name)

        # Define 'self' as a variable in the scope
        self_var = scope.define_variable("self", self.current_type)

        # Set the reference of 'self' variable info node
        self.variables[self_var] = VariableInfoNode(self.current_type, self_var)

        param_names = self.current_method.param_names
        param_types = self.current_method.param_types

        for i, (param_name, param_type) in enumerate(zip(param_names, param_types)):
            # Define parameter as local variable in current scope
            param_var_info = scope.define_variable(param_name, param_type)

            # Set the reference to the variable info node
            param_var_info_node = self.variables[param_var_info] = VariableInfoNode(
                param_type, param_var_info
            )

            if param_type.name == "AUTO_TYPE":
                # Get the parameter node
                parameter_node = self.methods[
                    self.current_type.name, self.current_method.name
                ][0][i]

                # Create the cycle of two nodes between param_var_info_node and parameter_node
                self.graph.add_edge(param_var_info_node, parameter_node)
                self.graph.add_edge(parameter_node, param_var_info_node)

        # Solve the body of the method
        body_node = self.visit(node.expr, scope)

        if self.current_method.return_type.name == "AUTO_TYPE":
            # Get the return type node and add an edge body_node -> return_type_node
            return_type_node = self.methods[
                self.current_type.name, self.current_method.name
            ][1]
            self.graph.add_edge(body_node, return_type_node)

    @visitor.when(cool.LetNode)
    def visit(self, node: cool.LetNode, scope: Scope):
        node.scope = scope
        for _id, _type, _expr in node.declaration:
            try:
                # Define and get the var_info
                var_info = scope.define_variable(_id, self.context.get_type(_type))
            except SemanticError:
                var_info = scope.define_variable(_id, ErrorType())
            var_info_node = self.variables[var_info] = VariableInfoNode(
                var_info.type, var_info
            )

            expr_node = (self.visit(_expr, scope.create_child()) if _expr is not None else None)

            if var_info.type.name == "AUTO_TYPE":
                # Create an edge or add an new node only if it is AutoType
                if expr_node is not None:
                    self.graph.add_edge(expr_node, var_info_node)
                    if expr_node.type.name == "AUTO_TYPE":
                        self.graph.add_edge(var_info_node, expr_node)
                else:
                    self.graph.add_node(var_info_node)
            elif expr_node is not None and expr_node.type.name == "AUTO_TYPE":
                self.graph.add_edge(var_info_node, expr_node)

        return self.visit(node.expr, scope.create_child())

    @visitor.when(cool.AssignNode)
    def visit(self, node: cool.AssignNode, scope: Scope):
        node.scope = scope
        var_info = scope.find_variable(node.idx)

        expr_node = self.visit(node.expr, scope)

        if var_info is not None:
            if expr_node.type.name != "AUTO_TYPE" and var_info.type.name == "AUTO_TYPE":
                self.graph.add_edge(expr_node, self.variables[var_info])
            elif (
                var_info.type.name != "AUTO_TYPE" and expr_node.type.name == "AUTO_TYPE"
            ):
                self.graph.add_edge(
                    AtomNode(self.context.get_type(var_info.type.name)), expr_node
                )
            elif (
                var_info.type.name == "AUTO_TYPE" and expr_node.type.name == "AUTO_TYPE"
            ):
                # Create a cycle
                self.graph.add_edge(expr_node, self.variables[var_info])
                self.graph.add_edge(self.variables[var_info], expr_node)
        else:
            pass

        return expr_node
    
    @visitor.when(cool.ExprParNode)
    def visit(self, node: cool.ExprParNode, scope: Scope):
        scope = node.scope
        return self.visit(node.expr, scope)
    

    @visitor.when(cool.BlockNode)
    def visit(self, node: cool.BlockNode, scope: Scope):
        node.scope = scope
        result_node = None
        for expr in node.expr:
            result_node = self.visit(expr, scope)
        return result_node

    @visitor.when(cool.ConditionalNode)
    def visit(self, node: cool.ConditionalNode, scope: Scope):
        node.scope = scope
        if_node = self.visit(node.if_expr, scope)

        if if_node is not None and not isinstance(if_node, AtomNode):
            self.graph.add_edge(AtomNode(self.context.get_type("Bool")), if_node)

        then_node = self.visit(node.then_expr, scope)
        else_node = self.visit(node.else_expr, scope)

        if isinstance(then_node, AtomNode) and isinstance(else_node, AtomNode):
            return AtomNode(then_node.type.join(else_node.type))

        conditional_node = ConditionalNode(
            self.context.get_type("AUTO_TYPE"), then_node, else_node
        )

        if then_node is None or else_node is None:
            return conditional_node

        if isinstance(then_node, AtomNode) and not isinstance(else_node, AtomNode):
            self.graph.add_edge(then_node, else_node)
        elif not isinstance(then_node, AtomNode) and isinstance(else_node, AtomNode):
            self.graph.add_edge(else_node, then_node)
        else:
            self.graph.add_edge(then_node, else_node)
            self.graph.add_edge(else_node, then_node)
            self.graph.add_edge(conditional_node, then_node)
            self.graph.add_edge(conditional_node, else_node)

        return conditional_node

    @visitor.when(cool.WhileNode)
    def visit(self, node: cool.WhileNode, scope: Scope):
        node.scope = scope
        self.visit(node.cond, scope)
        self.visit(node.data, scope)
        return AtomNode(self.context.get_type("Object"))

    @visitor.when(cool.CaseNode)
    def visit(self, node: cool.CaseNode, scope: Scope):
        node.scope = scope
        self.visit(node.expr, scope)

        defined_nodes = []
        not_defined_nodes = []
        case_nodes = []
        for _id, _type, _expr in node.params:
            new_scope = scope.create_child()

            try:
                case_type = self.context.get_type(_type)
                var_info = new_scope.define_variable(_id, case_type)
                self.variables[var_info] = VariableInfoNode(var_info.type, var_info)
            except SemanticError:
                pass

            case_node = self.visit(_expr, new_scope)
            if isinstance(case_node, AtomNode):
                defined_nodes.append(case_node)
            else:
                not_defined_nodes.append(case_node)
            case_nodes.append(case_node)

        if any(e is not None and e.type.name == "AUTO_TYPE" for e in case_nodes):
            if defined_nodes:
                t = Type.multi_join([x.type for x in defined_nodes])
                for x in not_defined_nodes:
                    self.graph.add_edge(AtomNode(t), x)
            case_of_node = CaseOfNode(self.context.get_type("AUTO_TYPE"), case_nodes)
            self.graph.add_node(case_of_node)
            return case_of_node
        return AtomNode(Type.multi_join([e.type for e in case_nodes if e is not None]))

    @visitor.when(cool.MethodCallNode)
    def visit(self, node: cool.MethodCallNode, scope: Scope):
        node.scope = scope
        if node.atom is None:
            node.atom = cool.VariableNode("self")
        obj_node = self.visit(node.atom, scope)

        if isinstance(obj_node, AtomNode) and obj_node.type.contains_method(node.idx):
            method, owner = obj_node.type.get_method(node.idx, owner=True)
            param_nodes, return_node = self.methods[owner.name, method.name]

            count_of_args = min(len(node.exprlist), len(param_nodes))
            for i in range(count_of_args):
                arg = node.exprlist[i]
                arg_node = self.visit(arg, scope)

                if arg_node is None:
                    # Possible error
                    continue

                if isinstance(arg_node, AtomNode):
                    if param_nodes[i].type.name == "AUTO_TYPE":
                        self.graph.add_edge(arg_node, param_nodes[i])
                    else:
                        continue
                else:
                    if param_nodes[i].type.name != "AUTO_TYPE":
                        self.graph.add_edge(param_nodes[i], arg_node)
                    else:
                        self.graph.add_edge(param_nodes[i], arg_node)
                        self.graph.add_edge(arg_node, param_nodes[i])

            if return_node.type.name == "AUTO_TYPE":
                return return_node
            return AtomNode(return_node.type if return_node.type.name != "SELF_TYPE" else obj_node.type)

        for arg in node.exprlist:
            self.visit(arg, scope)
        return AtomNode(self.context.get_type("Object"))

    @visitor.when(cool.NumberNode)
    def visit(self, node: cool.NumberNode, scope: Scope):
        node.scope = scope
        return AtomNode(self.context.get_type("Int"))

    @visitor.when(cool.StringNode)
    def visit(self, node: cool.StringNode, scope: Scope):
        node.scope = scope
        return AtomNode(self.context.get_type("String"))

    @visitor.when(cool.BooleanNode)
    def visit(self, node: cool.BooleanNode, scope: Scope):
        node.scope = scope
        return AtomNode(self.context.get_type("Bool"))

    @visitor.when(cool.VariableNode)
    def visit(self, node: cool.VariableNode, scope: Scope):
        node.scope = scope
        variable = scope.find_variable(node.lex)

        if variable is not None:
            if variable.type.name == "AUTO_TYPE":
                return self.variables[variable]
            else:
                return AtomNode(variable.type)
        else:
            return None

    @visitor.when(cool.NewNode)
    def visit(self, node: cool.NewNode, scope: Scope):
        node.scope = scope
        if node.type in self.context.types:
            return AtomNode(self.context.get_type(node.type))
        return AtomNode(self.context.get_type("Object"))

    @visitor.when(cool.NegationNode)
    def visit(self, node: cool.NegationNode, scope: Scope):
        node.scope = scope
        self.visit(node.expr, scope)
        return AtomNode(self.context.get_type("Bool"))

    @visitor.when(cool.ComplementNode)
    def visit(self, node: cool.ComplementNode, scope: Scope):
        node.scope = scope
        self.visit(node.expr, scope)
        return AtomNode(self.context.get_type("Int"))

    @visitor.when(cool.IsVoidNode)
    def visit(self, node: cool.IsVoidNode, scope: Scope):
        node.scope = scope
        self.visit(node.expr, scope)
        return AtomNode(self.context.get_type("Bool"))

    @visitor.when(cool.PlusNode)
    def visit(self, node: cool.PlusNode, scope: Scope):
        node.scope = scope
        return self._visit_arithmetic_node(
            node, scope, self.context.get_type("Int"), self.context.get_type("Int")
        )

    @visitor.when(cool.MinusNode)
    def visit(self, node: cool.MinusNode, scope: Scope):
        node.scope = scope
        return self._visit_arithmetic_node(
            node, scope, self.context.get_type("Int"), self.context.get_type("Int")
        )

    @visitor.when(cool.TimesNode)
    def visit(self, node: cool.TimesNode, scope: Scope):
        node.scope = scope
        return self._visit_arithmetic_node(
            node, scope, self.context.get_type("Int"), self.context.get_type("Int")
        )

    @visitor.when(cool.DivNode)
    def visit(self, node: cool.DivNode, scope: Scope):
        node.scope = scope
        return self._visit_arithmetic_node(
            node, scope, self.context.get_type("Int"), self.context.get_type("Int")
        )

    @visitor.when(cool.LessEqualNode)
    def visit(self, node: cool.LessEqualNode, scope: Scope):
        node.scope = scope
        return self._visit_arithmetic_node(
            node, scope, self.context.get_type("Int"), self.context.get_type("Bool")
        )

    @visitor.when(cool.LessNode)
    def visit(self, node: cool.LessNode, scope: Scope):
        node.scope = scope
        return self._visit_arithmetic_node(
            node, scope, self.context.get_type("Int"), self.context.get_type("Bool")
        )

    @visitor.when(cool.EqualNode)
    def visit(self, node: cool.EqualNode, scope: Scope):
        node.scope = scope
        self.visit(node.left, scope)
        self.visit(node.right, scope)
        return AtomNode(self.context.get_type("Bool"))

    def _visit_arithmetic_node(
        self, node: cool.BinaryNode, scope: Scope, member_types: Type, return_type: Type
    ):
        left = self.visit(node.left, scope)
        right = self.visit(node.right, scope)

        if left is not None and not isinstance(left, AtomNode):
            self.graph.add_edge(AtomNode(member_types), left)

        if right is not None and not isinstance(right, AtomNode):
            self.graph.add_edge(AtomNode(member_types), right)

        return AtomNode(return_type)


class InferenceTypeSubstitute:
    def __init__(self, context: Context, errors: List[str]):
        self.context: Context = context
        self.errors: List[str] = errors
        self.current_type: Optional[Type] = None
        self.current_method: Optional[Method] = None

    @visitor.on("node")
    def visit(self, node, tabs):
        pass

    @visitor.when(cool.ProgramNode)
    def visit(self, node: cool.ProgramNode, scope: Scope):
        scope = node.scope
        for i, elem in enumerate(node.class_list):
            self.visit(elem, scope.children[i])
        return scope

    @visitor.when(cool.ClassDecNode)
    def visit(self, node: cool.ClassDecNode, scope: Scope):
        scope = node.scope
        self.current_type = self.context.get_type(node.name)

        attrs = [feature for feature in node.data if isinstance(feature, cool.AttributeDecNode)]
        methods = [feature for feature in node.data if isinstance(feature, cool.MethodDecNode)]

        i = 0
        for attr in attrs:
            if attr.expr is not None:
                attr.index = i
                i += 1

            self.visit(attr, scope)

        # print(scope.children, len(methods), i)
        for i, method in enumerate(methods, start=i):
            self.visit(method, scope.children[i])

    @visitor.when(cool.AttributeDecNode)
    def visit(self, node: cool.AttributeDecNode, scope: Scope):
        scope = node.scope
        try:
            attr_type = self.context.get_type(node._type)
            var_info = scope.find_variable(node.name)

            if node.expr is not None:
                self.visit(node.expr, scope.children[node.index])

            if attr_type == self.context.get_type("AUTO_TYPE"):
                if var_info.type == self.context.get_type("AUTO_TYPE"):
                    self.errors.append(err.INFERENCE_ERROR_ATTRIBUTE % node.name)
                node._type = var_info.type.name
        except SemanticError:
            pass

    @visitor.when(cool.MethodDecNode)
    def visit(self, node: cool.MethodDecNode, scope: Scope):
        scope = node.scope
        self.current_method = self.current_type.get_method(node.name)

        try:
            return_type = self.context.get_type(node.type)
        except SemanticError:
            return_type = None

        for i, (name, _type) in enumerate(node.params):
            name, _ = name, _type
            variable_info = scope.find_variable(name)
            if variable_info.type == self.context.get_type("AUTO_TYPE"):
                self.errors.append(
                    err.INFERENCE_ERROR_ATTRIBUTE
                    % (
                        node.p_types_pos[i][0],
                        node.p_types_pos[i][1],
                        name,
                    )
                )
            node.params[i] = (name, variable_info.type.name)

        self.visit(node.expr, scope)

        if return_type is not None and return_type == self.context.get_type(
            "AUTO_TYPE"
        ):
            if self.current_method.return_type == self.context.get_type("AUTO_TYPE"):
                self.errors.append(err.INFERENCE_ERROR_ATTRIBUTE % node.name)
            node.type = self.current_method.return_type.name

    @visitor.when(cool.LetNode)
    def visit(self, node: cool.LetNode, scope: Scope):
        scope = node.scope
        child_index = 0
        for i, (_id, _type, _expr) in enumerate(node.declaration):
            variable_info = scope.find_variable(_id)

            if _expr is not None:
                self.visit(_expr, scope.children[child_index])
                child_index += 1

            if _type == "AUTO_TYPE":
                if variable_info.type == self.context.get_type("AUTO_TYPE"):
                    self.errors.append(err.INFERENCE_ERROR_ATTRIBUTE % _id)
                node.class_list[i] = (_id, variable_info.type.name, _expr)

        self.visit(node.expr, scope.children[child_index])

    @visitor.when(cool.AssignNode)
    def visit(self, node: cool.AssignNode, scope: Scope):
        scope = node.scope
        self.visit(node.expr, scope)

    @visitor.when(cool.BlockNode)
    def visit(self, node: cool.BlockNode, scope: Scope):
        scope = node.scope
        for _, expr in enumerate(node.expr):
            self.visit(expr, scope)

    @visitor.when(cool.ConditionalNode)
    def visit(self, node: cool.ConditionalNode, scope: Scope):
        scope = node.scope
        self.visit(node.if_expr, scope)
        self.visit(node.then_expr, scope)
        self.visit(node.else_expr, scope)

    @visitor.when(cool.WhileNode)
    def visit(self, node: cool.WhileNode, scope: Scope):
        scope = node.scope
        self.visit(node.cond, scope)
        self.visit(node.data, scope)

    @visitor.when(cool.CaseNode)
    def visit(self, node: cool.CaseNode, scope: Scope):
        scope = node.scope
        self.visit(node.expr, scope)
        for i, (_, _, _expr) in enumerate(node.params):
            self.visit(_expr, scope.children[i])

    @visitor.when(cool.MethodCallNode)
    def visit(self, node: cool.MethodCallNode, scope: Scope):
        scope = node.scope
        self.visit(node.atom, scope)

        for arg in node.exprlist:
            self.visit(arg, scope)

    @visitor.when(cool.AtomicNode)
    def visit(self, node: cool.AtomicNode, scope: Scope):
        scope = node.scope
        # pass

    @visitor.when(cool.UnaryNode)
    def visit(self, node: cool.UnaryNode, scope: Scope):
        scope = node.scope
        self.visit(node.expr, scope)

    @visitor.when(cool.BinaryNode)
    def visit(self, node: cool.BinaryNode, scope: Scope):
        scope = node.scope
        self.visit(node.left, scope)
        self.visit(node.right, scope)


#### Chequeo de tipos ####

class TypeChecker:
    def __init__(self, context: Context, errors: List[str]):
        self.context: Context = context
        self.errors: List[str] = errors
        self.current_type: Optional[Type] = None
        self.current_method: Optional[Method] = None
        self.current_attribute: Optional[Attribute] = None

    @visitor.on("node")
    def visit(self, node, scope):
        pass

    @visitor.when(cool.ProgramNode)
    def visit(self, node: cool.ProgramNode, scope: Scope = None):
        if scope is None:
            scope = Scope()

        node.scope = scope

        for elem in node.class_list:
            self.visit(elem, scope.create_child())

        return scope

    @visitor.when(cool.ClassDecNode)
    def visit(self, node: cool.ClassDecNode, scope: Scope):
        node.scope = scope
        self.current_type = self.context.get_type(node.name)

        attrs = [
            feature
            for feature in node.data
            if isinstance(feature, cool.AttributeDecNode)
        ]
        methods = [
            feature
            for feature in node.data
            if isinstance(feature, cool.MethodDecNode)
        ]

        for attr, attr_owner in self.current_type.all_attributes():
            if attr_owner != self.current_type:
                scope.define_variable(attr.name, attr.type)

        for attr in attrs:
            self.visit(attr, scope)

        for method in methods:
            self.visit(method, scope.create_child())

    @visitor.when(cool.AttributeDecNode)
    def visit(self, node: cool.AttributeDecNode, scope: Scope):
        node.scope = scope
        if node.name == "self":
            self.errors.append(err.SELF_INVALID_ATTRIBUTE_ID % (node.line, node.lexpos))

        try:
            attr_type = (
                self.context.get_type(node._type)
                if node._type != "SELF_TYPE"
                else self.current_type
            )
        except SemanticError:
            attr_type = ErrorType()

        scope.define_variable("self", self.current_type)

        # set the current attribute for analyze the body
        # and set the self.current_method variable to None
        self.current_attribute = self.current_type.get_attribute(node.name)
        self.current_method = None

        if node.expr is not None:
            expr_type = self.visit(node.expr, scope.create_child())
            if not expr_type.conforms_to(attr_type):
                line, column = node.expr_position
                self.errors.append(
                    err.INCOMPATIBLE_TYPES
                    % (line, column, expr_type.name, attr_type.name)
                )
        scope.define_variable(node.name, attr_type)

    @visitor.when(cool.MethodDecNode)
    def visit(self, node: cool.MethodDecNode, scope: Scope):
        node.scope = scope
        self.current_method = self.current_type.get_method(node.name)
        self.current_attribute = None

        scope.define_variable("self", self.current_type)

        for param_name, param_type in zip(
            self.current_method.param_names, self.current_method.param_types
        ):
            if not scope.is_local_variable(param_name):
                if param_type.name == "SELF_TYPE":
                    self.errors.append(err.INVALID_PARAM_TYPE % "SELF_TYPE")
                    scope.define_variable(param_name, ErrorType())
                else:
                    try:
                        scope.define_variable(
                            param_name, self.context.get_type(param_type.name)
                        )
                    except SemanticError:
                        scope.define_variable(param_name, ErrorType())
            else:
                self.errors.append(
                    err.LOCAL_ALREADY_DEFINED
                    % (node.line, node.lexpos, param_name, self.current_method.name)
                )

        try:
            return_type = (
                self.context.get_type(node.type)
                if node.type != "SELF_TYPE"
                else self.current_type
            )
        except SemanticError:
            return_type = ErrorType()

        expr_type = self.visit(node.expr, scope)

        if not expr_type.conforms_to(return_type):
            self.errors.append(
                err.INCOMPATIBLE_TYPES
                % (node.line, node.lexpos, expr_type.name, return_type.name)
            )

    # @visitor.when(cool.LetNode)
    # def visit(self, node: cool.LetNode, scope: Scope):
    #     node.scope = scope
    #     return self.visit(node.expr, scope)    

    @visitor.when(cool.LetNode)
    def visit(self, node: cool.LetNode, scope: Scope):
        node.scope = scope
        for i, (_id, _type, _expr) in enumerate(node.declaration):
            if _id == "self":
                line, column = node.dec_names_pos[i]
                self.errors.append(err.SELF_USED_IN_LET % (line, column))
                continue

            try:
                var_static_type = (
                    self.context.get_type(_type)
                    if _type != "SELF_TYPE"
                    else self.current_type
                )
            except SemanticError:
                line, column = node.dec_types_pos[i]
                self.errors.append(err.UNDEFINED_TYPE % (line, column, _type))
                var_static_type = ErrorType()

            scope.define_variable(_id, var_static_type)

            expr_type = (
                self.visit(_expr, scope.create_child()) if _expr is not None else None
            )
            if expr_type is not None and not expr_type.conforms_to(var_static_type):
                self.errors.append(
                    err.INCOMPATIBLE_TYPES
                    % (node.line, node.lexpos, expr_type.name, var_static_type.name)
                )

        return self.visit(node.expr, scope.create_child())

    @visitor.when(cool.AssignNode)
    def visit(self, node: cool.AssignNode, scope: Scope):
        node.scope = scope
        var_info = scope.find_variable(node.idx)

        if var_info.name == "self":
            self.errors.append(err.SELF_IS_READONLY % (node.line, node.lexpos))

        expr_type = self.visit(node.expr, scope)

        if var_info is None:
            self.errors.append(
                err.UNDEFINED_VARIABLE
                % (node.line, node.lexpos, node.idx, self.current_method.name)
            )
        else:
            if not expr_type.conforms_to(var_info.type):
                self.errors.append(
                    err.INCOMPATIBLE_TYPES
                    % (node.line, node.lexpos, expr_type.name, var_info.type.name)
                )

        return expr_type

    @visitor.when(cool.BlockNode)
    def visit(self, node: cool.BlockNode, scope: Scope):
        node.scope = scope
        return_type = ErrorType()
        for expr in node.expr:
            return_type = self.visit(expr, scope)
        return return_type

    @visitor.when(cool.ConditionalNode)
    def visit(self, node: cool.ConditionalNode, scope: Scope):
        node.scope = scope
        if_type = self.visit(node.if_expr, scope)
        then_type = self.visit(node.then_expr, scope)
        else_type = self.visit(node.else_expr, scope)
        if if_type != self.context.get_type("Bool"):
            self.errors.append(
                err.INCOMPATIBLE_TYPES % (node.line, node.lexpos, if_type.name, "Bool")
            )
        return then_type.join(else_type)

    @visitor.when(cool.WhileNode)
    def visit(self, node: cool.WhileNode, scope: Scope):
        node.scope = scope
        condition = self.visit(node.cond, scope)
        if condition != self.context.get_type("Bool"):
            self.errors.append(
                err.INCOMPATIBLE_TYPES
                % (node.line, node.lexpos, condition.name, "Bool")
            )

        self.visit(node.data, scope)
        return self.context.get_type("Object")

    @visitor.when(cool.CaseNode)
    def visit(self, node: cool.CaseNode, scope: Scope):
        node.scope = scope
        self.visit(node.expr, scope)
        types = []
        visited = set()
        for i, (identifier, type_name, expr) in enumerate(node.params):
            new_scope = scope.create_child()
            try:
                if type_name != "SELF_TYPE":
                    new_scope.define_variable(
                        identifier, self.context.get_type(type_name)
                    )
                else:
                    self.errors.append(err.INVALID_CASE_TYPE % type_name)
            except SemanticError:
                new_scope.define_variable(identifier, ErrorType())
                line, column = node.cases_positions[i]
                self.errors.append(
                    err.UNDEFINED_TYPE_IN_BRANCH % (line, column, type_name)
                )

            # Cannot be duplicated Branches types
            if type_name in visited:
                line, column = node.cases_positions[i]
                self.errors.append(
                    err.DUPLICATE_BARNCH_IN_CASE % (line, column, type_name)
                )

            visited.add(type_name)
            types.append(self.visit(expr, new_scope))

        return Type.multi_join(types)

    @visitor.when(cool.MethodCallNode)
    def visit(self, node: cool.MethodCallNode, scope: Scope):
        node.scope = scope
        if node.atom is None:
            node.atom = cool.VariableNode("self")
        obj_type = self.visit(node.atom, scope)

        if node.type is not None:
            try:
                ancestor_type = self.context.get_type(node.type)
            except SemanticError:
                ancestor_type = ErrorType()
                line, column = node.type_position
                self.errors.append(err.UNDEFINED_TYPE % (line, column, node.type))

            if not obj_type.conforms_to(ancestor_type):
                line, column = node.type_position
                self.errors.append(
                    err.INVALID_ANCESTOR
                    % (line, column, obj_type.name, ancestor_type.name)
                )
        else:
            ancestor_type = obj_type

        try:
            method = ancestor_type.get_method(node.idx)
        except SemanticError:
            line, column = node.id_position
            self.errors.append(
                err.DISPATCH_UNDEFINED_METHOD % (line, column, node.idx, obj_type.name)
            )

            for arg in node.exprlist:
                self.visit(arg, scope)
            return ErrorType()

        args_count = len(node.exprlist)
        params_count = len(method.param_names)
        if args_count != params_count:
            line, column = node.id_position
            self.errors.append(
                err.DISPATCH_WITH_WRONG_NUMBER_OF_ARGS
                % (line, column, method.name, obj_type.name, params_count, args_count)
            )

        number_of_args = min(args_count, params_count)
        for i, arg in enumerate(node.exprlist[:number_of_args]):
            arg_type = self.visit(arg, scope)
            if not arg_type.conforms_to(method.param_types[i]):
                line, column = node.exprlist_positions[i]
                self.errors.append(
                    err.INCOMPATIBLE_TYPES
                    % (
                        line,
                        column,
                        arg_type.name,
                        method.param_types[i].name,
                    )
                )

        return (
            method.return_type
            if method.return_type.name != "SELF_TYPE"
            else ancestor_type
        )

    @visitor.when(cool.NumberNode)
    def visit(self, node: cool.NumberNode, scope: Scope):
        node.scope = scope
        return self.context.get_type("Int")

    @visitor.when(cool.StringNode)
    def visit(self, node: cool.StringNode, scope: Scope):
        node.scope = scope
        return self.context.get_type("String")

    @visitor.when(cool.BooleanNode)
    def visit(self, node: cool.BooleanNode, scope: Scope):
        node.scope = scope
        return self.context.get_type("Bool")

    @visitor.when(cool.VariableNode)
    def visit(self, node: cool.VariableNode, scope: Scope):
        node.scope = scope
        variable = scope.find_variable(node.lex)
        if variable is None:
            if self.current_attribute is not None:
                name = self.current_attribute.name
            else:
                name = self.current_method.name

            self.errors.append(
                err.UNDEFINED_VARIABLE % (node.line, node.lexpos, node.lex, name)
            )
            return ErrorType()
        return variable.type

    @visitor.when(cool.NewNode)
    def visit(self, node: cool.NewNode, scope: Scope):
        node.scope = scope
        try:
            return (
                self.context.get_type(node.type)
                if node.type != "SELF_TYPE"
                else self.current_type
            )
        except SemanticError as e:
            line, column = node.type_position
            self.errors.append(err.UNDEFINED_NEW_TYPE % (line, column, node.type))
            return ErrorType()

    @visitor.when(cool.NegationNode)
    def visit(self, node: cool.NegationNode, scope: Scope):
        node.scope = scope
        return self._check_unary_operation(
            node, scope, "not", self.context.get_type("Bool")
        )

    @visitor.when(cool.ComplementNode)
    def visit(self, node: cool.ComplementNode, scope: Scope):
        node.scope = scope
        return self._check_unary_operation(
            node, scope, "~", self.context.get_type("Int")
        )

    @visitor.when(cool.IsVoidNode)
    def visit(self, node: cool.IsVoidNode, scope: Scope):
        node.scope = scope
        self.visit(node.expr, scope)
        return self.context.get_type("Bool")

    @visitor.when(cool.PlusNode)
    def visit(self, node: cool.PlusNode, scope: Scope):
        node.scope = scope
        return self._check_int_binary_operation(
            node, scope, "+", self.context.get_type("Int")
        )

    @visitor.when(cool.MinusNode)
    def visit(self, node: cool.MinusNode, scope: Scope):
        node.scope = scope
        return self._check_int_binary_operation(
            node, scope, "-", self.context.get_type("Int")
        )

    @visitor.when(cool.TimesNode)
    def visit(self, node: cool.TimesNode, scope: Scope):
        node.scope = scope
        return self._check_int_binary_operation(
            node, scope, "*", self.context.get_type("Int")
        )

    @visitor.when(cool.DivNode)
    def visit(self, node: cool.DivNode, scope: Scope):
        node.scope = scope
        return self._check_int_binary_operation(
            node, scope, "/", self.context.get_type("Int")
        )

    @visitor.when(cool.LessEqualNode)
    def visit(self, node: cool.LessEqualNode, scope: Scope):
        node.scope = scope
        return self._check_int_binary_operation(
            node, scope, "<=", self.context.get_type("Bool")
        )

    @visitor.when(cool.LessNode)
    def visit(self, node: cool.LessNode, scope: Scope):
        node.scope = scope
        return self._check_int_binary_operation(
            node, scope, "<", self.context.get_type("Bool")
        )

    @visitor.when(cool.EqualNode)
    def visit(self, node: cool.EqualNode, scope: Scope):
        node.scope = scope
        left_type = self.visit(node.left, scope)
        right_type = self.visit(node.right, scope)

        basic_types = ("Int", "String", "Bool")
        if (
            left_type.name in basic_types or left_type.name in basic_types
        ) and left_type.name != right_type.name:
            self.errors.append(
                err.INVALID_EQ_COMPARISON_OPERATION % (node.line, node.lexpos)
            )
        return self.context.get_type("Bool")

    def _check_int_binary_operation(
        self, node: cool.BinaryNode, scope: Scope, operation: str, return_type: Type
    ):
        left_type = self.visit(node.left, scope)
        right_type = self.visit(node.right, scope)

        if left_type == right_type == self.context.get_type("Int"):
            return return_type
        self.errors.append(
            err.INVALID_BINARY_OPERATION
            % (node.line, node.lexpos, operation, left_type.name, right_type.name)
        )
        return ErrorType()

    def _check_unary_operation(
        self, node: cool.UnaryNode, scope: Scope, operation: str, expected_type: Type
    ):
        typex = self.visit(node.expr, scope)
        if typex == expected_type:
            return typex
        self.errors.append(
            err.INVALID_UNARY_OPERATION
            % (node.line, node.lexpos, operation, typex.name)
        )
        return ErrorType()
