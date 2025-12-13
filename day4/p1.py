import os.path

dir_path = os.path.dirname(os.path.realpath(__file__))
input_path = os.path.join(dir_path, "input.txt")

data = open(input_path).read().splitlines()

ans = 0
for line in data:
    _, cards = line.split(": ", 1)
    win, pick = cards.split(" | ")
    hits = set(win.split()).intersection(set(pick.split()))
    if hits:
        ans += 2**(len(hits)-1)

print("Part 1:", ans)
