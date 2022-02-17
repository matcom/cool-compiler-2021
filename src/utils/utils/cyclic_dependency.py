from .semantic import Context, SemanticError

class CyclicDependency:
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

