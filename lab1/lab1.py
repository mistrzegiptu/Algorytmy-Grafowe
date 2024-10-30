from dimacs import *
from queue import PriorityQueue

source = 0
end = 1
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

file = "input/"
inputs = ["clique5", "clique20", "clique100", "clique1000", "g1", "grid5x5", "grid100x100", "path10", "path1000", "path10000", "pp10", "pp100", "pp1000", "rand20_100", "rand100_500", "rand1000_100000"]

for inputGraph in inputs:
    print(inputGraph)
    (V,L) = loadWeightedGraph(file+inputGraph)
    G = [[] for _ in range(V)]

    for u, v, c in L:
        u -= 1
        v -= 1
        G[u].append((v, c))
        G[v].append((u, c))

    result = Dijkstra(G)

    print(readSolution(file+inputGraph))
    assert int(readSolution(file+inputGraph))==result