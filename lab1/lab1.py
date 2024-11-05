from dimacs import *
from queue import PriorityQueue

source = 0
end = 1

class Node:
    def __init__(self, value):
        self.val = value
        self.parent = self
        self.rank = 0

def find(x):
    if x.parent != x:
        x.parent = find(x.parent)
    return x.parent
def union(x, y):
    x = find(x)
    y = find(y)

    if x == y:
        return
    if x.rank > y.rank:
        y.parent = x
    else:
        x.parent = y
        if x.rank == y.rank:
            y.rank += 1
def Dijkstra(G):
    Q = PriorityQueue()
    dist = [0] * len(G)
    dist[source] = float('inf')
    Q.put((-dist[source], source))

    while not Q.empty():
        currentWidth, u = Q.get()
        currentWidth = -currentWidth

        for v, c in G[u]:
            pathWidth = min(c, currentWidth)
            if pathWidth > dist[v]:
                dist[v] = pathWidth
                Q.put((-dist[v], v))

    #print(dist)
    return dist[end]

def DijkstraSolve(L, V):
    G = [[] for _ in range(V)]

    for u, v, c in L:
        u -= 1
        v -= 1
        G[u].append((v, c))
        G[v].append((u, c))

    return Dijkstra(G)

def UnionSolve(L, V):
    graphSet = [Node(i) for i in range(V)]
    L.sort(key=lambda x: -x[2])
    for u, v, c in L:
        union(graphSet[u-1], graphSet[v-1])

        if find(graphSet[source]) == find(graphSet[end]):
            return c

    return 0

file = "input/"
inputs = ["clique5", "clique20", "clique100", "clique1000", "g1", "grid5x5", "grid100x100", "path10", "path1000", "path10000", "pp10", "pp100", "pp1000", "rand20_100", "rand100_500", "rand1000_100000"]

for inputGraph in inputs:
    print(inputGraph)
    (V,L) = loadWeightedGraph(file+inputGraph)

    dijkstraRes = DijkstraSolve(L, V)
    unionSetRes = UnionSolve(L, V)



    print(readSolution(file+inputGraph))
    assert int(readSolution(file+inputGraph))==dijkstraRes
    assert int(readSolution(file+inputGraph))==unionSetRes