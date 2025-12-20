import os.path
from collections import deque

dir_path = os.path.dirname(os.path.realpath(__file__))
input_path = os.path.join(dir_path, "input.txt")

workflows_str, parts_str = open(input_path).read().split('\n\n')

workflows = {}
parts = []
q = deque()

for w_str in workflows_str.splitlines():
    name, rules_str = w_str.split('{')
    rules = []
    for rule_str in rules_str[:-1].split(','):
        if ':' in rule_str:  # 0: evaluate
            rules.append((0, list(rule_str.split(':'))))
        elif rule_str == 'A':  # 1: accept
            rules.append((1, 'A'))
        elif rule_str == 'R':  # 2: reject
            rules.append((2, 'R'))
        else:  # 3: send to workflow
            rules.append((3, rule_str))
    workflows[name] = rules

for i, p_str in enumerate(parts_str.splitlines()):
    vals = [*map(int, (v_str[2:] for v_str in p_str[1:-1].split(',')))]
    parts.append(vals)
    q.append((i, 'in'))

accepted = []
while q:
    pid, wid = q.pop()
    x, m, a, s = parts[pid]
    for rid, rule in workflows[wid]:
        if rid == 0 and not eval(rule[0]):
            continue
        match rid:
            case 0:  # eval is true
                _, action = rule
                match action:
                    case 'R':
                        pass
                    case 'A':
                        accepted.append(parts[pid])
                    case _:
                        q.append((pid, action))
            case 1:  # accept
                accepted.append(parts[pid])
            case 2:  # reject
                pass
            case 3:  # send to workflow
                q.append((pid, rule))
        break

print('Part 1:', sum(sum(part) for part in accepted))
