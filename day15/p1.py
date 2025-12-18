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


data = open(input_path).read()
ans = sum(hash(word) for word in data.split(','))

print("Part 1:",ans)
