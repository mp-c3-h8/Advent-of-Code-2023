import os.path
from itertools import pairwise, zip_longest
import matplotlib.pyplot as plt

dir_path = os.path.dirname(os.path.realpath(__file__))
input_path = os.path.join(dir_path, "input.txt")

data = open(input_path).read().splitlines()
LOOKUP: dict[str, complex] = {'R': 1, 'L': -1, 'D': 1j, 'U': -1j}

polygon: list[complex] = [0]
pos: complex = 0
prev_direction = LOOKUP[data[-1][0]]/LOOKUP[data[0][0]]

for line, next_line in zip_longest(data, data[1:], fillvalue=data[0]):
    d, length, _ = line.split(' ', 2)
    next_d = next_line[0]

    direction = LOOKUP[d]/LOOKUP[next_d]  # left or right turn

    # TODO: why does this work?
    correction = 0
    if prev_direction == direction == -1j:  # right
        correction = 1
    if prev_direction == direction == 1j:  # left
        correction = -1

    prev_direction = direction
    pos += LOOKUP[d] * (int(length) + correction)
    polygon.append(pos)


# https://en.wikipedia.org/wiki/Shoelace_formula
area = sum((x.real*y.imag) - (y.real*x.imag) for x, y in pairwise(polygon))
area = int(area // 2)

print('Part 1:', area)
plt.plot([z.real for z in polygon], [-z.imag for z in polygon])
plt.gca().set_aspect("equal")
plt.show()
