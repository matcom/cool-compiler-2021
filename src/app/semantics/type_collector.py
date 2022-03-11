from app.parser.ast import AstNode, ClassNode, ProgramNode
from app.semantics.tools import Context, SelfType
from app.semantics.tools.errors import SemanticError
import app.shared.visitor as visitor

from .constants import *


class TypeCollector:
    def __init__(self) -> None:
        self.context = Context()
        self.errors = []
        self.type_graph = {
            "Object": [*FORBIDDEN_INHERITANCE_TYPES.union({IO_TYPE})],
            "IO": [],
            "String": [],
            "Int": [],
            "Bool": [],
        }
        self.node_dict = dict()

    @visitor.on("node")
    def visit(self, node):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node: ProgramNode):
        self.context = Context()
        self.build_built_in()
        [self.visit(class_def) for class_def in node.classes]

        node.classes = self.get_type_hierarchy()
        self.context.type_graph = self.type_graph

    @visitor.when(ClassNode)
    def visit(self, node: ClassNode):
        self.node_dict[node.id] = node
        if not node.id in self.type_graph:
            self.type_graph[node.id] = []

        if node.parent:
            self._check_parent(node)
        else:
            node.parent = OBJECT_TYPE
            self.type_graph[OBJECT_TYPE].append(node.id)

        # Register type in context
        try:
            self.context.create_type(node.id)
        except SemanticError as e:
            self.add_error(node, e.text)
            return

    def _check_parent(self, node):
        if node.parent in FORBIDDEN_INHERITANCE_TYPES:
            self.add_error(node, SemanticError(
                "'{}' cannot inherit from '{}'".format(
                    node.id, node.parent)
            ).text)
        if node.parent in self.type_graph:
            self.type_graph[node.parent].append(node.id)
        else:
            self.type_graph[node.parent] = [node.id]

    def get_type_hierarchy(self):
        visited = set([OBJECT_TYPE])
        hierarchy = []
        errors = []
        self.dfs_type_graph(OBJECT_TYPE, self.type_graph,
                            visited, hierarchy, 1)
        for node in self.type_graph:
            if node in visited:
                continue
            visited.add(node)
            path = [node]
            err = self.check_circular_heritage(
                node, self.type_graph, path, visited)
            if err is not None:
                errors.append(
                    (path[1 if len(path) - 1 else 0], err)
                )
            for node in path:
                if not node in self.node_dict:
                    continue
                hierarchy = [*hierarchy, self.node_dict[node]]

        for node_id, err in errors:
            self.add_error(
                self.node_dict[node_id], "SemanticError: Circular dependency detected: " + err
            )

        return hierarchy

    def dfs_type_graph(self, root, graph, visited: set, new_order, index):
        if not root in graph:
            return

        for node in graph[root]:
            if node in visited:
                continue
            visited.add(node)
            if node not in ALL_BUILT_IN_TYPES:
                new_order.append(self.node_dict[node])
            self.context.get_type(node, unpacked=True).index = index
            self.dfs_type_graph(node, graph, visited, new_order, index + 1)

    def _check_node(self, node, root, graph, path, visited):
        if node in path:
            return " inherits from ".join(child for child in path + [path[0]])

        visited.add(node)
        path.append(node)
        return self.check_circular_heritage(node, graph, path, visited)

    def check_circular_heritage(self, root, graph, path, visited):
        nodes_len = len(graph[root])
        current_index = 0
        while(current_index < nodes_len):
            node = graph[root][current_index]
            current_index += 1
            return self._check_node(node, root, graph, path, visited)

    def build_built_in(self):
        self.context.create_type(OBJECT_TYPE).index = 0
        for type_name in ALL_BUILT_IN_TYPES - {OBJECT_TYPE}:
            self.context.create_type(type_name)

    def add_error(self, node: AstNode, message: str):
        self.errors.append(f"({node.lineno}, {node.columnno}) - " + message)
