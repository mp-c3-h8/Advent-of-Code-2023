import os.path
import re
from collections.abc import Iterator
from math import prod

dir_path = os.path.dirname(os.path.realpath(__file__))
input_path = os.path.join(dir_path, "input.txt")

data = open(input_path).read().splitlines()
grid = {(j, i): c for (j, line) in enumerate(data) for (i, c) in enumerate(list(line))}
dimy, dimx = len(data), len(data[0])


def digit_neighbors(y: int, x: int) -> Iterator[tuple[int, int]]:
    for p in ((y-1, x-1), (y-1, x), (y-1, x+1), (y+1, x-1), (y+1, x), (y+1, x+1), (y, x-1), (y, x+1)):
        if p in grid and grid[p].isdigit():
            yield p


def get_number(y: int, x: int) -> tuple[int, int, int, int]:
    xstart = xend = x
    while xstart > 0 and grid[(y, xstart-1)].isdigit():
        xstart -= 1
    while xend < dimx-1 and grid[(y, xend+1)].isdigit():
        xend += 1
    return (y, xstart, xend, int(data[y][xstart:xend+1]))


ans = 0
for j, line in enumerate(data):
    matches = re.finditer(r"\*{1}", line)
    for m in matches:
        numbers = set()
        for y, x in digit_neighbors(j, m.start()):
            numbers.add(get_number(y, x))
        if len(numbers) == 2:
            ans += prod(n for *_, n in numbers)

print("Part 2:", ans)
