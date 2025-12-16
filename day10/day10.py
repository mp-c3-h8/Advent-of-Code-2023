import os.path
from itertools import pairwise

dir_path = os.path.dirname(os.path.realpath(__file__))
input_path = os.path.join(dir_path, "input.txt")

data = open(input_path).read().splitlines()
grid = {(j, i): c for j, row in enumerate(data) for i, c in enumerate(row)}  # (y,x)

NORTH = (-1, 0)
EAST = (0, 1)
SOUTH = (1, 0)
WEST = (0, -1)

# tile: list of from -> to
LOOKUP: dict[str, dict[tuple[int, int], tuple[int, int]]] = {
    '-': {WEST: WEST, EAST: EAST},
    '|': {NORTH: NORTH, SOUTH: SOUTH},
    'L': {SOUTH: EAST, WEST: NORTH},
    'J': {SOUTH: WEST, EAST: NORTH},
    '7': {EAST: SOUTH, NORTH: WEST},
    'F': {NORTH: EAST, WEST: SOUTH},
}

start_coord = (25, 77)
start_tile = '|'
start_direction = NORTH

coord = tuple(x+y for x, y in zip(start_coord, start_direction))
direction = start_direction
loop = [start_coord]

while ((c := grid[coord]) != 'S'):
    loop.append(coord)
    direction = LOOKUP[c][direction]
    coord = tuple(x+y for x, y in zip(coord, direction))

part1 = len(loop) // 2
print("Part 1:", part1)


# https://en.wikipedia.org/wiki/Shoelace_formula
# https://en.wikipedia.org/wiki/Pick's_theorem

area = sum((p1[0]+p2[0])*(p1[1]-p2[1]) for p1, p2 in pairwise(loop))
area //= 2

print("Part 2:", area+1-part1)
