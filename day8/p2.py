import os.path
from itertools import cycle
from math import lcm

dir_path = os.path.dirname(os.path.realpath(__file__))
input_path = os.path.join(dir_path, "input.txt")

dir_str, network_str = open(input_path).read().split("\n\n", 1)

directions = [0 if c == "L" else 1 for c in dir_str.strip()]
network = {line[:3]: (line[7:10], line[12:15]) for line in network_str.splitlines()}
curr = [node for node in network if node.endswith('A')]

moves = []
for c in curr:
    for i, direction in enumerate(cycle(directions)):
        if c.endswith('Z'):
            moves.append(i)
            break
        c = network[c][direction]

# use Least common multiple
print("Part 2:", lcm(*moves))
