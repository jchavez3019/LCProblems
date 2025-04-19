import numpy as np
import heapq
from typing import List, Tuple, Optional, Union

inf = 10e6

GraphType = dict[str, dict[str, Union[List[str], int]]]

class Node:
    def __init__(self, prev: Optional[str], dest: str, dist: int):
        self.prev = prev
        self.dest = dest
        self.dist = dist

    def __lt__(self, other):
        # give priority to element with smaller min_dist
        return self.dist < other.dist

def create_graph(startGene: str, endGene: str, bank: List[str]) -> Tuple[GraphType, bool]:

    if endGene not in bank:
        return {}, False

    graph = {}  # hash elements by gene name for O(1) look-up speed

    # include the startGene into the graph
    bank.append(startGene)

    # create the graph
    for curr_gene in bank:
        destinations = []
        for other_gene in bank:
            if other_gene == curr_gene:
                continue

            num_diff = 0
            for c, oc in zip(curr_gene, other_gene):
                if c != oc:
                    num_diff += 1
                    if num_diff > 1:
                        break

            if num_diff == 1:
                destinations.append(other_gene)

        graph[curr_gene] = {
            'd': destinations,
            'min_dist': inf,
            'prev': None
        }

    return graph, True

def traverse_graph(graph: GraphType, startGene: str, endGene: str) -> Tuple[GraphType, int]:
    print(
        f"Traversing graph from {startGene} to {endGene}:"
    )

    min_heap = []
    heapq.heappush(min_heap, Node(None, startGene, 0))

    while len(min_heap) > 0:
        curr_node = heapq.heappop(min_heap)

        prev_gene, curr_gene, dist = curr_node.prev, curr_node.dest, curr_node.dist

        if dist < graph[curr_gene]['min_dist']:
            graph[curr_gene]['min_dist'] = dist
            graph[curr_gene]['prev'] = prev_gene

        new_dist = dist + 1
        for dest_gene in graph[curr_gene]['d']:
            if new_dist < graph[dest_gene]['min_dist']:
                heapq.heappush(min_heap, Node(curr_gene, dest_gene, new_dist))

    min_dist = graph[endGene]['min_dist']

    return graph, min_dist

def print_min_path(graph: GraphType, endGene: str):
    startNode = endGene

    path = []
    while startNode is not None:
        path.append(startNode)
        startNode = graph[startNode]['prev']

    path = path[::-1]
    print(f"Min path: {path}")

def solution(startGene: str, endGene: str, bank: List[str]) -> int:
    graph, endGeneExists = create_graph(startGene, endGene, bank)

    if not endGeneExists:
        return -1

    new_graph, min_dist = traverse_graph(graph, startGene, endGene)
    print(f"Min distance: {min_dist}")

    if min_dist == inf:
        # endGene was never reached
        return -1

    print_min_path(new_graph, endGene)

    return min_dist


def main():

    # startGene = "AACCGGTT"
    # endGene = "AACCGGTA"
    # bank = ["AACCGGTA"]

    startGene = "AACCGGTT"
    endGene = "AAACGGTA"
    bank = ["AACCGGTA","AACCGCTA","AAACGGTA"]

    ret = solution(startGene, endGene, bank)

    print(f"Solution returned: {ret}")


if __name__ == '__main__':
    main()