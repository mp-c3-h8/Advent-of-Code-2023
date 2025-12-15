import os.path
from collections import Counter
from operator import itemgetter

dir_path = os.path.dirname(os.path.realpath(__file__))
input_path = os.path.join(dir_path, "input.txt")


def get_type(hand: list[int]) -> int:
    counter = Counter(hand)
    _, n = counter.most_common(1)[0]
    match n:
        case 5:  # five of a kind
            return 7
        case 4:  # four of a kind
            return 6
        case 3:  # full house or three of a kind
            return 5 if len(counter) == 2 else 4
        case 2:  # two pair or one pair
            return 3 if len(counter) == 3 else 2
        case 1:  # high card
            return 1
        case _:
            return 0
    return 0


data = open(input_path).read().splitlines()
table = {'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}

hands: list[tuple[int, list[int], int]] = []  # (type,hand,bid)
for line in data:
    hand_str, bid_str = line.split(' ', 1)
    hand = [int(c) if c.isdigit() else table[c] for c in hand_str]
    hands.append((get_type(hand), hand, int(bid_str)))

ranked = sorted(hands, key=itemgetter(0, 1))
ans = sum(i*rank[2] for i, rank in enumerate(ranked, 1))
print("Part 1:", ans)
