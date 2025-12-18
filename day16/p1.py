import os.path

type Vec = tuple[int, int]

dir_path = os.path.dirname(os.path.realpath(__file__))
input_path = os.path.join(dir_path, "input.txt")

data = open(input_path).read().splitlines()
grid = {(j, i): c for j, row in enumerate(data) for i, c in enumerate(row)}  # (y,x)

NORTH = (-1, 0)
EAST = (0, 1)
SOUTH = (1, 0)
WEST = (0, -1)

# list of from -> to
LOOKUP: dict[str, dict[tuple[int, int], list[tuple[int, int]]]] = {
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

energized: set[Vec] = set()
seen: set[tuple[Vec, Vec]] = set()


def move(pos: Vec, d: Vec) -> None:
    while pos in grid and (pos, d) not in seen:
        c = grid[pos]
        energized.add(pos)
        seen.add((pos, d))
        if c == '.':
            pos = (pos[0]+d[0], pos[1]+d[1])
            continue

        new_d = LOOKUP[c][d]
        if len(new_d) > 1:
            for n in new_d:
                move((pos[0]+n[0], pos[1]+n[1]), n)
        else:
            n = new_d[0]
            pos = (pos[0]+n[0], pos[1]+n[1])
            d = n


move((0, 0), EAST)
print("Part 1:", len(energized))
