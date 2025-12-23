import os.path
import matplotlib.pyplot as plt
import numpy as np
from itertools import pairwise
import networkx as nx


type Node = complex
type Edge = tuple[Node, Node]


def neighbors(pos: Node) -> list[Node]:
    return [n for d in (1, -1, 1j, -1j) if (n := pos+d) in grid]


def is_branching(pos: Node) -> bool:
    return len(neighbors(pos)) > 2


def plot_maze(path=None) -> None:
    x = np.ones((dimx, dimy)) * 3
    for p in grid:
        x[int(p.imag), int(p.real)] = 1
    for p in graph:
        x[int(p.imag), int(p.real)] = 2.3

    if path:
        for p in path:
            x[int(p.imag), int(p.real)] = 2

    plt.imshow(x, cmap="Accent")
    plt.show()


dir_path = os.path.dirname(os.path.realpath(__file__))
input_path = os.path.join(dir_path, "input.txt")

data = open(input_path).read().splitlines()
grid = {complex(i, j): c for j, row in enumerate(data) for i, c in enumerate(row) if c != '#'}
dimy, dimx = len(data), len(data[0])

source = 1
target = complex(dimx-2, dimy-1)

# collapse to branching paths
graph: dict[Node, list[Node]] = {p: [] for p in grid if is_branching(p)}
graph.update({source: [], target: []})
weights: dict[Edge, int] = {}

seen = set()
for node in graph:  # floodfill to get edge weights
    starts = neighbors(node)
    if not starts:
        continue
    for start in starts:
        if start in seen:
            continue
        i = 1
        old = node
        while start not in graph:
            i += 1
            new = neighbors(start)
            new.remove(old)
            assert (len(new) == 1)
            old = start
            start = new[0]
        seen.add(old)
        # print(node, start,i)
        graph[node].append(start)
        graph[start].append(node)
        weights[(node, start)] = i
        weights[(start, node)] = i


G = nx.DiGraph()
G.add_nodes_from(g for g in graph)
for (u, v), w in weights.items():
    G.add_edge(u, v, weight=w)

ml = 0
mpath = []

for path in nx.all_simple_paths(G, source=source, target=target):
    l = sum(weights[u, v] for u, v in pairwise(path))
    if l > ml:
        ml = l
        mpath = path

print(ml)
