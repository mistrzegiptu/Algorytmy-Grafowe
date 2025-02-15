from data import runtests
from collections import defaultdict
from collections import deque


class Node:
    def __init__(self, value):
        self.val = value
        self.parent = self
        self.rank = 0


def find(x):
    root = x
    while root.parent != root:
        root = root.parent

    while x.parent != root:
        parent = x.parent
        x.parent = root
        x = parent

    return root


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


def kruskal(N, streets, nodes):
    sortedEdges = sorted(streets, key = lambda x: x[2])

    mst = []

    for u, v, weight in sortedEdges:
        u, v = u-1, v-1
        rootU = find(nodes[u])
        rootV = find(nodes[v])

        if rootU != rootV:
            mst.append((u, v, weight))
            union(rootU, rootV)

    return mst


def BFS(G, castles):
    n = len(G)
    pq = deque()
    visited = [False] * n
    parent = [-1] * n
    start = list(castles)[0] - 1
    visited[start] = True
    pq.append(start)

    while pq:
        v = pq.popleft()

        for u in G[v].keys():
            if not visited[u]:
                visited[u] = True
                parent[u] = v
                pq.append(u)

    guarding = set()
    totalWeight = 0
    for castle in castles:
        v = castle - 1
        while v != -1 and v not in guarding:
            guarding.add(v)
            if parent[v] != -1:
                totalWeight += G[v][parent[v]]
            v = parent[v]

    return guarding, totalWeight


def lexBfs(G, start = 0):
  n = len(G)
  visited = []
  labels = [set() for _ in range(len(G))]
  partitions = [set()]

  for v in G:
    partitions[0].add(v.idx)

  partitions[0].remove(start)
  partitions.insert(0, {start})

  while partitions:
    while partitions and not partitions[0]:
      del partitions[0]

    if not partitions:
      break

    u = partitions[0].pop()
    visited.append(u)

    newPartitions = []
    for part in partitions:
      leftPartition = set()
      rightPartition = set()

      for v in part:
        if v in G[u].out:
          labels[v].add(u)
          leftPartition.add(v)
        else:
          rightPartition.add(v)

      if leftPartition:
        newPartitions.append(leftPartition)

      if rightPartition:
        newPartitions.append(rightPartition)

      partitions = newPartitions

  return visited


def my_solve(N, streets, lords):
    print(f"Place: {N}, ulice: {len(streets)}, lordowie: {len(lords)}")
    nodes = [Node(i) for i in range(N)]
    mst = kruskal(N, streets, nodes)

    G = [{} for i in range(N)]
    for a, b, t in mst:
        # a, b = a-1, b-1
        G[a][b] = t
        G[b][a] = t

    lordsGuarding = []
    for i in range(len(lords)):
        lord = lords[i]
        path, totalWeight = BFS(G, lord)
        lordsGuarding.append((path, totalWeight))

    n = len(lordsGuarding)
    conflictG = [{} for _ in range(n)]

    '''for i in range(n):
        for j in range(i, n):
            if lordsGuarding[i][0] & lordsGuarding[j][0]:
                G[i][j] = 0
                G[j][i] = 0'''
    return 0

runtests(my_solve)
