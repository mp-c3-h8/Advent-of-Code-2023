import os.path
import re
from itertools import combinations

dir_path = os.path.dirname(os.path.realpath(__file__))
input_path = os.path.join(dir_path, "input.txt")

data = open(input_path).read().splitlines()
unknown_regex = re.compile(r'\?{1}')
groups_regex = re.compile(r'#+')


def verify(springs: list[str], groups_target: list[int]) -> bool:
    springs_str = ''.join(springs)
    groups_matches = groups_regex.finditer(springs_str)
    groups = [m.end()-m.start() for m in groups_matches]
    return groups == groups_target


ans = 0
for line in data:
    springs_str, groups_str = line.split(' ', 1)
    groups = [*map(int, groups_str.split(','))]
    unknown_matches = unknown_regex.finditer(springs_str)
    unknown_positions = [m.start() for m in unknown_matches]
    k = sum(groups) - springs_str.count('#')  # n choose k
    springs = list(springs_str.replace('?', '.'))
    for comb in combinations(unknown_positions, k):
        arrangement = springs.copy()
        for i in comb:
            arrangement[i] = '#'
        if verify(arrangement, groups):
            ans += 1
print("Part 1:", ans)
