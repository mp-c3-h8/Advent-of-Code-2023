import os.path
import matplotlib.pyplot as plt

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

ans = 1
x = [start_coord[1]]
y = [start_coord[0]]
while ((c := grid[coord]) != 'S'):
    x.append(coord[1])
    y.append(coord[0])
    direction = LOOKUP[c][direction]
    coord = tuple(x+y for x, y in zip(coord, direction))
    ans += 1

print("Part 1:", ans//2)
plt.plot(x, y)
plt.show()
