import os.path

dir_path = os.path.dirname(os.path.realpath(__file__))
input_path = os.path.join(dir_path, "input.txt")

data = open(input_path).read().splitlines()
count = [1] * len(data)

p1 = 0
for i, line in enumerate(data):
    _, cards = line.split(": ", 1)
    win, pick = cards.split(" | ")
    hits = set(win.split()).intersection(set(pick.split()))
    if hits:
        p1 += 2**(len(hits)-1)
    for j in range(1, len(hits)+1):
        count[i+j] += count[i]

print("Part 1:", p1)
print("Part 2:", sum(count))
