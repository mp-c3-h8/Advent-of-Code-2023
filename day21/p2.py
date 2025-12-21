import os.path
from collections import deque, defaultdict

dir_path = os.path.dirname(os.path.realpath(__file__))
input_path = os.path.join(dir_path, "input.txt")

data = open(input_path).read().splitlines()
grid = {complex(i, j): c for j, row in enumerate(data) for i, c in enumerate(row)}
dimy, dimx = len(data), len(data[0])
start = [z for z in grid if grid[z] == 'S'][0]

STEPS = dimy
q = deque([(start, STEPS)])
seen: defaultdict[complex, int] = defaultdict(int)
while q:
    pos, steps_left = q.popleft()

    if pos in seen or steps_left < 0:
        continue
    seen[pos] = steps_left

    for d in (1, -1, 1j, -1j):
        new_pos = pos + d
        if new_pos in grid and grid[new_pos] != '#':
            q.append((new_pos, steps_left-1))

# adapted: https://github.com/villuna/aoc23/wiki/A-Geometric-solution-to-advent-of-code-2023,-day-21
# kudos
steps_to_edge = dimy // 2
n = int((26501365-steps_to_edge) / dimy)

odd_corners = sum((STEPS-s) > steps_to_edge and (STEPS-s) % 2 == 1 for s in seen.values())
even_corners = sum((STEPS-s) > steps_to_edge and (STEPS-s) % 2 == 0 for s in seen.values())

odd_full = sum((STEPS-s) % 2 == 1 for s in seen.values())
even_full = sum((STEPS-s) % 2 == 0 for s in seen.values())

ans = (n + 1) ** 2 * odd_full + n**2 * even_full - ((n+1) * odd_corners) + n * even_corners

print("Part 2:", ans)
