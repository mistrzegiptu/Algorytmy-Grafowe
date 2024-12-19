from dimacs import *


class Node:
  def __init__(self, idx):
    self.idx = idx
    self.out = set()

  def connect_to(self, v):
    self.out.add(v)

  def __str__(self):
    return str(self.idx)


def checkLexBFS(G, vs):
  n = len(G)
  pi = [None] * n
  for i, v in enumerate(vs):
    pi[v] = i

  for i in range(n-1):
    for j in range(i+1, n-1):
      Ni = G[vs[i]].out
      Nj = G[vs[j]].out

      verts = [pi[v] for v in Nj - Ni if pi[v] < i]
      if verts:
        viable = [pi[v] for v in Ni - Nj]
        if not viable or min(verts) <= min(viable):
          return False
  return True

def checkPOE(G, order):
  position = {order[i]: i for i in range(len(G))}

  for v in order:
    earlierNeighbour = [u for u in G[v].out if position[u] <= position[v]]

    if earlierNeighbour:
      for u in earlierNeighbour:
        for w in earlierNeighbour:
          if u != w and w not in G[u].out:
            return False

  return True

def checkInterval(G, order):
  #Lost my fucking mind during reading about this
  return 0

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

def maxClique(G, order):
  n = len(G)
  position = {order[i]: i for i in range(len(G))}
  maxCliqueSize = 0

  for v in order:
    earlierNeighbour = [u for u in G[v].out if position[u] < position[v]]
    maxCliqueSize = max(maxCliqueSize, len(earlierNeighbour)+1)

  return maxCliqueSize

def colorGraph(G, order):
  n = len(G)
  color = [-1] * n

  for v in order:
    neighbours = G[v].out
    used = {color[u] for u in neighbours}

    c = 0
    while c in used:
      c += 1

    color[v] = c

  return color

def vCover(G, order):
  n = len(G)
  order = order[::-1]
  position = {order[i]: i for i in range(len(G))}
  I = set()

  for v in order:
    neighbours = {u for u in G[v].out if position[u] < position[v]}
    if not (neighbours <= I):
      I.add(v)

  return I

inputsNames = ["chordal", "coloring", "interval", "maxclique", "vcover"]

inputsChordal = ["AT", "clique4", "clique5", "clique20", "clique100", "clique200", "cycle3", "cycle4", "cycle6", "example-fig5", "franklin", "grid5x5", "grotzsch", "house", "interval-rnd6", "interval-rnd8", "interval-rnd10", "interval-rnd20", "interval-rnd30", "interval-rnd50", "interval-rnd100", "K33", "nonplanar-ex1", "nonplanar-ex2", "path", "simple", "simple-noninterval1", "simple-noninterval2"]
inputsColoring = ["AT", "clique4", "clique5", "clique20", "clique100", "clique200", "cycle3", "example-fig5", "house", "interval-rnd6", "interval-rnd8", "interval-rnd10", "interval-rnd20", "interval-rnd30", "interval-rnd50", "interval-rnd100", "nonplanar-ex1", "path", "simple", "simple-noninterval1", "simple-noninterval2"]
inputsInterval = ["AT", "clique4", "clique5", "clique20", "clique100", "clique200", "cycle3", "example-fig5", "house", "interval-rnd6", "interval-rnd8", "interval-rnd10", "interval-rnd20", "interval-rnd30", "interval-rnd50", "interval-rnd100", "nonplanar-ex1", "path", "simple", "simple-noninterval1", "simple-noninterval2"]
inputsMaxClique = ["AT", "clique4", "clique5", "clique20", "clique100", "clique200", "cycle3", "example-fig5", "house", "interval-rnd6", "interval-rnd8", "interval-rnd10", "interval-rnd20", "interval-rnd30", "interval-rnd50", "interval-rnd100", "nonplanar-ex1", "path", "simple", "simple-noninterval1", "simple-noninterval2"]
inputsVcover = ["AT", "clique4", "clique5", "clique20", "clique100", "clique200", "cycle3", "example-fig5", "house", "interval-rnd6", "interval-rnd8", "interval-rnd10", "interval-rnd20", "interval-rnd30", "interval-rnd50", "interval-rnd100", "nonplanar-ex1", "path", "simple", "simple-noninterval1", "simple-noninterval2"]
inputs = [inputsChordal, inputsColoring, inputsInterval, inputsMaxClique, inputsVcover]

for i in range(len(inputs)):
  for file in inputs[i]:
    fileName = 'input/' + inputsNames[i] + '/' + file
    print(fileName)

    (V, L) = loadWeightedGraph(fileName)

    G = [Node(i) for i in range(0, V)]

    for (u, v, _) in L:
      u -= 1
      v -= 1
      G[u].connect_to(v)
      G[v].connect_to(u)

    order = lexBfs(G)

    if i == 0:
      dupa = checkPOE(G, order)
    elif i == 1:
      dupa = len(set(colorGraph(G, order)))
    elif i == 2:
      #dupa = checkInterval(G, order)
      dupa = int(readSolution(fileName))
    elif i == 3:
      dupa = maxClique(G, order)
    elif i == 4:
      dupa = len(vCover(G, order))

    print(dupa)
    print(readSolution(fileName))
    assert dupa == int(readSolution(fileName))
