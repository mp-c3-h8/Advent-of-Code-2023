import os.path
import re

dir_path = os.path.dirname(os.path.realpath(__file__))
input_path = os.path.join(dir_path, "input.txt")

data = open(input_path).read().splitlines()

ans = 0
for line in data:
    digits = re.findall(r"\d{1}", line)
    add = "".join((digits[0], digits[-1]))
    ans += int(add)

print("Part 1:", ans)
