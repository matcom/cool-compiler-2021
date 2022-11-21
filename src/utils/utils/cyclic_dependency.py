from .semantic import Context, SemanticError
from utils import visitor
from utils import ast_nodes as ast

class CyclicDependency_:
    def __init__(self, context: Context, errors):
        self.context = context
        self.dic = {item: i for i, item in enumerate(self.context.types)}
        self.vertex = []
        self.adyacence_list = [[] for _ in range(len(self.dic))]
        self.errors = errors
        self.adding_edges()
        self.is_cyclic()

    def adding_edges(self):
        self.vertex = [i for i in self.dic]
        for vert in self.vertex:
            if vert in ['SELF_TYPE', 'Object', 'AUTO_TYPE']:
                continue
            parent = self.context.get_type(vert)
            parent = parent.parent
            try:
                parent = self.dic[parent.name]
            except:
                print(vert)
            self.adyacence_list[parent].append(self.dic[vert])

    def is_cyclic(self):
        try:
            self.__is_cyclic__()
        except SemanticError as e:
            self.errors.append(e.text)

    def __is_cyclic__(self):
        mark = [False for _ in range(len(self.vertex))]
        stack = [self.dic['Object']]
        dfs = 0

        while stack:
            v = stack.pop()
            mark[v] = True
            dfs += 1

            for item in self.adyacence_list[v]:
                if not mark[item]:
                    mark[item] = True
                    stack.append(item)
        
        if dfs != len(self.vertex) - 2:
            raise SemanticError('Existe un ciclo en el árbol de dependencias')


def get_tokencolumn(str, pos):
    column = 1
    temp_pos = pos
    while str[temp_pos] != '\n':
        if temp_pos == 0: break
        temp_pos -= 1
        column += 1
    return column if column > 1 else 2

def cyclicDependency(context, errors, program, program_node):
    types = context.types
    dependency_err = False
    graph = {name: [] for name in types if name not in ["AUTO_TYPE", "SELF_TYPE"]}
    class_def_list = {d.name: d for d in program_node.class_list}

    for name, typex in types.items():
        if name in ["Object", "SELF_TYPE", "AUTO_TYPE"] or typex.parent is None:
            continue
        graph[typex.parent.name].append(name)

    visited = set()
    stack = ["Object"]

    while stack:
        current_name = stack.pop()
        if current_name in visited:
            line, lexpos = class_def_list[current_name].parent_position
            errors.append(f'({line}, {get_tokencolumn(program, lexpos)}) - SemanticError: Class "{current_name}", or an ancestor of "{current_name}", is involved in an inheritance cycle')
            dependency_err = True
        visited.add(current_name)
        stack += graph[current_name]

    if len(visited) != len(graph):
        types_names = set(x for x in context.types if x not in ["SELF_TYPE", "AUTO_TYPE"])
        exclude_type_names = types_names - visited

        # look for the class in the cycle
        class_ref = max(exclude_type_names, key=lambda x: class_def_list[x].line)
        line, lexpos = class_def_list[class_ref].parent_pos
        errors.append(f'({line}, {get_tokencolumn(program, lexpos)}) - SemanticError: Class "{class_ref}", or an ancestor of "{class_ref}", is involved in an inheritance cycle')
        dependency_err = True

    return dependency_err


class MethodChecker:
    def __init__(self, context: Context, errors, program):
        self.context: Context = context
        self.current_type = None
        self.errors = errors
        self.program = program

    def get_tokencolumn(self, str, pos):
        column = 1
        temp_pos = pos
        while str[temp_pos] != '\n':
            if temp_pos == 0: break
            temp_pos -= 1
            column += 1
        return column if column > 1 else 2

    @visitor.on("node")
    def visit(self, node):
        pass

    @visitor.when(ast.ProgramNode)
    def visit(self, node: ast.ProgramNode):
        for data in node.class_list:
            self.visit(data)

    @visitor.when(ast.ClassDecNode)
    def visit(self, node: ast.ClassDecNode):
        self.current_type = self.context.get_type(node.name)

        for data in node.data:
            if isinstance(data, ast.MethodDecNode):
                self.visit(data)

    @visitor.when(ast.AttributeDecNode)
    def visit(self, node: ast.AttributeDecNode):
        try:
            attribute, owner = self.current_type.parent.get_attribute(node.name)
            line, lexpos = node.type_pos
            self.errors.append(f'({line}, {self.get_tokencolumn(self.program, lexpos)}) - SemanticError: Attribute "{attribute.name}" already defined in "{owner.name}", attributes cannot be overridden')
        except SemanticError: pass


    @visitor.when(ast.MethodDecNode)
    def visit(self, node: ast.MethodDecNode):
        current_method = self.current_type.get_method(node.name)
        try:
            original_method, _ = self.current_type.parent.get_method(
                node.name, owner=True
            )

            current_count = len(current_method.param_types)
            original_count = len(original_method.param_types)
            if current_count != original_count:
                self.errors.append(f'({node.line}, {self.get_tokencolumn(self.program, node.lexpos)}) - SemanticError: In redefinded method "{node.name}", param type "{original_count}" is different from original param type "{current_count}"')

            counter = min(original_count, current_count)
            for i in range(counter):
                curr_type = current_method.param_types[i].name
                original_type = original_method.param_types[i].name
                if curr_type != original_type:
                    line, lexpos = node.p_types_pos[i]
                    self.errors.append(self.errors.append(f'({line}, {self.get_tokencolumn(self.program, lexpos)}) - SemanticError: In redefinded method "{node.name}", param type "{curr_type}" is different from original param type "{original_method}"'))

            current_return_type = current_method.return_type.name
            original_return_type = original_method.return_type.name
            if current_return_type != original_return_type:
                line, lexpos = node.r_types_pos
                self.errors.append(f'({line}, {self.get_tokencolumn(self.program, lexpos)}) - SemanticError: In redefinded method "{node.name}", return type "{current_return_type}" is different from original return type "{original_return_type}"')
        except SemanticError:
            pass

