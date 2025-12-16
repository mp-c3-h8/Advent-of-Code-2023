import os.path

dir_path = os.path.dirname(os.path.realpath(__file__))
input_path = os.path.join(dir_path, "input.txt")

data = open(input_path).read().splitlines()
history = [list(map(int, line.split())) for line in data]


def extrapolate(seq: list[int]) -> int:
    diffs = [seq[i+1]-seq[i] for i in range(len(seq)-1)]
    if all(d == 0 for d in diffs):
        return seq[-1]
    return seq[-1] + extrapolate(diffs)


extras = [extrapolate(hist) for hist in history]
print("Part 1:", sum(extras))
