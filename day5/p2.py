import os.path
from itertools import batched

dir_path = os.path.dirname(os.path.realpath(__file__))
input_path = os.path.join(dir_path, "input.txt")


# intersect [a,b] and [c,d]
def intersect_intervals(i1: tuple[int, int], i2: tuple[int, int]) -> tuple[int, int] | None:
    a, b = i1
    c, d = i2
    il, ir = max(a, c), min(b, d)
    if il > ir:
        return None
    return (il, ir)


# calc [a,b] \ [c,d]
def difference_intervals(i1: tuple[int, int], i2: tuple[int, int]) -> list[tuple[int, int]]:
    a, b, c, d = i1 + i2
    res = []
    if d < a or b < c:  # no change
        return [(a, b)]
    if a < c:
        res.append((a, c-1))
    if d < b:
        res.append((d+1, b))
    return res


data = open(input_path).read()
seeds_data, maps_data = data.split("\n\n", 1)

seeds = [*map(int, seeds_data[6:].split())]
maps = [[*line.splitlines()[1:]] for line in maps_data.split("\n\n")]
seed_ranges = [(a, a+b-1) for a, b in batched(seeds, 2)]


for m in maps:
    for seed_interval in seed_ranges.copy():
        new = []
        for row in m:
            d_start, s_start, l = map(int, row.split(" ", 2))
            source_interval = (s_start, s_start+l-1)
            isect = intersect_intervals(seed_interval, source_interval)
            if not isect:
                continue
            shifted_interval = (isect[0] + d_start - s_start, isect[1] + d_start - s_start)
            new.append(shifted_interval)
            diff = difference_intervals(seed_interval, isect)
            if len(diff) == 1:  # no change
                continue
            seed_ranges.extend(diff)
        if new:
            seed_ranges.remove(seed_interval)
        seed_ranges.extend(new)

print("Part 2:", min(a for a, b in seed_ranges))
