import os.path
import re
from math import prod

dir_path = os.path.dirname(os.path.realpath(__file__))
input_path = os.path.join(dir_path, "input.txt")

data = open(input_path).read().splitlines()
colors = ["red", "green", "blue"]
max_count = [12, 13, 14]

p1 = p2 = 0
for i, line in enumerate(data, 1):
    *_, grabs = line.split(": ")
    possible = True
    rgb = [0, 0, 0]

    for grab in grabs.split(";"):
        for j, (color, mcount) in enumerate(zip(colors, max_count)):
            color_match = re.search(rf"\d+(?= {color})", grab)
            count = int(color_match.group(0)) if color_match else 0
            rgb[j] = max(rgb[j], count)
            if count > mcount:
                possible = False

    p1 += i if possible else 0
    p2 += prod(rgb)


print("Part 1:", p1)
print("Part 2:", p2)
