import os.path
from dataclasses import dataclass, field
from cachetools import cached
from cachetools.keys import hashkey
import sys
sys.setrecursionlimit(100000)

type Position = complex

DIRS = {'<': -1, '>': 1, 'v': 1j, '^': -1j}


@dataclass(order=True)
class PrioNode:
    cost: int  # priority
    node: Position = field(compare=False)


dir_path = os.path.dirname(os.path.realpath(__file__))
input_path = os.path.join(dir_path, "input.txt")

data = open(input_path).read().splitlines()
grid = {complex(i, j): c for j, row in enumerate(data) for i, c in enumerate(row) if c != '#'}
dimy, dimx = len(data), len(data[0])


def valid_neighbors(pos: Position, path: set[Position]) -> list[tuple[Position, int]]:
    res = []
    for d in (1, -1, 1j, -1j):
        new_pos = pos + d
        off = 0
        if new_pos in grid:
            if grid[new_pos] in '<>^v':
                new_pos += DIRS[grid[new_pos]]
                off = 1
            if new_pos not in path:
                res.append((new_pos, off))
    return res


@cached(cache={}, key=lambda pos, dest, path, l: hashkey(pos, dest, l), info=True)
def dfs(pos: Position, dest: Position, path: set[Position], l: int) -> int:
    if pos in path:
        return 0
    if pos == dest:
        return l
    while len((nei := valid_neighbors(pos, path))) == 1:
        n, o = nei[0]
        pos = n
        path.add(pos)
        l += 1+o
    nei = valid_neighbors(pos, path)
    if len(nei) == 0:
        return 0
    return l+1 + max((dfs(n, dest, path | {pos}, o)) for n, o in nei)


source = 1
target = complex(dimx-2, dimy-1)

ans = dfs(source, target, set(), 1) - 1
print('Part 1:', ans)
