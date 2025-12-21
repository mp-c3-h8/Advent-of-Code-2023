import os.path
from collections import deque, defaultdict

dir_path = os.path.dirname(os.path.realpath(__file__))
input_path = os.path.join(dir_path, "input.txt")

data = open(input_path).read().splitlines()
grid = {complex(i, j): c for j, row in enumerate(data) for i, c in enumerate(row)}
start = [z for z in grid if grid[z] == 'S'][0]

STEPS = 64
rem = STEPS % 2
q = deque([(start, STEPS)])
seen: defaultdict[complex, int] = defaultdict(int)
i = 0
while q:
    i += 1
    pos, steps_left = q.popleft()

    if pos in seen or steps_left < 0:
        continue
    seen[pos] = steps_left

    for d in (1, -1, 1j, -1j):
        new_pos = pos + d
        if new_pos in grid and grid[new_pos] != '#':
            q.append((new_pos, steps_left-1))

print("Part 1:", sum(s % 2 == rem or s == 0 for p, s in seen.items()))
