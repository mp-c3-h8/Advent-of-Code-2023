import os.path
from itertools import cycle

dir_path = os.path.dirname(os.path.realpath(__file__))
input_path = os.path.join(dir_path, "input.txt")

dir_str, network_str = open(input_path).read().split("\n\n", 1)

directions = [0 if c == "L" else 1 for c in dir_str.strip()]
network = {line[:3]: (line[7:10], line[12:15]) for line in network_str.splitlines()}

curr = 'AAA'
for i, direction in enumerate(cycle(directions)):
    if curr == 'ZZZ':
        print("Part 1:", i)
        break
    curr = network[curr][direction]
