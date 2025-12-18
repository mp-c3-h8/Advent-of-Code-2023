import os.path
from itertools import pairwise

dir_path = os.path.dirname(os.path.realpath(__file__))
input_path = os.path.join(dir_path, "input.txt")

data = open(input_path).read()
patterns = [[list(l) for l in p.splitlines()] for p in data.split('\n\n')]

ans = 0
for pattern in patterns:
    for n, matrix in ((100, pattern), (1, [list(c) for c in zip(*pattern)])):
        candidates = [j for j, (r1, r2) in enumerate(pairwise(matrix), 1) if r1 == r2]

        # grow
        max_reflection = 0
        winner = 0
        for c in candidates:
            i = 0
            while c-1-i >= 0 and c+i < len(matrix) and matrix[c-1-i] == matrix[c+i]:
                i += 1
            if i >= max_reflection and (c-1-i == 0 or c+i == len(matrix))-1:
                max_reflection = i
                winner = c
        ans += n*winner

print(ans)
print("40050 not correct")
print("56679 too high")
print("41752 too high")
print("35614 too low")
