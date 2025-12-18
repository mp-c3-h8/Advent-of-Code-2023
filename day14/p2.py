import os.path
from copy import deepcopy

type Matrix = list[list[str]]

dir_path = os.path.dirname(os.path.realpath(__file__))
input_path = os.path.join(dir_path, "input.txt")

data = open(input_path).read().splitlines()
platform = [list(l) for l in data]
dimy, dimx = len(platform), len(platform[0])


def get_load(matrix: Matrix) -> int:
    load = 0
    for j, row in enumerate(matrix):
        load += sum(len(matrix)-j for c in row if c == 'O')
    return load


def tilt_north(matrix: Matrix) -> Matrix:
    for x in range(len(matrix[0])):
        free = []
        for y in range(len(matrix)):
            val = matrix[y][x]
            match val:
                case '.':
                    free.append((y, x))
                case '#':
                    free = []
                case 'O':
                    if free:  # move it
                        free.append((y, x))
                        fy, fx = free.pop(0)
                        matrix[fy][fx] = 'O'
                        matrix[y][x] = '.'
    return matrix


def rot90(matrix: Matrix) -> Matrix:
    return list(map(list, zip(*matrix[::-1])))


def cycle(matrix: Matrix, n=1) -> Matrix:
    for _ in range(n):
        for __ in range(4):  # north, west, south,east
            matrix = tilt_north(matrix)
            matrix = rot90(matrix)
    return matrix


# find period
seen = {tuple(''.join(row) for row in platform)}
seen_list = [platform]
period_end = 0
for i in range(1, 1_000_000):
    platform = cycle(platform)
    search = tuple(''.join(row) for row in platform)
    if search in seen:
        period_end = i
        break
    seen.add(search)
    seen_list.append(deepcopy(platform))

period_start = seen_list.index(platform)
period = period_end-period_start
offset = (1_000_000_000-period_start) % period
final_platform = seen_list[period_start+offset]

print("Part 2:", get_load(final_platform))


# # let it settle
# SETTLE = 222
# platform = cycle(platform, SETTLE)

# # find period
# tilted = deepcopy(platform)
# period = 0
# while period < 1000:
#     tilted = cycle(tilted)
#     period += 1
#     if tilted == platform:
#         break

# # remaining cycles
# rem = (1_000_000_000 - SETTLE) % period
# tilted = cycle(platform, rem)

# print("Period:", period)
# print("Part 2:", get_load(tilted))
