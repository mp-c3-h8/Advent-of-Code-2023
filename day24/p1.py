import os.path
from dataclasses import dataclass
from itertools import combinations


@dataclass
class Line():
    a: int
    b: int
    c: int
    u: int
    v: int
    w: int

    def offset(self, o: int) -> None:
        self.a += o
        self.b += o
        self.c += o


dir_path = os.path.dirname(os.path.realpath(__file__))
input_path = os.path.join(dir_path, "input.txt")

data = open(input_path).read().splitlines()
lines: list[Line] = []

ML = 200000000000000
MR = 400000000000000
OFFSET = MR-ML
LB, UB = ML - OFFSET, MR-OFFSET
for row in data:
    pos, vel = row.split(' @ ')
    a, b, c = map(int, pos.split(','))
    u, v, w = map(int, vel.split(','))
    line = Line(a, b, c, u, v, w)
    line.offset(-OFFSET)
    lines.append(line)


ans = 0
for g, h in combinations(lines, 2):
    det = -g.u * h.v + g.v * h.u
    if det == 0:
        continue

    mx = h.a - g.a
    my = h.b - g.b
    r = 1/det * (-h.v * mx + h.u * my)
    s = 1/det * (-g.v * mx + g.u * my)

    if r <= 0 or s <= 0:
        continue

    x = g.a + r * g.u
    y = g.b + r * g.v

    if (x < LB or x > UB) or (y < LB or y > UB):
        continue

    ans += 1

print("Part 1:", ans)
