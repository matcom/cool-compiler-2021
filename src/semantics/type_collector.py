import semantics.visitor as visitor
from parsing.ast import Node, ProgramNode, ClassDeclarationNode
from semantics.tools import SemanticError
from semantics.tools import Context

class TypeCollector(object):
    def __init__(self) -> None:
        self.context = Context()
        self.errors = []
        self.type_graph = {"Object":["IO", "String", "Int", "Bool"], "IO":[], "String":[], "Int":[], "Bool":[]}
        self.node_dict = dict()

    @visitor.on('node')
    def visit(self, node):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node):
        self.context = Context()
        self.init_default_classes()

        for class_def in node.declarations:
            self.visit(class_def)

        new_declarations = self.get_type_hierarchy()
        node.declarations = new_declarations
        self.context.type_graph = self.type_graph

    @visitor.when(ClassDeclarationNode)
    def visit(self, node):
        try:
            self.context.create_type(node.id)
            self.type_graph[node.id] = []
            self.node_dict[node.id] = node
            if node.parent:
                if node.parent in {'String', 'Int, Bool'}:
                    raise SemanticError(f"Type \'{node.id}\' cannot inherit from \'{node.parent}\' beacuse is forbidden.")
                try:
                    self.type_graph[node.parent].append(node.id)
                except KeyError:
                    self.type_graph[node.parent] = [node.id]
            else:
                node.parent = "Object"
                self.type_graph["Object"].append(node.id)
        except SemanticError as error:
            self.add_error(node, error.text)
    
    def get_type_hierarchy(self):
        visited = set(["Object"])
        new_order = []
        self.dfs_type_graph("Object", self.type_graph, visited, new_order, 1)

        circular_heritage_errors = []
        for node in self.type_graph:
            if not node in visited:
                visited.add(node)
                path = [node]
                circular_heritage_errors.append(self.check_circular_heritage(node, self.type_graph, path, visited))
                new_order = new_order + [self.context.get_type(node) for node in path]
            
        if circular_heritage_errors:
            print(circular_heritage_errors)
            error = "Semantic Error: Circular Heritage:\n"
            error += "\n".join(err for err in circular_heritage_errors)
            self.add_error(None, error)

        return new_order

    def dfs_type_graph(self, root, graph, visited:set, new_order, index):
        if not root in graph:
            return
        
        for node in graph[root]:
            if node in visited:
                continue
            visited.add(node)
            if node not in {"Int", "String", "IO", "Bool", "Object"}:
                new_order.append(self.node_dict[node])
            self.context.get_type(node).index = index
            self.dfs_type_graph(node, graph, visited, new_order, index + 1)
    
    def check_circular_heritage(self, root, graph, path, visited):
        for node in graph[root]:
            if node in path:
                return ' -> '.join(child for child in visited + [visited[0]])

            visited.add(node)
            path.append(node)
            return self.check_circular_heritage(node, graph, path, visited)

    def init_default_classes(self):
        self.context.create_type('Object').index = 0
        self.context.create_type('String')
        self.context.create_type('Int')
        self.context.create_type('IO')
        self.context.create_type('Bool')
    
    def add_error(self, node, text:str):
        line, col = node.get_position() if node else 0, 0
        self.errors.append(f"Line: {line} Col: {col} " + text)