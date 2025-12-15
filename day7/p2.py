import os.path
from collections import Counter
from operator import itemgetter

dir_path = os.path.dirname(os.path.realpath(__file__))
input_path = os.path.join(dir_path, "input.txt")

FIVE_OF_A_KIND = 7
FOUR_OF_A_KIND = 6
FULL_HOUSE = 5
THREE_OF_A_KIND = 4
TWO_PAIR = 3
ONE_PAIR = 2
HIGH_CARD = 1


def get_type(hand: list[int]) -> int:
    counter = Counter(hand)
    m = counter.pop(1) if 1 in counter else 0  # number of jokers
    n = most[0][1] if (most := counter.most_common(1)) else 0
    n = max(m, n+m)

    match n:
        case 5:
            return FIVE_OF_A_KIND
        case 4:
            return FOUR_OF_A_KIND
        case 3:
            return FULL_HOUSE if len(counter) == 2 else THREE_OF_A_KIND
        case 2:
            return TWO_PAIR if len(counter) == 3 else ONE_PAIR
        case 1:
            return HIGH_CARD
        case _:
            return 0
    return 0


data = open(input_path).read().splitlines()
table = {'T': 10, 'J': 1, 'Q': 12, 'K': 13, 'A': 14}

hands: list[tuple[int, list[int], int]] = []  # (type,hand,bid)
for line in data:
    hand_str, bid_str = line.split(' ', 1)
    hand = [int(c) if c.isdigit() else table[c] for c in hand_str]
    hands.append((get_type(hand), hand, int(bid_str)))

ranked = sorted(hands, key=itemgetter(0, 1))
ans = sum(i*rank[2] for i, rank in enumerate(ranked, 1))
print("Part 2:", ans)
