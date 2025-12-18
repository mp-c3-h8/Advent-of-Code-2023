import os.path

type Vec = tuple[int, int]  # (y,x)

dir_path = os.path.dirname(os.path.realpath(__file__))
input_path = os.path.join(dir_path, "input.txt")

data = open(input_path).read().splitlines()
grid = {(j, i): c for j, row in enumerate(data) for i, c in enumerate(row)}  # (y,x)
dimy, dimx = len(data), len(data[0])

NORTH = (-1, 0)
EAST = (0, 1)
SOUTH = (1, 0)
WEST = (0, -1)

# list of from -> to
LOOKUP: dict[str, dict[Vec, list[Vec]]] = {
    '.': {
        NORTH: [NORTH],
        EAST: [EAST],
        SOUTH: [SOUTH],
        WEST: [WEST]
    },
    '/': {
        NORTH: [EAST],
        EAST: [NORTH],
        SOUTH: [WEST],
        WEST: [SOUTH]
    },
    '\\': {
        NORTH: [WEST],
        EAST: [SOUTH],
        SOUTH: [EAST],
        WEST: [NORTH]
    },
    '|': {
        NORTH: [NORTH],
        EAST: [NORTH, SOUTH],
        SOUTH: [SOUTH],
        WEST: [NORTH, SOUTH]
    },
    '-': {
        NORTH: [EAST, WEST],
        EAST: [EAST],
        SOUTH: [EAST, WEST],
        WEST: [WEST]
    }
}


def energize(pos: Vec, d: Vec) -> int:

    seen: set[tuple[Vec, Vec]] = set()

    def move(pos: Vec, d: Vec) -> None:
        while pos in grid and (pos, d) not in seen:
            c = grid[pos]
            seen.add((pos, d))
            if c == '.':
                pos = (pos[0]+d[0], pos[1]+d[1])
                continue

            new_d = LOOKUP[c][d]
            if len(new_d) == 1:
                n = new_d[0]
                pos = (pos[0]+n[0], pos[1]+n[1])
                d = n
                continue

            for n in new_d:
                move((pos[0]+n[0], pos[1]+n[1]), n)

    move(pos, d)
    energized = set(p for p, d in seen)
    return len(energized)


ans = 0
for x in range(dimx):
    res = energize((0, x), SOUTH)
    res2 = energize((dimy-1, x), NORTH)
    ans = max(ans, res, res2)
for y in range(dimy):
    res = energize((y, 0), EAST)
    res2 = energize((y, dimx-1), WEST)
    ans = max(ans, res, res2)
print("Part 2:", ans)
