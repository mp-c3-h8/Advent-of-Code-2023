import os.path
from itertools import pairwise

type Vec = tuple[int, int]

dir_path = os.path.dirname(os.path.realpath(__file__))
input_path = os.path.join(dir_path, "input.txt")

data = open(input_path).read().splitlines()
LOOKUP: dict[str, complex] = {
    'R': 1, 'L': -1, 'D': 1j, 'U': -1j,
    '0': 1, '2': -1, '1': 1j, '3': -1j
}
polygon: list[Vec] = [(0, 0)]
pos: Vec = (0, 0)

border = 0
for line in data:
    hexa_str = line.split(' ', 2)[-1]
    d, hexa = hexa_str[-2], hexa_str[2:7]
    length = int(hexa, 16)

    dz = LOOKUP[d]
    dy, dx = int(dz.imag), int(dz.real)
    px = dx * (length)
    py = dy * (length)
    pos = (pos[0]+py, pos[1]+px)
    border += length
    polygon.append(pos)


# https://en.wikipedia.org/wiki/Shoelace_formula
# https://en.wikipedia.org/wiki/Pick's_theorem
area = sum((x1*y2) - (x2*y1) for (y1, x1), (y2, x2) in pairwise(polygon)) / 2
internal = int(area - border/2 + 1)

print('Part 2:', internal + border)
