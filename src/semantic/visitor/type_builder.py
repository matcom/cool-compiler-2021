from semantic.tools.error import SemanticError, SemanticException, circular_dependency_, attr_not_exist_, invalid_return_type_, param_not_exist_, inherits_builtin_type, main_method_not_exist_, Main_not_defined_
from semantic.tools.type import Error_Type
from nodes import ProgramNode, ClassNode, ClassMethodNode, AttrInitNode, AttrDefNode
from semantic.visitor import visitor


class TypeBuilder:
    def __init__(self, context, errors=[]):
        self.context = context
        self.current_type = None
        self.errors = errors
        self.sort = []  # topologic sort for types
        self.visited = {key: False for key in self.context.graph.keys()} # types visited by dfs               

    @visitor.on('node')
    def visit(self, node):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node):
        self.topological_sort()
        for t in self.sort:
            if t not in ['Object', 'Int', 'String', 'Bool', 'IO']:
                try:
                    class_node = self.context.classes[t]
                except KeyError:
                    pass
                else:
                    self.visit(class_node)
        if not self.context.types.__contains__('Main'):
            error = SemanticError(Main_not_defined_, 0, 0,'TypeError')
            self.errors.append(error)
        else:
            if not self.context.types['Main'].methods.__contains__('main'):
                main_node = self.context.classes['Main']
                error = SemanticError(main_method_not_exist_, main_node.row, main_node.col,'AttributeError')
                self.errors.append(error)


    @visitor.when(ClassNode)
    def visit(self, node):
        try:
            self.current_type = self.context.get_type(node.name)
            if node.parent:
                try:
                    parent = self.context.get_type(node.parent)
                except SemanticException as e:
                    error = SemanticError(e.text, node.row, node.col, 'TypeError')
                    self.errors.append(error)
                    parent = Error_Type()
                    self.current_type.set_parent(parent)
                else:
                    if parent.name in ['Int', 'String', 'Bool']:
                        parent = Error_Type()
                        error = SemanticError(inherits_builtin_type.replace("%s", node.name, 1), node.row, node.col)
                        self.errors.append(error)
                    self.current_type.set_parent(parent)

        except SemanticException as e:
            error = SemanticError(e.text, node.row, node.col, 'TypeError')
            self.errors.append(error)

        for f in node.features:
            self.visit(f)

    @visitor.when(ClassMethodNode)
    def visit(self, node):
        try:
            param_names = []
            param_types = []
            for p in node.params:
                param_names.append(p.name)
                try:
                    param_type = self.context.get_type(p.param_type)
                except SemanticException:
                    param_type = Error_Type()
                    error = SemanticError(param_not_exist_.replace("%s", p.name, 1).replace("%s", node.name, 1).replace("%s", self.current_type.name, 1), node.row, node.col, 'TypeError')
                    self.errors.append(error)
                    
                param_types.append(param_type)

            try:
                return_type = self.context.get_type(node.return_type)
            except SemanticException:
                return_type = Error_Type()
                error = SemanticError(invalid_return_type_.replace( "%s", node.return_type, 1).replace("%s", node.name, 1).replace("%s", self.current_type.name, 1), node.row, node.col, 'TypeError')
                self.errors.append(error)

            self.current_type.define_method(
                node.name, param_names, param_types, return_type)
        except SemanticException as e:
            error = SemanticError(e.text, node.row, node.col)
            self.errors.append(error)

    @visitor.when(AttrInitNode)
    def visit(self, node):
        try:
            attr_type = self.context.get_type(node.attr_type)
        except SemanticException:
            attr_type = Error_Type()
            error = SemanticError(attr_not_exist_.replace( "%s", node.name, 1).replace("%s", self.current_type.name, 1), node.row, node.col, 'TypeError')
            self.errors.append(error)
        try:
            self.current_type.define_attribute(node.name, attr_type)
        except SemanticException as e:
            error = SemanticError(e.text, node.row, node.col)
            self.errors.append(error)

    @visitor.when(AttrDefNode)
    def visit(self, node):
        try:
            attr_type = self.context.get_type(node.attr_type)
        except SemanticException:
            attr_type = Error_Type()
            error = SemanticError(attr_not_exist_.replace( "%s", node.name, 1).replace("%s", self.current_type.name, 1), node.row, node.col, 'TypeError')
            self.errors.append(error)
        try:
            self.current_type.define_attribute(node.name, attr_type)
        except SemanticException as e:
            error = SemanticError(e.text, node.row, node.col)
            self.errors.append(error)


    def dfs(self, actual_type):
        self.sort.append(actual_type)
        self.visited[actual_type] = True
        for children in self.context.graph[actual_type]:
            self.dfs(children)

    def topological_sort(self):
        indeg = {key: 0 for key in self.context.graph.keys()}
        for u in self.context.graph.keys():
            for v in self.context.graph[u]:
                indeg[v] += 1

        roots = [key for key in indeg.keys() if indeg[key] == 0]

        for v in roots:
            self.dfs(v)
        
        visited = [x for x in self.visited]
        visited.reverse()
        for t in visited:
            if not self.visited[t] and not t in ['Object', 'Int', 'String', 'Bool', 'IO']:
                class_node = self.context.classes[t]
                error = SemanticError(circular_dependency_.replace('%s', t, 1), class_node.row, class_node.col)
                self.errors.append(error)
                break
