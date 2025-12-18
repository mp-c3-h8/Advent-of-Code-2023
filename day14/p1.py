import os.path

dir_path = os.path.dirname(os.path.realpath(__file__))
input_path = os.path.join(dir_path, "input.txt")

data = open(input_path).read().splitlines()
platform = [list(l) for l in data]
dimy, dimx = len(platform), len(platform[0])

load = 0
for x in range(dimx):
    free = []
    for y in range(dimy):
        val = platform[y][x]
        match val:
            case '.':
                free.append((y, x))
            case '#':
                free = []
            case 'O':
                dist = y
                if free:  # move it
                    free.append((y, x))
                    dist = free.pop(0)[0]
                load += dimy-dist

print("Part 1:", load)
