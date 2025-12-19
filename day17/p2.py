import os.path
from heapq import heapify, heappush, heappop
from dataclasses import dataclass, field

type Position = complex
type Direction = complex
type Node = tuple[Position, Direction, int]  # int: number straight steps


@dataclass(order=True)
class PriorityNode:
    cost: int  # priority
    node: Node = field(compare=False)


dir_path = os.path.dirname(os.path.realpath(__file__))
input_path = os.path.join(dir_path, "input.txt")

data = open(input_path).read().splitlines()
grid = {complex(i, j): int(c) for j, row in enumerate(data) for i, c in enumerate(row)}
dimy, dimx = len(data), len(data[0])


def valid_neighbors(node: Node, min_steps: int, max_steps: int) -> list[Node]:
    pos, d, s = node
    res = []
    if (left := pos + d*1j) in grid and s >= min_steps:
        res.append((left, d*1j, 1))
    if (right := pos - d*1j) in grid and s >= min_steps:
        res.append((right, -d*1j, 1))
    if (straight := pos + d) in grid and s < max_steps:
        res.append((straight, d, s+1))
    return res


# modified dijkstra
def dijkstra(source: Position, dest: Position, min_steps: int = 1, max_steps: int = 3) -> int:
    shortest_paths: dict[Node, int] = {}
    done: set[Node] = set()

    # init q
    q: list[PriorityNode] = [PriorityNode(0, (source, 1, 0)), PriorityNode(0, (source, 1j, 0))]
    heapify(q)

    while q:
        pnode = heappop(q)
        cost, node = pnode.cost, pnode.node

        if node[0] == dest and node[2] >= min_steps:
            return cost

        if node in done:
            continue
        done.add(node)

        for new_node in valid_neighbors(node, min_steps, max_steps):  # update valid neighbor
            new_pos = new_node[0]
            new_cost = cost + grid[new_pos]
            if new_node in shortest_paths and shortest_paths[new_node] <= new_cost:
                continue
            shortest_paths[new_node] = new_cost
            heappush(q, PriorityNode(new_cost, new_node))

    return -1


source = complex(0, 0)
dest = complex(dimx-1, dimy-1)
ans = dijkstra(source, dest, 4, 10)
print('Part 2:', ans)
