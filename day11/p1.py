import os.path
from collections import defaultdict
from itertools import combinations

dir_path = os.path.dirname(os.path.realpath(__file__))
input_path = os.path.join(dir_path, "input.txt")

data = open(input_path).read().splitlines()
dimy, dimx = len(data), len(data[0])

hor_expansion = 0
planets_by_x: defaultdict[int, list[int]] = defaultdict(list)
empty_columns = [1] * dimx
for y, row in enumerate(data):
    is_empty = True
    for x, c in enumerate(list(row)):
        if c == '#':
            is_empty = False
            empty_columns[x] = 0
            planets_by_x[x].append(y+hor_expansion)
    if is_empty:
        hor_expansion += 1

planets: list[tuple[int, int]] = []
ver_expansion = 0
for x in range(dimx):
    ver_expansion += empty_columns.pop(0)
    for y in planets_by_x[x]:
        planets.append((y, x+ver_expansion))

ans = 0
for (y1, x1), (y2, x2) in combinations(planets, 2):
    ans += abs(y2-y1) + abs(x2-x1)

print("Part 1:", ans)
