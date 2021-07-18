from typing import List, Tuple, Dict

Graph = Dict[str,List[str]]

def build_graph_list(type_list:List[Tuple[str,str]])->Graph:
    graph = { x:[] for x,_ in type_list }

    for x,y in type_list:
        graph[x].append(y)
        
    add_keys = [y for x,y in type_list if y not in graph]

    for key in add_keys:
        graph[key] = []

    return graph

def any_cycles(graph:Graph)->Tuple[Tuple[str,str],List[str]]:
    d,f,time,stack,cycles = { x:0 for x in graph },{ x:0 for x in graph },[1], [], []
    for x in graph:
        if not d[x]:
            d[x] = time[0]; time[0]+=1
            topological_order(graph,x,d,f,time,stack,cycles)
            f[x] = time[0]; time[0]+=1
            stack.append(x)
    stack.reverse()
    return cycles, stack


def topological_order(graph, node, d, f, time, stack, cycles):

    for adj in graph[node]:
        if not d[adj]:
            d[adj] = time[0]; time[0]+=1
            topological_order(graph,adj,d,f,time,stack,cycles)
            f[adj] = time[0]; time[0]+=1
            stack.append(adj)
        elif not f[adj]:
            cycles.append((node,adj))

gr = build_graph_list([('a','b'), ('b','c')]) # a->b->c
gr = build_graph_list([('b','a'), ('c','b')]) # a<-b<-c
gr = build_graph_list([('b','a'), ('b','b')]) # a<-b<-c

cycles, sort = any_cycles(gr)

print(gr,cycles,sort)