import os.path
import re
from collections import deque
from typing import Any
from math import prod

type Interval = range  # [a,b)
type Cube = list[range]  # n-cube: [a0,b0) x [a1,b1) x ...

INDICES = {'x': 0, 'm': 1, 'a': 2, 's': 3}

dir_path = os.path.dirname(os.path.realpath(__file__))
input_path = os.path.join(dir_path, "input.txt")
rule_regex = re.compile(r'(.+)(<|>)(\d+):(.+)')

workflows_str = open(input_path).read().split('\n\n')[0]
workflows: dict[str, list[tuple[int, Any]]] = {}

start_cube: Cube = [range(1, 4001) for _ in INDICES]
init: list[tuple[str, Cube]] = [('in', start_cube)]
q = deque(init)


def cut_range(r: range, val: int) -> tuple[range, range]:
    return (range(r.start, val), range(val, r.stop))


# return 2 cubes, such that expr is true for first cube, false for second cube
# example expr: x_3 > 10
def cut_cube(cube: Cube, dim: int, val: int, less: bool = True) -> tuple[Cube | None, Cube | None]:

    if dim > len(cube)-1:
        raise ValueError

    if not less:  # x > 5  <=>  x < 6  if  we switch output
        val += 1

    left, right = cut_range(cube[dim], val)
    cube_left = cube[:dim] + [left] + cube[dim+1:] if left else None
    cube_right = cube[:dim] + [right] + cube[dim+1:] if right else None

    return (cube_left, cube_right) if less else (cube_right, cube_left)


for w_str in workflows_str.splitlines():
    name, rules_str = w_str.split('{')
    rules = []
    for rule_str in rules_str[:-1].split(','):
        if ':' in rule_str:  # 0: evaluate
            rule_match = rule_regex.findall(rule_str)
            dim, less, val, action = rule_match[0]
            app = (INDICES[dim], less == '<', int(val), action)
            rules.append((0, app))
        elif rule_str == 'A':  # 1: accept
            rules.append((1, 'A'))
        elif rule_str == 'R':  # 2: reject
            rules.append((2, 'R'))
        else:  # 3: send to workflow
            rules.append((3, rule_str))
    workflows[name] = rules


accepted: list[Cube] = []
while q:
    workflow_id, cube = q.pop()
    for rule_id, rule in workflows[workflow_id]:
        match rule_id:
            case 0:
                dim, less, val, action = rule
                cube_true, cube_false = cut_cube(cube, dim, val, less)
                if cube_true:
                    match action:
                        case 'R':
                            pass
                        case 'A':
                            accepted.append(cube_true)
                        case _:
                            q.append((action, cube_true))
                if cube_false:  # continue workflow with whats left
                    cube = cube_false
                    continue
            case 1:  # accept
                accepted.append(cube)
            case 2:  # reject
                pass
            case 3:  # send to workflow
                q.append((rule, cube))
        break


vol = sum(prod(len(r) for r in cube) for cube in accepted)  # disjoint by construction
print('Part 2:', vol)
