import os.path
import re

dir_path = os.path.dirname(os.path.realpath(__file__))
input_path = os.path.join(dir_path, "input.txt")

data = open(input_path).read().splitlines()
grid = {(j, i): c for (j, line) in enumerate(data) for (i, c) in enumerate(list(line))}
dimy, dimx = len(data), len(data[0])
test = re.compile(r"(\d|\.)")


def neighbors(y: int, start: int, end: int):
    if y > 0:
        for x in range(start-1, end+1):
            if x >= 0 and x < dimx:
                yield grid[(y-1, x)]
    if y < dimy-1:
        for x in range(start-1, end+1):
            if x >= 0 and x < dimx:
                yield grid[(y+1, x)]
    if start > 0:
        yield grid[(y, start-1)]
    if end < dimx:
        yield grid[(y, end)]


ans = 0
for y, line in enumerate(data):
    matches = re.finditer(r"\d+", line)
    for m in matches:
        for n in neighbors(y, m.start(), m.end()):
            if not test.match(n):
                ans += int(m.group(0))
                break

print("Part 1:", ans)
