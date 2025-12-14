import os.path

dir_path = os.path.dirname(os.path.realpath(__file__))
input_path = os.path.join(dir_path, "input.txt")

data = open(input_path).read()
seeds_data, maps_data = data.split("\n\n", 1)

seeds = [*map(int, seeds_data[6:].split())]
maps = [[*line.splitlines()[1:]] for line in maps_data.split("\n\n")]

for m in maps:
    for i, seed in enumerate(seeds):
        for row in m:
            d_start, s_start, l = map(int, row.split(" ", 2))
            if seed in range(s_start, s_start+l):
                seeds[i] += d_start - s_start
                break

print("Part 1:", min(seeds))
