import os.path

dir_path = os.path.dirname(os.path.realpath(__file__))
input_path = os.path.join(dir_path, "input.txt")


def hash(word: str) -> int:
    res = 0
    for c in word:
        res += ord(c)
        res *= 17
        res %= 256
    return res


steps = [w for w in open(input_path).read().split(',')]
# dicts retain insertion order
boxes: list[dict[str, int]] = [dict() for _ in range(256)]

for step in steps:
    if step.endswith('-'):
        label = step[:-1]
        boxes[hash(label)].pop(label, None)
    else:
        label, focal = step.split('=', 1)
        boxes[hash(label)][label] = int(focal)

ans = sum(i*j*focal for i, box in enumerate(boxes, 1) for j, focal in enumerate(box.values(), 1))
print("Part 2:", ans)
