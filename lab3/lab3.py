from collections import deque
from queue import PriorityQueue

from dimacs import *

class Node:
    def __init__(self):
        self.edges = {}

    def addEdge(self, to, weight):
        self.edges[to] = self.edges.get(to, 0) + weight

    def delEdge(self, to):
        del self.edges[to]
def ReadToAdjList(L, V):
    G = [ Node() for i in range(V) ]

    for u, v, w in L:
        u -= 1
        v -= 1
        G[u].addEdge(v, w)
        G[v].addEdge(u, w)

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
            for v in G[u].edges:
                c = G[u].edges.get(v)
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
            for w in G[u].edges:
                c = G[u].edges.get(w)
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

def runEdmondsKarp(fileName):
    (V, L) = loadDirectedWeightedGraph(fileName)

    newG = [ Node() for i in range(V) ]

    for u, v, _ in L:
        u -= 1
        v -= 1
        newG[u].addEdge(v, 1)
        newG[v].addEdge(u, 1)

    min_cut = float('inf')
    for source in range(V):
        for end in range(source + 1, V):
            max_flow = EdmondsKarp(newG, source, end)
            min_cut = min(min_cut, max_flow)

    return min_cut

def mergeVertices(G, x, y):
    vertices = list(G[y].edges)

    for v in vertices:
        weight = G[y].edges.get(v)
        if v != x:
            G[x].addEdge(v, weight)
            G[v].addEdge(x, weight)
        G[v].delEdge(y)

    G[y].edges.clear()
    #del G[y]

def minimumCutPhase(G, n):
    a = 0
    S = []

    Q = PriorityQueue()
    values = {v: 0 for v in G}
    visited = {v: False for v in G}

    Q.put((0, a))

    while len(S) < n:
        c, v = Q.get()

        if visited[G[v]]:
            continue

        visited[G[v]] = True
        S.append(v)

        for w in G[v].edges:
            if not visited[G[w]]:
                cost = G[v].edges.get(w)
                values[G[w]] += cost
                Q.put((-values[G[w]], w))

    s = S[-2]
    t = S[-1]

    mergeVertices(G, s, t)

    return values[G[t]]

def StoerWagner(G):
    minCut = float('inf')
    n = len(G)

    while n > 1:
        minCut = min(minCut, minimumCutPhase(G, n))
        n = n - 1

    return minCut


inputs = ["clique5", "clique20", "clique100", "clique200", "cycle", "geo20_2b", "geo20_2c", "geo100_2a", "grid5x5", "grid100x100", "mc1", "mc2", "path", "rand20_100", "rand100_500", "simple", "trivial"]


for inputGraph in inputs:
    fileName = 'input/' + inputGraph
    print(inputGraph)

    (V,L) = loadWeightedGraph(fileName)
    G = ReadToAdjList(L, V)

    dupa = StoerWagner(G)
    print(dupa)
    assert dupa == int(readSolution(fileName))
    print(readSolution(fileName))
