import numpy as np
from sortedcontainers import SortedDict, SortedList
from typing import List, Tuple, Optional, Union
from numpy import ndarray
import heapq

inf = 1e10

# INPUT_EXAMPLE = [[-1,-1,-1,-1,-1,-1],
#                  [-1,-1,-1,-1,-1,-1],
#                  [-1,-1,-1,-1,-1,-1],
#                  [-1,35,-1,-1,13,-1],
#                  [-1,-1,-1,-1,-1,-1],
#                  [-1,15,-1,-1,-1,-1]]

# INPUT_EXAMPLE = [[-1,7,-1],[-1,6,9],[-1,-1,2]]
INPUT_EXAMPLE = [[-1,1,2,-1],[2,13,15,-1],[-1,10,-1,-1],[-1,6,2,8]]

# class Node:
#     def __init__(self, board_range: Tuple[int, int]):
#         self.board_range = board_range
#         self.min_key = board_range[0]
#         self.max_key = board_range[1]
#         self.map = SortedDict()  # Ordered dictionary for fast lookups
#
#     def insert(self, key, value):
#         """Insert a key-value pair."""
#         self.map[key] = value
#
#     def lookup(self, query):
#         """Find the smallest key greater than query and return (key, value) or None."""
#         idx = self.map.bisect_right(query)  # Find the first key greater than query
#         if idx < len(self.map):  # If a valid key exists
#             next_key = self.map.iloc[idx]
#             return (next_key, self.map[next_key])
#         return None  # No key greater than query
#
#     def get_iter(self, query: int) -> Union[SortedList, iter]:
#         if query > self.max_key:
#             return iter([])
#         else:
#             return self.map.irange(query, self.max_key)
class Node:
    def __init__(self, prev: int, dest: int, dist: int, took_ladder: bool):
        self.prev = prev
        self.dest = dest
        self.dist = dist
        self.took_ladder = took_ladder

    def __lt__(self, other):
        # give priority to element with smaller min_dist
        return self.dist < other.dist


def create_graph(board: List[List[int]]) -> ndarray:
    orig_board_np = np.array(board)
    board_np = np.zeros_like(orig_board_np)
    board_np[::2] = orig_board_np[-1::-2]
    board_np[1::2] = orig_board_np[-2::-2][:, ::-1]
    print(f"board_np (shape {board_np.shape}): {board_np}")
    board_np = board_np.flatten().reshape(-1, 1)
    board_np = np.where(board_np != -1, board_np - 1, -1)

    # creates n x 2 array where first index is the position on the board,
    # and the second index is the minimum distance to get to this position
    board_np = np.concatenate((board_np,
                               np.full_like(board_np, inf),
                               -1*np.ones_like(board_np)), axis=1)
    print(f"new board_np shape: {board_np.shape}")
    return board_np

def get_min_dist(graph: ndarray) -> Tuple[int, ndarray]:
    heap = []
    heapq.heappush(heap, Node(-1, 0, 0, False))
    graph_len = graph.shape[0]

    while len(heap) > 0:
        curr_node = heapq.heappop(heap)
        prev, curr, dist, took_ladder = curr_node.prev, curr_node.dest, curr_node.dist, curr_node.took_ladder

        if curr == graph_len - 1:
            continue

        new_dist = dist + 1

        next_idx = min(curr + 6, graph_len - 1)
        if  (graph[curr, 0] == -1 or took_ladder) and new_dist < graph[next_idx, 1]:
            graph[next_idx, 1] = new_dist
            graph[next_idx, 2] = curr

            if graph[graph[next_idx, 0], 0] == -1:
                heapq.heappush(heap, Node(curr, next_idx, new_dist, False))
            else:
                graph[graph[next_idx, 0], 1] = new_dist
                graph[graph[next_idx, 0], 2] = next_idx
                heapq.heappush(heap, Node(curr, graph[next_idx, 0], new_dist, True))

        for i in range(curr + 1 if took_ladder else curr, min(curr + 6, graph_len)):


            if (graph[i, 0] != -1
                    and new_dist + 1 < graph[graph[i, 0], 1]):

                    # update stepping to get to this local node
                    graph[i, 1] = new_dist
                    graph[i, 2] = curr
                    # update to get to node at the end of ladder/snake
                    graph[graph[i, 0], 1] = new_dist
                    graph[graph[i, 0], 2] = i
                    heapq.heappush(heap, Node(i, graph[i, 0], new_dist, True))

    min_dist = graph[-1, 1]
    return min_dist, graph

def print_traversal(graph: ndarray):
    curr_idx = graph.shape[0] - 1
    path = []
    while curr_idx > 0:
        path.append(curr_idx)
        curr_idx = graph[curr_idx, 2]

    path = path[::-1]
    print(path)

def main():
    graph = create_graph(INPUT_EXAMPLE)
    for i in range(graph.shape[0]):
        print(f"{i} | {graph[i, 0]}")
    min_dist, new_graph = get_min_dist(graph)
    print(f"min_dist: {min_dist}")
    print("new_graph:")
    for i in range(new_graph.shape[0]):
        print(f"{i} | ({new_graph[i, 0]}, {new_graph[i, 1]}, {new_graph[i, 2]})")
    print_traversal(new_graph)

if __name__ == '__main__':
    main()