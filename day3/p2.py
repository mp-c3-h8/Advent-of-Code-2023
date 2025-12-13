import os.path
import re
from math import prod

dir_path = os.path.dirname(os.path.realpath(__file__))
input_path = os.path.join(dir_path, "input.txt")

data = open(input_path).read().splitlines()
grid = {(j, i): c for (j, line) in enumerate(data) for (i, c) in enumerate(list(line))}
dimy, dimx = len(data), len(data[0])


def digit_neighbors(y: int, x: int):
    for p in ((y-1, x-1), (y-1, x), (y-1, x+1), (y+1, x-1), (y+1, x), (y+1, x+1), (y, x-1), (y, x+1)):
        if p in grid and grid[p].isdigit():
            yield p


ans = 0
for y, line in enumerate(data):
    matches = re.finditer(r"\*{1}", line)
    for m in matches:
        numbers = set()
        for j, i in digit_neighbors(y, m.start()):
            xstart = xend = i
            while xstart > 0 and grid[(j, xstart-1)].isdigit():
                xstart -= 1
            while xend < dimx-1 and grid[(j, xend+1)].isdigit():
                xend += 1
            numbers.add((j, xstart, xend, int(data[j][xstart:xend+1])))
        if len(numbers) == 2:
            ans += prod(n for *_, n in numbers)


print("Part 2:", ans)
