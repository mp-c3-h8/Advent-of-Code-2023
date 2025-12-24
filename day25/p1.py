import os.path
import networkx as nx
from networkx.algorithms.connectivity import minimum_st_edge_cut
from networkx.algorithms.components import connected_components
from math import prod


dir_path = os.path.dirname(os.path.realpath(__file__))
input_path = os.path.join(dir_path, "input.txt")

data = open(input_path).read().splitlines()

G = nx.Graph()

for line in data:
    nodes = line.replace(':', '').split()
    G.add_nodes_from(nodes)
    G.add_edges_from((nodes[0], n) for n in nodes[1:])

nodes = list(G.nodes)
source = nodes[0]

for target in nodes[1:]:
    egde_cut = minimum_st_edge_cut(G, source, target)
    if len(egde_cut) == 3:
        G.remove_edges_from(egde_cut)
        break

components = [*connected_components(G)]
assert (len(components) == 2)

print("Part1:", prod(len(comp) for comp in components))
