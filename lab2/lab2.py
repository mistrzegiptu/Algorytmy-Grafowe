from collections import deque

from dimacs import *
def ReadToAdjList(L, V):
    G = [[] for _ in range(V)]

    for u, v, w in L:
        u -= 1
        v -= 1
        G[u].append((v, w))
        G[v].append((u, 0))

    return G
def EdmondsKarp(G, source, end):
    n = len(G)
    flow = [[0]*n for _ in range(n)]
    maxFlow = 0

    while True:
        pred = [-1] * n
        pred[source] = source

        q = deque()
        q.append(source)

        while q and pred[end] == -1:
            u = q.popleft()
            for v, c in G[u]:
                if pred[v] == -1 and c > flow[u][v]:
                    pred[v] = u
                    q.append(v)
                    if v == end:
                        break

        if pred[end] == -1:
            break

        df = float('inf')
        v = end
        while v != source:
            u = pred[v]
            for w, c in G[u]:
                if w == v:
                    df = min(df, c - flow[u][v])
            v = u

        v = end
        while v != source:
            u = pred[v]
            flow[u][v] += df
            flow[v][u] -= df
            v = u

        maxFlow += df

    return maxFlow


inputsConn = ["clique5", "clique20", "clique100", "clique200", "cycle", "grid5x5", "grid100x100", "path", "rand20_100", "rand100_500", "simple"]
inputsFlow = ["clique5", "clique20", "clique100", "grid5x5", "grid100x100", "pp100", "rand20_100", "rand100_500", "simple", "simple2", "trivial", "trivial2", "worstcase"]

for inputGraph in inputsConn:
    fileName = 'input/connectivity/' + inputGraph
    print(inputGraph)

    (V,L) = loadDirectedWeightedGraph(fileName)
    G = ReadToAdjList(L, V)

    print(EdmondsKarp(G, 0, V-1))

    newG = [[] for _ in range(V)]
    for u, v, w in L:
        u -= 1
        v -= 1
        newG[u].append((v, 1))
        newG[v].append((u, 0))

    print("Number of edge disjoint paths: ")
    print(EdmondsKarp(newG, 0, V-1))
    print(readSolution(fileName))

for inputGraph in inputsFlow:
    fileName = 'input/flow/' + inputGraph
    print(inputGraph)

    (V,L) = loadDirectedWeightedGraph(fileName)
    G = ReadToAdjList(L, V)

    print(EdmondsKarp(G, 0, V-1))
    print(readSolution(fileName))
