import os.path
from operator import attrgetter
from dataclasses import dataclass, field
from heapq import heapify, heappush, heappop


dir_path = os.path.dirname(os.path.realpath(__file__))
input_path = os.path.join(dir_path, "input.txt")


@dataclass
class Brick:
    id: int
    x: range  # [xs,xe)
    y: range
    z: range
    supports: list[Brick] = field(default_factory=list)
    supported_by: list[Brick] = field(default_factory=list)

    def intersects_xy(self, other: Brick) -> bool:
        return self.intersects_range(self.x, other.x) and self.intersects_range(self.y, other.y)

    def intersects_range(self, a: range, b: range) -> bool:
        return max(a.start, b.start) < min(a.stop, b.stop)

    def fall(self, fall_height: int) -> None:
        self.z = range(self.z.start-fall_height, self.z.stop-fall_height)


data = open(input_path).read().splitlines()
bricks: list[Brick] = []

for i, line in enumerate(data):
    a, b = line.split('~')
    x1, y1, z1 = map(int, a.split(','))
    x2, y2, z2 = map(int, b.split(','))
    brick = Brick(i, range(x1, x2+1), range(y1, y2+1), range(z1, z2+1))
    bricks.append(brick)

bricks = sorted(bricks, key=attrgetter('z.start'))
done = []

for brick in bricks:
    # we only check vs done, because its ordered by z
    collision = [other for other in done if brick.intersects_xy(other)]
    done.append(brick)

    if not collision:  # falls onto ground or rests on ground
        if brick.z.start > 1:
            brick.fall(brick.z.start - 1)
        continue

    # can have multiple supports like a brick wall
    brick_max = max(collision, key=attrgetter('z.stop'))
    supports = [other for other in collision if other.z.stop == brick_max.z.stop]
    brick.supported_by = supports
    for supp in supports:
        supp.supports.append(brick)

    brick.fall(brick.z.start - brick_max.z.stop)


disintegrate = set(brick.id for brick in bricks
                   if (
                       all(len(supported.supported_by) > 1 for supported in brick.supports)
                   ))
print("Part 1:", len(disintegrate))


def chain_reaction(start: Brick) -> int:
    q = [(0, s.id, s,) for s in start.supports]
    heapify(q)  # prio = z-distance to start of reaction
    seen: set[int] = set()
    disintegrated: set[int] = set((start.id,))
    while q:
        _, _, brick = heappop(q)

        if brick.id in seen:
            continue
        seen.add(brick.id)

        remaining_support = set(b.id for b in brick.supported_by).difference(disintegrated)
        if remaining_support:
            continue

        disintegrated.add(brick.id)
        for supp in brick.supports:
            heappush(q, (supp.z.start-start.z.stop, supp.id, supp))

    return len(disintegrated) - 1


print("Part 2:", sum(chain_reaction(brick) for brick in bricks))
