import os.path
import re

dir_path = os.path.dirname(os.path.realpath(__file__))
input_path = os.path.join(dir_path, "input.txt")

data = open(input_path).read().splitlines()
words = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]

ans = 0
for line in data:
    for n, w in enumerate(words, 1):
        # overlaps possible: one -> o1ne, two -> t2wo  etc
        rep = w[:len(w)//2] + str(n) + w[len(w)//2:]
        line = line.replace(w, rep)
    digits = re.findall(r"\d{1}", line)
    add = "".join((digits[0], digits[-1]))
    ans += int(add)

print("Part 2:", ans)
