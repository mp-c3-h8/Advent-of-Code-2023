import os.path

dir_path = os.path.dirname(os.path.realpath(__file__))
input_path = os.path.join(dir_path, "input.txt")

data = open(input_path).read().splitlines()
times, distances = [list(map(int, l[10:].split())) for l in data]

ans = 1
for t, d in zip(times, distances):
    traveled = [(t-hold)*hold for hold in range(1, t)]
    ans *= sum(t > d for t in traveled)

print("Part 1:", ans)
