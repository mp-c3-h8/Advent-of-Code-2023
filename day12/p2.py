import os.path
import re
from functools import cache

dir_path = os.path.dirname(os.path.realpath(__file__))
input_path = os.path.join(dir_path, "input.txt")

data = open(input_path).read().splitlines()
groups_regex = re.compile(r'#+')
closed_groups_regex = re.compile(r'#+\.')

records: list[tuple[str, tuple[int, ...]]] = []
for line in data:
    springs_str, groups_str = line.split(' ', 1)
    record = ('?'.join([springs_str]*5), (*map(int, groups_str.split(',')),) * 5)
    records.append(record)


@cache
def count_arrangement(springs: str, groups: tuple[int, ...]) -> int:

    if springs.count('?') == 0:
        groups_matches = groups_regex.finditer(springs)
        final_groups = tuple(m.end()-m.start() for m in groups_matches)
        return groups == final_groups

    # every closed group (ending with .) left from first ? must be correct
    first_qu = springs.index('?')
    closed_groups_matches = closed_groups_regex.finditer(springs[:first_qu+1])
    closed_groups_ranges = [(m.start(), m.end()) for m in closed_groups_matches]
    closed_groups = [e-s-1 for s, e in closed_groups_ranges]

    if len(groups) < len(closed_groups) or any(x != y for x, y in zip(closed_groups, groups)):
        return 0

    # first closed groups correct, we cut them
    cut = 0 if not closed_groups else closed_groups_ranges[-1][1]
    new_groups = groups[len(closed_groups):]
    left = springs[cut:first_qu]
    right = springs[first_qu+1:]

    return sum(count_arrangement((left + x + right).strip('.'), new_groups) for x in '.#')


ans = 0
for springs, groups in records:
    ans += count_arrangement(springs.strip('.'), groups)

print("Part 2:", ans)