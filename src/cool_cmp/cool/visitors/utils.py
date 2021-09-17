def build_graph_list(type_list):
    graph = { x:[x.parent,] for x in type_list }
    for x in graph:
        if graph[x][0] is None or graph[x][0] not in type_list:
            graph[x] = []
    return graph

def reverse_graph(graph):
    graph = { x:y.copy() for x,y in graph.items() }
    reverse = { x:[] for x in graph }
    for x,y in graph.items():
        for z in y:
            reverse_list = reverse.get(z, [])
            if x not in reverse_list:
                reverse_list.append(x)
            reverse[z] = reverse_list
    return reverse

def build_graph_dict(context_types):
    graph = { y:[y.parent,] for x,y in context_types.items() }
    for x in graph:
        if graph[x][0] is None:
            graph[x] = []
    return graph


def dfs(graph, node=None):
    d = dict()
    f = dict()
    time = [0]
    if node:
        d[node] = time[0]; time[0]+=1
        _dfs(graph, node, d, f, time)
        f[node] = time[0]; time[0]+=1
    else:
        for node in graph:
            if node not in d:
                d[node] = time[0]; time[0]+=1
                _dfs(graph, node, d, f, time)
                f[node] = time[0]; time[0]+=1
    return d,f
        
def _dfs(graph, node, d, f, time):
    for adj in graph[node]:
        if adj not in d:
            d[adj] = time[0]; time[0]+=1
            _dfs(graph,adj,d,f,time)
            f[adj] = time[0]; time[0]+=1

def any_cycles(graph, return_sort=False):
    d,f,time,stack,cycles = { x:0 for x in graph },{ x:0 for x in graph },[1], [], []
    for x in graph:
        if not d[x]:
            d[x] = time[0]; time[0]+=1
            topological_order(graph,x,d,f,time,stack,cycles)
            f[x] = time[0]; time[0]+=1
            stack.append(x)
    if return_sort:
        stack.reverse()
        return cycles, stack
    return cycles


def topological_order(graph,node,d,f,time,stack,cycles):

    for adj in graph[node]:
        if not d[adj]:
            d[adj] = time[0]; time[0]+=1
            topological_order(graph,adj,d,f,time,stack,cycles)
            f[adj] = time[0]; time[0]+=1
            stack.append(adj)
        elif not f[adj]:
            cycles.append((node,adj))
            
def set_permutation(*iterables):
    if len(iterables) == 1:
        for x in iterables[0]:
            yield [x]
    else:
        permutations = [x for x in set_permutation(*iterables[1:])]
        for value in iterables[0]:
            for permutation in permutations:
                yield [value] + permutation