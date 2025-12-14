import os.path
from math import sqrt, ceil, floor

dir_path = os.path.dirname(os.path.realpath(__file__))
input_path = os.path.join(dir_path, "input.txt")

data = open(input_path).read().splitlines()
T, D = [int(l[10:].replace(" ", "")) for l in data]

# ans = 0
# for h in range(1, T):
#     traveled = (T-h)*h
#     if traveled > D:
#         ans += 1
# print("Part 2:", ans)

# solve Th - h*h - D = 0
part = sqrt(T*T/4-D)
h1 = T/2 - part
h2 = T/2 + part

print("Part 2:", floor(h2)-ceil(h1)+1)
